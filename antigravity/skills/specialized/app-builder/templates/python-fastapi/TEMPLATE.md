---
name: "python-fastapi"
tags: ["antigravity", "api", "app", "builder", "c:", "concepts", "directory", "fastapi", "frontend", "gemini", "key", "<YOUR_USERNAME>", "python", "setup", "specialized", "stack", "steps", "structure", "tech", "template"]
tier: 2
risk: "medium"
estimated_tokens: 420
tools_needed: ["markdown", "pytest", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "FastAPI REST API template principles. SQLAlchemy, Pydantic, Alembic."
---
# FastAPI API Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.11+ |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Auth | JWT + passlib |

---

## Directory Structure

```
project-name/
├── alembic/             # Migrations
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── database.py      # DB connection
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # API routes
│   ├── services/        # Business logic
│   ├── dependencies/    # DI
│   └── utils/
├── tests/
├── .env.example
└── requirements.txt
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Async | async/await throughout |
| Dependency Injection | FastAPI Depends |
| Pydantic v2 | Validation + serialization |
| SQLAlchemy 2.0 | Async sessions |

---

## API Structure

| Layer | Responsibility |
|-------|---------------|
| Routers | HTTP handling |
| Dependencies | Auth, validation |
| Services | Business logic |
| Models | Database entities |
| Schemas | Request/response |

---

## Setup Steps

1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install fastapi uvicorn sqlalchemy alembic pydantic`
4. Create `.env`
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload`

---

## Best Practices

- Use async everywhere
- Pydantic v2 for validation
- SQLAlchemy 2.0 async sessions
- Alembic for migrations
- pytest-asyncio for tests
