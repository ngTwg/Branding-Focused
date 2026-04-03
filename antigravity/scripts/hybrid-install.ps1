<#
.SYNOPSIS
    Hybrid Installer v1.0 — ngTwg PRIMARY + sickn33 External Layer
.DESCRIPTION
    Install ngTwg governance (PRIMARY) + sickn33 bundle (EXTERNAL) vào IDE target.
    ngTwg files được copy TRƯỚC và LUÔN LUÔN — đây là nguyên tắc bất biến.
.PARAMETER Target
    IDE target: gemini | claude | cursor | kiro | roo
.PARAMETER Bundle
    sickn33 bundle name: essentials | full-stack-developer | security-developer | ...
.PARAMETER ListBundles
    Liệt kê tất cả 38 bundles có sẵn
.EXAMPLE
    .\hybrid-install.ps1 -Target gemini -Bundle essentials
    .\hybrid-install.ps1 -Target claude -Bundle security-developer
    .\hybrid-install.ps1 -Target cursor -Bundle full-stack-developer
    .\hybrid-install.ps1 -ListBundles
#>

param(
    [ValidateSet("gemini","claude","cursor","kiro","roo")]
    [string]$Target = "gemini",

    [string]$Bundle = "essentials",

    [switch]$ListBundles,
    [switch]$All
)

$ErrorActionPreference = "Stop"

# ─── PATHS ───────────────────────────────────────────────────────────────────
$NGTWG_ROOT    = "C:\Users\<YOUR_USERNAME>\.gemini\antigravity"
$SICKN33_ROOT  = "C:\Users\<YOUR_USERNAME>\.gemini\antigravity\external\sickn33-skills"
$GEMINI_HOME   = "C:\Users\<YOUR_USERNAME>\.gemini"

$TARGET_PATHS = @{
    gemini = "$GEMINI_HOME\skills"
    claude = "$env:USERPROFILE\.claude\skills"
    cursor = "$pwd\.cursor\rules"
    kiro   = "$pwd\.kiro\steering"
    roo    = "$pwd\.roo\rules"
}

# ─── LIST BUNDLES ─────────────────────────────────────────────────────────────
if ($ListBundles) {
    Write-Host "`n📦 Available sickn33 Bundles (38 total):" -ForegroundColor Cyan
    Get-ChildItem "$SICKN33_ROOT\plugins" -Directory |
        ForEach-Object { Write-Host "  - $($_.Name -replace 'antigravity-bundle-','')" -ForegroundColor Yellow }
    Write-Host ""
    return
}

# ─── RESOLVE TARGET PATH ────────────────────────────────────────────────────
$TargetPath = $TARGET_PATHS[$Target]
Write-Host "`n🚀 Hybrid Installer v1.0" -ForegroundColor Cyan
Write-Host "   Target IDE : $Target"
Write-Host "   Target Path: $TargetPath"
Write-Host "   Bundle     : $Bundle"
Write-Host ""

# Create target directory if needed
if (-not (Test-Path $TargetPath)) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    Write-Host "  📁 Created target directory: $TargetPath"
}

$TargetParent = Split-Path $TargetPath -Parent

# ─── STEP 1: ngTwg GOVERNANCE (PRIMARY — ALWAYS FIRST) ───────────────────────
Write-Host "Step 1/4: Installing ngTwg governance (PRIMARY)..." -ForegroundColor Green

$govFiles = @(
    @{ src = "$GEMINI_HOME\GEMINI.md";       dst = "$TargetParent\GEMINI.md" },
    @{ src = "$NGTWG_ROOT\CONSTITUTION.md";  dst = "$TargetParent\CONSTITUTION.md" }
)

foreach ($f in $govFiles) {
    if (Test-Path $f.src) {
        Copy-Item $f.src $f.dst -Force
        Write-Host "  ✅ $([System.IO.Path]::GetFileName($f.dst))"
    } else {
        Write-Host "  ⚠️ Not found: $($f.src)"
    }
}

# ─── STEP 2: MASTER_ROUTER + MASTER INVENTORIES ──────────────────────────────
Write-Host "`nStep 2/4: Installing MASTER_ROUTER + Master Inventories..." -ForegroundColor Green

$routerSrc = "$NGTWG_ROOT\skills\MASTER_ROUTER.md"
if (Test-Path $routerSrc) {
    Copy-Item $routerSrc "$TargetPath\MASTER_ROUTER.md" -Force
    Write-Host "  ✅ MASTER_ROUTER.md"
}

# Copy all *-master-inventory.md files
Get-ChildItem "$NGTWG_ROOT\skills" -Recurse -Filter "*master-inventory*" |
    ForEach-Object {
        Copy-Item $_.FullName "$TargetPath\$($_.Name)" -Force
        Write-Host "  ✅ $($_.Name)"
    }

# ─── STEP 3: SICKN33 BRIDGE LAYER ────────────────────────────────────────────
Write-Host "`nStep 3/4: Installing SICKN33 Bridge layer..." -ForegroundColor Green

$bridgeSrc = "$NGTWG_ROOT\external\SICKN33_BRIDGE.md"
if (Test-Path $bridgeSrc) {
    Copy-Item $bridgeSrc "$TargetPath\SICKN33_BRIDGE.md" -Force
    Write-Host "  ✅ SICKN33_BRIDGE.md"
}

$unifiedSrc = "$NGTWG_ROOT\external\UNIFIED_SKILL_INVENTORY.md"
if (Test-Path $unifiedSrc) {
    Copy-Item $unifiedSrc "$TargetPath\UNIFIED_SKILL_INVENTORY.md" -Force
    Write-Host "  ✅ UNIFIED_SKILL_INVENTORY.md"
}

# ─── STEP 4: ACTIVATE sickn33 BUNDLE ─────────────────────────────────────────
Write-Host "`nStep 4/4: Activating sickn33 bundle '$Bundle'..." -ForegroundColor Green

$activateScript = Join-Path $PSScriptRoot "activate-bundle.ps1"
if (Test-Path $activateScript) {
    & $activateScript -Activate $Bundle -Target $TargetPath
} else {
    Write-Host "  ⚠️ activate-bundle.ps1 not found — skipping bundle activation"
}

# ─── VERIFICATION ────────────────────────────────────────────────────────────
Write-Host "`n📊 Verification:" -ForegroundColor Cyan
$installedFiles = (Get-ChildItem $TargetPath -File -Recurse -EA SilentlyContinue).Count
Write-Host "  Files in target: $installedFiles"
Write-Host "  GEMINI.md      : $(Test-Path "$TargetParent\GEMINI.md")"
Write-Host "  MASTER_ROUTER  : $(Test-Path "$TargetPath\MASTER_ROUTER.md")"
Write-Host "  SICKN33_BRIDGE : $(Test-Path "$TargetPath\SICKN33_BRIDGE.md")"

Write-Host "`n✅ ngTwg PRIMARY + sickn33/$Bundle → $Target" -ForegroundColor Green
Write-Host ""
