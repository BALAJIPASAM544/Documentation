Ran command: List test files (`Get-ChildItem -Path tests -File | Select-Object Name`)
Viewed crypto_service.py:1-60
Viewed routes_assessment.py:54-148
Viewed routes_assessment.py:320-343
Viewed routes_assessment.py:255-297
Viewed routes_planning.py:1-68
Ran command: Run pytest tests (`pytest -v`)

# Mira Modernize Platform — Complete Architectural & Functional Overview

**Mira Modernize** is an enterprise-grade, technology-agnostic application modernization platform. Powered by the **Google Agent Development Kit (ADK)** and state-of-the-art LLM reasoning, it automates the end-to-end journey of analyzing legacy codebases, evaluating migration feasibility, and generating phased, deterministic migration blueprints—all under strict human-in-the-loop architectural governance.

---

## 1. High-Level Architecture & Core Principles

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                           React + Vite Frontend                         │
  │   [Intake] → [Workflow Graph] → [Dashboard] → [Approval] → [Blueprint] │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │ REST / SSE Streaming
                                      ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                         FastAPI Application API Layer                  │
  │       /auth       /projects       /requests      /assessment     /planning  │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
  ┌───────────────────────────────────▼────────────────────────────────────┐
  │                 Mira Modernize Multi-Agent Orchestrator                │
  │                                                                        │
  │  Stage A: Request Intake & Normalization Agent                         │
  │                                                                        │
  │  Stage B: Assessment Pipeline (Sequential + Parallel ADK Tree)         │
  │    ├─ Repository Discovery Agent                                       │
  │    ├─ Technology Discovery Agent (Build manifests & code heuristics)   │
  │    ├─ Profile Selector (e.g., Java8To17Profile)                        │
  │    ├─ [PARALLEL ANALYSIS CLUSTER]                                      │
  │    │    ├─ Dependency Analysis Agent & Risk Matrix                     │
  │    │    ├─ Source Code Pattern Agent                                   │
  │    │    ├─ Framework Analysis Agent                                    │
  │    │    ├─ Configuration Analysis Agent                                │
  │    │    └─ Quality & Security Agent                                    │
  │    ├─ Findings Collector & Assessment Aggregator Agent                 │
  │    ├─ Feasibility & Alternative Agent                                  │
  │    └─ 5 Standard Assessment Reports Generator                          │
  │                                                                        │
  │  ────────────────── [HUMAN APPROVAL BOUNDARY (HITL)] ────────────────── │
  │                                                                        │
  │  Stage C: Migration Planning Agent                                     │
  │    └─ 5-Phase Blueprint • DAG Task Graph • Checkpoints • Rollback      │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
  ┌───────────────────────────────────▼────────────────────────────────────┐
  │                       Immutable Artifact Vault                         │
  │  requests/ • repository/ • technology/ • dependencies/ • findings/     │
  │  reports/  • feasibility/ • decisions/  • planning/blueprints          │
  └────────────────────────────────────────────────────────────────────────┘
```

### Core Design Foundations
1. **Multi-Agent Decomposition**: Replaces brittle monolithic prompts with single-responsibility agents executed either sequentially or in parallel (`SequentialAgent`, `ParallelAgent`).
2. **Deterministic Tools + LLM Reasoning**: Agents use deterministic read-only tools (parsers for Maven, Gradle, Ant, Pip, Poetry, AST extractors) to harvest empirical facts, then utilize LLM intelligence to evaluate architectural impact and remediation options.
3. **Artifact-Driven State Contracts**: All pipeline stages communicate strictly through immutable JSON schemas saved to the disk artifact store (`artifacts/`). Any stage can be inspected, replayed, or audited.
4. **Human-in-the-Loop (HITL) Boundary**: The platform **never** executes disruptive code transformations without an explicit human architect approval recorded in an immutable `migration-decision.json`.
5. **Scope Guardrails**: Granular scoping allows enterprises to modernize selectively (by repository, module, or subcomponent). Any generated task targeting out-of-scope code is flagged and reported.
6. **Zero-Trust Token Encryption**: Personal Access Tokens (PAT) for private Git repositories are client-encrypted using **RSA-OAEP with SHA-256** before transmission and decrypted securely in memory on the backend.

---

## 2. Feature & Functionality Breakdown

### Stage A: Intake & Normalization
* **Flexible Ingestion**: Ingests source repositories via Git Clone URL, local directory paths, or direct ZIP file uploads.
* **Technology Auto-Discovery**: Proactively inspects the codebase to identify languages, runtimes, build tools, and frameworks before submission.
* **Scope Specification**: Supports whole-repository modernization or strict sub-module scoping.
* **Intake Normalization**: Evaluates constraints, flags missing prerequisites, and generates the baseline contract: `modernization-request.json`.

---

### Stage B: Comprehensive Assessment Pipeline
* **Real-Time SSE Streaming**: Emits live progress events (`/assessment/stream`) so users observe each agent starting, discovering evidence, and completing in real-time.
* **5 Parallel Analytical Engines**:
  1. **Dependency Analysis**: Evaluates direct and transitive dependencies against target runtime compatibility matrices; pinpoints breaking version upgrades and sunset dependencies.
  2. **Source Analysis**: Scans source files for deprecated APIs, removed language constructs, import modifications, and syntax shifts.
  3. **Framework Analysis**: Evaluates core runtime frameworks (e.g., Spring Boot 1.x/2.x to 3.x, Jakarta EE migrations, config changes).
  4. **Configuration Analysis**: Reviews property files, XML beans, YAML configurations, and build manifests for deprecated properties.
  5. **Quality & Security Analysis**: Detects hardcoded secrets, security vulnerabilities, code smells, and test coverage gaps.
* **Aggregator & Feasibility Assessment**: Combines findings into an executive report with an overall feasibility status (`FEASIBLE`, `CONDITIONALLY_FEASIBLE`, `BLOCKED`) and alternative modernization strategies with risk ratings.
* **5 Standard Assessment Reports Generated**:
  1. *Dependency Risk Report*
  2. *Dependency Compatibility Matrix*
  3. *Feasibility & Readiness Report*
  4. *Architectural Impact Assessment*
  5. *Migration Risk Analysis*

---

### Human-in-the-Loop Architectural Sign-off
* **Strategy Selection**: Architects evaluate viable options (e.g., in-place migration, modular decomposition, parallel strangler pattern).
* **Governance Actions**:
  * **Approve**: Persists `migration-decision.json` and unlocks Stage C.
  * **Reject**: Halts the workflow and records justification.
  * **Re-Assess**: Takes feedback and additional architectural constraints to re-run the assessment without starting from scratch.

---

### Stage C: Migration Planning & Blueprint Generation
* **5 Structured Execution Phases**:
  * **Phase 1: Workspace & Baseline Isolation**: Isolates branches and snapshots baseline commit hashes.
  * **Phase 2: Build & Runtime Configuration**: Updates build manifests (Maven `pom.xml`, Gradle, compiler plugins).
  * **Phase 3: Dependency Upgrades**: Incrementally updates third-party libraries and coordinates.
  * **Phase 4: Source-Level & Framework Transformations**: Resolves package imports (e.g., `javax.*` to `jakarta.*`), deprecations, and business logic adapters.
  * **Phase 5: Automated Verification**: Executes unit test suites, integration tests, and quality gates.
* **Execution DAG**: Establishes prerequisite task chains (`taskGraph`) ensuring tasks run in topologically valid order.
* **Automated Checkpoints**: Enforces automated build validation and test-pass thresholds between phases.
* **Rollback & Safety Net**: Defines automated Git revert sequences and build cache restoration rules.
* **Scope Enforcer**: Inspects generated tasks and warns if any step touches files outside the declared scope.

---

### Frontend UI Capabilities
| Page / View | Key Features |
| :--- | :--- |
| **Intake Page** | Repository connection, ZIP drop zone, automatic tech stack detection, scope filters, and credential encryption. |
| **Workflow Page** | Interactive agent DAG visualizer with live SSE streaming status, animated states, and per-agent execution times. |
| **Dashboard** | High-level metrics (total files, direct dependencies, categorized findings) and 5 interactive report tabs. |
| **Findings Explorer** | Searchable table of code findings filterable by severity, category, module, and automation potential. |
| **Approval Portal** | Architectural review screen with risk trade-offs, strategy picker, notes, and approval/rejection triggers. |
| **Planning Page** | Complete Stage C Blueprint viewer with phase tabs, DAG dependencies, automation ratings, and scope tags. |
| **Artifact Vault** | Centralized repository of all versioned, immutable JSON artifacts generated across stages. |

---

# Speaker Notes: Explaining Mira Modernize (2 – 5 Minutes)

Use this script when presenting to technical leadership, clients, or engineering teams. Adjust pacing to fit your exact time window.

---

### ⏱ 0:00 – 0:45 | The Problem & The Mission
> *"Hello everyone. Today, every enterprise wants to move fast, adopt modern runtimes, and eliminate technical debt. But legacy application modernization remains slow, risky, and manually intensive.*
>
> *Teams often face thousands of files, outdated dependencies, breaking framework changes, and fear of breaking core business logic. Monolithic AI prompts don't solve this—they hallucinate, miss subtle dependencies, and lack guardrails.*
>
> *That’s why we built **Mira Modernize**—an agentic modernization platform powered by the **Google Agent Development Kit (ADK)** and advanced LLMs. It brings structure, deterministic inspection, and architectural governance to legacy migrations."*

---

### ⏱ 0:45 – 1:45 | Stage A & Stage B: The Multi-Agent Assessment Engine
> *"The platform works in three distinct stages: Stage A Intake, Stage B Assessment, and Stage C Planning.*
>
> *In **Stage A**, a team simply provides a Git repository or uploads an archive. The intake agent normalizes the request, discovers the underlying tech stack automatically, and establishes the migration boundaries.*
>
> *In **Stage B**, our ADK Multi-Agent pipeline takes over. Instead of one large prompt, specialized agents run in parallel:
> - One agent analyzes dependencies and builds a compatibility risk matrix.
> - Another inspects source code for deprecated APIs and breaking syntax.
> - Dedicated agents evaluate framework shifts, configuration files, and security risks.*
>
> *These agents harvest empirical facts using deterministic read-only tools, and an Aggregator synthesizes the findings into five comprehensive assessment reports that provide full visibility into technical debt and migration feasibility."*

---

### ⏱ 1:45 – 2:45 | The Human-in-the-Loop Governance Boundary
> *"Here is the most critical design philosophy of Mira Modernize: **Agents never make autonomous, unchecked architectural decisions.**
>
> *Once the assessment is complete, the system enters the **Awaiting Human Approval** state. 
>
> *Lead architects and engineering managers can review the feasibility report, examine alternative migration paths, and evaluate the trade-offs. 
>
> *From the UI, an architect can either:*
> 1. *Approve a specific modernization strategy,*
> 2. *Reject it with feedback, or*
> 3. *Request a re-assessment with updated architectural constraints.*
>
> *Every decision is cryptographically tracked as an immutable artifact before any execution planning begins."*

---

### ⏱ 2:45 – 4:00 | Stage C: Executable Migration Blueprint
> *"Once approved, **Stage C Migration Planning** is unlocked.
>
> *The Planning Agent converts the architectural decision into an actionable, step-by-step **Migration Blueprint**. 
>
> *The blueprint organizes the work across 5 logical phases:
> 1. Isolating the workspace and baseline commit.
> 2. Upgrading build descriptors and target runtimes.
> 3. Upgrading dependencies and third-party libraries.
> 4. Applying source-level code and framework refactoring.
> 5. Running automated verification test suites and quality gates.
>
> *Each task has defined dependencies forming a Directed Acyclic Graph (DAG), automated checkpoints, and rollback strategies. Furthermore, our scope engine guarantees that only files explicitly approved for modernization are modified."*

---

### ⏱ 4:00 – 5:00 | Summary & Impact (Wrap-Up)
> *"To summarize: Mira Modernize transforms what used to be a months-long, high-risk modernization guessing game into a predictable, automated, and auditable engineering process.
>
> - **Speed**: Automated multi-agent discovery reduces assessment time from weeks to minutes.
> - **Safety**: Scope guardrails, rollback plans, and human sign-off protect production stability.
> - **Determinism**: Every recommendation is backed by empirical artifact contracts.
>
> *Thank you! I'm happy to walk through a live demo or answer any questions."*

---

## 3. Quick Reference: Presentation Q&A Cheat Sheet

| Question | Recommended Answer |
| :--- | :--- |
| **How does it prevent AI hallucination?** | We combine deterministic tools (file finders, manifest parsers, AST analysis) with LLM reasoning. The LLM only interprets gathered evidence; it never invents repository structure. |
| **Can we modernize only one module of a mono-repo?** | Yes. Scoping allows configuring exact paths or module names. Any agent finding or generated task outside that scope is flagged as `OUT_OF_SCOPE`. |
| **How are credentials handled?** | Git Personal Access Tokens are encrypted client-side in the browser using RSA-OAEP before transmission, ensuring plaintext secrets are never exposed across network boundaries. |
| **What happens if a build fails during transformation?** | The Stage C blueprint specifies deterministic checkpoints and rollback strategies back to the baseline snapshot commit. |