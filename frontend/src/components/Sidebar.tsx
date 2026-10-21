import React from 'react';
import {
  Layers,
  ShieldCheck,
  Cpu,
  Activity,
  ChevronLeft,
  ChevronRight,
  Database,
  Command,
  Server,
  Terminal,
} from 'lucide-react';
import { HealthInfo } from '../types';

export type WorkspaceType = 'executive' | 'governance' | 'engineering' | 'operations';

interface SidebarProps {
  activeWorkspace: WorkspaceType;
  onSelectWorkspace: (ws: WorkspaceType) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
  health: HealthInfo | null;
  onOpenCommandPalette: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeWorkspace,
  onSelectWorkspace,
  collapsed,
  onToggleCollapse,
  health,
  onOpenCommandPalette,
}) => {
  const isConnected = health?.cloud_connected ?? false;
  const warehouseId = health?.warehouse_id || 'df4dc09688caf6d8';
  const latency = health?.latency_ms ?? 0;

  const navItems: {
    id: WorkspaceType;
    label: string;
    sublabel: string;
    icon: React.ComponentType<{ className?: string }>;
  }[] = [
    {
      id: 'executive',
      label: 'Executive & Strategy',
      sublabel: '2D TIME Matrix & FinOps',
      icon: Layers,
    },
    {
      id: 'governance',
      label: 'Sentinel Governance',
      sublabel: 'Policies, PR Simulator & ARB',
      icon: ShieldCheck,
    },
    {
      id: 'engineering',
      label: 'Engineering Modernization',
      sublabel: 'PAM Metamodel & Living Maps',
      icon: Cpu,
    },
    {
      id: 'operations',
      label: 'Operations & FinOps',
      sublabel: 'CMDB Drift & Reconcile',
      icon: Activity,
    },
  ];

  return (
    <aside
      className={`bg-[#0d1322] border-r border-[#1e293b] flex flex-col justify-between transition-all duration-300 z-30 select-none ${
        collapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Top Brand & Workspace Switcher */}
      <div>
        {/* Brand Header */}
        <div className="h-14 border-b border-[#1e293b] px-4 flex items-center justify-between">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 shrink-0">
              <Layers className="w-4 h-4" />
            </div>
            {!collapsed && (
              <div className="overflow-hidden">
                <div className="flex items-center space-x-1.5">
                  <span className="text-xs font-bold text-white tracking-tight truncate">
                    The Agentic EA
                  </span>
                  <span className="text-[9px] px-1 py-0.2 rounded bg-sky-500/20 text-sky-400 font-mono font-semibold">
                    v1.0
                  </span>
                </div>
                <p className="text-[10px] text-[#94a3b8] truncate">Autonomous Architect</p>
              </div>
            )}
          </div>
          <button
            onClick={onToggleCollapse}
            className="p-1 rounded text-[#94a3b8] hover:text-white hover:bg-[#1a233a] transition"
            title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Environment / Estate Card */}
        {!collapsed ? (
          <div className="p-3 mx-3 my-3 rounded-lg bg-[#131b2e] border border-[#1e293b]">
            <div className="flex items-center justify-between text-[11px]">
              <span className="text-[#94a3b8] font-medium">Enterprise Estate</span>
              <span className="flex items-center space-x-1 text-emerald-400 text-[10px] font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Live UC</span>
              </span>
            </div>
            <div className="text-xs font-semibold text-white mt-1 truncate">
              Databricks Prod
            </div>
            <div className="text-[10px] text-[#94a3b8] font-mono truncate mt-0.5">
              {warehouseId} {latency > 0 ? `• ${latency.toFixed(0)}ms` : ''}
            </div>
          </div>
        ) : (
          <div className="flex justify-center my-3">
            <span
              className="w-2.5 h-2.5 rounded-full bg-emerald-400"
              title={`Connected (${warehouseId})`}
            />
          </div>
        )}

        {/* Nav Links */}
        <nav className="px-2 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeWorkspace === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectWorkspace(item.id)}
                className={`w-full flex items-center px-3 py-2.5 rounded-lg text-xs font-medium transition group ${
                  isActive
                    ? 'bg-sky-500/10 text-white border border-sky-500/30 font-semibold'
                    : 'text-[#94a3b8] hover:text-white hover:bg-[#131b2e]'
                }`}
                title={collapsed ? item.label : undefined}
              >
                <Icon
                  className={`w-4 h-4 shrink-0 transition ${
                    isActive ? 'text-sky-400' : 'text-[#94a3b8] group-hover:text-white'
                  }`}
                />
                {!collapsed && (
                  <div className="ml-3 text-left overflow-hidden">
                    <div className="truncate">{item.label}</div>
                    <div className="text-[10px] text-[#94a3b8] font-normal truncate">
                      {item.sublabel}
                    </div>
                  </div>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Sidebar Footer */}
      <div className="p-3 border-t border-[#1e293b] space-y-2">
        {/* Quick Command Trigger */}
        <button
          onClick={onOpenCommandPalette}
          className={`w-full flex items-center justify-between p-2 rounded-lg bg-[#131b2e] hover:bg-[#1a233a] border border-[#1e293b] text-xs text-[#94a3b8] hover:text-white transition ${
            collapsed ? 'justify-center' : ''
          }`}
          title="Quick Command Palette (⌘K)"
        >
          <div className="flex items-center space-x-2">
            <Command className="w-3.5 h-3.5 text-sky-400" />
            {!collapsed && <span>Command Palette</span>}
          </div>
          {!collapsed && (
            <kbd className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#0d1322] border border-[#334155] text-[#94a3b8]">
              ⌘K
            </kbd>
          )}
        </button>

        {!collapsed && (
          <div className="px-2 py-1 flex items-center justify-between text-[10px] text-[#94a3b8]">
            <span className="font-mono">Databricks SQL</span>
            <span className="text-emerald-400 font-mono">100% Real</span>
          </div>
        )}
      </div>
    </aside>
  );
};
