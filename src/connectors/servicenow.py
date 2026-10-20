"""
Enterprise ServiceNow CMDB & ITSM Connector.
Integrates with ServiceNow Table API for CMDB baseline synchronization,
configuration item discovery, and architectural change request generation.
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from src.connectors.base import EnterpriseConnector, resolve_secret

logger = logging.getLogger("agentic_ea.connectors.servicenow")


class ServiceNowConnector(EnterpriseConnector):
    """
    Production connector for ServiceNow ITSM and CMDB Table APIs.
    Supports basic auth and OAuth Bearer tokens, CI table querying, and Change Request automation.
    """

    def __init__(
        self,
        instance: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 15,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        raw_instance = instance or resolve_secret("SERVICENOW_INSTANCE")
        base_url = ""
        if raw_instance:
            if raw_instance.startswith("http://") or raw_instance.startswith("https://"):
                base_url = raw_instance.rstrip("/")
            else:
                base_url = f"https://{raw_instance}.service-now.com"

        super().__init__(
            name="ServiceNow",
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

        self.instance = raw_instance
        self.username = username or resolve_secret("SERVICENOW_USER")
        self.password = password or resolve_secret("SERVICENOW_PASSWORD")
        self.token = token or resolve_secret("SERVICENOW_TOKEN")

        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

        if self.token:
            self.session.headers["Authorization"] = f"Bearer {self.token}"
        elif self.username and self.password:
            self.session.auth = (self.username, self.password)

    def test_connection(self) -> Dict[str, Any]:
        """
        Tests ServiceNow Table API connectivity by querying the CMDB CI table with limit=1.
        """
        if not self.base_url or (not self.token and not (self.username and self.password)):
            return self._format_result(
                status="UNCONFIGURED",
                latency_ms=0.0,
                details={"error": "Missing ServiceNow instance or credentials"},
                message="ServiceNow not configured. Set SERVICENOW_INSTANCE and credentials (SERVICENOW_TOKEN or USER/PASSWORD).",
            )

        start = time.perf_counter()
        try:
            resp = self._request("GET", "/api/now/table/cmdb_ci", params={"sysparm_limit": 1})
            latency_ms = (time.perf_counter() - start) * 1000

            if resp.status_code == 200:
                data = resp.json()
                results = data.get("result", [])
                details = {
                    "instance": self.base_url,
                    "sample_records_returned": len(results),
                    "auth_mode": "bearer" if self.token else "basic",
                }
                return self._format_result(
                    status="CONNECTED",
                    latency_ms=latency_ms,
                    details=details,
                    message=f"Successfully connected to ServiceNow instance at '{self.base_url}'.",
                )
            elif resp.status_code in (401, 403):
                return self._format_result(
                    status="AUTH_ERROR",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message="ServiceNow authentication failed: invalid username/password or token.",
                )
            else:
                return self._format_result(
                    status="UNREACHABLE",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message=f"ServiceNow API returned unexpected HTTP status {resp.status_code}.",
                )
        except requests.RequestException as e:
            latency_ms = (time.perf_counter() - start) * 1000
            return self._format_result(
                status="UNREACHABLE",
                latency_ms=latency_ms,
                details={"error": str(e)},
                message=f"ServiceNow instance unreachable: {str(e)}",
            )

    def fetch_ci_table(
        self,
        table_name: str = "cmdb_ci",
        query: str = "",
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Fetches Configuration Items from a given ServiceNow CMDB table (e.g. cmdb_ci, cmdb_ci_appl, cmdb_ci_database).
        """
        endpoint = f"/api/now/table/{table_name}"
        params: Dict[str, Any] = {"sysparm_limit": limit, "sysparm_offset": offset}
        if query:
            params["sysparm_query"] = query

        resp = self._request("GET", endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", []) if isinstance(data, dict) else []

    def create_change_request(
        self,
        short_description: str,
        description: str,
        risk: str = "Moderate",
        category: str = "Architecture Modernization",
        assignment_group: Optional[str] = None,
        additional_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Creates an ITSM Change Request ticket for architecture migrations, drift remediations, or decommissions.
        """
        payload: Dict[str, Any] = {
            "short_description": short_description,
            "description": description,
            "risk": risk,
            "category": category,
        }
        if assignment_group:
            payload["assignment_group"] = assignment_group
        if additional_fields:
            payload.update(additional_fields)

        resp = self._request("POST", "/api/now/table/change_request", json_data=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", {}) if isinstance(data, dict) else {}

    def update_ci(
        self,
        table_name: str,
        sys_id: str,
        fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Updates an existing Configuration Item in the ServiceNow CMDB.
        """
        endpoint = f"/api/now/table/{table_name}/{sys_id}"
        resp = self._request("PATCH", endpoint, json_data=fields)
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", {}) if isinstance(data, dict) else {}

    def sync_cmdb_cis_to_bronze_format(
        self,
        raw_cis: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Transforms raw ServiceNow Table API records into conformed ea.bronze.cmdb_ci rows.
        """
        conformed_rows = []
        now_ts = datetime.now(timezone.utc).isoformat()

        for ci in raw_cis:
            conformed = {
                "sys_id": str(ci.get("sys_id", "")),
                "name": str(ci.get("name") or ci.get("sys_name") or "unknown-ci"),
                "ci_class": str(ci.get("sys_class_name") or ci.get("ci_class") or "cmdb_ci"),
                "operational_status": str(ci.get("operational_status") or "Operational"),
                "environment": str(ci.get("environment") or "Production"),
                "tier": str(ci.get("business_criticality") or ci.get("tier") or "Tier-2"),
                "owner_team": str(ci.get("support_group") or ci.get("owner_team") or "Enterprise Architecture"),
                "ip_address": ci.get("ip_address"),
                "cloud_resource_id": ci.get("correlation_id") or ci.get("asset_tag"),
                "raw_attributes": json.dumps(ci),
                "synced_at": now_ts,
            }
            conformed_rows.append(conformed)

        return conformed_rows
