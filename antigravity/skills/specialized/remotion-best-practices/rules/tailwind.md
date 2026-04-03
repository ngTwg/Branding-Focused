---
name: "tailwind"
tags: ["antigravity", "best", "c:", "frontend", "gemini", "<YOUR_USERNAME>", "practices", "remotion", "rules", "specialized", "tailwind", "users"]
tier: 2
risk: "medium"
estimated_tokens: 128
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.47
description: "Using TailwindCSS in Remotion."
metadata: ""
---
You can and should use TailwindCSS in Remotion, if TailwindCSS is installed in the project.

Don't use `transition-*` or `animate-*` classes - always animate using the `useCurrentFrame()` hook.  

Tailwind must be installed and enabled first in a Remotion project - fetch  https://www.remotion.dev/docs/tailwind using WebFetch for instructions.
