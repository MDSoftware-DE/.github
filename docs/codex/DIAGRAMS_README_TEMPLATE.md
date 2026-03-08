# Diagrams

Use this directory for Mermaid diagrams and visual system views.

## Mermaid Baseline (Required)
- No `\\n` escapes inside Mermaid labels.
- Use `classDef` + `class`/`style` color mapping in flowcharts.
- Use `autonumber` or contiguous numeric labels in sequence diagrams.
- Keep syntax GitHub-renderer compatible.

## State Diagram Standard
- Use `stateDiagram-v2`.
- Define at least 3 semantic classes (recommended: `entry`, `active`, `review`, `success`, `error`, `terminal`).
- Use explicit state aliases (`state "Human Label" as state_id`).
- Map classes with grouped `class` assignments and, where useful, inline markers (`state_id:::class`).

## Recommended State Palette
- `entry`: `fill:#E3F2FD,stroke:#1565C0,color:#0D47A1`
- `active`: `fill:#E0F2F1,stroke:#00695C,color:#004D40`
- `review`: `fill:#FFF8E1,stroke:#F9A825,color:#795548`
- `success`: `fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20`
- `error`: `fill:#FBE9E7,stroke:#D84315,color:#BF360C`
- `terminal`: `fill:#ECEFF1,stroke:#546E7A,color:#263238`

## Notes
- Keep each diagram close to the topic it documents.
- Keep labels concise and deterministic.
- Prefer one topic per file under `docs/diagrams/`.
