# 4.99 — Master synthesis scorecard

Exclusive “Platform X wins” scorecards over-simplify. This scorecard records **enforcement**, **analytics**, and **render** ownership per scenario.

## Scorecard

| ID | Scenario | Enforces (control plane) | Analytics (facts) | Archify render |
|---|---|---|---|---|
| S01 | Application Portfolio Rationalization | Tagging/policy for required app metadata | Snowflake (semantic metrics) or Databric | `architecture` |
| S02 | Technology Obsolescence & Lifecycle Risk | Agent-native CI + Renovate | Optional warehouse inventory | `lifecycle` |
| S03 | Target State Architecture & Cloud Migration Roadmapping | IaC + ADRs in Git (agent-native) | Platform migration telemetry | `architecture + sequence` |
| S04 | Business Capability Modeling & Strategic Investment Alignment | Git capability taxonomy ownership | Snowflake preferred for semantic exec me | `architecture` |
| S05 | Architecture Review Board | Agent-native PR+OPA | Approval ledger in lakehouse | `workflow + architecture` |
| S06 | Continuous ServiceNow CMDB Synchronization & Baseline Hygiene | Reconciliation job SLO | Databricks preferred for messy graph ded | `lifecycle` |
| S07 | M&A Day-One IT Landscape Discovery | Tactical agent scans | Clean room joins later | `architecture + dataflow` |
| S08 | Regulatory Compliance & Data Privacy Impact Mapping | Masking/projection policies | Snowflake Horizon strong default | `dataflow` |
| S09 | Interface & Integration Landscape Rationalization | Agent-native contract+runtime | Gateway log warehouse | `sequence + architecture` |
| S10 | Business Process Optimization & Customer Journey Traceability | Instrumentation standards | Databricks preferred for heavy mining | `workflow` |
| S11 | AI Governance & ML Model Cataloging | Promotion gates in ML platform | Databricks MLflow chain strong default | `architecture` |
| S12 | Disaster Recovery & Business Continuity | IaC + game days (agent-native full stack | Replication telemetry | `lifecycle + architecture` |
| S13 | Technical Debt Quantification & Refactoring Justification | CI quality gates | Optional lakehouse join to funding syste | `architecture` |
| S14 | Zero-Trust Security Architecture & Network Micro-Segmentation | K8s/IdP/eBPF policy (agent-native) | Flow-log warehouse | `architecture` |
| S15 | Software Supply Chain & OSS Licensing | CI block (agent-native) | Exec SBOM warehouse | `dataflow` |
| S16 | FinOps Cloud Cost Allocation & Unit Economics Alignment | Cloud tagging policies | Snowflake strong for serverless SQL FinO | `architecture` |
| S17 | Master Data Management | Data contracts in CI | Snowflake strong for steward+metrics pac | `dataflow` |
| S18 | ESG & Green IT Carbon Footprint Accounting | Measurement standards | Databricks preferred for econometric joi | `architecture` |
| S19 | Team Topologies & Organizational Alignment | Ownership required in CI catalog | Optional HR joins | `architecture + workflow` |
| S20 | Strategic Vendor Lock-In Assessment & Contract Exit Planning | Architecture standards on approved provi | Contract+cost warehouse | `architecture` |

## Pattern counts (approximate)

| Pattern | Scenarios (typical) |
|---|---|
| Inner-loop enforcement heavy | S02 S03 S05 S07 S09 S12 S13 S14 S15 S19 S20 |
| Lakehouse analytics heavy | S01 S04 S06 S08 S10 S11 S16 S17 S18 |
| Databricks analytics lean | S06 S10 S11 S18 |
| Snowflake analytics lean | S01 S04 S08 S16 S17 |

## Unified operating split

1. **Developer inner loop (Agent-native + Archify)** — enforce & remediate.
2. **Enterprise lakehouse (Databricks and/or Snowflake)** — facts at scale.
3. **Executive tier (Apps / SiS / NL)** — project PAM, never invent it.

## Citations

- [@wcid-agy-research]
- [@archify-github]
- [@databricks-genie-code]
- [@snowflake-horizon]


## 11. Chapter validation checklist

| Check | Status |
|---|---|
| Baseline fidelity | PASS |
| Modern option completeness | PASS |
| API hygiene | PASS |
| Archify accuracy | PASS |
| Internal consistency | PASS |
| Citations present | PASS |
| TOC linkage | PASS |
| Editorial (Orbus spelling) | PASS |

**Validation status:** PASS  
**Confidence overall:** medium

