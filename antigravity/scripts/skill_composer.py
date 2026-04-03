"""Auto-compose skill chains from intent using rules + semantic fallback.

Wave 4 objective:
- Given user intent, produce an ordered skill chain.
- Prefer explicit composition rules, then semantic expansion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from semantic_skill_search import semantic_search
from skill_index_utils import ANTIGRAVITY_ROOT, load_json


DEFAULT_RULES = ANTIGRAVITY_ROOT / "config" / "skill_composition_rules.json"
DEFAULT_TEMPLATES_DIR = ANTIGRAVITY_ROOT / "config" / "composition_templates"
DEFAULT_EMBEDDINGS = ANTIGRAVITY_ROOT / "external" / "SKILL_EMBEDDINGS.json"


def normalize_text(value: str) -> str:
	return " ".join(value.lower().split())


def load_templates(templates_dir: Path) -> dict[str, dict]:
	templates: dict[str, dict] = {}
	if not templates_dir.exists():
		return templates

	for file_path in sorted(templates_dir.glob("*.json"), key=lambda p: p.name.lower()):
		data = load_json(file_path, default={})
		if isinstance(data, dict):
			key = str(data.get("id") or file_path.stem)
			templates[key] = data
	return templates


def match_rule(intent: str, rules_payload: dict, templates: dict[str, dict]) -> dict:
	intent_norm = normalize_text(intent)
	rules = rules_payload.get("rules", []) if isinstance(rules_payload, dict) else []

	best = None
	best_score = -1
	for rule in rules:
		if not isinstance(rule, dict):
			continue
		keywords = [normalize_text(str(k)) for k in rule.get("keywords", [])]
		score = sum(1 for keyword in keywords if keyword and keyword in intent_norm)
		if score > best_score:
			best_score = score
			best = rule

	if not best or best_score <= 0:
		return {}

	chain = []
	for step in best.get("skill_chain", []):
		if isinstance(step, str) and step.strip():
			chain.append(step.strip())

	template_ids = [str(item) for item in best.get("templates", []) if str(item).strip()]
	resolved_templates = [templates[item] for item in template_ids if item in templates]

	return {
		"rule_id": best.get("id"),
		"rule_score": best_score,
		"skill_chain": chain,
		"templates": resolved_templates,
	}


def compose_from_intent(
	intent: str,
	rules_path: Path,
	templates_dir: Path,
	embeddings_path: Path,
	top_k_semantic: int,
) -> dict:
	rules_payload = load_json(rules_path, default={})
	templates = load_templates(templates_dir)

	matched = match_rule(intent=intent, rules_payload=rules_payload, templates=templates)
	semantic = semantic_search(embeddings_path=embeddings_path, query=intent, top_k=top_k_semantic)

	chain = []
	if matched:
		chain.extend(matched.get("skill_chain", []))

	for row in semantic:
		key = str(row.get("key") or "").strip()
		if key and key not in chain:
			chain.append(key)

	return {
		"intent": intent,
		"matched_rule": matched.get("rule_id") if matched else None,
		"rule_score": matched.get("rule_score", 0),
		"templates": matched.get("templates", []),
		"semantic_candidates": semantic,
		"composed_chain": chain,
	}


def main() -> int:
	parser = argparse.ArgumentParser(description="Compose skills from user intent")
	parser.add_argument("intent", nargs="*", default=["frontend", "security"], help="User intent text")
	parser.add_argument("--rules", default=str(DEFAULT_RULES), help="Composition rules JSON")
	parser.add_argument("--templates-dir", default=str(DEFAULT_TEMPLATES_DIR), help="Templates directory")
	parser.add_argument("--embeddings", default=str(DEFAULT_EMBEDDINGS), help="Embeddings JSON path")
	parser.add_argument("--top-k-semantic", type=int, default=8, help="Semantic expansion size")
	parser.add_argument("--json", action="store_true", help="Print JSON output")
	args = parser.parse_args()

	intent_text = " ".join(args.intent).strip() or "frontend security"
	payload = compose_from_intent(
		intent=intent_text,
		rules_path=Path(args.rules),
		templates_dir=Path(args.templates_dir),
		embeddings_path=Path(args.embeddings),
		top_k_semantic=max(1, args.top_k_semantic),
	)

	if args.json:
		print(json.dumps(payload, indent=2, ensure_ascii=False))
		return 0

	print(f"Intent: {payload['intent']}")
	print(f"Matched rule: {payload['matched_rule']} (score={payload['rule_score']})")
	print("Composed chain:")
	for idx, item in enumerate(payload["composed_chain"], start=1):
		print(f"{idx}. {item}")

	if payload["templates"]:
		print("Templates:")
		for template in payload["templates"]:
			print(f"- {template.get('id')}: {template.get('name')}")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())