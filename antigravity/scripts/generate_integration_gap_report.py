"""Generate integration gap report from external pattern signals and apply high-impact merges.

This script compares pattern density between:
- external community repos (from external_pattern_report.json)
- internal Antigravity skills markdown corpus

It can optionally apply low-risk, high-impact config merges (persona bundles).
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "antigravity" / "skills"
PATTERN_REPORT = ROOT / "antigravity" / "reports" / "external_pattern_report.json"
OUT_JSON = ROOT / "antigravity" / "reports" / "integration_gap_report.json"
OUT_MD = ROOT / "antigravity" / "docs" / "INTEGRATION_GAP_REPORT_2026-04-02.md"
PERSONA_BUNDLES = ROOT / "antigravity" / "config" / "persona_bundles.json"


KEYWORD_GROUPS = {
    "packaging": [r"install", r"converter", r"convert", r"package", r"distribution"],
    "persona": [r"persona", r"role", r"profile", r"preset"],
    "security": [r"security", r"audit", r"scan", r"injection", r"sandbox"],
    "discoverability": [r"catalog", r"docs", r"search", r"marketplace", r"index"],
    "governance": [r"contributing", r"changelog", r"release", r"version", r"policy"],
}


SUGGESTED_BUNDLES = [
    {
        "id": "community-oss-maintainer",
        "description": "Open-source maintainer workflow focused on contribution quality and release hygiene.",
        "skills": [
            "workflows/code-review.md",
            "workflows/testing-strategies.md",
            "workflows/git-workflow.md",
            "workflows/documentation-templates",
        ],
    },
    {
        "id": "docs-discoverability-engineer",
        "description": "Documentation discoverability and catalog-quality delivery persona.",
        "skills": [
            "workflows/documentation-templates",
            "backend/api-design.md",
            "frontend/web-performance.md",
            "specialized/programmatic-seo",
        ],
    },
]


def scan_internal_density() -> tuple[int, dict[str, int], dict[str, float]]:
    markdown_files = list(SKILLS_ROOT.rglob("*.md"))
    counts = {group: 0 for group in KEYWORD_GROUPS}

    for md_file in markdown_files:
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue

        for group, patterns in KEYWORD_GROUPS.items():
            if any(re.search(pattern, text) for pattern in patterns):
                counts[group] += 1

    total = len(markdown_files)
    density = {group: (counts[group] / total if total else 0.0) for group in KEYWORD_GROUPS}
    return total, counts, density


def load_external_density() -> tuple[int, dict[str, int], dict[str, float]]:
    if not PATTERN_REPORT.exists():
        return 0, {group: 0 for group in KEYWORD_GROUPS}, {group: 0.0 for group in KEYWORD_GROUPS}

    payload = json.loads(PATTERN_REPORT.read_text(encoding="utf-8"))
    results = payload.get("results", [])

    total_markdown = 0
    counts = {group: 0 for group in KEYWORD_GROUPS}

    for row in results:
        total_markdown += int(row.get("markdown_files", 0))
        row_counts = row.get("counts", {})
        for group in KEYWORD_GROUPS:
            counts[group] += int(row_counts.get(group, 0))

    density = {group: (counts[group] / total_markdown if total_markdown else 0.0) for group in KEYWORD_GROUPS}
    return total_markdown, counts, density


def apply_persona_bundle_merges() -> list[str]:
    if not PERSONA_BUNDLES.exists():
        return []

    payload = json.loads(PERSONA_BUNDLES.read_text(encoding="utf-8"))
    bundles = payload.get("bundles", [])
    existing_ids = {str(bundle.get("id", "")) for bundle in bundles}

    applied: list[str] = []
    for bundle in SUGGESTED_BUNDLES:
        if bundle["id"] in existing_ids:
            continue
        bundles.append(bundle)
        applied.append(bundle["id"])

    if applied:
        payload["bundles"] = bundles
        PERSONA_BUNDLES.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return applied


def build_gap_rows(
    internal_density: dict[str, float],
    external_density: dict[str, float],
) -> list[dict]:
    rows = []
    for group in KEYWORD_GROUPS:
        ext = external_density.get(group, 0.0)
        internal = internal_density.get(group, 0.0)
        gap = ext - internal
        rows.append(
            {
                "group": group,
                "external_density": ext,
                "internal_density": internal,
                "gap": gap,
                "priority": "high" if gap > 0.05 else ("medium" if gap > 0.0 else "low"),
            }
        )

    return sorted(rows, key=lambda row: row["gap"], reverse=True)


def write_markdown(
    gap_rows: list[dict],
    internal_total: int,
    external_total: int,
    applied_merges: list[str],
) -> None:
    lines = [
        "# Integration Gap Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Internal markdown files scanned: {internal_total}",
        f"External markdown files scanned: {external_total}",
        "",
        "## Gap Summary",
        "",
        "| Group | External Density | Internal Density | Gap | Priority |",
        "|-------|------------------|------------------|-----|----------|",
    ]

    for row in gap_rows:
        lines.append(
            f"| {row['group']} | {row['external_density']:.4f} | {row['internal_density']:.4f} | {row['gap']:.4f} | {row['priority']} |"
        )

    lines.extend(
        [
            "",
            "## Applied High-Impact Merges",
            "",
        ]
    )

    if applied_merges:
        for merge in applied_merges:
            lines.append(f"- Added persona bundle: {merge}")
    else:
        lines.append("- No new persona bundle merges were required.")

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
            "1. Prioritize groups marked high where external density meaningfully exceeds internal coverage.",
            "2. Keep security gate in sync phase before inventory generation to ensure safe imports.",
            "3. Re-run this report after metadata normalization upgrades to track trend movement.",
        ]
    )

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate integration gap report")
    parser.add_argument("--apply", action="store_true", help="Apply high-impact config merges")
    args = parser.parse_args()

    internal_total, internal_counts, internal_density = scan_internal_density()
    external_total, external_counts, external_density = load_external_density()

    gap_rows = build_gap_rows(internal_density=internal_density, external_density=external_density)

    applied_merges = apply_persona_bundle_merges() if args.apply else []

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "internal": {
            "total_markdown": internal_total,
            "counts": internal_counts,
            "density": internal_density,
        },
        "external": {
            "total_markdown": external_total,
            "counts": external_counts,
            "density": external_density,
        },
        "gaps": gap_rows,
        "applied_merges": applied_merges,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(
        gap_rows=gap_rows,
        internal_total=internal_total,
        external_total=external_total,
        applied_merges=applied_merges,
    )

    print(f"Integration gap report JSON: {OUT_JSON}")
    print(f"Integration gap report MD: {OUT_MD}")
    if args.apply:
        if applied_merges:
            print(f"Applied merges: {', '.join(applied_merges)}")
        else:
            print("Applied merges: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
