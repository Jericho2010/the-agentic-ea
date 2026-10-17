"""
Databricks Unity Catalog Schemas and Table Definitions for The Agentic EA.
Target Databricks Workspace: https://dbc-2d6963b0-153b.cloud.databricks.com/
Catalog: ea
"""
from __future__ import annotations

CATALOG_NAME = "ea"
SCHEMA_METAMODEL = f"{CATALOG_NAME}.metamodel"
SCHEMA_BRONZE = f"{CATALOG_NAME}.bronze"
SCHEMA_SILVER = f"{CATALOG_NAME}.silver"
SCHEMA_GOLD = f"{CATALOG_NAME}.gold"

DDL_STATEMENTS = {
    # Schemas
    "schemas": [
        f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_METAMODEL} COMMENT 'Platform Architecture Metamodel (PAM) Conformed Tables';",
        f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_BRONZE} COMMENT 'Raw Ingestion Feeds (Git AST, Cloud CUR, Cloud Provider)';",
        f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_SILVER} COMMENT 'Cleaned & Validated PAM Graph Entities';",
        f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_GOLD} COMMENT 'Scenario Analytics Marts (TIME Matrix, Drift Reconciled)';",
    ],
    # Conformed Metamodel Tables
    "nodes": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_METAMODEL}.nodes (
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
    """,
    "edges": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_METAMODEL}.edges (
        source_urn STRING NOT NULL COMMENT 'Source entity URN',
        target_urn STRING NOT NULL COMMENT 'Target entity URN',
        relation STRING NOT NULL COMMENT 'ArchiMate relation (serves, accesses, flows_to, deploys_to, realizes, depends_on)',
        protocol STRING COMMENT 'Communication transport protocol (e.g. HTTPS/JSON, gRPC/mTLS, PostgreSQL/TLS)',
        contains_pii BOOLEAN DEFAULT false COMMENT 'True if personal identifiable or sensitive data flows across edge',
        last_updated TIMESTAMP NOT NULL COMMENT 'Timestamp of last reconciliation'
    )
    USING DELTA
    COMMENT 'Conformed PAM architectural edges';
    """,
    "evidence": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_METAMODEL}.evidence (
        evidence_id STRING NOT NULL COMMENT 'Unique evidence UUID',
        repo_url STRING NOT NULL COMMENT 'Source repository URL',
        commit_hash STRING NOT NULL COMMENT 'Git commit SHA-1 or SHA-256',
        ast_fingerprint STRING NOT NULL COMMENT 'AST or manifest hash signature',
        discovered_at TIMESTAMP NOT NULL COMMENT 'Timestamp of discovery',
        source_file STRING COMMENT 'Relative path of file generating evidence',
        extracted_by STRING COMMENT 'Extractor name or AST engine'
    )
    USING DELTA
    COMMENT 'Provenance and audit evidence for discovered graph elements';
    """,
    # Bronze Ingestion Tables
    "bronze_git_repos": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_BRONZE}.git_repos (
        repo_id STRING NOT NULL,
        repo_name STRING NOT NULL,
        org_name STRING NOT NULL,
        default_branch STRING,
        languages STRING,
        manifest_files STRING,
        ast_nodes STRING,
        discovered_edges STRING,
        extracted_at TIMESTAMP NOT NULL
    )
    USING DELTA
    COMMENT 'Raw Git repository AST extractions and manifest scans';
    """,
    "bronze_cloud_resources": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_BRONZE}.cloud_resources (
        resource_id STRING NOT NULL,
        resource_name STRING NOT NULL,
        provider STRING NOT NULL,
        account_id STRING,
        region STRING,
        resource_type STRING,
        tags STRING,
        monthly_cost_usd DOUBLE,
        ingested_at TIMESTAMP NOT NULL
    )
    USING DELTA
    COMMENT 'Raw Cloud CUR billing records and cloud resource configurations';
    """,
    # Gold Scenario Marts
    "gold_time_matrix": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.time_matrix (
        name STRING NOT NULL COMMENT 'System / component name',
        urn STRING NOT NULL COMMENT 'Entity URN',
        disposition STRING NOT NULL COMMENT 'Gartner TIME disposition: Invest, Tolerate, Migrate, Eliminate',
        annual_run_cost DOUBLE NOT NULL COMMENT 'Annualized hosting, licensing, and operational run cost in USD',
        tech_debt_score INT NOT NULL COMMENT 'Calculated architectural debt score (0 = clean, 100 = critical debt)',
        eol_date DATE COMMENT 'Vendor end-of-life or planned retirement date'
    )
    USING DELTA
    COMMENT 'Executive TIME Matrix scenario data mart';
    """,
    "gold_drift_reconciled": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.drift_reconciled (
        urn STRING NOT NULL COMMENT 'Entity URN',
        declared_state STRING NOT NULL COMMENT 'State declared in Git/Architecture manifest',
        runtime_state STRING NOT NULL COMMENT 'Observed runtime cloud/telemetry state',
        discrepancy_type STRING NOT NULL COMMENT 'e.g. Unapproved Datastore, Unencrypted Storage, Missing Owner',
        severity STRING NOT NULL COMMENT 'CRITICAL, HIGH, MEDIUM, LOW',
        reconciled_at TIMESTAMP NOT NULL COMMENT 'Reconciliation timestamp'
    )
    USING DELTA
    COMMENT 'Reconciled architecture drift between declared manifests and live estate telemetry';
    """,
    "gold_capability_realization": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.capability_realization (
        capability_urn STRING NOT NULL COMMENT 'Unique Capability URN (e.g. urn:ea:capability:payment-processing)',
        capability_name STRING NOT NULL COMMENT 'Canonical business capability name',
        capability_level INT NOT NULL COMMENT 'Hierarchical level (1 = L1 Domain, 2 = L2 Functional)',
        parent_capability_urn STRING COMMENT 'Parent capability URN for L2 capabilities',
        parent_capability_name STRING COMMENT 'Parent capability name for L2 capabilities',
        realizing_entity_urn STRING NOT NULL COMMENT 'PAM entity URN realizing this capability',
        realizing_entity_name STRING NOT NULL COMMENT 'Name of application, microservice, or database',
        realizing_entity_kind STRING NOT NULL COMMENT 'Kind of realizing entity (Application, Microservice, Database, etc.)',
        disposition STRING NOT NULL COMMENT 'Gartner TIME disposition (Invest, Tolerate, Migrate, Eliminate)',
        allocated_annual_cost DOUBLE NOT NULL COMMENT 'Annualized cloud run cost allocated to this capability in USD',
        tech_debt_score INT NOT NULL COMMENT 'Technical debt score of realizing entity (0-100)',
        criticality STRING NOT NULL COMMENT 'Operational criticality tier (Tier-0, Tier-1, Tier-2, Tier-3)'
    )
    USING DELTA
    COMMENT 'Executive Business Capability Realization and FinOps Investment Alignment Data Mart';
    """,
    "gold_arb_audit_ledger": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.arb_audit_ledger (
        audit_id STRING NOT NULL COMMENT 'Unique ARB audit evaluation UUID',
        pr_id STRING NOT NULL COMMENT 'Pull Request identifier (e.g. PR-104)',
        commit_hash STRING NOT NULL COMMENT 'Git commit hash evaluated',
        decision STRING NOT NULL COMMENT 'ARB Governance Decision: APPROVED or BLOCKED',
        policy_status STRING NOT NULL COMMENT 'COMPLIANT or VIOLATION_DETECTED',
        violations_count INT NOT NULL COMMENT 'Number of detected architectural policy violations',
        violations_json STRING NOT NULL COMMENT 'Serialized JSON array of detected violations',
        evaluator STRING NOT NULL COMMENT 'Evaluation provider (subscription_cli, databricks_mosaic, external_api)',
        resources_evaluated INT NOT NULL COMMENT 'Number of resources extracted from diff',
        diagram_delta_path STRING COMMENT 'Path to compiled Archify visual delta artifact',
        timestamp TIMESTAMP NOT NULL COMMENT 'Timestamp of ARB evaluation receipt'
    )
    USING DELTA
    COMMENT 'Immutable Architecture Review Board (ARB) Pre-Merge Governance Audit Ledger';
    """,
}


