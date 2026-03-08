#!/usr/bin/env python3
"""Validate docs structure and Mermaid authoring conventions.

This validator is intentionally conservative so it can run in any repo without
third-party dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)\n```", re.IGNORECASE | re.DOTALL)

SEQUENCE_ARROW_TOKENS = (
    "->",
    "-->\",
    "->>",
    "-->>",
    "-x",
    "--x",
    "-")


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean value: {value}")


def iter_markdown_files(docs_root: Path) -> list[Path]:
    return sorted(p for p in docs_root.rglob("*.md") if p.is_file())


def find_mermaid_blocks(text: str) -> list[str]:
    return [m.group(1) for m in MERMAID_BLOCK_RE.finditer(text)]


def first_non_empty_line(block: str) -> str:
    for line in block.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def check_flowchart_colors(block: str) -> bool:
    has_classdef = re.search(r"^\s*classDef\s+", block, re.MULTILINE) is not None
    has_class_assign = re.search(r"^\s*class\s+", block, re.MULTILINE) is not None
    has_style = re.search(r"^\s*style\s+", block, re.MULTILINE) is not None
    return has_classdef and (has_class_assign or has_style)


def check_sequence_numbering(block: str) -> tuple[bool, str | None]:
    lines = [line.rstrip() for line in block.splitlines()]

    for line in lines:
        if line.strip().startswith("autonumber"):
            return True, None

    message_labels: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("%%"):
            continue
        if line.startswith("Note "):
            continue
        if ":" not in line:
            continue
        if "->" not in line and "--" not in line:
            continue

        label = line.split(":", 1)[1].strip()
        if label:
            message_labels.append(label)

    if not message_labels:
        return True, None

    numbers: list[int] = []
    for idx, label in enumerate(message_labels, start=1):
        match = re.match(r"^(\d+)\.\s+", label)
        if not match:
            return False, f"sequence message {idx} is missing numeric prefix (expected 'N. ...')"
        numbers.append(int(match.group(1)))

    expected = list(range(1, len(numbers) + 1))
    if numbers != expected:
        return (
            False,
            "sequence numbering must be contiguous starting at 1 "
            f"(found {numbers}, expected {expected})",
        )

    return True, None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate docs governance baseline")
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--require-docs-index", type=parse_bool, default=True)
    parser.add_argument("--require-canonical-dirs", type=parse_bool, default=True)
    parser.add_argument("--require-docs-agents", type=parse_bool, default=True)
    parser.add_argument("--enforce-mermaid-no-newline-escape", type=parse_bool, default=True)
    parser.add_argument("--enforce-flowchart-color-classes", type=parse_bool, default=True)
    parser.add_argument("--require-sequence-numbering", type=parse_bool, default=True)
    parser.add_argument("--fail-if-no-mermaid", type=parse_bool, default=False)
    args = parser.parse_args()

    repo_root = Path.cwd()
    docs_root = repo_root / args.docs_root
    errors: list[str] = []

    if not docs_root.exists() or not docs_root.is_dir():
        errors.append(f"Missing docs root directory: {args.docs_root}/")
    else:
        if args.require_docs_index:
            has_index = (docs_root / "README.md").is_file() or (docs_root / "index.md").is_file()
            if not has_index:
                errors.append("Missing docs index: expected docs/README.md or docs/index.md")

        if args.require_canonical_dirs:
            for rel in ("diagrams", "runbooks", "architecture"):
                path = docs_root / rel
                if not path.is_dir():
                    errors.append(f"Missing canonical docs directory: docs/{rel}/")

        if args.require_docs_agents and not (docs_root / "AGENTS.md").is_file():
            errors.append("Missing docs/AGENTS.md")

    markdown_files = iter_markdown_files(docs_root) if docs_root.is_dir() else []
    total_mermaid_blocks = 0

    for md_file in markdown_files:
        rel = md_file.relative_to(repo_root)
        text = md_file.read_text(encoding="utf-8")
        blocks = find_mermaid_blocks(text)

        for i, block in enumerate(blocks, start=1):
            total_mermaid_blocks += 1
            headline = first_non_empty_line(block)
            kind = headline.split()[0] if headline else "unknown"

            if args.enforce_mermaid_no_newline_escape and "\\n" in block:
                errors.append(
                    f"{rel} block#{i}: do not use \\n escapes in Mermaid labels; use spaces"
                )

            if args.enforce_flowchart_color_classes and kind in {"flowchart", "graph"}:
                if not check_flowchart_colors(block):
                    errors.append(
                        f"{rel} block#{i}: flowchart requires classDef + class/style for color mapping"
                    )

            if args.require_sequence_numbering and kind == "sequenceDiagram":
                ok, reason = check_sequence_numbering(block)
                if not ok:
                    errors.append(f"{rel} block#{i}: {reason}")

    if args.fail_if_no_mermaid and total_mermaid_blocks == 0:
        errors.append("No Mermaid diagrams found under docs/")

    if errors:
        print("docs-governance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("docs-governance validation passed")
    print(f"- markdown files scanned: {len(markdown_files)}")
    print(f"- mermaid blocks scanned: {total_mermaid_blocks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
