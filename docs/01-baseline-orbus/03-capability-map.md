# 1.3 — Orbus capability map (canonical baseline)

This is the **stable capability vocabulary** used by Parts II–VII. Modernization ladders must remap to these IDs—not invent a parallel taxonomy.

## Canonical capability baseline

| ID | Capability | Description | Orbus Infinity baseline expression |
|---|---|---|---|
| C1 | Governed architecture repository | Central object store, reuse, history | Orbus Infinity repository |
| C2 | Metamodel & standards management | Entity/relationship types, standards library | CoreEA + standards modules |
| C3 | Business capability & strategy mapping | L1–L3 capabilities, investment views | Capability modeling |
| C4 | Application portfolio management | App inventory, lifecycle, TIME-like views | APM views |
| C5 | Technology portfolio & standards | Tech products, lifecycles, standards | Technology catalog |
| C6 | Data architecture & lineage views | Data objects, stores, flows | Data modeling views |
| C7 | Process & value-stream modeling | Processes linked to apps/capabilities | Process models |
| C8 | Integration / interface catalog | APIs and integration landscape | Interface objects |
| C9 | Diagramming & viewpoint publishing | Architecture views for stakeholders | Orbus diagramming UX |
| C10 | Integrations & synchronization | CMDB/Agile/cloud sync (Orbus Flow patterns) | Connectors / Flow |
| C11 | ARB / governance workflows | Intake, review, approvals, ADR-like records | Governance workflows |
| C12 | Reporting, audit & executive dashboards | Portfolio reports for leadership/audit | Reports / portals |
| C13 | Collaboration & stakeholder access | Broad read access beyond EA specialists | Portal / sharing |
| C14 | Security / risk architecture views | Zones, controls, risk annotations | Security viewpoints |
| C15 | Roadmapping & transformation planning | Waves, initiatives, dependency planning | Roadmaps |

`confidence: medium` — Names are practice-oriented groupings aligned to common Orbus Infinity usage, not a verbatim SKU list. [@orbus-infinity-product] [@wcid-agy-research]

## How to use this map

1. When evaluating a tool, ask which **C#** it covers.
2. Earth / Moon / Mars columns in [2.5](../02-modernization-ladders/05-four-column-matrix.md) use these IDs.
3. Scenario playbooks reference capabilities implicitly (e.g., S01→C4, S05→C11).

## Coverage notes

- Some Orbus deployments emphasize GRC/BPM modules beyond this EA-centric map; those are out of v1 scope unless they appear in S01–S20.
- “AI governance” (S11) stretches C4/C6/C11; PAM later adds explicit AIModel types.

## Citations

- [@orbus-infinity-product]
- [@wcid-agy-research]
- [@notebooklm-oss-agent-native-orbus]


## Chapter validation checklist

| Check | Status |
|---|---|
| Baseline fidelity | PASS |
| Modern option completeness | N/A (baseline part) |
| API hygiene | PASS |
| Archify accuracy | N/A |
| Internal consistency | PASS |
| Citations present | PASS |
| TOC linkage | PASS |
| Editorial (Orbus spelling) | PASS |

**Validation status:** PASS  
**Confidence overall:** medium

