# S05 — Architecture Review Board (ARB) Governance & Design Approvals

## 1. Orbus Infinity baseline

Intake forms, reviews, approvals, decision records attached to repository objects.

## 2. Failure modes of the legacy pattern

Disconnected portal; decisions lag delivery; no automated structural checks.

## 3. Agent-native modern alternative

ADRs in PRs; Conftest/OPA; Archify **workflow** gates + **architecture** visual diffs. [@opa-conftest]

**Primary Archify type(s):** `workflow + architecture`

## 4. Databricks pattern

Apps intake optional; webhook→Workflow compliance checks on notebooks/SQL; UC audit. [@databricks-apps] [@databricks-workflows]

## 5. Snowflake pattern

SPCS webhook listener; Task evaluates rules; tamper-evident approval tables. [@snowflake-tasks] [@snowflake-spcs-jobs-as-tasks]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Agent-native PR+OPA |
| **Analytics** | Approval ledger in lakehouse |
| **Renders** | Archify workflow/architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | ADR folders + tickets | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | ADR, Application |
| Writes | governs edge + approval receipt |

## 10. Citations

[@opa-conftest] [@orbus-infinity-product] [@databricks-apps] [@snowflake-tasks] [@archify-github] [@wcid-agy-research]


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

