# Archify bridge notes

## Valid architecture shape (conceptual)

```json
{
  "schema_version": "1",
  "diagram_type": "architecture",
  "meta": { "title": "Example", "quality_profile": "showcase" },
  "components": [
    { "id": "billing_api", "label": "Billing API" }
  ],
  "boundaries": [
    { "kind": "region", "label": "Applications", "wraps": ["billing_api"] }
  ],
  "connections": [
    { "from": "billing_api", "to": "billing_db", "label": "accesses" }
  ]
}
```

Exact fields must follow installed Archify `schemas/architecture.schema.json`. Always validate with `finalize`.

## Forbidden patterns from early research drafts

- Top-level `nodes` / `relationships`
- `boundaries[].type = domain|system|cloud`
- Assuming Archify accepts arbitrary property bags without schema

## Types

`architecture` | `workflow` | `sequence` | `dataflow` | `lifecycle`
