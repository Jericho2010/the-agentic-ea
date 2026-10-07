# 5.5 — Orchestration patterns

## Databricks

Multi-task Jobs/Workflows; DLT for continuous pipelines; event triggers on UC model promotion or file arrival. [@databricks-workflows] [@databricks-dlt]

Illustrative APM monthly job stages: ingest billing → ingest CMDB → classify TIME → compile Archify → publish App.

## Snowflake

Task graphs with predecessor dependencies; Dynamic Tables for declarative refresh; container work via:

```sql
CREATE TASK compile_archify
AS
  EXECUTE JOB SERVICE
    IN COMPUTE POOL ea_compute_pool
    FROM SPECIFICATION $$
    spec:
      containers:
      - name: main
        image: /ea_db/ea_schema/ea_repo/archify-runner:latest
    $$;
```

[@snowflake-tasks] [@snowflake-execute-job-service] [@snowflake-spcs-jobs-as-tasks]

**Do not use** invented helpers like `SYSTEM$RUN_CONTAINER` (see fact-check).

## Citations

- [@databricks-workflows]
- [@databricks-dlt]
- [@snowflake-tasks]
- [@snowflake-execute-job-service]
- [@snowflake-spcs-jobs-as-tasks]


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

