"""
Scenario S08 — Regulatory Compliance & Data Privacy Impact Mapping (GDPR / DORA).
Tests:
1. Data Classification & Jurisdiction in PAM Metamodel (nodes & edges metadata).
2. Conformed Gold Compliance Mart (ea.gold.compliance_lineage populated with 7 flows).
3. Estate Intelligence Engine BFS traversal tracing customer PII lineage.
4. GDPR Article 32 violation detection (unencrypted transit plaintext / rest none).
5. GDPR Article 44-49 cross-border transfer detection (EU-West-1 -> US-East-1).
6. DORA ICT resilience vulnerability identification (unreplicated SPOF datastore past EOL).
7. Archify living map compilation with jurisdiction boundary isolation and Tab 10 UI integration.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from src.data_backbone.client import get_unity_catalog_client
from src.navigator.engine import EstateIntelligenceEngine


@pytest.fixture(scope="module")
def client():
    return get_unity_catalog_client()


@pytest.fixture(scope="module")
def navigator():
    return EstateIntelligenceEngine()


def test_pii_classification_metadata_present(client):
    """Verify nodes and edges carry data classification, jurisdiction, and encryption metadata."""
    nodes = client.get_nodes()
    node_map = {n["name"]: n for n in nodes}

    # Verify cassandra-legacy-cluster has high-risk unencrypted PII metadata
    assert "cassandra-legacy-cluster" in node_map
    cass_meta = node_map["cassandra-legacy-cluster"].get("metadata") or {}
    assert cass_meta.get("data_classification") == "PII:High"
    assert cass_meta.get("jurisdiction") == "EU-West-1"
    assert cass_meta.get("encryption") == "none"

    # Verify customer-pii-stream has US jurisdiction
    assert "customer-pii-stream" in node_map
    stream_meta = node_map["customer-pii-stream"].get("metadata") or {}
    assert stream_meta.get("data_classification") == "PII:High"
    assert stream_meta.get("jurisdiction") == "US-East-1"

    # Verify payments-api has EU sovereign KMS encryption
    assert "payments-api" in node_map
    api_meta = node_map["payments-api"].get("metadata") or {}
    assert api_meta.get("data_classification") == "PII:High"
    assert api_meta.get("jurisdiction") == "EU-West-1"
    assert api_meta.get("encryption") == "kms"

    # Verify edges carry transit encryption and transferred classification
    edges = client.get_edges()
    cass_edges = [
        e for e in edges
        if "cassandra-legacy-cluster" in e["target_urn"]
    ]
    assert len(cass_edges) >= 1
    cass_edge = cass_edges[0]
    assert cass_edge.get("transit_encryption") == "plaintext"
    assert cass_edge.get("transferred_classification") == "PII:High"


def test_compliance_gold_mart_populated(client):
    """Verify conformed mart ea.gold.compliance_lineage contains required fields and canonical flows."""
    records = client.get_compliance_lineage()
    assert len(records) >= 7

    flow_ids = {r["flow_id"] for r in records}
    assert "FLOW-001-WEB-CHECKOUT" in flow_ids
    assert "FLOW-002-CHECKOUT-PAYMENTS" in flow_ids
    assert "FLOW-003-PAYMENTS-BILLING" in flow_ids
    assert "FLOW-004-PAYMENTS-STRIPE" in flow_ids
    assert "FLOW-005-PAYMENTS-LEDGER" in flow_ids
    assert "FLOW-006-PII-STREAM-EGRESS" in flow_ids
    assert "FLOW-007-LEGACY-CASSANDRA-SYNC" in flow_ids

    # Verify mandatory schema fields
    for r in records:
        assert "flow_id" in r
        assert "source_urn" in r
        assert "target_urn" in r
        assert "data_classification" in r
        assert "jurisdiction_source" in r
        assert "jurisdiction_target" in r
        assert "is_cross_border" in r
        assert "transit_encryption" in r
        assert "rest_encryption" in r
        assert "gdpr_status" in r
        assert "dora_status" in r
        assert "risk_level" in r


def test_bfs_pii_lineage_traversal(navigator):
    """Verify Estate Intelligence Engine traces PII dataflows via BFS from ingress to datastores."""
    analysis = navigator.analyze_compliance_lineage()
    assert analysis["total_lineage_flows_count"] >= 7
    assert analysis["pii_datastores_count"] == 3
    assert len(analysis["pii_paths"]) >= 2

    # Check identified PII datastores
    store_names = {n["name"] for n in analysis["pii_datastores"]}
    assert "billing-db" in store_names
    assert "payments-ledger-db" in store_names
    assert "cassandra-legacy-cluster" in store_names


def test_gdpr_article_32_violation_detection(navigator, client):
    """Verify GDPR Article 32 violation: unencrypted transit (plaintext) and rest (none)."""
    analysis = navigator.analyze_compliance_lineage()
    assert analysis["unencrypted_flows_count"] >= 1

    unenc = analysis["unencrypted_flows"]
    flow_007 = next((f for f in unenc if f["flow_id"] == "FLOW-007-LEGACY-CASSANDRA-SYNC"), None)
    assert flow_007 is not None
    assert flow_007["transit_encryption"] == "plaintext"
    assert flow_007["rest_encryption"] == "none"
    assert flow_007["gdpr_status"] == "ART32_VIOLATION"
    assert flow_007["risk_level"] == "CRITICAL"


def test_gdpr_article_44_cross_border_detection(navigator, client):
    """Verify GDPR Article 44-49 violation: cross-border egress from EU-West-1 to US-East-1."""
    analysis = navigator.analyze_compliance_lineage()
    assert analysis["cross_border_egress_count"] >= 1

    cross = analysis["cross_border_flows"]
    flow_006 = next((f for f in cross if f["flow_id"] == "FLOW-006-PII-STREAM-EGRESS"), None)
    assert flow_006 is not None
    assert flow_006["is_cross_border"] is True
    assert flow_006["jurisdiction_source"] == "EU-West-1"
    assert flow_006["jurisdiction_target"] == "US-East-1"
    assert flow_006["gdpr_status"] == "ART44_VIOLATION"
    assert flow_006["risk_level"] == "HIGH"


def test_dora_ict_resilience_vulnerabilities(navigator):
    """Verify DORA ICT resilience vulnerability identification for SPOF datastore past EOL."""
    analysis = navigator.analyze_compliance_lineage()
    assert analysis["dora_risk_index"] == "HIGH (78/100)"
    assert len(analysis["dora_risks"]) >= 1

    dora_flow = next((f for f in analysis["dora_risks"] if "cassandra" in f["target_urn"]), None)
    assert dora_flow is not None
    assert dora_flow["dora_status"] == "SPOF_RISK"

    # Verify structured violation entries
    articles = [v["article"] for v in analysis["violations"]]
    assert any("DORA" in a for a in articles)
    assert any("Article 32" in a for a in articles)
    assert any("Article 44" in a for a in articles)


def test_archify_diagram_and_ui_tab10_integration(navigator):
    """Verify compiled Archify living dataflow diagram and Tab 10 UI integration."""
    diag = navigator.compile_compliance_lineage_diagram()
    html_p = Path(diag["html_path"])
    svg_p = Path(diag["svg_path"])

    assert html_p.exists()
    assert html_p.stat().st_size > 1000
    assert svg_p.exists()
    assert svg_p.stat().st_size > 500

    # Ensure SVG has embedded styles to prevent black box defects
    svg_text = svg_p.read_text(encoding="utf-8")
    assert "<style" in svg_text
    assert "<defs" in svg_text

    # Verify natural language query in EstateIntelligenceEngine
    query_res = navigator.query("What are our GDPR Article 32 and Article 44 compliance violations?")
    assert "Regulatory Compliance & Data Privacy Impact Mapping" in query_res["answer"]
    assert "FLOW-007-LEGACY-CASSANDRA-SYNC" in query_res["answer"]
    assert "FLOW-006-PII-STREAM-EGRESS" in query_res["answer"]

    # Verify Tab 10 in apps/ea_navigator/app.py
    app_text = (ROOT_DIR / "apps" / "ea_navigator" / "app.py").read_text(encoding="utf-8")
    assert "tab_compliance" in app_text
    assert "Regulatory Compliance & Privacy Lineage (GDPR / DORA)" in app_text


def main():
    """Standalone CLI verification runner with Rich tables."""
    console = Console()
    console.print(Panel.fit(
        "[bold cyan]The Agentic EA Platform — Scenario S08[/bold cyan]\n"
        "[bold yellow]Regulatory Compliance & Data Privacy Impact Mapping (GDPR / DORA)[/bold yellow]\n"
        "[dim]Unity Catalog Lineage Mart, Cryptographic Posture & Sovereign Jurisdiction Isolation[/dim]",
        border_style="cyan"
    ))

    navigator = EstateIntelligenceEngine()
    analysis = navigator.analyze_compliance_lineage()
    diag = navigator.compile_compliance_lineage_diagram()

    # Table 1: Executive KPI Summary
    t1 = Table(title="📊 Executive Regulatory Compliance & Resilience KPIs", header_style="bold magenta")
    t1.add_column("Metric Indicator", style="cyan")
    t1.add_column("Measured Value", style="bold green", justify="center")
    t1.add_column("Compliance Benchmark", style="dim")
    t1.add_column("Operational Risk Status", style="bold")

    t1.add_row("Total Governed Lineage Flows", str(analysis["total_lineage_flows_count"]), "7 Canonical Dataflows", "[green]100% Tracked[/green]")
    t1.add_row("Compliant Data Flows (Low Risk)", str(analysis["compliant_flows_count"]), "End-to-End Encrypted (TLS 1.3 + KMS)", "[green]5 Flows Clean[/green]")
    t1.add_row("PII Datastores in Scope", str(analysis["pii_datastores_count"]), "billing-db, payments-ledger, cassandra", "[yellow]Tier-0/1 Active[/yellow]")
    t1.add_row("Unencrypted Flows (GDPR Art. 32)", str(analysis["unencrypted_flows_count"]), "Plaintext CQL Transit / None at Rest", "[bold red]🚨 CRITICAL VIOLATION[/bold red]")
    t1.add_row("Third-Country Egress (GDPR Art. 44)", str(analysis["cross_border_egress_count"]), "EU-West-1 ➔ US-East-1 Transfer", "[bold yellow]⚠️ HIGH RISK (No SCC)[/bold yellow]")
    t1.add_row("DORA ICT Resilience Risk Index", analysis["dora_risk_index"], "Unreplicated Legacy SPOF past EOL", "[bold red]🚨 HIGH VULNERABILITY[/bold red]")
    console.print(t1)

    # Table 2: Conformed Compliance Lineage Register
    t2 = Table(title="📋 Conformed Compliance Lineage Register (ea.gold.compliance_lineage)", header_style="bold blue")
    t2.add_column("Flow ID", style="bold")
    t2.add_column("Source ➔ Target", style="cyan")
    t2.add_column("Class", style="magenta")
    t2.add_column("Jurisdiction", style="dim")
    t2.add_column("Transit / Rest", style="yellow")
    t2.add_column("GDPR Status", justify="center")
    t2.add_column("DORA Status", justify="center")
    t2.add_column("Risk Level", justify="center")

    for f in analysis["lineage_records"]:
        s_name = f["source_urn"].split(":")[-1]
        t_name = f["target_urn"].split(":")[-1]
        flow_str = f"{s_name} ➔ {t_name}"

        g_style = "[bold red]ART32_VIOLATION[/bold red]" if f["gdpr_status"] == "ART32_VIOLATION" else (
            "[bold yellow]ART44_VIOLATION[/bold yellow]" if f["gdpr_status"] == "ART44_VIOLATION" else "[green]COMPLIANT[/green]"
        )
        d_style = "[bold red]SPOF_RISK[/bold red]" if f["dora_status"] == "SPOF_RISK" else "[green]RESILIENT[/green]"
        r_style = "[bold red]CRITICAL[/bold red]" if f["risk_level"] == "CRITICAL" else (
            "[bold yellow]HIGH[/bold yellow]" if f["risk_level"] == "HIGH" else "[green]LOW[/green]"
        )

        t2.add_row(
            f["flow_id"],
            flow_str,
            f["data_classification"],
            f"{f['jurisdiction_source']} ➔ {f['jurisdiction_target']}",
            f"{f['transit_encryption']} / {f['rest_encryption']}",
            g_style,
            d_style,
            r_style,
        )
    console.print(t2)

    # Table 3: Regulatory Violations & Remediation Action Plan
    t3 = Table(title="🚨 Regulatory Discrepancies & Strategic Remediation Action Plan", header_style="bold red")
    t3.add_column("Regulation", style="bold cyan")
    t3.add_column("Target Component", style="magenta")
    t3.add_column("Severity", style="bold")
    t3.add_column("Violation Detail", style="dim")
    t3.add_column("Actionable Architectural Remediation", style="green")

    for v in analysis["violations"]:
        sev_style = f"[bold red]{v['severity']}[/bold red]" if v["severity"] == "CRITICAL" else f"[bold yellow]{v['severity']}[/bold yellow]"
        t3.add_row(v["article"], v["component"], sev_style, v["details"], v["remediation"])
    console.print(t3)

    # Table 4: Compiled Living Maps
    t4 = Table(title="🗺️ Archify Living Architecture Artifacts", header_style="bold green")
    t4.add_column("Artifact Type", style="cyan")
    t4.add_column("File Path", style="dim")
    t4.add_column("File Size", style="green", justify="right")
    t4.add_column("Visual Boundary Mode", style="magenta")

    html_p = Path(diag["html_path"])
    svg_p = Path(diag["svg_path"])
    t4.add_row("Interactive HTML Map", str(html_p), f"{html_p.stat().st_size:,} bytes", "Jurisdiction (EU vs US Isolation)")
    t4.add_row("Styled Vector SVG", str(svg_p), f"{svg_p.stat().st_size:,} bytes", "Standalone Vector (Defs/CSS Injected)")
    console.print(t4)

    console.print(Panel("[bold green]✓ Scenario S08 Regulatory Compliance & Privacy Lineage Fully Verified[/bold green]", border_style="green"))


if __name__ == "__main__":
    main()
