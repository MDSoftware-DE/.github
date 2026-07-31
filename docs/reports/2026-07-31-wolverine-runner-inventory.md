# Wolverine GitHub Actions Runner Inventory — 2026-07-31

## Purpose

Record the organization-wide default-branch evidence needed to move feasible GitHub Actions execution to Wolverine without disabling required checks or silently using GitHub-hosted billing.

## Current Status Snapshot

- Active repositories inspected: 59.
- Repositories with active workflow files: 43; without workflow files: 16.
- Remote default branches containing GitHub-hosted runner labels: 13. The central `.github` repository is fixed in this branch, leaving 12 direct repository migrations after central integration.
- Repositories already containing explicit Wolverine labels: 19.
- Repositories calling central reusable workflows: 23.
- Repositories using GitHub-managed Actions artifacts: 8.
- Repositories with a default-branch Dependabot configuration: 2.
- Classification: inherits-central-default=17, migrated=12, migrated-in-this-branch=1, needs-direct-workflow-change=12, needs-runner-contract-review=1, no-actions-workflow=16.

Colossus remains exclusively a runtime, deployment, and monitoring target. Renovate and update pull-request automation belong on Wolverine and are already tracked by [vps-wolverine-config#143](https://github.com/MDSoftware-DE/vps-wolverine-config/issues/143). No duplicate Renovate issue is required.

## Last Change

On 2026-07-31, all 59 active organization repositories were queried through GitHub GraphQL using their real default branches. Workflow blobs and `.github/dependabot.yml` were classified from repository contents rather than search-index-only results.

Architecture references:

- [Colossus PR #326](https://github.com/MDSoftware-DE/vps-colossus-config/pull/326), commit `e23466d01937c1b9fd017e2223cbc19f7fb1faab`.
- [Wolverine PR #144](https://github.com/MDSoftware-DE/vps-wolverine-config/pull/144), commit `7ee75dcb01740a5c2896af8db0124bef56beb1a2`.
- [Wolverine Renovate issue #143](https://github.com/MDSoftware-DE/vps-wolverine-config/issues/143).

## Method

- Source: GitHub GraphQL repository objects for every non-archived `MDSoftware-DE` repository.
- Scope: YAML files directly below `.github/workflows/` on each real default branch plus `.github/dependabot.yml`.
- Hosted detection: literal Ubuntu, Windows, or macOS runner labels in `runs-on` or `runner_labels` values.
- Wolverine detection: workflow content containing both `self-hosted` and `wolverine`.
- Reusable detection: calls to `MDSoftware-DE/.github/.github/workflows/`.
- Artifact detection: `actions/upload-artifact` or `actions/download-artifact`.
- This snapshot does not claim that a referenced workflow run has already succeeded; live evidence is recorded separately.

## Repository Classification

| Repository | State | Workflow files | Hosted-label files | Central reusable files | Artifact files | Dependabot | Tracking |
|---|---|---:|---|---|---|---|---|
| `MDSoftware-DE/.github` | `migrated-in-this-branch` | 5 | `deterministic-builds-reusable.yml`, `docs-governance-reusable.yml`, `policy-standards-reusable.yml`, `quality-gate-reusable.yml`, `security-checks-reusable.yml` | — | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/3cx-api` | `migrated` | 1 | — | — | `ci.yml` | no | — |
| `MDSoftware-DE/ai-infra-architecture` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/ai-receptionist-platform` | `migrated` | 2 | — | — | `self-hosted-ci.yml` | no | — |
| `MDSoftware-DE/autodoc-enterprise` | `needs-direct-workflow-change` | 6 | `ci.yml`, `renovate.yml` | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/avv-checker` | `inherits-central-default` | 4 | — | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/car24-n8n-workflows` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/car24-recruiter` | `inherits-central-default` | 2 | — | `deterministic-builds.yml` | — | yes | [Wolverine #143](https://github.com/MDSoftware-DE/vps-wolverine-config/issues/143) |
| `MDSoftware-DE/codex-root` | `inherits-central-default` | 3 | — | `deterministic-builds.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/db-gebrauchtbus-landingpage` | `migrated` | 1 | — | — | `ci.yml` | no | — |
| `MDSoftware-DE/db-regio` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/dgx-spark-heimdall-config` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/dgx-spark-odin-config` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/dgx-spark-vision-config` | `inherits-central-default` | 4 | — | `security-checks.yml` | — | no | — |
| `MDSoftware-DE/dgx-spark-wanda-config` | `inherits-central-default` | 4 | — | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/drs-hagel-agent` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/drs-outbound-terminierung` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/drs-receptionist` | `migrated` | 2 | — | — | — | no | — |
| `MDSoftware-DE/drs-sky-api` | `inherits-central-default` | 2 | — | `ci-terminierung-backend.yml`, `ci.yml` | — | no | — |
| `MDSoftware-DE/empireon-datev-api` | `needs-runner-contract-review` | 18 | — | — | `frontend-e2e.yml`, `frontend-visual.yml`, `mermaid-render.yml`, `release-build.yml`, `secret-scan.yml`, `semgrep.yml` | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/empireon-landingpage-academy` | `migrated` | 2 | — | — | — | no | — |
| `MDSoftware-DE/empireon-landingpage-steuer-ki-ext1` | `needs-direct-workflow-change` | 1 | `ci.yml` | — | — | yes | [central #11](https://github.com/MDSoftware-DE/.github/issues/11); [Wolverine #143](https://github.com/MDSoftware-DE/vps-wolverine-config/issues/143) |
| `MDSoftware-DE/empireon-landingpage-steuerberater` | `migrated` | 1 | — | — | — | no | — |
| `MDSoftware-DE/empireon-landingpage-steuerberater-ext-1` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/empireon-landingpage-voice-ai-ext1` | `needs-direct-workflow-change` | 1 | `deploy.yml` | — | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/etl-mittelhessen` | `inherits-central-default` | 1 | — | `backend-ci.yml` | — | no | — |
| `MDSoftware-DE/etl-standorte-grabber` | `needs-direct-workflow-change` | 6 | `pr-template-guard.yml` | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/etl-voice-ai-receptionist` | `inherits-central-default` | 13 | — | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/infra-nightcrawler` | `inherits-central-default` | 3 | — | `deterministic-builds.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/llm-benchmarks` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/mahn-wizard` | `inherits-central-default` | 4 | — | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/md-dograh-voice-stack` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/md-knowledge-platform` | `migrated` | 2 | — | — | — | no | — |
| `MDSoftware-DE/md-mail-service` | `needs-direct-workflow-change` | 1 | `ci.yml` | — | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/md-n8n-shared-workflows` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/md-outlook-secretary` | `needs-direct-workflow-change` | 9 | `n8n-deploy.yml`, `n8n-post-deploy-rebind.yml`, `repo-hygiene.yml` | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/MD-Vault` | `inherits-central-default` | 4 | — | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/md-website-legacy` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/n8n-retell-invoicing-data` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/nas-hulk-config` | `needs-direct-workflow-change` | 5 | `org-agents-baseline-sync.yml`, `org-issue-template-sync.yml`, `org-pr-docs-remediation-automerge.yml`, `org-pr-docs-standards-sync.yml`, `troubleshooting-guardrails.yml` | — | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/nexus-api` | `migrated` | 11 | — | — | — | no | — |
| `MDSoftware-DE/opencve` | `needs-direct-workflow-change` | 3 | `release-image.yml`, `security-review.yml`, `tests.yml` | — | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/ops-triage` | `migrated` | 2 | — | — | — | no | — |
| `MDSoftware-DE/oracle` | `inherits-central-default` | 4 | — | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/paperless-gpt` | `needs-direct-workflow-change` | 2 | `docker-build-and-push.yml`, `smoke.yml` | — | `docker-build-and-push.yml` | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/paperless-hulk-pipeline` | `inherits-central-default` | 5 | — | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/Powershell` | `inherits-central-default` | 4 | — | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/protocol-slave` | `inherits-central-default` | 8 | — | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | `ci.yml` | no | — |
| `MDSoftware-DE/protocol-slave-legacy` | `inherits-central-default` | 5 | — | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/sauron` | `migrated` | 2 | — | — | `ci.yml`, `promote.yml` | no | — |
| `MDSoftware-DE/toenjes-recruiter` | `migrated` | 6 | — | — | `ci.yml` | no | — |
| `MDSoftware-DE/vps-blade-config` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/vps-colossus-config` | `inherits-central-default` | 5 | — | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | — |
| `MDSoftware-DE/vps-ghost-config` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/vps-nightcrawler-config` | `no-actions-workflow` | 0 | — | — | — | no | — |
| `MDSoftware-DE/vps-wolverine-config` | `migrated` | 2 | — | — | — | no | — |
| `MDSoftware-DE/whisperx-vision-pipeline` | `needs-direct-workflow-change` | 6 | `runtime-path-checks.yml` | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/zugferd` | `needs-direct-workflow-change` | 7 | `github-to-gitlab-sync.yml`, `validate-fixtures-xsd.yml` | `deterministic-builds.yml`, `docs-governance.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |
| `MDSoftware-DE/zukauf-agent-ui` | `needs-direct-workflow-change` | 6 | `i18n-check.yml`, `renovate.yml` | `deterministic-builds.yml`, `policy-standards.yml`, `quality-gate.yml`, `security-checks.yml` | — | no | [central #11](https://github.com/MDSoftware-DE/.github/issues/11) |

## Direct Hosted-Runner Migration Set

- `MDSoftware-DE/.github`: `deterministic-builds-reusable.yml`, `docs-governance-reusable.yml`, `policy-standards-reusable.yml`, `quality-gate-reusable.yml`, `security-checks-reusable.yml`.
- `MDSoftware-DE/autodoc-enterprise`: `ci.yml`, `renovate.yml`.
- `MDSoftware-DE/empireon-landingpage-steuer-ki-ext1`: `ci.yml`.
- `MDSoftware-DE/empireon-landingpage-voice-ai-ext1`: `deploy.yml`.
- `MDSoftware-DE/etl-standorte-grabber`: `pr-template-guard.yml`.
- `MDSoftware-DE/md-mail-service`: `ci.yml`.
- `MDSoftware-DE/md-outlook-secretary`: `n8n-deploy.yml`, `n8n-post-deploy-rebind.yml`, `repo-hygiene.yml`.
- `MDSoftware-DE/nas-hulk-config`: `org-agents-baseline-sync.yml`, `org-issue-template-sync.yml`, `org-pr-docs-remediation-automerge.yml`, `org-pr-docs-standards-sync.yml`, `troubleshooting-guardrails.yml`.
- `MDSoftware-DE/opencve`: `release-image.yml`, `security-review.yml`, `tests.yml`.
- `MDSoftware-DE/paperless-gpt`: `docker-build-and-push.yml`, `smoke.yml`.
- `MDSoftware-DE/whisperx-vision-pipeline`: `runtime-path-checks.yml`.
- `MDSoftware-DE/zugferd`: `github-to-gitlab-sync.yml`, `validate-fixtures-xsd.yml`.
- `MDSoftware-DE/zukauf-agent-ui`: `i18n-check.yml`, `renovate.yml`.

After this central branch is integrated, `MDSoftware-DE/.github` leaves this set. Every other repository in this section requires a repository-owned workflow change or a narrowly documented exception before the central guardrail can be considered organization-complete.

## GitHub-Managed Artifact Users

- `MDSoftware-DE/3cx-api`: `ci.yml`.
- `MDSoftware-DE/ai-receptionist-platform`: `self-hosted-ci.yml`.
- `MDSoftware-DE/db-gebrauchtbus-landingpage`: `ci.yml`.
- `MDSoftware-DE/empireon-datev-api`: `frontend-e2e.yml`, `frontend-visual.yml`, `mermaid-render.yml`, `release-build.yml`, `secret-scan.yml`, `semgrep.yml`.
- `MDSoftware-DE/paperless-gpt`: `docker-build-and-push.yml`.
- `MDSoftware-DE/protocol-slave`: `ci.yml`.
- `MDSoftware-DE/sauron`: `ci.yml`, `promote.yml`.
- `MDSoftware-DE/toenjes-recruiter`: `ci.yml`.

These entries remain on GitHub-managed artifact storage during Phase 1. They feed the separately designed Harbor plus generic artifact-store migration; Harbor is not treated as a universal replacement for arbitrary files.

## Dependency Automation Boundary

- `MDSoftware-DE/car24-recruiter` has a default-branch Dependabot configuration.
- `MDSoftware-DE/empireon-landingpage-steuer-ki-ext1` has a default-branch Dependabot configuration.

Dependabot itself cannot be redirected to Wolverine. Its pull-request checks can run on Wolverine. Any replacement by Renovate is implemented only through [vps-wolverine-config#143](https://github.com/MDSoftware-DE/vps-wolverine-config/issues/143); this phase does not implement Renovate or Watchtower.

## Quick Test

Re-run the GitHub GraphQL inventory against all active repositories, compare repository and classification counts with this snapshot, then run:

```sh
python .github/scripts/validate_runner_policy.py --repo-root . --repository MDSoftware-DE/.github --allowlist .github/runner-policy-allowlist.json
python .github/scripts/validate_docs_governance.py
```

Both validators must exit successfully on the central implementation branch.

## Maintenance Rule

Refresh this report whenever central runner defaults, the hosted-runner allowlist, organization repository membership, artifact storage, or dependency automation ownership changes. Direct repository migrations must link their repository issue and successful Wolverine run before moving to `migrated`.
