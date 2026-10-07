# S08 — Regulatory Compliance & Data Privacy Impact Mapping (GDPR / DORA)

## 1. Orbus Infinity baseline

Data objects/flows with classifications; system processing views for DPIA/audit.

## 2. Failure modes of the legacy pattern

Code scans without production lineage; missing access evidence.

## 3. Agent-native modern alternative

Semgrep PII + OTel cross-border hints; Archify **dataflow** with jurisdiction tags.

**Primary Archify type(s):** `dataflow`

## 4. Databricks pattern

UC column lineage; nightly Workflow compliance receipts. [@databricks-unity-catalog]

## 5. Snowflake pattern

Horizon classification, lineage, masking, access history; Task compiles maps. [@snowflake-horizon]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Masking/projection policies |
| **Analytics** | Snowflake Horizon strong default |
| **Renders** | Archify dataflow |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | DPIA docs + Visio | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Service, DataEntity |
| Writes | accesses + pii_classification |

## 10. Citations

[@snowflake-horizon] [@databricks-unity-catalog] [@orbus-infinity-product] [@archify-github] [@wcid-agy-research]


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

