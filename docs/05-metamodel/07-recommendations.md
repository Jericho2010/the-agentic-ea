# 6.7 — Chief architect recommendations

1. **Standardize on ArchiMate relation semantics** for edges; do not invent verbs. [@archimate-3-2]
2. **Use Backstage hierarchies for developer UX**; map cleanly into PAM layers. [@backstage-software-catalog]
3. **Store live graph in the lakehouse**; version schemas in Git; render with Archify. [@archify-github]
4. **Require aliases + evidence** from day one—or CMDB sync will poison trust.
5. **Coexist with Orbus Infinity** if needed for executive continuity, but make PAM authoritative for agents/CI.
6. **Pilot S01, S05, S08, S16** before boiling the ocean ([90-day pilot](../07-roadmap/02-ninety-day-pilot.md)).

## Ultimate result

Replace Orbus’s closed CoreEA *as the system of record for agents* with a living, open-standard autonomous knowledge graph—code-validated, lakehouse-refreshed, Archify-rendered.

## Citations

- [@orbus-coreea]
- [@archimate-3-2]
- [@backstage-software-catalog]
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

