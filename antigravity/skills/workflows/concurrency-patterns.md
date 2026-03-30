# CONCURRENCY PATTERNS - XỨ LÝ ĐỒNG THỜI AN TOÀN

> **Tier:** 2-3  
> **Tags:** `[concurrency, race-condition, locking, async, distributed]`  
> **Khi nào dùng:** Khi nhiều users/processes truy cập cùng resource, payment processing, inventory management, booking systems

---

## 📋 OVERVIEW

Race conditions xảy ra khi 2+ operations cùng đọc/ghi data, dẫn đến:
- **Double booking** (2 users book cùng 1 phòng)
- **Overselling** (bán vượt inventory)
- **Double payment** (charge 2 lần)
- **Lost updates** (update bị ghi đè)

**Thống kê:** 23% bugs production liên quan đến race conditions (Stack Overflow Survey 2023)

---

## 🎯 RACE CONDITION DETECTION CHECKLIST

### ⚠️ High-Risk Scenarios

```markdown
[ ] Payment processing (charge, refund)
[ ] Inventory management (stock decrease)
[ ] Booking systems (seats, rooms, appointments)
[ ] Counter increment (likes, views, votes)
[ ] File upload/download (concurrent writes)
[ ] Database transactions (read-modify-write)
[ ] Cache invalidation (stale data)
[ ] Session management (concurrent logins)
[ ] Rate limiting (token bucket)
[ ] Distributed locks (leader election)
```

### 🔍 Detection Questions

```
1. Có 2+ users có thể thực hiện action này cùng lúc không?
2. Action này có pattern "read → modify → write" không?
3. Có sử dụng shared state (DB, cache, file) không?
4. Có delay giữa read và write không? (network, computation)
5. Có kiểm tra "if exists" trước khi create/update không?
```

Nếu trả lời **YES** cho bất kỳ câu nào → **CẦN concurrency pattern**

---

## 🛡️ PATTERN 1: ATOMIC OPERATIONS

### Concept
Sử dụng database atomic operations (không thể bị interrupt giữa chừng)

### ❌ BAD: Race Condition

```javascript
// NGUY HIỂM: 2 users cùng book → overselling
async function bookSeat(seatId, userId) {
  const seat = await db.seats.findOne({ id: seatId });
  
  if (seat.available > 0) {  // ⚠️ Race condition here!
    // User A checks: available = 1 ✓
    // User B checks: available = 1 ✓ (cùng lúc)
    
    await db.seats.update(
      { id: seatId },
      { available: seat.available - 1 }
    );
    // Both users book → available = 0 (should be -1)
    
    await db.bookings.create({ seatId, userId });
    return { success: true };
  }
  
  return { success: false, error: 'Sold out' };
}
```

### ✅ GOOD: Atomic Decrement

```javascript
// AN TOÀN: Atomic operation
async function bookSeat(seatId, userId) {
  // Atomic decrement - DB đảm bảo không race
  const result = await db.seats.updateOne(
    { 
      id: seatId,
      available: { $gt: 0 }  // Only update if > 0
    },
    { 
      $inc: { available: -1 }  // Atomic decrement
    }
  );
  
  if (result.modifiedCount === 0) {
    return { success: false, error: 'Sold out' };
  }
  
  await db.bookings.create({ seatId, userId });
  return { success: true };
}
```

### SQL Example

```sql
-- ❌ BAD: Race condition
SELECT stock FROM products WHERE id = 123;  -- stock = 5
-- (Another user also reads stock = 5)
UPDATE products SET stock = 4 WHERE id = 123;
-- (Both users set stock = 4, should be 3)

-- ✅ GOOD: Atomic decrement
UPDATE products 
SET stock = stock - 1 
WHERE id = 123 AND stock > 0;

-- Check affected rows
IF @@ROWCOUNT = 0 THEN
  RAISE 'Out of stock';
END IF;
```

### PostgreSQL with RETURNING

```sql
-- Best: Atomic + return new value
UPDATE products 
SET stock = stock - 1 
WHERE id = 123 AND stock > 0
RETURNING stock;
-- Returns NULL if out of stock
```

---

## 🔒 PATTERN 2: OPTIMISTIC LOCKING

### Concept
Sử dụng version field để detect conflicts

### ✅ Implementation

```javascript
// Schema: Add version field
const productSchema = {
  id: Number,
  name: String,
  stock: Number,
  version: Number  // Increment on every update
};

// Update with version check
async function decreaseStock(productId, quantity) {
  const product = await db.products.findOne({ id: productId });
  
  if (product.stock < quantity) {
    throw new Error('Insufficient stock');
  }
  
  // Update only if version matches (no one else updated)
  const result = await db.products.updateOne(
    { 
      id: productId,
      version: product.version  // ⭐ Version check
    },
    { 
      $inc: { 
        stock: -quantity,
        version: 1  // Increment version
      }
    }
  );
  
  if (result.modifiedCount === 0) {
    // Someone else updated → retry
    throw new ConflictError('Product was modified, please retry');
  }
  
  return { success: true };
}
```

### With Retry Logic

```javascript
async function decreaseStockWithRetry(productId, quantity, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await decreaseStock(productId, quantity);
    } catch (error) {
      if (error instanceof ConflictError && attempt < maxRetries - 1) {
        // Exponential backoff
        await sleep(100 * Math.pow(2, attempt));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## 🔐 PATTERN 3: PESSIMISTIC LOCKING

### Concept
Lock row khi đọc, unlock khi commit/rollback

### ✅ SQL Implementation

```sql
-- PostgreSQL: SELECT FOR UPDATE
BEGIN TRANSACTION;

SELECT stock FROM products 
WHERE id = 123 
FOR UPDATE;  -- ⭐ Lock this row

-- Other transactions wait here until commit/rollback

UPDATE products 
SET stock = stock - 1 
WHERE id = 123;

COMMIT;  -- Release lock
```

### JavaScript (Sequelize)

```javascript
async function bookSeatPessimistic(seatId, userId) {
  const transaction = await db.sequelize.transaction();
  
  try {
    // Lock row
    const seat = await db.Seat.findOne({
      where: { id: seatId },
      lock: transaction.LOCK.UPDATE,  // ⭐ Pessimistic lock
      transaction
    });
    
    if (!seat || seat.available <= 0) {
      await transaction.rollback();
      return { success: false, error: 'Sold out' };
    }
    
    // Update (still locked)
    seat.available -= 1;
    await seat.save({ transaction });
    
    await db.Booking.create(
      { seatId, userId },
      { transaction }
    );
    
    await transaction.commit();  // Release lock
    return { success: true };
    
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
}
```

### ⚠️ Deadlock Prevention

```javascript
// ❌ BAD: Can cause deadlock
async function transfer(fromId, toId, amount) {
  // Transaction 1: locks A then B
  // Transaction 2: locks B then A
  // → Deadlock!
  
  await lockAccount(fromId);
  await lockAccount(toId);
}

// ✅ GOOD: Always lock in same order
async function transfer(fromId, toId, amount) {
  // Always lock smaller ID first
  const [firstId, secondId] = [fromId, toId].sort();
  
  await lockAccount(firstId);
  await lockAccount(secondId);
  
  // Now safe to transfer
}
```

---

## 🎫 PATTERN 4: IDEMPOTENCY KEYS

### Concept
Prevent duplicate operations (double payment, double booking)

### ✅ Implementation

```javascript
// Schema: Store idempotency keys
const paymentSchema = {
  id: String,
  userId: String,
  amount: Number,
  idempotencyKey: String,  // ⭐ Unique per request
  status: String,
  createdAt: Date
};

// Create unique index
db.payments.createIndex({ idempotencyKey: 1 }, { unique: true });

// Payment endpoint
async function processPayment(userId, amount, idempotencyKey) {
  // Check if already processed
  const existing = await db.payments.findOne({ idempotencyKey });
  
  if (existing) {
    // Return cached result (idempotent)
    return {
      success: true,
      paymentId: existing.id,
      cached: true
    };
  }
  
  // Process payment
  try {
    const payment = await db.payments.create({
      id: generateId(),
      userId,
      amount,
      idempotencyKey,  // ⭐ Store key
      status: 'pending'
    });
    
    // Call payment gateway
    await stripe.charges.create({ amount, currency: 'usd' });
    
    payment.status = 'completed';
    await payment.save();
    
    return { success: true, paymentId: payment.id };
    
  } catch (error) {
    if (error.code === 11000) {  // Duplicate key
      // Another request with same key succeeded
      const existing = await db.payments.findOne({ idempotencyKey });
      return { success: true, paymentId: existing.id, cached: true };
    }
    throw error;
  }
}
```

### Client-Side Key Generation

```javascript
// Frontend: Generate idempotency key
import { v4 as uuidv4 } from 'uuid';

async function handlePayment() {
  const idempotencyKey = uuidv4();  // ⭐ Generate once
  
  // Store in localStorage (survive page refresh)
  localStorage.setItem('payment_key', idempotencyKey);
  
  try {
    const result = await fetch('/api/payments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotencyKey  // ⭐ Send in header
      },
      body: JSON.stringify({ amount: 1000 })
    });
    
    if (result.ok) {
      localStorage.removeItem('payment_key');
    }
    
  } catch (error) {
    // Retry with SAME key
    console.error('Payment failed, retry with same key');
  }
}
```

---

## 🌐 PATTERN 5: DISTRIBUTED LOCKS

### Concept
Lock across multiple servers (Redis, DynamoDB)

### ✅ Redis Implementation (Redlock)

```javascript
import Redlock from 'redlock';
import Redis from 'ioredis';

const redis = new Redis();
const redlock = new Redlock([redis], {
  retryCount: 3,
  retryDelay: 200
});

async function processWithLock(resourceId, callback) {
  const lockKey = `lock:${resourceId}`;
  const ttl = 10000;  // 10 seconds
  
  let lock;
  try {
    // Acquire lock
    lock = await redlock.acquire([lockKey], ttl);
    
    // Critical section (only 1 server can execute)
    const result = await callback();
    
    return result;
    
  } finally {
    // Release lock
    if (lock) {
      await lock.release();
    }
  }
}

// Usage
await processWithLock('product:123', async () => {
  // Only 1 server processes this at a time
  const product = await db.products.findOne({ id: 123 });
  product.stock -= 1;
  await product.save();
});
```

### ⚠️ Lock Timeout Handling

```javascript
async function processWithLockSafe(resourceId, callback) {
  const lockKey = `lock:${resourceId}`;
  const ttl = 10000;
  
  let lock;
  try {
    lock = await redlock.acquire([lockKey], ttl);
    
    // Set timeout shorter than TTL
    const result = await Promise.race([
      callback(),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Operation timeout')), ttl - 1000)
      )
    ]);
    
    return result;
    
  } catch (error) {
    if (error.message === 'Operation timeout') {
      // Lock will auto-expire, don't retry
      throw new Error('Operation took too long');
    }
    throw error;
  } finally {
    if (lock) {
      try {
        await lock.release();
      } catch (err) {
        // Lock already expired, ignore
      }
    }
  }
}
```

---

## 🧪 TESTING CONCURRENT SCENARIOS

### Test 1: Simulate Race Condition

```javascript
// Test: 100 concurrent bookings for 10 seats
describe('Booking concurrency', () => {
  it('should not oversell seats', async () => {
    const seatId = 'seat-123';
    await db.seats.create({ id: seatId, available: 10 });
    
    // 100 users try to book simultaneously
    const promises = Array.from({ length: 100 }, (_, i) =>
      bookSeat(seatId, `user-${i}`)
    );
    
    const results = await Promise.allSettled(promises);
    
    const successful = results.filter(r => 
      r.status === 'fulfilled' && r.value.success
    );
    
    // Only 10 should succeed
    expect(successful.length).toBe(10);
    
    // Verify database
    const seat = await db.seats.findOne({ id: seatId });
    expect(seat.available).toBe(0);
  });
});
```

### Test 2: Idempotency

```javascript
describe('Payment idempotency', () => {
  it('should not double charge with same key', async () => {
    const key = 'payment-key-123';
    
    // Send same request 3 times
    const [result1, result2, result3] = await Promise.all([
      processPayment('user-1', 1000, key),
      processPayment('user-1', 1000, key),
      processPayment('user-1', 1000, key)
    ]);
    
    // All return same payment ID
    expect(result1.paymentId).toBe(result2.paymentId);
    expect(result2.paymentId).toBe(result3.paymentId);
    
    // Only 1 payment in database
    const payments = await db.payments.find({ idempotencyKey: key });
    expect(payments.length).toBe(1);
  });
});
```

---

## 📊 QUICK REFERENCE

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| **Atomic Operations** | Simple counters, stock | Fast, no locks | Limited operations |
| **Optimistic Locking** | Low contention | No blocking | Retry needed |
| **Pessimistic Locking** | High contention | Guaranteed | Can deadlock |
| **Idempotency Keys** | Payments, bookings | Prevent duplicates | Extra storage |
| **Distributed Locks** | Multi-server | Works across servers | Complex, can fail |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Check-Then-Act

```javascript
// ❌ BAD
if (await isAvailable(seatId)) {
  await book(seatId);  // Race condition!
}

// ✅ GOOD
const result = await bookAtomic(seatId);
if (!result.success) {
  throw new Error('Not available');
}
```

### ❌ Mistake 2: Long Transactions

```javascript
// ❌ BAD: Lock held too long
BEGIN TRANSACTION;
SELECT * FROM products WHERE id = 123 FOR UPDATE;
-- Call external API (5 seconds)
await stripe.charge(...);
UPDATE products SET stock = stock - 1;
COMMIT;

// ✅ GOOD: Minimize lock time
const product = await db.products.findOne({ id: 123 });
await stripe.charge(...);  // Outside transaction

BEGIN TRANSACTION;
UPDATE products SET stock = stock - 1 WHERE id = 123 AND stock > 0;
COMMIT;
```

### ❌ Mistake 3: Ignoring Retry

```javascript
// ❌ BAD: Give up on first conflict
try {
  await updateWithOptimisticLock(id);
} catch (error) {
  throw error;  // User sees error
}

// ✅ GOOD: Retry with backoff
await retryWithBackoff(() => updateWithOptimisticLock(id), 3);
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Implement booking system with concurrency safety:
- 100 seats available
- Prevent overselling (race condition)
- Use atomic operations or optimistic locking
- Include tests for 1000 concurrent requests
- Handle edge cases: timeout, retry, deadlock"
```

### AI Should

1. ✅ Ask about expected concurrency level
2. ✅ Choose appropriate pattern (atomic vs locking)
3. ✅ Add version field for optimistic locking
4. ✅ Include retry logic with exponential backoff
5. ✅ Write concurrent tests
6. ✅ Handle deadlock prevention

---

## 🔗 RELATED SKILLS

- `error-handling-patterns.md` - Handle lock timeout, conflicts
- `edge-case-catalog.md` - Concurrent edge cases
- `database-standards.md` - Transaction isolation levels

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium-High  
**Impact:** Critical (prevents data corruption)
