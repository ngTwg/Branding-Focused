# 🚀 QUICK REFERENCE - AI CODING RULES

> **1-page cheat sheet** - Print và dán lên màn hình!  
> **Version:** 1.0.0  
> **Last Updated:** 2026-03-30

---

## ⚡ BEFORE YOU CODE

```
□ Read MASTER_ROUTER.md → Load đúng skills
□ Verify library exists (npm view / pip show)
□ Check API docs (NEVER guess signatures)
□ Review edge cases catalog
□ Plan error handling strategy
```

---

## 🎯 CORE RULES (MUST FOLLOW)

### 1️⃣ NAMING CONVENTIONS
```javascript
// ✅ GOOD
const userName = "John";           // camelCase
class UserService {}               // PascalCase
const MAX_RETRIES = 3;            // UPPER_SNAKE_CASE
const isActive = true;            // Boolean prefix

// ❌ BAD
const UserName = "John";          // Wrong case
const max_retries = 3;            // Wrong case
const active = true;              // Missing prefix
```

### 2️⃣ ANTI-HALLUCINATION
```bash
# ALWAYS verify before using
npm view react-query    # Check exists
pip show pandas         # Check version
```

### 3️⃣ ERROR HANDLING
```javascript
// ✅ GOOD - Specific errors
try {
  await api.call();
} catch (error) {
  if (error instanceof NetworkError) {
    // Handle network
  } else if (error instanceof ValidationError) {
    // Handle validation
  }
  logger.error({ error, userId, requestId });
}

// ❌ BAD - Generic catch
try {
  await api.call();
} catch (e) {
  console.log(e);  // Too generic!
}
```

### 4️⃣ SECURITY CHECKLIST
```
□ No hardcoded secrets (use .env)
□ Validate ALL user inputs
□ Sanitize before DB queries
□ Use parameterized queries
□ Add rate limiting
□ Enable CORS properly
□ Set security headers
```

### 5️⃣ EDGE CASES
```javascript
// Test these ALWAYS
- null, undefined, empty string
- 0, -1, MAX_INT, MIN_INT
- Empty array [], empty object {}
- Special chars: <script>, ', ", \
- Network timeout, DB down
```

---

## 📊 COVERAGE CHECKLIST

| Category | Target | Check |
|----------|--------|-------|
| Naming | 85% | □ |
| Security | 95% | □ |
| Error Handling | 90% | □ |
| Edge Cases | 85% | □ |
| Documentation | 85% | □ |
| Tests | 80% | □ |

---

## 🔥 COMMON MISTAKES

### ❌ Mistake 1: Guessing API signatures
```javascript
// ❌ BAD - Guessing
const data = await fetch(url).json();

// ✅ GOOD - Verified
const response = await fetch(url);
const data = await response.json();
```

### ❌ Mistake 2: Missing input validation
```javascript
// ❌ BAD
function divide(a, b) {
  return a / b;  // What if b = 0?
}

// ✅ GOOD
function divide(a, b) {
  if (b === 0) throw new Error("Division by zero");
  return a / b;
}
```

### ❌ Mistake 3: Hardcoded secrets
```javascript
// ❌ BAD
const API_KEY = "sk-1234567890";

// ✅ GOOD
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error("API_KEY missing");
```

---

## 🛠️ ENFORCEMENT COMMANDS

### JavaScript/TypeScript
```bash
# Format & Lint
npx prettier --write .
npx eslint --fix --max-warnings 0 .

# Type check
npx tsc --noEmit

# Test
npm test -- --coverage --watchAll=false
```

### Python
```bash
# Format & Lint
ruff check --fix .
black .

# Type check
mypy .

# Test
pytest --cov=. --cov-report=term-missing
```

---

## 🚨 BEFORE COMMIT

```bash
# Run ALL these
□ npm run lint (or ruff check)
□ npm run format (or black)
□ npm run type-check (or mypy)
□ npm test (or pytest)
□ git diff (review changes)
□ Update PROJECT_MAP.md if needed
```

---

## 📚 SKILL FILES REFERENCE

| Category | File | When to Use |
|----------|------|-------------|
| **Naming** | `naming-conventions.md` | Before naming anything |
| **Hallucination** | `anti-hallucination-v2.md` | Before using library |
| **Errors** | `error-handling-patterns.md` | When writing try-catch |
| **Security** | `security-middleware-stack.md` | Setting up API |
| **Edge Cases** | `edge-case-catalog.md` | Before claiming "done" |
| **Refactoring** | `refactoring-triggers.md` | Code review time |
| **Concurrency** | `concurrency-patterns.md` | Multi-user features |
| **State** | `state-classification.md` | React state management |
| **API** | `api-design-standards.md` | Designing endpoints |
| **Database** | `database-standards.md` | Schema changes |
| **Logging** | `logging-standards.md` | Adding logs |
| **Environment** | `environment-standards.md` | Config setup |

---

## 🎯 TIER SYSTEM

| Tier | Examples | Requirements |
|------|----------|--------------|
| **1** | Blog, CRUD | Best practices |
| **2** | E-commerce, SaaS | OWASP, GDPR |
| **3** | Social media | Scalability |
| **4** | Medical, Space | Life-critical |

---

## 💡 AI REVIEW CHECKLIST

When reviewing AI-generated code:

```
□ Verify library exists (npm view / pip show)
□ Check API signatures match docs
□ Look for hardcoded values
□ Check error handling exists
□ Verify edge cases covered
□ Check naming conventions
□ Look for security issues
□ Verify tests included
□ Check documentation updated
```

---

## 🆘 EMERGENCY TROUBLESHOOTING

### Problem: AI hallucinating APIs
**Solution:** Run `npm view <package>` or check official docs

### Problem: Code fails in production
**Solution:** Check edge cases catalog, add missing validations

### Problem: Security vulnerability
**Solution:** Review security-middleware-stack.md, add missing layers

### Problem: Memory leak
**Solution:** Review resource-cleanup.md, check useEffect cleanup

### Problem: Race condition
**Solution:** Review concurrency-patterns.md, add locking

---

## 📞 NEED HELP?

1. **Check MASTER_ROUTER.md** - Find right skill
2. **Read specific skill file** - Detailed guidance
3. **Review examples** - ✅ GOOD vs ❌ BAD
4. **Run enforcement tools** - Automated checks
5. **Ask team** - Collective knowledge

---

## 🎓 LEARNING PATH

### Week 1: Foundation
- [ ] Read naming-conventions.md
- [ ] Read anti-hallucination-v2.md
- [ ] Read error-handling-patterns.md

### Week 2: Security
- [ ] Read security-middleware-stack.md
- [ ] Read edge-case-catalog.md

### Week 3: Quality
- [ ] Read refactoring-triggers.md
- [ ] Read concurrency-patterns.md

### Week 4: Standards
- [ ] Read api-design-standards.md
- [ ] Read database-standards.md

---

## 📈 MEASURING SUCCESS

Track these metrics weekly:

```
- Bugs found in code review: ↓ 50%
- Security vulnerabilities: ↓ 80%
- Production incidents: ↓ 70%
- Code review time: ↓ 40%
- Test coverage: ↑ 80%+
```

---

**Print this page and keep it visible while coding!**

**Version:** 1.0.0  
**Coverage:** 96%  
**Skills:** 15 core files  
**Status:** Production-Ready

---

**Quick Links:**
- Full docs: `antigravity/skills/`
- Master Router: `MASTER_ROUTER.md`
- Implementation Plan: `AI_RULES_IMPLEMENTATION_PLAN.md`
- Task Checklist: `AI_RULES_TASKS_CHECKLIST.md`
