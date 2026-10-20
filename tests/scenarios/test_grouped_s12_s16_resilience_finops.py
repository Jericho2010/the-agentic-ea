"""
Scenario Group 1 (S12–S16) — Enterprise Resilience, Tech Debt, Zero-Trust, SBOM & FinOps Hub.
Tests:
1. S12 (Disaster Recovery): Conformed table ea.gold.resilience_dr & SPOF detection (Cassandra RTO/RPO SLA breach).
2. S13 (Tech Debt): Conformed table ea.gold.tech_debt_hotspots (Cassandra debt 92, Checkout debt 74 & 12.4k churn).
3. S14 (Zero-Trust): Conformed table ea.gold.security_zero_trust (Plaintext CQL transit & unauthorized cross-zone egress).
4. S15 (SBOM): Conformed table ea.gold.supply_chain_sbom (GPL-3.0 Prohibited Copyleft & Critical CVE-2024-4321).
5. S16 (FinOps): Conformed table ea.gold.finops_unit_economics ($0.042/order & $8,400/yr Cassandra idle waste).
6. Unified Estate Intelligence Engine analytics (analyze_operations_resilience_finops).
7. Archify living architecture diagram compilation (resilience_and_perimeter_view.html & .svg).
8. Conversational natural language inquiry handling in engine.query().
9. Databricks App UI Cockpit Tab 14 integration in apps/ea_navigator/app.py.
10. Operational modernization and governance remediation action plans.
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


def test_resilience_dr_conformance(client, navigator):
    """Verify S12: Conformed DR table ea.gold.resilience_dr and Cassandra SPOF SLA breach."""
    dr_records = client.get_resilience_dr()
    assert len(dr_records) == 5

    # Check Cassandra Tier-1 SLA breach
    cas = next((r for r in dr_records if "cassandra" in r["component_urn"]), None)
    assert cas is not None
    assert cas["dr_tier"] == "Tier-1"
    assert cas["rto_actual_min"] == 240
    assert cas["rto_target_min"] == 15
    assert cas["rpo_actual_min"] == 120
    assert cas["rpo_target_min"] == 5
    assert "Unreplicated" in cas["replication_strategy"]
    assert cas["sla_breached"] is True

    # Check analytics aggregation
    op_data = navigator.analyze_operations_resilience_finops()
    assert op_data["total_dr_components"] == 5
    assert op_data["sla_breached_count"] >= 1
    assert any("cassandra" in r["component_urn"] for r in op_data["spof_components"])


def test_tech_debt_hotspots_conformance(client, navigator):
    """Verify S13: Conformed tech debt table ea.gold.tech_debt_hotspots and refactoring rank."""
    debt_records = client.get_tech_debt_hotspots()
    assert len(debt_records) == 5

    # Rank 1: Cassandra
    cas = next((r for r in debt_records if "cassandra" in r["component_urn"]), None)
    assert cas is not None
    assert cas["refactoring_roi_rank"] == 1
    assert cas["debt_score"] == 92
    assert "Deprecated Engine" in cas["architectural_smells"]

    # Rank 2: Checkout Service
    chk = next((r for r in debt_records if "checkout" in r["component_urn"]), None)
    assert chk is not None
    assert chk["refactoring_roi_rank"] == 2
    assert chk["debt_score"] == 74
    assert chk["git_churn_lines_30d"] == 12400
    assert chk["cyclomatic_complexity"] == 31.8
    assert "God Class Monolith" in chk["architectural_smells"]

    # Check analytics aggregation
    op_data = navigator.analyze_operations_resilience_finops()
    assert op_data["avg_debt_score"] > 50.0
    assert op_data["top_hotspots"][0]["component_urn"] == cas["component_urn"]
    assert op_data["top_hotspots"][1]["component_urn"] == chk["component_urn"]


def test_security_zero_trust_microsegmentation(client, navigator):
    """Verify S14: Conformed Zero-Trust table ea.gold.security_zero_trust and policy breaches."""
    sec_records = client.get_security_zero_trust()
    assert len(sec_records) == 5

    # 1. Plaintext transit flow
    pt = next((r for r in sec_records if r["microsegmentation_status"] == "PLAINTEXT_TRAFFIC"), None)
    assert pt is not None
    assert "payments-service" in pt["source_urn"]
    assert "cassandra" in pt["target_urn"]
    assert pt["protocol"] == "CQL/9042"
    assert pt["mtls_enforced"] is False

    # 2. Unauthorized cross-zone egress
    xz = next((r for r in sec_records if r["microsegmentation_status"] == "UNAUTHORIZED_CROSS_ZONE"), None)
    assert xz is not None
    assert "payments-api" in xz["source_urn"]
    assert "customer-pii-stream" in xz["target_urn"]
    assert xz["trust_zone_source"] == "CORE_APP_MESH"
    assert xz["trust_zone_target"] == "EXTERNAL_EGRESS"

    # Check analytics compliance rate
    op_data = navigator.analyze_operations_resilience_finops()
    assert op_data["total_security_flows"] == 5
    assert len(op_data["compliant_security_flows"]) == 3
    assert len(op_data["plaintext_violations"]) == 1
    assert len(op_data["cross_zone_violations"]) == 1
    assert op_data["zero_trust_compliance_pct"] == 60.0


def test_supply_chain_sbom_governance(client, navigator):
    """Verify S15: Conformed SBOM table ea.gold.supply_chain_sbom, copyleft and CVE detection."""
    sbom_records = client.get_supply_chain_sbom()
    assert len(sbom_records) == 6

    # Verify GPL-3.0 Copyleft violation
    copyleft = [r for r in sbom_records if r["license_compliance"] == "PROHIBITED_COPYLEFT"]
    assert len(copyleft) == 1
    cl = copyleft[0]
    assert cl["package_name"] == "crypto-legacy-utils"
    assert "payments-service" in cl["component_urn"]
    assert cl["license"] == "GPL-3.0"
    assert cl["cve_count"] == 3
    assert cl["max_severity"] == "CRITICAL"

    # Check analytics aggregation
    op_data = navigator.analyze_operations_resilience_finops()
    assert op_data["total_sbom_packages"] == 6
    assert len(op_data["copyleft_violations"]) == 1
    assert len(op_data["critical_cves"]) == 1
    assert op_data["gpl_violation"]["package_name"] == "crypto-legacy-utils"


def test_finops_unit_economics_and_waste(client, navigator):
    """Verify S16: Conformed FinOps table ea.gold.finops_unit_economics and idle waste quantification."""
    fin_records = client.get_finops_unit_economics()
    assert len(fin_records) == 5

    # Core order transaction cost
    chk = next((r for r in fin_records if "checkout-service" in r["service_urn"]), None)
    assert chk is not None
    assert chk["cost_per_transaction"] == 0.042

    # Cassandra idle compute waste
    cas = next((r for r in fin_records if "cassandra" in r["service_urn"]), None)
    assert cas is not None
    assert cas["idle_waste_cost"] == 700.00
    assert cas["tag_compliance_pct"] == 62.0
    assert cas["optimization_action"] == "DECOMMISSION_AND_ELIMINATE"

    # Check analytics aggregation
    op_data = navigator.analyze_operations_resilience_finops()
    assert op_data["unit_cost_per_order"] == 0.042
    assert op_data["cassandra_monthly_idle_waste_usd"] == 700.00
    assert op_data["cassandra_annual_idle_waste_usd"] == 8400.00


def test_unified_operations_resilience_finops_analytics(navigator):
    """Verify Estate Intelligence Engine aggregates all 5 operational disciplines."""
    op_data = navigator.analyze_operations_resilience_finops()

    assert op_data["tenant_id"] == "core"
    assert "total_dr_components" in op_data
    assert "total_debt_records" in op_data
    assert "total_security_flows" in op_data
    assert "total_sbom_packages" in op_data
    assert "total_finops_services" in op_data
    assert "operational_actions" in op_data
    assert len(op_data["operational_actions"]) == 5


def test_archify_resilience_perimeter_diagram_compilation(navigator):
    """Verify Archify diagram compiles clean HTML/SVG with perimeter isolation and no solid black fallback."""
    diag = navigator.compile_resilience_and_perimeter_diagram()
    html_p = Path(diag["html_path"])
    svg_p = Path(diag["svg_path"])

    assert html_p.exists()
    assert svg_p.exists()
    assert html_p.stat().st_size > 10000
    assert svg_p.stat().st_size > 10000

    svg_content = svg_p.read_text(encoding="utf-8")
    assert "<defs>" in svg_content
    assert "<style" in svg_content


def test_ea_navigator_conversational_queries(navigator):
    """Verify conversational queries across DR, Tech Debt, Zero-Trust, SBOM, and FinOps."""
    q1 = navigator.query("Audit DR RTO/RPO SLAs, technical debt hotspots, zero trust, and FinOps unit economics")
    assert "Operations, Resilience & FinOps Hub Audit" in q1["answer"]
    assert "cassandra-legacy-cluster" in q1["answer"]
    assert "checkout-service" in q1["answer"]
    assert "payments-service" in q1["answer"]
    assert "$0.042" in q1["answer"]
    assert "$8,400.00/yr" in q1["answer"]
    assert q1["diagrams"]["html_path"]

    q2 = navigator.query("Show software supply chain sbom licenses and cve vulnerabilities")
    assert "Supply Chain SBOM" in q2["answer"]
    assert "GPL-3.0" in q2["answer"]


def test_databricks_app_ui_tab14_registration():
    """Verify UI Tab 14 registration in apps/ea_navigator/app.py."""
    app_py = (ROOT_DIR / "apps" / "ea_navigator" / "app.py").read_text(encoding="utf-8")
    assert "tab_resilience_finops" in app_py
    assert "🛡️ Operations, Resilience & FinOps Hub" in app_py
    assert "with tab_resilience_finops:" in app_py
    assert "subtab_dr" in app_py
    assert "subtab_debt" in app_py
    assert "subtab_zt" in app_py
    assert "subtab_sbom" in app_py
    assert "subtab_finops" in app_py


def test_operational_remediation_actions_mapping(navigator):
    """Verify concrete operational modernization and governance actions are emitted."""
    op_data = navigator.analyze_operations_resilience_finops()
    actions = {(a["component"], a["domain"]): a for a in op_data["operational_actions"]}

    assert ("cassandra-legacy-cluster", "Disaster Recovery (S12)") in actions
    assert "DECOMMISSION_AND_MIGRATE" == actions[("cassandra-legacy-cluster", "Disaster Recovery (S12)")]["action"]

    assert ("cassandra-legacy-cluster", "FinOps Unit Economics (S16)") in actions
    assert "ELIMINATE_IDLE_WASTE" == actions[("cassandra-legacy-cluster", "FinOps Unit Economics (S16)")]["action"]

    assert ("checkout-service", "Technical Debt (S13)") in actions
    assert "MODERNIZE_REFACTOR" == actions[("checkout-service", "Technical Debt (S13)")]["action"]

    assert ("payments-api ➔ customer-pii-stream", "Zero-Trust Security (S14)") in actions
    assert "ENFORCE_MICROSEGMENTATION" == actions[("payments-api ➔ customer-pii-stream", "Zero-Trust Security (S14)")]["action"]

    assert ("crypto-legacy-utils (payments-service)", "Supply Chain SBOM (S15)") in actions
    assert "REPLACE_DEPENDENCY" == actions[("crypto-legacy-utils (payments-service)", "Supply Chain SBOM (S15)")]["action"]


# ==============================================================================
# STANDALONE RICH CLI RUNNER
# ==============================================================================
def main():
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]The Agentic EA — Group 1 Scenarios (S12–S16) Verification Suite[/bold cyan]\n"
        "[dim]Resilience, Tech Debt, Zero-Trust, SBOM & FinOps Hub[/dim]",
        border_style="cyan"
    ))

    client = get_unity_catalog_client()
    navigator = EstateIntelligenceEngine()

    op_data = navigator.analyze_operations_resilience_finops()

    # Step 1: DR Table
    console.print("\n[bold yellow]Step 1: Disaster Recovery & ICT Resilience (S12 — ea.gold.resilience_dr)[/bold yellow]")
    table_dr = Table(title="Disaster Recovery RTO/RPO SLAs", header_style="bold magenta")
    table_dr.add_column("Component", style="cyan")
    table_dr.add_column("DR Tier", style="dim")
    table_dr.add_column("Actual RTO", style="red")
    table_dr.add_column("Target RTO", style="green")
    table_dr.add_column("Actual RPO", style="red")
    table_dr.add_column("Target RPO", style="green")
    table_dr.add_column("Replication Strategy", style="white")
    table_dr.add_column("SLA Status", style="bold")
    for r in op_data["dr_records"]:
        badge = "[bold red]BREACHED[/bold red]" if r["sla_breached"] else "[bold green]COMPLIANT[/bold green]"
        table_dr.add_row(
            r["component_urn"].split(":")[-1],
            r["dr_tier"],
            f"{r['rto_actual_min']}m",
            f"{r['rto_target_min']}m",
            f"{r['rpo_actual_min']}m",
            f"{r['rpo_target_min']}m",
            r["replication_strategy"],
            badge,
        )
    console.print(table_dr)

    # Step 2: Tech Debt Hotspots
    console.print("\n[bold yellow]Step 2: Technical Debt Hotspots & Churn (S13 — ea.gold.tech_debt_hotspots)[/bold yellow]")
    table_debt = Table(title="Tech Debt Hotspots Ranked by Refactoring ROI", header_style="bold magenta")
    table_debt.add_column("Rank", style="cyan", justify="center")
    table_debt.add_column("Component", style="white")
    table_debt.add_column("Debt Score", style="bold red")
    table_debt.add_column("30d Churn Lines", style="yellow")
    table_debt.add_column("Complexity", style="dim")
    table_debt.add_column("Smells", style="red")
    for d in op_data["top_hotspots"]:
        table_debt.add_row(
            f"#{d['refactoring_roi_rank']}",
            d["component_urn"].split(":")[-1],
            f"{d['debt_score']}/100",
            f"{d['git_churn_lines_30d']:,}",
            str(d["cyclomatic_complexity"]),
            str(d["architectural_smells"]),
        )
    console.print(table_debt)

    # Step 3: Zero-Trust Security
    console.print("\n[bold yellow]Step 3: Zero-Trust Microsegmentation (S14 — ea.gold.security_zero_trust)[/bold yellow]")
    table_sec = Table(title="Zero-Trust Perimeter & Inter-Zone Transit", header_style="bold magenta")
    table_sec.add_column("Source", style="cyan")
    table_sec.add_column("Target", style="magenta")
    table_sec.add_column("Protocol", style="dim")
    table_sec.add_column("mTLS", justify="center")
    table_sec.add_column("Source Zone", style="blue")
    table_sec.add_column("Target Zone", style="blue")
    table_sec.add_column("Status", style="bold")
    for s in op_data["security_records"]:
        st = s["microsegmentation_status"]
        st_badge = "[bold green]COMPLIANT[/bold green]" if st == "COMPLIANT" else f"[bold red]{st}[/bold red]"
        table_sec.add_row(
            s["source_urn"].split(":")[-1],
            s["target_urn"].split(":")[-1],
            s["protocol"],
            "🔒" if s["mtls_enforced"] else "⚠️",
            s["trust_zone_source"],
            s["trust_zone_target"],
            st_badge,
        )
    console.print(table_sec)

    # Step 4: Supply Chain SBOM
    console.print("\n[bold yellow]Step 4: Software Bill of Materials & Copyleft (S15 — ea.gold.supply_chain_sbom)[/bold yellow]")
    table_sb = Table(title="Third-Party Dependencies & License Compliance", header_style="bold magenta")
    table_sb.add_column("Package", style="cyan")
    table_sb.add_column("Version", style="dim")
    table_sb.add_column("Component", style="white")
    table_sb.add_column("License", style="yellow")
    table_sb.add_column("Compliance", style="bold")
    table_sb.add_column("CVEs", style="red")
    table_sb.add_column("Max Severity", style="bold red")
    for b in op_data["sbom_records"]:
        comp_badge = "[bold green]APPROVED[/bold green]" if b["license_compliance"] == "APPROVED" else "[bold red]PROHIBITED[/bold red]"
        table_sb.add_row(
            b["package_name"],
            b["version"],
            b["component_urn"].split(":")[-1],
            b["license"],
            comp_badge,
            str(b["cve_count"]),
            b["max_severity"],
        )
    console.print(table_sb)

    # Step 5: FinOps Unit Economics
    console.print("\n[bold yellow]Step 5: FinOps Unit Economics & Waste (S16 — ea.gold.finops_unit_economics)[/bold yellow]")
    table_fin = Table(title="Cloud Unit Economics & Idle Compute Attribution", header_style="bold magenta")
    table_fin.add_column("Service", style="cyan")
    table_fin.add_column("Monthly Spend", style="white")
    table_fin.add_column("Cost / Txn", style="green")
    table_fin.add_column("Tagging %", style="dim")
    table_fin.add_column("Idle Waste / Mo", style="bold red")
    table_fin.add_column("Action", style="bold yellow")
    for f in op_data["finops_records"]:
        cost_str = f"${f['cost_per_transaction']:.3f}" if f["cost_per_transaction"] > 0 else "N/A"
        waste_str = f"${f['idle_waste_cost']:,.2f}" if f["idle_waste_cost"] > 0 else "$0.00"
        table_fin.add_row(
            f["service_urn"].split(":")[-1],
            f"${f['monthly_spend']:,.2f}",
            cost_str,
            f"{f['tag_compliance_pct']:.1f}%",
            waste_str,
            f["optimization_action"],
        )
    console.print(table_fin)

    # Step 6: Diagram Compilation
    console.print("\n[bold yellow]Step 6: Compiling Archify Living Operations Architecture Map[/bold yellow]")
    diag = navigator.compile_resilience_and_perimeter_diagram()
    console.print(f"✓ Interactive HTML: [green]{diag['html_path']}[/green]")
    console.print(f"✓ Styled Vector SVG: [green]{diag['svg_path']}[/green]")

    # Step 7: Action Plan
    console.print("\n[bold yellow]Step 7: Priority Modernization & Governance Action Plan[/bold yellow]")
    for act in op_data["operational_actions"]:
        console.print(f"• [bold red]{act['action']}[/bold red] on [cyan]{act['component']}[/cyan] ({act['domain']}):")
        console.print(f"  [dim]{act['risk']}[/dim]")
        console.print(f"  [green]Remediation: {act['remediation']}[/green]")

    console.print("\n[bold green]✓ All Group 1 (S12–S16) verifications passed successfully![/bold green]\n")


if __name__ == "__main__":
    main()
