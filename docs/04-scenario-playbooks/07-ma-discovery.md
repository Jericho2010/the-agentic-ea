# S07 — M&A Day-One IT Landscape Discovery

## 1. Orbus Infinity baseline

Stand up fenced repository; import discovery; map overlaps quickly.

## 2. Failure modes of the legacy pattern

Waiting for full Orbus modeling delays Day-One decisions.

## 3. Agent-native modern alternative

Zero-footprint CLI scans of repos/IaC/DNS; Archify **architecture** + **dataflow** fast.

**Primary Archify type(s):** `architecture + dataflow`

## 4. Databricks pattern

Upload dumps; Auto Loader; Clean Rooms for fenced sharing.

## 5. Snowflake pattern

Encrypted stages + Data Clean Rooms; Task DAG discovery.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Tactical agent scans |
| **Analytics** | Clean room joins later |
| **Renders** | Archify architecture/dataflow |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Spreadsheets + interviews | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | raw discoveries |
| Writes | new Node/Service/API entities |

## 10. Citations

[@orbus-infinity-product] [@databricks-autoloader] [@snowflake-tasks] [@archify-github] [@wcid-agy-research]


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

