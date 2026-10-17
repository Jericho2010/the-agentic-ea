"""
Modular Process Event Telemetry Ingestion Connector.
Ingests distributed trace execution spans into ea.bronze.process_event_logs for process mining
and customer journey latency attribution.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from src.data_backbone.client import get_unity_catalog_client


class ProcessEventLogIngestor:
    """Ingests distributed trace spans into ea.bronze.process_event_logs."""

    def __init__(self, process_id: str = "PROC-ORDER-TO-CASH"):
        self.process_id = process_id
        self.client = get_unity_catalog_client()

    def generate_trace_spans(self) -> List[Dict[str, Any]]:
        """Generate canonical trace spans for the Order-to-Cash customer journey across distributed traces."""
        now = datetime.now(timezone.utc).isoformat()
        spans: List[Dict[str, Any]] = [
            # Trace 1
            {
                "trace_id": "TRC-2026-OTC-001",
                "process_id": self.process_id,
                "step_id": "STEP-01",
                "step_name": "Cart Checkout Submission",
                "service_urn": "urn:ea:application:web-storefront",
                "duration_ms": 118.4,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-001",
                "process_id": self.process_id,
                "step_id": "STEP-02",
                "step_name": "Customer Profile & Loyalty Lookup",
                "service_urn": "urn:ea:database:cassandra-legacy-cluster",
                "duration_ms": 878.6,
                "status": "SLA_BREACH",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-001",
                "process_id": self.process_id,
                "step_id": "STEP-03",
                "step_name": "Payment Authorization & Fraud Scoring",
                "service_urn": "urn:ea:microservice:payments-service",
                "duration_ms": 308.2,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-001",
                "process_id": self.process_id,
                "step_id": "STEP-04",
                "step_name": "Ledger Posting & Invoice Generation",
                "service_urn": "urn:ea:database:billing-db",
                "duration_ms": 139.1,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-001",
                "process_id": self.process_id,
                "step_id": "STEP-05",
                "step_name": "Audit & Event Ingestion",
                "service_urn": "urn:ea:cloudresource:customer-pii-stream",
                "duration_ms": 44.8,
                "status": "SUCCESS",
                "timestamp": now,
            },
            # Trace 2
            {
                "trace_id": "TRC-2026-OTC-002",
                "process_id": self.process_id,
                "step_id": "STEP-01",
                "step_name": "Cart Checkout Submission",
                "service_urn": "urn:ea:application:web-storefront",
                "duration_ms": 122.1,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-002",
                "process_id": self.process_id,
                "step_id": "STEP-02",
                "step_name": "Customer Profile & Loyalty Lookup",
                "service_urn": "urn:ea:database:cassandra-legacy-cluster",
                "duration_ms": 884.2,
                "status": "SLA_BREACH",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-002",
                "process_id": self.process_id,
                "step_id": "STEP-03",
                "step_name": "Payment Authorization & Fraud Scoring",
                "service_urn": "urn:ea:microservice:payments-service",
                "duration_ms": 312.0,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-002",
                "process_id": self.process_id,
                "step_id": "STEP-04",
                "step_name": "Ledger Posting & Invoice Generation",
                "service_urn": "urn:ea:database:billing-db",
                "duration_ms": 141.5,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-002",
                "process_id": self.process_id,
                "step_id": "STEP-05",
                "step_name": "Audit & Event Ingestion",
                "service_urn": "urn:ea:cloudresource:customer-pii-stream",
                "duration_ms": 45.2,
                "status": "SUCCESS",
                "timestamp": now,
            },
            # Trace 3
            {
                "trace_id": "TRC-2026-OTC-003",
                "process_id": self.process_id,
                "step_id": "STEP-01",
                "step_name": "Cart Checkout Submission",
                "service_urn": "urn:ea:application:web-storefront",
                "duration_ms": 119.5,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-003",
                "process_id": self.process_id,
                "step_id": "STEP-02",
                "step_name": "Customer Profile & Loyalty Lookup",
                "service_urn": "urn:ea:database:cassandra-legacy-cluster",
                "duration_ms": 879.3,
                "status": "SLA_BREACH",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-003",
                "process_id": self.process_id,
                "step_id": "STEP-03",
                "step_name": "Payment Authorization & Fraud Scoring",
                "service_urn": "urn:ea:microservice:payments-service",
                "duration_ms": 309.8,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-003",
                "process_id": self.process_id,
                "step_id": "STEP-04",
                "step_name": "Ledger Posting & Invoice Generation",
                "service_urn": "urn:ea:database:billing-db",
                "duration_ms": 138.9,
                "status": "SUCCESS",
                "timestamp": now,
            },
            {
                "trace_id": "TRC-2026-OTC-003",
                "process_id": self.process_id,
                "step_id": "STEP-05",
                "step_name": "Audit & Event Ingestion",
                "service_urn": "urn:ea:cloudresource:customer-pii-stream",
                "duration_ms": 44.1,
                "status": "SUCCESS",
                "timestamp": now,
            },
        ]
        return spans

    def run_ingestion(self) -> int:
        """Execute ingestion of process event telemetry into Unity Catalog client."""
        spans = self.generate_trace_spans()
        saved = self.client.save_process_event_logs(spans)
        return saved


def main():
    parser = argparse.ArgumentParser(description="Process Event Log Ingestion Connector")
    parser.add_argument("--dry-run", action="store_true", help="Print trace spans without inserting")
    args = parser.parse_args()

    ingestor = ProcessEventLogIngestor()
    spans = ingestor.generate_trace_spans()

    if args.dry_run:
        print(f"Generated {len(spans)} process event trace spans:")
        print(json.dumps(spans, indent=2))
    else:
        saved = ingestor.run_ingestion()
        print(f"✓ Ingested {saved} process execution trace spans into ea.bronze.process_event_logs")


if __name__ == "__main__":
    main()
