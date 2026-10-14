# 10.4 Concurrent Multi-Repo Cartography

Enterprise architecture documentation decays rapidly because code changes daily while documentation is updated quarterly. To maintain an accurate knowledge graph, the **Cartographer Agent** must continuously discover systems, services, databases, and dependencies directly from source code.

In a large enterprise with hundreds of microservices, running sequential repository scans is too slow, often taking hours or days. **Evo 2** introduces **Parallel Worktree Fleet Orchestration**, allowing the Cartographer to sweep entire enterprise portfolios concurrently while maintaining strict isolation.

---

## 1. The Fleet Architecture

Instead of cloning repositories one by one, a central **Cartographer Coordinator** splits the work across a fleet of sandboxed worker panes managed by **Herdr** and governed by **Omnigent**:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ CARTOGRAPHER COORDINATOR AGENT                                              │
│  1. Discovers 200 active repositories via GitHub / GitLab API               │
│  2. Partitions repositories into concurrency batches matching host CPU cores│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Spawns Parallel Herdr Panes
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ HERDR MULTI-WORKTREE FLEET (Concurrently Running in Sandboxes)              │
│                                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────────┐ │
│  │ Worker Pane 1        │  │ Worker Pane 2        │  │ Worker Pane N      │ │
│  │ Repo: payments-api   │  │ Repo: auth-service   │  │ Repo: inventory-svc│ │
│  │ Worktree: /tmp/wt/p1 │  │ Worktree: /tmp/wt/p2 │  │ Worktree: /tmp/wt/n│ │
│  │ AST / IaC Extractor  │  │ AST / IaC Extractor  │  │ AST / IaC Extractor│ │
│  └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬─────────┘ │
└─────────────┼─────────────────────────┼─────────────────────────┼───────────┘
              │ Typed PAM Delta JSON    │ Typed PAM Delta JSON    │
              └─────────────────────────┼─────────────────────────┘
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ATOMIC DELTA LAKE INGESTION (Databricks Unity Catalog)                      │
│   MERGE INTO ea.metamodel.nodes AS target                                   │
│   USING raw_extracted_batch AS source                                       │
│   ON target.urn = source.urn                                                │
│   WHEN MATCHED THEN UPDATE SET ...                                          │
│   WHEN NOT MATCHED THEN INSERT ...                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The 5-Step Parallel Cartography Pipeline

### Step 1: Inventory Discovery
The Coordinator queries the organization's Git provider (e.g., `GET /orgs/company/repos`) and filters for repositories that have had commits in the last 24 hours. Repositories are queued in batches based on available system hardware (`-j$(nproc)`).

### Step 2: Ephemeral Worktree Allocation
For each repository in the active batch, Herdr creates an isolated, lightweight Git worktree:
```bash
# Herdr allocates isolated checkout without cloning a fresh repo
herdr worktree create /tmp/ea-worktrees/task-payment-svc --branch main
```
This takes milliseconds because it shares the local Git object database rather than performing a full clone over the network.

### Step 3: Sandboxed AST & IaC Extraction
Inside each sandboxed pane, the Cartographer runs specialized, lightweight extractors:
- **Application Services:** Parses `package.json`, `pom.xml`, `pyproject.toml`, or `go.mod` to extract service names, versions, and dependencies.
- **Infrastructure & Cloud:** Inspects Terraform files (`.tf`), Kubernetes manifests (`deployment.yaml`), and Dockerfiles to identify cloud databases, message queues, and API gateways.
- **Code Connections (AST):** Analyzes import statements and HTTP client configurations to map relationships (`serves`, `accesses`, `flows_to`).

### Step 4: Metamodel Schema Validation
Before any data leaves the worker, the extracted entities are validated against the strict platform schemas:
```bash
# Ensures every discovered node adheres to PAM Contract 1.1
jsonschema -i extracted_nodes.json schemas/pam/nodes.schema.json
```
If a repository contains malformed syntax or non-standard configurations, the worker records a non-fatal warning in the evidence log and continues. **One broken repository never breaks the sweep for the rest of the enterprise.**

### Step 5: Atomic Batch Merge to Unity Catalog
Once all workers in the batch report the `done` state, Omnigent consolidates the extracted JSON files and executes an atomic Delta Lake `MERGE` query against Unity Catalog. 

Active services are marked with `lifecycle_status = 'run'`, while services that were deleted or removed from code are flagged as `retired` using standard slowly changing dimension (SCD2) tracking.

---

## 3. Performance & Safety Guardrails

| Constraint | Enforcement Mechanism | Purpose |
| :--- | :--- | :--- |
| **CPU Saturation** | Worker pool capped at `nproc - 1`. | Leaves dedicated CPU overhead for Backstage and host operations. |
| **Memory Exhaustion** | 512 MB memory limit per Herdr pane via Linux cgroups. | Prevents runaway AST parsers from consuming all system RAM. |
| **Disk Bloat** | Worktrees stored on an ephemeral `tmpfs` RAM disk; auto-pruned on exit. | Zero residual disk buildup after sweeps. |
| **Git API Rate Limits** | Omnigent outbound proxy caches Git API tokens and throttles requests. | Prevents hitting enterprise Git rate limits (e.g., 5,000 req/hr). |
| **Crash Containment** | Herdr pane isolation (`Ring 1`). | A crash or segmentation fault in one worker is isolated to that pane only. |

---

## 4. Benchmark: Sequential vs. Parallel Fleet

In an enterprise portfolio of **250 microservices**:

| Metric | Sequential Script (Evo 1 Baseline) | Parallel Fleet (Evo 2 with Herdr & Omnigent) | Improvement |
| :--- | :--- | :--- | :--- |
| **Total Sweep Duration** | 3 hours, 45 minutes | **14 minutes, 20 seconds** | **15.7× Faster** |
| **Failure Impact** | 1 unparseable repo stops the entire script. | Failed repos isolated to individual worker logs. | **Fault-Tolerant** |
| **Disk Space Consumed** | Up to 15 GB (separate git clones). | Under 800 MB (shared Git object database). | **94% Less Disk** |
| **Metamodel Freshness** | Weekly overnight cron job. | Continuous hourly micro-sweeps. | **Real-Time Accuracy** |

---

## 5. Summary

By combining **Herdr's** lightweight worktree multiplexing with **Omnigent's** sandboxed execution boundaries, the Agentic EA platform turns repository documentation from a dreaded manual audit into a continuous, automated background process that costs pennies and runs in minutes.
