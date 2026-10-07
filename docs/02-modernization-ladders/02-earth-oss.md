# 2.2 — Earth ladder — OSS replacements

Earth is the **non-agent** open replacement stack for Orbus Infinity capabilities. It is necessary but not sufficient for ANEA.

## Representative Earth stack

| Orbus capability | Earth OSS options |
|---|---|
| C1 Repository | Git monorepo/polyrepo of YAML + Backstage catalog [@backstage-software-catalog] |
| C2 Metamodel | ArchiMate tooling + JSON Schema; Archi / coArchi patterns |
| C3 Capabilities | Markdown/YAML capability trees in Git |
| C4 APM | Spreadsheet/dbt models over CMDB exports (pre-lakehouse) |
| C5 Technology | Service catalogs; endoflife.date feeds [@endoflife-date] |
| C6 Data lineage | OpenLineage + data catalogs [@openlineage] |
| C7 Process | BPMN files in Git |
| C8 Interfaces | OpenAPI/AsyncAPI repos [@openapi-spec] |
| C9 Diagrams | Mermaid, Structurizr, LikeC4, draw.io [@structurizr] [@likec4] [@c4-model] |
| C10 Integrations | n8n, Airbyte, custom ETL (connectors replacing Orbus Flow patterns) |
| C11 ARB | ADR folders + Confluence/GitHub Issues workflows |
| C12 Reporting | Metabase/Superset over warehouse extracts |
| C13 Collaboration | Backstage portal + GitHub |
| C14 Security views | Manual C4 + policy docs |
| C15 Roadmaps | Markdown roadmaps / Jira Align exports |

## Earth strengths and gaps

- **Strength:** Portable, auditable, no EA-suite license.
- **Gap:** Still human-heavy; weak continuous reconciliation; diagrams rarely verified; no agent enforcement loop.

## Citations

- [@backstage-software-catalog]
- [@structurizr]
- [@likec4]
- [@openapi-spec]
- [@openlineage]
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

