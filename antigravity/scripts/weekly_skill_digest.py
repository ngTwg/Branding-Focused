#!/usr/bin/env python3
"""Generate weekly digest combining hot/cold usage and metadata coverage delta."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from skill_usage_tracker import summarize


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "antigravity" / "reports"
DOCS = ROOT / "antigravity" / "docs"
CATALOG = ROOT / "antigravity" / "external" / "SKILL_CATALOG.json"
METADATA_REPORT = ROOT / "antigravity" / "reports" / "skill_metadata_coverage.json"
LATEST_JSON = REPORTS / "weekly_skill_digest_latest.json"
LATEST_MD = DOCS / "WEEKLY_SKILL_DIGEST_LATEST.md"


def load_catalog_keys(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    records = payload.get("records", []) if isinstance(payload, dict) else []
    keys = []
    for row in records:
        if isinstance(row, dict):
            key = str(row.get("key") or "").strip()
            if key:
                keys.append(key)
    return sorted(set(keys))


def load_metadata_coverage(path: Path) -> float:
    if not path.exists():
        return 0.0
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return 0.0

    overall = payload.get("overall", {}) if isinstance(payload, dict) else {}
    return float(overall.get("average_coverage_ratio", 0.0) or 0.0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate weekly skill digest")
    parser.add_argument("--days", type=int, default=30, help="Usage window")
    parser.add_argument("--top-hot", type=int, default=10, help="Top hot skills")
    parser.add_argument("--top-cold", type=int, default=10, help="Top cold skills")
    parser.add_argument("--catalog", default=str(CATALOG), help="Catalog path")
    parser.add_argument("--metadata-report", default=str(METADATA_REPORT), help="Metadata report path")
    parser.add_argument("--output-json", default=str(LATEST_JSON), help="Digest JSON output")
    parser.add_argument("--output-md", default=str(LATEST_MD), help="Digest markdown output")
    args = parser.parse_args()

    usage = summarize(days=max(1, args.days))
    catalog_keys = load_catalog_keys(Path(args.catalog))
    used_keys = {str(row.get("skill_key") or "").strip() for row in usage.get("top_skills", [])}
    cold_keys = [key for key in catalog_keys if key not in used_keys]

    coverage_current = load_metadata_coverage(Path(args.metadata_report))
    previous_digest = {}
    out_json = Path(args.output_json)
    if out_json.exists():
        try:
            previous_digest = json.loads(out_json.read_text(encoding="utf-8"))
        except Exception:
            previous_digest = {}
    coverage_previous = float(previous_digest.get("metadata_coverage", 0.0) or 0.0)
    coverage_delta = coverage_current - coverage_previous

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "window_days": max(1, args.days),
        "metadata_coverage": round(coverage_current, 6),
        "metadata_coverage_previous": round(coverage_previous, 6),
        "metadata_coverage_delta": round(coverage_delta, 6),
        "hot": usage.get("top_skills", [])[: max(1, args.top_hot)],
        "cold": cold_keys[: max(1, args.top_cold)],
        "total_events": usage.get("total_events", 0),
        "unique_skills_used": usage.get("unique_skills", 0),
        "catalog_skills": len(catalog_keys),
    }

    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_lines = [
        "# Weekly Skill Digest",
        "",
        f"> Generated: {payload['timestamp']}",
        f"> Window: {payload['window_days']} days",
        "",
        f"- Total usage events: {payload['total_events']}",
        f"- Unique used skills: {payload['unique_skills_used']}",
        f"- Catalog size: {payload['catalog_skills']}",
        f"- Metadata coverage: {payload['metadata_coverage']}",
        f"- Coverage delta vs previous digest: {payload['metadata_coverage_delta']}",
        "",
        "## Top Hot Skills",
        "",
        "| Skill | Hits | Tokens |",
        "|-------|-----:|-------:|",
    ]
    for row in payload["hot"]:
        md_lines.append(
            f"| {row.get('skill_key')} | {row.get('count', 0)} | {row.get('tokens', 0)} |"
        )

    md_lines.extend(["", "## Top Cold Skills", ""])
    for key in payload["cold"]:
        md_lines.append(f"- {key}")

    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("Weekly skill digest generated.")
    print(f"  JSON: {out_json}")
    print(f"  Markdown: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
