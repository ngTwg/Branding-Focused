---
name: "PowerShell Windows Patterns"
tags: ["antigravity", "c:", "cmdlets", "core", "file", "frontend", "gemini", "<YOUR_USERNAME>", "management", "object", "operations", "overview", "patterns", "pipeline", "powershell", "process", "specialized", "system", "tools", "users"]
tier: 2
risk: "medium"
estimated_tokens: 1352
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.87
---
# PowerShell Windows Patterns

> **Tier:** 1-2  
> **Tags:** `powershell`, `windows`, `shell`, `terminal`, `scripting`  
> **When to Use:** Working on Windows systems, need PowerShell commands, Windows automation

---

## Overview

Essential PowerShell patterns for Windows. Object-based pipeline, cmdlets, scripting, and Windows-specific operations.

---

## 1. Core Cmdlets

### File Operations

| Task | Cmdlet |
|------|--------|
| List files | `Get-ChildItem` or `ls` |
| List all (hidden) | `Get-ChildItem -Force` |
| Find files | `Get-ChildItem -Recurse -Filter "*.js"` |
| File content | `Get-Content file.txt` |
| First N lines | `Get-Content file.txt -Head 20` |
| Last N lines | `Get-Content file.txt -Tail 20` |
| Search in files | `Select-String -Path "*.js" -Pattern "pattern"` |
| File size | `Get-ChildItem \| Measure-Object -Property Length -Sum` |
| Disk usage | `Get-PSDrive` |

---

## 2. Process Management

| Task | Cmdlet |
|------|--------|
| List processes | `Get-Process` |
| Find by name | `Get-Process -Name node` |
| Kill by name | `Stop-Process -Name node -Force` |
| Kill by PID | `Stop-Process -Id 1234 -Force` |
| Find port user | `Get-NetTCPConnection -LocalPort 3000` |
| Start process | `Start-Process npm -ArgumentList "run", "dev"` |

---

## 3. Object Pipeline

PowerShell pipelines pass **objects**, not text:

```powershell
# Get processes, filter, select properties, sort
Get-Process | 
    Where-Object { $_.CPU -gt 100 } |
    Select-Object Name, CPU, WorkingSet |
    Sort-Object CPU -Descending |
    Format-Table -AutoSize
```

### Common Pipeline Cmdlets

| Cmdlet | Purpose |
|--------|---------|
| `Where-Object` | Filter objects |
| `Select-Object` | Select properties |
| `Sort-Object` | Sort objects |
| `Group-Object` | Group by property |
| `Measure-Object` | Calculate stats |
| `ForEach-Object` | Loop over objects |

---

## 4. Environment Variables

| Task | Command |
|------|---------|
| View all | `Get-ChildItem Env:` |
| View one | `$env:PATH` |
| Set temporary | `$env:VAR = "value"` |
| Set permanent (user) | `[Environment]::SetEnvironmentVariable("VAR", "value", "User")` |
| Set permanent (system) | `[Environment]::SetEnvironmentVariable("VAR", "value", "Machine")` |
| Add to PATH | `$env:PATH += ";C:\new\path"` |

---

## 5. Network

| Task | Cmdlet |
|------|---------|
| Download file | `Invoke-WebRequest -Uri "https://example.com/file" -OutFile "file.zip"` |
| API request | `Invoke-RestMethod -Uri "https://api.example.com" -Method Get` |
| POST JSON | `Invoke-RestMethod -Uri $url -Method Post -Body ($json \| ConvertTo-Json) -ContentType "application/json"` |
| Test connection | `Test-NetConnection -ComputerName localhost -Port 3000` |
| Network info | `Get-NetIPAddress` |

---

## 6. Script Template

```powershell
#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$Name = "default"
)

# Error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Functions
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Main
try {
    Write-Info "Starting..."
    # Your logic here
    Write-Info "Done!"
}
catch {
    Write-ErrorMsg $_.Exception.Message
    exit 1
}
```

---

## 7. Common Patterns

### Check if command exists

```powershell
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "Node is installed"
}
```

### Default parameter value

```powershell
param(
    [string]$Name = "default_value"
)
```

### Read file line by line

```powershell
Get-Content file.txt | ForEach-Object {
    Write-Host $_
}
```

### Loop over files

```powershell
Get-ChildItem -Filter "*.js" | ForEach-Object {
    Write-Host "Processing $($_.Name)"
}
```

---

## 8. Differences from Bash

| Task | Bash | PowerShell |
|------|------|------------|
| List files | `ls -la` | `Get-ChildItem` or `ls` |
| Find files | `find . -type f` | `Get-ChildItem -Recurse` |
| Environment | `$VAR` | `$env:VAR` |
| String concat | `"$a$b"` | `"$a$b"` (same) |
| Null check | `if [ -n "$x" ]` | `if ($x)` |
| Pipeline | Text-based | Object-based |

---

## 9. Error Handling

### Try-Catch-Finally

```powershell
try {
    # Risky operation
    $result = Invoke-WebRequest -Uri $url
}
catch [System.Net.WebException] {
    Write-Error "Network error: $_"
}
catch {
    Write-Error "Unexpected error: $_"
}
finally {
    # Cleanup
    Remove-Item -Path $tempFile -ErrorAction SilentlyContinue
}
```

### Error Action Preference

```powershell
$ErrorActionPreference = "Stop"          # Throw on error
$ErrorActionPreference = "Continue"      # Log and continue
$ErrorActionPreference = "SilentlyContinue"  # Ignore errors
```

---

## 10. Execution Policy

```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy (run as admin)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Bypass for single script
powershell -ExecutionPolicy Bypass -File script.ps1
```

---

## Related Skills

- `bash-linux.md` - Linux/macOS equivalent
- `environment-setup-guide.md` - Setting up dev environments
- `file-organizer.md` - File management

---

**Version:** 1.0.0  
**Last Updated:** 2024-03-26  
**Size:** ~5KB
