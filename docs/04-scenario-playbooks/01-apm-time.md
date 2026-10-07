# S01 — Application Portfolio Rationalization (APM / TIME Model)

## 1. Orbus Infinity baseline

EAs maintain application objects with cost, criticality, and lifecycle attributes; produce TIME (Tolerate/Invest/Migrate/Eliminate) views for investment forums. [@gartner-time] [@orbus-infinity-product]

## 2. Failure modes of the legacy pattern

Stale CMDB links; cost attributes updated annually; TIME becomes political theater without telemetry.

## 3. Agent-native modern alternative

Agents pull Git churn + cloud billing APIs; score health; emit Archify **architecture** TIME quadrants as boundaries.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

Auto Loader ingests CUR/Parquet; Lakeflow Connect for ServiceNow; Workflow aggregates unit cost; App hosts Archify; Genie Code assists notebook logic. [@databricks-autoloader] [@databricks-lakeflow] [@databricks-genie-code] [@databricks-apps]

## 5. Snowflake pattern

Snowpipe loads billing; connectors stream CMDB; Dynamic Tables compute scores; Streamlit hosts Archify; Cortex Analyst answers portfolio questions. [@snowflake-snowpipe] [@snowflake-dynamic-tables] [@snowflake-streamlit] [@snowflake-cortex]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Tagging/policy for required app metadata (cloud + CI) |
| **Analytics** | Snowflake (semantic metrics) or Databricks (if Spark-heavy joins) |
| **Renders** | Archify architecture + SiS/Apps |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | CMDB export + spreadsheet TIME | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Application, Service, Owner |
| Writes | attributes.time_disposition |

## 10. Citations

[@gartner-time] [@orbus-infinity-product] [@databricks-autoloader] [@snowflake-snowpipe] [@archify-github] [@wcid-agy-research]


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

