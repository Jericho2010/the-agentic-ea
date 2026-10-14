#!/usr/bin/env python3
"""
Generates a high-fidelity SVG illustration of the Collaborative Co-Driving in Backstage interaction model.
Depicts:
1. Backstage Browser Operating Cockpit with Slide-Out Copilot Drawer.
2. Terminal thought stream with prompt detection.
3. Interactive one-click action buttons.
4. Bi-directional WebSocket keystroke bridge.
5. Omnigent Sandbox Container with Herdr PTY Multiplexer and Ephemeral Git Worktree.
"""

def generate_svg() -> str:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="100%" height="100%" style="background:#090d16; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <!-- Gradients -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19"/>
      <stop offset="50%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#070a12"/>
    </linearGradient>
    
    <linearGradient id="browserChrome" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1f2937"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="drawerBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141c2e"/>
      <stop offset="100%" stop-color="#0d1322"/>
    </linearGradient>

    <linearGradient id="btnPrimaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>

    <linearGradient id="btnSecondaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#243046"/>
      <stop offset="100%" stop-color="#1a2234"/>
    </linearGradient>

    <linearGradient id="bridgeLineUp" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>

    <linearGradient id="bridgeLineDown" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>

    <linearGradient id="sandboxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e1726"/>
      <stop offset="100%" stop-color="#080e1a"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.6"/>
    </filter>

    <filter id="drawerGlow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="-6" dy="0" stdDeviation="12" flood-color="#38bdf8" flood-opacity="0.25"/>
    </filter>

    <filter id="btnGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#3b82f6" flood-opacity="0.4"/>
    </filter>

    <filter id="amberGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#f59e0b" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- BACKGROUND -->
  <rect width="1280" height="880" fill="url(#bgGrad)"/>
  
  <!-- SUBTLE GRID -->
  <g opacity="0.04" stroke="#ffffff" stroke-width="1">
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
  <!-- 1. BACKSTAGE OPERATING COCKPIT (BROWSER CONTAINER)                         -->
  <!-- ========================================================================= -->
  <g id="backstage_browser" transform="translate(40, 24)">
    <!-- Browser Frame Outer Window -->
    <rect x="0" y="0" width="1200" height="520" rx="12" fill="#131b2a" stroke="#253349" stroke-width="1.5" filter="url(#cardShadow)"/>
    
    <!-- Title Bar / Chrome -->
    <path d="M0,12 Q0,0 12,0 L1188,0 Q1200,0 1200,12 L1200,42 L0,42 Z" fill="url(#browserChrome)"/>
    
    <!-- Traffic lights -->
    <circle cx="22" cy="21" r="6" fill="#ef4444"/>
    <circle cx="40" cy="21" r="6" fill="#f59e0b"/>
    <circle cx="58" cy="21" r="6" fill="#10b981"/>
    
    <!-- URL Bar -->
    <rect x="180" y="8" width="840" height="26" rx="6" fill="#0b0f17" stroke="#1f2937" stroke-width="1"/>
    <text x="600" y="25" text-anchor="middle" fill="#9ca3af" font-size="12" font-family="ui-monospace, monospace">
      <tspan fill="#38bdf8">https://</tspan>backstage.databricks.corp/catalog/services/payments-service <tspan fill="#4ade80">(Databricks Apps • Auth Active)</tspan>
    </text>
    
    <!-- Environment Pill -->
    <rect x="1040" y="9" width="130" height="24" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1"/>
    <circle cx="1052" cy="21" r="3.5" fill="#10b981"/>
    <text x="1062" y="25" fill="#cbd5e1" font-size="11" font-weight="600">PROD-DATABRICKS</text>

    <!-- Navigation Header Inside Backstage -->
    <g transform="translate(0, 42)">
      <rect x="0" y="0" width="1200" height="50" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
      
      <!-- Brand Logo -->
      <g transform="translate(24, 14)">
        <polygon points="11,0 22,11 11,22 0,11" fill="#38bdf8"/>
        <text x="32" y="16" fill="#ffffff" font-size="16" font-weight="700" letter-spacing="0.5">AGENTIC EA</text>
        <rect x="140" y="2" width="60" height="18" rx="4" fill="#3b82f6" fill-opacity="0.2"/>
        <text x="170" y="15" text-anchor="middle" fill="#60a5fa" font-size="10" font-weight="700">EVO 2</text>
      </g>
      
      <!-- Nav Tabs -->
      <g transform="translate(260, 16)">
        <!-- Tab 1: Software Catalog (Active) -->
        <text x="0" y="14" fill="#38bdf8" font-size="13" font-weight="600">Software Catalog</text>
        <rect x="0" y="22" width="108" height="2.5" fill="#38bdf8"/>
        
        <!-- Tab 2: Living Architecture Maps -->
        <text x="140" y="14" fill="#94a3b8" font-size="13" font-weight="500">Living Architecture Maps</text>
        
        <!-- Tab 3: Waiver Action Inbox -->
        <text x="330" y="14" fill="#94a3b8" font-size="13" font-weight="500">Waiver Action Inbox</text>
        <circle cx="468" cy="10" r="8" fill="#ef4444"/>
        <text x="468" y="13.5" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="700">2</text>
        
        <!-- Tab 4: TIME Standards -->
        <text x="500" y="14" fill="#94a3b8" font-size="13" font-weight="500">TIME Standards</text>
      </g>

      <!-- User Info -->
      <g transform="translate(1040, 12)">
        <circle cx="14" cy="14" r="14" fill="#334155"/>
        <text x="14" y="18" text-anchor="middle" fill="#93c5fd" font-size="12" font-weight="700">EA</text>
        <text x="36" y="18" fill="#e2e8f0" font-size="12" font-weight="500">S. Principal Architect</text>
      </g>
    </g>

    <!-- ===================================================================== -->
    <!-- LEFT PANEL: DIMMED BACKSTAGE SERVICE VIEW (Contextual Background)    -->
    <!-- ===================================================================== -->
    <g transform="translate(24, 108)" opacity="0.45">
      <!-- Service Title Banner -->
      <text x="0" y="24" fill="#ffffff" font-size="22" font-weight="700">payments-service</text>
      <rect x="180" y="6" width="60" height="20" rx="4" fill="#1e293b"/>
      <text x="210" y="20" text-anchor="middle" fill="#94a3b8" font-size="11">Service</text>
      
      <rect x="250" y="6" width="90" height="20" rx="4" fill="#1e293b"/>
      <text x="295" y="20" text-anchor="middle" fill="#10b981" font-size="11">Tier 1 Critical</text>

      <!-- Service Metadata Cards -->
      <g transform="translate(0, 44)">
        <rect x="0" y="0" width="160" height="64" rx="6" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
        <text x="14" y="22" fill="#64748b" font-size="10" font-weight="600" text-transform="uppercase">Owner Team</text>
        <text x="14" y="44" fill="#e2e8f0" font-size="13" font-weight="600">Core Checkout</text>

        <rect x="176" y="0" width="160" height="64" rx="6" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
        <text x="190" y="22" fill="#64748b" font-size="10" font-weight="600" text-transform="uppercase">Repository</text>
        <text x="190" y="44" fill="#e2e8f0" font-size="13" font-weight="600">github.com/org/pay</text>

        <rect x="352" y="0" width="140" height="64" rx="6" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
        <text x="366" y="22" fill="#64748b" font-size="10" font-weight="600" text-transform="uppercase">Catalog Graph</text>
        <text x="366" y="44" fill="#f59e0b" font-size="13" font-weight="600">14 Edges (Warn)</text>
      </g>

      <!-- Dependency Graph Preview Box -->
      <g transform="translate(0, 126)">
        <rect x="0" y="0" width="492" height="230" rx="8" fill="#0b0f19" stroke="#1e293b" stroke-width="1"/>
        <text x="16" y="24" fill="#94a3b8" font-size="12" font-weight="600">Topology &amp; Lineage (Unity Catalog PAM Graph)</text>
        
        <!-- Nodes -->
        <rect x="24" y="60" width="110" height="40" rx="6" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="79" y="84" text-anchor="middle" fill="#cbd5e1" font-size="11">checkout-web</text>
        
        <line x1="134" y1="80" x2="180" y2="80" stroke="#475569" stroke-width="1.5" stroke-dasharray="3 3"/>
        
        <rect x="180" y="60" width="120" height="40" rx="6" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5"/>
        <text x="240" y="84" text-anchor="middle" fill="#93c5fd" font-size="11" font-weight="600">payments-svc</text>
        
        <line x1="300" y1="80" x2="350" y2="80" stroke="#ef4444" stroke-width="1.5"/>
        
        <rect x="350" y="55" width="124" height="50" rx="6" fill="#450a0a" stroke="#ef4444" stroke-width="1.5"/>
        <text x="412" y="78" text-anchor="middle" fill="#fca5a5" font-size="11" font-weight="700">Cassandra 3.11</text>
        <text x="412" y="94" text-anchor="middle" fill="#ef4444" font-size="9" font-weight="700">TIME: Phase-Out [!]</text>
        
        <!-- Legend note -->
        <text x="24" y="150" fill="#64748b" font-size="11">● Unity Catalog PAM Graph identifies 14 downstream data edges.</text>
        <text x="24" y="172" fill="#64748b" font-size="11">● Flagged Violation: Cassandra 3.11 violates Golden Standard S02.</text>
      </g>
    </g>

    <!-- ===================================================================== -->
    <!-- RIGHT PANEL: SLIDE-OUT COPILOT DRAWER (HERO FEATURE)                  -->
    <!-- ===================================================================== -->
    <g id="slide_out_drawer" transform="translate(540, 92)" filter="url(#drawerGlow)">
      <!-- Drawer Background with Elevated Border -->
      <rect x="0" y="0" width="640" height="412" rx="10" fill="url(#drawerBg)" stroke="#38bdf8" stroke-width="1.5"/>
      
      <!-- Drawer Header Bar -->
      <g transform="translate(20, 16)">
        <!-- Sparkle Icon -->
        <rect x="0" y="0" width="28" height="28" rx="6" fill="#3b82f6" fill-opacity="0.2"/>
        <path d="M14,6 L16,11 L21,14 L16,17 L14,22 L12,17 L7,14 L12,11 Z" fill="#38bdf8"/>
        
        <text x="38" y="18" fill="#ffffff" font-size="15" font-weight="700">Slide-Out Copilot Drawer</text>
        <text x="220" y="18" fill="#64748b" font-size="12">| Session #copilot-4891</text>
        
        <!-- Status Pill: BLOCKED (Awaiting Input) -->
        <g transform="translate(420, 0)">
          <rect x="0" y="0" width="180" height="26" rx="13" fill="#451a03" stroke="#f59e0b" stroke-width="1" filter="url(#amberGlow)"/>
          <circle cx="14" cy="13" r="4" fill="#f59e0b"/>
          <text x="26" y="17" fill="#fbbf24" font-size="10.5" font-weight="700" letter-spacing="0.3">AWAITING INPUT (BLOCKED)</text>
        </g>
      </g>
      
      <!-- Latency and Transport Banner -->
      <g transform="translate(20, 52)">
        <rect x="0" y="0" width="600" height="24" rx="4" fill="#0b1120" stroke="#1e293b" stroke-width="1"/>
        <circle cx="12" cy="12" r="3" fill="#10b981"/>
        <text x="22" y="16" fill="#94a3b8" font-size="11">
          Connected via <tspan fill="#38bdf8" font-weight="600">WebSocket Keystroke Relay</tspan> to Herdr Sandbox (Latency: 2ms • Zero SSH Required)
        </text>
      </g>

      <!-- TERMINAL THOUGHT STREAM BOX -->
      <g transform="translate(20, 84)">
        <rect x="0" y="0" width="600" height="210" rx="8" fill="#070a13" stroke="#1e293b" stroke-width="1"/>
        
        <!-- Terminal Header dots -->
        <rect x="0" y="0" width="600" height="24" rx="8" fill="#0f172a"/>
        <circle cx="14" cy="12" r="3.5" fill="#334155"/>
        <circle cx="26" cy="12" r="3.5" fill="#334155"/>
        <circle cx="38" cy="12" r="3.5" fill="#334155"/>
        <text x="56" y="16" fill="#64748b" font-size="10.5" font-family="ui-monospace, monospace">live agent stream [stdout]</text>

        <!-- Monospace Output Lines -->
        <g transform="translate(16, 42)" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="11.5">
          <!-- Line 1 -->
          <text y="0" fill="#64748b">[10:14:02] <tspan fill="#38bdf8" font-weight="600">&gt; Agent:</tspan> <tspan fill="#e2e8f0">Analyzing blast radius for 'payments-service' v2.4...</tspan></text>
          
          <!-- Line 2 -->
          <text y="20" fill="#64748b">[10:14:04] <tspan fill="#38bdf8" font-weight="600">&gt; Agent:</tspan> <tspan fill="#e2e8f0">Querying Unity Catalog PAM graph: 14 downstream edges mapped.</tspan></text>
          
          <!-- Line 3 -->
          <text y="40" fill="#64748b">[10:14:05] <tspan fill="#f87171" font-weight="600">&gt; Agent:</tspan> <tspan fill="#fca5a5">Detected unapproved database protocol: Cassandra 3.11</tspan></text>
          
          <!-- Separator Line -->
          <line x1="0" y1="56" x2="568" y2="56" stroke="#334155" stroke-dasharray="3 3"/>
          
          <!-- Prompt Card Inside Terminal -->
          <rect x="-4" y="66" width="576" height="88" rx="6" fill="#1c1917" stroke="#b45309" stroke-width="1.2"/>
          <text x="8" y="86" fill="#fbbf24" font-weight="700">[!] QUESTION FOR ARCHITECT (Input Trigger Detected):</text>
          <text x="8" y="106" fill="#fef3c7">Cassandra 3.11 is marked as 'Phase-Out' under TIME standard S02.</text>
          <text x="8" y="126" fill="#fef3c7">Do you want to approve a temporary 90-day waiver, or should I</text>
          <text x="8" y="144" fill="#38bdf8" font-weight="600">draft an Architecture Decision Record (ADR) proposing Lakebase PostgreSQL?</text>
        </g>
      </g>

      <!-- INTERACTIVE ACTION BUTTONS -->
      <g transform="translate(20, 306)">
        <text x="0" y="16" fill="#94a3b8" font-size="11.5" font-weight="600">Interactive One-Click Response (Injects Keystroke to Agent TTY):</text>
        
        <!-- Button 1: Grant Waiver -->
        <g transform="translate(0, 28)">
          <rect x="0" y="0" width="160" height="42" rx="6" fill="url(#btnSecondaryGrad)" stroke="#334155" stroke-width="1"/>
          <text x="80" y="26" text-anchor="middle" fill="#cbd5e1" font-size="12" font-weight="600">Grant 90-Day Waiver</text>
        </g>

        <!-- Button 2: Draft ADR (Primary Recommended with Glow & Cursor) -->
        <g transform="translate(176, 28)" filter="url(#btnGlow)">
          <rect x="0" y="0" width="220" height="42" rx="6" fill="url(#btnPrimaryGrad)" stroke="#60a5fa" stroke-width="1.5"/>
          <text x="110" y="26" text-anchor="middle" fill="#ffffff" font-size="12.5" font-weight="700">Draft PostgreSQL ADR ✨</text>
          
          <!-- Click Pointer Cursor Mockup -->
          <g transform="translate(195, 26)">
            <polygon points="0,0 4,16 8,12 14,18 17,15 11,9 17,8" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
          </g>
        </g>

        <!-- Button 3: Freeform Reply -->
        <g transform="translate(412, 28)">
          <rect x="0" y="0" width="188" height="42" rx="6" fill="url(#btnSecondaryGrad)" stroke="#334155" stroke-width="1"/>
          <text x="94" y="26" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="500">Freeform Reply...</text>
        </g>
      </g>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. BI-DIRECTIONAL WEBSOCKET KEYSTROKE RELAY (MIDDLE BRIDGE)               -->
  <!-- ========================================================================= -->
  <g id="websocket_bridge" transform="translate(140, 560)">
    <!-- Bridge Container Card -->
    <rect x="0" y="0" width="1000" height="88" rx="8" fill="#0d1424" stroke="#1e293b" stroke-width="1.2"/>
    
    <!-- Title Tag -->
    <g transform="translate(24, 18)">
      <rect x="0" y="0" width="220" height="24" rx="4" fill="#1e293b"/>
      <circle cx="12" cy="12" r="4" fill="#38bdf8"/>
      <text x="24" y="16" fill="#38bdf8" font-size="11" font-weight="700">WEBSOCKET DATA BRIDGE</text>
      <text x="0" y="44" fill="#94a3b8" font-size="11.5">Bi-directional streaming between Backstage UI &amp; Omnigent container</text>
    </g>

    <!-- Upstream Channel (Terminal Stream Output) -->
    <g transform="translate(280, 20)">
      <!-- Animated / Dashed Line Up -->
      <path d="M 0,40 L 0,0" stroke="url(#bridgeLineUp)" stroke-width="2.5" stroke-dasharray="6 3"/>
      <polygon points="0,-4 -5,4 5,4" fill="#06b6d4"/>
      <text x="18" y="18" fill="#06b6d4" font-size="11.5" font-weight="600">Live stdout Stream</text>
      <text x="18" y="34" fill="#64748b" font-size="10.5">ansi / json stream (zero delay)</text>
    </g>

    <!-- Downstream Channel (Keystroke Injection) -->
    <g transform="translate(600, 20)">
      <!-- Animated / Dashed Line Down -->
      <path d="M 0,0 L 0,40" stroke="url(#bridgeLineDown)" stroke-width="2.5" stroke-dasharray="6 3"/>
      <polygon points="0,44 -5,36 5,36" fill="#8b5cf6"/>
      <text x="18" y="18" fill="#a78bfa" font-size="11.5" font-weight="600">Keystroke Injection (stdin)</text>
      <text x="18" y="34" fill="#64748b" font-size="10.5">herdr agent send-keys copilot "Draft PostgreSQL ADR"</text>
    </g>

    <!-- Round-Trip Latency Badge -->
    <g transform="translate(860, 28)">
      <rect x="0" y="0" width="116" height="32" rx="16" fill="#132338" stroke="#0284c7" stroke-width="1"/>
      <circle cx="16" cy="16" r="3.5" fill="#38bdf8"/>
      <text x="26" y="20" fill="#38bdf8" font-size="11" font-weight="700">&lt; 10ms P99</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. OMNIGENT SANDBOX CONTAINER & HERDR MULTIPLEXER (BOTTOM LAYER)          -->
  <!-- ========================================================================= -->
  <g id="omnigent_sandbox" transform="translate(40, 672)">
    <!-- Container Boundary Box -->
    <rect x="0" y="0" width="1200" height="176" rx="12" fill="url(#sandboxGrad)" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="6 4"/>
    
    <!-- Boundary Label Header -->
    <g transform="translate(20, 16)">
      <rect x="0" y="0" width="280" height="24" rx="4" fill="#1e3a8a" fill-opacity="0.4" stroke="#2563eb" stroke-width="1"/>
      <text x="12" y="16" fill="#93c5fd" font-size="11" font-weight="700">RING 2: OMNIGENT SECURE SANDBOX CONTAINER</text>
      <text x="300" y="16" fill="#64748b" font-size="11">gVisor / seccomp-bpf Jail • Spend Capped at $2.00 • Egress Filtered</text>
    </g>

    <!-- Component 1: Herdr PTY Multiplexer Box -->
    <g transform="translate(24, 52)">
      <rect x="0" y="0" width="450" height="106" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1"/>
      
      <!-- Box Header -->
      <g transform="translate(16, 16)">
        <rect x="0" y="0" width="18" height="18" rx="3" fill="#6366f1"/>
        <text x="26" y="14" fill="#ffffff" font-size="13" font-weight="700">Herdr PTY Multiplexer</text>
        <rect x="220" y="0" width="180" height="20" rx="10" fill="#1e293b"/>
        <text x="310" y="14" text-anchor="middle" fill="#94a3b8" font-size="10.5" font-family="ui-monospace, monospace">/dev/pts/3 • Pane #1</text>
      </g>
      
      <!-- Lifecycle State Transition Bar -->
      <g transform="translate(16, 48)">
        <text x="0" y="14" fill="#94a3b8" font-size="11" font-weight="600">Pane State Transition:</text>
        
        <!-- BLOCKED badge -->
        <rect x="130" y="0" width="70" height="22" rx="4" fill="#78350f"/>
        <text x="165" y="15" text-anchor="middle" fill="#fef3c7" font-size="10" font-weight="700">BLOCKED</text>
        
        <!-- Arrow -->
        <path d="M 206,11 L 222,11" stroke="#38bdf8" stroke-width="2"/>
        <polygon points="222,11 216,8 216,14" fill="#38bdf8"/>
        
        <!-- Key Injected badge -->
        <rect x="228" y="0" width="86" height="22" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
        <text x="271" y="15" text-anchor="middle" fill="#38bdf8" font-size="9.5" font-weight="600">Key Injected</text>

        <!-- Arrow -->
        <path d="M 320,11 L 336,11" stroke="#10b981" stroke-width="2"/>
        <polygon points="336,11 330,8 330,14" fill="#10b981"/>

        <!-- WORKING badge -->
        <rect x="342" y="0" width="74" height="22" rx="4" fill="#064e3b"/>
        <text x="379" y="15" text-anchor="middle" fill="#a7f3d0" font-size="10" font-weight="700">WORKING</text>
      </g>

      <text x="16" y="94" fill="#64748b" font-size="10.5">Auto-detected terminal input prompt via screen scraper; injected response with zero human SSH.</text>
    </g>

    <!-- Component 2: Autonomous Copilot Agent Runtime -->
    <g transform="translate(494, 52)">
      <rect x="0" y="0" width="330" height="106" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1"/>
      
      <g transform="translate(16, 16)">
        <rect x="0" y="0" width="18" height="18" rx="3" fill="#38bdf8"/>
        <text x="26" y="14" fill="#ffffff" font-size="13" font-weight="700">Copilot Agent CLI</text>
        <text x="180" y="14" fill="#64748b" font-size="11">PID 14209</text>
      </g>
      
      <g transform="translate(16, 44)" font-family="ui-monospace, monospace" font-size="10.5">
        <text y="0" fill="#cbd5e1">• Model: Claude 3.5 Sonnet / Mosaic DBRX</text>
        <text y="18" fill="#cbd5e1">• Task: payments-service ADR synthesis</text>
        <text y="36" fill="#10b981">• Action: Drafting ADR 0014 (PostgreSQL)</text>
      </g>
    </g>

    <!-- Component 3: Ephemeral Git Worktree -->
    <g transform="translate(844, 52)">
      <rect x="0" y="0" width="332" height="106" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1"/>
      
      <g transform="translate(16, 16)">
        <rect x="0" y="0" width="18" height="18" rx="3" fill="#10b981"/>
        <text x="26" y="14" fill="#ffffff" font-size="13" font-weight="700">Ephemeral Git Worktree</text>
      </g>
      
      <g transform="translate(16, 44)" font-family="ui-monospace, monospace" font-size="10.5">
        <text y="0" fill="#94a3b8">Branch: <tspan fill="#38bdf8">feat/payments-lakebase-adr</tspan></text>
        <text y="18" fill="#94a3b8">File: <tspan fill="#a7f3d0">docs/adr/0014-lakebase-postgres.md</tspan></text>
        <text y="36" fill="#64748b">Isolated scratch space; zero repo pollution.</text>
      </g>
    </g>
  </g>
</svg>'''
    return svg

if __name__ == '__main__':
    svg_code = generate_svg()
    target_path = '/home/shaun/Projects/the-agentic-ea/assets/diagrams/collaborative-codriving-ui.svg'
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(svg_code)
    print(f"Generated {target_path} successfully ({len(svg_code)} bytes).")
