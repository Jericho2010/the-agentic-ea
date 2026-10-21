import React from 'react';
import {
  Search,
  RefreshCw,
  Play,
  Database,
  User,
  GitPullRequest,
  CheckCircle2,
  ChevronRight,
} from 'lucide-react';
import { WorkspaceType } from './Sidebar';

interface TopNavProps {
  activeWorkspace: WorkspaceType;
  onOpenCommandPalette: () => void;
  onOpenSimulator: () => void;
  onTriggerReconciliation: () => void;
  onRefresh: () => void;
  loading: boolean;
}

export const TopNav: React.FC<TopNavProps> = ({
  activeWorkspace,
  onOpenCommandPalette,
  onOpenSimulator,
  onTriggerReconciliation,
  onRefresh,
  loading,
}) => {
  const workspaceLabels: Record<WorkspaceType, string> = {
    executive: 'Executive & Strategy',
    governance: 'Autonomous Governance & Compliance',
    engineering: 'Engineering Modernization',
    operations: 'Operations & FinOps',
  };

  return (
    <header className="h-14 border-b border-[#1e293b] bg-[#080c14]/90 backdrop-blur sticky top-0 z-20 flex items-center justify-between px-6">
      {/* Breadcrumbs */}
      <div className="flex items-center space-x-2 text-xs">
        <span className="text-[#94a3b8] hover:text-white transition cursor-pointer">
          Enterprise Estate
        </span>
        <ChevronRight className="w-3.5 h-3.5 text-[#94a3b8]" />
        <span className="text-white font-medium">{workspaceLabels[activeWorkspace]}</span>
      </div>

      {/* Center Search Input Trigger */}
      <div className="w-96 max-w-md">
        <button
          onClick={onOpenCommandPalette}
          className="w-full flex items-center justify-between px-3 py-1.5 rounded-lg bg-[#131b2e] border border-[#1e293b] hover:border-sky-500/40 text-xs text-[#94a3b8] hover:text-[#e2e8f0] transition shadow-inner"
        >
          <div className="flex items-center space-x-2">
            <Search className="w-3.5 h-3.5 text-sky-400" />
            <span>Search applications, PAM CIs, policies...</span>
          </div>
          <kbd className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#0d1322] border border-[#334155] text-[#94a3b8]">
            ⌘K
          </kbd>
        </button>
      </div>

      {/* Right Quick Actions */}
      <div className="flex items-center space-x-3">
        <button
          onClick={onOpenSimulator}
          className="px-2.5 py-1.5 rounded-lg bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 text-xs font-semibold transition flex items-center space-x-1.5"
          title="Simulate architectural PR diff"
        >
          <GitPullRequest className="w-3.5 h-3.5" />
          <span>Evaluate PR</span>
        </button>

        <button
          onClick={onTriggerReconciliation}
          className="px-2.5 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold transition flex items-center space-x-1.5"
          title="Reconcile ServiceNow CMDB with Cloud Telemetry"
        >
          <Database className="w-3.5 h-3.5" />
          <span>Sync CMDB</span>
        </button>

        <button
          onClick={onRefresh}
          disabled={loading}
          className="p-1.5 text-[#94a3b8] hover:text-white rounded-lg hover:bg-[#131b2e] transition border border-transparent hover:border-[#1e293b]"
          title="Refresh live Databricks estate"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-sky-400' : ''}`} />
        </button>

        <div className="h-4 w-px bg-[#1e293b]" />

        {/* User Role Badge */}
        <div className="flex items-center space-x-2 pl-1">
          <div className="w-7 h-7 rounded-full bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 text-xs font-bold">
            <User className="w-3.5 h-3.5" />
          </div>
          <div className="text-left hidden sm:block">
            <div className="text-xs font-bold text-white leading-tight">Principal EA</div>
            <div className="text-[10px] text-[#94a3b8] leading-tight">Global Architecture</div>
          </div>
        </div>
      </div>
    </header>
  );
};
