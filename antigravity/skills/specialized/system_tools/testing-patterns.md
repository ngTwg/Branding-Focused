---
name: "Testing Patterns"
tags: ["antigravity", "brittle", "c:", "fast", "feedback", "frontend", "gemini", "<YOUR_USERNAME>", "overview", "patterns", "quick", "reference", "rules", "slow", "specialized", "stable", "system", "testing", "tests", "tools"]
tier: 2
risk: "medium"
estimated_tokens: 2758
tools_needed: ["markdown", "playwright", "pytest", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# Testing Patterns

> **Tier:** 2-3  
> **Tags:** `testing`, `unit-tests`, `integration`, `e2e`, `tdd`, `quality`  
> **When to use:** Writing tests, TDD, test strategy planning, quality assurance

---

## Overview

Comprehensive testing strategies covering unit tests, integration tests, E2E tests, test-driven development (TDD), mocking/stubbing, and test coverage. Build confidence in code correctness through systematic testing.

---

## Rules

**RULE-001: Test Pyramid**
Follow test pyramid: many unit tests (fast, isolated), fewer integration tests (moderate speed), few E2E tests (slow, expensive). Ratio approximately 70:20:10.

```
❌ Bad: Inverted pyramid
E2E Tests:     ████████████ (100 tests, 2 hours)
Integration:   ████ (20 tests, 10 min)
Unit Tests:    ██ (10 tests, 1 min)
# Slow feedback, brittle tests

✅ Good: Proper pyramid
Unit Tests:    ████████████████████ (200 tests, 2 min)
Integration:   ████████ (40 tests, 5 min)
E2E Tests:     ██ (10 tests, 10 min)
# Fast feedback, stable tests
```

**RULE-002: Unit Test Patterns**
Test single units in isolation. Mock dependencies. Test behavior, not implementation. Use AAA pattern (Arrange, Act, Assert).

```typescript
❌ Bad: Testing implementation details
test('user service uses repository', () => {
  const service = new UserService(mockRepo);
  service.getUser(123);
  expect(mockRepo.findById).toHaveBeenCalled(); // Implementation detail
});

✅ Good: Testing behavior
test('getUser returns user data', async () => {
  // Arrange
  const mockRepo = {
    findById: jest.fn().mockResolvedValue({ id: 123, name: 'Alice' })
  };
  const service = new UserService(mockRepo);
  
  // Act
  const user = await service.getUser(123);
  
  // Assert
  expect(user).toEqual({ id: 123, name: 'Alice' });
});

test('getUser throws when user not found', async () => {
  // Arrange
  const mockRepo = {
    findById: jest.fn().mockResolvedValue(null)
  };
  const service = new UserService(mockRepo);
  
  // Act & Assert
  await expect(service.getUser(999)).rejects.toThrow('User not found');
});
```

**RULE-003: Integration Test Patterns**
Test multiple units working together. Use real dependencies where practical. Test critical paths and error scenarios.

```typescript
❌ Bad: Mock everything (not integration test)
test('create order flow', async () => {
  const mockInventory = { reserve: jest.fn() };
  const mockPayment = { charge: jest.fn() };
  const mockEmail = { send: jest.fn() };
  // This is still a unit test
});

✅ Good: Real integration
test('create order flow', async () => {
  // Use real database (test DB)
  const db = await setupTestDatabase();
  
  // Real services
  const inventoryService = new InventoryService(db);
  const paymentService = new PaymentService(testApiKey);
  const orderService = new OrderService(db, inventoryService, paymentService);
  
  // Test real flow
  const order = await orderService.createOrder({
    items: [{ id: 1, quantity: 2 }],
    total: 100
  });
  
  // Verify database state
  const savedOrder = await db.orders.findById(order.id);
  expect(savedOrder.status).toBe('confirmed');
  
  // Verify inventory updated
  const inventory = await db.inventory.findById(1);
  expect(inventory.quantity).toBe(8); // Was 10, reserved 2
  
  // Cleanup
  await cleanupTestDatabase(db);
});
```

**RULE-004: E2E Test Patterns**
Test complete user workflows. Use real browser (Playwright, Cypress). Test happy paths and critical error scenarios.

```typescript
❌ Bad: E2E for unit-level logic
test('email validation regex works', async () => {
  await page.goto('/signup');
  await page.fill('#email', 'invalid');
  await page.click('#submit');
  expect(await page.textContent('.error')).toBe('Invalid email');
  // This should be a unit test
});

✅ Good: E2E for user workflows
test('complete signup flow', async () => {
  // Navigate
  await page.goto('/signup');
  
  // Fill form
  await page.fill('#email', 'alice@example.com');
  await page.fill('#password', 'SecurePass123!');
  await page.fill('#name', 'Alice');
  
  // Submit
  await page.click('#submit');
  
  // Verify redirect to dashboard
  await page.waitForURL('/dashboard');
  expect(await page.textContent('h1')).toBe('Welcome, Alice!');
  
  // Verify email sent (check test inbox)
  const emails = await testMailbox.getEmails('alice@example.com');
  expect(emails).toHaveLength(1);
  expect(emails[0].subject).toBe('Welcome to App!');
});
```

**RULE-005: Test-Driven Development (TDD)**
Write test first (Red), implement code (Green), refactor (Refactor). Repeat cycle. Ensures testable design.

```typescript
// 1. RED: Write failing test
test('calculateDiscount applies 10% for orders over $100', () => {
  const order = { total: 150 };
  const discount = calculateDiscount(order);
  expect(discount).toBe(15); // Test fails, function doesn't exist
});

// 2. GREEN: Implement minimal code to pass
function calculateDiscount(order) {
  if (order.total > 100) {
    return order.total * 0.1;
  }
  return 0;
}
// Test passes

// 3. REFACTOR: Improve code quality
function calculateDiscount(order: Order): number {
  const DISCOUNT_THRESHOLD = 100;
  const DISCOUNT_RATE = 0.1;
  
  return order.total > DISCOUNT_THRESHOLD 
    ? order.total * DISCOUNT_RATE 
    : 0;
}
// Test still passes, code is cleaner

// 4. Add more tests
test('calculateDiscount returns 0 for orders under $100', () => {
  expect(calculateDiscount({ total: 50 })).toBe(0);
});
```

**RULE-006: Mocking and Stubbing**
Mock external dependencies (APIs, databases). Stub time-dependent code. Use test doubles appropriately.

```typescript
❌ Bad: No mocking (slow, flaky tests)
test('fetch user data', async () => {
  const data = await fetch('https://api.example.com/users/123');
  // Real API call: slow, requires network, can fail
});

✅ Good: Mock external dependencies
test('fetch user data', async () => {
  // Mock fetch
  global.fetch = jest.fn().mockResolvedValue({
    json: async () => ({ id: 123, name: 'Alice' })
  });
  
  const data = await fetchUser(123);
  expect(data).toEqual({ id: 123, name: 'Alice' });
  expect(fetch).toHaveBeenCalledWith('https://api.example.com/users/123');
});

// Stub time-dependent code
test('isExpired returns true for old dates', () => {
  // Stub Date.now()
  jest.spyOn(Date, 'now').mockReturnValue(new Date('2024-03-26').getTime());
  
  const token = { expiresAt: new Date('2024-03-25') };
  expect(isExpired(token)).toBe(true);
  
  // Restore
  jest.restoreAllMocks();
});
```

**RULE-007: Test Coverage Strategy**
Aim for 80%+ coverage on critical paths. 100% coverage not always necessary. Focus on business logic, not boilerplate.

```typescript
❌ Bad: Test everything equally
// 100% coverage including trivial code
test('getter returns value', () => {
  const obj = { name: 'Alice' };
  expect(obj.name).toBe('Alice'); // Trivial
});

✅ Good: Focus on critical paths
// High coverage on business logic
describe('PaymentProcessor', () => {
  test('processes valid payment', async () => { /* ... */ });
  test('handles insufficient funds', async () => { /* ... */ });
  test('retries on network error', async () => { /* ... */ });
  test('prevents double charging', async () => { /* ... */ });
});

// Skip trivial getters/setters
class User {
  get name() { return this._name; } // No test needed
  
  validateEmail() { /* Complex logic - needs tests */ }
}
```

**RULE-008: Test Organization**
Group related tests. Use descriptive names. Follow naming conventions. Keep tests maintainable.

```typescript
❌ Bad: Flat, unclear tests
test('test1', () => { /* ... */ });
test('test2', () => { /* ... */ });
test('test3', () => { /* ... */ });

✅ Good: Organized, descriptive tests
describe('UserService', () => {
  describe('createUser', () => {
    test('creates user with valid data', async () => { /* ... */ });
    test('throws ValidationError for invalid email', async () => { /* ... */ });
    test('throws ConflictError for duplicate email', async () => { /* ... */ });
  });
  
  describe('updateUser', () => {
    test('updates user fields', async () => { /* ... */ });
    test('throws NotFoundError for non-existent user', async () => { /* ... */ });
    test('throws ForbiddenError when updating other user', async () => { /* ... */ });
  });
  
  describe('deleteUser', () => {
    test('soft deletes user', async () => { /* ... */ });
    test('cascades to related records', async () => { /* ... */ });
  });
});
```

---

## Quick Reference

### Test Types Comparison

| Type | Scope | Speed | Cost | When to Use |
|------|-------|-------|------|-------------|
| Unit | Single function/class | Fast (ms) | Low | Business logic, utilities |
| Integration | Multiple units | Medium (seconds) | Medium | API endpoints, database operations |
| E2E | Full application | Slow (minutes) | High | Critical user workflows |

### Testing Frameworks

```bash
# JavaScript/TypeScript
npm install --save-dev jest @testing-library/react
npm install --save-dev vitest # Faster alternative
npm install --save-dev playwright # E2E

# Python
pip install pytest pytest-cov
pip install pytest-mock # Mocking
pip install playwright # E2E
```

### AAA Pattern Template

```typescript
test('descriptive test name', async () => {
  // Arrange: Setup test data and dependencies
  const mockDep = { method: jest.fn().mockReturnValue('result') };
  const sut = new SystemUnderTest(mockDep);
  const input = { /* test data */ };
  
  // Act: Execute the code being tested
  const result = await sut.methodUnderTest(input);
  
  // Assert: Verify the outcome
  expect(result).toEqual(expectedOutput);
  expect(mockDep.method).toHaveBeenCalledWith(expectedArgs);
});
```

### Mocking Patterns

```typescript
// Mock function
const mockFn = jest.fn().mockReturnValue('result');

// Mock resolved promise
const mockAsync = jest.fn().mockResolvedValue({ data: 'result' });

// Mock rejected promise
const mockError = jest.fn().mockRejectedValue(new Error('Failed'));

// Mock implementation
const mockComplex = jest.fn().mockImplementation((x) => x * 2);

// Spy on existing method
jest.spyOn(object, 'method').mockReturnValue('result');

// Restore mocks
jest.restoreAllMocks();
```

### Coverage Commands

```bash
# Jest
npm test -- --coverage
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'

# Vitest
vitest --coverage

# Pytest
pytest --cov=src --cov-report=html
```

### Test Naming Conventions

```typescript
// Pattern: test('should [expected behavior] when [condition]')
test('should return user when valid ID provided', () => {});
test('should throw NotFoundError when user does not exist', () => {});
test('should hash password when creating user', () => {});

// Or: describe + it
describe('UserService', () => {
  it('returns user when valid ID provided', () => {});
  it('throws NotFoundError when user does not exist', () => {});
});
```

---

## Metadata

- **Related Skills:** [test-fixing.md], [tdd-workflow.md], [code-review.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
