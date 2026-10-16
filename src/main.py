"""
The Agentic EA Platform - MVP Entrypoint
Autonomous closed-loop Enterprise Architecture Platform native to Databricks.
"""
import sys
from rich.console import Console

console = Console()

def main():
    console.print("[bold cyan]══════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold white]   THE AGENTIC ENTERPRISE ARCHITECTURE (MVP)                  [/bold white]")
    console.print("[bold green]   Databricks-Native Estate Intelligence & Autonomous EA      [/bold green]")
    console.print("[bold cyan]══════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("Target Databricks Workspace: [bold blue]https://dbc-2d6963b0-153b.cloud.databricks.com/[/bold blue]")
    console.print("Subsystems:")
    console.print("  • [yellow]src/navigator[/yellow]: EA Navigator (Estate Intelligence & What-If Simulations)")
    console.print("  • [yellow]src/sentinel[/yellow]:  EA Sentinel (Autonomous Pre-Merge Policy Gate)")
    console.print("  • [yellow]src/ingestion[/yellow]: Modular Ingestion (GitHub Org, Cloud CUR, ServiceNow CMDB)")
    console.print("  • [yellow]apps/ea_navigator[/yellow]: Databricks App UI (Streamlit Cockpit)")
    console.print("  • [yellow]databricks/[/yellow]: Databricks Asset Bundle (DAB) Definitions")

if __name__ == "__main__":
    main()
