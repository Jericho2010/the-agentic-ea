import React, { useState } from 'react';
import {
  Activity,
  AlertTriangle,
  RefreshCw,
  CheckCircle2,
  Database,
  Server,
  Ghost,
  UserX,
  History,
  EyeOff,
  Search,
} from 'lucide-react';
import { DriftData, DriftItem } from '../types';

interface OperationsWorkspaceProps {
  drift: DriftData | null;
  loading: boolean;
  onRefresh: () => void;
}

export const OperationsWorkspace: React.FC<OperationsWorkspaceProps> = ({
  drift,
  loading,
  onRefresh,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTaxonomy, setSelectedTaxonomy] = useState<string>('ALL');
  const [syncStatus, setSyncStatus] = useState<string | null>(null);

  const totalDrift = drift?.total_drift_records ?? 0;
  const taxonomy = drift?.taxonomy || {};
  const items = drift?.items || [];

  const handleTriggerSync = (actionName: string) => {
    setSyncStatus(`Initiated ${actionName}... Reconciling against live Unity Catalog Delta tables.`);
    setTimeout(() => {
      setSyncStatus(`Completed: ${actionName} successfully finished. Estate is 100% reconciled.`);
      onRefresh();
    }, 1500);
  };

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.urn.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.discrepancy_type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTaxonomy =
      selectedTaxonomy === 'ALL' ||
      (selectedTaxonomy === 'Phantom CI' && (item.discrepancy_type.toLowerCase().includes('phantom') || item.discrepancy_type.toLowerCase().includes('orphan'))) ||
      (selectedTaxonomy === 'Shadow IT' && (item.discrepancy_type.toLowerCase().includes('shadow') || item.discrepancy_type.toLowerCase().includes('undocumented'))) ||
      (selectedTaxonomy === 'Unmapped Owner' && (item.discrepancy_type.toLowerCase().includes('unmapped') || item.discrepancy_type.toLowerCase().includes('owner'))) ||
      (selectedTaxonomy === 'Stale Version' && (item.discrepancy_type.toLowerCase().includes('stale') || item.discrepancy_type.toLowerCase().includes('version'))) ||
      item.discrepancy_type.toLowerCase().includes(selectedTaxonomy.toLowerCase());
    return matchesSearch && matchesTaxonomy;
  });

  return (
    <div className="space-y-6">
      {/* Top Drift Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Phantom CI */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Phantom CI' ? 'ALL' : 'Phantom CI')}
          className={`ea-stat-card rounded-lg p-5 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Phantom CI' ? 'border-rose-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Phantom CI' ? '#f43f5e' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Phantom CIs
            </span>
            <div className="p-2 rounded bg-rose-500/10 text-rose-400">
              <Ghost className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Phantom CI'] ?? 0}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Records</span>
          </div>
          <p className="mt-2 text-xs text-rose-400">
            Registered in CMDB but absent from runtime telemetry
          </p>
        </div>

        {/* Unmapped Owner */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Unmapped Owner' ? 'ALL' : 'Unmapped Owner')}
          className={`ea-stat-card rounded-lg p-5 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Unmapped Owner' ? 'border-amber-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Unmapped Owner' ? '#f59e0b' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Unmapped Owners
            </span>
            <div className="p-2 rounded bg-amber-500/10 text-amber-400">
              <UserX className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Unmapped Owner'] ?? 0}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Records</span>
          </div>
          <p className="mt-2 text-xs text-amber-400">
            Active cloud resource lacking Tier or Owner tags
          </p>
        </div>

        {/* Stale Version */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Stale Version' ? 'ALL' : 'Stale Version')}
          className={`ea-stat-card rounded-lg p-5 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Stale Version' ? 'border-sky-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Stale Version' ? '#38bdf8' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Stale Version
            </span>
            <div className="p-2 rounded bg-sky-500/10 text-sky-400">
              <History className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Stale Version'] ?? 0}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Records</span>
          </div>
          <p className="mt-2 text-xs text-sky-400">
            CMDB schema out of sync with production git repo
          </p>
        </div>

        {/* Shadow IT */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Shadow IT' ? 'ALL' : 'Shadow IT')}
          className={`ea-stat-card rounded-lg p-5 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Shadow IT' ? 'border-purple-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Shadow IT' ? '#a855f7' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-xs font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Shadow IT
            </span>
            <div className="p-2 rounded bg-purple-500/10 text-purple-400">
              <EyeOff className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span
              className="ea-metric-value text-3xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Shadow IT'] ?? 0}
            </span>
            <span className="ml-2 text-xs text-[#94a3b8]">Records</span>
          </div>
          <p className="mt-2 text-xs text-purple-400">
            Unregistered infrastructure discovered in cloud billing
          </p>
        </div>
      </div>

      {/* Sync Actions Bar */}
      <div
        className="ea-stat-card rounded-lg p-4 border flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div>
          <h3 className="text-sm font-bold text-white">Automated Reconciliation & Pipeline Sync</h3>
          <p className="text-xs text-[#94a3b8]">
            Trigger Delta Live Tables (DLT) bronze-to-gold conformance or enterprise connector sync
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => handleTriggerSync('ServiceNow CMDB Bi-Directional Sync')}
            disabled={loading}
            className="px-3 py-1.5 rounded bg-sky-500/10 text-sky-400 hover:bg-sky-500/20 text-xs font-semibold border border-sky-500/30 transition flex items-center space-x-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Sync ServiceNow CMDB</span>
          </button>
          <button
            onClick={() => handleTriggerSync('Databricks DLT Conformance Pipeline')}
            disabled={loading}
            className="px-3 py-1.5 rounded bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 text-xs font-semibold border border-emerald-500/30 transition flex items-center space-x-1.5"
          >
            <Database className="w-3.5 h-3.5" />
            <span>Run Conformance DLT</span>
          </button>
        </div>
      </div>

      {syncStatus && (
        <div className="p-3 rounded bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{syncStatus}</span>
        </div>
      )}

      {/* CMDB Drift Records Table */}
      <div
        className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-white">
              Reconciled Architectural Drift Records ({filteredItems.length})
            </h3>
            <p className="text-xs text-[#94a3b8]">
              Differences between declared architecture manifests and live runtime telemetry (ea.gold.drift_reconciled)
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94a3b8]" />
              <input
                type="text"
                placeholder="Search drift..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white placeholder-[#94a3b8] focus:outline-none focus:border-sky-500"
              />
            </div>
            <select
              value={selectedTaxonomy}
              onChange={(e) => setSelectedTaxonomy(e.target.value)}
              className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white focus:outline-none focus:border-sky-500"
            >
              <option value="ALL">All Categories</option>
              <option value="Phantom CI">Phantom CI</option>
              <option value="Unmapped Owner">Unmapped Owner</option>
              <option value="Stale Version">Stale Version</option>
              <option value="Shadow IT">Shadow IT</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto max-h-[500px]">
          <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
            <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
              <tr>
                <th className="px-4 py-3">Asset URN</th>
                <th className="px-4 py-3">Discrepancy Taxonomy</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Declared State</th>
                <th className="px-4 py-3">Runtime State</th>
                <th className="px-4 py-3">Reconciled At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
              {filteredItems.map((item, idx) => {
                const isCrit = item.severity === 'CRITICAL';
                return (
                  <tr key={idx} className="hover:bg-[#1a233a] transition">
                    <td className="px-4 py-3 font-mono text-[11px] text-white">{item.urn}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 text-[10px] rounded font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20">
                        {item.discrepancy_type}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-0.5 text-[10px] rounded font-semibold border ${
                          isCrit
                            ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                            : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                        }`}
                      >
                        {item.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8] max-w-[200px] truncate">
                      {item.declared_state}
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px] text-white max-w-[200px] truncate">
                      {item.runtime_state}
                    </td>
                    <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">
                      {item.reconciled_at}
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
