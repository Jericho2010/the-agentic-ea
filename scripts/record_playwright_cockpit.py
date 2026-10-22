#!/usr/bin/env python3
"""
Record live screen actions for Videos 3, 4, and 5 using Playwright.
Saves raw webm video directly to data/video/raw/
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

RAW_DIR = Path("/home/shaun/Projects/the-agentic-ea/data/video/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "http://127.0.0.1:8088"

def record_video3():
    print("\n--- RECORDING VIDEO 3: ARCHIFY LIVING ARCHITECTURE ---")
    temp_dir = RAW_DIR / "temp_v3"
    temp_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"]
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(temp_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = ctx.new_page()
        page.goto(BASE_URL)
        page.wait_for_selector("aside", timeout=15000)
        time.sleep(2)
        
        # Navigate to Engineering Modernization
        print("  -> Clicking Engineering Modernization...")
        page.click("button:has-text('Engineering Modernization')")
        time.sleep(3)
        
        # Select Blast Radius diagram
        print("  -> Selecting Blast Radius diagram...")
        blast_btn = page.locator("button:has-text('Blast Radius')").first
        if blast_btn.count() > 0:
            blast_btn.click()
            time.sleep(3)
            
        # Hover inside iframe if present
        iframe = page.locator("iframe").first
        if iframe.count() > 0:
            print("  -> Interacting with Archify Living Map...")
            box = iframe.bounding_box()
            if box:
                # Top ingress
                page.mouse.move(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.25)
                time.sleep(2)
                # Middle tier (payments-api)
                page.mouse.move(box["x"] + box["width"] * 0.45, box["y"] + box["height"] * 0.5)
                page.mouse.click(box["x"] + box["width"] * 0.45, box["y"] + box["height"] * 0.5)
                time.sleep(2)
                # Trace down to cassandra
                page.mouse.move(box["x"] + box["width"] * 0.55, box["y"] + box["height"] * 0.75)
                page.mouse.click(box["x"] + box["width"] * 0.55, box["y"] + box["height"] * 0.75)
                time.sleep(3)
        
        time.sleep(2)
        page.close()
        ctx.close()
        browser.close()
        
    # Move recorded webm
    recorded = list(temp_dir.glob("*.webm"))
    if recorded:
        target = RAW_DIR / "live_archify_diagram.webm"
        if target.exists():
            target.unlink()
        recorded[0].rename(target)
        print(f"  ✓ Saved: {target} ({target.stat().st_size / 1024:.1f} KB)")
    for f in temp_dir.glob("*"):
        f.unlink()
    temp_dir.rmdir()


def record_video4():
    print("\n--- RECORDING VIDEO 4: SENTINEL PR SIMULATOR ---")
    temp_dir = RAW_DIR / "temp_v4"
    temp_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"]
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(temp_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = ctx.new_page()
        page.goto(BASE_URL)
        page.wait_for_selector("aside", timeout=15000)
        time.sleep(2)
        
        # Navigate to Sentinel Governance
        print("  -> Clicking Sentinel Governance...")
        page.click("button:has-text('Sentinel Governance')")
        time.sleep(2.5)
        
        # Select Cassandra sample patch
        print("  -> Selecting Cassandra sample patch...")
        cass_btn = page.locator("button:has-text('Deprecated Cassandra 3.11')").first
        if cass_btn.count() > 0:
            cass_btn.click()
            time.sleep(2)
            
        # Click Simulate Evaluation
        print("  -> Clicking Simulate Evaluation...")
        page.click("button:has-text('Simulate Evaluation')")
        time.sleep(4)
        
        # Scroll down to policy cards and automated GitHub PR comment
        print("  -> Scrolling down to policy receipt and PR comment...")
        page.mouse.wheel(0, 480)
        time.sleep(3.5)
        page.mouse.wheel(0, 200)
        time.sleep(3.5)
        
        page.close()
        ctx.close()
        browser.close()
        
    recorded = list(temp_dir.glob("*.webm"))
    if recorded:
        target = RAW_DIR / "live_sentinel_pr.webm"
        if target.exists():
            target.unlink()
        recorded[0].rename(target)
        print(f"  ✓ Saved: {target} ({target.stat().st_size / 1024:.1f} KB)")
    for f in temp_dir.glob("*"):
        f.unlink()
    temp_dir.rmdir()


def record_video5():
    print("\n--- RECORDING VIDEO 5: 2D TIME MATRIX & 520px DRAWER ---")
    temp_dir = RAW_DIR / "temp_v5"
    temp_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"]
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(temp_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = ctx.new_page()
        page.goto(BASE_URL)
        page.wait_for_selector("aside", timeout=15000)
        time.sleep(2)
        
        # Hover over 2D TIME Matrix bubbles
        print("  -> Hovering over 2D TIME Matrix bubbles...")
        page.mouse.move(720, 360)
        time.sleep(1.5)
        page.mouse.move(1080, 340)
        time.sleep(1.5)
        page.mouse.move(950, 450)
        time.sleep(1.5)
        
        # Click payments-api-compute in table to open drawer
        print("  -> Clicking row to open 520px Slide-Over Drawer...")
        row = page.locator("tbody tr:has-text('payments-api-compute')").first
        if row.count() > 0:
            row.click()
            time.sleep(2.5)
        else:
            # Fallback to first row
            page.locator("tbody tr").first.click()
            time.sleep(2.5)
            
        # Cycle drawer tabs: Lineage -> Governance -> Raw JSON
        print("  -> Cycling drawer tabs...")
        page.click("button:has-text('Lineage & Graph')")
        time.sleep(2)
        page.click("button:has-text('Governance & Rules')")
        time.sleep(2)
        page.click("button:has-text('Raw JSON')")
        time.sleep(2.5)
        
        # Close drawer with Escape
        print("  -> Closing drawer with Escape...")
        page.keyboard.press("Escape")
        time.sleep(1.5)
        
        # Trigger Command Palette (Ctrl+K)
        print("  -> Triggering Command Palette (Ctrl+K)...")
        page.keyboard.press("Control+k")
        time.sleep(1.5)
        
        search_input = page.locator("input[placeholder*='Search applications']")
        if search_input.count() > 0:
            search_input.type("cassandra", delay=120)
            time.sleep(2.5)
            
        # Dismiss with Escape
        print("  -> Dismissing Command Palette with Escape...")
        page.keyboard.press("Escape")
        time.sleep(2)
        
        page.close()
        ctx.close()
        browser.close()
        
    recorded = list(temp_dir.glob("*.webm"))
    if recorded:
        target = RAW_DIR / "live_time_matrix.webm"
        if target.exists():
            target.unlink()
        recorded[0].rename(target)
        print(f"  ✓ Saved: {target} ({target.stat().st_size / 1024:.1f} KB)")
    for f in temp_dir.glob("*"):
        f.unlink()
    temp_dir.rmdir()


if __name__ == "__main__":
    record_video3()
    record_video4()
    record_video5()
