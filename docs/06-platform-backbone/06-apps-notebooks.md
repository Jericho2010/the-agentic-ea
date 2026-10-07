# 5.6 — Apps & notebooks as EA delivery surfaces

## Notebooks

Good for: exploration, Genie Code / Cortex-assisted analytics, one-off reconciliations.  
Bad as: sole home for PAM schema or ARB system of record.

## Databricks Apps

Host Archify HTML + metrics from Unity Catalog tables; suitable executive TIME/risk consoles. [@databricks-apps]

## Streamlit in Snowflake

Steward curation (S17), FinOps consoles (S16), embed Archify HTML components. [@snowflake-streamlit]

## Feasibility matrix (summary)

| Workload | Notebook OK? | App/SiS OK? | CI required? |
|---|---|---|---|
| Schema validation | Prototype only | No | Yes |
| TIME scoring | Yes | Yes | Optional |
| ARB enforcement | No | Intake only | Yes |
| Archify compile | Possible in job | Display | Preferred in CI or Job/Task |

## Citations

- [@databricks-apps]
- [@databricks-genie-code]
- [@snowflake-streamlit]
- [@snowflake-cortex]


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

