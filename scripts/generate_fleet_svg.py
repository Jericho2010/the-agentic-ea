#!/usr/bin/env python3
"""
Generates a high-fidelity SVG illustration of the Fleet Architecture (10.4 Section 1).
Depicts:
1. Enterprise Git Provider & Cartographer Coordinator.
2. Herdr Multi-Worktree Fleet with worker panes, AST/IaC extractors, and schema gates.
3. Omnigent Batch Consolidation & Error Isolation.
4. Databricks Unity Catalog Atomic MERGE and Backstage Living Maps sync.
"""

def generate_svg() -> str:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="100%" height="100%" style="background:#090d16; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <!-- Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080c16"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#060911"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141d2f"/>
      <stop offset="100%" stop-color="#0d1424"/>
    </linearGradient>

    <linearGradient id="workerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#131e33"/>
      <stop offset="100%" stop-color="#0b1120"/>
    </linearGradient>

    <linearGradient id="flowDown" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#6366f1"/>
    </linearGradient>

    <linearGradient id="flowMerge" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>

    <linearGradient id="sqlBoxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050811"/>
      <stop offset="100%" stop-color="#0b101d"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="shadowLg" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000000" flood-opacity="0.55"/>
    </filter>

    <filter id="blueGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#38bdf8" flood-opacity="0.3"/>
    </filter>

    <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#10b981" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- BACKGROUND -->
  <rect width="1280" height="880" fill="url(#bgGrad)"/>

  <!-- SUBTLE ARCHITECTURE GRID -->
  <g opacity="0.035" stroke="#ffffff" stroke-width="1">
    <line x1="0" y1="80" x2="1280" y2="80"/>
    <line x1="0" y1="160" x2="1280" y2="160"/>
    <line x1="0" y1="240" x2="1280" y2="240"/>
    <line x1="0" y1="320" x2="1280" y2="320"/>
    <line x1="0" y1="400" x2="1280" y2="400"/>
    <line x1="0" y1="480" x2="1280" y2="480"/>
    <line x1="0" y1="560" x2="1280" y2="560"/>
    <line x1="0" y1="640" x2="1280" y2="640"/>
    <line x1="0" y1="720" x2="1280" y2="720"/>
    <line x1="0" y1="800" x2="1280" y2="800"/>
    
    <line x1="160" y1="0" x2="160" y2="880"/>
    <line x1="320" y1="0" x2="320" y2="880"/>
    <line x1="480" y1="0" x2="480" y2="880"/>
    <line x1="640" y1="0" x2="640" y2="880"/>
    <line x1="800" y1="0" x2="800" y2="880"/>
    <line x1="960" y1="0" x2="960" y2="880"/>
    <line x1="1120" y1="0" x2="1120" y2="880"/>
  </g>

  <!-- ========================================================================= -->
  <!-- HEADER & SYSTEM METRICS BANNER                                            -->
  <!-- ========================================================================= -->
  <g transform="translate(40, 24)">
    <!-- Title and Subtitle -->
    <text x="0" y="24" fill="#ffffff" font-size="20" font-weight="700" letter-spacing="0.5">AGENTIC EA • EVO 2 FLEET ARCHITECTURE</text>
    <text x="0" y="44" fill="#94a3b8" font-size="12">10.4 Concurrent Multi-Repo Cartography: Parallel Worktree Fleet &amp; Atomic Delta Lake Ingestion</text>

    <!-- Top Badges -->
    <g transform="translate(860, 4)">
      <rect x="0" y="0" width="130" height="26" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1"/>
      <circle cx="12" cy="13" r="3.5" fill="#38bdf8"/>
      <text x="22" y="17" fill="#cbd5e1" font-size="11" font-weight="600">PARALLEL FLEET</text>

      <rect x="140" y="0" width="100" height="26" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1"/>
      <circle cx="152" cy="13" r="3.5" fill="#10b981"/>
      <text x="162" y="17" fill="#cbd5e1" font-size="11" font-weight="600">-j$(nproc - 1)</text>

      <rect x="250" y="0" width="90" height="26" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1"/>
      <text x="295" y="17" text-anchor="middle" fill="#a78bfa" font-size="11" font-weight="600">512MB RAM</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 1. TOP TIER: DISCOVERY & COORDINATION PLANE                               -->
  <!-- ========================================================================= -->
  <g id="coordination_tier" transform="translate(40, 78)">
    <!-- Card 1: Enterprise Git Provider -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="460" height="96" rx="8" fill="url(#cardGrad)" stroke="#1e293b" stroke-width="1.5" filter="url(#shadowLg)"/>
      
      <g transform="translate(20, 18)">
        <rect x="0" y="0" width="28" height="28" rx="6" fill="#3b82f6" fill-opacity="0.2"/>
        <path d="M14,6 L22,14 L14,22 L6,14 Z" fill="#60a5fa"/>
        <text x="38" y="18" fill="#ffffff" font-size="14" font-weight="700">Enterprise Git Provider</text>
        <text x="240" y="18" fill="#64748b" font-size="11">GitHub / GitLab API</text>
        
        <text x="0" y="44" fill="#94a3b8" font-size="11.5">• 200+ Repositories in Enterprise Scope</text>
        <text x="0" y="62" fill="#94a3b8" font-size="11.5">• Active Delta Filter: <tspan fill="#38bdf8">Commits within last 24 hours</tspan></text>
      </g>
    </g>

    <!-- Connector: Git to Coordinator -->
    <g transform="translate(460, 48)">
      <line x1="0" y1="0" x2="80" y2="0" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 3"/>
      <polygon points="80,0 72,-4 72,4" fill="#38bdf8"/>
      <text x="40" y="-8" text-anchor="middle" fill="#38bdf8" font-size="10" font-weight="600">GET /repos</text>
    </g>

    <!-- Card 2: Cartographer Coordinator Agent -->
    <g transform="translate(540, 0)">
      <rect x="0" y="0" width="660" height="96" rx="8" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.5" filter="url(#blueGlow)"/>
      
      <g transform="translate(20, 18)">
        <rect x="0" y="0" width="28" height="28" rx="6" fill="#0284c7" fill-opacity="0.25"/>
        <circle cx="14" cy="14" r="7" stroke="#38bdf8" stroke-width="2" fill="none"/>
        <text x="38" y="18" fill="#ffffff" font-size="14" font-weight="700">Cartographer Coordinator Agent</text>
        <rect x="340" y="2" width="130" height="20" rx="10" fill="#1e293b"/>
        <text x="405" y="15" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="600">Omnigent Governed</text>

        <!-- Coordinator Bullet details -->
        <g transform="translate(0, 36)" font-size="11.5">
          <text y="8" fill="#cbd5e1">1. Partitions 200 repos into hardware-optimized concurrency batches (<tspan fill="#4ade80" font-weight="600">max workers = nproc - 1</tspan>)</text>
          <text y="28" fill="#cbd5e1">2. Enforces outbound Git API rate limiting (token cache avoids 5,000 req/hr ceiling)</text>
        </g>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- CONNECTOR TIER: DISPATCH TO WORKTREE FLEET                                 -->
  <!-- ========================================================================= -->
  <g transform="translate(640, 174)">
    <line x1="0" y1="0" x2="0" y2="40" stroke="url(#flowDown)" stroke-width="2.5" stroke-dasharray="5 3"/>
    <polygon points="0,44 -5,36 5,36" fill="#6366f1"/>
    <rect x="-140" y="12" width="280" height="20" rx="10" fill="#0b1120" stroke="#334155" stroke-width="1"/>
    <text x="0" y="26" text-anchor="middle" fill="#a78bfa" font-size="10.5" font-weight="600">Herdr Spawns Parallel Isolated Panes</text>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. MIDDLE TIER: HERDR MULTI-WORKTREE FLEET                                -->
  <!-- ========================================================================= -->
  <g id="fleet_tier" transform="translate(40, 224)">
    <!-- Outer Fleet Container Box -->
    <rect x="0" y="0" width="1200" height="276" rx="10" fill="#0b1120" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="6 4" filter="url(#shadowLg)"/>
    
    <!-- Container Header -->
    <g transform="translate(20, 16)">
      <rect x="0" y="0" width="360" height="24" rx="4" fill="#1e3a8a" fill-opacity="0.3" stroke="#2563eb" stroke-width="1"/>
      <text x="12" y="16" fill="#93c5fd" font-size="11" font-weight="700">HERDR MULTI-WORKTREE FLEET (RING 1/2 SANDBOXES)</text>
      <text x="380" y="16" fill="#64748b" font-size="11">Ephemeral tmpfs RAM disks • cgroups: 512MB RAM cap • Zero Residual Repo Pollution</text>
    </g>

    <!-- ==================== WORKER 1 CARD ==================== -->
    <g transform="translate(20, 50)">
      <rect x="0" y="0" width="370" height="206" rx="8" fill="url(#workerGrad)" stroke="#1e293b" stroke-width="1.2"/>
      
      <!-- Worker Header -->
      <g transform="translate(14, 14)">
        <circle cx="6" cy="6" r="4" fill="#10b981"/>
        <text x="16" y="9" fill="#ffffff" font-size="13" font-weight="700">Worker Pane #1</text>
        <text x="130" y="9" fill="#64748b" font-size="10.5" font-family="ui-monospace, monospace">pts/1 • PID 31024</text>
        <rect x="250" y="-3" width="90" height="18" rx="9" fill="#064e3b"/>
        <text x="295" y="9" text-anchor="middle" fill="#6ee7b7" font-size="9.5" font-weight="700">DONE (42ms)</text>
      </g>
      
      <!-- Target Repo & Worktree -->
      <g transform="translate(14, 42)" font-family="ui-monospace, monospace" font-size="10.5">
        <text y="0" fill="#94a3b8">Repo: <tspan fill="#38bdf8" font-weight="600">org/payments-api</tspan></text>
        <text y="18" fill="#94a3b8">Worktree: <tspan fill="#cbd5e1">/tmp/wt/p1 (tmpfs)</tspan></text>
      </g>

      <!-- Extractor Tasks -->
      <g transform="translate(14, 88)">
        <rect x="0" y="0" width="342" height="64" rx="6" fill="#080d18" stroke="#1e293b" stroke-width="1"/>
        <text x="10" y="18" fill="#64748b" font-size="9.5" font-weight="700" text-transform="uppercase">Sandboxed Extractors:</text>
        <text x="10" y="36" fill="#cbd5e1" font-size="11">• <tspan fill="#60a5fa">AST Parser:</tspan> pom.xml, Spring annotations</text>
        <text x="10" y="52" fill="#cbd5e1" font-size="11">• <tspan fill="#a78bfa">IaC Extractor:</tspan> main.tf (Postgres, SQS)</text>
      </g>

      <!-- Schema Validation Gate -->
      <g transform="translate(14, 166)">
        <rect x="0" y="0" width="342" height="26" rx="4" fill="#111f1a" stroke="#059669" stroke-width="1"/>
        <circle cx="12" cy="13" r="3.5" fill="#10b981"/>
        <text x="22" y="17" fill="#6ee7b7" font-size="10.5" font-weight="600">PAM Contract 1.1 Schema Validated ✓</text>
      </g>
    </g>

    <!-- ==================== WORKER 2 CARD ==================== -->
    <g transform="translate(415, 50)">
      <rect x="0" y="0" width="370" height="206" rx="8" fill="url(#workerGrad)" stroke="#1e293b" stroke-width="1.2"/>
      
      <!-- Worker Header -->
      <g transform="translate(14, 14)">
        <circle cx="6" cy="6" r="4" fill="#10b981"/>
        <text x="16" y="9" fill="#ffffff" font-size="13" font-weight="700">Worker Pane #2</text>
        <text x="130" y="9" fill="#64748b" font-size="10.5" font-family="ui-monospace, monospace">pts/2 • PID 31025</text>
        <rect x="250" y="-3" width="90" height="18" rx="9" fill="#064e3b"/>
        <text x="295" y="9" text-anchor="middle" fill="#6ee7b7" font-size="9.5" font-weight="700">DONE (38ms)</text>
      </g>
      
      <!-- Target Repo & Worktree -->
      <g transform="translate(14, 42)" font-family="ui-monospace, monospace" font-size="10.5">
        <text y="0" fill="#94a3b8">Repo: <tspan fill="#38bdf8" font-weight="600">org/auth-service</tspan></text>
        <text y="18" fill="#94a3b8">Worktree: <tspan fill="#cbd5e1">/tmp/wt/p2 (tmpfs)</tspan></text>
      </g>

      <!-- Extractor Tasks -->
      <g transform="translate(14, 88)">
        <rect x="0" y="0" width="342" height="64" rx="6" fill="#080d18" stroke="#1e293b" stroke-width="1"/>
        <text x="10" y="18" fill="#64748b" font-size="9.5" font-weight="700" text-transform="uppercase">Sandboxed Extractors:</text>
        <text x="10" y="36" fill="#cbd5e1" font-size="11">• <tspan fill="#60a5fa">AST Parser:</tspan> pyproject.toml, FastAPI endpoints</text>
        <text x="10" y="52" fill="#cbd5e1" font-size="11">• <tspan fill="#a78bfa">IaC Extractor:</tspan> k8s/deployment.yaml (Redis)</text>
      </g>

      <!-- Schema Validation Gate -->
      <g transform="translate(14, 166)">
        <rect x="0" y="0" width="342" height="26" rx="4" fill="#111f1a" stroke="#059669" stroke-width="1"/>
        <circle cx="12" cy="13" r="3.5" fill="#10b981"/>
        <text x="22" y="17" fill="#6ee7b7" font-size="10.5" font-weight="600">PAM Contract 1.1 Schema Validated ✓</text>
      </g>
    </g>

    <!-- ==================== WORKER N CARD ==================== -->
    <g transform="translate(810, 50)">
      <rect x="0" y="0" width="370" height="206" rx="8" fill="url(#workerGrad)" stroke="#1e293b" stroke-width="1.2"/>
      
      <!-- Worker Header -->
      <g transform="translate(14, 14)">
        <circle cx="6" cy="6" r="4" fill="#10b981"/>
        <text x="16" y="9" fill="#ffffff" font-size="13" font-weight="700">Worker Pane #N</text>
        <text x="130" y="9" fill="#64748b" font-size="10.5" font-family="ui-monospace, monospace">pts/8 • PID 31048</text>
        <rect x="250" y="-3" width="90" height="18" rx="9" fill="#064e3b"/>
        <text x="295" y="9" text-anchor="middle" fill="#6ee7b7" font-size="9.5" font-weight="700">DONE (51ms)</text>
      </g>
      
      <!-- Target Repo & Worktree -->
      <g transform="translate(14, 42)" font-family="ui-monospace, monospace" font-size="10.5">
        <text y="0" fill="#94a3b8">Repo: <tspan fill="#38bdf8" font-weight="600">org/inventory-svc</tspan></text>
        <text y="18" fill="#94a3b8">Worktree: <tspan fill="#cbd5e1">/tmp/wt/pn (tmpfs)</tspan></text>
      </g>

      <!-- Extractor Tasks -->
      <g transform="translate(14, 88)">
        <rect x="0" y="0" width="342" height="64" rx="6" fill="#080d18" stroke="#1e293b" stroke-width="1"/>
        <text x="10" y="18" fill="#64748b" font-size="9.5" font-weight="700" text-transform="uppercase">Sandboxed Extractors:</text>
        <text x="10" y="36" fill="#cbd5e1" font-size="11">• <tspan fill="#60a5fa">AST Parser:</tspan> go.mod, gRPC protobuf clients</text>
        <text x="10" y="52" fill="#cbd5e1" font-size="11">• <tspan fill="#a78bfa">IaC Extractor:</tspan> Helm charts, Kafka topics</text>
      </g>

      <!-- Schema Validation Gate -->
      <g transform="translate(14, 166)">
        <rect x="0" y="0" width="342" height="26" rx="4" fill="#111f1a" stroke="#059669" stroke-width="1"/>
        <circle cx="12" cy="13" r="3.5" fill="#10b981"/>
        <text x="22" y="17" fill="#6ee7b7" font-size="10.5" font-weight="600">PAM Contract 1.1 Schema Validated ✓</text>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. TRANSPORT & CONSOLIDATION LAYER                                        -->
  <!-- ========================================================================= -->
  <g id="aggregation_tier" transform="translate(40, 520)">
    <!-- Aggregator Card -->
    <rect x="180" y="0" width="840" height="60" rx="8" fill="#0e1726" stroke="#1e293b" stroke-width="1.2" filter="url(#shadowLg)"/>
    
    <!-- Three converge lines from workers -->
    <path d="M 205,-20 L 205,0" stroke="#10b981" stroke-width="2" stroke-dasharray="3 3"/>
    <path d="M 600,-20 L 600,0" stroke="#10b981" stroke-width="2" stroke-dasharray="3 3"/>
    <path d="M 995,-20 L 995,0" stroke="#10b981" stroke-width="2" stroke-dasharray="3 3"/>

    <g transform="translate(204, 18)">
      <circle cx="12" cy="12" r="4" fill="#38bdf8"/>
      <text x="26" y="16" fill="#ffffff" font-size="12" font-weight="700">Omnigent Batch Consolidation:</text>
      <text x="226" y="16" fill="#94a3b8" font-size="11.5">Streams Typed PAM Delta JSON (Nodes, Edges, Scopes)</text>
      <rect x="580" y="2" width="200" height="20" rx="4" fill="#1e293b"/>
      <text x="680" y="15" text-anchor="middle" fill="#f59e0b" font-size="10.5" font-weight="600">Fault Isolated: 0 Batch Halts</text>
    </g>
  </g>

  <!-- Flow line from Aggregator to Delta Lake -->
  <g transform="translate(640, 580)">
    <line x1="0" y1="0" x2="0" y2="40" stroke="url(#flowMerge)" stroke-width="2.5" stroke-dasharray="5 3"/>
    <polygon points="0,44 -5,36 5,36" fill="#06b6d4"/>
  </g>

  <!-- ========================================================================= -->
  <!-- 4. BOTTOM TIER: DATABRICKS UNITY CATALOG & BACKSTAGE                      -->
  <!-- ========================================================================= -->
  <g id="ingestion_tier" transform="translate(40, 634)">
    <!-- Container 1: Atomic Delta Lake Ingestion (Databricks Unity Catalog) -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="800" height="216" rx="10" fill="url(#cardGrad)" stroke="#059669" stroke-width="1.5" filter="url(#shadowLg)"/>
      
      <!-- Header -->
      <g transform="translate(20, 16)">
        <rect x="0" y="0" width="24" height="24" rx="4" fill="#059669" fill-opacity="0.3"/>
        <text x="7" y="16" fill="#34d399" font-size="12" font-weight="700">Δ</text>
        <text x="32" y="16" fill="#ffffff" font-size="14" font-weight="700">Atomic Delta Lake Ingestion</text>
        <text x="240" y="16" fill="#94a3b8" font-size="11.5">Databricks Unity Catalog (ea.metamodel.*)</text>
        
        <rect x="630" y="0" width="130" height="22" rx="11" fill="#064e3b" stroke="#059669" stroke-width="1"/>
        <text x="695" y="14" text-anchor="middle" fill="#6ee7b7" font-size="10.5" font-weight="700">ACID MERGE</text>
      </g>

      <!-- SQL Box -->
      <g transform="translate(20, 48)">
        <rect x="0" y="0" width="760" height="114" rx="6" fill="url(#sqlBoxGrad)" stroke="#1e293b" stroke-width="1"/>
        
        <g transform="translate(16, 20)" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="11">
          <text y="0" fill="#f43f5e">MERGE INTO <tspan fill="#ffffff">ea.metamodel.nodes</tspan> AS <tspan fill="#94a3b8">target</tspan></text>
          <text y="18" fill="#f43f5e">USING <tspan fill="#38bdf8">raw_extracted_batch</tspan> AS <tspan fill="#94a3b8">source</tspan></text>
          <text y="36" fill="#f43f5e">ON <tspan fill="#94a3b8">target.urn = source.urn</tspan></text>
          <text y="54" fill="#60a5fa">WHEN MATCHED THEN UPDATE SET <tspan fill="#cbd5e1">properties = source.props, last_scanned = NOW()</tspan></text>
          <text y="72" fill="#60a5fa">WHEN NOT MATCHED THEN INSERT <tspan fill="#cbd5e1">(urn, kind, name, lifecycle_status, properties) ...</tspan></text>
        </g>
      </g>

      <!-- Footer Info -->
      <g transform="translate(24, 178)" font-size="11" fill="#94a3b8">
        <text x="0" y="16">• <tspan fill="#34d399" font-weight="600">Active Services:</tspan> Marked with lifecycle_status = 'run'</text>
        <text x="360" y="16">• <tspan fill="#f59e0b" font-weight="600">Deleted Code:</tspan> Flagged as 'retired' via SCD2 history tracking</text>
      </g>
    </g>

    <!-- Connector: Unity Catalog to Backstage -->
    <g transform="translate(800, 108)">
      <line x1="0" y1="0" x2="40" y2="0" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 3"/>
      <polygon points="40,0 32,-4 32,4" fill="#38bdf8"/>
    </g>

    <!-- Container 2: Backstage Living Maps (Part 9 Integration) -->
    <g transform="translate(840, 0)">
      <rect x="0" y="0" width="360" height="216" rx="10" fill="url(#cardGrad)" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadowLg)"/>
      
      <!-- Header -->
      <g transform="translate(18, 16)">
        <polygon points="9,0 18,9 9,18 0,9" fill="#38bdf8"/>
        <text x="26" y="14" fill="#ffffff" font-size="14" font-weight="700">Backstage Living Maps</text>
        <text x="0" y="34" fill="#64748b" font-size="11">Real-Time Architecture Visualization</text>
      </g>

      <!-- Visual Node Mini Map -->
      <g transform="translate(18, 62)">
        <rect x="0" y="0" width="324" height="100" rx="6" fill="#080d1a" stroke="#1e293b" stroke-width="1"/>
        
        <!-- Nodes -->
        <rect x="14" y="24" width="80" height="28" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
        <text x="54" y="42" text-anchor="middle" fill="#93c5fd" font-size="9.5" font-weight="600">payments-api</text>

        <line x1="94" y1="38" x2="134" y2="38" stroke="#475569" stroke-width="1.5"/>

        <rect x="134" y="24" width="80" height="28" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1"/>
        <text x="174" y="42" text-anchor="middle" fill="#a7f3d0" font-size="9.5" font-weight="600">auth-service</text>

        <line x1="214" y1="38" x2="254" y2="38" stroke="#475569" stroke-width="1.5"/>

        <rect x="254" y="24" width="58" height="28" rx="4" fill="#1e293b" stroke="#a78bfa" stroke-width="1"/>
        <text x="283" y="42" text-anchor="middle" fill="#ddd6fe" font-size="9.5" font-weight="600">inv-svc</text>

        <text x="14" y="80" fill="#64748b" font-size="10">● Automated Lineage &amp; Blast Radius Graphs updated.</text>
      </g>

      <text x="18" y="194" fill="#38bdf8" font-size="11" font-weight="600">Sync completed across 200+ microservices.</text>
    </g>
  </g>
</svg>'''
    return svg

if __name__ == '__main__':
    svg_code = generate_svg()
    target_path = '/home/shaun/Projects/the-agentic-ea/assets/diagrams/fleet-architecture-mockup.svg'
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(svg_code)
    print(f"Generated {target_path} successfully ({len(svg_code)} bytes).")
