# 1.1 — What Orbus Infinity is (and is not)

## Definition

**Orbus Infinity** is a commercial enterprise architecture and related GRC/strategy tooling suite. In common EA practice it functions as:

1. A **governed object repository** for applications, technologies, capabilities, processes, data objects, and relationships.
2. A **modeling and visualization** environment for architecture views.
3. An **integration hub** (historically including Orbus Flow / connector patterns) to pull CMDB, Agile, and cloud inventory signals.
4. A **governance workflow** surface for architecture intake, review, and decision recording.

`confidence: medium` — exact module names and packaging vary by Orbus release and customer SKU. Always verify against your tenant. [@orbus-infinity-product]

## What it is optimized for

| Strength | Explanation |
|---|---|
| Shared vocabulary | Business and IT can point at the same Application / Capability objects |
| Pruned metamodel | CoreEA reduces ArchiMate overwhelm into a “sensible default” |
| Auditability | Decisions and repository history support governance narratives |
| Executive packaging | Portfolio and capability views for leadership forums |

## What it is not

| Not this | Why it matters |
|---|---|
| Not a CI system | It does not block merges in Git |
| Not a runtime sensor | It does not observe eBPF/HTTP between microservices by itself |
| Not a lakehouse | It is not built for billion-row FinOps or process-mining graphs |
| Not agent-native | Developers and coding agents cannot treat CoreEA as a first-class JSON Schema in Git |
| Not Archify | Visualization inside Orbus is product UI; Archify is a headless verified compile path |

## Relationship to standards

Orbus Infinity sits **above** open standards:

- **TOGAF** content ideas inform repository structure. [@togaf-10]
- **ArchiMate** informs relationship semantics, even when the product exposes a simplified CoreEA. [@archimate-3-2]

The product value is opinionated packaging + governance UX, not ownership of those standards.

## Baseline stance of this manual

We keep Orbus Infinity as the **baseline practice**. Every modernization option must answer: *Which Orbus job does this replace, coexist with, or improve?*

## Citations

- [@orbus-infinity-product]
- [@togaf-10]
- [@archimate-3-2]
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

