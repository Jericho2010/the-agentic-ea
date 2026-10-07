# Authoring Guide — The Agentic EA

This repository is a GitHub-native Markdown ideation manual. Orbus Infinity is the constant baseline.

## Spelling

- Always **Orbus Infinity** (product) and **Orbus** (vendor).
- **Orbis** appears only once in the glossary as a common misspelling.

## Chapter validation rubric

A chapter is **PASS** only if all apply:

1. **Baseline fidelity** — Orbus behavior stated without inventing product features; uncertain items marked `confidence: low|medium|high`
2. **Modern option completeness** — For Parts IV–V: Agent-native + Databricks + Snowflake all present
3. **API hygiene** — No invented Snowflake/Databricks SQL/APIs; disputed claims listed in [fact-check notes](docs/06-platform-backbone/08-factcheck-notes.md)
4. **Archify accuracy** — Diagram types limited to `architecture|workflow|sequence|dataflow|lifecycle`; bridge uses `components`/`connections`/`boundaries.kind`
5. **Internal consistency** — Capability names match Part I canonical map; scenario IDs stable (`S01`–`S20`)
6. **Citations** — Every non-obvious vendor claim has a `references/bib.yaml` key
7. **TOC linkage** — Chapter linked from `SUMMARY.md`
8. **Editorial** — Orbus spelling; illustrative snippets only (no production implementation)

Workflow: author → fill chapter checklist → update `docs/08-appendices/validation-log.md` → mark complete in `SUMMARY.md`.

## Scenario playbook template (Parts 4.1–4.20)

```markdown
# Sxx — Title

## 1. Orbus Infinity baseline
## 2. Failure modes of the legacy pattern
## 3. Agent-native modern alternative
## 4. Databricks pattern
## 5. Snowflake pattern
## 6. Control-plane verdict
## 7. Comparison table
## 8. Feasibility notes
## 9. PAM read/write
## 10. Citations
## 11. Chapter validation checklist
```

## Citation rules

- Add entries to `references/bib.yaml` with stable `id` keys.
- Cite inline as `[@citation-id]`.
- List chapter citations under **Citations**.
- Internal research (WCID-agy, NotebookLM) goes in `source-map.md`, not as sole authority for vendor facts.

## Confidence grades

| Grade | Meaning |
|---|---|
| high | Primary vendor docs or widely established practice |
| medium | Reasonable synthesis; product UI may vary by version |
| low | Inferred or research-hypothesis; verify before design |

## Control-plane verdict language

Prefer dual ownership language:

- **Enforces (control plane):** where change is blocked or applied
- **Analytics (system of record facts):** where enterprise-scale joins live
- **Renders:** Archify / Apps / Streamlit — never owns truth
