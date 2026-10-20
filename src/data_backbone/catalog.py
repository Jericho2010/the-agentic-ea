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
        transit_encryption STRING COMMENT 'In-transit encryption: tls_1_3, tls_1_2, plaintext',
        transferred_classification STRING COMMENT 'Data classification in flight: PII:High, PII:Medium, Internal, Public',
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
    "bronze_cmdb_ci": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_BRONZE}.cmdb_ci (
        sys_id STRING NOT NULL COMMENT 'ServiceNow unique sys_id',
        name STRING NOT NULL COMMENT 'Configuration Item name',
        ci_class STRING NOT NULL COMMENT 'CMDB CI class (e.g. cmdb_ci_appl, cmdb_ci_database, cmdb_ci_cloud_service)',
        operational_status STRING NOT NULL COMMENT 'Operational status (Operational, Retired, In Maintenance)',
        environment STRING COMMENT 'Environment (Production, Staging, Development)',
        tier STRING COMMENT 'Criticality tier (Tier-0, Tier-1, Tier-2, Tier-3)',
        owner_team STRING COMMENT 'Assigned support group / owner team',
        ip_address STRING COMMENT 'Management or ingress IP address',
        cloud_resource_id STRING COMMENT 'Associated cloud provider ARN or instance ID',
        raw_attributes STRING COMMENT 'JSON serialized attributes from ServiceNow CMDB',
        synced_at TIMESTAMP NOT NULL COMMENT 'Timestamp of last ServiceNow CMDB sync'
    )
    USING DELTA
    COMMENT 'Raw ServiceNow CMDB Configuration Items (Applications, Databases, Infrastructure)';
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
        drift_id STRING NOT NULL COMMENT 'Unique drift identifier UUID',
        urn STRING NOT NULL COMMENT 'Entity URN or identifier',
        ci_name STRING NOT NULL COMMENT 'Configuration item / entity name',
        drift_type STRING NOT NULL COMMENT 'ORPHAN_CI, SHADOW_IT, ATTRIBUTE_DRIFT, POLICY_VIOLATION',
        severity STRING NOT NULL COMMENT 'CRITICAL, HIGH, MEDIUM, LOW',
        declared_state STRING NOT NULL COMMENT 'State declared in Git/Architecture manifest or CMDB',
        runtime_state STRING NOT NULL COMMENT 'Observed runtime cloud/telemetry state',
        discrepancy_type STRING NOT NULL COMMENT 'e.g. Orphan CI, Undocumented Asset, Mismatched Tier',
        remediation_action STRING NOT NULL COMMENT 'RETIRE_CMDB_RECORD, REGISTER_CMDB_CI, SYNC_CMDB_METADATA, REMEDIATE_POLICY',
        remediation_payload STRING COMMENT 'JSON formatted ServiceNow REST API payload for automated remediation',
        reconciled_at TIMESTAMP NOT NULL COMMENT 'Reconciliation timestamp'
    )
    USING DELTA
    COMMENT 'Reconciled architecture and CMDB drift between declared manifests, CMDB baseline, and live telemetry';
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
    "gold_ma_synergies": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.ma_synergies (
        synergy_id STRING NOT NULL COMMENT 'Unique synergy item UUID',
        target_entity_name STRING NOT NULL COMMENT 'Acquired component name',
        target_entity_urn STRING NOT NULL COMMENT 'Acquired component URN',
        capability_name STRING NOT NULL COMMENT 'Realized capability',
        capability_urn STRING NOT NULL COMMENT 'Realized capability URN',
        core_counterpart_name STRING COMMENT 'Existing core enterprise component name',
        core_counterpart_urn STRING COMMENT 'Existing core enterprise component URN',
        overlap_type STRING NOT NULL COMMENT 'DUPLICATE_CAPABILITY, TECH_STACK_DIVERGENCE, DEBT_REMEDIATION',
        recommendation STRING NOT NULL COMMENT 'RETIRE_AND_MIGRATE, RATIONALIZE, RETAIN_TEMPORARILY',
        current_annual_cost DOUBLE NOT NULL COMMENT 'Current run cost of acquired asset in USD',
        potential_synergy_savings DOUBLE NOT NULL COMMENT 'Annual savings upon rationalization in USD',
        risk_level STRING NOT NULL COMMENT 'HIGH, MEDIUM, LOW',
        discovered_at TIMESTAMP NOT NULL COMMENT 'Discovery timestamp'
    )
    USING DELTA
    COMMENT 'M&A Day-One Portfolio Synergy & Overlap Analysis Mart';
    """,
    "gold_compliance_lineage": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.compliance_lineage (
        flow_id STRING NOT NULL COMMENT 'Unique privacy dataflow lineage UUID',
        source_urn STRING NOT NULL COMMENT 'Originating system/component PAM URN',
        target_urn STRING NOT NULL COMMENT 'Destination datastore/component PAM URN',
        data_classification STRING NOT NULL COMMENT 'Data classification: PII:High, PII:Medium, Internal, Public',
        jurisdiction_source STRING NOT NULL COMMENT 'Geographic jurisdiction of source (e.g. EU-West-1, US-East-1)',
        jurisdiction_target STRING NOT NULL COMMENT 'Geographic jurisdiction of target (e.g. EU-West-1, US-East-1)',
        is_cross_border BOOLEAN NOT NULL COMMENT 'True if flow crosses jurisdictional boundaries (e.g. EU to US)',
        transit_encryption STRING NOT NULL COMMENT 'Encryption in transit protocol: tls_1_3, plaintext',
        rest_encryption STRING NOT NULL COMMENT 'Encryption at rest at target: kms, none',
        gdpr_status STRING NOT NULL COMMENT 'COMPLIANT, ART32_VIOLATION, ART44_VIOLATION',
        dora_status STRING NOT NULL COMMENT 'RESILIENT, SPOF_RISK, UNREPLICATED_CRITICAL_DATASTORE',
        risk_level STRING NOT NULL COMMENT 'CRITICAL, HIGH, MEDIUM, LOW'
    )
    USING DELTA
    COMMENT 'Regulatory Compliance & Privacy Data Lineage (GDPR Article 32/44 & DORA ICT Resilience) Mart';
    """,
    "bronze_api_gateway_logs": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_BRONZE}.api_gateway_logs (
        log_id STRING NOT NULL COMMENT 'Unique API Gateway access log event UUID',
        endpoint STRING NOT NULL COMMENT 'Request path/URI (e.g. /v1/payments/authorize)',
        method STRING NOT NULL COMMENT 'HTTP/RPC method (GET, POST, PUT, DELETE, RPC)',
        protocol STRING NOT NULL COMMENT 'Transport/application protocol (HTTPS/REST, gRPC/mTLS, SOAP/XML)',
        auth_mechanism STRING NOT NULL COMMENT 'Authentication mechanism (OAuth2, mTLS, BearerToken, APIKey, None)',
        consumer_service STRING NOT NULL COMMENT 'Calling client or microservice identifier',
        provider_service STRING NOT NULL COMMENT 'Providing microservice or gateway name',
        requests_last_30d BIGINT NOT NULL COMMENT 'Aggregated request invocation count in the last 30 days',
        avg_latency_ms DOUBLE NOT NULL COMMENT 'Average response latency in milliseconds',
        error_rate DOUBLE NOT NULL COMMENT 'HTTP 4xx/5xx or RPC error rate (0.0 to 1.0)',
        last_seen_timestamp TIMESTAMP NOT NULL COMMENT 'Timestamp of most recent runtime invocation'
    )
    USING DELTA
    COMMENT 'Raw Ingested API Gateway Runtime Traffic Logs';
    """,
    "gold_interface_rationalization": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.interface_rationalization (
        interface_id STRING NOT NULL COMMENT 'Unique interface integration identifier (e.g. INT-001)',
        endpoint STRING NOT NULL COMMENT 'API endpoint path or RPC method',
        method STRING NOT NULL COMMENT 'HTTP or RPC method (GET, POST, PUT, DELETE, RPC)',
        protocol STRING NOT NULL COMMENT 'Protocol (HTTPS/REST, gRPC/mTLS, SOAP/XML)',
        provider_service STRING NOT NULL COMMENT 'Providing microservice or application URN/name',
        consumer_service STRING NOT NULL COMMENT 'Calling consumer microservice or application URN/name',
        is_declared BOOLEAN NOT NULL COMMENT 'True if documented in OpenAPI/PAM metamodel',
        is_active_runtime BOOLEAN NOT NULL COMMENT 'True if active in runtime API gateway traffic logs',
        discrepancy_type STRING NOT NULL COMMENT 'ZOMBIE_SHADOW, DEAD_ORPHAN, PROTOCOL_SPRAWL, COMPLIANT',
        rationalization_action STRING NOT NULL COMMENT 'DECOMMISSION, DOCUMENT_AND_SECURE, STANDARDIZE_MTLS, RETAIN',
        last_active_timestamp TIMESTAMP NOT NULL COMMENT 'Timestamp of last active invocation or registration'
    )
    USING DELTA
    COMMENT 'Conformed Interface and API Integration Landscape Rationalization Mart';
    """,
    "bronze_process_event_logs": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_BRONZE}.process_event_logs (
        trace_id STRING NOT NULL COMMENT 'Distributed trace identifier UUID',
        process_id STRING NOT NULL COMMENT 'Business process identifier (e.g. PROC-ORDER-TO-CASH)',
        step_id STRING NOT NULL COMMENT 'Sequential step identifier (e.g. STEP-01)',
        step_name STRING NOT NULL COMMENT 'Human-readable step name',
        service_urn STRING NOT NULL COMMENT 'Executing service or datastore PAM URN',
        duration_ms DOUBLE NOT NULL COMMENT 'Execution span duration in milliseconds',
        status STRING NOT NULL COMMENT 'Span execution status (SUCCESS, FAILED, SLA_BREACH)',
        timestamp TIMESTAMP NOT NULL COMMENT 'Event execution timestamp'
    )
    USING DELTA
    COMMENT 'Raw Ingested Distributed Process Execution Event Logs';
    """,
    "gold_process_optimization": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.process_optimization (
        process_id STRING NOT NULL COMMENT 'Business process identifier (e.g. PROC-ORDER-TO-CASH)',
        process_name STRING NOT NULL COMMENT 'Business process name (e.g. Order-to-Cash Customer Journey)',
        step_id STRING NOT NULL COMMENT 'Sequential step identifier (e.g. STEP-01)',
        step_name STRING NOT NULL COMMENT 'Step name',
        service_urn STRING NOT NULL COMMENT 'Executing service or datastore PAM URN',
        p50_latency_ms DOUBLE NOT NULL COMMENT '50th percentile latency in milliseconds',
        p95_latency_ms DOUBLE NOT NULL COMMENT '95th percentile latency in milliseconds',
        p99_latency_ms DOUBLE NOT NULL COMMENT '99th percentile latency in milliseconds',
        sla_target_ms DOUBLE NOT NULL COMMENT 'Agreed SLA target latency in milliseconds',
        error_rate_pct DOUBLE NOT NULL COMMENT 'Step error percentage (0.0 to 100.0)',
        is_bottleneck BOOLEAN NOT NULL COMMENT 'True if step is identified as a critical journey bottleneck',
        optimization_action STRING NOT NULL COMMENT 'Recommended architectural optimization remedy'
    )
    USING DELTA
    COMMENT 'Conformed Business Process Mining & Optimization Mart';
    """,
    "bronze_ai_models": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_BRONZE}.ai_models (
        model_id STRING NOT NULL COMMENT 'Unique AI/ML model identifier',
        model_name STRING NOT NULL COMMENT 'Canonical model name in MLflow registry',
        version STRING NOT NULL COMMENT 'Model version semver',
        framework STRING NOT NULL COMMENT 'ML framework (PyTorch, LangChain, Scikit-learn, etc.)',
        task_type STRING NOT NULL COMMENT 'AI task type (Emotion Recognition, Fraud Detection, GenAI Chatbot, Recommendation)',
        training_dataset_urn STRING NOT NULL COMMENT 'PAM URN of training dataset',
        serving_endpoint_urn STRING NOT NULL COMMENT 'PAM URN of model serving endpoint',
        owner_team STRING NOT NULL COMMENT 'Responsible engineering or data science team',
        license STRING NOT NULL COMMENT 'Model or weights license',
        has_human_in_the_loop BOOLEAN NOT NULL COMMENT 'True if human oversight is embedded in decision loop',
        timestamp TIMESTAMP NOT NULL COMMENT 'Registration timestamp'
    )
    USING DELTA
    COMMENT 'Raw Ingested AI/ML Model Registry Catalog';
    """,
    "gold_ai_governance": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.ai_governance (
        model_id STRING NOT NULL COMMENT 'Unique AI/ML model identifier',
        model_name STRING NOT NULL COMMENT 'Model name',
        version STRING NOT NULL COMMENT 'Model version',
        task_type STRING NOT NULL COMMENT 'AI task type',
        eu_risk_tier STRING NOT NULL COMMENT 'EU AI Act Risk Tier: UNACCEPTABLE_RISK, HIGH_RISK, LIMITED_RISK, MINIMAL_RISK',
        compliance_status STRING NOT NULL COMMENT 'COMPLIANT, ACTION_REQUIRED, PROHIBITED',
        has_model_card BOOLEAN NOT NULL COMMENT 'True if formal model card and risk documentation exists',
        has_data_lineage BOOLEAN NOT NULL COMMENT 'True if end-to-end training data to inference lineage is tracked',
        has_human_oversight BOOLEAN NOT NULL COMMENT 'True if human-in-the-loop oversight is active',
        governance_action STRING NOT NULL COMMENT 'DECOMMISSION_IMMEDIATELY, ENFORCE_HUMAN_OVERSIGHT, ATTACH_AI_DISCLOSURE, RETAIN'
    )
    USING DELTA
    COMMENT 'Conformed AI Governance & EU AI Act Compliance Mart';
    """,
    "gold_resilience_dr": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.resilience_dr (
        component_urn STRING NOT NULL COMMENT 'Unique PAM entity URN',
        dr_tier STRING NOT NULL COMMENT 'Disaster Recovery tier (Tier-1, Tier-2, Tier-3)',
        rto_actual_min INT NOT NULL COMMENT 'Current actual Recovery Time Objective in minutes',
        rto_target_min INT NOT NULL COMMENT 'Target agreed Recovery Time Objective in minutes',
        rpo_actual_min INT NOT NULL COMMENT 'Current actual Recovery Point Objective in minutes',
        rpo_target_min INT NOT NULL COMMENT 'Target agreed Recovery Point Objective in minutes',
        replication_strategy STRING NOT NULL COMMENT 'Replication architecture pattern',
        failover_automation STRING NOT NULL COMMENT 'Failover automation posture (AUTOMATED, MANUAL_RUNBOOK, NONE)',
        sla_breached BOOLEAN NOT NULL COMMENT 'True if actual RTO/RPO exceeds target SLA'
    )
    USING DELTA
    COMMENT 'Conformed Disaster Recovery, Business Continuity & RTO/RPO Alignment Mart';
    """,
    "gold_tech_debt_hotspots": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.tech_debt_hotspots (
        component_urn STRING NOT NULL COMMENT 'Unique PAM entity URN',
        debt_score INT NOT NULL COMMENT 'Calculated architectural technical debt score (0-100)',
        git_churn_lines_30d INT NOT NULL COMMENT 'Git code churn volume in lines over last 30 days',
        cyclomatic_complexity DOUBLE NOT NULL COMMENT 'Average cyclomatic code complexity index',
        architectural_smells STRING NOT NULL COMMENT 'Detected structural code and architectural smells',
        refactoring_roi_rank INT NOT NULL COMMENT 'Prioritized refactoring ROI rank (1 = highest priority)'
    )
    USING DELTA
    COMMENT 'Conformed Technical Debt Quantification & Refactoring Hotspots Mart';
    """,
    "gold_security_zero_trust": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.security_zero_trust (
        source_urn STRING NOT NULL COMMENT 'Source PAM entity URN',
        target_urn STRING NOT NULL COMMENT 'Target PAM entity URN',
        protocol STRING NOT NULL COMMENT 'Network / application protocol and port',
        mtls_enforced BOOLEAN NOT NULL COMMENT 'True if mutual TLS (mTLS) cryptographic identity is enforced',
        trust_zone_source STRING NOT NULL COMMENT 'Zero-Trust perimeter zone of source',
        trust_zone_target STRING NOT NULL COMMENT 'Zero-Trust perimeter zone of target',
        microsegmentation_status STRING NOT NULL COMMENT 'Microsegmentation status: COMPLIANT, UNAUTHORIZED_CROSS_ZONE, PLAINTEXT_TRAFFIC'
    )
    USING DELTA
    COMMENT 'Conformed Zero-Trust Security & Network Micro-Segmentation Mart';
    """,
    "gold_supply_chain_sbom": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.supply_chain_sbom (
        package_name STRING NOT NULL COMMENT 'Third-party open-source or commercial library name',
        version STRING NOT NULL COMMENT 'Package version string',
        component_urn STRING NOT NULL COMMENT 'Consuming PAM entity URN',
        license STRING NOT NULL COMMENT 'Software license (e.g. MIT, Apache-2.0, GPL-3.0)',
        license_compliance STRING NOT NULL COMMENT 'License gate posture: APPROVED, PROHIBITED_COPYLEFT',
        cve_count INT NOT NULL COMMENT 'Number of detected known security vulnerabilities',
        max_severity STRING NOT NULL COMMENT 'Highest vulnerability severity: NONE, LOW, MEDIUM, HIGH, CRITICAL'
    )
    USING DELTA
    COMMENT 'Conformed Software Supply Chain, SBOM & Open Source Licensing Gate Mart';
    """,
    "gold_finops_unit_economics": f"""
    CREATE TABLE IF NOT EXISTS {SCHEMA_GOLD}.finops_unit_economics (
        service_urn STRING NOT NULL COMMENT 'Unique PAM entity URN',
        monthly_spend DOUBLE NOT NULL COMMENT 'Total allocated monthly cloud hosting and infrastructure spend in USD',
        cost_per_transaction DOUBLE NOT NULL COMMENT 'Unit cost per business order / transaction in USD',
        tag_compliance_pct DOUBLE NOT NULL COMMENT 'Percentage of cloud resources adhering to mandatory FinOps tags',
        idle_waste_cost DOUBLE NOT NULL COMMENT 'Identified monthly idle waste or overprovisioned compute cost in USD',
        optimization_action STRING NOT NULL COMMENT 'Recommended FinOps action (RIGHTSIZE_COMPUTE, DECOMMISSION_AND_ELIMINATE, RETAIN)'
    )
    USING DELTA
    COMMENT 'Conformed FinOps Cloud Cost Allocation & Unit Economics Alignment Mart';
    """,
}



