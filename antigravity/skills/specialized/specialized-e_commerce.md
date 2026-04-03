---
name: "Specialized Skills - Category: E_COMMERCE"
tags: ["antigravity", "app", "authentication", "c:", "category", "commerce", "e", "e_commerce", "frontend", "gemini", "hubspot", "integration", "<YOUR_USERNAME>", "oauth", "patterns", "private", "skills", "specialized", "token", "users"]
tier: 2
risk: "medium"
estimated_tokens: 3401
tools_needed: ["git", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# Specialized Skills - Category: E_COMMERCE

> **System Integration: Antigravity v6.5.0-SLIM**

---

<a id="hubspotintegration"></a>

## Hubspot Integration

---
name: hubspot-integration
description: "Expert patterns for HubSpot CRM integration including OAuth authentication, CRM objects, associations, batch operations, webhooks, and custom objects. Covers Node.js and Python SDKs. Use when: hubspot, hubspot api, hubspot crm, hubspot integration, contacts api."
source: vibeship-spawner-skills (Apache 2.0)
---

# HubSpot Integration

## Patterns

### OAuth 2.0 Authentication

Secure authentication for public apps

### Private App Token

Authentication for single-account integrations

### CRM Object CRUD Operations

Create, read, update, delete CRM records

## Anti-Patterns

### ❌ Using Deprecated API Keys

### ❌ Individual Requests Instead of Batch

### ❌ Polling Instead of Webhooks

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |




---

<a id="notiontemplatebusiness"></a>

## Notion Template Business

---
name: notion-template-business
description: "Expert in building and selling Notion templates as a business - not just making templates, but building a sustainable digital product business. Covers template design, pricing, marketplaces, marketing, and scaling to real revenue. Use when: notion template, sell templates, digital product, notion business, gumroad."
source: vibeship-spawner-skills (Apache 2.0)
---

# Notion Template Business

**Role**: Template Business Architect

You know templates are real businesses that can generate serious income.
You've seen creators make six figures selling Notion templates. You
understand it's not about the template - it's about the problem it solves.
You build systems that turn templates into scalable digital products.

## Capabilities

- Notion template design
- Template pricing strategies
- Gumroad/Lemon Squeezy setup
- Template marketing
- Notion marketplace strategy
- Template support systems
- Template documentation
- Bundle strategies

## Patterns

### Template Design

Creating templates people pay for

**When to use**: When designing a Notion template

```javascript
## Template Design

### What Makes Templates Sell
| Factor | Why It Matters |
|--------|----------------|
| Solves specific problem | Clear value proposition |
| Beautiful design | First impression, shareability |
| Easy to customize | Users make it their own |
| Good documentation | Reduces support, increases satisfaction |
| Comprehensive | Feels worth the price |

### Template Structure
```
Template Package:
├── Main Template
│   ├── Dashboard (first impression)
│   ├── Core Pages (main functionality)
│   ├── Supporting Pages (extras)
│   └── Examples/Sample Data
├── Documentation
│   ├── Getting Started Guide
│   ├── Feature Walkthrough
│   └── FAQ
└── Bonus
    ├── Icon Pack
    └── Color Themes
```

### Design Principles
- Clean, consistent styling
- Clear hierarchy and navigation
- Helpful empty states
- Example data to show possibilities
- Mobile-friendly views

### Template Categories That Sell
| Category | Examples |
|----------|----------|
| Productivity | Second brain, task management |
| Business | CRM, project management |
| Personal | Finance tracker, habit tracker |
| Education | Study system, course notes |
| Creative | Content calendar, portfolio |
```

### Pricing Strategy

Pricing Notion templates for profit

**When to use**: When setting template prices

```javascript
## Template Pricing

### Price Anchoring
| Tier | Price Range | What to Include |
|------|-------------|-----------------|
| Basic | $15-29 | Core template only |
| Pro | $39-79 | Template + extras |
| Ultimate | $99-199 | Everything + updates |

### Pricing Factors
```
Value created:
- Time saved per month × 12 months
- Problems solved
- Comparable products cost

Example:
- Saves 5 hours/month
- 5 hours × $50/hour × 12 = $3000 value
- Price at $49-99 (1-3% of value)
```

### Bundle Strategy
- Individual templates: $29-49
- Bundle of 3-5: $79-129 (30% off)
- All-access: $149-299 (best value)

### Free vs Paid
| Free Template | Purpose |
|---------------|---------|
| Lead magnet | Email list growth |
| Upsell vehicle | "Get the full version" |
| Social proof | Reviews, shares |
| SEO | Traffic to paid |
```

### Sales Channels

Where to sell templates

**When to use**: When setting up sales

```javascript
## Sales Channels

### Platform Comparison
| Platform | Fee | Pros | Cons |
|----------|-----|------|------|
| Gumroad | 10% | Simple, trusted | Higher fees |
| Lemon Squeezy | 5-8% | Modern, lower fees | Newer |
| Notion Marketplace | 0% | Built-in audience | Approval needed |
| Your site | 3% (Stripe) | Full control | Build audience |

### Gumroad Setup
```
1. Create account
2. Add product
3. Upload template (duplicate link)
4. Write compelling description
5. Add preview images/video
6. Set price
7. Enable discounts
8. Publish
```

### Notion Marketplace
- Apply as creator
- Higher quality bar
- Built-in discovery
- Lower individual prices
- Good for volume

### Your Own Site
- Use Lemon Squeezy embed
- Custom landing pages
- Build email list
- Full brand control
```

## Anti-Patterns

### ❌ Building Without Audience

**Why bad**: No one knows about you.
Launch to crickets.
No email list.
No social following.

**Instead**: Build audience first.
Share work publicly.
Give away free templates.
Grow email list.

### ❌ Too Niche or Too Broad

**Why bad**: "Notion template" = too vague.
"Notion for left-handed fishermen" = too niche.
No clear buyer.
Weak positioning.

**Instead**: Specific but sizable market.
"Notion for freelancers"
"Notion for students"
"Notion for small teams"

### ❌ No Support System

**Why bad**: Support requests pile up.
Bad reviews.
Refund requests.
Stressful.

**Instead**: Great documentation.
Video walkthrough.
FAQ page.
Email/chat for premium.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Templates getting shared/pirated | medium | ## Handling Template Piracy |
| Drowning in customer support requests | medium | ## Scaling Template Support |
| All sales from one marketplace | medium | ## Diversifying Sales Channels |
| Old templates becoming outdated | low | ## Template Update Strategy |

## Related Skills

Works well with: `micro-saas-launcher`, `copywriting`, `landing-page-design`, `seo`




---

<a id="plaidfintech"></a>

## Plaid Fintech

---
name: plaid-fintech
description: "Expert patterns for Plaid API integration including Link token flows, transactions sync, identity verification, Auth for ACH, balance checks, webhook handling, and fintech compliance best practices. Use when: plaid, bank account linking, bank connection, ach, account aggregation."
source: vibeship-spawner-skills (Apache 2.0)
---

# Plaid Fintech

## Patterns

### Link Token Creation and Exchange

Create a link_token for Plaid Link, exchange public_token for access_token.
Link tokens are short-lived, one-time use. Access tokens don't expire but
may need updating when users change passwords.


### Transactions Sync

Use /transactions/sync for incremental transaction updates. More efficient
than /transactions/get. Handle webhooks for real-time updates instead of
polling.


### Item Error Handling and Update Mode

Handle ITEM_LOGIN_REQUIRED errors by putting users through Link update mode.
Listen for PENDING_DISCONNECT webhook to proactively prompt users.


## Anti-Patterns

### ❌ Storing Access Tokens in Plain Text

### ❌ Polling Instead of Webhooks

### ❌ Ignoring Item Errors

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |




---

<a id="salesforcedevelopment"></a>

## Salesforce Development

---
name: salesforce-development
description: "Expert patterns for Salesforce platform development including Lightning Web Components (LWC), Apex triggers and classes, REST/Bulk APIs, Connected Apps, and Salesforce DX with scratch orgs and 2nd generation packages (2GP). Use when: salesforce, sfdc, apex, lwc, lightning web components."
source: vibeship-spawner-skills (Apache 2.0)
---

# Salesforce Development

## Patterns

### Lightning Web Component with Wire Service

Use @wire decorator for reactive data binding with Lightning Data Service
or Apex methods. @wire fits LWC's reactive architecture and enables
Salesforce performance optimizations.


### Bulkified Apex Trigger with Handler Pattern

Apex triggers must be bulkified to handle 200+ records per transaction.
Use handler pattern for separation of concerns, testability, and
recursion prevention.


### Queueable Apex for Async Processing

Use Queueable Apex for async processing with support for non-primitive
types, monitoring via AsyncApexJob, and job chaining. Limit: 50 jobs
per transaction, 1 child job when chaining.


## Anti-Patterns

### ❌ SOQL Inside Loops

### ❌ DML Inside Loops

### ❌ Hardcoding IDs

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |




---

<a id="shopifyapps"></a>

## Shopify Apps

---
name: shopify-apps
description: "Expert patterns for Shopify app development including Remix/React Router apps, embedded apps with App Bridge, webhook handling, GraphQL Admin API, Polaris components, billing, and app extensions. Use when: shopify app, shopify, embedded app, polaris, app bridge."
source: vibeship-spawner-skills (Apache 2.0)
---

# Shopify Apps

## Patterns

### React Router App Setup

Modern Shopify app template with React Router

### Embedded App with App Bridge

Render app embedded in Shopify Admin

### Webhook Handling

Secure webhook processing with HMAC verification

## Anti-Patterns

### ❌ REST API for New Apps

### ❌ Webhook Processing Before Response

### ❌ Polling Instead of Webhooks

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | ## Respond immediately, process asynchronously |
| Issue | high | ## Check rate limit headers |
| Issue | high | ## Request protected customer data access |
| Issue | medium | ## Use TOML only (recommended) |
| Issue | medium | ## Handle both URL formats |
| Issue | high | ## Use GraphQL for all new code |
| Issue | high | ## Use latest App Bridge via script tag |
| Issue | high | ## Implement all GDPR handlers |




---

<a id="stripeintegration"></a>

## Stripe Integration

---
name: stripe-integration
description: "Get paid from day one. Payments, subscriptions, billing portal, webhooks, metered billing, Stripe Connect. The complete guide to implementing Stripe correctly, including all the edge cases that will bite you at 3am.  This isn't just API calls - it's the full payment system: handling failures, managing subscriptions, dealing with dunning, and keeping revenue flowing. Use when: stripe, payments, subscription, billing, checkout."
source: vibeship-spawner-skills (Apache 2.0)
---

# Stripe Integration

You are a payments engineer who has processed billions in transactions.
You've seen every edge case - declined cards, webhook failures, subscription
nightmares, currency issues, refund fraud. You know that payments code must
be bulletproof because errors cost real money. You're paranoid about race
conditions, idempotency, and webhook verification.

## Capabilities

- stripe-payments
- subscription-management
- billing-portal
- stripe-webhooks
- checkout-sessions
- payment-intents
- stripe-connect
- metered-billing
- dunning-management
- payment-failure-handling

## Requirements

- supabase-backend

## Patterns

### Idempotency Key Everything

Use idempotency keys on all payment operations to prevent duplicate charges

### Webhook State Machine

Handle webhooks as state transitions, not triggers

### Test Mode Throughout Development

Use Stripe test mode with real test cards for all development

## Anti-Patterns

### ❌ Trust the API Response

### ❌ Webhook Without Signature Verification

### ❌ Subscription Status Checks Without Refresh

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Not verifying webhook signatures | critical | # Always verify signatures: |
| JSON middleware parsing body before webhook can verify | critical | # Next.js App Router: |
| Not using idempotency keys for payment operations | high | # Always use idempotency keys: |
| Trusting API responses instead of webhooks for payment statu | critical | # Webhook-first architecture: |
| Not passing metadata through checkout session | high | # Always include metadata: |
| Local subscription state drifting from Stripe state | high | # Handle ALL subscription webhooks: |
| Not handling failed payments and dunning | high | # Handle invoice.payment_failed: |
| Different code paths or behavior between test and live mode | high | # Separate all keys: |

## Related Skills

Works well with: `nextjs-supabase-auth`, `supabase-backend`, `webhook-patterns`, `security`


