# 2.3 — Moon ladder — agent-native tooling

Moon adds **coding agents, policy-as-code, and verified visualization** on top of Earth.

## Core Moon moves

1. Agents parse repos (AST, IaC, OpenAPI) and emit PAM-valid entities.
2. OPA/Conftest gates block non-compliant architecture changes. [@opa-conftest]
3. Archify compiles typed JSON to interactive HTML/SVG with `finalize` gates. [@archify-github]
4. Renovate/Dependabot + Syft/Grype automate EOL/SBOM remediation paths.
5. PR becomes the ARB surface: ADR + policy result + Archify visual diff.

## Representative Moon tools

| Concern | Tools (illustrative) |
|---|---|
| Verified diagrams | Archify [@archify-github] |
| Collaborative agent canvas | Eraser DiagramGPT / MCP [@eraser-io] |
| Architecture DSL | LikeC4, Structurizr [@likec4] [@structurizr] |
| Policy | OPA, Conftest [@opa-conftest] |
| SBOM | Syft, Grype, CycloneDX [@cyclonedx] |
| Catalog UX | Backstage + entity providers [@backstage-software-catalog] |
| Coding agents | Cursor, Claude Code, Codex, Gemini CLI, agy — *harness choice is contextual* |

## Moon without a lakehouse

Moon can run locally/CI for many scenarios (S02, S05, S09, S13, S15). It struggles when questions need enterprise-scale joins (S01, S08, S16) or heavy graph mining (S06, S10).

## Citations

- [@archify-github]
- [@eraser-io]
- [@opa-conftest]
- [@cyclonedx]
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

