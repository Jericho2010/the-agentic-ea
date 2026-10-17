"""
Seed Data Script for Databricks Unity Catalog Conformed PAM Metamodel & Scenario Marts.
Populates ea.metamodel.nodes, ea.metamodel.edges, ea.gold.time_matrix, and ea.gold.drift_reconciled.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.data_backbone.client import get_unity_catalog_client

SEED_NODES = [
    {
        "urn": "urn:ea:application:web-storefront",
        "name": "web-storefront",
        "kind": "Application",
        "owner_team": "team-frontend",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "framework": "Next.js 14 / React",
            "domain": "store.enterprise.com",
            "ingress": "Cloudflare Edge",
        },
    },
    {
        "urn": "urn:ea:microservice:checkout-service",
        "name": "checkout-service",
        "kind": "Microservice",
        "owner_team": "team-checkout",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "runtime": "Java 21 / Spring Boot 3",
            "container": "distroless",
            "repo": "https://github.com/enterprise/checkout-service",
        },
    },
    {
        "urn": "urn:ea:microservice:payments-api",
        "name": "payments-api",
        "kind": "Microservice",
        "owner_team": "team-payments",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "runtime": "Go 1.22 / Gin",
            "pci_dss_scope": True,
            "repo": "https://github.com/enterprise/payments-api",
        },
    },
    {
        "urn": "urn:ea:microservice:payments-service",
        "name": "payments-service",
        "kind": "Microservice",
        "owner_team": "team-payments",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "runtime": "Go 1.22",
            "ledger_sync": True,
        },
    },
    {
        "urn": "urn:ea:microservice:auth-gateway",
        "name": "auth-gateway",
        "kind": "Microservice",
        "owner_team": "team-infra",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "proxy": "Envoy 1.29",
            "protocol": "mTLS / OAuth2",
        },
    },
    {
        "urn": "urn:ea:microservice:auth-service",
        "name": "auth-service",
        "kind": "Microservice",
        "owner_team": "team-auth",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "runtime": "Node.js 20",
            "status": "legacy-auth",
            "migration_target": "Auth0 / Okta",
            "eol_date": "2027-04-15",
        },
    },
    {
        "urn": "urn:ea:database:billing-db",
        "name": "billing-db",
        "kind": "Database",
        "owner_team": "team-data-platform",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "engine": "PostgreSQL 16 RDS",
            "encryption": "AES-256-GCM (AWS KMS)",
            "backup_retention_days": 35,
        },
    },
    {
        "urn": "urn:ea:database:payments-ledger-db",
        "name": "payments-ledger-db",
        "kind": "Database",
        "owner_team": "team-payments",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "engine": "PostgreSQL 16 RDS",
            "encryption": "KMS-Customer-Managed",
            "immutability": True,
        },
    },
    {
        "urn": "urn:ea:cloudresource:customer-pii-stream",
        "name": "customer-pii-stream",
        "kind": "CloudResource",
        "owner_team": "team-data-platform",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "provider": "AWS Kinesis Data Streams",
            "contains_pii": True,
            "encryption": "KMS-Customer-Managed",
            "retention_hours": 72,
            "eol_date": "2026-12-31",
        },
    },
    {
        "urn": "urn:ea:apiinterface:stripe-gateway",
        "name": "stripe-gateway",
        "kind": "APIInterface",
        "owner_team": "team-payments",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "type": "External-SaaS",
            "protocol": "HTTPS/TLS-1.3",
            "provider": "Stripe Payments Europe",
        },
    },
    {
        "urn": "urn:ea:database:cassandra-legacy-cluster",
        "name": "cassandra-legacy-cluster",
        "kind": "Database",
        "owner_team": "team-legacy-ops",
        "lifecycle_status": "phase-out",
        "criticality": "Tier-2",
        "metadata": {
            "engine": "Apache Cassandra 3.11",
            "encryption": "None",
            "backup_retention_days": 7,
            "eol_date": "2025-12-31",
            "disposition": "Eliminate",
        },
    },
    # --------------------------------------------------------------------------
    # Business Capabilities (Level-1 Strategic Domains & Level-2 Capabilities)
    # --------------------------------------------------------------------------
    {
        "urn": "urn:ea:capability:customer-experience",
        "name": "Customer Experience",
        "kind": "BusinessCapability",
        "owner_team": "exec-digital",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "level": 1,
            "domain": "Digital Commerce",
            "description": "End-to-end customer interaction, catalog discovery, and shopping journey.",
        },
    },
    {
        "urn": "urn:ea:capability:finance-and-billing",
        "name": "Finance & Billing",
        "kind": "BusinessCapability",
        "owner_team": "exec-finance",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "level": 1,
            "domain": "Financial Systems",
            "description": "Payment authorization, merchant settlement, ledger bookkeeping, and billing.",
        },
    },
    {
        "urn": "urn:ea:capability:security-and-compliance",
        "name": "Security & Compliance",
        "kind": "BusinessCapability",
        "owner_team": "exec-security",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "level": 1,
            "domain": "Enterprise Security",
            "description": "Identity verification, access control, encryption, and PII regulatory protection.",
        },
    },
    {
        "urn": "urn:ea:capability:digital-storefront",
        "name": "Digital Storefront",
        "kind": "BusinessCapability",
        "owner_team": "team-frontend",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "level": 2,
            "parent_urn": "urn:ea:capability:customer-experience",
            "parent_name": "Customer Experience",
            "description": "Web and mobile digital channel presentation and shopping cart management.",
        },
    },
    {
        "urn": "urn:ea:capability:order-fulfillment",
        "name": "Order Fulfillment",
        "kind": "BusinessCapability",
        "owner_team": "team-checkout",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "level": 2,
            "parent_urn": "urn:ea:capability:customer-experience",
            "parent_name": "Customer Experience",
            "description": "Checkout orchestration, order lifecycle processing, and inventory capture.",
        },
    },
    {
        "urn": "urn:ea:capability:payment-processing",
        "name": "Payment Processing",
        "kind": "BusinessCapability",
        "owner_team": "team-payments",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "level": 2,
            "parent_urn": "urn:ea:capability:finance-and-billing",
            "parent_name": "Finance & Billing",
            "description": "PCI-compliant payment transaction gateway, acquiring routing, and card authorization.",
        },
    },
    {
        "urn": "urn:ea:capability:subscription-billing",
        "name": "Subscription & Invoicing",
        "kind": "BusinessCapability",
        "owner_team": "team-data-platform",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "level": 2,
            "parent_urn": "urn:ea:capability:finance-and-billing",
            "parent_name": "Finance & Billing",
            "description": "Recurring customer invoicing, ledger persistence, and receivables accounting.",
        },
    },
    {
        "urn": "urn:ea:capability:identity-and-access-management",
        "name": "Identity & Access Management",
        "kind": "BusinessCapability",
        "owner_team": "team-auth",
        "lifecycle_status": "run",
        "criticality": "Tier-0",
        "metadata": {
            "level": 2,
            "parent_urn": "urn:ea:capability:security-and-compliance",
            "parent_name": "Security & Compliance",
            "description": "Authentication tokens, mTLS ingress verification, and user session management.",
        },
    },
    {
        "urn": "urn:ea:capability:data-privacy-and-governance",
        "name": "Data Privacy & Governance",
        "kind": "BusinessCapability",
        "owner_team": "team-data-platform",
        "lifecycle_status": "run",
        "criticality": "Tier-1",
        "metadata": {
            "level": 2,
            "parent_urn": "urn:ea:capability:security-and-compliance",
            "parent_name": "Security & Compliance",
            "description": "PII event stream filtering, regulatory data retention, and audit logging.",
        },
    },
]

SEED_EDGES = [
    {
        "source_urn": "urn:ea:application:web-storefront",
        "target_urn": "urn:ea:microservice:checkout-service",
        "relation": "flows_to",
        "protocol": "HTTPS/REST",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:microservice:checkout-service",
        "target_urn": "urn:ea:microservice:auth-service",
        "relation": "accesses",
        "protocol": "gRPC/mTLS",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:microservice:checkout-service",
        "target_urn": "urn:ea:microservice:payments-api",
        "relation": "serves",
        "protocol": "HTTPS/JSON",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:microservice:payments-api",
        "target_urn": "urn:ea:apiinterface:stripe-gateway",
        "relation": "flows_to",
        "protocol": "HTTPS/REST",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:microservice:payments-api",
        "target_urn": "urn:ea:cloudresource:customer-pii-stream",
        "relation": "flows_to",
        "protocol": "Kinesis-SDK",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:payments-api",
        "target_urn": "urn:ea:database:billing-db",
        "relation": "accesses",
        "protocol": "PostgreSQL/TLS",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:payments-service",
        "target_urn": "urn:ea:database:payments-ledger-db",
        "relation": "accesses",
        "protocol": "PostgreSQL/TLS",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:payments-api",
        "target_urn": "urn:ea:microservice:payments-service",
        "relation": "flows_to",
        "protocol": "gRPC/mTLS",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:payments-service",
        "target_urn": "urn:ea:database:cassandra-legacy-cluster",
        "relation": "accesses",
        "protocol": "CQL/TCP",
        "contains_pii": True,
    },
    # --------------------------------------------------------------------------
    # Capability Hierarchy Edges (Level-1 aggregates Level-2)
    # --------------------------------------------------------------------------
    {
        "source_urn": "urn:ea:capability:customer-experience",
        "target_urn": "urn:ea:capability:digital-storefront",
        "relation": "aggregates",
        "protocol": "ArchiMate/Composition",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:capability:customer-experience",
        "target_urn": "urn:ea:capability:order-fulfillment",
        "relation": "aggregates",
        "protocol": "ArchiMate/Composition",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:capability:finance-and-billing",
        "target_urn": "urn:ea:capability:payment-processing",
        "relation": "aggregates",
        "protocol": "ArchiMate/Composition",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:capability:finance-and-billing",
        "target_urn": "urn:ea:capability:subscription-billing",
        "relation": "aggregates",
        "protocol": "ArchiMate/Composition",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:capability:security-and-compliance",
        "target_urn": "urn:ea:capability:identity-and-access-management",
        "relation": "aggregates",
        "protocol": "ArchiMate/Composition",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:capability:security-and-compliance",
        "target_urn": "urn:ea:capability:data-privacy-and-governance",
        "relation": "aggregates",
        "protocol": "ArchiMate/Composition",
        "contains_pii": False,
    },
    # --------------------------------------------------------------------------
    # Business Capability Realization Edges (Application/Service realizes Capability)
    # --------------------------------------------------------------------------
    {
        "source_urn": "urn:ea:application:web-storefront",
        "target_urn": "urn:ea:capability:digital-storefront",
        "relation": "realizes",
        "protocol": "Application/Realization",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:microservice:checkout-service",
        "target_urn": "urn:ea:capability:order-fulfillment",
        "relation": "realizes",
        "protocol": "Service/Realization",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:database:cassandra-legacy-cluster",
        "target_urn": "urn:ea:capability:order-fulfillment",
        "relation": "realizes",
        "protocol": "Datastore/Realization",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:payments-api",
        "target_urn": "urn:ea:capability:payment-processing",
        "relation": "realizes",
        "protocol": "API/Realization",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:payments-service",
        "target_urn": "urn:ea:capability:payment-processing",
        "relation": "realizes",
        "protocol": "Service/Realization",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:database:billing-db",
        "target_urn": "urn:ea:capability:subscription-billing",
        "relation": "realizes",
        "protocol": "Datastore/Realization",
        "contains_pii": True,
    },
    {
        "source_urn": "urn:ea:microservice:auth-service",
        "target_urn": "urn:ea:capability:identity-and-access-management",
        "relation": "realizes",
        "protocol": "Service/Realization",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:microservice:auth-gateway",
        "target_urn": "urn:ea:capability:identity-and-access-management",
        "relation": "realizes",
        "protocol": "Gateway/Realization",
        "contains_pii": False,
    },
    {
        "source_urn": "urn:ea:cloudresource:customer-pii-stream",
        "target_urn": "urn:ea:capability:data-privacy-and-governance",
        "relation": "realizes",
        "protocol": "EventStream/Realization",
        "contains_pii": True,
    },
]

SEED_TIME_MATRIX = [
    {
        "name": "payments-api",
        "urn": "urn:ea:microservice:payments-api",
        "disposition": "Invest",
        "annual_run_cost": 72000.0,
        "tech_debt_score": 10,
        "eol_date": "2030-01-01",
    },
    {
        "name": "billing-db",
        "urn": "urn:ea:database:billing-db",
        "disposition": "Invest",
        "annual_run_cost": 54999.96,
        "tech_debt_score": 12,
        "eol_date": "2029-12-31",
    },
    {
        "name": "checkout-service",
        "urn": "urn:ea:microservice:checkout-service",
        "disposition": "Invest",
        "annual_run_cost": 48000.0,
        "tech_debt_score": 18,
        "eol_date": "2029-06-30",
    },
    {
        "name": "web-storefront",
        "urn": "urn:ea:application:web-storefront",
        "disposition": "Invest",
        "annual_run_cost": 34999.92,
        "tech_debt_score": 15,
        "eol_date": "2028-12-31",
    },
    {
        "name": "auth-service",
        "urn": "urn:ea:microservice:auth-service",
        "disposition": "Tolerate",
        "annual_run_cost": 24999.96,
        "tech_debt_score": 35,
        "eol_date": "2027-04-15",
    },
    {
        "name": "customer-pii-stream",
        "urn": "urn:ea:cloudresource:customer-pii-stream",
        "disposition": "Migrate",
        "annual_run_cost": 7800.0,
        "tech_debt_score": 65,
        "eol_date": "2026-12-31",
    },
    {
        "name": "cassandra-legacy-cluster",
        "urn": "urn:ea:database:cassandra-legacy-cluster",
        "disposition": "Eliminate",
        "annual_run_cost": 64999.92,
        "tech_debt_score": 90,
        "eol_date": "2025-12-31",
    },
]


SEED_DRIFT = [
    {
        "urn": "urn:ea:database:orders-cassandra-db",
        "declared_state": "Terraform PR #104 (Proposed: Cassandra 3.11, ContainsPII=true, Encrypted=false)",
        "runtime_state": "Policy Rule Violation: Datastore in Eliminate Disposition; Unencrypted Storage",
        "discrepancy_type": "Unapproved Datastore / Security Non-Compliance",
        "severity": "CRITICAL",
        "reconciled_at": "2026-10-16T12:00:00Z",
    }
]


SEED_CAPABILITY_REALIZATIONS = [
    {
        "capability_urn": "urn:ea:capability:digital-storefront",
        "capability_name": "Digital Storefront",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:customer-experience",
        "parent_capability_name": "Customer Experience",
        "realizing_entity_urn": "urn:ea:application:web-storefront",
        "realizing_entity_name": "web-storefront",
        "realizing_entity_kind": "Application",
        "disposition": "Invest",
        "allocated_annual_cost": 34999.92,
        "tech_debt_score": 15,
        "criticality": "Tier-1",
    },
    {
        "capability_urn": "urn:ea:capability:order-fulfillment",
        "capability_name": "Order Fulfillment",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:customer-experience",
        "parent_capability_name": "Customer Experience",
        "realizing_entity_urn": "urn:ea:microservice:checkout-service",
        "realizing_entity_name": "checkout-service",
        "realizing_entity_kind": "Microservice",
        "disposition": "Invest",
        "allocated_annual_cost": 48000.00,
        "tech_debt_score": 18,
        "criticality": "Tier-1",
    },
    {
        "capability_urn": "urn:ea:capability:order-fulfillment",
        "capability_name": "Order Fulfillment",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:customer-experience",
        "parent_capability_name": "Customer Experience",
        "realizing_entity_urn": "urn:ea:database:cassandra-legacy-cluster",
        "realizing_entity_name": "cassandra-legacy-cluster",
        "realizing_entity_kind": "Database",
        "disposition": "Eliminate",
        "allocated_annual_cost": 64999.92,
        "tech_debt_score": 90,
        "criticality": "Tier-2",
    },
    {
        "capability_urn": "urn:ea:capability:payment-processing",
        "capability_name": "Payment Processing",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:finance-and-billing",
        "parent_capability_name": "Finance & Billing",
        "realizing_entity_urn": "urn:ea:microservice:payments-api",
        "realizing_entity_name": "payments-api",
        "realizing_entity_kind": "Microservice",
        "disposition": "Invest",
        "allocated_annual_cost": 72000.00,
        "tech_debt_score": 10,
        "criticality": "Tier-0",
    },
    {
        "capability_urn": "urn:ea:capability:subscription-billing",
        "capability_name": "Subscription & Invoicing",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:finance-and-billing",
        "parent_capability_name": "Finance & Billing",
        "realizing_entity_urn": "urn:ea:database:billing-db",
        "realizing_entity_name": "billing-db",
        "realizing_entity_kind": "Database",
        "disposition": "Invest",
        "allocated_annual_cost": 54999.96,
        "tech_debt_score": 12,
        "criticality": "Tier-0",
    },
    {
        "capability_urn": "urn:ea:capability:identity-and-access-management",
        "capability_name": "Identity & Access Management",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:security-and-compliance",
        "parent_capability_name": "Security & Compliance",
        "realizing_entity_urn": "urn:ea:microservice:auth-service",
        "realizing_entity_name": "auth-service",
        "realizing_entity_kind": "Microservice",
        "disposition": "Tolerate",
        "allocated_annual_cost": 24999.96,
        "tech_debt_score": 35,
        "criticality": "Tier-0",
    },
    {
        "capability_urn": "urn:ea:capability:data-privacy-and-governance",
        "capability_name": "Data Privacy & Governance",
        "capability_level": 2,
        "parent_capability_urn": "urn:ea:capability:security-and-compliance",
        "parent_capability_name": "Security & Compliance",
        "realizing_entity_urn": "urn:ea:cloudresource:customer-pii-stream",
        "realizing_entity_name": "customer-pii-stream",
        "realizing_entity_kind": "CloudResource",
        "disposition": "Migrate",
        "allocated_annual_cost": 7800.00,
        "tech_debt_score": 65,
        "criticality": "Tier-1",
    },
]


SEED_ARB_AUDIT_LEDGER = [
    {
        "audit_id": "arb-pr-104-historical",
        "pr_id": "PR-104",
        "commit_hash": "8a91b2c",
        "decision": "BLOCKED",
        "policy_status": "VIOLATION_DETECTED",
        "violations_count": 3,
        "violations_json": [
            {
                "policy_id": "EA-POL-001",
                "resource": "aws_cassandra_table.customer_audit_log",
                "severity": "CRITICAL",
                "title": "Unapproved / Deprecated Datastore Enforcement",
                "detail": "Resource provisions or binds to unapproved / legacy datastore (Cassandra 3.11.10), which is unapproved or past End-of-Life and classified as 'Eliminate' in Gartner TIME matrix. Approved alternative: Databricks Unity Catalog Delta Lake or managed PostgreSQL.",
                "remediation": "Replace `aws_cassandra_table` with `databricks_table` (catalog_name = 'ea', schema_name = 'silver', format = 'DELTA') or eliminate dependency on unapproved Cassandra cluster."
            },
            {
                "policy_id": "EA-POL-002",
                "resource": "aws_cassandra_table.customer_audit_log",
                "severity": "CRITICAL",
                "title": "Mandatory Customer PII Storage Encryption (GDPR Art. 32)",
                "detail": "Resource handles customer PII (ContainsPII = true) but has encryption disabled or missing (type = 'NONE'). Violates GDPR Article 32 and enterprise data protection standards.",
                "remediation": "Configure KMS Customer Managed Key encryption: `encryption_specification { type = 'CUSTOMER_MANAGED_KMS_KEY', kms_key_identifier = '...' }` or enable server-side KMS encryption."
            },
            {
                "policy_id": "EA-POL-003",
                "resource": "aws_cassandra_table.customer_audit_log",
                "severity": "HIGH",
                "title": "Mandatory Architectural Tagging (Ownership & Tier Criticality)",
                "detail": "Resource lacks mandatory enterprise architectural governance tags: OwnerTeam, Tier. Required for automatic catalog registration and ownership attribution.",
                "remediation": "Add required governance tags: `tags = { OwnerTeam = \"team-...\", Tier = \"Tier-1\" }`."
            }
        ],
        "evaluator": "subscription_cli",
        "resources_evaluated": 1,
        "diagram_delta_path": str(ROOT_DIR / "data" / "diagrams" / "diagram_delta.html"),
        "timestamp": "2026-10-16T12:00:00Z",
    },
    {
        "audit_id": "arb-pr-105-historical",
        "pr_id": "PR-105",
        "commit_hash": "9c43d1a",
        "decision": "APPROVED",
        "policy_status": "COMPLIANT",
        "violations_count": 0,
        "violations_json": [],
        "evaluator": "subscription_cli",
        "resources_evaluated": 1,
        "diagram_delta_path": str(ROOT_DIR / "data" / "diagrams" / "diagram_delta.html"),
        "timestamp": "2026-10-16T14:30:00Z",
    },
]


def seed_database() -> Dict[str, int]:
    """Seed the Unity Catalog conformed tables."""
    client = get_unity_catalog_client()
    n_count = client.merge_nodes(SEED_NODES)
    e_count = client.merge_edges(SEED_EDGES)
    t_count = client.save_time_matrix(SEED_TIME_MATRIX)
    d_count = client.save_drift_records(SEED_DRIFT)
    c_count = client.save_capability_realizations(SEED_CAPABILITY_REALIZATIONS)
    a_count = sum(1 for rec in SEED_ARB_AUDIT_LEDGER if client.record_arb_audit(rec))
    return {
        "nodes": n_count,
        "edges": e_count,
        "time_matrix": t_count,
        "drift": d_count,
        "capability_realizations": c_count,
        "arb_audit_ledger": a_count,
    }


if __name__ == "__main__":
    res = seed_database()
    print(f"✓ Seeded Databricks Unity Catalog conformed tables: {res}")


