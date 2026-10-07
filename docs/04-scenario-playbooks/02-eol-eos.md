# S02 — Technology Obsolescence & Lifecycle Risk (EOL/EOS)

## 1. Orbus Infinity baseline

Technology objects tracked with lifecycle states; standards library flags non-compliant tech; reports for risk committees.

## 2. Failure modes of the legacy pattern

Inventory incomplete; no automated remediation; reports without PRs.

## 3. Agent-native modern alternative

Syft/Trivy + endoflife.date; Renovate opens upgrade PRs; Archify **lifecycle** Active→Deprecated→Sunset. [@endoflife-date]

**Primary Archify type(s):** `lifecycle`

## 4. Databricks pattern

Workflow fetches EOL/CVE feeds; cluster inventory in UC; Lakehouse Monitoring flags deprecated runtimes. [@databricks-workflows] [@databricks-unity-catalog]

## 5. Snowflake pattern

External access from SPCS/Notebooks to EOL APIs; Tasks alert; registry image checks. [@snowflake-tasks]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Agent-native CI + Renovate |
| **Analytics** | Optional warehouse inventory |
| **Renders** | Archify lifecycle |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Spreadsheets + endoflife.date | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | TechnologyService, repo_url |
| Writes | attributes.eol_status |

## 10. Citations

[@endoflife-date] [@orbus-infinity-product] [@databricks-workflows] [@snowflake-tasks] [@archify-github] [@wcid-agy-research]


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

