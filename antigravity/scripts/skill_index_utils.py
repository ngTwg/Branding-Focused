"""Shared utilities for skill indexing, semantic search, and quality analysis."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ANTIGRAVITY_ROOT = ROOT / "antigravity"
SKILLS_ROOT = ANTIGRAVITY_ROOT / "skills"

DEFAULT_INVENTORY = ANTIGRAVITY_ROOT / "external" / "UNIFIED_SKILL_INVENTORY.json"
DEFAULT_CATALOG = ANTIGRAVITY_ROOT / "external" / "SKILL_CATALOG.json"

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", flags=re.DOTALL)
CODE_FENCE_RE = re.compile(r"```[\s\S]*?```", flags=re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_\-\+]{1,}")

# Keep stop words compact for predictable behavior and low overhead.
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
    "this",
    "these",
    "those",
    "you",
    "your",
    "can",
    "will",
    "not",
    "when",
    "how",
    "what",
    "where",
    "why",
    "into",
    "over",
    "under",
    "than",
    "then",
    "they",
    "them",
    "their",
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def normalize_path(value: str) -> str:
    return value.replace("\\", "/")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, False

    metadata: dict[str, Any] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, text[match.end() :], True


def strip_markdown(text: str) -> str:
    cleaned = CODE_FENCE_RE.sub(" ", text)
    cleaned = MARKDOWN_LINK_RE.sub(r"\1", cleaned)
    cleaned = cleaned.replace("`", " ")
    cleaned = re.sub(r"^#+\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\|", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for match in TOKEN_RE.finditer(text.lower()):
        token = match.group(0)
        if len(token) < 2:
            continue
        if token in STOP_WORDS:
            continue
        tokens.append(token)
    return tokens


def resolve_record_path(record: dict[str, Any]) -> Path:
    raw = Path(str(record.get("path", "")))
    source = str(record.get("source", ""))

    if raw.as_posix().startswith("antigravity/"):
        return (ROOT / raw).resolve()
    if "PRIMARY" in source:
        return (SKILLS_ROOT / raw).resolve()
    return (ROOT / raw).resolve()


def load_inventory_records(inventory_path: Path | None = None) -> list[dict[str, Any]]:
    path = inventory_path or DEFAULT_INVENTORY
    payload = load_json(path, default={})
    records = payload.get("records", []) if isinstance(payload, dict) else []
    return records if isinstance(records, list) else []


def read_record_text(record: dict[str, Any], max_chars: int = 2500) -> tuple[bool, str, int, int]:
    path = resolve_record_path(record)
    if not path.exists() or not path.is_file():
        return False, "", 0, 0

    text = path.read_text(encoding="utf-8", errors="ignore")
    _, body, _ = parse_frontmatter(text)
    cleaned = strip_markdown(body)
    if max_chars > 0:
        cleaned = cleaned[:max_chars]
    line_count = len(text.splitlines())
    return True, cleaned, line_count, len(text)


def build_record_document(record: dict[str, Any], include_content_chars: int = 2500) -> tuple[str, dict[str, Any]]:
    exists, cleaned, line_count, char_count = read_record_text(record, max_chars=include_content_chars)
    key = str(record.get("key", ""))
    category = str(record.get("category", "unknown"))
    rel_path = str(record.get("path", ""))
    source = str(record.get("source", "unknown"))
    repo = record.get("repo")
    security_level = record.get("security_level")

    doc = " ".join(part for part in [key, category, rel_path, str(repo or ""), cleaned] if part)
    meta = {
        "key": key,
        "category": category,
        "path": rel_path,
        "source": source,
        "repo": str(repo) if repo else None,
        "security_level": str(security_level) if security_level else None,
        "file_exists": exists,
        "line_count": line_count,
        "char_count": char_count,
    }
    return doc, meta


def stable_file_hash(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
