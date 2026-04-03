---
name: "System Tools - Master Inventory"
tags: ["specialized", "system", "tools"]
tier: 4
risk: "high"
estimated_tokens: 1563
tools_needed: ["docker", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["specialized"]
quality_score: 0.55
---
# System Tools - Master Inventory

> **Category:** System Tools & Development Utilities  
> **Total Skills:** 16 atomic skills  
> **Token Savings:** ~95% for single-skill loads

---

## Overview

Comprehensive collection of system tools, shell scripting, development utilities, and software engineering practices. Each skill is atomic (< 20KB) for efficient loading.

---

## Quick Navigation

### Shell & Terminal (3 skills)
- **bash-linux.md** - Bash/Linux terminal patterns, piping, scripting
- **powershell-windows.md** - PowerShell cmdlets, object pipeline, Windows automation
- **busybox-on-windows.md** - Unix tools on Windows via BusyBox

### Development Tools (4 skills)
- **bullmq-specialist.md** - Redis-backed job queues, background processing
- **create-pr.md** - GitHub PR creation with proper formatting
- **environment-setup-guide.md** - Dev environment setup across platforms
- **file-organizer.md** - Intelligent file organization and cleanup

### Programming Concepts (2 skills)
- **javascript-mastery.md** - 33+ essential JS concepts
- **nosql-expert.md** - NoSQL databases, patterns, best practices

### Software Engineering (4 skills)
- **kaizen.md** - Continuous improvement, error-proofing, lean development
- **software-architecture.md** - Architecture patterns, design principles
- **production-code-audit.md** - Code quality, security, performance audits
- **executing-plans.md** - Batch execution with review checkpoints

### Testing & Quality (3 skills)
- **testing-patterns.md** - Unit, integration, E2E testing strategies
- **test-fixing.md** - Systematic test debugging and repair
- **file-uploads.md** - File upload handling, validation, security

---

## Skill Details

### 1. bash-linux.md
**Size:** ~4KB | **Tier:** 1-2  
**Tags:** `bash`, `linux`, `shell`, `terminal`, `scripting`

Essential Bash patterns for Linux/macOS:
- Operator syntax (`;`, `&&`, `||`, `|`)
- File operations (find, grep, tail)
- Process management (ps, kill, lsof)
- Text processing (sed, awk, cut)
- Environment variables
- Network commands (curl, nc)
- Script templates with error handling

**Use when:** Working on Linux/macOS, need terminal commands, shell scripting

---

### 2. powershell-windows.md
**Size:** ~5KB | **Tier:** 1-2  
**Tags:** `powershell`, `windows`, `shell`, `terminal`, `scripting`

PowerShell patterns for Windows:
- Core cmdlets (Get-ChildItem, Get-Process)
- Object-based pipeline
- Process management
- Environment variables (permanent/temporary)
- Network operations (Invoke-WebRequest)
- Script templates with try-catch
- Execution policy management

**Use when:** Working on Windows, need PowerShell automation

---

### 3. busybox-on-windows.md
**Size:** ~2KB | **Tier:** 1  
**Tags:** `busybox`, `windows`, `unix`, `tools`

Run Unix commands on Windows:
- BusyBox installation (x86/x64/ARM builds)
- Available Unix commands
- Usage patterns
- Integration with Windows workflows

**Use when:** Need Unix tools on Windows without WSL

---

### 4. bullmq-specialist.md
**Size:** ~6KB | **Tier:** 2-3  
**Tags:** `bullmq`, `redis`, `queue`, `background-jobs`, `async`

Production-grade job queues with BullMQ:
- Queue setup with proper configuration
- Delayed and scheduled jobs
- Job flows and dependencies
- Worker patterns and concurrency
- Rate limiting
- Anti-patterns (giant payloads, no DLQ, infinite concurrency)
- Best practices for reliability

**Use when:** Redis-backed queues, background processing, async workflows

---

### 5. create-pr.md
**Size:** ~3KB | **Tier:** 1-2  
**Tags:** `github`, `pr`, `pull-request`, `git`

Create GitHub PRs with proper formatting:
- PR title format (type, scope, summary)
- Conventional commit types
- PR body template
- Validation rules
- Examples for different scenarios

**Use when:** Creating PRs, submitting changes for review

---

### 6. environment-setup-guide.md
**Size:** ~12KB | **Tier:** 1-2  
**Tags:** `setup`, `environment`, `dev-tools`, `onboarding`

Complete dev environment setup:
- Node.js, Python, Docker setup
- Platform-specific instructions (macOS, Linux, Windows)
- Environment variables and configuration
- Verification steps
- Troubleshooting common issues
- Setup script templates

**Use when:** Setting up new dev environment, onboarding, troubleshooting

---

### 7. file-organizer.md
**Size:** ~8KB | **Tier:** 1-2  
**Tags:** `files`, `organization`, `cleanup`, `duplicates`

Intelligent file organization:
- Analyze current structure
- Find duplicates
- Suggest logical groupings
- Automate cleanup
- Maintain context
- Best practices for folder naming

**Use when:** Organizing downloads, cleaning up directories, removing duplicates

---

### 8. javascript-mastery.md
**Size:** ~8KB | **Tier:** 2-3  
**Tags:** `javascript`, `js`, `concepts`, `fundamentals`, `advanced`

33+ essential JavaScript concepts:
- Core concepts (call stack, types, coercion, scope)
- Functions (closures, HOF, recursion, this)
- OOP (prototypes, classes, inheritance)
- Async (Promises, async/await, event loop)
- Advanced (debounce, throttle, currying, memoization, generators, Proxy)

**Use when:** Deep JS understanding, interview prep, advanced patterns

---

### 9. nosql-expert.md
**Size:** ~10KB | **Tier:** 2-3  
**Tags:** `nosql`, `mongodb`, `redis`, `cassandra`, `database`

NoSQL databases and patterns:
- Document stores (MongoDB)
- Key-value stores (Redis)
- Column-family stores (Cassandra)
- Graph databases (Neo4j)
- When to use each type
- Data modeling patterns
- Performance optimization

**Use when:** Choosing NoSQL database, data modeling, scaling strategies

---

### 10. kaizen.md
**Size:** ~15KB | **Tier:** 2-3  
**Tags:** `kaizen`, `continuous-improvement`, `lean`, `quality`

Continuous improvement philosophy:
- Four pillars (Kaizen, Poka-Yoke, Genchi Genbutsu, Muda)
- Small incremental changes
- Error-proofing by design
- Go to the source
- Eliminate waste
- Integration with development workflow

**Use when:** Improving processes, preventing errors, lean development

---

### 11. software-architecture.md
**Size:** ~18KB | **Tier:** 3-4  
**Tags:** `architecture`, `design`, `patterns`, `scalability`

Architecture patterns and principles:
- Layered, microservices, event-driven architectures
- SOLID principles
- Design patterns (creational, structural, behavioral)
- Scalability patterns
- Security architecture
- Documentation practices

**Use when:** Designing systems, architecture decisions, scaling applications

---

### 12. production-code-audit.md
**Size:** ~12KB | **Tier:** 2-3  
**Tags:** `audit`, `code-quality`, `security`, `performance`

Comprehensive code audits:
- Security vulnerabilities (OWASP Top 10)
- Performance bottlenecks
- Code quality issues
- Best practices violations
- Dependency audits
- Automated audit tools

**Use when:** Code reviews, security audits, performance optimization

---

### 13. executing-plans.md
**Size:** ~3KB | **Tier:** 2  
**Tags:** `planning`, `execution`, `workflow`, `review`

Batch execution with checkpoints:
- Load and review plan critically
- Execute tasks in batches (default: 3 tasks)
- Report for review between batches
- When to stop and ask for help
- Integration with finishing-a-development-branch

**Use when:** Implementing written plans, need review checkpoints

---

### 14. testing-patterns.md
**Size:** ~14KB | **Tier:** 2-3  
**Tags:** `testing`, `unit-tests`, `integration`, `e2e`, `tdd`

Comprehensive testing strategies:
- Unit testing patterns
- Integration testing
- E2E testing
- Test-driven development (TDD)
- Mocking and stubbing
- Test coverage strategies
- Testing frameworks comparison

**Use when:** Writing tests, TDD, test strategy planning

---

### 15. test-fixing.md
**Size:** ~8KB | **Tier:** 2  
**Tags:** `testing`, `debugging`, `test-repair`, `troubleshooting`

Systematic test debugging:
- Identify test failure root cause
- Fix flaky tests
- Update tests for code changes
- Refactor test code
- Common test anti-patterns

**Use when:** Tests failing, flaky tests, test maintenance

---

### 16. file-uploads.md
**Size:** ~6KB | **Tier:** 2  
**Tags:** `uploads`, `files`, `validation`, `security`, `storage`

Secure file upload handling:
- File validation (type, size, content)
- Security best practices
- Storage strategies (local, S3, CDN)
- Progress tracking
- Error handling
- Malware scanning

**Use when:** Implementing file uploads, securing upload endpoints

---

## Routing Hints

### By Use Case

**Shell Scripting:**
- Linux/macOS → `bash-linux.md`
- Windows → `powershell-windows.md`
- Unix tools on Windows → `busybox-on-windows.md`

**Background Jobs:**
- Redis queues → `bullmq-specialist.md`

**Development Setup:**
- New environment → `environment-setup-guide.md`
- File organization → `file-organizer.md`

**Programming:**
- JavaScript deep dive → `javascript-mastery.md`
- NoSQL databases → `nosql-expert.md`

**Software Engineering:**
- Continuous improvement → `kaizen.md`
- Architecture design → `software-architecture.md`
- Code audits → `production-code-audit.md`

**Testing:**
- Test strategies → `testing-patterns.md`
- Fix failing tests → `test-fixing.md`

**Workflows:**
- Execute plans → `executing-plans.md`
- Create PRs → `create-pr.md`
- File uploads → `file-uploads.md`

---

## Token Efficiency

**Before Atomization:**
- Single monolithic file: 103.89KB
- Load time: High
- Context pollution: Severe

**After Atomization:**
- 16 atomic skills: 4-18KB each
- Average size: ~8KB
- Token savings: ~95% for single-skill loads
- Load only what you need

**Example:**
- Need Bash help? Load `bash-linux.md` (4KB) instead of entire 103.89KB file
- Savings: 96% fewer tokens

---

## Related Categories

- **Backend:** `backend-master-inventory.md`
- **Frontend:** `frontend-master-inventory.md`
- **Security:** `security-master-inventory.md`
- **Workflows:** `workflows-master-inventory.md`

---

**Version:** 1.0.0  
**Last Updated:** 2024-03-26  
**Atomization Date:** 2024-03-26  
**Total Size:** ~140KB (distributed across 16 files)
