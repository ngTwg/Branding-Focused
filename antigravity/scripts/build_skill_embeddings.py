"""Build semantic embeddings for skills using sparse TF-IDF vectors.

Wave 4 objective:
- Index 5k+ skills with deterministic, dependency-light embeddings.
- Persist an artifact that can be queried quickly for top-k semantic matches.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from skill_index_utils import (
	ANTIGRAVITY_ROOT,
	DEFAULT_INVENTORY,
	build_record_document,
	load_inventory_records,
	tokenize,
	write_json,
)


DEFAULT_OUTPUT = ANTIGRAVITY_ROOT / "external" / "SKILL_EMBEDDINGS.json"


def build_embeddings(
	inventory_path: Path,
	output_path: Path,
	min_token_len: int,
	max_features: int,
	include_content_chars: int,
) -> dict:
	records = load_inventory_records(inventory_path)

	doc_tokens: list[list[str]] = []
	doc_meta: list[dict] = []
	df_counter: Counter[str] = Counter()

	for record in records:
		doc_text, meta = build_record_document(record, include_content_chars=include_content_chars)
		tokens = [token for token in tokenize(doc_text) if len(token) >= min_token_len]
		if not tokens:
			# Keep empty doc placeholders so index IDs remain stable.
			tokens = ["_empty"]

		doc_tokens.append(tokens)
		doc_meta.append(meta)
		df_counter.update(set(tokens))

	# Keep top frequent terms for compact index while preserving relevance.
	most_common = df_counter.most_common(max_features) if max_features > 0 else df_counter.items()
	vocab = {term: idx for idx, (term, _) in enumerate(most_common)}
	doc_count = len(doc_tokens)

	idf = {}
	for term in vocab:
		df = max(1, df_counter.get(term, 1))
		idf[term] = math.log((1.0 + doc_count) / (1.0 + df)) + 1.0

	embeddings = []
	for idx, tokens in enumerate(doc_tokens):
		tf_counter = Counter(token for token in tokens if token in vocab)
		total = sum(tf_counter.values()) or 1

		weights = {}
		for term, tf in tf_counter.items():
			# normalized term frequency * inverse document frequency
			weights[str(vocab[term])] = round((tf / total) * idf[term], 8)

		norm = math.sqrt(sum(value * value for value in weights.values()))
		if norm > 0:
			for key in list(weights.keys()):
				weights[key] = round(weights[key] / norm, 8)

		meta = dict(doc_meta[idx])
		meta["index"] = idx
		embeddings.append({"meta": meta, "vector": weights})

	payload = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"version": "1.0.0",
		"inventory": str(inventory_path),
		"total_records": len(embeddings),
		"vocab_size": len(vocab),
		"max_features": max_features,
		"min_token_len": min_token_len,
		"idf": {term: round(value, 8) for term, value in idf.items()},
		"vocab": vocab,
		"embeddings": embeddings,
	}

	write_json(output_path, payload)
	return payload


def main() -> int:
	parser = argparse.ArgumentParser(description="Build sparse semantic embeddings for skills")
	parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY), help="Unified inventory path")
	parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Embedding JSON output path")
	parser.add_argument("--min-token-len", type=int, default=3, help="Minimum token length")
	parser.add_argument("--max-features", type=int, default=12000, help="Max vocabulary size")
	parser.add_argument(
		"--include-content-chars",
		type=int,
		default=2200,
		help="Max cleaned content chars included per document",
	)
	args = parser.parse_args()

	inventory_path = Path(args.inventory)
	output_path = Path(args.output)

	payload = build_embeddings(
		inventory_path=inventory_path,
		output_path=output_path,
		min_token_len=max(2, args.min_token_len),
		max_features=max(1000, args.max_features),
		include_content_chars=max(0, args.include_content_chars),
	)

	print("Skill embeddings built successfully.")
	print(f"  Records: {payload['total_records']}")
	print(f"  Vocab size: {payload['vocab_size']}")
	print(f"  Output: {output_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())