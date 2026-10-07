# S16 — FinOps Cloud Cost Allocation & Unit Economics Alignment

## 1. Orbus Infinity baseline

Cost attributes rolled to apps/capabilities for showback.

## 2. Failure modes of the legacy pattern

Tag gaps; shared cluster amortization ignored; monthly manual pain.

## 3. Agent-native modern alternative

Infracost PR diffs + OpenCost; Archify **architecture** cost labels.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

Auto Loader CUR; join system.billing.usage; daily Workflow unit economics; Apps. [@databricks-autoloader]

## 5. Snowflake pattern

Snowpipe billing; ACCOUNT_USAGE; Dynamic Tables allocation; Horizon metrics; SiS console. [@snowflake-snowpipe] [@snowflake-horizon]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Cloud tagging policies |
| **Analytics** | Snowflake strong for serverless SQL FinOps |
| **Renders** | Archify architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | CUR + spreadsheets | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Service, InfrastructureNode |
| Writes | cost_monthly_usd |

## 10. Citations

[@snowflake-horizon] [@databricks-autoloader] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

