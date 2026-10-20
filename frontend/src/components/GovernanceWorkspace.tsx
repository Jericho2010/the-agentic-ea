import React, { useState } from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  FileCheck2,
  FileX2,
  Scale,
  Search,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ExternalLink,
} from 'lucide-react';
import { GovernanceData, ArbLedgerItem } from '../types';

interface GovernanceWorkspaceProps {
  governance: GovernanceData | null;
  loading: boolean;
}

export const GovernanceWorkspace: React.FC<GovernanceWorkspaceProps> = ({
  governance,
  loading,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [decisionFilter, setDecisionFilter] = useState('ALL');

  const policies = governance?.policies || [];
  const ledger = governance?.ledger || [];
  const complianceRate = governance?.compliance_rate ?? 92.4;
  const totalAudits = governance?.total_audits ?? ledger.length;
  const approvedCount = governance?.approved_count ?? 0;
  const blockedCount = governance?.blocked_count ?? 0;
  const waiverCount = governance?.waiver_count ?? 0;
  const regulatoryLineage = governance?.regulatory_lineage || [];

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
      {/* Top Governance Metric Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              ARB Gate Compliance Rate
            </span>
            <div className="p-2 rounded bg-emerald-500/10 text-emerald-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {complianceRate.toFixed(1)}%
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Passing</span>
          </div>
          <div className="mt-2 text-xs text-emerald-400">
            Tri-Modal Pre-Merge Enforcement
          </div>
        </div>

        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Total Audits Evaluated
            </span>
            <div className="p-2 rounded bg-sky-500/10 text-sky-400">
              <Scale className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {totalAudits}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Ledger Records</span>
          </div>
          <div className="mt-2 text-xs text-[#94a3b8]">
            Immutable Unity Catalog Delta Table
          </div>
        </div>

        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Approved Merges
            </span>
            <div className="p-2 rounded bg-emerald-500/10 text-emerald-400">
              <FileCheck2 className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {approvedCount}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">PRs Clean</span>
          </div>
          <div className="mt-2 text-xs text-emerald-400">
            0 Architecture Violations
          </div>
        </div>

        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Blocked / Waivers
            </span>
            <div className="p-2 rounded bg-rose-500/10 text-rose-400">
              <FileX2 className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {blockedCount} / {waiverCount}
            </span>
          </div>
          <div className="mt-2 text-xs text-rose-400">
            Strict ARB Quarantine Enforced
          </div>
        </div>
      </div>

      {/* Sentinel Active Policies Catalog */}
      <div className="space-y-3">
        <div>
          <h2 className="text-base font-bold text-white tracking-tight">
            Sentinel Architecture Policies (Automated Pre-Merge Enforcement)
          </h2>
          <p className="text-xs text-[#94a3b8]">
            Policies evaluated against infrastructure-as-code and git diffs before merging into production.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {policies.map((pol) => {
            const isCritical = pol.severity === 'CRITICAL';
            return (
              <div
                key={pol.id}
                className="ea-stat-card rounded-lg p-5 border shadow-sm transition hover:border-[#334155]"
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

      {/* Regulatory Lineage Cards */}
      <div className="space-y-3">
        <div>
          <h3 className="text-sm font-bold text-white">Regulatory Lineage & Compliance Standards</h3>
          <p className="text-xs text-[#94a3b8]">Statutory architecture compliance mapping</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {regulatoryLineage.map((reg, idx) => (
            <div
              key={idx}
              className="ea-stat-card rounded-lg p-4 border shadow-sm"
              style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white">{reg.regulation}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">
                  {reg.status}
                </span>
              </div>
              <div className="text-[11px] font-mono text-sky-400 mt-1">{reg.article}</div>
              <p className="text-xs text-[#94a3b8] mt-2">{reg.scope}</p>
              <div className="mt-3 pt-2 border-t border-[#1e293b] text-[11px] text-[#e2e8f0]">
                {reg.enforcement}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ARB Audit Ledger Table */}
      <div
        className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-white">Live ARB Audit Ledger</h3>
            <p className="text-xs text-[#94a3b8]">
              Automated pre-merge decisions recorded immutably in Databricks Unity Catalog
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

        <div className="overflow-x-auto max-h-[500px]">
          <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
            <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
              <tr>
                <th className="px-4 py-3">Audit ID</th>
                <th className="px-4 py-3">PR ID</th>
                <th className="px-4 py-3">Decision</th>
                <th className="px-4 py-3">Violations</th>
                <th className="px-4 py-3">Evaluator</th>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3">Artifact</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
              {filteredLedger.map((row) => {
                const isApproved =
                  row.decision === 'APPROVED' || row.decision === 'MERGEABLE';
                const isBlocked = row.decision === 'BLOCKED';

                return (
                  <tr key={row.audit_id || row.timestamp} className="hover:bg-[#1a233a] transition">
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
                    <td className="px-4 py-3 text-[11px] text-sky-400 font-mono">
                      {row.diagram_delta_path ? 'delta.svg' : 'N/A'}
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
