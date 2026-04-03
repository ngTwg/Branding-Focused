"""
Orchestrator Execution Module — Execution Loop and Self-Healing for v6.5.0-SLIM.
"""

from __future__ import annotations
import logging
import hashlib
from pathlib import Path
from collections import deque
from typing import Optional, TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    from antigravity.core.schemas import ExecutionPlan, RouteDecision, ErrorDelta, TaskCompletionSpec
    from antigravity.core.llm_client import LLMClient
    from antigravity.core.budget_guard import BudgetGuard
    from antigravity.core.budget_strategy import BudgetStrategy
    from antigravity.core.backup_manager import BackupManager
    from antigravity.core.failure_memory import FailureMemory
    from antigravity.core.health_monitor import HealthMonitor
    from antigravity.core.action_runner import ActionDispatcher
    from antigravity.core.checker import DeterministicChecker

logger = logging.getLogger(__name__)

class ExecutionModule:
    """
    Handles the execution phase, self-healing loop, and artifact verification.
    """
    
    def __init__(
        self,
        llm: Optional[LLMClient] = None,
        budget_guard: Optional[BudgetGuard] = None,
        budget_strategy: Optional[BudgetStrategy] = None,
        backup_manager: Optional[BackupManager] = None,
        failure_memory: Optional[FailureMemory] = None,
        health_monitor: Optional[HealthMonitor] = None,
        context_window_size: int = 5,
    ):
        self.llm = llm
        self.budget_guard = budget_guard
        self.budget_strategy = budget_strategy
        self.backup_manager = backup_manager
        self.failure_memory = failure_memory
        self.health_monitor = health_monitor
        self.context_window_size = max(1, context_window_size)
        self._fingerprints = set()

    def run_loop(
        self,
        session_id: str,
        task_description: str,
        active_plan: 'ExecutionPlan',
        trace: any,
        replan_callback: Optional[callable] = None,
        project_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the provided plan and performs self-healing if needed.
        """
        from antigravity.core.action_runner import ActionDispatcher
        from antigravity.core.checker import DeterministicChecker
        from antigravity.core.id_utils import new_id
        from antigravity.core.schemas import ErrorDelta
        
        dispatcher = ActionDispatcher(self.llm)
        checker = DeterministicChecker()
        accumulated_context = deque(maxlen=self.context_window_size)
        
        MAX_REPAIR_ATTEMPTS = self.budget_guard._max_repair_attempts if self.budget_guard else 5
        repair_count = 0
        previous_error_delta = None
        
        with trace.span(name="execution_and_healing_loop") as exec_span:
            while repair_count <= MAX_REPAIR_ATTEMPTS:
                operation_id = new_id()
                
                # Identify modified files for backup
                modified_files = self._identify_modified_files(active_plan)
                
                # Backup and hash for no-op detection
                self._handle_backups(session_id, operation_id, modified_files)
                pre_hashes = self._get_file_hashes(modified_files)
                
                # Execute Steps
                self._execute_steps(active_plan, dispatcher, accumulated_context, exec_span)
                
                # No-op Detection (Rule 2.3)
                post_hashes = self._get_file_hashes(modified_files)
                if modified_files and pre_hashes == post_hashes:
                    logger.warning(f"No-op patch detected: {operation_id}")
                    if repair_count >= MAX_REPAIR_ATTEMPTS: break
                    repair_count += 1
                    active_plan = self._trigger_replan(task_description, active_plan, "No-op detected", exec_span, operation_id)
                    continue

                # Verification Pass
                prev_errors = previous_error_delta.errors_introduced if previous_error_delta else []
                error_delta = checker.examine(
                    active_plan.completion_criteria.deterministic_checks,
                    previous_errors=prev_errors,
                    project_root=project_path
                )
                
                # Trace Linking
                exec_span.link_patch_metadata(patch_id=operation_id, error_delta=error_delta, rollback_triggered=False)
                
                # Success Check
                if error_delta.net_improvement and error_delta.new_error_score == 0.0:
                    exec_span.update(status="success", repair_count=repair_count)
                    return {"status": "success", "repair_count": repair_count, "error_delta": error_delta}

                # Regression Guard & Rollback (Rule 2.2)
                if not error_delta.net_improvement:
                    self._handle_rollback(session_id, operation_id, error_delta, task_description, modified_files, exec_span)
                
                # Stagnation Guard (Rule 2.2)
                fingerprint = self._compute_fingerprint(active_plan, error_delta, modified_files)
                if fingerprint in self._fingerprints:
                    logger.error("Semantic Stagnation Detected. Exiting Loop.")
                    break
                self._fingerprints.add(fingerprint)

                # Replan for Healing
                repair_count += 1
                if repair_count > MAX_REPAIR_ATTEMPTS: break
                
                if replan_callback:
                    active_plan = replan_callback(task_description, active_plan, error_delta, exec_span)
                else: break
                
                previous_error_delta = error_delta

        return {"status": "partial", "repair_count": repair_count, "error_delta": previous_error_delta}

    def _identify_modified_files(self, plan: 'ExecutionPlan') -> List[str]:
        files = []
        for step in plan.steps:
            if step.action in ["write_file", "generate_code", "edit_file", "apply_diff"]:
                if "path" in step.input: files.append(step.input["path"])
                elif "files" in step.input:
                    for f in step.input["files"]:
                        if isinstance(f, dict) and "path" in f: files.append(f["path"])
        return list(set(files))

    def _handle_backups(self, session_id: str, op_id: str, files: List[str]):
        if files and self.backup_manager:
            try:
                self.backup_manager.create_backup(session_id, op_id, files)
            except Exception as e:
                logger.warning(f"Backup failed: {e}")

    def _get_file_hashes(self, files: List[str]) -> Dict[str, str]:
        hashes = {}
        for f in files:
            path = Path(f)
            if path.exists():
                try: hashes[f] = hashlib.sha256(path.read_bytes()).hexdigest()
                except: pass
        return hashes

    def _execute_steps(self, plan: 'ExecutionPlan', dispatcher: any, context: deque, span: any):
        for step in plan.steps:
            with span.span(name=f"step_{step.step_id}_{step.action}") as step_span:
                try:
                    res = dispatcher.dispatch(step.action, step.input, list(context))
                    context.append({"step": step.step_id, "action": step.action, "result": res})
                    step_span.update(agent=step.agent, action=step.action)
                except Exception as e:
                    logger.error(f"Step {step.step_id} failed: {e}")
                    context.append({"step": step.step_id, "action": step.action, "error": str(e)})

    def _handle_rollback(self, session_id: str, op_id: str, delta: 'ErrorDelta', task: str, files: List[str], span: any):
        if self.backup_manager:
            try:
                self.backup_manager.rollback(session_id, op_id)
                span.log_event("rollback_triggered", {"operation_id": op_id})
                if self.failure_memory:
                    self.failure_memory.record_failure(
                        failure_id=op_id,
                        patch_diff="Rollback triggered",
                        error_text="\n".join(delta.errors_introduced),
                        files_touched=files,
                        session_id=session_id
                    )
            except Exception as e:
                logger.critical(f"Rollback failed: {e}")

    def _compute_fingerprint(self, plan: 'ExecutionPlan', delta: 'ErrorDelta', files: List[str]) -> str:
        s = str([s.action for s in plan.steps]) + str(delta.errors_introduced) + str(files)
        return hashlib.sha256(s.encode()).hexdigest()

    def _trigger_replan(self, task: str, plan: 'ExecutionPlan', context: any, span: any, op_id: str) -> 'ExecutionPlan':
        from antigravity.core.schemas import ErrorDelta
        if isinstance(context, str):
            context = ErrorDelta(operation_id=op_id, errors_introduced=[context], old_error_score=1.0, new_error_score=1.0, net_improvement=False)
        
        span.log_event("replan_triggered", {"reason": context.errors_introduced[0] if context.errors_introduced else "Retry"})
        # Note: In a real implementation, this would call back to PlanningModule or use a callback
        # For now, we assume the orchestrator provides the replan function or PlanningModule is accessible.
        return plan # Placeholder; the caller handles replanning usually
