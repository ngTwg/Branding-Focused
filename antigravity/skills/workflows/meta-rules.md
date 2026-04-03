---
name: "META-RULES - QUY TẮC VỀ QUY TẮC"
tags: ["antigravity", "c:", "checklist", "conflict", "frontend", "gemini", "hierarchy", "<YOUR_USERNAME>", "meta", "order", "overview", "pattern", "priority", "quy", "resolution", "rule", "rules", "tắc", "users", "workflows"]
tier: 2
risk: "medium"
estimated_tokens: 3487
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# META-RULES - QUY TẮC VỀ QUY TẮC

> **Tier:** 3-4  
> **Tags:** `[meta, governance, rules, standards, evolution]`  
> **Khi nào dùng:** Khi thiết lập hoặc cập nhật coding standards, khi rules conflict, khi đánh giá effectiveness

---

## 📋 OVERVIEW

**Meta-rules** là quy tắc về cách tạo, áp dụng, và duy trì các quy tắc khác.

**Tại sao cần meta-rules:**
- Rules conflict → Cần hierarchy để resolve
- Rules outdated → Cần decay protocol
- Too many rules → Cần prioritization
- Rules ignored → Cần adoption strategy
- Cannot measure → Cần effectiveness metrics

---

## 🎯 META-RULES CHECKLIST

```markdown
[ ] Rule hierarchy defined (Security > Data > Business)
[ ] Conflict resolution protocol
[ ] Rule decay review schedule (quarterly)
[ ] Rule adoption metrics tracked
[ ] Rule effectiveness measured
[ ] Exception process documented
[ ] Rule creation guidelines
[ ] Rule deprecation process
[ ] Team buy-in achieved
[ ] Documentation up-to-date
```

---

## 🏆 PATTERN 1: RULE HIERARCHY

### Priority Order

```
1. SECURITY RULES (Highest Priority)
   - Never log passwords
   - Always validate input
   - Use HTTPS only
   - Scan for secrets
   
2. DATA INTEGRITY RULES
   - Foreign key constraints
   - Transactions for multi-step operations
   - Backup before destructive operations
   
3. BUSINESS LOGIC RULES
   - Validate business constraints
   - Audit trail for critical operations
   
4. CODE QUALITY RULES
   - Naming conventions
   - Function length limits
   - Test coverage
   
5. STYLE RULES (Lowest Priority)
   - Formatting
   - Comment style
```

### Conflict Resolution

```typescript
// Example: Security vs Performance conflict

// ❌ BAD: Performance over security
app.get('/api/users', (req, res) => {
  // Fast but insecure (no auth check)
  const users = await db.users.findAll();
  res.json(users);
});

// ✅ GOOD: Security wins
app.get('/api/users', authenticate, authorize('admin'), async (req, res) => {
  // Slower but secure
  const users = await db.users.findAll();
  res.json(users);
});

// Example: Data integrity vs Code simplicity

// ❌ BAD: Simple but no transaction
async function transferMoney(fromId, toId, amount) {
  await db.accounts.decrement({ id: fromId }, { balance: amount });
  await db.accounts.increment({ id: toId }, { balance: amount });
  // ⚠️ If second operation fails, money lost!
}

// ✅ GOOD: Data integrity wins
async function transferMoney(fromId, toId, amount) {
  const transaction = await db.sequelize.transaction();
  try {
    await db.accounts.decrement({ id: fromId }, { balance: amount }, { transaction });
    await db.accounts.increment({ id: toId }, { balance: amount }, { transaction });
    await transaction.commit();
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
}
```

---

## 🔄 PATTERN 2: RULE DECAY PROTOCOL

### Quarterly Review Process

```markdown
## Rule Review Schedule

### Q1 (January - March)
- [ ] Review all security rules
- [ ] Update for new vulnerabilities
- [ ] Check compliance with latest OWASP

### Q2 (April - June)
- [ ] Review database standards
- [ ] Update for new DB versions
- [ ] Check migration patterns

### Q3 (July - September)
- [ ] Review API standards
- [ ] Update for new HTTP standards
- [ ] Check versioning strategy

### Q4 (October - December)
- [ ] Review all rules
- [ ] Deprecate unused rules
- [ ] Plan next year updates
```

### Rule Decay Detection

```typescript
// Track rule usage
interface RuleMetrics {
  ruleId: string;
  name: string;
  category: string;
  createdAt: Date;
  lastUpdated: Date;
  lastUsed: Date;
  usageCount: number;
  violationCount: number;
  exceptionCount: number;
}

// Detect decayed rules
function detectDecayedRules(rules: RuleMetrics[]): RuleMetrics[] {
  const now = new Date();
  const sixMonthsAgo = new Date(now.getTime() - 180 * 24 * 60 * 60 * 1000);
  
  return rules.filter(rule => {
    // Rule not used in 6 months
    if (rule.lastUsed < sixMonthsAgo) return true;
    
    // Rule has too many exceptions (> 50%)
    if (rule.exceptionCount > rule.usageCount * 0.5) return true;
    
    // Rule rarely violated (< 5% violation rate)
    if (rule.violationCount < rule.usageCount * 0.05) return true;
    
    return false;
  });
}

// Example output
const decayedRules = detectDecayedRules(allRules);
console.log('Rules to review:', decayedRules.map(r => r.name));
// Output: ['No console.log in production', 'Max file size 200 lines', ...]
```

---

## 🎯 PATTERN 3: WHEN TO OVERRIDE RULES

### Valid Override Scenarios

```typescript
// Scenario 1: Performance-critical code
// Rule: "Always use async/await"
// Override: Use callbacks for hot path

// ❌ Normal code: Follow rule
async function processUser(userId: string) {
  const user = await db.users.findOne({ id: userId });
  const posts = await db.posts.findAll({ authorId: userId });
  return { user, posts };
}

// ✅ Hot path: Override allowed
function processUserHotPath(userId: string, callback: Function) {
  // OVERRIDE: Using callbacks for 10x performance
  // Justification: Called 1M times/second
  // Approved by: Tech Lead
  // Date: 2024-03-30
  db.users.findOne({ id: userId }, (err, user) => {
    if (err) return callback(err);
    db.posts.findAll({ authorId: userId }, (err, posts) => {
      if (err) return callback(err);
      callback(null, { user, posts });
    });
  });
}

// Scenario 2: Legacy integration
// Rule: "Use TypeScript"
// Override: Use JavaScript for legacy lib

// ✅ Override documented
// @ts-ignore
// OVERRIDE: Legacy library has no types
// Justification: Third-party lib, no @types available
// Approved by: Tech Lead
// Date: 2024-03-30
const legacyLib = require('old-library');

// Scenario 3: Temporary workaround
// Rule: "No any type"
// Override: Temporary any for migration

// ✅ Override with TODO
// TODO: Remove any after migration to v2 API
// OVERRIDE: Temporary during migration
// Deadline: 2024-06-30
// Approved by: Tech Lead
function migrateData(data: any) {
  // Migration logic
}
```

### Override Documentation Template

```typescript
// OVERRIDE: [Rule Name]
// Justification: [Why override is necessary]
// Alternative considered: [What else was tried]
// Impact: [Performance gain, compatibility, etc.]
// Approved by: [Name]
// Date: [YYYY-MM-DD]
// Review date: [YYYY-MM-DD] (if temporary)
```

---

## 📊 PATTERN 4: RULE ADOPTION STRATEGY

### Gradual Rollout

```markdown
## Phase 1: Pilot (Week 1-2)
- [ ] Introduce rule to 1 team (5 people)
- [ ] Gather feedback
- [ ] Adjust rule based on feedback
- [ ] Measure adoption rate

## Phase 2: Early Adopters (Week 3-4)
- [ ] Introduce to 3 teams (15 people)
- [ ] Create examples and documentation
- [ ] Host Q&A session
- [ ] Measure violation rate

## Phase 3: Company-wide (Week 5-8)
- [ ] Announce to all teams
- [ ] Add to CI/CD pipeline
- [ ] Enforce in code reviews
- [ ] Track compliance

## Phase 4: Enforcement (Week 9+)
- [ ] Block PRs that violate rule
- [ ] Add automated fixes (ESLint --fix)
- [ ] Celebrate teams with 100% compliance
```

### Adoption Metrics

```typescript
interface AdoptionMetrics {
  ruleId: string;
  totalFiles: number;
  compliantFiles: number;
  violationCount: number;
  fixedCount: number;
  adoptionRate: number;  // compliantFiles / totalFiles
  trend: 'improving' | 'stable' | 'declining';
}

function calculateAdoption(rule: string): AdoptionMetrics {
  // Scan codebase
  const files = scanCodebase();
  const violations = checkRule(rule, files);
  
  const compliantFiles = files.length - violations.length;
  const adoptionRate = compliantFiles / files.length;
  
  // Compare with last week
  const lastWeekRate = getHistoricalRate(rule, 7);
  const trend = adoptionRate > lastWeekRate + 0.05 ? 'improving'
    : adoptionRate < lastWeekRate - 0.05 ? 'declining'
    : 'stable';
  
  return {
    ruleId: rule,
    totalFiles: files.length,
    compliantFiles,
    violationCount: violations.length,
    fixedCount: 0,  // Track separately
    adoptionRate,
    trend
  };
}

// Example output
const metrics = calculateAdoption('no-console');
console.log(`Adoption: ${(metrics.adoptionRate * 100).toFixed(1)}%`);
console.log(`Trend: ${metrics.trend}`);
// Output: Adoption: 87.5%, Trend: improving
```

---

## 📈 PATTERN 5: MEASURING EFFECTIVENESS

### Rule Effectiveness Metrics

```typescript
interface RuleEffectiveness {
  ruleId: string;
  name: string;
  
  // Impact metrics
  bugsPreventedEstimate: number;
  timesSavedHours: number;
  incidentsAvoided: number;
  
  // Cost metrics
  adoptionTimeHours: number;
  maintenanceTimeHours: number;
  falsePositiveRate: number;
  
  // ROI
  roi: number;  // (timeSaved - adoptionTime - maintenanceTime) / adoptionTime
  
  // Verdict
  verdict: 'keep' | 'modify' | 'deprecate';
}

function evaluateRule(ruleId: string): RuleEffectiveness {
  // Gather data
  const violations = getViolations(ruleId);
  const incidents = getIncidents();
  const timeSpent = getTimeSpent(ruleId);
  
  // Estimate bugs prevented
  const bugsPreventedEstimate = violations.filter(v => 
    v.severity === 'high' || v.severity === 'critical'
  ).length;
  
  // Estimate time saved (2 hours per bug)
  const timesSavedHours = bugsPreventedEstimate * 2;
  
  // Calculate ROI
  const roi = (timesSavedHours - timeSpent.adoption - timeSpent.maintenance) 
    / timeSpent.adoption;
  
  // Verdict
  let verdict: 'keep' | 'modify' | 'deprecate';
  if (roi > 2) verdict = 'keep';  // 200% ROI
  else if (roi > 0.5) verdict = 'modify';  // 50% ROI
  else verdict = 'deprecate';  // Negative ROI
  
  return {
    ruleId,
    name: getRuleName(ruleId),
    bugsPreventedEstimate,
    timesSavedHours,
    incidentsAvoided: incidents.length,
    adoptionTimeHours: timeSpent.adoption,
    maintenanceTimeHours: timeSpent.maintenance,
    falsePositiveRate: violations.filter(v => v.falsePositive).length / violations.length,
    roi,
    verdict
  };
}

// Example output
const effectiveness = evaluateRule('no-any-type');
console.log(`Rule: ${effectiveness.name}`);
console.log(`ROI: ${(effectiveness.roi * 100).toFixed(0)}%`);
console.log(`Verdict: ${effectiveness.verdict}`);
// Output: Rule: No any type, ROI: 250%, Verdict: keep
```

---

## 🚨 PATTERN 6: RULE CREATION GUIDELINES

### Before Creating New Rule

```markdown
## Rule Proposal Checklist

### 1. Problem Statement
- [ ] What problem does this rule solve?
- [ ] How often does this problem occur?
- [ ] What is the impact? (bugs, security, performance)

### 2. Evidence
- [ ] Show 3+ real examples of the problem
- [ ] Link to incidents caused by this problem
- [ ] Estimate cost of problem (time, money)

### 3. Solution
- [ ] Describe the rule clearly
- [ ] Provide good and bad examples
- [ ] Explain why this is the best solution

### 4. Cost-Benefit Analysis
- [ ] Estimate adoption time
- [ ] Estimate maintenance cost
- [ ] Calculate expected ROI

### 5. Alternatives Considered
- [ ] List other solutions considered
- [ ] Explain why this rule is better

### 6. Pilot Plan
- [ ] Identify pilot team
- [ ] Set success criteria
- [ ] Plan rollout timeline
```

### Rule Template

```markdown
# RULE: [Rule Name]

## Problem
[What problem does this solve?]

## Rule
[Clear, concise rule statement]

## Examples

### ❌ BAD
```code
[Bad example]
```

### ✅ GOOD
```code
[Good example]
```

## Rationale
[Why this rule exists]

## Exceptions
[When can this rule be overridden?]

## Enforcement
- [ ] Manual (code review)
- [ ] Automated (linter)
- [ ] CI/CD (blocking)

## Metrics
- Adoption rate: [Target %]
- Violation rate: [Target %]
- ROI: [Target %]

## Review Schedule
- Next review: [Date]
- Owner: [Name]
```

---

## 📊 QUICK REFERENCE

| Aspect | Standard | Example |
|--------|----------|---------|
| **Hierarchy** | Security > Data > Business > Quality > Style | Security rules always win |
| **Review** | Quarterly | Every 3 months |
| **Override** | Document + Approve | OVERRIDE comment |
| **Adoption** | Gradual rollout | Pilot → Early → All |
| **Effectiveness** | ROI > 100% | Keep if ROI > 200% |
| **Creation** | Evidence-based | 3+ real examples |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Too Many Rules

```markdown
# ❌ BAD: 100+ rules
- No console.log
- No var keyword
- No == operator
- No any type
- No implicit any
- ... (96 more rules)

# ✅ GOOD: 10-20 high-impact rules
- Security: No hardcoded secrets
- Data: Use transactions for multi-step ops
- Quality: Test coverage > 80%
- Style: Use Prettier (auto-format)
```

### ❌ Mistake 2: No Measurement

```typescript
// ❌ BAD: Create rule, never measure
addRule('no-console');
// ... 6 months later, still don't know if it helps

// ✅ GOOD: Track metrics
addRule('no-console');
trackMetrics('no-console', {
  adoptionRate: 0.85,
  violationCount: 42,
  bugsPreventedEstimate: 5
});
```

### ❌ Mistake 3: Never Deprecate

```markdown
# ❌ BAD: Keep all rules forever
- Rule from 2015: "Use jQuery"
- Rule from 2018: "Use class components"
- Rule from 2020: "Use Redux"

# ✅ GOOD: Deprecate outdated rules
- ~~Rule from 2015: "Use jQuery"~~ (Deprecated 2020)
- ~~Rule from 2018: "Use class components"~~ (Deprecated 2021)
- Rule from 2023: "Use React hooks"
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Review our coding standards and:
- Identify rules that conflict
- Suggest hierarchy for conflict resolution
- Find rules not used in 6 months
- Calculate ROI for top 10 rules
- Recommend rules to deprecate"
```

### AI Should

1. ✅ Analyze rule usage patterns
2. ✅ Detect conflicts and suggest hierarchy
3. ✅ Calculate adoption rates
4. ✅ Estimate ROI for each rule
5. ✅ Recommend deprecations
6. ✅ Suggest new rules based on incidents

---

## 🔗 RELATED SKILLS

- All other skills (meta-rules govern all rules)
- `documentation-standards.md` - Document rules
- `refactoring-triggers.md` - When to update rules

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** High  
**Impact:** Critical (governs all other rules)
