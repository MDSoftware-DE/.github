# MDSoftware-DE Org Defaults

Default community health files, issue templates, and Codex governance defaults for repositories in the MDSoftware-DE organization.

## Language Policy

English is the default language for:
- Documentation
- GitHub issues
- Pull request titles and descriptions

See `CONTRIBUTING.md` for full policy details.

## Codex Baseline

Shared Codex standards and AGENTS baseline are maintained here:
- `docs/codex/CODEX_ORG_STANDARDS.md`
- `docs/codex/AGENTS_BASELINE_BLOCK.md`
- `docs/codex/AGENTS_TEMPLATE.md`

PR policy baseline:
- Reusable workflow: `.github/workflows/policy-standards-reusable.yml`
- Repo wrapper baseline: `docs/codex/workflows/policy-standards.yml`
- Workflow template: `.github/workflow-templates/policy-standards.yml`

Quality gate baseline:
- Reusable workflow: `.github/workflows/quality-gate-reusable.yml`
- Repo wrapper baseline: `docs/codex/workflows/quality-gate.yml`
- Workflow template: `.github/workflow-templates/quality-gate.yml`

Security baseline:
- Reusable workflow: `.github/workflows/security-checks-reusable.yml`
- Repo wrapper baseline: `docs/codex/workflows/security-checks.yml`
- Workflow template: `.github/workflow-templates/security-checks.yml`

Reusable skill package for Codex instances:
- `codex/skills/org-agents-governance/SKILL.md`
- `codex/skills/README.md`
