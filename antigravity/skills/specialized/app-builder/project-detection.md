---
name: "Project Type Detection"
tags: ["antigravity", "app", "builder", "c:", "detection", "frontend", "gemini", "keyword", "<YOUR_USERNAME>", "matrix", "process", "project", "specialized", "type", "users"]
tier: 2
risk: "medium"
estimated_tokens: 330
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# Project Type Detection

> Analyze user requests to determine project type and template.

## Keyword Matrix

| Keywords | Project Type | Template |
|----------|--------------|----------|
| blog, post, article | Blog | astro-static |
| e-commerce, product, cart, payment | E-commerce | nextjs-saas |
| dashboard, panel, management | Admin Dashboard | nextjs-fullstack |
| api, backend, service, rest | API Service | express-api |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | Mobile App (RN) | react-native-app |
| flutter, dart | Mobile App (Flutter) | flutter-app |
| portfolio, personal, cv | Portfolio | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe | SaaS | nextjs-saas |
| landing, promotional, marketing | Landing Page | nextjs-static |
| docs, documentation | Documentation | astro-static |
| extension, plugin, chrome | Browser Extension | chrome-extension |
| desktop, electron | Desktop App | electron-desktop |
| cli, command line, terminal | CLI Tool | cli-tool |
| monorepo, workspace | Monorepo | monorepo-turborepo |

## Detection Process

```
1. Tokenize user request
2. Extract keywords
3. Determine project type
4. Detect missing information → forward to conversation-manager
5. Suggest tech stack
```
