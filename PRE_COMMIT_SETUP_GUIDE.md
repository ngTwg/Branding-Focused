# 🔧 PRE-COMMIT HOOKS SETUP GUIDE

> **Automated enforcement** - Catch issues before they reach Git  
> **Version:** 1.0.0  
> **Last Updated:** 2026-03-30

---

## 🎯 OVERVIEW

Pre-commit hooks tự động chạy checks trước mỗi lần commit, đảm bảo code quality và security.

### What Gets Checked
- ✅ Code formatting (Prettier/Black)
- ✅ Linting (ESLint/Ruff)
- ✅ Type checking (TypeScript/mypy)
- ✅ Secret scanning (secretlint)
- ✅ Tests (affected files only)
- ✅ Naming conventions
- ✅ File size limits

---

## 📦 INSTALLATION

### JavaScript/TypeScript Projects

#### Step 1: Install Dependencies
```bash
npm install --save-dev husky lint-staged
npm install --save-dev @secretlint/secretlint-rule-preset-recommend
npm install --save-dev @secretlint/quick-start
```

#### Step 2: Initialize Husky
```bash
npx husky install
npm pkg set scripts.prepare="husky install"
```

#### Step 3: Create Pre-commit Hook
```bash
npx husky add .husky/pre-commit "npx lint-staged"
```

#### Step 4: Configure lint-staged
Add to `package.json`:
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

#### Step 5: Configure secretlint
Create `.secretlintrc.json`:
```json
{
  "rules": [
    {
      "id": "@secretlint/secretlint-rule-preset-recommend"
    }
  ]
}
```

---

### Python Projects

#### Step 1: Install Dependencies
```bash
pip install pre-commit
```

#### Step 2: Create Configuration
Create `.pre-commit-config.yaml`:
```yaml
repos:
  # Formatting
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  # Linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  # Secret scanning
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # General checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
```

#### Step 3: Install Hooks
```bash
pre-commit install
```

#### Step 4: Initialize Secrets Baseline
```bash
detect-secrets scan > .secrets.baseline
```

---

## 🔍 WHAT EACH HOOK DOES

### 1. Prettier/Black (Formatting)
**Purpose:** Enforce consistent code style  
**When it runs:** On every commit  
**What it checks:**
- Indentation (2 spaces for JS, 4 for Python)
- Line length (80-100 chars)
- Semicolons, quotes, trailing commas
- Blank lines, spacing

**Example:**
```javascript
// Before
const user={name:"John",age:30}

// After (auto-fixed)
const user = {
  name: "John",
  age: 30,
};
```

---

### 2. ESLint/Ruff (Linting)
**Purpose:** Catch code quality issues  
**When it runs:** On every commit  
**What it checks:**
- Unused variables
- Missing error handling
- Complexity too high
- Naming conventions
- Best practices violations

**Example:**
```javascript
// ❌ Will be caught
const unusedVar = 123;  // Unused variable
if (x = 5) {}          // Assignment in condition

// ✅ Auto-fixed or flagged
const USED_VAR = 123;
if (x === 5) {}
```

---

### 3. TypeScript/mypy (Type Checking)
**Purpose:** Catch type errors  
**When it runs:** On every commit  
**What it checks:**
- Type mismatches
- Missing type annotations
- Null/undefined issues
- Return type errors

**Example:**
```typescript
// ❌ Will be caught
function add(a, b) {  // Missing types
  return a + b;
}

// ✅ Correct
function add(a: number, b: number): number {
  return a + b;
}
```

---

### 4. Secretlint/detect-secrets (Secret Scanning)
**Purpose:** Prevent committing secrets  
**When it runs:** On every commit  
**What it checks:**
- API keys (AWS, OpenAI, etc.)
- Passwords
- Private keys
- Tokens
- Database URLs with credentials

**Example:**
```javascript
// ❌ Will be BLOCKED
const API_KEY = "sk-1234567890abcdef";
const DB_URL = "postgres://user:pass@localhost/db";

// ✅ Allowed
const API_KEY = process.env.API_KEY;
const DB_URL = process.env.DATABASE_URL;
```

---

### 5. Tests (Affected Files)
**Purpose:** Ensure tests pass  
**When it runs:** On every commit  
**What it checks:**
- Unit tests for changed files
- Integration tests if needed
- Coverage threshold (80%+)

**Configuration (package.json):**
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "jest --bail --findRelatedTests --passWithNoTests"
    ]
  }
}
```

---

## ⚙️ ADVANCED CONFIGURATION

### Skip Hooks (Emergency Only)
```bash
# Skip all hooks (NOT RECOMMENDED)
git commit --no-verify -m "Emergency fix"

# Better: Fix the issues instead
```

### Run Hooks Manually
```bash
# JavaScript
npx lint-staged

# Python
pre-commit run --all-files
```

### Update Hooks
```bash
# Python
pre-commit autoupdate
```

---

## 🚨 COMMON ISSUES & SOLUTIONS

### Issue 1: Hook fails with "command not found"
**Cause:** Dependencies not installed  
**Solution:**
```bash
# JavaScript
npm install

# Python
pip install -r requirements.txt
pre-commit install
```

---

### Issue 2: Secretlint false positive
**Cause:** Legitimate string looks like secret  
**Solution:**
Add to `.secretlintrc.json`:
```json
{
  "rules": [
    {
      "id": "@secretlint/secretlint-rule-preset-recommend",
      "allowMessagePatterns": ["/example-key-12345/"]
    }
  ]
}
```

---

### Issue 3: Tests take too long
**Cause:** Running all tests on every commit  
**Solution:**
Only run tests for changed files:
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "jest --bail --findRelatedTests --passWithNoTests"
    ]
  }
}
```

---

### Issue 4: Prettier conflicts with ESLint
**Cause:** Conflicting rules  
**Solution:**
Install compatibility plugin:
```bash
npm install --save-dev eslint-config-prettier
```

Add to `.eslintrc.json`:
```json
{
  "extends": ["eslint:recommended", "prettier"]
}
```

---

## 📊 MONITORING HOOK EFFECTIVENESS

Track these metrics:

```
Week 1 (Before hooks):
- Commits with issues: 45%
- Code review rejections: 30%
- Production bugs: 12

Week 4 (After hooks):
- Commits with issues: 5% ↓ 89%
- Code review rejections: 8% ↓ 73%
- Production bugs: 3 ↓ 75%
```

---

## 🎯 TEAM ADOPTION STRATEGY

### Phase 1: Soft Launch (Week 1-2)
- Install hooks on dev machines
- Run in warning mode (don't block commits)
- Collect feedback

### Phase 2: Enforcement (Week 3-4)
- Enable blocking mode
- Train team on fixing common issues
- Document exceptions

### Phase 3: Optimization (Week 5+)
- Fine-tune rules based on feedback
- Add custom checks
- Measure effectiveness

---

## 🔧 CUSTOM HOOKS

### Example: Check File Size
Create `.husky/pre-commit`:
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run lint-staged
npx lint-staged

# Check file sizes
MAX_SIZE=500000  # 500KB
for file in $(git diff --cached --name-only); do
  if [ -f "$file" ]; then
    size=$(wc -c < "$file")
    if [ $size -gt $MAX_SIZE ]; then
      echo "Error: $file is too large ($size bytes > $MAX_SIZE bytes)"
      exit 1
    fi
  fi
done
```

---

### Example: Check Naming Conventions
Add to `lint-staged` config:
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "node scripts/check-naming.js",
      "eslint --fix"
    ]
  }
}
```

Create `scripts/check-naming.js`:
```javascript
const fs = require('fs');
const path = require('path');

const files = process.argv.slice(2);

files.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Check for bad naming patterns
  const badPatterns = [
    /const [A-Z][a-z]+\s*=/,  // PascalCase for variables
    /function [a-z]+_[a-z]+/,  // snake_case for functions
  ];
  
  badPatterns.forEach(pattern => {
    if (pattern.test(content)) {
      console.error(`❌ Bad naming in ${file}`);
      process.exit(1);
    }
  });
});

console.log('✅ Naming conventions OK');
```

---

## 📚 INTEGRATION WITH CI/CD

Pre-commit hooks are the first line of defense. CI/CD is the second.

### GitHub Actions Example
`.github/workflows/ci.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run lint
      
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test -- --coverage
      
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm audit --audit-level=high
      - uses: trufflesecurity/trufflehog@main
```

---

## ✅ VERIFICATION CHECKLIST

After setup, verify everything works:

```bash
# 1. Make a test change
echo "const test = 123;" >> test.js

# 2. Try to commit
git add test.js
git commit -m "Test commit"

# Expected: Hooks should run and format/lint the file

# 3. Try to commit a secret
echo "const API_KEY = 'sk-1234567890';" >> test.js
git add test.js
git commit -m "Test secret"

# Expected: Should be BLOCKED by secretlint

# 4. Clean up
git reset HEAD test.js
rm test.js
```

---

## 🎓 TRAINING MATERIALS

### For Developers
1. **Video:** "Pre-commit Hooks in 5 Minutes"
2. **Cheat Sheet:** Common fixes for hook failures
3. **FAQ:** Troubleshooting guide

### For Team Leads
1. **Metrics Dashboard:** Track adoption and effectiveness
2. **ROI Calculator:** Measure time saved
3. **Customization Guide:** Add team-specific checks

---

## 📞 SUPPORT

### Hook fails?
1. Read error message carefully
2. Run hook manually: `npx lint-staged`
3. Check `.husky/pre-commit` file
4. Verify dependencies installed

### Need custom check?
1. Review examples above
2. Test in isolation first
3. Add to `.husky/pre-commit`
4. Document in team wiki

---

## 🎉 SUCCESS CRITERIA

Pre-commit hooks are working when:

- ✅ 95%+ commits pass hooks on first try
- ✅ Code review time reduced by 40%+
- ✅ Zero secrets committed to Git
- ✅ Consistent code style across team
- ✅ Fewer bugs in production

---

**Version:** 1.0.0  
**Status:** Production-Ready  
**Next:** Setup CI/CD pipeline (see CI_CD_SETUP_GUIDE.md)

---

**Quick Links:**
- Husky docs: https://typicode.github.io/husky/
- lint-staged: https://github.com/okonet/lint-staged
- pre-commit: https://pre-commit.com/
- secretlint: https://github.com/secretlint/secretlint
