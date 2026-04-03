"""Create release bundle artifacts and publish release notes for autonomous phases."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "antigravity" / "reports"
DOCS_DIR = ROOT / "antigravity" / "docs"
RELEASES_DIR = ROOT / "antigravity" / "releases"


REQUIRED_RELATIVE_ARTIFACTS = [
    Path("GEMINI.md"),
    Path("antigravity/skills/MASTER_ROUTER.md"),
    Path("tools/skillpack/skillpack.py"),
    Path("tools/skillpack/README.md"),
    Path("antigravity/config/persona_bundles.json"),
    Path("antigravity/reports/skillpack_install_report.json"),
    Path("antigravity/reports/skill_metadata_coverage.json"),
    Path("antigravity/reports/skill_metadata_normalized_top_tiers.json"),
    Path("antigravity/reports/security_gate_external_skills.json"),
    Path("antigravity/reports/integration_gap_report.json"),
    Path("antigravity/external/UNIFIED_SKILL_INVENTORY.json"),
    Path("antigravity/docs/AUTONOMOUS_EXECUTION_BOARD_2026-04-02.md"),
]


@dataclass
class ArtifactStatus:
    path: str
    required: bool
    status: str
    message: str


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def latest_file(pattern: str) -> Path | None:
    files = sorted(REPORTS_DIR.glob(pattern), key=lambda file_path: file_path.stat().st_mtime)
    return files[-1] if files else None


def gather_release_artifacts() -> list[Path]:
    artifacts = list(REQUIRED_RELATIVE_ARTIFACTS)

    latest_pipeline = latest_file("autonomous_pipeline_*.json")
    if latest_pipeline is not None:
        artifacts.append(latest_pipeline.relative_to(ROOT))

    latest_release_report = latest_file("release_bundle_*.json")
    if latest_release_report is not None:
        artifacts.append(latest_release_report.relative_to(ROOT))

    # Deduplicate while preserving order.
    deduped: list[Path] = []
    seen: set[str] = set()
    for artifact in artifacts:
        key = artifact.as_posix().lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(artifact)

    return deduped


def build_release_notes(version: str, release_id: str, included_count: int, missing_count: int) -> str:
    metadata_report = load_json(REPORTS_DIR / "skill_metadata_coverage.json")
    security_report = load_json(REPORTS_DIR / "security_gate_external_skills.json")
    integration_gap = load_json(REPORTS_DIR / "integration_gap_report.json")
    skillpack_report = load_json(REPORTS_DIR / "skillpack_install_report.json")

    latest_pipeline_path = latest_file("autonomous_pipeline_*.json")
    pipeline_report = load_json(latest_pipeline_path) if latest_pipeline_path else {}

    selected_after = metadata_report.get("selected_summary_after", {})
    security_status = str(security_report.get("status", "UNKNOWN"))
    applied_merges = integration_gap.get("applied_merges", [])

    lines = [
        f"# Release Notes - {version}",
        "",
        f"Release ID: {release_id}",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Highlights",
        "",
        "- B1 complete: skillpack converter/installer flow shipped for multi-agent targets.",
        "- B2 complete: metadata normalization now supports top-tier scope and apply mode.",
        "- B3 complete: release bundle artifacts generated with reproducible manifest and zip.",
        "",
        "## Evidence Snapshot",
        "",
        f"- Skillpack install targets processed: {skillpack_report.get('total', 0)}",
        f"- Skillpack install success count: {skillpack_report.get('ok', 0)}",
        f"- Metadata selected scope average coverage: {selected_after.get('avg_coverage_ratio', 0):.2%}",
        f"- Metadata selected files: {selected_after.get('total_files', 0)}",
        f"- Security gate status: {security_status}",
        f"- Integration gap applied merges: {', '.join(applied_merges) if applied_merges else 'none'}",
    ]

    if latest_pipeline_path is not None:
        lines.extend(
            [
                f"- Latest pipeline report: {latest_pipeline_path.relative_to(ROOT).as_posix()}",
                f"- Latest pipeline phase: {pipeline_report.get('phase', 'unknown')}",
                f"- Latest pipeline step result: {pipeline_report.get('ok', 0)}/{pipeline_report.get('total', 0)} ok",
            ]
        )

    lines.extend(
        [
            f"- Bundle included artifacts: {included_count}",
            f"- Bundle missing artifacts: {missing_count}",
            "",
            "## Notes",
            "",
            "- Release bundle is generated locally for packaging/distribution validation.",
            "- Re-run with updated reports when progressing to discoverability and benchmark phases.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build release bundle artifacts and release notes")
    parser.add_argument("--version", default="v6.5.0-SLIM", help="Release version label")
    parser.add_argument("--release-name", default="phase-b-packaging", help="Release codename")
    parser.add_argument("--output-dir", default=str(RELEASES_DIR), help="Release output directory")
    parser.add_argument("--notes-path", help="Release notes markdown path")
    parser.add_argument("--report-path", help="Bundle report JSON path")
    parser.add_argument("--dry-run", action="store_true", help="Print planned operations without writing files")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S")

    output_dir = Path(args.output_dir)
    release_id = f"{args.version}_{args.release_name}_{stamp}".replace("/", "-")
    release_root = output_dir / release_id
    zip_path = output_dir / f"{release_id}.zip"

    notes_path = Path(args.notes_path) if args.notes_path else DOCS_DIR / f"RELEASE_NOTES_{now.date().isoformat()}.md"
    report_path = Path(args.report_path) if args.report_path else REPORTS_DIR / f"release_bundle_{stamp}.json"

    artifacts = gather_release_artifacts()
    statuses: list[ArtifactStatus] = []
    copied_files: list[Path] = []

    for rel_path in artifacts:
        source = ROOT / rel_path
        if not source.exists():
            statuses.append(
                ArtifactStatus(
                    path=rel_path.as_posix(),
                    required=rel_path in REQUIRED_RELATIVE_ARTIFACTS,
                    status="missing",
                    message="not found",
                )
            )
            continue

        statuses.append(
            ArtifactStatus(
                path=rel_path.as_posix(),
                required=rel_path in REQUIRED_RELATIVE_ARTIFACTS,
                status="included",
                message="ok",
            )
        )

        if not args.dry_run:
            destination = release_root / rel_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied_files.append(destination)

    included_count = sum(1 for row in statuses if row.status == "included")
    missing_count = sum(1 for row in statuses if row.status == "missing")

    release_notes = build_release_notes(
        version=args.version,
        release_id=release_id,
        included_count=included_count,
        missing_count=missing_count,
    )

    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        release_root.mkdir(parents=True, exist_ok=True)

        notes_path.parent.mkdir(parents=True, exist_ok=True)
        notes_path.write_text(release_notes, encoding="utf-8")

        notes_copy = release_root / "RELEASE_NOTES.md"
        notes_copy.parent.mkdir(parents=True, exist_ok=True)
        notes_copy.write_text(release_notes, encoding="utf-8")
        copied_files.append(notes_copy)

        with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in copied_files:
                archive.write(file_path, arcname=str(file_path.relative_to(release_root)).replace("\\", "/"))

    summary = {
        "timestamp": now.isoformat(),
        "version": args.version,
        "release_name": args.release_name,
        "release_id": release_id,
        "dry_run": bool(args.dry_run),
        "release_root": str(release_root),
        "zip_path": str(zip_path),
        "notes_path": str(notes_path),
        "included": included_count,
        "missing": missing_count,
        "artifacts": [asdict(status) for status in statuses],
    }

    if not args.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Release root: {release_root}")
    print(f"Release notes: {notes_path}")
    print(f"Release zip: {zip_path}")
    print(f"Included artifacts: {included_count}")
    print(f"Missing artifacts: {missing_count}")
    if not args.dry_run:
        print(f"Release report: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
