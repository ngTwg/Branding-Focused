---
name: "Theme Organization and Shared Styles"
tags: ["and", "antigravity", "avalonia", "avoiding", "c:", "frontend", "gemini", "icons", "layout", "<YOUR_USERNAME>", "organization", "redundancy", "resources", "shared", "specialized", "structure", "styles", "theme", "themes", "users"]
tier: 2
risk: "medium"
estimated_tokens: 462
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.65
---
# Theme Organization and Shared Styles

Efficient theme organization is key to avoiding redundant XAML and ensuring visual consistency.

## 🏗️ Structure

Follow the pattern from Angor:

1.  **Colors & Brushes**: Define in a dedicated `Colors.axaml`. Use `DynamicResource` to support theme switching.
2.  **Styles**: Group styles by category (e.g., `Buttons.axaml`, `Containers.axaml`, `Typography.axaml`).
3.  **App-wide Theme**: Aggregate all styles in a main `Theme.axaml`.

## 🎨 Avoiding Redundancy

Instead of setting properties directly on elements:

```xml
<!-- ❌ BAD: Redundant properties -->
<HeaderedContainer CornerRadius="10" BorderThickness="1" BorderBrush="Blue" Background="LightBlue" />
<HeaderedContainer CornerRadius="10" BorderThickness="1" BorderBrush="Blue" Background="LightBlue" />

<!-- ✅ GOOD: Use Classes and Styles -->
<HeaderedContainer Classes="BlueSection" />
<HeaderedContainer Classes="BlueSection" />
```

Define the style in a shared `axaml` file:

```xml
<Style Selector="HeaderedContainer.BlueSection">
    <Setter Property="CornerRadius" Value="10" />
    <Setter Property="BorderThickness" Value="1" />
    <Setter Property="BorderBrush" Value="{DynamicResource Accent}" />
    <Setter Property="Background" Value="{DynamicResource SurfaceSubtle}" />
</Style>
```

## 🧩 Shared Icons and Resources

Centralize icon definitions and other shared resources in `Icons.axaml` and include them in the `MergedDictionaries` of your theme or `App.axaml`.

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <MergeResourceInclude Source="UI/Themes/Styles/Containers.axaml" />
            <MergeResourceInclude Source="UI/Shared/Resources/Icons.axaml" />
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```
