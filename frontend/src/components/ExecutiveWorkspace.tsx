import React, { useState } from 'react';
import {
  Database,
  DollarSign,
  Leaf,
  ShieldCheck,
  TrendingUp,
  AlertTriangle,
  Search,
  Grid,
  BarChart2,
  Maximize2,
  ArrowUpRight,
  Clock,
  Layers,
  ChevronRight,
} from 'lucide-react';
import { EstateStats, TimeMatrixData, TimeItem, LifecycleRisk } from '../types';

interface ExecutiveWorkspaceProps {
  stats: EstateStats | null;
  timeMatrix: TimeMatrixData | null;
  loading: boolean;
  onSelectEntity: (urn: string) => void;
}

export const ExecutiveWorkspace: React.FC<ExecutiveWorkspaceProps> = ({
  stats,
  timeMatrix,
  loading,
  onSelectEntity,
}) => {
  const [viewMode, setViewMode] = useState<'canvas' | 'table'>('canvas');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDisposition, setFilterDisposition] = useState<string>('ALL');
  const [hoveredApp, setHoveredApp] = useState<TimeItem | null>(null);

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

  const getAppCoordinates = (item: TimeItem, index: number) => {
    let health = 100 - (item.tech_debt_score || 30);
    let value = item.business_value_score || 50;

    if (!item.business_value_score) {
      if (item.disposition === 'Invest') {
        value = 65 + (index * 7) % 25;
        health = Math.max(health, 65);
      } else if (item.disposition === 'Tolerate') {
        value = 20 + (index * 8) % 25;
        health = Math.max(health, 60);
      } else if (item.disposition === 'Migrate') {
        value = 70 + (index * 5) % 20;
        health = Math.min(health, 40);
      } else if (item.disposition === 'Eliminate') {
        value = 15 + (index * 7) % 20;
        health = Math.min(health, 35);
      }
    }

    return { x: value, y: health };
  };

  return (
    <div className="space-y-6">
      {/* 1. SLIM KPI METRICS RIBBON (Modern Linear/Datadog style) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div
          className="ea-stat-card p-4 rounded-xl border flex items-center justify-between shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              PAM Managed Nodes
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {totalCis}
              </span>
              <span className="text-[11px] text-emerald-400 font-medium">100% Conformed</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-sky-500/10 text-sky-400">
            <Database className="w-5 h-5" />
          </div>
        </div>

        <div
          className="ea-stat-card p-4 rounded-xl border flex items-center justify-between shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Annual Estate Spend
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                ${(totalSpend / 1000).toFixed(1)}k
              </span>
              <span className="text-[11px] text-[#94a3b8]">/yr</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <DollarSign className="w-5 h-5" />
          </div>
        </div>

        <div
          className="ea-stat-card p-4 rounded-xl border flex items-center justify-between shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Avoidable Legacy CO2
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {avoidableCo2.toFixed(0)}
              </span>
              <span className="text-[11px] text-amber-400">kg/mo (Cassandra)</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-rose-500/10 text-rose-400">
            <Leaf className="w-5 h-5" />
          </div>
        </div>

        <div
          className="ea-stat-card p-4 rounded-xl border flex items-center justify-between shadow-sm transition hover:border-[#334155]"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div>
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase block"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Sentinel Policy Score
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span
                className="ea-metric-value text-2xl font-extrabold tracking-tight"
                style={{ color: 'rgb(255, 255, 255)' }}
              >
                {complianceScore.toFixed(1)}%
              </span>
              <span className="text-[11px] text-emerald-400">Gate Active</span>
            </div>
          </div>
          <div className="p-2.5 rounded-lg bg-sky-500/10 text-sky-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* 2. INTERACTIVE 2D TIME MATRIX SECTION */}
      <div
        className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        {/* Header Toolbar */}
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-[#0d1322]/80">
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white tracking-tight">
                Gartner TIME Matrix Portfolio Assessment
              </h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                Interactive 2D Canvas
              </span>
            </div>
            <p className="text-xs text-[#94a3b8] mt-0.5">
              Visualizes Business Value vs Technical Health. Click any application bubble to open the Inspector Drawer.
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div className="flex rounded-lg bg-[#0b0f19] p-0.5 border border-[#1e293b] text-xs">
              <button
                onClick={() => setViewMode('canvas')}
                className={`flex items-center space-x-1.5 px-3 py-1 rounded-md transition ${
                  viewMode === 'canvas'
                    ? 'bg-sky-500/20 text-sky-400 font-semibold'
                    : 'text-[#94a3b8] hover:text-white'
                }`}
              >
                <BarChart2 className="w-3.5 h-3.5" />
                <span>2D Visual Canvas</span>
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`flex items-center space-x-1.5 px-3 py-1 rounded-md transition ${
                  viewMode === 'table'
                    ? 'bg-sky-500/20 text-sky-400 font-semibold'
                    : 'text-[#94a3b8] hover:text-white'
                }`}
              >
                <Grid className="w-3.5 h-3.5" />
                <span>Structured Table</span>
              </button>
            </div>
          </div>
        </div>

        {/* VIEW A: 2D VISUAL CANVAS */}
        {viewMode === 'canvas' && (
          <div className="p-6 relative">
            {/* Quick Quadrant Summary Chips */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
              <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">
                    INVEST ({quadrants.Invest.length})
                  </span>
                  <div className="text-xs font-bold text-white">${(spendByQuad.Invest / 1000).toFixed(1)}k/yr</div>
                </div>
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-400"></div>
              </div>

              <div className="p-2.5 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase font-bold text-sky-400 tracking-wider">
                    TOLERATE ({quadrants.Tolerate.length})
                  </span>
                  <div className="text-xs font-bold text-white">${(spendByQuad.Tolerate / 1000).toFixed(1)}k/yr</div>
                </div>
                <div className="w-2.5 h-2.5 rounded-full bg-sky-400"></div>
              </div>

              <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase font-bold text-amber-400 tracking-wider">
                    MIGRATE ({quadrants.Migrate.length})
                  </span>
                  <div className="text-xs font-bold text-white">${(spendByQuad.Migrate / 1000).toFixed(1)}k/yr</div>
                </div>
                <div className="w-2.5 h-2.5 rounded-full bg-amber-400"></div>
              </div>

              <div className="p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/30 flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase font-bold text-rose-400 tracking-wider">
                    ELIMINATE ({quadrants.Eliminate.length})
                  </span>
                  <div className="text-xs font-bold text-white">${(spendByQuad.Eliminate / 1000).toFixed(1)}k/yr</div>
                </div>
                <div className="w-2.5 h-2.5 rounded-full bg-rose-400"></div>
              </div>
            </div>

            {/* Cartesian Grid Area */}
            <div className="relative w-full h-[500px] bg-[#080c14] rounded-xl border border-[#1e293b] p-4 overflow-hidden select-none">
              {/* Background 4 Quadrant Zones */}
              <div className="absolute inset-0 grid grid-cols-2 grid-rows-2">
                {/* Top-Left: TOLERATE */}
                <div className="border-r border-b border-[#1e293b]/70 p-4 relative bg-gradient-to-br from-sky-500/[0.03] to-transparent">
                  <span className="text-xs font-bold text-sky-400/60 uppercase tracking-wider">
                    TOLERATE
                  </span>
                  <span className="text-[10px] text-[#94a3b8]/50 block">Low Value, High Health</span>
                </div>

                {/* Top-Right: INVEST */}
                <div className="border-b border-[#1e293b]/70 p-4 relative text-right bg-gradient-to-bl from-emerald-500/[0.04] to-transparent">
                  <span className="text-xs font-bold text-emerald-400/60 uppercase tracking-wider">
                    INVEST
                  </span>
                  <span className="text-[10px] text-[#94a3b8]/50 block">High Value, High Health</span>
                </div>

                {/* Bottom-Left: ELIMINATE */}
                <div className="border-r border-[#1e293b]/70 p-4 relative flex flex-col justify-end bg-gradient-to-tr from-rose-500/[0.04] to-transparent">
                  <span className="text-xs font-bold text-rose-400/60 uppercase tracking-wider">
                    ELIMINATE
                  </span>
                  <span className="text-[10px] text-[#94a3b8]/50 block">Low Value, High Tech Debt</span>
                </div>

                {/* Bottom-Right: MIGRATE */}
                <div className="p-4 relative flex flex-col justify-end items-end bg-gradient-to-tl from-amber-500/[0.04] to-transparent">
                  <span className="text-xs font-bold text-amber-400/60 uppercase tracking-wider">
                    MIGRATE
                  </span>
                  <span className="text-[10px] text-[#94a3b8]/50 block">High Value, High Tech Debt</span>
                </div>
              </div>

              {/* Axis Labels */}
              <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[10px] font-bold text-[#94a3b8] uppercase tracking-wider bg-[#080c14]/80 px-2 py-0.5 rounded border border-[#1e293b]">
                Business Value (0 → 100)
              </div>
              <div className="absolute left-2 top-1/2 -translate-y-1/2 -rotate-90 origin-left text-[10px] font-bold text-[#94a3b8] uppercase tracking-wider bg-[#080c14]/80 px-2 py-0.5 rounded border border-[#1e293b]">
                Technical Health (0 → 100)
              </div>

              {/* Interactive Plotted Bubbles */}
              {items.map((app, idx) => {
                const coords = getAppCoordinates(app, idx);
                const leftPct = 8 + (coords.x / 100) * 84;
                const topPct = 92 - (coords.y / 100) * 84;

                const colorClasses =
                  app.disposition === 'Invest'
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400 shadow-emerald-500/20'
                    : app.disposition === 'Tolerate'
                    ? 'bg-sky-500/20 text-sky-300 border-sky-400 shadow-sky-500/20'
                    : app.disposition === 'Migrate'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-400 shadow-amber-500/20'
                    : 'bg-rose-500/20 text-rose-300 border-rose-400 shadow-rose-500/20';

                const sizePx = Math.max(34, Math.min(68, Math.round(Math.sqrt(app.annual_run_cost || 1000) * 0.18)));

                return (
                  <div
                    key={app.urn}
                    onClick={() => onSelectEntity(app.urn)}
                    onMouseEnter={() => setHoveredApp(app)}
                    onMouseLeave={() => setHoveredApp(null)}
                    style={{
                      left: `${leftPct}%`,
                      top: `${topPct}%`,
                      width: `${sizePx}px`,
                      height: `${sizePx}px`,
                    }}
                    className={`absolute -translate-x-1/2 -translate-y-1/2 rounded-full border-2 flex items-center justify-center cursor-pointer transition-all duration-200 hover:scale-125 hover:z-20 shadow-lg ${colorClasses}`}
                  >
                    <span className="text-[10px] font-bold truncate max-w-[85%] text-center leading-none">
                      {app.name.split('-')[0]}
                    </span>
                  </div>
                );
              })}

              {/* Floating Tooltip when hovering over a bubble */}
              {hoveredApp && (
                <div className="absolute top-4 right-4 z-30 p-3 rounded-lg bg-[#131b2e] border border-[#1e293b] shadow-2xl text-xs space-y-1 max-w-xs animate-in fade-in-50">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">{hoveredApp.name}</span>
                    <span
                      className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${
                        hoveredApp.disposition === 'Invest'
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : hoveredApp.disposition === 'Tolerate'
                          ? 'bg-sky-500/20 text-sky-400'
                          : hoveredApp.disposition === 'Migrate'
                          ? 'bg-amber-500/20 text-amber-400'
                          : 'bg-rose-500/20 text-rose-400'
                      }`}
                    >
                      {hoveredApp.disposition}
                    </span>
                  </div>
                  <div className="text-[11px] font-mono text-[#94a3b8] truncate">{hoveredApp.urn}</div>
                  <div className="grid grid-cols-2 gap-2 pt-1 border-t border-[#1e293b] text-[11px]">
                    <div>
                      <span className="text-[#94a3b8] block">Annual Spend</span>
                      <span className="font-bold text-white font-mono">
                        ${(hoveredApp.annual_run_cost / 1000).toFixed(1)}k/yr
                      </span>
                    </div>
                    <div>
                      <span className="text-[#94a3b8] block">Tech Debt</span>
                      <span className="font-bold text-white font-mono">{hoveredApp.tech_debt_score} / 100</span>
                    </div>
                  </div>
                  <div className="text-[10px] text-sky-400 font-medium pt-1">
                    Click to open Slide-Over Inspector Drawer →
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* VIEW B: STRUCTURED GRID TABLE */}
        {viewMode === 'table' && (
          <div className="space-y-4">
            <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
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
                    <th className="px-4 py-3 text-right">Action</th>
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
                      <tr
                        key={item.urn}
                        onClick={() => onSelectEntity(item.urn)}
                        className="hover:bg-[#1a233a] cursor-pointer transition"
                      >
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
        )}
      </div>

      {/* 3. LIFECYCLE HORIZONS & OBSOLESCENCE RISKS */}
      {lifecycleRisks.length > 0 && (
        <div
          className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
        >
          <div className="p-4 border-b border-[#1e293b]">
            <h3 className="text-sm font-bold text-white">Technology Obsolescence & Lifecycle Risk (EOL/EOS)</h3>
            <p className="text-xs text-[#94a3b8]">
              Automated tracking of End-of-Life horizons, callers, and financial exposure. Click to inspect asset in Drawer.
            </p>
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
                    <tr
                      key={risk.urn}
                      onClick={() => onSelectEntity(risk.urn)}
                      className="hover:bg-[#1a233a] cursor-pointer transition"
                    >
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
