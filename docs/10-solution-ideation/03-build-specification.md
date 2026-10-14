---
title: "Build Specification: The Agentic EA Platform"
version: "1.1"
date_created: "2026-10-14"
last_updated: "2026-10-14"
owner: "Enterprise Architecture Core Team"
tags: ["architecture", "spec", "build-specification", "agentic-ea", "databricks", "backstage", "archify", "github"]
---

# 9.3 — Build Specification: The Agentic EA Platform

**Status:** approved spec v1.1 · **Date:** 2026-10-14 · **Scope:** Full machine-executable build specification translating Section 9.2 into unambiguous engineering contracts, data schemas, infrastructure configurations, and verification criteria.

---

## 1. Purpose & Scope

This specification defines the exact technical requirements, schemas, component interfaces, and verification gates required for an autonomous agent or engineering team to build the **Agentic Enterprise Architecture (EA) Platform**.

### 1.1 Objective
Replace legacy, passive EA repositories (e.g., Orbus Infinity) with an active, closed-loop platform consisting of:
1. **GitHub:** Declarative intent, metamodel contracts, and PR-based ARB governance.
2. **Databricks:** Unity Catalog analytical backbone, scenario data marts, Lakebase (managed PostgreSQL) operational database, and **Databricks Apps hosting runtime**.
3. **Backstage (hosted in Databricks Apps):** Unified developer and architect software catalog, TechDocs, and ownership portal deployed natively as a Databricks App.
4. **Archify:** Automatic, on-demand compilation of typed architecture graph data into interactive SVG/HTML diagrams.
5. **Agentic Workflows:** Autonomous GitHub Actions and Databricks jobs for continuous discovery (Cartographer), pre-merge PR governance (ARB Gate with dual LLM provider options), and reality reconciliation (Drift Detector).

### 1.2 Non-Goals
- Building proprietary desktop diagramming plugins (e.g., Microsoft Visio stencils).
- Creating manual survey-intake forms for system inventory.
- Direct runtime modification of production cloud infrastructure (the platform proposes and gates; it does not deploy application workloads).

---

## 2. Definitions & Acronyms

- **ADR:** Architecture Decision Record (Markdown format, version-controlled in Git).
- **ARB:** Architecture Review Board.
- **DAB:** Databricks Asset Bundle (declarative YAML format for Databricks infrastructure).
- **Databricks Apps:** Serverless application hosting environment within Databricks workspaces.
- **Lakebase:** Databricks managed PostgreSQL engine registered in Unity Catalog.
- **MCP:** Model Context Protocol (standard interface for LLM tool invocation).
- **Mosaic AI Model Serving:** Databricks managed inference serving for open-weights or external foundation models.
- **PAM:** Platform Architecture Metamodel (open graph metamodel: nodes, edges, aliases, evidence).
- **SDP:** Spark Declarative Pipelines (Delta Live Tables declarative transform engine).
- **TIME:** Tolerate, Invest, Migrate, Eliminate (application portfolio disposition matrix).
- **URN:** Uniform Resource Name (e.g., `urn:ea:app:checkout-service`).

---

## 3. Requirements & Invariants

### 3.1 Functional Requirements (REQ)
- **REQ-001**: The system shall store the single source of truth for architectural intent (PAM schemas, ADRs, capability models) in Git.
- **REQ-002**: The Databricks environment shall maintain four unified schemas in Unity Catalog: `ea.metamodel`, `ea.bronze`, `ea.silver`, and `ea.gold`.
- **REQ-003 (Backstage Hosting in Databricks Apps)**: Backstage shall be deployed and executed as a **Databricks App** using the serverless Node.js runtime, connecting directly to Databricks Lakebase PostgreSQL within the same workspace boundary.
- **REQ-004**: Backstage shall ingest entities one-way from Databricks `ea.metamodel.nodes` via a scheduled custom Entity Provider querying Lakebase.
- **REQ-005**: Archify shall compile typed JSON models into standalone SVG/HTML supporting five canonical types: `architecture`, `workflow`, `sequence`, `dataflow`, and `lifecycle`.
- **REQ-006**: Every Pull Request modifying application architecture or infrastructure files shall trigger an autonomous ARB review action that posts a markdown summary and Archify visual diff.
- **REQ-007**: A daily scheduled Drift Detector shall compare declared Git entities against live CMDB/cloud records in `ea.gold.cmdb_reconciled` and open a GitHub issue if drift $> 0$.
- **REQ-008 (Dual LLM Provider Support)**: The ARB Reviewer Agent evaluator shall support **both** of the following LLM provider options via pluggable configuration:
  - **Option A (In-Platform Databricks Mosaic AI Model Serving):** Invokes an enterprise-hosted open-weights model (e.g., `databricks-meta-llama-3-1-70b-instruct`, `dbrx-instruct`, or `deepseek-v3`) via Databricks Model Serving endpoints with zero data egress outside the Databricks security perimeter.
  - **Option B (External LLM API):** Invokes external managed frontier endpoints (e.g., OpenAI `gpt-4o`, Google Gemini 1.5 Pro, or Anthropic Claude 3.5 Sonnet) via standard REST APIs.
  - The evaluator script and GitHub Action shall dynamically toggle between Option A and Option B using the `LLM_PROVIDER` environment variable without requiring code modifications.

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
│       ├── lakebase_db.yml
│       └── backstage_app.yml
├── backstage/
│   ├── app-config.yaml
│   ├── app.yaml
│   ├── package.json
│   └── packages/backend/src/plugins/ea-catalog-provider.ts
├── archify/
│   ├── Dockerfile
│   └── bridge/
│       └── pam-to-archify.py
├── scripts/
│   └── agent_arb_evaluator.py
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

  apps:
    ea_backstage_portal:
      name: "ea-backstage-portal"
      description: "Developer and EA software catalog portal hosted inside Databricks Apps"
      source_code_path: ../backstage
      command: ["node", "packages/backend/dist/index.js"]
      env:
        - name: NODE_ENV
          value: production
        - name: LAKEBASE_POSTGRES_HOST
          valueFrom: "secrets/ea-scope/lakebase-host"
        - name: LAKEBASE_POSTGRES_USER
          valueFrom: "secrets/ea-scope/lakebase-user"
        - name: LAKEBASE_POSTGRES_PASSWORD
          valueFrom: "secrets/ea-scope/lakebase-password"

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

### Subsystem 3: Backstage in Databricks Apps (`backstage/`)

Backstage is packaged to run within **Databricks Apps**, connecting to Databricks Lakebase Postgres.

#### Contract 3.1: Databricks App Manifest (`app.yaml`)
```yaml
version: 1
name: ea-backstage-portal
runtime: nodejs20
env:
  PORT: 8080
  APP_CONFIG_app_baseUrl: https://${DATABRICKS_APP_URL}
  APP_CONFIG_backend_baseUrl: https://${DATABRICKS_APP_URL}
  APP_CONFIG_backend_listen_port: 8080
build:
  command: "yarn build:backend"
run:
  command: "node packages/backend/dist/index.js"
```

#### Contract 3.2: `app-config.yaml` (Database & Catalog)
```yaml
app:
  title: Enterprise Architecture Portal
  baseUrl: ${APP_CONFIG_app_baseUrl}

backend:
  baseUrl: ${APP_CONFIG_backend_baseUrl}
  listen:
    port: ${APP_CONFIG_backend_listen_port}
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

#### Contract 3.3: Entity Provider Interface (`ea-catalog-provider.ts`)
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
      entities: entities.map(e => ({ entity: e, locationKey: 'ea-provider:lakebase' })),
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

### Subsystem 5: Agentic Automation Workflows & Dual LLM Support

#### Contract 5.1: Evaluator Provider Interface (`scripts/agent_arb_evaluator.py`)
```python
# Evaluator accepts dual provider selection via CLI or ENV:
# --provider databricks_mosaic  -> Queries Databricks Model Serving endpoint
# --provider external           -> Queries External OpenAI / Gemini / Anthropic API

import os
import argparse
import requests
import json

def get_llm_client(provider: str):
    if provider == "databricks_mosaic":
        host = os.environ["DATABRICKS_HOST"].rstrip("/")
        token = os.environ["DATABRICKS_TOKEN"]
        endpoint = os.environ.get("DATABRICKS_SERVING_ENDPOINT", "databricks-meta-llama-3-1-70b-instruct")
        url = f"{host}/serving-endpoints/{endpoint}/invocations"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        def complete(prompt: str) -> str:
            payload = {"messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        return complete

    elif provider == "external":
        base_url = os.environ.get("EXTERNAL_LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        api_key = os.environ["EXTERNAL_LLM_API_KEY"]
        model = os.environ.get("EXTERNAL_LLM_MODEL", "gpt-4o")
        url = f"{base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        def complete(prompt: str) -> str:
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        return complete
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
```

#### Contract 5.2: Autonomous ARB Review Gate (`arb-gate.yml`)
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
          # Select provider: 'databricks_mosaic' or 'external'
          LLM_PROVIDER: ${{ vars.LLM_PROVIDER || 'databricks_mosaic' }}
          # Option A credentials (Databricks Mosaic AI Model Serving)
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
          DATABRICKS_SERVING_ENDPOINT: ${{ vars.DATABRICKS_SERVING_ENDPOINT || 'databricks-meta-llama-3-1-70b-instruct' }}
          # Option B credentials (External API)
          EXTERNAL_LLM_API_KEY: ${{ secrets.EXTERNAL_LLM_API_KEY }}
          EXTERNAL_LLM_BASE_URL: ${{ vars.EXTERNAL_LLM_BASE_URL || 'https://api.openai.com/v1' }}
          EXTERNAL_LLM_MODEL: ${{ vars.EXTERNAL_LLM_MODEL || 'gpt-4o' }}
        run: |
          python scripts/agent_arb_evaluator.py \
            --provider "$LLM_PROVIDER" \
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
| **AC-003** | Backstage in Databricks Apps | Backstage app bundled via DAB | `databricks apps start ea-backstage-portal` runs | App starts in Databricks, serves UI on HTTPS URL, and connects to Lakebase |
| **AC-004** | Archify Render | A valid PAM subgraph JSON | `archify finalize` runs | Valid SVG file created with 0 overlapping nodes |
| **AC-005** | ARB PR Gate | A PR introducing an unapproved database | GitHub PR action triggers | Action leaves comment identifying violation and posts visual diff |
| **AC-006** | Drift Alert | Cloud CUR lists AWS Aurora missing from Git | Daily Drift Detector runs | GitHub Issue created with title `[Drift] Unregistered DB in us-east-1` |
| **AC-007** | Dual LLM Switching | Configured with `LLM_PROVIDER=databricks_mosaic` vs `external` | ARB evaluator runs | Evaluator successfully queries the selected endpoint and generates identical markdown evaluation format |

---

## 6. Implementation Task Breakdown (Execution Order)

The implementation must proceed sequentially according to this vertical slice:

```
[Task 1: Schemas] ──> [Task 2: Databricks DAB & Lakebase] ──> [Task 3: Backstage Databricks App] ──> [Task 4: Archify] ──> [Task 5: CI Agents with Dual LLM]
```

- [ ] **Task 1: Metamodel Schema Foundation**
  - Create `schemas/pam/nodes.schema.json`, `edges.schema.json`, `evidence.schema.json`.
  - Add AJV schema validation script to GitHub Actions.
  - *Verify:* Run `npm run test:schemas` against valid and invalid sample payloads.
- [ ] **Task 2: Databricks Asset Bundle & Lakebase**
  - Author `databricks/databricks.yml` declaring Unity Catalog tables, Lakebase PostgreSQL instance, and Backstage app resource.
  - *Verify:* `databricks bundle validate` passes and creates staging tables.
- [ ] **Task 3: Backstage in Databricks Apps Scaffolding**
  - Scaffold Backstage Node.js app using `@backstage/create-app`.
  - Author Databricks App manifest (`app.yaml`) and wire `app-config.yaml` to Lakebase Postgres.
  - Implement `EAMetamodelProvider` to sync Delta nodes into Backstage catalog.
  - *Verify:* Deploy to Databricks dev target (`databricks bundle deploy -t dev`) and verify app URL boots.
- [ ] **Task 4: Archify CLI Integration Bridge**
  - Write `bridge/pam-to-archify.py` to extract subgraphs to typed Archify JSON.
  - Package Docker container with Archify CLI.
  - *Verify:* Export a 5-node cluster and generate a valid SVG.
- [ ] **Task 5: ARB Gate & Drift Workflows (Dual LLM Support)**
  - Implement `scripts/agent_arb_evaluator.py` supporting both `databricks_mosaic` and `external` backends.
  - Author `.github/workflows/arb-gate.yml` with provider selection variables.
  - Author `.github/workflows/drift-detector.yml`.
  - *Verify:* Test evaluation against Databricks Mosaic AI serving endpoint and external fallback API.
