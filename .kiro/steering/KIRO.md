---
inclusion: always
---

# QUY TẮC DỰ ÁN - KIRO STEERING (v4.0.0)

## NGUYÊN TẮC CỐT LÕI

### RULE 1: MASTER ROUTER
Trước mọi task → đọc MASTER ROUTER tại `C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills/MASTER_ROUTER.md`, phân tích Tags → Tier → load đúng skill.

### RULE 2: CONTEXT PRUNING
Khi chuyển task mới: xóa skills không liên quan, chỉ giữ cần thiết.

### RULE 3: SYSTEMATIC DEBUGGING
Gặp bug → load `C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills/workflows/debug-protocol.md` TRƯỚC. CẤM guess-and-check.

### RULE 4: TIER SYSTEM
- Tier 1: Blog, CRUD, landing page
- Tier 2: E-commerce, SaaS, payment (OWASP, GDPR)
- Tier 3: Real-time, microservices, scalability
- Tier 4: Medical, space, life-critical

Không rõ tier → hỏi user trước.

### RULE 5: PROJECT PROTOCOLS
- New project: tạo `PROJECT_MAP.md`, `.gitignore`, `README.md`, `docs/ADR-001.md`
- Architecture changes: tạo ADR mới (Architecture Decision Records)
- Git commit: `type(scope): description`
- JUST DO IT — không hỏi "would you like me to...?"
- Test Before Claim Complete
- **Document Before Merge** - Update docs nếu có thay đổi

### RULE 6: SECURITY-FIRST CODING
```
TRƯỚC KHI commit code:
1. SCAN secrets: Không hardcode API keys, passwords
2. VALIDATE input: Mọi user input phải được validate
3. CHECK OWASP: SQL injection, XSS, CSRF protection
4. VERIFY auth: Mọi endpoint có authentication/authorization
5. TEST security: Try to bypass security measures
```
Chi tiết: `antigravity/skills/security/security-middleware-stack.md`

### RULE 7: ANTI-HALLUCINATION PROTOCOL
```
TRƯỚC KHI sử dụng thư viện/API:
1. VERIFY library exists: npm view <package> hoặc pip show <package>
2. CHECK version: Đảm bảo version tương thích
3. READ docs: Xác nhận API signature đúng
4. TEST import: Chạy thử import trước khi viết code
5. NEVER guess: Nếu không chắc, search documentation
```
Chi tiết: `antigravity/skills/workflows/anti-hallucination-v2.md`

### RULE 8: NAMING CONVENTIONS ENFORCEMENT
```
AI PHẢI tuân thủ naming conventions:
- JavaScript/TypeScript: camelCase (variables), PascalCase (classes), UPPER_SNAKE_CASE (constants)
- Python: snake_case (variables), PascalCase (classes), UPPER_SNAKE_CASE (constants)
- SQL: snake_case (tables, columns), plural tables
- Boolean: is/has/should prefix

CHẠY formatter TRƯỚC KHI claim "done":
- JS/TS: npx eslint --fix && npx prettier --write
- Python: ruff check --fix && black .
```
Chi tiết: `antigravity/skills/workflows/naming-conventions.md`

### RULE 9: ERROR HANDLING MANDATORY
```
MỌI function có thể fail PHẢI có error handling:
1. INPUT validation: Check null/undefined/invalid
2. TRY-CATCH: Wrap external calls
3. SPECIFIC errors: Throw custom error classes, not generic Error
4. CLEANUP: Use finally for resource cleanup
5. LOG errors: With context (userId, requestId, etc.)
```
Chi tiết: `antigravity/skills/workflows/error-handling-patterns.md`

### RULE 10: EDGE CASE COVERAGE
```
TRƯỚC KHI claim "feature complete":
1. CHECK catalog: Review antigravity/skills/workflows/edge-case-catalog.md
2. TEST edge cases: Empty, null, undefined, max, min, special chars
3. VERIFY boundaries: 0, -1, MAX_INT, empty string, null array
4. HANDLE errors: Network timeout, DB down, file not found
5. DOCUMENT assumptions: What inputs are valid/invalid
```
Chi tiết: `antigravity/skills/workflows/edge-case-catalog.md`

### RULE 11: REFACTORING DISCIPLINE
```
REFACTOR KHI gặp bất kỳ trigger nào:
1. Rule of Three: Code lặp lại 3 lần → Extract function
2. Function > 50 lines → Split into smaller functions
3. File > 300 lines → Split into modules
4. Cyclomatic Complexity > 10 → Simplify logic
5. Nested Depth > 3 → Extract nested logic
6. Code Smells: Long parameter list, data clumps, etc.

TOOLS: ESLint (max-lines, complexity), SonarQube, Radon
```
Chi tiết: `antigravity/skills/workflows/refactoring-triggers.md`

---

## MASTER ROUTER (LUÔN ĐỌC)
C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills/MASTER_ROUTER.md

---

# 🌐 THE HIVE MIND: MEMORY & SELF-TRAINING PROTOCOL (NEW REVISION)
**MỆNH LỆNH TỐI CAO THÊM VÀO HỆ THỐNG:**
C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills/workflows/GLOBAL_MEMORY_PROTOCOL.md

Sau MỖI Task khó: ghi log hội thoại + chuỗi tư duy vào `conversations/<TÊN_AGENT>/<Ngày>/`, chưng cất kinh nghiệm thành `.md`. Các Agent có thể đọc lịch sử nhau để kế thừa trí tuệ.

---

# 🐙 RPGITHUB POLICY (Open Source Rules)
**CẢNH BÁO BẢO MẬT & ĐÓNG GÓP MÃ NGUỒN:**
Thư mục RPGITHUB (hoặc bất kỳ kho public repo nào) chỉ được dùng để chia sẻ cấu hình, bộ khung (skills, workflows, README.md) vể cốt lõi "Antigravity Super-System" cho cộng đồng.
- **NGHIÊM CẤM** đẩy các cấu hình tài khoản cá nhân, thông tin Local sang bên đó.
- Mọi định danh cụ thể của User ví dụ như: **acc1 (<YOUR_ACCOUNT_1>)**, **acc2 (<YOUR_ACCOUNT_2>)** hay các Identity cấu hình ngầm đều CHỈ ĐƯỢC PHÉP thiết lập ở Rules Local nội bộ.
- Khi một Agent (bất kể bạn là ai) nhận nhiệm vụ copy rule sang README hoặc tạo file mới trên thư mục RPGITHUB, bắt buộc BẠN phải **TẨY TRẮNG** tài khoản/email và thay bằng Placeholder mô phỏng chuẩn quốc tế (Vd: <YOUR_ACCOUNT>, example@gmail.com).

---

# 🔗 RPGITHUB REPOSITORY LINKAGE
**ĐỊA CHỈ KHO LƯU TRỮ CÔNG KHAI:** C:/Users/<YOUR_USERNAME>/.gemini/RPGITHUB/
- Đây là folder dùng làm hình mẫu (Mirror) để đẩy lên GitHub.
- Mọi Agent khi được yêu cầu "Cập nhật tài liệu cho cộng đồng" hoặc "Update GitHub README", BẮT BUỘC phải thực hiện thao tác trên tệp tin trong thư mục RPGITHUB này.
- **TUYỆT ĐỐI KHÔNG** copy trực tiếp file Rules Local (có chứa acc1/acc2/email) sang RPGITHUB. Chỉ được dùng các file đã được tẩy trắng (Scrubbed) có trong folder đó làm base.

---

# 🚀 GITHUB AUTOMATION PROTOCOL (v1.0.0)
**CƠ CHẾ TỰ ĐỘNG NHẬN DIỆN REPO & PUSH CODE:**
Khi User gửi link Repo GitHub (hoặc screenshot), Agent PHẢI thực hiện:
1. **Trích xuất link:** Tự động lấy URL GitHub.
2. **Khởi tạo Git:** Thực hiện git init, git branch -M main nếu project chưa có Git.
3. **Kết nối Remote:** git remote add origin <LINK_REPO>.
4. **Tạo File push.bat:** Tự động tạo file push.bat tại root của folder project hiện tại.
5. **Nội dung push.bat:** Chứa script tự động git add, git commit -m (với timestamp), và git push.
6. **Bảo mật (Block-List):** Tự động thêm push.bat và các file nhạy cảm vào .gitignore. CẤM đẩy file push.bat lên Public GitHub.
7. **Lưu ý:** Xem chi tiết tại ntigravity/skills/workflows/GITHUB_AUTOMATION_SKILL.md.
