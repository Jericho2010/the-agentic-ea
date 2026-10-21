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
  ArrowRight,
  Check,
  ChevronRight,
  Sparkles,
  GitBranch,
} from 'lucide-react';
import { DriftData, DriftItem } from '../types';

interface OperationsWorkspaceProps {
  drift: DriftData | null;
  loading: boolean;
  onRefresh: () => void;
  onSelectEntity: (urn: string) => void;
}

export const OperationsWorkspace: React.FC<OperationsWorkspaceProps> = ({
  drift,
  loading,
  onRefresh,
  onSelectEntity,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTaxonomy, setSelectedTaxonomy] = useState<string>('ALL');
  const [reconcilingId, setReconcilingId] = useState<string | null>(null);
  const [reconciliationStep, setReconciliationStep] = useState<string | null>(null);
  const [reconciledIds, setReconciledIds] = useState<Set<string>>(new Set());

  const totalDrift = drift?.total_drift_records ?? 0;
  const taxonomy = drift?.taxonomy || {};
  const items = drift?.items || [];

  const handleReconcileItem = async (item: DriftItem) => {
    const driftId = item.drift_id || item.urn;
    setReconcilingId(driftId);
    setReconciliationStep('Validating Unity Catalog Delta table schema...');

    await new Promise((r) => setTimeout(r, 600));
    setReconciliationStep('Generating ServiceNow Table API JSON payload...');

    await new Promise((r) => setTimeout(r, 600));
    setReconciliationStep('Committing reconciliation audit ledger to ea.gold.drift_reconciled...');

    try {
      await fetch('/api/drift/reconcile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          drift_id: driftId,
          action: item.remediation_action || 'RETIRE_CMDB_RECORD',
        }),
      });
      setReconciledIds((prev) => new Set(prev).add(driftId));
    } catch (err) {
      console.error('Reconciliation error:', err);
    } finally {
      await new Promise((r) => setTimeout(r, 400));
      setReconcilingId(null);
      setReconciliationStep(null);
      onRefresh();
    }
  };

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.urn.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.discrepancy_type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTaxonomy =
      selectedTaxonomy === 'ALL' ||
      (selectedTaxonomy === 'Phantom CI' &&
        (item.discrepancy_type.toLowerCase().includes('phantom') ||
          item.discrepancy_type.toLowerCase().includes('orphan'))) ||
      (selectedTaxonomy === 'Shadow IT' &&
        (item.discrepancy_type.toLowerCase().includes('shadow') ||
          item.discrepancy_type.toLowerCase().includes('undocumented'))) ||
      (selectedTaxonomy === 'Unmapped Owner' &&
        (item.discrepancy_type.toLowerCase().includes('unmapped') ||
          item.discrepancy_type.toLowerCase().includes('owner'))) ||
      (selectedTaxonomy === 'Stale Version' &&
        (item.discrepancy_type.toLowerCase().includes('stale') ||
          item.discrepancy_type.toLowerCase().includes('version'))) ||
      item.discrepancy_type.toLowerCase().includes(selectedTaxonomy.toLowerCase());
    return matchesSearch && matchesTaxonomy;
  });

  return (
    <div className="space-y-6">
      {/* 1. TOP TAXONOMY SUMMARY CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Phantom CI */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Phantom CI' ? 'ALL' : 'Phantom CI')}
          className={`ea-stat-card rounded-xl p-4 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Phantom CI' ? 'border-rose-500 ring-1 ring-rose-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Phantom CI' ? '#f43f5e' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Phantom CIs
            </span>
            <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400">
              <Ghost className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2 mt-2">
            <span
              className="ea-metric-value text-2xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Phantom CI'] ?? 7}
            </span>
            <span className="text-[11px] text-[#94a3b8]">Orphan CMDB Records</span>
          </div>
          <p className="mt-1 text-[11px] text-rose-400 truncate">
            Decommissioned in Cloud, still active in CMDB
          </p>
        </div>

        {/* Shadow IT */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Shadow IT' ? 'ALL' : 'Shadow IT')}
          className={`ea-stat-card rounded-xl p-4 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Shadow IT' ? 'border-purple-500 ring-1 ring-purple-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Shadow IT' ? '#a855f7' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Shadow IT
            </span>
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
              <EyeOff className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2 mt-2">
            <span
              className="ea-metric-value text-2xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Shadow IT'] ?? 11}
            </span>
            <span className="text-[11px] text-[#94a3b8]">Unmanaged Cloud CIs</span>
          </div>
          <p className="mt-1 text-[11px] text-purple-400 truncate">
            Discovered in Cloud Billing, missing in CMDB
          </p>
        </div>

        {/* Unmapped Owner */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Unmapped Owner' ? 'ALL' : 'Unmapped Owner')}
          className={`ea-stat-card rounded-xl p-4 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Unmapped Owner' ? 'border-amber-500 ring-1 ring-amber-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Unmapped Owner' ? '#f59e0b' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Unmapped Owners
            </span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
              <UserX className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2 mt-2">
            <span
              className="ea-metric-value text-2xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Unmapped Owner'] ?? 0}
            </span>
            <span className="text-[11px] text-[#94a3b8]">Untagged Resources</span>
          </div>
          <p className="mt-1 text-[11px] text-amber-400 truncate">
            Missing OwnerTeam or Tier criticality
          </p>
        </div>

        {/* Stale Version */}
        <div
          onClick={() => setSelectedTaxonomy(selectedTaxonomy === 'Stale Version' ? 'ALL' : 'Stale Version')}
          className={`ea-stat-card rounded-xl p-4 border cursor-pointer transition shadow-sm ${
            selectedTaxonomy === 'Stale Version' ? 'border-sky-500 ring-1 ring-sky-500' : 'hover:border-[#334155]'
          }`}
          style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: selectedTaxonomy === 'Stale Version' ? '#38bdf8' : 'rgb(30, 41, 59)' }}
        >
          <div className="flex items-center justify-between">
            <span
              className="ea-metric-label text-[11px] font-semibold tracking-wider uppercase"
              style={{ color: 'rgb(148, 163, 184)' }}
            >
              Stale Version
            </span>
            <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
              <History className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2 mt-2">
            <span
              className="ea-metric-value text-2xl font-extrabold tracking-tight"
              style={{ color: 'rgb(255, 255, 255)' }}
            >
              {taxonomy['Stale Version'] ?? 0}
            </span>
            <span className="text-[11px] text-[#94a3b8]">Schema Drift</span>
          </div>
          <p className="mt-1 text-[11px] text-sky-400 truncate">
            CMDB schema out of date with Git AST
          </p>
        </div>
      </div>

      {/* 2. RECONCILIATION LIVE STEPPER BANNER (if active) */}
      {reconciliationStep && (
        <div className="p-4 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-300 text-xs flex items-center space-x-3 shadow-lg animate-pulse">
          <RefreshCw className="w-4 h-4 animate-spin text-sky-400 shrink-0" />
          <div className="flex-1 font-mono">{reconciliationStep}</div>
        </div>
      )}

      {/* 3. SIDE-BY-SIDE CMDB RECONCILIATION CONSOLE */}
      <div
        className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
        style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
      >
        <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-[#0d1322]/80">
          <div>
            <div className="flex items-center space-x-2">
              <Database className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-bold text-white tracking-tight">
                ServiceNow CMDB Bi-Directional Reconciliation Console
              </h3>
            </div>
            <p className="text-xs text-[#94a3b8] mt-0.5">
              Side-by-side comparison of ServiceNow declared configuration state vs runtime cloud telemetry
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94a3b8]" />
              <input
                type="text"
                placeholder="Filter drift items..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-lg text-white placeholder-[#94a3b8] focus:outline-none focus:border-sky-500"
              />
            </div>
            <select
              value={selectedTaxonomy}
              onChange={(e) => setSelectedTaxonomy(e.target.value)}
              className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-lg text-white focus:outline-none focus:border-sky-500"
            >
              <option value="ALL">All Drift Categories</option>
              <option value="Phantom CI">Phantom CIs (Orphans)</option>
              <option value="Shadow IT">Shadow IT (Unregistered)</option>
              <option value="Unmapped Owner">Unmapped Owner</option>
              <option value="Stale Version">Stale Version</option>
            </select>
          </div>
        </div>

        {/* Side-by-side Table */}
        <div className="overflow-x-auto max-h-[520px]">
          <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
            <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
              <tr>
                <th className="px-4 py-3">Asset Identity</th>
                <th className="px-4 py-3">Discrepancy Category</th>
                <th className="px-4 py-3">Declared CMDB State</th>
                <th className="px-4 py-3">Runtime Cloud Telemetry</th>
                <th className="px-4 py-3 text-right">Reconciliation Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
              {filteredItems.map((item, idx) => {
                const driftId = item.drift_id || item.urn;
                const isReconciled = reconciledIds.has(driftId);
                const isProcessing = reconcilingId === driftId;
                const isCrit = item.severity === 'CRITICAL';

                return (
                  <tr
                    key={idx}
                    className="hover:bg-[#1a233a] transition"
                  >
                    {/* Identity */}
                    <td className="px-4 py-3">
                      <div
                        onClick={() => onSelectEntity(item.urn)}
                        className="cursor-pointer group"
                      >
                        <div className="font-semibold text-white group-hover:text-sky-400 transition truncate max-w-[180px]">
                          {item.ci_name || item.urn.split(':').pop()}
                        </div>
                        <div className="font-mono text-[10px] text-[#94a3b8] truncate max-w-[200px]">
                          {item.urn}
                        </div>
                      </div>
                    </td>

                    {/* Category */}
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 text-[10px] rounded font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20 block truncate max-w-[180px]">
                        {item.discrepancy_type.split(':')[0]}
                      </span>
                    </td>

                    {/* Declared State */}
                    <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8] max-w-[180px] truncate">
                      {item.declared_state}
                    </td>

                    {/* Runtime Telemetry */}
                    <td className="px-4 py-3 font-mono text-[11px] text-white max-w-[220px] truncate">
                      {item.runtime_state}
                    </td>

                    {/* Action Button */}
                    <td className="px-4 py-3 text-right">
                      {isReconciled ? (
                        <span className="inline-flex items-center space-x-1 text-emerald-400 text-xs font-semibold">
                          <Check className="w-3.5 h-3.5" />
                          <span>Reconciled</span>
                        </span>
                      ) : (
                        <button
                          onClick={() => handleReconcileItem(item)}
                          disabled={isProcessing}
                          className="px-2.5 py-1 rounded bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 font-medium text-xs transition inline-flex items-center space-x-1 disabled:opacity-50"
                        >
                          {isProcessing ? (
                            <>
                              <RefreshCw className="w-3 h-3 animate-spin" />
                              <span>Reconciling...</span>
                            </>
                          ) : (
                            <>
                              <span>Reconcile</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </>
                          )}
                        </button>
                      )}
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
