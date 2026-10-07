# S13 — Technical Debt Quantification & Refactoring Justification

## 1. Orbus Infinity baseline

Health/debt attributes on applications for funding cases.

## 2. Failure modes of the legacy pattern

Jira anecdote without AST/churn evidence.

## 3. Agent-native modern alternative

Sonar/complexity + git hotspots; Archify **architecture** heat colors.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

Git history jobs + Jira velocity joins; Genie Code helps analysis notebooks. [@databricks-genie-code]

## 5. Snowflake pattern

Git integration + SPCS parsers; SiS velocity visuals.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | CI quality gates |
| **Analytics** | Optional lakehouse join to funding systems |
| **Renders** | Archify architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Sonar dashboards | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Service, repo_url |
| Writes | cyclomatic_complexity, churn_score |

## 10. Citations

[@databricks-genie-code] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

