#!/usr/bin/env python3
"""
Generate professional neural voiceovers for 'The Agentic EA' launch video.
Uses edge-tts with en-US-ChristopherNeural (authoritative, clear executive tone).
"""
import asyncio
import os
from pathlib import Path
import edge_tts

VOICE = "en-US-ChristopherNeural"
RATE = "+4%"

SCENES = {
    "scene1": (
        "There's a quiet failure mode in Enterprise Architecture: confusing the diagram with the system. "
        "While teams spend six figures on passive diagram catalogs, cloud infrastructure silently drifts."
    ),
    "scene2": (
        "Shift one: Metamodel as Data, Not Diagrams. "
        "Instead of an isolated SaaS silo, architecture lives directly on the Lakehouse. "
        "Git ASTs, Cloud CUR billing, and CMDB records stream into conformed Medallion Delta tables in Databricks Unity Catalog."
    ),
    "scene3": (
        "Shift two: Governance in the PR Flow. "
        "If architecture only gets evaluated at a monthly committee meeting, it's already too late. "
        "Autonomous pre-merge AI gates evaluate infrastructure diffs before code merges."
    ),
    "scene4": (
        "Shift three: Live Estate Intelligence and Blast Radius. "
        "Answering 'What is our financial exposure if this service is sunset?' or 'Where does PII cross DORA boundaries?' "
        "isn't a four-week consulting engagement. It's a graph traversal computed in milliseconds."
    ),
    "scene5": (
        "Shift four: Real Executive Value. "
        "Leadership doesn't need 500-box UML drawings. "
        "They need actionable portfolio governance: an interactive 2D TIME matrix plotted on business value versus technical debt, "
        "tied to live cloud run costs."
    ),
    "scene6": (
        "When architecture runs as code and live data, it stops being shelfware—and starts actively accelerating engineering velocity. "
        "Closing the loop between executive strategy and raw commit diffs."
    )
}

async def generate_all():
    out_dir = Path("data/video/audio")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for scene_id, text in SCENES.items():
        out_file = out_dir / f"{scene_id}.mp3"
        print(f"Generating voiceover for {scene_id}...")
        comm = edge_tts.Communicate(text, VOICE, rate=RATE)
        await comm.save(str(out_file))
        print(f"  ✓ Saved {out_file}")

if __name__ == "__main__":
    asyncio.run(generate_all())
