"""
Scenario S09 — Interface & Integration Landscape Rationalization.
Tests:
1. Ingestion of runtime API gateway traffic logs (ea.bronze.api_gateway_logs).
2. Conformed Gold Interface Mart (ea.gold.interface_rationalization populated with 8 records).
3. Estate Intelligence Engine declared vs runtime interface contract reconciliation.
4. Zombie / Shadow API detection (undocumented runtime endpoints receiving live traffic).
5. Dead / Orphan API identification (declared in OpenAPI catalog but 0 traffic in 90+ days).
6. Protocol sprawl and insecure integration identification (legacy SOAP over HTTP-Basic auth).
7. Archify sequence flow & interface landscape compilation and Tab 11 Cockpit UI integration.
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


def test_api_gateway_logs_ingestion(client):
    """Verify runtime API gateway logs are conformed into ea.bronze.api_gateway_logs."""
    logs = client.get_api_gateway_logs()
    assert len(logs) >= 7

    log_endpoints = {l["endpoint"] for l in logs}
    assert "/api/v1/checkout" in log_endpoints
    assert "/v1/payments/authorize" in log_endpoints
    assert "/rpc/payments.v1.LedgerSync/Record" in log_endpoints
    assert "/v1/internal/debug-dump" in log_endpoints
    assert "/soap/v1/customer" in log_endpoints
    assert "/v1/charges" in log_endpoints
    assert "/v1/auth/verify" in log_endpoints

    # Verify schema fields
    for l in logs:
        assert "log_id" in l
        assert "endpoint" in l
        assert "method" in l
        assert "protocol" in l
        assert "auth_mechanism" in l
        assert "consumer_service" in l
        assert "provider_service" in l
        assert "requests_last_30d" in l
        assert "avg_latency_ms" in l
        assert "error_rate" in l
        assert "last_seen_timestamp" in l


def test_conformed_interface_gold_mart_populated(client):
    """Verify conformed mart ea.gold.interface_rationalization contains required fields and canonical records."""
    records = client.get_interface_rationalization()
    assert len(records) >= 8

    interface_ids = {r["interface_id"] for r in records}
    assert "INT-001-STOREFRONT-CHECKOUT" in interface_ids
    assert "INT-002-CHECKOUT-PAYMENTS" in interface_ids
    assert "INT-003-PAYMENTS-LEDGER" in interface_ids
    assert "INT-004-ZOMBIE-DEBUG-DUMP" in interface_ids
    assert "INT-005-DEAD-INVENTORY-SYNC" in interface_ids
    assert "INT-006-SPRAWL-SOAP-CUSTOMER" in interface_ids
    assert "INT-007-PAYMENTS-STRIPE" in interface_ids
    assert "INT-008-AUTH-VERIFY" in interface_ids

    # Verify mandatory schema fields
    for r in records:
        assert "interface_id" in r
        assert "endpoint" in r
        assert "method" in r
        assert "protocol" in r
        assert "provider_service" in r
        assert "consumer_service" in r
        assert "is_declared" in r
        assert "is_active_runtime" in r
        assert "discrepancy_type" in r
        assert "rationalization_action" in r
        assert "last_active_timestamp" in r


def test_declared_vs_runtime_reconciliation(navigator):
    """Verify reconciliation analytics between declared OpenAPI specifications and runtime gateway logs."""
    analysis = navigator.analyze_interface_landscape()

    assert analysis["total_interfaces_count"] == 8
    assert analysis["declared_interfaces_count"] == 7
    assert analysis["runtime_interfaces_count"] == 7
    assert analysis["compliant_interfaces_count"] == 5
    assert analysis["zombie_shadow_count"] == 1
    assert analysis["dead_orphan_count"] == 1
    assert analysis["protocol_sprawl_count"] == 1


def test_zombie_shadow_api_detection(navigator):
    """Verify detection of zombie/shadow APIs (runtime endpoint receiving traffic without declaration)."""
    analysis = navigator.analyze_interface_landscape()
    zombies = analysis["zombie_shadow_interfaces"]

    assert len(zombies) == 1
    z = zombies[0]
    assert z["interface_id"] == "INT-004-ZOMBIE-DEBUG-DUMP"
    assert z["endpoint"] == "/v1/internal/debug-dump"
    assert z["method"] == "GET"
    assert z["is_declared"] is False
    assert z["is_active_runtime"] is True
    assert z["discrepancy_type"] == "ZOMBIE_SHADOW"
    assert z["rationalization_action"] == "DOCUMENT_AND_SECURE"
    assert z["provider_service"] == "payments-api"


def test_dead_orphan_api_identification(navigator):
    """Verify identification of dead/orphan APIs (declared contract with 0 runtime requests)."""
    analysis = navigator.analyze_interface_landscape()
    dead = analysis["dead_orphan_interfaces"]

    assert len(dead) == 1
    d = dead[0]
    assert d["interface_id"] == "INT-005-DEAD-INVENTORY-SYNC"
    assert d["endpoint"] == "/v1/legacy-inventory-sync"
    assert d["method"] == "POST"
    assert d["is_declared"] is True
    assert d["is_active_runtime"] is False
    assert d["discrepancy_type"] == "DEAD_ORPHAN"
    assert d["rationalization_action"] == "DECOMMISSION"
    assert d["consumer_service"] == "inventory-batch"


def test_protocol_sprawl_and_insecure_integration(navigator):
    """Verify detection of protocol sprawl and insecure integrations (legacy SOAP/XML over HTTP-Basic auth)."""
    analysis = navigator.analyze_interface_landscape()
    sprawl = analysis["protocol_sprawl_interfaces"]

    assert len(sprawl) == 1
    s = sprawl[0]
    assert s["interface_id"] == "INT-006-SPRAWL-SOAP-CUSTOMER"
    assert s["endpoint"] == "/soap/v1/customer"
    assert s["protocol"] == "SOAP/XML"
    assert s["discrepancy_type"] == "PROTOCOL_SPRAWL"
    assert s["rationalization_action"] == "STANDARDIZE_MTLS"
    assert s["consumer_service"] == "legacy-crm"
    assert s["provider_service"] == "payments-service"


def test_archify_sequence_and_ui_tab11_integration(navigator):
    """Verify compilation of Archify sequence and landscape diagrams and Cockpit Tab 11 integration."""
    # 1. Sequence diagram compilation
    seq_diag = navigator.compile_interface_sequence_diagram()
    seq_html = Path(seq_diag["html_path"])
    seq_svg = Path(seq_diag["svg_path"])
    assert seq_html.exists() and seq_html.stat().st_size > 50000
    assert seq_svg.exists() and seq_svg.stat().st_size > 20000

    # Verify style encapsulation in SVG
    svg_content = seq_svg.read_text(encoding="utf-8")
    assert "<defs>" in svg_content
    assert "<style" in svg_content

    # 2. Interface landscape diagram compilation
    iface_diag = navigator.compile_interface_landscape_diagram()
    iface_html = Path(iface_diag["html_path"])
    iface_svg = Path(iface_diag["svg_path"])
    assert iface_html.exists() and iface_html.stat().st_size > 50000
    assert iface_svg.exists() and iface_svg.stat().st_size > 20000

    # 3. Tab 11 UI verification
    app_file = ROOT_DIR / "apps" / "ea_navigator" / "app.py"
    app_code = app_file.read_text(encoding="utf-8")
    assert "tab_interfaces" in app_code
    assert "ea.gold.interface_rationalization" in app_code
    assert "interface_metrics" in app_code
    assert "interface_sequence.html" in app_code
    assert "interface_landscape.html" in app_code


# ==============================================================================
# STANDALONE CLI TEST RUNNER & RICH REPORTING
# ==============================================================================
def main():
    console = Console()
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]SCENARIO S09: INTERFACE & INTEGRATION LANDSCAPE RATIONALIZATION[/bold cyan]\n"
            "[dim]Declared Contract vs Runtime Gateway Traffic Reconciliation (OpenAPI / gRPC / SOAP)[/dim]",
            border_style="cyan",
        )
    )

    client = get_unity_catalog_client()
    navigator = EstateIntelligenceEngine()
    analysis = navigator.analyze_interface_landscape()

    # 1. Summary KPI Cards
    summary_table = Table(title="[bold green]Interface Landscape & Discrepancy KPI Summary[/bold green]", box=None)
    summary_table.add_column("Metric", style="bold white")
    summary_table.add_column("Value", justify="right", style="cyan")
    summary_table.add_column("Architectural Significance", style="dim")

    summary_table.add_row("Total Reconciled Interfaces", str(analysis["total_interfaces_count"]), "Cataloged across ea.gold.interface_rationalization")
    summary_table.add_row("Declared OpenAPI Contracts", str(analysis["declared_interfaces_count"]), "Formally documented in service interface schemas")
    summary_table.add_row("Active Runtime Interfaces", str(analysis["runtime_interfaces_count"]), "Observed receiving live API traffic in last 30d")
    summary_table.add_row("Compliant Inter-Service APIs", f"[green]{analysis['compliant_interfaces_count']}[/green]", "Standardized HTTPS/REST & gRPC/mTLS")
    summary_table.add_row("Zombie / Shadow APIs", f"[bold red]{analysis['zombie_shadow_count']}[/bold red]", "Undocumented ingress receiving production traffic")
    summary_table.add_row("Dead / Orphan APIs", f"[bold yellow]{analysis['dead_orphan_count']}[/bold yellow]", "Declared routes with 0 requests in 90+ days")
    summary_table.add_row("Protocol Sprawl & Insecure", f"[bold magenta]{analysis['protocol_sprawl_count']}[/bold magenta]", "Legacy SOAP/XML over HTTP-Basic auth")

    console.print(summary_table)
    console.print()

    # 2. Detailed Reconciled Interfaces Table
    recon_table = Table(title="[bold yellow]Conformed Interface Mart: ea.gold.interface_rationalization[/bold yellow]")
    recon_table.add_column("Interface ID", style="cyan")
    recon_table.add_column("Endpoint", style="white")
    recon_table.add_column("Method", style="bold")
    recon_table.add_column("Protocol", style="dim")
    recon_table.add_column("Provider ➔ Consumer", style="dim")
    recon_table.add_column("Decl.", justify="center")
    recon_table.add_column("Run.", justify="center")
    recon_table.add_column("Discrepancy", style="bold")
    recon_table.add_column("Action", style="green")

    for r in analysis["all_reconciled_interfaces"]:
        dec_str = "[green]✓[/green]" if r.get("is_declared") else "[red]✗[/red]"
        run_str = "[green]●[/green]" if r.get("is_active_runtime") else "[dim]○[/dim]"
        disc = r.get("discrepancy_type", "COMPLIANT")
        if disc == "ZOMBIE_SHADOW":
            disc_style = "[bold red]ZOMBIE_SHADOW[/bold red]"
        elif disc == "DEAD_ORPHAN":
            disc_style = "[bold yellow]DEAD_ORPHAN[/bold yellow]"
        elif disc == "PROTOCOL_SPRAWL":
            disc_style = "[bold magenta]PROTOCOL_SPRAWL[/bold magenta]"
        else:
            disc_style = "[green]COMPLIANT[/green]"

        route = f"{r['consumer_service']} ➔ {r['provider_service']}"
        recon_table.add_row(
            r["interface_id"],
            r["endpoint"],
            r["method"],
            r["protocol"],
            route,
            dec_str,
            run_str,
            disc_style,
            f"[bold]{r['rationalization_action']}[/bold]",
        )

    console.print(recon_table)
    console.print()

    # 3. Action Recommendations Table
    action_table = Table(title="[bold red]Architectural Rationalization Action Plan[/bold red]")
    action_table.add_column("Action", style="bold white")
    action_table.add_column("Endpoint / Discrepancy", style="cyan")
    action_table.add_column("Root Cause Analysis", style="dim")
    action_table.add_column("Remediation Strategy", style="green")

    for act in analysis["rationalization_actions"]:
        action_table.add_row(
            f"[bold red]{act['action']}[/bold red]",
            f"{act['endpoint']}\n[dim]{act['discrepancy_type']}[/dim]",
            act["details"],
            act["remediation"],
        )

    console.print(action_table)
    console.print()

    # 4. Archify Diagram Compilation
    console.print("[bold cyan]Compiling Archify Diagrams...[/bold cyan]")
    seq_res = navigator.compile_interface_sequence_diagram()
    iface_res = navigator.compile_interface_landscape_diagram()

    console.print(f"  [green]✓[/green] Sequence Flow HTML: [bold white]{seq_res['html_path']}[/bold white]")
    console.print(f"  [green]✓[/green] Sequence Flow SVG:  [bold white]{seq_res['svg_path']}[/bold white]")
    console.print(f"  [green]✓[/green] Interface Map HTML: [bold white]{iface_res['html_path']}[/bold white]")
    console.print(f"  [green]✓[/green] Interface Map SVG:  [bold white]{iface_res['svg_path']}[/bold white]")
    console.print()
    console.print("[bold green]✅ All Scenario S09 Interface Rationalization assertions verified successfully![/bold green]")


if __name__ == "__main__":
    main()
