-- ==============================================================================
-- Databricks Unity Catalog DDLs: Conformed Metamodel & Scenario Marts
-- Workspace: https://dbc-2d6963b0-153b.cloud.databricks.com/
-- Catalog: ea
-- ==============================================================================

-- 1. Unity Catalog Schemas
CREATE SCHEMA IF NOT EXISTS ea.metamodel COMMENT 'Platform Architecture Metamodel (PAM) Conformed Tables';
CREATE SCHEMA IF NOT EXISTS ea.bronze COMMENT 'Raw Ingestion Feeds (Git AST, Cloud CUR, Cloud Provider)';
CREATE SCHEMA IF NOT EXISTS ea.silver COMMENT 'Cleaned & Validated PAM Graph Entities';
CREATE SCHEMA IF NOT EXISTS ea.gold COMMENT 'Scenario Analytics Marts (TIME Matrix, Drift Reconciled)';

-- 2. Conformed PAM Metamodel Nodes
CREATE TABLE IF NOT EXISTS ea.metamodel.nodes (
    urn STRING NOT NULL COMMENT 'Unique PAM Uniform Resource Name (urn:ea:<kind>:<slug>)',
    name STRING NOT NULL COMMENT 'Canonical architectural entity name',
    kind STRING NOT NULL COMMENT 'Entity kind (Application, Microservice, Database, CloudResource, APIInterface)',
    owner_team STRING NOT NULL COMMENT 'Owning engineering or platform team',
    lifecycle_status STRING NOT NULL DEFAULT 'run' COMMENT 'Lifecycle phase (plan, build, run, phase-out, retired)',
    criticality STRING NOT NULL COMMENT 'Architectural criticality (Tier-0, Tier-1, Tier-2, Tier-3)',
    metadata STRING COMMENT 'JSON string containing configuration, runtime, framework, and tags',
    last_updated TIMESTAMP NOT NULL COMMENT 'Timestamp of last update or reconciliation'
)
USING DELTA
COMMENT 'Conformed PAM architectural nodes';

-- 3. Conformed PAM Metamodel Edges
CREATE TABLE IF NOT EXISTS ea.metamodel.edges (
    source_urn STRING NOT NULL COMMENT 'Source entity URN',
    target_urn STRING NOT NULL COMMENT 'Target entity URN',
    relation STRING NOT NULL COMMENT 'ArchiMate relation (serves, accesses, flows_to, deploys_to, realizes, depends_on)',
    protocol STRING COMMENT 'Communication transport protocol (e.g. HTTPS/JSON, gRPC/mTLS, PostgreSQL/TLS)',
    contains_pii BOOLEAN DEFAULT false COMMENT 'True if personal identifiable or sensitive data flows across edge',
    last_updated TIMESTAMP NOT NULL COMMENT 'Timestamp of last reconciliation'
)
USING DELTA
COMMENT 'Conformed PAM architectural edges';

-- 4. Audit & Discovery Evidence
CREATE TABLE IF NOT EXISTS ea.metamodel.evidence (
    evidence_id STRING NOT NULL COMMENT 'Unique evidence UUID',
    repo_url STRING NOT NULL COMMENT 'Source repository URL',
    commit_hash STRING NOT NULL COMMENT 'Git commit SHA',
    ast_fingerprint STRING NOT NULL COMMENT 'AST or manifest hash signature',
    discovered_at TIMESTAMP NOT NULL COMMENT 'Timestamp of discovery',
    source_file STRING COMMENT 'Relative path of file generating evidence',
    extracted_by STRING COMMENT 'Extractor name or AST engine'
)
USING DELTA
COMMENT 'Provenance and audit evidence for discovered graph elements';

-- 5. Executive TIME Matrix Data Mart
CREATE TABLE IF NOT EXISTS ea.gold.time_matrix (
    name STRING NOT NULL COMMENT 'System / component name',
    urn STRING NOT NULL COMMENT 'Entity URN',
    disposition STRING NOT NULL COMMENT 'Gartner TIME disposition: Invest, Tolerate, Migrate, Eliminate',
    annual_run_cost DOUBLE NOT NULL COMMENT 'Annualized hosting, licensing, and operational run cost in USD',
    tech_debt_score INT NOT NULL COMMENT 'Calculated architectural debt score (0 = clean, 100 = critical debt)',
    eol_date DATE COMMENT 'Vendor end-of-life or planned retirement date'
)
USING DELTA
COMMENT 'Executive TIME Matrix scenario data mart';

-- 6. Architecture Drift Reconciled
CREATE TABLE IF NOT EXISTS ea.gold.drift_reconciled (
    urn STRING NOT NULL COMMENT 'Entity URN',
    declared_state STRING NOT NULL COMMENT 'State declared in Git/Architecture manifest',
    runtime_state STRING NOT NULL COMMENT 'Observed runtime cloud/telemetry state',
    discrepancy_type STRING NOT NULL COMMENT 'e.g. Unapproved Datastore, Unencrypted Storage, Missing Owner',
    severity STRING NOT NULL COMMENT 'CRITICAL, HIGH, MEDIUM, LOW',
    reconciled_at TIMESTAMP NOT NULL COMMENT 'Reconciliation timestamp'
)
USING DELTA
COMMENT 'Reconciled architecture drift between declared manifests and live estate telemetry';
