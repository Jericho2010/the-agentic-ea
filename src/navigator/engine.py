"""
The Agentic EA Platform - EA Navigator Engine.
Estate Intelligence Engine (EIE):
- Graph traversal (BFS upstream/downstream dependency analysis)
- Financial risk quantification (ea.gold.time_matrix)
- Customer PII data lineage detection (GDPR Art. 32 / DORA)
- Dynamic Archify visual map compilation with node highlighting
- Standards-compliant Markdown Architecture Decision Record (MADR) generation
- Interactive Co-Driving action suggestions
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx

from src.archify.bridge import ArchifyBridge
from src.data_backbone.client import get_unity_catalog_client

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


logger = logging.getLogger("ea_navigator_engine")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class EstateIntelligenceEngine:
    """
    Core graph reasoning engine for EA Navigator.
    Grounds all analysis directly in Unity Catalog conformed Delta tables.
    """

    def __init__(self):
        self.client = get_unity_catalog_client()
        self.graph = nx.DiGraph()
        self.nodes_by_urn: Dict[str, Dict[str, Any]] = {}
        self.nodes_by_name: Dict[str, Dict[str, Any]] = {}
        self.time_matrix_by_urn: Dict[str, Dict[str, Any]] = {}
        self.archify_bridge = ArchifyBridge()
        self._load_estate_graph()

    def _load_estate_graph(self) -> None:
        """Loads conformed nodes, edges, and TIME matrix from Unity Catalog into NetworkX."""
        raw_nodes = self.client.get_nodes()
        raw_edges = self.client.get_edges()
        raw_time = self.client.get_time_matrix()

        # Index TIME matrix by URN and name
        for t in raw_time:
            self.time_matrix_by_urn[t["urn"]] = t
            self.time_matrix_by_urn[t["name"]] = t

        # Add nodes
        for n in raw_nodes:
            urn = n["urn"]
            name = n["name"]
            self.nodes_by_urn[urn] = n
            self.nodes_by_name[name.lower()] = n

            # Attach TIME matrix metrics if available
            time_data = self.time_matrix_by_urn.get(urn) or self.time_matrix_by_urn.get(name) or {}
            annual_cost = float(time_data.get("annual_run_cost", 15000.0))
            disposition = time_data.get("disposition", "Tolerate")
            tech_debt = int(time_data.get("tech_debt_score", 30))

            self.graph.add_node(
                urn,
                name=name,
                kind=n.get("kind", "Microservice"),
                owner_team=n.get("owner_team", "unassigned"),
                lifecycle_status=n.get("lifecycle_status", "run"),
                criticality=n.get("criticality", "Tier-2"),
                annual_run_cost=annual_cost,
                disposition=disposition,
                tech_debt_score=tech_debt,
                metadata=n.get("metadata", {}),
            )

        # Add edges
        # Note: In our model, edge (source_urn, target_urn, relation) means source_urn calls/accesses target_urn
        for e in raw_edges:
            src = e["source_urn"]
            tgt = e["target_urn"]
            if src in self.nodes_by_urn and tgt in self.nodes_by_urn:
                self.graph.add_edge(
                    src,
                    tgt,
                    relation=e.get("relation", "accesses"),
                    protocol=e.get("protocol", "HTTPS/JSON"),
                    contains_pii=bool(e.get("contains_pii", False)),
                )

    def resolve_node_urn(self, identifier: str) -> Optional[str]:
        """Resolves a URN or friendly name to a canonical PAM URN."""
        clean_id = identifier.strip().strip("'\"")
        if clean_id in self.nodes_by_urn:
            return clean_id
        lower_id = clean_id.lower()
        if lower_id in self.nodes_by_name:
            return self.nodes_by_name[lower_id]["urn"]
        # Partial match
        for name, node in self.nodes_by_name.items():
            if lower_id in name:
                return node["urn"]
        return None

    def calculate_blast_radius(self, target_identifier: str) -> Dict[str, Any]:
        """
        Performs comprehensive BFS graph traversal for a target component:
        - Direct and transitive upstream callers (who breaks if target is unavailable)
        - Direct and transitive downstream dependencies
        - Financial exposure at risk ($/yr)
        - Customer PII flow lineage (GDPR Art. 32 / DORA)
        - Maximum affected criticality tier
        """
        self._load_estate_graph()
        target_urn = self.resolve_node_urn(target_identifier)
        if not target_urn or target_urn not in self.graph:
            return {
                "error": f"Target entity '{target_identifier}' not found in Unity Catalog estate graph.",
                "found": False,
            }

        target_node = self.graph.nodes[target_urn]
        target_name = target_node.get("name", target_urn)

        # 1. Upstream Callers (Ancestors in call graph: reverse traversal)
        # Using reversed graph: edges point from target to caller
        reversed_graph = self.graph.reverse()
        upstream_urns = set(nx.descendants(reversed_graph, target_urn))
        direct_callers = set(reversed_graph.neighbors(target_urn))

        # 2. Downstream Dependencies (Descendants in call graph: forward traversal)
        downstream_urns = set(nx.descendants(self.graph, target_urn))
        direct_dependencies = set(self.graph.neighbors(target_urn))

        # All affected nodes (target + upstream callers)
        all_affected_urns = {target_urn} | upstream_urns

        # 3. Financial Exposure Quantification ($/yr)
        total_annual_exposure = sum(
            self.graph.nodes[u].get("annual_run_cost", 0.0) for u in all_affected_urns
        )

        upstream_summary = []
        for u in upstream_urns:
            n = self.graph.nodes[u]
            upstream_summary.append({
                "urn": u,
                "name": n.get("name", u),
                "kind": n.get("kind"),
                "criticality": n.get("criticality"),
                "owner_team": n.get("owner_team"),
                "annual_cost": n.get("annual_run_cost", 0.0),
                "is_direct": u in direct_callers,
            })

        downstream_summary = []
        for u in downstream_urns:
            n = self.graph.nodes[u]
            downstream_summary.append({
                "urn": u,
                "name": n.get("name", u),
                "kind": n.get("kind"),
                "criticality": n.get("criticality"),
                "owner_team": n.get("owner_team"),
                "is_direct": u in direct_dependencies,
            })

        # 4. Customer PII Lineage Detection
        pii_paths = []
        pii_involved_nodes = set()
        
        # Check all edges in the connected component for PII flags
        for u, v, data in self.graph.edges(data=True):
            if data.get("contains_pii"):
                pii_involved_nodes.add(u)
                pii_involved_nodes.add(v)
                if u in all_affected_urns or v in all_affected_urns or u == target_urn or v == target_urn:
                    src_name = self.graph.nodes[u].get("name", u)
                    dst_name = self.graph.nodes[v].get("name", v)
                    pii_paths.append({
                        "source": src_name,
                        "source_urn": u,
                        "target": dst_name,
                        "target_urn": v,
                        "protocol": data.get("protocol", "TLS"),
                        "description": f"PII data flow: {src_name} ➔ {dst_name} via {data.get('protocol', 'TLS')}",
                    })

        # 5. Criticality Tier Calculation
        tier_hierarchy = {"Tier-0": 0, "Tier-1": 1, "Tier-2": 2, "Tier-3": 3}
        highest_tier = "Tier-3"
        highest_tier_val = 3
        for u in all_affected_urns:
            c = self.graph.nodes[u].get("criticality", "Tier-2")
            val = tier_hierarchy.get(c, 2)
            if val < highest_tier_val:
                highest_tier_val = val
                highest_tier = c

        # Highlighted list for Archify diagram rendering
        highlighted_urns = sorted(list(all_affected_urns | downstream_urns))

        return {
            "found": True,
            "target": {
                "urn": target_urn,
                "name": target_name,
                "kind": target_node.get("kind"),
                "owner_team": target_node.get("owner_team"),
                "criticality": target_node.get("criticality"),
                "lifecycle_status": target_node.get("lifecycle_status"),
                "annual_run_cost": target_node.get("annual_run_cost", 0.0),
                "disposition": target_node.get("disposition", "Tolerate"),
                "tech_debt_score": target_node.get("tech_debt_score", 30),
            },
            "upstream_callers": upstream_summary,
            "upstream_count": len(upstream_urns),
            "direct_callers_count": len(direct_callers),
            "downstream_dependencies": downstream_summary,
            "downstream_count": len(downstream_urns),
            "financial_exposure": {
                "total_annual_risk_usd": total_annual_exposure,
                "target_annual_cost_usd": target_node.get("annual_run_cost", 0.0),
                "affected_services_count": len(all_affected_urns),
            },
            "pii_compliance": {
                "has_pii_exposure": len(pii_paths) > 0,
                "pii_paths": pii_paths,
                "regulatory_impact": "GDPR Art. 32 / DORA Resilience Mandate" if len(pii_paths) > 0 else "None",
            },
            "aggregate_criticality": highest_tier,
            "highlighted_urns": highlighted_urns,
        }

    def compile_blast_radius_diagram(
        self,
        target_identifier: str,
        highlight_urns: Optional[List[str]] = None,
        output_prefix: str = "blast_radius"
    ) -> Dict[str, str]:
        """
        Compiles dynamic interactive HTML and styled vector SVG maps
        with highlighted blast radius nodes using ArchifyBridge.
        """
        target_urn = self.resolve_node_urn(target_identifier) or target_identifier
        target_slug = target_urn.split(":")[-1]
        
        if highlight_urns is None:
            blast = self.calculate_blast_radius(target_urn)
            highlight_urns = blast.get("highlighted_urns", [target_urn])

        output_html = ROOT_DIR / "data" / "diagrams" / f"{output_prefix}_{target_slug}.html"
        output_svg = ROOT_DIR / "data" / "diagrams" / f"{output_prefix}_{target_slug}.svg"
        output_html.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generating Archify blast radius diagram for '{target_slug}' highlighting {len(highlight_urns)} nodes...")
        self.archify_bridge.compile_interactive_map(
            output_html_path=output_html,
            output_svg_path=output_svg,
            highlight_urns=highlight_urns
        )

        return {
            "html_path": str(output_html),
            "svg_path": str(output_svg),
            "highlighted_count": str(len(highlight_urns)),
        }

    def generate_madr(
        self,
        target_identifier: str,
        proposal_title: Optional[str] = None,
        context_details: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generates a standards-compliant Markdown Architecture Decision Record (MADR v3.0).
        """
        blast = self.calculate_blast_radius(target_identifier)
        if not blast.get("found"):
            return f"# Error: Cannot generate MADR for '{target_identifier}' (Component not found in catalog)."

        target = blast["target"]
        name = target["name"]
        title = proposal_title or f"Modernization & Risk Mitigation for {name}"
        fin = blast["financial_exposure"]
        pii = blast["pii_compliance"]
        crit = blast["aggregate_criticality"]

        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        madr = f"""# ADR-002: {title}

## Metadata
* **Status:** Proposed
* **Deciders:** Enterprise Architecture Board, Platform Engineering, FinOps
* **Date:** {today_str}
* **Target Component:** `{target['urn']}` ({target['kind']})
* **Architectural Criticality:** {crit}
* **Annual Exposure at Risk:** ${fin['total_annual_risk_usd']:,.2f}/yr

## Context and Problem Statement
The enterprise service `{name}` currently operates under the lifecycle status `{target['lifecycle_status']}` with an architectural disposition of `{target['disposition']}` (Tech Debt Score: {target['tech_debt_score']}/100).
Graph traversal reveals **{blast['upstream_count']} upstream callers** directly affected by service disruption, representing an aggregate annual financial risk of **${fin['total_annual_risk_usd']:,.2f}**.
{'⚠️ **Regulatory Warning:** The service is part of an active PII data stream subject to GDPR Art. 32 and DORA operational resilience mandates.' if pii['has_pii_exposure'] else 'No direct customer PII exposure detected.'}

## Decision Drivers
1. **Business Continuity:** Mitigate single point of failure affecting {blast['upstream_count']} upstream business services.
2. **FinOps & Modernization:** Eliminate legacy run cost (${target['annual_run_cost']:,.2f}/yr) and lower technical debt.
3. **Data Protection:** Enforce end-to-end KMS encryption and zero-trust mTLS protocols across all dependent edges.

## Considered Options
* **Option 1: In-Place Remediation & HA Clustering** (Retain current runtime, add multi-region replication).
* **Option 2: Target Architecture Migration to Databricks Unity Catalog & Managed Microservices** (Recommended).
* **Option 3: Tolerate Technical Debt with Exception Waiver** (Accept operational risk).

## Decision Outcome
**Chosen Option:** **Option 2: Target Architecture Migration to Databricks Unity Catalog & Managed Microservices**.

### Positive Consequences
* Eliminates ${target['annual_run_cost']:,.2f}/yr in unmanaged cloud compute costs.
* Brings technical debt score from {target['tech_debt_score']} down to <15.
* Enforces central Unity Catalog access controls, automated lineage tracking, and encryption at rest.
* De-risks upstream dependent services: {', '.join([c['name'] for c in blast['upstream_callers'][:5]])}.

### Negative Consequences
* Requires cross-team migration sprint coordinated with {target['owner_team']}.
* Temporary operational freeze during data migration cutover window.

## Pros and Cons of the Options

### Option 1: In-Place Remediation
* Good: Low engineering effort for application teams.
* Bad: Does not eliminate underlying technical debt ({target['tech_debt_score']}/100).
* Bad: Continued high annual infrastructure spend.

### Option 2: Databricks Unity Catalog Migration (Recommended)
* Good: Full alignment with EA North Star architecture and Lakehouse standards.
* Good: Native automated column-level PII lineage and governance.
* Good: Reduces total cost of ownership by up to 40%.
* Bad: Requires refactoring data access layer and schema migration.

### Option 3: Tolerate with Waiver
* Good: Zero immediate engineering cost.
* Bad: Fails EA Sentinel compliance gate `EA-POL-001`.
* Bad: High risk of unplanned catastrophic outage during peak traffic.

## Links & Provenance
* Metamodel Node: `{target['urn']}`
* Living Map Blast Radius: `data/diagrams/blast_radius_{name}.html`
* Reconciled Telemetry: `ea.gold.drift_reconciled`
"""
        return madr

    def evaluate_lifecycle_risks(self, reference_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Evaluates Technology Obsolescence & Lifecycle Risk (EOL/EOS) across all cataloged assets.
        Cross-references ea.gold.time_matrix and ea.metamodel.nodes with live graph dependencies:
        - Risk Classification:
            - EXPIRED (CRITICAL): eol_date < reference_date (Past EOL, unapproved datastore)
            - NEAR_EOL (HIGH): 0 <= days_remaining <= 365 (EOL within 1 year)
            - APPROACHING_EOL (MEDIUM): 366 <= days_remaining <= 730 (EOL within 2 years)
            - SUPPORTED (LOW): days_remaining > 730 (Active architectural support)
        - Graph Impact:
            - Discovers upstream callers at risk
            - Aggregates financial exposure ($/yr)
            - Flags customer PII lineage
            - Recommends actionable modernization or sunset roadmap
        """
        self._load_estate_graph()
        time_records = self.client.get_time_matrix()
        nodes_records = self.client.get_nodes()
        nodes_by_urn = {n["urn"]: n for n in nodes_records}
        nodes_by_name = {n["name"].lower(): n for n in nodes_records}

        if reference_date:
            try:
                ref_dt = datetime.strptime(reference_date, "%Y-%m-%d").date()
            except Exception:
                ref_dt = datetime.now(timezone.utc).date()
        else:
            ref_dt = datetime.now(timezone.utc).date()

        results = []
        for t in time_records:
            name = t["name"]
            urn = t["urn"]
            disposition = t.get("disposition", "Tolerate")
            annual_cost = float(t.get("annual_run_cost", 0.0))
            tech_debt = int(t.get("tech_debt_score", 0))

            # Cross-reference node details
            node = nodes_by_urn.get(urn) or nodes_by_name.get(name.lower()) or {}
            kind = node.get("kind", "Microservice")
            owner_team = node.get("owner_team", "unassigned")
            criticality = node.get("criticality", "Tier-2")
            lifecycle_status = node.get("lifecycle_status", "run")
            meta = node.get("metadata", {})

            eol_str = t.get("eol_date") or meta.get("eol_date")
            if not eol_str:
                continue

            try:
                eol_dt = datetime.strptime(eol_str, "%Y-%m-%d").date()
                days_remaining = (eol_dt - ref_dt).days
            except Exception:
                continue

            # Classify Risk Horizon
            if days_remaining < 0:
                risk_level = "CRITICAL"
                risk_status = "EXPIRED"
                urgency = "IMMEDIATE_SUNSET"
            elif days_remaining <= 365:
                risk_level = "HIGH"
                risk_status = "NEAR_EOL"
                urgency = "MIGRATION_REQUIRED"
            elif days_remaining <= 730:
                risk_level = "MEDIUM"
                risk_status = "APPROACHING_EOL"
                urgency = "MODERNIZATION_PLANNING"
            else:
                risk_level = "LOW"
                risk_status = "SUPPORTED"
                urgency = "STABLE_INVESTMENT"

            # Blast radius graph traversal
            blast = self.calculate_blast_radius(urn)
            upstream_callers = [c["name"] for c in blast.get("upstream_callers", [])]
            direct_callers = [c["name"] for c in blast.get("upstream_callers", []) if c.get("is_direct")]
            upstream_count = blast.get("upstream_count", 0)
            fin_exposure = blast.get("financial_exposure", {}).get("total_annual_risk_usd", annual_cost)
            has_pii = blast.get("pii_compliance", {}).get("has_pii_exposure", False)

            # Remediation recommendation
            if risk_status == "EXPIRED":
                recom = (
                    f"CRITICAL: Immediate sunset required for `{name}` (EOL expired {eol_str}). "
                    f"De-risk {upstream_count} upstream services ({', '.join(upstream_callers[:3]) or 'none'}) "
                    f"and eliminate ${annual_cost:,.2f}/yr run cost via migration to Databricks Unity Catalog."
                )
            elif risk_status == "NEAR_EOL":
                recom = (
                    f"HIGH: Fast-track migration for `{name}` before {eol_str} ({days_remaining} days remaining). "
                    f"Protect {upstream_count} callers from unplanned operational deprecation."
                )
            elif risk_status == "APPROACHING_EOL":
                recom = (
                    f"MEDIUM: Schedule target-state modernization for `{name}` before {eol_str} ({days_remaining} days remaining). "
                    f"Current architectural disposition: {disposition}."
                )
            else:
                recom = f"LOW: Asset `{name}` is actively supported until {eol_str}. Maintain regular lifecycle monitoring."

            results.append({
                "name": name,
                "urn": urn,
                "kind": kind,
                "owner_team": owner_team,
                "criticality": criticality,
                "lifecycle_status": lifecycle_status,
                "disposition": disposition,
                "annual_run_cost": annual_cost,
                "tech_debt_score": tech_debt,
                "eol_date": eol_str,
                "days_remaining": days_remaining,
                "risk_level": risk_level,
                "risk_status": risk_status,
                "urgency": urgency,
                "upstream_callers_count": upstream_count,
                "upstream_callers": upstream_callers,
                "direct_callers": direct_callers,
                "financial_exposure_usd": fin_exposure,
                "has_pii_exposure": has_pii,
                "recommendation": recom,
            })

        severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        results.sort(key=lambda x: (severity_rank.get(x["risk_level"], 99), x["days_remaining"]))
        return results

    def validate_binding_lifecycle(
        self, source_identifier: str, target_identifier: str, reference_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validates whether establishing an architectural dependency from source to target
        is compliant with Technology Obsolescence & Lifecycle policies.
        Blocks bindings to deprecated/sunset assets (disposition=Eliminate, status=EXPIRED).
        """
        self._load_estate_graph()
        target_urn = self.resolve_node_urn(target_identifier) or target_identifier
        source_urn = self.resolve_node_urn(source_identifier) or source_identifier

        risks = self.evaluate_lifecycle_risks(reference_date)
        target_risk = next((r for r in risks if r["urn"] == target_urn or r["name"].lower() == target_identifier.lower()), None)

        if not target_risk:
            node = self.nodes_by_urn.get(target_urn) or self.nodes_by_name.get(target_identifier.lower())
            if node and node.get("lifecycle_status") in ("phase-out", "retired"):
                return {
                    "allowed": False,
                    "status": "BLOCKED",
                    "policy_id": "EA-POL-001",
                    "target": target_identifier,
                    "target_urn": target_urn,
                    "risk_level": "CRITICAL",
                    "reason": f"Binding from '{source_identifier}' to '{target_identifier}' is strictly blocked: target is in '{node.get('lifecycle_status')}' status.",
                    "remediation": "Choose an approved modern architecture alternative.",
                }
            return {"allowed": True, "status": "APPROVED", "policy_id": None, "reason": "No lifecycle risk detected."}

        if target_risk["risk_status"] == "EXPIRED" or target_risk["disposition"] == "Eliminate":
            return {
                "allowed": False,
                "status": "BLOCKED",
                "policy_id": "EA-POL-001",
                "target": target_risk["name"],
                "target_urn": target_risk["urn"],
                "risk_level": "CRITICAL",
                "risk_status": target_risk["risk_status"],
                "eol_date": target_risk["eol_date"],
                "reason": (
                    f"Binding from '{source_identifier}' to '{target_risk['name']}' is strictly blocked under EA-POL-001: "
                    f"target is past End-of-Life (EOL: {target_risk['eol_date']}, Disposition: {target_risk['disposition']}). "
                    f"New dependencies on sunset assets are prohibited."
                ),
                "remediation": f"Redirect dependency to an approved modern datastore/service (e.g. Databricks Unity Catalog Delta Lake).",
                "upstream_blast_radius": target_risk["upstream_callers_count"],
            }
        elif target_risk["risk_status"] == "NEAR_EOL":
            return {
                "allowed": True,
                "status": "WARNING",
                "policy_id": "EA-POL-001",
                "target": target_risk["name"],
                "target_urn": target_risk["urn"],
                "risk_level": "HIGH",
                "risk_status": target_risk["risk_status"],
                "eol_date": target_risk["eol_date"],
                "reason": (
                    f"Warning: target '{target_risk['name']}' is near End-of-Life ({target_risk['days_remaining']} days remaining). "
                    f"Architecture waiver required before production deployment."
                ),
                "remediation": "Ensure target migration path is committed before binding.",
            }
        else:
            return {
                "allowed": True,
                "status": "APPROVED",
                "policy_id": None,
                "target": target_risk["name"],
                "target_urn": target_risk["urn"],
                "risk_level": target_risk["risk_level"],
                "reason": f"Target '{target_risk['name']}' is actively supported until {target_risk['eol_date']}.",
            }

    def get_codriving_actions(self, target_identifier: str) -> List[Dict[str, str]]:
        """Returns contextual interactive co-driving action chips for UI and EA Navigator interactions."""
        blast = self.calculate_blast_radius(target_identifier)

        if not blast.get("found"):
            return [
                {"label": "🔍 Explore Estate Catalog", "action": "explore_catalog", "query": "Show all registered PAM components"}
            ]

        target_name = blast["target"]["name"]
        return [
            {
                "label": f"💥 Simulate {target_name} Outage",
                "action": "simulate_outage",
                "query": f"Calculate complete blast radius and financial exposure if {target_name} experiences a catastrophic outage",
            },
            {
                "label": f"📝 Draft Modernization ADR",
                "action": "draft_adr",
                "query": f"Draft an architectural decision record (MADR) for modernizing {target_name} to Databricks Unity Catalog",
            },
            {
                "label": f"🔒 Audit PII Lineage",
                "action": "audit_pii",
                "query": f"Audit customer PII data flow lineage and GDPR compliance for {target_name}",
            },
            {
                "label": f"🗺️ Generate Living Blast Map",
                "action": "render_map",
                "query": f"Compile visual Archify blast radius diagram highlighting all callers and sinks of {target_name}",
            },
        ]

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Conversational reasoning interface for EA Navigator.
        Answers architectural inquiries grounded in the live estate graph.
        """
        q = user_query.lower()

        # 1. Component Extraction
        matched_target = None
        for name in self.nodes_by_name:
            if name in q:
                matched_target = name
                break
        
        # Default fallback target if none matched
        if not matched_target:
            matched_target = "payments-api"

        blast = self.calculate_blast_radius(matched_target)
        target = blast.get("target", {})
        fin = blast.get("financial_exposure", {})
        pii = blast.get("pii_compliance", {})

        # Compile blast radius diagram
        diag = self.compile_blast_radius_diagram(matched_target, blast.get("highlighted_urns"))

        # Generate response text based on query intent
        if "adr" in q or "decision record" in q:
            response_text = self.generate_madr(matched_target)
        elif "pii" in q or "gdpr" in q or "lineage" in q or "compliance" in q:
            response_text = f"""### 🔒 Customer PII Lineage & Regulatory Audit: `{target.get('name')}`

* **PII Exposure Detected:** {'⚠️ YES' if pii.get('has_pii_exposure') else '✅ NO'}
* **Regulatory Standard:** {pii.get('regulatory_impact')}
* **Direct & Transitive Flow Paths:**
"""
            for p in pii.get("pii_paths", []):
                response_text += f"\n  - `{p['source']}` ➔ `{p['target']}` ({p['protocol']}) — *Contains PII: True*"

            response_text += f"""

#### Governance Recommendation
Enforce mandatory column-level tagging in Databricks Unity Catalog and encrypt transport edges via mTLS to satisfy GDPR Art. 32 security requirements.
"""
        elif any(k in q for k in ["eol", "lifecycle", "obsolescence", "sunset", "eos", "expired", "deprecated"]):
            risks = self.evaluate_lifecycle_risks()
            expired = [r for r in risks if r["risk_status"] == "EXPIRED"]
            near_eol = [r for r in risks if r["risk_status"] == "NEAR_EOL"]
            approaching = [r for r in risks if r["risk_status"] == "APPROACHING_EOL"]
            supported = [r for r in risks if r["risk_status"] == "SUPPORTED"]

            response_text = f"""### ⏳ Technology Obsolescence & Lifecycle Risk (EOL/EOS) Assessment

* **Total Conformed Systems Evaluated:** {len(risks)}
* **Critical / Expired (Past EOL):** **{len(expired)}** systems (Immediate sunset required)
* **High Risk (Near EOL < 1yr):** **{len(near_eol)}** systems (Active migration required)
* **Medium Risk (Approaching < 2yr):** **{len(approaching)}** systems (Modernization planning)
* **Supported (Low Risk > 2yr):** **{len(supported)}** systems

#### Estate Lifecycle Risk Register
| System | URN | Status | Horizon | Days | Upstream Callers | Financial Risk |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
"""
            for r in risks:
                badge = "🔴 EXPIRED" if r["risk_status"] == "EXPIRED" else ("🟠 NEAR_EOL" if r["risk_status"] == "NEAR_EOL" else ("🟡 APPROACHING" if r["risk_status"] == "APPROACHING_EOL" else "🟢 SUPPORTED"))
                response_text += f"| `{r['name']}` | `{r['urn']}` | {badge} | {r['eol_date']} | {r['days_remaining']}d | {r['upstream_callers_count']} callers | ${r['financial_exposure_usd']:,.2f} |\n"

            response_text += f"""
#### Strategic Modernization Roadmap
"""
            for r in expired + near_eol + approaching:
                response_text += f"* **{r['name']} ({r['risk_status']}):** {r['recommendation']}\n"
        else:
            # Blast Radius & Impact Analysis
            callers_str = ", ".join([f"`{c['name']}` ({c['criticality']})" for c in blast.get("upstream_callers", [])]) or "None (Edge consumer)"
            sinks_str = ", ".join([f"`{c['name']}`" for c in blast.get("downstream_dependencies", [])]) or "None (Terminal datastore)"
            
            response_text = f"""### 💥 Estate Blast Radius Analysis: `{target.get('name')}`

* **URN:** `{target.get('urn')}`
* **Owning Team:** `{target.get('owner_team')}`
* **Architectural Criticality:** **{target.get('criticality')}** (Max Impact: **{blast.get('aggregate_criticality')}**)
* **Annual Financial Exposure:** **${fin.get('total_annual_risk_usd', 0.0):,.2f}/yr** across {fin.get('affected_services_count', 1)} systems

#### Impacted Topology
* **Upstream Callers ({blast.get('upstream_count')} total):** {callers_str}
* **Downstream Dependencies ({blast.get('downstream_count')} total):** {sinks_str}
* **PII Data Flow:** {'⚠️ Active PII Lineage Detected (GDPR Art. 32)' if pii.get('has_pii_exposure') else '✅ Clean (No customer PII detected)'}

#### Visual Architecture Map
Interactive living map compiled with highlighted blast radius:
* View in Cockpit: [Archify Living Map](file://{diag['html_path']})
"""

        return {
            "query": user_query,
            "target": matched_target,
            "answer": response_text,
            "blast_radius": blast,
            "diagrams": diag,
            "actions": self.get_codriving_actions(matched_target),
        }


def main():
    parser = argparse.ArgumentParser(description="EA Navigator - Estate Intelligence Engine")
    parser.add_argument("--target", default="payments-api", help="Target component URN or name")
    parser.add_argument("--query", help="Natural language architectural inquiry")
    parser.add_argument("--madr", action="store_true", help="Generate MADR architecture decision record")
    args = parser.parse_args()

    engine = EstateIntelligenceEngine()

    if args.query:
        res = engine.query(args.query)
        print(res["answer"])
        print("\nInteractive Co-Driving Actions:")
        for a in res["actions"]:
            print(f"  • {a['label']}: \"{a['query']}\"")
    elif args.madr:
        adr = engine.generate_madr(args.target)
        print(adr)
    else:
        blast = engine.calculate_blast_radius(args.target)
        diag = engine.compile_blast_radius_diagram(args.target, blast.get("highlighted_urns"))
        print(f"Target: {blast['target']['name']} ({blast['target']['urn']})")
        print(f"Upstream Callers: {blast['upstream_count']}")
        print(f"Total Annual Financial Risk: ${blast['financial_exposure']['total_annual_risk_usd']:,.2f}/yr")
        print(f"Aggregate Criticality: {blast['aggregate_criticality']}")
        print(f"PII Exposure: {blast['pii_compliance']['has_pii_exposure']}")
        print(f"Diagram Compiled: {diag['html_path']}")


if __name__ == "__main__":
    main()
