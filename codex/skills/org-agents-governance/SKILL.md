# Skill: org-agents-governance

Use this skill when you need to align a repository with MDSoftware-DE Codex governance.

## Purpose
Apply the shared AGENTS baseline, language defaults, docs structure baseline, and issue hygiene consistently across repositories.

## Inputs
- Target repository name
- Current `AGENTS.md` (if present)
- Current `docs/` structure

## Steps
1. Open `MDSoftware-DE/.github/docs/codex/AGENTS_BASELINE_BLOCK.md`.
2. Ensure target repo has `AGENTS.md`.
3. If missing, create from `MDSoftware-DE/.github/docs/codex/AGENTS_TEMPLATE.md`.
4. If present, ensure the full baseline block exists unchanged.
5. Ensure `docs/AGENTS.md` exists and documents Mermaid authoring constraints.
6. Ensure `.github/workflows/docs-governance.yml` is present and aligned with org defaults.
7. Ensure issue templates in target repo are aligned with org defaults.
8. If drift cannot be fixed immediately, open or update a TOCHECK issue.

## Output
- Repository aligned with org baseline, or
- TOCHECK issue documenting exact drift and remaining actions.

## References
- `references/checklist.md`
- `MDSoftware-DE/.github/docs/codex/CODEX_ORG_STANDARDS.md`
