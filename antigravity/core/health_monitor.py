"""
Health monitoring system for Antigravity v6.2.

This module provides health score computation, derived metrics, and self-evaluation
capabilities for the autonomous debugging runtime.

Phase 5: Health Monitoring - Task 16.1
Phase 6: Self-Evaluation - Task 21 (Performance Baseline)
Phase 6: Self-Evaluation - Task 22 (Actionable Suggestions)
"""

from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
import uuid

from antigravity.core.suggestion_engine import SuggestionEngine


@dataclass
class TaskMetrics:
    """
    Metrics for a single completed task.
    
    Used by HealthMonitor to track task-level performance and compute
    derived metrics like success rate, rollback rate, and token efficiency.
    
    Attributes:
        task_id: Unique identifier for the task
        success: Whether the task completed successfully
        patches_count: Number of patches applied during task execution
        rollback: Whether a rollback was triggered
        tokens_used: Total tokens consumed for this task
        no_op_patch: Whether a no-op patch was detected (patch with no changes)
        timestamp: When the task completed
    """
    
    task_id: str
    success: bool
    patches_count: int
    rollback: bool
    tokens_used: int
    no_op_patch: bool
    timestamp: datetime


@dataclass
class DerivedMetrics:
    """
    Computed metrics derived from a window of TaskMetrics history.
    
    These metrics are used to compute the health score and detect anomalies
    in system behavior. All rates are floats in range [0.0, 1.0].
    
    Computed from a window of TaskMetrics (e.g., last 10 tasks) to provide
    rolling statistics about system performance.
    
    Attributes:
        avg_patches_per_success: Average number of patches per successful task
        rollback_rate: Proportion of tasks that triggered rollbacks [0.0-1.0]
        no_op_patch_rate: Proportion of patches that were no-ops [0.0-1.0]
        slm_vs_llm_ratio: Ratio of SLM usage vs LLM usage (future: model routing)
        token_per_task: Average tokens consumed per task
        success_rate: Proportion of tasks that completed successfully [0.0-1.0]
    """
    
    avg_patches_per_success: float
    rollback_rate: float
    no_op_patch_rate: float
    slm_vs_llm_ratio: float
    token_per_task: float
    success_rate: float


@dataclass
class BaselineMetrics:
    """
    Performance baseline computed from first 50 successful tasks.
    
    This baseline provides a reference point for detecting performance degradation
    and anomalies. It is established once during system initialization and updated
    quarterly (every 90 days) to adapt to evolving system behavior.
    
    Used for anomaly detection by comparing current DerivedMetrics against these
    baseline values. Significant deviations trigger alerts or self-healing actions.
    
    Attributes:
        baseline_token_per_task: Expected average tokens per task from baseline period
        baseline_patches: Expected average patches per successful task from baseline
        baseline_success_rate: Expected success rate from baseline period [0.0-1.0]
        established_at: Timestamp when this baseline was computed
        task_count: Number of successful tasks used to compute this baseline (typically 50)
        version: Baseline version number (incremented on each update)
    """
    
    baseline_token_per_task: float
    baseline_patches: float
    baseline_success_rate: float
    established_at: datetime
    task_count: int
    version: int = 1  # Task 21.5: Add version tracking


class HealthMonitorMetricsAdapter:
    """
    Adapter to provide HealthMonitor metrics to SuggestionEngine.
    
    This adapter implements the MetricsProvider protocol required by SuggestionEngine,
    bridging the gap between HealthMonitor's internal state and the suggestion system.
    """
    
    def __init__(
        self,
        health_monitor: 'HealthMonitor',
        index_manager=None,
        budget_strategy=None
    ):
        """
        Initialize the metrics adapter.
        
        Args:
            health_monitor: HealthMonitor instance to get metrics from
            index_manager: Optional IndexManager for stale ratio (Task 22.2 Rule 1)
            budget_strategy: Optional BudgetStrategy for zone statistics (Task 22.2 Rule 3)
        """
        self._health_monitor = health_monitor
        self._index_manager = index_manager
        self._budget_strategy = budget_strategy
    
    def get_stale_ratio(self) -> float:
        """Get the ratio of stale embeddings from IndexManager."""
        if self._index_manager is None:
            raise NotImplementedError("IndexManager not provided")
        return self._index_manager.get_stale_ratio()
    
    def get_rollback_rate(self) -> float:
        """Get the rollback rate from HealthMonitor."""
        metrics = self._health_monitor.get_derived_metrics(window="last_10")
        return metrics.rollback_rate
    
    def get_red_zone_ratio(self) -> float:
        """Get the ratio of time spent in red budget zone from BudgetStrategy."""
        if self._budget_strategy is None:
            raise NotImplementedError("BudgetStrategy not provided")
        
        # Get zone statistics from BudgetStrategy
        stats = self._budget_strategy.get_zone_statistics()
        
        # Calculate red zone ratio
        total_tasks = sum(stats.values())
        if total_tasks == 0:
            return 0.0
        
        red_tasks = stats.get("red", 0)
        return red_tasks / total_tasks
    
    def get_slm_usage_ratio(self) -> float:
        """Get the ratio of SLM usage vs total from HealthMonitor."""
        metrics = self._health_monitor.get_derived_metrics(window="last_10")
        return metrics.slm_vs_llm_ratio
    
    def get_token_efficiency_ratio(self) -> float:
        """Get current token usage vs baseline from HealthMonitor."""
        metrics = self._health_monitor.get_derived_metrics(window="last_10")
        
        if self._health_monitor._baseline is None:
            return 1.0  # No baseline, assume normal
        
        baseline_tokens = self._health_monitor._baseline.baseline_token_per_task
        if baseline_tokens == 0:
            return 1.0
        
        return metrics.token_per_task / baseline_tokens
    
    def get_success_rate(self) -> float:
        """Get the success rate from HealthMonitor."""
        metrics = self._health_monitor.get_derived_metrics(window="last_10")
        return metrics.success_rate


class HealthMonitor:
    """
    Compute health score and derived metrics for self-evaluation.
    
    The HealthMonitor tracks task execution history and computes a health score
    that reflects overall system performance. It uses a weighted formula that
    considers success rate, rollback rate, retry count, and token efficiency.
    
    Health Score Formula:
        health_score = (
            success_rate * 100
            - rollback_rate * w1
            - (avg_patches - 1) * w2
            - (token_per_task / baseline_token) * w3
        )
        
        Default weights: w1=20 (rollback penalty), w2=10 (retry penalty), w3=5 (token penalty)
        Range: [0, 100]
    
    Health Categories:
        - Excellent: 80-100
        - Good: 60-79
        - Fair: 40-59
        - Poor: 0-39
    
    Task 22 Integration:
        The HealthMonitor now uses SuggestionEngine for enhanced actionable suggestions
        with priority scoring. External components (IndexManager, BudgetStrategy) can be
        provided for additional suggestion rules.
    
    Usage:
        monitor = HealthMonitor(window_size=10)
        monitor.record_task(success=True, patches=2, rollback=False, tokens=2500, no_op=False)
        score = monitor.compute_health_score()
        category = monitor.categorize_health(score)
    """
    
    def __init__(
        self,
        window_size: int = 10,
        weights: dict[str, float] | None = None,
        baseline_update_interval_days: int = 90,  # Task 21.1: Add baseline update interval
        data_dir: Path | str | None = None,  # Task 21.5: Add data directory for persistence
        index_manager=None,  # Task 22: Add IndexManager for Rule 1
        budget_strategy=None  # Task 22: Add BudgetStrategy for Rule 3
    ):
        """
        Initialize the HealthMonitor.
        
        Args:
            window_size: Number of recent tasks to analyze for rolling metrics (default: 10)
            weights: Custom weights for health score formula. If None, uses defaults:
                     {"rollback_rate": 20, "retry_count": 10, "token_efficiency": 5}
            baseline_update_interval_days: Days between automatic baseline updates (default: 90)
            data_dir: Directory for persisting baseline data (default: antigravity/data/)
            index_manager: Optional IndexManager for stale ratio suggestions (Task 22)
            budget_strategy: Optional BudgetStrategy for budget zone suggestions (Task 22)
        
        The health score is computed from a rolling window of recent tasks to provide
        up-to-date performance metrics. A larger window provides more stable metrics
        but is less responsive to recent changes.
        """
        self._window_size = window_size
        
        # Default weights for health score formula
        # w1: rollback penalty (high impact - indicates regression)
        # w2: retry penalty (medium impact - indicates inefficiency)
        # w3: token penalty (low impact - indicates resource usage)
        self._weights = weights or {
            "rollback_rate": 20,
            "retry_count": 10,
            "token_efficiency": 5
        }
        
        # Task history - stores metrics for recent tasks
        # Using deque with maxlen for automatic size limiting (bounded history)
        self._task_history: deque[TaskMetrics] = deque(maxlen=window_size)
        
        # Performance baseline - established from first 50 successful tasks
        # Used for anomaly detection and relative performance measurement
        self._baseline: BaselineMetrics | None = None
        
        # Current health metrics - cached for efficiency
        self._health_score: float = 100.0  # Start optimistic
        self._health_category: str = "excellent"
        
        # Task 21.1: Baseline update tracking
        self._baseline_update_interval = timedelta(days=baseline_update_interval_days)
        self._last_baseline_update: datetime | None = None
        self._tasks_since_baseline: int = 0  # Track tasks since last baseline update
        
        # Task 21.5: Data directory for persistence
        if data_dir is None:
            # Default to antigravity/data/
            current_file = Path(__file__)
            antigravity_root = current_file.parent.parent
            self._data_dir = antigravity_root / "data"
        else:
            self._data_dir = Path(data_dir)
        
        # Create data directory if it doesn't exist
        self._data_dir.mkdir(parents=True, exist_ok=True)
        
        # Task 22: Initialize SuggestionEngine and metrics adapter
        self._index_manager = index_manager
        self._budget_strategy = budget_strategy
        self._suggestion_engine = SuggestionEngine()
        self._metrics_adapter = HealthMonitorMetricsAdapter(
            health_monitor=self,
            index_manager=index_manager,
            budget_strategy=budget_strategy
        )
        
        # Task 21.5: Load baseline from disk if it exists
        self._load_baseline()
    
    def record_task(
        self,
        success: bool,
        patches_count: int,
        rollback: bool,
        tokens_used: int,
        no_op_patch: bool
    ) -> None:
        """
        Record metrics for a completed task.
        
        This method creates a TaskMetrics instance and appends it to the task history.
        It uses a deque with maxlen for automatic size limiting - when the deque is full,
        the oldest task is automatically removed when a new one is added.
        
        When the history reaches 50 tasks and no baseline exists, it automatically
        establishes a performance baseline for anomaly detection.
        
        Task 21.4: Checks if baseline should be updated and triggers update if needed.
        
        Args:
            success: Whether the task completed successfully
            patches_count: Number of patches applied during task execution
            rollback: Whether a rollback was triggered
            tokens_used: Total tokens consumed for this task
            no_op_patch: Whether a no-op patch was detected
        
        Side Effects:
            - Appends TaskMetrics to _task_history (deque automatically maintains maxlen)
            - Calls establish_baseline() when history reaches 50 tasks (if no baseline exists)
            - Calls update_baseline() if baseline update conditions are met (Task 21.4)
        
        Note:
            Parameter names match the method signature specified in task 16.5:
            record_task(success, patches_count, rollback, tokens_used, no_op_patch)
        """
        # Create TaskMetrics instance with generated task_id
        task_metric = TaskMetrics(
            task_id=str(uuid.uuid4()),
            success=success,
            patches_count=patches_count,
            rollback=rollback,
            tokens_used=tokens_used,
            no_op_patch=no_op_patch,
            timestamp=datetime.now()
        )
        
        # Append to history (deque automatically maintains maxlen)
        self._task_history.append(task_metric)
        
        # Track tasks since baseline for update logic
        if success:
            self._tasks_since_baseline += 1
        
        # Establish baseline after 50 tasks if not already established
        if len(self._task_history) == 50 and self._baseline is None:
            self.establish_baseline()
        
        # Task 21.4: Check if baseline should be updated
        if self.should_update_baseline():
            self.update_baseline()
    
    def compute_health_score(self) -> float:
        """
        Compute system health score (0-100).
        
        The health score reflects overall system performance using a weighted formula
        that considers multiple factors:
        
        Formula:
            health_score = (
                success_rate * 100
                - rollback_rate * w1
                - (avg_patches - 1) * w2
                - (token_per_task / baseline_token) * w3
            )
        
        Where:
            - success_rate: Proportion of successful tasks [0.0-1.0]
            - rollback_rate: Proportion of tasks with rollbacks [0.0-1.0]
            - avg_patches: Average patches per successful task
            - token_per_task: Average tokens consumed per task
            - baseline_token: Expected tokens from baseline (or current avg if no baseline)
            - w1, w2, w3: Configurable weights (default: 20, 10, 5)
        
        The score is clamped to [0, 100] range.
        
        Returns:
            Health score as a float in range [0.0, 100.0]
        
        Side Effects:
            - Updates self._health_score cache
        
        Note:
            Returns 100.0 if no task history exists (optimistic default).
        """
        # Return optimistic default if no history
        if not self._task_history:
            self._health_score = 100.0
            return self._health_score
        
        # Calculate success rate
        total_tasks = len(self._task_history)
        successful_tasks = sum(1 for task in self._task_history if task.success)
        success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0.0
        
        # Calculate rollback rate
        rollback_count = sum(1 for task in self._task_history if task.rollback)
        rollback_rate = rollback_count / total_tasks if total_tasks > 0 else 0.0
        
        # Calculate average patches per successful task
        if successful_tasks > 0:
            avg_patches = sum(
                task.patches_count for task in self._task_history if task.success
            ) / successful_tasks
        else:
            avg_patches = 1.0  # Default to 1 if no successful tasks
        
        # Calculate average tokens per task
        token_per_task = sum(task.tokens_used for task in self._task_history) / total_tasks
        
        # Get baseline token (use current avg if no baseline established)
        baseline_token = (
            self._baseline.baseline_token_per_task 
            if self._baseline 
            else token_per_task
        )
        
        # Avoid division by zero
        if baseline_token == 0:
            baseline_token = 1.0
        
        # Extract weights
        w1 = self._weights["rollback_rate"]
        w2 = self._weights["retry_count"]
        w3 = self._weights["token_efficiency"]
        
        # Compute health score using formula
        health_score = (
            success_rate * 100
            - rollback_rate * w1
            - (avg_patches - 1) * w2
            - (token_per_task / baseline_token) * w3
        )
        
        # Clamp to [0, 100]
        health_score = max(0.0, min(100.0, health_score))
        
        # Update cache
        self._health_score = health_score
        
        return health_score
    
    def categorize_health(self, score: float) -> str:
        """
        Categorize health score into human-readable categories.
        
        Categories are defined as:
            - Excellent: 80-100 (system performing optimally)
            - Good: 60-79 (system performing well with minor issues)
            - Fair: 40-59 (system has noticeable issues requiring attention)
            - Poor: 0-39 (system has critical issues requiring immediate action)
        
        Args:
            score: Health score in range [0.0, 100.0]
        
        Returns:
            Category string: "excellent", "good", "fair", or "poor"
        
        Side Effects:
            - Updates self._health_category cache
        """
        if score >= 80:
            category = "excellent"
        elif score >= 60:
            category = "good"
        elif score >= 40:
            category = "fair"
        else:
            category = "poor"
        
        # Update cache
        self._health_category = category
        
        return category
    
    def get_derived_metrics(self, window: str = "last_10") -> DerivedMetrics:
        """
        Compute derived metrics from a window of task history.
        
        This method computes rolling statistics from a subset of the task history
        based on the specified window. Supported windows:
            - "last_10": Last 10 tasks (default)
            - "last_hour": Tasks from the last hour
            - "last_24h": Tasks from the last 24 hours
            - "all": All tasks in history
        
        Args:
            window: Time window for metric computation (default: "last_10")
        
        Returns:
            DerivedMetrics instance with computed statistics
        
        Raises:
            ValueError: If window parameter is invalid
        
        Note:
            Returns metrics with all zeros if no tasks match the window criteria.
        """
        # Filter task history based on window
        if window == "last_10":
            filtered_tasks = list(self._task_history)[-10:]
        elif window == "last_hour":
            cutoff = datetime.now().timestamp() - 3600  # 1 hour ago
            filtered_tasks = [
                task for task in self._task_history
                if task.timestamp.timestamp() >= cutoff
            ]
        elif window == "last_24h":
            cutoff = datetime.now().timestamp() - 86400  # 24 hours ago
            filtered_tasks = [
                task for task in self._task_history
                if task.timestamp.timestamp() >= cutoff
            ]
        elif window == "all":
            filtered_tasks = list(self._task_history)
        else:
            raise ValueError(f"Invalid window: {window}. Must be one of: last_10, last_hour, last_24h, all")
        
        # Return zero metrics if no tasks in window
        if not filtered_tasks:
            return DerivedMetrics(
                avg_patches_per_success=0.0,
                rollback_rate=0.0,
                no_op_patch_rate=0.0,
                slm_vs_llm_ratio=0.0,
                token_per_task=0.0,
                success_rate=0.0
            )
        
        # Compute metrics
        total_tasks = len(filtered_tasks)
        successful_tasks = [task for task in filtered_tasks if task.success]
        success_count = len(successful_tasks)
        
        # Success rate
        success_rate = success_count / total_tasks if total_tasks > 0 else 0.0
        
        # Rollback rate
        rollback_count = sum(1 for task in filtered_tasks if task.rollback)
        rollback_rate = rollback_count / total_tasks if total_tasks > 0 else 0.0
        
        # No-op patch rate
        no_op_count = sum(1 for task in filtered_tasks if task.no_op_patch)
        no_op_patch_rate = no_op_count / total_tasks if total_tasks > 0 else 0.0
        
        # Average patches per successful task
        if success_count > 0:
            avg_patches_per_success = sum(
                task.patches_count for task in successful_tasks
            ) / success_count
        else:
            avg_patches_per_success = 0.0
        
        # Average tokens per task
        token_per_task = sum(task.tokens_used for task in filtered_tasks) / total_tasks
        
        # SLM vs LLM ratio (placeholder - will be implemented when model routing is added)
        slm_vs_llm_ratio = 0.0
        
        return DerivedMetrics(
            avg_patches_per_success=avg_patches_per_success,
            rollback_rate=rollback_rate,
            no_op_patch_rate=no_op_patch_rate,
            slm_vs_llm_ratio=slm_vs_llm_ratio,
            token_per_task=token_per_task,
            success_rate=success_rate
        )
    
    def establish_baseline(self) -> None:
        """
        Compute performance baseline from first 50 successful tasks.
        
        The baseline provides a reference point for detecting performance degradation
        and anomalies. It is computed from the first 50 successful tasks in the
        task history and includes:
            - Average tokens per task
            - Average patches per successful task
            - Success rate
        
        This method is automatically called by record_task() when the history
        reaches 50 tasks and no baseline exists. It can also be called manually
        to re-establish the baseline.
        
        Side Effects:
            - Sets self._baseline to a new BaselineMetrics instance
            - Sets self._last_baseline_update to current time
            - Resets self._tasks_since_baseline to 0
            - Persists baseline to disk (Task 21.5)
            - Logs a message indicating baseline establishment
        
        Note:
            Requires at least 50 tasks in history (not necessarily all successful).
            If fewer than 50 successful tasks exist, logs a warning and does not
            establish baseline.
        """
        # Check if we have enough tasks
        if len(self._task_history) < 50:
            print(f"[HEALTH] Warning: Cannot establish baseline with only {len(self._task_history)} tasks (need 50)")
            return
        
        # Take first 50 tasks (not just successful ones)
        first_50_tasks = list(self._task_history)[:50]
        successful_tasks = [task for task in first_50_tasks if task.success]
        
        if len(successful_tasks) < 10:  # Need at least 10 successful tasks for meaningful baseline
            print(f"[HEALTH] Warning: Only {len(successful_tasks)} successful tasks in first 50 (need at least 10)")
            return
        
        # Compute baseline metrics from successful tasks
        baseline_token_per_task = sum(task.tokens_used for task in successful_tasks) / len(successful_tasks)
        baseline_patches = sum(task.patches_count for task in successful_tasks) / len(successful_tasks)
        
        # Success rate from first 50 tasks (all tasks, not just successful ones)
        baseline_success_rate = len(successful_tasks) / len(first_50_tasks)
        
        # Create baseline with version 1 (initial baseline)
        self._baseline = BaselineMetrics(
            baseline_token_per_task=baseline_token_per_task,
            baseline_patches=baseline_patches,
            baseline_success_rate=baseline_success_rate,
            established_at=datetime.now(),
            task_count=50,
            version=1
        )
        
        # Initialize tracking variables
        self._last_baseline_update = datetime.now()
        self._tasks_since_baseline = 0
        
        # Log baseline establishment
        print(f"[HEALTH] Baseline established: {self._baseline}")
        
        # Task 21.5: Persist baseline to disk
        self._save_baseline()
    
    def detect_anomalies(self) -> list[str]:
        """
        Detect performance anomalies by comparing current metrics vs baseline.
        
        This method compares current derived metrics against the established baseline
        to identify significant deviations that may indicate performance degradation
        or system issues.
        
        Anomaly detection rules:
            - Success rate drop > 20%: "Success rate dropped significantly"
            - Token usage spike > 50%: "Token usage increased significantly"
            - Patches increase > 100%: "Retry count increased significantly"
        
        Returns:
            List of anomaly descriptions (empty list if no anomalies or no baseline)
        
        Note:
            Returns empty list if no baseline has been established yet.
        """
        # Cannot detect anomalies without baseline
        if not self._baseline:
            return []
        
        # Get current metrics
        current_metrics = self.get_derived_metrics(window="last_10")
        
        anomalies = []
        
        # Check success rate drop
        success_rate_drop = self._baseline.baseline_success_rate - current_metrics.success_rate
        if success_rate_drop > 0.2:  # 20% drop
            anomalies.append(
                f"Success rate dropped significantly: "
                f"{current_metrics.success_rate:.1%} (baseline: {self._baseline.baseline_success_rate:.1%})"
            )
        
        # Check token usage spike
        if self._baseline.baseline_token_per_task > 0:
            token_increase_ratio = (
                current_metrics.token_per_task / self._baseline.baseline_token_per_task
            )
            if token_increase_ratio > 1.5:  # 50% increase
                anomalies.append(
                    f"Token usage increased significantly: "
                    f"{current_metrics.token_per_task:.0f} tokens/task "
                    f"(baseline: {self._baseline.baseline_token_per_task:.0f})"
                )
        
        # Check patches increase
        if self._baseline.baseline_patches > 0:
            patches_increase_ratio = (
                current_metrics.avg_patches_per_success / self._baseline.baseline_patches
            )
            if patches_increase_ratio > 2.0:  # 100% increase
                anomalies.append(
                    f"Retry count increased significantly: "
                    f"{current_metrics.avg_patches_per_success:.1f} patches/task "
                    f"(baseline: {self._baseline.baseline_patches:.1f})"
                )
        
        return anomalies
    
    def suggest_actions(self) -> list[str]:
        """
        Suggest concrete improvement actions based on current metrics (Task 22.4).
        
        This method uses the SuggestionEngine to analyze current derived metrics
        and generate prioritized, actionable suggestions for improving system performance.
        
        The SuggestionEngine evaluates 6 rules with priority scoring:
            1. High stale_ratio (>20%) → "Re-index skills" (HIGH)
            2. High rollback_rate (>15%) → "Review error detection" (HIGH)
            3. Frequent Red zone (>30%) → "Increase budget" (MEDIUM)
            4. Low SLM usage (<20%) → "Check SLM router" (LOW)
            5. High token per task (>baseline*1.5) → "Optimize prompts" (MEDIUM)
            6. Low success rate (<70%) → "Review skill retrieval" (CRITICAL)
        
        Returns:
            List of top-3 actionable suggestion strings, sorted by priority
            (CRITICAL > HIGH > MEDIUM > LOW)
        
        Note:
            If IndexManager or BudgetStrategy are not provided during initialization,
            rules that depend on them will be skipped gracefully.
        """
        # Use SuggestionEngine to get top suggestions (Task 22.3)
        suggestions = self._suggestion_engine.get_top_suggestions(
            metrics=self._metrics_adapter,
            max_count=3
        )
        
        return suggestions
    
    def generate_self_eval_report(self) -> str:
        """
        Generate a self-evaluation report (Task 20.1).
        
        This method creates a formatted report that includes:
            - Current health score and category
            - Key metrics from the last 10 tasks
            - Top issue (worst metric vs baseline)
            - Top suggestion (most critical action)
            - Top strength (best metric vs baseline)
        
        Triggered every 100 tasks by the Orchestrator (Requirement 6.1).
        
        Returns:
            Formatted self-evaluation report as a multi-line string
        
        Format:
            [SELF-EVAL] Performance Report
            - Health Score: {score} ({category})
            - Top Issue: {top_issue}
            - Suggestion: {top_suggestion}
            - Top Strength: {top_strength}
        """
        # Compute current health score
        score = self.compute_health_score()
        category = self.categorize_health(score)
        
        # Get current metrics
        metrics = self.get_derived_metrics(window="last_10")
        
        # Get suggestions
        suggestions = self.suggest_actions()
        top_suggestion = suggestions[0] if suggestions else "No issues detected"
        
        # Identify top issue
        anomalies = self.detect_anomalies()
        top_issue = anomalies[0] if anomalies else "No anomalies detected"
        
        # Identify top strength
        top_strength = "System performing within expected parameters"
        if self._baseline:
            if metrics.success_rate >= self._baseline.baseline_success_rate:
                improvement = (metrics.success_rate - self._baseline.baseline_success_rate) * 100
                top_strength = f"Success rate improved by {improvement:.1f}%"
            elif metrics.token_per_task < self._baseline.baseline_token_per_task:
                savings = (1 - metrics.token_per_task / self._baseline.baseline_token_per_task) * 100
                top_strength = f"Token efficiency improved by {savings:.1f}%"
        
        # Format report (Task 20.1 - specified format)
        report = f"""[SELF-EVAL] Performance Report
- Health Score: {score:.1f} ({category})
- Top Issue: {top_issue}
- Suggestion: {top_suggestion}
- Top Strength: {top_strength}
"""
        
        return report
    
    def generate_report(self) -> str:
        """
        Alias for generate_self_eval_report() for backward compatibility.
        
        Returns:
            Formatted self-evaluation report
        """
        return self.generate_self_eval_report()
    
    def save_report(self, report_dir: Path | str = None) -> Path:
        """
        Save self-evaluation report to disk (Task 20.2).
        
        This method:
        1. Generates a self-evaluation report
        2. Saves it to antigravity/reports/self_eval_{timestamp}.md
        3. Keeps only the last 10 reports (deletes older ones)
        
        Args:
            report_dir: Directory to save reports (default: antigravity/reports/)
        
        Returns:
            Path to the saved report file
        
        Side Effects:
            - Creates report_dir if it doesn't exist
            - Deletes old reports (keeps last 10)
        """
        # Default report directory
        if report_dir is None:
            # Get antigravity root directory
            current_file = Path(__file__)
            antigravity_root = current_file.parent.parent
            report_dir = antigravity_root / "reports"
        else:
            report_dir = Path(report_dir)
        
        # Create reports directory if not exists
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate report
        report_content = self.generate_self_eval_report()
        
        # Create filename with timestamp (including microseconds for uniqueness)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        report_filename = f"self_eval_{timestamp}.md"
        report_path = report_dir / report_filename
        
        # Save report to file
        report_path.write_text(report_content, encoding="utf-8")
        
        # Keep only last 10 reports (delete older ones)
        self._cleanup_old_reports(report_dir, keep_count=10)
        
        return report_path
    
    def _cleanup_old_reports(self, report_dir: Path, keep_count: int = 10) -> None:
        """
        Delete old self-evaluation reports, keeping only the most recent ones.
        
        Args:
            report_dir: Directory containing reports
            keep_count: Number of recent reports to keep (default: 10)
        
        Side Effects:
            - Deletes old report files
        """
        # Find all self_eval_*.md files
        report_files = sorted(
            report_dir.glob("self_eval_*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True  # Most recent first
        )
        
        # Delete files beyond keep_count
        for old_report in report_files[keep_count:]:
            try:
                old_report.unlink()
            except Exception as e:
                # Log but don't fail if deletion fails
                print(f"[HEALTH] Warning: Failed to delete old report {old_report}: {e}")
    
    def should_update_baseline(self) -> bool:
        """
        Check if baseline should be updated (Task 21.2).
        
        Baseline update conditions:
        1. Time-based: More than baseline_update_interval (default 90 days) has passed
        2. Data-based: At least 50 successful tasks have been recorded since last update
        
        Both conditions must be met for update to proceed.
        
        Returns:
            True if baseline should be updated, False otherwise
        
        Note:
            Returns False if no baseline exists yet (use establish_baseline() first).
        """
        # Cannot update if no baseline exists
        if self._baseline is None:
            return False
        
        # Check time condition: Has enough time passed?
        time_since_update = datetime.now() - self._last_baseline_update
        time_condition = time_since_update > self._baseline_update_interval
        
        # Check data condition: Do we have enough new successful tasks?
        data_condition = self._tasks_since_baseline >= 50
        
        # Both conditions must be met
        return time_condition and data_condition
    
    def update_baseline(self) -> None:
        """
        Update the performance baseline with recent data (Task 21.3).
        
        This method:
        1. Takes the last 50 successful tasks from history
        2. Recomputes baseline metrics (tokens, patches, success rate)
        3. Logs the old and new baseline values
        4. Updates _last_baseline_update timestamp
        5. Resets _tasks_since_baseline counter
        6. Increments baseline version
        7. Persists the new baseline to disk
        
        The baseline is updated quarterly (every 90 days) to adapt to evolving
        system behavior while maintaining a stable reference point.
        
        Side Effects:
            - Updates self._baseline with new metrics
            - Updates self._last_baseline_update
            - Resets self._tasks_since_baseline to 0
            - Saves baseline to disk (antigravity/data/baseline.json)
        
        Note:
            Requires at least 50 successful tasks in history. If insufficient data,
            logs a warning and does not update baseline.
            
            The deque has a maxlen, so we need to collect successful tasks from
            the available history (which may be less than the full task count).
        """
        # Get all successful tasks from history (limited by deque maxlen)
        successful_tasks = [task for task in self._task_history if task.success]
        
        # Need at least 50 successful tasks for meaningful baseline
        if len(successful_tasks) < 50:
            print(f"[BASELINE] Warning: Cannot update baseline with only {len(successful_tasks)} successful tasks (need 50)")
            return
        
        # Store old baseline for logging
        old_baseline = self._baseline
        
        # Take last 50 successful tasks
        recent_successful = successful_tasks[-50:]
        
        # Compute new baseline metrics
        new_token_per_task = sum(task.tokens_used for task in recent_successful) / len(recent_successful)
        new_patches = sum(task.patches_count for task in recent_successful) / len(recent_successful)
        
        # Success rate from all recent tasks (not just successful ones)
        # Take last 50 tasks from history (mix of successful and failed)
        # But if we don't have 50 tasks in history, use what we have
        recent_all_tasks = list(self._task_history)[-50:] if len(self._task_history) >= 50 else list(self._task_history)
        recent_successful_count = sum(1 for task in recent_all_tasks if task.success)
        new_success_rate = recent_successful_count / len(recent_all_tasks) if recent_all_tasks else 1.0
        
        # Create new baseline with incremented version
        new_version = old_baseline.version + 1 if old_baseline else 1
        
        self._baseline = BaselineMetrics(
            baseline_token_per_task=new_token_per_task,
            baseline_patches=new_patches,
            baseline_success_rate=new_success_rate,
            established_at=datetime.now(),
            task_count=50,
            version=new_version
        )
        
        # Update tracking variables
        self._last_baseline_update = datetime.now()
        self._tasks_since_baseline = 0
        
        # Log baseline update (Task 21.3 - specified format)
        print(f"[BASELINE] Updated: old={old_baseline}, new={self._baseline}")
        
        # Task 21.5: Persist baseline to disk
        self._save_baseline()
    
    def _save_baseline(self) -> None:
        """
        Save baseline to disk (Task 21.5).
        
        Saves the current baseline to antigravity/data/baseline.json with metadata:
        - established_at (ISO format timestamp)
        - task_count (number of tasks used to compute baseline)
        - version (baseline version number)
        - All baseline metrics
        
        Side Effects:
            - Creates/overwrites antigravity/data/baseline.json
        """
        if self._baseline is None:
            return
        
        baseline_path = self._data_dir / "baseline.json"
        
        # Convert baseline to dict for JSON serialization
        baseline_dict = {
            "baseline_token_per_task": self._baseline.baseline_token_per_task,
            "baseline_patches": self._baseline.baseline_patches,
            "baseline_success_rate": self._baseline.baseline_success_rate,
            "established_at": self._baseline.established_at.isoformat(),
            "task_count": self._baseline.task_count,
            "version": self._baseline.version
        }
        
        # Save to file
        with open(baseline_path, 'w', encoding='utf-8') as f:
            json.dump(baseline_dict, f, indent=2)
    
    def _load_baseline(self) -> None:
        """
        Load baseline from disk (Task 21.5).
        
        Loads the baseline from antigravity/data/baseline.json if it exists.
        If the file doesn't exist or is invalid, does nothing (baseline will be
        established from first 50 tasks).
        
        Side Effects:
            - Sets self._baseline if file exists and is valid
            - Sets self._last_baseline_update from loaded data
        """
        baseline_path = self._data_dir / "baseline.json"
        
        if not baseline_path.exists():
            return
        
        try:
            with open(baseline_path, 'r', encoding='utf-8') as f:
                baseline_dict = json.load(f)
            
            # Parse datetime from ISO format
            established_at = datetime.fromisoformat(baseline_dict["established_at"])
            
            # Create BaselineMetrics instance
            self._baseline = BaselineMetrics(
                baseline_token_per_task=baseline_dict["baseline_token_per_task"],
                baseline_patches=baseline_dict["baseline_patches"],
                baseline_success_rate=baseline_dict["baseline_success_rate"],
                established_at=established_at,
                task_count=baseline_dict["task_count"],
                version=baseline_dict.get("version", 1)  # Default to 1 for old baselines
            )
            
            # Set last update time
            self._last_baseline_update = established_at
            
            print(f"[BASELINE] Loaded from disk: {self._baseline}")
            
        except Exception as e:
            print(f"[BASELINE] Warning: Failed to load baseline from {baseline_path}: {e}")
            # Continue without baseline - will be established from first 50 tasks
