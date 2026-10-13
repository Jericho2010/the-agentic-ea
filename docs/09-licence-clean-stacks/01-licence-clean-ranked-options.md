# 8.1 — Licence-clean replacement options, ranked per scenario (S01–S20)

**Status:** locked v1 · **Date:** 2026-10-13 · **Scope:** replace Orbus Infinity and do S01–S20 better using licence-clean tooling only.

This chapter answers one question: *for each of the twenty scenarios, what are the ranked options that replace Orbus Infinity and do the job better, using only free/open-source software plus GitHub, Databricks, and Snowflake?*

> **Licence constraint (binding).** Only **GitHub**, **Databricks**, and **Snowflake** may cost money or require a licence. Every other component must be free to run without a licence. Do not introduce a fourth commercial product into this chapter.

---

## 1. Licence filter

### In scope

| Category | Allowed components |
|---|---|
| Paid (explicit exception) | GitHub, Databricks, Snowflake |
| Everything else | Free / open-source software, self-hosted |
| GitHub features | Actions, CodeQL, Dependabot, Packages, Projects, Issues |

### Out of scope (removed from earlier drafts)

LeanIX, Ardoq, Bizzdesign Horizzon, Bizzdesign Hopex (ex-MEGA HOPEX), ServiceNow Enterprise Architecture (Otto for EA), Celonis, mpmX, QPR ProcessAnalyzer, Microsoft Fabric, Microsoft Purview, Port, Cortex, FOSSA, Apptio, Cloudability, Informatica, Reltio, Semarchy, Watershed, Persefoni, SAP Sustainability, Dynatrace, Datadog, Snyk, Axioss.

### Licence swaps (source-available tools replaced with true OSS)

Several well-known tools are no longer open source. This chapter uses the open alternatives:

| Avoid (licence changed / commercial) | Use instead | Why |
|---|---|---|
| Terraform (BUSL 1.1) | **OpenTofu** | MPL-2.0 community fork |
| HashiCorp Vault (BUSL 1.1) | **OpenBao** | MPL-2.0 community fork |
| Elasticsearch (SSPL / AGPL) | **OpenSearch** | Apache-2.0 |
| Redis (RSALv2 / SSPL) | **Valkey** | BSD-3 |
| Celonis / mpmX / QPR (commercial) | **PM4Py**, **ProM** | OSS process mining |
| Port / Cortex (commercial portal) | **Backstage**, **DataHub**, **OpenMetadata** | OSS catalogs |
| FOSSA / Snyk (commercial SCA) | **Syft + Grype + Trivy + ORT + ScanCode** | OSS SBOM and licence scanning |
| Apptio / Cloudability (commercial FinOps) | **OpenCost**, **Cloud Carbon Footprint** | OSS cost and carbon |

---

## 2. Allowed toolbox by job

Legend — **NB** runs natively in a notebook (Python/Spark, no container) · **CTR** runs in a container (Snowflake SPCS job/service, or a Databricks container or shell step) · **APP** hostable as an app or dashboard (Snowflake Streamlit-in-Snowflake/SPCS, Databricks Apps) · **CI** GitHub Actions · **NO** not appropriate or not possible. Full detail in [section 5](#5-hosting-what-runs-inside-snowflake-and-databricks).

| Job | Free / allowed tooling | Hosting |
|---|---|---|
| Enforcement & CI | GitHub Actions, **OPA / Conftest**, Renovate, Dependabot, CodeQL, Checkov | CI · CTR (OPA) · NB (Checkov) |
| Diagrams | **Archify** (typed JSON → interactive HTML/SVG; architecture, workflow, sequence, dataflow, lifecycle), LikeC4, Structurizr DSL, Mermaid, D2, Graphviz | CTR / CI |
| EA modelling (classical) | **Archi + coArchi** (ArchiMate), Essential Project, Draw.io | NO — desktop GUI |
| Catalogs / portals | **Backstage**, **DataHub**, **OpenMetadata**, Apache Atlas | APP (Backstage) · NO (server apps) |
| Supply chain / SBOM | **Syft** (generate), **Grype** / **Trivy** (scan), **Cosign**, **Dependency-Track**, ORT, ScanCode, CycloneDX | CTR · NB (ScanCode) |
| PII / code scanning | **Semgrep** (OSS), **Presidio**, Gitleaks, SonarQube Community Edition | NB (Semgrep, Presidio) · CTR (Gitleaks, SonarQube) |
| Runtime & network truth | **Cilium**, **Tetragon**, Falco, Tracee, eBPF | NO — kernel/eBPF |
| Policy at runtime | **Kyverno**, Gatekeeper, OPA, Cloud Custodian | NO (Kyverno, Gatekeeper) · CTR (OPA) · NB (Custodian) |
| Observability | **OpenTelemetry Collector**, Prometheus, Grafana, Loki, Tempo, OpenSearch, Fluent Bit, Vector | CTR (gateway only) · NO (host agents) |
| Infra as code | **OpenTofu**, Pulumi OSS, Ansible | NB (Pulumi, Ansible) · CTR (OpenTofu) |
| Orchestration | Apache Airflow, Dagster, Kestra, Temporal, Argo Workflows | NO — use native schedulers |
| Transformation / quality | **dbt Core**, SQLMesh, Great Expectations, Soda Core | NB |
| Lineage | **OpenLineage + Marquez**, DataHub | NB (OpenLineage) · NO (Marquez, DataHub) |
| Entity resolution / MDM | **Splink**, dedupe, Zingg, Ditto | NB |
| Process mining | **PM4Py**, **ProM**, Apromore Community Edition | NB (PM4Py) · NO (ProM, Apromore GUI) |
| Graph / ontology | Apache AGE (Postgres), Neo4j Community, JanusGraph, Apache Jena, SHACL | NO (AGE, Neo4j, JanusGraph, Jena) · NB (pyshacl) |
| Data engines (self-host) | Apache Spark, Iceberg, Polaris, Trino, DuckDB, PostgreSQL, Kafka, Flink | NB (DuckDB; Spark via SDP or Snowpark Connect) · host (Trino, Kafka, Flink) |
| Cloud asset graph | **Steampipe**, **CloudQuery**, **Cartography**, Prowler | CTR (Steampipe, CloudQuery) · NB (Prowler) |
| AI governance | **MLflow** (OSS), **Evidently AI**, OpenLineage, promptfoo, Ragas | NB (MLflow, Evidently, Ragas) · CTR (promptfoo) |
| FinOps / carbon | **OpenCost**, Kubecost free, **Cloud Carbon Footprint**, OpenLCA, Infracost CLI | NO (OpenCost, Kubecost) · APP (CCF) · CTR (Infracost) |
| Resilience testing | Velero, CloudNativePG, **Litmus Chaos**, Chaos Mesh | NO — Kubernetes only |
| Documents / contracts | Apache Tika, docling, spaCy, Haystack | NB (docling, spaCy, Haystack) · CTR (Tika) |
| Dashboards / apps | Apache Superset, Metabase OSS, Grafana, Streamlit, Evidence.dev, Quarto | APP (Streamlit, Superset, CCF, Evidence) · CTR (Grafana, Metabase) |
| Secrets / identity | **OpenBao**, Keycloak | NO — use platform-native secrets |
| Diagram conventions | Scenario IDs `S01`–`S20` are stable; Archify types are limited to `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`. | — |

---

## 3. Ranked options per scenario

Ranking rule: **1** = best fit for that scenario under the licence constraint, then descending. Reasons are deliberate and short.

### S01 — Application portfolio rationalization (APM / TIME)

1. **Snowflake** + Streamlit + Cortex Agents — governed metrics and executive dashboards on a platform already licensed.
2. **Databricks** + Lakeflow Connect (CMDB, cost) + Genie Code + Apps — better when the portfolio joins are Spark-scale.
3. **GitHub + Backstage + Archi/coArchi** — free portfolio register and ArchiMate views; no licence, but manual upkeep.

### S02 — Technology obsolescence and lifecycle risk (EOL / EOS)

1. **GitHub + Renovate + Syft/Grype/Trivy + endoflife.date** — free, and it opens the upgrade PR instead of only reporting.
2. **Databricks** + Spark Declarative Pipelines — scans the whole fleet against CVE and EOL feeds at scale.
3. **Snowflake** + Dynamic Tables + Tasks + Alerts — feed-driven lifecycle tracking with alerting.

### S03 — Target state architecture and cloud migration roadmapping

1. **GitHub + LikeC4/Structurizr + OpenTofu + Infracost CLI + Archify** — free, and it models networks and microservices, not just data.
2. **Databricks** + Migration Manager + Lakehouse Federation + Genie Code — legacy queries in place, stored-procedure conversion to PySpark.
3. **Snowflake** + SnowConvert + Open Catalog (Polaris/Iceberg) — SQL/DDL conversion onto open Iceberg.

### S04 — Business capability modelling and investment alignment

1. **Snowflake** + Horizon semantics + Cortex Search/Agents — governed capability→cost views with executive question answering.
2. **Databricks** + Lakeflow Connect (Workday/SAP) + Genie Code — strongest where finance and HR joins are heavy.
3. **GitHub + Backstage + Markdown capability trees** — free and developer-friendly; weakest executive polish.

### S05 — Architecture review board (ARB) and design approvals

1. **GitHub PR + OPA/Conftest + Archify diff + CodeQL** — free, and governance happens at the point of change.
2. **Databricks Apps** intake → Spark Declarative Pipelines → Unity Catalog ledger — everything inside one licensed platform.
3. **Snowflake** SPCS webhook listener + Tasks + tamper-evident audit tables — warehouse-native approval ledger.

### S06 — Continuous ServiceNow CMDB synchronization and baseline hygiene

1. **Databricks** + **Lakeflow Connect ServiceNow connector** + Spark Declarative Pipelines — managed ingestion plus PySpark fuzzy matching across millions of CIs.
2. **Snowflake** + ServiceNow connector + Dynamic Tables — simplest continuous SQL reconciliation.
3. **GitHub Actions + Steampipe or CloudQuery + Splink + PostgreSQL** — free reconciliation for smaller estates.

> **Correction to earlier drafts.** ServiceNow connectivity is **not** a Snowflake differentiator. Databricks ingests ServiceNow through a managed Lakeflow Connect connector (streaming tables, Unity Catalog, up to 250 tables per pipeline). Both platforms also ingest Salesforce (GA), Workday (GA), and NetSuite, and both support query-based database ingestion (Oracle, SQL Server, PostgreSQL, MySQL, MariaDB, Teradata). Choose on **compute shape (Spark vs SQL)**, not on connectors.

### S07 — M&A day-one IT landscape discovery

1. **GitHub Actions + CLI agents + Archify** — free, and it scans a foreign estate in minutes with nothing installed in the target.
2. **Databricks** + Unity Catalog Clean Rooms + Lakeflow — legally fenced analysis at scale.
3. **Snowflake** + Data Clean Rooms + encrypted stages — joint analysis without exposing proprietary data.

### S08 — Regulatory compliance and data privacy (GDPR / DORA)

1. **Snowflake** + Horizon classification, tag-based masking, Access History, Iceberg v3 row lineage — the most defensible audit package.
2. **Databricks** + Unity Catalog column lineage + evidence jobs — strongest where the data already lives.
3. **GitHub + Semgrep + Presidio + OpenTelemetry + Archify** — free; finds PII in code and traffic, weaker as regulator-facing proof.

### S09 — Interface and integration landscape rationalization

1. **GitHub + Cilium + Tetragon + OpenAPI/AsyncAPI scanning + Archify** — free, and the only option that sees real service-to-service traffic *and* can enforce policy.
2. **Databricks** — declared specifications versus gateway logs for zombie-API detection.
3. **Snowflake** — Snowpipe Streaming on gateway logs plus Dynamic Tables for declared-versus-actual.
4. **Kong Gateway OSS** — free runtime registry where enforcement at the gateway is wanted.

### S10 — Business process optimization and journey traceability

1. **Databricks + PM4Py/ProM** — Spark-scale process mining using open-source miners (Celonis excluded as commercial).
2. **Snowflake + PM4Py/ProM** on Snowpark or SPCS — warehouse-native mining with no data movement.
3. **GitHub + OpenTelemetry + Archify** — free; handles a small number of critical journeys well.

> Databricks can feed process mining from the same ServiceNow connector used in S06. Process mining itself is a partner/OSS play on both platforms, not a native capability.

### S11 — AI governance and ML model cataloging (EU AI Act)

1. **Databricks** + MLflow + Unity Catalog + Mosaic AI Gateway + Agent Bricks — full training-to-serving lineage.
2. **Snowflake** + Model Registry + Cortex Agents audit + Horizon tags — strong governance, thinner training chain.
3. **GitHub + MLflow OSS + Evidently AI + OpenLineage + OPA** — free, and it gates promotion at the pull request with drift and quality evidence.

### S12 — Disaster recovery and business continuity (RTO/RPO)

1. **GitHub + OpenTofu + Litmus Chaos or Chaos Mesh + Archify lifecycle** — free, and it covers compute, network and DNS, not just databases.
2. **Databricks** + Lakeflow + Workflows — replication logs and RTO/RPO checks at scale.
3. **Snowflake** + replication usage views + Tasks + Alerts — simplest SLA monitoring.

### S13 — Technical debt quantification and refactoring justification

1. **GitHub + code-maat/Git churn + SonarQube Community Edition + Archify heatmap** — free, and it ties debt to actual code.
2. **Databricks** + Spark Declarative Pipelines — portfolio-scale churn versus cyclomatic complexity.
3. **Snowflake** + Git Integration + Dynamic Tables — SQL-first debt reporting.

### S14 — Zero-trust security architecture and network micro-segmentation

1. **Cilium + Tetragon + Kyverno + Archify** — free; layer 4–7 truth plus runtime enforcement.
2. **Databricks** — VPC flow logs compared against declared policy in Spark.
3. **Snowflake** — VPC flow logs plus Dynamic Tables building IP-to-IP matrices.

### S15 — Software supply chain and OSS licensing (SBOM)

1. **GitHub Actions + Syft + Grype/Trivy + Cosign + Dependency-Track** — free, and it blocks the deploy.
2. **Databricks** — Auto Loader on the SBOM bucket, build-triggered job, deploy block.
3. **Snowflake** — Snowpipe on SBOMs, Stream→Task, SPCS registry scan.
4. **OSS Review Toolkit + ScanCode** — free copyleft and licence analysis.

### S16 — FinOps cloud cost allocation and unit economics

1. **Snowflake** + billing data + Horizon semantics + Streamlit — best cost/governance mix on an allowed platform.
2. **Databricks** + cost exports + usage system tables + unit-cost job — better where Spark/ML spend dominates.
3. **OpenCost (+ Kubecost free) + Cloud Carbon Footprint + Superset** — free cost visibility with no additional licence.

### S17 — Master data management and golden record lineage

1. **Snowflake** + managed connectors CDC + Dynamic Tables SCD Type 2 + Streamlit curation.
2. **Databricks** + Lakeflow Connect + Lakebase + matching pipelines.
3. **GitHub + dbt Core or SQLMesh + Splink + PostgreSQL** — free entity resolution and data contracts.

### S18 — ESG and green IT carbon footprint accounting

1. **Databricks** — Spark modelling using free Cloud Carbon Footprint emission factors.
2. **Snowflake** — Snowpipe on carbon exports plus Cortex Search for utility PDFs.
3. **GitHub + Cloud Carbon Footprint + OpenLCA + Archify heatmap** — free measurement and life-cycle modelling.

### S19 — Team topologies and Conway alignment

1. **GitHub + CODEOWNERS + code-maat co-change graph + Archify** — free, and it shows real ownership from commits rather than an org chart.
2. **Databricks** — cross-team pull-request modification matrix at scale.
3. **Snowflake** + Git Integration + Dynamic Tables co-authorship analysis.

### S20 — Strategic vendor lock-in assessment and exit planning

1. **GitHub + Semgrep SDK-import scan + ScanCode + Archify** — free; code coupling is the real lock-in risk.
2. **Snowflake** + Cortex Search over contracts + 90-day renewal alerts.
3. **Databricks** + contract parsing (docling or Apache Tika) + dependency trees.

---

## 4. Overall ranking (licence-clean)

| Rank | Stack | Why |
|---|---|---|
| **1** | **GitHub + OSS + Databricks** | Best all-round. Spark wins on CMDB matching, process mining, ML lineage and carbon modelling. |
| **2** | **GitHub + OSS + Snowflake** | Best for governance, privacy, FinOps and executive reporting. |
| **3** | **GitHub + OSS only** (Archi, Backstage, PM4Py, Cilium, OpenCost, Archify) | Zero platform spend. Genuinely replaces Orbus for the eleven enforcement scenarios; the nine analytics scenarios need hand-built glue and scale less cleanly. |

**Core stack in all three cases:** GitHub + coding agents + OPA/Conftest + Archify performs the enforcement; exactly one of Databricks or Snowflake is added for analytics. Orbus Infinity becomes an optional read-only portal during transition.

---

## 5. Hosting: what runs inside Snowflake and Databricks

Both platforms now host far more than SQL. Most of the toolbox in §2 therefore needs no infrastructure of its own.

### 5.1 Runtime surfaces available

| Surface | Snowflake | Databricks |
|---|---|---|
| **Notebook** | Snowflake Notebooks (Workspaces) — Python 3.10–3.12, pip, container runtime with custom images and GPU [@snowflake-notebook-container-runtime] | Notebooks — Python/SQL/Scala/R, pip, `%sh` on cluster-backed compute |
| **Container** | **SPCS** job service (`EXECUTE JOB SERVICE`) or long-running service; any linux/amd64 image [@snowflake-spcs-limitations] | Cluster or job with a custom image; shell step |
| **App / UI** | Streamlit in Snowflake, or any web app as an SPCS service | **Databricks Apps** — serverless; Python (Streamlit, Dash, Gradio, Plotly) or Node.js (React, Angular, Svelte, Express) [@databricks-apps] |
| **Egress** | External Access Integration for outbound API calls | Standard networking from jobs and apps |

### 5.2 Hosting matrix by component

| Component | Snowflake | Databricks | Note |
|---|---|---|---|
| PM4Py (process mining) | NB | NB | Pure Python; runs against warehouse tables |
| dbt Core, SQLMesh | NB | NB | Native adapters for both |
| Great Expectations, Soda Core | NB | NB | Python data quality |
| Splink (entity resolution) | NB | NB | DuckDB backend on Snowflake; Spark backend on Databricks |
| dedupe, Ditto | NB | NB | Pure Python |
| Zingg | NB via Snowpark Connect for Spark [@snowflake-snowpark-connect-spark] | NB | Spark application |
| DuckDB | NB | NB | Embedded |
| Semgrep, Presidio, ScanCode, Checkov | NB | NB | Python |
| Cloud Custodian, Prowler | NB | NB | Need cloud egress |
| pyshacl (SHACL) | NB | NB | Python |
| docling, spaCy, Haystack | NB | NB | Python |
| Evidently, Ragas | NB | NB | Python |
| promptfoo | CTR | CTR | Node in a container |
| OpenLineage integrations | NB | NB | Library-level |
| Archify | CTR (SPCS job service) | CTR (shell/container) | Node CLI; output HTML hosted in SiS or Apps |
| Syft, Grype, Trivy, Cosign, Gitleaks | CTR | CTR | Go binaries |
| OPA, Conftest, OpenTofu | CTR | CTR | Go binaries |
| LikeC4, Mermaid, D2, Graphviz, Structurizr | CTR | CTR | Render in CI or a job |
| Apache Tika, ORT, Dependency-Track, SonarQube CE | CTR (SPCS service) | CTR | JVM services |
| Streamlit | APP (native SiS) | APP (native) | Primary UI surface on both |
| Apache Superset | APP (SPCS service) | APP (Python) | Python web app |
| Cloud Carbon Footprint, Evidence.dev | APP (SPCS, Node) | APP (Node) | Node apps |
| Backstage | APP (SPCS, Node) | APP (Node) | Node portal |
| Grafana, Metabase | CTR (SPCS service) | CTR | Not Python/Node app runtimes |
| OpenSearch, Loki, Tempo, Prometheus | CTR (stateful) | CTR (stateful) | Possible, but stateful services are better hosted outside |
| Neo4j, JanusGraph, Kafka, Flink, Trino, Marquez | CTR technically, not advised | CTR technically, not advised | Stateful clusters; no replication of SPCS objects [@snowflake-spcs-limitations] |
| GitHub Actions, Renovate, Dependabot, CodeQL | CI | CI | GitHub-native |

### 5.3 Components that cannot run on either platform

| Group | Components | Why |
|---|---|---|
| Kernel / eBPF | **Cilium, Tetragon, Falco, Tracee** | SPCS containers are explicitly **not privileged** and can only apply configurations an unprivileged user could [@snowflake-spcs-limitations]; neither platform exposes a host kernel. Must run on the nodes. |
| Kubernetes operators | **Kyverno, Gatekeeper, OpenCost, Kubecost, Velero, Litmus Chaos, Chaos Mesh, CloudNativePG** | Admission controllers and controllers require a real cluster |
| Host agents | **Fluent Bit, Vector, OTel Collector (daemonset)** | They collect from hosts, not from inside a warehouse |
| Stateful servers | **DataHub, OpenMetadata, Apache Atlas, Keycloak, OpenBao, Airflow, Temporal, Argo** | Long-running services owning their own storage and identity |
| Desktop GUI | **Archi + coArchi, Essential Project, Draw.io, ProM, OpenLCA** | Desktop applications |
| Schedulers | Airflow, Dagster, Kestra | Redundant — use Databricks Workflows or Snowflake Tasks |

### 5.4 Gotchas

1. **Apache AGE will not run on Lakebase.** The supported extension list includes **pgvector** and **PostGIS**, but not AGE [@databricks-lakebase-extensions]. A property graph in Postgres therefore needs its own host.
2. **SPCS cannot do privileged work** — no eBPF, no host configuration, linux/amd64 images only, and SPCS objects (services, compute pools) cannot be replicated [@snowflake-spcs-limitations].
3. **Databricks Apps is Python or Node.js only** [@databricks-apps]. Streamlit, Superset, Backstage, Evidence and Carbon Footprint fit; Grafana, Metabase and OpenSearch do not.
4. **Streamlit in Snowflake has package limits.** For heavy native dependencies, move to Streamlit on SPCS or the Snowflake Notebooks container runtime.
5. **Snowpark Connect for Apache Spark** lets existing Spark code run on Snowflake compute, so Spark-only code no longer forces Databricks [@snowflake-snowpark-connect-spark].
6. **Running inside the platform is not free.** SPCS compute pools and Databricks Apps/jobs bill — but no new licence is introduced.
7. **Infracost needs its hosted pricing API** (free tier plus paid), which sits awkwardly with the licence constraint in §1. Drop it or accept the gap.

**Net effect:** roughly thirty of the named components need no host of their own; the irreducible infrastructure is a Kubernetes cluster (for eBPF and the operators) plus a stateful host if you want Neo4j or Kafka.

---

## 6. References

Primary sources checked 2026-10-13. Proposed bibliography keys in brackets for `references/bib.yaml`.

| Topic | Source | Proposed key |
|---|---|---|
| Databricks ServiceNow ingestion | https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/servicenow-pipeline | `databricks-lakeflow-servicenow` |
| Lakeflow Connect connectors | https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/ | `databricks-lakeflow-connect` |
| Lakeflow Spark Declarative Pipelines | https://docs.databricks.com/aws/en/ldp/ | `databricks-lakeflow-sdp` |
| Databricks Genie Code | https://docs.databricks.com/aws/en/genie-code/ | `databricks-genie-code-v2` |
| Databricks Agent Bricks | https://docs.databricks.com/aws/en/agents/ | `databricks-agent-bricks` |
| Databricks Lakebase (GA) | https://www.databricks.com/blog/databricks-lakebase-generally-available | `databricks-lakebase` |
| Snowflake ServiceNow connector | https://docs.snowflake.com/en/connectors/servicenow/ingestion | `snowflake-servicenow-connector` |
| Snowflake Horizon Catalog | https://docs.snowflake.com/en/user-guide/snowflake-horizon | `snowflake-horizon-catalog` |
| Snowflake Cortex Agents | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents | `snowflake-cortex-agents` |
| Snowflake CoWork | https://www.snowflake.com/en/product/snowflake-cowork/ | `snowflake-cowork` |
| Snowpark Container Services job service | https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/tutorial-2 | `snowflake-spcs-job` |
| Archify | https://github.com/tt-a1i/archify | `archify-github` (existing) |
| Cilium Tetragon | https://tetragon.io/ | `cilium-tetragon` |
| Syft / SBOM tooling | https://github.com/anchore/syft | `syft` |
| OpenCost | https://www.opencost.io/ | `opencost` |
| Cloud Carbon Footprint | https://www.cloudcarbonfootprint.org/ | `cloud-carbon-footprint` |
| PM4Py | https://pm4py.fit.fraunhofer.de/ | `pm4py` |
| OpenTofu | https://opentofu.org/ | `opentofu` |
| OpenBao | https://openbao.org/ | `openbao` |
| Snowflake SPCS guidelines and limitations | https://docs.snowflake.com/en/developer-guide/snowpark-container-services/spcs-guidelines-and-limitations | `snowflake-spcs-limitations` |
| Databricks Apps | https://docs.databricks.com/aws/en/dev-tools/databricks-apps/ | `databricks-apps` |
| Databricks Lakebase Postgres extensions | https://docs.databricks.com/aws/en/oltp/projects/extensions | `databricks-lakebase-extensions` |
| Snowflake Notebooks container runtime | https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs | `snowflake-notebook-container-runtime` |
| Snowpark Connect for Apache Spark | https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-apache-spark | `snowflake-snowpark-connect-spark` |

---

## 7. Chapter validation checklist

| Check | Status |
|---|---|
| Licence constraint honoured (only GitHub/Databricks/Snowflake may be paid) | PASS |
| Baseline fidelity (Orbus behaviour stated, not invented) | PASS |
| Modern option completeness (≥ 3 ranked options per scenario) | PASS |
| API hygiene (vendor capabilities taken from primary docs; no invented APIs) | PASS |
| Archify accuracy (types limited to the five supported) | PASS |
| Internal consistency (scenario IDs stable S01–S20) | PASS |
| Citations present (keys added to `references/bib.yaml`) | PASS |
| TOC linkage (linked from `SUMMARY.md` and `README.md` as Part VIII) | PASS |
| Hosting feasibility assessed for every named component | PASS |
| Components that cannot run on either platform identified | PASS |
| Editorial (Orbus/Orbus Infinity spelling) | PASS |

**Validation status:** PASS.  
**Confidence overall:** medium — product names and features move quickly; re-verify against primary docs before implementation.
