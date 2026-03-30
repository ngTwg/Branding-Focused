# NAMING CONVENTIONS - QUY TẮC ĐẶT TÊN BẮT BUỘC

> **Tier:** 1-2 (Foundation)  
> **Tags:** `[naming, code-style, maintainability, consistency]`  
> **Khi nào dùng:** Mọi dự án, mọi ngôn ngữ - BẮT BUỘC

---

## 🎯 OVERVIEW

Naming conventions không nhất quán là một trong những "bệnh" phổ biến nhất của AI code (tệ hơn 3x so với code người). AI thường trộn lẫn camelCase, snake_case, PascalCase trong cùng một file, gây khó đọc và khó bảo trì.

**Mục tiêu:** Đảm bảo 100% code tuân thủ naming convention của ngôn ngữ/framework.

---

## 🔴 VẤN ĐỀ THƯỜNG GẶP

### ❌ AI hay sinh code như thế này:
```javascript
// Trộn lung tung trong cùng file
const user_name = "John";        // snake_case
const userAge = 25;               // camelCase
const UserEmail = "john@test.com"; // PascalCase

function get_user_data() {}       // snake_case
function fetchUserOrders() {}     // camelCase
class userService {}              // camelCase (WRONG for class)
```

### ✅ Đúng chuẩn:
```javascript
// Nhất quán camelCase cho JS/TS
const userName = "John";
const userAge = 25;
const userEmail = "john@test.com";

function getUserData() {}
function fetchUserOrders() {}
class UserService {}  // PascalCase for classes
```

---

## 📋 RULES CHI TIẾT

### JAVASCRIPT / TYPESCRIPT

#### RULE-NC-001: Variables & Functions = camelCase
```typescript
✅ GOOD
const userName = "John";
const isActive = true;
const totalCount = 100;

function getUserData() {}
function calculateTotal() {}
async function fetchOrders() {}

❌ BAD
const user_name = "John";      // snake_case
const UserName = "John";        // PascalCase
const TOTAL_COUNT = 100;        // UPPER_SNAKE_CASE (dành cho constants)

function get_user_data() {}     // snake_case
function GetUserData() {}       // PascalCase
```

#### RULE-NC-002: Classes & Components = PascalCase
```typescript
✅ GOOD
class UserService {}
class PaymentProcessor {}
interface UserData {}
type OrderStatus = 'pending' | 'completed';

// React Components
const UserProfile = () => {};
const OrderList = () => {};

❌ BAD
class userService {}            // camelCase
class payment_processor {}      // snake_case
interface userData {}           // camelCase
const userProfile = () => {};   // camelCase for component
```

#### RULE-NC-003: Constants = UPPER_SNAKE_CASE
```typescript
✅ GOOD
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";
const DEFAULT_TIMEOUT = 5000;

❌ BAD
const maxRetryCount = 3;        // camelCase (not a constant)
const ApiBaseUrl = "...";       // PascalCase
const default_timeout = 5000;   // snake_case
```

#### RULE-NC-004: Private/Protected = _prefixed (optional but recommended)
```typescript
✅ GOOD
class UserService {
  private _cache: Map<string, User>;
  
  private _validateInput(data: unknown) {}
  protected _logError(error: Error) {}
}

// Or use TypeScript private keyword (preferred)
class UserService {
  private cache: Map<string, User>;
  
  private validateInput(data: unknown) {}
  protected logError(error: Error) {}
}

❌ BAD
class UserService {
  // Public-looking name but actually private
  private cache: Map<string, User>;  // Confusing without _prefix
}
```

#### RULE-NC-005: Boolean variables = is/has/should prefix
```typescript
✅ GOOD
const isActive = true;
const hasPermission = false;
const shouldRetry = true;
const canEdit = false;

function isValidEmail(email: string): boolean {}
function hasAccess(user: User): boolean {}

❌ BAD
const active = true;            // Unclear type
const permission = false;       // Unclear type
const retry = true;             // Unclear type

function validateEmail(): boolean {}  // Unclear return type
function checkAccess(): boolean {}    // Unclear return type
```

#### RULE-NC-006: Enums = PascalCase (keys = PascalCase)
```typescript
✅ GOOD
enum OrderStatus {
  Pending = 'pending',
  Processing = 'processing',
  Completed = 'completed',
  Cancelled = 'cancelled',
}

enum UserRole {
  Admin = 'admin',
  User = 'user',
  Guest = 'guest',
}

❌ BAD
enum orderStatus {              // camelCase
  pending = 'pending',          // lowercase
  PROCESSING = 'processing',    // UPPER_CASE
}
```

---

### PYTHON

#### RULE-NC-007: Functions & Variables = snake_case
```python
✅ GOOD
user_name = "John"
is_active = True
total_count = 100

def get_user_data():
    pass

def calculate_total():
    pass

async def fetch_orders():
    pass

❌ BAD
userName = "John"               # camelCase
UserName = "John"               # PascalCase
TOTAL_COUNT = 100               # UPPER_SNAKE_CASE (for constants)

def getUserData():              # camelCase
    pass

def GetUserData():              # PascalCase
    pass
```

#### RULE-NC-008: Classes = PascalCase
```python
✅ GOOD
class UserService:
    pass

class PaymentProcessor:
    pass

class OrderRepository:
    pass

❌ BAD
class userService:              # camelCase
    pass

class payment_processor:        # snake_case
    pass
```

#### RULE-NC-009: Constants = UPPER_SNAKE_CASE
```python
✅ GOOD
MAX_RETRY_COUNT = 3
API_BASE_URL = "https://api.example.com"
DEFAULT_TIMEOUT = 5000

❌ BAD
max_retry_count = 3             # snake_case (not a constant)
MaxRetryCount = 3               # PascalCase
```

#### RULE-NC-010: Private/Protected = _prefixed
```python
✅ GOOD
class UserService:
    def __init__(self):
        self._cache = {}        # Protected
        self.__secret = "key"   # Private (name mangling)
    
    def _validate_input(self, data):  # Protected method
        pass
    
    def __log_error(self, error):     # Private method
        pass

❌ BAD
class UserService:
    def __init__(self):
        self.cache = {}         # Looks public but should be private
    
    def validate_input(self):   # Looks public but should be private
        pass
```

---

### SQL / DATABASE

#### RULE-NC-011: Tables = snake_case, plural
```sql
✅ GOOD
users
order_items
product_categories
user_permissions

❌ BAD
User                    -- PascalCase, singular
OrderItems              -- PascalCase
product_category        -- singular
userPermissions         -- camelCase
```

#### RULE-NC-012: Columns = snake_case
```sql
✅ GOOD
first_name
created_at
order_id
is_active

❌ BAD
firstName               -- camelCase
CreatedAt               -- PascalCase
orderID                 -- mixed case
isActive                -- camelCase
```

#### RULE-NC-013: Foreign Keys = singular_table_id
```sql
✅ GOOD
user_id                 -- references users(id)
order_id                -- references orders(id)
product_id              -- references products(id)

❌ BAD
users_id                -- plural
orderId                 -- camelCase
product                 -- missing _id suffix
```

#### RULE-NC-014: Indexes = idx_table_columns
```sql
✅ GOOD
idx_users_email
idx_orders_user_id_status
idx_products_category_id

❌ BAD
users_email_index       -- inconsistent format
index_orders            -- unclear
email_idx               -- missing table name
```

#### RULE-NC-015: Unique Constraints = uq_table_columns
```sql
✅ GOOD
uq_users_email
uq_products_sku
uq_orders_external_id

❌ BAD
unique_users_email      -- inconsistent format
users_email_unique      -- inconsistent format
```

---

### CSS / SCSS

#### RULE-NC-016: Classes = kebab-case (BEM recommended)
```css
✅ GOOD
.user-profile {}
.order-list {}
.button-primary {}

/* BEM (Block Element Modifier) */
.card {}
.card__header {}
.card__body {}
.card--featured {}

❌ BAD
.userProfile {}         /* camelCase */
.UserProfile {}         /* PascalCase */
.user_profile {}        /* snake_case */
```

#### RULE-NC-017: IDs = kebab-case
```css
✅ GOOD
#main-content {}
#user-dashboard {}
#order-summary {}

❌ BAD
#mainContent {}         /* camelCase */
#MainContent {}         /* PascalCase */
```

---

## 🛠️ ENFORCEMENT - AUTOMATED TOOLS

### JavaScript/TypeScript

#### ESLint Configuration
```json
// .eslintrc.json
{
  "rules": {
    "camelcase": ["error", {
      "properties": "always",
      "ignoreDestructuring": false
    }],
    "@typescript-eslint/naming-convention": [
      "error",
      {
        "selector": "variable",
        "format": ["camelCase", "UPPER_CASE"]
      },
      {
        "selector": "function",
        "format": ["camelCase"]
      },
      {
        "selector": "typeLike",
        "format": ["PascalCase"]
      },
      {
        "selector": "enumMember",
        "format": ["PascalCase"]
      }
    ]
  }
}
```

#### Commands
```bash
# Check naming
npx eslint . --ext .ts,.tsx,.js,.jsx

# Auto-fix (some issues)
npx eslint . --ext .ts,.tsx,.js,.jsx --fix

# Format code
npx prettier --write "**/*.{ts,tsx,js,jsx}"
```

---

### Python

#### Pylint/Ruff Configuration
```toml
# pyproject.toml
[tool.ruff]
select = ["N"]  # Enable naming conventions

[tool.ruff.lint.pep8-naming]
classmethod-decorators = ["classmethod"]
staticmethod-decorators = ["staticmethod"]
```

#### Commands
```bash
# Check naming (Ruff - fast)
ruff check . --select N

# Auto-fix
ruff check . --select N --fix

# Format code
black .

# Check naming (Pylint - comprehensive)
pylint --disable=all --enable=invalid-name,bad-classmethod-argument .
```

---

### SQL

#### SQLFluff Configuration
```ini
# .sqlfluff
[sqlfluff]
dialect = postgres

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.identifiers]
extended_capitalisation_policy = lower
```

#### Commands
```bash
# Check SQL naming
sqlfluff lint .

# Auto-fix
sqlfluff fix .
```

---

## ✅ VALIDATION CHECKLIST

### Pre-commit Checklist
- [ ] Tất cả variables/functions theo đúng convention của ngôn ngữ
- [ ] Classes/Components dùng PascalCase
- [ ] Constants dùng UPPER_SNAKE_CASE
- [ ] Boolean variables có prefix is/has/should
- [ ] Private members có prefix _ (nếu áp dụng)
- [ ] Database tables/columns theo snake_case
- [ ] CSS classes theo kebab-case
- [ ] Không có tên viết tắt khó hiểu (usr, ord, prd)
- [ ] Không có tên quá chung chung (data, info, temp)

### Code Review Checklist
- [ ] Naming nhất quán trong toàn bộ file
- [ ] Naming nhất quán với codebase hiện có
- [ ] Tên mô tả rõ ràng mục đích (không cần comment giải thích)
- [ ] Không có typo trong tên
- [ ] Không có tên conflict với built-in functions

---

## 🚨 COMMON MISTAKES & FIXES

### Mistake 1: Trộn lẫn conventions
```typescript
❌ BAD
const user_name = "John";  // snake_case
const userAge = 25;        // camelCase
const UserEmail = "...";   // PascalCase

✅ FIX - Chọn một convention và stick với nó
const userName = "John";
const userAge = 25;
const userEmail = "...";
```

### Mistake 2: Constants không dùng UPPER_SNAKE_CASE
```typescript
❌ BAD
const maxRetryCount = 3;
const apiBaseUrl = "...";

✅ FIX
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "...";
```

### Mistake 3: Boolean không có prefix
```typescript
❌ BAD
const active = true;
const loading = false;

✅ FIX
const isActive = true;
const isLoading = false;
```

### Mistake 4: Class dùng camelCase
```typescript
❌ BAD
class userService {}

✅ FIX
class UserService {}
```

### Mistake 5: Database table dùng singular
```sql
❌ BAD
CREATE TABLE user (...);
CREATE TABLE order (...);

✅ FIX
CREATE TABLE users (...);
CREATE TABLE orders (...);
```

---

## 🎯 AI LEVERAGE

### Prompt Template
```markdown
Viết code với naming conventions sau:
- JavaScript/TypeScript: camelCase cho variables/functions, PascalCase cho classes
- Python: snake_case cho variables/functions, PascalCase cho classes
- Constants: UPPER_SNAKE_CASE
- Boolean: is/has/should prefix
- Database: snake_case, tables plural

Đảm bảo 100% nhất quán trong toàn bộ code.
```

### Review Prompt
```markdown
Review naming conventions trong code này:
1. Có trộn lẫn camelCase/snake_case/PascalCase không?
2. Constants có dùng UPPER_SNAKE_CASE không?
3. Classes có dùng PascalCase không?
4. Boolean variables có prefix is/has/should không?
5. Database tables/columns có theo snake_case không?

List tất cả violations và suggest fixes.
```

---

## 📚 QUICK REFERENCE

| Language | Variables/Functions | Classes | Constants | Private |
|----------|---------------------|---------|-----------|---------|
| JavaScript/TS | camelCase | PascalCase | UPPER_SNAKE_CASE | _prefixed |
| Python | snake_case | PascalCase | UPPER_SNAKE_CASE | _prefixed |
| SQL | snake_case | N/A | N/A | N/A |
| CSS | kebab-case | N/A | N/A | N/A |

---

## 🔗 RELATED SKILLS

- `workflows/code-review.md` - Code review checklist
- `workflows/refactoring-triggers.md` - When to refactor naming
- `backend/api-design-standards.md` - API naming conventions
- `backend/database-standards.md` - Database naming conventions

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ MANDATORY - Must be enforced in all projects
