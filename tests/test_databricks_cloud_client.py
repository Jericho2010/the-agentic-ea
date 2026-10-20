"""
Unit and Integration Tests for Databricks Unity Catalog Cloud Client.
Validates:
1. Completeness of TABLE_MAP across all 27 conformed metamodel, bronze, and gold tables.
2. Bidirectional SQL translation between local and Unity Catalog 3-level namespaces.
3. Offline SQLite execution fallback routing.
4. Live Databricks SQL Warehouse connectivity and query execution.
"""
from __future__ import annotations

import os
import pytest

from src.data_backbone.client import TABLE_MAP, UnityCatalogClient, get_unity_catalog_client


def test_table_map_completeness():
    """Verify TABLE_MAP contains all 27 conformed schemas and tables."""
    assert len(TABLE_MAP) == 27
    expected_prefixes = ("ea.metamodel.", "ea.bronze.", "ea.gold.")
    for local_tbl, uc_tbl in TABLE_MAP.items():
        assert uc_tbl.startswith(expected_prefixes), f"Table {uc_tbl} does not match expected prefix"
        assert "_" in local_tbl, f"Local table {local_tbl} should be snake_case"


def test_sql_translation_bidirectional():
    """Verify bidirectional SQL rewriting between local and Unity Catalog namespaces."""
    client = UnityCatalogClient(use_local_fallback=True)

    # Local to Cloud
    local_sql = "SELECT * FROM metamodel_nodes JOIN gold_time_matrix ON metamodel_nodes.urn = gold_time_matrix.urn WHERE 1=1"
    cloud_sql = client._to_cloud_sql(local_sql)
    assert "ea.metamodel.nodes" in cloud_sql
    assert "ea.gold.time_matrix" in cloud_sql
    assert "metamodel_nodes" not in cloud_sql
    assert "gold_time_matrix" not in cloud_sql

    # Cloud to Local
    roundtrip_local = client._to_local_sql(cloud_sql)
    assert "ea.metamodel.nodes" not in roundtrip_local
    assert "ea.gold.time_matrix" not in roundtrip_local
    assert "metamodel_nodes" in roundtrip_local
    assert "gold_time_matrix" in roundtrip_local


def test_offline_sqlite_fallback_execution():
    """Verify query execution when running in offline fallback mode."""
    # Force offline mode
    client = UnityCatalogClient(use_local_fallback=True)
    client.is_connected_to_cloud = False

    # Execute query using UC notation
    rows = client.execute_query("SELECT count(*) as cnt FROM ea.metamodel.nodes;")
    assert len(rows) == 1
    assert rows[0]["cnt"] > 0

    # Execute query using local notation
    rows_local = client.execute_query("SELECT count(*) as cnt FROM metamodel_nodes;")
    assert len(rows_local) == 1
    assert rows_local[0]["cnt"] == rows[0]["cnt"]


def test_get_methods_route_through_execute_query():
    """Verify all domain get_* methods route properly and return conformed records."""
    client = UnityCatalogClient(use_local_fallback=True)
    client.is_connected_to_cloud = False

    nodes = client.get_nodes()
    assert len(nodes) > 0
    assert "urn" in nodes[0]
    assert "kind" in nodes[0]

    edges = client.get_edges()
    assert len(edges) > 0
    assert "source_urn" in edges[0]

    time_matrix = client.get_time_matrix()
    assert len(time_matrix) >= 7

    drift = client.get_drift_reconciled()
    assert len(drift) > 0

    caps = client.get_capability_realizations()
    assert len(caps) > 0

    dr = client.get_resilience_dr()
    assert len(dr) > 0

    tech_debt = client.get_tech_debt_hotspots()
    assert len(tech_debt) > 0

    zt = client.get_security_zero_trust()
    assert len(zt) > 0

    sbom = client.get_supply_chain_sbom()
    assert len(sbom) > 0

    finops = client.get_finops_unit_economics()
    assert len(finops) > 0

    mdm = client.get_mdm_golden_records()
    assert len(mdm) > 0

    esg = client.get_esg_carbon_accounting()
    assert len(esg) > 0

    topologies = client.get_team_topologies()
    assert len(topologies) > 0

    lockin = client.get_vendor_lockin_exit()
    assert len(lockin) > 0


def test_live_databricks_sql_connection():
    """
    Test live Databricks SQL Warehouse connection when credentials are provided.
    Skipped if live connection cannot be established or in strict offline mode.
    """
    # Temporarily bypass offline env flag
    orig_offline = os.environ.get("DATABRICKS_OFFLINE")
    os.environ["DATABRICKS_OFFLINE"] = "0"
    try:
        client = UnityCatalogClient(use_local_fallback=True)
        if not client.is_connected_to_cloud:
            pytest.skip("Databricks SQL Warehouse not reachable from current environment")

        assert client.is_connected_to_cloud is True
        rows = client.execute_query("SELECT count(*) as cnt FROM ea.metamodel.nodes")
        assert len(rows) == 1
        assert rows[0]["cnt"] >= 30
    finally:
        if orig_offline is not None:
            os.environ["DATABRICKS_OFFLINE"] = orig_offline
        else:
            os.environ.pop("DATABRICKS_OFFLINE", None)
