"""
Modular ServiceNow CMDB Ingestion Connector.
Ingests enterprise configuration items (Applications, Databases, Cloud Services)
from ServiceNow Table API into ea.bronze.cmdb_ci.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from src.data_backbone.client import get_unity_catalog_client


class ServiceNowCMDBIngestor:
    """Ingests configuration items (CIs) from ServiceNow CMDB."""

    def __init__(self, instance_url: str = "https://enterprise.service-now.com"):
        self.instance_url = instance_url
        self.client = get_unity_catalog_client()

    def generate_cmdb_records(self) -> List[Dict[str, Any]]:
        """Generate realistic ServiceNow CMDB records across applications, databases, and infrastructure."""
        now = datetime.now(timezone.utc).isoformat()
        raw_cis = [
            {
                "sys_id": "sys-ci-appl-web-storefront-001",
                "name": "web-storefront",
                "ci_class": "cmdb_ci_appl",
                "operational_status": "Operational",
                "environment": "Production",
                "tier": "Tier-1",
                "owner_team": "team-frontend",
                "ip_address": "10.0.1.25",
                "cloud_resource_id": "enterprise-edge-prod/web-storefront",
                "raw_attributes": {
                    "install_status": "1",
                    "category": "Customer Experience Application",
                    "short_description": "Next.js Storefront Web Application",
                    "support_group": "team-frontend",
                    "u_disposition": "Invest",
                },
                "synced_at": now,
            },
            {
                "sys_id": "sys-ci-appl-payments-api-002",
                "name": "payments-api",
                "ci_class": "cmdb_ci_appl",
                "operational_status": "Operational",
                "environment": "Production",
                "tier": "Tier-0",
                "owner_team": "team-payments",
                "ip_address": "10.0.2.14",
                "cloud_resource_id": "arn:aws:eks:us-east-1:112233445566:fargate/payments-api",
                "raw_attributes": {
                    "install_status": "1",
                    "category": "Core Payment Processing Microservice",
                    "short_description": "Go Gin Payment Gateway API",
                    "support_group": "team-payments",
                    "u_pci_dss_scope": "true",
                },
                "synced_at": now,
            },
            {
                "sys_id": "sys-ci-db-billing-rds-003",
                "name": "billing-db",
                "ci_class": "cmdb_ci_database",
                "operational_status": "Operational",
                "environment": "Production",
                "tier": "Tier-0",
                "owner_team": "team-data-platform",
                "ip_address": "10.0.5.40",
                "cloud_resource_id": "arn:aws:rds:us-east-1:112233445566:db:billing-db-rds",
                "raw_attributes": {
                    "install_status": "1",
                    "database_type": "PostgreSQL 16",
                    "support_group": "team-data-platform",
                    "u_contains_pii": "true",
                    "u_kms_encrypted": "true",
                },
                "synced_at": now,
            },
            {
                # Attribute Drift: Tier-3 vs Git Tier-1, Staging vs Git Production, team-growth vs team-checkout
                "sys_id": "sys-ci-appl-checkout-service-004",
                "name": "checkout-service",
                "ci_class": "cmdb_ci_appl",
                "operational_status": "Operational",
                "environment": "Staging",
                "tier": "Tier-3",
                "owner_team": "team-growth",
                "ip_address": "10.0.3.18",
                "cloud_resource_id": "arn:aws:eks:us-east-1:112233445566:fargate/checkout-service",
                "raw_attributes": {
                    "install_status": "1",
                    "category": "Order Processing",
                    "short_description": "Java Spring Boot Checkout Service",
                    "support_group": "team-growth",
                    "u_drift_flag": "outdated_metadata",
                },
                "synced_at": now,
            },
            {
                # Lifecycle Drift: Marked Operational in CMDB, but Eliminate/phase-out in EA portfolio
                "sys_id": "sys-ci-db-cassandra-legacy-005",
                "name": "cassandra-legacy-cluster",
                "ci_class": "cmdb_ci_database",
                "operational_status": "Operational",
                "environment": "Production",
                "tier": "Tier-2",
                "owner_team": "team-legacy-ops",
                "ip_address": "10.0.8.100",
                "cloud_resource_id": "arn:aws:ec2:us-east-1:112233445566:instance/i-cassandra-legacy-node",
                "raw_attributes": {
                    "install_status": "1",
                    "database_type": "Cassandra 3.11",
                    "support_group": "team-legacy-ops",
                    "u_eol_status": "Active",
                },
                "synced_at": now,
            },
            {
                # Orphan CI: Registered in CMDB as Operational, but completely absent / terminated in cloud & Git
                "sys_id": "sys-ci-orphan-recs-ai-006",
                "name": "recommendations-ai-legacy",
                "ci_class": "cmdb_ci_appl",
                "operational_status": "Operational",
                "environment": "Production",
                "tier": "Tier-2",
                "owner_team": "team-recs",
                "ip_address": "10.0.9.15",
                "cloud_resource_id": "i-0987654321fedcba0",
                "raw_attributes": {
                    "install_status": "1",
                    "category": "Machine Learning Service",
                    "short_description": "Legacy Python Recommender - Terminated instance",
                    "support_group": "team-recs",
                },
                "synced_at": now,
            },
            {
                # Orphan CI: Registered in CMDB as Operational, but decommissioned in infrastructure
                "sys_id": "sys-ci-orphan-es-logging-007",
                "name": "elastic-search-v6-logging",
                "ci_class": "cmdb_ci_database",
                "operational_status": "Operational",
                "environment": "Production",
                "tier": "Tier-3",
                "owner_team": "team-logging",
                "ip_address": "10.0.9.88",
                "cloud_resource_id": "arn:aws:es:us-east-1:112233445566:domain/es-v6-logs",
                "raw_attributes": {
                    "install_status": "1",
                    "database_type": "Elasticsearch 6.8",
                    "support_group": "team-logging",
                },
                "synced_at": now,
            },
        ]
        return raw_cis

    def ingest(self, json_file: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Ingest ServiceNow CMDB CIs and persist to ea.bronze.cmdb_ci."""
        if json_file and json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                records = json.load(f)
        else:
            records = self.generate_cmdb_records()

        count = self.client.save_cmdb_ci(records)
        return records


def main():
    parser = argparse.ArgumentParser(description="Ingest ServiceNow CMDB Configuration Items into Unity Catalog Bronze")
    parser.add_argument("--file", help="Path to JSON CMDB export file")
    args = parser.parse_args()

    ingestor = ServiceNowCMDBIngestor()
    records = ingestor.ingest(Path(args.file) if args.file else None)
    print(f"✓ Ingested {len(records)} configuration items into ea.bronze.cmdb_ci:")
    for r in records:
        print(f"  • [{r['ci_class']}] {r['name']} (sys_id: {r['sys_id']}, env: {r['environment']}, tier: {r['tier']}, status: {r['operational_status']})")


if __name__ == "__main__":
    main()
