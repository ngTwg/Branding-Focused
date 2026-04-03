#!/usr/bin/env python3
"""Generate benchmark trend summary from benchmark pack history."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "antigravity" / "reports"
DOCS = ROOT / "antigravity" / "docs"
DEFAULT_JSON = REPORTS / "benchmark_trend.json"
DEFAULT_MD = DOCS / "BENCHMARK_TREND_REPORT.md"


def load_benchmark_reports(limit: int) -> list[dict[str, Any]]:
    files = sorted(REPORTS.glob("benchmark_pack_*.json"), key=lambda p: p.name)
    rows: list[dict[str, Any]] = []
    for path in files[-max(1, limit) :]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        payload["_file"] = str(path)
        rows.append(payload)
    return rows


def build_trend_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_suite: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        suite = str(row.get("suite", "unknown"))
        by_suite.setdefault(suite, []).append(row)

    suite_summaries = {}
    for suite, items in by_suite.items():
        durations = [float(item.get("duration_sec", 0.0) or 0.0) for item in items]
        failures = [int(item.get("failed", 0) or 0) for item in items]
        if not durations:
            continue

        points = []
        for item in items:
            points.append(
                {
                    "timestamp": item.get("timestamp"),
                    "duration_sec": float(item.get("duration_sec", 0.0) or 0.0),
                    "failed": int(item.get("failed", 0) or 0),
                    "ok": int(item.get("ok", 0) or 0),
                    "file": item.get("_file"),
                }
            )

        last = durations[-1]
        first = durations[0]
        delta_pct = 0.0 if first <= 0 else ((last - first) / first) * 100.0

        suite_summaries[suite] = {
            "runs": len(durations),
            "latest_duration_sec": round(last, 3),
            "median_duration_sec": round(median(durations), 3),
            "min_duration_sec": round(min(durations), 3),
            "max_duration_sec": round(max(durations), 3),
            "latest_failed": failures[-1] if failures else 0,
            "total_failed_runs": sum(1 for value in failures if value > 0),
            "delta_pct_first_to_latest": round(delta_pct, 3),
            "points": points,
        }

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_reports": len(rows),
        "suites": suite_summaries,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Benchmark Trend Report",
        "",
        f"> Generated: {payload.get('timestamp')}",
        f"> Reports analyzed: {payload.get('total_reports', 0)}",
        "",
    ]

    suites = payload.get("suites", {})
    if not suites:
        lines.append("No benchmark reports found.")
        return "\n".join(lines) + "\n"

    for suite in sorted(suites.keys()):
        row = suites[suite]
        lines.extend(
            [
                f"## Suite: {suite}",
                "",
                f"- Runs: {row.get('runs')}",
                f"- Latest duration: {row.get('latest_duration_sec')} sec",
                f"- Median duration: {row.get('median_duration_sec')} sec",
                f"- Min/Max: {row.get('min_duration_sec')} / {row.get('max_duration_sec')} sec",
                f"- Latest failed steps: {row.get('latest_failed')}",
                f"- Delta (first -> latest): {row.get('delta_pct_first_to_latest')}%",
                "",
                "| Timestamp | Duration (sec) | Failed |",
                "|-----------|---------------:|-------:|",
            ]
        )
        for point in row.get("points", [])[-15:]:
            lines.append(
                f"| {point.get('timestamp')} | {point.get('duration_sec')} | {point.get('failed')} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate benchmark trend summary")
    parser.add_argument("--limit", type=int, default=60, help="Max benchmark reports to analyze")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON), help="Trend JSON output")
    parser.add_argument("--output-md", default=str(DEFAULT_MD), help="Trend markdown output")
    args = parser.parse_args()

    rows = load_benchmark_reports(limit=max(1, args.limit))
    payload = build_trend_payload(rows)

    out_json = Path(args.output_json)
    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    out_md.write_text(render_markdown(payload), encoding="utf-8")

    print("Benchmark trend generated.")
    print(f"  Reports: {payload.get('total_reports', 0)}")
    print(f"  JSON: {out_json}")
    print(f"  Markdown: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
