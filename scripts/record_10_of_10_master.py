#!/usr/bin/env python3
"""
DIRECTOR'S 10/10 MASTER CUT RECORDER & COMPILER
Target: 1080p 60fps, Zero Subtitles, Zero Fake Mocks, Zero Artificial Wobble, 100% Real Software
8 Full-Frame Scenes:
  Scene 1: Databricks Workspace Home (6s)
  Scene 2: Databricks Catalog Explorer (10s)
  Scene 3: Databricks Apps Overview (6s)
  Scene 4: Databricks DLT Medallion Pipeline (6s)
  Scene 5: Executive Strategy & 2D TIME Matrix (16s)
  Scene 6: Engineering Modernization & Archify Living Maps (18s)
  Scene 7: Sentinel Pre-Merge PR Governance (18s)
  Scene 8: Operations & FinOps + Command Palette (12s)
Total Duration: 92.00s
"""
import os
import signal
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path("/home/shaun/Projects/the-agentic-ea")
RAW_DIR = PROJECT_ROOT / "data/video/raw"
CONFORMED_DIR = PROJECT_ROOT / "data/video/conformed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
CONFORMED_DIR.mkdir(parents=True, exist_ok=True)
FINAL_OUTPUT = PROJECT_ROOT / "data/video/the_agentic_ea_launch.mp4"

WINDOW_ID = "0x04000004"
DATABRICKS_BASE = "https://dbc-2d6963b0-153b.cloud.databricks.com"
APP_BASE = "http://127.0.0.1:8088"

def run_js(js_expr: str):
    escaped = js_expr.replace('"', '\\"')
    subprocess.run(f'opencli browser ea eval "{escaped}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def dismiss_infobar():
    # Clicks close on OpenCLI infobar if present at (1883, 25)
    subprocess.run("xdotool mousemove 1883 25 click 1", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.3)

def prepare_window():
    subprocess.run("xset s off", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run("xset -dpms", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run("cinnamon-screensaver-command -d", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(f"wmctrl -i -a {WINDOW_ID}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dismiss_infobar()

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

# =====================================================================
# SCENE 1: Databricks Workspace Home (6s target)
# =====================================================================
def record_scene1():
    print("\n🎬 [1/8] Recording Databricks Workspace Home...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/?email=shaundavidanderson%40gmail.com&autoLogin=true&o=3671477545521222"
    run_js(f"window.location.href = '{url}'")
    time.sleep(3.5)
    dismiss_infobar()
    time.sleep(0.5)
    
    out_file = RAW_DIR / "s1_home_raw.mp4"
    proc = start_recorder(out_file)
    try:
        # Hover avatar and resources
        subprocess.run("xdotool mousemove 1905 40", shell=True) # User avatar
        time.sleep(1.5)
        subprocess.run("xdotool mousemove 350 655", shell=True) # EA Medallion pipeline
        time.sleep(1.2)
        subprocess.run("xdotool mousemove 350 700", shell=True) # nodes table
        time.sleep(1.2)
        subprocess.run("xdotool mousemove 350 745", shell=True) # metamodel schema
        time.sleep(1.2)
        subprocess.run("xdotool mousemove 350 835", shell=True) # ea-navigator-cockpit app
        time.sleep(1.5)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S1 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 2: Databricks Unity Catalog Explorer (10s target)
# =====================================================================
def record_scene2():
    print("\n🎬 [2/8] Recording Databricks Catalog Explorer...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/explore/data/ea?o=3671477545521222"
    run_js(f"window.location.href = '{url}'")
    time.sleep(3.5)
    dismiss_infobar()
    
    out_file = RAW_DIR / "s2_catalog_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.2)
        # Click metamodel schema
        print("    -> Expanding metamodel schema...")
        run_js("""(() => {
          const m = document.querySelector("a[aria-label='metamodel'][role='treeitem']") ||
                    Array.from(document.querySelectorAll('a, button, span, td')).find(x => x.innerText.trim() === 'metamodel');
          if (m) m.click();
        })()""")
        time.sleep(2.0)
        
        # Click nodes table
        print("    -> Drilling into nodes table...")
        run_js("""(() => {
          const n = document.querySelector("a[aria-label='nodes'][role='treeitem']") ||
                    Array.from(document.querySelectorAll('a, button, span, td')).find(x => x.innerText.trim() === 'nodes');
          if (n) n.click();
        })()""")
        time.sleep(2.5)
        
        # Hover across conformed columns
        subprocess.run("xdotool mousemove 450 380", shell=True)
        time.sleep(1.5)
        
        # Click Sample Data tab
        print("    -> Showing Sample Data rows...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button[role="tab"]')).find(b => b.innerText.includes('Sample Data'));
          if (b) { b.focus(); b.click(); }
        })()""")
        time.sleep(3.5)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S2 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 3: Databricks Apps Overview (6s target)
# =====================================================================
def record_scene3():
    print("\n🎬 [3/8] Recording Databricks Apps Overview...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/apps-v2/app/ea-navigator-cockpit/overview?o=3671477545521222"
    run_js(f"window.location.href = '{url}'")
    time.sleep(3.5)
    dismiss_infobar()
    
    out_file = RAW_DIR / "s3_apps_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.0)
        # Hover Running badge
        subprocess.run("xdotool mousemove 365 305", shell=True)
        time.sleep(2.0)
        # Hover Instance compute specs
        subprocess.run("xdotool mousemove 400 340", shell=True)
        time.sleep(1.8)
        # Hover live URL link
        subprocess.run("xdotool mousemove 480 305", shell=True)
        time.sleep(1.8)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S3 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 4: Databricks DLT Medallion Pipeline DAG (6s target)
# =====================================================================
def record_scene4():
    print("\n🎬 [4/8] Recording Databricks DLT Medallion Pipeline...")
    prepare_window()
    url = f"{DATABRICKS_BASE}/pipelines/901138d7-92e5-4c26-b3a7-133ed7dd5f53"
    run_js(f"window.location.href = '{url}'")
    time.sleep(4.0)
    dismiss_infobar()
    
    out_file = RAW_DIR / "s4_dlt_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.0)
        # Trace across bronze feeds
        subprocess.run("xdotool mousemove 350 275", shell=True)
        time.sleep(1.5)
        # Hover silver nodes
        subprocess.run("xdotool mousemove 500 500", shell=True)
        time.sleep(1.8)
        # Hover gold time matrix
        subprocess.run("xdotool mousemove 500 260", shell=True)
        time.sleep(2.2)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S4 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 5: Executive Strategy & 2D TIME Matrix + Drawer (16s target)
# =====================================================================
def record_scene5():
    print("\n🎬 [5/8] Recording Executive Strategy & 2D TIME Matrix...")
    prepare_window()
    run_js(f"window.location.href = '{APP_BASE}/'")
    time.sleep(2.0)
    dismiss_infobar()
    
    # Wait for matrix data to be loaded before recording starts
    print("    -> Waiting for TIME Matrix items to load...")
    for _ in range(20):
        try:
            res = subprocess.check_output(
                'opencli browser ea eval "Boolean(document.querySelector(\'.cursor-pointer.rounded-full\'))"',
                shell=True
            ).decode()
            if "true" in res.lower():
                break
        except Exception:
            pass
        time.sleep(1.0)
    
    out_file = RAW_DIR / "s5_time_matrix_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.5)
        # Hover over 2D matrix glowing bubbles
        subprocess.run("xdotool mousemove 640 485", shell=True) # Invest payments-api
        time.sleep(1.5)
        subprocess.run("xdotool mousemove 720 485", shell=True) # Invest billing
        time.sleep(1.2)
        subprocess.run("xdotool mousemove 420 760", shell=True) # Eliminate cassandra
        time.sleep(1.8)
        
        # Switch to Structured Table tab
        print("    -> Switching to Structured Table...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Structured Table'));
          if (b) b.click();
        })()""")
        time.sleep(2.2)
        
        # Click payments-api-compute to open 520px Slide-Over Drawer
        print("    -> Opening 520px Slide-Over Drawer...")
        run_js("const row = document.querySelector('tbody tr'); if (row) row.click();")
        time.sleep(2.5)
        
        # Cycle drawer tabs: Lineage & Graph -> Governance & Rules -> Raw JSON
        print("    -> Drawer: Lineage & Graph...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Lineage & Graph'));
          if (b) b.click();
        })()""")
        time.sleep(1.8)
        
        print("    -> Drawer: Governance & Rules...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Governance & Rules'));
          if (b) b.click();
        })()""")
        time.sleep(1.8)
        
        print("    -> Drawer: Raw JSON...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Raw JSON'));
          if (b) b.click();
        })()""")
        time.sleep(2.0)
        
        # Dismiss drawer
        subprocess.run("xdotool key Escape", shell=True)
        time.sleep(1.0)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S5 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 6: Engineering Modernization & Archify Living Maps (18s target)
# =====================================================================
def record_scene6():
    print("\n🎬 [6/8] Recording Engineering Modernization & Archify Living Maps...")
    prepare_window()
    run_js(f"window.location.href = '{APP_BASE}/'")
    time.sleep(2.0)
    dismiss_infobar()
    
    # Click Engineering Modernization in sidebar
    run_js("""(() => {
      const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Engineering Modernization'));
      if (b) b.click();
    })()""")
    time.sleep(2.5)
    
    out_file = RAW_DIR / "s6_archify_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.5)
        # 1. Architecture View
        subprocess.run("xdotool mousemove 415 480", shell=True) # web-storefront
        time.sleep(2.0)
        
        # 2. Switch to Blast Radius Payments Api
        print("    -> Switching to Blast Radius Payments Api...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Blast Radius Payments Api'));
          if (b) b.click();
        })()""")
        time.sleep(2.5)
        
        # Trace red vector down to cassandra
        subprocess.run("xdotool mousemove 415 480", shell=True) # web-storefront
        time.sleep(1.2)
        subprocess.run("xdotool mousemove 415 900", shell=True) # payments-api
        time.sleep(1.8)
        
        # 3. Switch to GDPR Dora Lineage
        print("    -> Switching to GDPR Dora Lineage...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Gdpr Dora Lineage'));
          if (b) b.click();
        })()""")
        time.sleep(3.0)
        
        # 4. Switch to Conformed PAM Metamodel Explorer (36 CIs)
        print("    -> Switching to Conformed PAM Metamodel Explorer...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Conformed PAM Metamodel Explorer'));
          if (b) b.click();
        })()""")
        time.sleep(2.5)
        
        # Filter Kind dropdown
        run_js("""(() => {
          const s = document.querySelector('select');
          if (s) { s.value = 'AIModel'; s.dispatchEvent(new Event('change', {bubbles: true})); }
        })()""")
        time.sleep(3.0)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S6 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 7: Sentinel Pre-Merge PR Governance (18s target)
# =====================================================================
def record_scene7():
    print("\n🎬 [7/8] Recording Sentinel Pre-Merge PR Governance...")
    prepare_window()
    run_js(f"window.location.href = '{APP_BASE}/'")
    time.sleep(2.0)
    dismiss_infobar()
    
    # Click Sentinel Governance in sidebar
    run_js("""(() => {
      const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Sentinel Governance'));
      if (b) b.click();
    })()""")
    time.sleep(2.0)
    
    out_file = RAW_DIR / "s7_sentinel_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.2)
        # 1. Select Approved Scenario
        print("    -> Scenario 1: Databricks Unity Catalog Managed Delta Table...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Databricks Unity Catalog Managed Delta Table'));
          if (b) b.click();
        })()""")
        time.sleep(1.5)
        
        # Click Simulate Evaluation -> APPROVED
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Simulate Evaluation'));
          if (b) b.click();
        })()""")
        time.sleep(3.0)
        
        # 2. Select Blocked Scenario: Cassandra
        print("    -> Scenario 2: Deprecated Cassandra 3.11 Datastore with Plaintext PII...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Deprecated Cassandra 3.11'));
          if (b) b.click();
        })()""")
        time.sleep(1.5)
        
        # Click Simulate Evaluation -> BLOCKED
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Simulate Evaluation'));
          if (b) b.click();
        })()""")
        time.sleep(3.5)
        
        # Scroll down to show Live ARB Ledger
        print("    -> Scrolling down to Live ARB Audit Ledger...")
        run_js("window.scrollBy({top: 480, behavior: 'smooth'});")
        time.sleep(3.0)
        run_js("window.scrollBy({top: 350, behavior: 'smooth'});")
        time.sleep(2.5)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S7 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# SCENE 8: Operations & FinOps + Command Palette (12s target)
# =====================================================================
def record_scene8():
    print("\n🎬 [8/8] Recording Operations & FinOps + Command Palette...")
    prepare_window()
    run_js(f"window.location.href = '{APP_BASE}/'")
    time.sleep(2.0)
    dismiss_infobar()
    
    # Click Operations & FinOps in sidebar
    run_js("""(() => {
      const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Operations & FinOps'));
      if (b) b.click();
    })()""")
    time.sleep(2.0)
    
    out_file = RAW_DIR / "s8_operations_raw.mp4"
    proc = start_recorder(out_file)
    try:
        time.sleep(1.2)
        # Hover across CMDB drift cards
        subprocess.run("xdotool mousemove 320 180", shell=True)
        time.sleep(1.5)
        
        # Click Sync CMDB button
        print("    -> Clicking Sync CMDB...")
        run_js("""(() => {
          const b = Array.from(document.querySelectorAll('button')).find(x => x.innerText.includes('Sync CMDB'));
          if (b) b.click();
        })()""")
        time.sleep(2.0)
        
        # Click Quick Command Palette button
        print("    -> Opening universal Command Palette...")
        run_js("""(() => {
          const b = document.querySelector('button[title*=\"Quick Command Palette\"]');
          if (b) b.click();
        })()""")
        time.sleep(1.8)
        
        # Type 'cassandra'
        print("    -> Typing 'cassandra'...")
        run_js("""(() => {
          const inp = document.querySelector('input[placeholder*=\"Search applications\"]');
          if (inp) {
            inp.value = 'cassandra';
            inp.dispatchEvent(new Event('input', {bubbles: true}));
          }
        })()""")
        time.sleep(2.8)
        
        # Dismiss with Escape
        print("    -> Dismissing with Escape...")
        run_js("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}))")
        time.sleep(1.2)
    finally:
        stop_recorder(proc)
    print(f"  ✓ S8 raw recorded ({out_file.stat().st_size / 1024:.1f} KB)")

# =====================================================================
# CONFORMING & MASTER CONCATENATION (Stable 1080p60 CFR)
# =====================================================================
SCENE_DURATIONS = [
    ("s1_home_raw.mp4", "s1_conformed.mp4", 6.0),
    ("s2_catalog_raw.mp4", "s2_conformed.mp4", 10.0),
    ("s3_apps_raw.mp4", "s3_conformed.mp4", 6.0),
    ("s4_dlt_raw.mp4", "s4_conformed.mp4", 6.0),
    ("s5_time_matrix_raw.mp4", "s5_conformed.mp4", 16.0),
    ("s6_archify_raw.mp4", "s6_conformed.mp4", 18.0),
    ("s7_sentinel_raw.mp4", "s7_conformed.mp4", 18.0),
    ("s8_operations_raw.mp4", "s8_conformed.mp4", 12.0),
]

def conform_scenes():
    print("\n🎞️  CONFORMING SCENES TO EXACT 60fps CFR AND TARGET DURATIONS...")
    for raw_name, conf_name, duration in SCENE_DURATIONS:
        raw_p = RAW_DIR / raw_name
        conf_p = CONFORMED_DIR / conf_name
        if conf_p.exists():
            conf_p.unlink()
        print(f"  -> Conforming {raw_name} -> {conf_name} ({duration}s @ 60fps CFR)...")
        cmd = [
            "ffmpeg", "-y",
            "-ss", "0.5", # skip initial 0.5s recording lead-in
            "-i", str(raw_p),
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-r", "60",
            "-an",
            str(conf_p)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"     Done: {conf_p.stat().st_size / 1024:.1f} KB")

def assemble_master():
    print("\n🚀 ASSEMBLING 10/10 MASTER CUT (92s, 1080p60 CFR, 0 subtitles, 0 audio)...")
    concat_file = CONFORMED_DIR / "concat_list.txt"
    with open(concat_file, "w") as f:
        for _, conf_name, _ in SCENE_DURATIONS:
            conf_p = CONFORMED_DIR / conf_name
            f.write(f"file '{conf_p.resolve()}'\n")
            
    if FINAL_OUTPUT.exists():
        FINAL_OUTPUT.unlink()
        
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-r", "60",
        "-an",
        str(FINAL_OUTPUT)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n🎉 MASTER ASSEMBLED SUCCESSFULLY: {FINAL_OUTPUT}")
    print(f"   Size: {FINAL_OUTPUT.stat().st_size / (1024 * 1024):.2f} MB")

def main():
    print("=" * 70)
    print("   THE AGENTIC ENTERPRISE ARCHITECT — 10/10 MASTER CUT PIPELINE")
    print("=" * 70)
    record_scene1()
    record_scene2()
    record_scene3()
    record_scene4()
    record_scene5()
    record_scene6()
    record_scene7()
    record_scene8()
    conform_scenes()
    assemble_master()

if __name__ == "__main__":
    main()
