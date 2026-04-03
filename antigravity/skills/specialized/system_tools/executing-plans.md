---
name: "Executing Plans"
tags: ["antigravity", "c:", "checklist", "coding", "discover", "executing", "first", "frontend", "gemini", "issues", "later", "<YOUR_USERNAME>", "overview", "plan", "plans", "read", "review", "rules", "specialized", "start"]
tier: 2
risk: "medium"
estimated_tokens: 1934
tools_needed: ["docker", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.94
---
# Executing Plans

> **Tier:** 2  
> **Tags:** `planning`, `execution`, `workflow`, `review`, `checkpoints`  
> **When to use:** Implementing written plans, need review checkpoints, batch task execution

---

## Overview

Systematic approach to executing written plans with review checkpoints. Execute tasks in batches (default: 3 tasks), report progress for review, and know when to stop and ask for help. Prevents runaway execution and ensures quality.

---

## Rules

**RULE-001: Load and Review Plan Critically**
Read the entire plan before starting. Identify unclear steps, missing information, or potential issues. Ask clarifying questions upfront.

```markdown
❌ Bad: Start executing immediately
# Read first task, start coding
# Discover issues later, waste time

✅ Good: Review entire plan first
## Plan Review Checklist
- [ ] All steps clear and actionable?
- [ ] Dependencies identified?
- [ ] Required resources available?
- [ ] Estimated time reasonable?
- [ ] Success criteria defined?
- [ ] Rollback plan if needed?

## Questions Before Starting
1. Step 3 mentions "update config" - which config file?
2. Step 5 requires API key - where do I get it?
3. Step 7 says "test thoroughly" - what tests specifically?
```

**RULE-002: Execute in Batches**
Default batch size: 3 tasks. Complete batch, then report for review. Adjust batch size based on task complexity.

```markdown
❌ Bad: Execute all 20 tasks without pause
# Task 1: ✅
# Task 2: ✅
# Task 3: ✅
# ...
# Task 15: ❌ (wrong approach, wasted 14 tasks)

✅ Good: Batch execution with checkpoints
## Batch 1 (Tasks 1-3)
- [x] Task 1: Setup database schema
- [x] Task 2: Create user model
- [x] Task 3: Add validation

**CHECKPOINT: Review before continuing**
- All tests passing?
- Approach correct?
- Any issues discovered?

## Batch 2 (Tasks 4-6)
- [ ] Task 4: Create API endpoints
- [ ] Task 5: Add authentication
- [ ] Task 6: Write integration tests
```

**RULE-003: Report Progress After Each Batch**
Summarize what was completed, any issues encountered, and next steps. Wait for feedback before continuing.

```markdown
❌ Bad: Silent execution
# Complete 10 tasks
# No updates
# User doesn't know progress

✅ Good: Progress reports
## Batch 1 Complete (Tasks 1-3)

### Completed
✅ Task 1: Database schema created (users, posts tables)
✅ Task 2: User model with validation
✅ Task 3: Unit tests passing (15/15)

### Issues Encountered
⚠️ Task 2: Had to add email uniqueness constraint (not in plan)

### Next Batch (Tasks 4-6)
- Task 4: Create REST API endpoints
- Task 5: Add JWT authentication
- Task 6: Integration tests

**Ready to proceed? Any feedback on Batch 1?**
```

**RULE-004: Stop and Ask When Uncertain**
Don't guess or make assumptions. Stop execution and ask for clarification when encountering ambiguity or blockers.

```markdown
❌ Bad: Guess and continue
# Task says "configure the system"
# Guess what configuration is needed
# Implement wrong thing

✅ Good: Stop and clarify
## Execution Paused at Task 5

**Issue:** Task 5 says "configure the system" but doesn't specify:
1. Which configuration file? (.env, config.json, or database?)
2. What values to set?
3. Development or production config?

**Options I see:**
A. Configure .env with database credentials
B. Configure config.json with API settings
C. Both of the above

**Question:** Which configuration is needed for Task 5?
```

**RULE-005: Verify Success Criteria**
After each batch, verify tasks meet success criteria. Run tests, check output, validate functionality.

```markdown
❌ Bad: Assume success
# Task 3: "Add validation"
# Write validation code
# Move to next task (no verification)

✅ Good: Verify success
## Task 3: Add Validation

### Implementation
```typescript
function validateUser(user) {
  if (!user.email) throw new Error('Email required');
  if (!user.name) throw new Error('Name required');
}
```

### Verification
```bash
# Run tests
npm test -- user.test.ts
✅ All 5 validation tests passing

# Manual test
node -e "validateUser({})" # Throws error ✅
node -e "validateUser({email:'a@b.com',name:'Alice'})" # Success ✅
```

### Success Criteria Met
- [x] Email validation works
- [x] Name validation works
- [x] Tests passing
- [x] Error messages clear
```

**RULE-006: Handle Blockers Gracefully**
When blocked, document the blocker, attempted solutions, and ask for help. Don't waste time on dead ends.

```markdown
❌ Bad: Spend hours on blocker
# Task 7: Deploy to production
# Deployment fails
# Try 10 different things
# Still failing after 3 hours

✅ Good: Document and escalate
## Blocker at Task 7: Deployment Failing

### Error
```
Error: EACCES: permission denied, mkdir '/var/www/app'
```

### Attempted Solutions
1. ✅ Checked file permissions - correct (755)
2. ✅ Verified user has sudo access - yes
3. ❌ Tried `sudo npm run deploy` - same error
4. ❌ Changed directory to /tmp - different error

### Need Help
**Question:** Should I:
A. Request elevated permissions for /var/www/app?
B. Deploy to different directory?
C. Use Docker instead?

**Time spent:** 30 minutes
**Blocking:** Tasks 7-10 (deployment related)
```

**RULE-007: Adjust Batch Size Dynamically**
Reduce batch size for complex tasks. Increase for simple tasks. Typical ranges: 1-5 tasks per batch.

```markdown
# Complex tasks (1-2 per batch)
## Batch 1
- [ ] Task 1: Design database schema (complex)

## Batch 2
- [ ] Task 2: Implement authentication (complex)

# Simple tasks (4-5 per batch)
## Batch 1
- [ ] Task 1: Add logging
- [ ] Task 2: Update README
- [ ] Task 3: Fix typos
- [ ] Task 4: Format code
- [ ] Task 5: Update dependencies
```

**RULE-008: Integration with Finishing Branch**
When plan is part of feature branch, follow finishing-a-development-branch workflow after completion.

```markdown
## Plan Execution Complete ✅

All 15 tasks completed successfully.

### Next Steps (Finishing Branch)
1. Run full test suite
2. Check code coverage
3. Run linter
4. Update documentation
5. Create pull request
6. Request code review

**Ready to proceed with branch finishing workflow?**
```

---

## Quick Reference

### Execution Workflow

```
1. Load Plan
   ↓
2. Review Critically
   ↓
3. Execute Batch (3 tasks)
   ↓
4. Verify Success
   ↓
5. Report Progress
   ↓
6. Wait for Feedback
   ↓
7. Next Batch or Stop
```

### Batch Size Guidelines

| Task Complexity | Batch Size | Example |
|----------------|------------|---------|
| Very Complex | 1 task | Architecture design, complex algorithm |
| Complex | 2 tasks | Authentication system, API design |
| Medium | 3 tasks | CRUD endpoints, validation logic |
| Simple | 4-5 tasks | Documentation, formatting, minor fixes |

### Progress Report Template

```markdown
## Batch N Complete (Tasks X-Y)

### Completed
✅ Task X: [description] - [outcome]
✅ Task Y: [description] - [outcome]

### Issues Encountered
⚠️ [Issue description and resolution]

### Verification
- [x] Tests passing
- [x] Functionality verified
- [x] No regressions

### Next Batch (Tasks A-B)
- Task A: [description]
- Task B: [description]

**Ready to proceed?**
```

### When to Stop and Ask

- [ ] Task description unclear
- [ ] Missing required information
- [ ] Blocker encountered (>30 min)
- [ ] Approach seems wrong
- [ ] Success criteria ambiguous
- [ ] Breaking changes needed
- [ ] Security concerns
- [ ] Performance issues

### Verification Checklist

- [ ] Code compiles/runs
- [ ] Tests passing
- [ ] Linter passing
- [ ] Functionality works as expected
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] Success criteria met

---

## Metadata

- **Related Skills:** [finishing-a-development-branch.md], [systematic-debugging.md], [code-review.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
