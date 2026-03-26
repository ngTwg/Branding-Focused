# 📚 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG SKILLS

> **Dành cho:** Users và AI Agents
> **Version:** 2.0.0
> **Last Updated:** 2024-01-15

---

## 🎯 TÓM TẮT

Hệ thống skills đã được tổ chức lại hoàn toàn với:
- ✅ **252 skills** được phân loại khoa học
- ✅ **Master Router** thông minh tự động tìm đúng skill
- ✅ **4 tầng phân cấp** (Tier 1-4) từ đơn giản đến chuyên sâu
- ✅ **9 categories** bao trùm mọi lĩnh vực công nghệ

---

## 🚀 QUICK START

### Cho AI Agents:

```markdown
TRƯỚC KHI làm BẤT KỲ task nào:

1. ĐỌC: antigravity/skills/MASTER_ROUTER.md
2. PHÂN TÍCH: User request → Tags → Tier
3. LOAD: Skills phù hợp
4. THỰC THI: Theo rules trong skills
```

### Cho Users:

Bạn không cần làm gì! Chỉ cần:
1. Nói với AI những gì bạn muốn
2. AI sẽ tự động load đúng skills
3. AI sẽ làm việc theo chuẩn chuyên nghiệp

---

## 📖 CÁC TÌNH HUỐNG SỬ DỤNG

### Tình huống 1: Tạo Web App đơn giản

**User nói:**
```
"Tạo app quản lý sách với React và Supabase"
```

**AI sẽ tự động:**
1. Load `MASTER_ROUTER.md`
2. Nhận diện: [React, Web, CRUD, Database] → Tier 1-2
3. Load skills:
   - `frontend/react-patterns.md`
   - `backend/api-design.md`
   - `backend/database-patterns.md`
   - `security/attack-vectors.md` (XSS, SQL injection)
4. Code theo chuẩn Tier 1-2

**Kết quả:**
- Code sạch, có validation
- Bảo mật cơ bản (OWASP)
- Best practices React
- Database design tốt

---

### Tình huống 2: Fix Bug

**User nói:**
```
"App bị crash khi user checkout"
```

**AI sẽ tự động:**
1. Load `MASTER_ROUTER.md`
2. Nhận diện: [Debug, Bug, Payment]
3. Load skills (PRIORITY):
   - `workflows/debug-protocol.md` (FIRST!)
   - `systematic-debugging/skill.md` (FIRST!)
   - `specialized/fintech-payments.md` (context)
4. Follow systematic debugging:
   - Reproduce bug
   - Isolate root cause
   - Fix properly
   - Verify fix

**Kết quả:**
- Không guess-and-check
- Tìm đúng root cause
- Fix đúng vấn đề
- Add test để prevent regression

---

### Tình huống 3: Medical Device (CRITICAL)

**User nói:**
```
"Tạo firmware cho máy bơm insulin tự động"
```

**AI sẽ tự động:**
1. Load `MASTER_ROUTER.md`
2. Nhận diện: [Medical, IoT, Embedded, Life-Critical] → Tier 4
3. **HỎI USER:** "Thiết bị này cần FDA approval không?"
4. Load skills:
   - `specialized/healthtech-medical.md` (IEC 62304)
   - `specialized/iot-embedded.md` (Bare-metal, RTOS)
   - `security/compliance-regulations.md` (HIPAA)
   - `workflows/testing-strategies.md` (Critical testing)
5. Code với Tier 4 rules:
   - Hard fail-safe mechanisms
   - Traceability mọi dòng code
   - Extensive testing
   - Compliance documentation

**Kết quả:**
- Code đạt chuẩn y tế (IEC 62304)
- Fail-safe mechanisms
- Extensive documentation
- Ready for FDA submission

---

## 🎓 HIỂU VỀ TIER SYSTEM

### Tier 1: Đơn giản & Phổ biến
**Ví dụ:**
- Blog cá nhân
- Landing page
- CRUD app đơn giản
- Portfolio website

**Đặc điểm:**
- Fast development
- Best practices chuẩn
- Bảo mật cơ bản

---

### Tier 2: Bắt buộc & Sống còn
**Ví dụ:**
- E-commerce site
- SaaS application
- Payment system
- User authentication

**Đặc điểm:**
- OWASP Top 10
- GDPR/PCI-DSS compliance
- Proper error handling
- Audit logs

---

### Tier 3: Nâng cao
**Ví dụ:**
- Social media platform
- Real-time collaboration
- High-traffic API
- Microservices architecture

**Đặc điểm:**
- Scalability (millions of users)
- Real-time features
- Advanced caching
- Load balancing

---

### Tier 4: Chuyên sâu cực độ
**Ví dụ:**
- Medical devices
- Autonomous vehicles
- Space systems
- Financial trading systems
- Quantum computing

**Đặc điểm:**
- Life-critical or mission-critical
- Extreme reliability
- Regulatory compliance
- Formal verification
- Optimize every clock cycle

---

## 📊 DANH SÁCH SKILLS THEO CATEGORY

### 🎨 Frontend & UI (8+ skills)
- React patterns, hooks, state management
- CSS, Tailwind, animations
- Web performance, Core Web Vitals
- Forms, validation
- PWA, offline-first
- Accessibility, WCAG
- Web Components
- Dark mode, theming

### ⚙️ Backend & API (6+ skills)
- REST API design
- Database patterns, indexing
- Authentication, JWT, OAuth
- Input validation
- Error handling
- Caching strategies

### 🔒 Security & Compliance (5+ skills)
- OWASP Top 10, attack vectors
- Cryptography, encryption
- Compliance (HIPAA, GDPR, PCI-DSS)
- Security testing, pentesting
- Network security, zero trust

### 🚀 DevOps & Infrastructure (5+ skills)
- Docker, Kubernetes
- CI/CD pipelines
- Infrastructure as Code
- Monitoring, observability
- Cloud services (AWS, GCP, Azure)

### 🔄 Workflows & Processes (8+ skills)
- Systematic debugging
- Code review
- Refactoring
- Testing strategies
- Git workflow
- Incident management
- Test-driven development
- Verification before completion

### 📊 Data Engineering (4+ skills)
- ETL pipelines
- Analytics, BI
- Machine learning
- Real-time streaming

### 🔬 Deep Tech & Advanced (6+ skills)
- FPGA, hardware description
- Systems programming, kernel
- Signal processing
- Compiler infrastructure, MLIR
- GPU computing, CUDA
- Advanced cryptography, ZKP

### 🏥 Specialized Domains (20+ skills)
- Blockchain, Web3, smart contracts
- IoT, embedded systems
- Game development
- EdTech, assessment systems
- Fintech, payment systems
- HealthTech, medical devices (IEC 62304)
- GIS, geospatial
- Robotics, autonomous systems
- LegalTech, compliance automation
- PropTech, smart buildings
- Retail, supply chain
- GovTech, civic infrastructure
- Humanitarian tech, disaster response
- Autonomous logistics, drones
- Algorithmic economics, tokenization
- Generative media, AI studios
- Neuro-symbolic AI
- Macro-economics, CBDC
- Deep space networking
- Cognitive security, information warfare

### 🌌 Beyond Horizon (12+ skills)
- Exascale computing, supercomputing
- Green computing, carbon-aware
- Spatial OS, XR compositors
- Meta-rules, agentic protocols
- Astrodynamics, orbital networks
- Fully homomorphic encryption (FHE)
- Neuromorphic engineering, SNNs
- Topological data analysis
- Compiler infrastructure, MLIR
- Zero-knowledge proofs
- Stochastic superoptimization
- Photonic computing
- Materials informatics
- Plasma physics, fusion reactors
- Planetary geoengineering

---

## 🎯 TIPS CHO USERS

### Tip 1: Nói rõ tier nếu biết
```
❌ "Tạo app y tế"
✅ "Tạo app y tế Tier 4 - máy đo nhịp tim cần FDA approval"
```

### Tip 2: Mention domain cụ thể
```
❌ "Fix bug"
✅ "Fix bug trong payment flow khi user checkout"
```

### Tip 3: Nói rõ constraints
```
❌ "Tạo website"
✅ "Tạo website cần WCAG 2.1 AA compliance và GDPR compliant"
```

### Tip 4: Trust the system
```
AI sẽ tự động:
- Load đúng skills
- Hỏi clarifying questions nếu cần
- Apply đúng tier rules
- Follow best practices
```

---

## 🚨 QUY TẮC QUAN TRỌNG

### Rule 1: Systematic Debugging
```
KHI gặp bug:
❌ KHÔNG guess-and-check
✅ LUÔN follow systematic debugging process
```

### Rule 2: Security First
```
KHI code bất kỳ feature nào:
❌ KHÔNG skip security checks
✅ LUÔN apply OWASP best practices
```

### Rule 3: Test Before Claim
```
KHI nói "done" hoặc "fixed":
❌ KHÔNG claim without verification
✅ LUÔN run tests và verify output
```

### Rule 4: Tier-Appropriate
```
KHI code:
❌ KHÔNG apply Tier 4 rules cho Tier 1 project
✅ LUÔN match complexity với requirements
```

---

## 📞 TROUBLESHOOTING

### Problem: AI không load đúng skills
**Solution:**
1. Check `MASTER_ROUTER.md` có đúng mapping không
2. Verify tags trong request
3. Clarify tier với AI

### Problem: Code quá phức tạp cho simple app
**Solution:**
1. Nói rõ: "This is a Tier 1 simple app"
2. AI sẽ adjust complexity

### Problem: Code thiếu security
**Solution:**
1. Mention: "This needs Tier 2 security"
2. AI sẽ apply OWASP rules

---

## 🎓 HỌC THÊM

### Đọc thêm:
- `antigravity/skills/MASTER_ROUTER.md` - Hiểu routing logic
- `antigravity/skills/README.md` - Overview hệ thống
- Individual skill files - Deep dive vào từng topic

### Practice:
- Thử với simple requests
- Observe AI's skill loading process
- Learn from AI's responses

---

## 📝 CHANGELOG

### Version 2.0.0 (2024-01-15)
- ✅ Tổ chức lại toàn bộ skills system
- ✅ Tạo Master Router thông minh
- ✅ Phân loại 252 skills theo tier và category
- ✅ Tích hợp nội dung mở rộng (60+ chuyên mục)
- ✅ Tạo documentation đầy đủ

### Version 1.0.0
- Initial skills collection

---

**Maintained by:** Antigravity Skills System
**Questions?** Check `MASTER_ROUTER.md` or individual skill files
**Contributing:** Follow skill creation guidelines
