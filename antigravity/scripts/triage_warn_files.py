#!/usr/bin/env python3
"""Triage WARN findings from external security gate into actionable buckets."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "antigravity" / "reports"
SECURITY_REPORT = REPORTS / "security_gate_external_skills.json"
OUT_JSON = REPORTS / "warn_triage_report.json"
OUT_MD = ROOT / "antigravity" / "docs" / "WARN_TRIAGE_REPORT.md"


def repo_from_file(path: str) -> str:
    norm = path.replace("\\", "/")
    marker = "antigravity/external/community-repos/"
    idx = norm.lower().find(marker)
    if idx < 0:
        return "unknown"
    tail = norm[idx + len(marker) :]
    if not tail:
        return "unknown"
    return tail.split("/", 1)[0] if "/" in tail else tail


def main() -> int:
    parser = argparse.ArgumentParser(description="Triage WARN files from security gate")
    parser.add_argument("--security-report", default=str(SECURITY_REPORT), help="Security gate report")
    parser.add_argument("--output-json", default=str(OUT_JSON), help="JSON output")
    parser.add_argument("--output-md", default=str(OUT_MD), help="Markdown output")
    args = parser.parse_args()

    report_path = Path(args.security_report)
    if not report_path.exists():
        print(f"Security report not found: {report_path}")
        return 1

    payload = json.loads(report_path.read_text(encoding="utf-8"))
    findings = payload.get("findings", []) if isinstance(payload, dict) else []

    warn_findings = [row for row in findings if str(row.get("level", "")).upper() == "WARN"]
    by_rule = Counter(str(row.get("rule_id", "unknown")) for row in warn_findings)
    by_repo = Counter(repo_from_file(str(row.get("file", ""))) for row in warn_findings)

    actionable = []
    for rule_id, count in sorted(by_rule.items(), key=lambda item: (-item[1], item[0])):
        priority = "high" if count >= 50 else "medium" if count >= 15 else "low"
        actionable.append(
            {
                "rule_id": rule_id,
                "count": count,
                "priority": priority,
                "recommended_action": "refine detection context" if "prompt" in rule_id else "review snippets and patch",
            }
        )

    triage_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_warn_findings": len(warn_findings),
        "rules": actionable,
        "repos": [{"repo": repo, "count": count} for repo, count in sorted(by_repo.items(), key=lambda item: (-item[1], item[0]))],
    }

    out_json = Path(args.output_json)
    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(triage_payload, indent=2), encoding="utf-8")

    lines = [
        "# WARN Triage Report",
        "",
        f"> Generated: {triage_payload['timestamp']}",
        f"> Total WARN findings: {triage_payload['total_warn_findings']}",
        "",
        "## By Rule",
        "",
        "| Rule | Count | Priority | Action |",
        "|------|------:|----------|--------|",
    ]
    for row in triage_payload["rules"]:
        lines.append(
            f"| {row['rule_id']} | {row['count']} | {row['priority']} | {row['recommended_action']} |"
        )

    lines.extend(["", "## By Repository", "", "| Repo | Count |", "|------|------:|"])
    for row in triage_payload["repos"]:
        lines.append(f"| {row['repo']} | {row['count']} |")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("WARN triage report generated.")
    print(f"  JSON: {out_json}")
    print(f"  Markdown: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
