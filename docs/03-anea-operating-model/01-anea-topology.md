# 3.1 — ANEA topology (intended vs observed)

**ANEA** = Agent-Native Enterprise Architecture.

## Topology

```mermaid
flowchart TB
  subgraph inner [Developer_Inner_Loop]
    Git[Git_ADRs_IaC_OpenAPI]
    Agents[Coding_Agents]
    OPA[OPA_Gates]
    ArchifyCI[Archify_Finalize]
  end
  subgraph lake [Enterprise_Lakehouse]
    Ingest[AutoLoader_Snowpipe_Lakeflow]
    PAM[(PAM_Nodes_Edges)]
    Orch[Workflows_Tasks_DLT]
  end
  subgraph exec [Executive_Visual_Tier]
    Apps[Databricks_Apps_SiS]
    HTML[Archify_HTML_SVG]
    NL[Genie_Cortex]
  end
  Git --> Agents --> OPA --> ArchifyCI
  ArchifyCI --> PAM
  Ingest --> PAM
  Orch --> HTML
  PAM --> Apps
  PAM --> NL
  HTML --> Apps
```

## Dual-truth plane

| Plane | Sources | Failure if ignored |
|---|---|---|
| **Intended** | ADR, Terraform/Pulumi, OpenAPI, capability YAML, CODEOWNERS | Shadow architecture |
| **Observed** | CMDB CDC, CUR, VPC flow, OTel, MLflow, SBOM JSON | Comforting fiction |

Orbus Infinity primarily stores **declared** objects with connector assists. ANEA makes the dual plane explicit.

## Citations

- [@archify-github]
- [@databricks-autoloader]
- [@snowflake-snowpipe]
- [@wcid-agy-research]


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

