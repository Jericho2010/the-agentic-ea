#!/usr/bin/env python3
"""
Test recording Scene 1: Databricks Apps Overview
"""
import os
import signal
import subprocess
import time
from pathlib import Path

RAW_DIR = Path("/home/shaun/Projects/the-agentic-ea/data/video/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
WINDOW_ID = "0x03200004"

def record_scene1():
    print("Preparing Scene 1: Databricks Apps Overview...")
    subprocess.run(f"wmctrl -i -a {WINDOW_ID}", shell=True)
    subprocess.run(f"wmctrl -i -r {WINDOW_ID} -e 0,0,0,1920,1080", shell=True)
    time.sleep(1)
    
    # Navigate
    url = "https://dbc-2d6963b0-153b.cloud.databricks.com/apps-v2/app/ea-navigator-cockpit/overview?o=3671477545521222"
    subprocess.run(f"opencli browser ea open '{url}'", shell=True)
    time.sleep(3)
    
    out_file = RAW_DIR / "test_scene1.mp4"
    if out_file.exists():
        out_file.unlink()
        
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
        str(out_file)
    ]
    
    print("  -> Starting 60fps recording...")
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    try:
        # Hover over App Status / Running
        print("  -> Hovering over Running badge...")
        subprocess.run("opencli browser ea hover \"span:has-text('Running')\"", shell=True)
        time.sleep(3)
        
        # Hover over Compute
        print("  -> Hovering over Compute section...")
        subprocess.run("opencli browser ea hover \"h4:has-text('Compute')\"", shell=True)
        time.sleep(3)
        
        # Hover over live URL link
        print("  -> Hovering over live app URL...")
        subprocess.run("opencli browser ea hover \"a[href*='aws.databricksapps.com']\"", shell=True)
        time.sleep(4)
        
    finally:
        print("  -> Stopping FFmpeg...")
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            
    print(f"✓ Scene 1 recorded: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    record_scene1()
