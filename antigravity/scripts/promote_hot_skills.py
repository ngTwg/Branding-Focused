#!/usr/bin/env python3
"""Promote hot skills by usage volume and suggest tier upgrades."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from skill_usage_tracker import summarize


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "antigravity" / "external" / "SKILL_CATALOG.json"
REPORTS = ROOT / "antigravity" / "reports"
OUT_JSON = REPORTS / "hot_skills_promotion_report.json"
OUT_MD = ROOT / "antigravity" / "docs" / "HOT_SKILLS_PROMOTION_REPORT.md"


def tier_number(tier: str) -> int:
    text = str(tier).lower()
    if "4" in text:
        return 4
    if "3" in text:
        return 3
    if "2" in text:
        return 2
    return 1


def load_tier_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    records = payload.get("records", []) if isinstance(payload, dict) else []
    mapping: dict[str, str] = {}
    for row in records:
        if isinstance(row, dict):
            key = str(row.get("key") or "").strip()
            tier = str(row.get("tier") or "tier-1")
            if key:
                mapping[key] = tier
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest hot skill promotions")
    parser.add_argument("--catalog", default=str(CATALOG), help="Skill catalog path")
    parser.add_argument("--days", type=int, default=30, help="Window in days")
    parser.add_argument("--min-hits", type=int, default=3, help="Minimum hits for hot skill")
    parser.add_argument("--top", type=int, default=30, help="Max promoted skills")
    parser.add_argument("--output-json", default=str(OUT_JSON), help="JSON output")
    parser.add_argument("--output-md", default=str(OUT_MD), help="Markdown output")
    args = parser.parse_args()

    usage = summarize(days=max(1, args.days))
    tier_map = load_tier_map(Path(args.catalog))

    promoted = []
    for row in usage.get("top_skills", []):
        count = int(row.get("count") or 0)
        if count < max(1, args.min_hits):
            continue
        key = str(row.get("skill_key") or "").strip()
        if not key:
            continue

        current_tier = tier_map.get(key, "tier-1")
        current_num = tier_number(current_tier)
        target_num = min(4, current_num + 1)
        if target_num <= current_num:
            continue

        promoted.append(
            {
                "skill_key": key,
                "hits": count,
                "tokens": int(row.get("tokens") or 0),
                "current_tier": current_tier,
                "suggested_tier": f"tier-{target_num}",
            }
        )

    promoted = promoted[: max(1, args.top)]
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "window_days": max(1, args.days),
        "min_hits": max(1, args.min_hits),
        "suggestions": promoted,
    }

    out_json = Path(args.output_json)
    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_lines = [
        "# Hot Skills Promotion Report",
        "",
        f"> Generated: {payload['timestamp']}",
        f"> Window: {payload['window_days']} days",
        f"> Min hits: {payload['min_hits']}",
        "",
        "| Skill | Hits | Current Tier | Suggested Tier |",
        "|-------|-----:|--------------|----------------|",
    ]
    for row in promoted:
        md_lines.append(
            f"| {row['skill_key']} | {row['hits']} | {row['current_tier']} | {row['suggested_tier']} |"
        )
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("Hot skill promotion report generated.")
    print(f"  Suggestions: {len(promoted)}")
    print(f"  JSON: {out_json}")
    print(f"  Markdown: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
