<#
.SYNOPSIS
    Bundle Activator — sickn33 External Skill Bundles
.DESCRIPTION
    Activate/Deactivate sickn33 bundles mà KHÔNG ảnh hưởng ngTwg native skills.
    Đây là external layer — không bao giờ ghi đè files của ngTwg.
.PARAMETER Activate
    Bundle name(s) để activate (comma-separated)
.PARAMETER Deactivate
    Bundle name(s) để deactivate
.PARAMETER Target
    Destination directory (default: current skills dir)
.PARAMETER List
    Liệt kê tất cả 38 bundles
.PARAMETER Status
    Xem bundles đang active
.EXAMPLE
    .\activate-bundle.ps1 -Activate essentials
    .\activate-bundle.ps1 -Activate security-developer -Target "C:\path\to\skills"
    .\activate-bundle.ps1 -Deactivate seo-specialist
    .\activate-bundle.ps1 -List
    .\activate-bundle.ps1 -Status
#>

param(
    [string]$Activate,
    [string]$Deactivate,
    [string]$Target = "C:\Users\<YOUR_USERNAME>\.gemini\antigravity\external\active-bundles",
    [switch]$List,
    [switch]$Status
)

$BUNDLE_ROOT   = "C:\Users\<YOUR_USERNAME>\.gemini\antigravity\external\sickn33-skills\plugins"
$NGTWG_SKILLS  = "C:\Users\<YOUR_USERNAME>\.gemini\antigravity\skills"
$STATUS_FILE   = "C:\Users\<YOUR_USERNAME>\.gemini\antigravity\external\active-bundles.json"

# ─── GUARD: Never overwrite ngTwg native skills ───────────────────────────────
function Assert-NotNgTwg {
    param([string]$path)
    if ($path -like "*$NGTWG_SKILLS*") {
        Write-Error "❌ BLOCKED: Cannot write to ngTwg native skills directory!"
        exit 1
    }
}

# ─── LOAD/SAVE STATUS ─────────────────────────────────────────────────────────
function Get-Status {
    if (Test-Path $STATUS_FILE) {
        return Get-Content $STATUS_FILE | ConvertFrom-Json
    }
    return @{ active = @(); last_updated = "" }
}

function Save-Status {
    param($status)
    $status.last_updated = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $status | ConvertTo-Json | Set-Content $STATUS_FILE
}

# ─── LIST ─────────────────────────────────────────────────────────────────────
if ($List) {
    Write-Host "`n📦 Available sickn33 Bundles (38 total):" -ForegroundColor Cyan
    $status = Get-Status
    Get-ChildItem $BUNDLE_ROOT -Directory | ForEach-Object {
        $name = $_.Name -replace "antigravity-bundle-", ""
        $skillCount = (Get-ChildItem $_.FullName -File -Recurse -EA SilentlyContinue).Count
        $isActive = $status.active -contains $name
        $marker = if ($isActive) { "●" } else { "○" }
        $color  = if ($isActive) { "Green" } else { "Gray" }
        Write-Host "  $marker [$name] — ~$skillCount files" -ForegroundColor $color
    }
    Write-Host ""
    Write-Host "Legend: ● active  ○ inactive" -ForegroundColor DarkGray
    Write-Host ""
    return
}

# ─── STATUS ───────────────────────────────────────────────────────────────────
if ($Status) {
    $status = Get-Status
    Write-Host "`n📊 Active Bundles:" -ForegroundColor Cyan
    if ($status.active.Count -eq 0) {
        Write-Host "  (none active)"
    } else {
        $status.active | ForEach-Object { Write-Host "  ✅ $_" -ForegroundColor Green }
    }
    Write-Host "  Last updated: $($status.last_updated)"
    Write-Host ""
    return
}

# ─── ACTIVATE ─────────────────────────────────────────────────────────────────
if ($Activate) {
    Assert-NotNgTwg $Target

    # Create destination
    if (-not (Test-Path $Target)) {
        New-Item -ItemType Directory -Path $Target -Force | Out-Null
    }

    $bundleNames = $Activate -split "," | ForEach-Object { $_.Trim() }

    foreach ($bundleName in $bundleNames) {
        $bundleDir = "$BUNDLE_ROOT\antigravity-bundle-$bundleName"

        if (-not (Test-Path $bundleDir)) {
            Write-Host "❌ Bundle '$bundleName' not found in: $BUNDLE_ROOT" -ForegroundColor Red
            Write-Host "   Run: .\activate-bundle.ps1 -List  to see available bundles" -ForegroundColor Yellow
            continue
        }

        Write-Host "`n📦 Activating bundle: $bundleName" -ForegroundColor Cyan

        # Copy bundle contents to target
        $bundleFiles = Get-ChildItem $bundleDir -File -Recurse
        $copied = 0
        foreach ($file in $bundleFiles) {
            $relPath = $file.FullName.Substring($bundleDir.Length)
            $destPath = Join-Path $Target $bundleName
            $destFile = Join-Path $destPath $relPath

            $destDir = Split-Path $destFile -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }

            Copy-Item $file.FullName $destFile -Force
            $copied++
        }

        Write-Host "  ✅ Copied $copied files from bundle '$bundleName'"

        # Update status
        $status = Get-Status
        if ($status.active -notcontains $bundleName) {
            $status.active += $bundleName
            Save-Status $status
        }
    }

    Write-Host "`n✅ Bundle(s) '$Activate' activated → $Target" -ForegroundColor Green
    return
}

# ─── DEACTIVATE ───────────────────────────────────────────────────────────────
if ($Deactivate) {
    $bundleNames = $Deactivate -split "," | ForEach-Object { $_.Trim() }

    foreach ($bundleName in $bundleNames) {
        $bundlePath = Join-Path $Target $bundleName
        if (Test-Path $bundlePath) {
            Remove-Item $bundlePath -Recurse -Force
            Write-Host "  🗑️ Removed: $bundleName" -ForegroundColor Yellow
        } else {
            Write-Host "  ℹ️ '$bundleName' was not active"
        }

        # Update status
        $status = Get-Status
        $status.active = $status.active | Where-Object { $_ -ne $bundleName }
        Save-Status $status
    }

    Write-Host "✅ Deactivated: $Deactivate" -ForegroundColor Green
    return
}

# ─── NO PARAMS ────────────────────────────────────────────────────────────────
Write-Host "`n📦 activate-bundle.ps1 — Usage:" -ForegroundColor Cyan
Write-Host "  -Activate <bundle>   Activate a bundle"
Write-Host "  -Deactivate <bundle> Deactivate a bundle"
Write-Host "  -List                Show all 38 bundles"
Write-Host "  -Status              Show active bundles"
Write-Host ""
Write-Host "Examples:"
Write-Host "  .\activate-bundle.ps1 -Activate essentials"
Write-Host "  .\activate-bundle.ps1 -Activate 'security-developer,seo-specialist'"
Write-Host "  .\activate-bundle.ps1 -List"
Write-Host ""
