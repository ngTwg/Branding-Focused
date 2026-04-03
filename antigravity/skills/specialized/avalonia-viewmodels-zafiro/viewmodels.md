---
name: "ViewModels & Commands"
tags: ["and", "antigravity", "avalonia", "c:", "command", "commands", "creating", "enhanced", "error", "frontend", "gemini", "handling", "<YOUR_USERNAME>", "observation", "reactive", "specialized", "transformation", "users", "viewmodels", "zafiro"]
tier: 2
risk: "medium"
estimated_tokens: 441
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.77
---
# ViewModels & Commands

In a Zafiro-based application, ViewModels should be functional, reactive, and resilient.

## Reactive ViewModels

Use `ReactiveObject` as the base class. Properties should be defined using the `[Reactive]` attribute (from ReactiveUI.SourceGenerators) for brevity.

```csharp
public partial class MyViewModel : ReactiveObject
{
    [Reactive] private string name;
    [Reactive] private bool isBusy;
}
```

### Observation and Transformation

Use `WhenAnyValue` to react to property changes:

```csharp
this.WhenAnyValue(x => x.Name)
    .Select(name => !string.IsNullOrEmpty(name))
    .ToPropertyEx(this, x => x.CanSubmit);
```

## Enhanced Commands

Zafiro uses `IEnhancedCommand`, which extends `ICommand` and `IReactiveCommand` with additional metadata like `Name` and `Text`.

### Creating a Command

Use `ReactiveCommand.Create` or `ReactiveCommand.CreateFromTask` and then `Enhance()` it.

```csharp
public IEnhancedCommand Submit { get; }

public MyViewModel()
{
    Submit = ReactiveCommand.CreateFromTask(OnSubmit, canSubmit)
        .Enhance(text: "Submit Data", name: "SubmitCommand");
}
```

### Error Handling

Use `HandleErrorsWith` to automatically channel command errors to the `NotificationService`.

```csharp
Submit.HandleErrorsWith(uiServices.NotificationService, "Submission Failed")
    .DisposeWith(disposable);
```

## Disposables

Always use a `CompositeDisposable` to manage subscriptions and command lifetimes.

```csharp
public class MyViewModel : ReactiveObject, IDisposable
{
    private readonly CompositeDisposable disposables = new();

    public void Dispose() => disposables.Dispose();
}
```

> [!TIP]
> Use `.DisposeWith(disposables)` on any observable subscription or command to ensure proper cleanup.
