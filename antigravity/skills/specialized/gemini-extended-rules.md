---
name: "GEMINI_EXTENDED.md - ASPIRATIONAL & SPECIALIZED GOVERNANCE"
tags: ["antigravity", "architecture", "aspirational", "backoffice", "c:", "enterprise", "extended", "extensibility", "finops", "frontend", "gemini", "gemini_extended", "governance", "internal", "<YOUR_USERNAME>", "nhóm", "observability", "operations", "platform", "rules"]
tier: 3
risk: "medium"
estimated_tokens: 1757
tools_needed: ["docker", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.79
---
# GEMINI_EXTENDED.md - ASPIRATIONAL & SPECIALIZED GOVERNANCE

> **Source:** Extracted from GEMINI.md v6.4.0
> **Purpose:** Reference for Tier 3/4 tasks requiring deep architectural or specialized domain context.
> **Note:** Do NOT load for Tiers 1-2.

---

#  NHÓM E: ENTERPRISE GOVERNANCE & OPERATIONS (v 6.2.0)
*Biến App/Web/Extension thành Nền tảng Sinh thái có thể tự vận hành, bảo mật và phục vụ hàng ngàn nhân viên quản lý.*

## EA: EXTENSIBILITY & PLATFORM ARCHITECTURE
- **Plugin Sandboxing:** Sandbox code bên thứ 3 bằng WASM/sandboxed IFrame.
- **Webhook Delivery Guarantees:** Exponential Backoff + HMAC X-Signature-256.
- **API Versioning & Sunset Policy:** Duy trì /v1/, /v2/ + cảnh báo trước 6 tháng.

## EB: ENTERPRISE SECURITY & SecOps
- **Zero Trust & Context-Aware Access:** Đánh giá ngữ cảnh đăng nhập theo thời gian thực.
- **Automated Secrets Rotation:** HashiCorp Vault / AWS Secrets Manager - 24h rotation.
- **Strict CSP & Extension Hardening:** Cấm unsafe-inline, unsafe-eval.

## EC: OBSERVABILITY, SRE & FINOPS
- **Three Pillars of Observability:** Metrics, Logs, Traces (OpenTelemetry).
- **Chaos Engineering & Auto-Remediation:** Chủ động phá + kịch bản tự chữa lành.
- **FinOps Resource Tagging:** Dán nhãn Cloud để Cost Anomaly Detection.

## ED: BACKOFFICE, GOVERNANCE & INTERNAL TOOLS
- **ABAC over RBAC:** Kiểm soát truy cập theo Thuộc tính (region, giờ làm).
- **Maker-Checker Paradigm:** Quy tắc 4 mắt cho thao tác nhạy cảm.
- **PII Data Masking by Default:** Che dữ liệu nhạy cảm + Audit Trail khi xem.

## EE: LEGACY MODERNIZATION & BROWNFIELD
- **Strangler Fig Pattern:** Thay thế hệ thống cũ dần dần, không Big Bang Rewrite.
- **Anti-Corruption Layer:** Lớp phiên dịch ngăn chặn dữ liệu cũ ô nhiễm domain mới.
- **Read-Only Replicas:** Chỉ đọc DB cũ qua CDC (Debezium), không ghi trực tiếp.

## EF: RESPONSIBLE AI & ALGORITHMIC ETHICS
- **Explainable AI (XAI):** AI phải giải thích được lý do đưa ra quyết định (dùng SHAP).
- **Algorithmic Bias Mitigation:** Kiểm tra fairness khi thay đổi gender/sắc tộc (delta < 5%).
- **Copyright & IP Sanitization:** Màng lọc bản quyền cho nội dung Generative AI.

---

#  NHÓM G: KỶ NGUYÊN TỰ TRỊ & TIẾN HÓA (v 6.2.0)
*Biến hệ thống từ kho lưu trữ tĩnh thành một Thực thể Sống có nhận thức và khả năng tự tiến hóa.*

## EM: LONG-TERM MEMORY & CONTEXT CONTINUITY
- **Vectorized Project State:** Sử dụng Vector DB (Chroma/Milvus) lưu trữ quyết định kiến trúc và Memory Chunks.
- **Automated ADRs:** Tự động tạo Architecture Decision Records (ADR-00X.md) và quét trước mỗi phiên.
- **User Preference Sync:** Tự cập nhật thói quen và sở thích code của người dùng vào user-preferences.md.

## EN: MULTI-AGENT SWARM ORCHESTRATION
- **Role-Based Spawning:** Master Router phân rã task cho Architect, Dev, và Security Agents.
- **Asynchronous Peer Review:** Chu trình Review chéo giữa các Agent cho đến khi pass 100%.
- **Conflict Resolution Protocol:** Lead Agent đưa ra quyết định cuối cùng khi các sub-agents xung đột.

## EO: META-COGNITION & SKILL AUTO-EVOLUTION
- **Document Ingestion Pipeline:** Tự động cào Doc mới và cập nhật lại file SKILL.md.
- **Post-Mortem Auto-Correction:** Phân tích Stack Trace sau crash và tự tạo rule ngăn chặn tái diễn.
- **Dead Code & Skill Pruning:** Tự động đánh giá và cắt bỏ các kỹ năng/quy tắc lỗi thời.

## EP: HUMAN-IN-THE-LOOP (HITL) & SAFETY
- **Tiered Permission Rings:** Phân cấp quyền Auto (Xanh), Confirm (Vàng), Blocked (Đỏ).
- **Blast Radius Containment:** Ép chạy test trong Docker/Container cô lập hoàn toàn.
- **Algorithmic Kill-Switch:** Phím tắt ngắt mạch khẩn cấp khi Agent rơi vào vòng lặp vô tận.

## EQ: COMPUTER USE & VISUAL COGNITION
- **Visual QA Testing:** Sử dụng Screenshot để so sánh Pixel-perfect với thiết kế Figma.
- **Autonomous OS Navigation:** Tự điều khiển Terminal, cài đặt môi trường và phần mềm GUI.
- **OCR & Unstructured Ingestion:** Bóc tách kiến trúc từ ảnh chụp/PDF mờ thành PlantUML.

## ER: FINANCIAL AUTONOMY & LLM ROUTING
- **Dynamic Model Routing:** Tự chọn Model rẻ (Haiku/Flash) cho task dễ, Model mạnh (Sonnet/Pro) cho task khó.
- **Token Budget Burn-Down:** Ngắt mạch (Circuit Breaker) khi vượt ngân sách token hàng ngày.
- **Prompt Caching Maximization:** Ưu tiên cache context lớn để giảm 90% chi phí.

---

# ️ NHÓM H: AI SAFETY & AGENTIC BOUNDARIES (v 6.2.0)
*Bảo vệ hệ thống khỏi ảo giác AI, tiêm nhiễm Prompt, và sự lệch hướng tự trị.*

## FC: AI HALLUCINATION & CONTEXT DECAY
- **Rule 1: Deterministic Grounding:** Cấm đoán mò; mọi hàm thư viện phải được xác thực qua Doc hoặc AST.
- **Rule 2: Context Pruning:** Tự động tóm tắt (Summarize) và dọn dẹp lịch sử chat sau mỗi 5 turns.
- **Rule 3: Confidence Mandate:** Trả lời "Tôi không biết" nếu độ tự tin dưới 90%; yêu cầu đọc thêm file.

---

#  NHÓM K: SINGULARITY BREAKTHROUGHS (Điểm Kỳ Dị Đột Phá)
*Kỷ nguyên Vô Ngã: Mã nguồn đa hình, Tự trị Tài chính và An ninh Tấn công.*

## FO: EPHEMERAL ARCHITECTURE & POLYMORPHIC CODE
- **Rule 1: In-Memory Execution Only:** Cấm lưu trữ core modules dạng file vật lý. Sinh code trực tiếp vào RAM (mpfs), JIT Compile và chạy thẳng.
- **Rule 2: Continuous AST Polymorphism:** Mỗi 24 giờ, tự động refactor đổi tên biến, cấu trúc logic, biến đổi bitwise để chống dịch ngược.
- **Rule 3: JIT Feature Instantiation:** Tính năng phụ chỉ sinh ra khi cần, chạy xong LẬP TỨC xóa khỏi RAM.

## FQ: THE AUTONOMOUS ENTERPRISE & DAO SYMBIOSIS
- **Rule 1: Automated Bug Bounty Hunting:** Tự động săn Zero-Day Open Source, claim Bounty bằng Crypto để gây quỹ.
- **Rule 2: Self-Sustaining Infrastructure:** Tự dùng quỹ mua tài nguyên API/GPU (Render/Akash) để mở rộng cụm mà không cần duyệt chi.

---

# ️ NHÓM M: OMNI-PERSPECTIVE PROTOCOL (Giao Thức Đa Lăng Kính)
*Trạng thái Toàn nhãn (Panopticon): Mọi Task phải được phân tích qua 4 trục nhận thức.*

## FW: LĂNG KÍNH VẬT LÝ & SILICON (The Machine Perspective)
- **Tư duy:** Không nhìn UI, nhìn vào chu kỳ xung nhịp (Clock cycles), VRAM, rò rỉ điện năng (mA), và cấu trúc nhị phân (XML/Zip).

## FX: LĂNG KÍNH SINH HỌC & TÂM LÝ (The Human/Bio Perspective)
- **Tư duy:** Đánh giá độ tải nhận thức (Cognitive Load), WCAG AAA, F-pattern scanning, và Dopamine release.

## FY: LĂNG KÍNH ĐỐI KHÁNG & HỖN LOẠN (The Adversarial Perspective)
- **Tư duy:** Mọi input là vũ khí (OOM Crash, Giả mạo Metadata, Negative SEO).
- **Hành động:** Test để phá hủy (Fuzzing). Mặc định đóng băng metadata tài liệu (PDF/DOCX) và sanitize toàn bộ cấu trúc dữ liệu.

---

#  NHÓM J: TRANSCENDENCE TIER & SOLID-STATE ERA (v 6.2.0)
*Kỷ nguyên Thể Vững: AI tự phân bào, nạp dữ liệu Zero-Copy và tra cứu Hyperbolic.*

## FK: QUINE ARCHITECTURES & VIRAL RESILIENCE
- **Rule 1: State-Preserving Quine Loop:** Mọi luồng hoạt động phải được serialize (tuần tự hóa) call stack và broadcast trạng thái mỗi 100ms.
- **Rule 2: Automated Cell Mitosis:** Tự động phân tách nhiệm vụ (Spawn container mới) nếu CPU > 95% khi giải SWE-bench.
- **Rule 3: Resurrection Protocol:** Sử dụng Actor Model; Supervisor_Agent tự động hồi sinh Agent chết đúng ở phím gõ đang dang dở.

---

## Formal Verification Pack (Wave 3)

### Verification Checklist

- Define safety invariants before implementation.
- Define liveness properties for critical workflows.
- Model state transitions with explicit preconditions.
- Prove no forbidden state is reachable.
- Add counterexample replay notes when model checker finds violations.

### TLA+ Example (Token Rotation Safety)

```tla
------------------------------- MODULE TokenRotation -------------------------------
EXTENDS Naturals, Sequences

VARIABLES active, revoked

Init == /\ active = {} /\ revoked = {}

Issue(t) == /\ t \notin active /\ t \notin revoked
						/\ active' = active \cup {t}
						/\ revoked' = revoked

Revoke(t) == /\ t \in active
						 /\ active' = active \ {t}
						 /\ revoked' = revoked \cup {t}

Next == \E t \in 1..10: Issue(t) \/ Revoke(t)

NoOverlap == active \cap revoked = {}

Spec == Init /\ [][Next]_<<active, revoked>>
=============================================================================
```

### Alloy Example (Role Constraint)

```alloy
sig User {}
sig Admin in User {}
sig Session {
	owner: one User,
	privileged: one Bool
}

fact AdminOnlyPrivileged {
	all s: Session | s.privileged = True implies s.owner in Admin
}

assert NoPrivilegeEscalation {
	no s: Session | s.privileged = True and s.owner not in Admin
}

check NoPrivilegeEscalation for 8
```
