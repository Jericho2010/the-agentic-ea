#!/usr/bin/env python3
"""
Automated 1080p 60fps Recorder for all 6 real Databricks and Live App scenes:
Scene 1: Databricks Apps Overview (status 'Running', active compute)
Scene 2: Databricks Unity Catalog Explorer ('ea.metamodel.nodes' schema + sample data)
Scene 3: Databricks DLT Medallion Pipeline ('EA Medallion Ingestion & Conformance' DAG)
Scene 4: Live App - Archify Living Map (Blast Radius, payments-api -> cassandra)
Scene 5: Live App - Sentinel Governance (PR #412, instant BLOCKED, 3 violations, ARB ledger)
Scene 6: Live App - Executive 2D TIME Matrix (Cartesian bubbles, 520px Drawer, Lineage, Cmd+K)
"""
import os
import signal
import subprocess
import time
from pathlib import Path

RAW_DIR = Path("/home/shaun/Projects/the-agentic-ea/data/video/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
WINDOW_ID = "0x03200004"
DATABRICKS_BASE = "https://dbc-2d6963b0-153b.cloud.databricks.com"
APP_BASE = "https://ea-navigator-cockpit-3671477545521222.aws.databricksapps.com"

def run_js(js_expr: str):
    escaped = js_expr.replace('"', '\\"')
    subprocess.run(f'opencli browser ea eval "{escaped}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def prepare_window():
    print("Preparing window: focusing and ensuring 1920x1080 fullscreen...")
    subprocess.run(f"wmctrl -i -a {WINDOW_ID}", shell=True)
    subprocess.run(f"wmctrl -i -r {WINDOW_ID} -e 0,0,0,1920,1080", shell=True)
    time.sleep(1)

def start_recorder(out_path: Path) -> subprocess.Popen:
    if out_path.exists():
        out_path.unlink()
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "x11grab",
        "-draw_mouse", "1",
        "-framerate", "60",
        "-video_size", "1920x1080",
        "-i", ":0.0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        str(out_path)
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    return proc

def stop_recorder(proc: subprocess.Popen):
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    time.sleep(0.5)

# -------------------------------------------------------------
# SCENE 1: Databricks Apps Overview
# -------------------------------------------------------------
def record_scene1():
    print("\n🎬 RECORDING SCENE 1: Databricks Apps Overview...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/apps-v2/app/ea-navigator-cockpit/overview?o=3671477545521222"
    subprocess.run(f"opencli browser ea open '{url}'", shell=True)
    time.sleep(3.5)
    
    out_file = RAW_DIR / "scene1_apps_overview.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(2.0)
        # Hover Running badge
        subprocess.run("opencli browser ea hover \"[data-testid='apps-v2-hero-status-badge']\"", shell=True)
        time.sleep(3.0)
        # Hover Compute section
        subprocess.run("opencli browser ea hover \"[data-testid='apps-v2-compute-section']\"", shell=True)
        time.sleep(3.0)
        # Hover live URL link
        subprocess.run("opencli browser ea hover \"a[href*='aws.databricksapps.com']\"", shell=True)
        time.sleep(3.5)
    finally:
        stop_recorder(proc)
    print(f"  ✓ Scene 1 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

# -------------------------------------------------------------
# SCENE 2: Databricks Unity Catalog Explorer
# -------------------------------------------------------------
def record_scene2():
    print("\n🎬 RECORDING SCENE 2: Databricks Unity Catalog Explorer...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/explore/data/ea?o=3671477545521222"
    subprocess.run(f"opencli browser ea open '{url}'", shell=True)
    time.sleep(3.5)
    
    out_file = RAW_DIR / "scene2_unity_catalog.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(2.0)
        # Click metamodel schema
        print("  -> Expanding metamodel schema...")
        subprocess.run("opencli browser ea click \"a[aria-label='metamodel'][role='treeitem']\"", shell=True)
        time.sleep(2.5)
        
        # Click nodes table
        print("  -> Selecting nodes table...")
        subprocess.run("opencli browser ea click \"a[aria-label='nodes'][role='treeitem']\"", shell=True)
        time.sleep(3.0)
        
        # Show schema overview columns
        print("  -> Showing conformed schema columns...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Overview')); if(b) b.click();")
        time.sleep(3.5)
        
        # Click Sample Data tab
        print("  -> Showing live sample data rows...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Sample Data')); if(b) b.click();")
        time.sleep(5.5)
    finally:
        stop_recorder(proc)
    print(f"  ✓ Scene 2 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

# -------------------------------------------------------------
# SCENE 3: Databricks DLT Medallion Pipeline
# -------------------------------------------------------------
def record_scene3():
    print("\n🎬 RECORDING SCENE 3: Databricks DLT Medallion Pipeline...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/pipelines/901138d7-92e5-4c26-b3a7-133ed7dd5f53"
    subprocess.run(f"opencli browser ea open '{url}'", shell=True)
    time.sleep(4.0)
    
    out_file = RAW_DIR / "scene3_dlt_pipeline.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(2.0)
        # Hover across bronze feeds
        print("  -> Hovering bronze feed sources...")
        subprocess.run("opencli browser ea hover \"div[data-testid*='cloud_resources']\"", shell=True)
        time.sleep(2.5)
        
        # Click silver_nodes to show expectations and record counts
        print("  -> Clicking silver_nodes...")
        subprocess.run("opencli browser ea click \"div[aria-label='silver_nodes']\"", shell=True)
        time.sleep(4.5)
        
        # Click gold_time_matrix
        print("  -> Clicking gold_time_matrix...")
        subprocess.run("opencli browser ea click \"div[aria-label='gold_time_matrix']\"", shell=True)
        time.sleep(5.0)
    finally:
        stop_recorder(proc)
    print(f"  ✓ Scene 3 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

# -------------------------------------------------------------
# SCENE 4: Live App - Archify Living Architecture
# -------------------------------------------------------------
def record_scene4():
    print("\n🎬 RECORDING SCENE 4: Live App - Archify Living Map...")
    prepare_window()
    subprocess.run(f"opencli browser ea open '{APP_BASE}'", shell=True)
    time.sleep(3.5)
    
    out_file = RAW_DIR / "scene4_archify_diagram.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.5)
        # Click Engineering Modernization in sidebar
        print("  -> Navigating to Engineering Modernization...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Engineering Modernization')); if(b) b.click();")
        time.sleep(3.0)
        
        # Click Blast Radius Payments Api button
        print("  -> Switching to Blast Radius diagram...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Blast Radius Payments Api')); if(b) b.click();")
        time.sleep(3.5)
        
        # Inside Archify diagram: hover payments-api and cassandra
        print("  -> Tracing blast radius: payments-api -> cassandra...")
        run_js("const b = document.querySelector('button[aria-label*=\"Focus payments-api\"]'); if(b) b.click();")
        time.sleep(3.0)
        
        run_js("const b = document.querySelector('button[aria-label*=\"Focus cassandra-legacy-cluster\"]'); if(b) b.click();")
        time.sleep(4.5)
    finally:
        stop_recorder(proc)
    print(f"  ✓ Scene 4 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

# -------------------------------------------------------------
# SCENE 5: Live App - Sentinel Governance PR Simulator
# -------------------------------------------------------------
def record_scene5():
    print("\n🎬 RECORDING SCENE 5: Live App - Sentinel Pre-Merge PR Policy Simulator...")
    prepare_window()
    subprocess.run(f"opencli browser ea open '{APP_BASE}'", shell=True)
    time.sleep(3.0)
    
    out_file = RAW_DIR / "scene5_sentinel_pr.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.5)
        # Click Sentinel Governance in sidebar
        print("  -> Navigating to Sentinel Governance...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Sentinel Governance')); if(b) b.click();")
        time.sleep(2.5)
        
        # Select Deprecated Cassandra sample PR scenario
        print("  -> Selecting Cassandra sample patch...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Deprecated Cassandra 3.11')); if(b) b.click();")
        time.sleep(2.0)
        
        # Click Simulate Evaluation
        print("  -> Clicking Simulate Evaluation...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Simulate Evaluation')); if(b) b.click();")
        time.sleep(4.0)
        
        # Scroll down smoothly to show violations and GitHub bot comment
        print("  -> Scrolling down to policy receipt and GitHub bot comment...")
        run_js("window.scrollBy({top: 480, behavior: 'smooth'});")
        time.sleep(4.0)
        
        # Scroll down further to show ARB ledger
        print("  -> Scrolling to ARB ledger...")
        run_js("window.scrollBy({top: 350, behavior: 'smooth'});")
        time.sleep(4.0)
    finally:
        stop_recorder(proc)
    print(f"  ✓ Scene 5 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

# -------------------------------------------------------------
# SCENE 6: Live App - Executive 2D TIME Matrix & 520px Drawer
# -------------------------------------------------------------
def record_scene6():
    print("\n🎬 RECORDING SCENE 6: Live App - Executive 2D TIME Matrix & 520px Drawer...")
    prepare_window()
    subprocess.run(f"opencli browser ea open '{APP_BASE}'", shell=True)
    time.sleep(3.0)
    
    out_file = RAW_DIR / "scene6_time_matrix_drawer.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.5)
        # Click Executive & Strategy in sidebar
        print("  -> Navigating to Executive & Strategy...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Executive & Strategy')); if(b) b.click();")
        time.sleep(2.5)
        
        # Hover across bubbles
        print("  -> Gliding across 2D TIME Matrix bubbles...")
        time.sleep(3.0)
        
        # Click Structured Table
        print("  -> Switching to Structured Table tab...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Structured Table')); if(b) b.click();")
        time.sleep(2.5)
        
        # Click payments-api-compute row
        print("  -> Clicking payments-api-compute to open 520px Slide-Over Drawer...")
        run_js("const row = document.querySelector('tbody tr'); if(row) row.click();")
        time.sleep(3.5)
        
        # Cycle drawer tabs: Lineage -> Governance -> Raw JSON
        print("  -> Cycling drawer tabs: Lineage & Graph...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Lineage & Graph')); if(b) b.click();")
        time.sleep(2.5)
        
        print("  -> Cycling drawer tabs: Governance & Rules...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Governance & Rules')); if(b) b.click();")
        time.sleep(2.5)
        
        print("  -> Cycling drawer tabs: Raw JSON...")
        run_js("const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Raw JSON')); if(b) b.click();")
        time.sleep(3.0)
        
        # Close drawer with Escape
        print("  -> Dismissing drawer with Escape...")
        subprocess.run("opencli browser ea keys Escape", shell=True)
        time.sleep(1.5)
        
        # Trigger Command Palette
        print("  -> Opening Command Palette (Ctrl+K)...")
        subprocess.run("opencli browser ea keys Control+k", shell=True)
        time.sleep(1.5)
        
        # Type 'cassandra'
        print("  -> Typing 'cassandra'...")
        run_js("const inp = document.querySelector('input[placeholder*=\"Search applications\"]'); if(inp) { inp.value = 'cassandra'; inp.dispatchEvent(new Event('input', {bubbles: true})); }")
        time.sleep(2.5)
        
        # Dismiss Command Palette
        print("  -> Closing Command Palette with Escape...")
        subprocess.run("opencli browser ea keys Escape", shell=True)
        time.sleep(2.0)
    finally:
        stop_recorder(proc)
    print(f"  ✓ Scene 6 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")


def main():
    record_scene1()
    record_scene2()
    record_scene3()
    record_scene4()
    record_scene5()
    record_scene6()
    print("\n🎉 ALL 6 REAL ACTION SCENES RECORDED SUCCESSFULLY IN 1080p 60fps!")

if __name__ == "__main__":
    main()
