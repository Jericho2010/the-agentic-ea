# S11 — AI Governance & ML Model Cataloging (EU AI Act)

## 1. Orbus Infinity baseline

Register AI/ML-related assets and link to data/apps for risk committees.

## 2. Failure modes of the legacy pattern

Model cards in Git without training-to-serving lineage.

## 3. Agent-native modern alternative

Parse Model Cards; OpenLLMetry; Archify **architecture** of LLM pipelines.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

MLflow + UC lineage; Mosaic gateway controls; event Workflow on promotion. [@databricks-mlflow] [@databricks-unity-catalog]

## 5. Snowflake pattern

Model Registry + Cortex guardrails + Horizon RBAC/audit. [@snowflake-model-registry] [@snowflake-cortex]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Promotion gates in ML platform |
| **Analytics** | Databricks MLflow chain strong default |
| **Renders** | Archify architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Model card Markdown | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
| Strength | Shared EA vocabulary | Portable basics | Enforcement next to code | Scale compute / ML / graph | Semantics, governance, SiS |
| Watch-out | Stale declared truth | Manual toil | Weak at huge joins alone | Not full-stack enforcement | Not full-stack enforcement |

## 8. Feasibility notes

- **CI/agents:** Feasible for intended-architecture portions immediately.
- **Notebooks:** Use for analytics/prototypes; do not keep PAM schema only in notebooks.
- **Data Apps / SiS:** Host Archify HTML and metrics; keep URNs identical to PAM.
- **SPCS note:** Prefer Task → `EXECUTE JOB SERVICE` for containerized Archify compile. [@snowflake-execute-job-service] [@snowflake-spcs-jobs-as-tasks]

## 9. PAM read/write

| Direction | Entities / fields |
|---|---|
| Reads | AIModel, DataEntity |
| Writes | realizes + risk_tier |

## 10. Citations

[@databricks-mlflow] [@snowflake-model-registry] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


## 11. Chapter validation checklist

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
**Confidence overall:** medium

