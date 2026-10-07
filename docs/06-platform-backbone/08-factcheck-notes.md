# 5.8 — Fact-check notes & API accuracy

This chapter records corrections against earlier research drafts (WCID-agy) so the manual stays honest.

## Confirmed / preferred

| Topic | Correct reference |
|---|---|
| Databricks Assistant rename | **Genie Code** [@databricks-genie-code] |
| Snowflake container job in Task | `EXECUTE JOB SERVICE` inside Task body [@snowflake-execute-job-service] [@snowflake-spcs-jobs-as-tasks] |
| Archify architecture schema | `components`, `connections`, boundaries `kind: region\|security-group` + `wraps` [@archify-github] |
| Archify types | architecture, workflow, sequence, dataflow, lifecycle only |

## Rejected / do not copy into designs

| Invented or unsafe claim | Guidance |
|---|---|
| `SYSTEM$RUN_CONTAINER` | **Not a documented API** — use `EXECUTE JOB SERVICE` |
| `SYSTEM$NOTIFY_STREAMLIT_APP` as assumed primitive | Verify; do not rely without docs |
| Archify candidate with `nodes`/`relationships`/`boundary.type=domain` | Invalid vs current Archify schemas |
| Exclusive “Snowflake wins” for dual control-plane scenarios | Prefer enforce/analytics/render split |

## Confidence policy

Product UI names drift. Prefer linking primary docs in `references/bib.yaml` and re-verify before implementation programs.

## Citations

- [@snowflake-execute-job-service]
- [@snowflake-spcs-jobs-as-tasks]
- [@databricks-genie-code]
- [@archify-github]
- [@wcid-agy-research]


## Chapter validation checklist

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

