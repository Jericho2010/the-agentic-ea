# 1.6 — Baseline comparison tables

Quick-reference tables before the ladders.

## Table A — Orbus job vs open instinct

| Orbus job | Open / modern instinct |
|---|---|
| Repository | Git + catalog (Backstage) + lakehouse graph |
| CoreEA | PAM (ArchiMate relations + Backstage UX) |
| Diagram UX | Archify / C4 DSL / Eraser (see Part II) |
| CMDB sync | Lakeflow/Snowpipe/connectors + reconciliation jobs |
| ARB | PR + OPA + ADR + visual diff |
| Executive report | Databricks Apps / Streamlit in Snowflake / Genie / Cortex |

## Table B — Truth types Orbus often conflates

| Truth type | Example | Better owner when modernizing |
|---|---|---|
| Intended | ADR, IaC, OpenAPI, capability YAML | Git / inner loop |
| Observed | Runtime traffic, CUR bills, CMDB CDC | Lakehouse + sensors |
| Decided | ARB approval | Git + audit table |
| Presented | TIME matrix diagram | Archify / app tier |

## Table C — Scenario → primary Orbus capability

| Scenario | Primary capabilities |
|---|---|
| S01 APM/TIME | C4, C12 |
| S02 EOL | C5, C11 |
| S03 Migration | C15, C9 |
| S04 Capabilities | C3, C12 |
| S05 ARB | C11, C2 |
| S06 CMDB | C10, C1 |
| S07 M&A | C1, C9 |
| S08 Privacy | C6, C14 |
| S09 Interfaces | C8, C9 |
| S10 Process | C7, C3 |
| S11 AI Gov | C6, C11 |
| S12 DR | C14, C15 |
| S13 Tech debt | C4, C12 |
| S14 Zero-Trust | C14, C9 |
| S15 SBOM | C5, C11 |
| S16 FinOps | C4, C12 |
| S17 MDM | C6 |
| S18 ESG | C5, C12 |
| S19 Teams | C13, C4 |
| S20 Vendor exit | C5, C15 |

## Citations

- [@orbus-infinity-product]
- [@backstage-software-catalog]
- [@wcid-agy-research]


## Chapter validation checklist

| Check | Status |
|---|---|
| Baseline fidelity | PASS |
| Modern option completeness | N/A (baseline part) |
| API hygiene | PASS |
| Archify accuracy | N/A |
| Internal consistency | PASS |
| Citations present | PASS |
| TOC linkage | PASS |
| Editorial (Orbus spelling) | PASS |

**Validation status:** PASS  
**Confidence overall:** medium

