# 6.3 — Pragmatic Agentic Metamodel (PAM) specification

PAM combines ArchiMate-style relations with Backstage-friendly types and lakehouse storage.

## Layers

| Layer | Examples |
|---|---|
| strategy | Capability, BusinessProcess, Actor |
| application | Application, Service, API |
| technology | InfrastructureNode, TechnologyService, CloudResource |
| data | DataEntity, DataDomain, Dataset |
| governance | ADR, Standard, Control, AIModel |

## Relationship types (closed enum)

`realizes`, `serves`, `hosted_on`, `accesses`, `consumes`, `exposes`, `flows_to`, `governs`, `threatens`, `bundled_in`, `owned_by`

Prefer ArchiMate-aligned meanings; do not invent synonyms casually. [@archimate-3-2]

## Identity

```text
urn:ea:<layer>:<type>:<slug>
```

Example: `urn:ea:application:service:billing-api`

## Node fields (logical)

`urn`, `name`, `layer`, `type`, `owner_team`, `repo_url`, `attributes`, `last_updated_at`

## Edge fields

`source_urn`, `target_urn`, `relationship_type`, `attributes`, `last_updated_at`

## Supporting collections

- **aliases** — map CMDB sys_id, ARN, repo URL, billing tag → URN
- **evidence** — source, confidence, observed_at, pointer

See schema sketch: [`schemas/pam/metamodel.schema.json`](../../schemas/pam/metamodel.schema.json)

## Citations

- [@archimate-3-2]
- [@backstage-software-catalog]
- [@togaf-10]
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

