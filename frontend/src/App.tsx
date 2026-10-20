import React, { useState, useEffect, useCallback } from 'react';
import { Header, WorkspaceType } from './components/Header';
import { ExecutiveWorkspace } from './components/ExecutiveWorkspace';
import { GovernanceWorkspace } from './components/GovernanceWorkspace';
import { EngineeringWorkspace } from './components/EngineeringWorkspace';
import { OperationsWorkspace } from './components/OperationsWorkspace';
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

  return (
    <div className="min-h-screen bg-[#0b0f19] text-[#e2e8f0] flex flex-col font-sans">
      <Header
        activeWorkspace={activeWorkspace}
        onSelectWorkspace={setActiveWorkspace}
        health={health}
        loading={loading}
        onRefresh={fetchAllData}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {error && (
          <div className="mb-6 p-4 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center justify-between">
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
          <ExecutiveWorkspace stats={stats} timeMatrix={timeMatrix} loading={loading} />
        )}

        {activeWorkspace === 'governance' && (
          <GovernanceWorkspace governance={governance} loading={loading} />
        )}

        {activeWorkspace === 'engineering' && (
          <EngineeringWorkspace
            nodes={nodes}
            edges={edges}
            diagrams={diagrams}
            loading={loading}
          />
        )}

        {activeWorkspace === 'operations' && (
          <OperationsWorkspace drift={drift} loading={loading} onRefresh={fetchAllData} />
        )}
      </main>

      <footer className="border-t border-[#1e293b] bg-[#0b0f19] py-4 text-xs text-[#94a3b8]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-white">The Agentic EA Platform</span>
            <span>|</span>
            <span>Databricks Unity Catalog Delta Backbone</span>
            <span>|</span>
            <span className="font-mono text-[11px]">Warehouse: {health?.warehouse_id || 'df4dc09688caf6d8'}</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-emerald-400 font-medium">Enterprise Modernization Active</span>
            <span>v1.0.0</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
