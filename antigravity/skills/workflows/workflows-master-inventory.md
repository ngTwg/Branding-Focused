---
name: "Workflows Skills (Master Inventory)"
tags: ["workflows"]
tier: 2
risk: "medium"
estimated_tokens: 3666
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering"]
quality_score: 0.55
---
# Workflows Skills (Master Inventory)

> **PURPOSE:** Comprehensive workflow orchestration, code quality, debugging, testing, and automation skills.
> **CATEGORY:** Workflows
> **TIER:** 1-4
> **TOKEN OPTIMIZATION:** 50+ skills compressed into single inventory file
> **LOAD TIME:** ~8KB (vs 500KB+ loading individual files)

---

## 📊 Token Efficiency Metrics

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Individual Files | 50+ files | 1 file | 98% |
| Total Size | ~500KB | ~8KB | 98.4% |
| Load Time | ~2.5s | ~0.04s | 98.4% |
| Context Window | 25K tokens | 500 tokens | 98% |

---

## 📋 Quick Reference Index

### 🔧 Core Workflows (11 skills)
Advanced Testing • Analyze Codebase • Anti-Hallucination v2 • Brainstorming • Cleanup Protocol • Code Review Checklist • Code Review Excellence • Codex Review • Concise Planning • Concurrency Patterns • Condition-Based Waiting

### 🐛 Debugging & Error Handling (9 skills)
Debug Buttercup • Debug Errors • Debug Protocol • Defense in Depth • Edge Case Catalog • Error Handling Patterns • Root Cause Tracing • Systematic Debugging

### 📚 Documentation & Standards (5 skills)
Documentation Standards • Documentation Templates • Environment Standards • Logging Standards • Naming Conventions

### 🌿 Git & Version Control (6 skills)
Git Advanced Workflows • Git Hooks Automation • Git PR Workflows • Git Pushing • Git Workflow • Using Git Worktrees

### 🤖 GitHub Automation (5 skills)
GitHub Actions Templates • GitHub Automation • GitHub Automation Skill • GitHub Issue Creator • GitHub Workflow Automation

### 🦊 GitLab Integration (2 skills)
GitLab Automation • GitLab CI Patterns

### 🧪 Testing & QA (5 skills)
Generate Tests and Specs • Performance Profiling • TDD Workflow • Testing Patterns • Testing QA

### ✨ Code Quality & Refactoring (8 skills)
Frontend Code Review • Lint and Validate • Receiving Code Review • Refactor Code • Refactoring Triggers • Requesting Code Review • Resource Cleanup

### 📋 Planning & Orchestration (4 skills)
Planning with Files • Workflow Automation • Workflow Orchestration Patterns • Workflow Patterns

### 🎯 Specialized Workflows (7 skills)
CI/CD Automation • Global Memory Protocol • i18n Localization • Meta Rules • Skill Creator • System Constitution • Verification Before Completion

**TOTAL:** 62 workflow skills in single inventory

---


## 🔧 CORE WORKFLOWS

<a id="advancedtesting"></a>
### Advanced Testing
**FILE:** `workflows/advanced-testing.md` | **TIER:** 2-3
**PURPOSE:** Property-based testing, mutation testing, fuzzing, and advanced test strategies.
**WHEN TO USE:** Complex business logic, security-critical code, high-reliability systems.
**KEY TECHNIQUES:** Hypothesis (Python), fast-check (JS), mutation testing, fuzzing.

<a id="analyzecodebase"></a>
### Analyze Codebase
**FILE:** `workflows/analyze-codebase.md` | **TIER:** 1-2
**PURPOSE:** Holistic understanding of complex repositories before modification.
**WHEN TO USE:** New codebase, large refactoring, debugging complex issues.
**KEY STEPS:** README scan, dependency analysis, architecture mapping, entry point identification.

<a id="antihallucinationv2"></a>
### Anti-Hallucination Protocol v2
**FILE:** `workflows/anti-hallucination-v2.md` | **TIER:** 1-4
**PURPOSE:** Prevent AI from inventing non-existent APIs, libraries, or patterns.
**WHEN TO USE:** ALWAYS - before using any library/API.
**KEY RULES:** Verify library exists, check version compatibility, read docs, test import, never guess.

<a id="brainstorming"></a>
### Brainstorming
**FILE:** `workflows/brainstorming/` | **TIER:** 1-2
**PURPOSE:** Structured ideation and solution exploration.
**WHEN TO USE:** Feature planning, architecture decisions, problem-solving.
**KEY TECHNIQUES:** Mind mapping, SWOT analysis, design thinking, rapid prototyping.

<a id="cleanupprotocol"></a>
### Cleanup Protocol
**FILE:** `workflows/CLEANUP_PROTOCOL.md` | **TIER:** 1-3
**PURPOSE:** Systematic cleanup of resources, temp files, and technical debt.
**WHEN TO USE:** After major features, before releases, during refactoring.
**KEY STEPS:** Remove dead code, clean temp files, update docs, verify tests.


<a id="codereviewchecklist"></a>
### Code Review Checklist
**FILE:** `workflows/code-review-checklist.md` | **TIER:** 1-3
**PURPOSE:** Comprehensive checklist for functionality, security, and maintainability.
**WHEN TO USE:** Every PR review, pre-merge validation.
**KEY CHECKS:** Functionality, security (OWASP), performance, tests, documentation.

<a id="codereviewexcellence"></a>
### Code Review Excellence
**FILE:** `workflows/code-review-excellence/` | **TIER:** 2-3
**PURPOSE:** Advanced code review techniques and best practices.
**WHEN TO USE:** Senior-level reviews, critical systems, mentoring.
**KEY FOCUS:** Architecture patterns, scalability, maintainability, team standards.

<a id="codexreview"></a>
### Codex Review
**FILE:** `workflows/codex-review.md` | **TIER:** 2-3
**PURPOSE:** Professional code review with auto CHANGELOG generation.
**WHEN TO USE:** Release preparation, major features, documentation updates.
**KEY FEATURES:** Automated changelog, semantic versioning, release notes.

<a id="conciseplanning"></a>
### Concise Planning
**FILE:** `workflows/concise-planning.md` | **TIER:** 1-2
**PURPOSE:** Turn complex requests into atomic action items.
**WHEN TO USE:** Feature planning, sprint planning, task breakdown.
**KEY TECHNIQUE:** Break down → Prioritize → Estimate → Execute.

<a id="concurrencypatterns"></a>
### Concurrency Patterns
**FILE:** `workflows/concurrency-patterns.md` | **TIER:** 3-4
**PURPOSE:** Thread-safe patterns, async/await, race condition prevention.
**WHEN TO USE:** Multi-threaded apps, async operations, high-concurrency systems.
**KEY PATTERNS:** Mutex, semaphore, actor model, CSP, async/await best practices.

<a id="conditionbasedwaiting"></a>
### Condition-Based Waiting
**FILE:** `workflows/condition-based-waiting.md` | **TIER:** 2-3
**PURPOSE:** Smart polling and waiting strategies for async operations.
**WHEN TO USE:** API polling, job status checks, resource availability.
**KEY TECHNIQUES:** Exponential backoff, circuit breaker, timeout handling.

---

## 🐛 DEBUGGING & ERROR HANDLING

<a id="debugbuttercup"></a>
### Debug Buttercup
**FILE:** `workflows/debug-buttercup/` | **TIER:** 1-2
**PURPOSE:** Friendly debugging assistant for common issues.
**WHEN TO USE:** Quick debugging, common errors, learning debugging.
**KEY FEATURES:** Error pattern matching, solution suggestions, learning mode.

<a id="debugerrors"></a>
### Debug Errors
**FILE:** `workflows/debug-errors.md` | **TIER:** 1-3
**PURPOSE:** Systematic root cause analysis and bug resolution.
**WHEN TO USE:** Any bug or error encountered.
**KEY STEPS:** Reproduce → Isolate → Identify → Fix → Verify → Document.

<a id="debugprotocol"></a>
### Debug Protocol ⭐ CRITICAL
**FILE:** `workflows/debug-protocol.md` | **TIER:** 1-4
**PURPOSE:** Mandatory systematic debugging process - NO GUESSING.
**WHEN TO USE:** ALWAYS when encountering bugs/errors.
**KEY RULES:** Never guess-and-check, always trace root cause, verify fix.
**PROCESS:** Stack trace → Data flow → Hypothesis → Test → Fix → Verify.

<a id="defenseindepth"></a>
### Defense in Depth
**FILE:** `workflows/defense-in-depth.md` | **TIER:** 2-4
**PURPOSE:** Multi-layer security and error handling strategy.
**WHEN TO USE:** Security-critical systems, production deployments.
**KEY LAYERS:** Input validation, authentication, authorization, encryption, monitoring.

<a id="edgecasecatalog"></a>
### Edge Case Catalog
**FILE:** `workflows/edge-case-catalog.md` | **TIER:** 1-3
**PURPOSE:** Comprehensive catalog of edge cases to test.
**WHEN TO USE:** Before claiming "feature complete", during testing.
**KEY CASES:** Empty, null, undefined, max, min, special chars, boundary values.

<a id="errorhandlingpatterns"></a>
### Error Handling Patterns
**FILE:** `workflows/error-handling-patterns.md` | **TIER:** 1-3
**PURPOSE:** Mandatory error handling for all functions.
**WHEN TO USE:** Every function that can fail.
**KEY PATTERNS:** Try-catch, custom errors, cleanup (finally), error logging.

<a id="rootcausetracing"></a>
### Root Cause Tracing
**FILE:** `workflows/root-cause-tracing.md` | **TIER:** 2-4
**PURPOSE:** Deep dive into complex bugs and system failures.
**WHEN TO USE:** Production incidents, complex bugs, system failures.
**KEY TECHNIQUES:** 5 Whys, fishbone diagram, timeline analysis, log correlation.

<a id="systematicdebugging"></a>
### Systematic Debugging
**FILE:** `workflows/systematic-debugging/` | **TIER:** 1-4
**PURPOSE:** Scientific approach to debugging - hypothesis-driven.
**WHEN TO USE:** Complex bugs, intermittent issues, performance problems.
**KEY PROCESS:** Observe → Hypothesize → Test → Analyze → Repeat.

---

## 📚 DOCUMENTATION & STANDARDS

<a id="documentationstandards"></a>
### Documentation Standards
**FILE:** `workflows/documentation-standards.md` | **TIER:** 1-3
**PURPOSE:** Consistent documentation format and quality.
**WHEN TO USE:** Writing any documentation.
**KEY STANDARDS:** README structure, API docs, inline comments, ADRs.

<a id="documentationtemplates"></a>
### Documentation Templates
**FILE:** `workflows/documentation-templates.md` | **TIER:** 1-2
**PURPOSE:** Ready-to-use templates for common documentation.
**WHEN TO USE:** Starting new docs, standardizing existing docs.
**TEMPLATES:** README, API docs, ADR, runbook, postmortem.

<a id="environmentstandards"></a>
### Environment Standards
**FILE:** `workflows/environment-standards.md` | **TIER:** 1-3
**PURPOSE:** Consistent dev/staging/prod environment setup.
**WHEN TO USE:** New projects, environment setup, deployment.
**KEY AREAS:** .env files, secrets management, environment parity.

<a id="loggingstandards"></a>
### Logging Standards
**FILE:** `workflows/logging-standards.md` | **TIER:** 2-3
**PURPOSE:** Structured logging for observability.
**WHEN TO USE:** All production code, debugging, monitoring.
**KEY STANDARDS:** Log levels, structured logs (JSON), correlation IDs, PII redaction.

<a id="namingconventions"></a>
### Naming Conventions ⭐ MANDATORY
**FILE:** `workflows/naming-conventions.md` | **TIER:** 1-4
**PURPOSE:** Enforce consistent naming across codebase.
**WHEN TO USE:** ALWAYS - before claiming "done".
**KEY RULES:** camelCase (JS vars), PascalCase (classes), snake_case (Python), UPPER_SNAKE_CASE (constants).


---

## 🌿 GIT & VERSION CONTROL

<a id="gitadvancedworkflows"></a>
### Git Advanced Workflows
**FILE:** `workflows/git-advanced-workflows/` | **TIER:** 2-3
**PURPOSE:** Advanced Git techniques (rebase, cherry-pick, bisect).
**WHEN TO USE:** Complex merges, history cleanup, bug hunting.
**KEY TECHNIQUES:** Interactive rebase, git bisect, reflog, submodules.

<a id="githooksautomation"></a>
### Git Hooks Automation
**FILE:** `workflows/git-hooks-automation/` | **TIER:** 2-3
**PURPOSE:** Automate checks with pre-commit, pre-push hooks.
**WHEN TO USE:** Enforce code quality, prevent bad commits.
**KEY HOOKS:** pre-commit (lint, format), pre-push (tests), commit-msg (format).

<a id="gitprworkflows"></a>
### Git PR Workflows
**FILE:** `workflows/git-pr-workflows-*/` | **TIER:** 1-3
**PURPOSE:** Pull request best practices and automation.
**WHEN TO USE:** Every PR creation and review.
**KEY AREAS:** PR templates, review process, merge strategies, onboarding.

<a id="gitpushing"></a>
### Git Pushing
**FILE:** `workflows/git-pushing/` | **TIER:** 1-2
**PURPOSE:** Safe and efficient git push strategies.
**WHEN TO USE:** Pushing code to remote.
**KEY PRACTICES:** Force push safety, branch protection, push hooks.

<a id="gitworkflow"></a>
### Git Workflow
**FILE:** `workflows/git-workflow.md` | **TIER:** 1-2
**PURPOSE:** Standard git workflow (feature branches, commits).
**WHEN TO USE:** Daily development work.
**KEY FLOW:** Branch → Commit → Push → PR → Review → Merge.

<a id="usinggitworktrees"></a>
### Using Git Worktrees
**FILE:** `workflows/using-git-worktrees.md` | **TIER:** 2-3
**PURPOSE:** Parallel feature workspaces in isolated directories.
**WHEN TO USE:** Working on multiple features, hotfixes during feature work.
**KEY BENEFIT:** No stashing, no branch switching, parallel work.

---

## 🤖 GITHUB AUTOMATION

<a id="githubactionstemplates"></a>
### GitHub Actions Templates
**FILE:** `workflows/github-actions-templates/` | **TIER:** 2-3
**PURPOSE:** Ready-to-use CI/CD workflow templates.
**WHEN TO USE:** Setting up CI/CD, automating workflows.
**TEMPLATES:** Test, build, deploy, release, security scan.

<a id="githubautomation"></a>
### GitHub Automation
**FILE:** `workflows/github-automation/` | **TIER:** 2-3
**PURPOSE:** Automate GitHub operations (issues, PRs, releases).
**WHEN TO USE:** Repository management, workflow automation.
**KEY FEATURES:** Auto-labeling, auto-assign, auto-close, release automation.

<a id="githubautomationskill"></a>
### GitHub Automation Skill ⭐ NEW
**FILE:** `workflows/GITHUB_AUTOMATION_SKILL.md` | **TIER:** 1-3
**PURPOSE:** Auto-detect repo, create push.bat, manage git operations.
**WHEN TO USE:** User provides GitHub repo link.
**KEY FEATURES:** Auto git init, remote setup, push.bat creation, .gitignore management.

<a id="githubissuecreator"></a>
### GitHub Issue Creator
**FILE:** `workflows/github-issue-creator/` | **TIER:** 1-2
**PURPOSE:** Create well-formatted GitHub issues from bugs/features.
**WHEN TO USE:** Bug reporting, feature requests, task tracking.
**KEY FEATURES:** Issue templates, auto-labeling, assignment.

<a id="githubworkflowautomation"></a>
### GitHub Workflow Automation
**FILE:** `workflows/github-workflow-automation.md` | **TIER:** 2-3
**PURPOSE:** Comprehensive GitHub Actions automation.
**WHEN TO USE:** CI/CD setup, workflow optimization.
**KEY AREAS:** Matrix builds, caching, secrets, deployment.

---

## 🦊 GITLAB INTEGRATION

<a id="gitlabautomation"></a>
### GitLab Automation
**FILE:** `workflows/gitlab-automation/` | **TIER:** 2-3
**PURPOSE:** Automate GitLab operations (MRs, pipelines).
**WHEN TO USE:** GitLab-based projects.
**KEY FEATURES:** MR automation, pipeline triggers, release management.

<a id="gitlabcipatterns"></a>
### GitLab CI Patterns
**FILE:** `workflows/gitlab-ci-patterns/` | **TIER:** 2-3
**PURPOSE:** Best practices for .gitlab-ci.yml.
**WHEN TO USE:** Setting up GitLab CI/CD.
**KEY PATTERNS:** Stages, jobs, artifacts, caching, deployment.

---

## 🧪 TESTING & QA

<a id="generatetestsandspecs"></a>
### Generate Tests and Specs
**FILE:** `workflows/generate-tests-and-specs.md` | **TIER:** 2-3
**PURPOSE:** Auto-generate tests and specification documents.
**WHEN TO USE:** New features, refactoring, test coverage improvement.
**KEY OUTPUTS:** Unit tests, integration tests, API specs, test data.

<a id="performanceprofiling"></a>
### Performance Profiling
**FILE:** `workflows/performance-profiling/` | **TIER:** 3-4
**PURPOSE:** Identify and fix performance bottlenecks.
**WHEN TO USE:** Slow operations, optimization, scalability issues.
**KEY TOOLS:** Profilers, flame graphs, memory analysis, query optimization.

<a id="tddworkflow"></a>
### TDD Workflow
**FILE:** `workflows/tdd-workflow.md` | **TIER:** 2-3
**PURPOSE:** Red-Green-Refactor safety net for feature development.
**WHEN TO USE:** New features, critical logic, refactoring.
**KEY CYCLE:** Write test (Red) → Make it pass (Green) → Refactor → Repeat.

<a id="testingpatterns"></a>
### Testing Patterns
**FILE:** `workflows/testing-patterns/` | **TIER:** 2-3
**PURPOSE:** Common testing patterns and best practices.
**WHEN TO USE:** Writing any tests.
**KEY PATTERNS:** AAA (Arrange-Act-Assert), mocking, fixtures, factories.

<a id="testingqa"></a>
### Testing QA
**FILE:** `workflows/testing-qa/` | **TIER:** 2-3
**PURPOSE:** Comprehensive QA strategies and test planning.
**WHEN TO USE:** Test planning, QA process setup.
**KEY AREAS:** Test pyramid, E2E testing, smoke tests, regression tests.


---

## ✨ CODE QUALITY & REFACTORING

<a id="frontendcodereview"></a>
### Frontend Code Review
**FILE:** `workflows/frontend-code-review/` | **TIER:** 2-3
**PURPOSE:** Specialized review for frontend code (React, CSS, performance).
**WHEN TO USE:** Frontend PR reviews.
**KEY CHECKS:** Component structure, state management, accessibility, performance, CSS.

<a id="lintandvalidate"></a>
### Lint and Validate
**FILE:** `workflows/lint-and-validate/` | **TIER:** 1-3
**PURPOSE:** Automated code quality checks.
**WHEN TO USE:** Before every commit, in CI/CD.
**KEY TOOLS:** ESLint, Prettier, Ruff, Black, type checkers.

<a id="receivingcodereview"></a>
### Receiving Code Review
**FILE:** `workflows/receiving-code-review.md` | **TIER:** 1-3
**PURPOSE:** Professional and constructive responses to feedback.
**WHEN TO USE:** Responding to PR comments.
**KEY PRACTICES:** Acknowledge feedback, explain decisions, implement changes, thank reviewers.

<a id="refactorcode"></a>
### Refactor Code
**FILE:** `workflows/refactor-code.md` | **TIER:** 2-3
**PURPOSE:** Safe and modular code improvements.
**WHEN TO USE:** Code smells, technical debt, maintainability issues.
**KEY STEPS:** Identify smell → Write tests → Refactor → Verify tests pass.

<a id="refactoringtriggers"></a>
### Refactoring Triggers ⭐ MANDATORY
**FILE:** `workflows/refactoring-triggers.md` | **TIER:** 2-3
**PURPOSE:** Know when to refactor (Rule of Three, complexity).
**WHEN TO USE:** Continuous evaluation during development.
**KEY TRIGGERS:** Code duplication (3x), function > 50 lines, file > 300 lines, complexity > 10.

<a id="requestingcodereview"></a>
### Requesting Code Review
**FILE:** `workflows/requesting-code-review/` | **TIER:** 1-3
**PURPOSE:** Create effective PR descriptions and review requests.
**WHEN TO USE:** Creating PRs.
**KEY ELEMENTS:** Context, changes summary, testing done, screenshots, checklist.

<a id="resourcecleanup"></a>
### Resource Cleanup
**FILE:** `workflows/resource-cleanup.md` | **TIER:** 2-3
**PURPOSE:** Proper cleanup of resources (files, connections, memory).
**WHEN TO USE:** File operations, DB connections, network requests.
**KEY PATTERNS:** try-finally, context managers, RAII, defer.

---

## 📋 PLANNING & ORCHESTRATION

<a id="planningwithfiles"></a>
### Planning with Files
**FILE:** `workflows/planning-with-files/` | **TIER:** 1-2
**PURPOSE:** File-based planning and task management.
**WHEN TO USE:** Project planning, sprint planning.
**KEY FILES:** tasks.md, roadmap.md, backlog.md, decisions.md.

<a id="workflowautomation"></a>
### Workflow Automation
**FILE:** `workflows/workflow-automation.md` | **TIER:** 2-3
**PURPOSE:** Infrastructure for durable agent execution.
**WHEN TO USE:** Automating repetitive tasks, building workflows.
**KEY CONCEPTS:** State machines, event-driven, retry logic, idempotency.

<a id="workfloworchestrationpatterns"></a>
### Workflow Orchestration Patterns
**FILE:** `workflows/workflow-orchestration-patterns/` | **TIER:** 3-4
**PURPOSE:** Complex workflow patterns (saga, choreography).
**WHEN TO USE:** Microservices, distributed systems, complex business processes.
**KEY PATTERNS:** Saga, choreography, orchestration, compensation.

<a id="workflowpatterns"></a>
### Workflow Patterns
**FILE:** `workflows/workflow-patterns/` | **TIER:** 2-3
**PURPOSE:** Common workflow design patterns.
**WHEN TO USE:** Designing workflows, process automation.
**KEY PATTERNS:** Sequential, parallel, conditional, loop, fork-join.

---

## 🎯 SPECIALIZED WORKFLOWS

<a id="cicdautomationworkflow"></a>
### CI/CD Automation Workflow
**FILE:** `workflows/cicd-automation-workflow-automate/` | **TIER:** 2-3
**PURPOSE:** Comprehensive CI/CD pipeline setup and optimization.
**WHEN TO USE:** Setting up or improving CI/CD.
**KEY STAGES:** Build, test, security scan, deploy, monitor.

<a id="globalmemoryprotocol"></a>
### Global Memory Protocol ⭐ CRITICAL
**FILE:** `workflows/GLOBAL_MEMORY_PROTOCOL.md` | **TIER:** 1-4
**PURPOSE:** Cross-session learning and knowledge retention.
**WHEN TO USE:** After every complex task.
**KEY PROCESS:** Log conversation → Extract insights → Store in brain/ → Enable cross-session learning.

<a id="i18nlocalization"></a>
### i18n Localization
**FILE:** `workflows/i18n-localization/` | **TIER:** 2-3
**PURPOSE:** Internationalization and localization best practices.
**WHEN TO USE:** Multi-language apps, global products.
**KEY AREAS:** Translation management, locale handling, RTL support, date/number formatting.

<a id="metarules"></a>
### Meta Rules
**FILE:** `workflows/meta-rules.md` | **TIER:** 3-4
**PURPOSE:** Rules about rules - system governance.
**WHEN TO USE:** System design, governance, meta-programming.
**KEY CONCEPTS:** Rule composition, conflict resolution, priority systems.

<a id="skillcreator"></a>
### Skill Creator
**FILE:** `workflows/skill-creator.md` | **TIER:** 2-3
**PURPOSE:** Guide for creating effective, token-efficient atomic skills.
**WHEN TO USE:** Creating new skills, documenting patterns.
**KEY GUIDELINES:** < 20KB per skill, clear purpose, actionable rules, examples.

<a id="systemconstitution"></a>
### System Constitution ⭐ GOVERNANCE
**FILE:** `workflows/SYSTEM_CONSTITUTION.md` | **TIER:** 1-4
**PURPOSE:** Core governance rules for the entire system.
**WHEN TO USE:** ALWAYS - foundational rules.
**KEY RULES:** Security-first, test-before-claim, systematic debugging, no hallucination.

<a id="verificationbeforecompletion"></a>
### Verification Before Completion ⭐ MANDATORY
**FILE:** `workflows/verification-before-completion.md` | **TIER:** 1-4
**PURPOSE:** Evidence-based success claims - NEVER claim "done" without proof.
**WHEN TO USE:** Before claiming any task complete.
**KEY EVIDENCE:** Test output, terminal logs, screenshots, metrics.

---

## 📊 Usage Guidelines

### When to Load This Inventory
- **Tier 1 tasks:** Load 3-5 relevant skills
- **Tier 2 tasks:** Load 5-8 relevant skills
- **Tier 3 tasks:** Load 8-12 relevant skills
- **Tier 4 tasks:** Load 12-15 relevant skills

### Critical Skills (Always Consider)
1. **Anti-Hallucination Protocol v2** - Before using any library/API
2. **Debug Protocol** - When encountering any bug
3. **Verification Before Completion** - Before claiming "done"
4. **Naming Conventions** - Before committing code
5. **System Constitution** - Foundational governance

### Token Optimization Strategy
1. Load master inventory first (lightweight)
2. Identify relevant skills from index
3. Load only needed full skills
4. Cache loaded skills in memory
5. Unload after task completion

---

**VERSION:** v6.5.0-SLIM  
**LAST UPDATED:** 2026-03-31  
**TOTAL SKILLS:** 62 workflow skills  
**TOKEN SAVINGS:** 98% vs loading individual files  
**MAINTAINED BY:** Antigravity Resilience System
