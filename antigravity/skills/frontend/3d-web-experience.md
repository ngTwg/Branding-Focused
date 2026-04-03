---
name: "🧊 Skill: 3D Web Experience"
tags: ["3d", "activation", "antigravity", "benchmark", "c:", "execution", "experience", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "web"]
tier: 3
risk: "medium"
estimated_tokens: 329
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🧊 Skill: 3D Web Experience

> **PURPOSE:** Expert in building immersive 3D experiences using Three.js, React Three Fiber, and WebGL.
> **CATEGORY:** Frontend
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Three.js`, `React Three Fiber`, `WebGL`, `3D scene`, `Spline`.
- Task: Creating product configurators, 3D landing pages, or interactive 3D portfolios.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Stack Selection**: Choose between Spline (quick), R3F (React-native), or vanilla Three.js (max control).
2. **Model Pipeline**: Reduce poly count (< 100k), bake textures, and export as GLB/GLTF.
3. **Compression**: Use `gltf-transform` (draco/webp) to keep file sizes under 5MB.
4. **Scene Implementation**: Set up Canvas, lighting (ambient/point), and OrbitControls.
5. **Scroll Integration**: Use `ScrollControls` (drei) or GSAP ScrollTrigger for scroll-driven animations.
6. **Optimization**: Implement loading states (Suspense) and fallbacks for low-end mobile.

---

## 📝 OUTPUT SIGNATURE

- 3D Scenes (React components or vanilla JS).
- Optimized 3D model assets.
- Interactive animation logic.

---

## 🧪 BENCHMARK TASK

- **Input**: "Build a 3D spinning product showcase that reacts to scroll."
- **Output**: R3F Canvas -> useGLTF loader -> ScrollControls wrapper -> useFrame rotation logic.
