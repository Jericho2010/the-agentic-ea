# 10.1 Solution Ideation (Evo 2): Architecture of the Agent Runtime Fabric

In **Evo 1**, we established the foundational architecture: Databricks as the data backbone, Backstage as the user portal, the open PAM metamodel, and Archify for visual diagrams. In that baseline, agents run as simple background scripts triggered by GitHub Actions or scheduled jobs.

**Evo 2** addresses the next operational frontier: **How do we run, supervise, and control dozens of autonomous agents safely at enterprise scale?**

When agents move from running simple read-only queries to actively inspecting hundreds of repositories, generating code, and evaluating infrastructure changes, we need a dedicated **Agent Runtime Fabric**.

---

## 1. Why We Need an Agent Runtime Fabric

Running autonomous AI agents in an enterprise introduces three practical challenges:

1. **The CLI Agent Wrapper Problem:** Developers use rich interactive coding tools (such as Claude Code, Cursor, or internal coding CLIs). Running these tools from automated backend services is notoriously fragile if done via basic shell scripts, because interactive tools expect a real terminal (PTY), ask interactive questions, and output styled text.
2. **The Blast-Radius Risk:** An autonomous agent executing shell commands must never be allowed to access personal credentials (`~/.ssh`, cloud tokens), mutate live git branches directly, or send data to unapproved external servers.
3. **The Collaboration Gap:** Traditional automation is one-directional (run a script $\rightarrow$ post a comment). If an architect wants to step in, guide the agent, or answer a clarifying question, they need a live shared session, not another meeting.

To solve these problems without building a massive proprietary platform, Evo 2 integrates two lightweight open-source technologies:
- **Omnigent:** The enterprise management and governance control plane.
- **Herdr:** The agent terminal and process multiplexer.

---

## 2. The Separation of Concerns

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: USER WORKSPACES                                                    │
> **Interactive Architecture Diagram (Archify Showcase):** The full interactive diagram is compiled at [`assets/diagrams/agent-runtime-fabric.html`](../../assets/diagrams/agent-runtime-fabric.html). You can inspect the standalone vector render at [`assets/diagrams/agent-runtime-fabric.svg`](../../assets/diagrams/agent-runtime-fabric.svg) and the machine-readable model at [`assets/diagrams/agent-runtime-fabric.json`](../../assets/diagrams/agent-runtime-fabric.json).

```mermaid
flowchart TD
  subgraph humans [Layer 1: Human Stakeholders (Part 9)]
    Dev[Software Engineer<br/><i>Code & IaC Author</i>]
    EA[Enterprise Architect<br/><b>Primary User: Editor-in-Chief</b>]
    CIO[CIO & Tech Leadership<br/><i>Portfolio & Risk Decisions</i>]
  end

  subgraph workspaces [Layer 2: The 3 User Workspaces (Part 9)]
    PR[GitHub PR Review Gate<br/><i>Developer In-Flow & ARB Bot</i>]
    BS[Backstage Unified Cockpit<br/><i>Databricks Apps • Maps & Copilot</i>]
    Dash[Databricks AI/BI<br/><i>TIME Matrix & FinOps Metrics</i>]
  end

  subgraph fabric [Layer 3: Evo 2 Agent Runtime Fabric]
    Omni[Omnigent Control Plane<br/><i>Spend Caps • PII Filters • Sandboxes</i>]
    Herdr[Herdr Terminal Multiplexer<br/><i>PTY Panes • Worktrees • State Tracking</i>]
  end

  subgraph agents [Layer 4: Autonomous Agent Workforce & AI Engines]
    Arch[Archify Visualizer<br/><i>SVG Compiler & Living Maps</i>]
    ARB[ARB Reviewer Agent<br/><i>Pre-Merge Compliance Checks</i>]
    LLM[Tri-Modal LLM Engine<br/><i>A: Mosaic | B: API | C: CLI</i>]
    Copilot[Strategic Copilot Agent<br/><i>What-If Blast Radius & ADRs</i>]
    Carto[Cartographer Agent<br/><i>AST & Cloud Auto-Discovery</i>]
  end

  subgraph backbone [Layer 5: Databricks Enterprise Data Backbone (Part 9)]
    LB[(Lakebase PostgreSQL<br/><i>Operational Catalog DB</i>)]
    PAM[(Unity Catalog PAM<br/><i>Nodes, Edges, Evidence</i>)]
    Gold[(Gold Scenario Marts<br/><i>TIME, EOL & Drift Marts</i>)]
  end

  %% Human to Workspaces
  Dev -->|submits PRs & code| PR
  EA ==>|steers architecture & waivers| BS
  CIO -->|monitors portfolio health| Dash

  %% Workspaces to Runtime Fabric
  PR -->|PR review webhook| Omni
  BS ==>|live session stream URL| Omni
  Omni -->|dispatches sandboxed PTYs| Herdr

  %% Herdr to Agents
  Herdr -->|spawns PR review pane| ARB
  Herdr -->|spawns Copilot PTY pane| Copilot
  Herdr -->|parallel worktree fleet| Carto

  %% Agent Collaborations
  ARB -->|delta JSON| Arch
  Arch ==>|attaches visual diff SVG| PR
  Arch -->|embeds living maps| BS
  ARB -.->|reasoning critique| LLM
  Copilot -->|synthesis query| LLM

  %% Data Backbone Operations
  Carto -.->|atomic Delta merge| PAM
  PAM -->|graph blast-radius query| Copilot
  PAM -->|syncs active nodes| LB
  LB -->|powers software catalog| BS
  PAM -->|builds scenario marts| Gold
  Gold -->|powers executive metrics| Dash
```

---

## 3. How the Fabric Works in Plain English

### Component 1: Omnigent (The Gateway & Policy Enforcer)
**Omnigent** acts as the front door for agent requests coming from Backstage or GitHub:
- **Budget Control:** It enforces daily token and dollar spending caps so an agent caught in a reasoning loop cannot run up an unexpected bill.
- **Privacy & Secret Protection:** It intercepts network traffic to ensure proprietary code, customer information, or cloud credentials are never transmitted to external APIs unredacted.
- **Model Router:** It transparently directs tasks to the right model—whether that is a Databricks Mosaic AI private endpoint, an external commercial API, or a local developer subscription CLI.
- **Session Sharing:** When an architect wants to see what an agent is doing, Omnigent provides a secure web link that streams the live session directly into the Backstage portal.

### Component 2: Herdr (The Agent's Hands & Eyes in the Terminal)
**Herdr** manages the actual operating system processes and terminal windows:
- **Real Terminal Environment:** Coding agents expect a full terminal (PTY). Herdr provides this, ensuring agents don't freeze or drop output.
- **Status Classification:** Herdr constantly monitors the terminal output and classifies what the agent is doing into four simple states:
  - `working`: The agent is actively thinking, writing code, or running a tool.
  - `blocked`: The agent has stopped to ask a human a question or request an approval.
  - `idle`: The agent is finished and waiting for the next instruction.
  - `done`: The assigned task has completed successfully.
- **Zero-Collision Worktrees:** When an agent needs to inspect or test code, Herdr creates a separate, lightweight folder (`git worktree`). This allows ten agents to work on the same codebase simultaneously without interfering with each other or modifying the main branch.

---

## 4. A Day in the Life: End-to-End Execution Flow

To see how the fabric operates without friction, consider what happens when a developer opens a pull request that introduces an unapproved database connection:

1. **Trigger:** The developer opens a GitHub pull request modifying Terraform code.
2. **Dispatch:** A lightweight GitHub Action sends a webhook to Omnigent: `"Review PR #42 against enterprise architecture standards."`
3. **Sandbox Setup:** Omnigent asks Herdr to create an isolated workspace and an ephemeral Git worktree containing only the PR diff.
4. **Execution:** Herdr launches the **ARB Reviewer Agent** inside a read-only operating system sandbox.
5. **Evaluation:** The agent queries the Unity Catalog PAM graph for approved database patterns, detects the violation, and calls Archify to render a visual architecture diff.
6. **Notification:** The agent finishes (`done`). Omnigent collects the generated SVG diagram and markdown explanation and posts them directly as a PR comment.
7. **Clean-Up:** Herdr destroys the ephemeral worktree and closes the terminal pane. No leftover files, no persistent daemon overhead, and zero security footprint.

---

## 5. Summary of Architecture Benefits

- **No Agent Lock-In:** You can switch underlying agent engines (Claude Code, Cursor, custom Python agents) without changing Backstage or Databricks code.
- **Enterprise Safe by Default:** Agents run with locked-down filesystem and network permissions.
- **Human-Centric:** Architects and developers can observe and steer agents in real time instead of waiting for asynchronous batch reports.
