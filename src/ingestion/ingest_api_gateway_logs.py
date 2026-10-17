"""
Modular API Gateway Traffic Log Ingestion Connector.
Ingests runtime API gateway access and invocation logs into ea.bronze.api_gateway_logs.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from src.data_backbone.client import get_unity_catalog_client


class APIGatewayLogIngestor:
    """Ingests API Gateway access and runtime traffic logs."""

    def __init__(self, gateway_name: str = "kong-enterprise-ingress"):
        self.gateway_name = gateway_name
        self.client = get_unity_catalog_client()

    def generate_gateway_records(self) -> List[Dict[str, Any]]:
        """Generate realistic API Gateway runtime traffic logs across microservices."""
        now = datetime.now(timezone.utc).isoformat()
        logs = [
            {
                "log_id": "LOG-001-CHECKOUT-API",
                "endpoint": "/api/v1/checkout",
                "method": "POST",
                "protocol": "HTTPS/REST",
                "auth_mechanism": "OAuth2",
                "consumer_service": "web-storefront",
                "provider_service": "checkout-service",
                "requests_last_30d": 1450000,
                "avg_latency_ms": 42.5,
                "error_rate": 0.002,
                "last_seen_timestamp": now,
            },
            {
                "log_id": "LOG-002-PAYMENTS-AUTHORIZE",
                "endpoint": "/v1/payments/authorize",
                "method": "POST",
                "protocol": "HTTPS/REST",
                "auth_mechanism": "mTLS",
                "consumer_service": "checkout-service",
                "provider_service": "payments-api",
                "requests_last_30d": 980000,
                "avg_latency_ms": 18.2,
                "error_rate": 0.001,
                "last_seen_timestamp": now,
            },
            {
                "log_id": "LOG-003-PAYMENTS-LEDGER-SYNC",
                "endpoint": "/rpc/payments.v1.LedgerSync/Record",
                "method": "RPC",
                "protocol": "gRPC/mTLS",
                "auth_mechanism": "mTLS",
                "consumer_service": "payments-api",
                "provider_service": "payments-service",
                "requests_last_30d": 850000,
                "avg_latency_ms": 8.4,
                "error_rate": 0.0005,
                "last_seen_timestamp": now,
            },
            {
                "log_id": "LOG-004-ZOMBIE-DEBUG-DUMP",
                "endpoint": "/v1/internal/debug-dump",
                "method": "GET",
                "protocol": "HTTP/JSON",
                "auth_mechanism": "None",
                "consumer_service": "external-scanner",
                "provider_service": "payments-api",
                "requests_last_30d": 14200,
                "avg_latency_ms": 120.0,
                "error_rate": 0.045,
                "last_seen_timestamp": now,
            },
            {
                "log_id": "LOG-005-SPRAWL-SOAP-CUSTOMER",
                "endpoint": "/soap/v1/customer",
                "method": "POST",
                "protocol": "SOAP/XML",
                "auth_mechanism": "HTTP-Basic",
                "consumer_service": "legacy-crm",
                "provider_service": "payments-service",
                "requests_last_30d": 52000,
                "avg_latency_ms": 210.0,
                "error_rate": 0.012,
                "last_seen_timestamp": now,
            },
            {
                "log_id": "LOG-006-PAYMENTS-STRIPE",
                "endpoint": "/v1/charges",
                "method": "POST",
                "protocol": "HTTPS/REST",
                "auth_mechanism": "BearerToken",
                "consumer_service": "payments-api",
                "provider_service": "stripe-gateway",
                "requests_last_30d": 420000,
                "avg_latency_ms": 95.0,
                "error_rate": 0.003,
                "last_seen_timestamp": now,
            },
            {
                "log_id": "LOG-007-AUTH-VERIFY",
                "endpoint": "/v1/auth/verify",
                "method": "POST",
                "protocol": "HTTPS/REST",
                "auth_mechanism": "mTLS",
                "consumer_service": "checkout-service",
                "provider_service": "auth-service",
                "requests_last_30d": 1200000,
                "avg_latency_ms": 12.1,
                "error_rate": 0.0008,
                "last_seen_timestamp": now,
            },
        ]
        return logs

    def ingest(self, logs: Optional[List[Dict[str, Any]]] = None) -> Dict[str, int]:
        """Ingest API gateway logs into ea.bronze.api_gateway_logs."""
        if logs is None:
            logs = self.generate_gateway_records()
        count = self.client.save_api_gateway_logs(logs)
        return {"bronze_api_gateway_logs": count}


def main():
    parser = argparse.ArgumentParser(description="Ingest API Gateway Logs")
    parser.add_argument("--gateway", default="kong-enterprise-ingress", help="Gateway identifier")
    args = parser.parse_args()

    ingestor = APIGatewayLogIngestor(gateway_name=args.gateway)
    res = ingestor.ingest()
    print(f"✓ Ingested API gateway traffic logs: {res}")


if __name__ == "__main__":
    main()
