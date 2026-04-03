---
name: "frontend-patterns"
tags: ["antigravity", "c:", "component", "components", "composition", "compound", "core", "custom", "dev", "development", "frontend", "gemini", "hooks", "inheritance", "<YOUR_USERNAME>", "over", "patterns", "rendering", "slim", "specialized"]
tier: 2
risk: "medium"
estimated_tokens: 582
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.67
description: "Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices."
---
# Frontend Development Patterns (v6.5.0-SLIM)

Modern frontend patterns for React, Next.js, and performant user interfaces.

## Component Patterns

### 1. Composition Over Inheritance
- Build complex UI by combining smaller, specialized components.
- Use `Card`, `CardHeader`, `CardBody` pattern.

### 2. Compound Components
- Manage shared state implicitly between parent and children (Tabs, Modals, Accordions).

### 3. Rendering Patterns
- **Conditional Rendering:** Clear and concise. Avoid "ternary hell."
- **Render Props:** Define what is rendered by passing a function as a prop for more control over display.

## Custom Hooks Patterns
- **useToggle/useBoolean:** Manage basic state toggling.
- **useQuery:** Encapsulate async data fetching, loading, and error states.
- **useDebounce:** Limit rate of updates for search and filters.

## State Management Patterns
- **Context + Reducer:** Local application state (the "Context" for a specific feature).
- **Zustand (2025 Standard):** Minimal, high-performance state management for larger apps.

## Performance Optimization
- **Memoization:** Use `useMemo` for expensive computations and `useCallback` for functions passed to children.
- **React.memo:** Prevent unnecessary re-renders of pure components.
- **Lazy Loading:** Use `lazy` and `Suspense` for heavy charts, backgrounds, and routes.
- **Virtualization:** Use `@tanstack/react-virtual` for lists with 1,000+ items.

## Form Handling
- **Controlled vs Uncontrolled:** Controlled for validation; Uncontrolled for performance.
- **Validation:** Use `Zod` schema integration.

## UI & Accessibility
- **Error Boundaries:** Catch and handle runtime errors in component trees.
- **Animations:** Use `Framer Motion` for smooth transitions and gesture support.
- **Keyboard Navigation:** Trap focus in modals and enable full keyboard access for interactive elements.
- **ARIA Roles:** Use semantic HTML and `aria-*` tags for screen reader support.

## Project Structure
- Use `app/`, `components/`, `hooks/`, `lib/`, `types/`, and `styles/` organizational structure.
- PascalCase for components (`Button.tsx`), camelCase for hooks and utils (`useAuth.ts`).
