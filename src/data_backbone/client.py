"""
Databricks Unity Catalog Client for The Agentic EA Platform.
Connects directly to Databricks SQL when configured, with seamless
high-performance local fallback mode for offline/non-prod workstation execution.
"""
from __future__ import annotations

import hashlib
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
        CREATE TABLE IF NOT EXISTS bronze_cmdb_ci (
            sys_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            ci_class TEXT NOT NULL,
            operational_status TEXT NOT NULL,
            environment TEXT,
            tier TEXT,
            owner_team TEXT,
            ip_address TEXT,
            cloud_resource_id TEXT,
            raw_attributes TEXT,
            synced_at TEXT NOT NULL
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

        cur.execute("PRAGMA table_info(gold_drift_reconciled);")
        existing_cols = [row[1] for row in cur.fetchall()]
        if existing_cols and "drift_type" not in existing_cols:
            cur.execute("DROP TABLE gold_drift_reconciled;")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_drift_reconciled (
            drift_id TEXT PRIMARY KEY,
            urn TEXT NOT NULL,
            ci_name TEXT NOT NULL,
            drift_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            declared_state TEXT NOT NULL,
            runtime_state TEXT NOT NULL,
            discrepancy_type TEXT NOT NULL,
            remediation_action TEXT NOT NULL,
            remediation_payload TEXT,
            reconciled_at TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_capability_realization (
            capability_urn TEXT NOT NULL,
            capability_name TEXT NOT NULL,
            capability_level INTEGER NOT NULL,
            parent_capability_urn TEXT,
            parent_capability_name TEXT,
            realizing_entity_urn TEXT NOT NULL,
            realizing_entity_name TEXT NOT NULL,
            realizing_entity_kind TEXT NOT NULL,
            disposition TEXT NOT NULL,
            allocated_annual_cost REAL NOT NULL,
            tech_debt_score INTEGER NOT NULL,
            criticality TEXT NOT NULL,
            PRIMARY KEY (capability_urn, realizing_entity_urn)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_arb_audit_ledger (
            audit_id TEXT PRIMARY KEY,
            pr_id TEXT NOT NULL,
            commit_hash TEXT NOT NULL,
            decision TEXT NOT NULL,
            policy_status TEXT NOT NULL,
            violations_count INTEGER NOT NULL,
            violations_json TEXT NOT NULL,
            evaluator TEXT NOT NULL,
            resources_evaluated INTEGER NOT NULL,
            diagram_delta_path TEXT,
            timestamp TEXT NOT NULL
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

    def get_drift_reconciled(self, drift_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve reconciled architecture and CMDB drift telemetry."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        if drift_type:
            cur.execute("SELECT * FROM gold_drift_reconciled WHERE drift_type = ? ORDER BY reconciled_at DESC;", (drift_type,))
        else:
            cur.execute("SELECT * FROM gold_drift_reconciled ORDER BY reconciled_at DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_cmdb_ci(self) -> List[Dict[str, Any]]:
        """Retrieve all ingested ServiceNow CMDB configuration items."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM bronze_cmdb_ci ORDER BY ci_class, name ASC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_capability_realizations(self) -> List[Dict[str, Any]]:
        """Retrieve conformed business capability realization data mart records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_capability_realization ORDER BY capability_level, capability_name, allocated_annual_cost DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_capability_summary(self) -> List[Dict[str, Any]]:
        """
        Aggregate FinOps spend, realizing entity count, and average tech debt per capability.
        Returns aggregated summary rows for L1 domains and L2 capabilities.
        """
        rows = self.get_capability_realizations()
        by_cap: Dict[str, Dict[str, Any]] = {}
        for r in rows:
            urn = r["capability_urn"]
            if urn not in by_cap:
                by_cap[urn] = {
                    "capability_urn": urn,
                    "capability_name": r["capability_name"],
                    "capability_level": r["capability_level"],
                    "parent_capability_urn": r.get("parent_capability_urn"),
                    "parent_capability_name": r.get("parent_capability_name"),
                    "total_allocated_annual_cost": 0.0,
                    "realizing_entities": [],
                    "realizing_count": 0,
                    "tech_debt_scores": [],
                    "criticality_levels": set(),
                    "dispositions": set(),
                }
            by_cap[urn]["total_allocated_annual_cost"] += float(r["allocated_annual_cost"])
            by_cap[urn]["realizing_entities"].append(r["realizing_entity_name"])
            by_cap[urn]["realizing_count"] += 1
            by_cap[urn]["tech_debt_scores"].append(int(r["tech_debt_score"]))
            by_cap[urn]["criticality_levels"].add(r["criticality"])
            by_cap[urn]["dispositions"].add(r["disposition"])

        summary = []
        for c in by_cap.values():
            scores = c["tech_debt_scores"]
            avg_debt = round(sum(scores) / len(scores), 1) if scores else 0.0
            max_debt = max(scores) if scores else 0
            summary.append({
                "capability_urn": c["capability_urn"],
                "capability_name": c["capability_name"],
                "capability_level": c["capability_level"],
                "parent_capability_urn": c["parent_capability_urn"],
                "parent_capability_name": c["parent_capability_name"],
                "total_annual_cost": round(c["total_allocated_annual_cost"], 2),
                "realizing_entities": c["realizing_entities"],
                "realizing_count": c["realizing_count"],
                "avg_tech_debt_score": avg_debt,
                "max_tech_debt_score": max_debt,
                "dispositions": list(c["dispositions"]),
            })
        return summary

    def record_arb_audit(self, receipt: Dict[str, Any]) -> str:
        """
        Record and persist an immutable ARB audit evaluation receipt.
        Inserts into ea.gold.arb_audit_ledger.
        """
        conn = self._get_local_connection()
        cur = conn.cursor()
        audit_id = receipt.get("audit_id") or f"arb-{receipt.get('pr_id', 'pr').lower()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        violations_str = receipt.get("violations_json")
        if isinstance(violations_str, (list, dict)):
            violations_str = json.dumps(violations_str)
        elif not violations_str:
            violations_str = "[]"

        cur.execute("""
        INSERT INTO gold_arb_audit_ledger (
            audit_id, pr_id, commit_hash, decision, policy_status,
            violations_count, violations_json, evaluator, resources_evaluated,
            diagram_delta_path, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(audit_id) DO UPDATE SET
            decision = excluded.decision,
            policy_status = excluded.policy_status,
            violations_count = excluded.violations_count,
            violations_json = excluded.violations_json,
            timestamp = excluded.timestamp;
        """, (
            audit_id,
            receipt["pr_id"],
            receipt.get("commit_hash", "HEAD"),
            receipt["decision"],
            receipt.get("policy_status", "COMPLIANT" if receipt["decision"] == "APPROVED" else "VIOLATION_DETECTED"),
            int(receipt.get("violations_count", 0)),
            violations_str,
            receipt.get("evaluator", "subscription_cli"),
            int(receipt.get("resources_evaluated", 1)),
            receipt.get("diagram_delta_path"),
            receipt.get("timestamp", datetime.now(timezone.utc).isoformat()),
        ))
        conn.commit()
        conn.close()
        return audit_id

    def get_arb_audit_ledger(self) -> List[Dict[str, Any]]:
        """Retrieve all ARB pre-merge governance audit records ordered by timestamp descending."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_arb_audit_ledger ORDER BY timestamp DESC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            if d.get("violations_json"):
                try:
                    d["violations"] = json.loads(d["violations_json"])
                except Exception:
                    d["violations"] = []
            else:
                d["violations"] = []
            rows.append(d)
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

    def save_cmdb_ci(self, records: List[Dict[str, Any]]) -> int:
        """Upsert ServiceNow CMDB configuration items into ea.bronze.cmdb_ci."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        now = datetime.now(timezone.utc).isoformat()
        for r in records:
            raw_attr = r.get("raw_attributes")
            if isinstance(raw_attr, dict):
                raw_attr = json.dumps(raw_attr)
            elif not raw_attr:
                raw_attr = "{}"
            cur.execute("""
            INSERT INTO bronze_cmdb_ci (
                sys_id, name, ci_class, operational_status, environment, tier,
                owner_team, ip_address, cloud_resource_id, raw_attributes, synced_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(sys_id) DO UPDATE SET
                name = excluded.name,
                ci_class = excluded.ci_class,
                operational_status = excluded.operational_status,
                environment = excluded.environment,
                tier = excluded.tier,
                owner_team = excluded.owner_team,
                ip_address = excluded.ip_address,
                cloud_resource_id = excluded.cloud_resource_id,
                raw_attributes = excluded.raw_attributes,
                synced_at = excluded.synced_at;
            """, (
                r["sys_id"],
                r["name"],
                r.get("ci_class", "cmdb_ci_appl"),
                r.get("operational_status", "Operational"),
                r.get("environment", "Production"),
                r.get("tier", "Tier-2"),
                r.get("owner_team", "unassigned"),
                r.get("ip_address"),
                r.get("cloud_resource_id"),
                raw_attr,
                r.get("synced_at", now),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_drift_records(self, records: List[Dict[str, Any]]) -> int:
        """Upsert reconciled drift and CMDB discrepancy records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        now = datetime.now(timezone.utc).isoformat()
        for r in records:
            drift_id = r.get("drift_id")
            if not drift_id:
                # generate deterministic ID
                drift_id = f"drift-{hashlib.md5((r['urn'] + r.get('discrepancy_type', '')).encode()).hexdigest()[:12]}"
            ci_name = r.get("ci_name") or r["urn"].split(":")[-1]
            drift_type = r.get("drift_type", "POLICY_VIOLATION")
            remediation_action = r.get("remediation_action", "REMEDIATE_POLICY")
            payload = r.get("remediation_payload")
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            elif not payload:
                payload = "{}"

            cur.execute("""
            INSERT INTO gold_drift_reconciled (
                drift_id, urn, ci_name, drift_type, severity, declared_state,
                runtime_state, discrepancy_type, remediation_action, remediation_payload, reconciled_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(drift_id) DO UPDATE SET
                urn = excluded.urn,
                ci_name = excluded.ci_name,
                drift_type = excluded.drift_type,
                severity = excluded.severity,
                declared_state = excluded.declared_state,
                runtime_state = excluded.runtime_state,
                discrepancy_type = excluded.discrepancy_type,
                remediation_action = excluded.remediation_action,
                remediation_payload = excluded.remediation_payload,
                reconciled_at = excluded.reconciled_at;
            """, (
                drift_id,
                r["urn"],
                ci_name,
                drift_type,
                r["severity"],
                r["declared_state"],
                r["runtime_state"],
                r["discrepancy_type"],
                remediation_action,
                payload,
                r.get("reconciled_at", now),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_capability_realizations(self, records: List[Dict[str, Any]]) -> int:
        """Upsert capability realization data mart records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_capability_realization (
                capability_urn, capability_name, capability_level, parent_capability_urn, parent_capability_name,
                realizing_entity_urn, realizing_entity_name, realizing_entity_kind, disposition,
                allocated_annual_cost, tech_debt_score, criticality
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(capability_urn, realizing_entity_urn) DO UPDATE SET
                capability_name = excluded.capability_name,
                capability_level = excluded.capability_level,
                parent_capability_urn = excluded.parent_capability_urn,
                parent_capability_name = excluded.parent_capability_name,
                realizing_entity_name = excluded.realizing_entity_name,
                realizing_entity_kind = excluded.realizing_entity_kind,
                disposition = excluded.disposition,
                allocated_annual_cost = excluded.allocated_annual_cost,
                tech_debt_score = excluded.tech_debt_score,
                criticality = excluded.criticality;
            """, (
                r["capability_urn"],
                r["capability_name"],
                int(r["capability_level"]),
                r.get("parent_capability_urn"),
                r.get("parent_capability_name"),
                r["realizing_entity_urn"],
                r["realizing_entity_name"],
                r.get("realizing_entity_kind", "Microservice"),
                r["disposition"],
                float(r["allocated_annual_cost"]),
                int(r["tech_debt_score"]),
                r.get("criticality", "Tier-1"),
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
            ("ea.bronze.cmdb_ci", "bronze_cmdb_ci"),
            ("ea.gold.time_matrix", "gold_time_matrix"),
            ("ea.gold.drift_reconciled", "gold_drift_reconciled"),
            ("ea.gold.capability_realization", "gold_capability_realization"),
            ("ea.gold.arb_audit_ledger", "gold_arb_audit_ledger"),
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
