#!/usr/bin/env python3
"""
Automated live screen recorder for Databricks Unity Catalog (Video 1)
and Databricks DLT Pipeline (Video 2) using x11grab and opencli.
Produces 1080p 60fps raw videos saved to:
  data/video/raw/live_databricks_catalog.webm
  data/video/raw/live_databricks_dlt.webm
"""
import os
import signal
import subprocess
import time
from pathlib import Path

RAW_DIR = Path("/home/shaun/Projects/the-agentic-ea/data/video/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

WINDOW_ID = "0x04600020"

def focus_window():
    print("  -> Focusing and sizing Chrome window to 1920x1080...")
    subprocess.run(f"wmctrl -i -a {WINDOW_ID}", shell=True)
    subprocess.run(f"wmctrl -i -r {WINDOW_ID} -e 0,0,0,1920,1080", shell=True)
    time.sleep(1)


def record_video1_catalog():
    print("\n=======================================================")
    print("🎬 RECORDING VIDEO 1: DATABRICKS UNITY CATALOG")
    print("=======================================================")
    focus_window()
    
    # Pre-navigate to ensure connection is hot
    subprocess.run("opencli browser ea open 'https://dbc-2d6963b0-153b.cloud.databricks.com/explore/data/ea'", shell=True)
    time.sleep(3)
    
    raw_mp4 = "/tmp/raw_live_catalog.mp4"
    if os.path.exists(raw_mp4):
        os.remove(raw_mp4)
        
    # Start ffmpeg x11grab
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "x11grab",
        "-draw_mouse", "1",
        "-framerate", "30",
        "-video_size", "1920x1080",
        "-i", ":0.0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        raw_mp4
    ]
    
    print("  -> Starting FFmpeg live grab...")
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    
    try:
        # Step 1: Navigate to catalog ea
        print("  -> Navigating to catalog ea...")
        subprocess.run("opencli browser ea open 'https://dbc-2d6963b0-153b.cloud.databricks.com/explore/data/ea'", shell=True)
        time.sleep(3.5)
        
        # Step 2: Click and expand catalog metamodel
        print("  -> Clicking metamodel schema...")
        subprocess.run("opencli browser ea click \"a[aria-label='metamodel'][role='treeitem']\"", shell=True)
        time.sleep(2.5)
        
        # Step 3: Click nodes table
        print("  -> Clicking nodes table...")
        subprocess.run("opencli browser ea click \"a[aria-label='nodes'][role='treeitem']\"", shell=True)
        time.sleep(3.0)
        
        # Step 4: Show Overview (conformed schema)
        print("  -> Showing conformed schema columns...")
        subprocess.run("opencli browser ea click \"button[id*='trigger-overview']\"", shell=True)
        time.sleep(3.5)
        
        # Step 5: Click Sample Data tab
        print("  -> Clicking Sample Data tab to show live data rows...")
        subprocess.run("opencli browser ea click \"button[id*='trigger-sample']\"", shell=True)
        time.sleep(5.0)
        
    finally:
        print("  -> Stopping FFmpeg...")
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            
    # Transcode to webm
    target_webm = RAW_DIR / "live_databricks_catalog.webm"
    print(f"  -> Transcoding to webm: {target_webm}...")
    transcode_cmd = (
        f"ffmpeg -y -i {raw_mp4} -vf 'fps=30,scale=1920:1080:flags=lanczos' "
        f"-c:v libvpx-vp9 -b:v 4M -pix_fmt yuv420p {target_webm}"
    )
    subprocess.run(transcode_cmd, shell=True, check=True)
    print(f"  ✓ Saved: {target_webm} ({target_webm.stat().st_size / 1024:.1f} KB)")


def record_video2_dlt():
    print("\n=======================================================")
    print("🎬 RECORDING VIDEO 2: DATABRICKS DLT PIPELINE")
    print("=======================================================")
    focus_window()
    
    # Pre-navigate to ensure connection is hot
    subprocess.run("opencli browser ea open 'https://dbc-2d6963b0-153b.cloud.databricks.com/pipelines/901138d7-92e5-4c26-b3a7-133ed7dd5f53'", shell=True)
    time.sleep(3)
    
    raw_mp4 = "/tmp/raw_live_dlt.mp4"
    if os.path.exists(raw_mp4):
        os.remove(raw_mp4)
        
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "x11grab",
        "-draw_mouse", "1",
        "-framerate", "30",
        "-video_size", "1920x1080",
        "-i", ":0.0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        raw_mp4
    ]
    
    print("  -> Starting FFmpeg live grab...")
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    
    try:
        # Step 1: Open pipeline DAG
        print("  -> Navigating to DLT Medallion Pipeline...")
        subprocess.run("opencli browser ea open 'https://dbc-2d6963b0-153b.cloud.databricks.com/pipelines/901138d7-92e5-4c26-b3a7-133ed7dd5f53'", shell=True)
        time.sleep(4.0)
        
        # Step 2: Pan/hover across bronze sources
        print("  -> Hovering across bronze feed sources...")
        subprocess.run("opencli browser ea hover \"div[data-testid*='cloud_resources']\"", shell=True)
        time.sleep(2.0)
        
        # Step 3: Click silver_nodes to show expectations and record counts
        print("  -> Clicking silver_nodes...")
        subprocess.run("opencli browser ea click \"div[aria-label='silver_nodes']\"", shell=True)
        time.sleep(4.0)
        
        # Step 4: Click gold_time_matrix to show expectations and record counts
        print("  -> Clicking gold_time_matrix...")
        subprocess.run("opencli browser ea click \"div[aria-label='gold_time_matrix']\"", shell=True)
        time.sleep(4.5)
        
    finally:
        print("  -> Stopping FFmpeg...")
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            
    # Transcode to webm
    target_webm = RAW_DIR / "live_databricks_dlt.webm"
    print(f"  -> Transcoding to webm: {target_webm}...")
    transcode_cmd = (
        f"ffmpeg -y -i {raw_mp4} -vf 'fps=30,scale=1920:1080:flags=lanczos' "
        f"-c:v libvpx-vp9 -b:v 4M -pix_fmt yuv420p {target_webm}"
    )
    subprocess.run(transcode_cmd, shell=True, check=True)
    print(f"  ✓ Saved: {target_webm} ({target_webm.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    record_video1_catalog()
    record_video2_dlt()
