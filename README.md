# The Agentic EA (MVP)

**An autonomous, Databricks-native Enterprise Architecture Platform.**

Target Databricks Workspace: [https://dbc-2d6963b0-153b.cloud.databricks.com/](https://dbc-2d6963b0-153b.cloud.databricks.com/)  
Catalog: `ea` (Databricks Unity Catalog)

---

## 1. Overview & Paradigm Shift

The Agentic EA replaces passive diagram tools and static spreadsheets with a closed-loop, data-driven architecture platform anchored natively in Databricks:
- **Master Metamodel Backbone:** Pure Unity Catalog Delta tables (`ea.metamodel.*`, `ea.bronze.*`, `ea.silver.*`, `ea.gold.*`).
- **Autonomous Governance:** **EA Sentinel** running as pre-merge PR gates with Archify visual architecture diffs.
- **Estate Intelligence & What-If Simulations:** **EA Navigator** computing real-time graph blast radius, financial risk, and target-state ADR drafting.
- **Unified UI Cockpit:** Native Databricks App (Streamlit) deployable directly in Databricks Apps.
- **Continuous Ingestion:** Auto Loader and Delta Live Tables (DLT) streaming Git AST, Cloud CUR, and CMDB feeds into Delta Lake.

---

## 2. Subsystem Architecture

```
the-agentic-ea/
├── databricks/             # Databricks Asset Bundle (DAB) declarations
│   ├── databricks.yml      # Target host: dbc-2d6963b0-153b, schemas, apps, DLT pipelines
│   └── resources/          # Conformed SQL DDLs for Unity Catalog
├── src/
│   ├── data_backbone/      # Unity Catalog conformed tables client & seed loader
│   ├── archify/            # Archify v3 CLI bridge (dual HTML & vector SVG generator)
│   ├── navigator/          # EA Navigator reasoning engine & blast radius calculator
│   ├── sentinel/           # EA Sentinel pre-merge policy evaluation & PR gate
│   └── ingestion/          # Modular extractors (GitHub Org, Cloud CUR, DLT pipeline)
├── apps/
│   └── ea_navigator/       # Databricks App (Streamlit) Cockpit with 5 interactive tabs
├── pipelines/              # Delta Live Tables Medallion conformance transforms
├── schemas/
│   └── pam/                # Platform Architecture Metamodel (Draft-07 contracts)
├── tests/                  # Automated pytest suite (schemas, navigator, sentinel, ingestion)
├── demo.sh                 # Single executable end-to-end demonstration harness
├── setup.sh                # uv environment bootstrapping
├── run.sh                  # Execution entrypoint
└── README.md
```

---

## 3. Core Subsystems

### A. Data Backbone (Databricks Unity Catalog)
- **Conformed Tables:**
  - `ea.metamodel.nodes`: PAM nodes (URN, name, kind, owner_team, lifecycle_status, criticality, metadata).
  - `ea.metamodel.edges`: ArchiMate relations (source_urn, target_urn, relation, protocol, contains_pii).
  - `ea.metamodel.evidence`: AST signatures, commit hashes, provenance evidence.
- **Bronze Ingestion Feeds:**
  - `ea.bronze.git_repos`: Raw repository manifests and AST dependency extracts.
  - `ea.bronze.cloud_resources`: Cloud provider CUR billing telemetry and tags.
- **Gold Scenario Marts:**
  - `ea.gold.time_matrix`: Gartner TIME classification (Invest, Tolerate, Migrate, Eliminate) and annual run costs.
  - `ea.gold.drift_reconciled`: Tracked discrepancies between declared architecture and live telemetry.

### B. EA Navigator (Estate Intelligence Engine)
- **Graph Traversal:** Breadth-first search (BFS) discovering direct and transitive upstream callers and downstream sinks.
- **Financial Risk:** Quantifies annual dollar exposure at risk from `ea.gold.time_matrix`.
- **Customer PII Lineage:** Identifies GDPR Art. 32 / DORA regulatory exposure paths.
- **Living Maps:** Compiles dynamic Archify interactive maps with highlighted blast radius (`--highlight <urns>`).
- **MADR Generator:** Formats standards-compliant Markdown Architecture Decision Records (MADR v3.0).
- **Co-Driving Actions:** Contextual one-click scenario chips (`[Simulate Outage]`, `[Draft Migration ADR]`, `[Audit PII Lineage]`).

### C. EA Sentinel (Autonomous Governance Gate)
- **Pre-Merge PR Gate:** Evaluates unified diffs against core architectural policies:
  - `EA-POL-001`: Unapproved / deprecated datastore enforcement (e.g. Cassandra 3.11 in 'Eliminate' status).
  - `EA-POL-002`: Mandatory customer PII storage encryption at rest (KMS CMK).
  - `EA-POL-003`: Mandatory architectural tagging (`OwnerTeam` and `Tier`).
- **Tri-Modal Evaluation:**
  - Option A: Databricks Mosaic AI Model Serving (`databricks-meta-llama-3-1-70b-instruct`).
  - Option B: External LLM API (`gpt-4o` / Gemini).
  - Option C: Subscription CLI / Local deterministic agent ($0 token cost).
- **Visual Delta Diff:** Generates dual Archify `diagram_delta.html` and `.svg` highlighting non-compliant resources in rose red.

### D. Databricks App UI Cockpit (`apps/ea_navigator/app.py`)
- Deployable inside Databricks Apps with 5 interactive tabs:
  1. **Estate Catalog:** Filterable table of all conformed PAM entities and ArchiMate relations.
  2. **Living Architecture Maps:** Embedded interactive Archify HTML maps with pan, zoom, and tooltips.
  3. **EA Navigator Cockpit:** Conversational interface with live blast-radius calculations and MADR exporter.
  4. **EA Sentinel Audit:** PR evaluation view with visual architecture diffs and policy violation badges.
  5. **Executive TIME Matrix:** Portfolio quadrant analysis with FinOps annual run-cost aggregations.

---

## 4. Quick Start & Verification

```bash
# 1. Bootstrap environment via uv
./setup.sh

# 2. Run master demonstration (Verifies all 5 capabilities, tests, and outputs exit code 0)
./demo.sh

# 3. Launch interactive Databricks App UI Cockpit
streamlit run apps/ea_navigator/app.py
```

---

## 5. Build Log

- **2026-10-16 - MVP Repository Initialized** - Scaffolded clean repository structure, `pyproject.toml` (uv standard), Databricks Asset Bundle (`databricks.yml` targeting `dbc-2d6963b0-153b.cloud.databricks.com`), PAM Draft-07 schemas, and core modular subsystem directories (`src/navigator`, `src/sentinel`, `src/ingestion`, `apps/ea_navigator`).
- **2026-10-16 - MVP Completed & Verified** - Built and verified Databricks-native MVP: conformed Unity Catalog Delta tables, modular Bronze ingestors (Git AST, Cloud CUR), DLT conformance pipeline, EA Sentinel PR gate with Archify visual delta diffs, EA Navigator Estate Intelligence Engine with BFS blast-radius and MADR drafting, Streamlit UI cockpit, test suite passing 16/16 tests, and single executable `demo.sh` passing with exit code 0.
- **2026-10-16 - Scenario S01 Verified (APM / TIME Model)** - Implemented and validated dedicated scenario test `tests/scenarios/test_s01_apm_time.py`. Verified 100% coverage across all 4 Gartner TIME quadrants (Invest: $209,999.88, Tolerate: $24,999.96, Migrate: $7,800.00, Eliminate: $64,999.92), confirmed portfolio spend aggregation to exactly $307,799.76 in `ea.gold.time_matrix`, validated Tab 5 integration in Databricks App Cockpit, bringing automated test suite to 21/21 passing tests.
- **2026-10-16 - Scenario S02 Verified (Technology Obsolescence & Lifecycle Risk EOL/EOS)** - Implemented and validated dedicated scenario test `tests/scenarios/test_s02_eol_eos.py`. Verified detection and risk categorization of assets past/near EOL (cassandra-legacy-cluster: EXPIRED/CRITICAL, customer-pii-stream: NEAR_EOL/HIGH, auth-service: NEAR_EOL/APPROACHING_EOL), EA Navigator BFS blast-radius calculation for sunset datastore (4 upstream callers: payments-service, payments-api, checkout-service, web-storefront; $234,999.84/yr financial risk, customer PII exposure), EA Sentinel pre-merge gate and Navigator binding guard enforcing EA-POL-001 against bindings to sunset assets, and Databricks App UI Tab 5 Lifecycle Risk dashboard panel. Automated test suite expanded to 27/27 passing tests (100% success), with `./demo.sh` passing end-to-end with exit code 0.


