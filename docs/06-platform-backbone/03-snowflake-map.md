# 5.3 — Snowflake capability map for EA

| EA need | Snowflake capability | Notes |
|---|---|---|
| Ingest | Snowpipe / Snowpipe Streaming [@snowflake-snowpipe] | Billing, logs, SBOMs |
| Continuous transforms | Dynamic Tables [@snowflake-dynamic-tables] | Reconciliation, funnels |
| Orchestrate | Tasks / task graphs [@snowflake-tasks] | Scenario DAGs |
| Containers | SPCS + `EXECUTE JOB SERVICE` [@snowflake-execute-job-service] [@snowflake-spcs-jobs-as-tasks] | Archify compile jobs |
| Govern | Horizon [@snowflake-horizon] | Classification, lineage, masking |
| AI | Cortex [@snowflake-cortex] | Analyst/Search/guardrails |
| ML registry | Model Registry [@snowflake-model-registry] | S11 companion |
| Exec apps | Streamlit in Snowflake [@snowflake-streamlit] | Steward portals, TIME |

## Citations

- [@snowflake-snowpipe]
- [@snowflake-dynamic-tables]
- [@snowflake-tasks]
- [@snowflake-execute-job-service]
- [@snowflake-spcs-jobs-as-tasks]
- [@snowflake-horizon]
- [@snowflake-cortex]
- [@snowflake-streamlit]
- [@snowflake-model-registry]


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

