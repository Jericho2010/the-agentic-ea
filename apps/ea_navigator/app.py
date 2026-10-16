"""
The Agentic EA Platform - Databricks Apps UI Cockpit.
Native Streamlit Application deployable directly inside Databricks Apps.
Target Workspace: https://dbc-2d6963b0-153b.cloud.databricks.com/
Catalog: ea (Unity Catalog)
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.archify.bridge import ArchifyBridge
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
    .stMetric {
        background: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px;
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

# Navigation Tabs
tab_catalog, tab_maps, tab_navigator, tab_sentinel, tab_time = st.tabs([
    "🏛️ Estate Catalog",
    "🗺️ Living Architecture Maps",
    "🧭 EA Navigator Cockpit",
    "🛡️ EA Sentinel Governance",
    "📊 Executive TIME Matrix"
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

    if "Cassandra" in sample_pr:
        patch_file = PROJECT_ROOT / "tests" / "fixtures" / "pr_unapproved_db.patch"
    else:
        patch_file = PROJECT_ROOT / "tests" / "fixtures" / "pr_clean.patch"

    patch_content = patch_file.read_text(encoding="utf-8")
    
    with st.expander("📄 View Pull Request Diff"):
        st.code(patch_content, language="diff")

    if st.button("🚀 Evaluate PR with EA Sentinel Gate", type="primary"):
        with st.spinner(f"Evaluating PR diff via Tri-Modal option: {provider_choice}..."):
            gate_eval = EASentinelGate(provider=provider_choice)
            res = gate_eval.evaluate_patch(patch_content)

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


# ==============================================================================
# TAB 5: EXECUTIVE TIME MATRIX
# ==============================================================================
with tab_time:
    st.subheader("📊 Executive TIME Matrix & Architecture Drift")
    st.caption("Gartner TIME Quadrant Portfolio Assessment (Invest, Tolerate, Migrate, Eliminate) with FinOps Run-Cost Tracking.")

    time_data = client.get_time_matrix()
    drift_data = client.get_drift_reconciled()

    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    
    invest_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Invest")
    tolerate_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Tolerate")
    migrate_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Migrate")
    eliminate_cost = sum(t["annual_run_cost"] for t in time_data if t["disposition"] == "Eliminate")

    t_col1.metric("Invest (Grow & Modernize)", f"${invest_cost:,.0f}/yr")
    t_col2.metric("Tolerate (Stable Operations)", f"${tolerate_cost:,.0f}/yr")
    t_col3.metric("Migrate (High Tech Debt)", f"${migrate_cost:,.0f}/yr")
    t_col4.metric("Eliminate (Target Sunset)", f"${eliminate_cost:,.0f}/yr")

    st.markdown("---")
    st.markdown("#### Portfolio Systems Classification")
    df_time = pd.DataFrame(time_data)[["name", "urn", "disposition", "annual_run_cost", "tech_debt_score", "eol_date"]]
    st.dataframe(df_time, use_container_width=True)

    st.markdown("#### ⚠️ Reconciled Architectural Drift (Declared vs Runtime Telemetry)")
    if drift_data:
        df_drift = pd.DataFrame(drift_data)[["urn", "discrepancy_type", "severity", "declared_state", "runtime_state", "reconciled_at"]]
        st.dataframe(df_drift, use_container_width=True)
    else:
        st.info("Zero architecture drift detected across live estate telemetry.")
