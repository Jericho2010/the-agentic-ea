export interface HealthInfo {
  status: string;
  cloud_connected: boolean;
  warehouse_id: string;
  latency_ms: number;
  catalog: string;
  timestamp: number;
}

export interface EstateStats {
  total_cis: number;
  realization_edges: number;
  annual_spend_usd: number;
  annual_spend_m: number;
  avoidable_co2_kg_monthly: number;
  avoidable_co2_tons_annual: number;
  drift_count: number;
  sentinel_compliance_score: number;
  warehouse_id: string;
  cloud_connected: boolean;
}

export interface TimeItem {
  urn: string;
  name: string;
  disposition: 'Invest' | 'Tolerate' | 'Migrate' | 'Eliminate';
  annual_run_cost: number;
  tech_debt_score: number;
  business_value_score?: number;
  eol_date?: string;
  lifecycle?: string;
  domain?: string;
}

export interface LifecycleRisk {
  name: string;
  urn: string;
  risk_status: 'EXPIRED' | 'NEAR_EOL' | 'APPROACHING_EOL' | 'SUPPORTED';
  risk_level: string;
  eol_date: string;
  days_remaining: number;
  upstream_callers_count: number;
  financial_exposure_usd: number;
  recommendation: string;
}

export interface TimeMatrixData {
  items: TimeItem[];
  total_items: number;
  total_spend_usd: number;
  quadrants: {
    Invest: TimeItem[];
    Tolerate: TimeItem[];
    Migrate: TimeItem[];
    Eliminate: TimeItem[];
  };
  spend_by_quadrant: {
    Invest: number;
    Tolerate: number;
    Migrate: number;
    Eliminate: number;
  };
  lifecycle_risks: LifecycleRisk[];
}

export interface SentinelPolicy {
  id: string;
  title: string;
  severity: string;
  description: string;
  target_standard: string;
}

export interface ArbLedgerItem {
  audit_id: string;
  pr_id: string;
  commit_hash: string;
  decision: string;
  policy_status: string;
  violations_count: number;
  evaluator: string;
  resources_evaluated?: number;
  diagram_delta_path?: string;
  timestamp: string;
  violations?: any[];
}

export interface RegulatoryLineageItem {
  regulation: string;
  article: string;
  scope: string;
  status: string;
  enforcement: string;
}

export interface GovernanceData {
  policies: SentinelPolicy[];
  ledger: ArbLedgerItem[];
  total_audits: number;
  approved_count: number;
  blocked_count: number;
  waiver_count: number;
  compliance_rate: number;
  regulatory_lineage: RegulatoryLineageItem[];
}

export interface DriftItem {
  urn: string;
  ci_name?: string;
  discrepancy_type: string;
  severity: string;
  declared_state: string;
  runtime_state: string;
  reconciled_at: string;
  drift_id?: string;
  drift_type?: string;
  remediation_action?: string;
  remediation_payload?: string;
}

export interface DriftData {
  total_drift_records: number;
  items: DriftItem[];
  taxonomy: Record<string, number>;
  grouped_items: Record<string, DriftItem[]>;
}

export interface MetamodelNode {
  urn: string;
  kind: string;
  name: string;
  domain?: string;
  lifecycle?: string;
  status?: string;
  owner?: string;
  metadata?: any;
}

export interface MetamodelEdge {
  source_urn: string;
  target_urn: string;
  relationship: string;
  weight?: number;
}

export interface DiagramInfo {
  name: string;
  title: string;
  size_bytes: number;
}

export interface SamplePatch {
  id: string;
  name: string;
  decision_expected: string;
  description: string;
  patch: string;
}

export interface SimulationResult {
  audit_id?: string;
  pr_id?: string;
  decision: string;
  passed: boolean;
  policy_status?: string;
  violations_count: number;
  violations?: Array<{
    policy_id: string;
    rule_name: string;
    resource_type?: string;
    resource_name?: string;
    severity: string;
    description: string;
    recommendation?: string;
  }>;
  markdown_report?: string;
  diagrams?: Record<string, string>;
}

export interface EntityDetail {
  node: MetamodelNode;
  time_assessment?: TimeItem | null;
  drift_record?: DriftItem | null;
  upstream_callers: MetamodelEdge[];
  downstream_datastores: MetamodelEdge[];
  carbon_accounting?: Record<string, any>;
  raw_json: Record<string, any>;
}
