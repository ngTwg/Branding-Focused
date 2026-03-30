# ERROR HANDLING PATTERNS - XỬ LÝ LỖI CHUẨN

> **Tier:** 1-4 (All projects)  
> **Tags:** `[error-handling, exceptions, try-catch, robustness]`  
> **Khi nào dùng:** Mọi function có thể fail, mọi external call

---

## 🎯 OVERVIEW

AI thường bỏ qua null check, exception handling, và guard clauses (thiếu gấp đôi so với code người). Điều này dẫn đến crashes không mong muốn và bugs khó debug.

**Mục tiêu:** 
- Zero unhandled exceptions
- Graceful degradation
- Clear error messages
- Proper error logging

---

## 🔴 VẤN ĐỀ THƯỜNG GẶP

### ❌ AI hay sinh code như thế này:
```typescript
// Không có null check
function getUserEmail(user: User) {
  return user.profile.email;  // Crash if user.profile is null
}

// Exception quá rộng
try {
  processPayment(order);
} catch (error) {
  // Nuốt hết mọi lỗi, không xử lý gì
}

// Không có error handling
const data = await fetch(url).then(r => r.json());
// Crash if network fails
```

---

## 📋 ERROR HANDLING PATTERNS

### PATTERN 1: EARLY RETURN (Guard Clauses)

#### Concept
Kiểm tra điều kiện lỗi TRƯỚC, return sớm. Tránh nested if-else.

#### ❌ BAD - Nested ifs
```typescript
function processUser(user: User | null) {
  if (user) {
    if (user.email) {
      if (user.isActive) {
        if (user.hasPermission) {
          // Main logic buried deep
          return doSomething(user);
        }
      }
    }
  }
  return null;
}
```

#### ✅ GOOD - Early returns
```typescript
function processUser(user: User | null): Result | null {
  // Guard clauses at top
  if (!user) return null;
  if (!user.email) return null;
  if (!user.isActive) return null;
  if (!user.hasPermission) return null;
  
  // Main logic clear and flat
  return doSomething(user);
}
```

#### Benefits:
- Flat code structure (no nesting)
- Clear error conditions
- Main logic easy to find
- Easy to add new checks

---

### PATTERN 2: RESULT TYPE (No Exceptions)

#### Concept
Return success/failure object thay vì throw exception. Functional programming style.

#### ❌ BAD - Exceptions for control flow
```typescript
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// Caller must remember to catch
try {
  const result = divide(10, 0);
} catch (error) {
  console.error(error);
}
```

#### ✅ GOOD - Result type
```typescript
type Result<T, E> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) {
    return { ok: false, error: "Division by zero" };
  }
  return { ok: true, value: a / b };
}

// Caller forced to handle both cases
const result = divide(10, 2);
if (result.ok) {
  console.log("Result:", result.value);
} else {
  console.error("Error:", result.error);
}
```

#### Benefits:
- Explicit error handling (compiler enforced)
- No hidden control flow
- Type-safe errors
- Composable (can chain results)

#### Library: Use `neverthrow` for TypeScript
```typescript
import { Result, ok, err } from 'neverthrow';

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) {
    return err("Division by zero");
  }
  return ok(a / b);
}

// Chain operations
const result = divide(10, 2)
  .map(x => x * 2)
  .map(x => x + 1);
```

---

### PATTERN 3: CENTRALIZED ERROR HANDLER

#### Concept
Một nơi duy nhất xử lý tất cả errors. Consistent error format.

#### ❌ BAD - Error handling rải rác
```typescript
app.get('/users/:id', async (req, res) => {
  try {
    const user = await getUser(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/orders', async (req, res) => {
  try {
    const order = await createOrder(req.body);
    res.json(order);
  } catch (error) {
    // Different error format!
    res.status(500).send(error.toString());
  }
});
```

#### ✅ GOOD - Centralized handler
```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500,
    public details?: unknown
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super('NOT_FOUND', `${resource} with ID '${id}' not found`, 404);
  }
}

class ValidationError extends AppError {
  constructor(message: string, details: unknown) {
    super('VALIDATION_ERROR', message, 400, details);
  }
}

// Centralized error middleware (Express)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // Log error
  logger.error('Request error', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  // Handle known errors
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      },
    });
  }

  // Handle unknown errors (don't expose internals)
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
});

// Routes just throw errors
app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }
  res.json(user);
});
```

#### Benefits:
- Consistent error format
- Single place to log errors
- Don't expose internal errors
- Easy to add error tracking (Sentry)

---

### PATTERN 4: ERROR BOUNDARIES (React)

#### Concept
Catch React component errors, show fallback UI.

#### ❌ BAD - No error boundary
```typescript
function App() {
  return (
    <div>
      <UserProfile />  {/* If this crashes, whole app crashes */}
    </div>
  );
}
```

#### ✅ GOOD - Error boundary
```typescript
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to error tracking service
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>Something went wrong</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <UserProfile />
    </ErrorBoundary>
  );
}
```

#### Benefits:
- Prevent whole app crash
- Show user-friendly error
- Log errors for debugging
- Allow recovery

---

### PATTERN 5: ASYNC ERROR HANDLING

#### Concept
Proper error handling cho async operations.

#### ❌ BAD - Unhandled promise rejection
```typescript
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  return data;
}

// No error handling!
fetchUser('123');  // If fails, unhandled rejection
```

#### ✅ GOOD - Try-catch with specific errors
```typescript
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`, {
      signal: AbortSignal.timeout(5000),  // Timeout
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new NotFoundError('User', id);
      }
      if (response.status === 401) {
        throw new UnauthorizedError();
      }
      throw new AppError(
        'API_ERROR',
        `API returned ${response.status}`,
        response.status
      );
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // Network error
    if (error instanceof TypeError) {
      throw new AppError('NETWORK_ERROR', 'Network request failed');
    }
    // Timeout
    if (error.name === 'AbortError') {
      throw new AppError('TIMEOUT', 'Request timed out');
    }
    // Re-throw known errors
    throw error;
  }
}

// Usage with error handling
try {
  const user = await fetchUser('123');
  console.log(user);
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log('User not found');
  } else if (error instanceof AppError) {
    console.error('Error:', error.message);
  } else {
    console.error('Unexpected error:', error);
  }
}
```

---

### PATTERN 6: RETRY WITH EXPONENTIAL BACKOFF

#### Concept
Tự động retry khi gặp lỗi tạm thời (network, timeout).

#### ✅ Implementation
```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    initialDelay?: number;
    maxDelay?: number;
    shouldRetry?: (error: unknown) => boolean;
  } = {}
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 10000,
    shouldRetry = () => true,
  } = options;

  let lastError: unknown;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // Don't retry if not retryable
      if (!shouldRetry(error)) {
        throw error;
      }

      // Don't retry on last attempt
      if (attempt === maxRetries) {
        break;
      }

      // Calculate delay with exponential backoff
      const delay = Math.min(
        initialDelay * Math.pow(2, attempt),
        maxDelay
      );

      logger.warn(`Attempt ${attempt + 1} failed, retrying in ${delay}ms`, {
        error,
      });

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}

// Usage
const user = await fetchWithRetry(
  () => fetch('/api/users/123').then(r => r.json()),
  {
    maxRetries: 3,
    shouldRetry: (error) => {
      // Only retry on network errors or 5xx
      return error instanceof TypeError ||
             (error.status >= 500 && error.status < 600);
    },
  }
);
```

#### Library: Use `p-retry` for Node.js
```typescript
import pRetry from 'p-retry';

const user = await pRetry(
  () => fetch('/api/users/123').then(r => r.json()),
  {
    retries: 3,
    onFailedAttempt: error => {
      console.log(`Attempt ${error.attemptNumber} failed. ${error.retriesLeft} retries left.`);
    },
  }
);
```

---

## ✅ ERROR HANDLING CHECKLIST

### Function-Level Checklist
- [ ] All parameters validated (null/undefined check)
- [ ] All external calls wrapped in try-catch
- [ ] Specific error types thrown (not generic Error)
- [ ] Error messages descriptive
- [ ] Errors logged with context
- [ ] Resources cleaned up (finally block)

### API-Level Checklist
- [ ] Centralized error handler
- [ ] Consistent error response format
- [ ] HTTP status codes correct
- [ ] Don't expose internal errors
- [ ] Error tracking integrated (Sentry)
- [ ] Rate limiting on error-prone endpoints

### Frontend-Level Checklist
- [ ] Error boundaries around major sections
- [ ] Loading states for async operations
- [ ] Error states with retry button
- [ ] User-friendly error messages
- [ ] Errors logged to monitoring service

---

## 🚨 COMMON MISTAKES & FIXES

### Mistake 1: Catching too broadly
```typescript
❌ BAD
try {
  await processPayment(order);
} catch (error) {
  // Catches EVERYTHING, even bugs
  console.log('Payment failed');
}

✅ FIX - Catch specific errors
try {
  await processPayment(order);
} catch (error) {
  if (error instanceof PaymentDeclinedError) {
    notifyUser('Card declined');
  } else if (error instanceof NetworkError) {
    notifyUser('Network error, please retry');
  } else {
    // Unknown error - log and re-throw
    logger.error('Unexpected payment error', { error });
    throw error;
  }
}
```

### Mistake 2: Swallowing errors
```typescript
❌ BAD
try {
  await sendEmail(user.email);
} catch (error) {
  // Silent failure - user never knows
}

✅ FIX - Log and handle
try {
  await sendEmail(user.email);
} catch (error) {
  logger.error('Failed to send email', {
    userId: user.id,
    email: user.email,
    error,
  });
  // Queue for retry or notify admin
  await queueEmailRetry(user.email);
}
```

### Mistake 3: Not cleaning up resources
```typescript
❌ BAD
async function processFile(path: string) {
  const file = await fs.open(path);
  const data = await file.readFile();
  await processData(data);  // If this throws, file never closed
  await file.close();
}

✅ FIX - Use finally
async function processFile(path: string) {
  const file = await fs.open(path);
  try {
    const data = await file.readFile();
    await processData(data);
  } finally {
    await file.close();  // Always runs
  }
}
```

---

## 🎯 AI LEVERAGE

### Error Handling Prompt
```markdown
Add comprehensive error handling:

1. Input validation:
   - Check for null/undefined
   - Validate types
   - Check ranges/formats

2. External calls:
   - Wrap in try-catch
   - Handle specific errors
   - Add timeout
   - Add retry logic

3. Error responses:
   - Use custom error classes
   - Include error codes
   - Log with context
   - Don't expose internals

4. Resource cleanup:
   - Use finally blocks
   - Close connections
   - Release locks
```

---

## 📚 QUICK REFERENCE

| Pattern | When to Use | Benefits |
|---------|-------------|----------|
| Early Return | Input validation | Flat code, clear checks |
| Result Type | Functional style | Type-safe, explicit |
| Centralized Handler | API/Server | Consistent format |
| Error Boundary | React components | Prevent app crash |
| Retry | Network calls | Handle transient failures |

---

## 🔗 RELATED SKILLS

- `workflows/debug-protocol.md` - Debugging errors
- `workflows/logging-standards.md` - Error logging
- `backend/api-design-standards.md` - API error responses
- `workflows/testing-strategies.md` - Testing error cases

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ MANDATORY - All code must have proper error handling
