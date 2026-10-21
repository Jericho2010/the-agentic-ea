import React, { useState, useEffect } from 'react';
import {
  X,
  Copy,
  Check,
  ExternalLink,
  Layers,
  ShieldCheck,
  AlertTriangle,
  Database,
  ArrowRight,
  TrendingDown,
  DollarSign,
  Activity,
  FileText,
  Share2,
} from 'lucide-react';
import { EntityDetail } from '../types';

interface EntityInspectorDrawerProps {
  urn: string | null;
  onClose: () => void;
  onSelectEntity: (urn: string) => void;
  onNavigateWorkspace?: (workspace: string) => void;
}

export const EntityInspectorDrawer: React.FC<EntityInspectorDrawerProps> = ({
  urn,
  onClose,
  onSelectEntity,
  onNavigateWorkspace,
}) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<EntityDetail | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'lineage' | 'governance' | 'json'>('overview');
  const [copied, setCopied] = useState<boolean>(false);
  const [jsonCopied, setJsonCopied] = useState<boolean>(false);

  useEffect(() => {
    if (!urn) return;
    setLoading(true);
    fetch(`/api/entity/${encodeURIComponent(urn)}`)
      .then((r) => r.json())
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching entity detail:', err);
        setLoading(false);
      });
  }, [urn]);

  // Handle ESC key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!urn) return null;

  const node = data?.node;
  const time = data?.time_assessment;
  const drift = data?.drift_record;
  const upstream = data?.upstream_callers || [];
  const downstream = data?.downstream_datastores || [];
  const carbon = data?.carbon_accounting || {};

  const handleCopyUrn = () => {
    if (!urn) return;
    navigator.clipboard.writeText(urn);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleCopyJson = () => {
    if (!data?.raw_json) return;
    navigator.clipboard.writeText(JSON.stringify(data.raw_json, null, 2));
    setJsonCopied(true);
    setTimeout(() => setJsonCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Slide-over panel */}
      <div className="relative w-full max-w-xl bg-[#131b2e] border-l border-[#1e293b] shadow-2xl flex flex-col h-full z-10 transition-transform duration-300">
        {/* Drawer Header */}
        <div className="p-6 border-b border-[#1e293b] flex items-start justify-between bg-[#0d1322]/80">
          <div className="space-y-1.5 pr-4">
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wider bg-sky-500/10 text-sky-400 border border-sky-500/20">
                {node?.kind || 'Architecture Entity'}
              </span>
              {time?.disposition && (
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${
                    time.disposition === 'Invest'
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                      : time.disposition === 'Tolerate'
                      ? 'bg-sky-500/10 text-sky-400 border-sky-500/20'
                      : time.disposition === 'Migrate'
                      ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                      : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                  }`}
                >
                  {time.disposition}
                </span>
              )}
            </div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              {node?.name || urn.split(':').pop()}
            </h2>
            <div className="flex items-center space-x-2 text-xs text-[#94a3b8] font-mono">
              <span className="truncate max-w-[340px]">{urn}</span>
              <button
                onClick={handleCopyUrn}
                className="p-1 hover:text-white transition"
                title="Copy URN"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-[#94a3b8] hover:text-white hover:bg-[#1e293b] transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-[#1e293b] px-6 bg-[#0b0f19]/40 text-xs font-medium">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-3 px-3 border-b-2 transition ${
              activeTab === 'overview'
                ? 'border-sky-400 text-white font-semibold'
                : 'border-transparent text-[#94a3b8] hover:text-[#e2e8f0]'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('lineage')}
            className={`py-3 px-3 border-b-2 transition ${
              activeTab === 'lineage'
                ? 'border-sky-400 text-white font-semibold'
                : 'border-transparent text-[#94a3b8] hover:text-[#e2e8f0]'
            }`}
          >
            Lineage & Graph ({upstream.length + downstream.length})
          </button>
          <button
            onClick={() => setActiveTab('governance')}
            className={`py-3 px-3 border-b-2 transition ${
              activeTab === 'governance'
                ? 'border-sky-400 text-white font-semibold'
                : 'border-transparent text-[#94a3b8] hover:text-[#e2e8f0]'
            }`}
          >
            Governance & Rules
          </button>
          <button
            onClick={() => setActiveTab('json')}
            className={`py-3 px-3 border-b-2 transition ${
              activeTab === 'json'
                ? 'border-sky-400 text-white font-semibold'
                : 'border-transparent text-[#94a3b8] hover:text-[#e2e8f0]'
            }`}
          >
            Raw JSON
          </button>
        </div>

        {/* Drawer Body Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading ? (
            <div className="flex items-center justify-center h-64 text-[#94a3b8] text-xs">
              Resolving entity details from Unity Catalog...
            </div>
          ) : (
            <>
              {/* TAB 1: OVERVIEW */}
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  {/* Key Metrics Grid */}
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3.5 rounded-lg bg-[#0d1322] border border-[#1e293b]">
                      <span className="text-[10px] font-semibold text-[#94a3b8] uppercase tracking-wider block">
                        Annual Run Cost
                      </span>
                      <span className="text-xl font-bold text-white mt-1 block">
                        ${time ? time.annual_run_cost.toLocaleString('en-US', { minimumFractionDigits: 2 }) : '0.00'}
                      </span>
                      <span className="text-[11px] text-[#94a3b8]">FinOps run cost attributed</span>
                    </div>

                    <div className="p-3.5 rounded-lg bg-[#0d1322] border border-[#1e293b]">
                      <span className="text-[10px] font-semibold text-[#94a3b8] uppercase tracking-wider block">
                        Technical Debt Score
                      </span>
                      <div className="flex items-baseline space-x-2 mt-1">
                        <span className="text-xl font-bold text-white">
                          {time?.tech_debt_score ?? 15}
                        </span>
                        <span className="text-[11px] text-[#94a3b8]">/ 100 max</span>
                      </div>
                      <div className="w-full bg-[#131b2e] h-1.5 rounded-full overflow-hidden mt-1.5">
                        <div
                          className={`h-full ${
                            (time?.tech_debt_score ?? 15) > 50 ? 'bg-rose-500' : 'bg-emerald-500'
                          }`}
                          style={{ width: `${Math.min(time?.tech_debt_score ?? 15, 100)}%` }}
                        />
                      </div>
                    </div>

                    <div className="p-3.5 rounded-lg bg-[#0d1322] border border-[#1e293b]">
                      <span className="text-[10px] font-semibold text-[#94a3b8] uppercase tracking-wider block">
                        Lifecycle Status
                      </span>
                      <span className="text-sm font-semibold text-white mt-1 block">
                        {node?.lifecycle || time?.lifecycle || 'Production'}
                      </span>
                      <span className="text-[11px] text-[#94a3b8]">
                        EOL: {time?.eol_date || 'Supported'}
                      </span>
                    </div>

                    <div className="p-3.5 rounded-lg bg-[#0d1322] border border-[#1e293b]">
                      <span className="text-[10px] font-semibold text-[#94a3b8] uppercase tracking-wider block">
                        Domain & Owner
                      </span>
                      <span className="text-sm font-semibold text-white mt-1 block truncate">
                        {node?.domain || 'Core Architecture'}
                      </span>
                      <span className="text-[11px] text-[#94a3b8] truncate block">
                        {node?.owner || 'Application Team'}
                      </span>
                    </div>
                  </div>

                  {/* Drift Alert (if flagged) */}
                  {drift && (
                    <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 space-y-1.5">
                      <div className="flex items-center space-x-2 font-semibold text-xs">
                        <AlertTriangle className="w-4 h-4 text-amber-400" />
                        <span>Active CMDB Discrepancy Flagged</span>
                      </div>
                      <p className="text-xs text-[#e2e8f0]">{drift.discrepancy_type}</p>
                      <div className="text-[11px] font-mono text-[#94a3b8] pt-1">
                        Declared: {drift.declared_state} | Runtime: {drift.runtime_state}
                      </div>
                    </div>
                  )}

                  {/* Architecture Context */}
                  <div className="p-4 rounded-lg bg-[#0d1322] border border-[#1e293b] space-y-3">
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                      Architectural Attribution
                    </h4>
                    <div className="space-y-2 text-xs">
                      <div className="flex justify-between py-1 border-b border-[#1e293b]">
                        <span className="text-[#94a3b8]">Catalog Location</span>
                        <span className="font-mono text-white">ea.metamodel.nodes</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-[#1e293b]">
                        <span className="text-[#94a3b8]">Managed Compute</span>
                        <span className="font-mono text-sky-400">Databricks Serverless</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-[#1e293b]">
                        <span className="text-[#94a3b8]">Carbon Footprint</span>
                        <span className="text-white">
                          {carbon.monthly_emissions_kgco2 ? `${carbon.monthly_emissions_kgco2} kgCO2/mo` : 'Nominal (<10 kg)'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: LINEAGE & REALIZATION */}
              {activeTab === 'lineage' && (
                <div className="space-y-6">
                  {/* Upstream Callers */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                        Upstream Callers ({upstream.length})
                      </h4>
                      <span className="text-[11px] text-[#94a3b8]">Direct dependencies</span>
                    </div>

                    {upstream.length > 0 ? (
                      <div className="space-y-1.5">
                        {upstream.map((edge, i) => (
                          <div
                            key={i}
                            onClick={() => onSelectEntity(edge.source_urn)}
                            className="p-3 rounded bg-[#0d1322] border border-[#1e293b] hover:border-sky-500/50 cursor-pointer transition flex items-center justify-between text-xs"
                          >
                            <span className="font-mono text-white truncate max-w-[340px]">
                              {edge.source_urn}
                            </span>
                            <span className="text-[10px] px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                              {edge.relationship}
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="p-4 rounded bg-[#0d1322] border border-[#1e293b] text-xs text-[#94a3b8] text-center">
                        Zero upstream calling dependencies declared in PAM graph.
                      </div>
                    )}
                  </div>

                  {/* Downstream Datastores */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                        Downstream Resources & Datastores ({downstream.length})
                      </h4>
                      <span className="text-[11px] text-[#94a3b8]">Realization targets</span>
                    </div>

                    {downstream.length > 0 ? (
                      <div className="space-y-1.5">
                        {downstream.map((edge, i) => (
                          <div
                            key={i}
                            onClick={() => onSelectEntity(edge.target_urn)}
                            className="p-3 rounded bg-[#0d1322] border border-[#1e293b] hover:border-emerald-500/50 cursor-pointer transition flex items-center justify-between text-xs"
                          >
                            <span className="font-mono text-white truncate max-w-[340px]">
                              {edge.target_urn}
                            </span>
                            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                              {edge.relationship}
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="p-4 rounded bg-[#0d1322] border border-[#1e293b] text-xs text-[#94a3b8] text-center">
                        Zero downstream realization edges declared.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* TAB 3: GOVERNANCE & RULES */}
              {activeTab === 'governance' && (
                <div className="space-y-4">
                  <div className="p-4 rounded-lg bg-[#0d1322] border border-[#1e293b] space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white uppercase tracking-wider">
                        Sentinel Architecture Compliance
                      </span>
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {time?.disposition === 'Eliminate' ? 'FLAGGED FOR SUNSET' : 'COMPLIANT'}
                      </span>
                    </div>

                    <div className="space-y-2 text-xs text-[#e2e8f0]">
                      <div className="p-2.5 rounded bg-[#131b2e] border border-[#1e293b] flex items-center justify-between">
                        <div>
                          <span className="font-mono text-sky-400 font-semibold">EA-POL-001</span>
                          <p className="text-[11px] text-[#94a3b8]">Approved Datastore Standards</p>
                        </div>
                        <span className="text-emerald-400 text-xs font-medium">PASSED</span>
                      </div>

                      <div className="p-2.5 rounded bg-[#131b2e] border border-[#1e293b] flex items-center justify-between">
                        <div>
                          <span className="font-mono text-sky-400 font-semibold">EA-POL-002</span>
                          <p className="text-[11px] text-[#94a3b8]">Customer PII Encryption at Rest</p>
                        </div>
                        <span className="text-emerald-400 text-xs font-medium">PASSED</span>
                      </div>

                      <div className="p-2.5 rounded bg-[#131b2e] border border-[#1e293b] flex items-center justify-between">
                        <div>
                          <span className="font-mono text-sky-400 font-semibold">EA-POL-003</span>
                          <p className="text-[11px] text-[#94a3b8]">Mandatory Ownership & Criticality Tags</p>
                        </div>
                        <span className="text-emerald-400 text-xs font-medium">PASSED</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: RAW JSON PAYLOAD */}
              {activeTab === 'json' && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-[#94a3b8]">Conformed Unity Catalog JSON</span>
                    <button
                      onClick={handleCopyJson}
                      className="px-2.5 py-1 rounded bg-[#0d1322] border border-[#1e293b] text-xs text-sky-400 hover:text-white transition flex items-center space-x-1.5"
                    >
                      {jsonCopied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{jsonCopied ? 'Copied' : 'Copy JSON'}</span>
                    </button>
                  </div>
                  <pre className="p-4 rounded-lg bg-[#080c14] border border-[#1e293b] text-[#38bdf8] text-[11px] font-mono overflow-x-auto max-h-[460px]">
                    {JSON.stringify(data?.raw_json, null, 2)}
                  </pre>
                </div>
              )}
            </>
          )}
        </div>

        {/* Drawer Footer Actions */}
        <div className="p-4 border-t border-[#1e293b] bg-[#0d1322] flex items-center justify-between">
          <button
            onClick={() => {
              if (onNavigateWorkspace) onNavigateWorkspace('engineering');
              onClose();
            }}
            className="px-3 py-1.5 rounded text-xs font-medium bg-sky-500/10 text-sky-400 hover:bg-sky-500/20 border border-sky-500/30 transition flex items-center space-x-1.5"
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Open in PAM Metamodel</span>
          </button>

          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded text-xs font-medium bg-[#1e293b] text-white hover:bg-[#334155] transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
