#!/usr/bin/env python3
"""Run reproducible benchmark pack suites and publish structured reports."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
DEFAULT_CONFIG = ROOT / "antigravity" / "config" / "benchmark_pack.json"
REPORTS = ROOT / "antigravity" / "reports"
DOCS = ROOT / "antigravity" / "docs"


@dataclass
class BenchmarkStepResult:
    step_id: str
    description: str
    command: str
    status: str
    exit_code: int
    duration_sec: float
    output_excerpt: str


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_suite_baseline_durations(suite: str, lookback: int) -> list[float]:
    files = sorted(REPORTS.glob("benchmark_pack_*.json"), key=lambda p: p.name)
    durations: list[float] = []

    for path in files[-max(1, lookback) :]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        if str(payload.get("suite", "")) != suite:
            continue
        if bool(payload.get("dry_run", False)):
            continue
        if int(payload.get("failed", 0) or 0) > 0:
            continue

        duration = float(payload.get("duration_sec", 0.0) or 0.0)
        if duration > 0:
            durations.append(duration)

    return durations


def substitute_command(parts: list[str], python_path: Path) -> list[str]:
    return [str(python_path) if part == "{python}" else part for part in parts]


def run_step(step: dict[str, Any], dry_run: bool, timeout_sec: int) -> BenchmarkStepResult:
    step_id = str(step.get("id", "unknown_step"))
    description = str(step.get("description", ""))
    cmd_parts = step.get("command", [])

    if not isinstance(cmd_parts, list) or not all(isinstance(part, str) for part in cmd_parts):
        return BenchmarkStepResult(
            step_id=step_id,
            description=description,
            command="<invalid command>",
            status="failed",
            exit_code=2,
            duration_sec=0.0,
            output_excerpt="Invalid command format in benchmark config",
        )

    cmd = substitute_command(cmd_parts, PYTHON)
    command_str = " ".join(cmd)

    if dry_run:
        return BenchmarkStepResult(
            step_id=step_id,
            description=description,
            command=command_str,
            status="ok",
            exit_code=0,
            duration_sec=0.0,
            output_excerpt="DRY_RUN",
        )

    start = time.perf_counter()
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_sec if timeout_sec > 0 else None,
            check=True,
        )
        output = ((completed.stdout or "") + (completed.stderr or "")).strip()
        duration = time.perf_counter() - start
        return BenchmarkStepResult(
            step_id=step_id,
            description=description,
            command=command_str,
            status="ok",
            exit_code=0,
            duration_sec=round(duration, 3),
            output_excerpt=output[-6000:],
        )
    except subprocess.TimeoutExpired as err:
        duration = time.perf_counter() - start
        output = ((err.stdout or "") + (err.stderr or "")).strip()
        return BenchmarkStepResult(
            step_id=step_id,
            description=description,
            command=command_str,
            status="failed",
            exit_code=124,
            duration_sec=round(duration, 3),
            output_excerpt=(output + "\nTIMEOUT").strip()[-6000:],
        )
    except subprocess.CalledProcessError as err:
        duration = time.perf_counter() - start
        output = ((err.stdout or "") + (err.stderr or "")).strip()
        return BenchmarkStepResult(
            step_id=step_id,
            description=description,
            command=command_str,
            status="failed",
            exit_code=int(err.returncode),
            duration_sec=round(duration, 3),
            output_excerpt=output[-6000:],
        )


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Benchmark Pack Report",
        "",
        f"> Timestamp: {summary['timestamp']}",
        f"> Suite: {summary['suite']}",
        f"> Dry run: {summary['dry_run']}",
        "",
        "## Summary",
        "",
        f"- Total steps: {summary['total']}",
        f"- Passed: {summary['ok']}",
        f"- Failed: {summary['failed']}",
        f"- Total duration (sec): {summary['duration_sec']}",
        "",
    ]

    regression = summary.get("regression_gate", {})
    if isinstance(regression, dict) and regression.get("enabled"):
        lines.extend(
            [
                f"- Regression gate status: {regression.get('status')}",
                f"- Regression delta (%): {regression.get('delta_pct')}",
                f"- Regression threshold (%): {regression.get('threshold_pct')}",
                f"- Baseline median (sec): {regression.get('baseline_median_sec')}",
            ]
        )

    lines.extend(
        [
            "",
            "## Step Results",
            "",
            "| Step | Status | Exit | Duration (sec) |",
            "|------|--------|-----:|---------------:|",
        ]
    )

    for step in summary["steps"]:
        lines.append(
            f"| {step['step_id']} | {step['status']} | {step['exit_code']} | {step['duration_sec']} |"
        )

    lines.extend(
        [
            "",
            "## Reproduce",
            "",
            f"- Quick: {PYTHON} antigravity/scripts/run_benchmark_pack.py --suite quick",
            f"- Stable: {PYTHON} antigravity/scripts/run_benchmark_pack.py --suite stable",
            f"- Full: {PYTHON} antigravity/scripts/run_benchmark_pack.py --suite full",
            "",
            "Generated by: antigravity/scripts/run_benchmark_pack.py",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run benchmark pack suites")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Benchmark pack config JSON")
    parser.add_argument("--suite", default="stable", help="Suite name in config")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without execution")
    parser.add_argument("--timeout-sec", type=int, default=0, help="Per-step timeout; 0 means no timeout")
    parser.add_argument(
        "--regression-threshold-pct",
        type=float,
        default=-1.0,
        help="Fail if latest duration regresses above this %% vs baseline median; <0 disables",
    )
    parser.add_argument(
        "--regression-min-runs",
        type=int,
        default=0,
        help="Minimum historical passing runs required for regression gate; 0 uses config/default",
    )
    parser.add_argument(
        "--regression-lookback",
        type=int,
        default=0,
        help="Historical benchmark reports to inspect; 0 uses config/default",
    )
    parser.add_argument("--allow-fail", action="store_true", help="Always return success even on failed steps")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config not found: {config_path}")
        return 1

    config = load_config(config_path)
    suites = config.get("suites", {})
    if not isinstance(suites, dict) or args.suite not in suites:
        print(f"Suite not found: {args.suite}")
        print(f"Available suites: {', '.join(sorted(suites.keys()))}")
        return 1

    suite_steps = suites[args.suite]
    if not isinstance(suite_steps, list):
        print(f"Invalid suite format for: {args.suite}")
        return 1

    threshold_pct = float(args.regression_threshold_pct)
    if threshold_pct < 0:
        threshold_pct = float(config.get("regression_gate_pct", -1.0) or -1.0)
    regression_min_runs = (
        int(args.regression_min_runs)
        if args.regression_min_runs > 0
        else int(config.get("regression_min_runs", 3) or 3)
    )
    regression_lookback = (
        int(args.regression_lookback)
        if args.regression_lookback > 0
        else int(config.get("regression_lookback_runs", 30) or 30)
    )
    regression_lookback = max(regression_min_runs, regression_lookback)

    baseline_durations: list[float] = []
    if threshold_pct >= 0 and not args.dry_run:
        baseline_durations = load_suite_baseline_durations(args.suite, lookback=regression_lookback)

    REPORTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    results: list[BenchmarkStepResult] = []
    for step in suite_steps:
        if not isinstance(step, dict):
            continue
        result = run_step(step=step, dry_run=args.dry_run, timeout_sec=args.timeout_sec)
        results.append(result)
        print(f"[{result.status.upper()}] {result.step_id}")

    duration_total = round(sum(step.duration_sec for step in results), 3)
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": args.suite,
        "dry_run": args.dry_run,
        "config": config_path.as_posix(),
        "total": len(results),
        "ok": sum(1 for step in results if step.status == "ok"),
        "failed": sum(1 for step in results if step.status != "ok"),
        "duration_sec": duration_total,
        "steps": [asdict(step) for step in results],
    }

    regression_gate = {
        "enabled": threshold_pct >= 0,
        "threshold_pct": round(threshold_pct, 3) if threshold_pct >= 0 else None,
        "min_runs": regression_min_runs,
        "lookback_runs": regression_lookback,
        "baseline_runs": len(baseline_durations),
        "baseline_median_sec": None,
        "latest_duration_sec": round(duration_total, 3),
        "delta_pct": None,
        "status": "disabled" if threshold_pct < 0 else "insufficient-baseline",
    }

    regression_failed = False
    if threshold_pct >= 0 and not args.dry_run:
        if summary["failed"] > 0:
            regression_gate["status"] = "skipped-on-failures"
        elif len(baseline_durations) >= max(1, regression_min_runs):
            baseline_median = median(baseline_durations)
            delta_pct = 0.0
            if baseline_median > 0:
                delta_pct = ((duration_total - baseline_median) / baseline_median) * 100.0

            regression_failed = delta_pct > threshold_pct
            regression_gate["baseline_median_sec"] = round(baseline_median, 3)
            regression_gate["delta_pct"] = round(delta_pct, 3)
            regression_gate["status"] = "failed" if regression_failed else "ok"

    summary["regression_gate"] = regression_gate

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS / f"benchmark_pack_{stamp}.json"
    report_latest = REPORTS / "benchmark_pack_latest.json"
    md_path = DOCS / f"BENCHMARK_PACK_REPORT_{stamp}.md"
    md_latest = DOCS / "BENCHMARK_PACK_REPORT_LATEST.md"

    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    report_latest.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = render_markdown(summary)
    md_path.write_text(md, encoding="utf-8")
    md_latest.write_text(md, encoding="utf-8")

    print(f"Benchmark report JSON: {report_path}")
    print(f"Benchmark report MD: {md_path}")

    if regression_gate["enabled"]:
        print(
            "Regression gate: "
            f"{regression_gate['status']} "
            f"(delta_pct={regression_gate.get('delta_pct')}, threshold={regression_gate.get('threshold_pct')})"
        )

    if (summary["failed"] > 0 or regression_failed) and not args.allow_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
