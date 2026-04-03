---
name: "⚙️ Skill: Write Infrastructure and DevOps Configs"
tags: ["activation", "and", "antigravity", "benchmark", "c:", "configs", "devops", "execution", "frontend", "gemini", "infrastructure", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task"]
tier: 3
risk: "medium"
estimated_tokens: 274
tools_needed: ["ansible", "docker", "git", "markdown", "terminal", "terraform"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# ⚙️ Skill: Write Infrastructure and DevOps Configs

> **PURPOSE:** Create robust CI/CD, IaC, and system configuration files.
> **CATEGORY:** DevOps
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS
- Keywords: `CI/CD`, `Dockerfile`, `GitHub Actions`, `Terraform`, `Ansible`, `deployment config`.
- Task: Setting up a pipeline, containerizing a service, or managing secrets.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Environment Mapping**: Dev -> Staging -> Prod requirements.
2. **Step Selection**: Build -> Test -> Security Scan -> Deploy.
3. **Secret Handling**: Use env vars or secret managers (Vault, GitHub Secrets).
4. **Drafting**: Write clean YAML/HCL with logic.
5. **Validation**: Anticipate and handle common environment failures.

---

## 📝 OUTPUT SIGNATURE
- Configuration files (YAML, Dockerfile, etc.).
- Setup instructions.
- (Optional) Mermaid diagram for the pipeline.

---

## 🧪 BENCHMARK TASK
- **Input**: "Create a GitHub Action to deploy this Next.js app to Vercel."
- **Output**: `.github/workflows/deploy.yml` with: Trigger on push -> Build -> Vercel login -> Deployment.
