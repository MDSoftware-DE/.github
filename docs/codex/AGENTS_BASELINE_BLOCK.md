<!-- MD-ORG-AGENTS-BASELINE:START -->
## MDSoftware-DE Org Baseline

Default language: English.

Required rules:
- Use English for documentation, issues, pull requests, and operational run notes.
- Do not store secrets, passwords, tokens, or private keys in repository files.
- Keep project-specific operations and architecture guidance in this file.
- For workflow/process changes, document: Purpose, Current Status Snapshot, Last Change, Quick Test, Maintenance Rule.
- Keep docs structure consistent: include `docs/README.md` (or `docs/index.md`), `docs/diagrams/`, `docs/runbooks/`, `docs/architecture/`, and `docs/AGENTS.md`.
- Run every feasible Linux security, policy, quality, test, and build job on Wolverine with labels containing both `self-hosted` and `wolverine`.
- Never add an automatic fallback to GitHub-hosted runners and never disable a required security or quality gate to avoid billing.
- Central reusable workflows in `MDSoftware-DE/.github` must default to `["self-hosted","wolverine"]`; repository-specific labels may only refine that Wolverine pool.
- Treat a queued job as a Wolverine capacity or availability incident. Do not silently change it to `ubuntu-latest`.
- Permit Windows, macOS, or other hosted execution only through an exact centrally documented exception with owner, approval reference, and review date.
- Remember that `actions/upload-artifact` remains GitHub-managed storage and Dependabot remains a GitHub service; migrate those through the separately approved artifact-store and Renovate phases.
- Mermaid authoring baseline:
  - Never use `\\n` in Mermaid labels; use normal spaces.
  - Flowcharts in `docs/diagrams/*` should use `classDef` + `class`/`style` color mapping.
  - State diagrams in `docs/diagrams/*` must define at least 3 semantic color groups with `classDef`, map states using grouped `class`/`style` assignments, use semantic class names (for example: `entry`, `active`, `review`, `success`, `error`, `terminal`), and should prefer explicit state aliases plus inline `:::class` markers for GitHub compatibility.
  - Sequence diagrams must use `autonumber` or explicit contiguous numeric prefixes (`1.`, `2.`, ...), plus colored visual grouping (`rect` or `box`).
  - ER diagrams should use semantic color mapping (`classDef default`, semantic `classDef` + grouped `class`/`style`, or explicit `style` mapping) and keep ER style tokens GitHub-safe (`fill`, `stroke`, `color`; avoid `stroke-width`/`font-weight`).
- Keep this block unchanged so org automation can verify baseline adoption.

<!-- MD-ORG-AGENTS-BASELINE:END -->
