"""Score skill quality and emit marketplace-ready metadata."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any

from skill_index_utils import (
	ANTIGRAVITY_ROOT,
	DEFAULT_INVENTORY,
	parse_frontmatter,
	resolve_record_path,
	write_json,
)


REPORTS = ANTIGRAVITY_ROOT / "reports"
DEFAULT_REPORT = REPORTS / "skill_quality_scores.json"
DEFAULT_MARKETPLACE = ANTIGRAVITY_ROOT / "external" / "SKILL_MARKETPLACE.json"

CODE_FENCE_RE = re.compile(r"```[\s\S]*?```")
HEADING_RE = re.compile(r"^#{1,4}\s+", flags=re.MULTILINE)


def load_inventory(path: Path) -> list[dict[str, Any]]:
	if not path.exists():
		return []
	try:
		payload = json.loads(path.read_text(encoding="utf-8"))
	except Exception:
		return []
	records = payload.get("records", []) if isinstance(payload, dict) else []
	return records if isinstance(records, list) else []


def score_one(record: dict[str, Any]) -> dict[str, Any] | None:
	path = resolve_record_path(record)
	if not path.exists() or not path.is_file():
		return None

	text = path.read_text(encoding="utf-8", errors="ignore")
	metadata, content, has_frontmatter = parse_frontmatter(text)

	code_blocks = len(CODE_FENCE_RE.findall(content))
	headings = len(HEADING_RE.findall(content))
	char_count = len(text)
	line_count = len(text.splitlines())

	coverage = 0
	expected = ["name", "tags", "tier", "risk", "tools_needed", "quality_score"]
	for key in expected:
		if metadata.get(key):
			coverage += 1
	coverage_ratio = coverage / len(expected)

	# Weighted quality score (0-100)
	score = 0.0
	score += 22.0 if has_frontmatter else 0.0
	score += min(20.0, coverage_ratio * 20.0)
	score += min(25.0, code_blocks * 5.0)
	score += min(15.0, headings * 2.5)
	score += min(12.0, (char_count / 5000.0) * 12.0)
	score += min(6.0, (line_count / 200.0) * 6.0)

	if record.get("security_level") == "WARN":
		score -= 4.0
	elif record.get("security_level") == "FAIL":
		score -= 10.0

	score = max(0.0, min(100.0, score))
	if score >= 80:
		tier_grade = "A"
	elif score >= 55:
		tier_grade = "B"
	else:
		tier_grade = "C"

	return {
		"key": record.get("key"),
		"path": record.get("path"),
		"source": record.get("source"),
		"repo": record.get("repo"),
		"category": record.get("category"),
		"security_level": record.get("security_level"),
		"score": round(score, 2),
		"grade": tier_grade,
		"code_blocks": code_blocks,
		"headings": headings,
		"char_count": char_count,
		"line_count": line_count,
		"frontmatter": has_frontmatter,
		"frontmatter_coverage": round(coverage_ratio, 4),
	}


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
	scores = [float(row["score"]) for row in rows]
	if not scores:
		return {
			"count": 0,
			"mean": 0.0,
			"median": 0.0,
			"p10": 0.0,
			"p90": 0.0,
			"grade_distribution": {},
		}

	sorted_scores = sorted(scores)
	p10_idx = max(0, int(len(sorted_scores) * 0.10) - 1)
	p90_idx = min(len(sorted_scores) - 1, int(len(sorted_scores) * 0.90))
	grades: dict[str, int] = {}
	for row in rows:
		grade = str(row.get("grade", "C"))
		grades[grade] = grades.get(grade, 0) + 1

	return {
		"count": len(scores),
		"mean": round(sum(scores) / len(scores), 4),
		"median": round(median(scores), 4),
		"p10": round(sorted_scores[p10_idx], 4),
		"p90": round(sorted_scores[p90_idx], 4),
		"grade_distribution": dict(sorted(grades.items())),
	}


def to_marketplace(rows: list[dict[str, Any]]) -> dict[str, Any]:
	items = []
	for row in rows:
		items.append(
			{
				"name": row.get("key"),
				"domain": row.get("category"),
				"tier": row.get("grade"),
				"quality_score": row.get("score"),
				"install_count": 0,
				"last_updated": datetime.now(timezone.utc).date().isoformat(),
				"path": row.get("path"),
				"source": row.get("source"),
				"repo": row.get("repo"),
			}
		)
	return {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"version": "1.0.0",
		"items": items,
	}


def main() -> int:
	parser = argparse.ArgumentParser(description="Score skill quality and enforce quality gates")
	parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY), help="Unified inventory path")
	parser.add_argument("--scope", choices=["all", "external", "internal"], default="all")
	parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Quality report output")
	parser.add_argument("--marketplace", default=str(DEFAULT_MARKETPLACE), help="Marketplace output")
	parser.add_argument("--gate-min-score", type=float, default=40.0, help="Minimum score for gate")
	parser.add_argument("--fail-on-gate", action="store_true", help="Return non-zero if gate fails")
	args = parser.parse_args()

	rows = []
	for record in load_inventory(Path(args.inventory)):
		source = str(record.get("source", ""))
		if args.scope == "external" and "EXTERNAL" not in source:
			continue
		if args.scope == "internal" and "PRIMARY" not in source:
			continue

		scored = score_one(record)
		if scored is not None:
			rows.append(scored)

	rows.sort(key=lambda row: float(row.get("score", 0.0)), reverse=True)
	summary = summarize(rows)
	below_gate = [row for row in rows if float(row.get("score", 0.0)) < args.gate_min_score]

	payload = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"scope": args.scope,
		"gate_min_score": args.gate_min_score,
		"summary": summary,
		"below_gate_count": len(below_gate),
		"below_gate": below_gate[:300],
		"rows": rows,
	}

	write_json(Path(args.report), payload)
	write_json(Path(args.marketplace), to_marketplace(rows))

	print("Skill quality scoring completed.")
	print(f"  Rows: {len(rows)}")
	print(f"  Mean score: {summary['mean']}")
	print(f"  Below gate (<{args.gate_min_score}): {len(below_gate)}")
	print(f"  Report: {args.report}")
	print(f"  Marketplace: {args.marketplace}")

	if args.fail_on_gate and below_gate:
		return 1
	return 0


if __name__ == "__main__":
	raise SystemExit(main())