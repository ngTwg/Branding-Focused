---
name: "NoSQL Expert"
tags: ["antigravity", "c:", "database", "expert", "frontend", "gemini", "<YOUR_USERNAME>", "mongodb", "nosql", "overview", "patterns", "quick", "reference", "rules", "specialized", "system", "tools", "types", "users"]
tier: 2
risk: "medium"
estimated_tokens: 2403
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# NoSQL Expert

> **Tier:** 2-3  
> **Tags:** `nosql`, `mongodb`, `redis`, `cassandra`, `database`, `data-modeling`  
> **When to use:** Choosing NoSQL database, data modeling, scaling strategies, performance optimization

---

## Overview

Comprehensive guide to NoSQL databases covering document stores (MongoDB), key-value stores (Redis), column-family stores (Cassandra), and graph databases (Neo4j). Includes when to use each type, data modeling patterns, and performance optimization.

---

## Rules

**RULE-001: Choose Right NoSQL Type**
Match database type to access patterns. Document stores for flexible schemas, key-value for caching, column-family for time-series, graph for relationships.

```javascript
❌ Bad: Use MongoDB for everything
// Using MongoDB for simple cache
await db.cache.insertOne({ key: 'user:123', value: userData });

// Using MongoDB for graph traversal
await db.users.aggregate([/* complex $graphLookup */]);

✅ Good: Right tool for the job
// Redis for cache (key-value)
await redis.set('user:123', JSON.stringify(userData), 'EX', 3600);

// Neo4j for graph traversal
MATCH (u:User)-[:FOLLOWS*1..3]->(friend)
WHERE u.id = '123'
RETURN friend
```

**RULE-002: Document Store Data Modeling**
Embed related data for read performance. Reference for many-to-many or large arrays. Denormalize for query efficiency.

```javascript
❌ Bad: Over-normalization (SQL thinking)
// Users collection
{ _id: 1, name: 'Alice' }

// Posts collection
{ _id: 101, userId: 1, title: 'Post 1' }

// Comments collection
{ _id: 201, postId: 101, text: 'Comment 1' }

// Requires 3 queries to get user's posts with comments

✅ Good: Embed for read optimization
// Users collection with embedded posts
{
  _id: 1,
  name: 'Alice',
  posts: [
    {
      _id: 101,
      title: 'Post 1',
      comments: [
        { _id: 201, text: 'Comment 1', author: 'Bob' }
      ]
    }
  ]
}

// Single query gets everything
db.users.findOne({ _id: 1 });
```

**RULE-003: Key-Value Store Patterns**
Use Redis for caching, sessions, rate limiting, pub/sub. Structure keys hierarchically. Set expiration on all keys.

```javascript
❌ Bad: Unstructured keys, no expiration
await redis.set('data', JSON.stringify(data));
// Key never expires, no namespace

✅ Good: Structured keys with TTL
// Hierarchical key structure
const key = `app:${env}:user:${userId}:session`;
await redis.set(key, JSON.stringify(session), 'EX', 3600);

// Rate limiting pattern
const rateLimitKey = `ratelimit:${userId}:${Date.now() / 60000 | 0}`;
const count = await redis.incr(rateLimitKey);
await redis.expire(rateLimitKey, 60);

if (count > 100) {
  throw new Error('Rate limit exceeded');
}
```

**RULE-004: Column-Family Store Modeling**
Design for query patterns, not data structure. Denormalize heavily. Use wide rows for time-series data.

```javascript
❌ Bad: Normalized schema (SQL thinking)
// users table
CREATE TABLE users (id uuid PRIMARY KEY, name text);

// posts table
CREATE TABLE posts (id uuid PRIMARY KEY, user_id uuid, title text);

// Requires join (expensive in Cassandra)

✅ Good: Query-driven denormalization
// posts_by_user table (optimized for "get user's posts")
CREATE TABLE posts_by_user (
  user_id uuid,
  post_time timestamp,
  post_id uuid,
  title text,
  content text,
  PRIMARY KEY (user_id, post_time)
) WITH CLUSTERING ORDER BY (post_time DESC);

// Single partition read
SELECT * FROM posts_by_user WHERE user_id = ? LIMIT 10;
```

**RULE-005: Indexing Strategy**
Index only frequently queried fields. Avoid indexing high-cardinality fields in document stores. Use compound indexes for multi-field queries.

```javascript
❌ Bad: Index everything or nothing
// No indexes (slow queries)
db.users.find({ email: 'alice@example.com' }); // Full scan

// Too many indexes (slow writes)
db.users.createIndex({ email: 1 });
db.users.createIndex({ name: 1 });
db.users.createIndex({ age: 1 });
db.users.createIndex({ city: 1 });
// Every write updates 4 indexes

✅ Good: Strategic indexing
// Compound index for common query pattern
db.users.createIndex({ status: 1, createdAt: -1 });

// Query uses index efficiently
db.users.find({ status: 'active' }).sort({ createdAt: -1 });

// Unique index for email (enforces constraint)
db.users.createIndex({ email: 1 }, { unique: true });
```

**RULE-006: Aggregation Optimization**
Use aggregation pipelines for complex queries. Push filtering early. Limit data processed. Use indexes.

```javascript
❌ Bad: Load all data then filter
const users = await db.users.find({}).toArray();
const activeUsers = users.filter(u => u.status === 'active');
const sorted = activeUsers.sort((a, b) => b.score - a.score);
const top10 = sorted.slice(0, 10);

✅ Good: Aggregation pipeline
const top10 = await db.users.aggregate([
  // 1. Filter early (uses index)
  { $match: { status: 'active' } },
  
  // 2. Sort (uses index if available)
  { $sort: { score: -1 } },
  
  // 3. Limit early
  { $limit: 10 },
  
  // 4. Project only needed fields
  { $project: { name: 1, score: 1, _id: 0 } }
]).toArray();
```

**RULE-007: Sharding and Partitioning**
Choose shard key carefully (high cardinality, even distribution). Avoid hotspots. Plan for growth.

```javascript
❌ Bad: Poor shard key
// Shard by status (low cardinality, uneven distribution)
sh.shardCollection('app.users', { status: 1 });
// Most users are 'active', creates hotspot

// Shard by timestamp (monotonically increasing)
sh.shardCollection('app.events', { timestamp: 1 });
// All writes go to last shard

✅ Good: Balanced shard key
// Shard by hashed user_id (even distribution)
sh.shardCollection('app.users', { user_id: 'hashed' });

// Compound shard key for time-series
sh.shardCollection('app.events', { user_id: 1, timestamp: 1 });
// Distributes by user, maintains time ordering within user
```

**RULE-008: Consistency vs Performance**
Understand CAP theorem tradeoffs. Use appropriate consistency level. Implement eventual consistency patterns where acceptable.

```javascript
❌ Bad: Always use strong consistency
// Every read waits for all replicas
const user = await db.users.findOne(
  { _id: userId },
  { readConcern: { level: 'linearizable' } }
);
// Slow, may fail if replica unavailable

✅ Good: Match consistency to use case
// Strong consistency for critical operations
const balance = await db.accounts.findOne(
  { _id: accountId },
  { readConcern: { level: 'majority' } }
);

// Eventual consistency for non-critical reads
const profile = await db.users.findOne(
  { _id: userId },
  { readPreference: 'secondaryPreferred' }
);

// Optimistic locking for updates
const result = await db.accounts.updateOne(
  { _id: accountId, version: currentVersion },
  { $inc: { balance: amount, version: 1 } }
);

if (result.modifiedCount === 0) {
  throw new Error('Concurrent modification detected');
}
```

---

## Quick Reference

### NoSQL Database Types

| Type | Examples | Best For | Not For |
|------|----------|----------|---------|
| Document | MongoDB, CouchDB | Flexible schemas, nested data | Complex joins, transactions |
| Key-Value | Redis, DynamoDB | Caching, sessions, simple lookups | Complex queries, relationships |
| Column-Family | Cassandra, HBase | Time-series, high write throughput | Ad-hoc queries, complex joins |
| Graph | Neo4j, ArangoDB | Social networks, recommendations | Simple CRUD, high write volume |

### MongoDB Patterns

```javascript
// Embedding (1-to-few)
{
  _id: 1,
  name: 'Alice',
  addresses: [
    { street: '123 Main St', city: 'NYC' }
  ]
}

// Referencing (1-to-many)
// User document
{ _id: 1, name: 'Alice' }

// Post documents
{ _id: 101, userId: 1, title: 'Post 1' }
{ _id: 102, userId: 1, title: 'Post 2' }

// Hybrid (many-to-many)
{
  _id: 1,
  name: 'Alice',
  followingIds: [2, 3, 4], // Reference IDs
  recentFollowing: [ // Embed recent for performance
    { id: 2, name: 'Bob' },
    { id: 3, name: 'Charlie' }
  ]
}
```

### Redis Data Structures

```javascript
// String (simple key-value)
await redis.set('user:123:name', 'Alice');

// Hash (object)
await redis.hset('user:123', 'name', 'Alice', 'email', 'alice@example.com');

// List (queue, stack)
await redis.lpush('queue:jobs', JSON.stringify(job));
const job = await redis.brpop('queue:jobs', 0);

// Set (unique items)
await redis.sadd('user:123:tags', 'developer', 'nodejs');

// Sorted Set (leaderboard)
await redis.zadd('leaderboard', 1000, 'Alice');
const top10 = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');
```

### Cassandra Query Patterns

```cql
-- Time-series data
CREATE TABLE sensor_data (
  sensor_id uuid,
  timestamp timestamp,
  temperature double,
  PRIMARY KEY (sensor_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Query recent data
SELECT * FROM sensor_data
WHERE sensor_id = ?
AND timestamp > ?
LIMIT 100;

-- Materialized view for different query pattern
CREATE MATERIALIZED VIEW sensor_data_by_temp AS
  SELECT * FROM sensor_data
  WHERE temperature IS NOT NULL
  PRIMARY KEY (temperature, sensor_id, timestamp);
```

### Performance Optimization Checklist

- [ ] Indexes on frequently queried fields
- [ ] Compound indexes for multi-field queries
- [ ] Projection to limit returned fields
- [ ] Pagination for large result sets
- [ ] Connection pooling
- [ ] Read replicas for read-heavy workloads
- [ ] Caching layer (Redis) for hot data
- [ ] Batch operations for bulk writes
- [ ] Monitoring slow queries
- [ ] Regular index maintenance

---

## Metadata

- **Related Skills:** [database-patterns.md], [caching-strategies.md], [api-design.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
