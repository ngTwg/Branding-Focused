#!/usr/bin/env python3
"""Track and summarize skill usage events for Wave 5 self-evolving catalog."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "antigravity" / "reports"
USAGE_LOG = REPORTS / "skill_usage_log.jsonl"
USAGE_SUMMARY = REPORTS / "skill_usage_summary.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_usage(
    *,
    skill_key: str,
    source: str = "unknown",
    context: str = "",
    tokens: int = 0,
    metadata: dict[str, Any] | None = None,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": utc_now(),
        "skill_key": skill_key,
        "source": source,
        "context": context,
        "tokens": max(0, int(tokens)),
        "metadata": metadata or {},
    }
    with USAGE_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def load_events(days: int) -> list[dict[str, Any]]:
    if not USAGE_LOG.exists():
        return []

    min_time = datetime.now(timezone.utc) - timedelta(days=max(1, days))
    events: list[dict[str, Any]] = []
    for line in USAGE_LOG.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        ts_raw = str(row.get("timestamp", ""))
        try:
            ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if ts >= min_time:
            events.append(row)
    return events


def summarize(days: int) -> dict[str, Any]:
    events = load_events(days=days)
    by_skill: dict[str, dict[str, Any]] = {}

    for row in events:
        key = str(row.get("skill_key") or "").strip()
        if not key:
            continue
        entry = by_skill.setdefault(key, {"count": 0, "tokens": 0, "sources": {}})
        entry["count"] += 1
        entry["tokens"] += int(row.get("tokens") or 0)
        src = str(row.get("source") or "unknown")
        entry["sources"][src] = entry["sources"].get(src, 0) + 1

    sorted_skills = sorted(by_skill.items(), key=lambda item: (-item[1]["count"], item[0]))
    top = [
        {
            "skill_key": skill,
            "count": data["count"],
            "tokens": data["tokens"],
            "sources": data["sources"],
        }
        for skill, data in sorted_skills
    ]

    total_tokens = sum(item["tokens"] for item in top)
    total_events = sum(item["count"] for item in top)
    payload = {
        "timestamp": utc_now(),
        "window_days": days,
        "total_events": total_events,
        "unique_skills": len(top),
        "total_tokens": total_tokens,
        "top_skills": top,
    }
    USAGE_SUMMARY.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Track or summarize skill usage")
    parser.add_argument("--skill", default="", help="Skill key to log")
    parser.add_argument("--source", default="unknown", help="Source subsystem")
    parser.add_argument("--context", default="", help="Context text")
    parser.add_argument("--tokens", type=int, default=0, help="Approx token usage")
    parser.add_argument("--metadata-json", default="", help="JSON object string for metadata")
    parser.add_argument("--summary", action="store_true", help="Print summary instead of logging")
    parser.add_argument("--days", type=int, default=30, help="Summary window in days")
    args = parser.parse_args()

    if args.summary:
        payload = summarize(days=max(1, args.days))
        print(json.dumps(payload, indent=2))
        return 0

    if not args.skill.strip():
        print("Provide --skill to log usage, or use --summary.")
        return 1

    metadata: dict[str, Any] = {}
    if args.metadata_json.strip():
        try:
            parsed = json.loads(args.metadata_json)
            if isinstance(parsed, dict):
                metadata = parsed
        except Exception:
            metadata = {"raw": args.metadata_json}

    log_usage(
        skill_key=args.skill.strip(),
        source=args.source,
        context=args.context,
        tokens=max(0, args.tokens),
        metadata=metadata,
    )
    print(f"Logged skill usage: {args.skill.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
