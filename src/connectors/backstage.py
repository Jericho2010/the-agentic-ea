"""
Enterprise Spotify Backstage Developer Portal & Service Catalog Connector.
Integrates with Backstage Catalog API for bi-directional PAM metamodel synchronization,
software catalog ingestion, catalog-info.yaml generation, and TechDocs publishing.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

import requests

from src.connectors.base import EnterpriseConnector, resolve_secret

logger = logging.getLogger("agentic_ea.connectors.backstage")


class BackstageConnector(EnterpriseConnector):
    """
    Production connector for Spotify Backstage Software Catalog & TechDocs APIs.
    Enables bidirectional translation between Backstage Catalog Entities and PAM Metamodel nodes.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 15,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        resolved_url = base_url or resolve_secret("BACKSTAGE_URL") or ""
        super().__init__(
            name="Backstage",
            base_url=resolved_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

        self.token = token or resolve_secret("BACKSTAGE_TOKEN")
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

        if self.token:
            self.session.headers["Authorization"] = f"Bearer {self.token}"

    def test_connection(self) -> Dict[str, Any]:
        """
        Tests Backstage Catalog connectivity by querying entities with limit=1.
        """
        if not self.base_url:
            return self._format_result(
                status="UNCONFIGURED",
                latency_ms=0.0,
                details={"error": "Missing Backstage URL"},
                message="Backstage not configured. Set BACKSTAGE_URL (e.g. http://localhost:7007).",
            )

        start = time.perf_counter()
        try:
            resp = self._request("GET", "/api/catalog/entities", params={"limit": 1})
            latency_ms = (time.perf_counter() - start) * 1000

            if resp.status_code == 200:
                data = resp.json()
                count = len(data) if isinstance(data, list) else 0
                details = {
                    "base_url": self.base_url,
                    "catalog_accessible": True,
                    "sample_entities_count": count,
                }
                return self._format_result(
                    status="CONNECTED",
                    latency_ms=latency_ms,
                    details=details,
                    message=f"Successfully connected to Backstage Catalog at '{self.base_url}'.",
                )
            elif resp.status_code in (401, 403):
                return self._format_result(
                    status="AUTH_ERROR",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message="Backstage authentication failed: invalid token or forbidden access.",
                )
            else:
                return self._format_result(
                    status="UNREACHABLE",
                    latency_ms=latency_ms,
                    details={"status_code": resp.status_code, "error": resp.text},
                    message=f"Backstage API returned unexpected HTTP status {resp.status_code}.",
                )
        except requests.RequestException as e:
            latency_ms = (time.perf_counter() - start) * 1000
            return self._format_result(
                status="UNREACHABLE",
                latency_ms=latency_ms,
                details={"error": str(e)},
                message=f"Backstage instance unreachable: {str(e)}",
            )

    def fetch_entities(
        self,
        kind: Optional[str] = None,
        filter_query: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetches entity definitions from the Backstage catalog.
        """
        endpoint = "/api/catalog/entities"
        params: Dict[str, Any] = {}
        if kind:
            params["filter"] = f"kind={kind}"
        if filter_query:
            params["filter"] = filter_query

        resp = self._request("GET", endpoint, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []

    def convert_entity_to_pam_node(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a Backstage catalog entity into a conformed PAM (Pragmatic Architectural Model) node.
        """
        kind = entity.get("kind", "Component")
        metadata = entity.get("metadata", {})
        spec = entity.get("spec", {})

        name = metadata.get("name", "unknown")
        raw_type = str(spec.get("type", "service")).lower()
        tags = metadata.get("tags", [])
        annotations = metadata.get("annotations", {})

        # Determine PAM entity type & URN prefix
        if kind == "Component":
            if raw_type in ("service", "microservice", "backend"):
                entity_type = "Microservice"
                prefix = "microservice"
            elif raw_type in ("website", "frontend", "application", "app"):
                entity_type = "Application"
                prefix = "application"
            elif raw_type in ("library", "package"):
                entity_type = "Library"
                prefix = "library"
            else:
                entity_type = "Microservice"
                prefix = "microservice"
        elif kind == "Resource":
            if raw_type in ("database", "postgres", "mysql", "dynamo", "cassandra", "rds"):
                entity_type = "Database"
                prefix = "database"
            elif raw_type in ("queue", "stream", "kafka", "kinesis", "eventbridge"):
                entity_type = "EventStream"
                prefix = "stream"
            else:
                entity_type = "CloudResource"
                prefix = "cloud"
        elif kind == "API":
            entity_type = "Interface"
            prefix = "interface"
        elif kind == "System":
            entity_type = "System"
            prefix = "system"
        elif kind == "Domain":
            entity_type = "BusinessCapability"
            prefix = "capability"
        else:
            entity_type = "Microservice"
            prefix = "microservice"

        # Determine criticality tier
        tier = annotations.get("ea/tier")
        if not tier:
            tag_lower = [t.lower() for t in tags]
            if "tier-0" in tag_lower or "critical" in tag_lower:
                tier = "Tier-0"
            elif "tier-1" in tag_lower:
                tier = "Tier-1"
            elif "tier-3" in tag_lower:
                tier = "Tier-3"
            else:
                tier = "Tier-2"

        data_classification = annotations.get("ea/data_classification", "Internal")

        return {
            "urn": f"urn:ea:{prefix}:{name}",
            "entity_type": entity_type,
            "name": name,
            "tier": tier,
            "lifecycle_status": spec.get("lifecycle", "production"),
            "owner": spec.get("owner", "Enterprise Architecture"),
            "tags": tags,
            "data_classification": data_classification,
            "description": metadata.get("description", ""),
            "source": "backstage-catalog",
            "properties": {
                "backstage_uid": metadata.get("uid"),
                "system": spec.get("system"),
                "raw_kind": kind,
                "raw_type": raw_type,
                "annotations": annotations,
            },
        }

    def export_pam_nodes_to_backstage_entities(
        self,
        nodes: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Exports PAM nodes into Backstage Catalog entity descriptors (catalog-info.yaml compatible).
        """
        entities = []
        for node in nodes:
            name = node.get("name", "unknown")
            entity_type = node.get("entity_type", "Microservice")
            urn = node.get("urn", f"urn:ea:{name}")
            owner = node.get("owner", "architecture-team")
            lifecycle = node.get("lifecycle_status", "production")
            description = node.get("description", f"Conformed PAM entity: {name}")
            tags = list(node.get("tags") or [])

            # Map to Backstage kind and spec.type
            if entity_type == "Microservice":
                kind = "Component"
                spec_type = "service"
            elif entity_type == "Application":
                kind = "Component"
                spec_type = "website"
            elif entity_type == "Database":
                kind = "Resource"
                spec_type = "database"
            elif entity_type == "EventStream":
                kind = "Resource"
                spec_type = "queue"
            elif entity_type == "Interface":
                kind = "API"
                spec_type = "openapi"
            else:
                kind = "Component"
                spec_type = "service"

            entity = {
                "apiVersion": "backstage.io/v1alpha1",
                "kind": kind,
                "metadata": {
                    "name": name,
                    "title": name.replace("-", " ").title(),
                    "description": description,
                    "tags": tags,
                    "annotations": {
                        "ea.governance/urn": urn,
                        "ea.governance/tier": node.get("tier", "Tier-2"),
                        "ea.governance/data_classification": node.get("data_classification", "Internal"),
                    },
                },
                "spec": {
                    "type": spec_type,
                    "lifecycle": lifecycle,
                    "owner": owner,
                },
            }
            if kind == "API":
                entity["spec"]["definition"] = "$text: ./openapi.yaml"

            entities.append(entity)

        return entities

    def generate_techdocs_bundle(
        self,
        entity_name: str,
        adrs: Optional[List[Dict[str, Any]]] = None,
        diagrams: Optional[List[Dict[str, Any]]] = None,
        docs_content: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Generates a complete Backstage TechDocs package containing mkdocs.yml and markdown pages.
        """
        bundle: Dict[str, str] = {}

        # 1. mkdocs.yml
        mkdocs_config = f"""site_name: '{entity_name.replace("-", " ").title()} Architecture Documentation'
site_description: 'Living Architecture Documentation generated by The Agentic EA Platform'

nav:
  - Overview: index.md
  - Architectural Decisions:
    - Index: adrs/index.md
"""
        bundle["mkdocs.yml"] = mkdocs_config

        # 2. docs/index.md
        index_body = docs_content or f"""# {entity_name.title()} System Architecture

## Executive Overview
This document represents living, synchronized architecture telemetry maintained continuously by **The Agentic EA Platform**.

### System Specifications
- **Component ID:** `{entity_name}`
- **Governance Gate:** Automated Sentinel CI/CD Validation
- **Compliance Status:** GDPR / DORA / EU AI Act Conformed

## Visual Architecture
"""
        if diagrams:
            for diag in diagrams:
                index_body += f"\n### {diag.get('title', 'Architecture Topology')}\n"
                if "mermaid" in diag:
                    index_body += f"\n```mermaid\n{diag['mermaid']}\n```\n"
                elif "html_embed" in diag:
                    index_body += f"\n{diag['html_embed']}\n"

        bundle["docs/index.md"] = index_body

        # 3. docs/adrs/index.md & ADR records
        adr_index = f"""# Architectural Decision Records (MADRs)

Living architectural decisions governing `{entity_name}`.

| ADR # | Title | Status | Date |
|-------|-------|--------|------|
"""
        if adrs:
            for adr in adrs:
                adr_num = adr.get("number", "0001")
                adr_title = adr.get("title", "Untitled Architecture Decision")
                adr_status = adr.get("status", "Accepted")
                adr_date = adr.get("date", "2026-10-20")

                adr_filename = f"docs/adrs/ADR-{adr_num}.md"
                adr_index += f"| [{adr_num}](ADR-{adr_num}.md) | {adr_title} | `{adr_status}` | {adr_date} |\n"

                adr_content = f"""# ADR-{adr_num}: {adr_title}

* **Status:** {adr_status}
* **Deciders:** Enterprise Architecture Board, System Owners
* **Date:** {adr_date}

## Context and Problem Statement
{adr.get('context', 'Architecture evolution required to support scaling and regulatory governance.')}

## Decision Outcome
Chosen option: "{adr.get('decision', 'Adopt conformed microservice boundary with event-driven data backbone.')}"

## Consequences
### Positive
{adr.get('positive_consequences', '* Decoupled failure domains\\n* Unified data lineage')}

### Negative / Trade-offs
{adr.get('negative_consequences', '* Increased distributed tracing operational overhead')}
"""
                bundle[adr_filename] = adr_content
        else:
            adr_index += "| [0001](ADR-0001.md) | Initial Architecture Baseline | `Accepted` | 2026-10-20 |\n"
            bundle["docs/adrs/ADR-0001.md"] = f"""# ADR-0001: Initial Architecture Baseline for {entity_name}

* **Status:** Accepted
* **Deciders:** Enterprise Architecture Board
* **Date:** 2026-10-20

## Context
Initial ingestion and conformance into PAM metamodel.
"""

        bundle["docs/adrs/index.md"] = adr_index
        return bundle
