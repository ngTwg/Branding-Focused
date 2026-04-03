---
name: "Use Activity Component for Show/Hide"
tags: ["rendering, activity, visibility, state-preservation"]
tier: 2
risk: "medium"
estimated_tokens: 141
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.52
impact: "MEDIUM"
impactDescription: "preserves state/DOM"
title: "Use Activity Component for Show/Hide"
---
## Use Activity Component for Show/Hide

Use React's `<Activity>` to preserve state/DOM for expensive components that frequently toggle visibility.

**Usage:**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

Avoids expensive re-renders and state loss.
