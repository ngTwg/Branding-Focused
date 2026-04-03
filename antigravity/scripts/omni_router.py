#!/usr/bin/env python3
"""Omni router upgraded for Wave 4 using composition rules + semantic fallback."""

from __future__ import annotations

import argparse
from pathlib import Path

from router_metrics import log_routing_decision
from skill_composer import compose_from_intent


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES = ROOT / "antigravity" / "config" / "skill_composition_rules.json"
DEFAULT_TEMPLATES_DIR = ROOT / "antigravity" / "config" / "composition_templates"
DEFAULT_EMBEDDINGS = ROOT / "antigravity" / "external" / "SKILL_EMBEDDINGS.json"

ROUTE_PRESENTATION = {
    "security": {
        "label": "SECURITY & PENTEST",
        "color": "\033[91m",
        "chain": "[security-master] -> [owasp-armor] -> [pentest-playbook]",
    },
    "ai-agents": {
        "label": "AI AGENTS & ORCHESTRATION",
        "color": "\033[96m",
        "chain": "[ai-agents-master] -> [orchestrate-workflows] -> [mcp-builder]",
    },
    "data-engineering": {
        "label": "DATA ENGINEERING & ANALYTICS",
        "color": "\033[94m",
        "chain": "[data-master] -> [etl-patterns] -> [observability-monitoring]",
    },
    "frontend": {
        "label": "THE DIGITAL FORGE",
        "color": "\033[92m",
        "chain": "[architecture] -> [react-best] -> [loki-shield] -> [playwright-e2e]",
    },
    "specialized": {
        "label": "SPECIALIZED EXPERTISE",
        "color": "\033[95m",
        "chain": "[specialized-master] -> [cognitive-framework] -> [execution-pack]",
    },
    "general": {
        "label": "SOCRATIC TUTOR & SOLVER",
        "color": "\033[94m",
        "chain": "[writing-skills] -> [claude-d3js] -> [canvas-design]",
    },
}


def map_domain_to_route(domain: str) -> dict:
    return ROUTE_PRESENTATION.get(domain, ROUTE_PRESENTATION["general"])


def classify_and_route(intent: str, rules: Path, templates_dir: Path, embeddings: Path, top_k_semantic: int) -> dict:
    payload = compose_from_intent(
        intent=intent,
        rules_path=rules,
        templates_dir=templates_dir,
        embeddings_path=embeddings,
        top_k_semantic=top_k_semantic,
    )

    semantic = payload.get("semantic_candidates", [])
    first = semantic[0] if semantic else {}
    domain = str(first.get("category") or "general")
    route = map_domain_to_route(domain)

    route_id = payload.get("matched_rule") or f"SEMANTIC::{domain}"
    confidence = float(first.get("score", 0.0) or 0.0)

    log_routing_decision(
        router="omni_router",
        intent=intent,
        route_id=str(route_id),
        confidence=confidence,
        chain=[str(item) for item in payload.get("composed_chain", [])[:12]],
        metadata={
            "domain": domain,
            "semantic_top_key": first.get("key"),
            "semantic_top_path": first.get("path"),
        },
    )

    return {
        "route": route,
        "payload": payload,
        "domain": domain,
        "confidence": confidence,
        "route_id": route_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Omni router with semantic fallback")
    parser.add_argument("intent", nargs="*", default=["Thiet ke app ban hang va sinh PDF bao cao doanh thu."], help="Intent")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="Composition rules path")
    parser.add_argument("--templates-dir", default=str(DEFAULT_TEMPLATES_DIR), help="Templates directory")
    parser.add_argument("--embeddings", default=str(DEFAULT_EMBEDDINGS), help="Embeddings file")
    parser.add_argument("--top-k-semantic", type=int, default=10, help="Semantic candidates")
    args = parser.parse_args()

    intent = " ".join(args.intent).strip()
    resolved = classify_and_route(
        intent=intent,
        rules=Path(args.rules),
        templates_dir=Path(args.templates_dir),
        embeddings=Path(args.embeddings),
        top_k_semantic=max(3, args.top_k_semantic),
    )

    route = resolved["route"]
    payload = resolved["payload"]

    print("\n\033[96m" + "=" * 85 + "\033[0m")
    print("\033[1m                  THE OMNI-ROUTER IS CLASSIFYING INTENT                \033[0m")
    print("\033[96m" + "=" * 85 + "\033[0m")
    print(f"\033[97mNhiem vu dau vao (The Architect's Command):\033[0m {intent}\n")

    print("\033[90m>> Dang truy cap loi Neural Brain de moc noi ky nang...\033[0m")
    print(f"\n{route['color']}[MATCHED] TIN HIEU: {resolved['route_id']} - {route['label']}\033[0m")
    print(f">> Domain inferred: {resolved['domain']}")
    print(f">> Semantic confidence: {round(resolved['confidence'], 6)}")
    print(f">> Baseline chain: {route['chain']}")
    print(">> Composed chain: " + " -> ".join(payload.get("composed_chain", [])[:8]))

    print("\n\033[93m[EXECUTION PROTOCOL]\033[0m Da nhan dien luong hoat dong chinh xac.")
    print("\033[91mHE THONG DA SAN SANG THUC THI LIEN HOAN!\033[0m Giao quyen cho Mega-Pipelines...\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
