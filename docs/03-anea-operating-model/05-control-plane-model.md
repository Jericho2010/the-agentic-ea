# 3.5 — Control-plane vs analytics ownership

This chapter corrects exclusive “winner” thinking from early research scorecards.

## Three roles

| Role | Question it answers |
|---|---|
| **Enforces** | What stops a bad change? |
| **Analytics** | What computes enterprise-scale truth? |
| **Renders** | What do humans look at? |

## Worked examples

| Scenario | Enforces | Analytics | Renders |
|---|---|---|---|
| S05 ARB | PR + OPA | Audit tables in UC/Horizon | Archify workflow/architecture diff |
| S08 Privacy | Tag policies / masking | Column lineage & access history | Archify dataflow |
| S16 FinOps | Budget/tag policies in cloud | CUR amortization SQL | Archify cost-labeled architecture |
| S02 EOL | Renovate PR + CI fail | Inventory warehouse optional | Archify lifecycle |

## Implications

- Databricks vs Snowflake competition is mostly about **analytics fit**.
- Agent-native wins most **enforcement** loci.
- Archify is almost never the system of record.

## Citations

- [@opa-conftest]
- [@databricks-unity-catalog]
- [@snowflake-horizon]
- [@wcid-agy-research]


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

