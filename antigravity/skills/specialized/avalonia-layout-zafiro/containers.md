---
name: "Semantic Containers"
tags: ["antigravity", "avalonia", "c:", "card", "containers", "edgepanel", "gemini", "headeredcontainer", "key", "layout", "<YOUR_USERNAME>", "properties", "security", "semantic", "slots", "specialized", "users", "zafiro"]
tier: 2
risk: "medium"
estimated_tokens: 386
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["security", "compliance"]
quality_score: 0.71
---
# Semantic Containers

Using the right container for the data type simplifies XAML and improves maintainability. `Zafiro.Avalonia` provides specialized controls for common layout patterns.

## 📦 HeaderedContainer

Prefer `HeaderedContainer` over a `Border` or `Grid` when a section needs a title or header.

```xml
<HeaderedContainer Header="Security Settings" Classes="WizardSection">
    <StackPanel>
        <!-- Content here -->
    </StackPanel>
</HeaderedContainer>
```

### Key Properties:
- `Header`: The content or string for the header.
- `HeaderBackground`: Brush for the header area.
- `ContentPadding`: Padding for the content area.

## ↔️ EdgePanel

Use `EdgePanel` to position elements at the edges of a container without complex `Grid` definitions.

```xml
<EdgePanel StartContent="{Icon fa-wallet}" 
           Content="Wallet Balance" 
           EndContent="$1,234.00" />
```

### Slots:
- `StartContent`: Aligned to the left (or beginning).
- `Content`: Fills the remaining space in the middle.
- `EndContent`: Aligned to the right (or end).

## 📇 Card

A simple container for grouping related information, often used inside `HeaderedContainer` or as a standalone element in a list.

```xml
<Card Header="Enter recipient address:">
    <TextBox Text="{Binding Address}" />
</Card>
```

## 📐 Best Practices

- Use `Classes` to apply themed variants (e.g., `Classes="Section"`, `Classes="Highlight"`).
- Customize internal parts of the containers using templates in your styles when necessary, rather than nesting more controls.
