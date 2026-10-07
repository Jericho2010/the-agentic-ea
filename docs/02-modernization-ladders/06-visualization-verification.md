# 2.6 — Visualization & verification (Archify and peers)

## Orbus baseline

Orbus Infinity provides product diagramming and published views (C9). Value: stakeholder-ready pictures bound to repository objects. Limitation: not a headless, CI-friendly verification compiler.

## Archify (Moon default for verified render)

Archify compiles **typed JSON** into interactive HTML/SVG with validation gates (`finalize`). Supported types: `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`. [@archify-github]

Use Archify when you need:

- Deterministic, reviewable diagram artifacts in Git/CI
- Machine-checkable structure (not freeform LLM PNG)
- Scenario receipts (ARB diffs, TIME maps, lineage)

## Peers

| Tool | Strength vs Archify |
|---|---|
| Structurizr / LikeC4 | Excellent DSL/C4 authoring; pair with Archify when you need Archify’s delivery gates [@structurizr] [@likec4] |
| Eraser | Two-way collaborative canvas + agent integrations [@eraser-io] |
| Mermaid | Lightweight; weaker enterprise verification story |

## Rule

**Visualization is not the metamodel.** Renderers consume PAM subgraphs; they must not invent identity.

## Citations

- [@archify-github]
- [@eraser-io]
- [@structurizr]
- [@likec4]
- [@c4-model]


## Chapter validation checklist

| Check | Status |
|---|---|
| Baseline fidelity | PASS |
| Modern option completeness | PASS |
| API hygiene | PASS |
| Archify accuracy | PASS |
| Internal consistency | PASS |
| Citations present | PASS |
| TOC linkage | PASS |
| Editorial (Orbus spelling) | PASS |

**Validation status:** PASS

