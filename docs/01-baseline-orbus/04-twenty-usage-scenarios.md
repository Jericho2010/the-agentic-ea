# 1.4 — Twenty EA usage scenarios (Orbus as practiced)

These scenarios answer: *How does a group of enterprise architects actually use Orbus Infinity?* They are the spine of Part IV playbooks.

## Catalog

| ID | Scenario | What | When | Playbook |
|---|---|---|---|---|
| S01 | Application Portfolio Rationalization (APM / TIME) | Categorize applications into Tolerate / Invest / Migrate / Eliminate using value, cost, and health. | Quarterly portfolio reviews; M&A integration; cost-reduction programs. | See [playbook](../04-scenario-playbooks/01-apm-time.md) |
| S02 | Technology Obsolescence & Lifecycle Risk (EOL/EOS) | Track frameworks, OS, and runtimes approaching end of support. | Before major releases; security audits; annual tech radar updates. | See [playbook](../04-scenario-playbooks/02-eol-eos.md) |
| S03 | Target State Architecture & Cloud Migration | Plan waves from as-is to cloud-native to-be architectures. | Cloud programs; data center exits; platform consolidation. | See [playbook](../04-scenario-playbooks/03-target-state-migration.md) |
| S04 | Business Capability Modeling & Investment Alignment | Map L1–L3 capabilities to systems and spend. | Strategy cycles; operating model redesign; budget allocation. | See [playbook](../04-scenario-playbooks/04-capabilities.md) |
| S05 | Architecture Review Board (ARB) & Design Approvals | Enforce guardrails and record Architecture Decision Records. | Material designs; exceptions; standard deviations. | See [playbook](../04-scenario-playbooks/05-arb-governance.md) |
| S06 | Continuous CMDB Synchronization & Baseline Hygiene | Reconcile Orbus objects with ServiceNow (or similar) CIs. | Ongoing operations; audit prep; discovery after cloud growth. | See [playbook](../04-scenario-playbooks/06-cmdb-sync.md) |
| S07 | M&A Day-One IT Landscape Discovery | Rapidly inventory an acquired estate. | Pre-deal diligence; Day-One; first 100 days. | See [playbook](../04-scenario-playbooks/07-ma-discovery.md) |
| S08 | Regulatory Compliance & Data Privacy (GDPR / DORA) | Trace PII and critical data across systems and borders. | DPIAs; regulator inquiries; DORA ICT risk programs. | See [playbook](../04-scenario-playbooks/08-gdpr-dora.md) |
| S09 | Interface & Integration Landscape Rationalization | Inventory APIs and integration hubs; find zombies. | Platform consolidation; API programs; incident postmortems. | See [playbook](../04-scenario-playbooks/09-interfaces.md) |
| S10 | Business Process Optimization & Journey Traceability | Relate processes/journeys to supporting applications. | CX programs; shared-services redesign; bottleneck hunts. | See [playbook](../04-scenario-playbooks/10-process-mining.md) |
| S11 | AI Governance & ML Model Cataloging | Catalog models, datasets, and risk tiers (incl. EU AI Act themes). | Model promotion; AI risk committees; audit. | See [playbook](../04-scenario-playbooks/11-ai-governance.md) |
| S12 | Disaster Recovery & Business Continuity | Align RTO/RPO and failover paths to architecture. | BCP tests; multi-region programs; critical service designation. | See [playbook](../04-scenario-playbooks/12-disaster-recovery.md) |
| S13 | Technical Debt Quantification | Make structural debt visible for investment cases. | OKR planning; platform funding; risk committees. | See [playbook](../04-scenario-playbooks/13-tech-debt.md) |
| S14 | Zero-Trust & Network Micro-Segmentation | Describe trust zones and access paths. | Security architecture reviews; segmentation programs. | See [playbook](../04-scenario-playbooks/14-zero-trust.md) |
| S15 | Software Supply Chain & OSS Licensing | Track components/licenses and SBOM-oriented risk. | Procurement; release gates; customer security questionnaires. | See [playbook](../04-scenario-playbooks/15-sbom.md) |
| S16 | FinOps & Unit Economics | Attribute cloud/SaaS cost to products and capabilities. | Monthly FinOps; showback/chargeback; unit cost reviews. | See [playbook](../04-scenario-playbooks/16-finops.md) |
| S17 | Master Data & Golden Record Lineage | Show authoritative sources and lineage for core entities. | MDM programs; data platform redesign. | See [playbook](../04-scenario-playbooks/17-mdm.md) |
| S18 | ESG / Green IT Carbon Accounting | Allocate digital estate emissions for disclosure. | Sustainability reporting cycles. | See [playbook](../04-scenario-playbooks/18-esg-carbon.md) |
| S19 | Team Topologies & Conway Alignment | Relate org ownership to system boundaries. | Platform team design; post-reorg; scaling product orgs. | See [playbook](../04-scenario-playbooks/19-team-topologies.md) |
| S20 | Vendor Lock-In Assessment & Exit Planning | Quantify proprietary dependency and exit options. | Renewals; strategic sourcing; multi-cloud policy. | See [playbook](../04-scenario-playbooks/20-vendor-lockin.md) |

## Detailed what / when / how / why

### S01 — Application Portfolio Rationalization (APM / TIME)

| Lens | Detail |
|---|---|
| **What** | Categorize applications into Tolerate / Invest / Migrate / Eliminate using value, cost, and health. |
| **When** | Quarterly portfolio reviews; M&A integration; cost-reduction programs. |
| **How (in Orbus Infinity)** | Import CMDB + cost attributes; score applications; publish TIME views and heatmaps. |
| **Why** | Executives need a shared, governed portfolio view tied to investment decisions. |
| **Confidence** | medium |

### S02 — Technology Obsolescence & Lifecycle Risk (EOL/EOS)

| Lens | Detail |
|---|---|
| **What** | Track frameworks, OS, and runtimes approaching end of support. |
| **When** | Before major releases; security audits; annual tech radar updates. |
| **How (in Orbus Infinity)** | Maintain technology objects, standards, and lifecycle states; link to applications. |
| **Why** | Avoid unplanned risk and compliance exposure from unsupported stacks. |
| **Confidence** | medium |

### S03 — Target State Architecture & Cloud Migration

| Lens | Detail |
|---|---|
| **What** | Plan waves from as-is to cloud-native to-be architectures. |
| **When** | Cloud programs; data center exits; platform consolidation. |
| **How (in Orbus Infinity)** | Model current/target landscapes, roadmaps, and dependency constraints. |
| **Why** | Align delivery teams on sequenced change with visible dependencies. |
| **Confidence** | medium |

### S04 — Business Capability Modeling & Investment Alignment

| Lens | Detail |
|---|---|
| **What** | Map L1–L3 capabilities to systems and spend. |
| **When** | Strategy cycles; operating model redesign; budget allocation. |
| **How (in Orbus Infinity)** | Maintain capability hierarchies and realize/served-by links to applications. |
| **Why** | Connect IT spend to business outcomes leadership recognizes. |
| **Confidence** | medium |

### S05 — Architecture Review Board (ARB) & Design Approvals

| Lens | Detail |
|---|---|
| **What** | Enforce guardrails and record Architecture Decision Records. |
| **When** | Material designs; exceptions; standard deviations. |
| **How (in Orbus Infinity)** | Intake requests, capture decisions, attach diagrams, retain audit history. |
| **Why** | Prevent shadow IT and create an immutable decision ledger. |
| **Confidence** | medium |

### S06 — Continuous CMDB Synchronization & Baseline Hygiene

| Lens | Detail |
|---|---|
| **What** | Reconcile Orbus objects with ServiceNow (or similar) CIs. |
| **When** | Ongoing operations; audit prep; discovery after cloud growth. |
| **How (in Orbus Infinity)** | Integrate via connectors/Orbus Flow; resolve orphans and drift. |
| **Why** | Architecture repo must not diverge from operational inventory. |
| **Confidence** | medium |

### S07 — M&A Day-One IT Landscape Discovery

| Lens | Detail |
|---|---|
| **What** | Rapidly inventory an acquired estate. |
| **When** | Pre-deal diligence; Day-One; first 100 days. |
| **How (in Orbus Infinity)** | Stand up a fenced repository view; import discoveries; map overlaps. |
| **Why** | Speed and legal fencing matter more than perfect modeling. |
| **Confidence** | medium |

### S08 — Regulatory Compliance & Data Privacy (GDPR / DORA)

| Lens | Detail |
|---|---|
| **What** | Trace PII and critical data across systems and borders. |
| **When** | DPIAs; regulator inquiries; DORA ICT risk programs. |
| **How (in Orbus Infinity)** | Model data objects, flows, and system processing with classifications. |
| **Why** | Demonstrate control and lineage beyond slideware. |
| **Confidence** | medium |

### S09 — Interface & Integration Landscape Rationalization

| Lens | Detail |
|---|---|
| **What** | Inventory APIs and integration hubs; find zombies. |
| **When** | Platform consolidation; API programs; incident postmortems. |
| **How (in Orbus Infinity)** | Capture interfaces, consumers/providers, and integration patterns. |
| **Why** | Reduce brittle point-to-point and unmanaged endpoints. |
| **Confidence** | medium |

### S10 — Business Process Optimization & Journey Traceability

| Lens | Detail |
|---|---|
| **What** | Relate processes/journeys to supporting applications. |
| **When** | CX programs; shared-services redesign; bottleneck hunts. |
| **How (in Orbus Infinity)** | Model processes and links to applications/capabilities. |
| **Why** | Explain operational friction in business language. |
| **Confidence** | medium |

### S11 — AI Governance & ML Model Cataloging

| Lens | Detail |
|---|---|
| **What** | Catalog models, datasets, and risk tiers (incl. EU AI Act themes). |
| **When** | Model promotion; AI risk committees; audit. |
| **How (in Orbus Infinity)** | Register AI/ML assets and relationships to data/apps. |
| **Why** | Meet transparency and lineage expectations for AI systems. |
| **Confidence** | medium |

### S12 — Disaster Recovery & Business Continuity

| Lens | Detail |
|---|---|
| **What** | Align RTO/RPO and failover paths to architecture. |
| **When** | BCP tests; multi-region programs; critical service designation. |
| **How (in Orbus Infinity)** | Capture redundancy, recovery objectives, and dependency chains. |
| **Why** | Prove recoverability of business services, not only databases. |
| **Confidence** | medium |

### S13 — Technical Debt Quantification

| Lens | Detail |
|---|---|
| **What** | Make structural debt visible for investment cases. |
| **When** | OKR planning; platform funding; risk committees. |
| **How (in Orbus Infinity)** | Attach health/debt attributes to applications and components. |
| **Why** | Justify refactor funding with portfolio-level evidence. |
| **Confidence** | medium |

### S14 — Zero-Trust & Network Micro-Segmentation

| Lens | Detail |
|---|---|
| **What** | Describe trust zones and access paths. |
| **When** | Security architecture reviews; segmentation programs. |
| **How (in Orbus Infinity)** | Model zones, trust boundaries, and system placements. |
| **Why** | Communicate security architecture to non-network stakeholders. |
| **Confidence** | medium |

### S15 — Software Supply Chain & OSS Licensing

| Lens | Detail |
|---|---|
| **What** | Track components/licenses and SBOM-oriented risk. |
| **When** | Procurement; release gates; customer security questionnaires. |
| **How (in Orbus Infinity)** | Associate components/packages with applications where modeled. |
| **Why** | Reduce copyleft and vulnerability surprises. |
| **Confidence** | medium |

### S16 — FinOps & Unit Economics

| Lens | Detail |
|---|---|
| **What** | Attribute cloud/SaaS cost to products and capabilities. |
| **When** | Monthly FinOps; showback/chargeback; unit cost reviews. |
| **How (in Orbus Infinity)** | Import cost attributes; roll up to apps/capabilities. |
| **Why** | Tie architecture decisions to margin and run-rate. |
| **Confidence** | medium |

### S17 — Master Data & Golden Record Lineage

| Lens | Detail |
|---|---|
| **What** | Show authoritative sources and lineage for core entities. |
| **When** | MDM programs; data platform redesign. |
| **How (in Orbus Infinity)** | Model data entities, stores, and flows to consumers. |
| **Why** | Avoid competing 'sources of truth' without visibility. |
| **Confidence** | medium |

### S18 — ESG / Green IT Carbon Accounting

| Lens | Detail |
|---|---|
| **What** | Allocate digital estate emissions for disclosure. |
| **When** | Sustainability reporting cycles. |
| **How (in Orbus Infinity)** | Attach environmental attributes to tech/infra objects where used. |
| **Why** | Connect architecture choices to ESG metrics. |
| **Confidence** | medium |

### S19 — Team Topologies & Conway Alignment

| Lens | Detail |
|---|---|
| **What** | Relate org ownership to system boundaries. |
| **When** | Platform team design; post-reorg; scaling product orgs. |
| **How (in Orbus Infinity)** | Capture owners/teams on objects; analyze coupling. |
| **Why** | Detect socio-technical mismatch early. |
| **Confidence** | medium |

### S20 — Vendor Lock-In Assessment & Exit Planning

| Lens | Detail |
|---|---|
| **What** | Quantify proprietary dependency and exit options. |
| **When** | Renewals; strategic sourcing; multi-cloud policy. |
| **How (in Orbus Infinity)** | Tag vendor platforms; relate apps to proprietary services. |
| **Why** | Keep credible exit strategies before contracts renew. |
| **Confidence** | medium |


## Citations

- [@orbus-infinity-product]
- [@gartner-time]
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

