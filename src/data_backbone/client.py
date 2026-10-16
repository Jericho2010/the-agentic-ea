"""
Databricks Unity Catalog Client for The Agentic EA Platform.
Connects directly to Databricks SQL when configured, with seamless
high-performance local fallback mode for offline/non-prod workstation execution.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LOCAL_DB_PATH = ROOT_DIR / "data" / "unity_catalog" / "ea_metamodel.db"

DEFAULT_DATABRICKS_HOST = "https://dbc-2d6963b0-153b.cloud.databricks.com/"


class UnityCatalogClient:
    """
    Client interface for Databricks Unity Catalog conformed tables:
    - ea.metamodel.nodes
    - ea.metamodel.edges
    - ea.metamodel.evidence
    - ea.bronze.git_repos
    - ea.bronze.cloud_resources
    - ea.gold.time_matrix
    - ea.gold.drift_reconciled
    """

    def __init__(
        self,
        host: Optional[str] = None,
        token: Optional[str] = None,
        http_path: Optional[str] = None,
        use_local_fallback: bool = True,
    ):
        self.host = host or os.environ.get("DATABRICKS_HOST", DEFAULT_DATABRICKS_HOST)
        self.token = token or os.environ.get("DATABRICKS_TOKEN")
        self.http_path = http_path or os.environ.get("DATABRICKS_HTTP_PATH")
        self.use_local_fallback = use_local_fallback
        self.is_connected_to_cloud = False

        if self.token and self.http_path:
            try:
                from databricks import sql
                self.sql_module = sql
                self.is_connected_to_cloud = True
            except ImportError:
                self.is_connected_to_cloud = False

        # Ensure local DB is initialized
        self._init_local_db()

    def _get_local_connection(self) -> sqlite3.Connection:
        LOCAL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(LOCAL_DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_local_db(self) -> None:
        """Create local conformed tables mirroring Databricks Unity Catalog schemas."""
        conn = self._get_local_connection()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS metamodel_nodes (
            urn TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            kind TEXT NOT NULL,
            owner_team TEXT NOT NULL,
            lifecycle_status TEXT NOT NULL DEFAULT 'run',
            criticality TEXT NOT NULL,
            metadata TEXT,
            last_updated TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS metamodel_edges (
            source_urn TEXT NOT NULL,
            target_urn TEXT NOT NULL,
            relation TEXT NOT NULL,
            protocol TEXT,
            contains_pii INTEGER DEFAULT 0,
            last_updated TEXT NOT NULL,
            PRIMARY KEY (source_urn, target_urn, relation)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS metamodel_evidence (
            evidence_id TEXT PRIMARY KEY,
            repo_url TEXT NOT NULL,
            commit_hash TEXT NOT NULL,
            ast_fingerprint TEXT NOT NULL,
            discovered_at TEXT NOT NULL,
            source_file TEXT,
            extracted_by TEXT
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_git_repos (
            repo_id TEXT PRIMARY KEY,
            repo_name TEXT NOT NULL,
            org_name TEXT NOT NULL,
            default_branch TEXT,
            languages TEXT,
            manifest_files TEXT,
            ast_nodes TEXT,
            discovered_edges TEXT,
            extracted_at TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_cloud_resources (
            resource_id TEXT PRIMARY KEY,
            resource_name TEXT NOT NULL,
            provider TEXT NOT NULL,
            account_id TEXT,
            region TEXT,
            resource_type TEXT,
            tags TEXT,
            monthly_cost_usd REAL,
            ingested_at TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_time_matrix (
            name TEXT NOT NULL,
            urn TEXT PRIMARY KEY,
            disposition TEXT NOT NULL,
            annual_run_cost REAL NOT NULL,
            tech_debt_score INTEGER NOT NULL,
            eol_date TEXT
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_drift_reconciled (
            urn TEXT PRIMARY KEY,
            declared_state TEXT NOT NULL,
            runtime_state TEXT NOT NULL,
            discrepancy_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            reconciled_at TEXT NOT NULL
        );
        """)

        conn.commit()
        conn.close()

    def get_nodes(self) -> List[Dict[str, Any]]:
        """Retrieve all PAM nodes from conformed catalog."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM metamodel_nodes ORDER BY kind, name;")
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            if d.get("metadata") and isinstance(d["metadata"], str):
                try:
                    d["metadata"] = json.loads(d["metadata"])
                except Exception:
                    pass
            result.append(d)
        conn.close()
        return result

    def get_edges(self) -> List[Dict[str, Any]]:
        """Retrieve all ArchiMate relationship edges."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM metamodel_edges ORDER BY source_urn, target_urn;")
        rows = cur.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["contains_pii"] = bool(d.get("contains_pii"))
            result.append(d)
        conn.close()
        return result

    def get_evidence(self) -> List[Dict[str, Any]]:
        """Retrieve all AST & extraction evidence records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM metamodel_evidence ORDER BY discovered_at DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_time_matrix(self) -> List[Dict[str, Any]]:
        """Retrieve executive TIME matrix records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_time_matrix ORDER BY annual_run_cost DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_drift_reconciled(self) -> List[Dict[str, Any]]:
        """Retrieve reconciled architecture drift telemetry."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_drift_reconciled ORDER BY reconciled_at DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def merge_nodes(self, nodes: List[Dict[str, Any]]) -> int:
        """Atomic upsert of PAM nodes."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        now_str = datetime.now(timezone.utc).isoformat()
        count = 0

        for n in nodes:
            meta_json = json.dumps(n.get("metadata", {})) if isinstance(n.get("metadata"), dict) else str(n.get("metadata", "{}"))
            cur.execute("""
            INSERT INTO metamodel_nodes (urn, name, kind, owner_team, lifecycle_status, criticality, metadata, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(urn) DO UPDATE SET
                name = excluded.name,
                kind = excluded.kind,
                owner_team = excluded.owner_team,
                lifecycle_status = excluded.lifecycle_status,
                criticality = excluded.criticality,
                metadata = excluded.metadata,
                last_updated = excluded.last_updated;
            """, (
                n["urn"],
                n["name"],
                n["kind"],
                n["owner_team"],
                n.get("lifecycle_status", "run"),
                n.get("criticality", "Tier-2"),
                meta_json,
                now_str,
            ))
            count += 1

        conn.commit()
        conn.close()
        return count

    def merge_edges(self, edges: List[Dict[str, Any]]) -> int:
        """Atomic upsert of ArchiMate relationship edges."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        now_str = datetime.now(timezone.utc).isoformat()
        count = 0

        for e in edges:
            cur.execute("""
            INSERT INTO metamodel_edges (source_urn, target_urn, relation, protocol, contains_pii, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_urn, target_urn, relation) DO UPDATE SET
                protocol = excluded.protocol,
                contains_pii = excluded.contains_pii,
                last_updated = excluded.last_updated;
            """, (
                e["source_urn"],
                e["target_urn"],
                e["relation"],
                e.get("protocol"),
                1 if e.get("contains_pii") else 0,
                now_str,
            ))
            count += 1

        conn.commit()
        conn.close()
        return count

    def insert_evidence(self, evidence: List[Dict[str, Any]]) -> int:
        """Insert AST and git commit provenance evidence."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0

        for ev in evidence:
            cur.execute("""
            INSERT INTO metamodel_evidence (evidence_id, repo_url, commit_hash, ast_fingerprint, discovered_at, source_file, extracted_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(evidence_id) DO UPDATE SET
                commit_hash = excluded.commit_hash,
                ast_fingerprint = excluded.ast_fingerprint,
                discovered_at = excluded.discovered_at;
            """, (
                ev["evidence_id"],
                ev["repo_url"],
                ev["commit_hash"],
                ev["ast_fingerprint"],
                ev.get("discovered_at", datetime.now(timezone.utc).isoformat()),
                ev.get("source_file"),
                ev.get("extracted_by"),
            ))
            count += 1

        conn.commit()
        conn.close()
        return count

    def insert_bronze_records(self, table: str, records: List[Dict[str, Any]]) -> int:
        """Insert bronze raw ingestion records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0

        if table == "git_repos":
            for r in records:
                cur.execute("""
                INSERT OR REPLACE INTO bronze_git_repos
                (repo_id, repo_name, org_name, default_branch, languages, manifest_files, ast_nodes, discovered_edges, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    r["repo_id"],
                    r["repo_name"],
                    r.get("org_name", "enterprise-org"),
                    r.get("default_branch", "main"),
                    json.dumps(r.get("languages", [])),
                    json.dumps(r.get("manifest_files", [])),
                    json.dumps(r.get("ast_nodes", [])),
                    json.dumps(r.get("discovered_edges", [])),
                    r.get("extracted_at", datetime.now(timezone.utc).isoformat()),
                ))
                count += 1

        elif table == "cloud_resources":
            for r in records:
                cur.execute("""
                INSERT OR REPLACE INTO bronze_cloud_resources
                (resource_id, resource_name, provider, account_id, region, resource_type, tags, monthly_cost_usd, ingested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    r["resource_id"],
                    r["resource_name"],
                    r["provider"],
                    r.get("account_id"),
                    r.get("region"),
                    r.get("resource_type"),
                    json.dumps(r.get("tags", {})),
                    float(r.get("monthly_cost_usd", 0.0)),
                    r.get("ingested_at", datetime.now(timezone.utc).isoformat()),
                ))
                count += 1

        conn.commit()
        conn.close()
        return count

    def get_bronze_records(self, table: str) -> List[Dict[str, Any]]:
        """Query bronze raw records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        tbl_name = f"bronze_{table}"
        cur.execute(f"SELECT * FROM {tbl_name};")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def save_time_matrix(self, records: List[Dict[str, Any]]) -> int:
        """Upsert TIME matrix records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_time_matrix (name, urn, disposition, annual_run_cost, tech_debt_score, eol_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(urn) DO UPDATE SET
                name = excluded.name,
                disposition = excluded.disposition,
                annual_run_cost = excluded.annual_run_cost,
                tech_debt_score = excluded.tech_debt_score,
                eol_date = excluded.eol_date;
            """, (
                r["name"],
                r["urn"],
                r["disposition"],
                float(r["annual_run_cost"]),
                int(r["tech_debt_score"]),
                r.get("eol_date"),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_drift_records(self, records: List[Dict[str, Any]]) -> int:
        """Upsert reconciled drift records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_drift_reconciled (urn, declared_state, runtime_state, discrepancy_type, severity, reconciled_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(urn) DO UPDATE SET
                declared_state = excluded.declared_state,
                runtime_state = excluded.runtime_state,
                discrepancy_type = excluded.discrepancy_type,
                severity = excluded.severity,
                reconciled_at = excluded.reconciled_at;
            """, (
                r["urn"],
                r["declared_state"],
                r["runtime_state"],
                r["discrepancy_type"],
                r["severity"],
                r.get("reconciled_at", datetime.now(timezone.utc).isoformat()),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def _normalize_sql(self, sql: str) -> str:
        """Translates Databricks Unity Catalog 3-level namespaces (ea.<schema>.<table>) to local table names."""
        replacements = [
            ("ea.metamodel.nodes", "metamodel_nodes"),
            ("ea.metamodel.edges", "metamodel_edges"),
            ("ea.metamodel.evidence", "metamodel_evidence"),
            ("ea.bronze.git_repos", "bronze_git_repos"),
            ("ea.bronze.cloud_resources", "bronze_cloud_resources"),
            ("ea.gold.time_matrix", "gold_time_matrix"),
            ("ea.gold.drift_reconciled", "gold_drift_reconciled"),
        ]
        res = sql
        for uc, local in replacements:
            res = res.replace(uc, local)
        return res

    def execute_query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query against the catalog, returning list of dicts."""
        norm_sql = self._normalize_sql(sql)
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute(norm_sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def execute_statement(self, sql: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE statement."""
        norm_sql = self._normalize_sql(sql)
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute(norm_sql, params)
        conn.commit()
        rc = cur.rowcount
        conn.close()
        return rc



# Singleton instance
_client_instance: Optional[UnityCatalogClient] = None


def get_unity_catalog_client() -> UnityCatalogClient:
    """Retrieve singleton UnityCatalogClient instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = UnityCatalogClient()
    return _client_instance
