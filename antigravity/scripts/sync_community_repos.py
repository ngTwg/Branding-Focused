"""Sync community repositories used by Antigravity integration pipeline.

Usage:
  python antigravity/scripts/sync_community_repos.py --dry-run
  python antigravity/scripts/sync_community_repos.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "antigravity" / "config" / "community_repo_sources.json"
DEFAULT_TARGET = ROOT / "antigravity" / "external" / "community-repos"
DEFAULT_REPORT = ROOT / "antigravity" / "reports" / "community_repo_sync_report.json"


@dataclass
class RepoResult:
    name: str
    url: str
    target: str
    action: str
    status: str
    message: str


def run_command(cmd: list[str], cwd: Path | None = None, dry_run: bool = False) -> tuple[bool, str]:
    if dry_run:
        return True, "DRY_RUN: " + " ".join(cmd)

    try:
        completed = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, completed.stdout.strip() or completed.stderr.strip() or "ok"
    except subprocess.CalledProcessError as err:
        output = (err.stdout or "") + "\n" + (err.stderr or "")
        return False, output.strip() or str(err)


def resolve_source_path(path_value: str) -> Path:
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate
    return (ROOT / candidate).resolve()


def remove_tree_with_retries(target: Path, retries: int = 6, base_delay_sec: float = 0.3) -> None:
    """Remove directory with retry/backoff to tolerate transient file locks on Windows."""
    if not target.exists():
        return

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            shutil.rmtree(target)
            return
        except PermissionError as err:
            last_error = err
            if attempt == retries:
                break
            time.sleep(base_delay_sec * attempt)

    if last_error is not None:
        raise last_error


def mirror_local_directory(source: Path, target: Path, dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, f"DRY_RUN: mirror {source} -> {target}"

    if target.exists():
        remove_tree_with_retries(target)

    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "*.pyc",
        ),
    )
    return True, "mirrored"


def sync_repo(repo: dict, target_root: Path, dry_run: bool) -> RepoResult:
    name = repo["name"]
    source_type = str(repo.get("source_type", "git")).lower()
    url = repo.get("url", "")
    branch = repo.get("branch", "main")
    target = target_root / name

    if source_type in {"local", "local-dir", "local_path"} or repo.get("local_path"):
        local_path_value = str(repo.get("local_path", "")).strip()
        if not local_path_value:
            return RepoResult(name, "", str(target), "mirror-local", "failed", "Missing local_path")

        source = resolve_source_path(local_path_value)
        if not source.exists() or not source.is_dir():
            return RepoResult(name, str(source), str(target), "mirror-local", "failed", "Source path not found")

        ok, message = mirror_local_directory(source, target, dry_run)
        return RepoResult(name, str(source), str(target), "mirror-local", "ok" if ok else "failed", message)

    if not url:
        return RepoResult(name, "", str(target), "clone", "failed", "Missing url")

    if not target.exists():
        cmd = ["git", "clone", "--depth", "1", "--branch", branch, url, str(target)]
        ok, message = run_command(cmd, dry_run=dry_run)
        return RepoResult(name, url, str(target), "clone", "ok" if ok else "failed", message)

    git_dir = target / ".git"
    if not git_dir.exists():
        return RepoResult(name, url, str(target), "skip", "failed", "Target exists but is not a git repo")

    fetch_ok, fetch_msg = run_command(["git", "fetch", "--all", "--prune"], cwd=target, dry_run=dry_run)
    if not fetch_ok:
        return RepoResult(name, url, str(target), "update", "failed", fetch_msg)

    pull_ok, pull_msg = run_command(["git", "pull", "--ff-only"], cwd=target, dry_run=dry_run)
    if not pull_ok:
        return RepoResult(name, url, str(target), "update", "failed", pull_msg)

    return RepoResult(name, url, str(target), "update", "ok", pull_msg)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync community repositories")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to repository config JSON")
    parser.add_argument("--target-root", default=str(DEFAULT_TARGET), help="Directory where repos are cloned")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="JSON report path")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without running git")
    args = parser.parse_args()

    config_path = Path(args.config)
    target_root = Path(args.target_root)
    report_path = Path(args.report)

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    data = json.loads(config_path.read_text(encoding="utf-8"))
    repos = data.get("repositories", [])
    if not repos:
        raise ValueError("No repositories found in config")

    target_root.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    results: list[RepoResult] = []
    for repo in repos:
        results.append(sync_repo(repo, target_root, args.dry_run))

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": str(config_path),
        "target_root": str(target_root),
        "dry_run": args.dry_run,
        "total": len(results),
        "ok": sum(1 for r in results if r.status == "ok"),
        "failed": sum(1 for r in results if r.status == "failed"),
        "results": [asdict(r) for r in results],
    }

    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Synced repos: {summary['ok']}/{summary['total']} ok, {summary['failed']} failed")
    print(f"Report: {report_path}")

    return 1 if summary["failed"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
