---
name: "Locais Conhecidos para Deteccao de Skills"
tags: ["adicionando", "all", "antigravity", "c:", "com", "conhecidos", "deteccao", "escaneados", "estendidos", "frontend", "gemini", "ignorados", "installer", "known", "<YOUR_USERNAME>", "locais", "locations", "novos", "padrao", "padroes"]
tier: 2
risk: "medium"
estimated_tokens: 333
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
---
# Locais Conhecidos para Deteccao de Skills

O `detect_skills.py` escaneia os seguintes locais para encontrar skills nao-instaladas:

## Locais Padrao (sempre escaneados)

| Local | Motivo |
|-------|--------|
| `%USERPROFILE%\Desktop` | Usuario pode ter criado skill na area de trabalho |
| `%USERPROFILE%\Downloads` | Skills baixadas da internet |
| `%USERPROFILE%\Documents` | Documentos com skills criadas manualmente |
| `%TEMP%` | skill-creator pode deixar workspaces em temp |

## Locais Estendidos (com --all)

| Local | Motivo |
|-------|--------|
| `%USERPROFILE%` | Raiz do usuario |
| `%USERPROFILE%\Projects` | Projetos comuns |
| `%USERPROFILE%\dev` | Diretorio de desenvolvimento |
| `%USERPROFILE%\repos` | Repositorios git |
| `%USERPROFILE%\workspace` | Workspaces |
| `%USERPROFILE%\code` | Codigo-fonte |
| `C:\temp` | Temp alternativo |
| `C:\projects` | Projetos em raiz |

## Padroes Reconhecidos

- `*-workspace/v*/skill/SKILL.md` — Workspace do skill-creator
- Qualquer diretorio com `SKILL.md` com frontmatter YAML valido

## Locais Ignorados

- `C:\Users\renat\skills\` (ja instalados)
- `.git/`, `__pycache__/`, `node_modules/`, `.venv/`, `venv/`
- Profundidade maxima: 5 niveis

## Adicionando Novos Locais

Para escanear um local especifico:

```bash
python detect_skills.py --path "C:\meu\diretorio"
```
