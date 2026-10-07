# 5.4 — Ingestion patterns

## Pattern library

| Source | Databricks | Snowflake | Scenarios |
|---|---|---|---|
| Cloud billing CUR | Auto Loader | Snowpipe | S01 S16 |
| ServiceNow CMDB | Lakeflow Connect CDC | Managed connector | S01 S06 |
| API gateway logs | Auto Loader / streaming | Snowpipe Streaming | S09 |
| SBOM JSON from CI | Auto Loader (bucket) | Snowpipe | S15 |
| VPC flow logs | Auto Loader | Snowpipe | S14 |
| Git metadata | Git Folders / jobs | Git integration | S13 S19 S20 |
| Model events | MLflow/UC | Model Registry streams | S11 |

## Design rules

1. Land raw bronze/variant first; emit PAM in silver/gold.
2. Preserve source keys in `aliases`.
3. Attach `evidence` rows for observed edges.

## Citations

- [@databricks-autoloader]
- [@databricks-lakeflow]
- [@snowflake-snowpipe]


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

