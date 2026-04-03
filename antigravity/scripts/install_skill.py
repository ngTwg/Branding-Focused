"""Install a skill by name from marketplace index into local workspace registry."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from skill_index_utils import resolve_record_path


ROOT = Path(__file__).resolve().parents[2]
ANTIGRAVITY_ROOT = ROOT / "antigravity"
MARKETPLACE = ANTIGRAVITY_ROOT / "external" / "SKILL_MARKETPLACE.json"
INSTALL_ROOT = ANTIGRAVITY_ROOT / "skills" / "installed"
REGISTRY = ANTIGRAVITY_ROOT / "reports" / "installed_skills_registry.json"


def load_marketplace(path: Path) -> list[dict]:
	if not path.exists():
		return []
	try:
		payload = json.loads(path.read_text(encoding="utf-8"))
	except Exception:
		return []
	items = payload.get("items", []) if isinstance(payload, dict) else []
	return items if isinstance(items, list) else []


def find_skill(items: list[dict], name: str) -> dict | None:
	name_norm = name.strip().lower()
	for item in items:
		candidate = str(item.get("name") or "").strip().lower()
		if candidate == name_norm:
			return item
	for item in items:
		candidate = str(item.get("name") or "").strip().lower()
		if name_norm in candidate:
			return item
	return None


def resolve_source_path(item: dict) -> Path | None:
	rel = str(item.get("path") or "").strip()
	if not rel:
		return None

	record = {
		"path": rel,
		"source": str(item.get("source") or ""),
	}
	path = resolve_record_path(record)
	if path.exists() and path.is_file():
		return path

	# Fallback for already-rooted relative paths.
	fallback = ROOT / rel
	if fallback.exists() and fallback.is_file():
		return fallback
	return None


def update_registry(entry: dict) -> None:
	REGISTRY.parent.mkdir(parents=True, exist_ok=True)
	payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "items": []}
	if REGISTRY.exists():
		try:
			payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
		except Exception:
			payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "items": []}

	items = payload.get("items", []) if isinstance(payload, dict) else []
	if not isinstance(items, list):
		items = []
	items = [row for row in items if str(row.get("name", "")) != str(entry.get("name", ""))]
	items.append(entry)
	payload = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		"items": sorted(items, key=lambda row: str(row.get("name", "")).lower()),
	}
	REGISTRY.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def install_skill(name: str, marketplace: Path, dry_run: bool = False) -> tuple[bool, str]:
	items = load_marketplace(marketplace)
	if not items:
		return False, f"Marketplace is empty or missing: {marketplace}"

	item = find_skill(items, name)
	if item is None:
		return False, f"Skill not found: {name}"

	source_path = resolve_source_path(item)
	if source_path is None:
		return False, f"Source path unavailable for skill: {item.get('name')}"

	domain = str(item.get("domain") or "general").strip().lower().replace(" ", "-")
	target_dir = INSTALL_ROOT / domain
	target_dir.mkdir(parents=True, exist_ok=True)
	target_file = target_dir / source_path.name

	if dry_run:
		return True, f"DRY_RUN copy {source_path} -> {target_file}"

	shutil.copy2(source_path, target_file)
	registry_entry = {
		"name": item.get("name"),
		"domain": domain,
		"installed_at": datetime.now(timezone.utc).isoformat(),
		"source": item.get("source"),
		"repo": item.get("repo"),
		"source_path": str(source_path),
		"target_path": str(target_file),
		"quality_score": item.get("quality_score"),
	}
	update_registry(registry_entry)
	return True, f"Installed skill: {item.get('name')} -> {target_file}"


def main() -> int:
	parser = argparse.ArgumentParser(description="Install skill from marketplace")
	parser.add_argument("--name", required=True, help="Skill name to install")
	parser.add_argument("--marketplace", default=str(MARKETPLACE), help="Marketplace JSON path")
	parser.add_argument("--dry-run", action="store_true", help="Print action without copying")
	args = parser.parse_args()

	ok, message = install_skill(name=args.name, marketplace=Path(args.marketplace), dry_run=args.dry_run)
	print(message)
	return 0 if ok else 1


if __name__ == "__main__":
	raise SystemExit(main())