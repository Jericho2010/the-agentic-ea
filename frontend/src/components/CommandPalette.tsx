import React, { useState, useEffect, useRef } from 'react';
import {
  Search,
  Command,
  Layers,
  ShieldCheck,
  Cpu,
  Activity,
  FileCode,
  MapPin,
  X,
  ArrowRight,
} from 'lucide-react';
import { TimeItem, MetamodelNode, DriftItem, DiagramInfo } from '../types';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  timeItems: TimeItem[];
  nodes: MetamodelNode[];
  driftItems: DriftItem[];
  diagrams: DiagramInfo[];
  onSelectEntity: (urn: string) => void;
  onNavigateWorkspace: (ws: string) => void;
}

interface SearchResult {
  id: string;
  category: string;
  title: string;
  subtitle?: string;
  icon: React.ComponentType<{ className?: string }>;
  action: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  timeItems,
  nodes,
  driftItems,
  diagrams,
  onSelectEntity,
  onNavigateWorkspace,
}) => {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      } else if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Build searchable items
  const results: SearchResult[] = [];

  // Workspaces quick links
  if (!query || 'executive strategy time'.includes(query.toLowerCase())) {
    results.push({
      id: 'ws-exec',
      category: 'Workspace',
      title: 'Executive & Strategy (TIME Model)',
      icon: Layers,
      action: () => onNavigateWorkspace('executive'),
    });
  }
  if (!query || 'governance sentinel arb policy'.includes(query.toLowerCase())) {
    results.push({
      id: 'ws-gov',
      category: 'Workspace',
      title: 'Autonomous Governance & Compliance (Sentinel)',
      icon: ShieldCheck,
      action: () => onNavigateWorkspace('governance'),
    });
  }
  if (!query || 'engineering modernization pam metamodel maps'.includes(query.toLowerCase())) {
    results.push({
      id: 'ws-eng',
      category: 'Workspace',
      title: 'Engineering Modernization (Archify Living Maps)',
      icon: Cpu,
      action: () => onNavigateWorkspace('engineering'),
    });
  }
  if (!query || 'operations finops cmdb drift reconcile'.includes(query.toLowerCase())) {
    results.push({
      id: 'ws-ops',
      category: 'Workspace',
      title: 'Operations & FinOps (CMDB Drift Resolution)',
      icon: Activity,
      action: () => onNavigateWorkspace('operations'),
    });
  }

  // Filter applications
  timeItems
    .filter(
      (a) =>
        a.name.toLowerCase().includes(query.toLowerCase()) ||
        a.urn.toLowerCase().includes(query.toLowerCase()) ||
        a.disposition.toLowerCase().includes(query.toLowerCase())
    )
    .slice(0, 5)
    .forEach((app) => {
      results.push({
        id: `app-${app.urn}`,
        category: 'Application',
        title: `${app.name} (${app.disposition})`,
        subtitle: `$${(app.annual_run_cost / 1000).toFixed(1)}k/yr • ${app.urn}`,
        icon: FileCode,
        action: () => onSelectEntity(app.urn),
      });
    });

  // Filter PAM nodes
  nodes
    .filter(
      (n) =>
        n.name.toLowerCase().includes(query.toLowerCase()) ||
        n.urn.toLowerCase().includes(query.toLowerCase()) ||
        n.kind.toLowerCase().includes(query.toLowerCase())
    )
    .slice(0, 4)
    .forEach((n) => {
      results.push({
        id: `node-${n.urn}`,
        category: 'PAM Node',
        title: `${n.name} [${n.kind}]`,
        subtitle: n.urn,
        icon: Cpu,
        action: () => onSelectEntity(n.urn),
      });
    });

  // Filter Diagrams
  diagrams
    .filter((d) => d.title.toLowerCase().includes(query.toLowerCase()))
    .slice(0, 3)
    .forEach((d) => {
      results.push({
        id: `diag-${d.name}`,
        category: 'Archify Diagram',
        title: d.title,
        subtitle: d.name,
        icon: MapPin,
        action: () => onNavigateWorkspace('engineering'),
      });
    });

  const handleSelect = (idx: number) => {
    if (results[idx]) {
      results[idx].action();
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20">
      <div
        className="fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      <div className="relative w-full max-w-xl bg-[#131b2e] border border-[#1e293b] rounded-xl shadow-2xl overflow-hidden z-10 animate-in fade-in-0 zoom-in-95">
        {/* Search Input Bar */}
        <div className="p-4 border-b border-[#1e293b] flex items-center space-x-3 bg-[#0d1322]">
          <Search className="w-5 h-5 text-sky-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Search applications, PAM nodes, policies, living maps... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'ArrowDown') {
                e.preventDefault();
                setSelectedIndex((prev) => (prev + 1) % results.length);
              } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                setSelectedIndex((prev) => (prev - 1 + results.length) % results.length);
              } else if (e.key === 'Enter') {
                e.preventDefault();
                handleSelect(selectedIndex);
              }
            }}
            className="w-full bg-transparent text-sm text-white placeholder-[#94a3b8] focus:outline-none"
          />
          <kbd className="px-2 py-0.5 rounded text-[10px] font-mono bg-[#1e293b] text-[#94a3b8] border border-[#334155]">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 divide-y divide-[#1e293b]/50">
          {results.length > 0 ? (
            results.map((item, idx) => {
              const Icon = item.icon;
              const isSelected = selectedIndex === idx;
              return (
                <div
                  key={item.id}
                  onClick={() => handleSelect(idx)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`p-3 rounded-lg cursor-pointer transition flex items-center justify-between text-xs ${
                    isSelected ? 'bg-sky-500/10 text-white' : 'text-[#e2e8f0] hover:bg-[#1a233a]'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div
                      className={`p-1.5 rounded ${
                        isSelected ? 'bg-sky-500/20 text-sky-400' : 'bg-[#0d1322] text-[#94a3b8]'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-white">{item.title}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#1e293b] text-[#94a3b8] font-mono">
                          {item.category}
                        </span>
                      </div>
                      {item.subtitle && (
                        <p className="text-[11px] text-[#94a3b8] font-mono mt-0.5">{item.subtitle}</p>
                      )}
                    </div>
                  </div>
                  <ArrowRight
                    className={`w-3.5 h-3.5 transition ${isSelected ? 'text-sky-400 translate-x-0.5' : 'text-transparent'}`}
                  />
                </div>
              );
            })
          ) : (
            <div className="p-8 text-center text-xs text-[#94a3b8]">
              No matching architectural entities found for "{query}".
            </div>
          )}
        </div>

        {/* Footer shortcuts */}
        <div className="px-4 py-2 border-t border-[#1e293b] bg-[#0d1322] flex items-center justify-between text-[11px] text-[#94a3b8]">
          <div className="flex items-center space-x-3">
            <span>
              <kbd className="font-mono bg-[#1e293b] px-1.5 py-0.5 rounded">↑↓</kbd> to navigate
            </span>
            <span>
              <kbd className="font-mono bg-[#1e293b] px-1.5 py-0.5 rounded">↵</kbd> to select
            </span>
          </div>
          <span>The Agentic EA • Fast Entity Jump</span>
        </div>
      </div>
    </div>
  );
};
