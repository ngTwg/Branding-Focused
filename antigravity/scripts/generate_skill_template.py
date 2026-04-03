#!/usr/bin/env python3
"""Generate scaffolded skill template for onboarding new skills."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "antigravity" / "skills"


def slugify(text: str) -> str:
    value = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    while "--" in value:
        value = value.replace("--", "-")
    return value.strip("-") or "new-skill"


def build_template(name: str, domain: str, tier: str) -> str:
    skill_name = name.strip() or "New Skill"
    domain_tag = domain.strip().lower() or "specialized"
    return f"""---
name: \"{skill_name}\"
tags: [\"{domain_tag}\", \"template\", \"onboarding\"]
tier: {tier}
risk: \"medium\"
estimated_tokens: 800
tools_needed: [\"markdown\"]
applies_to_agents: [\"cursor\", \"claude\", \"copilot\", \"cline\", \"continue\", \"kiro\", \"roo\"]
industry: [\"general\"]
quality_score: 0.55
---
# {skill_name}

> Purpose: Describe when to use this skill.

## Activation

- Trigger phrase 1
- Trigger phrase 2

## Rules

1. Rule one.
2. Rule two.
3. Rule three.

## Examples

```bash
# Add runnable examples here
```

## Validation

- [ ] Includes frontmatter keys
- [ ] Includes actionable rules
- [ ] Includes at least one runnable example
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate new skill template")
    parser.add_argument("--name", required=True, help="Skill display name")
    parser.add_argument("--domain", default="specialized", help="Domain folder")
    parser.add_argument("--tier", default="2", help="Tier value")
    parser.add_argument("--output", default="", help="Optional explicit output path")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    if args.output.strip():
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = ROOT / out_path
    else:
        out_path = SKILLS_ROOT / slugify(args.domain) / f"{slugify(args.name)}.md"

    if out_path.exists() and not args.force:
        print(f"Template already exists: {out_path}")
        print("Use --force to overwrite.")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_template(args.name, args.domain, args.tier), encoding="utf-8")

    print(f"Skill template generated: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
