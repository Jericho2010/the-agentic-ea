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


def seed_database() -> Dict[str, int]:
    """Seed the Unity Catalog conformed tables."""
    client = get_unity_catalog_client()
    n_count = client.merge_nodes(SEED_NODES)
    e_count = client.merge_edges(SEED_EDGES)
    t_count = client.save_time_matrix(SEED_TIME_MATRIX)
    d_count = client.save_drift_records(SEED_DRIFT)
    return {
        "nodes": n_count,
        "edges": e_count,
        "time_matrix": t_count,
        "drift": d_count,
    }


if __name__ == "__main__":
    res = seed_database()
    print(f"✓ Seeded Databricks Unity Catalog conformed tables: {res}")
