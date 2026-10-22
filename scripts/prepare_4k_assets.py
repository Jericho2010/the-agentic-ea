#!/usr/bin/env python3
"""
Capture ultra-high-resolution 4K (3840x2160) master assets for all scenes
using Playwright with device_scale_factor=2 from local server http://127.0.0.1:8088.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS_DIR = Path("data/video/assets")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:8088"

SCENES_TO_CAPTURE = {
    "scene1_4k.png": f"{BASE_URL}/scene1_shelfware_trap.html",
    "scene4_4k.png": f"{BASE_URL}/scene4_sentinel_pr.html",
    "scene5_4k.png": f"{BASE_URL}/scene5_executive_time_drawer.html",
    "scene6_4k.png": f"{BASE_URL}/scene6_hero_launch.html",
}

def capture_4k_assets():
    print("Capturing 4K UHD assets with Playwright (device_scale_factor=2)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)

        for filename, url in SCENES_TO_CAPTURE.items():
            print(f"  -> Loading {url}...")
            page.goto(url)
            page.wait_for_timeout(1000)
            out_path = ASSETS_DIR / filename
            page.screenshot(path=str(out_path))
            print(f"  ✓ Saved 4K master: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

        browser.close()
    print("All 4K master assets successfully prepared.")

if __name__ == "__main__":
    capture_4k_assets()
