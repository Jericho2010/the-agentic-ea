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
            transit_encryption TEXT DEFAULT 'tls_1_3',
            transferred_classification TEXT DEFAULT 'Internal',
            last_updated TEXT NOT NULL,
            PRIMARY KEY (source_urn, target_urn, relation)
        );
        """)

        try:
            cur.execute("ALTER TABLE metamodel_edges ADD COLUMN transit_encryption TEXT DEFAULT 'tls_1_3';")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE metamodel_edges ADD COLUMN transferred_classification TEXT DEFAULT 'Internal';")
        except Exception:
            pass

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

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_ma_synergies (
            synergy_id TEXT PRIMARY KEY,
            target_entity_name TEXT NOT NULL,
            target_entity_urn TEXT NOT NULL,
            capability_name TEXT NOT NULL,
            capability_urn TEXT NOT NULL,
            core_counterpart_name TEXT,
            core_counterpart_urn TEXT,
            overlap_type TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            current_annual_cost REAL NOT NULL,
            potential_synergy_savings REAL NOT NULL,
            risk_level TEXT NOT NULL,
            discovered_at TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_compliance_lineage (
            flow_id TEXT PRIMARY KEY,
            source_urn TEXT NOT NULL,
            target_urn TEXT NOT NULL,
            data_classification TEXT NOT NULL,
            jurisdiction_source TEXT NOT NULL,
            jurisdiction_target TEXT NOT NULL,
            is_cross_border INTEGER NOT NULL DEFAULT 0,
            transit_encryption TEXT NOT NULL,
            rest_encryption TEXT NOT NULL,
            gdpr_status TEXT NOT NULL,
            dora_status TEXT NOT NULL,
            risk_level TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_api_gateway_logs (
            log_id TEXT PRIMARY KEY,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            protocol TEXT NOT NULL,
            auth_mechanism TEXT NOT NULL,
            consumer_service TEXT NOT NULL,
            provider_service TEXT NOT NULL,
            requests_last_30d INTEGER NOT NULL,
            avg_latency_ms REAL NOT NULL,
            error_rate REAL NOT NULL,
            last_seen_timestamp TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_interface_rationalization (
            interface_id TEXT PRIMARY KEY,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            protocol TEXT NOT NULL,
            provider_service TEXT NOT NULL,
            consumer_service TEXT NOT NULL,
            is_declared INTEGER NOT NULL DEFAULT 0,
            is_active_runtime INTEGER NOT NULL DEFAULT 0,
            discrepancy_type TEXT NOT NULL,
            rationalization_action TEXT NOT NULL,
            last_active_timestamp TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_process_event_logs (
            trace_id TEXT NOT NULL,
            process_id TEXT NOT NULL,
            step_id TEXT NOT NULL,
            step_name TEXT NOT NULL,
            service_urn TEXT NOT NULL,
            duration_ms REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_process_optimization (
            process_id TEXT NOT NULL,
            process_name TEXT NOT NULL,
            step_id TEXT NOT NULL,
            step_name TEXT NOT NULL,
            service_urn TEXT NOT NULL,
            p50_latency_ms REAL NOT NULL,
            p95_latency_ms REAL NOT NULL,
            p99_latency_ms REAL NOT NULL,
            sla_target_ms REAL NOT NULL,
            error_rate_pct REAL NOT NULL,
            is_bottleneck INTEGER NOT NULL DEFAULT 0,
            optimization_action TEXT NOT NULL,
            PRIMARY KEY (process_id, step_id)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze_ai_models (
            model_id TEXT PRIMARY KEY,
            model_name TEXT NOT NULL,
            version TEXT NOT NULL,
            framework TEXT NOT NULL,
            task_type TEXT NOT NULL,
            training_dataset_urn TEXT NOT NULL,
            serving_endpoint_urn TEXT NOT NULL,
            owner_team TEXT NOT NULL,
            license TEXT NOT NULL,
            has_human_in_the_loop INTEGER NOT NULL DEFAULT 0,
            timestamp TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_ai_governance (
            model_id TEXT PRIMARY KEY,
            model_name TEXT NOT NULL,
            version TEXT NOT NULL,
            task_type TEXT NOT NULL,
            eu_risk_tier TEXT NOT NULL,
            compliance_status TEXT NOT NULL,
            has_model_card INTEGER NOT NULL DEFAULT 0,
            has_data_lineage INTEGER NOT NULL DEFAULT 0,
            has_human_oversight INTEGER NOT NULL DEFAULT 0,
            governance_action TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_resilience_dr (
            component_urn TEXT PRIMARY KEY,
            dr_tier TEXT NOT NULL,
            rto_actual_min INTEGER NOT NULL,
            rto_target_min INTEGER NOT NULL,
            rpo_actual_min INTEGER NOT NULL,
            rpo_target_min INTEGER NOT NULL,
            replication_strategy TEXT NOT NULL,
            failover_automation TEXT NOT NULL,
            sla_breached INTEGER NOT NULL DEFAULT 0
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_tech_debt_hotspots (
            component_urn TEXT PRIMARY KEY,
            debt_score INTEGER NOT NULL,
            git_churn_lines_30d INTEGER NOT NULL,
            cyclomatic_complexity REAL NOT NULL,
            architectural_smells TEXT NOT NULL,
            refactoring_roi_rank INTEGER NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_security_zero_trust (
            id TEXT PRIMARY KEY,
            source_urn TEXT NOT NULL,
            target_urn TEXT NOT NULL,
            protocol TEXT NOT NULL,
            mtls_enforced INTEGER NOT NULL DEFAULT 0,
            trust_zone_source TEXT NOT NULL,
            trust_zone_target TEXT NOT NULL,
            microsegmentation_status TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_supply_chain_sbom (
            id TEXT PRIMARY KEY,
            package_name TEXT NOT NULL,
            version TEXT NOT NULL,
            component_urn TEXT NOT NULL,
            license TEXT NOT NULL,
            license_compliance TEXT NOT NULL,
            cve_count INTEGER NOT NULL,
            max_severity TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_finops_unit_economics (
            service_urn TEXT PRIMARY KEY,
            monthly_spend REAL NOT NULL,
            cost_per_transaction REAL NOT NULL,
            tag_compliance_pct REAL NOT NULL,
            idle_waste_cost REAL NOT NULL,
            optimization_action TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_mdm_golden_records (
            entity_name TEXT PRIMARY KEY,
            golden_record_urn TEXT NOT NULL,
            authoritative_source TEXT NOT NULL,
            competing_sources TEXT NOT NULL,
            divergence_detected INTEGER NOT NULL DEFAULT 0,
            data_contract_status TEXT NOT NULL,
            scd2_active INTEGER NOT NULL DEFAULT 1
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_esg_carbon_accounting (
            service_urn TEXT PRIMARY KEY,
            region TEXT NOT NULL,
            monthly_kwh REAL NOT NULL,
            grid_carbon_intensity_gco2_kwh REAL NOT NULL,
            monthly_emissions_kgco2 REAL NOT NULL,
            green_tier TEXT NOT NULL,
            reduction_recommendation TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_team_topologies (
            team_name TEXT PRIMARY KEY,
            team_type TEXT NOT NULL,
            owned_components TEXT NOT NULL,
            codeowners_match INTEGER NOT NULL DEFAULT 1,
            commit_co_change_friction REAL NOT NULL,
            conways_law_alignment TEXT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_vendor_lockin_exit (
            component_urn TEXT PRIMARY KEY,
            cloud_provider TEXT NOT NULL,
            proprietary_services_used TEXT NOT NULL,
            lockin_risk_score INTEGER NOT NULL,
            open_alternative TEXT NOT NULL,
            exit_effort_weeks INTEGER NOT NULL,
            exit_strategy_action TEXT NOT NULL
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
            d["transit_encryption"] = d.get("transit_encryption") or "tls_1_3"
            d["transferred_classification"] = d.get("transferred_classification") or ("PII:High" if d["contains_pii"] else "Internal")
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

    def get_ma_synergies(self) -> List[Dict[str, Any]]:
        """Retrieve all M&A capability overlap and synergy rationalization records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_ma_synergies ORDER BY potential_synergy_savings DESC, current_annual_cost DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_compliance_lineage(self) -> List[Dict[str, Any]]:
        """Retrieve all regulatory compliance and privacy dataflow lineage records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_compliance_lineage ORDER BY CASE risk_level WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END, flow_id ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["is_cross_border"] = bool(d.get("is_cross_border"))
            rows.append(d)
        conn.close()
        return rows

    def get_api_gateway_logs(self) -> List[Dict[str, Any]]:
        """Retrieve all ingested runtime API gateway access logs."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM bronze_api_gateway_logs ORDER BY requests_last_30d DESC, endpoint ASC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_interface_rationalization(self) -> List[Dict[str, Any]]:
        """Retrieve all conformed interface rationalization records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_interface_rationalization ORDER BY CASE discrepancy_type WHEN 'ZOMBIE_SHADOW' THEN 1 WHEN 'DEAD_ORPHAN' THEN 2 WHEN 'PROTOCOL_SPRAWL' THEN 3 ELSE 4 END, interface_id ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["is_declared"] = bool(d.get("is_declared"))
            d["is_active_runtime"] = bool(d.get("is_active_runtime"))
            rows.append(d)
        conn.close()
        return rows

    def get_process_event_logs(self, process_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all ingested process execution event logs."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        if process_id:
            cur.execute("SELECT * FROM bronze_process_event_logs WHERE process_id = ? ORDER BY timestamp ASC, step_id ASC;", (process_id,))
        else:
            cur.execute("SELECT * FROM bronze_process_event_logs ORDER BY timestamp ASC, step_id ASC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_process_optimization(self, process_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve conformed process optimization & SLA metrics."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        if process_id:
            cur.execute("SELECT * FROM gold_process_optimization WHERE process_id = ? ORDER BY step_id ASC;", (process_id,))
        else:
            cur.execute("SELECT * FROM gold_process_optimization ORDER BY process_id ASC, step_id ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["is_bottleneck"] = bool(d.get("is_bottleneck"))
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
            cur.execute("SELECT metadata FROM metamodel_nodes WHERE urn = ?;", (n["urn"],))
            existing_row = cur.fetchone()
            incoming_meta = n.get("metadata") or {}
            if isinstance(incoming_meta, str):
                try:
                    incoming_meta = json.loads(incoming_meta)
                except Exception:
                    incoming_meta = {}
            if existing_row and existing_row["metadata"]:
                try:
                    existing_meta = json.loads(existing_row["metadata"]) if isinstance(existing_row["metadata"], str) else existing_row["metadata"]
                    merged_meta = {**existing_meta, **incoming_meta}
                except Exception:
                    merged_meta = incoming_meta
            else:
                merged_meta = incoming_meta
            meta_json = json.dumps(merged_meta)

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
            transit_enc = e.get("transit_encryption") or ("plaintext" if "CQL" in str(e.get("protocol")) or "3306" in str(e.get("protocol")) else "tls_1_3")
            trans_class = e.get("transferred_classification") or ("PII:High" if e.get("contains_pii") else "Internal")
            cur.execute("""
            INSERT INTO metamodel_edges (source_urn, target_urn, relation, protocol, contains_pii, transit_encryption, transferred_classification, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_urn, target_urn, relation) DO UPDATE SET
                protocol = excluded.protocol,
                contains_pii = excluded.contains_pii,
                transit_encryption = excluded.transit_encryption,
                transferred_classification = excluded.transferred_classification,
                last_updated = excluded.last_updated;
            """, (
                e["source_urn"],
                e["target_urn"],
                e["relation"],
                e.get("protocol"),
                1 if e.get("contains_pii") else 0,
                transit_enc,
                trans_class,
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

    def save_ma_synergies(self, records: List[Dict[str, Any]]) -> int:
        """Upsert M&A synergy and overlap records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        now = datetime.now(timezone.utc).isoformat()
        for r in records:
            cur.execute("""
            INSERT INTO gold_ma_synergies (
                synergy_id, target_entity_name, target_entity_urn, capability_name, capability_urn,
                core_counterpart_name, core_counterpart_urn, overlap_type, recommendation,
                current_annual_cost, potential_synergy_savings, risk_level, discovered_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(synergy_id) DO UPDATE SET
                target_entity_name = excluded.target_entity_name,
                target_entity_urn = excluded.target_entity_urn,
                capability_name = excluded.capability_name,
                capability_urn = excluded.capability_urn,
                core_counterpart_name = excluded.core_counterpart_name,
                core_counterpart_urn = excluded.core_counterpart_urn,
                overlap_type = excluded.overlap_type,
                recommendation = excluded.recommendation,
                current_annual_cost = excluded.current_annual_cost,
                potential_synergy_savings = excluded.potential_synergy_savings,
                risk_level = excluded.risk_level,
                discovered_at = excluded.discovered_at;
            """, (
                r["synergy_id"],
                r["target_entity_name"],
                r["target_entity_urn"],
                r["capability_name"],
                r["capability_urn"],
                r.get("core_counterpart_name"),
                r.get("core_counterpart_urn"),
                r["overlap_type"],
                r["recommendation"],
                float(r["current_annual_cost"]),
                float(r["potential_synergy_savings"]),
                r.get("risk_level", "Medium"),
                r.get("discovered_at", now),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_compliance_lineage(self, records: List[Dict[str, Any]]) -> int:
        """Upsert compliance lineage records into ea.gold.compliance_lineage."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_compliance_lineage (
                flow_id, source_urn, target_urn, data_classification,
                jurisdiction_source, jurisdiction_target, is_cross_border,
                transit_encryption, rest_encryption, gdpr_status, dora_status, risk_level
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(flow_id) DO UPDATE SET
                source_urn = excluded.source_urn,
                target_urn = excluded.target_urn,
                data_classification = excluded.data_classification,
                jurisdiction_source = excluded.jurisdiction_source,
                jurisdiction_target = excluded.jurisdiction_target,
                is_cross_border = excluded.is_cross_border,
                transit_encryption = excluded.transit_encryption,
                rest_encryption = excluded.rest_encryption,
                gdpr_status = excluded.gdpr_status,
                dora_status = excluded.dora_status,
                risk_level = excluded.risk_level;
            """, (
                r["flow_id"],
                r["source_urn"],
                r["target_urn"],
                r["data_classification"],
                r["jurisdiction_source"],
                r["jurisdiction_target"],
                1 if r.get("is_cross_border") else 0,
                r["transit_encryption"],
                r["rest_encryption"],
                r["gdpr_status"],
                r["dora_status"],
                r["risk_level"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_api_gateway_logs(self, records: List[Dict[str, Any]]) -> int:
        """Upsert API gateway access logs into ea.bronze.api_gateway_logs."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO bronze_api_gateway_logs (
                log_id, endpoint, method, protocol, auth_mechanism,
                consumer_service, provider_service, requests_last_30d,
                avg_latency_ms, error_rate, last_seen_timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(log_id) DO UPDATE SET
                endpoint = excluded.endpoint,
                method = excluded.method,
                protocol = excluded.protocol,
                auth_mechanism = excluded.auth_mechanism,
                consumer_service = excluded.consumer_service,
                provider_service = excluded.provider_service,
                requests_last_30d = excluded.requests_last_30d,
                avg_latency_ms = excluded.avg_latency_ms,
                error_rate = excluded.error_rate,
                last_seen_timestamp = excluded.last_seen_timestamp;
            """, (
                r["log_id"],
                r["endpoint"],
                r["method"],
                r["protocol"],
                r.get("auth_mechanism", "None"),
                r["consumer_service"],
                r["provider_service"],
                int(r.get("requests_last_30d", 0)),
                float(r.get("avg_latency_ms", 0.0)),
                float(r.get("error_rate", 0.0)),
                r.get("last_seen_timestamp", datetime.now(timezone.utc).isoformat()),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_interface_rationalization(self, records: List[Dict[str, Any]]) -> int:
        """Upsert interface rationalization records into ea.gold.interface_rationalization."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_interface_rationalization (
                interface_id, endpoint, method, protocol,
                provider_service, consumer_service, is_declared,
                is_active_runtime, discrepancy_type, rationalization_action,
                last_active_timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(interface_id) DO UPDATE SET
                endpoint = excluded.endpoint,
                method = excluded.method,
                protocol = excluded.protocol,
                provider_service = excluded.provider_service,
                consumer_service = excluded.consumer_service,
                is_declared = excluded.is_declared,
                is_active_runtime = excluded.is_active_runtime,
                discrepancy_type = excluded.discrepancy_type,
                rationalization_action = excluded.rationalization_action,
                last_active_timestamp = excluded.last_active_timestamp;
            """, (
                r["interface_id"],
                r["endpoint"],
                r["method"],
                r["protocol"],
                r["provider_service"],
                r["consumer_service"],
                1 if r.get("is_declared") else 0,
                1 if r.get("is_active_runtime") else 0,
                r.get("discrepancy_type", "COMPLIANT"),
                r.get("rationalization_action", "RETAIN"),
                r.get("last_active_timestamp", datetime.now(timezone.utc).isoformat()),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_process_event_logs(self, records: List[Dict[str, Any]]) -> int:
        """Insert execution trace spans into ea.bronze.process_event_logs."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO bronze_process_event_logs (
                trace_id, process_id, step_id, step_name, service_urn,
                duration_ms, status, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                r["trace_id"],
                r["process_id"],
                r["step_id"],
                r["step_name"],
                r["service_urn"],
                float(r["duration_ms"]),
                r.get("status", "SUCCESS"),
                r.get("timestamp", datetime.now(timezone.utc).isoformat()),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def save_process_optimization(self, records: List[Dict[str, Any]]) -> int:
        """Upsert process optimization records into ea.gold.process_optimization."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_process_optimization (
                process_id, process_name, step_id, step_name, service_urn,
                p50_latency_ms, p95_latency_ms, p99_latency_ms, sla_target_ms,
                error_rate_pct, is_bottleneck, optimization_action
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(process_id, step_id) DO UPDATE SET
                process_name = excluded.process_name,
                step_name = excluded.step_name,
                service_urn = excluded.service_urn,
                p50_latency_ms = excluded.p50_latency_ms,
                p95_latency_ms = excluded.p95_latency_ms,
                p99_latency_ms = excluded.p99_latency_ms,
                sla_target_ms = excluded.sla_target_ms,
                error_rate_pct = excluded.error_rate_pct,
                is_bottleneck = excluded.is_bottleneck,
                optimization_action = excluded.optimization_action;
            """, (
                r["process_id"],
                r["process_name"],
                r["step_id"],
                r["step_name"],
                r["service_urn"],
                float(r["p50_latency_ms"]),
                float(r["p95_latency_ms"]),
                float(r["p99_latency_ms"]),
                float(r["sla_target_ms"]),
                float(r["error_rate_pct"]),
                1 if r.get("is_bottleneck") else 0,
                r.get("optimization_action", "RETAIN_CURRENT_SLA"),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def get_ai_models(self) -> List[Dict[str, Any]]:
        """Retrieve all ingested AI/ML models from ea.bronze.ai_models."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM bronze_ai_models ORDER BY model_id ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["has_human_in_the_loop"] = bool(d.get("has_human_in_the_loop"))
            rows.append(d)
        conn.close()
        return rows

    def save_ai_models(self, records: List[Dict[str, Any]]) -> int:
        """Upsert AI/ML model records into ea.bronze.ai_models."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO bronze_ai_models (
                model_id, model_name, version, framework, task_type,
                training_dataset_urn, serving_endpoint_urn, owner_team,
                license, has_human_in_the_loop, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(model_id) DO UPDATE SET
                model_name = excluded.model_name,
                version = excluded.version,
                framework = excluded.framework,
                task_type = excluded.task_type,
                training_dataset_urn = excluded.training_dataset_urn,
                serving_endpoint_urn = excluded.serving_endpoint_urn,
                owner_team = excluded.owner_team,
                license = excluded.license,
                has_human_in_the_loop = excluded.has_human_in_the_loop,
                timestamp = excluded.timestamp;
            """, (
                r["model_id"],
                r["model_name"],
                r["version"],
                r["framework"],
                r["task_type"],
                r["training_dataset_urn"],
                r["serving_endpoint_urn"],
                r["owner_team"],
                r["license"],
                1 if r.get("has_human_in_the_loop") else 0,
                r.get("timestamp", datetime.now(timezone.utc).isoformat()),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    def get_ai_governance(self) -> List[Dict[str, Any]]:
        """Retrieve conformed AI governance records from ea.gold.ai_governance."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_ai_governance ORDER BY model_id ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["has_model_card"] = bool(d.get("has_model_card"))
            d["has_data_lineage"] = bool(d.get("has_data_lineage"))
            d["has_human_oversight"] = bool(d.get("has_human_oversight"))
            rows.append(d)
        conn.close()
        return rows

    def save_ai_governance(self, records: List[Dict[str, Any]]) -> int:
        """Upsert AI governance records into ea.gold.ai_governance."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_ai_governance (
                model_id, model_name, version, task_type, eu_risk_tier,
                compliance_status, has_model_card, has_data_lineage,
                has_human_oversight, governance_action
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(model_id) DO UPDATE SET
                model_name = excluded.model_name,
                version = excluded.version,
                task_type = excluded.task_type,
                eu_risk_tier = excluded.eu_risk_tier,
                compliance_status = excluded.compliance_status,
                has_model_card = excluded.has_model_card,
                has_data_lineage = excluded.has_data_lineage,
                has_human_oversight = excluded.has_human_oversight,
                governance_action = excluded.governance_action;
            """, (
                r["model_id"],
                r["model_name"],
                r["version"],
                r["task_type"],
                r["eu_risk_tier"],
                r["compliance_status"],
                1 if r.get("has_model_card") else 0,
                1 if r.get("has_data_lineage") else 0,
                1 if r.get("has_human_oversight") else 0,
                r["governance_action"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S12: DISASTER RECOVERY & BUSINESS CONTINUITY (RTO/RPO)
    # =========================================================================
    def get_resilience_dr(self) -> List[Dict[str, Any]]:
        """Retrieve conformed Disaster Recovery and RTO/RPO records from ea.gold.resilience_dr."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_resilience_dr ORDER BY dr_tier ASC, component_urn ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["sla_breached"] = bool(d.get("sla_breached"))
            rows.append(d)
        conn.close()
        return rows

    def save_resilience_dr(self, records: List[Dict[str, Any]]) -> int:
        """Upsert Disaster Recovery and RTO/RPO records into ea.gold.resilience_dr."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_resilience_dr (
                component_urn, dr_tier, rto_actual_min, rto_target_min,
                rpo_actual_min, rpo_target_min, replication_strategy,
                failover_automation, sla_breached
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(component_urn) DO UPDATE SET
                dr_tier = excluded.dr_tier,
                rto_actual_min = excluded.rto_actual_min,
                rto_target_min = excluded.rto_target_min,
                rpo_actual_min = excluded.rpo_actual_min,
                rpo_target_min = excluded.rpo_target_min,
                replication_strategy = excluded.replication_strategy,
                failover_automation = excluded.failover_automation,
                sla_breached = excluded.sla_breached;
            """, (
                r["component_urn"],
                r["dr_tier"],
                int(r["rto_actual_min"]),
                int(r["rto_target_min"]),
                int(r["rpo_actual_min"]),
                int(r["rpo_target_min"]),
                r["replication_strategy"],
                r["failover_automation"],
                1 if r.get("sla_breached") else 0,
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S13: TECHNICAL DEBT & GIT CHURN HOTSPOTS
    # =========================================================================
    def get_tech_debt_hotspots(self) -> List[Dict[str, Any]]:
        """Retrieve conformed technical debt and git churn records from ea.gold.tech_debt_hotspots."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_tech_debt_hotspots ORDER BY refactoring_roi_rank ASC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def save_tech_debt_hotspots(self, records: List[Dict[str, Any]]) -> int:
        """Upsert technical debt hotspot records into ea.gold.tech_debt_hotspots."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_tech_debt_hotspots (
                component_urn, debt_score, git_churn_lines_30d,
                cyclomatic_complexity, architectural_smells, refactoring_roi_rank
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(component_urn) DO UPDATE SET
                debt_score = excluded.debt_score,
                git_churn_lines_30d = excluded.git_churn_lines_30d,
                cyclomatic_complexity = excluded.cyclomatic_complexity,
                architectural_smells = excluded.architectural_smells,
                refactoring_roi_rank = excluded.refactoring_roi_rank;
            """, (
                r["component_urn"],
                int(r["debt_score"]),
                int(r["git_churn_lines_30d"]),
                float(r["cyclomatic_complexity"]),
                r["architectural_smells"],
                int(r["refactoring_roi_rank"]),
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S14: ZERO-TRUST SECURITY & NETWORK MICRO-SEGMENTATION
    # =========================================================================
    def get_security_zero_trust(self) -> List[Dict[str, Any]]:
        """Retrieve conformed Zero-Trust microsegmentation flows from ea.gold.security_zero_trust."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_security_zero_trust ORDER BY source_urn ASC, target_urn ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["mtls_enforced"] = bool(d.get("mtls_enforced"))
            rows.append(d)
        conn.close()
        return rows

    def save_security_zero_trust(self, records: List[Dict[str, Any]]) -> int:
        """Upsert Zero-Trust microsegmentation flow records into ea.gold.security_zero_trust."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            flow_id = r.get("id") or f"{r['source_urn']}:{r['target_urn']}:{r['protocol']}"
            cur.execute("""
            INSERT INTO gold_security_zero_trust (
                id, source_urn, target_urn, protocol, mtls_enforced,
                trust_zone_source, trust_zone_target, microsegmentation_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                source_urn = excluded.source_urn,
                target_urn = excluded.target_urn,
                protocol = excluded.protocol,
                mtls_enforced = excluded.mtls_enforced,
                trust_zone_source = excluded.trust_zone_source,
                trust_zone_target = excluded.trust_zone_target,
                microsegmentation_status = excluded.microsegmentation_status;
            """, (
                flow_id,
                r["source_urn"],
                r["target_urn"],
                r["protocol"],
                1 if r.get("mtls_enforced") else 0,
                r["trust_zone_source"],
                r["trust_zone_target"],
                r["microsegmentation_status"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S15: SOFTWARE SUPPLY CHAIN & SBOM LICENSE GATE
    # =========================================================================
    def get_supply_chain_sbom(self) -> List[Dict[str, Any]]:
        """Retrieve conformed SBOM package records from ea.gold.supply_chain_sbom."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_supply_chain_sbom ORDER BY max_severity DESC, package_name ASC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def save_supply_chain_sbom(self, records: List[Dict[str, Any]]) -> int:
        """Upsert SBOM package records into ea.gold.supply_chain_sbom."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            pkg_id = r.get("id") or f"{r['package_name']}:{r['component_urn']}"
            cur.execute("""
            INSERT INTO gold_supply_chain_sbom (
                id, package_name, version, component_urn, license,
                license_compliance, cve_count, max_severity
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                package_name = excluded.package_name,
                version = excluded.version,
                component_urn = excluded.component_urn,
                license = excluded.license,
                license_compliance = excluded.license_compliance,
                cve_count = excluded.cve_count,
                max_severity = excluded.max_severity;
            """, (
                pkg_id,
                r["package_name"],
                r["version"],
                r["component_urn"],
                r["license"],
                r["license_compliance"],
                int(r["cve_count"]),
                r["max_severity"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S16: FINOPS CLOUD COST ALLOCATION & UNIT ECONOMICS
    # =========================================================================
    def get_finops_unit_economics(self) -> List[Dict[str, Any]]:
        """Retrieve conformed FinOps unit economics records from ea.gold.finops_unit_economics."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_finops_unit_economics ORDER BY monthly_spend DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def save_finops_unit_economics(self, records: List[Dict[str, Any]]) -> int:
        """Upsert FinOps unit economics records into ea.gold.finops_unit_economics."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_finops_unit_economics (
                service_urn, monthly_spend, cost_per_transaction,
                tag_compliance_pct, idle_waste_cost, optimization_action
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(service_urn) DO UPDATE SET
                monthly_spend = excluded.monthly_spend,
                cost_per_transaction = excluded.cost_per_transaction,
                tag_compliance_pct = excluded.tag_compliance_pct,
                idle_waste_cost = excluded.idle_waste_cost,
                optimization_action = excluded.optimization_action;
            """, (
                r["service_urn"],
                float(r["monthly_spend"]),
                float(r["cost_per_transaction"]),
                float(r["tag_compliance_pct"]),
                float(r["idle_waste_cost"]),
                r["optimization_action"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S17: MASTER DATA MANAGEMENT (MDM) & GOLDEN RECORDS
    # =========================================================================
    def get_mdm_golden_records(self) -> List[Dict[str, Any]]:
        """Retrieve conformed MDM golden records from ea.gold.mdm_golden_records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_mdm_golden_records ORDER BY entity_name ASC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["divergence_detected"] = bool(d["divergence_detected"])
            d["scd2_active"] = bool(d["scd2_active"])
            rows.append(d)
        conn.close()
        return rows

    def save_mdm_golden_records(self, records: List[Dict[str, Any]]) -> int:
        """Upsert MDM golden records into ea.gold.mdm_golden_records."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_mdm_golden_records (
                entity_name, golden_record_urn, authoritative_source,
                competing_sources, divergence_detected, data_contract_status, scd2_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entity_name) DO UPDATE SET
                golden_record_urn = excluded.golden_record_urn,
                authoritative_source = excluded.authoritative_source,
                competing_sources = excluded.competing_sources,
                divergence_detected = excluded.divergence_detected,
                data_contract_status = excluded.data_contract_status,
                scd2_active = excluded.scd2_active;
            """, (
                r["entity_name"],
                r["golden_record_urn"],
                r["authoritative_source"],
                r["competing_sources"],
                1 if r.get("divergence_detected") else 0,
                r["data_contract_status"],
                1 if r.get("scd2_active", True) else 0,
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S18: ESG & GREEN IT CARBON ACCOUNTING
    # =========================================================================
    def get_esg_carbon_accounting(self) -> List[Dict[str, Any]]:
        """Retrieve conformed ESG carbon records from ea.gold.esg_carbon_accounting."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_esg_carbon_accounting ORDER BY monthly_emissions_kgco2 DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def save_esg_carbon_accounting(self, records: List[Dict[str, Any]]) -> int:
        """Upsert ESG carbon records into ea.gold.esg_carbon_accounting."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_esg_carbon_accounting (
                service_urn, region, monthly_kwh,
                grid_carbon_intensity_gco2_kwh, monthly_emissions_kgco2,
                green_tier, reduction_recommendation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(service_urn) DO UPDATE SET
                region = excluded.region,
                monthly_kwh = excluded.monthly_kwh,
                grid_carbon_intensity_gco2_kwh = excluded.grid_carbon_intensity_gco2_kwh,
                monthly_emissions_kgco2 = excluded.monthly_emissions_kgco2,
                green_tier = excluded.green_tier,
                reduction_recommendation = excluded.reduction_recommendation;
            """, (
                r["service_urn"],
                r["region"],
                float(r["monthly_kwh"]),
                float(r["grid_carbon_intensity_gco2_kwh"]),
                float(r["monthly_emissions_kgco2"]),
                r["green_tier"],
                r["reduction_recommendation"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S19: TEAM TOPOLOGIES & CONWAY'S LAW
    # =========================================================================
    def get_team_topologies(self) -> List[Dict[str, Any]]:
        """Retrieve conformed Team Topologies records from ea.gold.team_topologies."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_team_topologies ORDER BY commit_co_change_friction DESC;")
        rows = []
        for r in cur.fetchall():
            d = dict(r)
            d["codeowners_match"] = bool(d["codeowners_match"])
            rows.append(d)
        conn.close()
        return rows

    def save_team_topologies(self, records: List[Dict[str, Any]]) -> int:
        """Upsert Team Topologies records into ea.gold.team_topologies."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_team_topologies (
                team_name, team_type, owned_components,
                codeowners_match, commit_co_change_friction, conways_law_alignment
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(team_name) DO UPDATE SET
                team_type = excluded.team_type,
                owned_components = excluded.owned_components,
                codeowners_match = excluded.codeowners_match,
                commit_co_change_friction = excluded.commit_co_change_friction,
                conways_law_alignment = excluded.conways_law_alignment;
            """, (
                r["team_name"],
                r["team_type"],
                r["owned_components"],
                1 if r.get("codeowners_match", True) else 0,
                float(r["commit_co_change_friction"]),
                r["conways_law_alignment"],
            ))
            count += 1
        conn.commit()
        conn.close()
        return count

    # =========================================================================
    # S20: VENDOR LOCK-IN & EXIT PLANNING
    # =========================================================================
    def get_vendor_lockin_exit(self) -> List[Dict[str, Any]]:
        """Retrieve conformed vendor lock-in exit records from ea.gold.vendor_lockin_exit."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gold_vendor_lockin_exit ORDER BY lockin_risk_score DESC;")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def save_vendor_lockin_exit(self, records: List[Dict[str, Any]]) -> int:
        """Upsert vendor lock-in exit records into ea.gold.vendor_lockin_exit."""
        conn = self._get_local_connection()
        cur = conn.cursor()
        count = 0
        for r in records:
            cur.execute("""
            INSERT INTO gold_vendor_lockin_exit (
                component_urn, cloud_provider, proprietary_services_used,
                lockin_risk_score, open_alternative, exit_effort_weeks, exit_strategy_action
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(component_urn) DO UPDATE SET
                cloud_provider = excluded.cloud_provider,
                proprietary_services_used = excluded.proprietary_services_used,
                lockin_risk_score = excluded.lockin_risk_score,
                open_alternative = excluded.open_alternative,
                exit_effort_weeks = excluded.exit_effort_weeks,
                exit_strategy_action = excluded.exit_strategy_action;
            """, (
                r["component_urn"],
                r["cloud_provider"],
                r["proprietary_services_used"],
                int(r["lockin_risk_score"]),
                r["open_alternative"],
                int(r["exit_effort_weeks"]),
                r["exit_strategy_action"],
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
            ("ea.bronze.api_gateway_logs", "bronze_api_gateway_logs"),
            ("ea.bronze.process_event_logs", "bronze_process_event_logs"),
            ("ea.bronze.ai_models", "bronze_ai_models"),
            ("ea.gold.time_matrix", "gold_time_matrix"),
            ("ea.gold.drift_reconciled", "gold_drift_reconciled"),
            ("ea.gold.capability_realization", "gold_capability_realization"),
            ("ea.gold.arb_audit_ledger", "gold_arb_audit_ledger"),
            ("ea.gold.ma_synergies", "gold_ma_synergies"),
            ("ea.gold.compliance_lineage", "gold_compliance_lineage"),
            ("ea.gold.interface_rationalization", "gold_interface_rationalization"),
            ("ea.gold.process_optimization", "gold_process_optimization"),
            ("ea.gold.ai_governance", "gold_ai_governance"),
            ("ea.gold.resilience_dr", "gold_resilience_dr"),
            ("ea.gold.tech_debt_hotspots", "gold_tech_debt_hotspots"),
            ("ea.gold.security_zero_trust", "gold_security_zero_trust"),
            ("ea.gold.supply_chain_sbom", "gold_supply_chain_sbom"),
            ("ea.gold.finops_unit_economics", "gold_finops_unit_economics"),
            ("ea.gold.mdm_golden_records", "gold_mdm_golden_records"),
            ("ea.gold.esg_carbon_accounting", "gold_esg_carbon_accounting"),
            ("ea.gold.team_topologies", "gold_team_topologies"),
            ("ea.gold.vendor_lockin_exit", "gold_vendor_lockin_exit"),
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
