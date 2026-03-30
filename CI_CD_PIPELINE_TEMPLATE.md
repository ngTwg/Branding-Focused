# 🚀 CI/CD PIPELINE TEMPLATE

> **Automated quality gates** - Catch issues before production  
> **Version:** 1.0.0  
> **Last Updated:** 2026-03-30

---

## 🎯 OVERVIEW

CI/CD pipeline tự động chạy checks trên mỗi push/PR, đảm bảo code quality trước khi merge.

### Pipeline Stages
1. **Lint** - Code style & quality
2. **Type Check** - Type safety
3. **Test** - Unit & integration tests
4. **Security** - Vulnerability scanning
5. **Build** - Production build
6. **Deploy** - Staging/Production

---

## 📦 GITHUB ACTIONS

### Complete Pipeline (.github/workflows/ci.yml)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '20.x'

jobs:
  lint:
    name: Lint & Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint -- --max-warnings 0
      
      - name: Check formatting
        run: npx prettier --check .

  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: TypeScript check
        run: npx tsc --noEmit

  test:
    name: Test & Coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test -- --coverage --watchAll=false
      
      - name: Check coverage threshold
        run: |
          COVERAGE=$(npx nyc report --reporter=text-summary | grep "Lines" | awk '{print $3}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run npm audit
        run: npm audit --audit-level=high
      
      - name: Secret scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
      
      - name: OWASP Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'project-name'
          path: '.'
          format: 'HTML'
      
      - name: Upload OWASP report
        uses: actions/upload-artifact@v3
        with:
          name: dependency-check-report
          path: reports/

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test, security]
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Check bundle size
        run: |
          SIZE=$(du -sk dist | cut -f1)
          MAX_SIZE=5000  # 5MB
          if [ $SIZE -gt $MAX_SIZE ]; then
            echo "Bundle size ${SIZE}KB exceeds ${MAX_SIZE}KB"
            exit 1
          fi
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  lighthouse:
    name: Lighthouse CI
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      
      - name: Download build
        uses: actions/download-artifact@v3
        with:
          name: build
          path: dist/
      
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            http://localhost:3000
          uploadArtifacts: true
          temporaryPublicStorage: true

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, lighthouse]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4
      
      - name: Download build
        uses: actions/download-artifact@v3
        with:
          name: build
          path: dist/
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, lighthouse]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4
      
      - name: Download build
        uses: actions/download-artifact@v3
        with:
          name: build
          path: dist/
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./
```

---

## 🐍 PYTHON PROJECTS

### GitHub Actions for Python (.github/workflows/python-ci.yml)

```yaml
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: '3.11'

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install ruff black mypy
          pip install -r requirements.txt
      
      - name: Run Ruff
        run: ruff check .
      
      - name: Check Black formatting
        run: black --check .
      
      - name: Type check with mypy
        run: mypy .

  test:
    name: Test & Coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install pytest pytest-cov
          pip install -r requirements.txt
      
      - name: Run tests
        run: pytest --cov=. --cov-report=xml --cov-report=term-missing
      
      - name: Check coverage
        run: |
          COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: pip install safety bandit
      
      - name: Check dependencies
        run: safety check
      
      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json
      
      - name: Upload Bandit report
        uses: actions/upload-artifact@v3
        with:
          name: bandit-report
          path: bandit-report.json
```

---

## 🔧 GITLAB CI

### .gitlab-ci.yml

```yaml
stages:
  - lint
  - test
  - security
  - build
  - deploy

variables:
  NODE_VERSION: "20"

lint:
  stage: lint
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run lint -- --max-warnings 0
    - npx prettier --check .
  cache:
    paths:
      - node_modules/

typecheck:
  stage: lint
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npx tsc --noEmit
  cache:
    paths:
      - node_modules/

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test -- --coverage --watchAll=false
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  cache:
    paths:
      - node_modules/

security:
  stage: security
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm audit --audit-level=high
  allow_failure: true

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
  cache:
    paths:
      - node_modules/

deploy:staging:
  stage: deploy
  image: node:${NODE_VERSION}
  script:
    - npm run deploy:staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy:production:
  stage: deploy
  image: node:${NODE_VERSION}
  script:
    - npm run deploy:production
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

---

## 📊 QUALITY GATES

### Required Checks

```yaml
# .github/branch-protection.yml
branches:
  - name: main
    protection:
      required_status_checks:
        strict: true
        contexts:
          - "Lint & Format Check"
          - "Type Check"
          - "Test & Coverage"
          - "Security Scan"
          - "Build"
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
      enforce_admins: true
      restrictions: null
```

---

## 🎯 CUSTOM CHECKS

### PR Size Check

```yaml
# .github/workflows/pr-size.yml
name: PR Size Check

on: pull_request

jobs:
  size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Check PR size
        run: |
          LINES=$(git diff --stat origin/${{ github.base_ref }}...HEAD | tail -1 | awk '{print $4}')
          if [ $LINES -gt 400 ]; then
            echo "::warning::PR has $LINES lines changed (>400). Consider splitting."
          fi
```

### Documentation Check

```yaml
# .github/workflows/docs-check.yml
name: Documentation Check

on: pull_request

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Check PROJECT_MAP updated
        run: |
          if git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -E '\.(ts|tsx|js|jsx)$'; then
            if ! git diff --name-only origin/${{ github.base_ref }}...HEAD | grep 'PROJECT_MAP.md'; then
              echo "::error::Code changed but PROJECT_MAP.md not updated"
              exit 1
            fi
          fi
```

---

## 🚨 NOTIFICATIONS

### Slack Integration

```yaml
# Add to any job
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "❌ CI Failed: ${{ github.workflow }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Workflow:* ${{ github.workflow }}\n*Status:* Failed\n*Branch:* ${{ github.ref }}\n*Author:* ${{ github.actor }}"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 📈 METRICS & MONITORING

### Track CI Performance

```yaml
# .github/workflows/metrics.yml
name: CI Metrics

on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Record metrics
        run: |
          echo "Duration: ${{ github.event.workflow_run.duration }}"
          echo "Status: ${{ github.event.workflow_run.conclusion }}"
          # Send to monitoring service
```

---

## ✅ SETUP CHECKLIST

```
□ Create .github/workflows/ci.yml
□ Add secrets to GitHub (CODECOV_TOKEN, VERCEL_TOKEN, etc.)
□ Configure branch protection rules
□ Setup Codecov integration
□ Configure Slack notifications
□ Test pipeline on feature branch
□ Document custom checks
□ Train team on CI/CD process
```

---

## 🎓 BEST PRACTICES

1. **Fail Fast** - Run quick checks (lint, typecheck) first
2. **Parallel Jobs** - Run independent jobs in parallel
3. **Cache Dependencies** - Cache node_modules, pip packages
4. **Artifacts** - Upload build artifacts for debugging
5. **Manual Gates** - Require manual approval for production
6. **Notifications** - Alert team on failures
7. **Metrics** - Track CI performance over time

---

**Version:** 1.0.0  
**Status:** Production-Ready  
**Next:** Setup monitoring dashboard

---

**Quick Links:**
- GitHub Actions: https://docs.github.com/actions
- GitLab CI: https://docs.gitlab.com/ee/ci/
- Codecov: https://codecov.io/
- Lighthouse CI: https://github.com/GoogleChrome/lighthouse-ci
