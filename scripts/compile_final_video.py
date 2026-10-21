#!/usr/bin/env python3
"""
Compile the official 1080p 60fps MP4 product demo video for 'The Agentic EA'.
Applies 60fps conform, speed adjustments, transparent caption overlays,
and clean concatenation into data/video/the_agentic_ea_launch.mp4.
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/shaun/Projects/the-agentic-ea")
RAW_DIR = PROJECT_ROOT / "data/video/raw"
OVERLAYS_DIR = PROJECT_ROOT / "data/video/overlays"
INTER_DIR = PROJECT_ROOT / "data/video/intermediate"
INTER_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = PROJECT_ROOT / "data/video/the_agentic_ea_launch.mp4"

def run_cmd(cmd, desc):
    print(f"\n▶ {desc}...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error in {desc}:")
        print(res.stderr)
        sys.exit(1)
    print(f"  ✓ {desc} completed successfully.")

def build_scene1():
    # Scene 1: 15.0s, no overlay needed (already in page)
    cmd = (
        f"ffmpeg -y -i {RAW_DIR}/scene1.webm "
        f"-vf 'fps=60,scale=1920:1080:flags=lanczos,format=yuv420p' "
        f"-t 15.0 -c:v libx264 -preset slow -crf 18 -r 60 "
        f"{INTER_DIR}/scene1_conformed.mp4"
    )
    run_cmd(cmd, "Processing Scene 1 (The Trap, 15.0s)")

def build_scene2():
    # Scene 2: 20.0s, no overlay needed (already in page)
    cmd = (
        f"ffmpeg -y -i {RAW_DIR}/scene2.webm "
        f"-vf 'fps=60,scale=1920:1080:flags=lanczos,format=yuv420p' "
        f"-t 20.0 -c:v libx264 -preset slow -crf 18 -r 60 "
        f"{INTER_DIR}/scene2_conformed.mp4"
    )
    run_cmd(cmd, "Processing Scene 2 (Shift 1: Lakehouse Data & DLT, 20.0s)")

def build_scene3():
    # Scene 3: Raw 36.2s -> Target 20.0s (speedup 1.81x) with scene3_overlay.png
    cmd = (
        f"ffmpeg -y -i {RAW_DIR}/scene3.webm -i {OVERLAYS_DIR}/scene3_overlay.png "
        f"-filter_complex '[0:v]setpts=(20.0/36.2)*(PTS-STARTPTS),fps=60,scale=1920:1080:flags=lanczos[base];"
        f"[base][1:v]overlay=0:0,format=yuv420p[out]' "
        f"-map '[out]' -t 20.0 -c:v libx264 -preset slow -crf 18 -r 60 "
        f"{INTER_DIR}/scene3_conformed.mp4"
    )
    run_cmd(cmd, "Processing Scene 3 (Shift 2: Governance in PR Flow, 20.0s)")

def build_scene4():
    # Scene 4: Raw 20.84s -> Target 20.0s with scene4_overlay.png
    cmd = (
        f"ffmpeg -y -i {RAW_DIR}/scene4.webm -i {OVERLAYS_DIR}/scene4_overlay.png "
        f"-filter_complex '[0:v]setpts=(20.0/20.84)*(PTS-STARTPTS),fps=60,scale=1920:1080:flags=lanczos[base];"
        f"[base][1:v]overlay=0:0,format=yuv420p[out]' "
        f"-map '[out]' -t 20.0 -c:v libx264 -preset slow -crf 18 -r 60 "
        f"{INTER_DIR}/scene4_conformed.mp4"
    )
    run_cmd(cmd, "Processing Scene 4 (Shift 3: Estate Intelligence & Blast Radius, 20.0s)")

def build_scene5():
    # Scene 5: Raw 52.28s -> Target 26.0s (speedup 2.01x) with scene5_overlay.png
    cmd = (
        f"ffmpeg -y -i {RAW_DIR}/scene5.webm -i {OVERLAYS_DIR}/scene5_overlay.png "
        f"-filter_complex '[0:v]setpts=(26.0/52.28)*(PTS-STARTPTS),fps=60,scale=1920:1080:flags=lanczos[base];"
        f"[base][1:v]overlay=0:0,format=yuv420p[out]' "
        f"-map '[out]' -t 26.0 -c:v libx264 -preset slow -crf 18 -r 60 "
        f"{INTER_DIR}/scene5_conformed.mp4"
    )
    run_cmd(cmd, "Processing Scene 5 (Shift 4: 2D TIME Matrix & Drawer, 26.0s)")

def build_scene6():
    # Scene 6: 15.0s, hero launch card
    cmd = (
        f"ffmpeg -y -i {RAW_DIR}/scene6.webm "
        f"-vf 'fps=60,scale=1920:1080:flags=lanczos,format=yuv420p' "
        f"-t 15.0 -c:v libx264 -preset slow -crf 18 -r 60 "
        f"{INTER_DIR}/scene6_conformed.mp4"
    )
    run_cmd(cmd, "Processing Scene 6 (The Payoff: Hero Launch Card, 15.0s)")

def concatenate_all():
    concat_list = INTER_DIR / "concat_list.txt"
    scenes = [
        "scene1_conformed.mp4",
        "scene2_conformed.mp4",
        "scene3_conformed.mp4",
        "scene4_conformed.mp4",
        "scene5_conformed.mp4",
        "scene6_conformed.mp4",
    ]
    with open(concat_list, "w") as f:
        for s in scenes:
            f.write(f"file '{INTER_DIR / s}'\n")

    cmd = (
        f"ffmpeg -y -f concat -safe 0 -i {concat_list} "
        f"-c:v libx264 -preset slow -crf 18 -r 60 -pix_fmt yuv420p "
        f"{OUT_FILE}"
    )
    run_cmd(cmd, f"Concatenating all scenes into master video ({OUT_FILE})")

def main():
    print("==================================================================")
    print("🎬 COMPILING MASTER 1080p 60fps MP4 PRODUCT LAUNCH VIDEO")
    print("==================================================================")
    build_scene1()
    build_scene2()
    build_scene3()
    build_scene4()
    build_scene5()
    build_scene6()
    concatenate_all()
    print("\n🎉 MASTER VIDEO COMPILATION COMPLETE!")
    print(f"Output File: {OUT_FILE}")

if __name__ == "__main__":
    main()
