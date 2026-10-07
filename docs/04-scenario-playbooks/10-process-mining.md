# S10 — Business Process Optimization & Customer Journey Traceability

## 1. Orbus Infinity baseline

Process models linked to applications/capabilities.

## 2. Failure modes of the legacy pattern

Static BPMN ignores real latency and drop-offs.

## 3. Agent-native modern alternative

BPMN parse + OTel correlation; Archify **workflow** with latency labels.

**Primary Archify type(s):** `workflow`

## 4. Databricks pattern

Structured Streaming + DLT process mining on Spark. [@databricks-dlt]

## 5. Snowflake pattern

Snowpipe Streaming + Dynamic Tables funnels; Cortex bottleneck Q&A.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Instrumentation standards |
| **Analytics** | Databricks preferred for heavy mining |
| **Renders** | Archify workflow |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | BPMN + BI | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | BusinessProcess, Application |
| Writes | latency metrics on serves edges |

## 10. Citations

[@databricks-dlt] [@snowflake-dynamic-tables] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

