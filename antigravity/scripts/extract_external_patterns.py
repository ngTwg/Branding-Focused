"""Extract reusable packaging/distribution patterns from synced community repositories."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPOS_ROOT = ROOT / "antigravity" / "external" / "community-repos"
REPORT_JSON = ROOT / "antigravity" / "reports" / "external_pattern_report.json"
REPORT_MD = ROOT / "antigravity" / "docs" / "EXTERNAL_PATTERN_REPORT_2026-04-01.md"


KEYWORD_GROUPS = {
    "packaging": [r"install", r"converter", r"convert", r"package", r"distribution"],
    "persona": [r"persona", r"role", r"profile", r"preset"],
    "security": [r"security", r"audit", r"scan", r"injection", r"sandbox"],
    "discoverability": [r"catalog", r"docs", r"search", r"marketplace", r"index"],
    "governance": [r"contributing", r"changelog", r"release", r"version", r"policy"],
}


def scan_repo(repo_dir: Path) -> dict:
    counts = defaultdict(int)
    samples = defaultdict(list)

    markdown_files = list(repo_dir.rglob("*.md"))
    for md_file in markdown_files:
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        text_lower = text.lower()
        rel = str(md_file.relative_to(repo_dir))

        for group, patterns in KEYWORD_GROUPS.items():
            hit = False
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    counts[group] += 1
                    hit = True
                    break
            if hit and len(samples[group]) < 5:
                samples[group].append(rel)

    return {
        "repo": repo_dir.name,
        "markdown_files": len(markdown_files),
        "counts": dict(counts),
        "samples": dict(samples),
    }


def write_markdown(results: list[dict]) -> None:
    lines = [
        "# External Pattern Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Source: {REPOS_ROOT}",
        "",
        "## Summary",
        "",
    ]

    for result in results:
        lines.append(f"### {result['repo']}")
        lines.append(f"- Markdown files scanned: {result['markdown_files']}")
        for group in KEYWORD_GROUPS.keys():
            value = result["counts"].get(group, 0)
            lines.append(f"- {group}: {value}")
        lines.append("")

        for group in KEYWORD_GROUPS.keys():
            samples = result["samples"].get(group, [])
            if samples:
                lines.append(f"{group} samples:")
                for sample in samples:
                    lines.append(f"- {sample}")
        lines.append("")

    lines.extend([
        "## Recommended Integrations",
        "",
        "1. Port packaging and converter UX patterns from top-scoring repositories.",
        "2. Add persona preset docs based on repositories with strong persona signals.",
        "3. Mirror security audit checks into external skill bridge ingestion.",
        "4. Consolidate discoverability patterns into a single catalog navigation model.",
    ])

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not REPOS_ROOT.exists():
        print(f"Repo root not found: {REPOS_ROOT}")
        return 1

    repos = [p for p in REPOS_ROOT.iterdir() if p.is_dir()]
    results = [scan_repo(repo) for repo in sorted(repos, key=lambda p: p.name.lower())]

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    write_markdown(results)

    print(f"Pattern report JSON: {REPORT_JSON}")
    print(f"Pattern report MD: {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
