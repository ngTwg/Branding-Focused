# Implementation Plan: Antigravity Architecture Upgrade

## Overview

Nâng cấp kiến trúc Antigravity từ v6.0.0-SOLID-STATE lên 3-layer architecture. Các tasks được sắp xếp theo thứ tự impact/effort: foundation trước, integration sau. Tất cả thay đổi phải backward compatible với `SkillStore.retrieve(task, errors)` và orchestrator hiện tại.

## Tasks

- [x] 1. ID Utilities — Foundation cho tất cả components
  - Tạo `antigravity/core/id_utils.py` với `generate_ulid()`, `generate_uuidv7()`, và `is_valid_time_sortable_id(id_str)`
  - Implement ULID generation (timestamp-based, 26-char base32) và UUIDv7 fallback
  - Export `new_id()` convenience function trả về ULID by default
  - _Requirements: 8.1, 8.3_

  - [x]* 1.1 Write property test cho time-sortable ID invariant
    - **Property 20: Time-Sortable ID Invariant**
    - **Validates: Requirements 8.1, 8.3**
    - Dùng `@given(n_ids=st.integers(min_value=2, max_value=50))` với `time.sleep(0.001)` giữa các lần generate
    - Verify `sorted(ids) == ids` (lexicographic == chronological)

- [x] 2. Data Models — Pydantic schemas cho toàn bộ hệ thống
  - Tạo `antigravity/core/schemas.py` (hoặc bổ sung vào file hiện có) với các models:
    - `SkillDocument`, `RankedSkill` (HybridRetriever)
    - `ASTNode`, `ASTContract` (ASTAnalyzer) với `field_validator` cho `node_id` format
    - `ErrorDelta` với `compute_score()` classmethod và `ERROR_WEIGHTS` dict
    - `SLMRouteDecision` (SLMRouter)
    - `BudgetStatus` (BudgetGuard)
    - `SessionContext` với validator cho `session_id` và `trace_id`
  - Import và dùng `is_valid_time_sortable_id` từ task 1 cho validators
  - _Requirements: 1.2, 2.2, 2.7, 3.1, 4.7, 7.8, 8.1_

  - [x]* 2.1 Write property test cho ErrorDelta score computation
    - **Property 9: ErrorDelta Score Computation**
    - **Validates: Requirements 3.1**
    - `@given(errors=st.lists(st.text(...)))` — verify thêm SyntaxError tăng score đúng 10

  - [x]* 2.2 Write property test cho node_id format invariant
    - **Property 7: Node ID Format Invariant**
    - **Validates: Requirements 2.7**
    - Verify mọi `node_id` match pattern `"<file>::<function>::<line>"` với 3 phần phân cách bởi `::`

- [x] 3. BackupManager — Atomic backup và rollback
  - Tạo `antigravity/core/backup_manager.py`
  - Implement `create_backup(session_id, operation_id, file_paths)` — copy files vào `antigravity/backups/{session_id}/{operation_id}/`
  - Implement `rollback(session_id, operation_id)` — restore files, log CRITICAL nếu backup missing (không crash)
  - Implement `_backup_path(session_id, operation_id)` helper
  - Idempotent: backup cùng file trong cùng `operation_id` → overwrite
  - _Requirements: 3.3, 3.6, 3.7, 3.8_

  - [ ]* 3.1 Write property test cho rollback round-trip invariant
    - **Property 10: Rollback Round-Trip Invariant**
    - **Validates: Requirements 3.3, 3.8**
    - `@given(file_content=st.text(...), patch_content=st.text(...))` — verify SHA-256 sau rollback == trước patch

  - [ ]* 3.2 Write property test cho backup idempotence
    - **Property 11: Backup Idempotence**
    - **Validates: Requirements 3.7**
    - Verify gọi `create_backup()` nhiều lần với cùng `operation_id` → số files trong backup dir == số unique files

- [x] 4. DeterministicChecker nâng cấp — ErrorDelta + severity scoring + no-op detection
  - Sửa `antigravity/core/checker.py`: thay đổi `examine()` để trả về `ErrorDelta` thay vì `list[str]`
  - Signature mới: `examine(checks, previous_errors=None, project_root=None) -> ErrorDelta`
  - Backward compatible: nếu `previous_errors=None`, `ErrorDelta.net_improvement=True` khi errors rỗng
  - Dùng `_normalize_errors()` hiện có để so sánh error sets, tránh false positives
  - Tính `old_error_score` và `new_error_score` bằng `ErrorDelta.compute_score()`
  - Set `net_improvement = new_error_score <= old_error_score`
  - _Requirements: 3.1, 3.2, 3.4, 3.5_

  - [ ]* 4.1 Write property test cho error normalization stability
    - **Property 12: Error Normalization Stability**
    - **Validates: Requirements 3.5**
    - Verify `_normalize_errors([e1]) == _normalize_errors([e2])` khi e1, e2 cùng root cause nhưng khác path/timestamp

- [x] 5. BudgetGuard — Pre-call enforcement
  - Tạo `antigravity/core/budget_guard.py`
  - Implement `__init__(max_steps, max_tokens, max_repair_attempts)` với safe defaults khi config missing
  - Implement `check_pre_call(estimated_input_tokens, max_expected_output_tokens)` — raise `BudgetExceededError` nếu `remaining < estimated_cost`
  - Implement `record_call(actual_tokens)`, `record_step()`, `record_repair()`
  - Implement `get_status() -> BudgetStatus`
  - Implement `_warn_if_approaching()` — log warning khi usage >= 80% của bất kỳ limit nào
  - Tạo `BudgetExceededError` exception với `termination_reason` field
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8_

  - [ ]* 5.1 Write property test cho budget pre-call enforcement
    - **Property 17: Budget Pre-Call Enforcement**
    - **Validates: Requirements 7.7**
    - `@given(tokens_used, estimated_input, max_output)` — verify raise `BudgetExceededError` khi `remaining < estimated_cost`

  - [ ]* 5.2 Write property test cho budget termination với reason
    - **Property 18: Budget Termination với Reason**
    - **Validates: Requirements 7.2**
    - Verify `BudgetStatus.termination_reason` chỉ rõ dimension bị vượt (steps/tokens/repairs)

  - [ ]* 5.3 Write property test cho token accumulation additivity
    - **Property 19: Token Accumulation Additivity**
    - **Validates: Requirements 7.3**
    - `@given(token_counts=st.lists(...))` — verify `_tokens_used == sum(token_counts)`

- [x] 6. ASTAnalyzer — Tree-sitter JSON contract
  - Tạo `antigravity/core/ast_analyzer.py`
  - Implement `analyze(targets: list[tuple[str, int]]) -> ASTContract` — multi-file entry point
  - Implement `_parse_file(file_path, error_line)` — extract nodes trong ±10 lines, `node_id` format `"file.py::function_name::start_line"`
  - Implement `_fallback_excerpt(file_path, error_line)` — raw excerpt ≤ 200 tokens khi tree-sitter fail, `is_fallback=True`
  - Hard limit: serialized JSON ≤ 4096 bytes — truncate `affected_nodes` nếu vượt
  - Lazy import `tree_sitter`; nếu không có → fallback mode
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.7, 2.8, 2.9_

  - [x]* 6.1 Write property test cho ASTContract size invariant
    - **Property 5: ASTContract Size Invariant**
    - **Validates: Requirements 2.2**
    - `@given(file_content=st.text(...), error_line=st.integers(...))` — verify `len(contract.model_dump_json().encode()) <= 4096`

  - [x]* 6.2 Write property test cho ASTContract compression ratio
    - **Property 6: ASTContract Compression Ratio**
    - **Validates: Requirements 2.3**
    - Verify `len(serialized) <= 0.3 * len(file_content)` khi file >= 100 bytes

  - [x]* 6.3 Write property test cho AST referential integrity
    - **Property 8: AST Referential Integrity**
    - **Validates: Requirements 2.8**
    - Verify mọi `node_id` trong contract tham chiếu đến node thực sự tồn tại trong AST gốc

- [x] 7. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. HybridRetriever — BM25 + cosine + tie-breaking
  - Tạo `antigravity/core/hybrid_retriever.py`
  - Implement `__init__(skills_dir, alpha=0.5, beta=0.5, embedding_model="all-MiniLM-L6-v2")`
  - Implement `index(documents: list[SkillDocument])` — build BM25 index và embedding matrix
  - Implement `retrieve(query, errors=None, domain_filter=None, top_k=5) -> list[RankedSkill]`
  - Implement `_normalize_bm25(scores)` — min-max → [0,1]
  - Implement `_normalize_cosine(scores)` — (score+1)/2 → [0,1]
  - Tie-breaking: cosine_norm desc → bm25_norm desc → skill_id lexicographic asc
  - Graceful degradation: nếu `sentence_transformers` không có → `_dense_available=False`, BM25-only, log WARNING
  - Index tất cả `.md` files trong `antigravity/skills/` theo domain tag từ đường dẫn
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11_

  - [ ]* 8.1 Write property test cho score normalization và ranking invariant
    - **Property 1: Score Normalization và Ranking Invariant**
    - **Validates: Requirements 1.2, 1.3**
    - `@given(query=st.text(...), alpha=st.floats(0,1), beta=st.floats(0,1))` — verify scores trong [0,1] và sorted desc

  - [ ]* 8.2 Write property test cho alpha/beta monotonicity
    - **Property 2: Monotonicity của Alpha/Beta Weights**
    - **Validates: Requirements 1.9**
    - `@given(alpha1 in [0,0.5], alpha2 in [0.5,1])` — verify `alpha2 * bm25_norm >= alpha1 * bm25_norm`

  - [ ]* 8.3 Write property test cho domain filter containment
    - **Property 3: Domain Filter Containment**
    - **Validates: Requirements 1.4**
    - Verify tất cả skills trong kết quả có `domain_filter` trong `domain_tags`

  - [ ]* 8.4 Write property test cho deterministic tie-breaking
    - **Property 4: Deterministic Tie-Breaking**
    - **Validates: Requirements 1.11**
    - Verify gọi `retrieve()` nhiều lần với cùng inputs → cùng thứ tự

- [x] 9. SLMRouter — Intent classification
  - Tạo `antigravity/core/slm_router.py`
  - Implement `__init__(prototypes_path, confidence_threshold=0.85)` — load prototype embeddings từ JSON
  - Implement `classify(query) -> SLMRouteDecision | None` — trả về `None` nếu confidence < threshold hoặc `_enabled=False`
  - Implement `reload_prototypes()` — hot-reload từ JSON file không cần restart
  - Graceful degradation: nếu `sentence_transformers` fail → `_enabled=False`, không crash
  - Log routing decisions theo format `{"chosen": ..., "confidence": ..., "top_k": [...]}`
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

  - [ ]* 9.1 Write property test cho SLM routing idempotence
    - **Property 13: SLM Routing Idempotence**
    - **Validates: Requirements 4.8**
    - `@given(query=st.text(...))` — verify `classify(classify(i).chosen).chosen == classify(i).chosen`

  - [ ]* 9.2 Write property test cho SLM confidence threshold routing
    - **Property 14: SLM Confidence Threshold Routing**
    - **Validates: Requirements 4.2, 4.3**
    - Verify khi `confidence >= threshold` → LLMClient không được gọi; khi `< threshold` → LLMClient được gọi

- [x] 10. LLMClient nâng cấp — Prefix caching
  - Sửa `antigravity/core/llm_client.py`: thêm `set_static_prefix(content: str)` method
  - Implement `_build_system_prompt(dynamic_suffix: str) -> str | list` — ghép `static_prefix + dynamic_suffix`
  - Với Anthropic: thêm `cache_control: {"type": "ephemeral"}` annotation vào static_prefix block
  - Log WARNING nếu `static_prefix` thay đổi sau lần đầu (cache invalidation)
  - `static_prefix` được load một lần khi khởi tạo, reuse across all calls trong session
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

  - [ ]* 10.1 Write property test cho static prefix invariant
    - **Property 15: Static Prefix Invariant**
    - **Validates: Requirements 5.6, 5.8**
    - Verify hai calls c1, c2 trong cùng session với cùng `static_prefix` → phần prefix trong system message identical byte-for-byte

- [x] 11. TracingService nâng cấp — Langfuse integration
  - Sửa `antigravity/core/tracing.py`: kích hoạt Langfuse khi `LANGFUSE_PUBLIC_KEY` và `LANGFUSE_SECRET_KEY` có trong env
  - Implement `log_generation(model, input_tokens, output_tokens, latency_ms, task_name)` — log đầy đủ fields, `None` nếu API không trả về
  - Implement `log_replan_triggered(error_delta)` — log event với ErrorDelta context
  - Implement `link_patch_metadata(patch_id, error_delta, rollback_triggered)` — link trong span hiện tại
  - Implement `score(value: float)` — gọi `trace.score()` với 1.0 khi success, 0.0 khi max repairs
  - Đảm bảo `flush()` được gọi trong `finally` block của Orchestrator session
  - Tag mỗi trace với `session_id` và `notebook_id`
  - Nested spans: `route_task` → `plan_execution` → `execution_loop` → `step_{id}` → `deterministic_check`
  - Graceful degradation: NoOp nếu credentials missing/invalid
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_

  - [ ]* 11.1 Write property test cho trace fields completeness
    - **Property 16: Trace Fields Completeness**
    - **Validates: Requirements 6.2, 6.5**
    - Verify mọi generation span chứa đủ `model`, `input_tokens`, `output_tokens`, `latency_ms`, `task_name` (kể cả khi `None`)

- [x] 12. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Orchestrator integration — Wire tất cả components
  - Sửa `antigravity/scripts/orchestrator.py`: khởi tạo tất cả components mới trong `__init__` hoặc `execute()`
  - Gọi `llm_client.set_static_prefix(constitution + master_router)` một lần khi khởi tạo
  - Gọi `budget_guard.check_pre_call()` TRƯỚC mỗi `llm.generate_structured()` / `llm.generate_text()`
  - Thử `slm_router.classify(task)` trước trong `route_task()`; nếu `None` → fall through sang LLMClient
  - Gọi `backup_manager.create_backup()` trước mỗi `ActionDispatcher.dispatch()`
  - Implement no-op patch detection: so sánh SHA-256 hash trước/sau patch; nếu bằng nhau → emit `no_op_patch_detected`, skip checker, request replan
  - Khi `ErrorDelta.net_improvement=False` → gọi `backup_manager.rollback()`, pass `error_delta` vào `replan_repair()`
  - Gọi `ast_analyzer.analyze()` thay vì raw file content khi construct repair prompts
  - Gọi `tracer.flush()` trong `finally` block
  - Gọi `budget_guard.finalize()` và `tracer.score()` khi session kết thúc
  - Reject externally-provided IDs không phải UUIDv7/ULID, generate compliant replacement, log `invalid_id_format`
  - _Requirements: 1.6, 2.6, 3.2, 3.3, 3.4, 3.6, 3.9, 4.2, 4.3, 5.1, 6.3, 6.8, 7.1, 7.2, 7.4, 7.7, 8.2_

  - [ ]* 13.1 Write integration test cho budget terminates before LLM call
    - Test `budget_guard.check_pre_call()` được gọi trước LLM call và terminate đúng khi budget exceeded
    - _Requirements: 7.7_

  - [ ]* 13.2 Write integration test cho regression triggers rollback và replan
    - Test khi `ErrorDelta.net_improvement=False` → rollback được trigger và `replan_repair()` nhận ErrorDelta context
    - _Requirements: 3.2, 3.4_

  - [ ]* 13.3 Write integration test cho full execution loop
    - Test route → plan → execute → check → complete với tất cả components wired
    - _Requirements: 1.6, 2.6, 4.2_

- [x] 14. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks đánh dấu `*` là optional, có thể skip để MVP nhanh hơn
- Mỗi task references requirements cụ thể để traceability
- Tất cả thay đổi phải backward compatible: `SkillStore.retrieve(task, errors)` giữ nguyên signature
- Property tests dùng `hypothesis` với `@settings(max_examples=100)`
- Tag format cho mỗi property test: `# Feature: antigravity-architecture-upgrade, Property N: <text>`
- Graceful degradation: mọi optional dependency (`sentence-transformers`, `langfuse`, `tree-sitter`) đều có NoOp fallback
