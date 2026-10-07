# F0 — Preface: Why this manual exists

Enterprise architecture (EA) tools have long promised a single source of truth for applications, capabilities, technology, and decisions. **Orbus Infinity** (and its CoreEA metamodel) is one of the most recognizable commercial realizations of that promise: a governed repository, diagramming, integrations (often via Orbus Flow), and Architecture Review Board (ARB) workflows.

Meanwhile, engineering practice has moved to:

- Git-native architecture decision records (ADRs)
- Policy-as-code and CI gates
- Observability and runtime truth (OpenTelemetry, eBPF, flow logs)
- Data+AI platforms (Snowflake, Databricks) as systems of analytical record
- Coding agents that can parse ASTs, open PRs, and compile verified diagrams

This manual treats Orbus Infinity as the **baseline**—not as an enemy to mock, but as the practice we must understand before modernizing. It then walks, step by step, through OSS (“Earth”), agent-native (“Moon”), and frontier (“Mars”) options, and shows how a modern data and AI platform becomes the **backbone** for living architecture facts.

It is an **ideation manual / book**, synthesized from structured research (including Herdr WCID-agy analysis and a NotebookLM source notebook). It is not product documentation from Orbus, Databricks, or Snowflake.

## Who it is for

- Chief / Principal / Enterprise Architects evaluating Orbus exit or coexist strategies
- Data platform leaders asked to “host EA” on Snowflake or Databricks
- Platform and DevEx engineers building agent-native governance loops
- Consultants writing modernization roadmaps

## What success looks like

After reading, you can:

1. Map any Orbus capability to Earth / Moon / Mars alternatives.
2. Decide, per scenario, what **enforces** change vs what **analyzes** facts vs what **renders** diagrams.
3. Specify an open metamodel (PAM) that replaces CoreEA without recreating a proprietary trap.
4. Run a credible 90-day pilot.

## Citations

- [@orbus-infinity-product]
- [@wcid-agy-research]
- [@notebooklm-oss-agent-native-orbus]


## Chapter validation checklist

| Check | Status |
|---|---|
| Baseline fidelity | PASS |
| Modern option completeness (if applicable) | PASS / N/A |
| API hygiene | PASS |
| Archify accuracy (if applicable) | PASS / N/A |
| Internal consistency | PASS |
| Citations present | PASS |
| TOC linkage | PASS |
| Editorial (Orbus spelling) | PASS |

**Validation status:** PASS

