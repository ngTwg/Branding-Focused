#!/usr/bin/env python3
"""Generate unified inventory from internal skills and security-gated external repos."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANTIGRAVITY_ROOT = ROOT / "antigravity"
NGTWG_SKILLS = ANTIGRAVITY_ROOT / "skills"
EXTERNAL_REPOS = ANTIGRAVITY_ROOT / "external" / "community-repos"
SECURITY_REPORT = ANTIGRAVITY_ROOT / "reports" / "security_gate_external_skills.json"
OUTPUT_MD = ANTIGRAVITY_ROOT / "external" / "UNIFIED_SKILL_INVENTORY.md"
OUTPUT_JSON = ANTIGRAVITY_ROOT / "external" / "UNIFIED_SKILL_INVENTORY.json"

EXTERNAL_FILE_NAMES = {
    "skill.md",
    "agents.md",
    "copilot-instructions.md",
}
EXTERNAL_SUFFIXES = (
    ".instructions.md",
    ".prompt.md",
    ".agent.md",
)
SKIP_INTERNAL_NAMES = {"readme.md", "master_router.md", "index-skills.md"}


@dataclass
class InventoryRecord:
    key: str
    source: str
    category: str
    path: str
    type: str
    repo: str | None = None
    security_level: str | None = None


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").lower()


def ensure_unique_key(records: dict[str, InventoryRecord], base_key: str) -> str:
    if base_key not in records:
        return base_key

    idx = 2
    while f"{base_key}::{idx}" in records:
        idx += 1
    return f"{base_key}::{idx}"


def scan_internal_skills() -> dict[str, InventoryRecord]:
    records: dict[str, InventoryRecord] = {}

    for md_file in NGTWG_SKILLS.rglob("*.md"):
        if md_file.name.lower() in SKIP_INTERNAL_NAMES:
            continue

        rel = md_file.relative_to(NGTWG_SKILLS)
        category = rel.parts[0] if len(rel.parts) > 1 else "root"
        base_key = md_file.stem
        key = ensure_unique_key(records, base_key)

        records[key] = InventoryRecord(
            key=key,
            source="ngTwg (PRIMARY)",
            category=category,
            path=rel.as_posix(),
            type="file",
        )

    return records


def load_security_levels(report_path: Path) -> tuple[str, set[str], set[str]]:
    if not report_path.exists():
        return "UNKNOWN", set(), set()

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception:
        return "UNKNOWN", set(), set()

    status = str(report.get("status", "UNKNOWN"))
    fail_files: set[str] = set()
    warn_files: set[str] = set()

    file_levels = report.get("file_levels", [])
    if isinstance(file_levels, list) and file_levels:
        for row in file_levels:
            file_path = normalize_path(str(row.get("file", "")))
            level = str(row.get("level", "")).upper()
            if not file_path:
                continue
            if level == "FAIL":
                fail_files.add(file_path)
            elif level == "WARN":
                warn_files.add(file_path)
        return status, fail_files, warn_files

    for finding in report.get("findings", []):
        file_path = normalize_path(str(finding.get("file", "")))
        level = str(finding.get("level", "")).upper()
        if not file_path:
            continue
        if level == "FAIL":
            fail_files.add(file_path)
        elif level == "WARN":
            warn_files.add(file_path)

    return status, fail_files, warn_files


def is_external_candidate(rel_to_repo: Path) -> bool:
    lower_name = rel_to_repo.name.lower()
    if lower_name in EXTERNAL_FILE_NAMES:
        return True
    if any(lower_name.endswith(suffix) for suffix in EXTERNAL_SUFFIXES):
        return True

    # Include README-based skills only when clearly under skill directories.
    if lower_name == "readme.md":
        parts_lower = [part.lower() for part in rel_to_repo.parts]
        if "skills" in parts_lower or "skill" in rel_to_repo.parent.name.lower():
            return True

    return False


def scan_external_skills(
    fail_files: set[str],
    warn_files: set[str],
    include_warn: bool,
) -> tuple[dict[str, InventoryRecord], int]:
    records: dict[str, InventoryRecord] = {}
    blocked = 0

    if not EXTERNAL_REPOS.exists():
        return records, blocked

    for repo_dir in sorted((p for p in EXTERNAL_REPOS.iterdir() if p.is_dir()), key=lambda p: p.name.lower()):
        for md_file in repo_dir.rglob("*.md"):
            rel_to_repo = md_file.relative_to(repo_dir)
            if not is_external_candidate(rel_to_repo):
                continue

            rel_to_root = md_file.relative_to(ROOT)
            norm_path = normalize_path(rel_to_root.as_posix())
            if norm_path in fail_files:
                blocked += 1
                continue

            security_level = "WARN" if norm_path in warn_files else "PASS"
            if security_level == "WARN" and not include_warn:
                continue

            category = rel_to_repo.parts[0] if len(rel_to_repo.parts) > 1 else "external"
            base_key = f"external::{repo_dir.name}::{md_file.stem}"
            key = ensure_unique_key(records, base_key)

            records[key] = InventoryRecord(
                key=key,
                source="community (EXTERNAL)",
                category=category,
                path=rel_to_root.as_posix(),
                type="file",
                repo=repo_dir.name,
                security_level=security_level,
            )

    return records, blocked


def generate_markdown(
    records: dict[str, InventoryRecord],
    security_status: str,
    blocked_count: int,
    max_rows: int,
) -> str:
    internal_count = sum(1 for row in records.values() if row.source == "ngTwg (PRIMARY)")
    external_count = sum(1 for row in records.values() if row.source != "ngTwg (PRIMARY)")
    warn_count = sum(1 for row in records.values() if row.security_level == "WARN")
    total_unique = len(records)

    lines = [
        "# UNIFIED SKILL INVENTORY",
        "",
        "> Version: 2.0.0 (Auto-generated)",
        f"> Generated: {datetime.now(timezone.utc).isoformat()}",
        "> Purpose: Unified index of ngTwg (PRIMARY) + community (EXTERNAL) skills",
        "",
        "---",
        "",
        "## Statistics",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| ngTwg (PRIMARY) | {internal_count} |",
        f"| community (EXTERNAL) | {external_count} |",
        f"| external WARN imported | {warn_count} |",
        f"| external FAIL blocked | {blocked_count} |",
        f"| total unique | {total_unique} |",
        "",
        "## Security Gate",
        "",
        f"- Gate status: {security_status}",
        f"- Blocked files: {blocked_count}",
        f"- WARN imports included: {warn_count}",
        "",
        "## Inventory (Truncated)",
        "",
        "| Skill Key | Source | Category | Security | Path |",
        "|-----------|--------|----------|----------|------|",
    ]

    sorted_records = sorted(
        records.values(),
        key=lambda row: (0 if row.source == "ngTwg (PRIMARY)" else 1, row.key.lower()),
    )

    for row in sorted_records[:max_rows]:
        lines.append(
            f"| {row.key} | {row.source} | {row.category} | {row.security_level or '-'} | {row.path} |"
        )

    if len(sorted_records) > max_rows:
        lines.append("")
        lines.append(f"Truncated to {max_rows} rows. Full inventory is in UNIFIED_SKILL_INVENTORY.json.")

    lines.extend(
        [
            "",
            "---",
            "",
            "Generated by: generate_unified_inventory.py",
            "Maintained by: Antigravity Integration Team",
            "Status: AUTO-GENERATED",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate unified skill inventory")
    parser.add_argument("--output-md", default=str(OUTPUT_MD), help="Output markdown path")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON), help="Output JSON path")
    parser.add_argument("--security-report", default=str(SECURITY_REPORT), help="Security report JSON")
    parser.add_argument("--max-rows-md", type=int, default=500, help="Max rows in markdown table")
    parser.add_argument("--exclude-warn-imports", action="store_true", help="Skip WARN external files")
    parser.add_argument(
        "--allow-security-fail",
        action="store_true",
        help="Generate inventory even when security gate status is FAIL",
    )
    args = parser.parse_args()

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    security_report = Path(args.security_report)

    print("Scanning internal skills...")
    internal_records = scan_internal_skills()
    print(f"  Found {len(internal_records)} internal skill records")

    security_status, fail_files, warn_files = load_security_levels(security_report)
    print(f"Security status: {security_status} (fail_files={len(fail_files)}, warn_files={len(warn_files)})")
    if security_status == "FAIL" and not args.allow_security_fail:
        print("Security gate is FAIL. Use --allow-security-fail to override.")
        return 1

    print("Scanning external skills with gate filters...")
    external_records, blocked_count = scan_external_skills(
        fail_files=fail_files,
        warn_files=warn_files,
        include_warn=not args.exclude_warn_imports,
    )
    print(f"  Imported external records: {len(external_records)}")
    print(f"  Blocked by FAIL gate: {blocked_count}")

    merged: dict[str, InventoryRecord] = {}
    merged.update(internal_records)
    for key, row in external_records.items():
        merged[ensure_unique_key(merged, key)] = row

    markdown = generate_markdown(
        records=merged,
        security_status=security_status,
        blocked_count=blocked_count,
        max_rows=args.max_rows_md,
    )

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(markdown, encoding="utf-8")

    json_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "security_status": security_status,
        "blocked_external_files": blocked_count,
        "total_records": len(merged),
        "records": [asdict(record) for record in sorted(merged.values(), key=lambda row: row.key.lower())],
    }
    output_json.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    print("Unified inventory generated successfully.")
    print(f"  Markdown: {output_md}")
    print(f"  JSON: {output_json}")
    print(f"  Total records: {len(merged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
