---
name: "BullMQ Specialist"
tags: ["antigravity", "basic", "bullmq", "c:", "capabilities", "core", "frontend", "gemini", "<YOUR_USERNAME>", "overview", "patterns", "philosophy", "queue", "setup", "specialist", "specialized", "system", "tools", "users"]
tier: 3
risk: "medium"
estimated_tokens: 1624
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.90
---
# BullMQ Specialist

> **Tier:** 2-3  
> **Tags:** `bullmq`, `redis`, `queue`, `background-jobs`, `async`, `nodejs`  
> **When to Use:** Redis-backed job queues, background processing, reliable async execution

---

## Overview

BullMQ expert for production-grade job queues. Process billions of jobs reliably with Redis-backed queues, handle complex workflows, and optimize worker concurrency.

**Source:** vibeship-spawner-skills (Apache 2.0)

---

## Core Philosophy

Queues are the backbone of scalable applications:
- **Decouple services** - Async communication between components
- **Smooth traffic spikes** - Buffer load during peak times
- **Enable reliability** - Retry failed jobs, handle errors gracefully
- **Scale independently** - Workers scale separate from API servers

Most queue problems are actually Redis problems or application design problems.

---

## Capabilities

- **bullmq-queues** - Create and manage job queues
- **job-scheduling** - Schedule jobs for future execution
- **delayed-jobs** - Jobs that run after a delay
- **repeatable-jobs** - Cron-like recurring jobs
- **job-priorities** - Priority-based job processing
- **rate-limiting-jobs** - Control job execution rate
- **job-events** - Listen to job lifecycle events
- **worker-patterns** - Efficient worker implementations
- **flow-producers** - Complex multi-step workflows
- **job-dependencies** - Parent-child job relationships

---

## Patterns

### Basic Queue Setup

Production-ready BullMQ queue with proper configuration:

```typescript
import { Queue, Worker } from 'bullmq';
import Redis from 'ioredis';

// Redis connection (reuse across queues)
const connection = new Redis({
  host: 'localhost',
  port: 6379,
  maxRetriesPerRequest: null, // Required for BullMQ
});

// Create queue
const emailQueue = new Queue('emails', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000, // Start with 1s, then 2s, 4s
    },
    removeOnComplete: 100, // Keep last 100 completed
    removeOnFail: 1000,    // Keep last 1000 failed
  },
});

// Add job
await emailQueue.add('send-welcome', {
  to: 'user@example.com',
  template: 'welcome',
});

// Worker
const worker = new Worker('emails', async (job) => {
  const { to, template } = job.data;
  await sendEmail(to, template);
}, {
  connection,
  concurrency: 5, // Process 5 jobs concurrently
});

// Event listeners
worker.on('completed', (job) => {
  console.log(`Job ${job.id} completed`);
});

worker.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed:`, err);
});
```

### Delayed and Scheduled Jobs

Jobs that run at specific times or after delays:

```typescript
// Delay by milliseconds
await queue.add('reminder', { userId: 123 }, {
  delay: 3600000, // 1 hour
});

// Schedule for specific time
const scheduledTime = new Date('2024-12-25T00:00:00Z');
await queue.add('holiday-email', { template: 'xmas' }, {
  delay: scheduledTime.getTime() - Date.now(),
});

// Repeatable jobs (cron-like)
await queue.add('daily-report', {}, {
  repeat: {
    pattern: '0 9 * * *', // Every day at 9 AM
    tz: 'America/New_York',
  },
});

// Remove repeatable job
await queue.removeRepeatable('daily-report', {
  pattern: '0 9 * * *',
});
```

### Job Flows and Dependencies

Complex multi-step job processing with parent-child relationships:

```typescript
import { FlowProducer } from 'bullmq';

const flow = new FlowProducer({ connection });

// Create flow: parent job with children
await flow.add({
  name: 'process-order',
  queueName: 'orders',
  data: { orderId: 123 },
  children: [
    {
      name: 'charge-payment',
      queueName: 'payments',
      data: { orderId: 123, amount: 99.99 },
    },
    {
      name: 'send-confirmation',
      queueName: 'emails',
      data: { orderId: 123, template: 'order-confirm' },
    },
  ],
});

// Children run in parallel, parent completes when all children complete
```

---

## Anti-Patterns

### ❌ Giant Job Payloads

**Don't:** Store large data in job payload
```typescript
// BAD: 10MB image in job data
await queue.add('process-image', {
  imageData: base64EncodedImage, // 10MB!
});
```

**Do:** Store reference, fetch data in worker
```typescript
// GOOD: Store S3 key, fetch in worker
await queue.add('process-image', {
  s3Key: 'images/photo123.jpg',
});

// Worker fetches from S3
const worker = new Worker('images', async (job) => {
  const image = await s3.getObject(job.data.s3Key);
  // Process image
});
```

### ❌ No Dead Letter Queue

**Don't:** Let failed jobs disappear
```typescript
// BAD: Failed jobs removed after 3 attempts
defaultJobOptions: {
  attempts: 3,
  removeOnFail: true, // Lost forever!
}
```

**Do:** Keep failed jobs for investigation
```typescript
// GOOD: Keep failed jobs, move to DLQ
defaultJobOptions: {
  attempts: 3,
  removeOnFail: false, // Keep for debugging
}

// Monitor failed jobs
worker.on('failed', async (job, err) => {
  if (job.attemptsMade >= job.opts.attempts) {
    // Move to dead letter queue
    await dlq.add('failed-job', {
      originalQueue: job.queueName,
      jobData: job.data,
      error: err.message,
    });
  }
});
```

### ❌ Infinite Concurrency

**Don't:** Process unlimited jobs concurrently
```typescript
// BAD: No concurrency limit
const worker = new Worker('emails', handler, {
  concurrency: 1000, // Will overwhelm system!
});
```

**Do:** Set reasonable concurrency based on resources
```typescript
// GOOD: Tune based on CPU/memory/external API limits
const worker = new Worker('emails', handler, {
  concurrency: 10, // Start conservative, tune up
  limiter: {
    max: 100,      // Max 100 jobs
    duration: 1000, // Per second
  },
});
```

---

## Best Practices

1. **Reuse Redis connections** - Don't create new connection per queue
2. **Set job TTL** - Use `removeOnComplete` and `removeOnFail`
3. **Monitor queue health** - Track job counts, processing time
4. **Use job priorities** - Critical jobs first
5. **Implement idempotency** - Jobs should be safe to retry
6. **Log job lifecycle** - Track progress for debugging
7. **Set reasonable timeouts** - Prevent stuck jobs
8. **Use flows for dependencies** - Don't manually chain jobs

---

## Related Skills

- `redis-specialist.md` - Redis optimization
- `backend-patterns.md` - Backend architecture
- `performance-hunter.md` - Performance optimization
- `email-systems.md` - Email sending patterns

---

**Version:** 1.0.0  
**Last Updated:** 2024-03-26  
**Size:** ~6KB
