#!/usr/bin/env python3
"""
Generate pixel-perfect transparent 1920x1080 PNG overlays with sleek Linear-style
lower-third caption ribbons for Scene 3, Scene 4, and Scene 5.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OVERLAYS_DIR = Path("data/video/overlays")
OVERLAYS_DIR.mkdir(parents=True, exist_ok=True)

OVERLAYS = {
    "scene3": {
        "badge": "SHIFT 2 OF 4: GOVERNANCE IN THE PR FLOW",
        "badge_color": "border-rose-500/50 text-rose-400 bg-rose-500/10",
        "title": "\"Autonomous pre-merge AI gates evaluate infrastructure diffs before code merges.\"",
        "subtitle": "Pre-Merge Policy Simulator: Cassandra 3.11 BLOCKED with 3 Critical Policy Violations",
        "tag": "EA Sentinel Gate • Live Delta Diff"
    },
    "scene4": {
        "badge": "SHIFT 3 OF 4: ESTATE INTELLIGENCE & BLAST RADIUS",
        "badge_color": "border-sky-500/50 text-sky-400 bg-sky-500/10",
        "title": "\"Answering 'What is our financial exposure?' is a graph traversal computed in milliseconds.\"",
        "subtitle": "Sub-Second BFS Graph Blast Radius ($234,999/yr) & Regulatory Compliance Lineage (GDPR/DORA)",
        "tag": "Living Architecture Maps • Archify Vector"
    },
    "scene5": {
        "badge": "SHIFT 4 OF 4: REAL EXECUTIVE VALUE",
        "badge_color": "border-emerald-500/50 text-emerald-400 bg-emerald-500/10",
        "title": "\"An interactive 2D TIME matrix plotted on business value vs technical debt, tied to live cloud spend.\"",
        "subtitle": "520px Slide-Over Entity Inspector Drawer • Command Palette (⌘K) • ServiceNow CMDB Reconcile",
        "tag": "2D Cartesian TIME Model • Live Cloud CUR"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{
      background: transparent !important;
      margin: 0;
      padding: 48px;
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      box-sizing: border-box;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <!-- Lower Third Subtitle Ribbon -->
  <div class="w-full bg-[#0d1322]/95 border border-[#38bdf8]/40 rounded-2xl p-4 shadow-2xl flex items-center justify-between backdrop-blur-md">
    <div class="flex items-center space-x-4">
      <div class="px-3 py-1 rounded-lg {badge_color} font-mono text-xs font-bold border">
        {badge}
      </div>
      <div>
        <div class="text-sm font-bold text-white tracking-tight">
          {title}
        </div>
        <div class="text-xs text-[#94a3b8] mt-0.5">
          {subtitle}
        </div>
      </div>
    </div>
    <div class="text-right font-mono text-xs text-[#94a3b8] shrink-0 pl-6 border-l border-[#1e293b]">
      <span class="text-sky-400 font-bold block">{tag}</span>
      <span class="text-[10px] text-[#64748b]">The Agentic EA • Databricks Native</span>
    </div>
  </div>
</body>
</html>
"""

def generate_overlays():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        for key, data in OVERLAYS.items():
            html = HTML_TEMPLATE.format(
                badge=data["badge"],
                badge_color=data["badge_color"],
                title=data["title"],
                subtitle=data["subtitle"],
                tag=data["tag"]
            )
            page.set_content(html)
            page.wait_for_timeout(500)
            out_png = OVERLAYS_DIR / f"{key}_overlay.png"
            page.screenshot(path=str(out_png), omit_background=True)
            print(f"  ✓ Generated transparent overlay: {out_png}")

        browser.close()

if __name__ == "__main__":
    generate_overlays()
