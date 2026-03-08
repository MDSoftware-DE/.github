# AGENTS.md - docs/

This file defines documentation and diagram quality rules for this repository.

## Scope
- Applies to all files under `docs/`.
- Applies to Mermaid diagrams in markdown code fences.

## Documentation Baseline
- Keep a docs entry point (`docs/README.md` or `docs/index.md`) current.
- Keep canonical structure in sync:
  - `docs/architecture/`
  - `docs/diagrams/`
  - `docs/runbooks/`
- Keep legacy flat docs (`docs/*.md`) cross-linked from the docs entry page.

## Mermaid Rules
- Do not use `\\n` escapes inside Mermaid labels.
- In `docs/diagrams/*` flowcharts, use color mapping via `classDef` and `class` or `style`.
- In `docs/diagrams/*` state diagrams:
  - define at least 3 semantic color groups via `classDef`
  - use semantic class names (for example: `entry`, `active`, `review`, `success`, `error`, `terminal`)
  - map states with grouped `class` assignments and prefer explicit state aliases (`state "Label" as id`)
  - use inline `:::class` markers where needed for GitHub renderer compatibility
- Sequence diagrams must use `autonumber` or explicit contiguous labels (`1.`, `2.`, ...).
- Prefer simple GitHub-compatible Mermaid syntax.

## Change Rules
- When behavior changes, update related docs in the same PR.
- Keep examples and step order aligned with current runtime behavior.
