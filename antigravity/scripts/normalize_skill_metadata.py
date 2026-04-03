"""Audit and optionally normalize skill metadata schema coverage.

By default this script generates coverage reports only.
Use --apply to write normalized frontmatter for selected scope.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "antigravity" / "skills"
REPORT_PATH = ROOT / "antigravity" / "reports" / "skill_metadata_coverage.json"
NORMALIZED_EXPORT_PATH = ROOT / "antigravity" / "reports" / "skill_metadata_normalized_top_tiers.json"

REQUIRED_KEYS = [
    "name",
    "tags",
    "tier",
    "risk",
    "estimated_tokens",
    "tools_needed",
    "applies_to_agents",
    "industry",
    "quality_score",
]

SKIP_FILE_NAMES = {"readme.md", "master_router.md", "index-skills.md"}
TOP_TIER_NAMES = {"master_router.md", "index-skills.md"}
DEFAULT_AGENTS = ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]

DEFAULTS_BY_CATEGORY: dict[str, dict[str, str]] = {
    "frontend": {"tier": "2", "risk": "medium", "industry": "web"},
    "backend": {"tier": "2", "risk": "medium", "industry": "platform"},
    "workflows": {"tier": "2", "risk": "medium", "industry": "engineering"},
    "devops": {"tier": "3", "risk": "high", "industry": "platform"},
    "security": {"tier": "3", "risk": "high", "industry": "security"},
    "data-engineering": {"tier": "3", "risk": "high", "industry": "data"},
    "ai-agents": {"tier": "3", "risk": "high", "industry": "ai"},
    "deep-tech": {"tier": "4", "risk": "high", "industry": "research"},
    "specialized": {"tier": "4", "risk": "high", "industry": "specialized"},
    "beyond": {"tier": "4", "risk": "high", "industry": "research"},
}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", flags=re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+)$", flags=re.MULTILINE)


@dataclass
class SkillRow:
    path: str
    category: str
    has_frontmatter: bool
    present_keys: list[str]
    missing_keys: list[str]
    coverage_ratio: float


def parse_scalar(value: str) -> object:
    raw = value.strip()
    if not raw:
        return ""

    if raw.startswith("[") and raw.endswith("]"):
        try:
            return json.loads(raw)
        except Exception:
            return raw

    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]

    if re.fullmatch(r"\d+", raw):
        return int(raw)
    if re.fullmatch(r"\d+\.\d+", raw):
        try:
            return float(raw)
        except Exception:
            return raw

    return raw


def parse_frontmatter(text: str) -> tuple[dict[str, object], str, bool]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, False

    body = match.group(1)
    metadata: dict[str, object] = {}
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = parse_scalar(value)

    content = text[match.end() :]
    return metadata, content, True


def collect_markdown_files() -> list[Path]:
    files: list[Path] = []
    for file_path in SKILLS_ROOT.rglob("*.md"):
        if file_path.name.lower() in SKIP_FILE_NAMES:
            continue
        files.append(file_path)
    return sorted(files, key=lambda path: path.as_posix().lower())


def get_category(file_path: Path) -> str:
    rel = file_path.relative_to(SKILLS_ROOT)
    if len(rel.parts) > 1:
        return rel.parts[0]
    return "root"


def is_top_tier_file(file_path: Path) -> bool:
    name = file_path.name.lower()
    if name in TOP_TIER_NAMES:
        return True
    return name.endswith("-master-inventory.md")


def serialize_value(value: object) -> str:
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, float):
        return f"{value:.2f}"
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def build_frontmatter(metadata: dict[str, object]) -> str:
    ordered_keys = list(REQUIRED_KEYS)
    for key in sorted(metadata.keys()):
        if key not in ordered_keys:
            ordered_keys.append(key)

    lines = ["---"]
    for key in ordered_keys:
        if key not in metadata:
            continue
        lines.append(f"{key}: {serialize_value(metadata[key])}")
    lines.append("---")
    return "\n".join(lines)


def infer_tags(file_path: Path, category: str) -> list[str]:
    rel = file_path.relative_to(SKILLS_ROOT)
    tokens: set[str] = {category}
    for part in rel.parts:
        token = part.lower().replace(".md", "")
        for split in re.split(r"[-_.]", token):
            if split and split not in {"skill", "skills", "master", "inventory"}:
                tokens.add(split)
    return sorted(tokens)


def infer_tools(text_lower: str, category: str) -> list[str]:
    tools = ["markdown"]
    if "pytest" in text_lower:
        tools.append("pytest")
    if "docker" in text_lower:
        tools.append("docker")
    if "terraform" in text_lower:
        tools.append("terraform")
    if "kubernetes" in text_lower or "k8s" in text_lower:
        tools.append("kubernetes")
    if "mcp" in text_lower:
        tools.append("mcp")
    if category in {"security", "devops"}:
        tools.append("terminal")
    return sorted(set(tools))


def infer_metadata(
    file_path: Path,
    category: str,
    text: str,
    existing: dict[str, object],
    coverage_ratio: float,
) -> dict[str, object]:
    text_lower = text.lower()
    heading_match = H1_RE.search(text)
    heading = heading_match.group(1).strip() if heading_match else file_path.stem.replace("-", " ")

    category_defaults = DEFAULTS_BY_CATEGORY.get(category, {"tier": "2", "risk": "medium", "industry": "general"})
    inferred: dict[str, object] = {
        "name": heading,
        "tags": infer_tags(file_path=file_path, category=category),
        "tier": category_defaults["tier"],
        "risk": category_defaults["risk"],
        "estimated_tokens": max(256, min(8192, int(len(re.findall(r"\w+", text)) * 1.3))),
        "tools_needed": infer_tools(text_lower=text_lower, category=category),
        "applies_to_agents": DEFAULT_AGENTS,
        "industry": category_defaults["industry"],
        "quality_score": round(min(0.99, 0.55 + (coverage_ratio * 0.45)), 2),
    }

    if any(keyword in text_lower for keyword in ["medical", "aerospace", "life-critical", "quantum"]):
        inferred["tier"] = "4"
        inferred["risk"] = "critical"

    if any(keyword in text_lower for keyword in ["tutorial", "quickstart", "getting started"]):
        inferred["tier"] = "1"
        inferred["risk"] = "low"

    merged = dict(existing)
    for key in REQUIRED_KEYS:
        value = merged.get(key)
        if value in (None, "", []):
            merged[key] = inferred[key]
    return merged


def build_row(file_path: Path) -> SkillRow | None:
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    metadata, _, has_frontmatter = parse_frontmatter(text)
    present = sorted(metadata.keys())
    missing = [key for key in REQUIRED_KEYS if key not in metadata]
    ratio = 0.0 if not REQUIRED_KEYS else (len(REQUIRED_KEYS) - len(missing)) / len(REQUIRED_KEYS)

    return SkillRow(
        path=str(file_path.relative_to(ROOT)).replace("\\", "/"),
        category=get_category(file_path),
        has_frontmatter=has_frontmatter,
        present_keys=present,
        missing_keys=missing,
        coverage_ratio=ratio,
    )


def summarize_rows(rows: list[SkillRow]) -> dict[str, float | int]:
    total = len(rows)
    return {
        "total_files": total,
        "with_frontmatter": sum(1 for row in rows if row.has_frontmatter),
        "avg_coverage_ratio": (sum(row.coverage_ratio for row in rows) / total) if total else 0.0,
    }


def select_scope_files(files: list[Path], scope: str) -> list[Path]:
    if scope == "top-tier":
        return [path for path in files if is_top_tier_file(path)]
    return files


def apply_normalization(file_path: Path) -> tuple[bool, dict[str, object] | None]:
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False, None

    category = get_category(file_path)
    existing, content, _ = parse_frontmatter(text)
    missing_before = [key for key in REQUIRED_KEYS if key not in existing]
    coverage_ratio = 0.0 if not REQUIRED_KEYS else (len(REQUIRED_KEYS) - len(missing_before)) / len(REQUIRED_KEYS)
    normalized = infer_metadata(
        file_path=file_path,
        category=category,
        text=text,
        existing=existing,
        coverage_ratio=coverage_ratio,
    )

    if all(key in existing and existing.get(key) not in (None, "", []) for key in REQUIRED_KEYS):
        return False, None

    frontmatter = build_frontmatter(normalized)
    new_text = f"{frontmatter}\n{content.lstrip()}"

    if not new_text.endswith("\n"):
        new_text += "\n"

    file_path.write_text(new_text, encoding="utf-8")
    return True, normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and normalize skill metadata schema")
    parser.add_argument("--apply", action="store_true", help="Write normalized frontmatter to selected files")
    parser.add_argument(
        "--scope",
        choices=["all", "top-tier"],
        default="all",
        help="Scope of normalization operations",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=0,
        help="Maximum number of files to modify in --apply mode (0 means no limit)",
    )
    parser.add_argument("--report", default=str(REPORT_PATH), help="Coverage report JSON path")
    parser.add_argument(
        "--normalized-export",
        default=str(NORMALIZED_EXPORT_PATH),
        help="Normalized metadata export JSON path",
    )
    args = parser.parse_args()

    report_path = Path(args.report)
    normalized_export_path = Path(args.normalized_export)

    markdown_files = collect_markdown_files()
    before_rows = [row for row in (build_row(path) for path in markdown_files) if row is not None]
    before_summary = summarize_rows(before_rows)

    selected_files = select_scope_files(markdown_files, args.scope)
    selected_set = {str(path.relative_to(ROOT)).replace("\\", "/") for path in selected_files}

    selected_rows_before = [row for row in before_rows if row.path in selected_set]
    selected_summary_before = summarize_rows(selected_rows_before)

    updated_files: list[dict[str, object]] = []
    normalized_records: list[dict[str, object]] = []

    if args.apply:
        candidates = sorted(
            (row for row in selected_rows_before if row.missing_keys),
            key=lambda row: (-len(row.missing_keys), row.coverage_ratio, row.path),
        )

        limit = args.max_files if args.max_files > 0 else len(candidates)
        candidate_paths = [ROOT / row.path for row in candidates[:limit]]

        for path in candidate_paths:
            changed, normalized = apply_normalization(path)
            if changed:
                updated_files.append({"path": str(path.relative_to(ROOT)).replace("\\", "/")})
                if normalized is not None:
                    normalized_records.append(
                        {
                            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                            "metadata": normalized,
                        }
                    )

    after_rows = [row for row in (build_row(path) for path in markdown_files) if row is not None]
    after_summary = summarize_rows(after_rows)

    selected_rows_after = [row for row in after_rows if row.path in selected_set]
    selected_summary_after = summarize_rows(selected_rows_after)

    overall = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scope": args.scope,
        "apply": bool(args.apply),
        "required_keys": REQUIRED_KEYS,
        "total_files": after_summary["total_files"],
        "with_frontmatter": after_summary["with_frontmatter"],
        "avg_coverage_ratio": after_summary["avg_coverage_ratio"],
        "summary_before": before_summary,
        "summary_after": after_summary,
        "selected_files": len(selected_files),
        "selected_summary_before": selected_summary_before,
        "selected_summary_after": selected_summary_after,
        "updated_files_count": len(updated_files),
        "updated_files": updated_files,
        "rows": [
            {
                "path": row.path,
                "category": row.category,
                "has_frontmatter": row.has_frontmatter,
                "present_keys": row.present_keys,
                "missing_keys": row.missing_keys,
                "coverage_ratio": row.coverage_ratio,
            }
            for row in after_rows
        ],
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(overall, indent=2), encoding="utf-8")

    normalized_export = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scope": args.scope,
        "records": normalized_records,
    }
    normalized_export_path.parent.mkdir(parents=True, exist_ok=True)
    normalized_export_path.write_text(json.dumps(normalized_export, indent=2), encoding="utf-8")

    print(f"Metadata coverage report: {report_path}")
    print(f"Normalized export: {normalized_export_path}")
    print(f"Skills scanned: {overall['total_files']}")
    print(f"Files with frontmatter: {overall['with_frontmatter']}")
    print(f"Average coverage ratio: {overall['avg_coverage_ratio']:.2%}")
    print(
        "Selected scope coverage: "
        f"{selected_summary_after['avg_coverage_ratio']:.2%} "
        f"(files={selected_summary_after['total_files']})"
    )
    if args.apply:
        print(f"Updated files: {len(updated_files)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
