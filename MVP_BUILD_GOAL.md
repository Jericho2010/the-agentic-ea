# BUILD GOAL: The Agentic EA Platform — Databricks-Native MVP

## Mission
Build the clean, production-grade Minimum Viable Product (MVP) of **The Agentic EA Platform** in `/home/shaun/Projects/the-agentic-ea`, targeting the Databricks workspace instance:
`https://dbc-2d6963b0-153b.cloud.databricks.com/`

---

## 1. Context & Architectural Overhaul
The previous exploratory ideation codebase has been moved to `/home/shaun/Projects/the-agentic-ea-ideation`.
You are now building the clean, modular MVP in `/home/shaun/Projects/the-agentic-ea`.

### Strict Terminology & Nomenclature Directives:
1. **Retire "Copilot":** Replace all references to "Copilot" with:
   - **EA Navigator**: The user-facing conversational engine, What-If simulator, and strategic advisor.
   - **Estate Intelligence Engine (EIE)**: The core analytical backend and graph traversal engine.
2. **Retire "ARB Gate":** Replace with **EA Sentinel** (autonomous pre-merge policy and compliance gate).
3. **Retire "Lakebase":** There is no native product called "Lakebase" on Databricks. Eliminate synthetic local PostgreSQL containers. The master source of truth is **pure Databricks Unity Catalog Delta tables**.

---

## 2. Target Architecture & Components to Build

### A. Data Backbone (Databricks Unity Catalog)
- Target Host: `https://dbc-2d6963b0-153b.cloud.databricks.com/`
- Databricks Asset Bundle (`databricks/databricks.yml`):
  - Schemas: `ea.metamodel`, `ea.bronze`, `ea.silver`, `ea.gold`.
  - Conformed Tables:
    - `ea.metamodel.nodes` (PAM nodes: URN, name, kind, owner_team, lifecycle, criticality, metadata)
    - `ea.metamodel.edges` (ArchiMate relations: source_urn, target_urn, relation, protocol, contains_pii)
    - `ea.metamodel.evidence` (Source provenance, commit hashes, AST fingerprints, timestamps)
  - Scenario Marts:
    - `ea.gold.time_matrix` (System, disposition: Invest/Tolerate/Migrate/Eliminate, annual run cost, tech debt score, EOL date)
    - `ea.gold.drift_reconciled` (Declared vs runtime cloud discrepancies)
- Access layer: Use `databricks-sdk` and `databricks-sql-connector` with local fallback mode for testing when offline.

### B. Ingestion Engine (`src/ingestion/`)
Implement real modular ingestion connectors streaming into Delta Lake Bronze:
1. `ingest_github_org.py`: Discovers active repositories, extracts ASTs and package manifests (`pom.xml`, `package.json`, `pyproject.toml`, `Dockerfile`), and parses service relations.
2. `ingest_cloud_cur.py`: Ingests cloud billing/CUR records and resource configurations into `ea.bronze.cloud_resources`.
3. `dlt_metamodel_pipeline.py`: Delta Live Tables (DLT) / Spark transforms conforming Bronze feeds into Silver PAM graph (`ea.metamodel.nodes` & `ea.metamodel.edges`).

### C. EA Navigator Engine (`src/navigator/`)
1. `engine.py`: Grounded Estate Intelligence Engine:
   - Breadth-first search (BFS) upstream/downstream dependency graph traversal.
   - Financial exposure quantification at risk (pulling annual run costs from `ea.gold.time_matrix`).
   - Customer PII data flow lineage detection (GDPR Art. 32 / DORA).
   - Dynamic Archify visual map generation with highlighted affected nodes/edges (`--highlight <urns>`).
   - Standards-compliant Markdown Architecture Decision Record (MADR) drafting.
   - Interactive Co-Driving action suggestions (One-click waivers, migration proposals).

### D. EA Sentinel Governance Gate (`src/sentinel/`)
1. `gate.py`: Pre-merge architectural compliance checker.
   - Analyzes PR diffs against PAM rules:
     - `EA-POL-001`: Unapproved / deprecated datastore detection (e.g. Cassandra 3.11 in 'Eliminate').
     - `EA-POL-002`: Unencrypted PII storage check (`ContainsPII = true` with `Encrypted = false`).
     - `EA-POL-003`: Missing ownership team or Tier criticality tags.
   - Tri-Modal LLM evaluation:
     - Option A: Databricks Mosaic AI Model Serving (`databricks-meta-llama-3-1-70b-instruct`)
     - Option B: External LLM API (`gpt-4o` / Gemini)
     - Option C: Subscription CLI (`agy` / `cursor`) for $0 token cost in non-prod/demo
   - Compiles before/after visual delta diagrams via Archify.

### E. Unified UI Cockpit in Databricks Apps (`apps/ea_navigator/`)
1. Build a modern Python Streamlit application (`app.py`) deployable natively inside Databricks Apps:
   - **View 1: Estate Catalog**: Browse all PAM entities filtered by kind, tier, owner, and lifecycle.
   - **View 2: Living Architecture Maps**: Interactive embedded Archify HTML maps with pan/zoom/hover.
   - **View 3: EA Navigator Cockpit**: Interactive conversational drawer with live blast-radius calculations, inline diagram previews, and one-click action buttons.
   - **View 4: EA Sentinel Audit**: PR evaluation view with visual architecture diffs and policy violation badges.
   - **View 5: Executive TIME Matrix**: Interactive portfolio quadrant (Invest, Tolerate, Migrate, Eliminate) with FinOps run-cost aggregations.

### F. Verification & Demonstration Harness
1. `demo.sh`: Single executable script that boots the local verification environment, runs schema tests, runs ingestion, tests EA Sentinel against a sample PR diff, executes EA Navigator blast radius, and serves the Streamlit Cockpit.
2. Ensure `run.sh` launches the verified MVP smoothly.

---

## 3. Definition of Done
- All code resides in `/home/shaun/Projects/the-agentic-ea`.
- Zero references to "Copilot" or fake "Lakebase".
- All PAM contracts in `schemas/pam/` validate.
- Databricks Asset Bundle passes validation for workspace `https://dbc-2d6963b0-153b.cloud.databricks.com/`.
- `./demo.sh` completes end-to-end with exit code 0.
