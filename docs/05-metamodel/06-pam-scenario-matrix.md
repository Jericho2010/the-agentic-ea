# 6.6 — How PAM powers all 20 scenarios


| Scenario | Reads | Writes |
|---|---|---|
| S01 APM | Application, Service, Owner | attributes.time_disposition |
| S02 EOL | Service, repo_url | attributes.eol_status |
| S03 Migration | Application, hosted_on | target hosted_on edges |
| S04 Capabilities | Capability, realizes | capex_allocation, business_value |
| S05 ARB | ADR, Application | governs + approval receipt |
| S06 CMDB | InfrastructureNode, Service | hosted_on reconciliation |
| S07 M&A | raw discoveries | new Node/Service/API |
| S08 Privacy | Service, DataEntity | accesses + pii_classification |
| S09 Interfaces | Service, API | consumes/exposes |
| S10 Process | BusinessProcess, Application | latency on serves |
| S11 AI Gov | AIModel, DataEntity | realizes + risk_tier |
| S12 DR | InfrastructureNode, Database | rto_minutes, rpo_minutes |
| S13 Tech debt | Service, repo_url | complexity, churn_score |
| S14 Zero-Trust | Service, API, Node | zone boundaries, mTLS |
| S15 SBOM | Service, repo_url | SBOMPackage bundled_in |
| S16 FinOps | Service, InfrastructureNode | cost_monthly_usd |
| S17 MDM | DataEntity, DataDomain | flows_to golden lineage |
| S18 ESG | InfrastructureNode, CloudResource | carbon_kg_co2e |
| S19 Teams | Service, owner_team | team/communication edges |
| S20 Vendor | Service, SDKs | vendor_lock_in_risk |


When all scenarios share URNs and relation enums, cross-scenario queries become SQL/graph—not heroics.

## Citations

- [@wcid-agy-research]
- [@archimate-3-2]


## Chapter validation checklist

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

