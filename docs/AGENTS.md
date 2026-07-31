# Documentation Agent Rules

## Scope

These rules apply to every file below `docs/` in the shared MDSoftware-DE governance repository.

## Required Structure

- Operational documents include Purpose, Current Status Snapshot, Last Change, Quick Test, and Maintenance Rule.
- Architecture decisions belong under `architecture/`.
- Mermaid source belongs under `diagrams/` and follows the canonical color and compatibility rules in `docs/codex/CODEX_ORG_STANDARDS.md`.
- Operational procedures belong under `runbooks/`.
- Approved specifications and implementation plans remain under `superpowers/`.
- Dated migration evidence belongs under `reports/`.

## Verification

Run `python .github/scripts/validate_docs_governance.py` and `git diff --check` before committing documentation changes.

## Maintenance Rule

Update this file whenever the documentation layout or validation contract changes.
