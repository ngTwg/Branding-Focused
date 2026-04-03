"""
Orchestrator Routing Module — Tier Analysis and Task Routing for v6.5.0-SLIM.
"""

from __future__ import annotations
import logging
import os
import re
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from antigravity.core.slm_router import SLMRouter
    from antigravity.core.llm_client import LLMClient
    from antigravity.core.budget_guard import BudgetGuard
    from antigravity.core.budget_strategy import BudgetStrategy
    from antigravity.core.schemas import RouteDecision

logger = logging.getLogger(__name__)

CLARIFICATION_SKILL = "specialized/ask-questions-if-underspecified/SKILL.md"

class TierAnalysis(BaseModel):
    """Result of tier analysis."""
    tier: int
    reason: str
    is_complex: bool
    requires_external_research: bool = False
    confidence: float = 1.0

class RoutingModule:
    """
    Handles task routing and tier analysis for AntigravityOrchestrator.
    """
    
    def __init__(
        self, 
        slm_router: Optional[SLMRouter] = None,
        llm: Optional[LLMClient] = None,
        budget_guard: Optional[BudgetGuard] = None,
        budget_strategy: Optional[BudgetStrategy] = None
    ):
        self.slm_router = slm_router
        self.llm = llm
        self.budget_guard = budget_guard
        self.budget_strategy = budget_strategy

    def analyze_tier(self, task_description: str) -> int:
        """
        v6.5: Rule 1 - Tier-Based Dynamic Routing.
        Categorizes task complexity to optimize token loading.
        """
        q = task_description.lower()
        
        # Tier 4: Aspirational/Singularity
        if any(w in q for w in ["singularity", "transcendence", "polymorphic", "omni-perspective"]):
            return 4
            
        # Tier 3: System Architecture / Migration
        if any(w in q for w in ["architecture", "migration", "refactor system", "restructure"]):
            return 3
            
        # Tier 1: Tiny Snippets / Typos
        if len(task_description) < 150 and not any(w in q for w in ["create", "build", "implement", "feature"]):
            return 1
            
        # Tier 2: Default (New Feature / Security / Bugfix)
        return 2

    def _infer_intent(self, task_description: str) -> str:
        q = task_description.lower()
        if any(w in q for w in ["error", "bug", "exception", "fails", "traceback", "stack trace"]):
            return "debug"
        if any(w in q for w in ["create", "build", "generate", "scaffold", "implement"]):
            return "generate"
        if any(w in q for w in ["edit", "update", "modify", "refactor", "change"]):
            return "edit"
        if any(w in q for w in ["explain", "why", "how does", "what does"]):
            return "explain"
        if any(w in q for w in ["find", "search", "lookup", "where"]):
            return "retrieve"
        return "analyze"

    def _is_underspecified(self, task_description: str) -> bool:
        q = task_description.lower().strip()
        tokens = re.findall(r"\w+", q)

        if not tokens:
            return True

        vague_markers = [
            "fix this",
            "help me",
            "do it",
            "make it better",
            "this issue",
            "that bug",
            "it fails",
            "something broke",
            "optimize this",
            "improve this",
        ]
        has_vague_marker = any(marker in q for marker in vague_markers)

        has_specific_anchor = bool(
            re.search(r"\b\w+\.(py|ts|tsx|js|jsx|json|md|yaml|yml)\b", q)
            or re.search(r"\bline\s+\d+\b", q)
            or re.search(r"\btraceback\b|\bexception\b|\berror\s*:\b", q)
            or re.search(r"\bfunction\s+\w+\b|\bclass\s+\w+\b", q)
        )

        too_short_for_action = len(tokens) <= 4 and any(
            w in q for w in ["fix", "debug", "build", "create", "update", "implement"]
        )

        return (has_vague_marker and not has_specific_anchor) or (too_short_for_action and not has_specific_anchor)

    def _infer_candidate_skills(
        self,
        task_description: str,
        domain: str,
        intent: str,
        needs_clarification: bool,
    ) -> list[str]:
        q = task_description.lower()
        candidates: list[str] = []

        if needs_clarification:
            candidates.append(CLARIFICATION_SKILL)

        domain_map = {
            "frontend": [
                "frontend/react-patterns.md",
                "frontend/css-styling.md",
                "frontend/web-performance.md",
            ],
            "backend": [
                "backend/api-design.md",
                "backend/database-patterns.md",
                "backend/error-handling.md",
            ],
            "infra": [
                "devops/containerization.md",
                "devops/cicd-pipelines.md",
                "devops/observability.md",
            ],
            "debug": [
                "workflows/debug-protocol.md",
                "workflows/systematic-debugging.md",
            ],
            "architecture": [
                "backend/api-design.md",
                "devops/infrastructure-as-code.md",
            ],
            "general": [
                "workflows/code-review.md",
                "workflows/testing-strategies.md",
            ],
        }
        candidates.extend(domain_map.get(domain, []))

        intent_map = {
            "debug": ["workflows/debug-protocol.md"],
            "generate": ["workflows/test-driven-development.md"],
            "edit": ["workflows/refactoring.md"],
            "retrieve": ["workflows/code-review.md"],
        }
        candidates.extend(intent_map.get(intent, []))

        if any(w in q for w in ["payment", "checkout", "stripe", "paypal"]):
            candidates.append("specialized/fintech-payments.md")
        if any(w in q for w in ["medical", "fda", "hipaa", "insulin"]):
            candidates.append("specialized/healthtech-medical.md")
        if any(w in q for w in ["security", "owasp", "xss", "sqli", "auth"]):
            candidates.append("security/attack-vectors.md")

        deduped: list[str] = []
        seen: set[str] = set()
        for skill in candidates:
            if skill not in seen:
                deduped.append(skill)
                seen.add(skill)

        return deduped[:15]

    def _compose_reasoning(self, base: str, needs_clarification: bool) -> str:
        if not needs_clarification:
            return base[:300]
        suffix = " Clarification required before implementation."
        composed = f"{base.strip()} {suffix}".strip()
        return composed[:300]

    def route_task(self, task_description: str, span: any) -> 'RouteDecision':
        """
        Route task using SLMRouter first, fall through to LLM if needed.
        """
        from antigravity.core.schemas import RouteDecision
        
        # v6.2: Get current budget zone and strategy
        remaining_ratio = self.budget_guard.remaining_ratio if self.budget_guard else 1.0
        current_zone = self.budget_strategy.get_current_zone(remaining_ratio) if self.budget_strategy else None
        strategy_config = self.budget_strategy.get_strategy(current_zone) if self.budget_strategy else None
        
        # Log zone transition if changed
        if self.budget_strategy:
            self.budget_strategy.log_zone_transition(
                old_zone=self.budget_strategy._current_zone,
                new_zone=current_zone,
                remaining_ratio=remaining_ratio
            )
            self.budget_strategy._current_zone = current_zone

        needs_clarification = self._is_underspecified(task_description)
        inferred_intent = self._infer_intent(task_description)
        span.update(needs_clarification=needs_clarification)

        # Try SLM router first
        slm_enabled_by_strategy = (
            strategy_config is None
            or strategy_config.prefer_slm
            or strategy_config.prompt_mode == "full"
        )

        if self.slm_router and slm_enabled_by_strategy:
            try:
                slm_decision = self.slm_router.classify(task_description)
                if slm_decision is not None:
                    logger.info(f"SLMRouter classified with confidence {slm_decision.confidence:.3f}")
                    span.update(slm_used=True, slm_confidence=slm_decision.confidence)
                    candidate_skills = self._infer_candidate_skills(
                        task_description=task_description,
                        domain=slm_decision.chosen,
                        intent=inferred_intent,
                        needs_clarification=needs_clarification,
                    )
                    
                    return RouteDecision(
                        domain=slm_decision.chosen,
                        intent=inferred_intent,
                        requires_retrieval=True,
                        confidence=slm_decision.confidence,
                        candidate_skills=candidate_skills,
                        reasoning_summary=self._compose_reasoning(
                            f"SLM classification: {slm_decision.chosen}",
                            needs_clarification,
                        )
                    )
            except Exception as e:
                logger.warning(f"SLMRouter failed: {e}, falling through to LLM")
                span.update(slm_error=str(e))
        
        # Fall through to LLM routing
        system_prompt = '''You are a routing engine for the Antigravity orchestrator.
Classify the request into: domain, intent, whether retrieval is required, candidate skills.
Rules:
- Prefer "debug" when user includes errors, stack traces, failing behavior.
- Prefer "generate" when user asks to create new code.
- Prefer "edit" when modifying existing code.
- Set requires_retrieval=true when domain-specific project knowledge is needed.
Return only data matching the schema.'''

        messages = [{"role": "user", "content": f"User Request: {task_description}"}]
        
        if self.llm and self.budget_guard:
            try:
                # Estimate token cost
                estimated_input = len(system_prompt) // 4 + len(task_description) // 4
                max_output = 200
                
                self.budget_guard.check_pre_call(estimated_input, max_output)
                
                result = self.llm.generate_structured(
                    task_name="router_primary",
                    model=os.getenv("AG_LLM_MODEL", "gemini-2.5-flash"),
                    system=system_prompt,
                    messages=messages,
                    response_model=RouteDecision
                )

                if result.candidate_skills:
                    if needs_clarification and CLARIFICATION_SKILL not in result.candidate_skills:
                        result.candidate_skills = [CLARIFICATION_SKILL] + result.candidate_skills
                    result.candidate_skills = result.candidate_skills[:15]
                else:
                    result.candidate_skills = self._infer_candidate_skills(
                        task_description=task_description,
                        domain=result.domain,
                        intent=result.intent,
                        needs_clarification=needs_clarification,
                    )

                result.reasoning_summary = self._compose_reasoning(
                    result.reasoning_summary,
                    needs_clarification,
                )
                
                actual_in, actual_out = self.llm.last_call_tokens
                self.budget_guard.record_call(actual_in + actual_out)
                self.budget_guard.record_step()
                
                return result
            except Exception as e:
                logger.warning(f"LLM Routing failed: {e}")
                span.log_error(str(e))
        
        return self._deterministic_router_fallback(task_description, Exception("All routing failed"))

    def _deterministic_router_fallback(self, query: str, err: Exception) -> 'RouteDecision':
        from antigravity.core.schemas import RouteDecision
        q = query.lower()
        domain = "general"
        intent = self._infer_intent(query)
        needs_clarification = self._is_underspecified(query)
        
        if any(w in q for w in ["react", "next", "component", "css", "ui"]): domain = "frontend"
        elif any(w in q for w in ["api", "database", "sql", "node"]): domain = "backend"
        elif any(w in q for w in ["docker", "deploy", "nginx"]): domain = "infra"

        candidate_skills = self._infer_candidate_skills(
            task_description=query,
            domain=domain,
            intent=intent,
            needs_clarification=needs_clarification,
        )
            
        return RouteDecision(
            domain=domain, intent=intent, requires_retrieval=True, confidence=0.1,
            candidate_skills=candidate_skills,
            reasoning_summary=self._compose_reasoning(
                f"Heuristic Fallback: {str(err)[:50]}",
                needs_clarification,
            )
        )
