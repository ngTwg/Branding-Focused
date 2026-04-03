"""Routing decision metrics logger for Wave 4 router intelligence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "antigravity" / "reports"
LOG_FILE = REPORTS / "router_metrics.jsonl"


def log_routing_decision(
    *,
    router: str,
    intent: str,
    route_id: str,
    confidence: float,
    chain: list[str],
    metadata: dict[str, Any] | None = None,
) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "router": router,
        "intent": intent,
        "route_id": route_id,
        "confidence": round(float(confidence), 6),
        "chain": chain,
        "metadata": metadata or {},
    }
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def summarize(limit: int = 5000) -> dict[str, Any]:
    if not LOG_FILE.exists():
        return {
            "total": 0,
            "by_router": {},
            "by_route": {},
            "avg_confidence": 0.0,
        }

    lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()[-max(1, limit) :]
    total = 0
    by_router: dict[str, int] = {}
    by_route: dict[str, int] = {}
    confidence_sum = 0.0

    for line in lines:
        try:
            row = json.loads(line)
        except Exception:
            continue
        total += 1
        router = str(row.get("router", "unknown"))
        route_id = str(row.get("route_id", "unknown"))
        by_router[router] = by_router.get(router, 0) + 1
        by_route[route_id] = by_route.get(route_id, 0) + 1
        confidence_sum += float(row.get("confidence", 0.0) or 0.0)

    return {
        "total": total,
        "by_router": dict(sorted(by_router.items(), key=lambda item: (-item[1], item[0]))),
        "by_route": dict(sorted(by_route.items(), key=lambda item: (-item[1], item[0]))),
        "avg_confidence": round(confidence_sum / total, 6) if total else 0.0,
    }


def main() -> int:
    summary = summarize()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
