# 2.7 — Validation & rendering engine

In agent-native EA, diagram generation is a **compiler pipeline**, not a screenshot.

```text
Intent/Observed facts
    → PAM entity emission (schema validate)
    → Policy checks (OPA/Conftest)
    → Archify candidate JSON (type-specific schema)
    → finalize (validate → deliver → check → browser-check)
    → HTML/SVG artifact + receipt
```

## Gates that matter

1. **Metamodel gate** — unknown types/relations fail CI.
2. **Policy gate** — e.g., public API without owner blocked.
3. **Archify gate** — structural/layout/quality profile checks. [@archify-github]
4. **Evidence gate** — claimed edges need `evidence` rows when marked observed.

## Anti-pattern

LLM → PNG attached to Confluence with no schema, no PAM URN, no receipt.

## Citations

- [@archify-github]
- [@opa-conftest]
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

