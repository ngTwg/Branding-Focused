---
name: "Test Fixing"
tags: ["antigravity", "c:", "causes", "commands", "common", "debugging", "failure", "fixing", "frontend", "gemini", "<YOUR_USERNAME>", "overview", "quick", "reference", "rules", "specialized", "system", "test", "tools", "users"]
tier: 2
risk: "medium"
estimated_tokens: 2700
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# Test Fixing

> **Tier:** 2  
> **Tags:** `testing`, `debugging`, `test-repair`, `troubleshooting`, `flaky-tests`  
> **When to use:** Tests failing, flaky tests, test maintenance, updating tests for code changes

---

## Overview

Systematic approach to debugging and fixing failing tests. Identify root causes, fix flaky tests, update tests for code changes, refactor test code, and avoid common test anti-patterns.

---

## Rules

**RULE-001: Identify Failure Root Cause**
Determine if test failure is due to: broken code, broken test, environmental issue, or flaky test. Don't fix blindly.

```typescript
❌ Bad: Fix test without understanding
test('user creation', async () => {
  const user = await createUser({ name: 'Alice' });
  expect(user.id).toBe(123); // Fails
  // Change to: expect(user.id).toBeDefined() // Masks real issue
});

✅ Good: Investigate root cause
// 1. Read error message
// Expected: 123, Received: 456

// 2. Check if code changed
// git log --oneline -- src/user-service.ts

// 3. Determine cause
// Code now generates random IDs (correct behavior)
// Test expects specific ID (incorrect expectation)

// 4. Fix test properly
test('user creation', async () => {
  const user = await createUser({ name: 'Alice' });
  expect(user.id).toBeDefined();
  expect(typeof user.id).toBe('number');
  expect(user.name).toBe('Alice');
});
```

**RULE-002: Fix Flaky Tests**
Flaky tests pass/fail randomly. Common causes: timing issues, shared state, external dependencies, non-deterministic code.

```typescript
❌ Bad: Flaky test (timing issue)
test('async operation completes', async () => {
  startAsyncOperation();
  await new Promise(resolve => setTimeout(resolve, 100)); // Race condition
  expect(isComplete()).toBe(true); // Sometimes fails
});

✅ Good: Wait for actual condition
test('async operation completes', async () => {
  startAsyncOperation();
  
  // Wait for condition, not arbitrary time
  await waitFor(() => {
    expect(isComplete()).toBe(true);
  }, { timeout: 5000 });
});

❌ Bad: Flaky test (shared state)
let counter = 0; // Shared between tests

test('increments counter', () => {
  counter++;
  expect(counter).toBe(1); // Fails if tests run in different order
});

✅ Good: Isolated state
test('increments counter', () => {
  let counter = 0; // Local to test
  counter++;
  expect(counter).toBe(1);
});

// Or use beforeEach
describe('Counter', () => {
  let counter;
  
  beforeEach(() => {
    counter = 0; // Reset before each test
  });
  
  test('increments counter', () => {
    counter++;
    expect(counter).toBe(1);
  });
});
```

**RULE-003: Update Tests for Code Changes**
When code behavior changes intentionally, update tests to match. Don't just make tests pass without understanding why they failed.

```typescript
// Code changed: email validation now requires @
function validateEmail(email) {
  return email.includes('@'); // Was: email.length > 0
}

❌ Bad: Blindly update test
test('validates email', () => {
  expect(validateEmail('alice')).toBe(true); // Fails now
  // Change to: expect(validateEmail('alice')).toBe(false)
  // Without understanding why
});

✅ Good: Update test with understanding
test('validates email', () => {
  // Updated: email validation now requires @
  expect(validateEmail('alice@example.com')).toBe(true);
  expect(validateEmail('alice')).toBe(false); // No @
  expect(validateEmail('')).toBe(false);
});
```

**RULE-004: Refactor Test Code**
Apply same quality standards to test code. Extract helpers, remove duplication, improve readability.

```typescript
❌ Bad: Duplicated test setup
test('creates user with email', async () => {
  const db = await setupDatabase();
  const service = new UserService(db);
  const user = await service.create({ email: 'a@b.com' });
  expect(user.email).toBe('a@b.com');
  await cleanupDatabase(db);
});

test('creates user with name', async () => {
  const db = await setupDatabase();
  const service = new UserService(db);
  const user = await service.create({ name: 'Alice' });
  expect(user.name).toBe('Alice');
  await cleanupDatabase(db);
});

✅ Good: Extract common setup
describe('UserService', () => {
  let db, service;
  
  beforeEach(async () => {
    db = await setupDatabase();
    service = new UserService(db);
  });
  
  afterEach(async () => {
    await cleanupDatabase(db);
  });
  
  test('creates user with email', async () => {
    const user = await service.create({ email: 'a@b.com' });
    expect(user.email).toBe('a@b.com');
  });
  
  test('creates user with name', async () => {
    const user = await service.create({ name: 'Alice' });
    expect(user.name).toBe('Alice');
  });
});
```

**RULE-005: Fix Test Anti-Patterns**
Avoid: testing implementation details, brittle selectors, magic numbers, unclear assertions, missing cleanup.

```typescript
❌ Bad: Testing implementation details
test('user service calls repository', () => {
  const mockRepo = { save: jest.fn() };
  const service = new UserService(mockRepo);
  service.createUser({ name: 'Alice' });
  expect(mockRepo.save).toHaveBeenCalled(); // Implementation detail
});

✅ Good: Test behavior
test('user service creates user', async () => {
  const mockRepo = { save: jest.fn().mockResolvedValue({ id: 1, name: 'Alice' }) };
  const service = new UserService(mockRepo);
  const user = await service.createUser({ name: 'Alice' });
  expect(user).toEqual({ id: 1, name: 'Alice' });
});

❌ Bad: Magic numbers
test('calculates discount', () => {
  expect(calculateDiscount(150)).toBe(15);
  expect(calculateDiscount(200)).toBe(20);
});

✅ Good: Named constants
test('calculates 10% discount for orders over $100', () => {
  const DISCOUNT_RATE = 0.1;
  expect(calculateDiscount(150)).toBe(150 * DISCOUNT_RATE);
  expect(calculateDiscount(200)).toBe(200 * DISCOUNT_RATE);
});
```

**RULE-006: Debug Test Failures Systematically**
Use debugging tools, add logging, isolate failing test, check test environment.

```typescript
// 1. Run single test
npm test -- user.test.ts -t "creates user"

// 2. Add debug logging
test('creates user', async () => {
  console.log('Input:', userData);
  const user = await createUser(userData);
  console.log('Output:', user);
  expect(user.name).toBe('Alice');
});

// 3. Use debugger
test('creates user', async () => {
  debugger; // Pause here
  const user = await createUser(userData);
  expect(user.name).toBe('Alice');
});

// Run with debugger
node --inspect-brk node_modules/.bin/jest --runInBand

// 4. Check test environment
test('environment check', () => {
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('Database:', process.env.DATABASE_URL);
});
```

**RULE-007: Handle Async Test Issues**
Common async issues: missing await, unhandled promise rejections, timeouts.

```typescript
❌ Bad: Missing await
test('async operation', async () => {
  createUser({ name: 'Alice' }); // Missing await
  const users = await getUsers();
  expect(users).toHaveLength(1); // Fails, user not created yet
});

✅ Good: Proper await
test('async operation', async () => {
  await createUser({ name: 'Alice' });
  const users = await getUsers();
  expect(users).toHaveLength(1);
});

❌ Bad: Unhandled rejection
test('handles error', async () => {
  createUser({ invalid: 'data' }); // Promise rejection not caught
});

✅ Good: Expect rejection
test('handles error', async () => {
  await expect(createUser({ invalid: 'data' }))
    .rejects
    .toThrow('Validation error');
});

// Increase timeout for slow tests
test('slow operation', async () => {
  await slowOperation();
}, 10000); // 10 second timeout
```

**RULE-008: Maintain Test Data**
Use factories, fixtures, or builders for test data. Keep test data realistic but minimal.

```typescript
❌ Bad: Inline test data everywhere
test('test 1', () => {
  const user = { id: 1, name: 'Alice', email: 'alice@example.com', age: 30 };
  // ...
});

test('test 2', () => {
  const user = { id: 2, name: 'Bob', email: 'bob@example.com', age: 25 };
  // ...
});

✅ Good: Test data factory
// test-helpers.ts
export function createTestUser(overrides = {}) {
  return {
    id: Math.floor(Math.random() * 1000),
    name: 'Test User',
    email: 'test@example.com',
    age: 30,
    ...overrides
  };
}

// tests
test('test 1', () => {
  const user = createTestUser({ name: 'Alice' });
  // ...
});

test('test 2', () => {
  const user = createTestUser({ name: 'Bob', age: 25 });
  // ...
});
```

---

## Quick Reference

### Common Test Failure Causes

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Test passes locally, fails in CI | Environment difference | Check env vars, dependencies |
| Test fails randomly | Flaky test (timing, state) | Fix race conditions, isolate state |
| All tests fail after code change | Breaking change | Update tests for new behavior |
| Test fails after dependency update | API change | Check changelog, update usage |
| Test times out | Slow operation, infinite loop | Increase timeout, debug code |

### Debugging Commands

```bash
# Run single test
npm test -- path/to/test.ts -t "test name"

# Run with debugger
node --inspect-brk node_modules/.bin/jest --runInBand

# Verbose output
npm test -- --verbose

# Show console.log
npm test -- --silent=false

# Run tests serially (easier to debug)
npm test -- --runInBand

# Update snapshots
npm test -- -u
```

### Flaky Test Checklist

- [ ] Remove arbitrary timeouts (use waitFor)
- [ ] Isolate test state (no shared variables)
- [ ] Mock external dependencies
- [ ] Use deterministic data (no Math.random(), Date.now())
- [ ] Clean up after test (afterEach)
- [ ] Avoid test order dependencies
- [ ] Check for race conditions

### Test Refactoring Patterns

```typescript
// Extract test helper
function expectUserToBeValid(user) {
  expect(user.id).toBeDefined();
  expect(user.email).toMatch(/@/);
  expect(user.name).toBeTruthy();
}

// Use test.each for similar tests
test.each([
  ['alice@example.com', true],
  ['invalid', false],
  ['', false]
])('validates email %s', (email, expected) => {
  expect(validateEmail(email)).toBe(expected);
});

// Extract test fixtures
const validUser = { name: 'Alice', email: 'alice@example.com' };
const invalidUser = { name: '', email: 'invalid' };
```

### Async Test Patterns

```typescript
// Wait for condition
await waitFor(() => {
  expect(element).toBeVisible();
});

// Wait for element
await screen.findByText('Welcome');

// Expect rejection
await expect(promise).rejects.toThrow('Error');

// Expect resolution
await expect(promise).resolves.toBe(value);

// Custom timeout
test('slow test', async () => {
  // ...
}, 10000);
```

---

## Metadata

- **Related Skills:** [testing-patterns.md], [systematic-debugging.md], [code-review.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
