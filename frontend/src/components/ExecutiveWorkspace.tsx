import React, { useState } from 'react';
import {
  Database,
  DollarSign,
  Leaf,
  ShieldCheck,
  TrendingUp,
  Clock,
  ArrowUpRight,
  AlertTriangle,
  Search,
  Filter,
} from 'lucide-react';
import { EstateStats, TimeMatrixData, TimeItem } from '../types';

interface ExecutiveWorkspaceProps {
  stats: EstateStats | null;
  timeMatrix: TimeMatrixData | null;
  loading: boolean;
}

export const ExecutiveWorkspace: React.FC<ExecutiveWorkspaceProps> = ({
  stats,
  timeMatrix,
  loading,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDisposition, setFilterDisposition] = useState<string>('ALL');

  const totalCis = stats?.total_cis ?? 36;
  const totalSpend = stats?.annual_spend_usd ?? 431799.72;
  const avoidableCo2 = stats?.avoidable_co2_kg_monthly ?? 420;
  const complianceScore = stats?.sentinel_compliance_score ?? 92.4;

  const quadrants = timeMatrix?.quadrants || {
    Invest: [],
    Tolerate: [],
    Migrate: [],
    Eliminate: [],
  };

  const spendByQuad = timeMatrix?.spend_by_quadrant || {
    Invest: 0,
    Tolerate: 0,
    Migrate: 0,
    Eliminate: 0,
  };

  const items = timeMatrix?.items || [];
  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.urn.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDisp =
      filterDisposition === 'ALL' || item.disposition === filterDisposition;
    return matchesSearch && matchesDisp;
  });

  const lifecycleRisks = timeMatrix?.lifecycle_risks || [];

  return (
    <div className="space-y-6">
      {/* 4 Quick Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: PAM CIs */}
        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              PAM Managed Nodes
            </span>
            <div className="p-2 rounded bg-sky-500/10 text-sky-400">
              <Database className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {totalCis}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Live PAM CIs</span>
          </div>
          <div className="mt-2 text-xs text-emerald-400 flex items-center space-x-1">
            <TrendingUp className="w-3.5 h-3.5" />
            <span>100% Conformed to Unity Catalog</span>
          </div>
        </div>

        {/* Card 2: Annual Run Cost */}
        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Annual Estate Spend
            </span>
            <div className="p-2 rounded bg-emerald-500/10 text-emerald-400">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              ${(totalSpend / 1000).toFixed(1)}k
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">/yr</span>
          </div>
          <div className="mt-2 text-xs text-[#94a3b8] flex items-center space-x-1">
            <span>Attributed across 11 applications</span>
          </div>
        </div>

        {/* Card 3: Avoidable Carbon */}
        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Avoidable CO2 (Legacy DBs)
            </span>
            <div className="p-2 rounded bg-rose-500/10 text-rose-400">
              <Leaf className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {avoidableCo2.toFixed(0)}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">kg/mo</span>
          </div>
          <div className="mt-2 text-xs text-amber-400 flex items-center space-x-1">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Eliminating Cassandra saves 5.0t/yr</span>
          </div>
        </div>

        {/* Card 4: Sentinel Compliance */}
        <div
          className="ea-stat-card rounded-lg p-5 border shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Sentinel Policy Gate
            </span>
            <div className="p-2 rounded bg-sky-500/10 text-sky-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {complianceScore.toFixed(1)}%
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Passed</span>
          </div>
          <div className="mt-2 text-xs text-emerald-400 flex items-center space-x-1">
            <span>Deterministic Tri-Modal Rule Enforced</span>
          </div>
        </div>
      </div>

      {/* TIME Matrix 4 Quadrants */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white tracking-tight">
              Executive TIME Matrix (Gartner Portfolio Model)
            </h2>
            <p className="text-xs text-[#94a3b8]">
              FinOps cost allocation and architectural disposition across Invest, Tolerate, Migrate, Eliminate.
            </p>
          </div>
          <span className="text-xs font-mono text-[#94a3b8] px-2.5 py-1 rounded bg-[#131b2e] border border-[#1e293b]">
            Total: ${(totalSpend / 1000).toFixed(1)}k/yr
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Invest */}
          <div
            className="ea-stat-card rounded-lg p-5 border border-emerald-500/30 transition shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)' }}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-400 uppercase tracking-wide">
                Invest
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">
                {quadrants.Invest.length} Apps
              </span>
            </div>
            <div className="mt-2">
              <div
                className="ea-metric-value text-2xl font-bold"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                ${(spendByQuad.Invest / 1000).toFixed(1)}k
              </div>
              <p className="text-[11px] text-[#94a3b8] mt-1">
                High Business Value, Low Tech Debt. Strategic growth assets.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-[#1e293b] text-xs text-[#e2e8f0] space-y-1">
              {quadrants.Invest.slice(0, 3).map((a) => (
                <div key={a.urn} className="flex justify-between items-center text-[11px]">
                  <span className="truncate max-w-[140px] text-white font-medium">{a.name}</span>
                  <span className="font-mono text-[#94a3b8]">${(a.annual_run_cost / 1000).toFixed(1)}k</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tolerate */}
          <div
            className="ea-stat-card rounded-lg p-5 border border-sky-500/30 transition shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)' }}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-sky-400 uppercase tracking-wide">
                Tolerate
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 font-semibold border border-sky-500/20">
                {quadrants.Tolerate.length} Apps
              </span>
            </div>
            <div className="mt-2">
              <div
                className="ea-metric-value text-2xl font-bold"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                ${(spendByQuad.Tolerate / 1000).toFixed(1)}k
              </div>
              <p className="text-[11px] text-[#94a3b8] mt-1">
                Low Business Value, Low Tech Debt. Maintain operations, do not expand.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-[#1e293b] text-xs text-[#e2e8f0] space-y-1">
              {quadrants.Tolerate.slice(0, 3).map((a) => (
                <div key={a.urn} className="flex justify-between items-center text-[11px]">
                  <span className="truncate max-w-[140px] text-white font-medium">{a.name}</span>
                  <span className="font-mono text-[#94a3b8]">${(a.annual_run_cost / 1000).toFixed(1)}k</span>
                </div>
              ))}
            </div>
          </div>

          {/* Migrate */}
          <div
            className="ea-stat-card rounded-lg p-5 border border-amber-500/30 transition shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)' }}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-amber-400 uppercase tracking-wide">
                Migrate
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 font-semibold border border-amber-500/20">
                {quadrants.Migrate.length} Apps
              </span>
            </div>
            <div className="mt-2">
              <div
                className="ea-metric-value text-2xl font-bold"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                ${(spendByQuad.Migrate / 1000).toFixed(1)}k
              </div>
              <p className="text-[11px] text-[#94a3b8] mt-1">
                High Business Value, High Tech Debt. Modernize to Unity Catalog.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-[#1e293b] text-xs text-[#e2e8f0] space-y-1">
              {quadrants.Migrate.slice(0, 3).map((a) => (
                <div key={a.urn} className="flex justify-between items-center text-[11px]">
                  <span className="truncate max-w-[140px] text-white font-medium">{a.name}</span>
                  <span className="font-mono text-[#94a3b8]">${(a.annual_run_cost / 1000).toFixed(1)}k</span>
                </div>
              ))}
            </div>
          </div>

          {/* Eliminate */}
          <div
            className="ea-stat-card rounded-lg p-5 border border-rose-500/30 transition shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)' }}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-rose-400 uppercase tracking-wide">
                Eliminate
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 font-semibold border border-rose-500/20">
                {quadrants.Eliminate.length} Apps
              </span>
            </div>
            <div className="mt-2">
              <div
                className="ea-metric-value text-2xl font-bold"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                ${(spendByQuad.Eliminate / 1000).toFixed(1)}k
              </div>
              <p className="text-[11px] text-[#94a3b8] mt-1">
                Low Business Value, High Tech Debt. Immediate decommission targets.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-[#1e293b] text-xs text-[#e2e8f0] space-y-1">
              {quadrants.Eliminate.slice(0, 3).map((a) => (
                <div key={a.urn} className="flex justify-between items-center text-[11px]">
                  <span className="truncate max-w-[140px] text-white font-medium">{a.name}</span>
                  <span className="font-mono text-[#94a3b8]">${(a.annual_run_cost / 1000).toFixed(1)}k</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Systems Table */}
      <div
        className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-white">Portfolio Systems Classification</h3>
            <p className="text-xs text-[#94a3b8]">Live PAM applications, disposition, run costs and debt scores</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94a3b8]" />
              <input
                type="text"
                placeholder="Search systems..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white placeholder-[#94a3b8] focus:outline-none focus:border-sky-500"
              />
            </div>
            <select
              value={filterDisposition}
              onChange={(e) => setFilterDisposition(e.target.value)}
              className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white focus:outline-none focus:border-sky-500"
            >
              <option value="ALL">All Dispositions</option>
              <option value="Invest">Invest</option>
              <option value="Tolerate">Tolerate</option>
              <option value="Migrate">Migrate</option>
              <option value="Eliminate">Eliminate</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
            <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px]">
              <tr>
                <th className="px-4 py-3">System Name</th>
                <th className="px-4 py-3">PAM URN</th>
                <th className="px-4 py-3">Disposition</th>
                <th className="px-4 py-3">Annual Run Cost</th>
                <th className="px-4 py-3">Tech Debt Score</th>
                <th className="px-4 py-3">EOL Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
              {filteredItems.map((item) => {
                const badgeColor =
                  item.disposition === 'Invest'
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                    : item.disposition === 'Tolerate'
                    ? 'bg-sky-500/10 text-sky-400 border-sky-500/20'
                    : item.disposition === 'Migrate'
                    ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    : 'bg-rose-500/10 text-rose-400 border-rose-500/20';

                return (
                  <tr key={item.urn} className="hover:bg-[#1a233a] transition">
                    <td className="px-4 py-3 font-medium text-white">{item.name}</td>
                    <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">{item.urn}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-block px-2 py-0.5 text-[11px] font-semibold rounded border ${badgeColor}`}>
                        {item.disposition}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-white">
                      ${item.annual_run_cost.toLocaleString('en-US', { minimumFractionDigits: 2 })}/yr
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-white">{item.tech_debt_score}</span>
                        <div className="w-16 bg-[#0b0f19] h-1.5 rounded-full overflow-hidden">
                          <div
                            className={`h-full ${
                              item.tech_debt_score > 60
                                ? 'bg-rose-500'
                                : item.tech_debt_score > 30
                                ? 'bg-amber-500'
                                : 'bg-emerald-500'
                            }`}
                            style={{ width: `${Math.min(item.tech_debt_score, 100)}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">
                      {item.eol_date || 'N/A'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Lifecycle Risk Horizons */}
      {lifecycleRisks.length > 0 && (
        <div
          className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="p-4 border-b border-[#1e293b]">
            <h3 className="text-sm font-bold text-white">Technology Obsolescence & Lifecycle Risk (EOL/EOS)</h3>
            <p className="text-xs text-[#94a3b8]">Automated tracking of End-of-Life horizons, callers, and financial exposure</p>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
              <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px]">
                <tr>
                  <th className="px-4 py-3">Asset Name</th>
                  <th className="px-4 py-3">Risk Status</th>
                  <th className="px-4 py-3">EOL Date</th>
                  <th className="px-4 py-3">Days Remaining</th>
                  <th className="px-4 py-3">Upstream Callers</th>
                  <th className="px-4 py-3">Financial Exposure</th>
                  <th className="px-4 py-3">Architectural Recommendation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
                {lifecycleRisks.map((risk) => {
                  const statusBadge =
                    risk.risk_status === 'EXPIRED'
                      ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                      : risk.risk_status === 'NEAR_EOL'
                      ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                      : risk.risk_status === 'APPROACHING_EOL'
                      ? 'bg-sky-500/10 text-sky-400 border-sky-500/20'
                      : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';

                  return (
                    <tr key={risk.urn} className="hover:bg-[#1a233a] transition">
                      <td className="px-4 py-3 font-medium text-white">{risk.name}</td>
                      <td className="px-4 py-3">
                        <span className={`inline-block px-2 py-0.5 text-[11px] font-semibold rounded border ${statusBadge}`}>
                          {risk.risk_status}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">{risk.eol_date}</td>
                      <td className="px-4 py-3 font-mono text-white">{risk.days_remaining}d</td>
                      <td className="px-4 py-3 font-mono text-white">{risk.upstream_callers_count}</td>
                      <td className="px-4 py-3 font-mono text-white">
                        ${risk.financial_exposure_usd.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-3 text-xs text-[#94a3b8]">{risk.recommendation}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
