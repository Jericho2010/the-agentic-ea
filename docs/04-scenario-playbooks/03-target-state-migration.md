# S03 — Target State Architecture & Cloud Migration Roadmapping

## 1. Orbus Infinity baseline

As-is/to-be landscapes, roadmaps, dependency views for migration waves.

## 2. Failure modes of the legacy pattern

Static drawings diverge from IaC; non-data apps ignored if only warehouse migration tools used.

## 3. Agent-native modern alternative

LikeC4/Structurizr + Infracost; Archify **architecture** + **sequence** for cutover waves. [@likec4] [@structurizr]

**Primary Archify type(s):** `architecture + sequence`

## 4. Databricks pattern

Federation/migration tooling for data estates; Workflows track burndown; Genie Code helps refactor jobs. [@databricks-genie-code]

## 5. Snowflake pattern

SnowConvert/Open Catalog patterns for data migration; Tasks track milestones.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | IaC + ADRs in Git (agent-native) |
| **Analytics** | Platform migration telemetry |
| **Renders** | Archify architecture/sequence |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Visio/Structurizr only | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Application, hosted_on |
| Writes | target-state hosted_on edges |

## 10. Citations

[@likec4] [@structurizr] [@orbus-infinity-product] [@databricks-genie-code] [@archify-github] [@wcid-agy-research]


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

