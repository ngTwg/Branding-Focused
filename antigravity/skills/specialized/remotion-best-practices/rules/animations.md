---
name: "animations"
tags: ["animations, transitions, frames, useCurrentFrame"]
tier: 1
risk: "medium"
estimated_tokens: 197
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.52
description: "Fundamental animation skills for Remotion"
metadata: ""
---
All animations MUST be driven by the `useCurrentFrame()` hook.  
Write animations in seconds and multiply them by the `fps` value from `useVideoConfig()`.

```tsx
import { useCurrentFrame } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: 'clamp',
  });
 
  return (
    <div style={{ opacity }}>Hello World!</div>
  );
};
```

CSS transitions or animations are FORBIDDEN - they will not render correctly.  
Tailwind animation class names are FORBIDDEN - they will not render correctly.  
