---
title: "Build Specification: The Agentic EA Platform"
version: "1.0"
date_created: "2026-10-14"
last_updated: "2026-10-14"
owner: "Enterprise Architecture Core Team"
tags: ["architecture", "spec", "build-specification", "agentic-ea", "databricks", "backstage", "archify", "github"]
---

# 9.3 — Build Specification: The Agentic EA Platform

**Status:** approved spec v1 · **Date:** 2026-10-14 · **Scope:** Full machine-executable build specification translating Section 9.2 into unambiguous engineering contracts, data schemas, infrastructure configurations, and verification criteria.

---

## 1. Purpose & Scope

This specification defines the exact technical requirements, schemas, component interfaces, and verification gates required for an autonomous agent or engineering team to build the **Agentic Enterprise Architecture (EA) Platform**.

### 1.1 Objective
Replace legacy, passive EA repositories (e.g., Orbus Infinity) with an active, closed-loop platform consisting of:
1. **GitHub:** Declarative intent, metamodel contracts, and PR-based ARB governance.
2. **Databricks:** Unity Catalog analytical backbone, scenario data marts, and Lakebase (managed PostgreSQL) operational database.
3. **Backstage:** Unified developer and architect software catalog, TechDocs, and ownership portal.
4. **Archify:** Automatic, on-demand compilation of typed architecture graph data into interactive SVG/HTML diagrams.
5. **Agentic Workflows:** Autonomous GitHub Actions and Databricks jobs for continuous discovery (Cartographer), pre-merge PR governance (ARB Gate), and reality reconciliation (Drift Detector).

### 1.2 Non-Goals
- Building proprietary desktop diagramming plugins (e.g., Microsoft Visio stencils).
- Creating manual survey-intake forms for system inventory.
- Direct runtime modification of production cloud infrastructure (the platform proposes and gates; it does not deploy application workloads).

---

## 2. Definitions & Acronyms

- **ADR:** Architecture Decision Record (Markdown format, version-controlled in Git).
- **ARB:** Architecture Review Board.
- **DAB:** Databricks Asset Bundle (declarative YAML format for Databricks infrastructure).
- **Lakebase:** Databricks managed PostgreSQL engine registered in Unity Catalog.
- **MCP:** Model Context Protocol (standard interface for LLM tool invocation).
- **PAM:** Platform Architecture Metamodel (open graph metamodel: nodes, edges, aliases, evidence).
- **SDP:** Spark Declarative Pipelines (Delta Live Tables declarative transform engine).
- **TIME:** Tolerate, Invest, Migrate, Eliminate (application portfolio disposition matrix).
- **URN:** Uniform Resource Name (e.g., `urn:ea:app:checkout-service`).

---

## 3. Requirements & Invariants

### 3.1 Functional Requirements (REQ)
- **REQ-001**: The system shall store the single source of truth for architectural intent (PAM schemas, ADRs, capability models) in Git.
- **REQ-002**: The Databricks environment shall maintain four unified schemas in Unity Catalog: `ea.metamodel`, `ea.bronze`, `ea.silver`, and `ea.gold`.
- **REQ-003**: Backstage shall run on Node.js and persist all internal state and catalog entities into Databricks Lakebase PostgreSQL.
- **REQ-004**: Backstage shall ingest entities one-way from Databricks `ea.metamodel.nodes` via a scheduled custom Entity Provider.
- **REQ-005**: Archify shall compile typed JSON models into standalone SVG/HTML supporting five canonical types: `architecture`, `workflow`, `sequence`, `dataflow`, and `lifecycle`.
- **REQ-006**: Every Pull Request modifying application architecture or infrastructure files shall trigger an autonomous ARB review action that posts a markdown summary and Archify visual diff.
- **REQ-007**: A daily scheduled Drift Detector shall compare declared Git entities against live CMDB/cloud records in `ea.gold.cmdb_reconciled` and open a GitHub issue if drift $> 0$.

### 3.2 Constraints (CON)
- **CON-001 (Licence Filter)**: Only **GitHub**, **Databricks**, and permissive open-source software (OSS) may be used. No commercial third-party EA licenses permitted.
- **CON-002 (Database Storage)**: Backstage MUST NOT use local SQLite in any environment; it must connect directly to Lakebase PostgreSQL.
- **CON-003 (Deterministic Diagrams)**: Archify rendering must be deterministic: identical JSON inputs must yield identical SVG layout coordinates.

### 3.3 Security & Operational Boundaries (SEC)
- **SEC-001**: GitHub Actions runners must access Databricks using OAuth service principals / short-lived M2M tokens, never static personal access tokens.
- **SEC-002**: All PII and credential fields ingested from external APIs into Databricks Bronze must be tagged with Unity Catalog governance tags (`tag: PII = true`) and masked for non-EA queries.
- **SEC-003 (Agent Boundaries)**:
  - **Always do:** Run schema validation before committing; post visual diffs on architectural PRs; tag service owners on drift.
  - **Ask first (Human-in-the-Loop):** Modifying PAM core schema; granting ARB waivers; retiring application entities.
  - **Never do:** Commit cloud secrets; merge PRs bypassing required status checks; execute unreviewed DDL migrations in production.

---

## 4. Subsystem Specifications & Data Contracts

```
[Repository Root]
├── .github/workflows/
│   ├── arb-gate.yml
│   └── cartographer-sweep.yml
├── databricks/
│   ├── databricks.yml
│   └── resources/
│       ├── metamodel_tables.sql
│       └── ingestion_pipelines.yml
├── backstage/
│   ├── app-config.yaml
│   └── packages/backend/src/plugins/ea-catalog-provider.ts
├── archify/
│   ├── Dockerfile
│   └── bridge/
│       └── pam-to-archify.py
└── schemas/pam/
    ├── nodes.schema.json
    ├── edges.schema.json
    └── evidence.schema.json
```

---

### Subsystem 1: Core Metamodel Contracts (`schemas/pam/`)

The platform architecture metamodel is defined as strict JSON Schema draft-07 files.

#### Contract 1.1: `nodes.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PAMNode",
  "type": "object",
  "required": ["urn", "name", "kind", "owner_team", "criticality"],
  "properties": {
    "urn": {
      "type": "string",
      "pattern": "^urn:ea:[a-z0-9_-]+:[a-z0-9._-]+$"
    },
    "name": { "type": "string", "minLength": 1 },
    "kind": {
      "type": "string",
      "enum": [
        "BusinessCapability",
        "Application",
        "Microservice",
        "Database",
        "CloudResource",
        "APIInterface",
        "AIModel"
      ]
    },
    "owner_team": { "type": "string" },
    "lifecycle_status": {
      "type": "string",
      "enum": ["plan", "build", "run", "phase-out", "retired"],
      "default": "run"
    },
    "criticality": {
      "type": "string",
      "enum": ["Tier-0", "Tier-1", "Tier-2", "Tier-3"]
    },
    "metadata": { "type": "object" }
  },
  "additionalProperties": false
}
```

#### Contract 1.2: `edges.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PAMEdge",
  "type": "object",
  "required": ["source_urn", "target_urn", "relation"],
  "properties": {
    "source_urn": { "type": "string" },
    "target_urn": { "type": "string" },
    "relation": {
      "type": "string",
      "enum": [
        "serves",
        "accesses",
        "flows_to",
        "deploys_to",
        "realizes",
        "depends_on"
      ]
    },
    "protocol": { "type": "string" },
    "contains_pii": { "type": "boolean", "default": false }
  },
  "additionalProperties": false
}
```

---

### Subsystem 2: Databricks Backbone Declaration (`databricks/`)

The backbone is declared via **Databricks Asset Bundles (DAB)** to guarantee repeatable deployment.

#### Contract 2.1: `databricks.yml`
```yaml
bundle:
  name: ea-platform-backbone

targets:
  dev:
    mode: development
    workspace:
      host: https://adb-dev.azuredatabricks.net
  prod:
    mode: production
    workspace:
      host: https://adb-prod.azuredatabricks.net

resources:
  models:
    ea_metamodel:
      catalog: ea
      schema: metamodel
      tables:
        - name: nodes
          schema_file: ./resources/nodes_ddl.sql
        - name: edges
          schema_file: ./resources/edges_ddl.sql
        - name: evidence
          schema_file: ./resources/evidence_ddl.sql
        - name: aliases
          schema_file: ./resources/aliases_ddl.sql

  databases:
    ea_lakebase_postgres:
      engine: POSTGRESQL
      size: MEDIUM
      catalog: ea
      database_name: ea_operational

  pipelines:
    ea_reconciliation_pipeline:
      name: "EA Reconciliation & Gold Marts"
      edition: ADVANCED
      channel: CURRENT
      libraries:
        - notebook:
            path: ./pipelines/reconciliation_transforms.py
      target: ea.gold
      continuous: false
```

#### Contract 2.2: Unity Catalog DDL (`nodes_ddl.sql`)
```sql
CREATE TABLE IF NOT EXISTS ea.metamodel.nodes (
  urn STRING NOT NULL,
  name STRING NOT NULL,
  kind STRING NOT NULL,
  owner_team STRING NOT NULL,
  lifecycle_status STRING NOT NULL,
  criticality STRING NOT NULL,
  metadata VARIANT,
  last_updated TIMESTAMP NOT NULL
)
USING DELTA
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

ALTER TABLE ea.metamodel.nodes ADD CONSTRAINT pk_pam_nodes PRIMARY KEY (urn);
```

---

### Subsystem 3: Backstage Portal Configuration (`backstage/`)

Backstage is configured to use Databricks Lakebase Postgres and load the custom PAM entity provider.

#### Contract 3.1: `app-config.yaml` (Database & Catalog)
```yaml
app:
  title: Enterprise Architecture Portal
  baseUrl: http://localhost:3000

backend:
  baseUrl: http://localhost:7007
  listen:
    port: 7007
  database:
    client: pg
    connection:
      host: ${LAKEBASE_POSTGRES_HOST}
      port: 5432
      user: ${LAKEBASE_POSTGRES_USER}
      password: ${LAKEBASE_POSTGRES_PASSWORD}
      database: ea_operational
      ssl: { rejectUnauthorized: true }

catalog:
  rules:
    - allow: [Component, System, API, Resource, Domain]
  providers:
    eaMetamodel:
      schedule:
        frequency: { minutes: 15 }
        timeout: { minutes: 3 }
```

#### Contract 3.2: Entity Provider Interface (`ea-catalog-provider.ts`)
```typescript
import { EntityProvider, EntityProviderConnection } from '@backstage/plugin-catalog-node';
import { Client } from 'pg';

export class EAMetamodelProvider implements EntityProvider {
  private connection?: EntityProviderConnection;
  private readonly dbClient: Client;

  constructor(dbClient: Client) {
    this.dbClient = dbClient;
  }

  getProviderName(): string {
    return 'EAMetamodelProvider';
  }

  async connect(connection: EntityProviderConnection): Promise<void> {
    this.connection = connection;
  }

  async run(): Promise<void> {
    if (!this.connection) return;
    const res = await this.dbClient.query(
      'SELECT urn, name, kind, owner_team, lifecycle_status FROM ea_sync.active_nodes'
    );
    const entities = res.rows.map(row => ({
      apiVersion: 'backstage.io/v1alpha1',
      kind: row.kind === 'Microservice' ? 'Component' : 'Resource',
      metadata: {
        name: row.name.toLowerCase().replace(/[^a-z0-9_-]/g, '-'),
        annotations: { 'ea.urn': row.urn },
      },
      spec: {
        type: 'service',
        lifecycle: row.lifecycle_status,
        owner: row.owner_team,
      },
    }));

    await this.connection.applyMutation({
      type: 'full',
      entities: entities.map(e => ({ entity: e, locationKey: 'ea-provider:db' })),
    });
  }
}
```

---

### Subsystem 4: Archify Visual Engine & Conversion Bridge (`archify/`)

Archify transforms graph extracts from Databricks into interactive SVG diagrams.

#### Contract 4.1: Archify Input Schema (`archify-input.schema.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ArchifyInputSpec",
  "type": "object",
  "required": ["diagram_type", "title", "components", "connections"],
  "properties": {
    "diagram_type": {
      "type": "string",
      "enum": ["architecture", "workflow", "sequence", "dataflow", "lifecycle"]
    },
    "title": { "type": "string" },
    "components": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "label", "kind"],
        "properties": {
          "id": { "type": "string" },
          "label": { "type": "string" },
          "kind": { "type": "string" },
          "status": { "type": "string" },
          "metadata": { "type": "object" }
        }
      }
    },
    "connections": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["from", "to", "label"],
        "properties": {
          "from": { "type": "string" },
          "to": { "type": "string" },
          "label": { "type": "string" },
          "animated": { "type": "boolean", "default": false }
        }
      }
    }
  }
}
```

#### Contract 4.2: Execution CLI Command
```bash
# Compilation command
archify finalize \
  --input ./dist/spec-subgraph.json \
  --format svg \
  --theme dark \
  --output ./dist/architecture-view.svg
```

---

### Subsystem 5: Agentic Automation Workflows (`.github/workflows/`)

#### Contract 5.1: Autonomous ARB Review Gate (`arb-gate.yml`)
```yaml
name: "Autonomous ARB Review Gate"
on:
  pull_request:
    paths:
      - 'architecture/**'
      - 'infrastructure/**'
      - 'schemas/**'

jobs:
  arb-evaluation:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Validate Schema Changes
        run: |
          npx ajv-cli compile -s schemas/pam/nodes.schema.json
          npx ajv-cli compile -s schemas/pam/edges.schema.json

      - name: Run ARB Agent Evaluator
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/agent_arb_evaluator.py \
            --pr-number ${{ github.event.pull_request.number }} \
            --diff-output ./diff.patch \
            --out-comment ./arb_comment.md \
            --out-archify-spec ./diagram_delta.json

      - name: Compile Archify Visual Diff
        run: |
          archify finalize \
            --input ./diagram_delta.json \
            --format svg \
            --output ./diagram_delta.svg

      - name: Post PR Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const comment = fs.readFileSync('./arb_comment.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## 5. Acceptance Criteria & Verification Scenarios

| Test ID | Scenario | Given | When | Then |
|---|---|---|---|---|
| **AC-001** | Schema Validation | An invalid node JSON missing `owner_team` | AJV schema validator runs | Pipeline exits status 1 and highlights missing field |
| **AC-002** | Backbone Deploy | Valid Databricks credentials | `databricks bundle deploy -t dev` runs | `ea.metamodel` tables and Lakebase instance exist in Unity Catalog |
| **AC-003** | Backstage Sync | 10 application nodes loaded in Lakebase | Backstage catalog scheduler runs | 10 entities appear in Backstage `/catalog` with `urn` annotations |
| **AC-004** | Archify Render | A valid PAM subgraph JSON | `archify finalize` runs | Valid SVG file created with 0 overlapping nodes |
| **AC-005** | ARB PR Gate | A PR introducing an unapproved database | GitHub PR action triggers | Action leaves comment identifying violation and posts visual diff |
| **AC-006** | Drift Alert | Cloud CUR lists AWS Aurora missing from Git | Daily Drift Detector runs | GitHub Issue created with title `[Drift] Unregistered DB in us-east-1` |

---

## 6. Implementation Task Breakdown (Execution Order)

The implementation must proceed sequentially according to this vertical slice:

```
[Task 1: Schemas] ──> [Task 2: Databricks DAB] ──> [Task 3: Backstage] ──> [Task 4: Archify] ──> [Task 5: CI Agents]
```

- [ ] **Task 1: Metamodel Schema Foundation**
  - Create `schemas/pam/nodes.schema.json`, `edges.schema.json`, `evidence.schema.json`.
  - Add AJV schema validation script to GitHub Actions.
  - *Verify:* Run `npm run test:schemas` against valid and invalid sample payloads.
- [ ] **Task 2: Databricks Asset Bundle & Lakebase**
  - Author `databricks/databricks.yml` and table DDL scripts.
  - Configure Lakebase PostgreSQL operational instance.
  - *Verify:* `databricks bundle validate` passes and creates staging tables.
- [ ] **Task 3: Backstage Scaffolding & Provider**
  - Scaffold Backstage Node.js app using `@backstage/create-app`.
  - Wire `app-config.yaml` to Lakebase Postgres.
  - Implement `EAMetamodelProvider` to sync Delta nodes into Backstage catalog.
  - *Verify:* `yarn dev` boots and loads catalog entities from Lakebase.
- [ ] **Task 4: Archify CLI Integration Bridge**
  - Write `bridge/pam-to-archify.py` to extract subgraphs to typed Archify JSON.
  - Package Docker container with Archify CLI.
  - *Verify:* Export a 5-node cluster and generate a valid SVG.
- [ ] **Task 5: ARB Gate & Drift Workflows**
  - Implement `.github/workflows/arb-gate.yml` and evaluator script.
  - Implement `.github/workflows/drift-detector.yml`.
  - *Verify:* Submit a synthetic test PR and verify comment and Archify diff attachment.
