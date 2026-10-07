# 6.5 — Archify visual transformer bridge (schema-correct)

## Critical correction

Do **not** emit fake Archify JSON shaped as `nodes` / `relationships` / `boundary.type: domain|system|cloud`.

Current Archify **architecture** candidates use approximately:

- `components` (not nodes)
- `connections` (not relationships)
- `boundaries[]` with `kind` ∈ `region` | `security-group` and required `wraps` [@archify-github]

See also [`schemas/archify-bridge.md`](../../schemas/archify-bridge.md).

## Mapping rules

| PAM | Archify |
|---|---|
| layer strategy/application/technology clusters | `boundaries` with `wraps` component ids |
| node | `components[]` entry |
| edge | `connections[]` entry |
| scenario view choice | pick diagram **type** first via Archify router |

## Compile command (illustrative)

```bash
node bin/archify.mjs finalize architecture candidate.json out.html --quality showcase --json
```

## Citations

- [@archify-github]
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

