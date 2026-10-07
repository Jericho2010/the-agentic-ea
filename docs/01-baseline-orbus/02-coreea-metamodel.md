# 1.2 — CoreEA metamodel: what it got right and wrong

## What CoreEA is trying to be

**CoreEA** (Orbus’s product metamodel concept) is a pruned, opinionated enterprise metamodel covering the usual layers practitioners need day to day: business (capabilities, processes), application, technology, data, and governance artifacts. `confidence: medium` [@orbus-coreea] [@wcid-agy-research]

It exists because raw ArchiMate / full TOGAF content metamodels can overwhelm teams into taxonomy debates instead of shipping architecture decisions.

## What CoreEA got right

1. **Sensible defaults** — A reduced entity set beats an infinite palette for most enterprises.
2. **Cross-layer joins** — The point of EA is multi-hop questions (“if we sunset X, which capabilities fail?”).
3. **Governance attachment** — Decisions and standards can hang off the same objects executives already recognize.
4. **Integration-shaped** — Designed to be fed by CMDB and related enterprise systems, not only hand drawing.

## What CoreEA got wrong (for an agent-native world)

1. **Closed store** — The metamodel lives in a proprietary repository/schema agents and Python jobs cannot import as a first-class contract.
2. **Weak developer ergonomics** — Engineers think in Backstage/C4/OpenAPI; CoreEA thinks in EA repository objects.
3. **Declared-over-observed bias** — Manual and connector-fed objects lag runtime truth.
4. **Diagram ≠ verification** — UI diagrams are not a deterministic compile with machine-checkable gates like Archify `finalize`. [@archify-github]
5. **Ivory-tower risk remains** — A pruned metamodel still fails if the operating model is “update Orbus after the fact.”

## Open-standard counterparts

| Concern | Open counterpart |
|---|---|
| Conceptual metamodel | TOGAF 10 content metamodel [@togaf-10] |
| Formal relations | ArchiMate 3.2 [@archimate-3-2] |
| Developer catalog UX | Backstage Domain→System→Component→API [@backstage-software-catalog] |
| Architecture views | C4 [@c4-model] |
| Data movement graph | OpenLineage [@openlineage] |

## Implication for this manual

Part VI defines **PAM (Pragmatic Agentic Metamodel)** as an open, Git-validated, lakehouse-stored CoreEA *equivalent*—not a clone of Orbus’s proprietary schema.

## Citations

- [@orbus-coreea]
- [@togaf-10]
- [@archimate-3-2]
- [@backstage-software-catalog]
- [@archify-github]
- [@wcid-agy-research]


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

