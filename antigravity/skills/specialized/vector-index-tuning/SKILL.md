---
name: "vector-index-tuning"
tags: ["antigravity", "c:", "frontend", "gemini", "index", "instructions", "<YOUR_USERNAME>", "not", "resources", "safety", "skill", "specialized", "this", "tuning", "use", "users", "vector", "when"]
tier: 3
risk: "medium"
estimated_tokens: 379
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.63
date_added: "2026-02-27"
description: "Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure."
source: "community"
---
# Vector Index Tuning

Guide to optimizing vector indexes for production performance.

## Use this skill when

- Tuning HNSW parameters
- Implementing quantization
- Optimizing memory usage
- Reducing search latency
- Balancing recall vs speed
- Scaling to billions of vectors

## Do not use this skill when

- You only need exact search on small datasets (use a flat index)
- You lack workload metrics or ground truth to validate recall
- You need end-to-end retrieval system design beyond index tuning

## Instructions

1. Gather workload targets (latency, recall, QPS), data size, and memory budget.
2. Choose an index type and establish a baseline with default parameters.
3. Benchmark parameter sweeps using real queries and track recall, latency, and memory.
4. Validate changes on a staging dataset before rolling out to production.

Refer to `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.

## Safety

- Avoid reindexing in production without a rollback plan.
- Validate changes under realistic load before applying globally.
- Track recall regressions and revert if quality drops.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.
