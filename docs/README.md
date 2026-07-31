# Organization Governance Documentation

## Purpose

Provide the entry point for MDSoftware-DE organization-wide repository governance, reusable workflows, operational standards, designs, plans, and migration evidence.

## Current Status Snapshot

- `codex/` contains canonical agent and documentation standards.
- `architecture/` contains organization architecture decisions.
- `diagrams/` contains governed Mermaid system views.
- `runbooks/` contains operational procedures and recovery guidance.
- `superpowers/specs/` and `superpowers/plans/` contain approved designs and executable plans.
- `reports/` contains dated implementation evidence when a migration produces an organization inventory.

## Last Change

On 2026-07-31, the missing documentation entry point and canonical directories were restored so the repository can pass its own docs-governance validator.

## Quick Test

Run `python .github/scripts/validate_docs_governance.py` from the repository root.

## Maintenance Rule

Keep this index current when a documentation domain is added, renamed, or retired. Every operational document must identify its owner, verification path, and maintenance rule.
