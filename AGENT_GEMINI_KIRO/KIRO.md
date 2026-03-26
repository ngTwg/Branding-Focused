---
inclusion: always
---

# QUY TẮC DỰ ÁN - KIRO STEERING (v4.0.0)

## NGUYÊN TẮC CỐT LÕI

### RULE 1: MASTER ROUTER
Trước mọi task → đọc MASTER ROUTER tại `{Antigravity_ROOT}/skills/MASTER_ROUTER.md`, phân tích Tags → Tier → load đúng skill.

### RULE 2: CONTEXT PRUNING
Khi chuyển task mới: xóa skills không liên quan, chỉ giữ cần thiết.

### RULE 3: SYSTEMATIC DEBUGGING
Gặp bug → load `{Antigravity_ROOT}/skills/workflows/debug-protocol.md` TRƯỚC. CẤM guess-and-check.

### RULE 4: TIER SYSTEM
- Tier 1: Blog, CRUD, landing page
- Tier 2: E-commerce, SaaS, payment (OWASP, GDPR)
- Tier 3: Real-time, microservices, scalability
- Tier 4: Medical, space, life-critical

Không rõ tier → hỏi user trước.

### RULE 5: PROJECT PROTOCOLS
- New project: tạo `PROJECT_MAP.md`, `.gitignore`, `README.md`
- Git commit: `type(scope): description`
- JUST DO IT — không hỏi "would you like me to...?"
- Test Before Claim Complete

---

## MASTER ROUTER (LUÔN ĐỌC)
{Antigravity_ROOT}/skills/MASTER_ROUTER.md

---

# 🌐 THE HIVE MIND: MEMORY & SELF-TRAINING PROTOCOL (NEW REVISION)
**MỆNH LỆNH TỐI CAO THÊM VÀO HỆ THỐNG:**
{Antigravity_ROOT}/skills/workflows/GLOBAL_MEMORY_PROTOCOL.md

Sau MỖI Task khó: ghi log hội thoại + chuỗi tư duy vào `conversations/<TÊN_AGENT>/<Ngày>/`, chưng cất kinh nghiệm thành `.md`. Các Agent có thể đọc lịch sử nhau để kế thừa trí tuệ.

---

# 🐙 Global Repository POLICY (Open Source Rules)
**CẢNH BÁO BẢO MẬT & ĐÓNG GÓP MÃ NGUỒN:**
Thư mục Global Repository (hoặc bất kỳ kho public repo nào) chỉ được dùng để chia sẻ cấu hình, bộ khung (skills, workflows, README.md) vể cốt lõi "Antigravity Super-System" cho cộng đồng.
- **NGHIÊM CẤM** đẩy các cấu hình tài khoản cá nhân, thông tin Local sang bên đó.
- Mọi định danh cụ thể của User ví dụ như: **acc1 ([SCRUBBED_USER] hmail)**, **acc2 ([SCRUBBED_USER])** hay các Identity cấu hình ngầm đều CHỈ ĐƯỢC PHÉP thiết lập ở Rules Local nội bộ.
- Khi một Agent (bất kể bạn là ai) nhận nhiệm vụ copy rule sang README hoặc tạo file mới trên thư mục Global Repository, bắt buộc BẠN phải **TẨY TRẮNG** tài khoản/email và thay bằng Placeholder mô phỏng chuẩn quốc tế (Vd: <YOUR_ACCOUNT>, agent@antigravity-system.io).

---

# 🔗 Global Repository REPOSITORY LINKAGE
**ĐỊA CHỈ KHO LƯU TRỮ CÔNG KHAI:** C:/Users/<USER_NAME>/.gemini/Global Repository/
- Đây là folder dùng làm hình mẫu (Mirror) để đẩy lên GitHub.
- Mọi Agent khi được yêu cầu "Cập nhật tài liệu cho cộng đồng" hoặc "Update GitHub README", BẮT BUỘC phải thực hiện thao tác trên tệp tin trong thư mục Global Repository này.
- **TUYỆT ĐỐI KHÔNG** copy trực tiếp file Rules Local (có chứa acc1/acc2/email) sang Global Repository. Chỉ được dùng các file đã được tẩy trắng (Scrubbed) có trong folder đó làm base.

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
7. **Lưu ý:** Xem chi tiết tại antigravity/skills/workflows/GITHUB_AUTOMATION_SKILL.md.
