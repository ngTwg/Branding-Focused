---
name: "Create Pull Request"
tags: ["additions", "antigravity", "bug", "c:", "create", "documentation", "feature", "fixes", "frontend", "gemini", "<YOUR_USERNAME>", "overview", "pr", "pull", "request", "rules", "specialized", "system", "tools", "users"]
tier: 3
risk: "medium"
estimated_tokens: 1443
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.90
---
# Create Pull Request

> **Tier:** 1-2  
> **Tags:** `github`, `pr`, `pull-request`, `git`, `code-review`  
> **When to use:** Creating GitHub pull requests with proper formatting and conventions

---

## Overview

Standardized approach to creating GitHub pull requests with clear titles, descriptions, and conventional commit formats. Ensures PRs are reviewable, traceable, and follow team conventions.

---

## Rules

**RULE-001: PR Title Format**
Use conventional commit format: `type(scope): summary`. Type indicates change category, scope indicates affected area, summary is concise description.

```markdown
❌ Bad: Vague titles
"Fix bug"
"Update code"
"Changes"

✅ Good: Descriptive conventional format
"fix(auth): resolve token expiration issue"
"feat(api): add user profile endpoint"
"docs(readme): update installation instructions"
```

**RULE-002: Conventional Commit Types**
Use standard types: feat (new feature), fix (bug fix), docs (documentation), style (formatting), refactor (code restructure), test (tests), chore (maintenance).

```markdown
# Feature additions
feat(dashboard): add real-time metrics chart

# Bug fixes
fix(payment): handle null payment method

# Documentation
docs(api): add authentication examples

# Code quality
refactor(utils): simplify date formatting logic

# Tests
test(auth): add login flow integration tests

# Maintenance
chore(deps): update dependencies to latest
```

**RULE-003: PR Body Template**
Include: summary, changes made, testing done, related issues, breaking changes (if any). Use markdown formatting for readability.

```markdown
❌ Bad: Empty or minimal description
"Fixed the bug"

✅ Good: Comprehensive description
## Summary
Resolves token expiration issue causing users to be logged out prematurely.

## Changes
- Updated token refresh logic in `auth.service.ts`
- Added 5-minute buffer before expiration
- Implemented automatic retry on 401 responses

## Testing
- [x] Unit tests pass
- [x] Manual testing with expired tokens
- [x] Verified refresh flow in production-like environment

## Related Issues
Closes #123

## Breaking Changes
None
```

**RULE-004: Scope Naming**
Use consistent scope names matching project structure: component names, module names, or feature areas. Keep scopes short and recognizable.

```markdown
❌ Bad: Inconsistent or vague scopes
feat(stuff): add thing
fix(code): fix problem

✅ Good: Clear, consistent scopes
feat(user-profile): add avatar upload
fix(shopping-cart): correct tax calculation
docs(contributing): add PR guidelines
```

**RULE-005: Summary Guidelines**
Keep summary under 72 characters. Use imperative mood ("add" not "added"). Be specific about what changed, not why.

```markdown
❌ Bad: Too long or wrong tense
"Added a new feature that allows users to upload profile pictures"
"Fixed the bug that was causing crashes"

✅ Good: Concise imperative
"add profile picture upload"
"fix crash on null user data"
```

**RULE-006: Link Related Issues**
Reference issues using keywords: Closes, Fixes, Resolves. GitHub auto-links and closes issues when PR merges.

```markdown
❌ Bad: No issue reference
"This fixes the login bug"

✅ Good: Explicit issue linking
Closes #456
Fixes #789, #790
Resolves #123
```

**RULE-007: Breaking Changes**
Clearly mark breaking changes in PR body. Explain what breaks and migration path. Use BREAKING CHANGE: prefix in commit message for semantic versioning.

```markdown
## Breaking Changes
⚠️ **BREAKING:** Removed deprecated `getUserData()` method

**Migration:**
Replace `getUserData()` with `getUser().data`

```typescript
// Before
const data = getUserData();

// After
const data = getUser().data;
```
```

**RULE-008: Draft PRs**
Use draft PRs for work-in-progress. Mark as "ready for review" only when complete and tests pass. Add [WIP] prefix to title if not using draft feature.

```markdown
# Draft PR (not ready)
[WIP] feat(api): add user profile endpoint

# Ready for review
feat(api): add user profile endpoint
```

---

## Quick Reference

### PR Title Format

```
<type>(<scope>): <summary>

Examples:
feat(auth): add OAuth2 login
fix(cart): correct discount calculation
docs(api): update endpoint documentation
refactor(db): optimize query performance
test(user): add profile update tests
chore(ci): update GitHub Actions workflow
```

### Conventional Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat(search): add fuzzy matching` |
| `fix` | Bug fix | `fix(login): handle empty password` |
| `docs` | Documentation | `docs(readme): add setup instructions` |
| `style` | Code style | `style(app): format with prettier` |
| `refactor` | Code restructure | `refactor(api): extract validation logic` |
| `perf` | Performance | `perf(db): add index on user_id` |
| `test` | Tests | `test(auth): add token expiration tests` |
| `build` | Build system | `build(webpack): optimize bundle size` |
| `ci` | CI/CD | `ci(actions): add automated tests` |
| `chore` | Maintenance | `chore(deps): update react to v18` |

### PR Body Checklist

- [ ] Summary of changes
- [ ] List of specific changes made
- [ ] Testing performed
- [ ] Related issue links (Closes #123)
- [ ] Breaking changes documented
- [ ] Migration guide (if breaking)
- [ ] Screenshots (if UI changes)

### GitHub CLI Commands

```bash
# Create PR from current branch
gh pr create --title "feat(api): add user endpoint" --body "Description here"

# Create draft PR
gh pr create --draft --title "[WIP] feat(api): add user endpoint"

# Create PR with template
gh pr create --fill

# View PR status
gh pr status

# Mark draft as ready
gh pr ready
```

---

## Metadata

- **Related Skills:** [git-workflow.md], [code-review.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
