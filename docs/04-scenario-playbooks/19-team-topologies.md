# S19 — Team Topologies & Organizational Alignment (Conway's Law)

## 1. Orbus Infinity baseline

Owner/team fields on objects; org charts linked loosely.

## 2. Failure modes of the legacy pattern

HR charts ≠ commit coupling reality.

## 3. Agent-native modern alternative

CODEOWNERS + co-authorship graphs + PR latency; Archify **architecture** + **workflow** handoffs. [@team-topologies]

**Primary Archify type(s):** `architecture + workflow`

## 4. Databricks pattern

Monthly Workflow co-change matrices + Jira joins.

## 5. Snowflake pattern

Git integration + Workday joins; Task graph analysis in SPCS.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Ownership required in CI catalog |
| **Analytics** | Optional HR joins |
| **Renders** | Archify architecture/workflow |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | ORG charts + CODEOWNERS | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Service, owner_team |
| Writes | team boundaries, communication edges |

## 10. Citations

[@team-topologies] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

