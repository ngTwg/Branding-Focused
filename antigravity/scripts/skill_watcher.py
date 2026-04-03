"""Watch skill files and trigger incremental discoverability refresh."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "antigravity" / "skills"
EXTERNAL_ROOT = ROOT / "antigravity" / "external" / "community-repos"
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
REPORTS = ROOT / "antigravity" / "reports"
EVENT_LOG = REPORTS / "skill_watcher_events.jsonl"


def snapshot(paths: list[Path]) -> dict[str, tuple[int, int]]:
	state: dict[str, tuple[int, int]] = {}
	for base in paths:
		if not base.exists():
			continue
		for file_path in base.rglob("*.md"):
			try:
				stat = file_path.stat()
			except OSError:
				continue
			rel = file_path.relative_to(ROOT).as_posix()
			state[rel] = (int(stat.st_mtime_ns), int(stat.st_size))
	return state


def diff_paths(old: dict[str, tuple[int, int]], new: dict[str, tuple[int, int]]) -> list[str]:
	changed = []
	keys = set(old.keys()) | set(new.keys())
	for key in sorted(keys):
		if old.get(key) != new.get(key):
			changed.append(key)
	return changed


def append_event(event_type: str, changed_paths: list[str], status: str, details: str) -> None:
	REPORTS.mkdir(parents=True, exist_ok=True)
	payload = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"event": event_type,
		"changed_count": len(changed_paths),
		"changed_paths": changed_paths[:200],
		"status": status,
		"details": details,
	}
	with EVENT_LOG.open("a", encoding="utf-8") as handle:
		handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def run_command(cmd: list[str]) -> tuple[bool, str]:
	try:
		completed = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, check=True)
		out = ((completed.stdout or "") + (completed.stderr or "")).strip()
		return True, out
	except subprocess.CalledProcessError as err:
		out = ((err.stdout or "") + (err.stderr or "")).strip()
		return False, out


def refresh_discoverability(changed_paths: list[str]) -> tuple[bool, str]:
	# Refresh inventory first so new files are visible to catalog generation.
	ok, msg = run_command([str(PYTHON), "antigravity/scripts/generate_unified_inventory.py", "--allow-security-fail"])
	if not ok:
		return False, f"inventory refresh failed: {msg}"

	cmd = [
		str(PYTHON),
		"antigravity/scripts/generate_skill_catalog.py",
		"--base-catalog",
		"antigravity/external/SKILL_CATALOG.json",
	]
	for item in changed_paths[:500]:
		cmd.extend(["--changed-path", item])

	ok2, msg2 = run_command(cmd)
	if not ok2:
		return False, f"catalog refresh failed: {msg2}"

	return True, "inventory+catalog refreshed"


def watch(interval_sec: float, debounce_sec: float, once: bool) -> int:
	watch_paths = [SKILLS_ROOT, EXTERNAL_ROOT]
	previous = snapshot(watch_paths)
	pending: set[str] = set()
	last_change = 0.0

	print("Skill watcher started.")
	print(f"Watching: {[p.as_posix() for p in watch_paths]}")
	print(f"Interval: {interval_sec}s | Debounce: {debounce_sec}s")

	while True:
		time.sleep(max(0.2, interval_sec))
		current = snapshot(watch_paths)
		changed = diff_paths(previous, current)
		previous = current

		if changed:
			pending.update(changed)
			last_change = time.time()
			append_event("change_detected", changed, "pending", "")
			print(f"Detected changes: {len(changed)}")

		if pending and (time.time() - last_change) >= debounce_sec:
			changed_paths = sorted(pending)
			pending.clear()
			ok, details = refresh_discoverability(changed_paths)
			append_event(
				"refresh",
				changed_paths,
				"ok" if ok else "failed",
				details[-4000:],
			)
			print(f"Refresh status: {'ok' if ok else 'failed'}")
			if not ok:
				print(details)
			if once:
				return 0 if ok else 1

		if once and not pending and not changed:
			# In --once mode, run one immediate refresh even if no changes.
			ok, details = refresh_discoverability([])
			append_event("refresh_once", [], "ok" if ok else "failed", details[-4000:])
			print(f"Refresh status: {'ok' if ok else 'failed'}")
			if not ok:
				print(details)
			return 0 if ok else 1


def main() -> int:
	parser = argparse.ArgumentParser(description="Watch skills and hot-reload catalog")
	parser.add_argument("--interval", type=float, default=2.0, help="Polling interval in seconds")
	parser.add_argument("--debounce", type=float, default=2.0, help="Debounce window in seconds")
	parser.add_argument("--once", action="store_true", help="Run one refresh cycle then exit")
	args = parser.parse_args()
	return watch(interval_sec=args.interval, debounce_sec=args.debounce, once=args.once)


if __name__ == "__main__":
	raise SystemExit(main())