import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  FileCheck2,
  FileX2,
  Scale,
  Search,
  CheckCircle2,
  AlertTriangle,
  Play,
  RefreshCw,
  GitPullRequest,
  ExternalLink,
  ChevronRight,
  Code2,
} from 'lucide-react';
import { GovernanceData, ArbLedgerItem, SamplePatch, SimulationResult } from '../types';

interface GovernanceWorkspaceProps {
  governance: GovernanceData | null;
  loading: boolean;
  onSelectEntity: (urn: string) => void;
  openSimulatorDirectly?: boolean;
}

export const GovernanceWorkspace: React.FC<GovernanceWorkspaceProps> = ({
  governance,
  loading,
  onSelectEntity,
  openSimulatorDirectly = false,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [decisionFilter, setDecisionFilter] = useState('ALL');

  // PR Simulator state
  const [samples, setSamples] = useState<SamplePatch[]>([]);
  const [selectedSampleId, setSelectedSampleId] = useState<string>('unapproved_db');
  const [customPatch, setCustomPatch] = useState<string>('');
  const [simulating, setSimulating] = useState<boolean>(false);
  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);

  const policies = governance?.policies || [];
  const ledger = governance?.ledger || [];
  const complianceRate = governance?.compliance_rate ?? 92.4;
  const totalAudits = governance?.total_audits ?? ledger.length;
  const approvedCount = governance?.approved_count ?? 0;
  const blockedCount = governance?.blocked_count ?? 0;
  const waiverCount = governance?.waiver_count ?? 0;
  const regulatoryLineage = governance?.regulatory_lineage || [];

  // Fetch sample patches on mount
  useEffect(() => {
    fetch('/api/governance/sample-patches')
      .then((r) => r.json())
      .then((res) => {
        if (res.samples && res.samples.length > 0) {
          setSamples(res.samples);
          const defaultSample = res.samples.find((s: SamplePatch) => s.id === 'unapproved_db') || res.samples[0];
          setSelectedSampleId(defaultSample.id);
          setCustomPatch(defaultSample.patch);
        }
      })
      .catch((err) => console.error('Error fetching sample patches:', err));
  }, []);

  const handleSelectSample = (sample: SamplePatch) => {
    setSelectedSampleId(sample.id);
    setCustomPatch(sample.patch);
    setSimulationResult(null);
  };

  const handleRunSimulation = async () => {
    if (!customPatch) return;
    setSimulating(true);
    setSimulationResult(null);
    try {
      const res = await fetch('/api/governance/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patch: customPatch }),
      });
      const data = await res.json();
      if (data.result) {
        setSimulationResult(data.result);
      }
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setSimulating(false);
    }
  };

  const filteredLedger = ledger.filter((item) => {
    const matchesSearch =
      item.pr_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.audit_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.evaluator?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDecision =
      decisionFilter === 'ALL' || item.decision === decisionFilter;
    return matchesSearch && matchesDecision;
  });

  return (
    <div className="space-y-6">
      {/* 1. TOP METRICS RIBBON */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div
          className="ea-stat-card rounded-xl p-4 border flex items-center justify-between shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Sentinel Pass Rate
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {complianceRate.toFixed(1)}%
              </span>
              <span className="text-[11px] text-emerald-400 font-medium">Deterministic</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>

        <div
          className="ea-stat-card rounded-xl p-4 border flex items-center justify-between shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Total ARB Audits
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {totalAudits}
              </span>
              <span className="text-[11px] text-[#94a3b8]">Ledger Records</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-sky-500/10 text-sky-400">
            <Scale className="w-5 h-5" />
          </div>
        </div>

        <div
          className="ea-stat-card rounded-xl p-4 border flex items-center justify-between shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Approved Merges
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {approvedCount}
              </span>
              <span className="text-[11px] text-emerald-400 font-medium">0 Violations</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <FileCheck2 className="w-5 h-5" />
          </div>
        </div>

        <div
          className="ea-stat-card rounded-xl p-4 border flex items-center justify-between shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Blocked / Waivers
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {blockedCount} / {waiverCount}
              </span>
              <span className="text-[11px] text-rose-400 font-medium">Quarantined</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-rose-500/10 text-rose-400">
            <FileX2 className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* 2. INTERACTIVE PR POLICY SIMULATOR */}
      <div
        className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-[#0d1322]/80">
          <div>
            <div className="flex items-center space-x-2">
              <GitPullRequest className="w-4 h-4 text-sky-400" />
              <h3 className="text-sm font-bold text-white tracking-tight">
                Sentinel Pre-Merge PR Policy Simulator
              </h3>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Live Engine
              </span>
            </div>
            <p className="text-xs text-[#94a3b8] mt-0.5">
              Simulate incoming Infrastructure-as-Code diffs against PAM rules before merging to production.
            </p>
          </div>

          <button
            onClick={handleRunSimulation}
            disabled={simulating || !customPatch}
            className="px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-400 text-[#0b0f19] font-bold text-xs transition flex items-center space-x-2 shadow-lg shadow-sky-500/20 disabled:opacity-50"
          >
            {simulating ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Evaluating Patch...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Simulate Evaluation</span>
              </>
            )}
          </button>
        </div>

        <div className="p-6 space-y-4">
          {/* Sample Patch Picker Pills */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-[#94a3b8] font-medium mr-1">Sample PR Scenarios:</span>
            {samples.map((s) => (
              <button
                key={s.id}
                onClick={() => handleSelectSample(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center space-x-2 border ${
                  selectedSampleId === s.id
                    ? 'bg-sky-500/10 text-sky-300 border-sky-500/40'
                    : 'bg-[#0d1322] text-[#94a3b8] border-[#1e293b] hover:text-white'
                }`}
              >
                <span>{s.name}</span>
                <span
                  className={`text-[9px] px-1 py-0.2 rounded font-mono font-bold ${
                    s.decision_expected === 'APPROVED'
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : s.decision_expected === 'BLOCKED'
                      ? 'bg-rose-500/20 text-rose-400'
                      : 'bg-amber-500/20 text-amber-400'
                  }`}
                >
                  {s.decision_expected}
                </span>
              </button>
            ))}
          </div>

          {/* Unified Diff Editor Area */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-xs text-[#94a3b8]">
                <span className="font-mono">unified_git_diff.patch</span>
                <span>Editable TerraForm / K8s Manifest</span>
              </div>
              <textarea
                value={customPatch}
                onChange={(e) => {
                  setCustomPatch(e.target.value);
                  setSelectedSampleId('custom');
                }}
                rows={12}
                className="w-full p-3.5 rounded-lg bg-[#080c14] border border-[#1e293b] text-sky-300 font-mono text-xs focus:outline-none focus:border-sky-500/50 leading-relaxed"
                placeholder="Paste unified git diff here..."
              />
            </div>

            {/* Simulation Results Display */}
            <div className="p-4 rounded-lg bg-[#080c14] border border-[#1e293b] flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-[#1e293b]">
                  <span className="text-xs font-bold text-white uppercase tracking-wider">
                    Evaluation Result
                  </span>
                  {simulationResult ? (
                    <span
                      className={`text-xs font-extrabold px-2.5 py-1 rounded border ${
                        simulationResult.decision === 'APPROVED' || simulationResult.decision === 'MERGEABLE'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                          : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                      }`}
                    >
                      {simulationResult.decision}
                    </span>
                  ) : (
                    <span className="text-xs text-[#94a3b8] font-mono">Awaiting Trigger</span>
                  )}
                </div>

                {simulating && (
                  <div className="py-12 flex flex-col items-center justify-center space-y-3 text-xs text-[#94a3b8]">
                    <RefreshCw className="w-6 h-6 text-sky-400 animate-spin" />
                    <span>Executing Tri-Modal Deterministic PAM Evaluation...</span>
                  </div>
                )}

                {!simulating && !simulationResult && (
                  <div className="py-12 text-center text-xs text-[#94a3b8] space-y-1">
                    <p>Select a scenario above and click "Simulate Evaluation".</p>
                    <p className="text-[11px] text-[#94a3b8]/60">
                      Evaluates EA-POL-001 (Datastores), EA-POL-002 (PII KMS), EA-POL-003 (Tags).
                    </p>
                  </div>
                )}

                {!simulating && simulationResult && (
                  <div className="py-3 space-y-3">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-[#94a3b8]">Violations Detected:</span>
                      <span className="font-bold text-white font-mono">
                        {simulationResult.violations_count}
                      </span>
                    </div>

                    {simulationResult.violations && simulationResult.violations.length > 0 ? (
                      <div className="space-y-2 max-h-48 overflow-y-auto">
                        {simulationResult.violations.map((v, i) => (
                          <div
                            key={i}
                            className="p-2.5 rounded bg-[#131b2e] border border-rose-500/30 text-xs space-y-1"
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-mono text-rose-400 font-bold">{v.policy_id}</span>
                              <span className="text-[10px] text-rose-400 font-semibold uppercase">{v.severity}</span>
                            </div>
                            <p className="text-white font-medium">{v.description}</p>
                            {v.recommendation && (
                              <p className="text-[11px] text-[#94a3b8]">{v.recommendation}</p>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="p-3 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center space-x-2">
                        <CheckCircle2 className="w-4 h-4 shrink-0" />
                        <span>All architectural standards passed. PR is safe to merge.</span>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {simulationResult?.diagrams && (
                <div className="pt-3 border-t border-[#1e293b] flex justify-between items-center text-xs">
                  <span className="text-[#94a3b8]">Archify Visual Delta Generated</span>
                  <a
                    href="/api/diagrams/diagram_delta.html"
                    target="_blank"
                    rel="noreferrer"
                    className="text-sky-400 hover:text-sky-300 font-medium flex items-center space-x-1"
                  >
                    <span>Inspect Delta Map</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 3. POLICY CATALOG CARDS */}
      <div className="space-y-3">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">
            Active Sentinel Architectural Policies
          </h2>
          <p className="text-xs text-[#94a3b8]">
            Enforced continuously across all repositories and cloud accounts.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {policies.map((pol) => {
            const isCritical = pol.severity === 'CRITICAL';
            return (
              <div
                key={pol.id}
                className="ea-stat-card rounded-xl p-5 border shadow-sm transition hover:border-[#334155]"
                style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-sky-400">
                    {pol.id}
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                      isCritical
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    }`}
                  >
                    {pol.severity}
                  </span>
                </div>
                <h4 className="text-sm font-semibold text-white mt-2">
                  {pol.title}
                </h4>
                <p className="text-xs text-[#94a3b8] mt-1 line-clamp-3">
                  {pol.description}
                </p>
                <div className="mt-3 pt-3 border-t border-[#1e293b] text-[11px]">
                  <span className="text-[#94a3b8]">Target Standard: </span>
                  <span className="text-[#e2e8f0] font-medium">{pol.target_standard}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. ARB AUDIT LEDGER TABLE */}
      <div
        className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-[#0d1322]/80">
          <div>
            <h3 className="text-sm font-bold text-white">Live ARB Audit Ledger</h3>
            <p className="text-xs text-[#94a3b8]">
              Automated pre-merge decisions recorded immutably in Databricks Unity Catalog. Click any row to inspect in Drawer.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94a3b8]" />
              <input
                type="text"
                placeholder="Search audits..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white placeholder-[#94a3b8] focus:outline-none focus:border-sky-500"
              />
            </div>
            <select
              value={decisionFilter}
              onChange={(e) => setDecisionFilter(e.target.value)}
              className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white focus:outline-none focus:border-sky-500"
            >
              <option value="ALL">All Decisions</option>
              <option value="APPROVED">APPROVED</option>
              <option value="MERGEABLE">MERGEABLE</option>
              <option value="BLOCKED">BLOCKED</option>
              <option value="WAIVER_GRANTED">WAIVER_GRANTED</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto max-h-[460px]">
          <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
            <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
              <tr>
                <th className="px-4 py-3">Audit ID</th>
                <th className="px-4 py-3">PR ID</th>
                <th className="px-4 py-3">Decision</th>
                <th className="px-4 py-3">Violations</th>
                <th className="px-4 py-3">Evaluator</th>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
              {filteredLedger.map((row) => {
                const isApproved =
                  row.decision === 'APPROVED' || row.decision === 'MERGEABLE';
                const isBlocked = row.decision === 'BLOCKED';

                return (
                  <tr
                    key={row.audit_id || row.timestamp}
                    onClick={() => onSelectEntity(row.audit_id || row.pr_id)}
                    className="hover:bg-[#1a233a] cursor-pointer transition"
                  >
                    <td className="px-4 py-3 font-mono text-[11px] text-sky-400">
                      {row.audit_id ? row.audit_id.slice(0, 16) : 'N/A'}
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px] text-white">
                      {row.pr_id || 'manual-eval'}
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-block px-2 py-0.5 text-[11px] font-semibold rounded border ${
                          isApproved
                            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                            : isBlocked
                            ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                            : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                        }`}
                      >
                        {row.decision}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-white">
                      {row.violations_count ?? (row.violations ? row.violations.length : 0)}
                    </td>
                    <td className="px-4 py-3 text-[#94a3b8] text-[11px]">
                      {row.evaluator || 'subscription_cli'}
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">
                      {row.timestamp ? new Date(row.timestamp).toLocaleString() : 'N/A'}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <span className="text-xs text-sky-400 hover:text-white font-medium flex items-center justify-end space-x-1">
                        <span>Inspect</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
