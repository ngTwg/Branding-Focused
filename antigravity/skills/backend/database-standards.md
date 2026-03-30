# DATABASE STANDARDS - CHUẨN MỰC CƠ SỞ DỮ LIỆU

> **Tier:** 2-3  
> **Tags:** `[database, sql, migrations, indexing, schema-design, postgres, mongodb]`  
> **Khi nào dùng:** Khi thiết kế schema, viết migrations, optimize queries, hoặc làm việc với bất kỳ database nào

---

## 📋 OVERVIEW

**Bad database design** dẫn đến:
- Slow queries → Timeout, poor UX
- Data inconsistency → Bugs, data loss
- Migration failures → Downtime
- Scalability issues → Cannot handle growth
- Data integrity violations → Corrupt data

**Thống kê:**
- 80% performance issues liên quan đến database (DataDog 2023)
- Average query time tăng 10x khi thiếu index

---

## 🎯 DATABASE DESIGN CHECKLIST

```markdown
[ ] Naming conventions (snake_case, plural tables)
[ ] Primary keys defined (UUID or auto-increment)
[ ] Foreign keys with constraints (CASCADE, SET NULL)
[ ] Indexes on frequently queried columns
[ ] Unique constraints where needed
[ ] NOT NULL constraints for required fields
[ ] Default values set appropriately
[ ] Timestamps (created_at, updated_at)
[ ] Soft delete column (deleted_at) if needed
[ ] Migrations are idempotent
[ ] Migrations have rollback (down)
[ ] No sensitive data in plain text
[ ] Proper data types (INT vs BIGINT, VARCHAR length)
[ ] Normalized to 3NF (unless denormalized for performance)
[ ] Backup strategy defined
```

---

## 📝 PATTERN 1: NAMING CONVENTIONS

### ✅ Table & Column Names

```sql
-- ✅ GOOD: snake_case, plural tables
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  date_of_birth DATE,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  bio TEXT,
  avatar_url VARCHAR(500)
);

CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  published_at TIMESTAMP,
  view_count INT DEFAULT 0
);

-- ❌ BAD: Inconsistent naming
CREATE TABLE User (  -- ❌ Singular, PascalCase
  ID int,  -- ❌ UPPERCASE
  Email varchar(255),  -- ❌ PascalCase
  firstName VARCHAR(100),  -- ❌ camelCase
  date_created DATETIME  -- ❌ Inconsistent with created_at
);
```

### Rules

1. **Tables:** Plural nouns, snake_case (`users`, `user_profiles`)
2. **Columns:** snake_case (`first_name`, `created_at`)
3. **Booleans:** Prefix with `is_`, `has_`, `can_` (`is_active`, `has_verified_email`)
4. **Foreign keys:** `{table_singular}_id` (`user_id`, `post_id`)
5. **Timestamps:** `created_at`, `updated_at`, `deleted_at`, `published_at`
6. **Counts:** Suffix with `_count` (`view_count`, `like_count`)

---

## 🔑 PATTERN 2: PRIMARY KEYS

### UUID vs Auto-Increment

```sql
-- Option 1: Auto-increment (simple, sequential)
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,  -- PostgreSQL
  -- id BIGINT AUTO_INCREMENT PRIMARY KEY  -- MySQL
  name VARCHAR(100)
);

-- Pros: Simple, small size (8 bytes), sequential
-- Cons: Predictable, exposes count, hard to merge databases

-- Option 2: UUID (distributed, unpredictable)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- PostgreSQL
  name VARCHAR(100)
);

-- Pros: Globally unique, unpredictable, easy to merge
-- Cons: Larger size (16 bytes), random (index fragmentation)

-- Option 3: ULID (best of both worlds)
-- Sortable like auto-increment, unique like UUID
CREATE TABLE users (
  id CHAR(26) PRIMARY KEY,  -- Store ULID as string
  name VARCHAR(100)
);
-- Generate ULID in application code
```

### When to Use

| Use Case | Recommendation |
|----------|----------------|
| **Simple app** | Auto-increment |
| **Distributed system** | UUID or ULID |
| **Public API** | UUID (hide count) |
| **High write volume** | ULID (better index) |
| **Microservices** | UUID or ULID |

---

## 🔗 PATTERN 3: FOREIGN KEYS & CONSTRAINTS

### ✅ Proper Foreign Keys

```sql
-- Users table
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL
);

-- Posts table with foreign key
CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- ⭐ Foreign key with CASCADE
  CONSTRAINT fk_posts_author
    FOREIGN KEY (author_id)
    REFERENCES users(id)
    ON DELETE CASCADE  -- Delete posts when user deleted
    ON UPDATE CASCADE
);

-- Comments table
CREATE TABLE comments (
  id BIGSERIAL PRIMARY KEY,
  post_id BIGINT NOT NULL,
  user_id BIGINT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- ⭐ Multiple foreign keys
  CONSTRAINT fk_comments_post
    FOREIGN KEY (post_id)
    REFERENCES posts(id)
    ON DELETE CASCADE,  -- Delete comments when post deleted
  
  CONSTRAINT fk_comments_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE SET NULL  -- Keep comment, set user_id to NULL
);
```

### ON DELETE Options

```sql
-- CASCADE: Delete child rows
ON DELETE CASCADE

-- SET NULL: Set foreign key to NULL (column must be nullable)
ON DELETE SET NULL

-- RESTRICT: Prevent deletion if child rows exist (default)
ON DELETE RESTRICT

-- NO ACTION: Same as RESTRICT
ON DELETE NO ACTION

-- SET DEFAULT: Set to default value
ON DELETE SET DEFAULT
```

### Example: Soft Delete with Foreign Keys

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  deleted_at TIMESTAMP NULL  -- Soft delete
);

CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT NOT NULL,
  title VARCHAR(200) NOT NULL,
  deleted_at TIMESTAMP NULL,
  
  CONSTRAINT fk_posts_author
    FOREIGN KEY (author_id)
    REFERENCES users(id)
    ON DELETE RESTRICT  -- ⭐ Prevent hard delete if posts exist
);

-- Soft delete user (posts remain)
UPDATE users SET deleted_at = NOW() WHERE id = 123;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

---

## 📊 PATTERN 4: INDEXES

### When to Add Index

```sql
-- ✅ Index on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at);

-- ✅ Composite index (order matters!)
CREATE INDEX idx_posts_author_created 
  ON posts(author_id, created_at DESC);
-- Good for: WHERE author_id = ? ORDER BY created_at DESC

-- ✅ Partial index (filtered)
CREATE INDEX idx_posts_published 
  ON posts(created_at) 
  WHERE published_at IS NOT NULL;
-- Only index published posts

-- ✅ Unique index (enforce uniqueness)
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
-- Better than UNIQUE constraint (can be partial)

-- ❌ BAD: Over-indexing
CREATE INDEX idx_users_name ON users(name);  -- Rarely queried
CREATE INDEX idx_posts_content ON posts(content);  -- Full-text search better
```

### Index Guidelines

```markdown
✅ DO index:
- Primary keys (automatic)
- Foreign keys (manual)
- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY
- Columns in GROUP BY
- Unique constraints

❌ DON'T index:
- Small tables (< 1000 rows)
- Columns rarely queried
- Columns with low cardinality (few unique values)
- Columns frequently updated
- Large text columns (use full-text search)
```

### Analyze Query Performance

```sql
-- PostgreSQL: EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT * FROM posts 
WHERE author_id = 123 
ORDER BY created_at DESC 
LIMIT 10;

-- Look for:
-- - Seq Scan (bad) → Add index
-- - Index Scan (good)
-- - Execution time

-- MySQL: EXPLAIN
EXPLAIN
SELECT * FROM posts 
WHERE author_id = 123;

-- Look for:
-- - type: ALL (bad) → Add index
-- - type: ref, range (good)
```

---

## 🔄 PATTERN 5: MIGRATIONS (Idempotent & Rollback)

### ✅ Idempotent Migrations

```sql
-- ❌ BAD: Not idempotent (fails if run twice)
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255)
);

-- ✅ GOOD: Idempotent (safe to run multiple times)
CREATE TABLE IF NOT EXISTS users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255)
);

-- Add column (idempotent)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'users' AND column_name = 'phone'
  ) THEN
    ALTER TABLE users ADD COLUMN phone VARCHAR(20);
  END IF;
END $$;

-- Add index (idempotent)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

### ✅ Rollback Migrations

```javascript
// Knex.js migration example
exports.up = async function(knex) {
  // ⭐ UP: Apply changes
  await knex.schema.createTable('users', (table) => {
    table.bigIncrements('id').primary();
    table.string('email', 255).notNullable().unique();
    table.string('name', 100).notNullable();
    table.timestamps(true, true);  // created_at, updated_at
  });
  
  await knex.schema.createTable('posts', (table) => {
    table.bigIncrements('id').primary();
    table.bigInteger('author_id').notNullable()
      .references('id').inTable('users').onDelete('CASCADE');
    table.string('title', 200).notNullable();
    table.text('content').notNullable();
    table.timestamps(true, true);
    
    table.index('author_id');
  });
};

exports.down = async function(knex) {
  // ⭐ DOWN: Rollback changes (reverse order!)
  await knex.schema.dropTableIfExists('posts');
  await knex.schema.dropTableIfExists('users');
};
```

### Migration Best Practices

```markdown
✅ DO:
- Make migrations idempotent (IF NOT EXISTS)
- Always write rollback (down)
- Test migrations on staging first
- Keep migrations small (one change per file)
- Add indexes in separate migration (can be slow)
- Use transactions (automatic in most tools)
- Version migrations (timestamp prefix)

❌ DON'T:
- Modify old migrations (create new one)
- Delete data without backup
- Run migrations manually in production
- Mix schema and data changes
- Forget to commit migration files
```

---

## 🗂️ PATTERN 6: SOFT DELETE

### Implementation

```sql
-- Add deleted_at column
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL  -- ⭐ Soft delete
);

-- Soft delete (update)
UPDATE users SET deleted_at = NOW() WHERE id = 123;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;

-- Query deleted users
SELECT * FROM users WHERE deleted_at IS NOT NULL;

-- Restore user
UPDATE users SET deleted_at = NULL WHERE id = 123;

-- Hard delete (permanent)
DELETE FROM users WHERE id = 123 AND deleted_at IS NOT NULL;
```

### With Application Code

```javascript
// Sequelize model
const User = sequelize.define('User', {
  email: DataTypes.STRING,
  name: DataTypes.STRING,
  deletedAt: DataTypes.DATE  // ⭐ Soft delete column
}, {
  paranoid: true,  // ⭐ Enable soft delete
  timestamps: true
});

// Soft delete
await User.destroy({ where: { id: 123 } });
// SQL: UPDATE users SET deleted_at = NOW() WHERE id = 123

// Query active users (automatic)
await User.findAll();
// SQL: SELECT * FROM users WHERE deleted_at IS NULL

// Query with deleted users
await User.findAll({ paranoid: false });
// SQL: SELECT * FROM users

// Restore user
await User.restore({ where: { id: 123 } });
// SQL: UPDATE users SET deleted_at = NULL WHERE id = 123
```

---

## 📐 PATTERN 7: NORMALIZATION

### 3NF (Third Normal Form)

```sql
-- ❌ BAD: Denormalized (data duplication)
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_email VARCHAR(255),
  customer_phone VARCHAR(20),
  product_name VARCHAR(200),
  product_price DECIMAL(10, 2),
  quantity INT
);
-- Problem: Customer data duplicated in every order

-- ✅ GOOD: Normalized (3NF)
CREATE TABLE customers (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone VARCHAR(20)
);

CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
  id BIGSERIAL PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id BIGINT NOT NULL REFERENCES products(id),
  quantity INT NOT NULL,
  price_at_purchase DECIMAL(10, 2) NOT NULL  -- ⭐ Snapshot price
);
```

### When to Denormalize

```sql
-- ✅ Denormalize for performance (read-heavy)
CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  
  -- ⭐ Denormalized counts (avoid COUNT queries)
  comment_count INT DEFAULT 0,
  like_count INT DEFAULT 0,
  view_count INT DEFAULT 0,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update counts with triggers or application code
CREATE OR REPLACE FUNCTION update_post_comment_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE posts SET comment_count = comment_count + 1 WHERE id = NEW.post_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE posts SET comment_count = comment_count - 1 WHERE id = OLD.post_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_comment_count
AFTER INSERT OR DELETE ON comments
FOR EACH ROW EXECUTE FUNCTION update_post_comment_count();
```

---

## 🔒 PATTERN 8: DATA TYPES

### Choose Appropriate Types

```sql
-- ✅ GOOD: Appropriate types
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,  -- BIGINT for large tables
  email VARCHAR(255) NOT NULL,  -- Reasonable length
  age SMALLINT CHECK (age >= 0 AND age <= 150),  -- Small range
  balance DECIMAL(10, 2),  -- Exact decimal (money)
  is_active BOOLEAN DEFAULT true,
  metadata JSONB,  -- Structured data (PostgreSQL)
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ❌ BAD: Wrong types
CREATE TABLE users (
  id INT,  -- ❌ Too small (max 2 billion)
  email TEXT,  -- ❌ Unbounded (use VARCHAR)
  age VARCHAR(10),  -- ❌ Should be INT
  balance FLOAT,  -- ❌ Imprecise (use DECIMAL for money)
  is_active VARCHAR(5),  -- ❌ Should be BOOLEAN
  metadata TEXT,  -- ❌ Should be JSON/JSONB
  created_at VARCHAR(50)  -- ❌ Should be TIMESTAMP
);
```

### Type Guidelines

| Data | Type | Example |
|------|------|---------|
| **ID** | BIGSERIAL, UUID | `id BIGSERIAL PRIMARY KEY` |
| **Email** | VARCHAR(255) | `email VARCHAR(255)` |
| **Name** | VARCHAR(100) | `name VARCHAR(100)` |
| **Phone** | VARCHAR(20) | `phone VARCHAR(20)` |
| **Age** | SMALLINT | `age SMALLINT CHECK (age >= 0)` |
| **Money** | DECIMAL(10, 2) | `price DECIMAL(10, 2)` |
| **Boolean** | BOOLEAN | `is_active BOOLEAN` |
| **Date** | DATE | `date_of_birth DATE` |
| **Timestamp** | TIMESTAMP | `created_at TIMESTAMP` |
| **JSON** | JSONB (PostgreSQL) | `metadata JSONB` |
| **Text** | TEXT | `content TEXT` |

---

## 📊 QUICK REFERENCE

| Aspect | Standard | Example |
|--------|----------|---------|
| **Table Names** | Plural, snake_case | `users`, `user_profiles` |
| **Column Names** | snake_case | `first_name`, `created_at` |
| **Primary Key** | BIGSERIAL or UUID | `id BIGSERIAL PRIMARY KEY` |
| **Foreign Key** | {table}_id | `user_id`, `post_id` |
| **Timestamps** | created_at, updated_at | `TIMESTAMP DEFAULT NOW()` |
| **Soft Delete** | deleted_at | `deleted_at TIMESTAMP NULL` |
| **Booleans** | is_, has_, can_ | `is_active`, `has_verified` |
| **Indexes** | idx_{table}_{column} | `idx_users_email` |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: No Indexes on Foreign Keys

```sql
-- ❌ BAD: No index on foreign key
CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT REFERENCES users(id)
);
-- Slow: SELECT * FROM posts WHERE author_id = 123

-- ✅ GOOD: Index on foreign key
CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT REFERENCES users(id)
);
CREATE INDEX idx_posts_author_id ON posts(author_id);
```

### ❌ Mistake 2: Using FLOAT for Money

```sql
-- ❌ BAD: Imprecise
CREATE TABLE products (
  price FLOAT
);
-- 0.1 + 0.2 = 0.30000000000000004

-- ✅ GOOD: Exact decimal
CREATE TABLE products (
  price DECIMAL(10, 2)
);
-- 0.1 + 0.2 = 0.3
```

### ❌ Mistake 3: No Timestamps

```sql
-- ❌ BAD: No audit trail
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255)
);

-- ✅ GOOD: Always add timestamps
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Design database schema for blog with:
- Users (email, name, password_hash)
- Posts (title, content, author, published_at)
- Comments (content, author, post)
- Tags (name)
- Post-Tag many-to-many relationship
- Proper indexes, foreign keys, timestamps
- Soft delete for users and posts
- Follow PostgreSQL best practices"
```

### AI Should

1. ✅ Use snake_case, plural tables
2. ✅ Add BIGSERIAL primary keys
3. ✅ Add foreign keys with CASCADE
4. ✅ Add indexes on foreign keys
5. ✅ Add created_at, updated_at, deleted_at
6. ✅ Create junction table for many-to-many
7. ✅ Write idempotent migrations with rollback

---

## 🔗 RELATED SKILLS

- `api-design-standards.md` - API design for database
- `concurrency-patterns.md` - Database transactions
- `logging-standards.md` - Database query logging

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium  
**Impact:** Critical (foundation of app)
