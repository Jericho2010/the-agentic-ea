# S17 — Master Data Management (MDM) & Golden Record Lineage

## 1. Orbus Infinity baseline

Authoritative data entities and lineage to consumers.

## 2. Failure modes of the legacy pattern

No steward UX; competing golden records.

## 3. Agent-native modern alternative

dbt contracts + Great Expectations; Archify **dataflow** lineage.

**Primary Archify type(s):** `dataflow`

## 4. Databricks pattern

Lakeflow + DLT SCD2 golden tables; Workflow lineage extract. [@databricks-dlt]

## 5. Snowflake pattern

Managed connectors + Dynamic Tables matching + DMF + SiS steward portal. [@snowflake-dynamic-tables] [@snowflake-streamlit]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Data contracts in CI |
| **Analytics** | Snowflake strong for steward+metrics package |
| **Renders** | Archify dataflow |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | dbt docs | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | DataEntity, DataDomain |
| Writes | flows_to golden lineage |

## 10. Citations

[@snowflake-dynamic-tables] [@databricks-dlt] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

