---
name: "Overlay and toasts"
tags: ["and", "antigravity", "c:", "choices", "core", "design", "example", "frontend", "gemini", "intent", "keep", "<YOUR_USERNAME>", "overlay", "patterns", "pitfalls", "references", "specialized", "swiftui", "toast", "toasts"]
tier: 2
risk: "medium"
estimated_tokens: 309
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
---
# Overlay and toasts

## Intent

Use overlays for transient UI (toasts, banners, loaders) without affecting layout.

## Core patterns

- Use `.overlay(alignment:)` to place global UI without changing the underlying layout.
- Keep overlays lightweight and dismissible.
- Use a dedicated `ToastCenter` (or similar) for global state if multiple features trigger toasts.

## Example: toast overlay

```swift
struct AppRootView: View {
  @State private var toast: Toast?

  var body: some View {
    content
      .overlay(alignment: .top) {
        if let toast {
          ToastView(toast: toast)
            .transition(.move(edge: .top).combined(with: .opacity))
            .onAppear {
              DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                withAnimation { self.toast = nil }
              }
            }
        }
      }
  }
}
```

## Design choices to keep

- Prefer overlays for transient UI rather than embedding in layout stacks.
- Use transitions and short auto-dismiss timers.
- Keep the overlay aligned to a clear edge (`.top` or `.bottom`).

## Pitfalls

- Avoid overlays that block all interaction unless explicitly needed.
- Don’t stack many overlays; use a queue or replace the current toast.
