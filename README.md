# The Agentic EA (MVP)

**An autonomous, Databricks-native Enterprise Architecture Platform.**

Target Databricks Workspace: [https://dbc-2d6963b0-153b.cloud.databricks.com/](https://dbc-2d6963b0-153b.cloud.databricks.com/)

---

## 1. Overview & Paradigm Shift

The Agentic EA replaces passive diagram tools and static spreadsheets with a closed-loop, data-driven architecture platform anchored in Databricks:
- **Master Metamodel Backbone:** Unity Catalog Delta tables (`ea.metamodel.*`, `ea.bronze.*`, `ea.silver.*`, `ea.gold.*`).
- **Autonomous Governance:** **EA Sentinel** running as pre-merge PR gates with Archify visual architecture diffs.
- **Estate Intelligence & What-If Simulations:** **EA Navigator** computing real-time graph blast radius, financial risk, and target-state ADR drafting.
- **Unified UI Cockpit:** Native Databricks App (Streamlit) embedded in the Databricks workspace.
- **Continuous Ingestion:** Auto Loader and Delta Live Tables (DLT) streaming Git AST, Cloud CUR, and CMDB feeds.

---

## 2. Subsystem Architecture

```
the-agentic-ea/
├── databricks/             # Databricks Asset Bundle (DAB) declarations
│   └── databricks.yml      # Unity Catalog schemas, Apps, and DLT pipelines
├── src/
│   ├── navigator/          # EA Navigator reasoning engine & blast radius calculator
│   ├── sentinel/           # EA Sentinel pre-merge policy evaluation & PR gate
│   └── ingestion/          # Modular extractors (GitHub Org, Cloud CUR, ServiceNow)
├── apps/
│   └── ea_navigator/       # Databricks App (Streamlit) Cockpit with Archify embeds
├── pipelines/              # Delta Live Tables Medallion conformance transforms
├── schemas/
│   └── pam/                # Platform Architecture Metamodel (Draft-07 contracts)
├── setup.sh                # uv environment bootstrapping
├── run.sh                  # Execution entrypoint
└── README.md
```

---

## 3. Quick Start

```bash
# 1. Setup virtual environment via uv
./setup.sh

# 2. Run verification entrypoint
./run.sh
```

---

## 4. Build Log

- 2026-10-16 - MVP Repository Initialized - Scaffolded clean repository structure, `pyproject.toml` (uv standard), Databricks Asset Bundle (`databricks.yml` targeting `dbc-2d6963b0-153b.cloud.databricks.com`), PAM Draft-07 schemas, and core modular subsystem directories (`src/navigator`, `src/sentinel`, `src/ingestion`, `apps/ea_navigator`).
