# 5.2 — Databricks capability map for EA

| EA need | Databricks capability | Notes |
|---|---|---|
| Ingest files/events | Auto Loader [@databricks-autoloader] | CUR, SBOM JSON, flow logs |
| Ingest SaaS/DB | Lakeflow Connect [@databricks-lakeflow] | ServiceNow, Salesforce patterns |
| Transform/graph | Spark + DLT [@databricks-dlt] | CMDB matching, process mining |
| Orchestrate | Workflows/Jobs [@databricks-workflows] | Scenario DAGs |
| Govern | Unity Catalog [@databricks-unity-catalog] | Lineage, permissions |
| ML/AI estate | MLflow [@databricks-mlflow] | S11 chain of custody |
| Coding agent | Genie Code [@databricks-genie-code] | Data-team agent in workspace |
| Exec apps | Databricks Apps [@databricks-apps] | Host Archify + metrics |
| NL analytics | AI/BI Genie (business) vs Genie Code (technical) | Do not conflate |

## Citations

- [@databricks-autoloader]
- [@databricks-lakeflow]
- [@databricks-dlt]
- [@databricks-workflows]
- [@databricks-unity-catalog]
- [@databricks-mlflow]
- [@databricks-genie-code]
- [@databricks-apps]


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

