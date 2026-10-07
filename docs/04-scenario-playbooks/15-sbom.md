# S15 — Software Supply Chain & OSS Licensing (SBOM)

## 1. Orbus Infinity baseline

Component/license associations for questionnaires and standards.

## 2. Failure modes of the legacy pattern

Post-hoc inventories; non-compliant deps already merged.

## 3. Agent-native modern alternative

Syft/Grype CycloneDX; Cosign; OPA merge block; Archify **dataflow** dep trees. [@cyclonedx] [@opa-conftest]

**Primary Archify type(s):** `dataflow`

## 4. Databricks pattern

Auto Loader SBOM JSON; event Workflow license queries.

## 5. Snowflake pattern

Snowpipe SBOM variants; Cortex package Q&A; SPCS registry scans.

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | CI block (agent-native) |
| **Analytics** | Exec SBOM warehouse |
| **Renders** | Archify dataflow |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | Manual SCA tools | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Writes | SBOMPackage bundled_in edges |

## 10. Citations

[@cyclonedx] [@opa-conftest] [@databricks-autoloader] [@snowflake-snowpipe] [@archify-github] [@wcid-agy-research]


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

