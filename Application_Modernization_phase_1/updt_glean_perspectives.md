Ran search for roadmap files
Checked task Search for roadmap files
Killing task Search for roadmap files
Ran list all git branches
Analyzed implementation-decisions.md:L1-100
Analyzed implementation-decisions.md:L101-107
Analyzed pre-scan.md:L1-60
Analyzed pre-scan.md:L61-140
Analyzed pre-scan.md:L141-220

Here is a comprehensive breakdown of the **updates planned for the Mira Modernize Platform**, divided into:
1. **The Core Feature Roadmap & Backlog** (already planned and specified in the codebase via [pre-scan.md](file:///d:/BALAJI/Mira_modernize_stageC/pre-scan.md) and active feature branches).
2. **The Enterprise Governance & Institutional Memory Upgrades** (required to directly answer the 6 organizational questions about approved stacks, banned packages, coding standards, and past learnings).

---

### Part 1: Core Feature Roadmap & Backlog (In-Flight in Codebase)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              IN-FLIGHT PLATFORM ROADMAP                                │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ 1. Lightweight Pre-Scan Layer  │ 2. Stack Coupling Engine  │ 3. Multi-Provider Git Pub │
│    • Component auto-discovery  │    • Cross-layer coupling │    • Direct PRs to GitHub │
│    • Frontend/Backend split    │    • Shared contract maps │    • GitLab & Bitbucket   │
│    • Scoped recommendations    │    • Microservice topology│    • Automated change log │
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

#### 1. Lightweight Repository Pre-Scan & Recommendation Engine ([pre-scan.md](file:///d:/BALAJI/Mira_modernize_stageC/pre-scan.md))
- **Zero-Friction Ingestion**: Allows users to provide a Git URL or folder *without* having to specify target frameworks upfront.
- **Automated Component Classification**: Automatically partitions repositories into `frontend`, `backend`, `shared libraries`, `data/persistence`, and `infrastructure` (supporting monorepos).
- **Target Recommendation Cards**: Generates evidence-based modernization options (e.g., Frontend Modernization, Backend Modernization, or Combined) with risk scores, migration rationale, and prerequisites mapped into `ModernizationRequest`.

#### 2. Stack Coupling & Architecture Topology Detection (`feature/1013`)
- **Cross-Layer Coupling Analysis**: Maps tight couplings between frontend clients and backend APIs (e.g., hardcoded REST endpoints, shared DTO types, serialization formats).
- **Service Boundary Discovery**: Detects whether legacy modules are modular monoliths, tight spaghetti, or distributed microservices to guide safe modernization phases.

#### 3. Enterprise Git Publishing Integration (`feature/1016`)
- **Multi-Provider Adapters**: Native integration with **GitHub, GitLab, and Bitbucket** APIs via personal access tokens or OAuth.
- **Automated PR / MR Creation**: Automatically commits modernized code from the sandbox workspace into a new branch (`modernize/<project-id>`) and opens a pull request with an architectural changelog, test execution summaries, and validation reports.

#### 4. Stage E Toolchain Expansion & Self-Healing Resilience (`feature/1015`)
- **Broader Compiler Coverage**: Expanding beyond Maven and Gradle to first-class support for `dotnet build/test`, `cargo check`, `go test`, and monorepo build tools (`pnpm`, `turborepo`, `nx`).
- **Remediation Loop Hardening**: Enhancing AST-level self-healing in Stage D when Stage E encounters compilation or assertion failures.

---

### Part 2: Enterprise Governance & Institutional Memory Upgrades
*(Planned enhancements to enable the agent to answer enterprise policy and institutional questions)*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ENTERPRISE GOVERNANCE & POLICY LAYER                            │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ 1. Enterprise Policy Store     │ 2. Prohibited Library Reg │ 3. Cross-Project RAG Mem  │
│    • Approved Java/Runtime LTS │    • Corporate Blacklist  │    • Past project lessons │
│    • EA Recommended Frameworks │    • License compliance   │    • Anti-pattern library │
│    • Preferred Cloud Targets   │    • Sunset package flags │    • Retrospective notes  │
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

#### 1. Enterprise Architecture Policy Store (`EnterprisePolicyRegistry`)
- **What it solves**: Gives the agent built-in organizational context on approved runtime versions (e.g., *"Company policy mandates Java 17 or 21 LTS"*), recommended frameworks (e.g., *"Spring Boot 3.3 with Virtual Threads"*), and cloud destinations (*"Azure AKS"*).
- **Implementation**:
  - Extend [app/profiles/base.py](file:///d:/BALAJI/Mira_modernize_stageC/app/profiles/base.py) to load company-wide policy profiles (YAML/JSON or database).
  - Inject organizational mandates into Stage A intake and Stage B assessment automatically.

#### 2. Corporate Prohibited Library & Licensing Registry
- **What it solves**: Detects libraries that are forbidden by corporate security or legal teams even if they don't have active CVEs (e.g., unapproved logging frameworks, banned utility libraries, GPL/AGPL copyleft licenses).
- **Implementation**:
  - Add an enterprise blacklist validator to [dependency_vulnerability_assessment.py](file:///d:/BALAJI/Mira_modernize_stageC/app/agents/assessment/dependency_vulnerability_assessment.py).
  - Automatically flag forbidden packages as `POLICY_VIOLATION` in Stage B findings.

#### 3. Enterprise Coding Standards & Linter Rule Engine
- **What it solves**: Enforces client-specific code conventions (e.g., Domain-Driven Design, Java records for DTOs, constructor injection, immutability) during Stage D refactoring.
- **Implementation**:
  - Allow uploading corporate Checkstyle, Spotless, SonarQube, or ESLint rules.
  - Bind these rules to the prompts of [source_transformation_prompt.py](file:///d:/BALAJI/Mira_modernize_stageC/app/prompts/source_transformation_prompt.py) and [test_remediation_prompt.py](file:///d:/BALAJI/Mira_modernize_stageC/app/prompts/test_remediation_prompt.py).

#### 4. Cross-Project Institutional Memory (Modernization RAG)
- **What it solves**: Enables the platform to remember past project successes, roadblocks, and lessons learned across teams.
- **Implementation**:
  - Shared vector store / knowledge index indexing past migration retrospectives, build recovery resolutions, and developer feedback.
  - When ingesting a new repository, the agent automatically retrieves:
    > *"In Project X (migrated last month), upgrading library Y caused memory leaks in containerized environments. Recommended alternative: Z."*

---

### Summary Checklist for Reference

| # | Update Item | Category | Target Benefit |
| :---: | :--- | :--- | :--- |
| **1** | **Repository Pre-Scan Layer** | Core Platform | Zero-friction ingestion; auto-detects components before target selection. |
| **2** | **Stack Coupling Detection** | Architecture | Identifies cross-layer API & model dependencies in monorepos. |
| **3** | **Unified Git Publishing** | DevEx / CI/CD | One-click PR creation for GitHub, GitLab, and Bitbucket. |
| **4** | **Stage E Compiler Expansion** | Validation | Deeper build/test execution across Java, .NET, Node, Go, Rust. |
| **5** | **Enterprise Policy Registry** | Governance | Auto-resolves approved Java versions, target frameworks, and cloud platforms. |
| **6** | **Prohibited Library Registry** | Security/Legal | Flags company-banned libraries and copyleft licensing violations. |
| **7** | **Coding Standards Injector** | Code Quality | Enforces company architecture rules during code refactoring. |
| **8** | **Cross-Project Memory (RAG)** | Institutional AI | Learns from past modernization projects and prevents recurring mistakes. |
