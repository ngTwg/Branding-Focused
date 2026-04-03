---
name: "Authentication Patterns"
tags: ["antigravity", "api", "auth", "authentication", "backend", "c:", "frontend", "gemini", "guide", "jwt", "<YOUR_USERNAME>", "patterns", "principles", "selection", "users"]
tier: 2
risk: "medium"
estimated_tokens: 136
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.55
---
# Authentication Patterns

> Choose auth pattern based on use case.

## Selection Guide

| Pattern | Best For |
|---------|----------|
| **JWT** | Stateless, microservices |
| **Session** | Traditional web, simple |
| **OAuth 2.0** | Third-party integration |
| **API Keys** | Server-to-server, public APIs |
| **Passkey** | Modern passwordless (2025+) |

## JWT Principles

```
Important:
├── Always verify signature
├── Check expiration
├── Include minimal claims
├── Use short expiry + refresh tokens
└── Never store sensitive data in JWT
```

## Request Schema Validation

```typescript
import { z } from 'zod';

export const loginSchema = z.object({
	email: z.string().email(),
	password: z.string().min(8).max(128),
	deviceId: z.string().min(8).max(128).optional(),
});

export const refreshSchema = z.object({
	refreshToken: z.string().min(32),
});

export type LoginInput = z.infer<typeof loginSchema>;
```

## Error Handling Contract

```json
{
	"error": {
		"code": "AUTH_INVALID_TOKEN",
		"message": "Token is invalid or expired",
		"requestId": "req_01HS8...",
		"retryable": false
	}
}
```

```typescript
export function authError(code: string, message: string, requestId: string) {
	return {
		error: {
			code,
			message,
			requestId,
			retryable: code === 'AUTH_PROVIDER_UNAVAILABLE',
		},
	};
}
```

## Prisma Refresh Token Pattern

```prisma
model RefreshToken {
	id         String   @id @default(cuid())
	userId     String
	tokenHash  String   @unique
	expiresAt  DateTime
	revokedAt  DateTime?
	createdAt  DateTime @default(now())

	user User @relation(fields: [userId], references: [id], onDelete: Cascade)

	@@index([userId, revokedAt])
	@@index([expiresAt])
}
```

## NestJS Validation and Guard Example

```typescript
import { IsEmail, IsString, MinLength } from 'class-validator';
import { ValidationPipe, Controller, Post, Body, UseGuards } from '@nestjs/common';

class LoginDto {
	@IsEmail()
	email!: string;

	@IsString()
	@MinLength(8)
	password!: string;
}

@Controller('auth')
export class AuthController {
	@Post('login')
	login(@Body(new ValidationPipe({ whitelist: true })) body: LoginDto) {
		return { ok: true, email: body.email };
	}

	@Post('refresh')
	@UseGuards(RefreshTokenGuard)
	refresh() {
		return { rotated: true };
	}
}
```

## Implementation Links

- Prisma model and token lifecycle: see `antigravity/skills/backend/authentication.md`.
- JWT and OAuth hardening examples: see `antigravity/skills/backend/api-security-best-practices/SKILL.md`.
- Provider-specific auth selection: see `antigravity/skills/backend/api-patterns/SKILL.md`.
