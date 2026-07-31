#!/usr/bin/env python3
"""Enforce the MDSoftware-DE Wolverine GitHub Actions runner policy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

WORKFLOW_SUFFIXES = {".yml", ".yaml"}
REQUIRED_LABELS = {"self-hosted", "wolverine"}
HOSTED_LABEL_RE = re.compile(r"^(?:ubuntu|windows|macos)(?:-.+)?$", re.IGNORECASE)
KEY_RE = re.compile(r"^([A-Za-z0-9_.-]+):(?:\s*(.*))?$")
KNOWN_WOLVERINE_REUSABLES = {
    "deterministic-builds-reusable.yml",
    "docs-governance-reusable.yml",
    "policy-standards-reusable.yml",
    "quality-gate-reusable.yml",
    "security-checks-reusable.yml",
}
EXPECTED_DYNAMIC_RUNS_ON = "${{ fromJSON(inputs.runner_labels) }}"


class PolicyDataError(ValueError):
    """Raised when the policy or workflow contract cannot be interpreted safely."""


@dataclass(frozen=True)
class Finding:
    repository: str
    workflow: str
    job: str
    value: str
    reason: str


@dataclass
class JobRecord:
    name: str
    runs_on: Optional[str] = None
    uses: Optional[str] = None
    runner_labels: Optional[str] = None


def _indent(raw: str) -> int:
    return len(raw) - len(raw.lstrip(" "))


def _strip_comment(raw: str) -> str:
    quote: Optional[str] = None
    escaped = False
    output: List[str] = []
    for char in raw:
        if escaped:
            output.append(char)
            escaped = False
            continue
        if char == "\\" and quote == '"':
            output.append(char)
            escaped = True
            continue
        if char in {"'", '"'}:
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            output.append(char)
            continue
        if char == "#" and quote is None:
            break
        output.append(char)
    return "".join(output).rstrip()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        inner = value[1:-1]
        if value[0] == "'":
            return inner.replace("''", "'")
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return inner
        return str(decoded)
    return value


def _parse_labels(value: str) -> Optional[List[str]]:
    normalized = _unquote(value)
    if "${{" in normalized:
        return None
    if not normalized:
        raise PolicyDataError("runner label value is empty")
    if normalized.startswith("[") and normalized.endswith("]"):
        try:
            parsed = json.loads(normalized)
        except json.JSONDecodeError:
            parsed = [_unquote(item.strip()) for item in normalized[1:-1].split(",")]
        if not isinstance(parsed, list):
            raise PolicyDataError(f"runner label array is invalid: {value}")
        labels = [str(item).strip() for item in parsed if str(item).strip()]
    elif normalized.startswith('"') and normalized.endswith('"'):
        parsed_scalar = json.loads(normalized)
        labels = [str(parsed_scalar).strip()]
    else:
        labels = [normalized.strip()]
    if not labels:
        raise PolicyDataError("runner label list is empty")
    return labels


def _display_labels(labels: Iterable[str]) -> str:
    values = list(labels)
    if len(values) == 1:
        return values[0]
    return json.dumps(values, separators=(",", ":"))


def _labels_reason(labels: Sequence[str]) -> Optional[str]:
    normalized = {label.lower() for label in labels}
    hosted = sorted(label for label in labels if HOSTED_LABEL_RE.match(label))
    if hosted:
        return "GitHub-hosted runner labels are prohibited: " + ", ".join(hosted)
    missing = sorted(REQUIRED_LABELS - normalized)
    if missing:
        return "Wolverine runner labels are incomplete; missing: " + ", ".join(missing)
    return None


def _workflow_paths(repo_root: Path) -> List[Path]:
    workflow_dir = repo_root / ".github" / "workflows"
    if not workflow_dir.is_dir():
        return []
    return sorted(
        path
        for path in workflow_dir.iterdir()
        if path.is_file() and path.suffix.lower() in WORKFLOW_SUFFIXES
    )


def _parse_jobs(lines: Sequence[str]) -> List[JobRecord]:
    jobs_indent: Optional[int] = None
    job_indent: Optional[int] = None
    current: Optional[JobRecord] = None
    current_with_indent: Optional[int] = None
    records: List[JobRecord] = []
    index = 0
    while index < len(lines):
        raw = _strip_comment(lines[index])
        stripped = raw.strip()
        indent = _indent(raw)
        if not stripped:
            index += 1
            continue
        if jobs_indent is None:
            if stripped == "jobs:":
                jobs_indent = indent
            index += 1
            continue
        if indent <= jobs_indent:
            break
        match = KEY_RE.match(stripped)
        if match and indent == jobs_indent + 2:
            current = JobRecord(name=match.group(1))
            records.append(current)
            job_indent = indent
            current_with_indent = None
            index += 1
            continue
        if current is None or job_indent is None or indent <= job_indent:
            index += 1
            continue
        if current_with_indent is not None and indent <= current_with_indent:
            current_with_indent = None
        if stripped == "with:":
            current_with_indent = indent
            index += 1
            continue
        if stripped.startswith("uses:"):
            current.uses = _unquote(stripped.split(":", 1)[1])
            index += 1
            continue
        if stripped.startswith("runner_labels:") and current_with_indent is not None:
            current.runner_labels = stripped.split(":", 1)[1].strip()
            index += 1
            continue
        if stripped.startswith("runs-on:"):
            value = stripped.split(":", 1)[1].strip()
            if not value:
                sequence_labels: List[str] = []
                lookahead = index + 1
                while lookahead < len(lines):
                    candidate = _strip_comment(lines[lookahead])
                    if not candidate.strip():
                        lookahead += 1
                        continue
                    if _indent(candidate) <= indent:
                        break
                    item = candidate.strip()
                    if not item.startswith("-"):
                        break
                    sequence_labels.append(_unquote(item[1:].strip()))
                    lookahead += 1
                if sequence_labels:
                    value = json.dumps(sequence_labels, separators=(",", ":"))
                    index = lookahead
                    current.runs_on = value
                    continue
            current.runs_on = value
        index += 1
    return records


def _runner_default(lines: Sequence[str]) -> Optional[str]:
    for index, raw_line in enumerate(lines):
        raw = _strip_comment(raw_line)
        if raw.strip() != "runner_labels:":
            continue
        base_indent = _indent(raw)
        for candidate_raw in lines[index + 1 :]:
            candidate = _strip_comment(candidate_raw)
            if not candidate.strip():
                continue
            if _indent(candidate) <= base_indent:
                break
            if candidate.strip().startswith("default:"):
                return candidate.strip().split(":", 1)[1].strip()
    return None


def _is_known_central_reusable(uses: str) -> bool:
    prefix = "MDSoftware-DE/.github/.github/workflows/"
    if not uses.startswith(prefix) or "@" not in uses:
        return False
    workflow_name = uses[len(prefix) :].split("@", 1)[0]
    return workflow_name in KNOWN_WOLVERINE_REUSABLES


def _workflow_findings(repo_root: Path, repository: str, path: Path) -> List[Finding]:
    relative = path.relative_to(repo_root).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: List[Finding] = []
    dynamic_default_checked = False
    for job in _parse_jobs(lines):
        if job.runs_on is not None:
            labels = _parse_labels(job.runs_on)
            if labels is None:
                normalized_dynamic = _unquote(job.runs_on)
                if normalized_dynamic != EXPECTED_DYNAMIC_RUNS_ON:
                    findings.append(Finding(repository, relative, job.name, normalized_dynamic, "Dynamic runs-on expression is not the approved runner_labels contract"))
                elif not dynamic_default_checked:
                    dynamic_default_checked = True
                    default_value = _runner_default(lines)
                    if default_value is None:
                        findings.append(Finding(repository, relative, "workflow_call.inputs.runner_labels", "missing", "Dynamic Wolverine runner contract has no runner_labels default"))
                    else:
                        default_labels = _parse_labels(default_value)
                        if default_labels is None:
                            findings.append(Finding(repository, relative, "workflow_call.inputs.runner_labels", _unquote(default_value), "runner_labels default must be a literal JSON label array"))
                        else:
                            reason = _labels_reason(default_labels)
                            if reason:
                                findings.append(Finding(repository, relative, "workflow_call.inputs.runner_labels", _display_labels(default_labels), reason))
            else:
                reason = _labels_reason(labels)
                if reason:
                    findings.append(Finding(repository, relative, job.name, _display_labels(labels), reason))
            continue
        if job.uses:
            if not _is_known_central_reusable(job.uses):
                findings.append(Finding(repository, relative, job.name, job.uses, "Reusable workflow is not in the known Wolverine-default set"))
                continue
            if job.runner_labels is not None:
                labels = _parse_labels(job.runner_labels)
                if labels is None:
                    findings.append(Finding(repository, relative, job.name, _unquote(job.runner_labels), "Reusable runner_labels override must be literal"))
                else:
                    reason = _labels_reason(labels)
                    if reason:
                        findings.append(Finding(repository, relative, job.name, _display_labels(labels), reason))
    return findings


def _load_allowlist(path: Path) -> List[Dict[str, str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyDataError(f"cannot load allowlist {path}: {exc}") from exc
    if payload.get("version") != 1 or not isinstance(payload.get("exceptions"), list):
        raise PolicyDataError("allowlist must contain version 1 and an exceptions list")
    required = {"repository", "workflow", "job", "value", "reason", "owner", "approval", "review_date"}
    validated: List[Dict[str, str]] = []
    for index, item in enumerate(payload["exceptions"]):
        if not isinstance(item, dict):
            raise PolicyDataError(f"allowlist exception {index} is not an object")
        missing = sorted(key for key in required if not isinstance(item.get(key), str) or not item[key].strip())
        if missing:
            raise PolicyDataError(f"allowlist exception {index} has missing fields: {', '.join(missing)}")
        try:
            date.fromisoformat(item["review_date"])
        except ValueError as exc:
            raise PolicyDataError(f"allowlist exception {index} has invalid review_date") from exc
        if not item["approval"].startswith("https://github.com/"):
            raise PolicyDataError(f"allowlist exception {index} approval must be a GitHub URL")
        validated.append({key: str(item[key]) for key in required})
    return validated


def _apply_allowlist(findings: Sequence[Finding], exceptions: Sequence[Dict[str, str]], today: date) -> List[Finding]:
    remaining: List[Finding] = []
    for finding in findings:
        matches = [
            item
            for item in exceptions
            if item["repository"] == finding.repository
            and item["workflow"] == finding.workflow
            and item["job"] == finding.job
            and item["value"] == finding.value
        ]
        active = [item for item in matches if date.fromisoformat(item["review_date"]) >= today]
        if active:
            continue
        if matches:
            expired = max(item["review_date"] for item in matches)
            remaining.append(Finding(finding.repository, finding.workflow, finding.job, finding.value, f"Matching allowlist entry expired on {expired}; {finding.reason}"))
        else:
            remaining.append(finding)
    return remaining


def validate_repository(repo_root: Path, repository: str, allowlist_path: Path, today: date) -> List[Finding]:
    root = repo_root.resolve()
    findings: List[Finding] = []
    for path in _workflow_paths(root):
        findings.extend(_workflow_findings(root, repository, path))
    exceptions = _load_allowlist(allowlist_path)
    return sorted(_apply_allowlist(findings, exceptions, today), key=lambda item: (item.workflow, item.job, item.value))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--repository", required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parser().parse_args(argv)
    try:
        findings = validate_repository(args.repo_root, args.repository, args.allowlist, date.today())
    except PolicyDataError as exc:
        print(f"runner-policy data error: {exc}", file=sys.stderr)
        return 2
    if findings:
        for finding in findings:
            print(f"{finding.workflow}: job={finding.job} value={finding.value} reason={finding.reason}")
        return 1
    print("runner-policy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
