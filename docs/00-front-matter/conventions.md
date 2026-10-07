# F3 — Conventions, verdict language, confidence grades

## Spelling

- **Orbus Infinity** — product name used throughout this manual.
- **Orbus** — vendor.
- **Orbis** — common misspelling; see [Glossary](../08-appendices/glossary.md) only.

## Scenario IDs

Stable IDs `S01`–`S20` are used in Part I catalogs, Part IV playbooks, Part VI PAM matrices, and the master scorecard. Do not renumber without a migration note.

## Verdict language (control plane)

| Role | Meaning |
|---|---|
| **Enforces** | Where a change is blocked, approved, or applied (CI, OPA, cluster policy, merge gate) |
| **Analytics** | Where large-scale joins, lineage, and semantic metrics live (lakehouse) |
| **Renders** | Where humans see diagrams/apps (Archify HTML, Databricks Apps, Streamlit in Snowflake) |

Prefer: “Agent-native **enforces**; Snowflake **analytics**; Archify **renders**” over “Snowflake wins exclusively.”

## Ladders

| Ladder | Meaning |
|---|---|
| **Legacy** | Orbus Infinity baseline |
| **Earth** | Open-source / conventional replacements |
| **Moon** | Agent-native tooling and verified diagram compile |
| **Mars** | Frontier stretch (MCP canvases, durable agent harnesses, deep runtime sensing) |

## Confidence grades

| Grade | Use when |
|---|---|
| high | Primary vendor documentation cited |
| medium | Established practice; UI/feature names may vary by version |
| low | Research hypothesis or inferred from secondary synthesis |

## Citation form

Inline: `[@bib-id]`  
Keys live in [`references/bib.yaml`](../../references/bib.yaml).

## Archify diagram types

Only: `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`.

## Citations

- [@archify-github]
- See also [AUTHORING.md](../../AUTHORING.md)


## Chapter validation checklist

| Check | Status |
|---|---|
| Baseline fidelity | PASS |
| Modern option completeness (if applicable) | PASS / N/A |
| API hygiene | PASS |
| Archify accuracy (if applicable) | PASS / N/A |
| Internal consistency | PASS |
| Citations present | PASS |
| TOC linkage | PASS |
| Editorial (Orbus spelling) | PASS |

**Validation status:** PASS

