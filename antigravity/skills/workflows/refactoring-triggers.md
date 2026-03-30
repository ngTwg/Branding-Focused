# REFACTORING TRIGGERS - KHI NÀO CẦN REFACTOR

> **Tier:** 1-4 (All projects)  
> **Tags:** `[refactoring, code-quality, maintainability, technical-debt]`  
> **Khi nào dùng:** Code review, maintenance, before adding features

---

## 🎯 OVERVIEW

AI code thiếu module hóa và tái sử dụng. Code "brute-force", không tối ưu gốc rễ, vi phạm DRY principle. Không biết KHI NÀO cần refactor dẫn đến technical debt tích lũy.

**Mục tiêu:** 
- Identify refactoring opportunities early
- Prevent technical debt accumulation
- Maintain code quality over time

---

## 🚨 REFACTORING TRIGGERS

### TRIGGER 1: RULE OF THREE (Copy-Paste 3 lần)

#### Rule
```
Khi copy-paste code lần thứ 3 → REFACTOR ngay lập tức
```

#### ❌ BAD - Repeated code
```typescript
function getUserEmail(userId: string) {
  const user = await db.users.findOne({ id: userId });
  if (!user) throw new Error('User not found');
  return user.email;
}

function getUserName(userId: string) {
  const user = await db.users.findOne({ id: userId });
  if (!user) throw new Error('User not found');
  return user.name;
}

function getUserAge(userId: string) {
  const user = await db.users.findOne({ id: userId });
  if (!user) throw new Error('User not found');
  return user.age;
}
```

#### ✅ GOOD - Extracted common logic
```typescript
async function getUser(userId: string): Promise<User> {
  const user = await db.users.findOne({ id: userId });
  if (!user) throw new NotFoundError('User', userId);
  return user;
}

async function getUserEmail(userId: string) {
  const user = await getUser(userId);
  return user.email;
}

async function getUserName(userId: string) {
  const user = await getUser(userId);
  return user.name;
}

async function getUserAge(userId: string) {
  const user = await getUser(userId);
  return user.age;
}
```

---

### TRIGGER 2: FUNCTION > 50 LINES

#### Rule
```
Nếu function > 50 lines → Chia nhỏ thành sub-functions
```

#### ❌ BAD - 80 line function
```typescript
async function processOrder(orderId: string) {
  // Lines 1-10: Fetch order
  const order = await db.orders.findOne({ id: orderId });
  if (!order) throw new Error('Order not found');
  
  // Lines 11-20: Validate order
  if (order.status !== 'pending') {
    throw new Error('Order already processed');
  }
  if (order.items.length === 0) {
    throw new Error('Order has no items');
  }
  
  // Lines 21-40: Check inventory
  for (const item of order.items) {
    const product = await db.products.findOne({ id: item.productId });
    if (!product) {
      throw new Error(`Product ${item.productId} not found`);
    }
    if (product.stock < item.quantity) {
      throw new Error(`Insufficient stock for ${product.name}`);
    }
  }
  
  // Lines 41-60: Process payment
  const paymentResult = await stripe.charges.create({
    amount: order.total * 100,
    currency: 'usd',
    source: order.paymentToken,
  });
  
  if (paymentResult.status !== 'succeeded') {
    throw new Error('Payment failed');
  }
  
  // Lines 61-80: Update inventory and order
  for (const item of order.items) {
    await db.products.updateOne(
      { id: item.productId },
      { $inc: { stock: -item.quantity } }
    );
  }
  
  await db.orders.updateOne(
    { id: orderId },
    { status: 'completed', paidAt: new Date() }
  );
  
  await sendOrderConfirmation(order);
  
  return order;
}
```

#### ✅ GOOD - Split into focused functions
```typescript
async function processOrder(orderId: string) {
  const order = await fetchAndValidateOrder(orderId);
  await checkInventory(order);
  await processPayment(order);
  await updateInventoryAndOrder(order);
  await sendOrderConfirmation(order);
  return order;
}

async function fetchAndValidateOrder(orderId: string) {
  const order = await db.orders.findOne({ id: orderId });
  if (!order) throw new NotFoundError('Order', orderId);
  
  if (order.status !== 'pending') {
    throw new BusinessError('Order already processed');
  }
  if (order.items.length === 0) {
    throw new ValidationError('Order has no items');
  }
  
  return order;
}

async function checkInventory(order: Order) {
  for (const item of order.items) {
    const product = await db.products.findOne({ id: item.productId });
    if (!product) {
      throw new NotFoundError('Product', item.productId);
    }
    if (product.stock < item.quantity) {
      throw new InsufficientStockError(product.name);
    }
  }
}

async function processPayment(order: Order) {
  const result = await stripe.charges.create({
    amount: order.total * 100,
    currency: 'usd',
    source: order.paymentToken,
  });
  
  if (result.status !== 'succeeded') {
    throw new PaymentFailedError();
  }
}

async function updateInventoryAndOrder(order: Order) {
  await db.transaction(async (tx) => {
    for (const item of order.items) {
      await tx.products.updateOne(
        { id: item.productId },
        { $inc: { stock: -item.quantity } }
      );
    }
    
    await tx.orders.updateOne(
      { id: order.id },
      { status: 'completed', paidAt: new Date() }
    );
  });
}
```

**Benefits:**
- Each function has single responsibility
- Easy to test individually
- Easy to understand
- Easy to modify

---

### TRIGGER 3: FILE > 300 LINES

#### Rule
```
Nếu file > 300 lines → Chia thành multiple files
```

#### ❌ BAD - 500 line file
```typescript
// user-service.ts (500 lines)
class UserService {
  async createUser() { /* 50 lines */ }
  async updateUser() { /* 50 lines */ }
  async deleteUser() { /* 50 lines */ }
  async getUserOrders() { /* 50 lines */ }
  async getUserPayments() { /* 50 lines */ }
  async getUserAddresses() { /* 50 lines */ }
  async sendWelcomeEmail() { /* 50 lines */ }
  async sendPasswordReset() { /* 50 lines */ }
  async validateEmail() { /* 50 lines */ }
  async hashPassword() { /* 50 lines */ }
}
```

#### ✅ GOOD - Split by responsibility
```typescript
// user-service.ts (100 lines)
class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService,
    private authService: AuthService
  ) {}
  
  async createUser() { /* ... */ }
  async updateUser() { /* ... */ }
  async deleteUser() { /* ... */ }
}

// user-repository.ts (100 lines)
class UserRepository {
  async findById() { /* ... */ }
  async findByEmail() { /* ... */ }
  async create() { /* ... */ }
  async update() { /* ... */ }
  async delete() { /* ... */ }
}

// email-service.ts (100 lines)
class EmailService {
  async sendWelcomeEmail() { /* ... */ }
  async sendPasswordReset() { /* ... */ }
  async sendOrderConfirmation() { /* ... */ }
}

// auth-service.ts (100 lines)
class AuthService {
  async validateEmail() { /* ... */ }
  async hashPassword() { /* ... */ }
  async verifyPassword() { /* ... */ }
  async generateToken() { /* ... */ }
}
```

---

### TRIGGER 4: CYCLOMATIC COMPLEXITY > 10

#### Rule
```
Nếu có > 10 if/else/switch → Refactor thành strategy pattern
```

#### Measuring Complexity
```typescript
// Cyclomatic Complexity = 1 + number of decision points
function example() {  // +1
  if (a) {            // +1
    if (b) {          // +1
      // ...
    } else {          // +1
      // ...
    }
  } else if (c) {     // +1
    // ...
  }
  
  switch (d) {
    case 1:           // +1
    case 2:           // +1
    case 3:           // +1
  }
  
  return a && b || c; // +2
}
// Total: 11 (TOO COMPLEX!)
```

#### ❌ BAD - High complexity
```typescript
function calculateShipping(order: Order): number {
  let cost = 0;
  
  if (order.country === 'US') {
    if (order.state === 'CA') {
      if (order.weight < 5) {
        cost = 10;
      } else if (order.weight < 10) {
        cost = 15;
      } else {
        cost = 20;
      }
    } else if (order.state === 'NY') {
      if (order.weight < 5) {
        cost = 12;
      } else if (order.weight < 10) {
        cost = 18;
      } else {
        cost = 25;
      }
    } else {
      cost = 15;
    }
  } else if (order.country === 'CA') {
    cost = 20;
  } else if (order.country === 'UK') {
    cost = 25;
  } else {
    cost = 30;
  }
  
  if (order.express) {
    cost *= 2;
  }
  
  if (order.total > 100) {
    cost = 0;  // Free shipping
  }
  
  return cost;
}
```

#### ✅ GOOD - Strategy pattern
```typescript
interface ShippingStrategy {
  calculate(order: Order): number;
}

class USShippingStrategy implements ShippingStrategy {
  private stateRates = {
    CA: { light: 10, medium: 15, heavy: 20 },
    NY: { light: 12, medium: 18, heavy: 25 },
    default: { light: 15, medium: 15, heavy: 15 },
  };
  
  calculate(order: Order): number {
    const rates = this.stateRates[order.state] || this.stateRates.default;
    
    if (order.weight < 5) return rates.light;
    if (order.weight < 10) return rates.medium;
    return rates.heavy;
  }
}

class InternationalShippingStrategy implements ShippingStrategy {
  private countryRates = {
    CA: 20,
    UK: 25,
    default: 30,
  };
  
  calculate(order: Order): number {
    return this.countryRates[order.country] || this.countryRates.default;
  }
}

class ShippingCalculator {
  private strategies: Map<string, ShippingStrategy> = new Map([
    ['US', new USShippingStrategy()],
    ['CA', new InternationalShippingStrategy()],
    ['UK', new InternationalShippingStrategy()],
  ]);
  
  calculate(order: Order): number {
    const strategy = this.strategies.get(order.country) 
      || new InternationalShippingStrategy();
    
    let cost = strategy.calculate(order);
    
    if (order.express) cost *= 2;
    if (order.total > 100) cost = 0;
    
    return cost;
  }
}
```

---

### TRIGGER 5: NESTED DEPTH > 3

#### Rule
```
Nếu nested if/for > 3 levels → Extract functions
```

#### ❌ BAD - Deep nesting
```typescript
function processOrders(orders: Order[]) {
  for (const order of orders) {                    // Level 1
    if (order.status === 'pending') {              // Level 2
      if (order.items.length > 0) {                // Level 3
        for (const item of order.items) {          // Level 4
          if (item.inStock) {                      // Level 5
            // Process item (TOO DEEP!)
          }
        }
      }
    }
  }
}
```

#### ✅ GOOD - Extracted functions
```typescript
function processOrders(orders: Order[]) {
  const pendingOrders = orders.filter(o => o.status === 'pending');
  pendingOrders.forEach(processPendingOrder);
}

function processPendingOrder(order: Order) {
  const validItems = order.items.filter(item => item.inStock);
  validItems.forEach(processItem);
}

function processItem(item: Item) {
  // Process item (flat, easy to read)
}
```

---

### TRIGGER 6: CODE SMELLS

#### Smell 1: Long Parameter List (> 3 params)
```typescript
❌ BAD
function createUser(
  email: string,
  password: string,
  firstName: string,
  lastName: string,
  age: number,
  country: string,
  city: string,
  zipCode: string
) { /* ... */ }

✅ GOOD - Use object
function createUser(data: CreateUserData) { /* ... */ }

interface CreateUserData {
  email: string;
  password: string;
  profile: {
    firstName: string;
    lastName: string;
    age: number;
  };
  address: {
    country: string;
    city: string;
    zipCode: string;
  };
}
```

#### Smell 2: Magic Numbers
```typescript
❌ BAD
if (user.age > 18) { /* ... */ }
setTimeout(callback, 5000);
const tax = price * 0.08;

✅ GOOD - Named constants
const LEGAL_AGE = 18;
const RETRY_DELAY_MS = 5000;
const TAX_RATE = 0.08;

if (user.age > LEGAL_AGE) { /* ... */ }
setTimeout(callback, RETRY_DELAY_MS);
const tax = price * TAX_RATE;
```

#### Smell 3: Comments Explaining Code
```typescript
❌ BAD
// Check if user is admin and has permission
if (user.role === 'admin' && user.permissions.includes('delete')) {
  // ...
}

✅ GOOD - Self-documenting code
function canDeleteUser(user: User): boolean {
  return user.role === 'admin' && user.permissions.includes('delete');
}

if (canDeleteUser(user)) {
  // ...
}
```

#### Smell 4: Feature Envy
```typescript
❌ BAD - Method uses another object's data too much
class Order {
  calculateTotal(user: User) {
    let total = this.subtotal;
    
    // Using user data extensively
    if (user.isPremium) {
      total *= 0.9;
    }
    if (user.loyaltyPoints > 1000) {
      total -= 10;
    }
    if (user.country === 'US') {
      total *= 1.08;  // Tax
    }
    
    return total;
  }
}

✅ GOOD - Move logic to User class
class Order {
  calculateTotal(user: User) {
    const discount = user.getDiscount();
    const tax = user.getTaxRate();
    return (this.subtotal - discount) * (1 + tax);
  }
}

class User {
  getDiscount(): number {
    let discount = 0;
    if (this.isPremium) discount += this.subtotal * 0.1;
    if (this.loyaltyPoints > 1000) discount += 10;
    return discount;
  }
  
  getTaxRate(): number {
    return this.country === 'US' ? 0.08 : 0;
  }
}
```

---

## 🔍 DETECTION TOOLS

### ESLint Rules
```json
{
  "rules": {
    "complexity": ["error", 10],
    "max-depth": ["error", 3],
    "max-lines": ["error", 300],
    "max-lines-per-function": ["error", 50],
    "max-params": ["error", 3],
    "max-nested-callbacks": ["error", 3]
  }
}
```

### SonarQube Metrics
- Cyclomatic Complexity
- Cognitive Complexity
- Code Duplication
- Code Smells
- Technical Debt Ratio

### Manual Code Review Checklist
- [ ] Any function > 50 lines?
- [ ] Any file > 300 lines?
- [ ] Any function with > 3 parameters?
- [ ] Any nested depth > 3?
- [ ] Any duplicated code (Rule of Three)?
- [ ] Any magic numbers?
- [ ] Any complex conditionals?

---

## ✅ REFACTORING CHECKLIST

### Before Refactoring
- [ ] Understand current code behavior
- [ ] Have tests in place (or write them)
- [ ] Identify refactoring trigger
- [ ] Plan refactoring approach
- [ ] Commit current working state

### During Refactoring
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Commit after each successful step
- [ ] Don't add features while refactoring

### After Refactoring
- [ ] All tests pass
- [ ] Code is more readable
- [ ] Code is more maintainable
- [ ] No functionality changed
- [ ] Update documentation if needed

---

## 🚨 WHEN NOT TO REFACTOR

### Don't Refactor If:
1. **No tests** - Write tests first
2. **Deadline pressure** - Schedule for later
3. **Code works and won't change** - Leave it
4. **Rewrite is better** - Consider full rewrite
5. **Not your code and no bugs** - Don't touch

### Refactor Later If:
- In middle of feature development
- Close to release
- No time for proper testing
- Code is legacy and fragile

---

## 🎯 AI LEVERAGE

### Refactoring Detection Prompt
```markdown
Analyze this code for refactoring opportunities:

[CODE]

Check for:
1. Functions > 50 lines
2. Files > 300 lines
3. Cyclomatic complexity > 10
4. Nested depth > 3
5. Duplicated code (Rule of Three)
6. Code smells (magic numbers, long params, etc.)

Suggest specific refactorings with examples.
```

### Refactoring Execution Prompt
```markdown
Refactor this code:

[CODE]

Apply:
1. Extract functions for repeated code
2. Reduce complexity with strategy pattern
3. Flatten nested conditionals
4. Replace magic numbers with constants
5. Improve naming

Maintain exact same functionality. Provide tests.
```

---

## 📚 QUICK REFERENCE

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Rule of Three | 3 copies | Extract function |
| Function Length | > 50 lines | Split function |
| File Length | > 300 lines | Split file |
| Complexity | > 10 | Strategy pattern |
| Nesting | > 3 levels | Extract functions |
| Parameters | > 3 params | Use object |

---

## 🔗 RELATED SKILLS

- `workflows/code-review.md` - Review for refactoring needs
- `workflows/testing-strategies.md` - Test before refactoring
- `workflows/naming-conventions.md` - Improve naming during refactor

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ RECOMMENDED - Refactor regularly to prevent technical debt
