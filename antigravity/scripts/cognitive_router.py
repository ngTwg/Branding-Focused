#!/usr/bin/env python3
"""Cognitive router with semantic fallback and composition-aware output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from router_metrics import log_routing_decision
from skill_composer import compose_from_intent


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES = ROOT / "antigravity" / "config" / "skill_composition_rules.json"
DEFAULT_TEMPLATES_DIR = ROOT / "antigravity" / "config" / "composition_templates"
DEFAULT_EMBEDDINGS = ROOT / "antigravity" / "external" / "SKILL_EMBEDDINGS.json"


def build_yaml_output(intent: str, payload: dict) -> str:
    chain = payload.get("composed_chain", [])
    semantic = payload.get("semantic_candidates", [])
    matched_rule = payload.get("matched_rule")
    confidence = 0.0

    if semantic:
        confidence = float(semantic[0].get("score", 0.0))
    if matched_rule:
        confidence = max(confidence, min(1.0, 0.55 + (payload.get("rule_score", 0) * 0.07)))

    first_checks = [row.get("key") for row in semantic[:3] if row.get("key")]
    if not first_checks:
        first_checks = ["run baseline integration checks"]

    yaml_lines = [
        "root_cause_hypotheses:",
        f"  - \"Intent interpreted as: {intent}\"",
        f"  - \"Matched rule: {matched_rule or 'semantic-only'}\"",
        "diag_required:",
    ]
    for item in first_checks:
        yaml_lines.append(f"  - \"{item}\"")

    yaml_lines.append("solution_plan:")
    for step in chain[:8]:
        yaml_lines.append(f"  - \"{step}\"")

    yaml_lines.append(f"confidence: \"{round(confidence, 4)}\"")
    return "\n".join(yaml_lines)


def analyze_input(intent: str, rules: Path, templates_dir: Path, embeddings: Path, top_k_semantic: int) -> dict:
    payload = compose_from_intent(
        intent=intent,
        rules_path=rules,
        templates_dir=templates_dir,
        embeddings_path=embeddings,
        top_k_semantic=top_k_semantic,
    )

    semantic = payload.get("semantic_candidates", [])
    confidence = float(semantic[0].get("score", 0.0)) if semantic else 0.0
    route_id = payload.get("matched_rule") or "SEMANTIC_FALLBACK"

    log_routing_decision(
        router="cognitive_router",
        intent=intent,
        route_id=str(route_id),
        confidence=confidence,
        chain=[str(item) for item in payload.get("composed_chain", [])[:12]],
        metadata={
            "rule_score": payload.get("rule_score", 0),
            "semantic_count": len(semantic),
        },
    )

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Cognitive router with semantic fallback")
    parser.add_argument("intent", nargs="*", default=["App web load cham qua, quay mong mong!"], help="Intent")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="Composition rules path")
    parser.add_argument("--templates-dir", default=str(DEFAULT_TEMPLATES_DIR), help="Templates directory")
    parser.add_argument("--embeddings", default=str(DEFAULT_EMBEDDINGS), help="Embeddings file")
    parser.add_argument("--top-k-semantic", type=int, default=10, help="Semantic candidates")
    parser.add_argument("--json", action="store_true", help="Emit JSON payload")
    args = parser.parse_args()

    intent = " ".join(args.intent).strip()
    payload = analyze_input(
        intent=intent,
        rules=Path(args.rules),
        templates_dir=Path(args.templates_dir),
        embeddings=Path(args.embeddings),
        top_k_semantic=max(3, args.top_k_semantic),
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("\n========================== OMNI-EXPERT PIPELINE ======================")
    print(f"Input: {intent}")
    print("----------------------------------------------------------------------")
    print("[1] STOP & ISOLATE:")
    print(f"Matched rule: {payload.get('matched_rule') or 'semantic-only'}")
    print("\n[2] CROSS-DISCIPLINARY CHECK:")
    for row in payload.get("semantic_candidates", [])[:5]:
        print(f"- {row.get('key')} | score={row.get('score')}")

    print("\n[3] GIAI PHAP PHAU THUAT (YAML OUTPUT):")
    print(build_yaml_output(intent=intent, payload=payload))
    print("======================================================================\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
