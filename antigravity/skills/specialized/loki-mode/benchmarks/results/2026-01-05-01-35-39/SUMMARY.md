---
name: "Loki Mode Benchmark Results"
tags: ["01", "05", "2026", "35", "39", "antigravity", "bench", "benchmark", "benchmarks", "c:", "datasets", "download", "frontend", "gemini", "<YOUR_USERNAME>", "lite", "loki", "methodology", "mode", "only"]
tier: 3
risk: "medium"
estimated_tokens: 335
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.70
---
# Loki Mode Benchmark Results

**Generated:** 2026-01-05 02:32:40

## Overview

This directory contains benchmark results for Loki Mode multi-agent system.

## SWE-bench Lite Results

| Metric | Value |
|--------|-------|
| Problems | 50 |
| Patches Generated | 50 |
| Errors | 0 |
| Model | opus |
| Time | 3413.75s |

**Next Step:** Run the SWE-bench evaluator to validate patches:

```bash
python -m swebench.harness.run_evaluation     --predictions /Users/lokesh/git/loki-mode/benchmarks/results/2026-01-05-01-35-39/swebench-predictions.json     --max_workers 4
```

## Methodology

Loki Mode uses its multi-agent architecture to solve each problem:
1. **Architect Agent** analyzes the problem
2. **Engineer Agent** implements the solution
3. **QA Agent** validates with test cases
4. **Review Agent** checks code quality

This mirrors real-world software development more accurately than single-agent approaches.

## Running Benchmarks

```bash
# Setup only (download datasets)
./benchmarks/run-benchmarks.sh all

# Execute with Claude
./benchmarks/run-benchmarks.sh humaneval --execute
./benchmarks/run-benchmarks.sh humaneval --execute --limit 10  # First 10 only
./benchmarks/run-benchmarks.sh swebench --execute --limit 5    # First 5 only

# Use different model
./benchmarks/run-benchmarks.sh humaneval --execute --model opus
```
