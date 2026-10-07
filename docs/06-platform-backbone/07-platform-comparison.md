# 5.7 — Side-by-side platform comparison for EA

| Dimension | Databricks | Snowflake | EA implication |
|---|---|---|---|
| Heavy graph/process compute | Strong (Spark) | Possible but different shape | Prefer DBX for S06/S10/S18-class |
| Governed semantic metrics / masking | UC + semantic layers evolving | Horizon strong | Prefer SF for S08/S01/S16-class |
| ML training→serving lineage | MLflow+UC excellent | Model Registry + Cortex | Prefer DBX for S11 default |
| Containerized sidecars | Jobs clusters / apps | SPCS + EXECUTE JOB SERVICE | Both can compile Archify |
| Data-team coding agent | Genie Code | Cortex + notebooks | Different personas |
| Exec app UX | Databricks Apps | Streamlit in Snowflake | Both viable |
| Cost model | DBU/compute oriented | Warehouse/serverless SQL oriented | FinOps modeling differs |

Neither platform replaces Orbus Infinity alone. Pair with agent-native enforcement + PAM.

## Citations

- [@databricks-genie-code]
- [@databricks-mlflow]
- [@snowflake-horizon]
- [@snowflake-execute-job-service]
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

