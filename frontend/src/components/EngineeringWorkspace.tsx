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
} from 'lucide-react';
import { MetamodelNode, MetamodelEdge, DiagramInfo } from '../types';

interface EngineeringWorkspaceProps {
  nodes: MetamodelNode[];
  edges: MetamodelEdge[];
  diagrams: DiagramInfo[];
  loading: boolean;
}

export const EngineeringWorkspace: React.FC<EngineeringWorkspaceProps> = ({
  nodes,
  edges,
  diagrams,
  loading,
}) => {
  const [activeTab, setActiveTab] = useState<'graph' | 'diagrams'>('diagrams');
  const [selectedDiagram, setSelectedDiagram] = useState<string>('architecture-view.html');
  const [nodeSearch, setNodeSearch] = useState('');
  const [kindFilter, setKindFilter] = useState('ALL');

  useEffect(() => {
    if (diagrams.length > 0 && !selectedDiagram) {
      setSelectedDiagram(diagrams[0].name);
    }
  }, [diagrams, selectedDiagram]);

  const uniqueKinds = Array.from(new Set(nodes.map((n) => n.kind))).filter(Boolean);

  const filteredNodes = nodes.filter((n) => {
    const matchesSearch =
      n.name.toLowerCase().includes(nodeSearch.toLowerCase()) ||
      n.urn.toLowerCase().includes(nodeSearch.toLowerCase());
    const matchesKind = kindFilter === 'ALL' || n.kind === kindFilter;
    return matchesSearch && matchesKind;
  });

  return (
    <div className="space-y-6">
      {/* Subtab Navigation */}
      <div className="flex items-center justify-between border-b border-[#1e293b] pb-3">
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveTab('diagrams')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'diagrams'
                ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                : 'text-[#94a3b8] hover:text-white hover:bg-[#131b2e]'
            }`}
          >
            <MapPin className="w-3.5 h-3.5" />
            <span>Living Architecture Maps</span>
          </button>
          <button
            onClick={() => setActiveTab('graph')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-semibold transition ${
              activeTab === 'graph'
                ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                : 'text-[#94a3b8] hover:text-white hover:bg-[#131b2e]'
            }`}
          >
            <Network className="w-3.5 h-3.5" />
            <span>Conformed PAM Metamodel Explorer</span>
          </button>
        </div>

        <div className="text-xs text-[#94a3b8] font-mono">
          {nodes.length} Nodes | {edges.length} Edges | {diagrams.length} Diagrams
        </div>
      </div>

      {/* VIEW 1: LIVING ARCHITECTURE MAPS */}
      {activeTab === 'diagrams' && (
        <div className="space-y-4">
          <div
            className="ea-stat-card rounded-lg p-4 border flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded bg-sky-500/10 text-sky-400">
                <Layers className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">Archify Living Architecture Viewer</h3>
                <p className="text-xs text-[#94a3b8]">
                  Deterministic living diagrams compiled from conformed Unity Catalog graph models
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <label className="text-xs text-[#94a3b8]">Select Diagram:</label>
              <select
                value={selectedDiagram}
                onChange={(e) => setSelectedDiagram(e.target.value)}
                className="py-1.5 px-3 text-xs bg-[#0b0f19] border border-[#1e293b] rounded-md text-white focus:outline-none focus:border-sky-500 max-w-[280px]"
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
                className="p-1.5 rounded bg-[#0b0f19] text-[#94a3b8] hover:text-white border border-[#1e293b] hover:border-[#334155] transition"
                title="Open diagram in new tab"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Embedded Diagram Iframe */}
          <div
            className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            {selectedDiagram ? (
              <iframe
                key={selectedDiagram}
                src={`/api/diagrams/${selectedDiagram}`}
                title="Archify Living Architecture Diagram"
                className="w-full h-[680px] border-none bg-[#0b0f19]"
                sandbox="allow-scripts allow-same-origin allow-popups"
              />
            ) : (
              <div className="h-[680px] flex items-center justify-center text-[#94a3b8]">
                Loading diagram...
              </div>
            )}
          </div>
        </div>
      )}

      {/* VIEW 2: CONFORMED PAM METAMODEL EXPLORER */}
      {activeTab === 'graph' && (
        <div className="space-y-4">
          <div
            className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            <div className="p-4 border-b border-[#1e293b] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-bold text-white">Platform Architecture Metamodel (PAM) Nodes</h3>
                <p className="text-xs text-[#94a3b8]">Conformed entities stored in ea.metamodel.nodes Delta table</p>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94a3b8]" />
                  <input
                    type="text"
                    placeholder="Search nodes..."
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
              </div>
            </div>

            <div className="overflow-x-auto max-h-[500px]">
              <table className="min-w-full divide-y divide-[#1e293b] text-left text-xs">
                <thead className="bg-[#0b0f19]/70 text-[#94a3b8] uppercase font-semibold text-[11px] sticky top-0 z-10 backdrop-blur">
                  <tr>
                    <th className="px-4 py-3">Node Name</th>
                    <th className="px-4 py-3">Kind</th>
                    <th className="px-4 py-3">PAM URN</th>
                    <th className="px-4 py-3">Domain</th>
                    <th className="px-4 py-3">Lifecycle</th>
                    <th className="px-4 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e293b] text-[#e2e8f0]">
                  {filteredNodes.map((n) => (
                    <tr key={n.urn} className="hover:bg-[#1a233a] transition">
                      <td className="px-4 py-3 font-medium text-white">{n.name}</td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 text-[10px] rounded font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20">
                          {n.kind}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-[11px] text-[#94a3b8]">{n.urn}</td>
                      <td className="px-4 py-3 text-[#94a3b8] text-xs">{n.domain || 'Core'}</td>
                      <td className="px-4 py-3 text-xs text-white">{n.lifecycle || 'Production'}</td>
                      <td className="px-4 py-3">
                        <span className="text-emerald-400 text-xs font-medium">Active</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Realization Edges View */}
          <div
            className="ea-stat-card rounded-lg border overflow-hidden shadow-sm"
            style={{ backgroundColor: 'rgb(19, 27, 46)', borderColor: 'rgb(30, 41, 59)' }}
          >
            <div className="p-4 border-b border-[#1e293b]">
              <h3 className="text-sm font-bold text-white">Metamodel Realization Edges</h3>
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
                  {edges.slice(0, 50).map((edge, idx) => (
                    <tr key={idx} className="hover:bg-[#1a233a] transition">
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
