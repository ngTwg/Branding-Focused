"""Run security gate checks for external skill markdowns.

PASS/WARN/FAIL checks are policy-driven and focused on actionable risks.
The script emits file-level severity so downstream bridge import can block FAIL files.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import argparse


ROOT = Path(__file__).resolve().parents[2]
TARGET_ROOT = ROOT / "antigravity" / "external" / "community-repos"
REPORT_PATH = ROOT / "antigravity" / "reports" / "security_gate_external_skills.json"
POLICY_PATH = ROOT / "antigravity" / "config" / "external_security_gate_policy.json"


CODE_FENCE_PATTERN = re.compile(r"```(?P<lang>[a-zA-Z0-9_+-]*)\n(?P<body>.*?)```", re.DOTALL)
SHELL_LANGS = {"bash", "sh", "shell", "zsh", "powershell", "pwsh", "cmd", "console"}


DEFAULT_POLICY = {
    "exclude_file_name_regex": [
        r"^code_of_conduct\.md$",
        r"^license(\.md)?$",
    ],
    "exclude_path_regex": [
        r"/\.git/",
        r"/node_modules/",
        r"/dist/",
        r"/build/",
    ],
    "fail_patterns": [
        {
            "id": "destructive_delete_root",
            "regex": r"\brm\s+-rf\s+/(?:\s|$)",
            "scan": "text",
        },
        {
            "id": "powershell_downloadstring_iex",
            "regex": r"(?i)iex\s*\(\s*new-object\s+net\.webclient\s*\)\s*\.downloadstring\(",
            "scan": "text",
        },
        {
            "id": "disk_wipe_pattern",
            "regex": r"(?i)diskpart\b[\s\S]*\bclean\s+all\b",
            "scan": "text",
        },
    ],
    "warn_patterns": [
        {
            "id": "shell_true_subprocess",
            "regex": r"subprocess\.Popen\([^\n]*shell\s*=\s*True",
            "scan": "code",
        },
        {
            "id": "curl_pipe_shell",
            "regex": r"\bcurl\s+[^\n]*\|\s*(?:sh|bash)\b",
            "scan": "command",
        },
        {
            "id": "invoke_webrequest_iex",
            "regex": r"(?i)Invoke-WebRequest\s+[^\n]*\|\s*iex\b",
            "scan": "command",
        },
        {
            "id": "eval_usage",
            "regex": r"\beval\s*\(",
            "scan": "code",
        },
        {
            "id": "exec_usage",
            "regex": r"\bexec\s*\(",
            "scan": "code",
        },
        {
            "id": "prompt_injection_phrase",
            "regex": r"ignore\s+previous\s+instructions",
            "scan": "text",
        },
        {
            "id": "system_prompt_leak_phrase",
            "regex": r"\bsystem\s+prompt\b",
            "scan": "text",
        },
    ],
}


@dataclass
class ScanFinding:
    file: str
    level: str
    rule_id: str
    pattern: str
    snippet: str


@dataclass
class FileSeverity:
    file: str
    level: str
    fail_count: int
    warn_count: int


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lower()


def load_policy(path: Path) -> dict:
    if not path.exists():
        return DEFAULT_POLICY

    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return DEFAULT_POLICY

    policy = dict(DEFAULT_POLICY)
    for key in ("exclude_file_name_regex", "exclude_path_regex", "fail_patterns", "warn_patterns"):
        if key in loaded and isinstance(loaded[key], list):
            policy[key] = loaded[key]
    return policy


def should_skip(path: Path, policy: dict) -> bool:
    file_name = path.name.lower()
    rel_norm = normalize_path(str(path))

    for rx in policy.get("exclude_file_name_regex", []):
        if re.search(rx, file_name, flags=re.IGNORECASE):
            return True

    for rx in policy.get("exclude_path_regex", []):
        if re.search(rx, rel_norm, flags=re.IGNORECASE):
            return True

    return False


def extract_regions(text: str) -> tuple[str, str]:
    code_regions: list[str] = []
    command_regions: list[str] = []

    for match in CODE_FENCE_PATTERN.finditer(text):
        lang = (match.group("lang") or "").strip().lower()
        body = match.group("body") or ""
        code_regions.append(body)
        if lang in SHELL_LANGS:
            command_regions.append(body)

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("$ "):
            command_regions.append(stripped[2:])
            continue
        if stripped.startswith("PS> "):
            command_regions.append(stripped[4:])
            continue
        if re.match(r"^(curl|wget|pip|python|uv|npm|pnpm|yarn|pwsh|powershell|bash|sh|cmd|make|docker|kubectl|git)\b", stripped, flags=re.IGNORECASE):
            command_regions.append(stripped)

    return "\n".join(code_regions), "\n".join(command_regions)


def scan_with_rules(file_path: Path, scan_target: str, rules: list[dict], level: str) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    for rule in rules:
        rule_id = str(rule.get("id", "unnamed_rule"))
        pattern = str(rule.get("regex", ""))
        if not pattern:
            continue

        for match in re.finditer(pattern, scan_target, flags=re.IGNORECASE):
            start = max(0, match.start() - 60)
            end = min(len(scan_target), match.end() + 60)
            findings.append(
                ScanFinding(
                    file=str(file_path),
                    level=level,
                    rule_id=rule_id,
                    pattern=pattern,
                    snippet=scan_target[start:end],
                )
            )
    return findings


def scan_text(path: Path, text: str, policy: dict) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    code_text, command_text = extract_regions(text)

    fail_rules = policy.get("fail_patterns", [])
    warn_rules = policy.get("warn_patterns", [])

    for rule in fail_rules:
        scan_mode = str(rule.get("scan", "text")).lower()
        target = text
        if scan_mode == "code":
            target = code_text
        elif scan_mode == "command":
            target = command_text
        findings.extend(scan_with_rules(path, target, [rule], "FAIL"))

    for rule in warn_rules:
        scan_mode = str(rule.get("scan", "text")).lower()
        target = text
        if scan_mode == "code":
            target = code_text
        elif scan_mode == "command":
            target = command_text
        findings.extend(scan_with_rules(path, target, [rule], "WARN"))

    return findings


def classify(findings: list[ScanFinding]) -> str:
    if any(f.level == "FAIL" for f in findings):
        return "FAIL"
    if any(f.level == "WARN" for f in findings):
        return "WARN"
    return "PASS"


def summarize_file_levels(findings: list[ScanFinding]) -> list[FileSeverity]:
    grouped: dict[str, dict[str, int]] = {}

    for finding in findings:
        grouped.setdefault(finding.file, {"FAIL": 0, "WARN": 0})
        grouped[finding.file][finding.level] += 1

    summaries: list[FileSeverity] = []
    for file_path, counts in grouped.items():
        level = "FAIL" if counts["FAIL"] > 0 else "WARN"
        summaries.append(
            FileSeverity(
                file=file_path,
                level=level,
                fail_count=counts["FAIL"],
                warn_count=counts["WARN"],
            )
        )

    return sorted(summaries, key=lambda item: (item.level != "FAIL", item.file.lower()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run external security gate checks")
    parser.add_argument("--target-root", default=str(TARGET_ROOT), help="External repo root")
    parser.add_argument("--report", default=str(REPORT_PATH), help="Output report path")
    parser.add_argument("--policy", default=str(POLICY_PATH), help="Policy JSON path")
    parser.add_argument("--max-findings", type=int, default=1000, help="Max serialized findings")
    parser.add_argument("--fail-on-warn", action="store_true", help="Return non-zero when WARN findings exist")
    args = parser.parse_args()

    target_root = Path(args.target_root)
    report_path = Path(args.report)
    policy_path = Path(args.policy)

    if not target_root.exists():
        print(f"External repo root not found: {target_root}")
        return 1

    policy = load_policy(policy_path)

    markdown_files = list(target_root.rglob("*.md"))
    all_findings: list[ScanFinding] = []
    skipped_files = 0

    for md_file in markdown_files:
        rel_from_root = md_file.relative_to(ROOT)
        if should_skip(rel_from_root, policy):
            skipped_files += 1
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        all_findings.extend(scan_text(rel_from_root, text, policy))

    file_levels = summarize_file_levels(all_findings)

    status = classify(all_findings)
    fail_files = [row.file for row in file_levels if row.level == "FAIL"]
    warn_files = [row.file for row in file_levels if row.level == "WARN"]

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "policy_path": str(policy_path),
        "scanned_markdown_files": len(markdown_files),
        "skipped_markdown_files": skipped_files,
        "finding_count": len(all_findings),
        "fail_count": sum(1 for f in all_findings if f.level == "FAIL"),
        "warn_count": sum(1 for f in all_findings if f.level == "WARN"),
        "files_with_findings": len(file_levels),
        "blocked_files": fail_files,
        "warn_files": warn_files,
        "file_levels": [asdict(row) for row in file_levels],
        "findings": [asdict(f) for f in all_findings[: args.max_findings]],
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Security gate status: {status}")
    print(f"Scanned markdown files: {len(markdown_files)} (skipped: {skipped_files})")
    print(f"Findings: {len(all_findings)}")
    print(f"Blocked files: {len(fail_files)}")
    print(f"Warn files: {len(warn_files)}")
    print(f"Report: {report_path}")

    if status == "FAIL":
        return 1
    if status == "WARN" and args.fail_on_warn:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
