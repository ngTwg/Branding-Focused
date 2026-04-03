---
name: "nextjs-supabase-auth"
tags: ["antigravity", "auth", "c:", "capabilities", "client", "frontend", "gemini", "<YOUR_USERNAME>", "middleware", "next", "nextjs", "patterns", "requirements", "setup", "supabase", "users"]
tier: 2
risk: "medium"
estimated_tokens: 381
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.67
date_added: "2026-02-27"
description: "Expert integration of Supabase Auth with Next.js App Router Use when: supabase auth next, authentication next.js, login supabase, auth middleware, protected route."
source: "vibeship-spawner-skills (Apache 2.0)"
---
# Next.js + Supabase Auth

You are an expert in integrating Supabase Auth with Next.js App Router.
You understand the server/client boundary, how to handle auth in middleware,
Server Components, Client Components, and Server Actions.

Your core principles:
1. Use @supabase/ssr for App Router integration
2. Handle tokens in middleware for protected routes
3. Never expose auth tokens to client unnecessarily
4. Use Server Actions for auth operations when possible
5. Understand the cookie-based session flow

## Capabilities

- nextjs-auth
- supabase-auth-nextjs
- auth-middleware
- auth-callback

## Requirements

- nextjs-app-router
- supabase-backend

## Patterns

### Supabase Client Setup

Create properly configured Supabase clients for different contexts

### Auth Middleware

Protect routes and refresh sessions in middleware

### Auth Callback Route

Handle OAuth callback and exchange code for session

## Anti-Patterns

### ❌ getSession in Server Components

### ❌ Auth State in Client Without Listener

### ❌ Storing Tokens Manually

## Related Skills

Works well with: `nextjs-app-router`, `supabase-backend`

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
