#!/usr/bin/env python3
"""
Automated High-Fidelity 1080p Screencast Recorder for The Agentic EA.
Captures all 6 scenes of the master launch video at 1920x1080 resolution
targeting the live serverless Databricks backend on http://127.0.0.1:8088.
"""
import os
import shutil
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

RAW_DIR = Path("data/video/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:8088"

def record_scene(scene_name: str, duration_sec: float, runner_fn):
    print(f"\n=======================================================")
    print(f"🎬 RECORDING {scene_name.upper()} (Target: {duration_sec}s)")
    print(f"=======================================================")
    
    scene_dir = RAW_DIR / scene_name
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080",
                "--hide-scrollbars",
            ]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(scene_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        start_time = time.time()
        runner_fn(page)
        elapsed = time.time() - start_time
        remaining = duration_sec - elapsed
        if remaining > 0:
            print(f"Holding scene for {remaining:.1f}s to match {duration_sec}s pacing...")
            page.wait_for_timeout(int(remaining * 1000))

        page.close()
        context.close()
        browser.close()

    # Find recorded webm file
    files = list(scene_dir.glob("*.webm"))
    if files:
        final_file = RAW_DIR / f"{scene_name}.webm"
        if final_file.exists():
            final_file.unlink()
        files[0].rename(final_file)
        print(f"  ✓ {scene_name} saved: {final_file} ({final_file.stat().st_size / 1024:.1f} KB)")


def record_scene1(page):
    """Scene 1: The Trap — Static Shelfware & Cloud Drift (15s)"""
    page.goto(f"{BASE_URL}/scene1_shelfware_trap.html")
    page.wait_for_timeout(3000)
    page.mouse.move(500, 350)
    page.wait_for_timeout(3000)
    page.mouse.move(750, 480)
    page.wait_for_timeout(3000)
    page.mouse.move(1400, 300)
    page.wait_for_timeout(3000)


def record_scene2(page):
    """Scene 2: Shift 1 — Metamodel as Lakehouse Data & DLT (20s)"""
    page.goto(f"{BASE_URL}/scene2_lakehouse_dlt_uc.html")
    page.wait_for_timeout(3000)
    # Pan over Unity Catalog schemas
    page.mouse.move(300, 280)
    page.wait_for_timeout(2500)
    page.mouse.move(300, 480)
    page.wait_for_timeout(2500)
    # Pan over DLT Medallion Pipeline
    page.mouse.move(1100, 260)
    page.wait_for_timeout(3000)
    page.mouse.move(1400, 260)
    page.wait_for_timeout(3000)
    # Highlight connectors
    page.mouse.move(1000, 520)
    page.wait_for_timeout(3000)


def record_scene3(page):
    """Scene 3: Shift 2 — Governance in the PR Flow (Sentinel Gate) (20s)"""
    page.goto(BASE_URL)
    page.wait_for_selector("aside", timeout=15000)
    page.wait_for_timeout(2000)

    # Click Sentinel Governance in sidebar
    print("  -> Navigating to Sentinel Governance...")
    page.click("button:has-text('Sentinel Governance')")
    page.wait_for_timeout(2500)

    # Select Cassandra PR scenario
    print("  -> Selecting Cassandra sample patch...")
    page.click("button:has-text('Deprecated Cassandra 3.11')")
    page.wait_for_timeout(2000)

    # Click Simulate Evaluation
    print("  -> Triggering Simulate Evaluation...")
    page.click("button:has-text('Simulate Evaluation')")
    page.wait_for_timeout(4000)

    # Scroll down to policy cards and ARB ledger
    print("  -> Scrolling policy ledger...")
    page.mouse.wheel(0, 450)
    page.wait_for_timeout(3000)
    page.mouse.wheel(0, -450)
    page.wait_for_timeout(2000)


def record_scene4(page):
    """Scene 4: Shift 3 — Live Estate Intelligence & Blast Radius (20s)"""
    page.goto(BASE_URL)
    page.wait_for_selector("aside", timeout=15000)
    page.wait_for_timeout(2000)

    # Click Engineering Modernization
    print("  -> Navigating to Engineering Modernization...")
    page.click("button:has-text('Engineering Modernization')")
    page.wait_for_timeout(3000)

    # Select Blast Radius diagram
    print("  -> Selecting Blast Radius diagram...")
    blast_btn = page.locator("button:has-text('Blast Radius')").first
    if blast_btn.count() > 0:
        blast_btn.click()
        page.wait_for_timeout(3500)

    # Select GDPR DORA diagram
    print("  -> Selecting GDPR DORA Lineage...")
    gdpr_btn = page.locator("button:has-text('Gdpr Dora Lineage')").first
    if gdpr_btn.count() > 0:
        gdpr_btn.click()
        page.wait_for_timeout(3500)

    # Switch to Conformed PAM Metamodel Explorer
    print("  -> Switching to PAM Metamodel Explorer...")
    page.click("button:has-text('Conformed PAM Metamodel Explorer')")
    page.wait_for_timeout(2500)
    page.mouse.wheel(0, 300)
    page.wait_for_timeout(2500)


def record_scene5(page):
    """Scene 5: Shift 4 — 2D Cartesian TIME Matrix & Entity Inspector Drawer (25s)"""
    page.goto(BASE_URL)
    page.wait_for_selector("aside", timeout=15000)
    page.wait_for_timeout(2500)

    # Hover over 2D TIME Matrix bubbles
    print("  -> Hovering over 2D TIME Matrix bubbles...")
    page.mouse.move(700, 350)
    page.wait_for_timeout(1500)
    page.mouse.move(1100, 350)
    page.wait_for_timeout(2000)

    # Click payments-api-compute in table to open 520px Slide-Over Drawer
    print("  -> Clicking row to trigger Slide-Over Entity Inspector Drawer...")
    page.locator("tbody tr:has-text('payments-api-compute')").first.click()
    page.wait_for_timeout(3000)

    # Cycle drawer tabs: Lineage -> Governance -> Raw JSON
    print("  -> Cycling drawer tabs...")
    page.click("button:has-text('Lineage & Graph')")
    page.wait_for_timeout(2000)
    page.click("button:has-text('Governance & Rules')")
    page.wait_for_timeout(2000)
    page.click("button:has-text('Raw JSON')")
    page.wait_for_timeout(2500)

    # Dismiss drawer with Escape
    print("  -> Closing drawer with Escape...")
    page.keyboard.press("Escape")
    page.wait_for_timeout(1500)

    # Trigger Command Palette (⌘K)
    print("  -> Opening Command Palette...")
    page.click("button:has-text('Search applications')")
    page.wait_for_timeout(1500)
    page.locator("input[placeholder*='Search applications']").type("cassandra", delay=120)
    page.wait_for_timeout(2000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1500)

    # Navigate to Operations & FinOps workspace
    print("  -> Navigating to Operations workspace...")
    page.click("button:has-text('Operations & FinOps')")
    page.wait_for_timeout(2500)
    page.mouse.wheel(0, 300)
    page.wait_for_timeout(2000)


def record_scene6(page):
    """Scene 6: The Payoff — Architecture as Velocity (15s)"""
    page.goto(f"{BASE_URL}/scene6_hero_launch.html")
    page.wait_for_timeout(3000)
    page.mouse.move(960, 250)
    page.wait_for_timeout(3000)
    page.mouse.move(960, 500)
    page.wait_for_timeout(4000)
    page.mouse.move(960, 800)
    page.wait_for_timeout(3000)


def main():
    record_scene("scene1", 15.0, record_scene1)
    record_scene("scene2", 20.0, record_scene2)
    record_scene("scene3", 20.0, record_scene3)
    record_scene("scene4", 20.0, record_scene4)
    record_scene("scene5", 25.0, record_scene5)
    record_scene("scene6", 15.0, record_scene6)
    print("\n🎉 ALL 6 SCENES RECORDED SUCCESSFULLY IN 1080p!")

if __name__ == "__main__":
    main()
