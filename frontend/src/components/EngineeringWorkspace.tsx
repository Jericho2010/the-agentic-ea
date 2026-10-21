import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Layers,
  Network,
  Search,
  Filter,
  ExternalLink,
  MapPin,
  GitBranch,
  Database,
  ArrowRight,
  Maximize2,
  ChevronRight,
  Sparkles,
} from 'lucide-react';
import { MetamodelNode, MetamodelEdge, DiagramInfo } from '../types';

interface EngineeringWorkspaceProps {
  nodes: MetamodelNode[];
  edges: MetamodelEdge[];
  diagrams: DiagramInfo[];
  loading: boolean;
  onSelectEntity: (urn: string) => void;
}

export const EngineeringWorkspace: React.FC<EngineeringWorkspaceProps> = ({
  nodes,
  edges,
  diagrams,
  loading,
  onSelectEntity,
}) => {
  const [activeTab, setActiveTab] = useState<'diagrams' | 'graph'>('diagrams');
  const [selectedDiagram, setSelectedDiagram] = useState<string>('architecture-view.html');
  const [nodeSearch, setNodeSearch] = useState('');
  const [kindFilter, setKindFilter] = useState('ALL');
  const [domainFilter, setDomainFilter] = useState('ALL');

  useEffect(() => {
    if (diagrams.length > 0 && !selectedDiagram) {
      setSelectedDiagram(diagrams[0].name);
    }
  }, [diagrams, selectedDiagram]);

  const uniqueKinds = Array.from(new Set(nodes.map((n) => n.kind))).filter(Boolean);
  const uniqueDomains = Array.from(new Set(nodes.map((n) => n.domain || 'Core'))).filter(Boolean);

  const filteredNodes = nodes.filter((n) => {
    const matchesSearch =
      n.name.toLowerCase().includes(nodeSearch.toLowerCase()) ||
      n.urn.toLowerCase().includes(nodeSearch.toLowerCase());
    const matchesKind = kindFilter === 'ALL' || n.kind === kindFilter;
    const matchesDomain = domainFilter === 'ALL' || (n.domain || 'Core') === domainFilter;
    return matchesSearch && matchesKind && matchesDomain;
  });

  return (
    <div className="space-y-6">
      {/* Subtab Navigation Pills */}
      <div className="flex items-center justify-between border-b border-[#1e293b] pb-3">
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveTab('diagrams')}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'diagrams'
                ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                : 'text-[#94a3b8] hover:text-white hover:bg-[#131b2e]'
            }`}
          >
            <MapPin className="w-3.5 h-3.5" />
            <span>Living Architecture Maps ({diagrams.length})</span>
          </button>
          <button
            onClick={() => setActiveTab('graph')}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'graph'
                ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                : 'text-[#94a3b8] hover:text-white hover:bg-[#131b2e]'
            }`}
          >
            <Network className="w-3.5 h-3.5" />
            <span>Conformed PAM Metamodel Explorer ({nodes.length} CIs)</span>
          </button>
        </div>

        <div className="text-xs text-[#94a3b8] font-mono">
          Databricks Unity Catalog • ea.metamodel.*
        </div>
      </div>

      {/* VIEW 1: LIVING ARCHITECTURE MAPS (Archify Viewer) */}
      {activeTab === 'diagrams' && (
        <div className="space-y-4">
          {/* Floating Diagram Selector Pills */}
          <div
            className="ea-stat-card rounded-xl p-4 border flex flex-col lg:flex-row lg:items-center justify-between gap-3 shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            <div className="flex items-center space-x-3">
              <div className="p-2.5 rounded-lg bg-sky-500/10 text-sky-400 shrink-0">
                <Layers className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">Archify Living Architecture Viewer</h3>
                <p className="text-xs text-[#94a3b8]">
                  Select a live architectural perspective compiled from conformed graph telemetry
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <select
                value={selectedDiagram}
                onChange={(e) => setSelectedDiagram(e.target.value)}
                className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-lg text-white focus:outline-none focus:border-sky-500 max-w-[280px]"
              >
                {diagrams.map((d) => (
                  <option key={d.name} value={d.name}>
                    {d.title}
                  </option>
                ))}
              </select>

              <a
                href={`/api/diagrams/${selectedDiagram}`}
                target="_blank"
                rel="noreferrer"
                className="p-2 rounded-lg bg-[#0b0f19] text-[#94a3b8] hover:text-white border border-[#1e293b] hover:border-[#334155] transition flex items-center space-x-1 text-xs"
                title="Open diagram in standalone window"
              >
                <ExternalLink className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Fullscreen</span>
              </a>
            </div>
          </div>

          {/* Quick Perspective Filter Chips */}
          <div className="flex flex-wrap gap-2">
            {diagrams.slice(0, 6).map((d) => (
              <button
                key={d.name}
                onClick={() => setSelectedDiagram(d.name)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition border ${
                  selectedDiagram === d.name
                    ? 'bg-sky-500/20 text-sky-300 border-sky-500/50'
                    : 'bg-[#131b2e] text-[#94a3b8] border-[#1e293b] hover:text-white'
                }`}
              >
                {d.title}
              </button>
            ))}
          </div>

          {/* Embedded Diagram Canvas */}
          <div
            className="ea-stat-card rounded-xl border overflow-hidden shadow-2xl"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            {selectedDiagram ? (
              <iframe
                key={selectedDiagram}
                src={`/api/diagrams/${selectedDiagram}`}
                title="Archify Living Architecture Diagram"
                className="w-full h-[720px] border-none bg-[#080c14]"
                sandbox="allow-scripts allow-same-origin allow-popups"
              />
            ) : (
              <div className="h-[720px] flex items-center justify-center text-[#94a3b8] text-xs">
                Loading architecture diagram...
              </div>
            )}
          </div>
        </div>
      )}

      {/* VIEW 2: CONFORMED METAMODEL EXPLORER */}
      {activeTab === 'graph' && (
        <div className="space-y-4">
          {/* PAM Nodes Table */}
          <div
            className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-[#0d1322]/80">
              <div>
                <h3 className="text-sm font-bold text-white">Platform Architecture Metamodel (PAM) Nodes</h3>
                <p className="text-xs text-[#94a3b8]">
                  Click any entity to inspect in deep Slide-Over Drawer
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94a3b8]" />
                  <input
                    type="text"
                    placeholder="Search PAM entities..."
                    value={nodeSearch}
                    onChange={(e) => setNodeSearch(e.target.value)}
                    className="pl-8 pr-3 py-1.5 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white placeholder-[#94a3b8] focus:outline-none focus:border-sky-500"
                  />
                </div>
                <select
                  value={kindFilter}
                  onChange={(e) => setKindFilter(e.target.value)}
                  className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="ALL">All Kinds</option>
                  {uniqueKinds.map((k) => (
                    <option key={k} value={k}>
                      {k}
                    </option>
                  ))}
                </select>
                <select
                  value={domainFilter}
                  onChange={(e) => setDomainFilter(e.target.value)}
                  className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="ALL">All Domains</option>
                  {uniqueDomains.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="overflow-x-auto max-h-[480px]">
              <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
                <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
                  <tr>
                    <th className="px-4 py-3">Node Name</th>
                    <th className="px-4 py-3">Kind</th>
                    <th className="px-4 py-3">PAM URN</th>
                    <th className="px-4 py-3">Domain</th>
                    <th className="px-4 py-3">Lifecycle</th>
                    <th className="px-4 py-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
                  {filteredNodes.map((n) => (
                    <tr
                      key={n.urn}
                      onClick={() => onSelectEntity(n.urn)}
                      className="hover:bg-[#1a233a] cursor-pointer transition"
                    >
                      <td className="px-4 py-3 font-medium text-white">{n.name}</td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 text-[10px] rounded font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20">
                          {n.kind}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">{n.urn}</td>
                      <td className="px-4 py-3 text-[#94a3b8] text-xs">{n.domain || 'Core'}</td>
                      <td className="px-4 py-3 text-xs text-white">{n.lifecycle || 'Production'}</td>
                      <td className="px-4 py-3 text-right">
                        <span className="text-xs text-sky-400 hover:text-white font-medium flex items-center justify-end space-x-1">
                          <span>Inspect</span>
                          <ChevronRight className="w-3.5 h-3.5" />
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Realization Edges View */}
          <div
            className="ea-stat-card rounded-xl border overflow-hidden shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            <div className="p-4 border-b border-[#1e293b] bg-[#0d1322]/80">
              <h3 className="text-sm font-bold text-white">Metamodel Realization Edges ({edges.length})</h3>
              <p className="text-xs text-[#94a3b8]">Relationships stored in ea.metamodel.edges Delta table</p>
            </div>
            <div className="overflow-x-auto max-h-[350px]">
              <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
                <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
                  <tr>
                    <th className="px-4 py-3">Source Node</th>
                    <th className="px-4 py-3">Relationship</th>
                    <th className="px-4 py-3">Target Node</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
                  {edges.map((edge, idx) => (
                    <tr
                      key={idx}
                      onClick={() => onSelectEntity(edge.source_urn)}
                      className="hover:bg-[#1a233a] cursor-pointer transition"
                    >
                      <td className="px-4 py-3 font-mono text-[11px] text-white">{edge.source_urn}</td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 text-[10px] rounded font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {edge.relationship}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">{edge.target_urn}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
