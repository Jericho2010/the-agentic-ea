# 2.8 — Delivery & observability

## Delivery

Architecture outputs must ship through the same pathways as software:

| Channel | Artifact |
|---|---|
| PR | ADR + policy log + Archify HTML diff |
| Portal | Backstage / Databricks App / Streamlit in Snowflake |
| Lakehouse tables | PAM nodes/edges queryable by Genie/Cortex |
| Alerts | Drift, EOL, RPO breach, license violation |

## Observability of the EA system itself

Treat the EA platform as a product:

- Pipeline freshness (CMDB sync lag)
- Schema validation failure rates
- % applications with owners
- % interfaces with OpenAPI + runtime evidence
- Archify finalize pass rate

## Intended vs observed

Delivery without observability recreates Orbus rot in Git form. Always retain both planes (see Part III).

## Citations

- [@databricks-apps]
- [@snowflake-streamlit]
- [@backstage-software-catalog]
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

