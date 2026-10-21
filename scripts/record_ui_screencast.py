#!/usr/bin/env python3
"""
Playwright live screencast recorder for The Agentic EA.
Records 1920x1080 60fps webm screencasts of live UI interactions
on https://ea-navigator-cockpit-3671477545521222.aws.databricksapps.com
"""
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

RAW_DIR = Path("data/video/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

APP_URL = "https://ea-navigator-cockpit-3671477545521222.aws.databricksapps.com"

def record_ui_interactions():
    print(f"Starting Playwright browser targeting {APP_URL}...")
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
            record_video_dir=str(RAW_DIR),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        print("Navigating to live Databricks App...")
        page.goto(APP_URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)

        # ----------------------------------------------------------------------
        # SCENE A: Executive Workspace & 2D TIME Matrix & Entity Inspector Drawer
        # ----------------------------------------------------------------------
        print("Recording 2D TIME Matrix interactions...")
        
        # Smooth mouse move over Executive KPI ribbon
        page.mouse.move(350, 140)
        page.wait_for_timeout(1000)
        page.mouse.move(700, 140)
        page.wait_for_timeout(1000)

        # Hover over 2D TIME Matrix bubbles
        # payments-api-compute bubble
        print("Hovering over payments-api-compute bubble...")
        bubble_payments = page.locator("div:has-text('payments')").last
        if bubble_payments.count() > 0:
            box = bubble_payments.bounding_box()
            if box:
                page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                page.wait_for_timeout(2000)
        
        # Hover over cassandra-legacy-nodes
        print("Hovering over cassandra bubble...")
        bubble_cass = page.locator("div:has-text('cassandra')").last
        if bubble_cass.count() > 0:
            box = bubble_cass.bounding_box()
            if box:
                page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                page.wait_for_timeout(2000)

        # Click payments bubble to open Slide-Over Entity Inspector Drawer (w-[520px])
        print("Clicking bubble to trigger slide-over Entity Inspector Drawer...")
        row_target = page.locator("tbody tr:has-text('payments-api-compute')").first
        if row_target.count() > 0:
            row_target.click()
        else:
            page.locator("span:has-text('payments')").first.click()
        page.wait_for_timeout(3000)

        # Drawer Tab cycling: Overview -> Lineage -> Governance -> Raw JSON
        print("Cycling drawer tabs...")
        page.click("button:has-text('Lineage & Graph')")
        page.wait_for_timeout(2000)

        page.click("button:has-text('Governance & Rules')")
        page.wait_for_timeout(2000)

        page.click("button:has-text('Raw JSON')")
        page.wait_for_timeout(2500)

        # Close drawer with Escape
        print("Dismissing drawer with Escape key...")
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)

        # ----------------------------------------------------------------------
        # SCENE B: Command Palette (Cmd+K) & Fuzzy Search
        # ----------------------------------------------------------------------
        print("Triggering Command Palette (⌘K)...")
        # Click search trigger in top bar
        page.click("button:has-text('Search applications')")
        page.wait_for_timeout(1500)

        # Type 'cassandra'
        print("Typing 'cassandra' in command palette...")
        search_input = page.locator("input[placeholder*='Search applications']")
        search_input.type("cassandra", delay=120)
        page.wait_for_timeout(2000)

        # Press Escape to close Command Palette
        page.keyboard.press("Escape")
        page.wait_for_timeout(1500)

        # ----------------------------------------------------------------------
        # SCENE C: Sentinel Pre-Merge PR Policy Simulator
        # ----------------------------------------------------------------------
        print("Navigating to Sentinel Governance workspace...")
        page.click("button:has-text('Sentinel Governance')")
        page.wait_for_timeout(3000)

        # Select sample scenario: Cassandra with PII
        print("Selecting Cassandra PR scenario...")
        page.click("button:has-text('Deprecated Cassandra 3.11')")
        page.wait_for_timeout(1500)

        # Click Simulate Evaluation
        print("Clicking Simulate Evaluation...")
        page.click("button:has-text('Simulate Evaluation')")
        page.wait_for_timeout(3500)

        # Scroll down to policy cards and ARB ledger
        print("Scrolling Sentinel policy ledger...")
        page.mouse.wheel(0, 450)
        page.wait_for_timeout(2000)
        page.mouse.wheel(0, -450)
        page.wait_for_timeout(1000)

        # ----------------------------------------------------------------------
        # SCENE D: Engineering Modernization & Archify Living Maps
        # ----------------------------------------------------------------------
        print("Navigating to Engineering Modernization workspace...")
        page.click("button:has-text('Engineering Modernization')")
        page.wait_for_timeout(3000)

        # Switch diagram perspectives
        print("Selecting Blast Radius diagram...")
        blast_btn = page.locator("button:has-text('Blast Radius')").first
        if blast_btn.count() > 0:
            blast_btn.click()
            page.wait_for_timeout(3000)

        print("Selecting GDPR DORA Lineage diagram...")
        gdpr_btn = page.locator("button:has-text('Gdpr Dora Lineage')").first
        if gdpr_btn.count() > 0:
            gdpr_btn.click()
            page.wait_for_timeout(3000)

        # Switch to Conformed PAM Metamodel Explorer tab
        print("Switching to PAM Metamodel Explorer...")
        page.click("button:has-text('Conformed PAM Metamodel Explorer')")
        page.wait_for_timeout(2000)

        # Scroll PAM table
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(1500)
        page.mouse.wheel(0, -300)
        page.wait_for_timeout(1000)

        # ----------------------------------------------------------------------
        # SCENE E: Operations & FinOps (CMDB Drift Console)
        # ----------------------------------------------------------------------
        print("Navigating to Operations & FinOps workspace...")
        page.click("button:has-text('Operations & FinOps')")
        page.wait_for_timeout(3000)

        # Scroll side-by-side reconciliation table
        print("Scrolling CMDB reconciliation console...")
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(2000)
        page.mouse.wheel(0, -350)
        page.wait_for_timeout(1000)

        # Click Sync CMDB in top bar
        print("Clicking Sync CMDB action...")
        page.click("button:has-text('Sync CMDB')")
        page.wait_for_timeout(2500)

        # Back to Executive Workspace
        print("Returning to Executive & Strategy workspace...")
        page.click("button:has-text('Executive & Strategy')")
        page.wait_for_timeout(2500)

        print("Finishing recording...")
        page.close()
        context.close()
        browser.close()

    print("Playwright UI screencast recording complete.")

if __name__ == "__main__":
    record_ui_interactions()
