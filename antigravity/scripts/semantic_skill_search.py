"""Semantic search over skill embeddings.

Wave 4 objective:
- Query unified skill space using sparse vector similarity.
- Return top-k skill candidates with score and metadata.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from skill_index_utils import ANTIGRAVITY_ROOT, load_json, tokenize


DEFAULT_EMBEDDINGS = ANTIGRAVITY_ROOT / "external" / "SKILL_EMBEDDINGS.json"


def build_query_vector(query: str, vocab: dict[str, int], idf: dict[str, float]) -> dict[str, float]:
	tf = {}
	tokens = [token for token in tokenize(query) if token in vocab]
	if not tokens:
		return {}

	for token in tokens:
		tf[token] = tf.get(token, 0) + 1

	total = sum(tf.values()) or 1
	vector = {}
	for token, freq in tf.items():
		idx = str(vocab[token])
		vector[idx] = (freq / total) * float(idf.get(token, 1.0))

	norm = math.sqrt(sum(value * value for value in vector.values()))
	if norm > 0:
		for key in list(vector.keys()):
			vector[key] = vector[key] / norm
	return vector


def sparse_dot(left: dict[str, float], right: dict[str, float]) -> float:
	# Iterate over smaller vector for lower constant factor.
	if len(left) > len(right):
		left, right = right, left
	score = 0.0
	for key, value in left.items():
		rv = right.get(key)
		if rv is not None:
			score += value * rv
	return score


def semantic_search(embeddings_path: Path, query: str, top_k: int) -> list[dict]:
	payload = load_json(embeddings_path, default={})
	vocab = payload.get("vocab", {})
	idf = payload.get("idf", {})
	embeddings = payload.get("embeddings", [])

	if not isinstance(vocab, dict) or not isinstance(idf, dict) or not isinstance(embeddings, list):
		return []

	query_vector = build_query_vector(query=query, vocab=vocab, idf=idf)
	if not query_vector:
		return []

	scored = []
	for row in embeddings:
		vector = row.get("vector", {})
		meta = row.get("meta", {})
		if not isinstance(vector, dict):
			continue

		score = sparse_dot(query_vector, vector)
		if score <= 0:
			continue

		scored.append(
			{
				"score": round(score, 6),
				"key": meta.get("key"),
				"category": meta.get("category"),
				"path": meta.get("path"),
				"source": meta.get("source"),
				"repo": meta.get("repo"),
				"security_level": meta.get("security_level"),
			}
		)

	scored.sort(key=lambda row: row["score"], reverse=True)
	return scored[: max(1, top_k)]


def main() -> int:
	parser = argparse.ArgumentParser(description="Semantic search over skill embeddings")
	parser.add_argument("query", nargs="?", default="example", help="Search query")
	parser.add_argument("--embeddings", default=str(DEFAULT_EMBEDDINGS), help="Embeddings JSON path")
	parser.add_argument("--top-k", type=int, default=5, help="Top-k results")
	args = parser.parse_args()

	results = semantic_search(
		embeddings_path=Path(args.embeddings),
		query=args.query,
		top_k=max(1, args.top_k),
	)

	print(f"Query: {args.query}")
	if not results:
		print("No semantic matches found.")
		return 0

	print(f"Top {len(results)} results:")
	for idx, row in enumerate(results, start=1):
		print(
			f"{idx}. score={row['score']:.6f} key={row.get('key')} "
			f"category={row.get('category')} path={row.get('path')}"
		)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())