"""
Scenario S11 — AI Governance & ML Model Cataloging (EU AI Act).
Tests:
1. Ingestion of enterprise AI/ML models into ea.bronze.ai_models.
2. Conformed Gold AI Governance Mart (ea.gold.ai_governance populated with 4 models across EU risk tiers).
3. EU AI Act 4-tier risk classification (Unacceptable, High, Limited, Minimal).
4. Prohibited AI system detection (Art. 5 candidate-biometric-evaluator -> DECOMMISSION_IMMEDIATELY).
5. High-risk system human oversight enforcement (Annex III fraud-risk-scorer-v2 -> ENFORCE_HUMAN_OVERSIGHT).
6. End-to-end data lineage traversal in PAM graph (Training Data -> MLflow Model Registry -> Serving Endpoints).
7. Archify AI model lineage diagram compilation and Cockpit Tab 13 integration.
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


def test_ai_models_bronze_ingestion(client):
    """Verify enterprise AI/ML models are ingested into ea.bronze.ai_models."""
    models = client.get_ai_models()
    assert len(models) == 4

    model_ids = {m["model_id"] for m in models}
    assert "MDL-001-BIOMETRIC-EVALUATOR" in model_ids
    assert "MDL-002-FRAUD-RISK-SCORER" in model_ids
    assert "MDL-003-CUSTOMER-SUPPORT-LLM" in model_ids
    assert "MDL-004-PRODUCT-RECOMMENDER" in model_ids

    # Verify mandatory schema fields
    for m in models:
        assert "model_id" in m
        assert "model_name" in m
        assert "version" in m
        assert "framework" in m
        assert "task_type" in m
        assert "training_dataset_urn" in m
        assert "serving_endpoint_urn" in m
        assert "owner_team" in m
        assert "license" in m
        assert "has_human_in_the_loop" in m
        assert "timestamp" in m


def test_conformed_gold_ai_governance_mart_populated(client):
    """Verify conformed mart ea.gold.ai_governance contains 4 governed models with compliance metadata."""
    gov_records = client.get_ai_governance()
    assert len(gov_records) == 4

    model_names = {g["model_name"] for g in gov_records}
    assert "candidate-biometric-evaluator" in model_names
    assert "fraud-risk-scorer-v2" in model_names
    assert "customer-support-llm-v1" in model_names
    assert "product-recommender-v3" in model_names

    # Verify mandatory schema fields
    for g in gov_records:
        assert "model_id" in g
        assert "model_name" in g
        assert "version" in g
        assert "task_type" in g
        assert "eu_risk_tier" in g
        assert g["eu_risk_tier"] in ("UNACCEPTABLE_RISK", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK")
        assert "compliance_status" in g
        assert g["compliance_status"] in ("COMPLIANT", "ACTION_REQUIRED", "PROHIBITED")
        assert "has_model_card" in g
        assert "has_data_lineage" in g
        assert "has_human_oversight" in g
        assert "governance_action" in g


def test_eu_ai_act_risk_classification(client, navigator):
    """Verify Estate Intelligence Engine correctly classifies models into 4 EU AI Act risk tiers."""
    ai_data = navigator.analyze_ai_governance()

    assert ai_data["total_models_count"] == 4
    assert ai_data["prohibited_count"] == 1
    assert ai_data["high_risk_count"] == 1
    assert ai_data["limited_risk_count"] == 1
    assert ai_data["minimal_risk_count"] == 1
    assert ai_data["action_required_count"] == 3
    assert ai_data["compliant_count"] == 1


def test_prohibited_ai_system_detection(navigator):
    """Verify detection of prohibited emotion recognition system under EU AI Act Art. 5."""
    ai_data = navigator.analyze_ai_governance()

    prohibited = [m for m in ai_data["lineage_traces"] if m["eu_risk_tier"] == "UNACCEPTABLE_RISK"]
    assert len(prohibited) == 1
    p = prohibited[0]

    assert p["model_name"] == "candidate-biometric-evaluator"
    assert p["compliance_status"] == "PROHIBITED"
    assert p["governance_action"] == "DECOMMISSION_IMMEDIATELY"
    assert "candidate-evaluation-endpoint" in p["serving_endpoint_name"]

    # Verify automated remediation action definition
    action = next((a for a in ai_data["governance_actions"] if a["model_name"] == "candidate-biometric-evaluator"), None)
    assert action is not None
    assert action["action"] == "DECOMMISSION_IMMEDIATELY"
    assert "Article 5" in action["article"]


def test_high_risk_human_oversight_enforcement(client, navigator):
    """Verify enforcement of mandatory human-in-the-loop oversight on high-risk fraud scorer (Annex III)."""
    ai_data = navigator.analyze_ai_governance()

    high_risk = [m for m in ai_data["lineage_traces"] if m["eu_risk_tier"] == "HIGH_RISK"]
    assert len(high_risk) == 1
    h = high_risk[0]

    assert h["model_name"] == "fraud-risk-scorer-v2"
    assert h["compliance_status"] == "ACTION_REQUIRED"
    assert h["has_human_oversight"] is False
    assert h["governance_action"] == "ENFORCE_HUMAN_OVERSIGHT"
    assert "payments-fraud-scoring-endpoint" in h["serving_endpoint_name"]

    action = next((a for a in ai_data["governance_actions"] if a["model_name"] == "fraud-risk-scorer-v2"), None)
    assert action is not None
    assert action["action"] == "ENFORCE_HUMAN_OVERSIGHT"
    assert "Annex III" in action["article"]


def test_ai_model_lineage_traversal(client, navigator):
    """Verify PAM graph contains end-to-end data lineage connecting training datasets, models, and endpoints."""
    nodes = client.get_nodes()
    edges = client.get_edges()

    node_urns = {n["urn"] for n in nodes}
    edge_pairs = {(e["source_urn"], e["target_urn"], e.get("relation")) for e in edges}

    # 1. Biometric evaluator lineage
    assert "urn:ea:database:recruitment-video-corpus" in node_urns
    assert "urn:ea:aimodel:candidate-biometric-evaluator" in node_urns
    assert "urn:ea:microservice:candidate-evaluation-endpoint" in node_urns
    assert ("urn:ea:database:recruitment-video-corpus", "urn:ea:aimodel:candidate-biometric-evaluator", "trains") in edge_pairs
    assert ("urn:ea:aimodel:candidate-biometric-evaluator", "urn:ea:microservice:candidate-evaluation-endpoint", "serves") in edge_pairs

    # 2. Fraud risk scorer lineage
    assert "urn:ea:database:historical-transaction-ledger" in node_urns
    assert "urn:ea:aimodel:fraud-risk-scorer-v2" in node_urns
    assert "urn:ea:microservice:payments-fraud-scoring-endpoint" in node_urns
    assert ("urn:ea:database:historical-transaction-ledger", "urn:ea:aimodel:fraud-risk-scorer-v2", "trains") in edge_pairs
    assert ("urn:ea:aimodel:fraud-risk-scorer-v2", "urn:ea:microservice:payments-fraud-scoring-endpoint", "serves") in edge_pairs

    # 3. Customer support LLM lineage
    assert "urn:ea:database:support-ticket-kb-corpus" in node_urns
    assert "urn:ea:aimodel:customer-support-llm-v1" in node_urns
    assert "urn:ea:microservice:support-chatbot-endpoint" in node_urns
    assert ("urn:ea:database:support-ticket-kb-corpus", "urn:ea:aimodel:customer-support-llm-v1", "trains") in edge_pairs
    assert ("urn:ea:aimodel:customer-support-llm-v1", "urn:ea:microservice:support-chatbot-endpoint", "serves") in edge_pairs

    # 4. Product recommender lineage
    assert "urn:ea:database:catalog-clickstream-mart" in node_urns
    assert "urn:ea:aimodel:product-recommender-v3" in node_urns
    assert "urn:ea:microservice:storefront-recommendations-endpoint" in node_urns
    assert ("urn:ea:database:catalog-clickstream-mart", "urn:ea:aimodel:product-recommender-v3", "trains") in edge_pairs
    assert ("urn:ea:aimodel:product-recommender-v3", "urn:ea:microservice:storefront-recommendations-endpoint", "serves") in edge_pairs


def test_archify_ai_diagram_and_ui_tab13_integration(navigator):
    """Verify Archify AI lineage diagram compiles clean HTML/SVG and Tab 13 is wired into Databricks App UI."""
    diag = navigator.compile_ai_model_lineage_diagram()
    html_p = Path(diag["html_path"])
    svg_p = Path(diag["svg_path"])

    assert html_p.exists()
    assert svg_p.exists()
    assert html_p.stat().st_size > 10000
    assert svg_p.stat().st_size > 10000

    svg_content = svg_p.read_text(encoding="utf-8")
    assert "<defs>" in svg_content
    assert "<style" in svg_content

    # Verify query handling
    query_res = navigator.query("Audit AI models under EU AI Act")
    assert "EU AI Act" in query_res["answer"]
    assert "candidate-biometric-evaluator" in query_res["answer"]
    assert "fraud-risk-scorer-v2" in query_res["answer"]
    assert "customer-support-llm-v1" in query_res["answer"]
    assert "product-recommender-v3" in query_res["answer"]
    assert query_res["diagrams"]["html_path"]

    # Verify UI Tab 13 registration in apps/ea_navigator/app.py
    app_py = (ROOT_DIR / "apps" / "ea_navigator" / "app.py").read_text(encoding="utf-8")
    assert "tab_ai_governance" in app_py
    assert "🤖 AI Governance & ML Catalog (EU AI Act)" in app_py
    assert "with tab_ai_governance:" in app_py


# ==============================================================================
# STANDALONE RICH CLI RUNNER
# ==============================================================================
def main():
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]The Agentic EA — Scenario S11 Verification Suite[/bold cyan]\n"
        "[dim]AI Governance & ML Model Cataloging (EU AI Act)[/dim]",
        border_style="cyan"
    ))

    client = get_unity_catalog_client()
    navigator = EstateIntelligenceEngine()

    console.print("\n[bold yellow]Step 1: Ingested AI/ML Models (ea.bronze.ai_models)[/bold yellow]")
    models = client.get_ai_models()
    table_m = Table(title="Bronze AI Model Registry", header_style="bold magenta")
    table_m.add_column("Model ID", style="cyan")
    table_m.add_column("Model Name", style="white")
    table_m.add_column("Version", style="dim")
    table_m.add_column("Framework", style="green")
    table_m.add_column("Task Type", style="yellow")
    table_m.add_column("Owner Team", style="blue")
    for m in models:
        table_m.add_row(m["model_id"], m["model_name"], m["version"], m["framework"], m["task_type"], m["owner_team"])
    console.print(table_m)

    console.print("\n[bold yellow]Step 2: EU AI Act Risk & Compliance Audit (ea.gold.ai_governance)[/bold yellow]")
    ai_data = navigator.analyze_ai_governance()

    table_gov = Table(title="Conformed Gold AI Governance Mart", header_style="bold magenta")
    table_gov.add_column("Model ID", style="cyan")
    table_gov.add_column("Model Name", style="white")
    table_gov.add_column("Risk Tier", style="bold")
    table_gov.add_column("Compliance", style="bold")
    table_gov.add_column("Model Card", justify="center")
    table_gov.add_column("Lineage", justify="center")
    table_gov.add_column("Oversight", justify="center")
    table_gov.add_column("Governance Action", style="bold green")

    for t in ai_data["lineage_traces"]:
        tier_color = "red" if t["eu_risk_tier"] == "UNACCEPTABLE_RISK" else ("yellow" if t["eu_risk_tier"] == "HIGH_RISK" else ("cyan" if t["eu_risk_tier"] == "LIMITED_RISK" else "green"))
        status_color = "red" if t["compliance_status"] == "PROHIBITED" else ("yellow" if t["compliance_status"] == "ACTION_REQUIRED" else "green")
        card_icon = "✅" if t["has_model_card"] else "❌"
        lineage_icon = "✅" if t["has_data_lineage"] else "❌"
        oversight_icon = "✅" if t["has_human_oversight"] else "❌"

        table_gov.add_row(
            t["model_id"],
            t["model_name"],
            f"[{tier_color}]{t['eu_risk_tier']}[/{tier_color}]",
            f"[{status_color}]{t['compliance_status']}[/{status_color}]",
            card_icon,
            lineage_icon,
            oversight_icon,
            t["governance_action"],
        )
    console.print(table_gov)

    console.print("\n[bold yellow]Step 3: End-to-End AI Model Lineage Topology[/bold yellow]")
    table_lin = Table(title="PAM Graph End-to-End Lineage Traces", header_style="bold blue")
    table_lin.add_column("Training Corpus (Dataset)", style="cyan")
    table_lin.add_column("Relation", style="dim", justify="center")
    table_lin.add_column("ML Model", style="bold white")
    table_lin.add_column("Relation", style="dim", justify="center")
    table_lin.add_column("Serving Endpoint", style="magenta")

    for t in ai_data["lineage_traces"]:
        table_lin.add_row(
            t["training_dataset_name"],
            "──trains──▶",
            t["model_name"],
            "──serves──▶",
            t["serving_endpoint_name"],
        )
    console.print(table_lin)

    console.print("\n[bold yellow]Step 4: Compiling Archify Living Lineage Diagram[/bold yellow]")
    diag = navigator.compile_ai_model_lineage_diagram()
    console.print(f"✓ Interactive HTML: [green]{diag['html_path']}[/green]")
    console.print(f"✓ Styled Vector SVG: [green]{diag['svg_path']}[/green]")

    console.print("\n[bold yellow]Step 5: Automated Governance Remediation Plan[/bold yellow]")
    for act in ai_data["governance_actions"]:
        console.print(f"• [bold red]{act['action']}[/bold red] on [cyan]{act['model_name']}[/cyan] ({act['risk_tier']}):")
        console.print(f"  [dim]{act['details']}[/dim]")
        console.print(f"  [green]Remediation: {act['remediation']}[/green]")

    console.print("\n[bold green]✓ All Scenario S11 AI Governance verifications passed successfully![/bold green]\n")


if __name__ == "__main__":
    main()
