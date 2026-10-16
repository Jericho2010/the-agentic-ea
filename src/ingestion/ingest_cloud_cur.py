"""
Modular Cloud Cost and Usage Report (CUR) Ingestion Connector.
Ingests cloud infrastructure, telemetry, and billing records into ea.bronze.cloud_resources.
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


class CloudCURIngestor:
    """Ingests cloud billing line-items and cloud provider asset telemetry."""

    def __init__(self, provider: str = "AWS"):
        self.provider = provider
        self.client = get_unity_catalog_client()

    def generate_cur_records(self) -> List[Dict[str, Any]]:
        """Generate realistic FinOps CUR and resource telemetry records."""
        raw_resources = [
            {
                "name": "payments-api-compute",
                "provider": "AWS",
                "account_id": "112233445566",
                "region": "us-east-1",
                "resource_type": "AWS::EKS::FargateProfile",
                "monthly_cost": 6000.0,
                "tags": {
                    "System": "payments-api",
                    "Tier": "Tier-0",
                    "OwnerTeam": "team-payments",
                    "Environment": "production",
                },
            },
            {
                "name": "billing-db-rds",
                "provider": "AWS",
                "account_id": "112233445566",
                "region": "us-east-1",
                "resource_type": "AWS::RDS::DBInstance",
                "monthly_cost": 4583.33,
                "tags": {
                    "System": "billing-db",
                    "Tier": "Tier-0",
                    "OwnerTeam": "team-data-platform",
                    "ContainsPII": "true",
                    "Encrypted": "true",
                    "KMSKeyId": "arn:aws:kms:us-east-1:112233445566:key/billing-cmk",
                },
            },
            {
                "name": "checkout-service-compute",
                "provider": "AWS",
                "account_id": "112233445566",
                "region": "us-east-1",
                "resource_type": "AWS::EKS::FargateProfile",
                "monthly_cost": 4000.0,
                "tags": {
                    "System": "checkout-service",
                    "Tier": "Tier-1",
                    "OwnerTeam": "team-checkout",
                    "Environment": "production",
                },
            },
            {
                "name": "web-storefront-hosting",
                "provider": "Cloudflare/Vercel",
                "account_id": "enterprise-edge-prod",
                "region": "global",
                "resource_type": "Edge::CDN::NextJS",
                "monthly_cost": 2916.66,
                "tags": {
                    "System": "web-storefront",
                    "Tier": "Tier-1",
                    "OwnerTeam": "team-frontend",
                    "Domain": "store.enterprise.com",
                },
            },
            {
                "name": "auth-service-legacy",
                "provider": "AWS",
                "account_id": "112233445566",
                "region": "us-east-1",
                "resource_type": "AWS::ECS::Service",
                "monthly_cost": 2083.33,
                "tags": {
                    "System": "auth-service",
                    "Tier": "Tier-0",
                    "OwnerTeam": "team-auth",
                    "Disposition": "Tolerate",
                },
            },
            {
                "name": "customer-pii-kinesis",
                "provider": "AWS",
                "account_id": "112233445566",
                "region": "us-east-1",
                "resource_type": "AWS::Kinesis::Stream",
                "monthly_cost": 650.0,
                "tags": {
                    "System": "customer-pii-stream",
                    "Tier": "Tier-1",
                    "OwnerTeam": "team-data-platform",
                    "ContainsPII": "true",
                    "Encrypted": "true",
                },
            },
            {
                "name": "cassandra-legacy-nodes",
                "provider": "AWS",
                "account_id": "112233445566",
                "region": "us-east-1",
                "resource_type": "AWS::EC2::Instance",
                "monthly_cost": 5416.66,
                "tags": {
                    "System": "cassandra-legacy-cluster",
                    "Tier": "Tier-2",
                    "OwnerTeam": "team-legacy-ops",
                    "Disposition": "Eliminate",
                    "Encrypted": "false",
                },
            },
        ]

        records = []
        for r in raw_resources:
            res_id = hashlib.sha256(f"{r['provider']}/{r['account_id']}/{r['name']}".encode()).hexdigest()[:16]
            records.append({
                "resource_id": res_id,
                "resource_name": r["name"],
                "provider": r["provider"],
                "account_id": r["account_id"],
                "region": r["region"],
                "resource_type": r["resource_type"],
                "tags": r["tags"],
                "monthly_cost_usd": r["monthly_cost"],
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            })

        return records

    def ingest(self, cur_file: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Ingest cloud resources and write to ea.bronze.cloud_resources."""
        if cur_file and cur_file.exists():
            with open(cur_file, "r", encoding="utf-8") as f:
                records = json.load(f)
        else:
            records = self.generate_cur_records()

        self.client.insert_bronze_records("cloud_resources", records)
        return records


def main():
    parser = argparse.ArgumentParser(description="Ingest Cloud CUR Billing & Telemetry into Unity Catalog Bronze")
    parser.add_argument("--cur-file", help="Path to JSON CUR file")
    args = parser.parse_args()

    ingestor = CloudCURIngestor()
    records = ingestor.ingest(Path(args.cur_file) if args.cur_file else None)
    total_monthly = sum(r["monthly_cost_usd"] for r in records)
    print(f"✓ Ingested {len(records)} cloud resources into ea.bronze.cloud_resources:")
    print(f"  • Total Monthly Cloud Run Cost: ${total_monthly:,.2f}/mo (Annualized: ${total_monthly * 12:,.2f}/yr)")
    for r in records:
        print(f"  - [{r['provider']}] {r['resource_name']} ({r['resource_type']}) -> ${r['monthly_cost_usd']:,.2f}/mo")


if __name__ == "__main__":
    main()
