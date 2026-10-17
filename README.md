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
- Deployable inside Databricks Apps with 9 interactive tabs:
  1. **Estate Catalog:** Filterable table of all conformed PAM entities and ArchiMate relations.
  2. **Living Architecture Maps:** Embedded interactive Archify HTML maps with pan, zoom, and tooltips.
  3. **EA Navigator Cockpit:** Conversational interface with live blast-radius calculations and MADR exporter.
  4. **EA Sentinel Audit:** PR evaluation view with visual architecture diffs and policy violation badges.
  5. **Executive TIME Matrix:** Portfolio quadrant analysis with FinOps annual run-cost aggregations.
  6. **Target-State Migration Roadmap:** Phased modernization waves, target PAM metamodel topology, and MADR v3.0 decision record exporter.
  7. **Business Capabilities & Investment:** Hierarchical capability tree (L1 Domains & L2 Capabilities) with FinOps cloud run-cost attribution and tech debt heatmaps.
  8. **CMDB Baseline Hygiene & Drift:** Continuous ServiceNow CMDB reconciliation (Orphan CIs, Shadow IT, Attribute Drift) with automated Table API REST remediation payloads.
  9. **M&A Day-One Landscape Discovery:** Rapid zero-footprint ingestion of acquired entity IT estate, capability overlap mapping, technology stack divergence, FinOps synergy rationalization ($84,000.00/yr savings), and merged Archify vector living maps.
  10. **Regulatory Compliance & Privacy Lineage (GDPR / DORA):** Continuous data privacy impact mapping, customer PII dataflow lineage traversal, cross-border third-country transfer detection (GDPR Art. 44: EU-West-1 ➔ US-East-1), encryption in transit/rest posture (GDPR Art. 32), DORA ICT resilience auditing (unreplicated legacy SPOF past EOL), and jurisdiction-isolated Archify living maps.

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
- **2026-10-17 - Scenario S03 Verified (Target State Architecture & Cloud Migration Roadmapping)** - Implemented plan_target_state_migration, get_target_state_graph, and Tab 6 Migration Roadmap in app.py. Validated 3 phased waves, PAM target-state mapping (orders-delta-table, customer-events-dlt, hosted_on, migrates_to), MADR v3.0 decision record, and $64,999.92/yr spend elimination. Dedicated test suite tests/scenarios/test_s03_target_state_migration.py passing 6/6 tests, master suite 33/33 tests passing, demo.sh exit code 0.
- **2026-10-17 - Scenario S04 Verified (Business Capability Modeling & Strategic Investment Alignment)** - Conformed hierarchical business capability nodes (Level-1 Strategic Domains & Level-2 Functional Capabilities) in PAM metamodel with realizes and aggregates relationships. Created conformed gold data mart ea.gold.capability_realization via Unity Catalog client attributing exactly $307,799.76/yr estate spend (Customer Experience: $147,999.84, Finance & Billing: $126,999.96, Security & Compliance: $32,799.96) and identifying technical debt concentrations. Integrated Tab 7 into Databricks App Cockpit. Dedicated test suite tests/scenarios/test_s04_capabilities.py passing 6/6 tests, master suite 39/39 tests passing (100%), and demo.sh passing with exit code 0.
- **2026-10-17 - Scenario S05 Verified (ARB Governance & Pre-Merge Policy Gate)** - Verified EA Sentinel pre-merge gate enforcing EA-POL-001 (unapproved datastores: Cassandra, MongoDB, unapproved engines), EA-POL-002 (mandatory KMS CMK encryption for customer PII storage and transmission), and EA-POL-003 (mandatory OwnerTeam and Tier criticality governance tags). Implemented conformed audit ledger `ea.gold.arb_audit_ledger` in Databricks Unity Catalog client, compiled Archify visual delta diffs (`diagram_delta.html` / `.svg`) with zero black box defects, and integrated ledger view and visual diffs into Tab 4 in `apps/ea_navigator/app.py`. Dedicated test suite `tests/scenarios/test_s05_arb_governance.py` passing 7/7 tests, master suite 46/46 tests passing, and `./demo.sh` passing end-to-end with exit code 0.
- **2026-10-17 - Scenario S06 Verified (Continuous ServiceNow CMDB Synchronization & Baseline Hygiene)** - Implemented ServiceNow CMDB modular ingestion connector (`src/ingestion/ingest_servicenow_cmdb.py`) populating conformed Bronze table `ea.bronze.cmdb_ci`. Implemented continuous 3-way baseline reconciliation in `dlt_metamodel_pipeline.py` and `src/navigator/engine.py` across CMDB CIs, Git PAM graph, and live runtime cloud resources, identifying Orphan CIs (`recommendations-ai-legacy`, `elastic-search-v6-logging`), Shadow IT (`customer-pii-stream`, `payments-service`), and Attribute/Lifecycle Drift (`checkout-service`, `cassandra-legacy-cluster`). Populated conformed gold mart `ea.gold.drift_reconciled` with complete discrepancy taxonomy and automated ServiceNow Table API REST remediation payloads. Integrated Tab 8 into Databricks App Cockpit in `apps/ea_navigator/app.py`. Dedicated test suite `tests/scenarios/test_s06_cmdb_sync.py` passing 7/7 tests, master suite 53/53 tests passing (100%), and `./demo.sh` passing end-to-end with exit code 0.
- **2026-10-17 - Scenario S07 Verified (M&A Day-One IT Landscape Discovery & Overlap Analysis)** - Implemented M&A Estate modular ingestion connector (`src/ingestion/ingest_ma_estate.py`) simulating zero-footprint ingestion of an acquired entity (`acquired-target-org`, tenant `acq-target-corp`, AWS account `998877665544`) into Bronze Delta tables (`ea.bronze.git_repos`, `ea.bronze.cloud_resources`). Conformed acquired assets into PAM graph (`urn:ea:acquired:*`) with domain realization edges. Implemented M&A landscape analysis in `src/navigator/engine.py` identifying duplicate capabilities (`Payment Processing`, `Identity & Access Management`), tech stack divergence (PHP 8.1, Node.js 16, MySQL 5.7 past EOL 2024-10-31, AWS Redshift vs enterprise Go 1.22, Java 21, Unity Catalog / Postgres), and debt disparity (acquired avg 72.5 vs core 35.4). Calculated Day-One combined run cost ($431,799.76/yr = $307,799.76 core + $124,000.00 acquired), identified rationalization synergies ($84,000.00/yr savings; target run cost: $347,799.76/yr), and populated `ea.gold.ma_synergies`. Compiled merged Archify living architecture map (`data/diagrams/ma_landscape_view.html` / `.svg`) and integrated Tab 9 into Databricks App Cockpit (`apps/ea_navigator/app.py`). Dedicated test suite `tests/scenarios/test_s07_ma_discovery.py` passing 7/7 tests, master test suite 60/60 tests passing (100%), and `./demo.sh` passing end-to-end with exit code 0.
- **2026-10-17 - Scenario S08 Verified (Regulatory Compliance & Data Privacy Impact Mapping GDPR / DORA)** - Enriched PAM metamodel nodes and relationship edges with data classification tiers (PII:High, PII:Medium, Internal, Public), sovereign jurisdictions (EU-West-1, US-East-1), and cryptographic transport/rest specifications (tls_1_3, plaintext, kms, none). Created and populated conformed gold compliance mart `ea.gold.compliance_lineage` via Databricks Unity Catalog client across 7 canonical flows. Implemented `analyze_compliance_lineage()` in `src/navigator/engine.py` performing BFS graph traversal to trace customer PII flows from ingress gateways (`web-storefront`, `payments-api`) to datastores and egress points, identifying GDPR Article 32 violations (unencrypted plaintext CQL transit & rest none on `cassandra-legacy-cluster`), GDPR Article 44-49 violations (unauthorized cross-border EU➔US egress to `customer-pii-stream`), and DORA ICT resilience vulnerabilities (unreplicated SPOF past EOL). Implemented `compile_compliance_lineage_diagram()` generating jurisdiction-isolated Archify living maps (`gdpr_dora_lineage.html` / `.svg`) with zero black box defects. Integrated Tab 10 into Databricks App UI Cockpit (`apps/ea_navigator/app.py`). Dedicated scenario test suite `tests/scenarios/test_s08_gdpr_dora.py` passing 7/7 tests, master automated test suite expanded to 67/67 passing tests (100%), and `./demo.sh` passing end-to-end with exit code 0.





