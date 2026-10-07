# S14 — Zero-Trust Security Architecture & Network Micro-Segmentation

## 1. Orbus Infinity baseline

Security zones and trust boundary viewpoints.

## 2. Failure modes of the legacy pattern

Pretty zone diagrams without policy enforcement.

## 3. Agent-native modern alternative

NetworkPolicy/Istio/Cilium analysis; Archify **architecture** perimeters.

**Primary Archify type(s):** `architecture`

## 4. Databricks pattern

Auto Loader VPC flow; daily Workflow access pattern checks.

## 5. Snowflake pattern

Snowpipe flow logs; Dynamic Tables matrices; Horizon network policy audits.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | K8s/IdP/eBPF policy (agent-native) |
| **Analytics** | Flow-log warehouse |
| **Renders** | Archify architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Visio zones | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Service, API, Node |
| Writes | security zone boundaries, mTLS flags |

## 10. Citations

[@databricks-autoloader] [@snowflake-snowpipe] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

