# Tài Liệu Yêu Cầu

## Giới Thiệu

Hệ thống Antigravity AI Agent Framework (v6.0.0-SOLID-STATE) là một orchestrator Python tùy chỉnh với vòng lặp while có khả năng chịu lỗi, tích hợp Instructor + Pydantic cho structured output, và SkillStore dựa trên keyword matching. Tài liệu này mô tả các yêu cầu nâng cấp kiến trúc theo 6 hướng ưu tiên, nhằm cải thiện chất lượng retrieval, giảm token rác, tăng độ tin cậy của verification, tối ưu chi phí LLM, và kích hoạt full observability — trong khi vẫn duy trì backward compatibility với orchestrator hiện tại.

## Bảng Thuật Ngữ

- **SkillStore**: Module `core/skill_store.py` — kho lưu trữ và truy xuất các Skill object.
- **Skill**: Pydantic model đại diện cho một kỹ năng có trigger patterns, plan template, và success criteria.
- **HybridRetriever**: Component mới thay thế phương thức `retrieve()` hiện tại trong SkillStore, kết hợp BM25 và dense embedding.
- **ASTAnalyzer**: Component mới trong `core/` sử dụng py-tree-sitter để parse Python source files thành JSON contract.
- **ErrorDelta**: Pydantic model mới biểu diễn sự thay đổi giữa tập lỗi trước và sau khi áp dụng patch.
- **DeterministicChecker**: Module `core/checker.py` — thực hiện các kiểm tra xác định tính đúng đắn của artifacts.
- **SLMRouter**: Component mới sử dụng model ngôn ngữ nhỏ (SLM) để phân loại intent trước khi chuyển sang LLM lớn.
- **TracingService**: Module `core/tracing.py` — skeleton observability đã có, cần kích hoạt Langfuse.
- **Orchestrator**: `scripts/orchestrator.py` — vòng lặp điều phối chính của hệ thống.
- **LLMClient**: `core/llm_client.py` — abstract adapter cho các LLM provider.
- **Contextual_Retrieval**: Kỹ thuật retrieval nâng cao kết hợp BM25 sparse search và dense embedding search.
- **Prefix_Cache**: Cơ chế cache prompt của Anthropic/OpenAI dựa trên static prefix đứng đầu.
- **RouteDecision**: Pydantic schema cho kết quả routing của orchestrator.
- **ExecutionPlan**: Pydantic schema cho kế hoạch thực thi của orchestrator.
- **operation_id**: Định danh duy nhất cho mỗi thao tác patch/repair — SHALL use UUIDv7 or ULID format để đảm bảo time-sortable ordering.
- **patch_id**: Định danh duy nhất cho mỗi patch artifact — SHALL use UUIDv7 or ULID format.
- **session_id**: Định danh duy nhất cho mỗi phiên làm việc của Orchestrator — SHALL use UUIDv7 or ULID format.
- **trace_id**: Định danh duy nhất cho mỗi trace trong TracingService — SHALL use UUIDv7 or ULID format.

---

## Yêu Cầu

### Yêu Cầu 1: Hybrid Retrieval cho SkillStore

**User Story:** Là một AI agent, tôi muốn truy xuất skills bằng cả keyword matching lẫn semantic similarity, để tôi có thể tìm đúng skill ngay cả khi query không khớp từ khóa chính xác.

#### Tiêu Chí Chấp Nhận

1. THE HybridRetriever SHALL implement BM25 sparse search kết hợp với dense embedding search sử dụng sentence-transformers để tính cosine similarity.
2. WHEN a query is submitted to HybridRetriever, THE HybridRetriever SHALL return a ranked list of Skill objects bằng cách kết hợp BM25 score và cosine similarity score với trọng số có thể cấu hình.
3. THE HybridRetriever SHALL normalize all scores to a common scale before combination: BM25 scores SHALL be normalized to [0,1] via min-max or sigmoid; cosine similarity scores SHALL be normalized to [0,1] via (score+1)/2. Final score SHALL be computed as: `final_score = α * bm25_norm + β * cosine_norm`.
4. THE HybridRetriever SHALL support metadata filtering theo domain tags (ví dụ: "frontend", "backend", "debug") để thu hẹp không gian tìm kiếm trước khi ranking.
5. WHEN a skill document is indexed, THE HybridRetriever SHALL generate a contextual summary bằng cách prepend context của document vào chunk trước khi embedding, theo kỹ thuật Contextual Retrieval.
6. THE SkillStore SHALL expose the same `retrieve(task, errors)` interface như hiện tại để đảm bảo backward compatibility với Orchestrator.
7. IF the sentence-transformers library is not installed, THEN THE HybridRetriever SHALL fall back to keyword-only matching và log một warning message.
8. THE HybridRetriever SHALL index tất cả `.md` files trong thư mục `antigravity/skills/` theo domain tag được suy ra từ đường dẫn thư mục.
9. FOR ANY query, increasing α SHALL monotonically increase the ranking contribution of BM25 scores, and increasing β SHALL monotonically increase the ranking contribution of cosine scores (monotonicity property).
10. FOR ALL queries q1 và q2 có cùng semantic meaning nhưng khác từ khóa, THE HybridRetriever SHALL return overlapping top-3 results với ít nhất 1 skill chung (round-trip semantic property).
11. IF multiple skills have identical final_score, THEN THE HybridRetriever SHALL apply deterministic tie-breaking in this order: (1) higher cosine_norm score, (2) then higher bm25_norm score, (3) then lexicographic order of skill_id — để đảm bảo reproducibility và test stability.

---

### Yêu Cầu 2: AST Code Analysis với Tree-sitter

**User Story:** Là một AI agent, tôi muốn nhận thông tin lỗi dưới dạng JSON contract thu gọn thay vì raw log text, để tôi có thể giảm token rác và tập trung vào đúng vị trí lỗi trong code.

#### Tiêu Chí Chấp Nhận

1. THE ASTAnalyzer SHALL parse Python source files sử dụng py-tree-sitter để trích xuất node coordinates bao gồm: function name, class name, line range, và scope path.
2. WHEN a Python file and an error message are provided, THE ASTAnalyzer SHALL return a JSON contract chứa: file path, error type, affected function name, line range, và scope path — với tổng kích thước thỏa mãn dual constraint: ≤ 500 tokens (approximate, soft limit for LLM context) AND ≤ 4KB serialized JSON (hard limit, enforceable without tokenizer dependency).
3. THE ASTAnalyzer SHALL reduce raw error log size by at least 70% so với việc truyền toàn bộ file content vào LLM prompt.
4. IF a file cannot be parsed by tree-sitter (ví dụ: syntax error quá nặng), THEN THE ASTAnalyzer SHALL return a fallback JSON contract chứa raw error excerpt giới hạn 200 tokens.
5. THE ASTAnalyzer SHALL extract function signatures (name, parameters, return annotation) cho tất cả functions trong phạm vi ±10 lines của dòng lỗi.
6. THE Orchestrator SHALL use ASTAnalyzer output thay vì raw file content khi constructing repair prompts cho LLMClient.
7. THE ASTAnalyzer SHALL assign each node a stable `node_id` theo format `"file.py::function_name::start_line"` để enable diff và cross-session tracking.
8. FOR ALL JSON contracts produced by ASTAnalyzer, ALL node references in the contract MUST map to valid nodes in the original AST (referential integrity property). Note: round-trip equality is NOT guaranteed vì JSON contract là lossy compression.
9. THE ASTAnalyzer SHALL handle multi-file error contexts bằng cách accept một list các (file_path, error_line) tuples và trả về một consolidated JSON contract.

---

### Yêu Cầu 3: Delta Verification và Atomic Backup

**User Story:** Là một AI agent, tôi muốn biết chính xác patch nào tạo ra regression bug mới, để tôi có thể tự động rollback và yêu cầu LLM reasoning lại thay vì tiếp tục với code bị hỏng.

#### Tiêu Chí Chấp Nhận

1. THE DeterministicChecker SHALL return an ErrorDelta object sau mỗi lần `examine()`, chứa: `errors_resolved` (list lỗi đã fix), `errors_introduced` (list lỗi mới xuất hiện), `net_improvement` (boolean), và `error_score` = Σ(weight[type] * count) với weights: syntax_error=10, runtime_error=7, lint_warning=1.
2. WHEN `new_error_score > old_error_score` in an ErrorDelta, THE Orchestrator SHALL trigger automatic rollback bằng cách restore file từ atomic backup của đúng `operation_id` đã introduce regression.
3. THE Orchestrator SHALL create an atomic backup của tất cả files sẽ bị modify trước mỗi patch attempt, lưu vào `antigravity/backups/{session_id}/{operation_id}/` với timestamp.
4. WHEN a rollback is triggered, THE Orchestrator SHALL pass the ErrorDelta context vào replan_repair prompt để LLM hiểu tại sao patch trước thất bại.
5. THE DeterministicChecker SHALL compare error sets bằng normalized error signatures (sử dụng `_normalize_errors()` đã có) để tránh false positives do path/timestamp differences.
6. IF backup files are missing or corrupted, THEN THE Orchestrator SHALL log a critical warning và continue without rollback thay vì crash.
7. THE atomic backup mechanism SHALL be idempotent: backing up the same file multiple times trong cùng `operation_id` SHALL overwrite previous backup, không tạo duplicate files.
8. FOR ALL patch sequences [p1, p2, ..., pN], nếu pi introduces regression (new_error_score > old_error_score), THEN rollback SHALL restore files from the exact `operation_id` of pi, và state sau rollback SHALL be identical to state trước khi áp dụng pi (invariant property).
9. IF a patch produces no semantic change — determined by comparing file hash (SHA-256) before and after patch application, or by AST structural diff — THEN THE Orchestrator SHALL skip DeterministicChecker entirely và request replan immediately, logging a `no_op_patch_detected` event.

---

### Yêu Cầu 4: SLM Router Integration

**User Story:** Là một AI agent, tôi muốn sử dụng model nhỏ để phân loại intent đơn giản, để tôi có thể tiết kiệm chi phí bằng cách chỉ gọi model lớn cho các task cần reasoning phức tạp.

#### Tiêu Chí Chấp Nhận

1. THE SLMRouter SHALL classify user intent thành các categories đã định nghĩa trong RouteDecision schema sử dụng sentence-transformers cosine similarity với một tập prototype embeddings.
2. WHEN SLMRouter confidence score is above a configurable threshold (default: 0.85), THE Orchestrator SHALL use SLMRouter result trực tiếp mà không gọi LLM lớn cho routing step.
3. WHEN SLMRouter confidence score is below the threshold, THE Orchestrator SHALL fall through to the existing LLMClient routing call như hiện tại.
4. THE SLMRouter SHALL load prototype embeddings từ một JSON file có thể cập nhật mà không cần restart service.
5. THE SLMRouter SHALL operate with latency under 100ms cho classification step trên CPU (không cần GPU).
6. IF the sentence-transformers model fails to load, THEN THE SLMRouter SHALL disable itself và THE Orchestrator SHALL use LLMClient routing như trước, không crash.
7. THE SLMRouter SHALL log routing decisions bao gồm: chosen category, confidence score, top-k candidates với similarity scores, và whether LLM fallback was triggered — theo format: `{"chosen": "<category>", "confidence": <score>, "top_k": [{"label": "<label>", "score": <score>}, ...]}` — để TracingService có thể capture.
8. FOR ALL intents i classified by SLMRouter, re-classifying i SHALL return the same category (idempotence property).

---

### Yêu Cầu 5: Prefix-First Prompt Caching

**User Story:** Là một AI agent, tôi muốn các static prompt sections luôn đứng đầu message, để tôi có thể tận dụng Anthropic/OpenAI prompt caching và giảm chi phí token.

#### Tiêu Chí Chấp Nhận

1. THE LLMClient SHALL structure all prompts với static prefix (CONSTITUTION block và MASTER_ROUTER summary) đứng đầu system message, trước bất kỳ dynamic content nào.
2. THE LLMClient SHALL separate prompt content thành hai phần: `static_prefix` (không thay đổi giữa các calls) và `dynamic_suffix` (thay đổi theo task).
3. WHEN calling Anthropic API, THE LLMClient SHALL add `cache_control: {"type": "ephemeral"}` annotation vào static_prefix block để kích hoạt prompt caching.
4. WHEN calling OpenAI-compatible API, THE LLMClient SHOULD aim for a large static prefix to maximize cache hit rate; THE LLMClient SHALL NOT enforce a hard token minimum vì automatic prefix caching behavior is not officially guaranteed by OpenAI.
5. THE LLMClient SHALL expose a `set_static_prefix(content: str)` method để Orchestrator có thể inject CONSTITUTION và MASTER_ROUTER content khi khởi tạo.
6. THE static_prefix SHALL be loaded once at LLMClient initialization và reused across all subsequent calls trong cùng session.
7. IF static_prefix content changes between calls, THEN THE LLMClient SHALL log a warning vì điều này sẽ invalidate cache.
8. FOR ALL calls c1 và c2 trong cùng session với cùng static_prefix, THE LLMClient SHALL produce identical prompt structure cho phần prefix (invariant property).

---

### Yêu Cầu 6: Langfuse Full Observability Integration

**User Story:** Là một developer, tôi muốn xem toàn bộ traces, generations, và scores trên Langfuse dashboard, để tôi có thể debug và optimize agent behavior dựa trên dữ liệu thực.

#### Tiêu Chí Chấp Nhận

1. THE TracingService SHALL initialize a real Langfuse client WHEN `LANGFUSE_PUBLIC_KEY` và `LANGFUSE_SECRET_KEY` environment variables are present.
2. THE TracingService SHALL log every LLM generation call với đầy đủ: model name, input tokens, output tokens, latency_ms, và task_name.
3. THE TracingService SHALL create nested spans phản ánh đúng cấu trúc orchestrator: `route_task` → `plan_execution` → `execution_loop` → `step_{id}` → `deterministic_check`.
4. WHEN a repair cycle is triggered, THE TracingService SHALL log an event `replan_triggered` với ErrorDelta context vào span hiện tại.
5. THE TracingService SHALL link `patch_id`, `error_delta`, và `rollback_triggered` (boolean) trong cùng một span, theo format: `{trace_id, step_id, patch_id, error_delta, rollback_triggered: bool}`.
6. THE TracingService SHALL call `trace.score()` với value 1.0 khi task hoàn thành thành công và 0.0 khi đạt max repair attempts.
7. IF Langfuse credentials are missing or invalid, THEN THE TracingService SHALL degrade gracefully to NoOp behavior như hiện tại, không raise exception.
8. THE TracingService SHALL flush all pending traces khi Orchestrator session kết thúc, đảm bảo không mất data.
9. THE TracingService SHALL tag mỗi trace với `session_id` và `notebook_id` (nếu có) để cho phép filtering trên dashboard.
10. FOR ALL traces t created in a session, flushing then re-querying Langfuse API SHALL return t với đầy đủ spans (round-trip observability property).

---

### Yêu Cầu 7: Execution Budget Guard

**User Story:** Là một AI agent, tôi muốn có giới hạn cứng về số bước thực thi, token tiêu thụ, và số lần repair, để hệ thống không bao giờ rơi vào vòng lặp vô tận hoặc vượt ngân sách chi phí.

#### Tiêu Chí Chấp Nhận

1. THE Orchestrator SHALL maintain a BudgetGuard tracking: `max_steps`, `max_tokens`, và `max_repair_attempts` — tất cả configurable tại khởi tạo.
2. WHEN any budget limit is exceeded, THE Orchestrator SHALL terminate execution gracefully và emit a final trace event với `termination_reason` chỉ rõ limit nào bị vượt.
3. THE BudgetGuard SHALL track cumulative token usage across all LLM calls trong một session.
4. IF `max_repair_attempts` is reached without `net_improvement`, THEN THE Orchestrator SHALL escalate to human-in-the-loop mode thay vì tiếp tục retry.
5. THE BudgetGuard SHALL log a warning khi usage reaches 80% of any configured limit (early warning).
6. IF budget configuration is missing or incomplete, THEN THE Orchestrator SHALL apply safe defaults: `max_steps=50`, `max_tokens=100000`, `max_repair_attempts=5`.
7. THE Orchestrator SHALL ensure no NEW LLM call is initiated IF `remaining_token_budget < estimated_call_cost`. Estimated call cost SHALL be calculated as: `(static_prefix_tokens + dynamic_suffix_tokens + max_expected_output_tokens)` — để enforce trước khi gọi thực tế thay vì enforce sau khi API trả về output length không biết trước.
8. THE BudgetGuard SHALL be queryable mid-session via a `get_status()` method để Orchestrator có thể adjust strategy trước khi hit limit.

---

### Yêu Cầu Xuyên Suốt: Global ID Format Invariant

**User Story:** Là một developer, tôi muốn tất cả system-generated IDs đều có thể sắp xếp theo thời gian, để tôi có thể trace ordering, debug timeline, và correlate events across components một cách chính xác.

#### Tiêu Chí Chấp Nhận

1. THE System SHALL generate all session_id, operation_id, patch_id, và trace_id values using UUIDv7 or ULID format để đảm bảo time-sortable ordering.
2. THE Orchestrator SHALL reject any externally-provided ID that does not conform to UUIDv7 or ULID format, logging a `invalid_id_format` warning và generating a compliant replacement.
3. FOR ALL IDs generated within a session, sorting IDs lexicographically SHALL produce the same ordering as sorting by creation timestamp (time-sortable invariant).
