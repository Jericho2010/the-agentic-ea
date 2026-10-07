# S12 — Disaster Recovery & Business Continuity (RTO/RPO Alignment)

## 1. Orbus Infinity baseline

Capture RTO/RPO, redundancy, dependency chains for BCP.

## 2. Failure modes of the legacy pattern

Data replication monitored; compute/DNS/failover untested.

## 3. Agent-native modern alternative

Multi-region IaC audit + chaos experiments; Archify **lifecycle** + **architecture**.

**Primary Archify type(s):** `lifecycle + architecture`

## 4. Databricks pattern

Geo-replication monitors; hourly Workflow SLA checks.

## 5. Snowflake pattern

Failover groups + ACCOUNT_USAGE replication history Tasks.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | IaC + game days (agent-native full stack) |
| **Analytics** | Replication telemetry |
| **Renders** | Archify lifecycle/architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | BCP documents | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | InfrastructureNode, Database |
| Writes | rto_minutes, rpo_minutes |

## 10. Citations

[@orbus-infinity-product] [@databricks-workflows] [@snowflake-tasks] [@archify-github] [@wcid-agy-research]


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

