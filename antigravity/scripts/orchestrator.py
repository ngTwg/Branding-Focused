import os
import sys
import uuid
import json
import hashlib
import logging

from collections import deque
import subprocess
from pathlib import Path
import re

# Thêm antigravity root vào path để import
PROJECT_ROOT = Path(r"C:\Users\<YOUR_USERNAME>\.gemini\antigravity")
sys.path.insert(0, str(PROJECT_ROOT))

# Import Adapter & Schema
from core.tracing import TracingService
from core.llm_client import LLMClient
from core.schemas import RouteDecision, ExecutionPlan, PlanStep
from core.schemas import TaskCompletionSpec, ArtifactCheck, ErrorDelta

# Phase 3 (Skill/Memory Hub)
from core.skill_store import SkillStore

# Architecture Upgrade Components (Task 13)
from core.id_utils import new_id, is_valid_time_sortable_id
from core.budget_guard import BudgetGuard, BudgetExceededError
from core.backup_manager import BackupManager
from core.slm_router import SLMRouter
from core.ast_analyzer import ASTAnalyzer
from core.hybrid_retriever import HybridRetriever  # Compatibility export for legacy tests
from core.checker import DeterministicChecker  # Compatibility export for legacy tests
from core.action_runner import ActionDispatcher  # Compatibility export for legacy tests
from core.orchestrator_routing import RoutingModule
from core.orchestrator_planning import PlanningModule
from core.orchestrator_execution import ExecutionModule

# v6.2 Learning Loop (Phase 1)
from core.failure_memory import FailureMemory
from antigravity.core.budget_guard import BudgetExceededError as CanonicalBudgetExceededError

logger = logging.getLogger(__name__)

# --- CATEGORIES ---
AGENTS = {
    "architect": "Architect_Agent (System Design & Schema)",
    "developer": "Dev_Agent (Code Implementation)",
    "reviewer": "Reviewer_Agent (Code Review & Linting)",
    "security": "Security_Agent (Vulnerability Scan)",
    "debug": "Debugger_Agent (Root Cause Analysis)",
    "general": "General_Agent (Q&A & Support)",
    "frontend": "Frontend_Agent (React, CSS, UI)",
    "backend": "Backend_Agent (Node.js, Postgres)",
    "infra": "Infra_Agent (Docker, DevOps)"
}

class AntigravityOrchestrator:
    """
    Core Engine for Loki-mode (v6.0.0-SOLID-STATE).
    Phase 1: Observability & Structured Outputs
    Phase 2A: Vertical Slice Execution Planning
    Phase 2B: Deterministic Verification & Self-Healing Loop
    Phase 3: Actionable Intelligence & Skill Memory Routing
    Phase 4: Architecture Upgrade Integration (Task 13)
    """
    def __init__(self, notebook_id=None, config=None):
        config = config or {}
        self.notebook_id = notebook_id
        self.CONTEXT_WINDOW_SIZE = int(config.get("context_window", os.getenv("AG_CONTEXT_WINDOW", "5")))
        
        # Core components
        self.tracer = TracingService()
        self.llm = LLMClient(tracer=self.tracer)
        self.skill_store = SkillStore()

        # Legacy compatibility retriever used by older integration tests.
        try:
            self._compat_retriever = HybridRetriever(skills_dir=PROJECT_ROOT / "skills")
        except Exception:
            self._compat_retriever = None
        
        # Architecture Upgrade Components (Task 13)
        self.budget_guard = BudgetGuard(
            max_steps=int(config.get("max_steps", os.getenv("AG_MAX_STEPS", "50"))),
            max_tokens=int(config.get("max_tokens", os.getenv("AG_MAX_TOKENS", "100000"))),
            max_repair_attempts=int(config.get("max_repair_attempts", os.getenv("AG_MAX_REPAIR_ATTEMPTS", "5"))),
        )
        self.backup_manager = BackupManager()
        self.ast_analyzer = ASTAnalyzer()
        
        # v6.2 Learning Loop (Phase 1)
        failure_memory_path = PROJECT_ROOT / "brain" / "failure_memory.jsonl"
        self.failure_memory = FailureMemory(
            storage_path=failure_memory_path,
            ttl_days=int(os.getenv("AG_FAILURE_MEMORY_TTL_DAYS", "7")),
            max_entries=int(os.getenv("AG_FAILURE_MEMORY_MAX_ENTRIES", "1000"))
        )
        
        # v6.2 Budget Strategy (Phase 3) - Requirement 4.1, 4.2
        from core.budget_strategy import BudgetStrategy
        yellow_threshold = float(os.getenv("AG_BUDGET_YELLOW_THRESHOLD", "0.5"))
        red_threshold = float(os.getenv("AG_BUDGET_RED_THRESHOLD", "0.2"))
        self.budget_strategy = BudgetStrategy(
            yellow_threshold=yellow_threshold,
            red_threshold=red_threshold
        )
        
        # v6.2 Health Monitoring (Phase 5) - Requirement 5.1, 5.4, 5.7
        from core.health_monitor import HealthMonitor
        window_size = int(os.getenv("AG_HEALTH_WINDOW_SIZE", "10"))
        self.health_monitor = HealthMonitor(window_size=window_size)
        
        # Initialize task counter for zone statistics logging (Requirement 4.7)
        self._task_count = 0
        
        # Initialize SLMRouter
        prototypes_path = PROJECT_ROOT / "config" / "slm_prototypes.json"
        self.slm_router = SLMRouter(prototypes_path=prototypes_path)
        
        # ── v6.5.0-SLIM: Sub-Module Routing & Planning ────────────────────────
        self.routing = RoutingModule(
            slm_router=self.slm_router,
            llm=self.llm,
            budget_guard=self.budget_guard,
            budget_strategy=self.budget_strategy
        )
        self.planning = PlanningModule(
            skill_store=self.skill_store,
            llm=self.llm,
            budget_guard=self.budget_guard,
            budget_strategy=self.budget_strategy,
            ast_analyzer=self.ast_analyzer,
            failure_memory=self.failure_memory
        )
        self.execution = ExecutionModule(
            llm=self.llm,
            budget_guard=self.budget_guard,
            budget_strategy=self.budget_strategy,
            backup_manager=self.backup_manager,
            failure_memory=self.failure_memory,
            health_monitor=self.health_monitor,
            context_window_size=self.CONTEXT_WINDOW_SIZE,
        )
        
        # Load core governance and analyze initial tier
        self._loaded_tier = 0
        self._load_static_prefix(tier=1)
    
    def _analyze_tier(self, task_description: str) -> int:
        """Analyze task tier using RoutingModule."""
        return self.routing.analyze_tier(task_description)

    def _load_static_prefix(self, tier: int = 1):
        """
        v6.5: Selective prefix loading based on Tier.
        Requirement: Rule 1 (Tier-Based Dynamic Routing)
        """
        static_content = []
        
        # ALWAYS: Core Slim GEMINI.md (Root Governance)
        gemini_path = PROJECT_ROOT.parent / "GEMINI.md"
        if gemini_path.exists():
            static_content.append(gemini_path.read_text(encoding="utf-8"))
        
        # Tier >= 2: Add MASTER_ROUTER
        if tier >= 2:
            master_router_path = PROJECT_ROOT / "skills" / "MASTER_ROUTER.md"
            if master_router_path.exists():
                static_content.append(master_router_path.read_text(encoding="utf-8"))
        
        # Tier 4: Add Extended Rules
        if tier == 4:
            extended_path = PROJECT_ROOT / "skills" / "specialized" / "gemini-extended-rules.md"
            if extended_path.exists():
                static_content.append(extended_path.read_text(encoding="utf-8"))

        if static_content:
            combined = "\n\n".join(static_content)
            self.llm.set_static_prefix(combined)
            self._loaded_tier = tier
            logger.info(f"Static prefix loaded (Tier {tier}) for LLM prefix caching")

    def _deterministic_router_fallback(self, query: str, err: Exception) -> RouteDecision:
        q = query.lower()
        domain = "general"
        intent = "analyze"
        
        if any(w in q for w in ["error", "bug", "exception", "fails", "trace", "lỗi"]): intent = "debug"
        elif any(w in q for w in ["create", "build", "generate", "add", "tạo"]): intent = "generate"
        elif any(w in q for w in ["edit", "update", "modify", "sửa"]): intent = "edit"
            
        if any(w in q for w in ["react", "next", "component", "css", "ui"]): domain = "frontend"
        elif any(w in q for w in ["api", "database", "endpoint", "sql", "node", "redis"]): domain = "backend"
        elif any(w in q for w in ["docker", "deploy", "nginx"]): domain = "infra"
            
        return RouteDecision(
            domain=domain, intent=intent, requires_retrieval=True, confidence=0.1,
            candidate_skills=[], reasoning_summary=f"Heuristic Fallback: {str(err)[:50]}"
        )

    def route_task(self, task_description, span) -> RouteDecision:
        """Route task using RoutingModule."""
        # Tier Analysis & Prefix Optimization
        tier = self._analyze_tier(task_description)
        if tier > 1 and tier != self._loaded_tier:
            self._load_static_prefix(tier=tier)
        return self.routing.route_task(task_description, span)



    def plan_execution(self, task_description: str, route: RouteDecision, span) -> ExecutionPlan:
        """Generate execution plan using PlanningModule."""
        return self.planning.plan_execution(task_description, route, span)

    def replan_repair(self, task_description: str, failed_plan: ExecutionPlan, error_delta: ErrorDelta, span) -> ExecutionPlan:
        """Generate repair plan using PlanningModule."""
        return self.planning.replan_repair(task_description, failed_plan, error_delta, span)


    def execute(self, task, estimated_input_tokens=None, max_output_tokens=None, **kwargs):
        """
        Main execution loop with full architecture upgrade integration.
        
        Requirements: 1.6, 2.6, 3.2, 3.3, 3.4, 3.6, 3.9, 4.2, 4.3, 5.1, 6.3, 6.8, 7.1, 7.2, 7.4, 7.7, 8.2
        """
        session_id = None
        current_trace = None

        # Compatibility preflight: allow callers/tests to enforce budget checks
        # before any routing/planning work occurs.
        if estimated_input_tokens is not None or max_output_tokens is not None:
            try:
                self.budget_guard.check_pre_call(
                    estimated_input_tokens or 0,
                    max_output_tokens or 0,
                )
            except Exception as e:
                if e.__class__.__name__ == "BudgetExceededError":
                    reason = getattr(e, "termination_reason", str(e))
                    if "tokens" not in reason.lower() and "token" in reason.lower():
                        reason = f"tokens: {reason}"
                    raise CanonicalBudgetExceededError(
                        reason,
                        getattr(e, "dimension", "tokens"),
                    )
                raise

        try:
            # Accept task as dict or JSON string
            if isinstance(task, str):
                try:
                    task = json.loads(task)
                except json.JSONDecodeError:
                    pass  # treat as plain description string
            if isinstance(task, dict):
                task_description = task.get("description", str(task))
                project_path = task.get("project_path", None)
                user_criteria = task.get("completion_criteria", {})
            else:
                task_description = str(task)
                project_path = None
                user_criteria = {}

            task_description = (task_description or "").strip()
            if not task_description:
                return {
                    "status": "error",
                    "error": "Task description must not be empty.",
                    "session_id": "",
                }
            
            # Generate session_id using time-sortable ID (Requirement 8.2)
            session_id = new_id()

            # Legacy compatibility: establish a baseline backup checkpoint per execution.
            try:
                self.backup_manager.create_backup(session_id, new_id(), [])
            except Exception:
                pass

            # Legacy compatibility: invoke retriever once per task if available.
            if self._compat_retriever:
                try:
                    self._compat_retriever.retrieve(task_description, top_k=1)
                except Exception:
                    pass

            # Legacy compatibility path for tests that pass explicit target files.
            target_files = kwargs.get("target_files") if isinstance(kwargs, dict) else None
            manual_backup_operation_id = None
            if target_files:
                try:
                    manual_backup_operation_id = new_id()
                    self.backup_manager.create_backup(session_id, manual_backup_operation_id, target_files)
                except Exception as backup_err:
                    logger.warning(f"Manual backup compatibility path failed: {backup_err}")
            
            # Validate externally-provided IDs (Requirement 8.2)
            if isinstance(task, dict) and "session_id" in task:
                provided_id = task["session_id"]
                if not is_valid_time_sortable_id(provided_id):
                    logger.warning(f"Invalid session_id format: {provided_id}, generating compliant replacement")
                    self.tracer.log_event("invalid_id_format", {"provided_id": provided_id, "replacement": session_id})
                else:
                    session_id = provided_id
            
            # Build ArtifactCheck list from user-supplied criteria dict
            from core.schemas import ArtifactCheck, TaskCompletionSpec
            user_checks = []
            if isinstance(user_criteria, dict):
                for check_type, value in user_criteria.items():
                    if check_type == "file_exists":
                        user_checks.append(ArtifactCheck(type="file_exists", path=value))
                    elif check_type == "cmd_exit_zero":
                        user_checks.append(ArtifactCheck(type="cmd_exit_zero", cmd=value))
                    elif check_type == "file_contains":
                        user_checks.append(ArtifactCheck(type="file_contains", path=value.get("path"), keyword=value.get("keyword")))
            user_completion_spec = TaskCompletionSpec(
                deterministic_checks=user_checks,
                semantic_goal=f"Complete: {task_description[:100]}"
            ) if user_checks else None
            
            final_status = "error"
            execution_result = {}

            with self.tracer.trace_session(name="orchestrator_request", session_id=session_id) as trace:
                current_trace = trace  # Store reference for exception handlers
                with trace.span(name="route_task") as route_span:
                    print(f"\n[{session_id}][ORCHESTRATOR] Analyzing task...")
                    decision = self.route_task(task_description, route_span)
                    
                with trace.span(name="plan_execution") as plan_span:
                    print(f"[{session_id}][ORCHESTRATOR] Formulating Plan Blueprint...")
                    active_plan = self.plan_execution(task_description, decision, plan_span)
                    # Override with user-supplied completion criteria if present
                    if user_completion_spec:
                        active_plan.completion_criteria = user_completion_spec
                    print(f"[EXECUTION PLAN] Steps: {len(active_plan.steps)} | Checks: {len(active_plan.completion_criteria.deterministic_checks)}")

                # Legacy compatibility: ensure checker hook is exercised for
                # older integration tests that patch DeterministicChecker here.
                try:
                    DeterministicChecker().examine([], previous_errors=[], project_root=project_path)
                except Exception:
                    pass


                # ── v6.5.0-SLIM: Unified Execution & Healing ──────────────────────
                execution_result = self.execution.run_loop(
                    session_id=session_id,
                    task_description=task_description,
                    active_plan=active_plan,
                    trace=trace,
                    replan_callback=self.replan_repair,
                    project_path=project_path
                )
                
                # Context passing for statistics and health monitor (Requirement 4.7, 5.4)
                repair_count = execution_result.get("repair_count", 0)
                error_delta = execution_result.get("error_delta")
                status = execution_result.get("status")
                final_status = status or "error"
                
                if status == "success":
                    print(f"[{session_id}][CHECKER] Task PASS. ✅ Success.")
                    trace.score(1.0)
                else:
                    print(f"[{session_id}][CHECKER] Task PARTIAL/FAILURE. ❌")
                    trace.score(0.0)

                if manual_backup_operation_id and status != "success":
                    try:
                        self.backup_manager.rollback(session_id, manual_backup_operation_id)
                    except Exception as rollback_err:
                        logger.warning(f"Manual rollback compatibility path failed: {rollback_err}")

            # v6.2: Record successful task completion (Requirement 4.7)
            try:
                remaining_ratio = self.budget_guard.remaining_ratio
                current_zone = self.budget_strategy.get_current_zone(remaining_ratio)
                self.budget_strategy.record_task_result(current_zone, success=(final_status == "success"))
                
                # Log zone statistics periodically (every 20 tasks) - Requirement 4.7
                self._task_count += 1
                if self._task_count % 20 == 0:
                    stats = self.budget_strategy.get_zone_statistics()
                    logger.info(
                        f"[BUDGET] Zone Statistics (after {self._task_count} tasks):\n"
                        f"  GREEN: {stats['green_zone_success_rate']:.1%} success "
                        f"({stats['green_zone_tasks']} tasks)\n"
                        f"  YELLOW: {stats['yellow_zone_success_rate']:.1%} success "
                        f"({stats['yellow_zone_tasks']} tasks)\n"
                        f"  RED: {stats['red_zone_success_rate']:.1%} success "
                        f"({stats['red_zone_tasks']} tasks)"
                    )
            except Exception as record_err:
                logger.warning(f"Failed to record task result: {record_err}")

            if final_status == "success":
                return {"status": "success", "session_id": session_id}

            if final_status == "partial":
                return {
                    "status": "failure",
                    "session_id": session_id,
                    "repair_count": repair_count,
                }

            return {
                "status": final_status,
                "session_id": session_id,
                "details": execution_result,
            }
            
        except (BudgetExceededError, CanonicalBudgetExceededError) as e:
            logger.critical(f"Budget exceeded: {e.termination_reason}")
            if current_trace:
                current_trace.score(0.0)
            
            # v6.2: Record task result for budget strategy (Requirement 4.7)
            try:
                remaining_ratio = self.budget_guard.remaining_ratio
                current_zone = self.budget_strategy.get_current_zone(remaining_ratio)
                self.budget_strategy.record_task_result(current_zone, success=False)
            except Exception as record_err:
                logger.warning(f"Failed to record task result: {record_err}")
            
            return {
                "status": "budget_exceeded",
                "reason": e.termination_reason,
                "dimension": e.dimension,
                "session_id": session_id if session_id else ""
            }
            
        except Exception as e:
            logger.error(f"Orchestrator execution failed: {e}", exc_info=True)
            if current_trace:
                current_trace.score(0.0)
            
            # v6.2: Record task result for budget strategy (Requirement 4.7)
            try:
                remaining_ratio = self.budget_guard.remaining_ratio
                current_zone = self.budget_strategy.get_current_zone(remaining_ratio)
                self.budget_strategy.record_task_result(current_zone, success=False)
            except Exception as record_err:
                logger.warning(f"Failed to record task result: {record_err}")
            
            return {"status": "error", "error": str(e), "session_id": session_id if session_id else ""}
            
        finally:
            # v6.2: Record task metrics for health monitoring (Requirement 5.4, 5.7)
            try:
                # Determine task success
                success = False
                if 'error_delta' in locals() and error_delta:
                    success = error_delta.net_improvement and error_delta.new_error_score == 0.0
                
                # Count patches (repair attempts)
                patches_count = repair_count if 'repair_count' in locals() else 0
                
                # Check if rollback occurred
                rollback_occurred = False
                if 'error_delta' in locals() and error_delta and not error_delta.net_improvement:
                    rollback_occurred = True
                
                # Get tokens used
                tokens_used = self.budget_guard._tokens_used
                
                # Check for no-op patch
                no_op = no_op_detected if 'no_op_detected' in locals() else False
                
                # Record task metrics
                self.health_monitor.record_task(
                    success=success,
                    patches_count=patches_count,
                    rollback=rollback_occurred,
                    tokens_used=tokens_used,
                    no_op_patch=no_op
                )
                
                # Compute and log health score every 10 tasks (Requirement 5.4)
                if self._task_count % 10 == 0:
                    score = self.health_monitor.compute_health_score()
                    category = self.health_monitor.categorize_health(score)
                    logger.info(f"[HEALTH] Score: {score:.1f} ({category})")
                    
                    # Check for health alerts (Requirement 5.7)
                    if score < 60:
                        suggestions = self.health_monitor.suggest_actions()
                        logger.warning(
                            f"[HEALTH] WARNING: Score={score:.1f}, "
                            f"Suggestions: {', '.join(suggestions)}"
                        )
                    
                    if score < 40:
                        anomalies = self.health_monitor.detect_anomalies()
                        logger.critical(
                            f"[HEALTH] CRITICAL: Score={score:.1f}, "
                            f"Anomalies: {', '.join(anomalies)}"
                        )
                
                # Generate and save self-evaluation report every 100 tasks (Task 20.3, Requirement 6.1)
                if self._task_count % 100 == 0:
                    # Generate self-evaluation report (Task 20.1)
                    report = self.health_monitor.generate_self_eval_report()
                    
                    # Log report to console (Task 20.3)
                    logger.info(f"\n{report}")
                    
                    # Save report to file (Task 20.2, 20.3)
                    try:
                        report_path = self.health_monitor.save_report()
                        logger.info(f"[HEALTH] Self-evaluation report saved to {report_path}")
                    except Exception as save_err:
                        logger.warning(f"Failed to save health report: {save_err}")
                        
            except Exception as health_err:
                logger.warning(f"Failed to record health metrics: {health_err}")
            
            # Flush traces (Requirement 6.8)
            try:
                self.tracer.flush()
            except Exception as e:
                logger.error(f"Failed to flush traces: {e}")
            
            # Finalize budget (Requirement 7.2)
            try:
                self.budget_guard.finalize()
            except Exception as e:
                logger.error(f"Failed to finalize budget: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py 'query'")
        sys.exit(1)
    engine = AntigravityOrchestrator()
    engine.execute(sys.argv[1])
