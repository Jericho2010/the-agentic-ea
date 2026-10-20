"""
Databricks Unity Catalog Live Seeding Script.
Connects directly to the live Databricks SQL Warehouse (df4dc09688caf6d8),
executes DDLs to ensure all conformed schemas and Delta tables exist in catalog 'ea',
and seeds conformed PAM metamodel entities, bronze ingestion logs, and gold scenario marts.
"""
from __future__ import annotations

import configparser
import logging
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from databricks import sql

from src.data_backbone.catalog import DDL_STATEMENTS
from src.data_backbone.client import LOCAL_DB_PATH, UnityCatalogClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_databricks_uc")

DEFAULT_DATABRICKS_HOST = "https://dbc-2d6963b0-153b.cloud.databricks.com/"
DEFAULT_WAREHOUSE_ID = "df4dc09688caf6d8"
DEFAULT_HTTP_PATH = f"/sql/1.0/warehouses/{DEFAULT_WAREHOUSE_ID}"

TABLE_MAP: Dict[str, str] = {
    "metamodel_nodes": "ea.metamodel.nodes",
    "metamodel_edges": "ea.metamodel.edges",
    "metamodel_evidence": "ea.metamodel.evidence",
    "bronze_git_repos": "ea.bronze.git_repos",
    "bronze_cloud_resources": "ea.bronze.cloud_resources",
    "bronze_cmdb_ci": "ea.bronze.cmdb_ci",
    "bronze_api_gateway_logs": "ea.bronze.api_gateway_logs",
    "bronze_process_event_logs": "ea.bronze.process_event_logs",
    "bronze_ai_models": "ea.bronze.ai_models",
    "gold_time_matrix": "ea.gold.time_matrix",
    "gold_drift_reconciled": "ea.gold.drift_reconciled",
    "gold_capability_realization": "ea.gold.capability_realization",
    "gold_arb_audit_ledger": "ea.gold.arb_audit_ledger",
    "gold_ma_synergies": "ea.gold.ma_synergies",
    "gold_compliance_lineage": "ea.gold.compliance_lineage",
    "gold_interface_rationalization": "ea.gold.interface_rationalization",
    "gold_process_optimization": "ea.gold.process_optimization",
    "gold_ai_governance": "ea.gold.ai_governance",
    "gold_resilience_dr": "ea.gold.resilience_dr",
    "gold_tech_debt_hotspots": "ea.gold.tech_debt_hotspots",
    "gold_security_zero_trust": "ea.gold.security_zero_trust",
    "gold_supply_chain_sbom": "ea.gold.supply_chain_sbom",
    "gold_finops_unit_economics": "ea.gold.finops_unit_economics",
    "gold_mdm_golden_records": "ea.gold.mdm_golden_records",
    "gold_esg_carbon_accounting": "ea.gold.esg_carbon_accounting",
    "gold_team_topologies": "ea.gold.team_topologies",
    "gold_vendor_lockin_exit": "ea.gold.vendor_lockin_exit",
}


def resolve_databricks_credentials() -> Tuple[str, str, str]:
    """
    Resolves Databricks host, token, and warehouse HTTP path:
    1. Environment variables (DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_HTTP_PATH)
    2. ~/.databrickscfg standard configuration file
    """
    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH") or DEFAULT_HTTP_PATH

    cfg_path = Path.home() / ".databrickscfg"
    if (not host or not token) and cfg_path.exists():
        cfg = configparser.ConfigParser()
        cfg.read(cfg_path)
        profile = os.environ.get("DATABRICKS_CONFIG_PROFILE", "DEFAULT")
        if profile in cfg:
            host = host or cfg[profile].get("host")
            token = token or cfg[profile].get("token")
        elif "DEFAULT" in cfg:
            host = host or cfg["DEFAULT"].get("host")
            token = token or cfg["DEFAULT"].get("token")

    host = (host or DEFAULT_DATABRICKS_HOST).rstrip("/")
    if host.startswith("https://"):
        hostname = host.replace("https://", "").rstrip("/")
    elif host.startswith("http://"):
        hostname = host.replace("http://", "").rstrip("/")
    else:
        hostname = host

    if not token:
        raise ValueError("Databricks access token could not be resolved from env or ~/.databrickscfg.")

    return hostname, token, http_path


def to_sql_literal(val: Any) -> str:
    """Safely converts Python/SQLite values to SQL literals."""
    if val is None:
        return "NULL"
    elif isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, (int, float)):
        return str(val)
    else:
        s = str(val).replace("'", "''")
        return f"'{s}'"


def seed_unity_catalog(clean: bool = True) -> Dict[str, int]:
    """
    Executes DDL statements and transfers all conformed data from local SQLite
    into live Databricks Unity Catalog Delta tables using high-throughput multi-row INSERTs.
    """
    hostname, token, http_path = resolve_databricks_credentials()
    logger.info(f"Connecting to Databricks SQL Warehouse at {hostname} ({http_path})...")

    # Ensure local database is populated with conformed data
    _ = UnityCatalogClient()
    if not LOCAL_DB_PATH.exists():
        raise FileNotFoundError(f"Local SQLite database not found at {LOCAL_DB_PATH}")

    conn_local = sqlite3.connect(LOCAL_DB_PATH)
    conn_local.row_factory = sqlite3.Row
    cur_local = conn_local.cursor()

    results: Dict[str, int] = {}

    with sql.connect(
        server_hostname=hostname,
        http_path=http_path,
        access_token=token,
    ) as conn:
        with conn.cursor() as cursor:
            # 1. Execute DDL statements
            logger.info("Ensuring schemas and tables exist in catalog 'ea'...")
            for s in DDL_STATEMENTS["schemas"]:
                cursor.execute(s)

            for key, ddl in DDL_STATEMENTS.items():
                if key != "schemas":
                    cursor.execute(ddl)

            # Also create compatibility view for capability realizations
            cursor.execute(
                "CREATE VIEW IF NOT EXISTS ea.gold.capability_realizations AS SELECT * FROM ea.gold.capability_realization"
            )

            # 2. Transfer data table by table
            logger.info("Transferring data into live Databricks Unity Catalog tables...")
            for l_tbl, r_tbl in TABLE_MAP.items():
                cur_local.execute(f"SELECT * FROM {l_tbl}")
                local_rows = [dict(r) for r in cur_local.fetchall()]
                if not local_rows:
                    logger.warning(f"No local rows found in {l_tbl}. Skipping.")
                    results[r_tbl] = 0
                    continue

                # Discover remote table columns to ensure strict alignment
                cursor.execute(f"DESCRIBE {r_tbl}")
                r_cols = [
                    row[0]
                    for row in cursor.fetchall()
                    if row[0] and not row[0].startswith("#")
                ]

                # Match columns
                cols = [c for c in r_cols if c in local_rows[0]]
                if not cols:
                    logger.error(f"No matching columns between {l_tbl} and {r_tbl}!")
                    continue

                if clean:
                    cursor.execute(f"TRUNCATE TABLE {r_tbl}")

                col_names = ", ".join(cols)

                # Batch multi-row statements in chunks of 100 rows
                chunk_size = 100
                for i in range(0, len(local_rows), chunk_size):
                    chunk = local_rows[i : i + chunk_size]
                    val_rows = []
                    for r in chunk:
                        val_strs = [to_sql_literal(r.get(c)) for c in cols]
                        val_rows.append(f"({', '.join(val_strs)})")

                    insert_sql = (
                        f"INSERT INTO {r_tbl} ({col_names}) VALUES\n"
                        + ",\n".join(val_rows)
                    )
                    cursor.execute(insert_sql)

                # Verify remote count
                cursor.execute(f"SELECT count(*) FROM {r_tbl}")
                cnt = cursor.fetchone()[0]
                results[r_tbl] = cnt
                logger.info(f"✓ Seeded {r_tbl:35} -> {cnt} rows")

    conn_local.close()

    # Verification assertions
    metamodel_tables = [t for t in results if t.startswith("ea.metamodel.")]
    gold_tables = [t for t in results if t.startswith("ea.gold.")]

    assert all(results[t] > 0 for t in metamodel_tables), f"Some metamodel tables have 0 rows: {results}"
    assert all(results[t] > 0 for t in gold_tables), f"Some gold tables have 0 rows: {results}"

    logger.info("=================================================================")
    logger.info("   UNITY CATALOG SEEDING COMPLETE: ALL TABLES VERIFIED IN LIVE UC")
    logger.info("=================================================================")
    return results


if __name__ == "__main__":
    try:
        res = seed_unity_catalog(clean=True)
        print("\nUnity Catalog Live Seed Summary:")
        for tbl, count in sorted(res.items()):
            print(f"  • {tbl}: {count} records")
        print("\nAll Unity Catalog metamodel and gold tables successfully populated!")
    except Exception as e:
        logger.error(f"Failed to seed Databricks Unity Catalog: {e}")
        sys.exit(1)
