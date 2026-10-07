# 3.2 — Developer inner loop

## Jobs of the inner loop

1. Author intended architecture beside code.
2. Validate metamodel + policy on every PR.
3. Compile Archify artifacts for human review.
4. Open remediation PRs (EOL, SBOM, missing owners).

## Typical toolchain

GitHub/GitLab → coding agent → schema/OPA → Archify finalize → review → merge → entity export to lakehouse.

## Scenarios dominated by inner loop

S02, S03, S05, S07, S09, S12, S13, S14, S15, S19, S20 (see [scorecard](../04-scenario-playbooks/99-master-scorecard.md)).

## Orbus relationship

Inner loop **replaces** Orbus as the system of enforcement. Orbus may still display published results during coexist.

## Citations

- [@opa-conftest]
- [@archify-github]
- [@backstage-software-catalog]


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

