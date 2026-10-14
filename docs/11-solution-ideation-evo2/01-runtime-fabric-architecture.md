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
│   • GitHub PR Review Gate (Developers)                                      │
│   • Backstage Unified Cockpit (Enterprise Architects)                       │
│   • Databricks AI/BI Dashboards (CIO & Leadership)                          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Session API / WebSockets
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ LAYER 3: THE AGENT RUNTIME FABRIC (Evo 2)                                   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ OMNIGENT: Management & Governance Control Plane                       │  │
│  │  • Enforces spending limits and token quotas per team                 │  │
│  │  • Filters out sensitive personal data and secrets before API calls   │  │
│  │  • Generates secure URLs for live browser-based collaboration         │  │
│  │  • Manages operating system sandboxes (Bubblewrap / Seccomp)          │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │ Dispatches & Observes                 │
│  ┌───────────────────────────────────▼───────────────────────────────────┐  │
│  │ HERDR: Terminal Multiplexer & Process Manager (HERDR_ENV=1)           │  │
│  │  • Manages real terminal sessions (workspaces, tabs, and panes)       │  │
│  │  • Automatically detects agent status (Working, Blocked, Done, Idle)  │  │
│  │  • Handles safe text pasting and keyboard input                       │  │
│  │  • Creates disposable Git worktree folders for clean parallel tasks   │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │ Supervised Execution                  │
│  ┌───────────────────────────────────▼───────────────────────────────────┐  │
│  │ AUTONOMOUS AGENT WORKERS (Running Inside Sandboxes)                   │  │
│  │  • ARB Reviewer Agent (Checks pull requests against PAM rules)        │  │
│  │  • Cartographer Agent (Discovers code, cloud assets, and pipelines)   │  │
│  │  • Strategic Copilot Agent (Runs What-If simulations & drafts ADRs)   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Read / Write Knowledge Graph
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ LAYER 4: DATABRICKS ENTERPRISE DATA BACKBONE                                │
│   • Unity Catalog (PAM Delta Tables: nodes, edges, evidence)                │
│   • Lakebase Managed PostgreSQL (Backstage software catalog)                │
│   • Gold Scenario Marts (Pre-computed TIME, EOL, and FinOps analytics)      │
└─────────────────────────────────────────────────────────────────────────────┘
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
