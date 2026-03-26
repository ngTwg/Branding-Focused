# Tài Liệu Thiết Kế: Antigravity Resilience Upgrade (v6.2)

## Tổng Quan

Nâng cấp v6.2 biến Antigravity từ **production-grade** (correct, tested) thành **production-resilient** (adaptive, self-improving). Focus vào 5 gaps quan trọng nhất được identify từ v6.1 production readiness review.

### Philosophy Shift

```
v6.1: "Observable System"
  ↓
v6.2: "Self-Evaluable System"
  ↓
v6.3: "Self-Improving System" (future)
```

---

## Kiến Trúc Tổng Thể

### New Components (5 additions)

```
┌─────────────────────────────────────────────────────────────┐
│                    RESILIENCE LAYER (NEW)                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ IndexManager │  │FailureMemory │  │ HealthMonitor   │  │
│  │ (lifecycle)  │  │ (learning)   │  │ (self-eval)     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                  INTELLIGENCE PLANE (v6.1)                   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │HybridRetriever│  │ ASTAnalyzer │  │  BudgetGuard    │  │
│  │  + adaptive  │  │ + prioritize │  │  + strategy     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Component 1: IndexManager

### Purpose
Maintain retrieval quality khi skills thay đổi (address gap #1).

### Interface

```python
class IndexManager:
    """
    Lifecycle management cho HybridRetriever index.
    Prevents silent quality degradation.
    """

    def __init__(
        self,
        skills_dir: Path,
        cache_dir: Path,
        stale_threshold: float = 0.2  # 20%
    ):
        self._skills_dir = skills_dir
        self._cache_dir = cache_dir
        self._stale_threshold = stale_threshold
        self._index_version = 0
        self._checksums: dict[str, str] = {}  # file -> SHA-256
        self._last_index_time: datetime | None = None

    def detect_changes(self) -> list[str]:
        """
        Scan skills_dir và detect changed files.
        Returns: list of changed file paths.
        """
        ...

    def mark_stale(self, file_paths: list[str]) -> None:
        """Mark embeddings as stale for given files."""
        ...

    def get_stale_ratio(self) -> float:
        """Return ratio of stale embeddings (0.0-1.0)."""
        ...

    def should_reindex(self) -> bool:
        """Check if re-index needed based on stale_threshold."""
        ...

    def reindex(self, retriever: HybridRetriever) -> None:
        """
        Trigger incremental re-index.
        Only re-embed changed files.
        """
        ...

    def get_health_metrics(self) -> dict:
        """
        Return index health metrics:
        {
            "total_skills": int,
            "stale_embeddings": int,
            "stale_ratio": float,
            "last_index_time": datetime,
            "index_version": int
        }
        """
        ...

    def save_checkpoint(self) -> None:
        """Save current index state to disk."""
        ...

    def rollback_index(self, version: int) -> None:
        """Rollback to previous index version."""
        ...
```

### Data Flow

```
Skills Directory Change
    │
    ▼
[IndexManager.detect_changes()]
    │ → compute SHA-256 checksums
    │ → compare with cached checksums
    ▼
Changed Files List
    │
    ▼
[IndexManager.mark_stale()]
    │
    ▼
Check stale_ratio
    ├─ < 20% → continue (no action)
    └─ ≥ 20% → [IndexManager.reindex()]
                    │
                    ▼
                [HybridRetriever.incremental_index()]
                    │ → only re-embed changed files
                    │ → update BM25 index
                    ▼
                Index Updated ✅
```

### Storage Format

```json
// cache_dir/index_metadata.json
{
  "index_version": 5,
  "last_index_time": "2026-03-26T10:30:00Z",
  "checksums": {
    "skills/frontend/react.md": "abc123...",
    "skills/backend/api.md": "def456..."
  },
  "stale_files": ["skills/frontend/react.md"]
}
```

---

## Component 2: ErrorPrioritizer (ASTAnalyzer Extension)

### Purpose
Focus on root cause errors khi có nhiều lỗi (address gap #2).

### Interface

```python
class ErrorPrioritizer:
    """
    Intelligent error prioritization và clustering.
    Prevents LLM context overload.
    """

    PRIORITY_WEIGHTS = {
        "SyntaxError": 1,      # Highest priority
        "RuntimeError": 2,
        "LintWarning": 3       # Lowest priority
    }

    def prioritize_errors(
        self,
        errors: list[str],
        max_errors: int = 3
    ) -> list[PrioritizedError]:
        """
        Sort errors by priority và return top-k.

        Returns:
            List of PrioritizedError with:
            - error_text: str
            - priority: int (1-3)
            - is_root_cause: bool
            - dependent_errors: list[str]
        """
        ...

    def detect_error_chains(
        self,
        errors: list[str]
    ) -> dict[str, list[str]]:
        """
        Detect dependency chains: error A → causes error B.

        Returns:
            {root_error: [dependent_errors]}
        """
        ...

    def cluster_errors(
        self,
        errors: list[str]
    ) -> list[ErrorCluster]:
        """
        Group similar errors together.

        Returns:
            List of ErrorCluster with:
            - cluster_type: str (e.g., "undefined_name")
            - count: int
            - representative: str (example error)
        """
        ...

    def estimate_context_size(
        self,
        errors: list[str]
    ) -> int:
        """Estimate token count for error context."""
        ...
```

### Prioritization Logic

```python
def _classify_error(error_text: str) -> tuple[str, int]:
    """
    Classify error và assign priority.

    Returns: (error_type, priority)
    """
    if "SyntaxError" in error_text or "invalid syntax" in error_text:
        return ("SyntaxError", 1)

    if any(kw in error_text for kw in ["RuntimeError", "Exception", "Traceback"]):
        return ("RuntimeError", 2)

    return ("LintWarning", 3)

def _detect_import_chain(errors: list[str]) -> dict:
    """
    Detect: missing import → undefined name chain.

    Example:
        Error 1: "ModuleNotFoundError: No module named 'foo'"
        Error 2: "NameError: name 'foo' is not defined"

    → Error 1 is root cause, Error 2 is dependent
    """
    ...
```

### Integration with ASTAnalyzer

```python
# In ASTAnalyzer.analyze()
def analyze(self, targets: list[tuple[str, int]]) -> ASTContract:
    # ... existing code ...

    # NEW: Prioritize errors
    prioritizer = ErrorPrioritizer()
    all_errors = [node.error_text for node in affected_nodes if node.error_text]

    prioritized = prioritizer.prioritize_errors(all_errors, max_errors=3)

    # Only include top-priority errors in contract
    contract.affected_nodes = [
        node for node in affected_nodes
        if node.error_text in [p.error_text for p in prioritized]
    ]

    contract.error_priority_info = {
        "total_errors": len(all_errors),
        "included_errors": len(prioritized),
        "root_causes": [p.error_text for p in prioritized if p.is_root_cause]
    }

    return contract
```

---

## Component 3: FailureMemory

### Purpose
Learn from failed patches để không lặp lại sai lầm (address gap #3 - HIGHEST IMPACT).

### Interface

```python
class FailureMemory:
    """
    Persistent memory of failed patches.
    Enables learning loop.
    """

    def __init__(
        self,
        storage_path: Path,
        ttl_hours: int = 24,
        max_entries: int = 1000
    ):
        self._storage_path = storage_path
        self._ttl = timedelta(hours=ttl_hours)
        self._max_entries = max_entries
        self._memory: dict[str, FailureEntry] = {}

    def record_failure(
        self,
        patch_content: str,
        error_delta: ErrorDelta,
        session_id: str
    ) -> str:
        """
        Record a failed patch.

        Returns: failure_id (hash of patch)
        """
        ...

    def search_similar(
        self,
        current_error: str,
        top_k: int = 3
    ) -> list[FailureEntry]:
        """
        Find similar past failures.
        Uses cosine similarity on error embeddings.
        """
        ...

    def extract_pattern(
        self,
        patch_content: str,
        error_delta: ErrorDelta
    ) -> str:
        """
        Extract failure pattern from patch.

        Examples:
        - "missing closing bracket in list comprehension"
        - "forgot to import module before use"
        - "incorrect indentation in function definition"
        """
        ...

    def format_for_prompt(
        self,
        similar_failures: list[FailureEntry]
    ) -> str:
        """
        Format failure memory for LLM prompt injection.

        Returns:
            [FAILURE MEMORY]
            Previous failed attempts:
            - Patch X caused SyntaxError at foo.py:12
              Pattern: missing closing bracket
            - Patch Y caused RuntimeError: undefined variable
              Pattern: forgot to import module

            AVOID similar patterns in your repair.
        """
        ...

    def purge_expired(self) -> int:
        """Remove entries older than TTL. Returns count removed."""
        ...

    def get_statistics(self) -> dict:
        """
        Return memory statistics:
        {
            "total_entries": int,
            "pattern_distribution": dict[str, int],
            "avg_age_hours": float,
            "most_common_failure": str
        }
        """
        ...

    def persist(self) -> None:
        """Save memory to disk (JSON)."""
        ...

    def load(self) -> None:
        """Load memory from disk."""
        ...
```

### Data Model

```python
@dataclass
class FailureEntry:
    failure_id: str              # SHA-256 hash
    patch_content: str
    error_delta: ErrorDelta
    failure_pattern: str         # extracted pattern
    timestamp: datetime
    session_id: str
    embedding: list[float] | None  # for similarity search
```

### Pattern Extraction Logic

```python
def _extract_syntax_pattern(error_text: str) -> str:
    """
    Extract pattern from syntax errors.

    Examples:
        "SyntaxError: invalid syntax at line 12"
        → "invalid syntax"

        "SyntaxError: unmatched ']' at line 5"
        → "unmatched closing bracket"
    """
    patterns = {
        r"unmatched ['\")\]]": "unmatched closing bracket",
        r"expected [':']": "missing colon",
        r"invalid syntax": "invalid syntax",
        r"unexpected indent": "incorrect indentation"
    }

    for regex, pattern in patterns.items():
        if re.search(regex, error_text):
            return pattern

    return "unknown syntax error"

def _extract_semantic_pattern(patch_content: str, error_text: str) -> str:
    """
    Extract semantic pattern from patch + error.

    Example:
        Patch adds: "result = foo.bar()"
        Error: "NameError: name 'foo' is not defined"
        → Pattern: "used undefined variable"
    """
    ...
```

### Integration with Orchestrator

```python
# In Orchestrator.replan_repair()
def replan_repair(
    self,
    task_description: str,
    failed_plan: ExecutionPlan,
    error_delta: ErrorDelta,
    span
) -> ExecutionPlan:
    # NEW: Record failure
    patch_content = self._extract_patch_from_plan(failed_plan)
    self.failure_memory.record_failure(patch_content, error_delta, self.session_id)

    # NEW: Search similar failures
    similar_failures = self.failure_memory.search_similar(
        error_delta.errors_introduced[0] if error_delta.errors_introduced else "",
        top_k=3
    )

    # NEW: Inject failure memory into prompt
    failure_context = self.failure_memory.format_for_prompt(similar_failures)

    system_prompt = f'''You are the Targeted Repair Planner.

{failure_context}

[ERROR DELTA ANALYSIS]
...
'''

    # ... rest of existing code ...
```

---

## Component 4: BudgetStrategy (BudgetGuard Extension)

### Purpose
Adaptive behavior khi budget thấp (address gap #4).

### Interface

```python
class BudgetStrategy:
    """
    Strategy pattern for budget-aware behavior.
    """

    @dataclass
    class StrategyConfig:
        top_k_skills: int
        enable_retrieval_expansion: bool
        max_prompt_tokens: int
        enable_repair_loop: bool
        prefer_slm: bool

    STRATEGIES = {
        "green": StrategyConfig(
            top_k_skills=5,
            enable_retrieval_expansion=True,
            max_prompt_tokens=4000,
            enable_repair_loop=True,
            prefer_slm=False
        ),
        "yellow": StrategyConfig(
            top_k_skills=3,
            enable_retrieval_expansion=False,
            max_prompt_tokens=2000,
            enable_repair_loop=True,
            prefer_slm=True
        ),
        "red": StrategyConfig(
            top_k_skills=1,
            enable_retrieval_expansion=False,
            max_prompt_tokens=500,
            enable_repair_loop=False,
            prefer_slm=True
        )
    }

    def __init__(
        self,
        budget_guard: BudgetGuard,
        yellow_threshold: float = 0.5,
        red_threshold: float = 0.2
    ):
        self._budget_guard = budget_guard
        self._yellow_threshold = yellow_threshold
        self._red_threshold = red_threshold

    def get_current_zone(self) -> Literal["green", "yellow", "red"]:
        """Determine current budget zone."""
        status = self._budget_guard.get_status()

        # Check token budget
        token_remaining_ratio = status.tokens_remaining / self._budget_guard._max_tokens

        if token_remaining_ratio <= self._red_threshold:
            return "red"
        elif token_remaining_ratio <= self._yellow_threshold:
            return "yellow"
        else:
            return "green"

    def get_strategy(self) -> StrategyConfig:
        """Get strategy config for current zone."""
        zone = self.get_current_zone()
        return self.STRATEGIES[zone]

    def log_zone_transition(self, old_zone: str, new_zone: str) -> None:
        """Log when zone changes."""
        logger.warning(
            f"[BUDGET] Zone transition: {old_zone} → {new_zone}\n"
            f"[BUDGET] Strategy: {self.STRATEGIES[new_zone]}"
        )
```

### Integration with Orchestrator

```python
# In Orchestrator.__init__()
self.budget_strategy = BudgetStrategy(self.budget_guard)
self._current_zone = "green"

# In Orchestrator.route_task()
def route_task(self, task_description, span) -> RouteDecision:
    # Check zone transition
    new_zone = self.budget_strategy.get_current_zone()
    if new_zone != self._current_zone:
        self.budget_strategy.log_zone_transition(self._current_zone, new_zone)
        self._current_zone = new_zone

    strategy = self.budget_strategy.get_strategy()

    # Apply strategy
    if strategy.prefer_slm and self.slm_router:
        # Try SLM first
        ...

    # ... rest of routing logic ...

# In Orchestrator.plan_execution()
def plan_execution(self, task_description, route, span) -> ExecutionPlan:
    strategy = self.budget_strategy.get_strategy()

    # Adjust retrieval based on strategy
    if strategy.enable_retrieval_expansion:
        skill = self.skill_store.retrieve(task_description, top_k=strategy.top_k_skills)
    else:
        skill = None  # Skip retrieval in degraded mode

    # Truncate prompt if needed
    if len(system_prompt) > strategy.max_prompt_tokens * 4:  # rough estimate
        system_prompt = system_prompt[:strategy.max_prompt_tokens * 4]

    # ... rest of planning logic ...
```

---

## Component 5: HealthMonitor

### Purpose
Self-evaluation với actionable metrics (address gap #5).

### Interface

```python
class HealthMonitor:
    """
    Compute health score và derived metrics.
    Enable self-evaluation.
    """

    def __init__(
        self,
        window_size: int = 10,  # last N tasks
        weights: dict[str, float] = None
    ):
        self._window_size = window_size
        self._weights = weights or {
            "rollback_rate": 20,
            "retry_count": 10,
            "token_efficiency": 5
        }
        self._task_history: deque[TaskMetrics] = deque(maxlen=window_size)
        self._baseline: BaselineMetrics | None = None

    def record_task(
        self,
        success: bool,
        patches_count: int,
        rollback_triggered: bool,
        tokens_used: int,
        no_op_patch: bool
    ) -> None:
        """Record metrics for completed task."""
        ...

    def compute_health_score(self) -> float:
        """
        Compute system health score (0-100).

        Formula:
            health_score = (
                success_rate * 100
                - rollback_rate * w1
                - avg_retry_count * w2
                - (token_per_task / baseline) * w3
            )
        """
        ...

    def get_derived_metrics(self) -> DerivedMetrics:
        """
        Compute derived metrics:
        {
            "avg_patches_per_success": float,
            "rollback_rate": float,
            "no_op_patch_rate": float,
            "slm_vs_llm_ratio": float,
            "token_per_task": float
        }
        """
        ...

    def categorize_health(self, score: float) -> str:
        """
        Categorize health score:
        - Excellent: 80-100
        - Good: 60-79
        - Fair: 40-59
        - Poor: 0-39
        """
        ...

    def detect_anomalies(self) -> list[str]:
        """
        Detect performance anomalies.

        Returns: list of anomaly descriptions
        """
        ...

    def suggest_actions(self) -> list[str]:
        """
        Suggest concrete improvement actions.

        Examples:
        - "Consider re-indexing skills (stale_ratio=25%)"
        - "Review failed patches in session X"
        - "Budget entering Red zone frequently - increase limits?"
        """
        ...

    def generate_report(self) -> str:
        """
        Generate self-evaluation report.

        Format:
            [SELF-EVAL] Performance Report
            - Health Score: 78 (Good)
            - Top Issue: High rollback rate (15%)
            - Suggestion: Review error detection logic
            - Top Strength: Low token usage (avg 2000/task)
        """
        ...

    def establish_baseline(self) -> None:
        """
        Compute baseline from first 50 successful tasks.
        Used for anomaly detection.
        """
        ...
```

### Data Models

```python
@dataclass
class TaskMetrics:
    success: bool
    patches_count: int
    rollback_triggered: bool
    tokens_used: int
    no_op_patch: bool
    timestamp: datetime

@dataclass
class DerivedMetrics:
    avg_patches_per_success: float
    rollback_rate: float
    no_op_patch_rate: float
    slm_vs_llm_ratio: float
    token_per_task: float

@dataclass
class BaselineMetrics:
    avg_tokens: float
    avg_patches: float
    success_rate: float
    established_at: datetime
```

### Integration with Orchestrator

```python
# In Orchestrator.__init__()
self.health_monitor = HealthMonitor()

# In Orchestrator.execute() - finally block
finally:
    # Record task metrics
    self.health_monitor.record_task(
        success=(result["status"] == "success"),
        patches_count=repair_count,
        rollback_triggered=rollback_occurred,
        tokens_used=self.budget_guard._tokens_used,
        no_op_patch=no_op_detected
    )

    # Compute health score every 10 tasks
    if self.health_monitor._task_history.count() % 10 == 0:
        score = self.health_monitor.compute_health_score()
        category = self.health_monitor.categorize_health(score)
        logger.info(f"[HEALTH] Score: {score:.1f} ({category})")

        # Check for anomalies
        anomalies = self.health_monitor.detect_anomalies()
        if anomalies:
            logger.warning(f"[HEALTH] Anomalies detected: {anomalies}")

        # Suggest actions
        suggestions = self.health_monitor.suggest_actions()
        if suggestions:
            logger.info(f"[HEALTH] Suggestions: {suggestions}")
```

---

## Testing Strategy

### Unit Tests (per component)

1. **IndexManager**: 15 tests
   - detect_changes() accuracy
   - stale_ratio calculation
   - incremental reindex
   - checkpoint save/load
   - rollback functionality

2. **ErrorPrioritizer**: 12 tests
   - priority classification
   - error chain detection
   - clustering accuracy
   - context size estimation

3. **FailureMemory**: 18 tests
   - record/search operations
   - pattern extraction
   - similarity search accuracy
   - TTL expiration
   - persistence

4. **BudgetStrategy**: 10 tests
   - zone detection
   - strategy selection
   - zone transitions
   - config application

5. **HealthMonitor**: 15 tests
   - health score computation
   - derived metrics
   - anomaly detection
   - baseline establishment
   - report generation

### Integration Tests

1. **Index Lifecycle**: Test full reindex flow
2. **Learning Loop**: Test failure memory injection
3. **Budget Adaptation**: Test strategy switching
4. **Health Monitoring**: Test end-to-end metrics

### Property-Based Tests

1. **Health Score Monotonicity**: Better metrics → higher score
2. **Strategy Consistency**: Same zone → same strategy
3. **Memory Similarity**: Similar errors → similar patterns

---

## Migration Path

### Phase 1: Foundation (Week 1)
- Implement IndexManager
- Implement ErrorPrioritizer
- Unit tests

### Phase 2: Learning (Week 2)
- Implement FailureMemory
- Integrate with Orchestrator
- Integration tests

### Phase 3: Adaptation (Week 3)
- Implement BudgetStrategy
- Implement HealthMonitor
- Full system tests

### Phase 4: Validation (Week 4)
- Real workload testing
- Performance tuning
- Documentation

---

## Success Metrics

| Metric | v6.1 Baseline | v6.2 Target |
|--------|---------------|-------------|
| Retry reduction rate | N/A | > 30% |
| Health score | N/A | > 70 consistently |
| Token savings | N/A | > 20% |
| Silent failures | Unknown | 0 (detected) |
| Index staleness | Unknown | < 20% |

---

**Version:** v6.2.0-RESILIENCE-UPGRADE
**Philosophy:** Observable → Self-Evaluable → Self-Improving
**Target:** Autonomous debugging runtime with learning capability
