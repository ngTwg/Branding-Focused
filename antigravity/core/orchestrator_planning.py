"""
Orchestrator Planning Module — Task Planning and Repair for v6.5.0-SLIM.
"""

from __future__ import annotations
import logging
import os
import re
from typing import Optional, TYPE_CHECKING, List
from pydantic import BaseModel

if TYPE_CHECKING:
    from antigravity.core.schemas import PlanStep, TaskCompletionSpec, Skill, ExecutionPlan, RouteDecision, ErrorDelta
    from antigravity.core.skill_store import SkillStore
    from antigravity.core.llm_client import LLMClient
    from antigravity.core.budget_guard import BudgetGuard
    from antigravity.core.budget_strategy import BudgetStrategy
    from antigravity.core.ast_analyzer import ASTAnalyzer
    from antigravity.core.failure_memory import FailureMemory

logger = logging.getLogger(__name__)

class PlanningModule:
    """
    Handles planning, task breakdown, and repair strategies for AntigravityOrchestrator.
    """
    
    def __init__(
        self, 
        skill_store: Optional[SkillStore] = None,
        llm: Optional[LLMClient] = None,
        budget_guard: Optional[BudgetGuard] = None,
        budget_strategy: Optional[BudgetStrategy] = None,
        ast_analyzer: Optional[ASTAnalyzer] = None,
        failure_memory: Optional[FailureMemory] = None
    ):
        self.skill_store = skill_store
        self.llm = llm
        self.budget_guard = budget_guard
        self.budget_strategy = budget_strategy
        self.ast_analyzer = ast_analyzer
        self.failure_memory = failure_memory

    def _build_skill_injector(self, skills: List['Skill'], repair_mode: bool = False) -> str:
        if not skills:
            return ""

        header = "[SKILL MEMORY MATCHES - APPLY IN ORDER]"
        if repair_mode:
            header = "[CRITICAL REPAIR SKILLS - APPLY IN ORDER]"

        lines = [header]
        for idx, skill in enumerate(skills[:3], start=1):
            lines.append(
                f"{idx}. Name: {skill.name} | Blueprint: {skill.plan_template} | Success: {skill.success_criteria}"
            )

        return "\n" + "\n".join(lines) + "\n"

    def _retrieve_ranked_skills(
        self,
        task_description: str,
        route: Optional['RouteDecision'] = None,
        errors: Optional[List[str]] = None,
        top_k: int = 3,
    ) -> List['Skill']:
        if not self.skill_store:
            return []

        try:
            if hasattr(self.skill_store, "retrieve_many"):
                return self.skill_store.retrieve_many(
                    task=task_description,
                    errors=errors,
                    top_k=top_k,
                    candidate_skills=route.candidate_skills if route else None,
                    domain_hint=route.domain if route else None,
                )

            # Backward compatibility for old SkillStore interface.
            single = self.skill_store.retrieve(task_description, errors)
            return [single] if single else []
        except Exception as e:
            logger.warning(f"Skill retrieval failed: {e}")
            return []

    def plan_execution(self, task_description: str, route: 'RouteDecision', span: any) -> 'ExecutionPlan':
        """
        Generate execution plan with budget-aware retrieval and prompt optimization.
        """
        from antigravity.core.schemas import ExecutionPlan
        
        # v6.2: Get current budget strategy
        remaining_ratio = self.budget_guard.remaining_ratio if self.budget_guard else 1.0
        current_zone = self.budget_strategy.get_current_zone(remaining_ratio) if self.budget_strategy else None
        strategy_config = self.budget_strategy.get_strategy(current_zone) if self.budget_strategy else None
        
        # Planner Augmentation: ranked multi-skill retrieval.
        ranked_skills = self._retrieve_ranked_skills(
            task_description=task_description,
            route=route,
            top_k=3,
        )
        skill_injector = ""
        if ranked_skills and (strategy_config is None or strategy_config.use_expansion):
            skill_injector = self._build_skill_injector(ranked_skills)
            span.update(skill_matches=[skill.name for skill in ranked_skills])

        # v6.2: Adapt prompt based on strategy mode
        prompt_mode = strategy_config.prompt_mode if strategy_config else "full"
        if prompt_mode == "full":
            system_prompt = f'''You are the Lead Execution Planner. 
Break down the task into minimal executable steps AND define strict deterministic completion criteria.
Domain={route.domain}, Intent={route.intent}.
{skill_injector}'''
        elif prompt_mode == "short":
            system_prompt = f'''Lead Execution Planner. Break task into steps.
Domain={route.domain}, Intent={route.intent}.
{skill_injector}'''
        else:
            system_prompt = f'''Plan steps for: {route.domain}/{route.intent}.'''

        messages = [{"role": "user", "content": f"User Request: {task_description}"}]
        
        if self.llm:
            try:
                return self.llm.generate_structured(
                    task_name="planner_primary",
                    model=os.getenv("AG_LLM_MODEL", "gemini-2.5-flash"),
                    system=system_prompt,
                    messages=messages,
                    response_model=ExecutionPlan
                )
            except Exception as e:
                logger.warning(f"Planning failed: {e}")
                span.log_error(str(e))
                
        return self._deterministic_planner_fallback(task_description, Exception("All planning failed"), route.domain)

    def replan_repair(self, task_description: str, failed_plan: 'ExecutionPlan', error_delta: 'ErrorDelta', span: any) -> 'ExecutionPlan':
        """
        Generate repair plan using context from ErrorDelta, ASTAnalyzer, and FailureMemory.
        """
        from antigravity.core.schemas import ExecutionPlan, PlanStep
        
        # v6.2: Check if repair is enabled in current budget zone
        remaining_ratio = self.budget_guard.remaining_ratio if self.budget_guard else 1.0
        current_zone = self.budget_strategy.get_current_zone(remaining_ratio) if self.budget_strategy else None
        strategy_config = self.budget_strategy.get_strategy(current_zone) if self.budget_strategy else None
        
        if strategy_config and not strategy_config.enable_repair:
            logger.warning(f"[BUDGET] Repair disabled in {current_zone} zone")
            return ExecutionPlan(
                objective=f"Repair disabled in {current_zone} zone",
                steps=[],
                completion_criteria=failed_plan.completion_criteria,
                risk_flags=[f"Repair disabled due to budget constraints ({current_zone} zone)"]
            )
        
        # Repair Macro Retrieval (ranked)
        errors_list = error_delta.errors_introduced + error_delta.errors_resolved
        ranked_skills = self._retrieve_ranked_skills(
            task_description=task_description,
            errors=errors_list,
            top_k=3,
        )
        skill_injector = self._build_skill_injector(ranked_skills, repair_mode=True)

        # AST Analysis context
        ast_context = ""
        if error_delta.errors_introduced and self.ast_analyzer:
            error_files = []
            for err in error_delta.errors_introduced:
                file_matches = re.findall(r'[\w/\\.-]+\.(?:py|js|jsx|ts|tsx)', err)
                for match in file_matches:
                    if match not in error_files: error_files.append(match)
            
            if error_files:
                try:
                    targets = [(f, 1) for f in error_files[:3]]
                    ast_contract = self.ast_analyzer.analyze(targets, errors=error_delta.errors_introduced)
                    ast_context = f"\n[AST ANALYSIS]\n{ast_contract.model_dump_json(indent=2)}\n"
                except Exception as e:
                    logger.warning(f"AST analysis failed: {e}")
        
        # Failure Lessons context
        failure_memory_context = ""
        if self.failure_memory:
            try:
                err_str = '\n'.join(error_delta.errors_introduced)
                relevant_failures = self.failure_memory.retrieve_lessons(task_description, err_str, top_k=3)
                if relevant_failures:
                    failure_memory_context = "\n" + self.failure_memory.format_for_prompt(relevant_failures) + "\n"
                    for pattern, lesson, score in relevant_failures:
                        self.failure_memory._store._increment_injection_count(pattern.signature)
            except Exception as e:
                logger.warning(f"FailureMemory retrieval failed: {e}")

        # Build repair prompt
        system_prompt = f'''You are the Targeted Repair Planner.
[ERROR DELTA ANALYSIS]
Errors Resolved: {error_delta.errors_resolved}
Errors Introduced: {error_delta.errors_introduced}
{ast_context}
{failure_memory_context}
Generate a MINIMAL plan to fix ONLY the failed step.
{skill_injector}'''

        err_str = '\n'.join(error_delta.errors_introduced)
        messages = [{"role": "user", "content": f"Original task: {task_description}\nFailed checks:\n{err_str}"}]
        
        if self.llm:
            try:
                plan = self.llm.generate_structured(
                    task_name="replan_repair",
                    model=os.getenv("AG_LLM_MODEL", "gemini-2.5-flash"),
                    system=system_prompt,
                    messages=messages,
                    response_model=ExecutionPlan
                )
                plan.completion_criteria = failed_plan.completion_criteria
                return plan
            except Exception as e:
                logger.warning(f"Repair replan failed: {e}")
                
        return self._deterministic_planner_fallback(task_description, Exception("Repair failed"), "debug", failed_plan.completion_criteria)

    def _deterministic_planner_fallback(self, task_desc: str, err: Exception, domain: str, completion_spec: 'TaskCompletionSpec' = None) -> 'ExecutionPlan':
        from antigravity.core.schemas import ExecutionPlan, PlanStep, TaskCompletionSpec, ArtifactCheck
        if not completion_spec:
            completion_spec = TaskCompletionSpec(
                deterministic_checks=[ArtifactCheck(type="file_exists", path=f"fallback_{domain}.log")],
                semantic_goal="Analyze task and output fallback log."
            )
        elif hasattr(completion_spec, "model_dump"):
            completion_spec = completion_spec.model_dump()
        return ExecutionPlan(
            objective=f"Fallback Execution: {task_desc[:50]}",
            steps=[PlanStep(step_id=1, action="analyze", agent=domain, input={"query": str(task_desc), "fallback": True})],
            completion_criteria=completion_spec,
            risk_flags=[f"Planner Failed: {str(err)}"]
        )
