#!/usr/bin/env python3
"""
Master Cinematography & Keynote Zoom Compiler for 'The Agentic EA' Launch Video.
Directorial Revision Mandate:
- NO SUBTITLES (0 ribbons, 0 text overlays)
- NO FAKE HTML MOCKS (100% real Databricks workspace + real live app)
- Keynote-style smooth optical punch-in zooms with cubic easing
- 1080p, 60.00 fps progressive CFR, no audio
- Final output: data/video/the_agentic_ea_launch.mp4
"""
import os
import subprocess
import time
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path("/home/shaun/Projects/the-agentic-ea")
RAW_DIR = PROJECT_ROOT / "data/video/raw"
INTER_DIR = PROJECT_ROOT / "data/video/intermediate"
INTER_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = PROJECT_ROOT / "data/video/the_agentic_ea_launch.mp4"

WIDTH = 1920
HEIGHT = 1080
FPS = 60
FRAME_SIZE = WIDTH * HEIGHT * 3

def smoothstep(edge0: float, edge1: float, x: float) -> float:
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

def process_scene_with_zoom(
    in_path: Path,
    out_path: Path,
    duration_sec: float,
    zoom_fn,
    desc: str
):
    print(f"\n🎬 {desc}...")
    total_frames = int(round(duration_sec * FPS))
    
    in_cmd = [
        "ffmpeg", "-y",
        "-i", str(in_path),
        "-t", str(duration_sec),
        "-f", "image2pipe",
        "-pix_fmt", "rgb24",
        "-vcodec", "rawvideo",
        "-r", str(FPS),
        "-"
    ]
    out_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        str(out_path)
    ]
    
    p_in = subprocess.Popen(in_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    p_out = subprocess.Popen(out_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    t0 = time.time()
    frame_idx = 0
    
    while frame_idx < total_frames:
        raw = p_in.stdout.read(FRAME_SIZE)
        if len(raw) < FRAME_SIZE:
            break
            
        t_sec = frame_idx / float(FPS)
        zoom, cx, cy = zoom_fn(t_sec, duration_sec)
        
        im = Image.frombytes("RGB", (WIDTH, HEIGHT), raw)
        
        if zoom > 1.001:
            crop_w = WIDTH / zoom
            crop_h = HEIGHT / zoom
            
            x0 = max(0.0, min(float(WIDTH) - crop_w, (cx * WIDTH) - (crop_w * 0.5)))
            y0 = max(0.0, min(float(HEIGHT) - crop_h, (cy * HEIGHT) - (crop_h * 0.5)))
            x1 = x0 + crop_w
            y1 = y0 + crop_h
            
            box = (int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))
            frame_processed = im.crop(box).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
        else:
            frame_processed = im
            
        p_out.stdin.write(frame_processed.tobytes())
        frame_idx += 1
        
    p_in.stdout.close()
    p_in.wait()
    p_out.stdin.close()
    p_out.wait()
    
    elapsed = time.time() - t0
    fps_actual = frame_idx / elapsed if elapsed > 0 else 0
    print(f"  ✓ {frame_idx} frames rendered in {elapsed:.1f}s ({fps_actual:.1f} fps) -> {out_path.name}")


# ----------------------------------------------------------------------
# Zoom Schedule Definitions
# ----------------------------------------------------------------------

def zoom_scene1(t: float, total: float):
    # Scene 1: Databricks Apps Overview (12.0s)
    # 0.0 - 2.0s: 1.0x wide
    # 2.0 - 5.5s: punch-in to 1.35x centered on Running badge & Compute (0.55, 0.38)
    # 5.5 - 9.0s: hold 1.35x
    # 9.0 - 12.0s: pull back to 1.0x
    if t < 2.0:
        return 1.0, 0.5, 0.5
    elif t < 5.5:
        p = smoothstep(2.0, 5.5, t)
        return 1.0 + 0.35 * p, 0.5 + 0.05 * p, 0.5 - 0.12 * p
    elif t < 9.0:
        return 1.35, 0.55, 0.38
    else:
        p = smoothstep(9.0, 12.0, t)
        return 1.35 - 0.35 * p, 0.55 - 0.05 * p, 0.38 + 0.12 * p


def zoom_scene2(t: float, total: float):
    # Scene 2: Databricks Unity Catalog Explorer (18.0s)
    # 0.0 - 3.0s: 1.0x wide (expanding metamodel and nodes)
    # 3.0 - 7.0s: punch-in to 1.45x centered on schema columns & sample rows (0.52, 0.55)
    # 7.0 - 15.0s: hold 1.45x on live conformed PAM nodes
    # 15.0 - 18.0s: pull back to 1.0x
    if t < 3.0:
        return 1.0, 0.5, 0.5
    elif t < 7.0:
        p = smoothstep(3.0, 7.0, t)
        return 1.0 + 0.45 * p, 0.5 + 0.02 * p, 0.5 + 0.05 * p
    elif t < 15.0:
        return 1.45, 0.52, 0.55
    else:
        p = smoothstep(15.0, 18.0, t)
        return 1.45 - 0.45 * p, 0.52 - 0.02 * p, 0.55 - 0.05 * p


def zoom_scene3(t: float, total: float):
    # Scene 3: Databricks DLT Medallion Pipeline (17.0s)
    # 0.0 - 2.5s: 1.0x wide
    # 2.5 - 6.5s: punch-in to 1.40x on silver_nodes & expectations (0.62, 0.45)
    # 6.5 - 13.5s: track across to gold_time_matrix (0.70, 0.45)
    # 13.5 - 17.0s: pull back to 1.0x
    if t < 2.5:
        return 1.0, 0.5, 0.5
    elif t < 6.5:
        p = smoothstep(2.5, 6.5, t)
        return 1.0 + 0.40 * p, 0.5 + 0.12 * p, 0.5 - 0.05 * p
    elif t < 13.5:
        p = smoothstep(6.5, 13.5, t)
        return 1.40, 0.62 + 0.08 * p, 0.45
    else:
        p = smoothstep(13.5, 17.0, t)
        return 1.40 - 0.40 * p, 0.70 - 0.20 * p, 0.45 + 0.05 * p


def zoom_scene4(t: float, total: float):
    # Scene 4: Archify Living Map in Live App (18.0s)
    # 0.0 - 3.0s: 1.0x wide
    # 3.0 - 7.5s: punch-in to 1.50x on payments-api (0.48, 0.50)
    # 7.5 - 14.5s: trace down vector line to cassandra (0.55, 0.68)
    # 14.5 - 18.0s: pull back to 1.0x
    if t < 3.0:
        return 1.0, 0.5, 0.5
    elif t < 7.5:
        p = smoothstep(3.0, 7.5, t)
        return 1.0 + 0.50 * p, 0.5 - 0.02 * p, 0.50
    elif t < 14.5:
        p = smoothstep(7.5, 14.5, t)
        return 1.50, 0.48 + 0.07 * p, 0.50 + 0.18 * p
    else:
        p = smoothstep(14.5, 18.0, t)
        return 1.50 - 0.50 * p, 0.55 - 0.05 * p, 0.68 - 0.18 * p


def zoom_scene5(t: float, total: float):
    # Scene 5: Sentinel PR Policy Simulator in Live App (19.0s)
    # 0.0 - 2.5s: 1.0x wide
    # 2.5 - 6.5s: punch-in to 1.45x on instant red BLOCKED badge (0.74, 0.28)
    # 6.5 - 15.0s: tracks down with page scroll into PR bot comment ($235k blast radius) (0.50, 0.58)
    # 15.0 - 19.0s: pull back to 1.0x
    if t < 2.5:
        return 1.0, 0.5, 0.5
    elif t < 6.5:
        p = smoothstep(2.5, 6.5, t)
        return 1.0 + 0.45 * p, 0.5 + 0.24 * p, 0.5 - 0.22 * p
    elif t < 15.0:
        p = smoothstep(6.5, 15.0, t)
        return 1.45, 0.74 - 0.24 * p, 0.28 + 0.30 * p
    else:
        p = smoothstep(15.0, 19.0, t)
        return 1.45 - 0.45 * p, 0.50, 0.58 - 0.08 * p


def zoom_scene6(t: float, total: float):
    # Scene 6: Executive 2D TIME Matrix & 520px Drawer in Live App (24.0s)
    # 0.0 - 3.0s: 1.0x wide (Cartesian bubbles)
    # 3.0 - 6.5s: tracks right as 520px drawer glides open (1.35x, 0.72, 0.50)
    # 6.5 - 16.5s: holds on drawer tab cycling (Lineage, Rules, Raw JSON)
    # 16.5 - 20.0s: pulls back to 1.0x as Command Palette opens
    # 20.0 - 24.0s: holds on filtered search results & clean dismiss
    if t < 3.0:
        return 1.0, 0.5, 0.5
    elif t < 6.5:
        p = smoothstep(3.0, 6.5, t)
        return 1.0 + 0.35 * p, 0.5 + 0.22 * p, 0.50
    elif t < 16.5:
        return 1.35, 0.72, 0.50
    elif t < 20.0:
        p = smoothstep(16.5, 20.0, t)
        return 1.35 - 0.35 * p, 0.72 - 0.22 * p, 0.50
    else:
        return 1.0, 0.5, 0.5


def concatenate_master():
    print("\n🎬 CONCATENATING MASTER VIDEO...")
    concat_txt = INTER_DIR / "master_concat_list.txt"
    scenes = [
        "scene1_cinematic.mp4",
        "scene2_cinematic.mp4",
        "scene3_cinematic.mp4",
        "scene4_cinematic.mp4",
        "scene5_cinematic.mp4",
        "scene6_cinematic.mp4",
    ]
    with open(concat_txt, "w") as f:
        for s in scenes:
            f.write(f"file '{(INTER_DIR / s).resolve()}'\n")
            
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(OUT_FILE)
    ]
    subprocess.run(concat_cmd, check=True)
    print(f"\n🎉 MASTER DELIVERABLE READY: {OUT_FILE}")
    print(f"   Size: {OUT_FILE.stat().st_size / (1024*1024):.2f} MB")


def main():
    print("=================================================================")
    print("🚀 COMPILING TAKE 3 MASTER: THE AGENTIC EA (REAL WORKSPACE + APP)")
    print("=================================================================")
    
    process_scene_with_zoom(
        RAW_DIR / "scene1_apps_overview.mp4",
        INTER_DIR / "scene1_cinematic.mp4",
        12.0,
        zoom_scene1,
        "Scene 1: Databricks Apps Overview (12.0s, Running & Compute Punch-in)"
    )
    
    process_scene_with_zoom(
        RAW_DIR / "scene2_unity_catalog.mp4",
        INTER_DIR / "scene2_cinematic.mp4",
        18.0,
        zoom_scene2,
        "Scene 2: Databricks Unity Catalog Explorer (18.0s, Metamodel & Sample Rows)"
    )
    
    process_scene_with_zoom(
        RAW_DIR / "scene3_dlt_pipeline.mp4",
        INTER_DIR / "scene3_cinematic.mp4",
        17.0,
        zoom_scene3,
        "Scene 3: Databricks DLT Medallion Pipeline (17.0s, DAG & Expectations)"
    )
    
    process_scene_with_zoom(
        RAW_DIR / "scene4_archify_diagram.mp4",
        INTER_DIR / "scene4_cinematic.mp4",
        18.0,
        zoom_scene4,
        "Scene 4: Live App - Archify Living Map (18.0s, Vector Blast Radius Trace)"
    )
    
    process_scene_with_zoom(
        RAW_DIR / "scene5_sentinel_pr.mp4",
        INTER_DIR / "scene5_cinematic.mp4",
        19.0,
        zoom_scene5,
        "Scene 5: Live App - Sentinel PR Policy Simulator (19.0s, Instant BLOCKED & Bot Receipt)"
    )
    
    process_scene_with_zoom(
        RAW_DIR / "scene6_time_matrix_drawer.mp4",
        INTER_DIR / "scene6_cinematic.mp4",
        24.0,
        zoom_scene6,
        "Scene 6: Live App - Executive 2D TIME Matrix (24.0s, 520px Drawer & Cmd+K)"
    )
    
    concatenate_master()


if __name__ == "__main__":
    main()
