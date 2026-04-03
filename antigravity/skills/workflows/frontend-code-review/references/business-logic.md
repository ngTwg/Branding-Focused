---
name: "Rule Catalog — Business Logic"
tags: ["antigravity", "business", "c:", "can", "catalog", "code", "components", "description", "fix", "frontend", "gemini", "<YOUR_USERNAME>", "logic", "node", "references", "review", "rule", "suggested", "use", "users"]
tier: 2
risk: "medium"
estimated_tokens: 154
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.55
---
# Rule Catalog — Business Logic

## Can't use workflowStore in Node components

IsUrgent: True

### Description

File path pattern of node components: `web/app/components/workflow/nodes/[nodeName]/node.tsx`

Node components are also used when creating a RAG Pipe from a template, but in that context there is no workflowStore Provider, which results in a blank screen. [This Issue](https://github.com/langgenius/dify/issues/29168) was caused by exactly this reason.

### Suggested Fix

Use `import { useNodes } from 'reactflow'` instead of `import useNodes from '@/app/components/workflow/store/workflow/use-nodes'`.
