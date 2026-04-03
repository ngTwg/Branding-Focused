---
name: "Controls (Toggle, Slider, Picker)"
tags: ["antigravity", "c:", "controls", "core", "enums", "example", "for", "frontend", "gemini", "intent", "<YOUR_USERNAME>", "patterns", "picker", "references", "sections", "slider", "specialized", "swiftui", "text", "toggle"]
tier: 3
risk: "medium"
estimated_tokens: 419
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.73
---
# Controls (Toggle, Slider, Picker)

## Intent

Use native controls for settings and configuration screens, keeping labels accessible and state bindings clear.

## Core patterns

- Bind controls directly to `@State`, `@Binding`, or `@AppStorage`.
- Prefer `Toggle` for boolean preferences.
- Use `Slider` for numeric ranges and show the current value in a label.
- Use `Picker` for discrete choices; use `.pickerStyle(.segmented)` only for 2–4 options.
- Keep labels visible and descriptive; avoid embedding buttons inside controls.

## Example: toggles with sections

```swift
Form {
  Section("Notifications") {
    Toggle("Mentions", isOn: $preferences.notificationsMentionsEnabled)
    Toggle("Follows", isOn: $preferences.notificationsFollowsEnabled)
    Toggle("Boosts", isOn: $preferences.notificationsBoostsEnabled)
  }
}
```

## Example: slider with value text

```swift
Section("Font Size") {
  Slider(value: $fontSizeScale, in: 0.5...1.5, step: 0.1)
  Text("Scale: \(String(format: \"%.1f\", fontSizeScale))")
    .font(.scaledBody)
}
```

## Example: picker for enums

```swift
Picker("Default Visibility", selection: $visibility) {
  ForEach(Visibility.allCases, id: \.self) { option in
    Text(option.title).tag(option)
  }
}
```

## Design choices to keep

- Group related controls in a `Form` section.
- Use `.disabled(...)` to reflect locked or inherited settings.
- Use `Label` inside toggles to combine icon + text when it adds clarity.

## Pitfalls

- Avoid `.pickerStyle(.segmented)` for large sets; use menu or inline styles instead.
- Don’t hide labels for sliders; always show context.
- Avoid hard-coding colors for controls; use theme tint sparingly.
