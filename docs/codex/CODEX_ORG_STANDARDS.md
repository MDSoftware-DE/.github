# Codex Org Standards

This document defines the minimum standard for Codex-driven changes across MDSoftware-DE repositories.

## Default Language
English is the default language for:
- Documentation
- GitHub issues
- Pull request titles and descriptions
- Operational run notes

## Required Repo Files
Each active repository should contain:
- `AGENTS.md` with the org baseline block from `docs/codex/AGENTS_BASELINE_BLOCK.md`
- `docs/AGENTS.md` with repository-specific documentation and Mermaid authoring notes
- `.github/ISSUE_TEMPLATE/*` aligned with the org baseline
- `.github/workflows/policy-standards.yml` aligned with `docs/codex/workflows/policy-standards.yml`
- `.github/workflows/quality-gate.yml` aligned with `docs/codex/workflows/quality-gate.yml`
- `.github/workflows/security-checks.yml` aligned with `docs/codex/workflows/security-checks.yml`
- `.github/workflows/deterministic-builds.yml` aligned with `docs/codex/workflows/deterministic-builds.yml`
- `.github/workflows/docs-governance.yml` aligned with `docs/codex/workflows/docs-governance.yml`
- `pull_request_template.md` and `CONTRIBUTING.md` aligned with org defaults

## Documentation Structure Baseline
Documentation is standardized around these canonical paths:
- `docs/README.md` (or `docs/index.md`) as entry point
- `docs/architecture/` for architecture-level artifacts
- `docs/diagrams/` for Mermaid diagrams and visual system views
- `docs/runbooks/` for operational procedures and recovery playbooks

When legacy flat files exist (for example `docs/architecture.md`), keep them linked and migrate incrementally.

## Mermaid Quality Baseline
- Do not use `\\n` escape sequences in Mermaid labels.
- Use color mapping in flowcharts (`classDef` + `class`/`style`) for key domains.
- Use semantic color grouping in state diagrams (`classDef` + `class`/`style`) so state families are visually separated by intent (for example: entry, processing, success, warning/error, terminal).
- Sequence diagrams must use `autonumber` or explicit contiguous prefixes (`1.`, `2.`, ...).
- Prefer diagrams under `docs/diagrams/` and keep them renderer-safe for GitHub.

## Enforcement Model
- Org defaults live in `MDSoftware-DE/.github`.
- Reusable PR policy workflow source:
  - `.github/workflows/policy-standards-reusable.yml`
- Reusable quality gate workflow source:
  - `.github/workflows/quality-gate-reusable.yml`
- Reusable security checks workflow source:
  - `.github/workflows/security-checks-reusable.yml`
- Reusable deterministic builds workflow source:
  - `.github/workflows/deterministic-builds-reusable.yml`
- Reusable docs governance workflow source:
  - `.github/workflows/docs-governance-reusable.yml`
- Drift detection workflows run from `MDSoftware-DE/nas-hulk-config` and open TOCHECK issues per repository.
- Branch protection baseline is applied where GitHub plan features permit it.
  - Public repositories: enforced.
  - Private repositories on user account plans may require GitHub Pro for branch protection/rulesets.

## Onboarding New Repositories
1. Copy `docs/codex/AGENTS_TEMPLATE.md` to `<repo>/AGENTS.md`.
2. Add `docs/AGENTS.md` with repo-specific documentation guidance.
3. Add `.github/workflows/policy-standards.yml` from `docs/codex/workflows/policy-standards.yml`.
4. Add `.github/workflows/quality-gate.yml` from `docs/codex/workflows/quality-gate.yml`.
5. Add `.github/workflows/security-checks.yml` from `docs/codex/workflows/security-checks.yml`.
6. Add `.github/workflows/deterministic-builds.yml` from `docs/codex/workflows/deterministic-builds.yml`.
7. Add `.github/workflows/docs-governance.yml` from `docs/codex/workflows/docs-governance.yml`.
8. Confirm issue templates come from org defaults.
9. Keep `pull_request_template.md` and `CONTRIBUTING.md` aligned with org defaults.
10. Create the first TOCHECK issue only if intentional deviations are required.
