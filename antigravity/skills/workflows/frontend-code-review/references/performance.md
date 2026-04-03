---
name: "Rule Catalog — Performance"
tags: ["antigravity", "c:", "catalog", "code", "complex", "data", "description", "flow", "frontend", "gemini", "<YOUR_USERNAME>", "memoization", "performance", "prop", "react", "references", "review", "rule", "usage", "users"]
tier: 2
risk: "medium"
estimated_tokens: 231
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.63
---
# Rule Catalog — Performance

## React Flow data usage

IsUrgent: True
Category: Performance

### Description

When rendering React Flow, prefer `useNodes`/`useEdges` for UI consumption and rely on `useStoreApi` inside callbacks that mutate or read node/edge state. Avoid manually pulling Flow data outside of these hooks.

## Complex prop memoization

IsUrgent: True
Category: Performance

### Description

Wrap complex prop values (objects, arrays, maps) in `useMemo` prior to passing them into child components to guarantee stable references and prevent unnecessary renders.

Update this file when adding, editing, or removing Performance rules so the catalog remains accurate.

Wrong:

```tsx
<HeavyComp
    config={{
        provider: ...,
        detail: ...
    }}
/>
```

Right:

```tsx
const config = useMemo(() => ({
    provider: ...,
    detail: ...
}), [provider, detail]);

<HeavyComp
    config={config}
/>
```
