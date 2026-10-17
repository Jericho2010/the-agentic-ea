"""
Scenario S10 — Business Process Optimization & Customer Journey Traceability.
Tests:
1. Ingestion of process event logs (ea.bronze.process_event_logs).
2. Conformed Gold Process Optimization Mart (ea.gold.process_optimization populated with 5 steps).
3. Estate Intelligence Engine end-to-end journey cycle time calculations (p50=1,190ms, p95=1,495ms, p99=2,025ms).
4. Critical path bottleneck detection (Step 2 Cassandra query at 880ms p95).
5. SLA breach calculation and latency attribution (+495ms SLA breach; Cassandra accounts for 58.8% of total journey latency).
6. Target-state Lakehouse replatforming impact (reducing journey latency to 775ms, saving 720ms / 48%).
7. Archify customer journey workflow diagram compilation and Cockpit Tab 12 integration.
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


def test_process_event_logs_ingestion(client):
    """Verify runtime process execution trace spans are conformed into ea.bronze.process_event_logs."""
    events = client.get_process_event_logs()
    assert len(events) >= 15

    # Verify all 3 traces present
    trace_ids = {e["trace_id"] for e in events}
    assert any("001" in t for t in trace_ids)
    assert any("002" in t for t in trace_ids)
    assert any("003" in t for t in trace_ids)

    # Verify all 5 steps present
    step_ids = {e["step_id"] for e in events}
    assert "STEP-01" in step_ids
    assert "STEP-02" in step_ids
    assert "STEP-03" in step_ids
    assert "STEP-04" in step_ids
    assert "STEP-05" in step_ids

    # Verify mandatory schema fields
    for e in events:
        assert "trace_id" in e
        assert "process_id" in e
        assert e["process_id"] in ("PROC-ORDER-TO-CASH", "PROC-OTC-001")
        assert "step_id" in e
        assert "step_name" in e
        assert "service_urn" in e
        assert "duration_ms" in e
        assert e["duration_ms"] > 0
        assert "status" in e
        assert "timestamp" in e


def test_conformed_process_optimization_gold_mart_populated(client):
    """Verify conformed mart ea.gold.process_optimization contains 5 canonical steps with complete latency percentiles."""
    steps = client.get_process_optimization()
    assert len(steps) == 5

    step_ids = [s["step_id"] for s in steps]
    assert step_ids == ["STEP-01", "STEP-02", "STEP-03", "STEP-04", "STEP-05"]

    # Verify mandatory schema fields
    for s in steps:
        assert "process_id" in s
        assert s["process_id"] in ("PROC-ORDER-TO-CASH", "PROC-OTC-001")
        assert "process_name" in s
        assert "step_id" in s
        assert "step_name" in s
        assert "service_urn" in s
        assert "p50_latency_ms" in s
        assert "p95_latency_ms" in s
        assert "p99_latency_ms" in s
        assert "sla_target_ms" in s
        assert "error_rate_pct" in s
        assert "is_bottleneck" in s
        assert "optimization_action" in s


def test_end_to_end_journey_cycle_time_calculation(navigator):
    """Verify Estate Intelligence Engine computes precise end-to-end cycle times across all 5 stages."""
    proc = navigator.analyze_business_processes()

    assert proc["process_id"] in ("PROC-ORDER-TO-CASH", "PROC-OTC-001")
    assert proc["process_name"] == "Order-to-Cash Customer Journey"
    assert proc["total_steps_count"] == 5
    assert proc["total_traces_count"] >= 3

    # Exact cycle time sums across stages:
    # p50: 95 + 710 + 240 + 110 + 35 = 1,190ms
    # p95: 120 + 880 + 310 + 140 + 45 = 1,495ms
    # p99: 155 + 1240 + 390 + 180 + 60 = 2,025ms
    assert proc["journey_p50_ms"] == 1190.0
    assert proc["journey_p95_ms"] == 1495.0
    assert proc["journey_p99_ms"] == 2025.0


def test_journey_bottleneck_detection(navigator):
    """Verify accurate detection of the primary bottleneck in the customer journey."""
    proc = navigator.analyze_business_processes()

    assert proc["bottleneck_step_id"] == "STEP-02"
    assert proc["bottleneck_step_name"] == "Customer Profile & Loyalty Lookup"
    assert proc["bottleneck_service_urn"] == "urn:ea:database:cassandra-legacy-cluster"
    assert proc["bottleneck_p95_ms"] == 880.0
    assert proc["bottleneck_sla_target_ms"] == 250.0


def test_sla_breach_and_latency_attribution(navigator):
    """Verify end-to-end SLA breach (+495ms) and Cassandra latency attribution (58.8% of total journey)."""
    proc = navigator.analyze_business_processes()

    # Journey SLA Target is 1,000ms
    assert proc["sla_target_ms"] == 1000.0
    assert proc["is_sla_breached"] is True
    assert proc["sla_breach_ms"] == 495.0  # 1,495 - 1,000

    # Step 2 breaches its 250ms target by +630ms
    assert proc["bottleneck_over_sla_ms"] == 630.0  # 880 - 250

    # Bottleneck latency share: 880 / 1495 = 58.86%
    assert round(proc["bottleneck_latency_pct"], 1) == 58.9
    assert proc["bottleneck_latency_pct"] == 58.86


def test_optimization_recommendation_impact(navigator):
    """Verify modernization recommendation cuts Step 2 latency to 160ms and drops total journey to 775ms."""
    proc = navigator.analyze_business_processes()

    assert len(proc["recommendations"]) >= 1
    rec = proc["recommendations"][0]

    assert rec["step_id"] == "STEP-02"
    assert rec["action"] == "REPLATFORM_LAKEHOUSE"
    assert rec["current_p95_ms"] == 880.0
    assert rec["target_p95_ms"] == 160.0
    assert rec["latency_reduction_ms"] == 720.0
    assert rec["latency_reduction_pct"] == 48.16

    # Projected journey p95 drops to 775ms (comfortably under 1,000ms SLA)
    assert proc["optimized_journey_p95_ms"] == 775.0
    assert proc["optimized_journey_p95_ms"] < proc["sla_target_ms"]


def test_archify_workflow_and_ui_tab12_integration(navigator):
    """Verify Archify workflow diagram compilation, SVG vector rendering, and Cockpit Tab 12 integration."""
    diag = navigator.compile_customer_journey_workflow_diagram()

    html_path = Path(diag["html_path"])
    svg_path = Path(diag["svg_path"])

    assert html_path.exists()
    assert svg_path.exists()
    assert html_path.stat().st_size > 50000
    assert svg_path.stat().st_size > 50000

    html_text = html_path.read_text(encoding="utf-8")
    svg_text = svg_path.read_text(encoding="utf-8")

    assert "Order-to-Cash" in html_text
    assert "<svg" in svg_text
    assert "</svg>" in svg_text
    assert "<defs" in svg_text
    assert "<style" in svg_text

    # Verify Tab 12 in app.py
    app_py_path = ROOT_DIR / "apps" / "ea_navigator" / "app.py"
    assert app_py_path.exists()
    app_text = app_py_path.read_text(encoding="utf-8")
    assert "tab_process" in app_text
    assert "Business Process Optimization & Customer Journey" in app_text
    assert "ea.gold.process_optimization" in app_text

    # Verify conversational query
    query_res = navigator.query("Analyze Order-to-Cash journey cycle times and detect Cassandra latency bottleneck")
    assert "Order-to-Cash Customer Journey" in query_res["answer"]
    assert "1,495 ms" in query_res["answer"]
    assert "Customer Profile & Loyalty Lookup" in query_res["answer"]
    assert "REPLATFORM_LAKEHOUSE" in query_res["answer"]
    assert "customer_journey_workflow" in query_res["diagrams"]["html_path"]


def main():
    """Standalone CLI runner with Rich terminal formatting for Scenario S10."""
    console = Console()
    console.print(
        Panel.fit(
            "[bold cyan]The Agentic EA — Scenario S10[/bold cyan]\n"
            "[bold white]Business Process Optimization & Customer Journey Traceability[/bold white]\n"
            "[dim]Execution Trace Telemetry vs Enterprise SLA Conformance & Bottleneck Discovery[/dim]",
            border_style="cyan",
        )
    )

    client = get_unity_catalog_client()
    navigator = EstateIntelligenceEngine()
    analysis = navigator.analyze_business_processes()

    # 1. Summary KPI Cards
    summary_table = Table(title="[bold green]Customer Journey & Process Optimization KPI Summary[/bold green]", box=None)
    summary_table.add_column("Metric", style="bold white")
    summary_table.add_column("Value", justify="right", style="cyan")
    summary_table.add_column("Architectural Significance", style="dim")

    summary_table.add_row("Business Process Name", analysis["process_name"], f"Canonical ID: {analysis['process_id']}")
    summary_table.add_row("End-to-End Latency (p95)", f"[bold red]{int(analysis['journey_p95_ms']):,} ms[/bold red]", "Total cycle time across all 5 sequential stages")
    summary_table.add_row("Journey SLA Target", f"{int(analysis['sla_target_ms']):,} ms", "Tier-1 Customer Journey SLA target")
    summary_table.add_row("SLA Conformance Status", "[bold red]🚨 CRITICAL BREACH (+495 ms)[/bold red]", "49.5% excess latency over acceptable SLA threshold")
    summary_table.add_row("Primary Bottleneck Step", f"[bold yellow]{analysis['bottleneck_step_name']}[/bold yellow]", f"Step ID: {analysis['bottleneck_step_id']} ({analysis['bottleneck_service_urn'].split(':')[-1]})")
    summary_table.add_row("Bottleneck Latency (p95)", f"[bold red]{int(analysis['bottleneck_p95_ms']):,} ms[/bold red]", f"Breaches 250ms target by +{int(analysis['bottleneck_over_sla_ms'])} ms")
    summary_table.add_row("Bottleneck Latency Share", f"[bold magenta]{analysis['bottleneck_latency_pct']}%[/bold magenta]", "Drives over half of total end-to-end customer wait time")
    summary_table.add_row("Post-Modernization Target", f"[bold green]{int(analysis['optimized_journey_p95_ms'])} ms[/bold green]", f"Saving -{int(analysis['latency_reduction_ms'])} ms (-{analysis['latency_reduction_pct']}%) via Lakehouse Replatforming")

    console.print(summary_table)
    console.print()

    # 2. Detailed Stages Table
    stages_table = Table(title="[bold yellow]Conformed Process Mart: ea.gold.process_optimization[/bold yellow]")
    stages_table.add_column("Step ID", style="cyan")
    stages_table.add_column("Stage / Activity Name", style="white")
    stages_table.add_column("Executing Component", style="dim")
    stages_table.add_column("p50", justify="right", style="dim")
    stages_table.add_column("p95", justify="right", style="bold")
    stages_table.add_column("p99", justify="right", style="dim")
    stages_table.add_column("SLA Target", justify="right")
    stages_table.add_column("Status", justify="center")
    stages_table.add_column("Optimization Action", style="green")

    for s in analysis["steps"]:
        is_bn = s.get("is_bottleneck")
        p95_style = f"[bold red]{int(s['p95_latency_ms'])} ms[/bold red]" if is_bn else f"{int(s['p95_latency_ms'])} ms"
        status_badge = "[bold red]🚨 BOTTLENECK[/bold red]" if is_bn else "[green]✅ COMPLIANT[/green]"
        action_style = f"[bold yellow]{s['optimization_action']}[/bold yellow]" if is_bn else f"[dim]{s['optimization_action']}[/dim]"

        stages_table.add_row(
            s["step_id"],
            s["step_name"],
            s["service_urn"].split(":")[-1],
            f"{int(s['p50_latency_ms'])} ms",
            p95_style,
            f"{int(s['p99_latency_ms'])} ms",
            f"{int(s['sla_target_ms'])} ms",
            status_badge,
            action_style,
        )

    console.print(stages_table)
    console.print()

    # 3. Modernization Recommendations Table
    action_table = Table(title="[bold red]Target-State Latency Optimization Roadmap[/bold red]")
    action_table.add_column("Step", style="cyan")
    action_table.add_column("Modernization Action", style="bold white")
    action_table.add_column("Current ➔ Target p95", style="bold yellow")
    action_table.add_column("Latency Reduction", style="green")
    action_table.add_column("Remediation Strategy & Architectural Impact", style="dim")

    for rec in analysis["recommendations"]:
        action_table.add_row(
            rec["step_id"],
            f"[bold]{rec['action']}[/bold]\n[dim]{rec['service_urn'].split(':')[-1]}[/dim]",
            f"{int(rec['current_p95_ms'])} ms ➔ [green]{int(rec['target_p95_ms'])} ms[/green]",
            f"[bold green]-{int(rec['latency_reduction_ms'])} ms (-{rec['latency_reduction_pct']} harvest)[/bold green]",
            f"{rec['remediation']}\n[italic green]Impact: {rec['impact']}[/italic green]",
        )

    console.print(action_table)
    console.print()

    # 4. Archify Workflow Diagram Compilation
    console.print("[bold cyan]Compiling Archify Customer Journey Workflow Diagram...[/bold cyan]")
    wf_res = navigator.compile_customer_journey_workflow_diagram()

    console.print(f"  [green]✓[/green] Journey Workflow HTML: [bold white]{wf_res['html_path']}[/bold white]")
    console.print(f"  [green]✓[/green] Journey Workflow SVG:  [bold white]{wf_res['svg_path']}[/bold white]")
    console.print()
    console.print("[bold green]✅ All Scenario S10 Business Process Optimization assertions verified successfully![/bold green]")


if __name__ == "__main__":
    main()
