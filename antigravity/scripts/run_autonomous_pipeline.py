"""Run autonomous upgrade pipeline phases for bugfix + ecosystem integration."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
REPORTS = ROOT / "antigravity" / "reports"


@dataclass
class StepResult:
    step: str
    command: str
    status: str
    output: str


def run_step(step: str, cmd: list[str], dry_run: bool) -> StepResult:
    command_str = " ".join(cmd)
    if dry_run:
        return StepResult(step, command_str, "ok", "DRY_RUN")

    try:
        completed = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, check=True)
        output = (completed.stdout or "") + (completed.stderr or "")
        return StepResult(step, command_str, "ok", output.strip())
    except subprocess.CalledProcessError as err:
        output = (err.stdout or "") + (err.stderr or "")
        return StepResult(step, command_str, "failed", output.strip())


def build_steps(phase: str, dry_run: bool) -> list[tuple[str, list[str]]]:
    test_cmd = [
        str(PYTHON),
        "-m",
        "pytest",
        "antigravity/tests/integration",
        "-q",
    ]

    targeted_cmd = [
        str(PYTHON),
        "-m",
        "pytest",
        "antigravity/tests/test_schemas.py",
        "antigravity/tests/test_failure_memory.py",
        "antigravity/tests/test_hybrid_retriever_properties.py",
        "antigravity/tests/test_hybrid_retriever_properties_v3.py",
        "antigravity/tests/test_llm_client_properties.py",
        "antigravity/tests/test_llm_client_properties_v2.py",
        "antigravity/tests/test_slm_router_properties.py",
        "antigravity/tests/test_tracing_properties.py",
        "antigravity/tests/test_tracing_properties_v2.py",
        "-q",
    ]

    sync_cmd = [str(PYTHON), "antigravity/scripts/sync_community_repos.py"]
    extract_cmd = [str(PYTHON), "antigravity/scripts/extract_external_patterns.py"]
    gap_cmd = [str(PYTHON), "antigravity/scripts/generate_integration_gap_report.py", "--apply"]
    metadata_cmd = [str(PYTHON), "antigravity/scripts/normalize_skill_metadata.py"]
    metadata_apply_cmd = [
        str(PYTHON),
        "antigravity/scripts/normalize_skill_metadata.py",
        "--scope",
        "top-tier",
        "--apply",
        "--report",
        "antigravity/reports/skill_metadata_coverage.json",
        "--normalized-export",
        "antigravity/reports/skill_metadata_normalized_top_tiers.json",
    ]
    skillpack_install_cmd = [
        str(PYTHON),
        "tools/skillpack/skillpack.py",
        "install",
        "--targets",
        "cursor",
        "claude",
        "copilot",
        "--source",
        "GEMINI.md",
        "--workspace-root",
        "antigravity/tmp/skillpack_validation",
        "--report",
        "antigravity/reports/skillpack_install_report.json",
        "--force",
    ]
    skillpack_convert_cmd = [
        str(PYTHON),
        "tools/skillpack/skillpack.py",
        "convert",
        "--target",
        "cline",
        "--source",
        "GEMINI.md",
        "--output",
        "antigravity/tmp/skillpack_validation/.cline/rules/CLINE.md",
    ]
    release_cmd = [
        str(PYTHON),
        "antigravity/scripts/build_release_bundle.py",
        "--version",
        "v6.5.0-SLIM",
        "--release-name",
        "phase-b-packaging",
    ]
    security_cmd = [str(PYTHON), "antigravity/scripts/security_gate_external_skills.py"]
    bridge_cmd = [str(PYTHON), "antigravity/scripts/generate_unified_inventory.py"]
    catalog_cmd = [str(PYTHON), "antigravity/scripts/generate_skill_catalog.py"]
    benchmark_cmd = [
        str(PYTHON),
        "antigravity/scripts/run_benchmark_pack.py",
        "--suite",
        "quick",
    ]
    build_embeddings_cmd = [str(PYTHON), "antigravity/scripts/build_skill_embeddings.py"]
    semantic_smoke_cmd = [
        str(PYTHON),
        "antigravity/scripts/semantic_skill_search.py",
        "frontend performance observability",
        "--top-k",
        "5",
    ]
    compose_smoke_cmd = [
        str(PYTHON),
        "antigravity/scripts/skill_composer.py",
        "build saas mvp auth billing",
        "--json",
    ]
    quality_score_cmd = [
        str(PYTHON),
        "antigravity/scripts/score_skill_quality.py",
        "--scope",
        "all",
        "--gate-min-score",
        "35",
    ]
    usage_summary_cmd = [
        str(PYTHON),
        "antigravity/scripts/skill_usage_tracker.py",
        "--summary",
        "--days",
        "30",
    ]
    cold_skills_cmd = [str(PYTHON), "antigravity/scripts/detect_cold_skills.py", "--days", "30"]
    hot_skills_cmd = [
        str(PYTHON),
        "antigravity/scripts/promote_hot_skills.py",
        "--days",
        "30",
        "--min-hits",
        "3",
    ]
    weekly_digest_cmd = [str(PYTHON), "antigravity/scripts/weekly_skill_digest.py", "--days", "30"]
    benchmark_trend_cmd = [str(PYTHON), "antigravity/scripts/benchmark_trend.py", "--limit", "60"]
    triage_warn_cmd = [str(PYTHON), "antigravity/scripts/triage_warn_files.py"]
    validate_skill_pr_cmd = [
        str(PYTHON),
        "antigravity/scripts/validate_skill_pr.py",
        "--min-chars",
        "200",
        "--min-code-blocks",
        "0",
        "--allow-fail",
    ]
    community_surface_cmd = [
        str(PYTHON),
        "antigravity/scripts/validate_community_surface.py",
    ]
    board_cmd = [str(PYTHON), "antigravity/scripts/generate_autonomous_task_board.py"]

    if dry_run:
        sync_cmd.append("--dry-run")

    if phase == "bugfix":
        return [("integration_tests", test_cmd), ("targeted_regressions", targeted_cmd)]
    if phase == "sync":
        return [
            ("sync_community_repos", sync_cmd),
            ("extract_external_patterns", extract_cmd),
            ("generate_integration_gap_report", gap_cmd),
            ("security_gate_external_skills", security_cmd),
            ("triage_warn_files", triage_warn_cmd),
            ("generate_unified_inventory", bridge_cmd),
        ]
    if phase == "packaging":
        return [
            ("skillpack_convert", skillpack_convert_cmd),
            ("skillpack_install", skillpack_install_cmd),
            ("normalize_skill_metadata_top_tier", metadata_apply_cmd),
            ("build_release_bundle", release_cmd),
        ]
    if phase == "planning":
        return [
            ("normalize_skill_metadata", metadata_cmd),
            ("generate_execution_board", board_cmd),
        ]
    if phase == "wave4":
        return [
            ("build_skill_embeddings", build_embeddings_cmd),
            ("semantic_skill_search_smoke", semantic_smoke_cmd),
            ("skill_composer_smoke", compose_smoke_cmd),
        ]
    if phase == "wave5":
        return [
            ("skill_usage_summary", usage_summary_cmd),
            ("detect_cold_skills", cold_skills_cmd),
            ("promote_hot_skills", hot_skills_cmd),
            ("weekly_skill_digest", weekly_digest_cmd),
            ("benchmark_trend", benchmark_trend_cmd),
        ]
    if phase == "wave6":
        return [
            ("score_skill_quality", quality_score_cmd),
            ("validate_skill_pr", validate_skill_pr_cmd),
        ]
    if phase == "discoverability":
        return [
            ("generate_skill_catalog", catalog_cmd),
            ("build_skill_embeddings", build_embeddings_cmd),
            ("score_skill_quality", quality_score_cmd),
            ("run_benchmark_pack", benchmark_cmd),
            ("benchmark_trend", benchmark_trend_cmd),
            ("skill_usage_summary", usage_summary_cmd),
            ("detect_cold_skills", cold_skills_cmd),
            ("promote_hot_skills", hot_skills_cmd),
            ("weekly_skill_digest", weekly_digest_cmd),
            ("validate_skill_pr", validate_skill_pr_cmd),
            ("validate_community_surface", community_surface_cmd),
        ]

    return [
        ("integration_tests", test_cmd),
        ("targeted_regressions", targeted_cmd),
        ("skillpack_convert", skillpack_convert_cmd),
        ("skillpack_install", skillpack_install_cmd),
        ("normalize_skill_metadata_top_tier", metadata_apply_cmd),
        ("build_release_bundle", release_cmd),
        ("normalize_skill_metadata", metadata_cmd),
        ("sync_community_repos", sync_cmd),
        ("extract_external_patterns", extract_cmd),
        ("generate_integration_gap_report", gap_cmd),
        ("security_gate_external_skills", security_cmd),
        ("triage_warn_files", triage_warn_cmd),
        ("generate_unified_inventory", bridge_cmd),
        ("generate_skill_catalog", catalog_cmd),
        ("build_skill_embeddings", build_embeddings_cmd),
        ("score_skill_quality", quality_score_cmd),
        ("run_benchmark_pack", benchmark_cmd),
        ("benchmark_trend", benchmark_trend_cmd),
        ("skill_usage_summary", usage_summary_cmd),
        ("detect_cold_skills", cold_skills_cmd),
        ("promote_hot_skills", hot_skills_cmd),
        ("weekly_skill_digest", weekly_digest_cmd),
        ("validate_skill_pr", validate_skill_pr_cmd),
        ("validate_community_surface", community_surface_cmd),
        ("generate_execution_board", board_cmd),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run autonomous execution pipeline")
    parser.add_argument(
        "--phase",
        choices=["all", "bugfix", "packaging", "sync", "planning", "discoverability", "wave4", "wave5", "wave6"],
        default="all",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    REPORTS.mkdir(parents=True, exist_ok=True)

    results: list[StepResult] = []
    for step_name, cmd in build_steps(args.phase, args.dry_run):
        result = run_step(step_name, cmd, args.dry_run)
        results.append(result)
        print(f"[{result.status.upper()}] {step_name}")
        if result.status == "failed":
            print(result.output)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
        "dry_run": args.dry_run,
        "total": len(results),
        "ok": sum(1 for r in results if r.status == "ok"),
        "failed": sum(1 for r in results if r.status == "failed"),
        "steps": [asdict(r) for r in results],
    }

    out = REPORTS / f"autonomous_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Pipeline report: {out}")

    return 1 if summary["failed"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
