---
name: "ENVIRONMENT STANDARDS - QUẢN LÝ CẤU HÌNH MÔI TRƯỜNG"
tags: ["antigravity", "c:", "checklist", "commit", "cấu", "env", "environment", "file", "frontend", "gemini", "hình", "<YOUR_USERNAME>", "môi", "never", "overview", "pattern", "proper", "quản", "standards", "structure"]
tier: 2
risk: "medium"
estimated_tokens: 3131
tools_needed: ["git", "markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# ENVIRONMENT STANDARDS - QUẢN LÝ CẤU HÌNH MÔI TRƯỜNG

> **Tier:** 2-3  
> **Tags:** `[environment, config, secrets, env-vars, zod, validation]`  
> **Khi nào dùng:** Mọi application (frontend, backend), đặc biệt khi deploy multi-environment

---

## 📋 OVERVIEW

**Bad environment management** dẫn đến:
- Secrets leaked to Git → Security breach
- App crashes in production → Missing env vars
- Different behavior dev vs prod → Hard to debug
- Cannot reproduce bugs → Env mismatch
- Deployment failures → Wrong config

**Thống kê:**
- 40% production incidents do misconfiguration (Datadog 2023)
- 30% security breaches from leaked secrets (GitHub 2023)

---

## 🎯 ENVIRONMENT CHECKLIST

```markdown
[ ] .env file in .gitignore
[ ] .env.example committed (no secrets)
[ ] Environment validation on startup (Zod, Joi)
[ ] Type-safe env access (no process.env.X everywhere)
[ ] Secrets management (Vault, AWS Secrets Manager)
[ ] Environment-specific configs (dev, staging, prod)
[ ] Default values for optional vars
[ ] Error messages for missing required vars
[ ] No hardcoded secrets in code
[ ] CI/CD env vars configured
[ ] Documentation for all env vars
```

---

## 🔐 PATTERN 1: ENV FILE STRUCTURE

### ✅ Proper .env Structure

```bash
# .env (NEVER commit this file!)

# ============================================
# APPLICATION
# ============================================
NODE_ENV=development
PORT=3000
APP_NAME=my-app
APP_URL=http://localhost:3000

# ============================================
# DATABASE
# ============================================
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10

# ============================================
# REDIS
# ============================================
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=secret123

# ============================================
# AUTHENTICATION
# ============================================
JWT_SECRET=super-secret-key-change-in-production
JWT_EXPIRES_IN=7d
SESSION_SECRET=another-secret-key

# ============================================
# EXTERNAL APIS
# ============================================
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx

# ============================================
# AWS
# ============================================
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx
AWS_REGION=us-east-1
AWS_S3_BUCKET=my-bucket

# ============================================
# MONITORING
# ============================================
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
LOG_LEVEL=debug
```

### ✅ .env.example (Safe to commit)

```bash
# .env.example (COMMIT this file!)

# ============================================
# APPLICATION
# ============================================
NODE_ENV=development
PORT=3000
APP_NAME=my-app
APP_URL=http://localhost:3000

# ============================================
# DATABASE
# ============================================
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10

# ============================================
# REDIS
# ============================================
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=

# ============================================
# AUTHENTICATION
# ============================================
JWT_SECRET=
JWT_EXPIRES_IN=7d
SESSION_SECRET=

# ============================================
# EXTERNAL APIS (Get from respective dashboards)
# ============================================
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
SENDGRID_API_KEY=

# ============================================
# AWS
# ============================================
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
AWS_S3_BUCKET=

# ============================================
# MONITORING
# ============================================
SENTRY_DSN=
LOG_LEVEL=info
```

---

## ✅ PATTERN 2: ENV VALIDATION WITH ZOD

### Type-Safe Environment

```typescript
// config/env.ts
import { z } from 'zod';

// ⭐ Define schema
const envSchema = z.object({
  // Application
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.string().transform(Number).pipe(z.number().min(1).max(65535)),
  APP_NAME: z.string().min(1),
  APP_URL: z.string().url(),
  
  // Database
  DATABASE_URL: z.string().url(),
  DATABASE_POOL_MIN: z.string().transform(Number).default('2'),
  DATABASE_POOL_MAX: z.string().transform(Number).default('10'),
  
  // Redis
  REDIS_URL: z.string().url(),
  REDIS_PASSWORD: z.string().optional(),
  
  // Authentication
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('7d'),
  SESSION_SECRET: z.string().min(32),
  
  // External APIs
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith('whsec_'),
  SENDGRID_API_KEY: z.string().startsWith('SG.'),
  
  // AWS
  AWS_ACCESS_KEY_ID: z.string().length(20),
  AWS_SECRET_ACCESS_KEY: z.string().length(40),
  AWS_REGION: z.string(),
  AWS_S3_BUCKET: z.string(),
  
  // Monitoring
  SENTRY_DSN: z.string().url().optional(),
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace']).default('info')
});

// ⭐ Validate on startup
export const env = envSchema.parse(process.env);

// ⭐ Type-safe access
export type Env = z.infer<typeof envSchema>;

// Usage in code:
// import { env } from './config/env';
// console.log(env.PORT);  // Type: number
// console.log(env.NODE_ENV);  // Type: 'development' | 'staging' | 'production'
```

### Startup Validation

```typescript
// index.ts
import { env } from './config/env';

// ⭐ Validate immediately on startup
try {
  console.log('✓ Environment variables validated');
  console.log(`✓ Running in ${env.NODE_ENV} mode`);
  console.log(`✓ Server will start on port ${env.PORT}`);
} catch (error) {
  console.error('❌ Invalid environment variables:');
  console.error(error);
  process.exit(1);  // ⭐ Fail fast
}

// Start server
app.listen(env.PORT, () => {
  console.log(`Server running on ${env.APP_URL}`);
});
```

---

## 🔒 PATTERN 3: SECRETS MANAGEMENT

### ❌ NEVER Hardcode Secrets

```typescript
// ❌ BAD: Hardcoded secrets
const stripe = new Stripe('sk_live_xxxxxxxxxxxxx');
const jwt = sign(payload, 'my-secret-key');
const s3 = new S3({
  accessKeyId: 'AKIAXXXXXXXXXXXXX',
  secretAccessKey: 'xxxxxxxxxxxxx'
});

// ✅ GOOD: Use environment variables
import { env } from './config/env';

const stripe = new Stripe(env.STRIPE_SECRET_KEY);
const jwt = sign(payload, env.JWT_SECRET);
const s3 = new S3({
  accessKeyId: env.AWS_ACCESS_KEY_ID,
  secretAccessKey: env.AWS_SECRET_ACCESS_KEY
});
```

### AWS Secrets Manager

```typescript
// config/secrets.ts
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: env.AWS_REGION });

export async function getSecret(secretName: string): Promise<any> {
  try {
    const response = await client.send(
      new GetSecretValueCommand({ SecretId: secretName })
    );
    
    return JSON.parse(response.SecretString!);
  } catch (error) {
    console.error(`Failed to get secret ${secretName}:`, error);
    throw error;
  }
}

// Usage
const dbCredentials = await getSecret('prod/database/credentials');
const apiKeys = await getSecret('prod/api-keys');
```

### HashiCorp Vault

```typescript
// config/vault.ts
import vault from 'node-vault';

const client = vault({
  endpoint: env.VAULT_ADDR,
  token: env.VAULT_TOKEN
});

export async function getVaultSecret(path: string): Promise<any> {
  try {
    const result = await client.read(path);
    return result.data;
  } catch (error) {
    console.error(`Failed to read from Vault: ${path}`, error);
    throw error;
  }
}

// Usage
const secrets = await getVaultSecret('secret/data/myapp/prod');
```

---

## 🌍 PATTERN 4: ENVIRONMENT-SPECIFIC CONFIGS

### Config Files

```typescript
// config/index.ts
import { env } from './env';

interface Config {
  app: {
    name: string;
    url: string;
    port: number;
  };
  database: {
    url: string;
    poolMin: number;
    poolMax: number;
    ssl: boolean;
  };
  redis: {
    url: string;
    password?: string;
  };
  features: {
    enableNewUI: boolean;
    enableBetaFeatures: boolean;
  };
  rateLimit: {
    windowMs: number;
    max: number;
  };
}

// ⭐ Environment-specific configs
const configs: Record<string, Config> = {
  development: {
    app: {
      name: env.APP_NAME,
      url: env.APP_URL,
      port: env.PORT
    },
    database: {
      url: env.DATABASE_URL,
      poolMin: env.DATABASE_POOL_MIN,
      poolMax: env.DATABASE_POOL_MAX,
      ssl: false  // ⭐ No SSL in dev
    },
    redis: {
      url: env.REDIS_URL,
      password: env.REDIS_PASSWORD
    },
    features: {
      enableNewUI: true,  // ⭐ Enable in dev
      enableBetaFeatures: true
    },
    rateLimit: {
      windowMs: 60000,
      max: 1000  // ⭐ Relaxed in dev
    }
  },
  
  production: {
    app: {
      name: env.APP_NAME,
      url: env.APP_URL,
      port: env.PORT
    },
    database: {
      url: env.DATABASE_URL,
      poolMin: env.DATABASE_POOL_MIN,
      poolMax: env.DATABASE_POOL_MAX,
      ssl: true  // ⭐ SSL required in prod
    },
    redis: {
      url: env.REDIS_URL,
      password: env.REDIS_PASSWORD
    },
    features: {
      enableNewUI: false,  // ⭐ Disable in prod
      enableBetaFeatures: false
    },
    rateLimit: {
      windowMs: 60000,
      max: 100  // ⭐ Strict in prod
    }
  }
};

// ⭐ Export config for current environment
export const config = configs[env.NODE_ENV];
```

---

## 🔧 PATTERN 5: TYPE-SAFE ENV ACCESS

### Centralized Config Module

```typescript
// config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32)
});

export const env = envSchema.parse(process.env);

// ❌ BAD: Direct process.env access (no type safety)
// app.ts
const port = process.env.PORT;  // Type: string | undefined
const dbUrl = process.env.DATABASE_URL;  // Type: string | undefined

// ✅ GOOD: Centralized config (type-safe)
// app.ts
import { env } from './config/env';

const port = env.PORT;  // Type: number
const dbUrl = env.DATABASE_URL;  // Type: string
```

---

## 📊 QUICK REFERENCE

| Aspect | Standard | Example |
|--------|----------|---------|
| **File Name** | .env (gitignored) | `.env` |
| **Example File** | .env.example (committed) | `.env.example` |
| **Validation** | Zod schema on startup | `envSchema.parse()` |
| **Access** | Centralized config module | `import { env }` |
| **Secrets** | Never hardcode | Use env vars |
| **Sensitive Data** | Secrets manager | AWS Secrets Manager |
| **Type Safety** | Zod + TypeScript | `z.infer<typeof schema>` |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Committing .env

```bash
# ❌ BAD: .env committed to Git
git add .env
git commit -m "Add config"

# ✅ GOOD: .env in .gitignore
echo ".env" >> .gitignore
git add .env.example
git commit -m "Add env example"
```

### ❌ Mistake 2: No Validation

```typescript
// ❌ BAD: No validation (crashes at runtime)
const port = parseInt(process.env.PORT!);
app.listen(port);  // Crashes if PORT is invalid

// ✅ GOOD: Validate on startup
const env = envSchema.parse(process.env);
app.listen(env.PORT);  // Fails fast with clear error
```

### ❌ Mistake 3: Hardcoded Secrets

```typescript
// ❌ BAD
const apiKey = 'sk_live_xxxxxxxxxxxxx';

// ✅ GOOD
const apiKey = env.STRIPE_SECRET_KEY;
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Setup environment configuration for Node.js app with:
- Zod validation for all env vars
- Type-safe access (no process.env)
- .env.example file
- Secrets management (AWS Secrets Manager)
- Environment-specific configs (dev, prod)
- Fail fast on startup if invalid"
```

### AI Should

1. ✅ Create Zod schema for validation
2. ✅ Add .env.example (no secrets)
3. ✅ Add .env to .gitignore
4. ✅ Create centralized config module
5. ✅ Validate on startup (fail fast)
6. ✅ Use type-safe env access
7. ✅ Never hardcode secrets

---

## 🔗 RELATED SKILLS

- `security-middleware-stack.md` - Secrets security
- `error-handling-patterns.md` - Config error handling
- `logging-standards.md` - Log config issues

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium  
**Impact:** Critical (security & reliability)
