param(
    [ValidateSet("quick", "stable", "full")]
    [string]$Suite = "stable",
    [switch]$DryRun,
    [int]$TimeoutSec = 0,
    [switch]$AllowFail
)

$ErrorActionPreference = "Stop"
$python = "C:/Users/<YOUR_USERNAME>/.gemini/.venv/Scripts/python.exe"
$args = @("antigravity/scripts/run_benchmark_pack.py", "--suite", $Suite)

if ($DryRun) {
    $args += "--dry-run"
}
if ($TimeoutSec -gt 0) {
    $args += @("--timeout-sec", "$TimeoutSec")
}
if ($AllowFail) {
    $args += "--allow-fail"
}

Write-Host "Running benchmark pack suite: $Suite"
& $python $args
exit $LASTEXITCODE
