"""
Enterprise Connector Manager.
Orchestrates enterprise connectors across GitHub, ServiceNow, Jira, and Backstage.
Provides parallel health checking, active service discovery, and unified bronze data synchronization.
"""
from __future__ import annotations

import concurrent.futures
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.connectors.backstage import BackstageConnector
from src.connectors.base import EnterpriseConnector
from src.connectors.github import GitHubConnector
from src.connectors.jira import JiraConnector
from src.connectors.servicenow import ServiceNowConnector

logger = logging.getLogger("agentic_ea.connectors.manager")


class ConnectorManager:
    """
    Unified manager orchestrating enterprise connectors for The Agentic EA Platform.
    """

    def __init__(
        self,
        github: Optional[GitHubConnector] = None,
        servicenow: Optional[ServiceNowConnector] = None,
        jira: Optional[JiraConnector] = None,
        backstage: Optional[BackstageConnector] = None,
    ):
        self.github = github or GitHubConnector()
        self.servicenow = servicenow or ServiceNowConnector()
        self.jira = jira or JiraConnector()
        self.backstage = backstage or BackstageConnector()

        self._connectors: Dict[str, EnterpriseConnector] = {
            "github": self.github,
            "servicenow": self.servicenow,
            "jira": self.jira,
            "backstage": self.backstage,
        }

    def get_connector(self, name: str) -> Optional[EnterpriseConnector]:
        """Returns the connector instance by name."""
        return self._connectors.get(name.lower())

    def test_all_connections(self, parallel: bool = True) -> Dict[str, Dict[str, Any]]:
        """
        Executes connection health checks across all registered enterprise connectors.
        Can run in parallel across a thread pool or sequentially.
        """
        results: Dict[str, Dict[str, Any]] = {}

        if parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self._connectors)) as executor:
                future_to_name = {
                    executor.submit(connector.test_connection): name
                    for name, connector in self._connectors.items()
                }
                for future in concurrent.futures.as_completed(future_to_name):
                    name = future_to_name[future]
                    try:
                        results[name] = future.result()
                    except Exception as e:
                        logger.error(f"Error testing connection for {name}: {e}")
                        results[name] = {
                            "connector": name.capitalize(),
                            "status": "UNREACHABLE",
                            "latency_ms": 0.0,
                            "details": {"error": str(e)},
                            "message": f"Health check failed with exception: {str(e)}",
                            "tested_at": datetime.now(timezone.utc).isoformat(),
                        }
        else:
            for name, connector in self._connectors.items():
                try:
                    results[name] = connector.test_connection()
                except Exception as e:
                    logger.error(f"Error testing connection for {name}: {e}")
                    results[name] = {
                        "connector": name.capitalize(),
                        "status": "UNREACHABLE",
                        "latency_ms": 0.0,
                        "details": {"error": str(e)},
                        "message": f"Health check failed with exception: {str(e)}",
                        "tested_at": datetime.now(timezone.utc).isoformat(),
                    }

        return results

    def get_active_connectors(self) -> List[str]:
        """
        Returns list of connectors that successfully established a live connection.
        """
        health_checks = self.test_all_connections(parallel=True)
        return [
            name
            for name, result in health_checks.items()
            if result.get("status") == "CONNECTED"
        ]

    def sync_all_to_bronze(self, client: Optional[Any] = None) -> Dict[str, Any]:
        """
        Synchronizes telemetry from active external systems into Bronze delta tables:
        - ServiceNow CMDB CIs -> ea.bronze.cmdb_ci
        - Backstage Catalog Entities -> PAM Metamodel Nodes (ea.metamodel.nodes)
        """
        if client is None:
            try:
                from src.data_backbone.client import get_unity_catalog_client
                client = get_unity_catalog_client()
            except Exception as e:
                logger.warning(f"Could not initialize UnityCatalogClient: {e}")
                client = None

        report: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "synced_connectors": [],
            "skipped_connectors": [],
            "records_ingested": {},
        }

        # 1. ServiceNow CMDB Sync
        sn_status = self.servicenow.test_connection()
        if sn_status.get("status") == "CONNECTED":
            try:
                cis = self.servicenow.fetch_ci_table("cmdb_ci", limit=100)
                conformed_cis = self.servicenow.sync_cmdb_cis_to_bronze_format(cis)
                count = 0
                if client and conformed_cis:
                    count = client.save_cmdb_ci(conformed_cis)
                report["synced_connectors"].append("servicenow")
                report["records_ingested"]["cmdb_ci"] = count or len(conformed_cis)
            except Exception as e:
                logger.error(f"Failed to sync ServiceNow CMDB CIs: {e}")
                report["skipped_connectors"].append({"connector": "servicenow", "reason": str(e)})
        else:
            report["skipped_connectors"].append({
                "connector": "servicenow",
                "reason": sn_status.get("message", "Not connected"),
            })

        # 2. Backstage Software Catalog Sync
        bs_status = self.backstage.test_connection()
        if bs_status.get("status") == "CONNECTED":
            try:
                entities = self.backstage.fetch_entities()
                pam_nodes = [self.backstage.convert_entity_to_pam_node(e) for e in entities]
                count = 0
                if client and pam_nodes:
                    count = client.merge_nodes(pam_nodes)
                report["synced_connectors"].append("backstage")
                report["records_ingested"]["pam_nodes_from_backstage"] = count or len(pam_nodes)
            except Exception as e:
                logger.error(f"Failed to sync Backstage entities: {e}")
                report["skipped_connectors"].append({"connector": "backstage", "reason": str(e)})
        else:
            report["skipped_connectors"].append({
                "connector": "backstage",
                "reason": bs_status.get("message", "Not connected"),
            })

        return report
