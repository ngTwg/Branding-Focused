# 📋 HƯỚNG DẪN THỰC HIỆN CÁC TASKS MANUAL

> **Mục đích:** Hướng dẫn chi tiết cách thực hiện các tasks còn lại  
> **Đối tượng:** Team Lead, DevOps, Developers  
> **Thời gian:** 4-8 tuần  
> **Version:** 1.0.0

---

## 🎯 TỔNG QUAN

Tất cả documentation và automation templates đã hoàn thành. Các tasks còn lại là **áp dụng thực tế** vào project và team.

### Phân loại tasks:
1. **Setup & Configuration** (Week 15-16) - Technical
2. **Training & Adoption** (Month 2) - People
3. **Monitoring & Optimization** (Quarter 2) - Process

---

## 📅 WEEK 15-16: SETUP & CONFIGURATION

### Task 1: Setup Pre-commit Hooks trong Sample Project

**Mục tiêu:** Cài đặt pre-commit hooks để test trước khi rollout toàn team

**Người thực hiện:** DevOps / Tech Lead

**Thời gian:** 2-3 giờ

**Các bước thực hiện:**

#### Bước 1: Chọn Sample Project
```bash
# Chọn 1 project nhỏ để test
cd /path/to/sample-project

# Verify project có package.json hoặc requirements.txt
ls -la
```

#### Bước 2: Install Dependencies (JavaScript/TypeScript)
```bash
# Theo hướng dẫn trong PRE_COMMIT_SETUP_GUIDE.md
npm install --save-dev husky lint-staged
npm install --save-dev @secretlint/secretlint-rule-preset-recommend
npm install --save-dev @secretlint/quick-start

# Initialize husky
npx husky install
npm pkg set scripts.prepare="husky install"

# Create pre-commit hook
npx husky add .husky/pre-commit "npx lint-staged"
```

#### Bước 3: Configure lint-staged
Thêm vào `package.json`:
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix --max-warnings 0",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    "*.{js,jsx,ts,tsx,json,md}": [
      "secretlint"
    ]
  }
}
```

#### Bước 4: Test Pre-commit Hook
```bash
# Tạo test file
echo "const test = 123" > test.js

# Try commit
git add test.js
git commit -m "Test pre-commit hook"

# Expected: Hook chạy và format code
# Verify: Check test.js đã được format

# Clean up
git reset HEAD test.js
rm test.js
```

#### Bước 5: Document Issues
Tạo file `PRE_COMMIT_ISSUES.md` ghi lại:
- Issues gặp phải
- Solutions
- Team feedback
- Adjustments needed

**Deliverable:** Sample project với pre-commit hooks hoạt động

---

### Task 2: Test CI/CD Pipeline trên Real Project

**Mục tiêu:** Verify CI/CD templates hoạt động với real project

**Người thực hiện:** DevOps Engineer

**Thời gian:** 3-4 giờ

**Các bước thực hiện:**

#### Bước 1: Chọn Test Project
```bash
# Chọn project có:
- Git repository
- Tests đã có
- Build process
- Không critical (để test an toàn)
```

#### Bước 2: Setup GitHub Actions
```bash
# Tạo workflow file
mkdir -p .github/workflows
cp CI_CD_PIPELINE_TEMPLATE.md .github/workflows/ci.yml

# Edit ci.yml:
# - Adjust Node version
# - Update test commands
# - Configure secrets
```

#### Bước 3: Add GitHub Secrets
Vào GitHub repo → Settings → Secrets:
```
- CODECOV_TOKEN (nếu dùng Codecov)
- VERCEL_TOKEN (nếu deploy Vercel)
- SLACK_WEBHOOK (nếu dùng notifications)
```

#### Bước 4: Test Pipeline
```bash
# Create test branch
git checkout -b test-ci-pipeline

# Make small change
echo "# Test CI" >> README.md

# Commit and push
git add README.md
git commit -m "test: CI pipeline"
git push origin test-ci-pipeline

# Create PR và observe:
- Lint job runs
- Test job runs
- Security scan runs
- Build succeeds
```

#### Bước 5: Review Results
Check:
- [ ] All jobs pass
- [ ] Coverage report uploaded
- [ ] Security scan completes
- [ ] Build artifacts created
- [ ] Notifications sent (if configured)

#### Bước 6: Document
Tạo `CI_CD_TEST_RESULTS.md`:
```markdown
## Test Results

### Jobs Status
- Lint: ✅ Pass (2m 30s)
- Test: ✅ Pass (5m 15s)
- Security: ✅ Pass (3m 45s)
- Build: ✅ Pass (4m 20s)

### Issues Found
1. [Issue description]
   - Solution: [How fixed]

### Adjustments Made
1. [Adjustment description]
   - Reason: [Why needed]

### Recommendations
1. [Recommendation for rollout]
```

**Deliverable:** Working CI/CD pipeline + test results document

---

## 📚 MONTH 2: TRAINING & ADOPTION

### Task 3: Team Training Sessions (4 x 1 hour)

**Mục tiêu:** Train team về 15 skills mới

**Người thực hiện:** Tech Lead / Senior Developer

**Thời gian:** 4 tuần (1 session/week)

**Format:** 1 hour session = 40 min presentation + 20 min Q&A

---

#### Session 1: Foundation Skills (Week 1)

**Topics:**
1. Naming Conventions (15 min)
2. Anti-Hallucination Protocol (15 min)
3. Error Handling Patterns (10 min)

**Agenda:**
```
00:00-00:05: Introduction & Overview
00:05-00:20: Naming Conventions
  - Demo: Bad vs Good examples
  - Live coding: Fix naming issues
  - Tool: Run eslint --fix

00:20-00:35: Anti-Hallucination
  - Demo: Verify library exists
  - Live coding: Check API docs
  - Tool: npm view, pip show

00:35-00:45: Error Handling
  - Demo: 6 patterns
  - Live coding: Add try-catch
  - Tool: Error boundaries

00:45-01:00: Q&A + Hands-on Exercise
```

**Materials:**
- Slides: Extract from skill files
- Code examples: From QUICK_REFERENCE.md
- Exercise: Fix 5 naming issues in sample code

**Homework:**
- Read: naming-conventions.md
- Practice: Fix naming in your current PR
- Quiz: 10 questions (Google Form)

---

#### Session 2: Security & Quality (Week 2)

**Topics:**
1. Security Middleware Stack (15 min)
2. Edge Case Catalog (15 min)
3. Refactoring Triggers (10 min)

**Agenda:**
```
00:00-00:05: Recap Session 1
00:05-00:20: Security Middleware
  - Demo: 7-layer defense
  - Live coding: Add Helmet.js
  - Tool: npm audit

00:20-00:35: Edge Cases
  - Demo: 70+ edge cases
  - Live coding: Add validation
  - Tool: Test edge cases

00:35-00:45: Refactoring
  - Demo: 6 triggers
  - Live coding: Extract function
  - Tool: ESLint complexity

00:45-01:00: Q&A + Security Exercise
```

**Materials:**
- Security checklist
- Edge case examples
- Refactoring before/after

**Homework:**
- Read: security-middleware-stack.md
- Practice: Add 1 security layer to your API
- Quiz: Security scenarios

---

#### Session 3: Advanced Patterns (Week 3)

**Topics:**
1. Concurrency Patterns (15 min)
2. State Classification (15 min)
3. Resource Cleanup (10 min)

**Agenda:**
```
00:00-00:05: Recap Session 2
00:05-00:20: Concurrency
  - Demo: Race conditions
  - Live coding: Add locking
  - Tool: Test concurrent scenarios

00:20-00:35: State Management
  - Demo: 7 state types
  - Live coding: Classify state
  - Tool: React DevTools

00:35-00:45: Resource Cleanup
  - Demo: Memory leaks
  - Live coding: Add cleanup
  - Tool: Chrome DevTools

00:45-01:00: Q&A + Debugging Exercise
```

**Materials:**
- Concurrency examples
- State decision tree
- Memory leak demos

**Homework:**
- Read: concurrency-patterns.md
- Practice: Fix race condition in your code
- Quiz: State classification

---

#### Session 4: API & Standards (Week 4)

**Topics:**
1. API Design Standards (15 min)
2. Database Standards (15 min)
3. Logging & Environment (10 min)

**Agenda:**
```
00:00-00:05: Recap Session 3
00:05-00:20: API Design
  - Demo: REST best practices
  - Live coding: Design endpoint
  - Tool: OpenAPI spec

00:20-00:35: Database
  - Demo: Schema design
  - Live coding: Write migration
  - Tool: Database tools

00:35-00:45: Logging & Env
  - Demo: Structured logging
  - Live coding: Add logs
  - Tool: Zod validation

00:45-01:00: Q&A + Final Exercise
```

**Materials:**
- API examples
- Database patterns
- Logging templates

**Homework:**
- Read: All remaining skills
- Practice: Apply to current project
- Final Quiz: Comprehensive

---

### Task 4: Code Review Checklist Integration

**Mục tiêu:** Integrate skills vào code review process

**Người thực hiện:** Tech Lead

**Thời gian:** 2-3 giờ

**Các bước thực hiện:**

#### Bước 1: Tạo Code Review Template
Tạo `.github/PULL_REQUEST_TEMPLATE.md`:
```markdown
## Description
[Describe changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## AI Rules Checklist

### Naming (RULE 8)
- [ ] Variables: camelCase
- [ ] Classes: PascalCase
- [ ] Constants: UPPER_SNAKE_CASE
- [ ] Booleans: is/has/should prefix

### Anti-Hallucination (RULE 7)
- [ ] All libraries verified (npm view / pip show)
- [ ] API signatures checked against docs
- [ ] No guessed implementations

### Error Handling (RULE 9)
- [ ] Input validation added
- [ ] Try-catch for external calls
- [ ] Specific error types used
- [ ] Cleanup in finally blocks

### Security (RULE 6)
- [ ] No hardcoded secrets
- [ ] Input sanitization added
- [ ] OWASP checks passed
- [ ] Auth/authorization verified

### Edge Cases (RULE 10)
- [ ] Null/undefined handled
- [ ] Empty arrays/objects handled
- [ ] Boundary values tested
- [ ] Error scenarios covered

### Code Quality (RULE 11)
- [ ] No code duplication (Rule of Three)
- [ ] Functions < 50 lines
- [ ] Files < 300 lines
- [ ] Complexity < 10

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added (if needed)
- [ ] Coverage > 80%
- [ ] All tests pass

## Documentation
- [ ] README updated (if needed)
- [ ] PROJECT_MAP updated (if code structure changed)
- [ ] ADR created (if architecture changed)
- [ ] Comments added for complex logic

## Pre-merge Checklist
- [ ] Pre-commit hooks pass
- [ ] CI pipeline passes
- [ ] No merge conflicts
- [ ] Approved by reviewer
```

#### Bước 2: Update GitHub Settings
Settings → Branches → Branch protection rules:
```
- Require pull request reviews (1 approval)
- Require status checks to pass
- Require conversation resolution
- Include administrators
```

#### Bước 3: Train Reviewers
Tạo `CODE_REVIEW_GUIDE.md`:
```markdown
# Code Review Guide

## What to Look For

### 1. Naming (5 min)
- Check variable names
- Check function names
- Check file names
- Tool: Search for bad patterns

### 2. Security (10 min)
- Check for secrets
- Check input validation
- Check SQL queries
- Tool: GitHub secret scanning

### 3. Error Handling (5 min)
- Check try-catch blocks
- Check error types
- Check cleanup
- Tool: Search for "catch (e)"

### 4. Edge Cases (10 min)
- Check null handling
- Check empty arrays
- Check boundary values
- Tool: Read tests

### 5. Code Quality (10 min)
- Check function length
- Check complexity
- Check duplication
- Tool: ESLint reports

## Review Checklist
[Use PR template checklist]

## Common Issues
[Link to QUICK_REFERENCE.md]
```

**Deliverable:** PR template + review guide

---

### Task 5: Metrics Dashboard Setup

**Mục tiêu:** Track adoption và effectiveness của rules

**Người thực hiện:** DevOps / Data Engineer

**Thời gian:** 4-6 giờ

**Các bước thực hiện:**

#### Bước 1: Define Metrics
```javascript
// metrics.js
const metrics = {
  // Code Quality
  bugsInCodeReview: {
    before: 45, // % of PRs with bugs
    target: 20,
    current: 0, // Track weekly
  },
  
  // Security
  securityVulnerabilities: {
    before: 12, // per month
    target: 3,
    current: 0,
  },
  
  // Productivity
  codeReviewTime: {
    before: 60, // minutes average
    target: 35,
    current: 0,
  },
  
  // Coverage
  testCoverage: {
    before: 65, // %
    target: 80,
    current: 0,
  },
  
  // Adoption
  preCommitHooksUsage: {
    target: 95, // % of team
    current: 0,
  },
  
  ciPipelineSuccess: {
    target: 90, // % of runs
    current: 0,
  },
};
```

#### Bước 2: Setup Data Collection
```bash
# Option 1: GitHub API
# Collect từ GitHub:
- PR comments (bugs found)
- Security alerts
- CI/CD run times
- Test coverage reports

# Option 2: Custom Script
# Parse logs và tạo metrics
```

#### Bước 3: Create Dashboard
```
Tools options:
1. Grafana + Prometheus (self-hosted)
2. Datadog (cloud)
3. Google Sheets (simple)
4. Custom React dashboard
```

#### Bước 4: Simple Google Sheets Dashboard
```
Sheet 1: Weekly Metrics
- Week | Bugs | Security | Review Time | Coverage

Sheet 2: Charts
- Line chart: Bugs over time
- Bar chart: Coverage by project
- Pie chart: Rule adoption

Sheet 3: Team Adoption
- Developer | Pre-commit | CI Pass Rate | Avg Review Time
```

#### Bước 5: Automate Updates
```bash
# Script chạy weekly
# Collect metrics từ GitHub
# Update Google Sheets via API
# Send summary email
```

**Deliverable:** Dashboard tracking 5-10 key metrics

---

### Task 6: Adoption Tracking

**Mục tiêu:** Monitor team adoption của rules

**Người thực hiện:** Tech Lead

**Thời gian:** 1-2 giờ/week

**Các bước thực hiện:**

#### Bước 1: Create Adoption Checklist
```markdown
# Team Adoption Checklist

## Per Developer

### Week 1-2: Awareness
- [ ] Attended training session 1
- [ ] Read QUICK_REFERENCE.md
- [ ] Completed quiz 1

### Week 3-4: Practice
- [ ] Attended training session 2
- [ ] Applied rules in 1 PR
- [ ] Completed quiz 2

### Week 5-6: Adoption
- [ ] Pre-commit hooks installed
- [ ] 3+ PRs with rules applied
- [ ] Peer reviewed 2+ PRs

### Week 7-8: Mastery
- [ ] All training completed
- [ ] 90%+ rule compliance
- [ ] Helping others
```

#### Bước 2: Track Weekly
```
Spreadsheet columns:
- Developer Name
- Training Attended (1-4)
- PRs with Rules Applied
- Pre-commit Hooks Installed
- Quiz Scores
- Compliance Rate
- Status (Beginner/Intermediate/Advanced)
```

#### Bước 3: Weekly Check-in
```
Every Friday:
1. Review adoption metrics
2. Identify blockers
3. Provide support
4. Celebrate wins
```

#### Bước 4: Monthly Report
```markdown
# Monthly Adoption Report

## Summary
- Team size: 10
- Adoption rate: 80%
- Compliance rate: 75%

## By Developer
| Name | Status | Compliance | Notes |
|------|--------|------------|-------|
| Dev1 | Advanced | 95% | Excellent |
| Dev2 | Intermediate | 70% | Needs support |

## Blockers
1. [Blocker description]
   - Action: [How to resolve]

## Next Month Goals
1. [Goal 1]
2. [Goal 2]
```

**Deliverable:** Weekly tracking + monthly reports

---

## 📊 QUARTER 2: MONITORING & OPTIMIZATION

### Task 7: Measure ROI for Each Rule

**Mục tiêu:** Quantify impact của từng rule

**Người thực hiện:** Tech Lead + Product Manager

**Thời gian:** 4-6 giờ

**Các bước thực hiện:**

#### Bước 1: Define ROI Metrics
```javascript
const ruleROI = {
  'RULE 6: Security': {
    metric: 'Security vulnerabilities prevented',
    before: 12, // per month
    after: 2,
    reduction: 83, // %
    timesSaved: 40, // hours (fixing vulnerabilities)
    costSaved: 8000, // $ (40h * $200/h)
  },
  
  'RULE 7: Anti-Hallucination': {
    metric: 'Bugs from wrong API usage',
    before: 25,
    after: 5,
    reduction: 80,
    timeSaved: 30,
    costSaved: 6000,
  },
  
  // ... for each rule
};
```

#### Bước 2: Collect Data
```
Sources:
- GitHub issues (bugs tagged)
- Jira tickets (time spent)
- Code review comments
- Production incidents
- Developer surveys
```

#### Bước 3: Calculate ROI
```
ROI Formula:
ROI = (Time Saved * Hourly Rate - Implementation Cost) / Implementation Cost * 100%

Example:
- Time saved: 200 hours
- Hourly rate: $200
- Value: $40,000
- Implementation cost: $14,000 (70h * $200)
- ROI: ($40,000 - $14,000) / $14,000 * 100% = 186%
```

#### Bước 4: Create Report
```markdown
# ROI Report - AI Rules Implementation

## Overall ROI
- Investment: $14,000 (70 hours)
- Return: $52,000 (260 hours saved)
- ROI: 271%
- Payback period: 2 months

## By Rule
| Rule | Time Saved | Cost Saved | ROI |
|------|------------|------------|-----|
| RULE 6 | 40h | $8,000 | 300% |
| RULE 7 | 30h | $6,000 | 250% |
| ... | ... | ... | ... |

## Intangible Benefits
- Improved code quality
- Faster onboarding
- Better team confidence
- Reduced technical debt
```

**Deliverable:** ROI report with quantified impact

---

### Task 8: Quarterly Rule Review

**Mục tiêu:** Review và update rules based on usage

**Người thực hiện:** Tech Lead + Team

**Thời gian:** 2-3 giờ/quarter

**Các bước thực hiện:**

#### Bước 1: Collect Feedback
```
Survey questions:
1. Which rules are most useful? (1-5 scale)
2. Which rules are too strict?
3. Which rules are unclear?
4. What's missing?
5. Suggestions for improvement?
```

#### Bước 2: Analyze Usage
```
Metrics:
- Rule compliance rate (by rule)
- Rule violation frequency
- Time spent on each rule
- Developer satisfaction
```

#### Bước 3: Review Meeting
```
Agenda (2 hours):
1. Present usage data (15 min)
2. Discuss feedback (30 min)
3. Identify issues (30 min)
4. Propose changes (30 min)
5. Vote on changes (15 min)
```

#### Bước 4: Update Rules
```
Actions:
- Clarify unclear rules
- Relax overly strict rules
- Add missing rules
- Deprecate unused rules
- Update examples
```

**Deliverable:** Updated rules + changelog

---

### Task 9: Deprecate Unused Rules

**Mục tiêu:** Remove rules không được sử dụng

**Người thực hiện:** Tech Lead

**Thời gian:** 1-2 giờ

**Các bước thực hiện:**

#### Bước 1: Identify Unused Rules
```
Criteria for deprecation:
- Compliance rate < 20%
- No violations in 3 months
- Team feedback: "Not useful"
- Replaced by better rule
```

#### Bước 2: Announce Deprecation
```markdown
# Rule Deprecation Notice

## Rules to be Deprecated
- [Rule name]: [Reason]

## Timeline
- Announcement: [Date]
- Deprecation: [Date + 1 month]
- Removal: [Date + 3 months]

## Migration Guide
- [How to adapt]
```

#### Bước 3: Update Documentation
```
- Mark as deprecated in skill file
- Update MASTER_ROUTER.md
- Update QUICK_REFERENCE.md
- Remove from PR template
```

#### Bước 4: Remove After Grace Period
```
After 3 months:
- Archive skill file
- Remove from KIRO.md
- Update all references
```

**Deliverable:** Cleaned up rules system

---

### Task 10: Expand to New Categories

**Mục tiêu:** Add new skills based on team needs

**Người thực hiện:** Tech Lead + Senior Developers

**Thời gian:** Variable (per new skill)

**Các bước thực hiện:**

#### Bước 1: Identify Gaps
```
Sources:
- Team feedback
- Production incidents
- Code review patterns
- Industry trends
```

#### Bước 2: Prioritize New Skills
```
Criteria:
- Impact: High/Medium/Low
- Effort: High/Medium/Low
- Urgency: High/Medium/Low

Priority = Impact * Urgency / Effort
```

#### Bước 3: Create New Skill
```
Follow format:
1. Overview
2. Rules (with examples)
3. AI Leverage
4. Quick Reference
5. Related Skills
```

#### Bước 4: Integrate
```
- Add to MASTER_ROUTER.md
- Add to KIRO.md (if core rule)
- Update QUICK_REFERENCE.md
- Train team
```

**Deliverable:** New skills as needed

---

## 📊 SUCCESS METRICS

Track these metrics to measure success:

### Week 4 (After Setup)
- [ ] Pre-commit hooks: 50%+ adoption
- [ ] CI pipeline: 90%+ success rate
- [ ] Team trained: 100%

### Month 2 (After Training)
- [ ] Rule compliance: 70%+
- [ ] Bugs in review: ↓ 30%
- [ ] Security issues: ↓ 50%

### Quarter 2 (After Optimization)
- [ ] Rule compliance: 90%+
- [ ] Bugs in review: ↓ 50%
- [ ] Security issues: ↓ 80%
- [ ] ROI: 200%+

---

## 🎯 QUICK START CHECKLIST

```
Week 15:
□ Setup pre-commit hooks in sample project
□ Test and document issues

Week 16:
□ Setup CI/CD pipeline in test project
□ Verify all jobs pass

Week 17-20 (Month 2):
□ Training Session 1: Foundation
□ Training Session 2: Security
□ Training Session 3: Advanced
□ Training Session 4: Standards

Week 21-24:
□ Integrate code review checklist
□ Setup metrics dashboard
□ Track adoption weekly

Quarter 2:
□ Measure ROI
□ Quarterly review
□ Deprecate unused rules
□ Add new skills as needed
```

---

## 📞 SUPPORT

### Questions?
- Check individual guides (PRE_COMMIT_SETUP_GUIDE.md, etc.)
- Review QUICK_REFERENCE.md
- Ask in team channel

### Issues?
- Document in [PROJECT]_ISSUES.md
- Discuss in weekly sync
- Escalate to Tech Lead

---

**Version:** 1.0.0  
**Created:** 2026-03-30  
**Status:** Ready to Execute

**Next Action:** Start with Week 15 tasks
