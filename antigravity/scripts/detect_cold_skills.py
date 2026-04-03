#!/usr/bin/env python3
"""Detect skills with zero usage in a configurable time window."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from skill_usage_tracker import load_events


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "antigravity" / "external" / "SKILL_CATALOG.json"
REPORTS = ROOT / "antigravity" / "reports"
OUT_JSON = REPORTS / "cold_skills_report.json"
OUT_MD = ROOT / "antigravity" / "docs" / "COLD_SKILLS_REPORT.md"


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect cold skills")
    parser.add_argument("--catalog", default=str(CATALOG), help="Skill catalog path")
    parser.add_argument("--days", type=int, default=30, help="Window in days")
    parser.add_argument("--top", type=int, default=200, help="Max cold skills in markdown")
    parser.add_argument("--output-json", default=str(OUT_JSON), help="JSON report output")
    parser.add_argument("--output-md", default=str(OUT_MD), help="Markdown report output")
    args = parser.parse_args()

    catalog_keys = load_catalog_keys(Path(args.catalog))
    events = load_events(days=max(1, args.days))

    used = {str(row.get("skill_key") or "").strip() for row in events if str(row.get("skill_key") or "").strip()}
    cold = [key for key in catalog_keys if key not in used]

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "window_days": max(1, args.days),
        "catalog_skills": len(catalog_keys),
        "used_skills": len(used),
        "cold_skills": len(cold),
        "cold_ratio": round((len(cold) / len(catalog_keys)) if catalog_keys else 0.0, 6),
        "keys": cold,
    }

    out_json = Path(args.output_json)
    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_lines = [
        "# Cold Skills Report",
        "",
        f"> Generated: {payload['timestamp']}",
        f"> Window: {payload['window_days']} days",
        "",
        f"- Catalog skills: {payload['catalog_skills']}",
        f"- Used skills: {payload['used_skills']}",
        f"- Cold skills: {payload['cold_skills']}",
        f"- Cold ratio: {payload['cold_ratio']}",
        "",
        "## Top Cold Skills",
        "",
    ]
    for key in cold[: max(1, args.top)]:
        md_lines.append(f"- {key}")
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("Cold skill detection completed.")
    print(f"  Cold skills: {len(cold)}")
    print(f"  JSON: {out_json}")
    print(f"  Markdown: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
