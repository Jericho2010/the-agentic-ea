# Enterprise Architecture Navigator Cockpit — Modern SaaS UX Specification

## Mission
Elevate the application from a "dashboard" (flat cards + tables layout) to a **modern, professional, enterprise-grade SaaS application** (Linear / Datadog / Stripe / Vercel caliber).

---

## 1. Core UX & Architectural Upgrades

### A. Professional SaaS Application Shell
1. **Left Navigation Rail / Sidebar (Collapsible)**:
   - **Header**: Sleek brand logo + "The Agentic EA" + "v1.0" badge.
   - **Environment / Estate Switcher**: "Enterprise Prod (UC df4dc09688caf6d8)" with green live ping indicator.
   - **Primary Workspace Navigation**:
     - 📊 **Executive & Strategy** (TIME Matrix, Lifecycle Horizons, FinOps)
     - 🛡️ **Sentinel Governance** (Policy Catalog, PR Simulator, ARB Audit Ledger)
     - 🗺️ **Engineering Modernization** (Conformed PAM Metamodel, Living Architecture Maps)
     - ⚡ **Operations & FinOps** (CMDB Drift Resolution, Reconcile Workflows)
   - **Sidebar Footer**:
     - Databricks SQL Warehouse connection status with latency ping.
     - Keyboard shortcut indicator (`⌘K` Command Palette).
     - Collapse/Expand toggle.

2. **Top Global Utility Bar**:
   - Breadcrumb navigation (`Enterprise Estate / <Active Workspace> / <Sub-section>`).
   - **Global Search / Quick Command (`Cmd+K`)**:
     - Instant filter/search input with keyboard shortcut tooltip (`/` or `⌘K`).
     - Searches across all PAM CIs, applications, policies, drift items, and Archify maps.
   - **Quick Actions**:
     - "Evaluate PR" button (opens Sentinel PR Simulator).
     - "Sync CMDB" button (triggers drift reconciliation).
     - "Refresh" button with spin animation and last-synced timestamp.
     - User / Role badge ("Enterprise Architect").

---

### B. Deep Slide-Over Entity Inspector Drawer (Crucial SaaS Feature)
In a modern SaaS tool, clicking **ANY** entity (an application, PAM node, audit record, or drift item) must not be a dead end:
- A smooth slide-over drawer slides in from the right (`w-[520px]`, dark slate with glassmorphism backdrop).
- Keyboard accessible (`Esc` to close).
- **Tabs inside Drawer**:
  1. **Overview**: Key metrics (Cost, Tech Debt, CO2, Tier, Owner, Lifecycle status).
  2. **Lineage & Realization**: Upstream callers, downstream datastores, Cloud Resource mapping.
  3. **Governance & Compliance**: Applicable Sentinel policies, compliance pass/fail, violation details.
  4. **Raw JSON Payload**: Formatted JSON viewer with 1-click copy.
- **Contextual Actions**:
  - "Inspect in Metamodel Explorer"
  - "View in Archify Architecture Map"
  - "Reconcile in CMDB"

---

### C. Workspace Overhauls

#### 1. Executive & Strategy Workspace
- **Top Metrics Ribbon**: Modern slim KPI bar with percentage comparisons and micro-badges instead of giant blocky cards.
- **Interactive 2D TIME Matrix Canvas**:
  - View Toggle: **"2D Visual Canvas"** vs **"Structured Grid Table"**.
  - **2D Canvas View**:
    - Cartesian grid: X-axis = Business Value (0–100), Y-axis = Technical Health / Debt (0–100).
    - 4 distinct colored quadrant zones with subtle gradient backdrops:
      - **INVEST** (High Value, High Health — Emerald)
      - **TOLERATE** (Low Value, High Health — Blue/Sky)
      - **MIGRATE** (High Value, Low Health — Amber)
      - **ELIMINATE** (Low Value, Low Health — Rose)
    - Plotted interactive application bubbles, sized proportionally to annual spend.
    - Hovering displays quick tooltip card with spend, debt, and disposition.
    - Clicking any application opens the **Slide-Over Entity Inspector Drawer**.
- **Portfolio Obsolescence & Lifecycle Horizon**:
  - Timeline cards showing EOL horizons (Expired, Near EOL, Approaching EOL) with financial exposure and mitigation recommendations.

#### 2. Autonomous Governance & Compliance Workspace
- **Sentinel Policy Catalog**:
  - Interactive policy cards with severity badges, target standards (EU AI Act, GDPR, DORA), and enforcement toggles.
- **Interactive PR Policy Simulator**:
  - Allows the architect to simulate an incoming PR diff (e.g., adding an unapproved Cassandra datastore or unencrypted PII stream).
  - Live "Simulate Evaluation" trigger showing the Tri-Modal evaluation pipeline, policy checks, and resulting visual delta badge in real time!
- **ARB Audit Ledger**:
  - Searchable, filterable audit history (Filter by Approved, Blocked, Waiver).
  - Clicking any audit row opens the Drawer with full PR commit details, evaluator, and violation list.

#### 3. Engineering Modernization Workspace
- **Living Architecture Maps (Archify Viewer)**:
  - Full-height, sleek diagram canvas.
  - Floating top toolbar: Diagram selector pills (Architecture View, AI Model Lineage, Interface Sequence, Blast Radius Payments API, etc.), Fullscreen toggle, SVG/HTML export button.
- **Conformed Metamodel Explorer**:
  - Multi-faceted search & filter pills (Kind: AIModel, CloudResource, Capability, Application; Domain: Core, Payments; Lifecycle: Production, Legacy).
  - Graph node & realization edge tables with click-to-inspect opening the Drawer.

#### 4. Operations & FinOps Workspace
- **CMDB Drift Resolution Console**:
  - Discrepancy taxonomy filter pills (Phantom CIs: 7, Shadow IT: 11) with active indicator.
  - Side-by-side reconciliation comparison:
    - Left column: CMDB Declared State (`sys_id`, `operational_status`).
    - Right column: Runtime Cloud Telemetry (`cost/mo`, discovered cloud resource).
  - 1-Click "Automated Reconcile" action dialog with live execution stepper (`Validating Delta table` -> `Generating ServiceNow payload` -> `Writing audit trail` -> `Reconciled`).

---

## 2. Design System & Aesthetics
- **Dark Theme**: Linear/Datadog palette:
  - Base background: `#080c14` (ultra-deep navy-black)
  - Sidebar: `#0d1322`
  - Elevated Cards / Surfaces: `#131b2e` with hairline borders (`#1e293b` / `rgba(255,255,255,0.06)`)
  - Accent / Primary: `#38bdf8` (Sky) and `#10b981` (Emerald)
  - Typography: Crisp white `#ffffff` for primary values/headers, muted slate `#94a3b8` for secondary text.
- **Strictly ZERO Emojis**: 100% Lucide SVG icons.
- **Smooth Animations**: Subtle transitions on drawer open, tabs switch, hover states, and modals.
- **Keyboard Shortcuts**: `⌘K` or `/` for search, `Esc` to close drawer/modals.

---

## 3. Verification Protocol
1. Manual review and traversal of the app in Chrome via `opencli browser ea`.
2. Validate that clicking entities opens the Slide-over Entity Inspector Drawer.
3. Validate that the 2D TIME Matrix canvas renders and is interactive.
4. Validate that all 4 workspaces have zero console errors and 100% live Databricks Unity Catalog data.
5. Deploy to Databricks Apps and verify live URL.
