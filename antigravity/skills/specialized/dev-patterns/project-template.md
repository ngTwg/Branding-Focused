---
name: "project-template"
tags: ["antigravity", "api", "architecture", "c:", "code", "dev", "file", "frontend", "gemini", "guidelines", "integration", "<YOUR_USERNAME>", "overview", "patterns", "project", "response", "slim", "specialized", "structure", "template"]
tier: 2
risk: "medium"
estimated_tokens: 529
tools_needed: ["docker", "markdown", "playwright", "pytest", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.75
description: "Project-specific guidelines template (Zenith Example). Use as a base for architecture, file structure, and code patterns."
---
# Project Guidelines Template (v6.5.0-SLIM)

Template for defining project-specific architecture, patterns, and workflows.

## 1. Architecture Overview
**Tech Stack:**
- **Frontend:** Next.js 15 (App Router), TypeScript, React, TailwindCSS.
- **Backend:** FastAPI (Python) or Express (TypeScript).
- **Database:** Supabase (PostgreSQL), Prisma ORM.
- **AI:** Claude SDK (Structured Output), OpenAI (Image Gen).
- **Deployment:** Google Cloud Run, Vercel, or Fly.io.

## 2. File Structure
```text
project/
├── frontend/
│   └── src/
│       ├── app/              # Next.js app router
│       ├── components/       # UI/Forms/Layouts
│       ├── hooks/            # useQuery, useAuth
│       └── lib/              # api, utils, constants
├── backend/
│   ├── routers/              # Route handlers
│   ├── services/             # Business logic
│   └── tests/                # pytest / vitest
├── deploy/                   # Docker, CI/CD
└── docs/                     # RFCs, Plans
```

## 3. Code Patterns

### API Response Structure
**TypeScript:**
```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}
```

### AI Integration
**Structured Output Pattern:**
```python
# FastAPI / Claude example
class AnalysisResult(BaseModel):
    summary: str
    confidence: float

# Tool-calling logic
response = client.messages.create(
    tools=[{"name": "analyze", "input_schema": AnalysisResult.model_json_schema()}],
    tool_choice={"type": "tool", "name": "analyze"}
)
```

## 4. Testing Requirements
- **Frontend:** Vitest + React Testing Library (Unit/Component), Playwright (E2E).
- **Backend:** pytest (Async/DB checks).
- **Coverage Target:** 80% on business logic services.

## 5. Deployment Workflow
- **Staging:** Automatic push on PR.
- **Production:** Manual release tag triggers deployment.
- **Environment:** Use `.env.production` for secrets and API endpoints.

---
*Based on Zenith AI Platform patterns.*
