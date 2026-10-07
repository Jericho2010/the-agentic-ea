# 6.4 — Lakehouse physical model (nodes/edges/aliases/evidence)

Illustrative DDL compatible in spirit with Unity Catalog or Snowflake (types may need dialect tweaks).

```sql
CREATE SCHEMA IF NOT EXISTS enterprise_architecture.metamodel;

CREATE TABLE enterprise_architecture.metamodel.nodes (
  urn STRING NOT NULL,
  name STRING NOT NULL,
  layer STRING NOT NULL,
  type STRING NOT NULL,
  owner_team STRING,
  repo_url STRING,
  cost_monthly_usd DECIMAL(18,2),
  cve_critical_count INT,
  carbon_intensity_kg INT,
  attributes VARIANT,
  last_updated_at TIMESTAMP
);

CREATE TABLE enterprise_architecture.metamodel.edges (
  source_urn STRING NOT NULL,
  target_urn STRING NOT NULL,
  relationship_type STRING NOT NULL,
  attributes VARIANT,
  last_updated_at TIMESTAMP
);

CREATE TABLE enterprise_architecture.metamodel.aliases (
  alias_namespace STRING NOT NULL,
  alias_value STRING NOT NULL,
  urn STRING NOT NULL,
  last_updated_at TIMESTAMP
);

CREATE TABLE enterprise_architecture.metamodel.evidence (
  evidence_id STRING NOT NULL,
  urn STRING,
  edge_source_urn STRING,
  edge_target_urn STRING,
  source_system STRING NOT NULL,
  confidence STRING NOT NULL,
  observed_at TIMESTAMP,
  pointer STRING,
  details VARIANT
);
```

## Citations

- [@databricks-unity-catalog]
- [@snowflake-horizon]
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

