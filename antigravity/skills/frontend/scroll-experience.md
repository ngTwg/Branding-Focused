---
name: "📜 Skill: Scroll Experience"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "experience", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "scroll", "signals", "signature", "skill", "steps", "sub", "task", "users"]
tier: 3
risk: "medium"
estimated_tokens: 354
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 📜 Skill: Scroll Experience

> **PURPOSE:** Design and build engaging, scroll-driven visual narratives and interactions.
> **CATEGORY:** Frontend
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `scrollytelling`, `parallax`, `on-scroll animations`, `sticky sections`.
- Goal: Telling stories through scroll (e.g., Apple-style product pages).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify segments of the story/experience (e.g., Intro -> Feature 1 -> Feature 2).
2. **Animation Strategy**: Choose between CSS `scroll-timeline` (experimental) or JS libraries (`framer-motion`, `GSAP`).
3. **Trigger Logic**: define when animations start/end (e.g., `viewport`, `offset`).
4. **Implementation**: Use `useScroll` (framer-motion) or `ScrollTrigger` (GSAP) for binding state to scroll position.
5. **Aesthetics Pass**: Apply: Parallax depth, Smooth pinning, Fade-in/out, Type-reveal on scroll.
6. **Accessibility**: Ensure "Prefers reduced motion" users have a working, non-animated fallback.

---

## 📝 OUTPUT SIGNATURE

- Interactive scrollytelling artifacts (React/Next/HTML).
- Parallax section implementations.
- Progress bar and scroll-indicator components.

---

## 🧪 BENCHMARK TASK

- **Input**: "Build a parallax product landing page with sticky features."
- **Output**: Section 1 (Sticky Hero) -> Section 2 (Fade-in features) -> Section 3 (Scroll-progress animation).
