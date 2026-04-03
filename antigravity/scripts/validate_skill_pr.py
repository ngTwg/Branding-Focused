#!/usr/bin/env python3
"""Validate skill files for onboarding quality gate."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from skill_index_utils import FRONTMATTER_RE


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "antigravity" / "skills"
REPORT = ROOT / "antigravity" / "reports" / "skill_pr_validation.json"

REQUIRED_KEYS = {
	"name",
	"tags",
	"tier",
	"risk",
	"estimated_tokens",
	"tools_needed",
	"applies_to_agents",
	"industry",
	"quality_score",
}


def parse_frontmatter_keys(text: str) -> set[str]:
	match = FRONTMATTER_RE.match(text)
	if not match:
		return set()
	keys = set()
	for line in match.group(1).splitlines():
		stripped = line.strip()
		if ":" not in stripped:
			continue
		key = stripped.split(":", 1)[0].strip()
		if key:
			keys.add(key)
	return keys


def validate_file(path: Path, min_chars: int, min_code_blocks: int) -> dict:
	text = path.read_text(encoding="utf-8", errors="ignore")
	keys = parse_frontmatter_keys(text)
	missing = sorted(REQUIRED_KEYS - keys)
	code_blocks = len(re.findall(r"```", text)) // 2
	char_count = len(text)

	issues = []
	if missing:
		issues.append(f"missing_frontmatter_keys={','.join(missing)}")
	if char_count < min_chars:
		issues.append(f"content_too_short<{min_chars}")
	if code_blocks < min_code_blocks:
		issues.append(f"code_blocks<{min_code_blocks}")

	return {
		"file": str(path.relative_to(ROOT)).replace("\\", "/"),
		"missing_keys": missing,
		"char_count": char_count,
		"code_blocks": code_blocks,
		"status": "PASS" if not issues else "FAIL",
		"issues": issues,
	}


def collect_targets(paths: list[str]) -> list[Path]:
	if paths:
		targets = []
		for raw in paths:
			path = Path(raw)
			if not path.is_absolute():
				path = ROOT / path
			if path.exists() and path.is_file() and path.suffix.lower() == ".md":
				targets.append(path)
		return targets
	return sorted(SKILLS_ROOT.rglob("*.md"), key=lambda p: p.as_posix().lower())


def main() -> int:
	parser = argparse.ArgumentParser(description="Validate skill PR files")
	parser.add_argument("--files", nargs="*", default=[], help="Specific files to validate")
	parser.add_argument("--min-chars", type=int, default=500, help="Minimum file length")
	parser.add_argument("--min-code-blocks", type=int, default=1, help="Minimum code blocks")
	parser.add_argument("--report", default=str(REPORT), help="Validation report output")
	parser.add_argument("--allow-fail", action="store_true", help="Return success even when validation fails")
	args = parser.parse_args()

	targets = collect_targets(args.files)
	if not targets:
		print("No markdown files found to validate.")
		return 1

	rows = [
		validate_file(path=path, min_chars=max(100, args.min_chars), min_code_blocks=max(0, args.min_code_blocks))
		for path in targets
	]
	failed = [row for row in rows if row["status"] == "FAIL"]

	payload = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"total": len(rows),
		"failed": len(failed),
		"rows": rows,
	}

	report_path = Path(args.report)
	report_path.parent.mkdir(parents=True, exist_ok=True)
	report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

	print(f"Validated files: {len(rows)}")
	print(f"Failed: {len(failed)}")
	print(f"Report: {report_path}")
	if args.allow_fail:
		return 0
	return 1 if failed else 0


if __name__ == "__main__":
	raise SystemExit(main())
