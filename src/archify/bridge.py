"""
PAM to Archify Bridge.
Converts Platform Architecture Metamodel (PAM) graphs into typed Archify architecture diagrams.
Compiles interactive HTML and standalone styled vector SVG living maps via Archify CLI.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ARCHIFY_CLI = Path("/home/shaun/.agents/skills/archify/bin/archify.mjs")

KIND_TO_ARCHIFY_TYPE = {
    "Application": "frontend",
    "Microservice": "backend",
    "Database": "database",
    "CloudResource": "cloud",
    "APIInterface": "external",
    "BusinessCapability": "security",
    "AIModel": "backend",
}


def sanitize_id(urn_or_name: str) -> str:
    """Convert URN or name to valid Archify id pattern ^[a-z0-9_-]+$."""
    slug = urn_or_name.split(":")[-1]
    cleaned = re.sub(r"[^a-z0-9_-]", "-", slug.lower())
    return cleaned.strip("-") or "node"


def build_archify_spec(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    title: str = "Enterprise Architecture Living Map",
    subtitle: str = "Databricks Unity Catalog Conformed Metamodel Topology",
    output_html_rel: str = "architecture-view.html",
    highlight_urns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Compile PAM nodes and edges into strict Archify architecture specification."""
    highlight_set = set(highlight_urns or [])

    # Group components by layer/kind for deterministic layout
    layer_order = ["Application", "Microservice", "Database", "CloudResource", "APIInterface"]
    layers: Dict[str, List[Dict[str, Any]]] = {k: [] for k in layer_order}
    for n in nodes:
        kind = n.get("kind", "Microservice")
        if kind not in layers:
            layers[kind] = []
        layers[kind].append(n)

    components = []
    boundaries = []
    connections = []

    # Layout coordinates: row by layer, col within layer
    start_y = 60
    row_height = 180
    col_width = 280
    start_x = 60
    max_cols_per_row = 3

    app_wraps = []
    service_wraps = []
    data_wraps = []

    current_layer_row = 0
    node_id_map: Dict[str, str] = {}

    for kind in layer_order:
        layer_nodes = layers.get(kind, [])
        if not layer_nodes:
            continue

        for idx, node in enumerate(layer_nodes):
            urn = node["urn"]
            cid = sanitize_id(urn)
            node_id_map[urn] = cid

            col_idx = idx % max_cols_per_row
            row_within_layer = idx // max_cols_per_row
            x = start_x + (col_idx * col_width)
            y = start_y + ((current_layer_row + row_within_layer) * row_height)
            is_highlighted = (urn in highlight_set) or (node.get("name") in highlight_set)

            tag = node.get("criticality", "Tier-2")
            if is_highlighted:
                tag = "VIOLATION"

            comp_type = KIND_TO_ARCHIFY_TYPE.get(kind, "backend")
            sublabel = f"{node.get('owner_team', 'unassigned')} • {node.get('lifecycle_status', 'run')}"

            comp = {
                "id": cid,
                "type": comp_type,
                "label": node["name"],
                "sublabel": sublabel,
                "tag": tag,
                "pos": [x, y],
                "size": [190, 60],
            }
            components.append(comp)

            # Assign to boundaries
            if kind == "Application":
                app_wraps.append(cid)
            elif kind == "Microservice":
                service_wraps.append(cid)
            elif kind in ("Database", "CloudResource", "APIInterface"):
                data_wraps.append(cid)

        rows_consumed = ((len(layer_nodes) - 1) // max_cols_per_row) + 1
        current_layer_row += rows_consumed

    if app_wraps:
        boundaries.append({
            "kind": "region",
            "label": "Ingress & Edge Applications",
            "wraps": app_wraps,
        })
    if service_wraps:
        boundaries.append({
            "kind": "region",
            "label": "Core Enterprise Microservices",
            "wraps": service_wraps,
        })
    if data_wraps:
        boundaries.append({
            "kind": "region",
            "label": "Governed Datastores & Cloud Telemetry",
            "wraps": data_wraps,
        })

    # Connections
    for idx, e in enumerate(edges):
        s_urn = e["source_urn"]
        t_urn = e["target_urn"]

        s_id = node_id_map.get(s_urn, sanitize_id(s_urn))
        t_id = node_id_map.get(t_urn, sanitize_id(t_urn))

        # Check if endpoints exist in components
        valid_ids = {c["id"] for c in components}
        if s_id not in valid_ids or t_id not in valid_ids:
            continue

        relation = e.get("relation", "flows_to")
        is_pii = e.get("contains_pii", False)
        is_violating = (s_urn in highlight_set) or (t_urn in highlight_set)

        variant = "security" if (is_pii or is_violating) else ("emphasis" if relation in ("accesses", "serves") else "default")

        connections.append({
            "id": f"conn_{idx}_{s_id}_{t_id}",
            "from": s_id,
            "to": t_id,
            "variant": variant,
        })


    cards = [
        {
            "dot": "emerald",
            "title": "Unity Catalog Metamodel Status",
            "items": [
                f"Active PAM Nodes: {len(components)}",
                f"ArchiMate Relations: {len(connections)}",
                "Schema: ea.metamodel conformed",
            ],
        }
    ]

    if highlight_set:
        cards.append({
            "dot": "rose",
            "title": "EA Sentinel Policy Alert",
            "items": [
                f"Flagged Components: {len(highlight_set)}",
                "Violations: Policy Failure / Unencrypted PII",
                "Status: Gate Blocked",
            ],
        })

    spec = {
        "schema_version": 1,
        "diagram_type": "architecture",
        "meta": {
            "title": title,
            "subtitle": subtitle,
            "output": output_html_rel,
            "quality_profile": "standard",
        },

        "components": components,
        "boundaries": boundaries,
        "connections": connections,
        "cards": cards,
    }
    return spec


def extract_svg_from_html(html_path: Path) -> Optional[str]:
    """
    Extracts standalone SVG from Archify compiled HTML.
    Extracts all embedded CSS styles and encapsulates them within <defs><style>
    to prevent solid black fallback boxes.
    """
    if not html_path.exists():
        return None

    content = html_path.read_text(encoding="utf-8")

    # Extract all <style> blocks from the HTML header
    style_matches = re.findall(r"<style[^>]*>([\s\S]*?)</style>", content, re.IGNORECASE)
    combined_css = "\n".join(style_matches)

    # Scoped fallback styles for Archify component classes
    fallback_css = """
    svg {
      background-color: var(--bg, #020617);
      color: var(--text, #ffffff);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .c-component {
      fill: var(--backend-fill, rgba(6, 78, 59, 0.4));
      stroke: var(--backend-stroke, #34d399);
    }
    .c-region {
      fill: var(--panel, rgba(15, 23, 42, 0.5));
      stroke: var(--panel-border, #1e293b);
    }
    """
    combined_css = fallback_css + "\n" + combined_css

    # Remap :root pseudo-selector to :root, svg
    combined_css = re.sub(r":root\s*\{", ":root, svg {", combined_css)

    # Locate the main diagram <svg>
    svg_match = re.search(r"(<svg\b[^>]*role=[\"']img[\"'][^>]*>[\s\S]*?</svg>)", content)
    if not svg_match:
        svg_match = re.search(r"(<svg\b[^>]*xmlns=[\"']http://www.w3.org/2000/svg[\"'][^>]*>[\s\S]*?</svg>)", content)

    if not svg_match:
        return None

    svg_chunk = svg_match.group(1)

    # Inject <style> inside <defs> within the SVG
    defs_match = re.search(r"<defs\b[^>]*>", svg_chunk)
    if defs_match:
        inject_pos = defs_match.end()
        svg_chunk = (
            svg_chunk[:inject_pos]
            + f"\n<style type=\"text/css\"><![CDATA[\n{combined_css}\n]]></style>"
            + svg_chunk[inject_pos:]
        )
    else:
        svg_tag_match = re.search(r"<svg\b[^>]*>", svg_chunk)
        if svg_tag_match:
            inject_pos = svg_tag_match.end()
            svg_chunk = (
                svg_chunk[:inject_pos]
                + f"\n<defs>\n<style type=\"text/css\"><![CDATA[\n{combined_css}\n]]></style>\n</defs>"
                + svg_chunk[inject_pos:]
            )

    return svg_chunk


def compile_archify_diagram(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    output_path: Path,
    title: str = "Enterprise Architecture Living Map",
    subtitle: str = "Databricks Unity Catalog Conformed Metamodel Topology",
    highlight_urns: Optional[List[str]] = None,
) -> Tuple[Path, Path]:
    """
    Compiles PAM nodes and edges into BOTH interactive HTML and styled vector SVG.
    Returns (html_path, svg_path).
    """
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    target_html = out_file.with_suffix(".html")
    target_svg = out_file.with_suffix(".svg")

    from datetime import datetime
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    work_dir = ROOT_DIR / ".archify" / f"run-{run_id}"
    work_dir.mkdir(parents=True, exist_ok=True)

    temp_json = work_dir / "candidate.json"
    temp_html = work_dir / "rendered.html"
    rel_html = str(temp_html.relative_to(ROOT_DIR))

    spec = build_archify_spec(
        nodes=nodes,
        edges=edges,
        title=title,
        subtitle=subtitle,
        output_html_rel=rel_html,
        highlight_urns=highlight_urns,
    )

    with open(temp_json, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    # Invoke Archify CLI
    cmd = [
        "node",
        str(ARCHIFY_CLI),
        "finalize",
        "architecture",
        str(temp_json),
        str(temp_html),
        "--quality",
        "standard",
        "--json",

    ]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Archify Bridge] Warning: Archify CLI exited with {res.returncode}:\n{res.stderr or res.stdout}", file=sys.stderr)
        if not temp_html.exists():
            raise RuntimeError(f"Archify CLI failed to generate HTML: {res.stderr or res.stdout}")

    # Copy HTML
    html_content = temp_html.read_text(encoding="utf-8")
    target_html.write_text(html_content, encoding="utf-8")

    # Extract styled SVG
    svg_content = extract_svg_from_html(temp_html)
    if svg_content:
        target_svg.write_text(svg_content, encoding="utf-8")
    else:
        target_svg.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200">'
            f'<rect width="100%" height="100%" fill="#080c16"/>'
            f'<text x="20" y="50" fill="#38bdf8" font-family="sans-serif" font-size="16">{title}</text>'
            f'<text x="20" y="80" fill="#94a3b8" font-family="sans-serif" font-size="12">{subtitle}</text>'
            f'</svg>',
            encoding="utf-8",
        )

    return target_html, target_svg


class ArchifyBridge:
    """High-level Archify compilation bridge for PAM estate graphs."""

    def __init__(self):
        from src.data_backbone.client import get_unity_catalog_client
        self.client = get_unity_catalog_client()

    def compile_interactive_map(
        self,
        output_html_path: Optional[Path] = None,
        output_svg_path: Optional[Path] = None,
        nodes: Optional[List[Dict[str, Any]]] = None,
        edges: Optional[List[Dict[str, Any]]] = None,
        highlight_urns: Optional[List[str]] = None,
        title: str = "The Agentic EA — Enterprise Architecture Living Map",
        subtitle: str = "Databricks Unity Catalog Conformed Metamodel Topology",
    ) -> Tuple[Path, Path]:
        """Compiles conformed PAM graph from Unity Catalog into interactive HTML and styled SVG."""
        if nodes is None:
            nodes = self.client.get_nodes()
        if edges is None:
            edges = self.client.get_edges()

        out_base = output_html_path or (ROOT_DIR / "data" / "diagrams" / "architecture-view.html")
        return compile_archify_diagram(
            nodes=nodes,
            edges=edges,
            output_path=Path(out_base),
            title=title,
            subtitle=subtitle,
            highlight_urns=highlight_urns,
        )


def main():

    parser = argparse.ArgumentParser(description="PAM to Archify Bridge CLI")
    parser.add_argument("--input", "-i", help="Input delta/graph JSON file.")
    parser.add_argument("--output", "-o", default="./data/diagrams/architecture-view.svg", help="Output SVG/HTML path.")
    parser.add_argument("--title", default="The Agentic EA — Enterprise Architecture Living Map")
    parser.add_argument("--subtitle", default="Databricks Unity Catalog Conformed Metamodel Topology")
    parser.add_argument("--highlight", nargs="*", default=[], help="URNs to visually highlight")
    args = parser.parse_args()

    nodes = []
    edges = []

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])
    else:
        from src.data_backbone.client import get_unity_catalog_client
        client = get_unity_catalog_client()
        nodes = client.get_nodes()
        edges = client.get_edges()


    html_p, svg_p = compile_archify_diagram(
        nodes=nodes,
        edges=edges,
        output_path=Path(args.output),
        title=args.title,
        subtitle=args.subtitle,
        highlight_urns=args.highlight,
    )
    print(f"✓ Interactive HTML: {html_p} ({html_p.stat().st_size:,} bytes)")
    print(f"✓ Styled Vector SVG: {svg_p} ({svg_p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
