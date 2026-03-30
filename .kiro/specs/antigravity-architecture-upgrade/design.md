# Tài Liệu Thiết Kế: Antigravity Architecture Upgrade

## Tổng Quan

Tài liệu này mô tả thiết kế kỹ thuật cho việc nâng cấp kiến trúc Antigravity AI Agent Framework từ v6.0.0-SOLID-STATE lên kiến trúc 3-layer mới. Mục tiêu là cải thiện chất lượng retrieval, giảm token rác, tăng độ tin cậy verification, tối ưu chi phí LLM, và kích hoạt full observability — trong khi duy trì backward compatibility hoàn toàn với orchestrator hiện tại.

### Phạm Vi Thay Đổi

Hệ thống hiện tại (`scripts/orchestrator.py`) sử dụng vòng lặp while đơn giản với keyword-only retrieval, raw error logs, và TracingService skeleton chưa kích hoạt. Bản nâng cấp này bổ sung 5 component mới và nâng cấp 3 component hiện có mà không phá vỡ interface `retrieve(task, errors)` hay execution loop.

### Quyết Định Thiết Kế Quan Trọng

- **Không dùng GraphRAG hay LangGraph**: Tránh over-engineering. BM25 + cosine similarity đủ cho use case hiện tại.
- **Backward compatible**: `SkillStore.retrieve(task, errors)` giữ nguyên signature.
- **Graceful degradation**: Mọi optional dependency (sentence-transformers, langfuse) đều có NoOp fallback.
- **Budget-first**: `BudgetGuard` enforce TRƯỚC khi gọi LLM, không phải sau.
- **All IDs time-sortable**: UUIDv7 hoặc ULID cho tất cả system-generated IDs.

---

## Kiến Trúc

### 3-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CONTROL PLANE                            │
│                                                                 │
│   ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│   │   Orchestrator  │  │  BudgetGuard │  │   SLMRouter     │  │
│   │  (scripts/)     │◄─┤  (enforce    │  │  (intent        │  │
│   │  execution loop │  │   pre-call)  │  │   classifier)   │  │
│   └────────┬────────┘  └──────────────┘  └────────┬────────┘  │
│            │                                        │           │
└────────────┼────────────────────────────────────────┼───────────┘
             │                                        │
┌────────────▼────────────────────────────────────────▼───────────┐
│                      INTELLIGENCE PLANE                          │
│                                                                  │
│   ┌──────────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│   │  HybridRetriever │  │ ASTAnalyzer │  │   LLMClient      │  │
│   │  BM25 + cosine   │  │ tree-sitter │  │  prefix-cached   │  │
│   │  (replaces       │  │ JSON contract│  │  static prefix   │  │
│   │   keyword-only)  │  │             │  │                  │  │
│   └──────────────────┘  └─────────────┘  └──────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────────────────┐
│                      RELIABILITY PLANE                            │
│                                                                   │
│   ┌──────────────────────┐  ┌──────────────┐  ┌──────────────┐  │
│   │  DeterministicChecker│  │ BackupManager│  │TracingService│  │
│   │  + ErrorDelta        │  │ atomic ops   │  │ Langfuse     │  │
│   │  (nâng cấp checker   │  │ session/op   │  │ full spans   │  │
│   │   hiện có)           │  │ hierarchy    │  │              │  │
│   └──────────────────────┘  └──────────────┘  └──────────────┘  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Data Flow: Full Execution Loop

```
User Task
    │
    ▼
[BudgetGuard.check_pre_call()]  ← ENFORCE TRƯỚC
    │ budget OK
    ▼
[SLMRouter.classify(task)]
    ├─ confidence >= 0.85 → RouteDecision (no LLM call)
    └─ confidence < 0.85  → LLMClient.generate_structured(RouteDecision)
    │
    ▼
[HybridRetriever.retrieve(task, errors)]
    │ → ranked Skill list
    ▼
[ASTAnalyzer.analyze(files, error_lines)]
    │ → ASTContract (JSON, ≤4KB)
    ▼
[LLMClient.generate_structured(ExecutionPlan)]
    │ static_prefix cached
    ▼
[BackupManager.create_backup(session_id, operation_id, files)]
    │
    ▼
[ActionDispatcher.dispatch(steps)]
    │
    ▼
[DeterministicChecker.examine() → ErrorDelta]
    ├─ net_improvement=True  → continue / complete
    └─ net_improvement=False → [BackupManager.rollback(operation_id)]
                                    │
                                    ▼
                              [replan_repair(task, error_delta)]
                                    │
                                    └─ loop (max_repair_attempts)
    │
    ▼
[TracingService.flush()]
[BudgetGuard.finalize()]
```

---

## Components và Interfaces

### 1. HybridRetriever (`core/hybrid_retriever.py`)

Thay thế logic keyword-only trong `SkillStore.retrieve()`. Kết hợp BM25 sparse search và dense embedding search.

```python
class HybridRetriever:
    def __init__(
        self,
        skills_dir: Path,
        alpha: float = 0.5,   # BM25 weight
        beta: float = 0.5,    # cosine weight
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        # Graceful degradation: nếu sentence-transformers không có
        # thì _dense_available = False, chỉ dùng BM25
        ...

    def index(self, documents: list[SkillDocument]) -> None:
        """Build BM25 index và embedding matrix. Gọi một lần khi khởi tạo."""
        ...

    def retrieve(
        self,
        query: str,
        errors: list[str] | None = None,
        domain_filter: str | None = None,
        top_k: int = 5,
    ) -> list[RankedSkill]:
        """
        Public interface — backward compatible với SkillStore.retrieve(task, errors).
        Returns ranked list, sorted by final_score descending.
        Tie-breaking: (1) cosine_norm desc, (2) bm25_norm desc, (3) skill_id lexicographic.
        """
        ...

    def _normalize_bm25(self, scores: list[float]) -> list[float]:
        """Min-max normalization → [0, 1]."""
        ...

    def _normalize_cosine(self, scores: list[float]) -> list[float]:
        """(score + 1) / 2 → [0, 1]."""
        ...
```

**Integration point**: `SkillStore.__init__()` khởi tạo `HybridRetriever` và delegate `retrieve()` call. Interface bên ngoài không thay đổi.

**Graceful degradation**: Nếu `import sentence_transformers` raise `ImportError`, set `_dense_available = False`, log warning, chỉ dùng BM25. `beta` bị ignore.

---

### 2. ASTAnalyzer (`core/ast_analyzer.py`)

Parse Python source files thành JSON contract thu gọn, thay thế raw file content trong repair prompts.

```python
class ASTAnalyzer:
    def __init__(self):
        # Lazy import tree_sitter; nếu không có thì fallback mode
        ...

    def analyze(
        self,
        targets: list[tuple[str, int]],  # [(file_path, error_line), ...]
    ) -> ASTContract:
        """
        Multi-file entry point. Trả về consolidated ASTContract.
        Hard limit: serialized JSON ≤ 4096 bytes.
        """
        ...

    def _parse_file(self, file_path: str, error_line: int) -> list[ASTNode]:
        """
        Extract nodes trong phạm vi ±10 lines của error_line.
        node_id format: "filename.py::function_name::start_line"
        """
        ...

    def _fallback_excerpt(self, file_path: str, error_line: int) -> ASTContract:
        """
        Khi tree-sitter parse fail: trả về raw excerpt ≤ 200 tokens.
        """
        ...
```

**Integration point**: `Orchestrator.replan_repair()` gọi `ASTAnalyzer.analyze()` thay vì đọc raw file content trước khi construct repair prompt.

---

### 3. BudgetGuard (`core/budget_guard.py`)

Enforce execution budget TRƯỚC mỗi LLM call. Không phải sau.

```python
class BudgetGuard:
    def __init__(
        self,
        max_steps: int = 50,
        max_tokens: int = 100_000,
        max_repair_attempts: int = 5,
    ):
        self._steps_used: int = 0
        self._tokens_used: int = 0
        self._repairs_used: int = 0

    def check_pre_call(
        self,
        estimated_input_tokens: int,
        max_expected_output_tokens: int,
    ) -> None:
        """
        Raise BudgetExceededError nếu remaining_budget < estimated_cost.
        estimated_cost = static_prefix_tokens + dynamic_suffix_tokens + max_expected_output_tokens
        Gọi TRƯỚC khi invoke LLMClient.
        """
        ...

    def record_call(self, actual_tokens: int) -> None:
        """Cộng dồn token usage sau mỗi LLM call thành công."""
        ...

    def record_step(self) -> None:
        """Increment step counter."""
        ...

    def record_repair(self) -> None:
        """Increment repair counter."""
        ...

    def get_status(self) -> BudgetStatus:
        """Queryable mid-session. Trả về snapshot hiện tại."""
        ...

    def _warn_if_approaching(self) -> None:
        """Log warning khi usage >= 80% của bất kỳ limit nào."""
        ...
```

**Integration point**: `Orchestrator.execute()` khởi tạo `BudgetGuard` và gọi `check_pre_call()` trước mỗi `llm.generate_structured()` / `llm.generate_text()`.

---

### 4. SLMRouter (`core/slm_router.py`)

Phân loại intent bằng cosine similarity với prototype embeddings. Tiết kiệm LLM call cho routing step.

```python
class SLMRouter:
    def __init__(
        self,
        prototypes_path: Path,
        confidence_threshold: float = 0.85,
    ):
        # Nếu sentence-transformers không load được: _enabled = False
        ...

    def classify(self, query: str) -> SLMRouteDecision | None:
        """
        Returns SLMRouteDecision nếu confidence >= threshold.
        Returns None nếu confidence < threshold (fall through to LLM).
        Returns None nếu _enabled = False.
        Idempotent: classify(x) == classify(classify(x).chosen) nếu called twice.
        """
        ...

    def reload_prototypes(self) -> None:
        """Hot-reload prototypes từ JSON file mà không restart."""
        ...
```

**Integration point**: `Orchestrator.route_task()` thử `SLMRouter.classify()` trước. Nếu trả về `None`, fall through sang `LLMClient.generate_structured(RouteDecision)` như hiện tại.

---

### 5. BackupManager (`core/backup_manager.py`)

Atomic backup và rollback cho files trước mỗi patch attempt.

```python
class BackupManager:
    def __init__(self, backup_root: Path):
        # backup_root = antigravity/backups/
        ...

    def create_backup(
        self,
        session_id: str,
        operation_id: str,
        file_paths: list[str],
    ) -> None:
        """
        Copy files vào backup_root/{session_id}/{operation_id}/.
        Idempotent: backup cùng file trong cùng operation_id → overwrite.
        """
        ...

    def rollback(self, session_id: str, operation_id: str) -> None:
        """
        Restore files từ backup. Nếu backup missing → log critical warning, không crash.
        """
        ...

    def _backup_path(self, session_id: str, operation_id: str) -> Path:
        ...
```

**Integration point**: `Orchestrator.execute()` gọi `BackupManager.create_backup()` trước mỗi `ActionDispatcher.dispatch()`. Khi `ErrorDelta.net_improvement = False`, gọi `BackupManager.rollback()`.

---

### 6. LLMClient — Nâng Cấp Prefix Caching (`core/llm_client.py`)

Bổ sung `set_static_prefix()` và tách prompt thành `static_prefix` + `dynamic_suffix`.

```python
# Thêm vào LLMClient hiện có:

def set_static_prefix(self, content: str) -> None:
    """
    Inject CONSTITUTION + MASTER_ROUTER content.
    Gọi một lần khi Orchestrator khởi tạo.
    Log warning nếu prefix thay đổi sau lần đầu.
    """
    ...

def _build_system_prompt(self, dynamic_suffix: str) -> str | list:
    """
    Ghép static_prefix + dynamic_suffix.
    Với Anthropic: thêm cache_control annotation vào static_prefix block.
    """
    ...
```

---

### 7. DeterministicChecker — Nâng Cấp ErrorDelta (`core/checker.py`)

Bổ sung `ErrorDelta` return type cho `examine()`.

```python
# examine() hiện tại trả về list[str] errors
# Nâng cấp: trả về ErrorDelta

def examine(
    self,
    checks: list[ArtifactCheck],
    previous_errors: list[str] | None = None,
    project_root: str | Path = None,
) -> ErrorDelta:
    """
    Backward compatible: nếu previous_errors=None, ErrorDelta.net_improvement=True
    khi errors rỗng (giống behavior cũ).
    """
    ...
```

---

### 8. TracingService — Kích Hoạt Langfuse (`core/tracing.py`)

Skeleton đã có. Cần bổ sung:
- `log_generation()` với đầy đủ fields (model, tokens, latency, task_name)
- `log_replan_triggered(error_delta)` event
- `link_patch_metadata(patch_id, error_delta, rollback_triggered)` trong span
- `score()` call khi session kết thúc
- `flush()` đảm bảo được gọi trong `finally` block

---

## Data Models

Tất cả models dùng Pydantic v2. Tất cả IDs dùng UUIDv7 hoặc ULID.

```python
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
import re

# ── ID Utilities ──────────────────────────────────────────────────────────────

ULID_PATTERN = re.compile(r"^[0-9A-Z]{26}$")
UUIDV7_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

def is_valid_time_sortable_id(id_str: str) -> bool:
    return bool(ULID_PATTERN.match(id_str) or UUIDV7_PATTERN.match(id_str))


# ── Requirement 1: HybridRetriever ───────────────────────────────────────────

class SkillDocument(BaseModel):
    skill_id: str
    name: str
    content: str
    domain_tags: list[str] = Field(default_factory=list)
    file_path: str

class RankedSkill(BaseModel):
    skill: "Skill"  # existing Skill model
    bm25_norm: float = Field(ge=0.0, le=1.0)
    cosine_norm: float = Field(ge=0.0, le=1.0)
    final_score: float = Field(ge=0.0, le=1.0)


# ── Requirement 2: ASTAnalyzer ────────────────────────────────────────────────

class ASTNode(BaseModel):
    node_id: str  # format: "file.py::function_name::start_line"
    file_path: str
    function_name: str | None = None
    class_name: str | None = None
    start_line: int
    end_line: int
    scope_path: str  # e.g. "MyClass.my_method"
    signature: str | None = None  # "def foo(x: int) -> str"

    @field_validator("node_id")
    @classmethod
    def validate_node_id_format(cls, v: str) -> str:
        parts = v.split("::")
        if len(parts) != 3:
            raise ValueError(f"node_id must be 'file::function::line', got: {v}")
        return v

class ASTContract(BaseModel):
    """
    JSON contract thu gọn thay thế raw file content trong repair prompts.
    Hard limit: serialized JSON ≤ 4096 bytes.
    """
    error_type: str
    affected_nodes: list[ASTNode]
    raw_excerpt: str | None = None  # chỉ khi fallback mode
    is_fallback: bool = False
    source_files: list[str]
    total_size_bytes: int = 0  # populated after serialization


# ── Requirement 3: ErrorDelta ─────────────────────────────────────────────────

ERROR_WEIGHTS: dict[str, int] = {
    "syntax_error": 10,
    "runtime_error": 7,
    "lint_warning": 1,
}

class ErrorDelta(BaseModel):
    operation_id: str  # UUIDv7 or ULID
    errors_resolved: list[str] = Field(default_factory=list)
    errors_introduced: list[str] = Field(default_factory=list)
    old_error_score: float = Field(ge=0.0)
    new_error_score: float = Field(ge=0.0)
    net_improvement: bool  # True khi new_error_score <= old_error_score

    @field_validator("operation_id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not is_valid_time_sortable_id(v):
            raise ValueError(f"operation_id must be UUIDv7 or ULID: {v}")
        return v

    @classmethod
    def compute_score(cls, errors: list[str]) -> float:
        """
        error_score = Σ(weight[type] * count)
        Classify errors by keyword matching vào syntax_error / runtime_error / lint_warning.
        """
        score = 0.0
        for err in errors:
            err_lower = err.lower()
            if any(k in err_lower for k in ["syntaxerror", "syntax error", "invalid syntax"]):
                score += ERROR_WEIGHTS["syntax_error"]
            elif any(k in err_lower for k in ["runtimeerror", "traceback", "exception", "error:"]):
                score += ERROR_WEIGHTS["runtime_error"]
            else:
                score += ERROR_WEIGHTS["lint_warning"]
        return score


# ── Requirement 4: SLMRouter ──────────────────────────────────────────────────

class SLMRouteDecision(BaseModel):
    chosen: str  # category label, maps to RouteDecision.domain
    confidence: float = Field(ge=0.0, le=1.0)
    top_k: list[dict[str, float]] = Field(
        default_factory=list,
        description='[{"label": "frontend", "score": 0.92}, ...]'
    )
    llm_fallback_triggered: bool = False


# ── Requirement 7: BudgetGuard ────────────────────────────────────────────────

class BudgetStatus(BaseModel):
    steps_used: int
    steps_remaining: int
    tokens_used: int
    tokens_remaining: int
    repairs_used: int
    repairs_remaining: int
    warning_threshold_reached: bool  # True khi bất kỳ dimension nào >= 80%
    termination_reason: str | None = None  # populated khi budget exceeded


# ── Requirement 8: Global ID Invariant ───────────────────────────────────────

class SessionContext(BaseModel):
    """Metadata gắn với mỗi Orchestrator session."""
    session_id: str   # UUIDv7 or ULID
    notebook_id: str | None = None
    trace_id: str | None = None  # UUIDv7 or ULID

    @field_validator("session_id", "trace_id")
    @classmethod
    def validate_time_sortable(cls, v: str | None) -> str | None:
        if v is not None and not is_valid_time_sortable_id(v):
            raise ValueError(f"ID must be UUIDv7 or ULID: {v}")
        return v
```

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

---

### Property 1: Score Normalization và Ranking Invariant

*For any* query và skill corpus, tất cả `bm25_norm` và `cosine_norm` scores trong kết quả trả về của `HybridRetriever.retrieve()` phải nằm trong `[0.0, 1.0]`, và `final_score = α * bm25_norm + β * cosine_norm` phải đúng với mọi item. Danh sách kết quả phải được sắp xếp giảm dần theo `final_score`.

**Validates: Requirements 1.2, 1.3**

---

### Property 2: Monotonicity của Alpha/Beta Weights

*For any* query, skill corpus, và hai cấu hình `(α1, β1)` và `(α2, β2)` với `α2 > α1` (và `β` giữ nguyên), ranking contribution của BM25 phải tăng đơn điệu. Cụ thể: với mọi skill `s`, `α2 * bm25_norm(s) >= α1 * bm25_norm(s)`.

**Validates: Requirements 1.9**

---

### Property 3: Domain Filter Containment

*For any* query với `domain_filter = d`, tất cả skills trong kết quả trả về phải có `d` trong `domain_tags`. Không có skill nào thuộc domain khác được xuất hiện trong kết quả.

**Validates: Requirements 1.4**

---

### Property 4: Deterministic Tie-Breaking

*For any* tập skills với identical `final_score`, gọi `retrieve()` nhiều lần với cùng inputs phải luôn trả về cùng thứ tự. Thứ tự tie-breaking: `cosine_norm` desc → `bm25_norm` desc → `skill_id` lexicographic asc.

**Validates: Requirements 1.11**

---

### Property 5: ASTContract Size Invariant

*For any* Python file và error message, `ASTContract` được serialize thành JSON phải có kích thước `≤ 4096 bytes`. Nếu vượt quá, analyzer phải truncate `affected_nodes` cho đến khi thỏa mãn constraint.

**Validates: Requirements 2.2**

---

### Property 6: ASTContract Compression Ratio

*For any* Python file có kích thước `S` bytes, kích thước `ASTContract` serialized phải `≤ 0.3 * S` (giảm ít nhất 70%). Nếu file quá nhỏ (< 100 bytes), property này không áp dụng.

**Validates: Requirements 2.3**

---

### Property 7: Node ID Format Invariant

*For any* Python file được parse bởi `ASTAnalyzer`, tất cả `node_id` trong `ASTContract.affected_nodes` phải match format `"<filename>::<function_name>::<start_line>"` — ba phần phân cách bởi `::`, phần cuối là số nguyên dương.

**Validates: Requirements 2.7**

---

### Property 8: AST Referential Integrity

*For any* Python file và `ASTContract` được tạo từ file đó, mọi `node_id` trong contract phải tham chiếu đến một node thực sự tồn tại trong AST của file gốc (tức là `start_line` phải nằm trong range hợp lệ của file, và `function_name` phải là tên function thực sự xuất hiện tại dòng đó).

**Validates: Requirements 2.8**

---

### Property 9: ErrorDelta Score Computation

*For any* danh sách errors, `ErrorDelta.compute_score(errors)` phải bằng `Σ(weight[type] * count)` với weights `syntax_error=10, runtime_error=7, lint_warning=1`. Thêm một error vào list phải tăng score đúng bằng weight của error type đó.

**Validates: Requirements 3.1**

---

### Property 10: Rollback Round-Trip Invariant

*For any* file `f` và patch operation `p`, nếu `BackupManager.create_backup()` được gọi trước khi apply `p`, thì sau khi `BackupManager.rollback()` được gọi, nội dung của `f` phải identical với nội dung trước khi apply `p` (so sánh bằng SHA-256 hash).

**Validates: Requirements 3.3, 3.8**

---

### Property 11: Backup Idempotence

*For any* `session_id`, `operation_id`, và file `f`, gọi `BackupManager.create_backup()` nhiều lần với cùng `operation_id` phải chỉ tạo một bản backup duy nhất (overwrite, không duplicate). Số lượng files trong `backup_root/{session_id}/{operation_id}/` phải bằng số unique files được backup.

**Validates: Requirements 3.7**

---

### Property 12: Error Normalization Stability

*For any* hai error strings `e1` và `e2` có cùng root cause nhưng khác nhau về file path hoặc timestamp, `_normalize_errors([e1]) == _normalize_errors([e2])` phải là `True`. Normalization phải loại bỏ paths, timestamps, hex addresses, và standalone numbers.

**Validates: Requirements 3.5**

---

### Property 13: SLM Routing Idempotence

*For any* intent string `i`, gọi `SLMRouter.classify(i)` nhiều lần phải luôn trả về cùng `chosen` category (khi prototype embeddings không thay đổi). `classify(classify(i).chosen) == classify(i).chosen`.

**Validates: Requirements 4.8**

---

### Property 14: SLM Confidence Threshold Routing

*For any* query, nếu `SLMRouter.classify()` trả về `confidence >= threshold`, thì `LLMClient` không được gọi cho routing step. Nếu `confidence < threshold` hoặc `SLMRouter` disabled, `LLMClient` phải được gọi như bình thường.

**Validates: Requirements 4.2, 4.3**

---

### Property 15: Static Prefix Invariant

*For any* hai LLM calls `c1` và `c2` trong cùng session với cùng `static_prefix`, phần prefix trong system message của cả hai calls phải identical (byte-for-byte). Dynamic suffix có thể khác nhau.

**Validates: Requirements 5.6, 5.8**

---

### Property 16: Trace Fields Completeness

*For any* LLM generation call được log bởi `TracingService`, span phải chứa đầy đủ: `model`, `input_tokens`, `output_tokens`, `latency_ms`, `task_name`. Nếu bất kỳ field nào là `None` (do API không trả về), field đó phải được log là `None` chứ không phải bị bỏ qua.

**Validates: Requirements 6.2, 6.5**

---

### Property 17: Budget Pre-Call Enforcement

*For any* trạng thái `BudgetGuard` với `remaining_token_budget < estimated_call_cost`, `check_pre_call()` phải raise `BudgetExceededError` và LLM call phải không được thực hiện. `estimated_call_cost = static_prefix_tokens + dynamic_suffix_tokens + max_expected_output_tokens`.

**Validates: Requirements 7.7**

---

### Property 18: Budget Termination với Reason

*For any* session, khi bất kỳ budget limit nào bị vượt (`steps > max_steps`, `tokens > max_tokens`, hoặc `repairs > max_repair_attempts`), execution phải terminate và `BudgetStatus.termination_reason` phải chỉ rõ dimension nào bị vượt.

**Validates: Requirements 7.2**

---

### Property 19: Token Accumulation Additivity

*For any* sequence của `n` LLM calls với token counts `[t1, t2, ..., tn]`, `BudgetGuard._tokens_used` sau tất cả calls phải bằng `Σ(ti)`. Token tracking phải additive và không bị mất.

**Validates: Requirements 7.3**

---

### Property 20: Time-Sortable ID Invariant

*For any* tập IDs `{id1, id2, ..., idN}` được generate trong một session theo thứ tự thời gian `t1 < t2 < ... < tN`, sắp xếp IDs theo lexicographic order phải cho cùng thứ tự `id1 < id2 < ... < idN`. Áp dụng cho `session_id`, `operation_id`, `patch_id`, `trace_id`.

**Validates: Requirements 8.1, 8.3**

---

## Error Handling

### Graceful Degradation Matrix

| Component | Failure Condition | Behavior |
|-----------|------------------|----------|
| `HybridRetriever` | `sentence-transformers` không install | Fall back to BM25-only, log WARNING, `_dense_available=False` |
| `SLMRouter` | `sentence-transformers` load fail | `_enabled=False`, Orchestrator dùng LLMClient routing như cũ |
| `ASTAnalyzer` | `tree-sitter` parse fail (syntax error nặng) | Return fallback `ASTContract` với raw excerpt ≤ 200 tokens, `is_fallback=True` |
| `BackupManager` | Backup files missing khi rollback | Log CRITICAL warning, continue without rollback (không crash) |
| `TracingService` | Langfuse credentials missing/invalid | NoOp behavior (đã có), không raise exception |
| `BudgetGuard` | Config missing/incomplete | Apply safe defaults: `max_steps=50, max_tokens=100_000, max_repair_attempts=5` |
| `LLMClient` | `static_prefix` thay đổi giữa các calls | Log WARNING về cache invalidation |

### Error Propagation

```
BudgetExceededError
    └─ Raised bởi BudgetGuard.check_pre_call()
    └─ Caught bởi Orchestrator.execute()
    └─ Emit final trace event với termination_reason
    └─ Return {"status": "budget_exceeded", "reason": "<dimension>"}

RollbackError (non-fatal)
    └─ Raised bởi BackupManager.rollback() khi backup missing
    └─ Caught bởi Orchestrator, log CRITICAL
    └─ Continue execution (không crash)

ASTParseError (non-fatal)
    └─ Raised bởi ASTAnalyzer._parse_file()
    └─ Caught internally, return fallback ASTContract
    └─ Orchestrator nhận ASTContract.is_fallback=True, vẫn tiếp tục

InvalidIDError
    └─ Raised bởi Pydantic validator khi ID không phải UUIDv7/ULID
    └─ Orchestrator generate compliant replacement ID
    └─ Log WARNING với invalid_id_format event
```

### No-Op Patch Detection

Trước khi gọi `DeterministicChecker`, Orchestrator tính SHA-256 hash của tất cả files sẽ bị modify. Nếu hash sau patch == hash trước patch, emit `no_op_patch_detected` event và request replan ngay lập tức mà không chạy checker.

```python
# Pseudo-code trong Orchestrator.execute()
pre_hash = {f: sha256(f) for f in modified_files}
dispatcher.dispatch(steps)
post_hash = {f: sha256(f) for f in modified_files}

if pre_hash == post_hash:
    tracer.log_event("no_op_patch_detected")
    # skip checker, request replan
    continue
```

---

## Testing Strategy

### Dual Testing Approach

Mỗi component cần cả unit tests (ví dụ cụ thể, edge cases) lẫn property-based tests (universal properties). Hai loại bổ sung cho nhau: unit tests bắt concrete bugs, property tests verify general correctness.

**Property-Based Testing Library**: [`hypothesis`](https://hypothesis.readthedocs.io/) cho Python.

```bash
pip install hypothesis pytest
```

**Cấu hình**: Minimum 100 iterations mỗi property test (`@settings(max_examples=100)`).

**Tag format**: Mỗi property test phải có comment:
```python
# Feature: antigravity-architecture-upgrade, Property N: <property_text>
```

---

### Unit Tests (Ví Dụ Cụ Thể và Edge Cases)

```
tests/
├── test_hybrid_retriever.py
│   ├── test_backward_compatible_interface()       # Req 1.6: retrieve(task, errors) vẫn hoạt động
│   ├── test_index_skills_directory()              # Req 1.8: index tất cả .md files
│   ├── test_semantic_overlap_fixed_pairs()        # Req 1.10: fixed query pairs có overlapping results
│   └── test_fallback_when_no_sentence_transformers()  # Req 1.7: edge case
│
├── test_ast_analyzer.py
│   ├── test_fallback_on_broken_file()             # Req 2.4: edge case
│   ├── test_multi_file_consolidated_contract()    # Req 2.9: multi-file input
│   └── test_functions_in_range()                 # Req 2.5: ±10 lines
│
├── test_budget_guard.py
│   ├── test_safe_defaults_when_no_config()        # Req 7.6: edge case
│   ├── test_get_status_mid_session()              # Req 7.8: queryable
│   └── test_escalate_to_hitl_on_max_repairs()    # Req 7.4
│
├── test_slm_router.py
│   ├── test_hot_reload_prototypes()               # Req 4.4
│   └── test_disabled_when_model_fails()           # Req 4.6: edge case
│
├── test_tracing_service.py
│   ├── test_noop_when_no_credentials()            # Req 6.7: edge case
│   ├── test_langfuse_init_when_env_present()      # Req 6.1: example
│   └── test_flush_called_on_session_end()         # Req 6.8
│
└── test_llm_client_prefix.py
    └── test_set_static_prefix_method_exists()     # Req 5.5: example
```

---

### Property-Based Tests

```python
# tests/property_tests/test_hybrid_retriever_props.py

from hypothesis import given, settings, strategies as st

@given(
    query=st.text(min_size=1, max_size=200),
    alpha=st.floats(min_value=0.0, max_value=1.0),
    beta=st.floats(min_value=0.0, max_value=1.0),
)
@settings(max_examples=100)
def test_score_normalization_and_ranking(query, alpha, beta):
    # Feature: antigravity-architecture-upgrade, Property 1: Score normalization và ranking invariant
    retriever = HybridRetriever(skills_dir=TEST_SKILLS_DIR, alpha=alpha, beta=beta)
    results = retriever.retrieve(query)
    for r in results:
        assert 0.0 <= r.bm25_norm <= 1.0
        assert 0.0 <= r.cosine_norm <= 1.0
        assert abs(r.final_score - (alpha * r.bm25_norm + beta * r.cosine_norm)) < 1e-6
    scores = [r.final_score for r in results]
    assert scores == sorted(scores, reverse=True)


@given(
    query=st.text(min_size=1),
    alpha1=st.floats(min_value=0.0, max_value=0.5),
    alpha2=st.floats(min_value=0.5, max_value=1.0),
    beta=st.floats(min_value=0.0, max_value=1.0),
)
@settings(max_examples=100)
def test_alpha_monotonicity(query, alpha1, alpha2, beta):
    # Feature: antigravity-architecture-upgrade, Property 2: Monotonicity của alpha/beta weights
    r1 = HybridRetriever(skills_dir=TEST_SKILLS_DIR, alpha=alpha1, beta=beta)
    r2 = HybridRetriever(skills_dir=TEST_SKILLS_DIR, alpha=alpha2, beta=beta)
    results1 = {r.skill.name: r for r in r1.retrieve(query)}
    results2 = {r.skill.name: r for r in r2.retrieve(query)}
    for name in results1:
        if name in results2:
            assert alpha2 * results2[name].bm25_norm >= alpha1 * results1[name].bm25_norm


@given(
    file_content=st.text(min_size=10, max_size=5000),
    error_line=st.integers(min_value=1, max_value=100),
)
@settings(max_examples=100)
def test_ast_contract_size_invariant(file_content, error_line):
    # Feature: antigravity-architecture-upgrade, Property 5: ASTContract size invariant
    analyzer = ASTAnalyzer()
    contract = analyzer.analyze([(write_temp_file(file_content), error_line)])
    serialized = contract.model_dump_json()
    assert len(serialized.encode("utf-8")) <= 4096


@given(errors=st.lists(st.text(min_size=1, max_size=200), min_size=0, max_size=20))
@settings(max_examples=100)
def test_error_score_additivity(errors):
    # Feature: antigravity-architecture-upgrade, Property 9: ErrorDelta score computation
    total = ErrorDelta.compute_score(errors)
    # Thêm một syntax error phải tăng score đúng 10
    new_errors = errors + ["SyntaxError: invalid syntax"]
    new_total = ErrorDelta.compute_score(new_errors)
    assert new_total == total + 10


@given(
    file_content=st.text(min_size=1, max_size=10000),
    patch_content=st.text(min_size=1, max_size=10000),
)
@settings(max_examples=100)
def test_rollback_round_trip(file_content, patch_content):
    # Feature: antigravity-architecture-upgrade, Property 10: Rollback round-trip invariant
    with temp_file(file_content) as f:
        manager = BackupManager(backup_root=TEMP_BACKUP_DIR)
        session_id, op_id = new_ulid(), new_ulid()
        manager.create_backup(session_id, op_id, [f])
        f.write_text(patch_content)
        manager.rollback(session_id, op_id)
        assert f.read_text() == file_content


@given(query=st.text(min_size=1, max_size=200))
@settings(max_examples=100)
def test_slm_router_idempotence(query):
    # Feature: antigravity-architecture-upgrade, Property 13: SLM routing idempotence
    router = SLMRouter(prototypes_path=TEST_PROTOTYPES)
    result1 = router.classify(query)
    if result1 is not None:
        result2 = router.classify(result1.chosen)
        assert result2 is not None
        assert result2.chosen == result1.chosen


@given(
    tokens_used=st.integers(min_value=0, max_value=90_000),
    estimated_input=st.integers(min_value=1000, max_value=5000),
    max_output=st.integers(min_value=500, max_value=2000),
)
@settings(max_examples=100)
def test_budget_pre_call_enforcement(tokens_used, estimated_input, max_output):
    # Feature: antigravity-architecture-upgrade, Property 17: Budget pre-call enforcement
    guard = BudgetGuard(max_tokens=100_000)
    guard._tokens_used = tokens_used
    estimated_cost = estimated_input + max_output
    remaining = 100_000 - tokens_used
    if remaining < estimated_cost:
        with pytest.raises(BudgetExceededError):
            guard.check_pre_call(estimated_input, max_output)
    else:
        guard.check_pre_call(estimated_input, max_output)  # không raise


@given(
    token_counts=st.lists(st.integers(min_value=0, max_value=5000), min_size=1, max_size=20)
)
@settings(max_examples=100)
def test_token_accumulation_additivity(token_counts):
    # Feature: antigravity-architecture-upgrade, Property 19: Token accumulation additivity
    guard = BudgetGuard(max_tokens=10_000_000)
    for t in token_counts:
        guard.record_call(t)
    assert guard._tokens_used == sum(token_counts)


@given(n_ids=st.integers(min_value=2, max_value=50))
@settings(max_examples=100)
def test_time_sortable_id_invariant(n_ids):
    # Feature: antigravity-architecture-upgrade, Property 20: Time-sortable ID invariant
    import time
    ids = []
    for _ in range(n_ids):
        ids.append(generate_ulid())  # hoặc generate_uuidv7()
        time.sleep(0.001)  # đảm bảo timestamp khác nhau
    lexicographic_order = sorted(ids)
    assert lexicographic_order == ids  # generation order == lexicographic order
```

---

### Integration Tests

```
tests/integration/
├── test_orchestrator_with_budget.py
│   └── test_budget_terminates_before_llm_call()
├── test_orchestrator_rollback_cycle.py
│   └── test_regression_triggers_rollback_and_replan()
└── test_full_execution_loop.py
    └── test_route_plan_execute_check_complete()
```

### Coverage Targets

| Component | Unit | Property | Integration |
|-----------|------|----------|-------------|
| HybridRetriever | ≥ 80% | Properties 1-4 | ✓ |
| ASTAnalyzer | ≥ 80% | Properties 5-8 | ✓ |
| DeterministicChecker + ErrorDelta | ≥ 90% | Properties 9, 12 | ✓ |
| BackupManager | ≥ 90% | Properties 10, 11 | ✓ |
| SLMRouter | ≥ 75% | Properties 13, 14 | ✓ |
| LLMClient (prefix) | ≥ 75% | Property 15 | ✓ |
| TracingService | ≥ 80% | Property 16 | ✓ |
| BudgetGuard | ≥ 90% | Properties 17-19 | ✓ |
| ID utilities | ≥ 95% | Property 20 | ✓ |
