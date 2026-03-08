<!-- MD-ORG-AGENTS-BASELINE:START -->
## MDSoftware-DE Org Baseline

Default language: English.

Required rules:
- Use English for documentation, issues, pull requests, and operational run notes.
- Do not store secrets, passwords, tokens, or private keys in repository files.
- Keep project-specific operations and architecture guidance in this file.
- For workflow/process changes, document: Purpose, Current Status Snapshot, Last Change, Quick Test, Maintenance Rule.
- Keep docs structure consistent: include `docs/README.md` (or `docs/index.md`), `docs/diagrams/`, `docs/runbooks/`, `docs/architecture/`, and `docs/AGENTS.md`.
- Mermaid authoring baseline:
  - Never use `\\n` in Mermaid labels; use normal spaces.
  - Flowcharts in `docs/diagrams/*` should use `classDef` + `class`/`style` color mapping.
  - Sequence diagrams must use `autonumber` or explicit contiguous numeric prefixes (`1.`, `2.`, ...).
- Keep this block unchanged so org automation can verify baseline adoption.

<!-- MD-ORG-AGENTS-BASELINE:END -->
