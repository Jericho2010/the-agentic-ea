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
    boundary_mode: str = "layer",
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
            meta = node.get("metadata", {}) or {}
            if boundary_mode == "jurisdiction":
                cls = meta.get("data_classification", "Internal")
                jur = meta.get("jurisdiction", "EU-West-1")
                sublabel = f"{cls} • {jur}"
            else:
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

    if boundary_mode == "jurisdiction":
        eu_wraps = []
        us_wraps = []
        for n in nodes:
            cid = node_id_map.get(n["urn"])
            if not cid:
                continue
            meta = n.get("metadata", {}) or {}
            jur = meta.get("jurisdiction", "")
            if jur == "US-East-1" or "customer-pii-stream" in cid or "customer-pii-stream" in n.get("urn", ""):
                us_wraps.append(cid)
            else:
                eu_wraps.append(cid)
        if eu_wraps:
            boundaries.append({
                "kind": "region",
                "label": "EEA Sovereign Jurisdiction (EU-West-1 — GDPR Art. 32 / DORA Scope)",
                "wraps": eu_wraps,
            })
        if us_wraps:
            boundaries.append({
                "kind": "region",
                "label": "Third Country Egress Jurisdiction (US-East-1 — GDPR Art. 44 Scope)",
                "wraps": us_wraps,
            })
    elif boundary_mode == "interfaces":
        comp_wraps = []
        disc_wraps = []
        for n in nodes:
            cid = node_id_map.get(n["urn"])
            if not cid:
                continue
            if cid in highlight_set or n["urn"] in highlight_set or any(d in cid for d in ["scanner", "batch", "crm"]):
                disc_wraps.append(cid)
            else:
                comp_wraps.append(cid)
        if comp_wraps:
            boundaries.append({
                "kind": "region",
                "label": "Governed & Compliant Enterprise Interfaces (HTTPS / gRPC / mTLS)",
                "wraps": comp_wraps,
            })
        if disc_wraps:
            boundaries.append({
                "kind": "region",
                "label": "Flagged Interface Discrepancies (Zombie / Dead / Protocol Sprawl)",
                "wraps": disc_wraps,
            })
    else:
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

    if boundary_mode == "jurisdiction":
        cards = [
            {
                "dot": "emerald",
                "title": "GDPR / DORA Regulatory Scope",
                "items": [
                    f"EU Sovereign Assets: {len(eu_wraps)}",
                    f"Third Country Egress: {len(us_wraps)}",
                    "Governed Lineage: ea.gold.compliance_lineage",
                ],
            }
        ]
        if highlight_set:
            cards.append({
                "dot": "rose",
                "title": "Compliance Violations Detected",
                "items": [
                    f"Flagged Assets: {len(highlight_set)}",
                    "GDPR Art 32 / 44 Violations",
                    "DORA ICT SPOF Identified",
                ],
            })
    elif boundary_mode == "interfaces":
        cards = [
            {
                "dot": "emerald",
                "title": "Conformed Interface Mart (`ea.gold.interface_rationalization`)",
                "items": [
                    f"Active Inter-Service Endpoints: {len(components)}",
                    "Declared Contracts: 7 OpenAPI & gRPC endpoints",
                    "Authoritative Catalog: ea.gold.interface_rationalization",
                ],
            },
            {
                "dot": "rose",
                "title": "Integration Discrepancies Flagged",
                "items": [
                    "Zombie / Shadow API: /v1/internal/debug-dump (Undocumented)",
                    "Dead / Orphan API: /v1/legacy-inventory-sync (0 req / 90d)",
                    "Protocol Sprawl: /soap/v1/customer (HTTP-Basic / Insecure)",
                ],
            },
            {
                "dot": "orange",
                "title": "Rationalization Action Plan",
                "items": [
                    "DOCUMENT_AND_SECURE: Shadow debug dump endpoint",
                    "DECOMMISSION: Dead inventory batch integration",
                    "STANDARDIZE_MTLS: Legacy SOAP CRM integration",
                ],
            },
        ]
    else:
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
    boundary_mode: str = "layer",
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
        boundary_mode=boundary_mode,
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


def build_archify_sequence_spec(
    participants: Optional[List[Dict[str, Any]]] = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    activations: Optional[List[Dict[str, Any]]] = None,
    segments: Optional[List[Dict[str, Any]]] = None,
    cards: Optional[List[Dict[str, Any]]] = None,
    title: str = "Checkout & Payment Sequence Flow",
    subtitle: str = "Enterprise API Gateway & Inter-Service Transaction Trace",
    output_html_rel: str = "interface-sequence.html",
) -> Dict[str, Any]:
    """Compile sequence flow specification into strict Archify sequence schema."""
    if participants is None:
        participants = [
            {"id": "user", "type": "external", "label": "Customer", "sublabel": "Browser / Mobile App"},
            {"id": "storefront", "type": "frontend", "label": "Web Storefront", "sublabel": "Next.js Storefront"},
            {"id": "checkout", "type": "backend", "label": "Checkout Service", "sublabel": "Go Microservice"},
            {"id": "auth", "type": "security", "label": "Auth Service", "sublabel": "Identity & Token Verifier"},
            {"id": "payments-api", "type": "backend", "label": "Payments API", "sublabel": "API Gateway / Ingress"},
            {"id": "stripe", "type": "external", "label": "Stripe Gateway", "sublabel": "SaaS Payment Provider"},
            {"id": "payments-service", "type": "backend", "label": "Payments Service", "sublabel": "Core Ledger Service"},
        ]

    if segments is None:
        segments = [
            {"from": 150, "to": 258, "label": "Authentication & Order Intake"},
            {"from": 265, "to": 345, "label": "Payment Authorization"},
            {"from": 352, "to": 490, "label": "Ledger Sync & Confirmation"},
        ]

    if messages is None:
        messages = [
            {"id": "open-checkout", "from": "user", "to": "storefront", "y": 160, "label": "POST /cart/checkout", "variant": "emphasis"},
            {"id": "checkout-req", "from": "storefront", "to": "checkout", "y": 189, "label": "POST /api/v1/checkout", "variant": "emphasis"},
            {"id": "verify-auth", "from": "checkout", "to": "auth", "y": 218, "label": "POST /v1/auth/verify (mTLS)", "variant": "security"},
            {"id": "auth-ok", "from": "auth", "to": "checkout", "y": 247, "label": "200 Claims Valid", "variant": "return"},
            {"id": "pay-auth", "from": "checkout", "to": "payments-api", "y": 276, "label": "POST /v1/payments/authorize (mTLS)", "variant": "emphasis"},
            {"id": "stripe-charge", "from": "payments-api", "to": "stripe", "y": 305, "label": "POST /v1/charges (Bearer Token)", "variant": "security"},
            {"id": "stripe-ok", "from": "stripe", "to": "payments-api", "y": 334, "label": "200 Charge Captured", "variant": "return"},
            {"id": "ledger-sync", "from": "payments-api", "to": "payments-service", "y": 363, "label": "RPC LedgerSync/Record (gRPC)", "variant": "dashed"},
            {"id": "ledger-ack", "from": "payments-service", "to": "payments-api", "y": 392, "label": "Ack Recorded", "variant": "return"},
            {"id": "pay-ok", "from": "payments-api", "to": "checkout", "y": 421, "label": "200 Payment Authorized", "variant": "return"},
            {"id": "order-ok", "from": "checkout", "to": "storefront", "y": 450, "label": "201 Order Created", "variant": "return"},
            {"id": "order-confirm", "from": "storefront", "to": "user", "y": 479, "label": "Order Confirmation View", "variant": "return"},
        ]

    if activations is None:
        activations = [
            {"participant": "storefront", "from": 155, "to": 485, "type": "frontend"},
            {"participant": "checkout", "from": 180, "to": 455, "type": "backend"},
            {"participant": "auth", "from": 210, "to": 252, "type": "security"},
            {"participant": "payments-api", "from": 270, "to": 425, "type": "backend"},
            {"participant": "stripe", "from": 300, "to": 340, "type": "external"},
            {"participant": "payments-service", "from": 358, "to": 400, "type": "backend"},
        ]

    if cards is None:
        cards = [
            {
                "dot": "emerald",
                "title": "Conformed Inter-Service Contracts",
                "items": [
                    "Endpoints validated against OpenAPI & gRPC specifications",
                    "Zero unauthenticated traffic across critical payment transaction path",
                    "Audit trail and telemetry streamed to Unity Catalog",
                ],
            },
            {
                "dot": "rose",
                "title": "Security Boundary & Protocols",
                "items": [
                    "OAuth2 / mTLS enforced between checkout-service & payments-api",
                    "gRPC / mTLS for immutable ledger sync (payments-service)",
                    "PCI-DSS egress strictly scoped to Stripe Gateway",
                ],
            },
            {
                "dot": "orange",
                "title": "Interface Rationalization Impact",
                "items": [
                    "Zombie endpoints (/v1/internal/debug-dump) isolated & secured",
                    "SOAP legacy protocol decommission candidate (/soap/v1/customer)",
                    "100% active traffic mapped to conformed PAM nodes",
                ],
            },
        ]

    spec = {
        "schema_version": 1,
        "diagram_type": "sequence",
        "meta": {
            "title": title,
            "subtitle": subtitle,
            "output": output_html_rel,
            "viewBox": [1080, 580],
            "column_fit": "spread",
            "animation": "trace",
            "quality_profile": "standard",
        },
        "participants": participants,
        "segments": segments,
        "messages": messages,
        "activations": activations,
        "cards": cards,
    }
    return spec


def compile_archify_sequence_diagram(
    output_path: Path,
    participants: Optional[List[Dict[str, Any]]] = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    activations: Optional[List[Dict[str, Any]]] = None,
    segments: Optional[List[Dict[str, Any]]] = None,
    cards: Optional[List[Dict[str, Any]]] = None,
    title: str = "Checkout & Payment Sequence Flow",
    subtitle: str = "Enterprise API Gateway & Inter-Service Transaction Trace",
) -> Tuple[Path, Path]:
    """
    Compiles Archify sequence flow into BOTH interactive HTML and styled vector SVG.
    Returns (html_path, svg_path).
    """
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    target_html = out_file.with_suffix(".html")
    target_svg = out_file.with_suffix(".svg")

    from datetime import datetime
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    work_dir = ROOT_DIR / ".archify" / f"run-seq-{run_id}"
    work_dir.mkdir(parents=True, exist_ok=True)

    temp_json = work_dir / "candidate_sequence.json"
    temp_html = work_dir / "rendered_sequence.html"
    rel_html = str(temp_html.relative_to(ROOT_DIR))

    spec = build_archify_sequence_spec(
        participants=participants,
        messages=messages,
        activations=activations,
        segments=segments,
        cards=cards,
        title=title,
        subtitle=subtitle,
        output_html_rel=rel_html,
    )

    with open(temp_json, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    # Invoke Archify CLI for sequence
    cmd = [
        "node",
        str(ARCHIFY_CLI),
        "finalize",
        "sequence",
        str(temp_json),
        str(temp_html),
        "--quality",
        "standard",
        "--json",
    ]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Archify Bridge] Warning: Archify CLI sequence exited with {res.returncode}:\n{res.stderr or res.stdout}", file=sys.stderr)
        if not temp_html.exists():
            raise RuntimeError(f"Archify CLI failed to generate sequence HTML: {res.stderr or res.stdout}")

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
        boundary_mode: str = "layer",
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
            boundary_mode=boundary_mode,
        )

    def compile_sequence_diagram(
        self,
        output_html_path: Optional[Path] = None,
        title: str = "Checkout & Payment Sequence Flow",
        subtitle: str = "Enterprise API Gateway & Inter-Service Transaction Trace",
    ) -> Tuple[Path, Path]:
        """Compiles sequence diagram into interactive HTML and styled SVG."""
        out_base = output_html_path or (ROOT_DIR / "data" / "diagrams" / "interface_sequence.html")
        return compile_archify_sequence_diagram(
            output_path=Path(out_base),
            title=title,
            subtitle=subtitle,
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
