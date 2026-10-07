# 3.4 — Executive visual / app tier

Executives do not browse Git. They need:

1. Interactive Archify HTML/SVG hosted in Apps/SiS
2. Natural-language Q&A over PAM (Genie / Cortex Analyst)
3. Scheduled narrative packs (TIME, risk, cost)

## Hosting patterns

| Host | Pattern |
|---|---|
| Databricks Apps | Serve Archify artifact + metrics from UC [@databricks-apps] |
| Streamlit in Snowflake | `st.components` HTML + Dynamic Table metrics [@snowflake-streamlit] |
| Backstage | Eng portal for system pages |
| Orbus Infinity (coexist) | Publish selected views until retirement |

## Rule

The executive tier **never invents entities**. It only projects PAM.

## Citations

- [@databricks-apps]
- [@snowflake-streamlit]
- [@archify-github]


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

