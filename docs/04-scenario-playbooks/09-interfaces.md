# S09 — Interface & Integration Landscape Rationalization

## 1. Orbus Infinity baseline

Interface objects linking providers/consumers; integration landscape diagrams.

## 2. Failure modes of the legacy pattern

Declared APIs only; zombie runtime traffic invisible.

## 3. Agent-native modern alternative

OpenAPI/gRPC scan + eBPF/Cilium runtime; Archify **sequence** + **architecture**. [@openapi-spec]

**Primary Archify type(s):** `sequence + architecture`

## 4. Databricks pattern

Git Folders specs + Auto Loader gateway logs; weekly Workflow zombie detect.

## 5. Snowflake pattern

Snowpipe Streaming logs; Dynamic Tables declared-vs-actual; SPCS Archify compile via EXECUTE JOB SERVICE. [@snowflake-execute-job-service]

## 6. Control-plane verdict

| Role | Owner |
|---|---|
| **Enforces** | Agent-native contract+runtime |
| **Analytics** | Gateway log warehouse |
| **Renders** | Archify sequence/architecture |

## 7. Comparison table

| Dimension | Orbus Infinity | Earth OSS | Agent-native | Databricks | Snowflake |
|---|---|---|---|---|---|
| Core approach | Repository objects & views | OpenAPI repos only | Inner-loop agents + verified diagrams | Lakehouse pipelines + Apps | Governed SQL/apps + Tasks/SPCS |
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
| Reads | Service, API |
| Writes | consumes/exposes edges |

## 10. Citations

[@openapi-spec] [@databricks-autoloader] [@snowflake-execute-job-service] [@archify-github] [@wcid-agy-research]


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

