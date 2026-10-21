import React, { useState, useEffect, useCallback } from 'react';
import { Sidebar, WorkspaceType } from './components/Sidebar';
import { TopNav } from './components/TopNav';
import { ExecutiveWorkspace } from './components/ExecutiveWorkspace';
import { GovernanceWorkspace } from './components/GovernanceWorkspace';
import { EngineeringWorkspace } from './components/EngineeringWorkspace';
import { OperationsWorkspace } from './components/OperationsWorkspace';
import { EntityInspectorDrawer } from './components/EntityInspectorDrawer';
import { CommandPalette } from './components/CommandPalette';
import {
  HealthInfo,
  EstateStats,
  TimeMatrixData,
  GovernanceData,
  DriftData,
  MetamodelNode,
  MetamodelEdge,
  DiagramInfo,
} from './types';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const App: React.FC = () => {
  const [activeWorkspace, setActiveWorkspace] = useState<WorkspaceType>('executive');
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState<boolean>(false);
  const [selectedEntityUrn, setSelectedEntityUrn] = useState<string | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [health, setHealth] = useState<HealthInfo | null>(null);
  const [stats, setStats] = useState<EstateStats | null>(null);
  const [timeMatrix, setTimeMatrix] = useState<TimeMatrixData | null>(null);
  const [governance, setGovernance] = useState<GovernanceData | null>(null);
  const [drift, setDrift] = useState<DriftData | null>(null);
  const [nodes, setNodes] = useState<MetamodelNode[]>([]);
  const [edges, setEdges] = useState<MetamodelEdge[]>([]);
  const [diagrams, setDiagrams] = useState<DiagramInfo[]>([]);

  const fetchAllData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        resHealth,
        resStats,
        resTime,
        resGov,
        resDrift,
        resNodes,
        resEdges,
        resDiagrams,
      ] = await Promise.all([
        fetch('/api/health').then((r) => r.json()),
        fetch('/api/stats').then((r) => r.json()),
        fetch('/api/time-matrix').then((r) => r.json()),
        fetch('/api/governance/sentinel').then((r) => r.json()),
        fetch('/api/drift').then((r) => r.json()),
        fetch('/api/nodes').then((r) => r.json()),
        fetch('/api/edges').then((r) => r.json()),
        fetch('/api/diagrams').then((r) => r.json()),
      ]);

      setHealth(resHealth);
      setStats(resStats);
      setTimeMatrix(resTime);
      setGovernance(resGov);
      setDrift(resDrift);
      setNodes(resNodes.nodes || []);
      setEdges(resEdges.edges || []);
      setDiagrams(resDiagrams.diagrams || []);
    } catch (err: any) {
      console.error('Error fetching estate data:', err);
      setError(err?.message || 'Failed to fetch estate data from Databricks backend');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Global hotkeys (e.g. Cmd+K or /)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen((prev) => !prev);
      } else if (e.key === '/' && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="min-h-screen bg-[#080c14] text-[#e2e8f0] flex font-sans antialiased selection:bg-sky-500/30 selection:text-white">
      {/* 1. COLLAPSIBLE LEFT NAVIGATION SIDEBAR */}
      <Sidebar
        activeWorkspace={activeWorkspace}
        onSelectWorkspace={setActiveWorkspace}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed((prev) => !prev)}
        health={health}
        onOpenCommandPalette={() => setCommandPaletteOpen(true)}
      />

      {/* 2. MAIN APPLICATION CONTENT AREA */}
      <div className="flex-1 flex flex-col min-w-0 overflow-x-hidden">
        {/* Top Global Utility Bar */}
        <TopNav
          activeWorkspace={activeWorkspace}
          onOpenCommandPalette={() => setCommandPaletteOpen(true)}
          onOpenSimulator={() => setActiveWorkspace('governance')}
          onTriggerReconciliation={() => setActiveWorkspace('operations')}
          onRefresh={fetchAllData}
          loading={loading}
        />

        {/* Workspace Body */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-6 space-y-6">
          {error && (
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
              <button
                onClick={fetchAllData}
                className="px-2.5 py-1 rounded bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 font-medium transition"
              >
                Retry
              </button>
            </div>
          )}

          {activeWorkspace === 'executive' && (
            <ExecutiveWorkspace
              stats={stats}
              timeMatrix={timeMatrix}
              loading={loading}
              onSelectEntity={(urn) => setSelectedEntityUrn(urn)}
            />
          )}

          {activeWorkspace === 'governance' && (
            <GovernanceWorkspace
              governance={governance}
              loading={loading}
              onSelectEntity={(urn) => setSelectedEntityUrn(urn)}
            />
          )}

          {activeWorkspace === 'engineering' && (
            <EngineeringWorkspace
              nodes={nodes}
              edges={edges}
              diagrams={diagrams}
              loading={loading}
              onSelectEntity={(urn) => setSelectedEntityUrn(urn)}
            />
          )}

          {activeWorkspace === 'operations' && (
            <OperationsWorkspace
              drift={drift}
              loading={loading}
              onRefresh={fetchAllData}
              onSelectEntity={(urn) => setSelectedEntityUrn(urn)}
            />
          )}
        </main>

        {/* Sleek Minimal Footer */}
        <footer className="border-t border-[#1e293b] bg-[#0d1322] py-3 text-xs text-[#94a3b8]">
          <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-2">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-white">The Agentic EA Platform</span>
              <span>•</span>
              <span>Databricks Unity Catalog Delta</span>
              <span>•</span>
              <span className="font-mono text-[11px] text-[#94a3b8]">{health?.warehouse_id || 'df4dc09688caf6d8'}</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-emerald-400 font-medium">Enterprise SaaS v1.0</span>
              <kbd className="font-mono text-[10px] bg-[#131b2e] px-1.5 py-0.5 rounded border border-[#1e293b]">
                ⌘K Quick Command
              </kbd>
            </div>
          </div>
        </footer>
      </div>

      {/* 3. DEEP SLIDE-OVER ENTITY INSPECTOR DRAWER */}
      <EntityInspectorDrawer
        urn={selectedEntityUrn}
        onClose={() => setSelectedEntityUrn(null)}
        onSelectEntity={(newUrn) => setSelectedEntityUrn(newUrn)}
        onNavigateWorkspace={(ws) => setActiveWorkspace(ws as WorkspaceType)}
      />

      {/* 4. COMMAND PALETTE MODAL */}
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
        timeItems={timeMatrix?.items || []}
        nodes={nodes}
        driftItems={drift?.items || []}
        diagrams={diagrams}
        onSelectEntity={(urn) => setSelectedEntityUrn(urn)}
        onNavigateWorkspace={(ws) => setActiveWorkspace(ws as WorkspaceType)}
      />
    </div>
  );
};

export default App;
