# S04 — Business Capability Modeling & Strategic Investment Alignment

## 1. Orbus Infinity baseline

Capability hierarchies linked to applications and initiatives for strategy alignment.

## 2. Failure modes of the legacy pattern

Capabilities become poster art; no join to GL/HR spend.

## 3. Agent-native modern alternative

Capability YAML in Git; agents tag repos to capabilities; Archify nested **architecture** boundaries.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

Lakeflow ingests HR/finance; Workflow ROI aggregation; Genie for exec Q&A. [@databricks-lakeflow]

## 5. Snowflake pattern

Managed connectors + Cortex Search/Analyst for strategy docs + spend. [@snowflake-cortex]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Git capability taxonomy ownership |
| **Analytics** | Snowflake preferred for semantic exec metrics |
| **Renders** | Archify architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Capability Markdown trees | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Capability, realizes edges |
| Writes | attributes.capex_allocation, business_value |

## 10. Citations

[@orbus-infinity-product] [@snowflake-cortex] [@databricks-lakeflow] [@archify-github] [@wcid-agy-research]


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

