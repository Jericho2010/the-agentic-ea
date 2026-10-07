# S06 — Continuous ServiceNow CMDB Synchronization & Baseline Hygiene

## 1. Orbus Infinity baseline

Connectors/Orbus Flow sync CIs; reconcile orphans; keep repository baseline.

## 2. Failure modes of the legacy pattern

Naive matching; duplicates; architecture trust collapses.

## 3. Agent-native modern alternative

CloudQuery/Steampipe→DuckDB drift detect; Archify **lifecycle** for CI states.

**Primary Archify type(s):** `lifecycle`

## 4. Databricks pattern

Lakeflow CDC + Auto Loader assets; DLT/graph matching at scale. [@databricks-lakeflow] [@databricks-dlt]

## 5. Snowflake pattern

ServiceNow connector + Dynamic Tables + DMFs for orphan alerts. [@snowflake-dynamic-tables]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Reconciliation job SLO |
| **Analytics** | Databricks preferred for messy graph dedup |
| **Renders** | Archify lifecycle |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Nightly CSV diffs | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | InfrastructureNode, Service |
| Writes | hosted_on drift reconciliation |

## 10. Citations

[@databricks-dlt] [@databricks-lakeflow] [@snowflake-dynamic-tables] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

