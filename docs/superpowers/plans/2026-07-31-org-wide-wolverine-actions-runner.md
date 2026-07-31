# Organization-Wide Wolverine GitHub Actions Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move every feasible MDSoftware-DE GitHub Actions job to Wolverine, enforce the rule centrally, persist it in global Codex and Claude instructions, and prove the change with the DGX Spark security canary.

**Architecture:** Central reusable workflows default to `["self-hosted","wolverine"]`. A dependency-free validator checks active workflow files and a narrow allowlist, while global and canonical agent instructions prevent future sessions from restoring hosted runners. The DGX Spark PR is the first live canary; organization repositories then migrate in recorded batches.

**Tech Stack:** GitHub Actions YAML, Python 3 standard library, `unittest`, GitHub CLI, Git, Markdown, Wolverine self-hosted runners.

---

## File Map

- Modify `/volume1/homes/Miki/.codex/AGENTS.md`: effective global Codex rule.
- Modify `/volume1/homes/Miki/.claude/CLAUDE.md`: effective global Claude rule and removal of stale central-default wording.
- Modify `AGENTS.md`: central repository lessons and operating rule.
- Modify `docs/codex/AGENTS_BASELINE_BLOCK.md`: canonical organization rule distributed to repositories.
- Modify `docs/codex/AGENTS_TEMPLATE.md`: new-repository agent template.
- Modify `docs/codex/CODEX_ORG_STANDARDS.md`: human-readable CI ownership standard.
- Create `docs/README.md`, `docs/AGENTS.md`, `docs/architecture/README.md`, `docs/diagrams/README.md`, and `docs/runbooks/README.md`: restore the declared documentation baseline.
- Create `.github/runner-policy-allowlist.json`: exact, reviewable exceptions with owner and expiry.
- Create `.github/scripts/validate_runner_policy.py`: dependency-free workflow runner-policy validator.
- Create `.github/scripts/tests/test_validate_runner_policy.py`: validator contract tests.
- Create `.github/workflows/runner-policy.yml`: central repository policy check on Wolverine.
- Modify `.github/workflows/policy-standards-reusable.yml`: enforce runner policy in consumers.
- Modify the five `.github/workflows/*-reusable.yml` files: Wolverine defaults and examples.
- Modify `.github/workflow-templates/policy-standards.yml`: enable the guardrail explicitly in new consumers.
- Modify `/volume1/homes/Miki/.config/superpowers/worktrees/dgx-spark-vision-config/qwen36-dynamo-phase1/.github/workflows/security-checks.yml`: explicit Wolverine canary labels before the central default reaches `main`.
- Create `docs/reports/2026-07-31-wolverine-runner-inventory.md`: organization migration evidence.

### Task 1: Persist the no-hosted-runner rule globally and canonically

**Files:**
- Modify: `/volume1/homes/Miki/.codex/AGENTS.md`
- Modify: `/volume1/homes/Miki/.claude/CLAUDE.md`
- Modify: `AGENTS.md`
- Modify: `docs/codex/AGENTS_BASELINE_BLOCK.md`
- Modify: `docs/codex/AGENTS_TEMPLATE.md`
- Modify: `docs/codex/CODEX_ORG_STANDARDS.md`

- [ ] **Step 1: Back up the two effective global files without overwriting an existing backup**

Run:
```sh
cp --update=none /volume1/homes/Miki/.codex/AGENTS.md /volume1/homes/Miki/.codex/AGENTS.md.pre-wolverine-phase1
cp --update=none /volume1/homes/Miki/.claude/CLAUDE.md /volume1/homes/Miki/.claude/CLAUDE.md.pre-wolverine-phase1
```
Expected: both source files remain unchanged and each backup exists.

- [ ] **Step 2: Add the identical durable rule block to both global files and the canonical organization baseline**

Use this exact rule content:
```markdown
## GitHub Actions Build Routing — permanent organization rule

- Run every feasible Linux security, policy, quality, test, and build job on Wolverine with labels containing both `self-hosted` and `wolverine`.
- Never add an automatic fallback to GitHub-hosted runners and never disable a required security or quality gate to avoid billing.
- Central reusable workflows in `MDSoftware-DE/.github` must default to `["self-hosted","wolverine"]`; repository-specific labels may only refine that Wolverine pool.
- Treat a queued job as a Wolverine capacity or availability incident. Do not silently change it to `ubuntu-latest`.
- Permit Windows, macOS, or other hosted execution only through an exact centrally documented exception with owner, approval reference, and review date.
- Remember that `actions/upload-artifact` remains GitHub-managed storage and Dependabot remains a GitHub service; migrate those through the separately approved artifact-store and Renovate phases.
```

In Claude, replace the stale lesson that says the central default is `ubuntu-latest`; do not keep contradictory instructions.

- [ ] **Step 3: Verify the effective files contain the same normalized rule block**

Run:
```sh
python -c "from pathlib import Path; files=[Path(\"/volume1/homes/Miki/.codex/AGENTS.md\"),Path(\"/volume1/homes/Miki/.claude/CLAUDE.md\")]; required=[\"self-hosted\",\"wolverine\",\"Never add an automatic fallback\",\"actions/upload-artifact\",\"Dependabot\"]; assert all(all(token in p.read_text() for token in required) for p in files)"
rg -n "default is .*ubuntu-latest|Default ist .*ubuntu-latest" /volume1/homes/Miki/.codex/AGENTS.md /volume1/homes/Miki/.claude/CLAUDE.md
```
Expected: Python exits 0; `rg` exits 1 because no stale default statement remains.

- [ ] **Step 4: Commit only the repository-owned canonical rule changes**

```sh
git add AGENTS.md docs/codex/AGENTS_BASELINE_BLOCK.md docs/codex/AGENTS_TEMPLATE.md docs/codex/CODEX_ORG_STANDARDS.md
git commit -m "docs: make Wolverine the permanent CI runner rule"
```

### Task 2: Restore the central documentation-governance baseline

**Files:**
- Create: `docs/README.md`
- Create: `docs/AGENTS.md`
- Create: `docs/architecture/README.md`
- Create: `docs/diagrams/README.md`
- Create: `docs/runbooks/README.md`

- [ ] **Step 1: Run the existing validator and record the expected red baseline**

Run: `python .github/scripts/validate_docs_governance.py`

Expected: failure naming the missing docs index, canonical directories, and `docs/AGENTS.md`.

- [ ] **Step 2: Create the minimal governed documentation structure**

`docs/README.md` links to `architecture/`, `diagrams/`, `runbooks/`, `codex/`, `superpowers/specs/`, `superpowers/plans/`, and `reports/`. `docs/AGENTS.md` states that operational documents use Purpose, Current Status Snapshot, Last Change, Quick Test, and Maintenance Rule. Each directory README explains its ownership and contains no empty promises.

- [ ] **Step 3: Re-run the validator**

Run: `python .github/scripts/validate_docs_governance.py`

Expected: `docs-governance validation passed`.

- [ ] **Step 4: Commit the baseline repair**

```sh
git add docs/README.md docs/AGENTS.md docs/architecture/README.md docs/diagrams/README.md docs/runbooks/README.md
git commit -m "docs: restore governance baseline"
```

### Task 3: Build the runner-policy validator test-first

**Files:**
- Create: `.github/runner-policy-allowlist.json`
- Create: `.github/scripts/tests/test_validate_runner_policy.py`
- Create: `.github/scripts/validate_runner_policy.py`

- [ ] **Step 1: Write contract tests for accepted and rejected workflows**

The test module must create temporary repositories and cover these exact cases:

- `test_accepts_literal_wolverine_labels`
- `test_rejects_ubuntu_latest`
- `test_rejects_self_hosted_without_wolverine`
- `test_accepts_central_reusable_default`
- `test_rejects_reusable_override_to_hosted_runner`
- `test_accepts_exact_unexpired_allowlist_entry`
- `test_rejects_expired_allowlist_entry`
- `test_ignores_workflow_examples_outside_active_workflow_directory`
- `test_reports_path_and_job_for_each_violation`

Fixtures use active files under `.github/workflows/`; the exception fixture contains repository, workflow path, job, reason, owner, approval URL, and ISO review date.

- [ ] **Step 2: Run the tests and verify the red state is caused by the missing validator**

Run: `python -m unittest discover -s .github/scripts/tests -p "test_validate_runner_policy.py" -v`

Expected: import failure for `validate_runner_policy`, not a syntax or fixture failure.

- [ ] **Step 3: Implement the dependency-free validator**

The module exposes:

- Immutable `Finding` records with `repository`, `workflow`, `job`, `value`, and `reason` string fields.
- Public callable `validate_repository(repo_root: Path, repository: str, allowlist_path: Path, today: date) -> list[Finding]`.
- CLI entry point `main(argv: Sequence[str] | None = None) -> int`.

It scans only `.github/workflows/*.yml` and `.yaml`, tracks YAML indentation for job scopes, validates literal `runs-on` strings and arrays, validates explicit `with.runner_labels` JSON on central reusable calls, and treats an omitted override as valid only when the referenced MDSoftware-DE reusable is in the known Wolverine-default set. Dynamic expressions not matching the central `fromJSON(inputs.runner_labels)` contract fail closed. Exit 0 means clean, exit 1 means policy findings, and exit 2 means invalid policy data.

The allowlist starts as:
```json
{"version":1,"exceptions":[]}
```

- [ ] **Step 4: Run validator tests and repository smoke checks**

```sh
python -m unittest discover -s .github/scripts/tests -p "test_validate_runner_policy.py" -v
python .github/scripts/validate_runner_policy.py --repo-root . --repository MDSoftware-DE/.github --allowlist .github/runner-policy-allowlist.json
```

Expected: all named tests pass; the repository smoke reports no unapproved active hosted runner.

- [ ] **Step 5: Commit the validator**

```sh
git add .github/runner-policy-allowlist.json .github/scripts/validate_runner_policy.py .github/scripts/tests/test_validate_runner_policy.py
git commit -m "feat: enforce Wolverine runner policy"
```

### Task 4: Switch all central reusable defaults to Wolverine

**Files:**
- Modify: `.github/workflows/deterministic-builds-reusable.yml`
- Modify: `.github/workflows/docs-governance-reusable.yml`
- Modify: `.github/workflows/policy-standards-reusable.yml`
- Modify: `.github/workflows/quality-gate-reusable.yml`
- Modify: `.github/workflows/security-checks-reusable.yml`

- [ ] **Step 1: Add a failing contract assertion for all five defaults**

Add a test that reads each file and requires exactly one `runner_labels` default equal to the JSON string `["self-hosted","wolverine"]`, while rejecting `ubuntu-latest` and `nightcrawler` in the input description.

- [ ] **Step 2: Run the test and confirm all five old defaults fail**

Run: `python -m unittest discover -s .github/scripts/tests -v`

Expected: one contract failure listing all five reusable workflows.

- [ ] **Step 3: Change descriptions and defaults in all five workflows**

Use this exact input contract:
```yaml
runner_labels:
  description: JSON array for Wolverine runner selection, for example ["self-hosted","wolverine"] or ["self-hosted","wolverine","repository-label"]
  required: false
  default: '["self-hosted","wolverine"]'
  type: string
```

Do not rename jobs, required checks, scanner inputs, or permissions.

- [ ] **Step 4: Run all central tests and scan active workflows**

```sh
python -m unittest discover -s .github/scripts/tests -v
python .github/scripts/validate_runner_policy.py --repo-root . --repository MDSoftware-DE/.github --allowlist .github/runner-policy-allowlist.json
git diff --check
```

Expected: all tests pass, policy is clean, and the diff has no whitespace errors.

- [ ] **Step 5: Commit the default migration**

```sh
git add .github/workflows/deterministic-builds-reusable.yml .github/workflows/docs-governance-reusable.yml .github/workflows/policy-standards-reusable.yml .github/workflows/quality-gate-reusable.yml .github/workflows/security-checks-reusable.yml .github/scripts/tests/test_validate_runner_policy.py
git commit -m "ci: default reusable workflows to Wolverine"
```

### Task 5: Wire the guardrail into central and consumer policy checks

**Files:**
- Create: `.github/workflows/runner-policy.yml`
- Modify: `.github/workflows/policy-standards-reusable.yml`
- Modify: `.github/workflow-templates/policy-standards.yml`

- [ ] **Step 1: Extend tests for workflow wiring**

Require the central workflow to run on `[self-hosted, wolverine]`, checkout the target repository, and invoke `validate_runner_policy.py`. Require the reusable policy workflow to default `enforce_wolverine_runner_policy` to true and invoke the same validator after checking out `MDSoftware-DE/.github` at `main`.

- [ ] **Step 2: Add the central workflow**

```yaml
name: runner-policy
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  validate:
    runs-on: [self-hosted, wolverine]
    steps:
      - uses: actions/checkout@v4
      - name: Validate Wolverine runner policy
        run: python .github/scripts/validate_runner_policy.py --repo-root . --repository "${{ github.repository }}" --allowlist .github/runner-policy-allowlist.json
```

- [ ] **Step 3: Add consumer enforcement to the reusable policy workflow**

Add boolean input `enforce_wolverine_runner_policy` with default true. Checkout the consumer, checkout `MDSoftware-DE/.github@main` into `_org_defaults`, then run the validator with the central allowlist. Keep the existing PR metadata check name `policy/standards` unchanged.

- [ ] **Step 4: Validate workflow wiring and commit**

```sh
python -m unittest discover -s .github/scripts/tests -v
python .github/scripts/validate_runner_policy.py --repo-root . --repository MDSoftware-DE/.github --allowlist .github/runner-policy-allowlist.json
git diff --check
git add .github/workflows/runner-policy.yml .github/workflows/policy-standards-reusable.yml .github/workflow-templates/policy-standards.yml .github/scripts/tests/test_validate_runner_policy.py
git commit -m "ci: add Wolverine runner policy guardrail"
```

### Task 6: Validate, publish, and open the central pull request

**Files:**
- Modify: `docs/reports/2026-07-31-wolverine-runner-inventory.md`

- [ ] **Step 1: Run the complete local gate**

```sh
python .github/scripts/validate_docs_governance.py
python -m unittest discover -s .github/scripts/tests -v
python .github/scripts/validate_runner_policy.py --repo-root . --repository MDSoftware-DE/.github --allowlist .github/runner-policy-allowlist.json
git diff --check
```

Expected: every command exits 0.

- [ ] **Step 2: Inventory organization workflow references without changing repositories**

Use `gh repo list MDSoftware-DE --limit 1000 --json nameWithOwner,isArchived` and targeted GitHub code searches for `runs-on:`, `ubuntu-latest`, `windows-latest`, `macos-latest`, central reusable workflow names, `actions/upload-artifact`, and Dependabot configuration. Record each active repository, workflow path, current runner, reusable caller, artifact usage, and migration state in the report.

- [ ] **Step 3: Commit the inventory report**

```sh
git add docs/reports/2026-07-31-wolverine-runner-inventory.md
git commit -m "docs: inventory organization runner migration"
```

- [ ] **Step 4: Push and open a PR linked to issue 11**

```sh
git push -u origin docs/wolverine-actions-runner-design
gh pr create --repo MDSoftware-DE/.github --base main --head docs/wolverine-actions-runner-design --title "ci: make Wolverine the organization Actions runner" --body-file /tmp/wolverine-actions-pr.md
```

The PR body uses the repository template, links `https://github.com/MDSoftware-DE/.github/issues/11`, lists every verification command, and checks the English confirmation line. Do not merge without separate authorization.

### Task 7: Run the DGX Spark security canary on Wolverine

**Files:**
- Modify: `/volume1/homes/Miki/.config/superpowers/worktrees/dgx-spark-vision-config/qwen36-dynamo-phase1/.github/workflows/security-checks.yml`

- [ ] **Step 1: Verify the existing feature worktree and branch before editing**

```sh
git -C /volume1/homes/Miki/.config/superpowers/worktrees/dgx-spark-vision-config/qwen36-dynamo-phase1 status --short --branch
git -C /volume1/homes/Miki/.config/superpowers/worktrees/dgx-spark-vision-config/qwen36-dynamo-phase1 rev-parse HEAD
```

Expected: branch `feat/qwen36-dynamo-phase1`, clean worktree, and existing phase-1 commit history.

- [ ] **Step 2: Add the explicit canary override**

Under the existing reusable security job `with:` block add:
```yaml
runner_labels: '["self-hosted","wolverine","vision-config"]'
```

Parse the resulting YAML and assert there is exactly one `with:` mapping for the job.

- [ ] **Step 3: Run the repository contract tests and commit**

Run the existing workflow contract test suite and `git diff --check`. Commit with `ci: run security checks on Wolverine`, then push the existing branch.

- [ ] **Step 4: Re-run and inspect PR 138 checks**

Use `gh pr checks 138 --repo MDSoftware-DE/dgx-spark-vision-config --watch` and inspect both security job logs.

Expected: Semgrep and Gitleaks start on Wolverine, execute non-empty steps, and no job contains the GitHub billing annotation. Existing policy, quality, and deterministic-build checks remain green.

### Task 8: Record remaining repository migrations without silent work

**Files:**
- Modify: `docs/reports/2026-07-31-wolverine-runner-inventory.md`

- [ ] **Step 1: Classify every remaining active repository**

Use states `migrated`, `inherits-central-default`, `needs-direct-workflow-change`, `approved-os-exception`, or `no-actions-workflow`. Every non-final state includes an issue URL and exact workflow paths.

- [ ] **Step 2: Search before creating each repository issue**

Run:
```sh
gh repo list MDSoftware-DE --limit 1000 --json nameWithOwner,isArchived --jq ".[] | select(.isArchived == false) | .nameWithOwner" > /tmp/mdsoftware-active-repos.txt
while IFS= read -r repository; do
  gh issue list --repo "$repository" --state all --search "Wolverine runner migration in:title"
done < /tmp/mdsoftware-active-repos.txt
```
Update a matching issue or create one detailed English issue; never create duplicates.

- [ ] **Step 3: Update central issue 11 and the central PR**

Comment with the inventory commit, the canary evidence, repositories migrated through inherited defaults, direct migrations still required, artifact-storage users for the later Harbor phase, and Dependabot users for the later Renovate phase.

- [ ] **Step 4: Produce the implementation checkpoint**

Report commits, changed global files, backup paths, test counts, central PR URL, canary run URLs, unresolved repository issues, runner capacity risks, and confirm that no production/runtime service was changed.

## Final Verification

- [ ] Both effective global files contain the permanent rule and no stale central-default statement.
- [ ] Canonical agent templates carry the same policy.
- [ ] All five reusable defaults are Wolverine JSON arrays.
- [ ] The structured guardrail rejects hosted labels and accepts only exact live exceptions.
- [ ] Docs governance and all unit/contract tests pass.
- [ ] DGX Spark Semgrep and Gitleaks execute on Wolverine with real steps.
- [ ] Organization inventory and follow-up issues are complete.
- [ ] No workflow silently falls back to GitHub-hosted compute.
- [ ] No production or runtime host was modified.

## Execution Mode

Execute inline with `superpowers:executing-plans` because the current collaboration mode does not authorize subagent delegation. Stop for review before any merge; pushing branches and opening pull requests are allowed by the approved implementation scope.
