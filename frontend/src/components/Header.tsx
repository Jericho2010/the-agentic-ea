import React from 'react';
import {
  LayoutDashboard,
  ShieldCheck,
  Cpu,
  Activity,
  Database,
  RefreshCw,
  Server,
  Layers,
} from 'lucide-react';
import { HealthInfo } from '../types';

export type WorkspaceType =
  | 'executive'
  | 'governance'
  | 'engineering'
  | 'operations';

interface HeaderProps {
  activeWorkspace: WorkspaceType;
  onSelectWorkspace: (ws: WorkspaceType) => void;
  health: HealthInfo | null;
  loading: boolean;
  onRefresh: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeWorkspace,
  onSelectWorkspace,
  health,
  loading,
  onRefresh,
}) => {
  const isConnected = health?.cloud_connected ?? false;
  const warehouseId = health?.warehouse_id || 'df4dc09688caf6d8';
  const latency = health?.latency_ms ?? 0;

  const tabs: { id: WorkspaceType; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: 'executive', label: 'Executive & Strategy', icon: LayoutDashboard },
    { id: 'governance', label: 'Autonomous Governance & Compliance', icon: ShieldCheck },
    { id: 'engineering', label: 'Engineering Modernization', icon: Cpu },
    { id: 'operations', label: 'Operations & FinOps', icon: Activity },
  ];

  return (
    <header className="border-b border-[#1e293b] bg-[#0b0f19]/90 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-base font-bold text-white tracking-tight">
                  The Agentic Enterprise Architect
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-[#1e293b] text-sky-400 font-mono font-medium border border-sky-500/20">
                  Navigator Cockpit
                </span>
              </div>
              <p className="text-xs text-[#94a3b8]">
                Databricks-Native Estate Intelligence, Sentinel Governance & Living Maps
              </p>
            </div>
          </div>

          {/* Connection Badge & Actions */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-md bg-[#131b2e] border border-[#1e293b]">
              <span className="relative flex h-2 w-2">
                {isConnected ? (
                  <>
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </>
                ) : (
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                )}
              </span>
              <div className="flex items-center space-x-1.5 text-xs">
                <span className="font-medium text-[#e2e8f0]">
                  {isConnected ? 'Connected' : 'Emulated Fallback'}
                </span>
                <span className="text-[#94a3b8] font-mono">({warehouseId})</span>
                {latency > 0 && (
                  <span className="text-emerald-400 font-mono text-[11px]">
                    {latency.toFixed(1)}ms
                  </span>
                )}
              </div>
            </div>

            <button
              onClick={onRefresh}
              disabled={loading}
              className="p-1.5 text-[#94a3b8] hover:text-white rounded-md hover:bg-[#131b2e] transition border border-transparent hover:border-[#1e293b] disabled:opacity-50"
              title="Refresh Estate Data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-sky-400' : ''}`} />
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-1 -mb-px">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeWorkspace === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onSelectWorkspace(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2.5 border-b-2 text-xs font-medium transition-all ${
                  isActive
                    ? 'border-sky-400 text-white bg-[#131b2e]/60'
                    : 'border-transparent text-[#94a3b8] hover:text-[#e2e8f0] hover:border-[#334155]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-[#94a3b8]'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
