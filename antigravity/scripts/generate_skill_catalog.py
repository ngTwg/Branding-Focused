#!/usr/bin/env python3
"""Generate searchable skill catalog with filter fields for discoverability."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ANTIGRAVITY_ROOT = ROOT / "antigravity"
DEFAULT_INVENTORY = ANTIGRAVITY_ROOT / "external" / "UNIFIED_SKILL_INVENTORY.json"
DEFAULT_SECURITY = ANTIGRAVITY_ROOT / "reports" / "security_gate_external_skills.json"
DEFAULT_OUTPUT_JSON = ANTIGRAVITY_ROOT / "external" / "SKILL_CATALOG.json"
DEFAULT_OUTPUT_MD = ANTIGRAVITY_ROOT / "docs" / f"SKILL_CATALOG_{date.today().isoformat()}.md"

DOMAIN_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("security", ("security", "owasp", "xss", "sqli", "pentest", "exploit", "crypt", "compliance")),
    ("frontend", ("frontend", "react", "next", "vue", "angular", "css", "tailwind", "ux", "ui")),
    ("backend", ("backend", "api", "server", "database", "postgres", "prisma", "auth", "redis")),
    ("data-engineering", ("data", "etl", "stream", "analytics", "clickhouse", "warehouse", "spark")),
    ("ai-agents", ("agent", "llm", "prompt", "rag", "mcp", "autogen", "langgraph", "crewai")),
    ("devops", ("devops", "docker", "kubernetes", "k8s", "terraform", "iac", "cicd", "observability")),
    ("workflows", ("workflow", "testing", "debug", "refactor", "quality", "incident")),
    (
        "specialized",
        (
            "specialized",
            "fintech",
            "health",
            "medical",
            "iot",
            "robot",
            "blockchain",
            "legal",
            "govtech",
        ),
    ),
]

TIER_4_HINTS = (
    "medical",
    "critical",
    "aerospace",
    "insulin",
    "kernel",
    "firmware",
    "quantum",
    "safety",
    "formal",
)
TIER_3_HINTS = (
    "scal",
    "distributed",
    "orchestrat",
    "real-time",
    "realtime",
    "benchmark",
    "observability",
    "swarm",
)
TIER_2_HINTS = (
    "auth",
    "payment",
    "api",
    "database",
    "security",
    "compliance",
    "deploy",
    "cicd",
)

HIGH_RISK_HINTS = (
    "privilege-escalation",
    "reverse-shell",
    "offensive",
    "red-team",
    "ransomware",
    "malware",
    "exploit",
)


@dataclass
class CatalogRecord:
    key: str
    source: str
    repo: str | None
    category: str
    domain: str
    tier: str
    risk: str
    security_level: str | None
    token_estimate: int
    token_bucket: str
    file_exists: bool
    line_count: int
    char_count: int
    path: str


def normalize_text(*values: str) -> str:
    return " ".join(value.lower() for value in values if value)


def infer_domain(category: str, key: str, path: str) -> str:
    text = normalize_text(category, key, path)
    for domain, hints in DOMAIN_RULES:
        if any(hint in text for hint in hints):
            return domain
    return "general"


def infer_tier(category: str, key: str, path: str) -> str:
    text = normalize_text(category, key, path)
    if any(hint in text for hint in TIER_4_HINTS):
        return "tier-4"
    if any(hint in text for hint in TIER_3_HINTS):
        return "tier-3"
    if any(hint in text for hint in TIER_2_HINTS):
        return "tier-2"
    return "tier-1"


def infer_risk(security_level: str | None, domain: str, key: str, path: str) -> str:
    level = (security_level or "").upper()
    if level == "FAIL":
        return "high"
    if level == "WARN":
        return "medium"

    text = normalize_text(key, path)
    if any(hint in text for hint in HIGH_RISK_HINTS):
        return "high"
    if domain == "security":
        return "medium"
    return "low"


def token_bucket(tokens: int) -> str:
    if tokens <= 300:
        return "tiny"
    if tokens <= 800:
        return "small"
    if tokens <= 2000:
        return "medium"
    if tokens <= 5000:
        return "large"
    return "xlarge"


def resolve_record_path(record: dict[str, Any]) -> Path:
    raw = Path(str(record.get("path", "")))
    source = str(record.get("source", ""))

    if raw.as_posix().startswith("antigravity/"):
        return ROOT / raw
    if "PRIMARY" in source:
        return ANTIGRAVITY_ROOT / "skills" / raw
    return ROOT / raw


def read_text_stats(path: Path) -> tuple[bool, int, int]:
    if not path.exists() or not path.is_file():
        return False, 0, 0

    content = path.read_text(encoding="utf-8", errors="ignore")
    return True, len(content.splitlines()), len(content)


def build_catalog_records(records: list[dict[str, Any]]) -> tuple[list[CatalogRecord], int]:
    output: list[CatalogRecord] = []
    missing_files = 0

    for row in records:
        category = str(row.get("category") or "unknown")
        key = str(row.get("key") or "")
        rel_path = str(row.get("path") or "")
        source = str(row.get("source") or "unknown")
        repo = row.get("repo")
        security_level = row.get("security_level")

        domain = infer_domain(category=category, key=key, path=rel_path)
        tier = infer_tier(category=category, key=key, path=rel_path)
        risk = infer_risk(security_level=security_level, domain=domain, key=key, path=rel_path)

        resolved = resolve_record_path(row)
        exists, line_count, char_count = read_text_stats(resolved)
        if not exists:
            missing_files += 1

        tokens = max(1, round(char_count / 4)) if exists else 0

        output.append(
            CatalogRecord(
                key=key,
                source=source,
                repo=str(repo) if repo else None,
                category=category,
                domain=domain,
                tier=tier,
                risk=risk,
                security_level=str(security_level) if security_level else None,
                token_estimate=tokens,
                token_bucket=token_bucket(tokens),
                file_exists=exists,
                line_count=line_count,
                char_count=char_count,
                path=rel_path,
            )
        )

    return output, missing_files


def render_markdown(
    catalog: list[CatalogRecord],
    source_inventory: Path,
    missing_files: int,
    output_json: Path,
) -> str:
    domain_counter = Counter(row.domain for row in catalog)
    tier_counter = Counter(row.tier for row in catalog)
    risk_counter = Counter(row.risk for row in catalog)

    lines = [
        "# Skill Catalog",
        "",
        "> Version: 1.0.0",
        f"> Generated: {datetime.now(timezone.utc).isoformat()}",
        f"> Source inventory: {source_inventory.as_posix()}",
        "",
        "## Filter Coverage",
        "",
        f"- Domains: {len(domain_counter)}",
        f"- Tiers: {len(tier_counter)}",
        f"- Risk levels: {len(risk_counter)}",
        f"- Missing source files: {missing_files}",
        "",
        "## Counts by Domain",
        "",
        "| Domain | Count |",
        "|--------|------:|",
    ]

    for name, count in sorted(domain_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {name} | {count} |")

    lines.extend(
        [
            "",
            "## Counts by Tier",
            "",
            "| Tier | Count |",
            "|------|------:|",
        ]
    )
    for name, count in sorted(tier_counter.items(), key=lambda item: item[0]):
        lines.append(f"| {name} | {count} |")

    lines.extend(
        [
            "",
            "## Counts by Risk",
            "",
            "| Risk | Count |",
            "|------|------:|",
        ]
    )
    for name, count in sorted(risk_counter.items(), key=lambda item: item[0]):
        lines.append(f"| {name} | {count} |")

    lines.extend(
        [
            "",
            "## Catalog Preview (Top 120 by Token Estimate)",
            "",
            "| Key | Domain | Tier | Risk | Tokens | Path |",
            "|-----|--------|------|------|-------:|------|",
        ]
    )

    for row in sorted(catalog, key=lambda item: item.token_estimate, reverse=True)[:120]:
        lines.append(
            f"| {row.key} | {row.domain} | {row.tier} | {row.risk} | {row.token_estimate} | {row.path} |"
        )

    lines.extend(
        [
            "",
            "## Query Examples",
            "",
            "- Filter domain=ai-agents and risk!=high from JSON.",
            "- Filter tier=tier-4 and token_bucket in [large, xlarge].",
            "- Sort by token_estimate descending for context planning.",
            "",
            f"Full machine-readable catalog: {output_json.as_posix()}",
            "",
            "Generated by: antigravity/scripts/generate_skill_catalog.py",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate searchable skill catalog")
    parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY), help="Unified inventory JSON path")
    parser.add_argument("--security-report", default=str(DEFAULT_SECURITY), help="Security report path")
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON), help="Output JSON path")
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD), help="Output markdown path")
    # Compatibility options for incremental refresh callers.
    parser.add_argument("--base-catalog", default="", help="Optional previous catalog (metadata only)")
    parser.add_argument("--changed-path", action="append", default=[], help="Changed skill path")
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    security_path = Path(args.security_report)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)

    if not inventory_path.exists():
        print(f"Inventory not found: {inventory_path}")
        return 1

    payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if not isinstance(records, list):
        print("Invalid inventory format: records must be a list")
        return 1

    catalog, missing_files = build_catalog_records(records)
    changed_paths = [str(Path(item).as_posix()) for item in args.changed_path if str(item).strip()]
    base_catalog = str(Path(args.base_catalog)) if str(args.base_catalog).strip() else None

    domain_counter = Counter(row.domain for row in catalog)
    tier_counter = Counter(row.tier for row in catalog)
    risk_counter = Counter(row.risk for row in catalog)
    bucket_counter = Counter(row.token_bucket for row in catalog)

    security_status = "UNKNOWN"
    if security_path.exists():
        try:
            security_status = str(json.loads(security_path.read_text(encoding="utf-8")).get("status", "UNKNOWN"))
        except Exception:
            security_status = "UNKNOWN"

    json_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "security_status": security_status,
        "source_inventory": inventory_path.as_posix(),
        "total_records": len(catalog),
        "missing_source_files": missing_files,
        "incremental": {
            "base_catalog": base_catalog,
            "changed_paths_count": len(changed_paths),
            "changed_paths": changed_paths[:500],
        },
        "filters": {
            "domain": sorted(domain_counter.keys()),
            "tier": sorted(tier_counter.keys()),
            "risk": sorted(risk_counter.keys()),
            "token_bucket": sorted(bucket_counter.keys()),
        },
        "stats": {
            "by_domain": dict(sorted(domain_counter.items(), key=lambda item: item[0])),
            "by_tier": dict(sorted(tier_counter.items(), key=lambda item: item[0])),
            "by_risk": dict(sorted(risk_counter.items(), key=lambda item: item[0])),
            "by_token_bucket": dict(sorted(bucket_counter.items(), key=lambda item: item[0])),
        },
        "records": [asdict(row) for row in catalog],
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")
    output_md.write_text(
        render_markdown(
            catalog=catalog,
            source_inventory=inventory_path,
            missing_files=missing_files,
            output_json=output_json,
        ),
        encoding="utf-8",
    )

    print("Skill catalog generated successfully.")
    print(f"  Records: {len(catalog)}")
    if changed_paths:
        print(f"  Incremental hint: {len(changed_paths)} changed paths received")
    print(f"  JSON: {output_json}")
    print(f"  Markdown: {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
