---
name: "text-animations"
tags: ["typography, text, typewriter, highlighter ken"]
tier: 3
risk: "high"
estimated_tokens: 175
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["data", "analytics"]
quality_score: 0.55
description: "Typography and text animation patterns for Remotion."
metadata: ""
---
## Text animations

Based on `useCurrentFrame()`, reduce the string character by character to create a typewriter effect.

## Typewriter Effect

See [Typewriter](assets/text-animations-typewriter.tsx) for an advanced example with a blinking cursor and a pause after the first sentence.

Always use string slicing for typewriter effects. Never use per-character opacity.

## Word Highlighting

See [Word Highlight](assets/text-animations-word-highlight.tsx) for an example for how a word highlight is animated, like with a highlighter pen.
