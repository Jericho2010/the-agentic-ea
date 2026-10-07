# S18 — ESG & Green IT Carbon Footprint Accounting

## 1. Orbus Infinity baseline

Environmental attributes on tech/infra for sustainability reporting.

## 2. Failure modes of the legacy pattern

Vendor carbon CSVs without allocation to services.

## 3. Agent-native modern alternative

Kepler/CCF CLIs; Archify **architecture** carbon heatmap.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

Auto Loader carbon/IoT; monthly Workflow LCA on Spark. [@databricks-workflows]

## 5. Snowflake pattern

Snowpipe carbon reports; Cortex document parse for invoices; monthly Task.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Measurement standards |
| **Analytics** | Databricks preferred for econometric joins |
| **Renders** | Archify architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Annual ESG spreadsheet | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | InfrastructureNode, CloudResource |
| Writes | carbon_kg_co2e |

## 10. Citations

[@databricks-workflows] [@snowflake-snowpipe] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

