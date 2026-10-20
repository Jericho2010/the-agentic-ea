"""
The Agentic EA Platform - Databricks Apps UI Cockpit.
Native Streamlit Application deployable directly inside Databricks Apps.
Target Workspace: https://dbc-2d6963b0-153b.cloud.databricks.com/
Catalog: ea (Unity Catalog)
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = PROJECT_ROOT
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.archify.bridge import ArchifyBridge
from src.connectors import (
    BackstageConnector,
    ConnectorManager,
    GitHubConnector,
    JiraConnector,
    ServiceNowConnector,
)
from src.data_backbone.client import get_unity_catalog_client
from src.navigator.engine import EstateIntelligenceEngine
from src.sentinel.gate import EASentinelGate, POLICIES

# Page Configuration
st.set_page_config(
    page_title="The Agentic EA — Navigator Cockpit",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.85rem !important;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] label,
    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        font-weight: 600 !important;
    }
    .stMetric {
        background: #131b2e !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.25) !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    p, span, label {
        color: #e2e8f0 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #131b2e;
        border-radius: 6px;
        color: #94a3b8;
        padding: 8px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
    .badge-pass {
        background-color: #065f46;
        color: #34d399;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-fail {
        background-color: #881337;
        color: #fda4af;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Initialize State & Backing Engines
@st.cache_resource
def load_clients():
    client = get_unity_catalog_client()
    navigator = EstateIntelligenceEngine()
    sentinel = EASentinelGate(provider="subscription_cli")
    bridge = ArchifyBridge()
    return client, navigator, sentinel, bridge

client, navigator, sentinel, bridge = load_clients()

# Top Header Bar
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🏛️ The Agentic EA Platform")
    st.caption("Databricks-Native Estate Intelligence, Autonomous Sentinel Governance & Interactive Living Maps")
with col_h2:
    st.markdown("""
    <div style="text-align: right; margin-top: 10px;">
        <span style="background: #1e293b; color: #38bdf8; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 600;">
            ⚡ Databricks UC: dbc-2d6963b0-153b
        </span>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# LEFT SIDEBAR: WORKSPACE NAVIGATION & SYSTEM STATUS
# ==============================================================================
st.sidebar.title("🏛️ The Agentic EA")
st.sidebar.markdown("### Navigation Workspace")

workspace = st.sidebar.radio(
    "Select Workspace",
    [
        "🏛️ Executive & Strategy",
        "🛡️ Autonomous Governance & Compliance",
        "⚡ Engineering Modernization",
        "⚙️ Operations, Resilience & FinOps",
    ],
    index=0,
)

st.sidebar.markdown("---")

# Dynamic Databricks Unity Catalog Connection Status
if getattr(client, "is_connected_to_cloud", False):
    try:
        t0 = time.perf_counter()
        client.execute_query("SELECT 1")
        cloud_latency_ms = (time.perf_counter() - t0) * 1000
        latency_str = f"{cloud_latency_ms:.1f}ms latency"
    except Exception:
        latency_str = "Active"

    st.sidebar.markdown(f"""
    <div style="background: #0f2027; border: 1px solid #10b981; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 700; color: #38bdf8; margin-bottom: 4px;">
            ⚡ Databricks Unity Catalog
        </div>
        <div style="font-size: 12px; color: #34d399; font-weight: 600;">
            🟢 Connected: Live Databricks SQL (df4dc09688caf6d8) | Catalog: ea
        </div>
        <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">
            Warehouse: df4dc09688caf6d8 | {latency_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="background: #1e1b18; border: 1px solid #f59e0b; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 700; color: #f59e0b; margin-bottom: 4px;">
            ⚡ Databricks Unity Catalog
        </div>
        <div style="font-size: 12px; color: #fbbf24; font-weight: 600;">
            🟡 Emulated: Local SQLite Fallback
        </div>
        <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">
            Workstation Mode | Offline Emulation
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.sidebar.button("🔄 Reconnect to Databricks SQL", key="btn_reconnect_uc"):
        if hasattr(client, "_connect_to_cloud"):
            client._connect_to_cloud(max_retries=3, backoff_base=2.0)
        st.cache_resource.clear()
        st.rerun()

# Quick Estate Stats in Sidebar
sb_nodes = client.get_nodes()
sb_edges = client.get_edges()
sb_time = client.get_time_matrix()
sb_spend = sum(t.get("annual_run_cost", 0.0) for t in sb_time)
sb_esg = client.get_esg_carbon_accounting()
sb_cas_carbon = next((e for e in sb_esg if "cassandra" in e.get("service_urn", "")), {})
sb_avoidable_carbon = sb_cas_carbon.get("monthly_emissions_kgco2", 420.0)

st.sidebar.markdown("#### 📊 Estate Quick Stats")
sb_col1, sb_col2 = st.sidebar.columns(2)
sb_col1.metric("Nodes", len(sb_nodes))
sb_col2.metric("Edges", len(sb_edges))
sb_col3, sb_col4 = st.sidebar.columns(2)
sb_col3.metric("Spend", f"${sb_spend/1000:,.1f}k/yr")
sb_col4.metric("Avoidable CO₂", f"{sb_avoidable_carbon:.0f} kg/mo")


# ==============================================================================
# WORKSPACE 1: EXECUTIVE & STRATEGY
# ==============================================================================
if workspace == "🏛️ Executive & Strategy":
    tab_time, tab_capabilities, tab_migration, tab_ma, tab_strategic_ecosystem = st.tabs([
        "📊 Executive TIME Matrix",
        "🎯 Business Capabilities & Investment",
        "🚀 Target-State Migration Roadmap",
        "🏢 M&A Day-One Landscape Discovery",
        "🌐 Strategic Enterprise Governance & Ecosystem Hub",
    ])

    # ==============================================================================
    # TAB 5: EXECUTIVE TIME MATRIX
    # ==============================================================================
    with tab_time:
        st.subheader("📊 Executive TIME Matrix & Architecture Drift")
        st.caption("Gartner TIME Quadrant Portfolio Assessment (Invest, Tolerate, Migrate, Eliminate) with FinOps Run-Cost Tracking.")

        time_data = client.get_time_matrix()
        drift_data = client.get_drift_reconciled()

        total_portfolio = sum(t["annual_run_cost"] for t in time_data)
        invest_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Invest")
        tolerate_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Tolerate")
        migrate_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Migrate")
        eliminate_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Eliminate")

        col_tot, t_col1, t_col2, t_col3, t_col4 = st.columns([1.2, 1, 1, 1, 1])
        col_tot.metric("Total Portfolio Spend", f"${total_portfolio:,.2f}/yr")
        t_col1.metric("Invest (Grow & Modernize)", f"${invest_cost:,.2f}/yr")
        t_col2.metric("Tolerate (Stable Operations)", f"${tolerate_cost:,.2f}/yr")
        t_col3.metric("Migrate (High Tech Debt)", f"${migrate_cost:,.2f}/yr")
        t_col4.metric("Eliminate (Target Sunset)", f"${eliminate_cost:,.2f}/yr")


        st.markdown("---")
        st.markdown("#### Portfolio Systems Classification")
        df_time = pd.DataFrame(time_data)[["name", "urn", "disposition", "annual_run_cost", "tech_debt_score", "eol_date"]]
        st.dataframe(df_time, use_container_width=True)

        st.markdown("---")
        st.markdown("#### ⏳ Technology Obsolescence & Lifecycle Risk (EOL/EOS Assessment)")
        st.caption("Automated tracking of End-of-Life horizons, affected upstream dependencies, and financial risk.")

        lifecycle_risks = navigator.evaluate_lifecycle_risks()
        if lifecycle_risks:
            expired_count = sum(1 for r in lifecycle_risks if r["risk_status"] == "EXPIRED")
            near_eol_count = sum(1 for r in lifecycle_risks if r["risk_status"] == "NEAR_EOL")
            approaching_count = sum(1 for r in lifecycle_risks if r["risk_status"] == "APPROACHING_EOL")
            supported_count = sum(1 for r in lifecycle_risks if r["risk_status"] == "SUPPORTED")

            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            r_col1.metric("🔴 Expired (Past EOL)", f"{expired_count} systems")
            r_col2.metric("🟠 Near EOL (<1 Year)", f"{near_eol_count} systems")
            r_col3.metric("🟡 Approaching EOL (<2 Years)", f"{approaching_count} systems")
            r_col4.metric("🟢 Supported (>2 Years)", f"{supported_count} systems")

            df_risks = pd.DataFrame(lifecycle_risks)[[
                "name", "urn", "risk_status", "risk_level", "eol_date", "days_remaining", 
                "upstream_callers_count", "financial_exposure_usd", "recommendation"
            ]]
            st.dataframe(df_risks, use_container_width=True)

        st.markdown("---")
        st.markdown("#### ⚠️ Reconciled Architectural Drift (Declared vs Runtime Telemetry)")
        if drift_data:
            df_drift = pd.DataFrame(drift_data)[["urn", "discrepancy_type", "severity", "declared_state", "runtime_state", "reconciled_at"]]
            st.dataframe(df_drift, use_container_width=True)
        else:
            st.info("Zero architecture drift detected across live estate telemetry.")


    # ==============================================================================
    # TAB 7: BUSINESS CAPABILITIES & INVESTMENT
    # ==============================================================================
    with tab_capabilities:
        st.subheader("🎯 Business Capability Modeling & Strategic Investment Alignment")
        st.caption("Hierarchical capability tree (Level-1 Strategic Domains & Level-2 Functional Capabilities) with FinOps cloud run cost attribution and technical debt concentration.")

        cap_tree = navigator.get_capability_tree()
        cap_summary = navigator.get_capability_finops_summary()
        cap_realizations = client.get_capability_realizations()

        # Top Level Executive KPIs
        c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
        c_kpi1.metric("Total Capability Spend", f"${cap_tree['total_estate_capability_spend_usd']:,.2f}/yr", "100.0% Attributed")
        c_kpi2.metric("Strategic Domains (L1)", f"{cap_tree['l1_domains_count']} Strategic Domains")
        c_kpi3.metric("Functional Capabilities (L2)", f"{cap_tree['l2_capabilities_count']} Capabilities")
        c_kpi4.metric("Realizing Systems", f"{cap_tree['total_realizations_count']} Production Realizations")

        st.markdown("---")
        st.markdown("#### 🏛️ Strategic Domain FinOps Investment Allocation (Level-1)")

        col_d1, col_d2, col_d3 = st.columns(3)
        domain_columns = [col_d1, col_d2, col_d3]
        for idx, domain in enumerate(cap_tree["domains"]):
            col = domain_columns[idx % 3]
            with col:
                st.markdown(f"""
                <div style="background: #131b2e; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <div style="font-size: 16px; font-weight: 700; color: #38bdf8;">{domain['name']}</div>
                    <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Domain: {domain['domain']}</div>
                    <div style="font-size: 20px; font-weight: 800; color: #f8fafc; margin-top: 8px;">${domain['total_annual_cost']:,.2f}/yr</div>
                    <div style="font-size: 13px; color: #34d399; font-weight: 600;">{domain['percentage_of_estate']}% of Enterprise Cloud Spend</div>
                    <div style="font-size: 12px; color: #cbd5e1; margin-top: 6px;">Average Tech Debt: <b>{domain['avg_tech_debt']}/100</b></div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Realized by: <i>{', '.join(domain['realizing_systems'])}</i></div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📊 Capability FinOps & Technical Debt Heatmap")
        df_cap_summary = pd.DataFrame(cap_summary)
        st.dataframe(df_cap_summary, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🌳 Interactive Hierarchical Capability Tree Explorer")

        for domain in cap_tree["domains"]:
            with st.expander(f"📁 {domain['name']} — ${domain['total_annual_cost']:,.2f}/yr ({domain['percentage_of_estate']}%)", expanded=True):
                st.markdown(f"**Domain Description:** {domain['description']}")
                st.markdown(f"**Owning Leadership:** `{domain['owner_team']}` | **Criticality:** `{domain['criticality']}`")

                for cap in domain["capabilities"]:
                    st.markdown(f"##### ↳ `{cap['name']}` ({cap['urn']})")
                    c_col1, c_col2, c_col3 = st.columns(3)
                    c_col1.metric("Capability Spend", f"${cap['allocated_annual_cost']:,.2f}/yr", f"{cap['percentage_of_estate']}% of Estate")
                    c_col2.metric("Tech Debt Exposure", f"{cap['max_tech_debt']}/100 max", f"Avg: {cap['avg_tech_debt']}/100")
                    c_col3.metric("Realizing Systems", f"{cap['realizing_count']} components")

                    st.markdown("**Realizing Architectural Entities (PAM `realizes` Contracts):**")
                    df_reals = pd.DataFrame(cap["realizing_entities"])[[
                        "realizing_entity_name", "realizing_entity_kind", "disposition",
                        "allocated_annual_cost", "tech_debt_score", "criticality"
                    ]]
                    st.dataframe(df_reals, use_container_width=True)
                    st.markdown(" ")

        st.markdown("---")
        st.markdown("#### 📋 Conformed Gold Table: `ea.gold.capability_realization`")
        if cap_realizations:
            df_full = pd.DataFrame(cap_realizations)[[
                "capability_name", "capability_level", "parent_capability_name",
                "realizing_entity_name", "realizing_entity_kind", "disposition",
                "allocated_annual_cost", "tech_debt_score", "criticality"
            ]]
            st.dataframe(df_full, use_container_width=True)
            st.download_button(
                label="📥 Download Capability Realizations (CSV)",
                data=df_full.to_csv(index=False),
                file_name="ea_gold_capability_realization.csv",
                mime="text/csv",
            )


    # ==============================================================================
    # TAB 6: TARGET-STATE MIGRATION ROADMAP
    # ==============================================================================
    with tab_migration:
        st.subheader("🚀 Target-State Architecture & Cloud Migration Roadmapping")
        st.caption("Automated generation of phased migration waves, target-state PAM topology mapping, and FinOps cost elimination.")

        col_m1, col_m2 = st.columns([2, 1])
        selected_target = col_m1.selectbox(
            "Candidate Legacy Asset for Target-State Cloud Migration",
            ["cassandra-legacy-cluster", "customer-pii-stream"]
        )
    
        plan = navigator.plan_target_state_migration(selected_target)
        fin = plan["financial_summary"]
        node = plan["target_state_node"]
        curr = plan["current_state"]

        # Top KPI Metrics
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Legacy Cost Eliminated", f"${fin['cost_eliminated_usd']:,.2f}/yr")
        kpi2.metric("Net Annual Savings", f"${fin['annual_savings_usd']:,.2f}/yr")
        kpi3.metric("Tech Debt Reduction", f"-{fin['tech_debt_reduction_points']} pts", f"{fin['current_tech_debt']} ➔ {fin['target_tech_debt']}")
        kpi4.metric("Migration Timeline", f"{len(plan['phased_waves'])} Phased Waves")

        st.markdown("---")
        st.markdown(f"#### 🌊 Phased Migration Waves: `{curr['name']}` ➔ `{node['name']}`")

        for w in plan["phased_waves"]:
            with st.expander(f"Wave {w['wave']}: {w['name']} ({w['duration']}) — Milestone: {w['milestone']}", expanded=True):
                st.markdown(f"**Target Milestone:** `{w['milestone']}`")
                st.markdown("**Core Migration Activities:**")
                for act in w["activities"]:
                    st.markdown(f"- {act}")
                st.markdown(f"**Verification & Exit Criteria:** *{w['exit_criteria']}*")
                if "annual_cost_eliminated_usd" in w:
                    st.success(f"FinOps Milestone: Eliminates ${w['annual_cost_eliminated_usd']:,.2f}/yr in legacy infrastructure charges.")

        st.markdown("---")
        st.markdown("#### 🏛️ Target-State PAM Metamodel Mapping")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("**New Target Node Specification:**")
            st.json(node)
        with col_t2:
            st.markdown("**Target Graph Relationships (PAM Edges):**")
            df_edges = pd.DataFrame(plan["target_state_edges"])
            st.dataframe(df_edges, use_container_width=True)

        with st.expander("📝 View / Export Compliant MADR v3.0 Architectural Decision Record"):
            st.markdown(plan["madr"])
            st.download_button(
                label="📥 Download ADR (.md)",
                data=plan["madr"],
                file_name=f"ADR-002_{selected_target}_migration.md",
                mime="text/markdown",
            )

        # Consolidated Estate Target Graph
        with st.expander("🌐 Global Target-State Portfolio Topology & Elimination Summary"):
            target_graph = navigator.get_target_state_graph()
            g_col1, g_col2, g_col3 = st.columns(3)
            g_col1.metric("Total Legacy Spend Eliminated", f"${target_graph['summary']['total_cost_eliminated_usd']:,.2f}/yr")
            g_col2.metric("Total Tech Debt Drop", f"-{target_graph['summary']['total_tech_debt_eliminated_points']} pts")
            g_col3.metric("Target Planned Nodes", f"{target_graph['summary']['target_planned_nodes_count']} nodes")
            st.markdown(f"**Retired Systems:** {', '.join([u.split(':')[-1] for u in target_graph['retired_nodes']])}")
            st.markdown(f"**Target-State Modern Assets:** {', '.join([u.split(':')[-1] for u in target_graph['planned_nodes']])}")


    # ==============================================================================
    # TAB 9: M&A DAY-ONE LANDSCAPE DISCOVERY & SYNERGIES
    # ==============================================================================
    with tab_ma:
        st.subheader("🏢 M&A Day-One IT Landscape Discovery & Overlap Analysis")
        st.caption("Rapid zero-footprint discovery of acquired entity IT estate, business capability overlap mapping, technology stack divergence, and FinOps synergy rationalization.")

        ma_metrics = navigator.analyze_ma_landscape()
        synergies = client.get_ma_synergies() or ma_metrics["synergies"]

        # Top KPI Metrics Cards
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Day-One Total Spend", f"${ma_metrics['combined_annual_cost_usd']:,.2f}", f"Core: ${ma_metrics['core_annual_cost_usd']:,.0f}")
        k2.metric("Acquired Estate Spend", f"${ma_metrics['acquired_annual_cost_usd']:,.2f}", "4 Systems Tracked")
        k3.metric("Rationalization Synergies", f"${ma_metrics['potential_synergy_savings_usd']:,.2f}", "67.7% Acquired Run Cost", delta_color="normal")
        k4.metric("Target Post-Synergy Spend", f"${ma_metrics['post_synergy_annual_cost_usd']:,.2f}", "Annual Target")
        k5.metric("Technical Debt Score", f"{ma_metrics['acquired_avg_tech_debt']} / 100", f"Core: {ma_metrics['core_avg_tech_debt']} / 100", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### 🎯 Capability Overlap & Synergy Rationalization Matrix (`ea.gold.ma_synergies`)")
        st.caption("Identified duplicate capabilities and overlapping services between acquired entity and enterprise core estate.")

        if synergies:
            df_syn = pd.DataFrame(synergies)[[
                "synergy_id", "target_entity_name", "capability_name", "core_counterpart_name",
                "overlap_type", "potential_synergy_savings", "current_annual_cost", "risk_level", "recommendation"
            ]]
            st.dataframe(df_syn, use_container_width=True)

        st.markdown("---")
        st.markdown("#### ⚙️ Technology Stack Divergence & Obsolescence Analysis")
        st.caption("Architectural comparison between acquired technology choices and core enterprise standards.")

        div_cols = st.columns(2)
        for idx, div in enumerate(ma_metrics["tech_stack_divergence"]):
            col = div_cols[idx % 2]
            with col:
                risk_color = "#ef4444" if div.get("risk") == "High" else ("#f59e0b" if div.get("risk") == "Medium" else "#10b981")
                st.markdown(f"""
                <div style="background: #0f172a; border-left: 4px solid {risk_color}; border-radius: 8px; padding: 14px; margin-bottom: 12px; border: 1px solid #1e293b;">
                    <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">{div['area']} <span style="font-size: 11px; color: {risk_color}; background: #1e293b; padding: 2px 6px; border-radius: 4px; margin-left: 8px;">Risk: {div.get('risk', 'Low')}</span></div>
                    <div style="margin-top: 6px; font-size: 13px; color: #94a3b8;">
                        <strong>Acquired Tech:</strong> <code style="color: #fda4af;">{div['acquired']}</code><br/>
                        <strong>Enterprise Standard:</strong> <code style="color: #6ee7b7;">{div['core']}</code>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>{div['action']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗺️ Living Architecture Map: Merged M&A Landscape")
        st.caption("Interactive Archify vector living map highlighting acquired target assets and overlap connections.")

        ma_diag_path = ROOT_DIR / "data" / "diagrams" / "ma_landscape_view.html"
        if not ma_diag_path.exists():
            navigator.compile_ma_landscape_diagram()

        if ma_diag_path.exists():
            html_code = ma_diag_path.read_text(encoding="utf-8")
            st.components.v1.html(html_code, height=650, scrolling=True)
        else:
            st.warning("Diagram could not be loaded.")


    # ==============================================================================
    # TAB 15: STRATEGIC ENTERPRISE GOVERNANCE & ECOSYSTEM HUB (S17-S20)
    # ==============================================================================
    with tab_strategic_ecosystem:
        st.subheader("🌐 Strategic Enterprise Governance & Ecosystem Hub (Scenarios S17–S20)")
        st.caption("Synthesized executive intelligence across Master Data Management (MDM), ESG & Green IT Carbon Accounting, Team Topologies / Conway's Law, and Strategic Vendor Lock-In & Open Exit Planning.")

        strat_data = navigator.analyze_strategic_governance_ecosystem()

        # Executive KPI Metric Cards
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        kpi1.metric("MDM Divergence", f"{strat_data['divergent_count']} Divergent / {strat_data['total_mdm_entities']}", delta="CustomerProfile Drift", delta_color="inverse")
        kpi2.metric("ESG Carbon Footprint", f"{strat_data['total_monthly_emissions_kgco2']:,.1f} kgCO2/mo", delta=f"{strat_data['avoidable_monthly_carbon_kgco2']:,.0f} kgCO2 Avoidable", delta_color="inverse")
        kpi3.metric("Conway Alignment", f"{strat_data['conways_alignment_pct']}%", delta=f"{len(strat_data['friction_teams'])} Monolithic Friction", delta_color="inverse")
        kpi4.metric("High Lock-In Assets", f"{len(strat_data['high_lockin_components'])} / {strat_data['total_evaluated_components']}", delta=f"Avg Score: {strat_data['avg_lockin_score']:.0f}/100", delta_color="inverse")
        kpi5.metric("Avg Exit Effort", f"{strat_data['avg_exit_effort_weeks']:.1f} Weeks", delta="Cassandra (8wks) / Kinesis (6wks)", delta_color="off")

        st.markdown("---")

        subtab_mdm, subtab_esg, subtab_tt, subtab_lockin = st.tabs([
            "🧬 S17: Master Data Management (MDM)",
            "🌱 S18: ESG & Green IT Carbon Footprint",
            "👥 S19: Team Topologies & Conway's Law",
            "🔓 S20: Vendor Lock-In & Exit Planning",
        ])

        with subtab_mdm:
            st.markdown("#### Master Data Management & Golden Record Lineage (`ea.gold.mdm_golden_records`)")
            st.caption("Reconciles core master entities against competing siloed stores, enforcing schema contracts and SCD2 delta history.")
            mdm_rows = strat_data["mdm_records"]
            if mdm_rows:
                df_mdm = pd.DataFrame(mdm_rows)
                df_mdm_disp = df_mdm.copy()
                df_mdm_disp["divergence_status"] = df_mdm_disp["divergence_detected"].apply(
                    lambda d: "🔴 DIVERGENT" if d else "🟢 IN_SYNC"
                )
                df_mdm_disp["contract_status"] = df_mdm_disp["data_contract_status"].apply(
                    lambda s: "🟢 COMPLIANT" if s == "COMPLIANT" else f"🔴 {s}"
                )
                df_mdm_disp["scd2_status"] = df_mdm_disp["scd2_active"].apply(
                    lambda b: "✅ Active" if b else "❌ Inactive"
                )
                st.dataframe(
                    df_mdm_disp[[
                        "entity_name", "authoritative_source", "competing_sources",
                        "divergence_status", "contract_status", "scd2_status"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export MDM Golden Records (CSV)",
                    data=df_mdm.to_csv(index=False),
                    file_name="ea_gold_mdm_golden_records.csv",
                    mime="text/csv",
                )

        with subtab_esg:
            st.markdown("#### ESG & Green IT Carbon Footprint Accounting (`ea.gold.esg_carbon_accounting`)")
            st.caption("Calculates regional energy consumption (kWh) and grid carbon intensity (gCO2/kWh) to isolate idle, high-emission legacy workloads.")
            esg_rows = strat_data["esg_records"]
            if esg_rows:
                df_esg = pd.DataFrame(esg_rows)
                df_esg_disp = df_esg.copy()
                df_esg_disp["service"] = df_esg_disp["service_urn"].apply(lambda u: u.split(":")[-1])
                df_esg_disp["monthly_kwh_fmt"] = df_esg_disp["monthly_kwh"].apply(lambda v: f"{v:,} kWh")
                df_esg_disp["grid_intensity"] = df_esg_disp["grid_carbon_intensity_gco2_kwh"].apply(lambda v: f"{v} gCO2/kWh")
                df_esg_disp["monthly_emissions_fmt"] = df_esg_disp["monthly_emissions_kgco2"].apply(lambda v: f"{v:,.2f} kgCO2")
                df_esg_disp["green_tier_badge"] = df_esg_disp["green_tier"].apply(
                    lambda t: "🟢 RENEWABLE_CLEAN" if t == "RENEWABLE_CLEAN" else ("🔴 HIGH_CARBON" if t == "HIGH_CARBON" else "🟡 MODERATE")
                )
                st.dataframe(
                    df_esg_disp[[
                        "service", "region", "monthly_kwh_fmt", "grid_intensity",
                        "monthly_emissions_fmt", "green_tier_badge", "reduction_recommendation"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export ESG Carbon Accounting Ledger (CSV)",
                    data=df_esg.to_csv(index=False),
                    file_name="ea_gold_esg_carbon_accounting.csv",
                    mime="text/csv",
                )

        with subtab_tt:
            st.markdown("#### Team Topologies & Conway's Law Alignment (`ea.gold.team_topologies`)")
            st.caption("Audits stream-aligned and platform team boundaries against monolithic repositories to eliminate commit contention and cognitive overload.")
            tt_rows = strat_data["team_records"]
            if tt_rows:
                df_tt = pd.DataFrame(tt_rows)
                df_tt_disp = df_tt.copy()
                df_tt_disp["codeowners_status"] = df_tt_disp["codeowners_match"].apply(
                    lambda b: "✅ Match" if b else "⚠️ Mismatch"
                )
                df_tt_disp["friction_idx"] = df_tt_disp["commit_co_change_friction"].apply(lambda v: f"{v:.2f}")
                df_tt_disp["conway_badge"] = df_tt_disp["conways_law_alignment"].apply(
                    lambda a: "🟢 ALIGNED" if a == "ALIGNED" else f"🔴 {a}"
                )
                st.dataframe(
                    df_tt_disp[[
                        "team_name", "team_type", "owned_components",
                        "codeowners_status", "friction_idx", "conway_badge"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export Team Topologies Ledger (CSV)",
                    data=df_tt.to_csv(index=False),
                    file_name="ea_gold_team_topologies.csv",
                    mime="text/csv",
                )

        with subtab_lockin:
            st.markdown("#### Strategic Vendor Lock-In Assessment & Open Exit Planning (`ea.gold.vendor_lockin_exit`)")
            st.caption("Quantifies reliance on proprietary cloud services and specifies open lakehouse migration paths with estimated exit efforts.")
            lockin_rows = strat_data["lockin_records"]
            if lockin_rows:
                df_lockin = pd.DataFrame(lockin_rows)
                df_lockin_disp = df_lockin.copy()
                df_lockin_disp["component"] = df_lockin_disp["component_urn"].apply(lambda u: u.split(":")[-1])
                df_lockin_disp["lockin_badge"] = df_lockin_disp["lockin_risk_score"].apply(
                    lambda s: f"🔴 {s}/100" if s >= 80 else (f"🟡 {s}/100" if s >= 50 else f"🟢 {s}/100")
                )
                df_lockin_disp["effort_weeks"] = df_lockin_disp["exit_effort_weeks"].apply(lambda w: f"{w} wks")
                st.dataframe(
                    df_lockin_disp[[
                        "component", "cloud_provider", "proprietary_services_used",
                        "lockin_badge", "open_alternative", "effort_weeks", "exit_strategy_action"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export Vendor Lock-In & Exit Register (CSV)",
                    data=df_lockin.to_csv(index=False),
                    file_name="ea_gold_vendor_lockin_exit.csv",
                    mime="text/csv",
                )

        st.markdown("---")
        st.markdown("#### 🛠️ Priority Strategic Governance & Remediation Actions")
        strat_col1, strat_col2 = st.columns(2)

        for idx, act in enumerate(strat_data["strategic_actions"]):
            target_col = strat_col1 if idx % 2 == 0 else strat_col2
            with target_col:
                st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #f8fafc; font-size: 15px;">{act['component']}</span>
                        <span style="background: #1e293b; color: #38bdf8; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{act['domain']}</span>
                    </div>
                    <div style="margin-top: 8px; font-size: 13px; color: #f43f5e; font-weight: 600;">
                        {act['risk']}
                    </div>
                    <div style="margin-top: 6px; font-size: 13px; color: #94a3b8;">
                        <strong>Action:</strong> <code>{act['action']}</code>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>Remediation: {act['remediation']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗺️ Interactive Strategic Governance & Ecosystem Map")
        st.caption("Interactive Archify vector map displaying golden data core lineage, stream-aligned application boundaries, and proprietary cloud vendor lock-in heatmaps.")

        strat_diag_path = ROOT_DIR / "data" / "diagrams" / "strategic_governance_and_ecosystem_view.html"
        if not strat_diag_path.exists():
            navigator.compile_strategic_governance_diagram()
        if strat_diag_path.exists():
            html_code = strat_diag_path.read_text(encoding="utf-8")
            st.components.v1.html(html_code, height=650, scrolling=True)
        else:
            st.warning("Strategic governance and ecosystem diagram could not be loaded.")







# ==============================================================================
# WORKSPACE 2: AUTONOMOUS GOVERNANCE & COMPLIANCE
# ==============================================================================
elif workspace == "🛡️ Autonomous Governance & Compliance":
    tab_sentinel, tab_ai_governance, tab_compliance = st.tabs([
        "🛡️ EA Sentinel Governance",
        "🤖 AI Governance & ML Catalog (EU AI Act)",
        "⚖️ Regulatory Compliance & Privacy Lineage (GDPR / DORA)",
    ])

    # ==============================================================================
    # TAB 4: EA SENTINEL GOVERNANCE
    # ==============================================================================
    with tab_sentinel:
        st.subheader("🛡️ EA Sentinel: Autonomous Pre-Merge Architectural Gate")
        st.caption("Validates Pull Requests against PAM policies (EA-POL-001, EA-POL-002, EA-POL-003) and compiles visual diffs.")

        col_s1, col_s2 = st.columns([2, 1])
        sample_pr = col_s1.selectbox(
            "Choose Synthetic Pull Request Diff",
            [
                "PR #104: Introduce Unapproved Cassandra Datastore & Unencrypted PII (Violating)",
                "PR #105: Conformed Databricks Unity Catalog Delta Table with KMS (Compliant)",
            ]
        )
        provider_choice = col_s2.selectbox(
            "Tri-Modal Reasoning Provider",
            ["subscription_cli", "databricks_mosaic", "external_api"],
            index=0
        )

        pr_id = "PR-104" if "Cassandra" in sample_pr else "PR-105"
        commit_hash = "8a91b2c" if "Cassandra" in sample_pr else "9c43d1a"

        if "Cassandra" in sample_pr:
            patch_file = PROJECT_ROOT / "tests" / "fixtures" / "pr_unapproved_db.patch"
        else:
            patch_file = PROJECT_ROOT / "tests" / "fixtures" / "pr_clean.patch"

        patch_content = patch_file.read_text(encoding="utf-8")
    
        with st.expander("📄 View Pull Request Diff"):
            st.code(patch_content, language="diff")

        if st.button("🚀 Evaluate PR with EA Sentinel Gate", type="primary"):
            with st.spinner(f"Evaluating {pr_id} diff via Tri-Modal option: {provider_choice}..."):
                gate_eval = EASentinelGate(provider=provider_choice)
                res = gate_eval.evaluate_patch(patch_content, pr_id=pr_id, commit_hash=commit_hash)

            if res["passed"]:
                st.markdown('<span class="badge-pass">✅ GATE PASSED: PR IS ARCHITECTURALLY COMPLIANT</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="badge-fail">🚫 GATE BLOCKED: {res["violations_count"]} ARCHITECTURAL VIOLATIONS DETECTED</span>', unsafe_allow_html=True)

            st.markdown(res["markdown_report"])

            # Visual Delta Map
            delta_html = Path(res["diagrams"]["html_path"])
            if delta_html.exists():
                st.markdown("#### 🗺️ Visual Architecture Diff (Before vs Proposed After)")
                components.html(delta_html.read_text(encoding="utf-8"), height=600, scrolling=True)

        st.markdown("---")
        st.markdown("#### 📜 Architecture Review Board (ARB) Pre-Merge Audit Ledger")
        st.caption("Conformed immutable audit receipts recorded in `ea.gold.arb_audit_ledger` via Databricks Unity Catalog.")

        audit_ledger = client.get_arb_audit_ledger()
        if audit_ledger:
            a_col1, a_col2, a_col3 = st.columns(3)
            total_evals = len(audit_ledger)
            approved_evals = sum(1 for a in audit_ledger if a["decision"] == "APPROVED")
            blocked_evals = sum(1 for a in audit_ledger if a["decision"] == "BLOCKED")

            a_col1.metric("Total ARB Audits", f"{total_evals} receipts")
            a_col2.metric("🟢 Approved PRs", f"{approved_evals} compliant")
            a_col3.metric("🔴 Blocked PRs", f"{blocked_evals} non-compliant")

            df_ledger = pd.DataFrame(audit_ledger)[[
                "pr_id", "commit_hash", "decision", "policy_status",
                "violations_count", "evaluator", "timestamp"
            ]]
            st.dataframe(df_ledger, use_container_width=True)

            with st.expander("🔍 View Policy Violations Details by PR"):
                for audit in audit_ledger:
                    badge = "🟢 APPROVED" if audit["decision"] == "APPROVED" else "🔴 BLOCKED"
                    st.markdown(f"**{audit['pr_id']} (Commit `{audit['commit_hash']}`) — {badge}** ({audit['timestamp']})")
                    if audit.get("violations"):
                        for v in audit["violations"]:
                            st.markdown(f"- **`{v['policy_id']}` ({v['severity']}):** {v['detail']}")
                            st.caption(f"  *Remediation:* {v['remediation']}")
                    else:
                        st.markdown("- *Zero violations detected. Architectural conformance verified.*")

            st.download_button(
                label="📥 Export ARB Audit Ledger (CSV)",
                data=df_ledger.to_csv(index=False),
                file_name="ea_gold_arb_audit_ledger.csv",
                mime="text/csv",
            )
        else:
            st.info("No ARB audit receipts currently recorded in `ea.gold.arb_audit_ledger`.")



    # ==============================================================================
    # TAB 13: AI GOVERNANCE & ML CATALOG (EU AI ACT)
    # ==============================================================================
    with tab_ai_governance:
        st.subheader("🤖 AI Governance, ML Model Catalog & EU AI Act Compliance")
        st.caption("Conformed ML model catalog in `ea.gold.ai_governance` mapping EU AI Act risk tiers (Art. 5 Prohibited, Annex III High-Risk, Art. 50 Limited-Risk, Minimal-Risk) and end-to-end data lineage.")

        ai_data = navigator.analyze_ai_governance()

        # 5 KPI Metric Cards
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        m_col1.metric("Total AI Models", f"{ai_data['total_models_count']} Systems")
        m_col2.metric("🚨 Prohibited (Art. 5)", f"{ai_data['prohibited_count']}", delta="-1 Action Required", delta_color="inverse")
        m_col3.metric("⚠️ High-Risk (Annex III)", f"{ai_data['high_risk_count']}", delta="Needs Oversight", delta_color="inverse")
        m_col4.metric("💬 Limited-Risk (Art. 50)", f"{ai_data['limited_risk_count']}", delta="Needs Disclosure", delta_color="inverse")
        m_col5.metric("🟢 Minimal-Risk", f"{ai_data['minimal_risk_count']}", delta="Compliant")

        st.markdown("---")
        st.markdown("#### 📋 AI Model Registry & EU AI Act Compliance Matrix (`ea.gold.ai_governance`)")

        gov_rows = ai_data["lineage_traces"]
        if gov_rows:
            df_gov = pd.DataFrame(gov_rows)
            df_display = df_gov.copy()
            df_display["model_card"] = df_display["has_model_card"].apply(lambda b: "✅ Available" if b else "❌ Missing")
            df_display["data_lineage"] = df_display["has_data_lineage"].apply(lambda b: "✅ Verified" if b else "❌ Unmapped")
            df_display["human_oversight"] = df_display["has_human_oversight"].apply(lambda b: "✅ Enforced" if b else "❌ Absent")
            df_display["status"] = df_display["compliance_status"].apply(
                lambda s: "🚨 PROHIBITED" if s == "PROHIBITED" else ("⚠️ ACTION REQUIRED" if s == "ACTION_REQUIRED" else "✅ COMPLIANT")
            )

            st.dataframe(
                df_display[[
                    "model_id", "model_name", "version", "framework", "task_type",
                    "eu_risk_tier", "status", "model_card", "data_lineage", "human_oversight", "governance_action"
                ]],
                use_container_width=True,
            )

            st.download_button(
                label="📥 Export AI Governance Catalog (CSV)",
                data=df_gov.to_csv(index=False),
                file_name="ea_gold_ai_governance.csv",
                mime="text/csv",
            )

        st.markdown("---")
        st.markdown("#### ⚖️ Priority Automated AI Governance Actions")
        act_col1, act_col2 = st.columns(2)

        for idx, act in enumerate(ai_data["governance_actions"]):
            target_col = act_col1 if idx % 2 == 0 else act_col2
            with target_col:
                badge_color = "#f43f5e" if act["risk_tier"] == "UNACCEPTABLE_RISK" else ("#f59e0b" if act["risk_tier"] == "HIGH_RISK" else ("#38bdf8" if act["risk_tier"] == "LIMITED_RISK" else "#10b981"))
                st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #f8fafc; font-size: 15px;">{act['model_name']}</span>
                        <span style="background: #1e293b; color: {badge_color}; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{act['risk_tier']}</span>
                    </div>
                    <div style="margin-top: 8px; font-size: 13px; color: #94a3b8;">
                        <strong>Action:</strong> <span style="color: {badge_color}; font-weight: bold;">{act['action']}</span> | 
                        <strong>Article:</strong> <code>{act['article']}</code>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #cbd5e1;">
                        {act['details']}
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>Remediation: {act['remediation']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗺️ Interactive End-to-End AI Model Lineage & Topology Diagram")
        st.caption("Interactive Archify vector map displaying complete lineage from Training Datasets ➔ MLflow Model Registry (EU AI Act Governed Tiers) ➔ Model Serving Endpoints.")

        ai_diag_path = ROOT_DIR / "data" / "diagrams" / "ai_model_lineage.html"
        if not ai_diag_path.exists():
            navigator.compile_ai_model_lineage_diagram()
        if ai_diag_path.exists():
            html_code = ai_diag_path.read_text(encoding="utf-8")
            st.components.v1.html(html_code, height=650, scrolling=True)
        else:
            st.warning("AI model lineage diagram could not be loaded.")


    # ==============================================================================
    # TAB 10: REGULATORY COMPLIANCE & PRIVACY LINEAGE (GDPR / DORA)
    # ==============================================================================
    with tab_compliance:
        st.subheader("⚖️ Regulatory Compliance & Privacy Lineage (GDPR / DORA)")
        st.caption("Continuous regulatory impact mapping, customer PII dataflow lineage traversal, cross-border third-country transfer detection (GDPR Art. 44), encryption in transit/rest posture (GDPR Art. 32), and DORA ICT resilience auditing.")

        compliance_metrics = navigator.analyze_compliance_lineage()
        lineage_records = client.get_compliance_lineage() or compliance_metrics["lineage_records"]

        # 4 Top KPI Metric Cards
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Governed Lineage Flows", f"{compliance_metrics['total_lineage_flows_count']}", f"{compliance_metrics['compliant_flows_count']} Compliant Flows")
        c2.metric("PII Datastores in Scope", f"{compliance_metrics['pii_datastores_count']}", "billing-db, payments-ledger, cassandra")
        c3.metric("Unencrypted Flows (Art. 32)", f"{compliance_metrics['unencrypted_flows_count']}", "Plaintext Transit / None at Rest", delta_color="inverse")
        c4.metric("Third Country Egress (Art. 44)", f"{compliance_metrics['cross_border_egress_count']}", "EU-West-1 ➔ US-East-1", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### 📋 Conformed Regulatory Compliance Lineage Mart (`ea.gold.compliance_lineage`)")
        st.caption("Authoritative dataflow lineage records tracking jurisdiction boundaries, classification tiers, cryptographic posture, and regulatory violation classifications.")

        if lineage_records:
            df_comp = pd.DataFrame(lineage_records)[[
                "flow_id", "source_urn", "target_urn", "data_classification",
                "jurisdiction_source", "jurisdiction_target", "is_cross_border",
                "transit_encryption", "rest_encryption", "gdpr_status", "dora_status", "risk_level"
            ]]
            st.dataframe(df_comp, use_container_width=True)
            st.download_button(
                label="📥 Download Compliance Lineage (CSV)",
                data=df_comp.to_csv(index=False),
                file_name="ea_gold_compliance_lineage.csv",
                mime="text/csv",
            )

        st.markdown("---")
        st.markdown("#### 🚨 Regulatory Violations & Remediations")
        st.caption("Actionable remediation guidance for identified GDPR and DORA compliance discrepancies.")

        v_cols = st.columns(3)
        for idx, v in enumerate(compliance_metrics["violations"]):
            col = v_cols[idx % 3]
            with col:
                v_color = "#ef4444" if v.get("severity") == "CRITICAL" else "#f59e0b"
                st.markdown(f"""
                <div style="background: #0f172a; border-left: 4px solid {v_color}; border-radius: 8px; padding: 14px; margin-bottom: 12px; border: 1px solid #1e293b; min-height: 200px;">
                    <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">{v['article']} <span style="font-size: 11px; color: {v_color}; background: #1e293b; padding: 2px 6px; border-radius: 4px; margin-left: 8px;">{v.get('severity', 'HIGH')}</span></div>
                    <div style="margin-top: 6px; font-size: 13px; color: #94a3b8;">
                        <strong>Flagged Asset:</strong> <code style="color: #fda4af;">{v['component']}</code><br/>
                        <strong>Flow:</strong> <code style="color: #6ee7b7;">{v['flow']}</code>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #cbd5e1;">
                        {v['details']}
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>Remediation: {v['remediation']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗺️ Living Architecture Map: GDPR Sovereign Jurisdiction & Dataflow Lineage")
        st.caption("Interactive Archify vector living map isolating EEA Sovereign Jurisdiction (EU-West-1) from Third Country Egress (US-East-1), highlighting encryption failures and SPOFs.")

        comp_diag_path = ROOT_DIR / "data" / "diagrams" / "gdpr_dora_lineage.html"
        if not comp_diag_path.exists():
            navigator.compile_compliance_lineage_diagram()

        if comp_diag_path.exists():
            html_code = comp_diag_path.read_text(encoding="utf-8")
            st.components.v1.html(html_code, height=650, scrolling=True)
        else:
            st.warning("Compliance lineage diagram could not be loaded.")



# ==============================================================================
# WORKSPACE 3: ENGINEERING MODERNIZATION
# ==============================================================================
elif workspace == "⚡ Engineering Modernization":
    tab_catalog, tab_maps, tab_navigator, tab_interfaces, tab_ecosystem = st.tabs([
        "🏛️ Estate Catalog",
        "🗺️ Living Architecture Maps",
        "🧭 EA Navigator Cockpit",
        "🔌 Interface & Integration Rationalization",
        "🔌 Ecosystem Connectors & Backstage Sync",
    ])

    # ==============================================================================
    # TAB 1: ESTATE CATALOG
    # ==============================================================================
    with tab_catalog:
        st.subheader("Platform Architecture Metamodel (PAM) Conformed Catalog")
    
        nodes = client.get_nodes()
        edges = client.get_edges()
        time_matrix = client.get_time_matrix()

        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        total_cost = sum(t.get("annual_run_cost", 0.0) for t in time_matrix)
        tier0_count = sum(1 for n in nodes if n.get("criticality") == "Tier-0")
        pii_edge_count = sum(1 for e in edges if e.get("contains_pii"))

        m1.metric("Registered PAM Nodes", len(nodes))
        m2.metric("ArchiMate Relations", len(edges))
        m3.metric("Tier-0 Mission Critical", tier0_count)
        m4.metric("Estate Annual Run Cost", f"${total_cost:,.0f}")

        # Filters
        st.markdown("---")
        f_col1, f_col2, f_col3 = st.columns(3)
    
        all_kinds = sorted(list({n.get("kind", "Microservice") for n in nodes}))
        all_teams = sorted(list({n.get("owner_team", "unassigned") for n in nodes}))
        all_tiers = ["All", "Tier-0", "Tier-1", "Tier-2", "Tier-3"]

        sel_kinds = f_col1.multiselect("Filter by Kind", all_kinds, default=all_kinds)
        sel_teams = f_col2.multiselect("Filter by Owning Team", all_teams, default=all_teams)
        sel_tier = f_col3.selectbox("Filter by Criticality Tier", all_tiers)

        filtered_nodes = [
            n for n in nodes
            if n.get("kind") in sel_kinds
            and n.get("owner_team") in sel_teams
            and (sel_tier == "All" or n.get("criticality") == sel_tier)
        ]

        st.write(f"Showing **{len(filtered_nodes)}** of **{len(nodes)}** conformed nodes:")
    
        df_nodes = pd.DataFrame(filtered_nodes)[["urn", "name", "kind", "owner_team", "criticality", "lifecycle_status"]]
        st.dataframe(df_nodes, use_container_width=True)

        with st.expander("🔍 Explore Relationship Graph Edges"):
            df_edges = pd.DataFrame(edges)[["source_urn", "target_urn", "relation", "protocol", "contains_pii"]]
            st.dataframe(df_edges, use_container_width=True)


    # ==============================================================================
    # TAB 2: LIVING ARCHITECTURE MAPS
    # ==============================================================================
    with tab_maps:
        st.subheader("Archify Living Architecture Topology")
        st.caption("Interactive, vector-grade architectural map generated directly from Databricks Unity Catalog conformed graph.")

        map_choice = st.radio(
            "Select Architecture View",
            ["Master Estate Living Map", "Blast Radius Simulation (Payments API)", "EA Sentinel PR Delta Diff"],
            horizontal=True
        )

        diagram_dir = PROJECT_ROOT / "data" / "diagrams"
    
        if map_choice == "Master Estate Living Map":
            html_file = diagram_dir / "architecture-view.html"
            if not html_file.exists():
                with st.spinner("Compiling master living architecture map..."):
                    bridge.compile_interactive_map(output_html_path=html_file)
        elif map_choice == "Blast Radius Simulation (Payments API)":
            html_file = diagram_dir / "blast_radius_payments-api.html"
            if not html_file.exists():
                with st.spinner("Compiling blast radius map..."):
                    navigator.compile_blast_radius_diagram("payments-api")
        else:
            html_file = diagram_dir / "diagram_delta.html"
            if not html_file.exists():
                with st.spinner("Compiling Sentinel delta map..."):
                    patch = (PROJECT_ROOT / "tests" / "fixtures" / "pr_unapproved_db.patch").read_text()
                    sentinel.evaluate_patch(patch)

        if html_file.exists():
            html_content = html_file.read_text(encoding="utf-8")
            components.html(html_content, height=720, scrolling=True)
        else:
            st.warning(f"Diagram not found at {html_file}. Click 'Regenerate' below.")

        if st.button("🔄 Regenerate Living Maps"):
            with st.spinner("Regenerating all Archify vector maps..."):
                bridge.compile_interactive_map(output_html_path=diagram_dir / "architecture-view.html")
                navigator.compile_blast_radius_diagram("payments-api")
                st.success("Living Maps updated cleanly.")
                st.rerun()


    # ==============================================================================
    # TAB 3: EA NAVIGATOR COCKPIT
    # ==============================================================================
    with tab_navigator:
        st.subheader("🧭 EA Navigator: Conversational Estate Intelligence & What-If Simulations")
        st.caption("Grounded reasoning over dependency graph, customer PII data flows, and TIME financial risk.")

        # Target Selector
        col_t1, col_t2 = st.columns([2, 1])
        node_names = sorted([n["name"] for n in nodes])
        default_idx = node_names.index("payments-api") if "payments-api" in node_names else 0
        selected_target = col_t1.selectbox("Focus Architectural Component", node_names, index=default_idx)

        # Co-Driving Action Chips
        st.markdown("**Interactive Co-Driving Scenarios:**")
        actions = navigator.get_codriving_actions(selected_target)
        act_cols = st.columns(len(actions))
    
        trigger_prompt = None
        for idx, act in enumerate(actions):
            if act_cols[idx].button(act["label"], use_container_width=True):
                trigger_prompt = act["query"]

        # Natural Language Inquiry Input
        user_query = st.text_input(
            "Ask EA Navigator about dependencies, regulatory compliance, or migration proposals:",
            value=trigger_prompt or f"What is the blast radius and financial exposure if {selected_target} experiences an outage?",
        )

        if user_query:
            with st.spinner("Traversing graph & computing blast radius..."):
                res = navigator.query(user_query)

            blast = res.get("blast_radius", {})
            fin = blast.get("financial_exposure", {})
            pii = blast.get("pii_compliance", {})

            # Metrics bar
            b_col1, b_col2, b_col3, b_col4 = st.columns(4)
            b_col1.metric("Upstream Callers at Risk", f"{blast.get('upstream_count', 0)} services")
            b_col2.metric("Annual Financial Exposure", f"${fin.get('total_annual_risk_usd', 0.0):,.2f}")
            b_col3.metric("Max Affected Criticality", blast.get("aggregate_criticality", "Tier-2"))
            b_col4.metric("Customer PII Lineage", "⚠️ DETECTED" if pii.get("has_pii_exposure") else "✅ CLEAN")

            # Response content
            st.markdown(res["answer"])

            # Embedded dynamic blast radius map
            diag_path = Path(res["diagrams"]["html_path"])
            if diag_path.exists():
                st.markdown("#### 🗺️ Dynamic Visual Blast Radius Map")
                components.html(diag_path.read_text(encoding="utf-8"), height=580, scrolling=True)

            # ADR Expander
            with st.expander("📝 View / Export Target-State Architecture Decision Record (MADR)"):
                madr_text = navigator.generate_madr(selected_target)
                st.markdown(madr_text)
                st.download_button(
                    label="📥 Download MADR (.md)",
                    data=madr_text,
                    file_name=f"ADR_{selected_target}_modernization.md",
                    mime="text/markdown",
                )


    # ==============================================================================
    # TAB 11: INTERFACE & INTEGRATION LANDSCAPE RATIONALIZATION
    # ==============================================================================
    with tab_interfaces:
        st.subheader("🔌 Interface & Integration Landscape Rationalization")
        st.caption("Reconciliation of declared OpenAPI/gRPC contracts against live runtime API gateway traffic logs. Automatic detection of Zombie/Shadow APIs, Dead/Orphan routes, and Protocol Sprawl.")

        interface_metrics = navigator.analyze_interface_landscape()
        reconciled_interfaces = client.get_interface_rationalization() or interface_metrics["all_reconciled_interfaces"]
        gateway_logs = client.get_api_gateway_logs() or interface_metrics["gateway_logs"]

        # 5 KPI Metric Cards
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Reconciled Interfaces", f"{interface_metrics['total_interfaces_count']}", f"{interface_metrics['declared_interfaces_count']} Declared")
        k2.metric("Active Runtime Traffic", f"{interface_metrics['runtime_interfaces_count']}", "100% Ingress Audited")
        k3.metric("Compliant Contracts", f"{interface_metrics['compliant_interfaces_count']}", "REST/OAuth2, gRPC/mTLS")
        k4.metric("Zombie / Shadow APIs", f"{interface_metrics['zombie_shadow_count']}", "Undocumented Ingress", delta_color="inverse")
        k5.metric("Dead APIs / Protocol Sprawl", f"{interface_metrics['dead_orphan_count'] + interface_metrics['protocol_sprawl_count']}", "Decommission / Upgrade", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### 📋 Conformed Interface Rationalization Mart (`ea.gold.interface_rationalization`)")
        st.caption("Authoritative interface inventory tracking declared contract status, runtime gateway activity, discrepancy classifications, and recommended architectural actions.")

        # Discrepancy Filter
        disc_filter = st.selectbox(
            "Filter by Discrepancy Type:",
            ["All Discrepancies", "COMPLIANT", "ZOMBIE_SHADOW", "DEAD_ORPHAN", "PROTOCOL_SPRAWL"],
            key="iface_disc_filter",
        )

        filtered_interfaces = reconciled_interfaces
        if disc_filter != "All Discrepancies":
            filtered_interfaces = [r for r in reconciled_interfaces if r.get("discrepancy_type") == disc_filter]

        if filtered_interfaces:
            df_iface = pd.DataFrame(filtered_interfaces)[[
                "interface_id", "endpoint", "method", "protocol", "provider_service",
                "consumer_service", "is_declared", "is_active_runtime", "discrepancy_type",
                "rationalization_action", "last_active_timestamp"
            ]]
            st.dataframe(df_iface, use_container_width=True)
            st.download_button(
                label="📥 Download Interface Rationalization (CSV)",
                data=df_iface.to_csv(index=False),
                file_name="ea_gold_interface_rationalization.csv",
                mime="text/csv",
            )

        st.markdown("---")
        st.markdown("#### 🚨 Architectural Rationalization Actions")
        st.caption("Actionable governance remedies for identified shadow endpoints, orphaned routes, and protocol sprawl.")

        a_cols = st.columns(3)
        for idx, act in enumerate(interface_metrics["rationalization_actions"]):
            col = a_cols[idx % 3]
            with col:
                act_color = "#ef4444" if act.get("discrepancy_type") == "ZOMBIE_SHADOW" else ("#f59e0b" if act.get("discrepancy_type") == "PROTOCOL_SPRAWL" else "#64748b")
                st.markdown(f"""
                <div style="background: #0f172a; border-left: 4px solid {act_color}; border-radius: 8px; padding: 14px; margin-bottom: 12px; border: 1px solid #1e293b; min-height: 220px;">
                    <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">
                        {act['action']} 
                        <span style="font-size: 11px; color: {act_color}; background: #1e293b; padding: 2px 6px; border-radius: 4px; margin-left: 8px;">{act.get('discrepancy_type')}</span>
                    </div>
                    <div style="margin-top: 6px; font-size: 13px; color: #94a3b8;">
                        <strong>Endpoint:</strong> <code style="color: #fda4af;">{act['endpoint']}</code> ({act['method']})<br/>
                        <strong>Route:</strong> <code style="color: #6ee7b7;">{act['consumer']} ➔ {act['provider']}</code>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #cbd5e1;">
                        {act['details']}
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>Remediation: {act['remediation']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        diag_tab1, diag_tab2 = st.tabs(["🗺️ Interface Landscape Topology Map", "⚡ Checkout & Payment Transaction Sequence"])

        with diag_tab1:
            st.caption("Interactive Archify vector living map isolating compliant enterprise interfaces from shadow endpoints and legacy protocol sprawl.")
            iface_diag_path = ROOT_DIR / "data" / "diagrams" / "interface_landscape.html"
            if not iface_diag_path.exists():
                navigator.compile_interface_landscape_diagram()
            if iface_diag_path.exists():
                html_code = iface_diag_path.read_text(encoding="utf-8")
                st.components.v1.html(html_code, height=650, scrolling=True)
            else:
                st.warning("Interface landscape diagram could not be loaded.")

        with diag_tab2:
            st.caption("Interactive Archify sequence diagram tracing the end-to-end checkout, payment authorization, and ledger synchronization transaction flow.")
            seq_diag_path = ROOT_DIR / "data" / "diagrams" / "interface_sequence.html"
            if not seq_diag_path.exists():
                navigator.compile_interface_sequence_diagram()
            if seq_diag_path.exists():
                seq_code = seq_diag_path.read_text(encoding="utf-8")
                st.components.v1.html(seq_code, height=650, scrolling=True)
            else:
                st.warning("Interface sequence diagram could not be loaded.")

    # ==============================================================================
    # TAB 5: ECOSYSTEM CONNECTORS & BACKSTAGE SYNC
    # ==============================================================================
    with tab_ecosystem:
        st.subheader("🔌 Enterprise Ecosystem Connectors & Backstage Sync")
        st.caption("Live integration backbone connecting The Agentic EA Platform to Git repositories, ITSM change management, architecture backlog, and developer service portals.")

        if st.button("🔄 Test All Ecosystem Connections", use_container_width=True):
            conn_mgr = ConnectorManager()
            with st.spinner("Executing health checks across GitHub, ServiceNow, Jira, and Backstage..."):
                st.session_state["connector_health"] = conn_mgr.test_all_connections()

        health = st.session_state.get("connector_health")
        if not health:
            conn_mgr = ConnectorManager()
            health = conn_mgr.test_all_connections()
            st.session_state["connector_health"] = health

        st.markdown("#### Live Connector Telemetry")
        c1, c2, c3, c4 = st.columns(4)

        connector_meta = [
            ("github", "🐙 GitHub REST API", c1),
            ("servicenow", "📋 ServiceNow CMDB", c2),
            ("jira", "🎯 Atlassian Jira", c3),
            ("backstage", "🎭 Spotify Backstage", c4),
        ]

        status_styles = {
            "CONNECTED": ("🟢", "#10b981", "Connected & Healthy"),
            "AUTH_ERROR": ("🔴", "#ef4444", "Authentication Failed"),
            "UNREACHABLE": ("🟠", "#f59e0b", "Endpoint Unreachable"),
            "UNCONFIGURED": ("⚪", "#64748b", "Not Configured"),
        }

        for key, title, col in connector_meta:
            res = health.get(key, {})
            st_code = res.get("status", "UNCONFIGURED")
            icon, color, label = status_styles.get(st_code, ("⚪", "#64748b", "Unknown"))
            latency = res.get("latency_ms", 0.0)

            with col:
                st.markdown(f"""
                <div style="background: #131b2e; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; margin-bottom: 10px;">
                    <div style="font-weight: 600; font-size: 1.05rem; margin-bottom: 4px;">{title}</div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 1.1rem;">{icon}</span>
                        <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">{st_code}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px;">Latency: <strong>{latency:.1f} ms</strong></div>
                    <div style="font-size: 0.75rem; color: #cbd5e1; line-height: 1.3;">{res.get('message', '')[:90]}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        b_col1, b_col2 = st.columns([3, 2])

        with b_col1:
            st.markdown("### 🎭 Spotify Backstage Catalog Conformance")
            st.caption("Bidirectional translation between Platform Architecture Metamodel (PAM) nodes and Backstage catalog-info.yaml entities.")

            bs_conn = BackstageConnector()
            pam_nodes = client.get_nodes()
            exported_entities = bs_conn.export_pam_nodes_to_backstage_entities(pam_nodes)

            catalog_preview = []
            for e in exported_entities:
                catalog_preview.append({
                    "Name": e.get("metadata", {}).get("name"),
                    "Kind": e.get("kind"),
                    "Type": e.get("spec", {}).get("type"),
                    "Lifecycle": e.get("spec", {}).get("lifecycle"),
                    "Owner": e.get("spec", {}).get("owner"),
                    "URN": e.get("metadata", {}).get("annotations", {}).get("ea.governance/urn"),
                })
            st.dataframe(pd.DataFrame(catalog_preview), use_container_width=True, height=280)

        with b_col2:
            st.markdown("### 📦 Backstage TechDocs Publishing")
            st.caption("Generate complete Markdown TechDocs bundles with Archify diagram embeds and Architectural Decision Records (MADRs).")

            if st.button("🚀 Generate Backstage TechDocs Package", use_container_width=True):
                bs_conn = BackstageConnector()
                adrs = [
                    {
                        "number": "0001",
                        "title": "Adopt CockroachDB for Distributed Orders",
                        "status": "Accepted",
                        "date": "2026-10-20",
                        "context": "Need multi-region transactional consistency without SPOF.",
                        "decision": "Migrate to managed CockroachDB cluster.",
                    },
                    {
                        "number": "0002",
                        "title": "Standardize Unity Catalog as Master Source of Truth",
                        "status": "Accepted",
                        "date": "2026-10-20",
                        "context": "S06 CMDB and S17 MDM golden record governance.",
                        "decision": "Enforce Unity Catalog Delta tables for all metamodel telemetry.",
                    },
                ]
                bundle = bs_conn.generate_techdocs_bundle("enterprise-architecture-estate", adrs=adrs)

                # Write bundle to data/backstage/
                backstage_dir = ROOT_DIR / "data" / "backstage"
                (backstage_dir / "docs" / "adrs").mkdir(parents=True, exist_ok=True)

                for file_path, content in bundle.items():
                    out_file = backstage_dir / file_path
                    out_file.parent.mkdir(parents=True, exist_ok=True)
                    out_file.write_text(content, encoding="utf-8")

                # Also write catalog-info.yaml
                import yaml
                try:
                    cat_yaml = yaml.dump_all(exported_entities, sort_keys=False)
                except Exception:
                    cat_yaml = json.dumps(exported_entities, indent=2)
                (backstage_dir / "catalog-info.yaml").write_text(cat_yaml, encoding="utf-8")

                st.success(f"✓ Backstage TechDocs package compiled ({len(bundle)} files + catalog-info.yaml) in `data/backstage/`!")

            backstage_dir = ROOT_DIR / "data" / "backstage"
            mkdocs_file = backstage_dir / "mkdocs.yml"
            if mkdocs_file.exists():
                with st.expander("📄 View Generated mkdocs.yml"):
                    st.code(mkdocs_file.read_text(encoding="utf-8"), language="yaml")

            cat_file = backstage_dir / "catalog-info.yaml"
            if cat_file.exists():
                with st.expander("📄 View Generated catalog-info.yaml"):
                    st.code(cat_file.read_text(encoding="utf-8")[:1500], language="yaml")

        st.markdown("---")
        st.markdown("### 🛡️ GitHub EA Sentinel Commit Status & PR Gate")
        st.caption("Automated pre-merge gating integrating EA Sentinel policy evaluations with GitHub commit status checks.")

        pr_col1, pr_col2 = st.columns([2, 3])
        with pr_col1:
            gh_repo = st.text_input("GitHub Target Repository", value="enterprise/checkout-service")
            gh_sha = st.text_input("Commit SHA", value="e8f49a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f")
            sim_gate = st.selectbox("Simulate PR Gate Outcome", ["Approved Clean Patch", "Violating Patch (Cassandra / PII)"])

        with pr_col2:
            if st.button("🧪 Simulate GitHub Commit Status Dispatch", use_container_width=True):
                if "Clean" in sim_gate:
                    state = "success"
                    desc = "All EA Sentinel architectural governance policies passed."
                    comment_preview = "### ✅ EA Sentinel Pre-Merge Gate: APPROVED\\n* **EA-POL-001**: Passed\\n* **EA-POL-002**: Passed\\n* **EA-POL-003**: Passed"
                else:
                    state = "failure"
                    desc = "EA Sentinel: 3 policy violations detected (EA-POL-001, 002, 003)."
                    comment_preview = "### ❌ EA Sentinel Pre-Merge Gate: REJECTED\\n* **EA-POL-001**: Unapproved datastore `cassandra`.\\n* **EA-POL-002**: Unencrypted customer PII flow.\\n* **EA-POL-003**: Missing mandatory OwnerTeam/Tier tags."

                st.markdown(f"""
                <div style="background: #1e293b; border-left: 4px solid {'#10b981' if state == 'success' else '#ef4444'}; padding: 12px; border-radius: 4px; margin-bottom: 10px;">
                    <strong>GitHub Status Payload:</strong><br/>
                    <code>POST /repos/{gh_repo}/statuses/{gh_sha[:10]}</code><br/>
                    State: <strong>{state.upper()}</strong> | Context: <code>ea/sentinel-gate</code><br/>
                    Description: <em>{desc}</em>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("View PR Markdown Comment"):
                    st.markdown(comment_preview)



# ==============================================================================
# WORKSPACE 4: OPERATIONS, RESILIENCE & FINOPS
# ==============================================================================
elif workspace == "⚙️ Operations, Resilience & FinOps":
    tab_cmdb, tab_process, tab_resilience_finops = st.tabs([
        "🔄 CMDB Baseline Hygiene & Drift",
        "⏱️ Business Process Optimization & Customer Journey",
        "🛡️ Operations, Resilience & FinOps Hub",
    ])

    # ==============================================================================
    # TAB 8: SERVICENOW CMDB BASELINE HYGIENE & DRIFT
    # ==============================================================================
    with tab_cmdb:
        st.subheader("🔄 Continuous ServiceNow CMDB Synchronization & Baseline Hygiene")
        st.caption("Automated 3-way reconciliation between ServiceNow CMDB CIs (ea.bronze.cmdb_ci), Git architecture (ea.metamodel.nodes), and runtime Cloud CUR telemetry (ea.bronze.cloud_resources).")

        hygiene = navigator.get_cmdb_hygiene_metrics()
        cmdb_cis = client.get_cmdb_ci()
        drift_records = client.get_drift_reconciled()

        # KPI Metrics Bar
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total CMDB CIs", f"{hygiene['total_cmdb_cis']} CIs", "ServiceNow Table API")
        k2.metric("In-Sync Baseline", f"{hygiene['in_sync_percentage']}%", f"{hygiene['in_sync_count']} Authoritative")
        k3.metric("Orphan Records", f"{hygiene['orphan_ci_count']}", "Terminated in Cloud", delta_color="inverse")
        k4.metric("Shadow IT", f"{hygiene['shadow_it_count']}", "Missing in CMDB", delta_color="inverse")
        k5.metric("Attribute Drift", f"{hygiene['attribute_drift_count']}", "Metadata Mismatch", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### 🚨 Reconciled Estate Drift & CMDB Discrepancy Taxonomy")
        st.caption("Conformed mart `ea.gold.drift_reconciled` categorizing discrepancies and providing actionable remediation.")

        # Drift Type Filter
        drift_filter = st.selectbox(
            "Filter by Discrepancy Taxonomy:",
            ["All Discrepancies", "ORPHAN_CI (Terminated in Cloud, Active in CMDB)", "SHADOW_IT (Running in Cloud/Git, Missing in CMDB)", "ATTRIBUTE_DRIFT (Mismatched Tier/Env/Lifecycle)", "POLICY_VIOLATION (Unapproved Datastores / Security)"],
            index=0
        )

        filtered_drift = drift_records
        if "ORPHAN_CI" in drift_filter:
            filtered_drift = [d for d in drift_records if d.get("drift_type") == "ORPHAN_CI"]
        elif "SHADOW_IT" in drift_filter:
            filtered_drift = [d for d in drift_records if d.get("drift_type") == "SHADOW_IT"]
        elif "ATTRIBUTE_DRIFT" in drift_filter:
            filtered_drift = [d for d in drift_records if d.get("drift_type") == "ATTRIBUTE_DRIFT"]
        elif "POLICY_VIOLATION" in drift_filter:
            filtered_drift = [d for d in drift_records if d.get("drift_type") == "POLICY_VIOLATION"]

        if filtered_drift:
            df_d = pd.DataFrame(filtered_drift)[[
                "drift_id", "ci_name", "drift_type", "severity", "discrepancy_type",
                "remediation_action", "declared_state", "runtime_state", "reconciled_at"
            ]]
            st.dataframe(df_d, use_container_width=True)

            st.markdown("#### ⚡ Automated ServiceNow REST API Remediation Payloads")
            st.caption("Pre-compiled Table API payloads ready for automated dispatch to bring CMDB into 100% hygiene alignment.")

            for d in filtered_drift:
                with st.expander(f"🔧 [{d.get('severity', 'HIGH')}] {d.get('drift_type')} — `{d.get('ci_name')}` ➔ Action: `{d.get('remediation_action')}`"):
                    st.markdown(f"**Discrepancy Detail:** {d.get('discrepancy_type')}")
                    st.markdown(f"**Declared Baseline:** {d.get('declared_state')}")
                    st.markdown(f"**Observed Runtime:** {d.get('runtime_state')}")
                    st.markdown("**Automated ServiceNow Remediation Payload (JSON):**")
                    payload = navigator.generate_cmdb_remediation_payload(d.get("drift_id", ""))
                    st.json(payload or d.get("remediation_payload", "{}"))
        else:
            st.success("✅ Zero drift discrepancies detected for selected filter.")

        st.markdown("---")
        st.markdown("#### 📦 Raw ServiceNow CMDB Inventory (`ea.bronze.cmdb_ci`)")
        if cmdb_cis:
            df_cmdb = pd.DataFrame(cmdb_cis)[[
                "sys_id", "name", "ci_class", "operational_status", "environment",
                "tier", "owner_team", "ip_address", "cloud_resource_id", "synced_at"
            ]]
            st.dataframe(df_cmdb, use_container_width=True)
            st.download_button(
                label="📥 Download ServiceNow CMDB CIs (CSV)",
                data=df_cmdb.to_csv(index=False),
                file_name="ea_bronze_cmdb_ci.csv",
                mime="text/csv",
            )


    # ==============================================================================
    # TAB 12: BUSINESS PROCESS OPTIMIZATION & CUSTOMER JOURNEY
    # ==============================================================================
    with tab_process:
        st.markdown("### ⏱️ Business Process Optimization & Customer Journey Traceability")
        st.caption("Reconciles runtime execution trace spans (`ea.bronze.process_event_logs`) against enterprise SLAs (`ea.gold.process_optimization`) to pinpoint latency bottlenecks, compute journey cycle times, and recommend modernization paths.")

        proc_data = navigator.analyze_business_processes()

        # 5 KPI Metric Cards
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
        col_p1.metric("End-to-End Latency", f"{int(proc_data['journey_p95_ms'])} ms", "p95 Cycle Time")
        col_p2.metric("Journey SLA Target", f"{int(proc_data['sla_target_ms'])} ms", "1,000 ms SLA")
        col_p3.metric("SLA Status", "🚨 CRITICAL BREACH", f"+{int(proc_data['sla_breach_ms'])} ms", delta_color="inverse")
        col_p4.metric("Primary Bottleneck", "Cassandra Query", f"{int(proc_data['bottleneck_p95_ms'])} ms ({proc_data['bottleneck_latency_pct']}%)", delta_color="inverse")
        col_p5.metric("Optimized Target", f"{int(proc_data['optimized_journey_p95_ms'])} ms", f"-{int(proc_data['latency_reduction_ms'])} ms (-{proc_data['latency_reduction_pct']}%)")

        st.markdown("---")
        st.markdown("#### 📊 Order-to-Cash Customer Journey Stage Matrix (`ea.gold.process_optimization`)")

        steps_df = pd.DataFrame(proc_data["steps"])
        if not steps_df.empty:
            steps_display = steps_df[[
                "step_id", "step_name", "service_urn", "p50_latency_ms",
                "p95_latency_ms", "p99_latency_ms", "sla_target_ms",
                "error_rate_pct", "is_bottleneck", "optimization_action"
            ]].copy()
            steps_display["service"] = steps_display["service_urn"].apply(lambda u: u.split(":")[-1])
            steps_display["p50"] = steps_display["p50_latency_ms"].apply(lambda v: f"{int(v)} ms")
            steps_display["p95"] = steps_display["p95_latency_ms"].apply(lambda v: f"{int(v)} ms")
            steps_display["p99"] = steps_display["p99_latency_ms"].apply(lambda v: f"{int(v)} ms")
            steps_display["sla"] = steps_display["sla_target_ms"].apply(lambda v: f"{int(v)} ms")
            steps_display["error_rate"] = steps_display["error_rate_pct"].apply(lambda v: f"{v:.2f}%")
            steps_display["status"] = steps_display["is_bottleneck"].apply(lambda b: "🚨 BOTTLENECK" if b else "✅ COMPLIANT")

            st.dataframe(
                steps_display[["step_id", "step_name", "service", "p50", "p95", "p99", "sla", "error_rate", "status", "optimization_action"]],
                use_container_width=True,
            )

            st.download_button(
                label="📥 Export Process Optimization Matrix (CSV)",
                data=steps_df.to_csv(index=False),
                file_name="ea_gold_process_optimization.csv",
                mime="text/csv",
            )

        st.markdown("---")
        st.markdown("#### 🚀 Target-State Modernization & Latency Optimization Roadmap")
        rec_col1, rec_col2 = st.columns(2)

        for idx, rec in enumerate(proc_data["recommendations"]):
            target_col = rec_col1 if idx % 2 == 0 else rec_col2
            with target_col:
                st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #f8fafc; font-size: 15px;">{rec['step_name']} ({rec['step_id']})</span>
                        <span style="background: #1e293b; color: #38bdf8; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{rec['action']}</span>
                    </div>
                    <div style="margin-top: 8px; font-size: 13px; color: #94a3b8;">
                        <strong>Service:</strong> <code>{rec['service_urn'].split(':')[-1]}</code> | 
                        <strong>Current p95:</strong> <span style="color: #f43f5e; font-weight: bold;">{int(rec['current_p95_ms'])} ms</span> ➔ 
                        <strong>Target p95:</strong> <span style="color: #10b981; font-weight: bold;">{int(rec['target_p95_ms'])} ms</span>
                        (<span style="color: #38bdf8;">-{int(rec['latency_reduction_ms'])} ms / -{rec['latency_reduction_pct']}%</span>)
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #cbd5e1;">
                        {rec['details']}
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>Remediation: {rec['remediation']}</em>
                    </div>
                    <div style="margin-top: 6px; font-size: 12px; color: #10b981;">
                        🎯 <em>Impact: {rec['impact']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗺️ Order-to-Cash Interactive Process Workflow Diagram")
        st.caption("Interactive Archify vector workflow diagram tracing Order-to-Cash journey stages, latency badges, SLA breach path, and Lakehouse target-state.")

        wf_diag_path = ROOT_DIR / "data" / "diagrams" / "customer_journey_workflow.html"
        if not wf_diag_path.exists():
            navigator.compile_customer_journey_workflow_diagram()
        if wf_diag_path.exists():
            html_code = wf_diag_path.read_text(encoding="utf-8")
            st.components.v1.html(html_code, height=650, scrolling=True)
        else:
            st.warning("Customer journey workflow diagram could not be loaded.")


    # ==============================================================================
    # TAB 14: OPERATIONS, RESILIENCE & FINOPS HUB (S12–S16)
    # ==============================================================================
    with tab_resilience_finops:
        st.subheader("🛡️ Enterprise Operations, Resilience & FinOps Hub (S12–S16)")
        st.caption("Unified telemetry hub synthesizing Disaster Recovery (S12), Technical Debt (S13), Zero-Trust Microsegmentation (S14), Supply Chain SBOM (S15), and FinOps Unit Economics (S16).")

        op_data = navigator.analyze_operations_resilience_finops()

        # 5 KPI Metric Cards
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        kpi1.metric("DR SLA Breaches", f"{op_data['sla_breached_count']} Breaches", delta="Cassandra SPOF", delta_color="inverse")
        kpi2.metric("Avg Tech Debt", f"{op_data['avg_debt_score']}/100", delta="Cassandra #1 (92)", delta_color="inverse")
        kpi3.metric("Zero-Trust Mesh", f"{op_data['zero_trust_compliance_pct']}%", delta="2 Flagged Flows", delta_color="inverse")
        kpi4.metric("SBOM Violations", f"{len(op_data['copyleft_violations'])} Copyleft / {len(op_data['critical_cves'])} CVE", delta="GPL-3.0 Flagged", delta_color="inverse")
        kpi5.metric("FinOps Cost / Order", f"${op_data['unit_cost_per_order']:.3f}", delta=f"${op_data['cassandra_monthly_idle_waste_usd']:,.0f}/mo Idle Waste", delta_color="inverse")

        st.markdown("---")

        subtab_dr, subtab_debt, subtab_zt, subtab_sbom, subtab_finops = st.tabs([
            "🔥 S12: Disaster Recovery",
            "📉 S13: Tech Debt Hotspots",
            "🔒 S14: Zero-Trust Security",
            "📦 S15: Supply Chain SBOM",
            "💰 S16: FinOps Unit Economics",
        ])

        with subtab_dr:
            st.markdown("#### Disaster Recovery & ICT Resilience Matrix (`ea.gold.resilience_dr`)")
            st.caption("Evaluates multi-region failover automation and RTO/RPO SLA compliance against DORA ICT standards.")
            dr_rows = op_data["dr_records"]
            if dr_rows:
                df_dr = pd.DataFrame(dr_rows)
                df_dr_disp = df_dr.copy()
                df_dr_disp["sla_status"] = df_dr_disp["sla_breached"].apply(lambda b: "🔴 BREACHED" if b else "🟢 COMPLIANT")
                df_dr_disp["component"] = df_dr_disp["component_urn"].apply(lambda u: u.split(":")[-1])
                st.dataframe(
                    df_dr_disp[[
                        "component", "dr_tier", "rto_actual_min", "rto_target_min",
                        "rpo_actual_min", "rpo_target_min", "replication_strategy",
                        "failover_automation", "sla_status"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export DR Resilience Ledger (CSV)",
                    data=df_dr.to_csv(index=False),
                    file_name="ea_gold_resilience_dr.csv",
                    mime="text/csv",
                )

        with subtab_debt:
            st.markdown("#### Technical Debt Hotspots & Refactoring Prioritization (`ea.gold.tech_debt_hotspots`)")
            st.caption("Correlates 30-day git churn, cyclomatic complexity, and architectural smells to rank refactoring ROI.")
            debt_rows = op_data["debt_records"]
            if debt_rows:
                df_debt = pd.DataFrame(debt_rows)
                df_debt_disp = df_debt.copy()
                df_debt_disp["component"] = df_debt_disp["component_urn"].apply(lambda u: u.split(":")[-1])
                st.dataframe(
                    df_debt_disp[[
                        "refactoring_roi_rank", "component", "debt_score",
                        "git_churn_lines_30d", "cyclomatic_complexity", "architectural_smells"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export Tech Debt Hotspots (CSV)",
                    data=df_debt.to_csv(index=False),
                    file_name="ea_gold_tech_debt_hotspots.csv",
                    mime="text/csv",
                )

        with subtab_zt:
            st.markdown("#### Zero-Trust Microsegmentation & Transit Encryption (`ea.gold.security_zero_trust`)")
            st.caption("Monitors trust zone crossings, mTLS enforcement, and flags unauthorized cross-zone egress.")
            sec_rows = op_data["security_records"]
            if sec_rows:
                df_sec = pd.DataFrame(sec_rows)
                df_sec_disp = df_sec.copy()
                df_sec_disp["source"] = df_sec_disp["source_urn"].apply(lambda u: u.split(":")[-1])
                df_sec_disp["target"] = df_sec_disp["target_urn"].apply(lambda u: u.split(":")[-1])
                df_sec_disp["mtls"] = df_sec_disp["mtls_enforced"].apply(lambda b: "🔒 Enforced" if b else "⚠️ None")
                df_sec_disp["status"] = df_sec_disp["microsegmentation_status"].apply(
                    lambda s: "🟢 COMPLIANT" if s == "COMPLIANT" else f"🔴 {s}"
                )
                st.dataframe(
                    df_sec_disp[[
                        "source", "target", "protocol", "mtls",
                        "trust_zone_source", "trust_zone_target", "status"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export Zero-Trust Registry (CSV)",
                    data=df_sec.to_csv(index=False),
                    file_name="ea_gold_security_zero_trust.csv",
                    mime="text/csv",
                )

        with subtab_sbom:
            st.markdown("#### Software Bill of Materials (SBOM) & License Compliance (`ea.gold.supply_chain_sbom`)")
            st.caption("Tracks third-party package dependencies, copyleft license risks (GPL-3.0), and vulnerability CVE severities.")
            sbom_rows = op_data["sbom_records"]
            if sbom_rows:
                df_sbom = pd.DataFrame(sbom_rows)
                df_sbom_disp = df_sbom.copy()
                df_sbom_disp["component"] = df_sbom_disp["component_urn"].apply(lambda u: u.split(":")[-1])
                df_sbom_disp["compliance"] = df_sbom_disp["license_compliance"].apply(
                    lambda c: "🟢 APPROVED" if c == "APPROVED" else "🔴 PROHIBITED"
                )
                df_sbom_disp["severity"] = df_sbom_disp["max_severity"].apply(
                    lambda s: "🚨 CRITICAL" if s == "CRITICAL" else ("⚠️ HIGH" if s == "HIGH" else "✅ NONE")
                )
                st.dataframe(
                    df_sbom_disp[[
                        "package_name", "version", "component", "license",
                        "compliance", "cve_count", "severity"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export SBOM & License Ledger (CSV)",
                    data=df_sbom.to_csv(index=False),
                    file_name="ea_gold_supply_chain_sbom.csv",
                    mime="text/csv",
                )

        with subtab_finops:
            st.markdown("#### FinOps Unit Economics & Idle Waste Elimination (`ea.gold.finops_unit_economics`)")
            st.caption("Attributes cloud spend to business unit transactions ($0.042/order) and detects untagged idle compute waste.")
            fin_rows = op_data["finops_records"]
            if fin_rows:
                df_fin = pd.DataFrame(fin_rows)
                df_fin_disp = df_fin.copy()
                df_fin_disp["service"] = df_fin_disp["service_urn"].apply(lambda u: u.split(":")[-1])
                df_fin_disp["monthly_spend_fmt"] = df_fin_disp["monthly_spend"].apply(lambda v: f"${v:,.2f}")
                df_fin_disp["cost_per_order"] = df_fin_disp["cost_per_transaction"].apply(lambda v: f"${v:.3f}" if v > 0 else "N/A")
                df_fin_disp["tag_compliance"] = df_fin_disp["tag_compliance_pct"].apply(lambda v: f"{v:.1f}%")
                df_fin_disp["waste_fmt"] = df_fin_disp["idle_waste_cost"].apply(lambda v: f"${v:,.2f}" if v > 0 else "$0.00")
                st.dataframe(
                    df_fin_disp[[
                        "service", "monthly_spend_fmt", "cost_per_order",
                        "tag_compliance", "waste_fmt", "optimization_action"
                    ]],
                    use_container_width=True,
                )
                st.download_button(
                    label="📥 Export FinOps Unit Economics (CSV)",
                    data=df_fin.to_csv(index=False),
                    file_name="ea_gold_finops_unit_economics.csv",
                    mime="text/csv",
                )

        st.markdown("---")
        st.markdown("#### 🛠️ Priority Operations Modernization & Remediation Actions")
        op_col1, op_col2 = st.columns(2)

        for idx, act in enumerate(op_data["operational_actions"]):
            target_col = op_col1 if idx % 2 == 0 else op_col2
            with target_col:
                st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #f8fafc; font-size: 15px;">{act['component']}</span>
                        <span style="background: #1e293b; color: #38bdf8; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{act['domain']}</span>
                    </div>
                    <div style="margin-top: 8px; font-size: 13px; color: #f43f5e; font-weight: 600;">
                        {act['risk']}
                    </div>
                    <div style="margin-top: 6px; font-size: 13px; color: #94a3b8;">
                        <strong>Action:</strong> <code>{act['action']}</code>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #38bdf8;">
                        💡 <em>Remediation: {act['remediation']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🗺️ Interactive Resilience, Zero-Trust Perimeter & Operations Map")
        st.caption("Interactive Archify vector map displaying perimeter isolation (DMZ Ingress, Core Application Mesh, Secure Data Vault, External Egress), DR failovers, and FinOps waste.")

        res_diag_path = ROOT_DIR / "data" / "diagrams" / "resilience_and_perimeter_view.html"
        if not res_diag_path.exists():
            navigator.compile_resilience_and_perimeter_diagram()
        if res_diag_path.exists():
            html_code = res_diag_path.read_text(encoding="utf-8")
            st.components.v1.html(html_code, height=650, scrolling=True)
        else:
            st.warning("Resilience and perimeter diagram could not be loaded.")


