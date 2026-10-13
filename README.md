# The Agentic EA

**An ideation manual for modernizing enterprise architecture practice**  
Baseline: **Orbus Infinity** → Agent-native tooling → Snowflake / Databricks data+AI backbone → open metamodel (PAM)

> Research and ideation only. Not a vendor implementation guide. Not affiliated with Orbus Software, Databricks, or Snowflake.

## How to read

1. Start with [Preface](docs/00-front-matter/preface.md) and [How to use this manual](docs/00-front-matter/how-to-use-this-manual.md).
2. Use the full hyperlinked contents in [SUMMARY.md](SUMMARY.md).
3. Follow a [reading path](docs/00-front-matter/reading-paths.md) for your role.
4. Authoring / validation rules: [AUTHORING.md](AUTHORING.md).

## Thesis

Orbus Infinity is the baseline enterprise architecture practice: a governed repository, a pruned metamodel (CoreEA), integrations, and ARB workflows. Modernization is not “draw nicer diagrams.” It is replacing a closed proprietary store with an **agent-validated, lakehouse-backed, Archify-rendered** knowledge graph—using Snowflake and/or Databricks as the analytical backbone.

## Master table of contents

### Front matter
- [F0 Preface](docs/00-front-matter/preface.md)
- [F1 How to use this manual](docs/00-front-matter/how-to-use-this-manual.md)
- [F2 Reading paths](docs/00-front-matter/reading-paths.md)
- [F3 Conventions](docs/00-front-matter/conventions.md)

### Part I — Orbus Infinity as Baseline
- [1.1 What Orbus Infinity is](docs/01-baseline-orbus/01-what-orbus-is.md)
- [1.2 CoreEA metamodel](docs/01-baseline-orbus/02-coreea-metamodel.md)
- [1.3 Capability map](docs/01-baseline-orbus/03-capability-map.md)
- [1.4 Twenty usage scenarios](docs/01-baseline-orbus/04-twenty-usage-scenarios.md)
- [1.5 Critique](docs/01-baseline-orbus/05-critique.md)
- [1.6 Baseline tables](docs/01-baseline-orbus/06-baseline-tables.md)

### Part II — Modernization Ladders
- [2.1 Paradigm shift](docs/02-modernization-ladders/01-paradigm-shift.md)
- [2.2 Earth — OSS](docs/02-modernization-ladders/02-earth-oss.md)
- [2.3 Moon — Agent-native](docs/02-modernization-ladders/03-moon-agent-native.md)
- [2.4 Mars — Frontier](docs/02-modernization-ladders/04-mars-frontier.md)
- [2.5 Four-column matrix](docs/02-modernization-ladders/05-four-column-matrix.md)
- [2.6 Visualization & verification](docs/02-modernization-ladders/06-visualization-verification.md)
- [2.7 Validation & rendering](docs/02-modernization-ladders/07-validation-rendering.md)
- [2.8 Delivery & observability](docs/02-modernization-ladders/08-delivery-observability.md)

### Part III — ANEA Operating Model
- [3.1 Topology](docs/03-anea-operating-model/01-anea-topology.md)
- [3.2 Inner loop](docs/03-anea-operating-model/02-inner-loop.md)
- [3.3 Lakehouse tier](docs/03-anea-operating-model/03-lakehouse-tier.md)
- [3.4 Executive tier](docs/03-anea-operating-model/04-executive-tier.md)
- [3.5 Control-plane model](docs/03-anea-operating-model/05-control-plane-model.md)

### Part IV — Twenty Scenario Playbooks
- [4.0 Index](docs/04-scenario-playbooks/00-scenario-index.md)
- [S01 APM / TIME](docs/04-scenario-playbooks/01-apm-time.md) · [S02 EOL](docs/04-scenario-playbooks/02-eol-eos.md) · [S03 Migration](docs/04-scenario-playbooks/03-target-state-migration.md) · [S04 Capabilities](docs/04-scenario-playbooks/04-capabilities.md) · [S05 ARB](docs/04-scenario-playbooks/05-arb-governance.md)
- [S06 CMDB](docs/04-scenario-playbooks/06-cmdb-sync.md) · [S07 M&A](docs/04-scenario-playbooks/07-ma-discovery.md) · [S08 GDPR/DORA](docs/04-scenario-playbooks/08-gdpr-dora.md) · [S09 Interfaces](docs/04-scenario-playbooks/09-interfaces.md) · [S10 Process](docs/04-scenario-playbooks/10-process-mining.md)
- [S11 AI Gov](docs/04-scenario-playbooks/11-ai-governance.md) · [S12 DR](docs/04-scenario-playbooks/12-disaster-recovery.md) · [S13 Tech debt](docs/04-scenario-playbooks/13-tech-debt.md) · [S14 Zero-Trust](docs/04-scenario-playbooks/14-zero-trust.md) · [S15 SBOM](docs/04-scenario-playbooks/15-sbom.md)
- [S16 FinOps](docs/04-scenario-playbooks/16-finops.md) · [S17 MDM](docs/04-scenario-playbooks/17-mdm.md) · [S18 ESG](docs/04-scenario-playbooks/18-esg-carbon.md) · [S19 Teams](docs/04-scenario-playbooks/19-team-topologies.md) · [S20 Vendor exit](docs/04-scenario-playbooks/20-vendor-lockin.md)
- [4.99 Master scorecard](docs/04-scenario-playbooks/99-master-scorecard.md)

### Part V — Platform Backbone
- [5.1 Why backbone](docs/06-platform-backbone/01-why-backbone.md)
- [5.2 Databricks map](docs/06-platform-backbone/02-databricks-map.md)
- [5.3 Snowflake map](docs/06-platform-backbone/03-snowflake-map.md)
- [5.4 Ingestion](docs/06-platform-backbone/04-ingestion.md)
- [5.5 Orchestration](docs/06-platform-backbone/05-orchestration.md)
- [5.6 Apps & notebooks](docs/06-platform-backbone/06-apps-notebooks.md)
- [5.7 Platform comparison](docs/06-platform-backbone/07-platform-comparison.md)
- [5.8 Fact-check notes](docs/06-platform-backbone/08-factcheck-notes.md)

### Part VI — Open Metamodel (PAM)
- [6.1 Semantic gap](docs/05-metamodel/01-semantic-gap.md)
- [6.2 Taxonomy spectrum](docs/05-metamodel/02-taxonomy-spectrum.md)
- [6.3 PAM specification](docs/05-metamodel/03-pam-spec.md)
- [6.4 Lakehouse DDL](docs/05-metamodel/04-lakehouse-ddl.md)
- [6.5 Archify bridge](docs/05-metamodel/05-archify-bridge.md)
- [6.6 PAM × scenarios](docs/05-metamodel/06-pam-scenario-matrix.md)
- [6.7 Recommendations](docs/05-metamodel/07-recommendations.md)

### Part VII — Adoption Roadmap
- [7.1 Migration postures](docs/07-roadmap/01-migration-postures.md)
- [7.2 90-day pilot](docs/07-roadmap/02-ninety-day-pilot.md)
- [7.3 Org operating model](docs/07-roadmap/03-org-operating-model.md)
- [7.4 Risks & anti-patterns](docs/07-roadmap/04-risks-antipatterns.md)
- [7.5 Research backlog](docs/07-roadmap/05-research-backlog.md)

### Part VIII — Licence-clean replacement options
- [8.1 Licence-clean ranked options per scenario (S01–S20)](docs/09-licence-clean-stacks/01-licence-clean-ranked-options.md)
- [8.2 Databricks-hosted reference solution (C1–C15, S01–S20)](docs/09-licence-clean-stacks/02-databricks-reference-solution.md)

### Appendices
- [A Glossary](docs/08-appendices/glossary.md)
- [B Bibliography](docs/08-appendices/bibliography.md)
- [C Validation log](docs/08-appendices/validation-log.md)
- [D Source map](docs/08-appendices/source-map.md)

## Major tables

- [Orbus capability baseline](docs/01-baseline-orbus/03-capability-map.md)
- [Earth / Moon / Mars matrix](docs/02-modernization-ladders/05-four-column-matrix.md)
- [20-scenario catalog](docs/01-baseline-orbus/04-twenty-usage-scenarios.md)
- [Master scorecard](docs/04-scenario-playbooks/99-master-scorecard.md)
- [Databricks vs Snowflake for EA](docs/06-platform-backbone/07-platform-comparison.md)
- [PAM taxonomy](docs/05-metamodel/03-pam-spec.md)
- [PAM × 20 scenarios](docs/05-metamodel/06-pam-scenario-matrix.md)

## License

MIT — see [LICENSE](LICENSE).
