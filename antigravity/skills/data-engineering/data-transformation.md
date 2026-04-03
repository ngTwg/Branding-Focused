---
name: "data-transformation"
tags: ["antigravity", "apache", "big", "c:", "core", "data", "data-engineering", "dbt", "elt", "engineering", "etl", "frontend", "gemini", "layer", "<YOUR_USERNAME>", "matrix", "medium", "pandas", "paradigms", "patterns"]
tier: 2
risk: "medium"
estimated_tokens: 730
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.69
author: "Antigravity System"
description: "Core patterns for data transformation (ETL vs ELT), tool selection (Spark, Pandas, SQL), schema evolution, and performance optimization. Trigger: data cleaning, transformation logic, schema evolution, Spark, Pandas, SQL optimization."
version: "1.0"
---
# 🛠️ DATA TRANSFORMATION PATTERNS

> **MANDATORY:** Apply these patterns when designing data pipelines, cleaning datasets, or optimizing analytical queries.

---

## 🔄 CORE PARADIGMS: ETL VS. ELT

| Feature | ETL (Extract, Transform, Load) | ELT (Extract, Load, Transform) |
|:---|:---|:---|
| **Sequence** | Transform *before* loading. | Load raw data, *then* transform. |
| **Compute** | Dedicated ETL server/engine. | Target Warehouse/Lake (BigQuery, Spark). |
| **Best For** | On-prem, strict privacy, small data. | Cloud-native, high volume, agile analytics. |
| **Format** | Clean data in warehouse. | Raw "Bronze" data lake storage. |

---

## 🏗️ TOOL SELECTION MATRIX

### 1. Pandas (Small-Medium Data)
*   **Best Use:** Local EDA, quick prototyping, small datasets (<1GB).
*   **Risk:** Memory-intensive (single-node). Will fail (OOM) on large data.

### 2. Apache Spark / PySpark (Big Data)
*   **Best Use:** Massive datasets, distributed processing, heavy enrichment.
*   **Pros:** Highly scalable, parallel execution.

### 3. SQL / dbt (Semantic Layer)
*   **Best Use:** Business logic, aggregations, data mart creation.
*   **Pros:** Highly readable, engine-optimized throughput.

---

## 🛡️ SCHEMA EVOLUTION STRATEGIES

- **Additive-Only**: Only append new columns; never rename or delete existing ones.
- **Data Contracts**: Define expectation schemas at ingestion hooks to prevent breaking downstream components.
- **Semantic Versioning**: Version your data schemas (v1.0, v2.0) and maintain backward compatibility layers (Views).
- **Self-Describing Formats**: Use Parquet or Avro to embed metadata within the data files.

---

## 🚀 PERFORMANCE OPTIMIZATION (HIGH THROUGHPUT)

1. **Partitioning**: Always partition large tables by time (Date) or high-frequency filter keys.
2. **Columnar Storage**: Use Parquet or ORC to reduce I/O by reading only required columns.
3. **Incremental Processing**: Process only new/changed records (CDC) instead of full table refreshes.
4. **CTEs over Subqueries**: Use Common Table Expressions for readability and better engine optimization.
5. **Caching**: Cache intermediate results in Spark (`.cache()`) if reused across multiple actions.

---

## 🚦 ANTI-PATTERNS (REJECT THESE)

- **Row-by-Row Processing**: Avoid loops; use vectorized operations or set-based SQL logic.
- **Nested Subqueries**: Excessive nesting hinders optimizer performance and readability.
- **Hard-coded Schemas**: Never hard-code column indices; use named references.
- **Ignoring Nulls**: Always handle missing data (`fillna`, `COALESCE`) before aggregations.
