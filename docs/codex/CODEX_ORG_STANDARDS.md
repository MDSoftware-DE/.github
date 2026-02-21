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
- `.github/ISSUE_TEMPLATE/*` aligned with the org baseline
- `.github/workflows/policy-standards.yml` aligned with `docs/codex/workflows/policy-standards.yml`
- `.github/workflows/quality-gate.yml` aligned with `docs/codex/workflows/quality-gate.yml`
- `pull_request_template.md` and `CONTRIBUTING.md` aligned with org defaults

## Enforcement Model
- Org defaults live in `MDSoftware-DE/.github`.
- Reusable PR policy workflow source:
  - `.github/workflows/policy-standards-reusable.yml`
- Reusable quality gate workflow source:
  - `.github/workflows/quality-gate-reusable.yml`
- Drift detection workflows run from `MDSoftware-DE/nas-hulk-config` and open TOCHECK issues per repository.
- Branch protection baseline is applied where GitHub plan features permit it.
  - Public repositories: enforced.
  - Private repositories on user account plans may require GitHub Pro for branch protection/rulesets.

## Onboarding New Repositories
1. Copy `docs/codex/AGENTS_TEMPLATE.md` to `<repo>/AGENTS.md`.
2. Add `.github/workflows/policy-standards.yml` from `docs/codex/workflows/policy-standards.yml`.
3. Add `.github/workflows/quality-gate.yml` from `docs/codex/workflows/quality-gate.yml`.
4. Confirm issue templates come from org defaults.
5. Keep `pull_request_template.md` and `CONTRIBUTING.md` aligned with org defaults.
6. Create the first TOCHECK issue only if intentional deviations are required.
