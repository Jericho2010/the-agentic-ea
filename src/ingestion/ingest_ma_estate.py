"""
M&A Day-One Zero-Footprint IT Landscape Ingestor.
Simulates rapid tenant/organization discovery of an acquired target entity's IT estate:
- Ingests git repositories into ea.bronze.git_repos (org: acquired-target-org)
- Ingests cloud CUR resource lines into ea.bronze.cloud_resources (account: 998877665544)
- Conforms acquired assets into PAM graph (urn:ea:acquired:*) with capability mappings
- Computes and populates initial M&A synergy rationalization ledger (ea.gold.ma_synergies)
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
from src.data_backbone.seed import SEED_MA_EDGES, SEED_MA_NODES, SEED_MA_SYNERGIES


class MAEstateIngestor:
    """Ingests acquired entity repositories, cloud footprints, and conformed PAM nodes."""

    def __init__(self, org_name: str = "acquired-target-org", account_id: str = "998877665544"):
        self.org_name = org_name
        self.account_id = account_id
        self.client = get_unity_catalog_client()

    def generate_bronze_git_repos(self) -> List[Dict[str, Any]]:
        """Generate discovered git repositories for acquired organization."""
        repos = [
            {
                "name": "acquired-payment-gateway",
                "languages": ["PHP", "Hack"],
                "manifest_files": ["composer.json", "artisan"],
                "ast_nodes": [
                    {
                        "urn": "urn:ea:acquired:microservice:acquired-payment-gateway",
                        "name": "acquired-payment-gateway",
                        "kind": "Microservice",
                        "owner_team": "acq-payments-team",
                        "criticality": "Tier-1",
                        "metadata": {
                            "framework": "Laravel 10",
                            "php_version": "8.1",
                            "tenant_id": "acq-target-corp",
                        },
                    }
                ],
                "edges": [
                    {
                        "source_urn": "urn:ea:acquired:microservice:acquired-payment-gateway",
                        "target_urn": "urn:ea:acquired:database:acquired-crm-db",
                        "relation": "connects_to",
                        "protocol": "TCP/3306",
                        "contains_pii": True,
                    }
                ],
            },
            {
                "name": "acquired-auth-portal",
                "languages": ["JavaScript", "Node.js"],
                "manifest_files": ["package.json", "server.js"],
                "ast_nodes": [
                    {
                        "urn": "urn:ea:acquired:microservice:acquired-auth-portal",
                        "name": "acquired-auth-portal",
                        "kind": "Microservice",
                        "owner_team": "acq-security-team",
                        "criticality": "Tier-1",
                        "metadata": {
                            "runtime": "Node.js 16 Express",
                            "tenant_id": "acq-target-corp",
                        },
                    }
                ],
                "edges": [],
            },
        ]

        records = []
        for r in repos:
            repo_id = hashlib.sha256(f"{self.org_name}/{r['name']}".encode()).hexdigest()[:16]
            records.append({
                "repo_id": repo_id,
                "repo_name": r["name"],
                "org_name": self.org_name,
                "default_branch": "main",
                "languages": r["languages"],
                "manifest_files": r["manifest_files"],
                "ast_nodes": r["ast_nodes"],
                "discovered_edges": r["edges"],
                "extracted_at": datetime.now(timezone.utc).isoformat(),
            })
        return records

    def generate_bronze_cloud_resources(self) -> List[Dict[str, Any]]:
        """Generate discovered AWS CUR infrastructure records for acquired entity."""
        return [
            {
                "resource_id": f"arn:aws:ecs:us-east-1:{self.account_id}:service/acquired-payment-gateway",
                "resource_name": "acquired-payment-gateway",
                "provider": "AWS",
                "account_id": self.account_id,
                "region": "us-east-1",
                "resource_type": "AWS::ECS::Service",
                "tags": {
                    "Environment": "Production",
                    "Owner": "acq-payments-team",
                    "Tier": "Tier-1",
                    "Tenant": "acq-target-corp",
                    "Application": "acquired-payment-gateway",
                },
                "monthly_cost_usd": 3500.00,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "resource_id": f"arn:aws:ecs:us-east-1:{self.account_id}:service/acquired-auth-portal",
                "resource_name": "acquired-auth-portal",
                "provider": "AWS",
                "account_id": self.account_id,
                "region": "us-east-1",
                "resource_type": "AWS::ECS::Service",
                "tags": {
                    "Environment": "Production",
                    "Owner": "acq-security-team",
                    "Tier": "Tier-1",
                    "Tenant": "acq-target-corp",
                    "Application": "acquired-auth-portal",
                },
                "monthly_cost_usd": 1500.00,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "resource_id": f"arn:aws:ec2:us-east-1:{self.account_id}:instance/acquired-crm-db",
                "resource_name": "acquired-crm-db",
                "provider": "AWS",
                "account_id": self.account_id,
                "region": "us-east-1",
                "resource_type": "AWS::EC2::Instance",
                "tags": {
                    "Environment": "Production",
                    "Owner": "acq-data-team",
                    "Tier": "Tier-1",
                    "Tenant": "acq-target-corp",
                    "Database": "MySQL-5.7",
                },
                "monthly_cost_usd": 2333.33,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "resource_id": f"arn:aws:redshift:us-east-1:{self.account_id}:cluster/acquired-analytics-pipeline",
                "resource_name": "acquired-analytics-pipeline",
                "provider": "AWS",
                "account_id": self.account_id,
                "region": "us-east-1",
                "resource_type": "AWS::Redshift::Cluster",
                "tags": {
                    "Environment": "Production",
                    "Owner": "acq-bi-team",
                    "Tier": "Tier-2",
                    "Tenant": "acq-target-corp",
                },
                "monthly_cost_usd": 3000.00,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            },
        ]

    def ingest(self) -> Dict[str, int]:
        """Execute full Day-One discovery ingestion into Bronze and Gold marts."""
        git_records = self.generate_bronze_git_repos()
        cloud_records = self.generate_bronze_cloud_resources()

        n_git = self.client.insert_bronze_records("git_repos", git_records)
        n_cloud = self.client.insert_bronze_records("cloud_resources", cloud_records)

        # Merge acquired metamodel nodes & edges into graph
        n_nodes = self.client.merge_nodes(SEED_MA_NODES)
        n_edges = self.client.merge_edges(SEED_MA_EDGES)

        # Populate synergies
        n_synergies = self.client.save_ma_synergies(SEED_MA_SYNERGIES)

        return {
            "bronze_git_repos": n_git,
            "bronze_cloud_resources": n_cloud,
            "metamodel_nodes": n_nodes,
            "metamodel_edges": n_edges,
            "gold_ma_synergies": n_synergies,
        }


def main():
    parser = argparse.ArgumentParser(description="Ingest acquired IT estate for M&A Day-One discovery")
    parser.add_argument("--org", default="acquired-target-org", help="Acquired GitHub organization")
    parser.add_argument("--account", default="998877665544", help="Acquired Cloud account ID")
    args = parser.parse_args()

    ingestor = MAEstateIngestor(org_name=args.org, account_id=args.account)
    stats = ingestor.ingest()
    print(f"✓ Ingested M&A IT Landscape into Databricks Unity Catalog: {stats}")


if __name__ == "__main__":
    main()
