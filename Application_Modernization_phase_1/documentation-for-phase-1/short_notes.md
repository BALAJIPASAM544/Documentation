Here is a short note on each agent in the **Mira Modernize Platform**:

# 📥 Stage A: Request Intake & Scoping
### 1. Modernization Request Intake Agent (`ModernizationRequestAgent`)
1. **What you're building**: An intake gateway that ingests natural language, user requests, or API payloads and normalizes them into a standardized [ModernizationRequest](file:///d:/Mira_modernize_stageC/app/models/modernization_request.py) contract.
2. **What problem it solves**: Raw modernization requests are often vague, ambiguous, or miss critical parameters (e.g., target language runtime, framework versions, repository URL, or in-scope/out-of-scope paths).
3. **How you're building it (tools, approach)**: 
   - **Tools**: Google ADK / Gemini / Azure OpenAI LLM prompting with strict Pydantic JSON schema parsing.
   - **Approach**: Extracts source/target runtimes, repository metadata, constraints, and scope boundaries; flags missing information before any codebase operations begin.
### 2. Reassessment Coordinator Agent (`ReassessmentCoordinatorAgent`)
1. **What you're building**: An intake feedback loop agent that handles user rejections, alternative strategy selections, and revised migration constraints.
2. **What problem it solves**: When human reviewers reject a proposed modernization strategy, the system must incorporate new boundaries without restarting the entire onboarding from scratch.
3. **How you're building it (tools, approach)**:
   - **Tools**: Artifact Service, [WorkflowStateEngine]
   - **Approach**: Appends user feedback and new constraints to the existing request artifact and rolls the state machine back to `REASSESSMENT_REQUIRED`.

---

# 🔬 Stage B: Codebase Discovery & Assessment Pipeline

### 3. Repository Discovery Agent (`RepositoryDiscoveryAgent`)
1. **What you're building**: A structural analyzer that maps repository layouts, module boundaries, directory trees, and total file counts into a `RepositoryManifest`.
2. **What problem it solves**: LLMs fail when fed unindexed codebases. This agent creates a deterministic topology map so downstream agents inspect only relevant code.
3. **How you're building it (tools, approach)**:
   - **Tools**: Python `os.walk`, `pathlib`, Git metadata, read-only filesystem utilities.
   - **Approach**: Deterministic file scanning and filtering (ignoring `.git`, `node_modules`, `target`, `.venv`) to catalog modules, sizes, and extensions without LLM hallucination.

### 4. Technology Discovery Agent (`TechnologyDiscoveryAgent`)
1. **What you're building**: An inspection agent that detects the underlying languages, runtimes, build systems, and application types (e.g., Spring Boot, Node/Express, Python/FastAPI).
2. **What problem it solves**: Teams often lack accurate, up-to-date documentation on legacy tech stacks.
3. **How you're building it (tools, approach)**:
   - **Tools**: Deterministic file signature checks (`pom.xml`, `package.json`, `build.gradle`, `requirements.txt`) combined with LLM fallback.
   - **Approach**: Matches manifest indicators against technology profiles, yielding confidence scores and evidence links in a `TechnologyInventory`.

### 5. Dependency Analysis Agent (`DependencyAnalysisAgent`)
1. **What you're building**: An agent evaluating direct and transitive third-party libraries against the target platform.
2. **What problem it solves**: Legacy dependencies often have no direct target support, contain breaking package renames (e.g., `javax.*` to `jakarta.*`), or have known vulnerabilities.
3. **How you're building it (tools, approach)**:
   - **Tools**: XML/JSON/TOML parsers (`pom.xml`, `package.json`), Modernization Profiles, LLM reasoning.
   - **Approach**: Extracts dependencies, checks target runtime compatibility matrices, and generates structured incompatibility findings. Runs concurrently inside an ADK `ParallelAgent`.

### 6. Source Analysis Agent (`SourceAnalysisAgent`)
1. **What you're building**: A deep-inspection agent that scans application source files for deprecated APIs, removed language constructs, and obsolete syntax.
2. **What problem it solves**: Identifies compilation-blocking changes across thousands of lines of code without manually reading every file.
3. **How you're building it (tools, approach)**:
   - **Tools**: AST/regex pattern matching, scope filtering, LLM sampling (`gpt-6-luna` / Gemini).
   - **Approach**: Samples in-scope source files based on target migration patterns and outputs line-referenced code snippets with severity ratings. Runs in parallel.

### 7. Framework Analysis Agent (`FrameworkAnalysisAgent`)
1. **What you're building**: An agent evaluating major framework version upgrades (e.g., Spring Boot 2.x to 3.x, Angular JS to Angular, Express to NestJS).
2. **What problem it solves**: Framework migrations introduce breaking lifecycle, configuration, and architectural paradigm shifts beyond simple syntax edits.
3. **How you're building it (tools, approach)**:
   - **Tools**: Framework-specific migration profiles and LLM reasoning.
   - **Approach**: Analyzes framework annotations, imports, and bootstrap classes against target specifications to pinpoint required architectural refactoring. Runs in parallel.

### 8. Configuration Analysis Agent (`ConfigurationAnalysisAgent`)
1. **What you're building**: An agent analyzing application configuration files (`application.properties`, `.yml`, `.env`, Dockerfiles, XML configs).
2. **What problem it solves**: Upgrades frequently deprecate or alter configuration property names, datasource connection formats, and environment setups.
3. **How you're building it (tools, approach)**:
   - **Tools**: YAML/Properties/XML parsers, LLM inspection.
   - **Approach**: Flags deprecated property keys, altered default behaviors, and environment-specific incompatibilities. Runs in parallel.

### 9. Quality & Security Agent (`QualitySecurityAgent`)
1. **What you're building**: A code health and security scanner assessing existing test coverage, anti-patterns, and vulnerabilities before migration begins.
2. **What problem it solves**: Migrating low-quality, untested code compounds risk and causes silent functional regressions.
3. **How you're building it (tools, approach)**:
   - **Tools**: Static analysis rules, test suite detection (JUnit, pytest, Jest), security pattern checks.
   - **Approach**: Flags missing unit tests and risky patterns as prerequisite risks in the assessment findings. Runs in parallel.

### 10. Assessment Aggregator Agent (`AssessmentAggregatorAgent`)
1. **What you're building**: A consolidation agent that deduplicates and unifies findings from all parallel analysis agents into an authoritative [AssessmentReport](file:///d:/Mira_modernize_stageC/app/models/assessment_report.py).
2. **What problem it solves**: Prevents finding fragmentation, resolves duplicate reports between source/framework agents, and categorizes findings by component and severity.
3. **How you're building it (tools, approach)**:
   - **Tools**: Deterministic ID normalization, deduplication algorithms, and Pydantic models.
   - **Approach**: Merges dependency, source, framework, configuration, and security findings into a single structured artifact.

### 11. Feasibility Agent (`FeasibilityAgent`)
1. **What you're building**: A strategic decision agent that determines if migration is viable (`FEASIBLE`, `CONDITIONALLY_FEASIBLE`, or `BLOCKED`), estimates effort, and enforces human review.
2. **What problem it solves**: Prevents projects from blindly executing transformations when critical blockers (e.g., unsupported proprietary SDKs) exist.
3. **How you're building it (tools, approach)**:
   - **Tools**: Heuristic risk matrix + LLM reasoning, [ArtifactService](file:///d:/Mira_modernize_stageC/app/services/artifact_service.py).
   - **Approach**: Evaluates total finding severity, generates alternative migration strategies with pros/cons, and marks workflow state as `AWAITING_APPROVAL` (Human-in-the-Loop boundary).

---

# 📋 Stage C: Migration Planning & Architecture

### 12. Migration Planner Agent (`MigrationPlannerAgent`)
1. **What you're building**: An architect agent translating the approved strategy and assessment findings into an ordered, executable [MigrationBlueprint](file:///d:/Mira_modernize_stageC/app/models/migration_blueprint.py).
2. **What problem it solves**: Transforming code all at once breaks builds and causes irrecoverable states. Changes must be ordered logically into discrete phases with dependencies, checkpoints, and rollback strategies.
3. **How you're building it (tools, approach)**:
   - **Tools**: Azure OpenAI / Gemini LLM reasoning over the `AssessmentReport` and `MigrationDecision`.
   - **Approach**: Synthesizes a phased plan (Phase 1: Workspace Baseline → Phase 2: Build & Dependencies → Phase 3: Framework & Config → Phase 4: Source Code → Phase 5: Test & Validation), assigning automated tasks and validation checkpoints.

---

# ⚡ Stage D: Controlled Transformation Agents

### 13. Stage D Orchestrator (`StageDOrchestrator`)
1. **What you're building**: The autonomous coordinator that drives the execution of the Stage C blueprint tasks.
2. **What problem it solves**: Static rule engines cannot adapt when a transformation fails midway. The orchestrator makes real-time decisions on sequencing, dispatching specialized agents, triggering checkpoints, and managing remediation loops.
3. **How you're building it (tools, approach)**:
   - **Tools**: Google ADK `LlmAgent`, Azure OpenAI (`gpt-6-luna`), ThreadPoolExecutor.
   - **Approach**: Autonomous step-by-step reasoning cycle (`ANALYZE` → `SELECT_AGENT` → `EXECUTE` → `VALIDATE` → `REMEDIATE` / `COMPLETE`) using context snapshots and state checkpoints.

### 14. Workspace Branch Agent (`WorkspaceBranchAgent`)
1. **What you're building**: An environment isolation agent managing Git branches, worktrees, and baseline commits.
2. **What problem it solves**: Transformation must never contaminate the original source code or default branch.
3. **How you're building it (tools, approach)**:
   - **Tools**: Git CLI wrappers, [WorkspaceManager](file:///d:/Mira_modernize_stageC/app/agents/transformation/workspace_manager.py).
   - **Approach**: Creates dedicated migration branches (e.g., `modernize/<project-id>`), commits baselines, and enforces out-of-scope file protection boundaries.

### 15. Build Configuration Agent (`BuildConfigurationAgent`)
1. **What you're building**: An agent modernizing build tool manifests (`pom.xml`, `build.gradle`, `package.json`, `pyproject.toml`).
2. **What problem it solves**: Upgrading compiler target versions, plugins, and build lifecycle configurations must precede source code updates.
3. **How you're building it (tools, approach)**:
   - **Tools**: XML/JSON AST and regex parsers, LLM contextual code generation.
   - **Approach**: Updates compiler targets (e.g., Java 8 `<source>1.8</source>` → Java 17 `<release>17</release>`), adjusts build plugins, and generates diffs.

### 16. Dependency Migration Agent (`DependencyMigrationAgent`)
1. **What you're building**: An agent upgrading package versions and swapping obsolete dependencies for modern equivalents.
2. **What problem it solves**: Manually researching and updating dozens of interdependent library versions leads to version mismatch conflicts.
3. **How you're building it (tools, approach)**:
   - **Tools**: Build file editors, compatibility lookup rules, LLM reasoning.
   - **Approach**: Replaces deprecated coordinates, updates semantic versions, and handles groupId/artifactId changes (e.g., `javax.servlet` to `jakarta.servlet`).

### 17. Source Transformation Agent (`SourceTransformationAgent`)
1. **What you're building**: An agent performing precise refactoring on application code files.
2. **What problem it solves**: Rewriting deprecated method calls, updated language constructs (e.g., switch expressions, records, type annotations), and removed APIs across classes.
3. **How you're building it (tools, approach)**:
   - **Tools**: In-context source code diff generator, LLM code transform prompting.
   - **Approach**: Receives the specific file, finding evidence, and target runtime specifications; outputs unified diffs, applies changes, and records file audit trails.

### 18. Framework Transformation Agent (`FrameworkTransformationAgent`)
1. **What you're building**: An agent applying structural framework upgrades across code and annotations.
2. **What problem it solves**: Complex framework shifts (e.g., Spring Security 5 WebSecurityConfigurerAdapter deprecation to SecurityFilterChain beans).
3. **How you're building it (tools, approach)**:
   - **Tools**: Architecture-guided LLM code synthesis.
   - **Approach**: Restructures class patterns, swaps annotation namespaces, and injects modern framework conventions.

### 19. Configuration Migration Agent (`ConfigurationMigrationAgent`)
1. **What you're building**: An agent rewriting configuration schemas, property files, and environmental manifests.
2. **What problem it solves**: Property renames and format changes that cause application startup failures after framework upgrades.
3. **How you're building it (tools, approach)**:
   - **Tools**: YAML/Properties parser, string manipulation, LLM rewriting.
   - **Approach**: Translates old configuration keys into their new equivalents while preserving existing custom values and comments.

### 20. Test Remediation Agent (`TestRemediationAgent`)
1. **What you're building**: An agent updating test suites to match modernized frameworks and libraries.
2. **What problem it solves**: Test suites break during upgrades (e.g., JUnit 4 `@Test` / `@Before` to JUnit 5 Jupiter `@Test` / `@BeforeEach`, Mockito version changes).
3. **How you're building it (tools, approach)**:
   - **Tools**: Test framework conversion prompts, test runner diagnostic parser.
   - **Approach**: Migrates test assertions, lifecycle hooks, and mock annotations so the test suite passes on the new runtime.
