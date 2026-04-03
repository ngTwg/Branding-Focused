#!/usr/bin/env python3
"""Batch-enrich skill metadata frontmatter using rule-based inference.

Wave 2 objectives:
- Infer and backfill required metadata keys.
- Apply by mode (tier2 / tier3 / all).
- Emit before/after coverage report for auditability.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "antigravity" / "skills"
DEFAULT_RULES = ROOT / "antigravity" / "config" / "metadata_enrichment_rules.json"
DEFAULT_REPORT = ROOT / "antigravity" / "reports" / "skill_metadata_enrichment.json"

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", flags=re.DOTALL)
VALID_YAML_LINE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*\s*:")
HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", flags=re.MULTILINE)
WORD_RE = re.compile(r"\w+")


@dataclass
class FileCoverage:
    path: str
    category: str
    domain: str
    inferred_tier: int
    has_valid_frontmatter: bool
    coverage_before: float
    coverage_after: float
    updated: bool


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""

    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except Exception:
            return value

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    if re.fullmatch(r"\d+", value):
        return int(value)

    if re.fullmatch(r"\d+\.\d+", value):
        try:
            return float(value)
        except Exception:
            return value

    if value.lower() in {"true", "false"}:
        return value.lower() == "true"

    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, False

    block = match.group(1)
    lines = [line.rstrip() for line in block.splitlines()]
    candidate_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
    if not candidate_lines:
        return {}, text, False

    key_lines = [line for line in candidate_lines if VALID_YAML_LINE_RE.match(line)]
    if not key_lines or len(key_lines) / len(candidate_lines) < 0.8:
        # Looks like markdown content that starts with '---', not true frontmatter.
        return {}, text, False

    metadata: dict[str, Any] = {}
    for line in key_lines:
        key, value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(value)

    return metadata, text[match.end() :], True


def serialize_value(value: Any) -> str:
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.2f}"
    return json.dumps(str(value), ensure_ascii=False)


def build_frontmatter(metadata: dict[str, Any], required_keys: list[str]) -> str:
    ordered = list(required_keys)
    for key in sorted(metadata.keys()):
        if key not in ordered:
            ordered.append(key)

    lines = ["---"]
    for key in ordered:
        if key in metadata:
            lines.append(f"{key}: {serialize_value(metadata[key])}")
    lines.append("---")
    return "\n".join(lines)


def normalize_required_types(metadata: dict[str, Any], domain_defaults: dict[str, Any], default_agents: list[str]) -> dict[str, Any]:
    result = dict(metadata)

    # tier as integer
    tier_value = result.get("tier", domain_defaults.get("tier", 2))
    if isinstance(tier_value, str) and tier_value.isdigit():
        tier_value = int(tier_value)
    elif not isinstance(tier_value, int):
        tier_value = int(domain_defaults.get("tier", 2))
    result["tier"] = max(1, min(4, tier_value))

    # industry as list
    industry_value = result.get("industry", domain_defaults.get("industry", ["general"]))
    if isinstance(industry_value, str):
        industry_value = [industry_value]
    if not isinstance(industry_value, list) or not industry_value:
        industry_value = domain_defaults.get("industry", ["general"])
    result["industry"] = [str(item) for item in industry_value if str(item).strip()]

    # tags/tools/agents as list
    for list_key in ("tags", "tools_needed", "applies_to_agents"):
        list_value = result.get(list_key)
        if isinstance(list_value, str):
            list_value = [list_value]
        if not isinstance(list_value, list) or not list_value:
            if list_key == "applies_to_agents":
                list_value = list(default_agents)
            else:
                list_value = []
        result[list_key] = [str(item) for item in list_value if str(item).strip()]

    # estimated_tokens as integer
    estimated_tokens = result.get("estimated_tokens", 0)
    if isinstance(estimated_tokens, str) and estimated_tokens.isdigit():
        estimated_tokens = int(estimated_tokens)
    if not isinstance(estimated_tokens, int) or estimated_tokens <= 0:
        estimated_tokens = 256
    result["estimated_tokens"] = estimated_tokens

    # quality_score within [0,1]
    quality_score = result.get("quality_score", 0.5)
    if isinstance(quality_score, str):
        try:
            quality_score = float(quality_score)
        except Exception:
            quality_score = 0.5
    if not isinstance(quality_score, (int, float)):
        quality_score = 0.5
    result["quality_score"] = max(0.0, min(1.0, float(quality_score)))

    # risk string
    risk = str(result.get("risk", domain_defaults.get("risk", "medium"))).lower()
    if risk not in {"low", "medium", "high", "critical"}:
        risk = str(domain_defaults.get("risk", "medium")).lower()
    result["risk"] = risk

    # name fallback
    result["name"] = str(result.get("name") or "Unnamed Skill").strip() or "Unnamed Skill"

    return result


def tokenize_path(path: Path) -> list[str]:
    text = path.as_posix().lower().replace(".md", "")
    tokens: list[str] = []
    for chunk in re.split(r"[\-/_.]", text):
        if chunk and chunk not in {"skill", "skills", "master", "inventory"}:
            tokens.append(chunk)
    return tokens


def infer_domain(category: str, path: Path, content_lower: str, rules: dict[str, Any]) -> str:
    combined = " ".join([category, path.as_posix().lower(), content_lower[:4000]])
    domain_keywords: dict[str, list[str]] = rules.get("domain_keywords", {})

    for domain, keywords in domain_keywords.items():
        if any(keyword.lower() in combined for keyword in keywords):
            return domain

    if category in rules.get("domain_defaults", {}):
        return category
    return "root"


def infer_tier(domain: str, path: Path, content_lower: str, rules: dict[str, Any]) -> int:
    tier_keywords: dict[str, list[str]] = rules.get("tier_keywords", {})
    combined = " ".join([domain, path.as_posix().lower(), content_lower[:5000]])

    for tier in ("4", "3", "2", "1"):
        if any(keyword.lower() in combined for keyword in tier_keywords.get(tier, [])):
            return int(tier)

    defaults = rules.get("domain_defaults", {}).get(domain, {})
    default_tier = defaults.get("tier", 2)
    return int(default_tier) if isinstance(default_tier, int) else 2


def infer_risk(domain: str, content_lower: str, rules: dict[str, Any]) -> str:
    risk_keywords: dict[str, list[str]] = rules.get("risk_keywords", {})
    combined = f"{domain} {content_lower[:5000]}"

    for level in ("critical", "high", "medium"):
        if any(keyword.lower() in combined for keyword in risk_keywords.get(level, [])):
            return level

    defaults = rules.get("domain_defaults", {}).get(domain, {})
    risk = str(defaults.get("risk", "medium")).lower()
    if risk not in {"low", "medium", "high", "critical"}:
        risk = "medium"
    return risk


def infer_name(path: Path, content: str) -> str:
    heading = HEADING_RE.search(content)
    if heading:
        return heading.group(1).strip()
    return path.stem.replace("-", " ").strip().title() or "Unnamed Skill"


def infer_tags(path: Path, content: str, domain: str, category: str) -> list[str]:
    tokens = set(tokenize_path(path))
    tokens.add(domain)
    tokens.add(category)

    for heading in HEADING_RE.findall(content)[:6]:
        for token in re.split(r"\W+", heading.lower()):
            if token and len(token) > 2:
                tokens.add(token)

    return sorted(tokens)[:20]


def infer_tools(content_lower: str, category: str, rules: dict[str, Any]) -> list[str]:
    tools = {"markdown"}
    mapping: dict[str, str] = rules.get("tool_keywords", {})
    for keyword, tool_name in mapping.items():
        if keyword.lower() in content_lower:
            tools.add(str(tool_name))

    if category in {"security", "devops", "backend", "workflows"}:
        tools.add("terminal")

    return sorted(tools)


def infer_estimated_tokens(content: str) -> int:
    chars = len(content)
    estimate = max(128, min(16384, chars // 4))
    return int(estimate)


def infer_quality_score(content: str, base_coverage: float) -> float:
    words = len(WORD_RE.findall(content))
    headings = len(HEADING_RE.findall(content))
    code_blocks = content.count("```") // 2

    score = 0.45
    score += min(0.18, words / 6000)
    score += min(0.16, headings * 0.02)
    score += min(0.16, code_blocks * 0.03)
    score += min(0.10, base_coverage * 0.10)

    return round(max(0.20, min(0.98, score)), 2)


def coverage_ratio(metadata: dict[str, Any], required_keys: list[str]) -> float:
    if not required_keys:
        return 0.0

    present = 0
    for key in required_keys:
        value = metadata.get(key)
        if value not in (None, "", []):
            present += 1
    return present / len(required_keys)


def should_select(mode: str, inferred_tier: int, inferred_domain: str, rules: dict[str, Any]) -> bool:
    selector = rules.get("mode_selector", {}).get(mode, {})
    allowed_tiers = set(selector.get("tiers", []))
    preferred_domains = set(selector.get("preferred_domains", []))

    if mode == "tier3":
        return inferred_tier in allowed_tiers or inferred_domain in preferred_domains

    if not allowed_tiers:
        return True
    return inferred_tier in allowed_tiers


def collect_markdown_files(skip_file_names: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in SKILLS_ROOT.rglob("*.md"):
        if path.name.lower() in skip_file_names:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.as_posix().lower())


def infer_and_merge(
    path: Path,
    existing: dict[str, Any],
    content: str,
    category: str,
    rules: dict[str, Any],
    required_keys: list[str],
    force: bool,
) -> tuple[dict[str, Any], str, int]:
    content_lower = content.lower()
    inferred_domain = infer_domain(category=category, path=path, content_lower=content_lower, rules=rules)
    inferred_tier = infer_tier(domain=inferred_domain, path=path, content_lower=content_lower, rules=rules)
    defaults = rules.get("domain_defaults", {}).get(inferred_domain, rules.get("domain_defaults", {}).get(category, {}))

    inferred = {
        "name": infer_name(path=path, content=content),
        "tags": infer_tags(path=path, content=content, domain=inferred_domain, category=category),
        "tier": inferred_tier,
        "risk": infer_risk(domain=inferred_domain, content_lower=content_lower, rules=rules),
        "estimated_tokens": infer_estimated_tokens(content=content),
        "tools_needed": infer_tools(content_lower=content_lower, category=category, rules=rules),
        "applies_to_agents": list(rules.get("default_agents", [])),
        "industry": defaults.get("industry", ["general"]),
        "quality_score": infer_quality_score(content=content, base_coverage=coverage_ratio(existing, required_keys)),
    }

    merged = dict(existing)
    for key in required_keys:
        if force or merged.get(key) in (None, "", []):
            merged[key] = inferred[key]

    merged = normalize_required_types(
        metadata=merged,
        domain_defaults=defaults if isinstance(defaults, dict) else {},
        default_agents=list(rules.get("default_agents", [])),
    )

    return merged, inferred_domain, inferred_tier


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich skill metadata frontmatter")
    parser.add_argument("--mode", choices=["tier2", "tier3", "all"], default="all")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="Path to enrichment rules JSON")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Output report JSON path")
    parser.add_argument("--apply", action="store_true", help="Write metadata to files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing required metadata keys")
    parser.add_argument("--max-files", type=int, default=0, help="Limit number of updated files (0 = no limit)")
    args = parser.parse_args()

    rules_path = Path(args.rules)
    report_path = Path(args.report)

    if not rules_path.exists():
        raise SystemExit(f"Rules file not found: {rules_path}")

    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    required_keys = list(rules.get("required_keys", []))
    if not required_keys:
        raise SystemExit("Rules file must include required_keys")

    skip_file_names = {name.lower() for name in rules.get("skip_file_names", [])}
    files = collect_markdown_files(skip_file_names=skip_file_names)

    records: list[FileCoverage] = []
    updated: list[dict[str, Any]] = []

    update_budget = args.max_files if args.max_files > 0 else len(files)

    total_before = 0.0
    total_after = 0.0
    selected_before = 0.0
    selected_after = 0.0
    selected_count = 0
    valid_frontmatter_count = 0

    for path in files:
        rel_path = str(path.relative_to(ROOT)).replace("\\", "/")
        category = path.relative_to(SKILLS_ROOT).parts[0] if len(path.relative_to(SKILLS_ROOT).parts) > 1 else "root"

        text = path.read_text(encoding="utf-8", errors="ignore")
        existing_metadata, content, has_valid_frontmatter = parse_frontmatter(text)
        if has_valid_frontmatter:
            valid_frontmatter_count += 1

        before_ratio = coverage_ratio(existing_metadata, required_keys)

        merged_metadata, inferred_domain, inferred_tier = infer_and_merge(
            path=path,
            existing=existing_metadata,
            content=text,
            category=category,
            rules=rules,
            required_keys=required_keys,
            force=args.force,
        )
        after_ratio = coverage_ratio(merged_metadata, required_keys)

        selected = should_select(mode=args.mode, inferred_tier=inferred_tier, inferred_domain=inferred_domain, rules=rules)
        updated_this_file = False

        if selected:
            selected_count += 1
            selected_before += before_ratio
            selected_after += after_ratio

            should_update = merged_metadata != existing_metadata or not has_valid_frontmatter
            if args.apply and should_update and len(updated) < update_budget:
                new_frontmatter = build_frontmatter(metadata=merged_metadata, required_keys=required_keys)
                new_text = f"{new_frontmatter}\n{content.lstrip()}"
                if not new_text.endswith("\n"):
                    new_text += "\n"
                path.write_text(new_text, encoding="utf-8")
                updated_this_file = True
                updated.append(
                    {
                        "path": rel_path,
                        "category": category,
                        "domain": inferred_domain,
                        "tier": inferred_tier,
                        "coverage_before": before_ratio,
                        "coverage_after": after_ratio,
                    }
                )
        else:
            after_ratio = before_ratio

        total_before += before_ratio
        total_after += after_ratio if selected else before_ratio

        records.append(
            FileCoverage(
                path=rel_path,
                category=category,
                domain=inferred_domain,
                inferred_tier=inferred_tier,
                has_valid_frontmatter=has_valid_frontmatter,
                coverage_before=before_ratio,
                coverage_after=after_ratio if selected else before_ratio,
                updated=updated_this_file,
            )
        )

    file_count = len(files)
    overall_before = (total_before / file_count) if file_count else 0.0
    overall_after = (total_after / file_count) if file_count else 0.0
    scope_before = (selected_before / selected_count) if selected_count else 0.0
    scope_after = (selected_after / selected_count) if selected_count else 0.0

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "apply": bool(args.apply),
        "force": bool(args.force),
        "rules": str(rules_path.relative_to(ROOT)).replace("\\", "/"),
        "required_keys": required_keys,
        "files_scanned": file_count,
        "valid_frontmatter_files": valid_frontmatter_count,
        "selected_files": selected_count,
        "overall_coverage_before": overall_before,
        "overall_coverage_after": overall_after,
        "scope_coverage_before": scope_before,
        "scope_coverage_after": scope_after,
        "updated_files_count": len(updated),
        "updated_files": updated,
        "records": [
            {
                "path": row.path,
                "category": row.category,
                "domain": row.domain,
                "inferred_tier": row.inferred_tier,
                "has_valid_frontmatter": row.has_valid_frontmatter,
                "coverage_before": row.coverage_before,
                "coverage_after": row.coverage_after,
                "updated": row.updated,
            }
            for row in records
        ],
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Metadata enrichment report: {report_path}")
    print(f"Mode: {args.mode}")
    print(f"Files scanned: {file_count}")
    print(f"Selected files: {selected_count}")
    print(f"Overall coverage: {overall_before:.2%} -> {overall_after:.2%}")
    print(f"Scope coverage: {scope_before:.2%} -> {scope_after:.2%}")
    if args.apply:
        print(f"Updated files: {len(updated)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
