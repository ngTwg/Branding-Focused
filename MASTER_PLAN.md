# 📋 MASTER PLAN - KẾ HOẠCH HOÀN THIỆN HỆ THỐNG SKILLS

> **Mục tiêu:** Tổng hợp TẤT CẢ skills vào một hệ thống thống nhất, dễ quản lý, tiết kiệm token
> **Timeline:** Thực hiện từng bước một cách có hệ thống
> **Status:** READY TO EXECUTE

---

## 🎯 TỔNG QUAN

### Hiện trạng:
- ✅ Có `antigravity/skills/` với 25+ skills hiện có
- ✅ Có `antigravity/skills/` với 19 skills đã di chuyển và tổng hợp
- ✅ Có `GEMINI.md` với rules tổng thể (25,167 dòng - QUÁ LỚN!)
- ✅ Có `antigravity/skills/MASTER_ROUTER.md` đã tạo
- ⚠️ Skills rải rác, chưa tổng hợp
- ⚠️ GEMINI.md quá lớn, AI không thể load hết

### Mục tiêu cuối cùng:
1. **Tổng hợp TẤT CẢ skills** vào `antigravity/skills/` (thư mục chuẩn)
2. **GEMINI.md gọn nhẹ** - chỉ chứa rules cơ bản + hướng dẫn chọn skill
3. **Master Router thông minh** - tự động tìm đúng skill
4. **Dễ quản lý** - user và agent đều dễ sử dụng
5. **Tiết kiệm token** - chỉ load skills cần thiết

---

## 📊 PHASE 1: PHÂN TÍCH & INVENTORY (30 phút)

### Step 1.1: Liệt kê TẤT CẢ skills hiện có
```bash
# Quét antigravity/skills/
find .ai-skills -name "*.md" -o -name "skill.md"

# Quét antigravity/skills/
find .ai-skills -name "*.md"

# Tạo inventory file
```

**Output:** `SKILLS_INVENTORY.md` - danh sách đầy đủ tất cả skills

### Step 1.2: Phân loại skills theo category
```
Categories:
- Frontend (React, CSS, Performance, Forms, PWA)
- Backend (API, Database, Auth, Validation, Error, Cache)
- Security (Attack Vectors, Crypto, Compliance)
- DevOps (CI/CD, Container, Observability)
- Workflows (Debug, Code Review, Git, Testing)
- Data Engineering (ETL, Analytics, ML, Streaming)
- Deep Tech (FPGA, Systems, DSP, Compiler, GPU, Crypto)
- Specialized (Blockchain, IoT, Game, EdTech, Fintech, HealthTech, etc.)
- Beyond Horizon (Exascale, Green, XR, Meta-Rules, Astro, etc.)
```

### Step 1.3: Xác định skills trùng lặp
```
Ví dụ:
- antigravity/skills/workflows/systematic-debugging.md
- antigravity/skills/workflows/debug-protocol.md
→ Merge thành một skill duy nhất
```

**Output:** `DUPLICATES_REPORT.md` - danh sách skills trùng lặp

---

## 📦 PHASE 2: TÁI CẤU TRÚC THƯ MỤC (1 giờ)

### Step 2.1: Tạo cấu trúc chuẩn `antigravity/skills/`
```
antigravity/skills/
├── index-skills.md              # Master index
├── MASTER_ROUTER.md             # Router thông minh
│
├── frontend/
│   ├── react-patterns.md
│   ├── css-styling.md
│   ├── web-performance.md
│   ├── forms-validation.md
│   ├── pwa-offline.md
│   ├── web-components.md
│   ├── accessibility-theme.md
│   └── frontend-design.md       # Từ antigravity/skills/ (Migrated)
│
├── backend/
│   ├── api-design.md
│   ├── database-patterns.md
│   ├── authentication.md
│   ├── validation-patterns.md
│   ├── error-handling.md
│   └── caching-strategies.md
│
├── security/
│   ├── attack-vectors.md
│   ├── cryptography.md
│   ├── compliance-regulations.md
│   ├── security-testing.md
│   └── network-security.md
│
├── devops/
│   ├── cicd-pipelines.md
│   ├── containerization.md
│   ├── observability.md
│   ├── infrastructure-as-code.md
│   └── cloud-services.md
│
├── workflows/
│   ├── debug-protocol.md
│   ├── systematic-debugging.md  # Merge từ antigravity
│   ├── code-review.md
│   ├── refactoring.md
│   ├── testing-strategies.md
│   ├── git-workflow.md
│   ├── incident-management.md
│   ├── test-driven-development.md
│   └── verification-before-completion.md
│
├── data-engineering/
│   ├── etl-pipelines.md
│   ├── analytics.md
│   ├── machine-learning.md
│   └── streaming-data.md
│
├── deep-tech/
│   ├── fpga-hardware.md
│   ├── systems-programming.md
│   ├── signal-processing.md
│   ├── compiler-tools.md
│   ├── gpu-computing.md
│   └── advanced-crypto.md
│
├── specialized/
│   ├── blockchain-web3.md
│   ├── iot-embedded.md
│   ├── game-development.md
│   ├── edtech-systems.md
│   ├── fintech-payments.md
│   ├── healthtech-medical.md
│   ├── geospatial-gis.md
│   ├── robotics-autonomous.md
│   ├── quantum-computing.md
│   ├── bioinformatics.md
│   ├── legaltech.md
│   ├── proptech.md
│   ├── retail-supply-chain.md
│   ├── govtech.md
│   ├── humanitarian-tech.md
│   ├── autonomous-logistics.md
│   ├── algorithmic-economics.md
│   ├── generative-media.md
│   ├── neuro-symbolic-ai.md
│   ├── macro-economics-cbdc.md
│   ├── deep-space-networking.md
│   ├── cognitive-security.md
│   └── topological-data-analysis.md
│
└── beyond/
    ├── exascale-computing.md
    ├── green-computing.md
    ├── spatial-os-xr.md
    ├── meta-rules-agentic.md
    ├── astrodynamics.md
    ├── fully-homomorphic-encryption.md
    ├── neuromorphic-snn.md
    ├── topological-data-analysis.md
    ├── compiler-mlir.md
    ├── zero-knowledge-proofs.md
    ├── stochastic-superoptimization.md
    ├── photonic-computing.md
    ├── materials-informatics.md
    ├── plasma-fusion.md
    └── planetary-geoengineering.md
```

### Step 2.2: Script tự động di chuyển
```python
# migrate_all_skills.py
"""
1. Đọc antigravity/skills/ (Source of truth)
2. Phân loại theo category
3. Di chuyển vào antigravity/skills/ đúng thư mục
4. Merge skills trùng lặp
5. Cập nhật references
"""
```

---

## 📝 PHASE 3: TẠO SKILLS MỚI (2 giờ)

### Step 3.1: Tạo skills từ nội dung mở rộng

**Beyond Horizon (12 skills):**
- ✅ exascale-computing.md (ĐÃ TẠO)
- ✅ green-computing.md (ĐÃ TẠO)
- ⏳ spatial-os-xr.md
- ⏳ meta-rules-agentic.md
- ⏳ astrodynamics.md
- ⏳ fully-homomorphic-encryption.md
- ⏳ neuromorphic-snn.md
- ⏳ compiler-mlir.md
- ⏳ zero-knowledge-proofs.md
- ⏳ stochastic-superoptimization.md
- ⏳ photonic-computing.md

**Specialized (thêm 8 skills):**
- ⏳ legaltech.md
- ⏳ proptech.md
- ⏳ retail-supply-chain.md
- ⏳ govtech.md
- ⏳ humanitarian-tech.md
- ⏳ autonomous-logistics.md
- ⏳ algorithmic-economics.md
- ⏳ generative-media.md
- ⏳ neuro-symbolic-ai.md
- ⏳ macro-economics-cbdc.md
- ⏳ deep-space-networking.md
- ⏳ cognitive-security.md
- ⏳ materials-informatics.md
- ⏳ plasma-fusion.md
- ⏳ planetary-geoengineering.md

### Step 3.2: Format chuẩn cho mỗi skill
```markdown
# SKILL NAME

> **Tier:** 1-4
> **Tags:** `[tag1, tag2, tag3]`
> **Khi nào dùng:** Description

---

## OVERVIEW
Brief description

---

## RULES

**RULE-001.** Description
```code example```

**RULE-002.** Description
```code example```

---

## AI LEVERAGE
How AI can help

---

## QUICK REFERENCE
Table or list

---

**Related Skills:**
- skill1.md
- skill2.md

**Version:** 1.0.0
**Last Updated:** 2024-01-15
```

---

## 🔄 PHASE 4: CẬP NHẬT GEMINI.md (1 giờ)

### Step 4.1: Tạo GEMINI.md mới (GỌN NHẸ)

**Nội dung GEMINI.md mới:**
```markdown
# GEMINI.md - QUY TẮC DỰ ÁN

> **Phiên bản:** 3.0.0 - REFACTORED
> **Nguyên tắc:** Gọn nhẹ, chỉ chứa rules cơ bản

---

## 🎯 NGUYÊN TẮC CỐT LÕI

### RULE 1: LUÔN LOAD MASTER ROUTER TRƯỚC
```
TRƯỚC KHI làm BẤT KỲ task nào:
1. ĐỌC: antigravity/skills/MASTER_ROUTER.md
2. PHÂN TÍCH: User request → Tags → Tier
3. LOAD: Skills phù hợp
4. THỰC THI: Theo rules trong skills
```

### RULE 2: CONTEXT PRUNING
```
TRƯỚC KHI chuyển task mới:
1. XÓA rules không liên quan
2. CHỈ giữ skills cần thiết
3. TRÁNH quá tải context
```

### RULE 3: SYSTEMATIC DEBUGGING
```
KHI gặp bug/error:
1. LUÔN load workflows/debug-protocol.md
2. LUÔN load workflows/systematic-debugging.md
3. TUÂN THỦ quy trình systematic
4. KHÔNG guess-and-check
```

### RULE 4: TIER-APPROPRIATE RESPONSE
```
KHI user không rõ tier:
1. HỎI user về tier
2. GIẢI THÍCH sự khác biệt
3. ÁP DỤNG đúng rules của tier đó
```

---

## 📚 HỆ THỐNG SKILLS

Tất cả skills được tổ chức trong `antigravity/skills/`

**Cách sử dụng:**Bước 4:** Đảm bảo AI đọc `antigravity/skills/MASTER_ROUTER.md` trước tiên. Tìm skill phù hợp theo tags
3. Load skill và follow rules

**Categories:**
- Frontend (8+ skills)
- Backend (6+ skills)
- Security (5+ skills)
- DevOps (5+ skills)
- Workflows (9+ skills)
- Data Engineering (4+ skills)
- Deep Tech (6+ skills)
- Specialized (25+ skills)
- Beyond Horizon (15+ skills)

**Tổng cộng:** 80+ skills

---

## 🔗 LIÊN KẾT

- **[Master Router](antigravity/skills/MASTER_ROUTER.md)** - Bộ điều phối
- **[Skills Index](antigravity/skills/index-skills.md)** - Danh sách đầy đủ
- **[Skills Guide](SKILLS_GUIDE.md)** - Hướng dẫn sử dụng

---

## 📊 MA TRẬN PHÂN TẦNG

### TIER 1: Đơn giản & Phổ biến
- Blog, landing page, CRUD app
- Best practices chuẩn

### TIER 2: Bắt buộc & Sống còn
- E-commerce, SaaS, payment
- OWASP, GDPR, PCI-DSS

### TIER 3: Nâng cao
- Social media, real-time
- Microservices, scalability

### TIER 4: Chuyên sâu cực độ
- Medical devices, space systems
- Life-critical, optimize every clock cycle

---

## 🚨 QUY TẮC BẮT BUỘC

1. **Always Load Master Router First**
2. **Context Pruning Before New Task**
3. **Systematic Debugging for Bugs**
4. **Tier-Appropriate Response**
5. **Test Before Claim Complete**

---

**Version:** 3.0.0
**Last Updated:** 2024-01-15
**Total Lines:** ~200 (vs 25,167 trước đây)
```

### Step 4.2: Backup GEMINI.md cũ
```bash
mv GEMINI.md GEMINI_OLD_BACKUP.md
```

---

## 🎨 PHASE 5: TẠO MASTER ROUTER HOÀN CHỈNH (1 giờ)

### Step 5.1: Cập nhật MASTER_ROUTER.md
```markdown
# Thêm mapping cho TẤT CẢ skills mới
# Cập nhật decision tree
# Thêm examples cho mỗi category
```

### Step 5.2: Tạo index-skills.md
```markdown
# INDEX SKILLS - BẢN ĐỒ ĐẦY ĐỦ

Danh sách TẤT CẢ 80+ skills với:
- Tags
- Tier
- File path
- Description ngắn gọn
```

---

## 🧹 PHASE 6: DỌN DẸP & TỐI ƯU (30 phút)

### Step 6.1: Xóa files không cần thiết
```bash
# Xóa duplicates
# Xóa backup files cũ
# Xóa temp files
```

### Step 6.2: Cập nhật tất cả references
```bash
# Tìm và thay thế paths cũ
# Cập nhật links trong README files
# Fix broken references
```

### Step 6.3: Tạo .gitignore
```gitignore
# Backup files
*_BACKUP.md
*_OLD.md
*.bak

# Temp files
*.tmp
*.temp

# OS files
.DS_Store
Thumbs.db
```

---

## ✅ PHASE 7: TESTING & VALIDATION (1 giờ)

### Step 7.1: Test Master Router
```
Test cases:
1. "Tạo app quản lý sách" → Load đúng skills?
2. "Fix bug trong checkout" → Load debug skills first?
3. "Tạo firmware máy bơm insulin" → Tier 4, hỏi FDA?
```

### Step 7.2: Validate structure
```bash
# Check tất cả skills có format đúng
# Check tất cả links hoạt động
# Check không có duplicates
```

### Step 7.3: Test với AI
```
Yêu cầu AI:
1. Load GEMINI.md mới
2. Load MASTER_ROUTER.md
3. Thực hiện sample tasks
4. Verify AI load đúng skills
```

---

## 📚 PHASE 8: DOCUMENTATION (30 phút)

### Step 8.1: Cập nhật README files
```
- Project root README.md
- antigravity/skills/README.md
- Mỗi category README.md
```

### Step 8.2: Tạo CHANGELOG.md
```markdown
# CHANGELOG

## Version 3.0.0 (2024-01-15)

### Major Changes
- ✅ Refactored GEMINI.md (25,167 → 200 lines)
- ✅ Consolidated all skills into antigravity/skills/
- ✅ Created Master Router system
- ✅ Added 40+ new skills
- ✅ Implemented tier system

### Migration
- Moved antigravity/skills/ (Final structure verified)
- Merged duplicate skills
- Standardized format

### New Skills
- Beyond Horizon: 15 skills
- Specialized: 25 skills
- Total: 80+ skills
```

### Step 8.3: Tạo MIGRATION_GUIDE.md
```markdown
# MIGRATION GUIDE

## For Users
1. Old: Read GEMINI.md (25k lines)
2. New: Read GEMINI.md (200 lines) + Load specific skills

## For AI Agents
1. Always load MASTER_ROUTER.md first
2. Follow routing logic
3. Load only needed skills
```

---

## 🎉 PHASE 9: FINAL VERIFICATION (30 phút)

### Checklist:
- [ ] Tất cả skills đã được di chuyển
- [ ] Không còn duplicates
- [ ] GEMINI.md gọn nhẹ (<300 lines)
- [ ] MASTER_ROUTER.md hoàn chỉnh
- [ ] index-skills.md đầy đủ
- [ ] Tất cả links hoạt động
- [ ] Format chuẩn cho tất cả skills
- [ ] Documentation đầy đủ
- [ ] Test cases pass
- [ ] AI có thể sử dụng được

---

## 📊 TIMELINE TỔNG HỢP

| Phase | Duration | Status |
|-------|----------|--------|
| 1. Phân tích & Inventory | 30 min | ⏳ TODO |
| 2. Tái cấu trúc thư mục | 1 hour | ⏳ TODO |
| 3. Tạo skills mới | 2 hours | 🔄 IN PROGRESS (2/40) |
| 4. Cập nhật GEMINI.md | 1 hour | ⏳ TODO |
| 5. Master Router | 1 hour | 🔄 IN PROGRESS |
| 6. Dọn dẹp & Tối ưu | 30 min | ⏳ TODO |
| 7. Testing & Validation | 1 hour | ⏳ TODO |
| 8. Documentation | 30 min | ⏳ TODO |
| 9. Final Verification | 30 min | ⏳ TODO |
| **TOTAL** | **8 hours** | **10% COMPLETE** |

---

## 🚀 EXECUTION ORDER

### Immediate (Bây giờ):
1. ✅ Tạo MASTER_PLAN.md (file này)
2. ⏳ Chạy inventory script
3. ⏳ Tạo SKILLS_INVENTORY.md
4. ⏳ Tạo DUPLICATES_REPORT.md

### Next (Tiếp theo):
5. ⏳ Chạy migrate_all_skills.py
6. ⏳ Tạo 40+ skills mới
7. ⏳ Refactor GEMINI.md
8. ⏳ Hoàn thiện MASTER_ROUTER.md

### Final (Cuối cùng):
9. ⏳ Testing
10. ⏳ Documentation
11. ⏳ Verification
12. ✅ COMPLETE!

---

## 📝 NOTES

### Nguyên tắc thực hiện:
1. **Từng bước một** - không skip
2. **Test sau mỗi phase** - đảm bảo hoạt động
3. **Backup trước khi xóa** - an toàn dữ liệu
4. **Document mọi thứ** - dễ maintain sau này

### Ưu tiên:
1. **Gọn nhẹ** - GEMINI.md <300 lines
2. **Dễ dùng** - Master Router tự động
3. **Tiết kiệm token** - chỉ load cần thiết
4. **Đầy đủ** - 80+ skills bao trùm mọi lĩnh vực

---

## 🎯 SUCCESS CRITERIA

Hệ thống được coi là HOÀN THÀNH khi:
- ✅ GEMINI.md <300 lines
- ✅ 80+ skills trong antigravity/skills/
- ✅ Master Router hoạt động
- ✅ AI load đúng skills
- ✅ User dễ quản lý
- ✅ Documentation đầy đủ
- ✅ Test cases pass

---

**Created by:** Kiro AI Assistant
**Date:** 2024-01-15
**Status:** READY TO EXECUTE
**Next Action:** Run inventory script
