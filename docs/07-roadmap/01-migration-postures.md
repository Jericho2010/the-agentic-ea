# 7.1 — Migration postures (coexist / strangler / greenfield)

| Posture | Description | When |
|---|---|---|
| **Coexist** | Orbus Infinity remains exec portal; PAM+agents become system of enforcement/facts | Political/contract constraints; large user base in Orbus |
| **Strangler** | Scenario-by-scenario cutover (start S05/S02 CI, then S01 lakehouse) | Default recommendation |
| **Greenfield** | No Orbus; Backstage+PAM+lakehouse from day one | New platform org / post-Orbus exit |

## Strangler sequence (recommended)

1. Stand up PAM schema in Git + empty lakehouse tables.
2. Turn on PR ARB (S05) and EOL/SBOM gates (S02/S15).
3. Ingest CMDB+CUR; publish TIME app (S01/S16).
4. Privacy lineage (S08).
5. Retire Orbus modules as PAM coverage ≥ threshold.

## Citations

- [@orbus-infinity-product]
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

