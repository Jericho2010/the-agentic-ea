"""
The Agentic EA Platform - MVP Entrypoint.
Autonomous closed-loop Enterprise Architecture Platform native to Databricks.
Target Databricks Workspace: https://dbc-2d6963b0-153b.cloud.databricks.com/
Catalog: ea
"""
import argparse
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

ROOT_DIR = Path(__file__).resolve().parent.parent
console = Console()


def print_banner():
    console.print("[bold cyan]══════════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold white]   THE AGENTIC ENTERPRISE ARCHITECTURE (MVP)                          [/bold white]")
    console.print("[bold green]   Databricks-Native Estate Intelligence & Autonomous EA              [/bold green]")
    console.print("[bold cyan]══════════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("Target Workspace: [bold blue]https://dbc-2d6963b0-153b.cloud.databricks.com/[/bold blue]")
    console.print("Master Metamodel: [bold magenta]Databricks Unity Catalog (ea.metamodel.*)[/bold magenta]\n")


def print_status():
    from src.data_backbone.client import get_unity_catalog_client
    client = get_unity_catalog_client()
    nodes = client.get_nodes()
    edges = client.get_edges()
    time_matrix = client.get_time_matrix()
    drift = client.get_drift_reconciled()

    table = Table(title="Conformed Estate Overview (Databricks Unity Catalog)")
    table.add_column("Subsystem / Table", style="cyan")
    table.add_column("Namespace", style="magenta")
    table.add_column("Record Count", style="green", justify="right")
    table.add_column("Status", style="yellow")

    table.add_row("PAM Nodes", "ea.metamodel.nodes", str(len(nodes)), "Active")
    table.add_row("ArchiMate Edges", "ea.metamodel.edges", str(len(edges)), "Conformed")
    table.add_row("Git Bronze Repos", "ea.bronze.git_repos", str(len(client.get_bronze_records("git_repos"))), "Streamed")
    table.add_row("Cloud CUR Telemetry", "ea.bronze.cloud_resources", str(len(client.get_bronze_records("cloud_resources"))), "Ingested")
    table.add_row("TIME Matrix Mart", "ea.gold.time_matrix", str(len(time_matrix)), "Reconciled")
    table.add_row("Reconciled Drift", "ea.gold.drift_reconciled", str(len(drift)), "Tracked")

    console.print(table)


def run_ingestion():
    console.print("[bold blue]Starting Bronze Ingestion & Delta Live Tables Conformance Pipeline...[/bold blue]")
    subprocess.run([sys.executable, "-m", "src.ingestion.ingest_cloud_cur"], cwd=str(ROOT_DIR), check=True)
    subprocess.run([sys.executable, "-m", "src.ingestion.ingest_github_org"], cwd=str(ROOT_DIR), check=True)
    subprocess.run([sys.executable, "-m", "src.ingestion.dlt_metamodel_pipeline"], cwd=str(ROOT_DIR), check=True)
    console.print("[bold green]✓ Ingestion and conformance completed successfully.[/bold green]")


def run_navigator(target: str = "payments-api"):
    from src.navigator.engine import EstateIntelligenceEngine
    engine = EstateIntelligenceEngine()
    blast = engine.calculate_blast_radius(target)
    diag = engine.compile_blast_radius_diagram(target, blast.get("highlighted_urns"))
    console.print(Panel(
        f"[bold white]Target Component:[/bold white] {blast['target']['name']} ({blast['target']['urn']})\n"
        f"[bold white]Criticality:[/bold white] {blast['target']['criticality']} (Max Affected: {blast['aggregate_criticality']})\n"
        f"[bold white]Upstream Callers:[/bold white] {blast['upstream_count']} services\n"
        f"[bold white]Annual Exposure Risk:[/bold white] ${blast['financial_exposure']['total_annual_risk_usd']:,.2f}/yr\n"
        f"[bold white]PII Flow Lineage:[/bold white] {'⚠️ Active PII Detected' if blast['pii_compliance']['has_pii_exposure'] else '✅ Clean'}\n"
        f"[bold white]Living Blast Map:[/bold white] file://{diag['html_path']}",
        title="[bold green]EA Navigator: Blast Radius Analysis[/bold green]",
        border_style="green",
    ))


def run_sentinel():
    from src.sentinel.gate import EASentinelGate
    gate = EASentinelGate(provider="subscription_cli")
    patch = (ROOT_DIR / "tests" / "fixtures" / "pr_unapproved_db.patch").read_text(encoding="utf-8")
    res = gate.evaluate_patch(patch)
    console.print(res["markdown_report"])


def launch_app():
    console.print("[bold cyan]Launching Databricks App UI Cockpit in Streamlit...[/bold cyan]")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT_DIR / "apps" / "ea_navigator" / "app.py"),
        "--server.port",
        "8501",
        "--server.headless",
        "true",
    ]
    subprocess.run(cmd, cwd=str(ROOT_DIR))


def main():
    parser = argparse.ArgumentParser(description="The Agentic EA Platform - MVP Entrypoint")
    parser.add_argument("--ingest", action="store_true", help="Run Bronze and DLT ingestion pipeline")
    parser.add_argument("--navigator", help="Execute EA Navigator blast radius on target component")
    parser.add_argument("--sentinel", action="store_true", help="Run EA Sentinel gate audit on sample PR")
    parser.add_argument("--app", action="store_true", help="Launch Streamlit Databricks App UI Cockpit")
    parser.add_argument("--verify", action="store_true", help="Run complete pytest test suite")
    args = parser.parse_args()

    print_banner()

    if args.ingest:
        run_ingestion()
    elif args.navigator:
        run_navigator(args.navigator)
    elif args.sentinel:
        run_sentinel()
    elif args.app:
        launch_app()
    elif args.verify:
        subprocess.run([sys.executable, "-m", "pytest", "tests/"], cwd=str(ROOT_DIR), check=True)
    else:
        print_status()
        console.print("\n[bold yellow]Available Commands:[/bold yellow]")
        console.print("  • python src/main.py --ingest              Run Bronze & DLT Ingestion pipeline")
        console.print("  • python src/main.py --navigator <target>  Run EA Navigator blast radius")
        console.print("  • python src/main.py --sentinel            Run EA Sentinel PR governance gate")
        console.print("  • python src/main.py --verify              Run all 16 PAM & platform tests")
        console.print("  • python src/main.py --app                 Launch Databricks Streamlit Cockpit")
        console.print("  • ./demo.sh                                Execute master end-to-end demonstration")


if __name__ == "__main__":
    main()
