# EDGE CASE CATALOG - DANH MỤC TRƯỜNG HỢP BIÊN

> **Tier:** 1-4 (All projects)  
> **Tags:** `[edge-cases, testing, validation, robustness]`  
> **Khi nào dùng:** TRƯỚC KHI viết code, TRƯỚC KHI test

---

## 🎯 OVERVIEW

AI bỏ sót edge cases gấp 75% so với code người. AI code cho happy path, quên các trường hợp: input rỗng, số âm, số 0, Unicode, timezone, concurrent access.

**Mục tiêu:** 
- Zero crashes từ edge cases
- Comprehensive test coverage
- Defensive programming mindset

---

## 📋 UNIVERSAL EDGE CASES (Mọi domain)

### 1. NULL & UNDEFINED
```typescript
✅ Test cases:
- null
- undefined
- empty object {}
- empty array []
```

### 2. EMPTY VALUES
```typescript
✅ Test cases:
- Empty string ""
- Whitespace only "   "
- Single space " "
- Tab/newline "\t\n"
```

### 3. NUMERIC EDGE CASES
```typescript
✅ Test cases:
- Zero: 0
- Negative: -1, -999
- Very large: Number.MAX_SAFE_INTEGER
- Very small: Number.MIN_SAFE_INTEGER
- Decimal: 0.1 + 0.2 !== 0.3
- Infinity: Infinity, -Infinity
- NaN: NaN
```

### 4. STRING EDGE CASES
```typescript
✅ Test cases:
- Very long: 10,000+ characters
- Unicode: "你好", "مرحبا", "🎉"
- Emoji: "👨‍👩‍👧‍👦" (family emoji - 1 char but 11 bytes)
- Special chars: <script>, ', ", \, NULL byte
- SQL injection: "'; DROP TABLE users--"
- XSS: "<script>alert('xss')</script>"
```

### 5. ARRAY EDGE CASES
```typescript
✅ Test cases:
- Empty array: []
- Single element: [1]
- Duplicates: [1, 1, 1]
- Very large: 100,000+ elements
- Mixed types: [1, "two", null, {}]
```

### 6. DATE/TIME EDGE CASES
```typescript
✅ Test cases:
- Leap year: Feb 29, 2024
- DST transition: March 10, 2024 2:00 AM
- Timezone: UTC, UTC+14, UTC-12
- Unix epoch: Jan 1, 1970
- Year 2038 problem: Jan 19, 2038
- Invalid dates: Feb 30, Month 13
```

---

## 🔐 AUTHENTICATION EDGE CASES

### Email Validation
```typescript
✅ Test cases:
// Valid
- "user@example.com"
- "user+tag@example.com"
- "user.name@example.co.uk"
- "123@example.com"

// Invalid
- ""  // Empty
- "user"  // No @
- "@example.com"  // No local part
- "user@"  // No domain
- "user @example.com"  // Space
- "user@example"  // No TLD
- "user@.com"  // No domain name
- "user..name@example.com"  // Double dot
- "user@example..com"  // Double dot in domain

// Edge cases
- "a@b.c"  // Minimum valid
- "user@subdomain.example.com"  // Subdomain
- "user@192.168.1.1"  // IP address (valid but unusual)
- "user@[IPv6:2001:db8::1]"  // IPv6
- "very.long.email.address.with.many.dots@very.long.domain.name.example.com"  // Long
```

### Password Validation
```typescript
✅ Test cases:
// Strength
- ""  // Empty
- "a"  // Too short
- "password"  // Common password
- "12345678"  // Only numbers
- "abcdefgh"  // Only lowercase
- "ABCDEFGH"  // Only uppercase
- "Abcd1234"  // Good
- "Abcd1234!@#"  // Strong

// Special cases
- "Pass word1!"  // Space
- "Пароль123!"  // Unicode
- "🔒🔑🔐123"  // Emoji
- "A".repeat(1000)  // Very long
```

### Login Attempts
```typescript
✅ Test cases:
- First attempt (success)
- 5 failed attempts (lock account)
- Attempt after lock (reject)
- Attempt from different IP (allow/block?)
- Concurrent login attempts (race condition)
- Login with expired session
- Login with revoked token
```

---

## 🛒 E-COMMERCE EDGE CASES

### Product Quantity
```typescript
✅ Test cases:
- 0 quantity (should reject)
- Negative quantity (should reject)
- 1 quantity (minimum)
- 999 quantity (bulk order)
- Quantity > stock (should reject)
- Decimal quantity: 1.5 (depends on product)
- Very large: 1,000,000 (DoS risk)
```

### Pricing
```typescript
✅ Test cases:
- $0.00 (free item)
- $0.01 (minimum)
- $999,999.99 (very expensive)
- Negative price (should reject)
- Price with many decimals: $10.999 (round to $11.00)
- Currency conversion rounding
- Tax calculation rounding
```

### Discount Codes
```typescript
✅ Test cases:
- Valid code
- Expired code
- Not yet active code
- Already used code (single-use)
- Code used max times
- Code for different product
- Code for minimum order not met
- Multiple codes (allow/reject?)
- 100% discount code
- Discount > order total
```

### Checkout
```typescript
✅ Test cases:
- Empty cart
- Item removed from cart during checkout
- Item out of stock during checkout
- Price changed during checkout
- Payment declined
- Payment timeout
- Duplicate order submission (double-click)
- Concurrent checkout (last item)
```

---

## 📝 FORM VALIDATION EDGE CASES

### Name Fields
```typescript
✅ Test cases:
- ""  // Empty
- "A"  // Single character
- "John Doe"  // Normal
- "Mary-Jane"  // Hyphen
- "O'Brien"  // Apostrophe
- "José"  // Accent
- "李明"  // Chinese
- "محمد"  // Arabic
- "Nguyễn Văn A"  // Vietnamese
- "X Æ A-12"  // Elon's kid
- "A".repeat(1000)  // Very long
```

### Phone Numbers
```typescript
✅ Test cases:
- ""  // Empty
- "1234567890"  // 10 digits
- "+1 (555) 123-4567"  // Formatted
- "+44 20 7946 0958"  // UK
- "+86 138 0000 0000"  // China
- "123"  // Too short
- "12345678901234567890"  // Too long
- "abc-def-ghij"  // Letters
- "+1 555 123 4567 ext 123"  // Extension
```

### Address
```typescript
✅ Test cases:
- PO Box: "PO Box 123"
- Apartment: "123 Main St Apt 4B"
- No street number: "Main Street"
- Very long: "123 Very Long Street Name..."
- Special chars: "123 O'Malley St."
- International: "東京都渋谷区..."
- Zip code: "12345", "12345-6789", "SW1A 1AA" (UK)
```

### File Upload
```typescript
✅ Test cases:
- No file selected
- Empty file (0 bytes)
- Very large file (> limit)
- Wrong file type (.exe instead of .jpg)
- Corrupted file
- File with no extension
- File with double extension: image.jpg.exe
- File with Unicode name: "文件.jpg"
- File with special chars: "file<>|.jpg"
- Multiple files (if allowed)
- Duplicate filename
```

---

## 📅 DATE/TIME EDGE CASES

### Date Picker
```typescript
✅ Test cases:
- Today
- Yesterday
- Tomorrow
- 100 years ago
- 100 years future
- Feb 29 (leap year)
- Feb 29 (non-leap year) - should reject
- Invalid: Feb 30, Month 13, Day 32
- Timezone: User in UTC+8 books for UTC-5
- DST: March 10, 2024 2:30 AM (doesn't exist)
```

### Age Calculation
```typescript
✅ Test cases:
- Born today (age 0)
- Born yesterday (age 0)
- Born 1 year ago today (age 1)
- Born 1 year ago yesterday (age 1)
- Born 1 year ago tomorrow (age 0)
- Born Feb 29 (leap year baby)
- Born in future (should reject)
- Born 150 years ago (should reject)
```

### Booking/Reservation
```typescript
✅ Test cases:
- Start = End (0 duration)
- Start > End (invalid)
- Start in past (should reject)
- Overlapping bookings
- Back-to-back bookings
- Booking during maintenance window
- Booking on holiday
- Booking across DST transition
- Booking across midnight
- Booking across year boundary
```

---

## 🔢 NUMERIC CALCULATION EDGE CASES

### Division
```typescript
✅ Test cases:
- 10 / 2 = 5  // Normal
- 10 / 3 = 3.333...  // Repeating decimal
- 1 / 0 = Infinity  // Division by zero
- 0 / 0 = NaN  // Undefined
- -10 / 2 = -5  // Negative
```

### Percentage
```typescript
✅ Test cases:
- 0% of 100 = 0
- 100% of 100 = 100
- 50% of 100 = 50
- 33.33% of 100 = 33.33
- 150% of 100 = 150 (over 100%)
- -10% of 100 = -10 (negative %)
- 10% of 0 = 0
```

### Currency
```typescript
✅ Test cases:
- $0.01 + $0.02 = $0.03  // Rounding
- $0.10 * 3 = $0.30  // Floating point
- $10.00 / 3 = $3.33 (not $3.333...)
- $100.00 - $99.99 = $0.01
- $999,999.99 + $0.01 = $1,000,000.00
```

---

## 🔄 CONCURRENCY EDGE CASES

### Race Conditions
```typescript
✅ Test cases:
- 2 users buy last item simultaneously
- 2 users update same record simultaneously
- User deletes while another reads
- User logs out while request in flight
- Cache invalidation during read
- Database connection pool exhausted
```

### Idempotency
```typescript
✅ Test cases:
- Submit form twice (double-click)
- Retry failed request (network error)
- Webhook delivered twice
- Payment processed twice
- Email sent twice
```

---

## 🌐 INTERNATIONALIZATION EDGE CASES

### Language
```typescript
✅ Test cases:
- English (LTR)
- Arabic (RTL)
- Chinese (no spaces)
- German (long compound words)
- Thai (no word boundaries)
- Emoji in text
```

### Currency
```typescript
✅ Test cases:
- USD: $1,234.56
- EUR: 1.234,56 €
- JPY: ¥1,234 (no decimals)
- BTC: ₿0.00012345 (8 decimals)
```

### Number Format
```typescript
✅ Test cases:
- US: 1,234.56
- EU: 1.234,56
- India: 1,23,456.78
```

---

## 🔍 SEARCH EDGE CASES

### Search Query
```typescript
✅ Test cases:
- ""  // Empty
- " "  // Space only
- "a"  // Single char
- "the"  // Common word
- "iPhone"  // Case sensitivity
- "iphone"
- "IPHONE"
- "i phone"  // Space
- "i-phone"  // Hyphen
- "i_phone"  // Underscore
- "🔍"  // Emoji
- "SELECT * FROM"  // SQL
- "<script>"  // XSS
- "A".repeat(1000)  // Very long
```

### Search Results
```typescript
✅ Test cases:
- 0 results
- 1 result
- 1000+ results (pagination)
- Exact match
- Partial match
- Fuzzy match
- Results deleted during pagination
```

---

## 📊 PAGINATION EDGE CASES

```typescript
✅ Test cases:
- Page 1 (first page)
- Last page
- Page 0 (should reject or redirect to 1)
- Page -1 (should reject)
- Page 999999 (beyond last page)
- Page size: 0, -1, 1, 100, 10000
- Total items: 0, 1, 99, 100, 101
- Items deleted during pagination
```

---

## 🎯 TESTING CHECKLIST

### Before Writing Code
- [ ] List all possible inputs
- [ ] Identify edge cases for each input
- [ ] Consider null/empty/zero
- [ ] Consider very large/very small
- [ ] Consider invalid/malicious input
- [ ] Consider concurrent access

### Before Claiming "Done"
- [ ] Test with empty input
- [ ] Test with null/undefined
- [ ] Test with very large input
- [ ] Test with invalid input
- [ ] Test with Unicode/emoji
- [ ] Test concurrent operations
- [ ] Test error cases

---

## 🚨 COMMON MISTAKES

### Mistake 1: Only testing happy path
```typescript
❌ BAD
function divide(a: number, b: number) {
  return a / b;  // Only tested with divide(10, 2)
}

✅ GOOD - Test edge cases
divide(10, 2);   // 5
divide(10, 3);   // 3.333...
divide(10, 0);   // Infinity - handle this!
divide(0, 0);    // NaN - handle this!
```

### Mistake 2: Assuming input is valid
```typescript
❌ BAD
function getUser(id: string) {
  return db.users.findOne({ id });  // What if id is ""?
}

✅ GOOD
function getUser(id: string) {
  if (!id || id.trim() === '') {
    throw new ValidationError('User ID is required');
  }
  return db.users.findOne({ id });
}
```

---

## 🎯 AI LEVERAGE

### Edge Case Generation Prompt
```markdown
Generate comprehensive edge cases for this function:

[FUNCTION CODE]

Include:
1. Null/undefined/empty inputs
2. Boundary values (min/max)
3. Invalid inputs
4. Very large inputs
5. Unicode/special characters
6. Concurrent access scenarios
7. Error conditions

Format as test cases.
```

---

## 📚 QUICK REFERENCE

| Category | Key Edge Cases |
|----------|----------------|
| Null | null, undefined, {}, [] |
| Empty | "", " ", "\t\n" |
| Numeric | 0, -1, Infinity, NaN |
| String | Very long, Unicode, SQL/XSS |
| Array | [], [1], duplicates |
| Date | Leap year, DST, timezone |
| Concurrent | Race conditions, double-submit |

---

## 🔗 RELATED SKILLS

- `workflows/error-handling-patterns.md` - Handle edge case errors
- `workflows/testing-strategies.md` - Test edge cases
- `workflows/anti-hallucination-v2.md` - Verify edge case handling

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ MANDATORY - Test all edge cases before claiming done
