# MITRA AI
**Miracle Integration Transformation Accelerator**

> *Mitra (Sanskrit): friend, ally, companion — the partner you need to navigate complex migrations.*

---

## Business Challenge

Enterprise customers running MuleSoft face a confluence of pressures: rising licensing costs, End-of-Life runtime deadlines, and the daunting task of understanding their own integration estate before they can migrate anywhere. Manually inventorying flows, documenting integrations, assessing complexity, and planning a migration sequence takes weeks to months per customer engagement —
before a single line of new code is written.

The problem is not just technical. It is organizational. Teams cannot prioritize what they cannot see. They cannot sequence migrations they cannot map. They cannot estimate timelines without complexity data. And they cannot build confidence with stakeholders when the current state is a black box.

MITRA AI exists to change that.

---

## What is MITRA AI?

MITRA AI is a platform by Miracle Software Systems that compresses MuleSoft migration engagements from months to days. It combines deterministic code analysis, AI-generated documentation, and intelligent agent workflows into a unified platform that gives integration teams a complete picture of their estate — and a clear path forward.

The platform is organized around three capabilities:

---

### MITRA Analyze — Evaluation & Analysis Engine

MITRA Analyze is the first tool in the platform and the foundation of every migration engagement. A customer uploads their MuleSoft application exports. MITRA Analyze parses every XML configuration file and DataWeave transformation, produces a complete inventory of every flow and connector, scores the complexity of each flow with a full deterministic audit trail,
builds a dependency graph across applications, generates Integration Requirement Documents (IRDs) per flow, produces a sequenced migration project plan, and provides a knowledge chat agent scoped to the entire project.

What previously took weeks of manual discovery work completes in **24–48 hours**.

---

### MITRA Build — Development Acceleration Toolkit *(coming soon)*

MITRA Build picks up where MITRA Analyze leaves off. Using the IRDs and architecture diagrams produced during analysis, MITRA Build accelerates the actual development of replacement integrations on the target platform — generating boilerplate, suggesting patterns, and reducing the time from architecture decision to working code.

---

### MITRA Observe — Observability & Self-Healing Platform *(coming soon)*

MITRA Observe provides post-migration visibility. Once integrations are running on their new platform, MITRA Observe monitors health, detects anomalies, and surfaces self-healing recommendations — closing the loop on the migration lifecycle.

---

## MITRA Analyze — Deep Dive

The key scope of the `AI Fellowship` exercise is expected to be focussed on `MITRA AI - Analyze`.

### What MITRA Analyze Does

A customer uploads their MuleSoft application exports. MITRA Analyze:

1. Parses every XML config file and DataWeave (DWL) file in the uploaded ZIPs
2. Produces a complete inventory of every flow and subflow
3. Identifies every connector, system, and integration element — per flow
4. Scores the complexity of each flow deterministically with a full audit trail
5. Builds a dependency graph across flows and applications
6. Flags missing dependencies prominently so nothing is silently incomplete
7. Generates Integration Requirement Documents (IRDs) per flow
8. Produces a prioritized migration project plan
9. Generates current-state MuleSoft and future-state AWS architecture diagrams
10. Provides a knowledge chat agent scoped to the entire project

---

### Content Hierarchy

MITRA Analyze organizes MuleSoft content using MuleSoft's native hierarchy:

```text
Project
└── Application  (one per uploaded ZIP export)
    └── Flow
        └── Subflow
```

- **Project** — top-level workspace, represents one customer engagement
- **Application** — a single MuleSoft application, uploaded as a ZIP export from Anypoint Studio or Anypoint Platform
- **Flow** — a named integration flow defined via `<flow>` in XML config
- **Subflow** — a reusable component defined via `<sub-flow>`, called via `<flow-ref>`

---

### User Experience Flow

```text
1. Create Project
   ├── Enter project name and metadata
   └── Select migration target: Mule → AWS  (only option in Phase 1)

2. Upload Application(s)
   ├── Upload ZIP export from Anypoint Studio / Anypoint Platform
   ├── System extracts and parses XML, DWL, pom.xml, mule-artifact.json,
   │   and properties files
   ├── Dependency resolution runs — missing applications flagged immediately
   └── Analysis pipeline begins (async, progress shown per stage)

3. Review Analysis Results  [Phase 1]
   ├── Flow & subflow inventory
   ├── Per-flow structured analysis (trigger → processing → transform → destination)
   ├── Integration element and connector map
   ├── Dependency graph (with missing dependency indicators)
   └── Complexity scores with full scoring breakdown

4. Enrich & Document  [Phase 2]
   ├── Upload supplemental docs per flow or application
   │   (existing IRDs, PDFs, API specs, sample payloads, JSON logs)
   ├── Review AI-generated IRDs per flow
   ├── Edit IRDs inline or via chat
   └── Respond to agent clarification prompts

5. Plan Migration  [Phase 2]
   ├── Assign priority labels (P1 / P2 / P3) to applications
   ├── Review auto-generated migration sequence based on dependency graph
   └── Adjust sequencing manually if needed

6. Customize Component Mapping  [Phase 4]
   ├── Review default Mule → AWS component mapping
   └── Override per-project preferences via UI or chat

7. Generate Architecture Diagrams  [Phase 4]
   ├── Review current-state MuleSoft flow diagrams
   ├── Review proposed AWS architecture diagrams
   └── Edit diagrams visually or refine via chat

8. Chat & Explore  [Phase 3]
   ├── Project-level or application-level scoped queries
   └── Answers drawn from all analysis, IRDs, source code, and uploaded docs
```

---

## Phase 1 — Application Analysis

### What's Inside a MuleSoft Application ZIP

| File / Directory | Purpose |
| --- | --- |
| `src/main/mule/*.xml` | Flow definitions — primary analysis target |
| `src/main/resources/*.dwl` | DataWeave transformation files |
| `src/main/resources/*.yaml` / `*.properties` | Configuration and environment properties |
| `pom.xml` | Maven dependencies — authoritative connector list with versions |
| `mule-artifact.json` | Runtime version, secure properties flag, required features |

---

### Connector Identification Strategy

The parser uses a **two-pass approach** to identify connectors deterministically — no hardcoded static list required.

**Pass 1 — Namespace extraction from XML.**
Every MuleSoft connector declares a unique XML namespace prefix. The parser scans all XML files and extracts every unique prefix in use (e.g., `salesforce:`, `sqs:`, `db:`, `kafka:`).

**Pass 2 — Resolution via `pom.xml`.**
The `pom.xml` dependency list maps each connector to its exact artifact ID, group ID, and version. The combination of XML namespace + `pom.xml` entry gives a deterministic, version-accurate identification of every connector in the application.

**Unrecognized namespaces** — any prefix not resolvable via `pom.xml` is flagged as an unknown connector and surfaced as an agent clarification request to the user.

---

### Missing Dependency Handling

When a flow references another flow (`flow-ref`) or application that has not been uploaded into the project, MITRA Analyze flags this prominently at every relevant level. Missing dependencies are never silently ignored.

#### Dependency Graph View
- Missing applications render as **ghost nodes** — dashed border, gray fill, ⚠️ badge
- Edges connecting to missing nodes are rendered as **dotted lines** rather than solid
- Tooltip on hover: *"Application `payments-api` referenced but not yet uploaded"*

#### Application Card
- Applications with unresolved dependencies display a banner:
  **⚠️ Incomplete — 2 dependency applications not yet uploaded**

#### Flow Detail View
- Any `flow-ref` pointing to a flow outside the uploaded ZIPs is flagged inline:
  *"References `process-payment-subflow` in application `payments-api` — not uploaded"*

#### Complexity Score — Provisional State
When dependencies are missing, the complexity score is rendered as **provisional**:
- Displayed as: `6+ ⚠️ (incomplete — missing dependencies may increase score)`
- A definitive score is only assigned once all dependencies are resolved or explicitly marked out of scope

#### Resolution Paths
Missing dependency flags are cleared in one of two ways:
1. **Upload the missing application** — system re-analyzes and resolves automatically
2. **Mark as out of scope** — user acknowledges the dependency won't be migrated; flag converts from a warning ⚠️ to an informational note ℹ️ and the complexity score is finalized with a notation

---

### Per-Flow Structured Analysis Schema

Every flow produces a structured record with seven sections. Sections 1–5 are **fully deterministic** (parsed directly from XML and DWL). Section 6 is deterministic with an optional AI advisory note. Section 7 is AI-generated.

---

#### Section 1 — Flow Identity

| Field | Source | Description |
| --- | --- | --- |
| Flow Name | XML `name` attribute | Exact name from config |
| Flow Type | XML element | `Flow`, `Sub-Flow`, or `Private Flow` |
| Source File | File path | Which XML file contains this flow |
| Application Name | Parent ZIP | Which application this belongs to |
| Mule Runtime Version | `pom.xml` `app.runtime` | e.g., `4.6.0` |
| Is Referenced By | `flow-ref` scan | Flows that call this flow |
| References | `flow-ref` scan | Flows and subflows this flow calls |
| Missing Dependencies | `flow-ref` resolution | References that could not be resolved — flagged ⚠️ |

---

#### Section 2 — Trigger (Source System)

Every flow has exactly one trigger. Classified into one of the following:

| Trigger Type | XML Elements |
| --- | --- |
| **HTTP / HTTPS Inbound** | `http:listener` |
| **API-Managed Inbound** | `apikit:router` — RAML or OAS-backed, has API policies |
| **Scheduled / Polling** | `scheduler` — cron expression or fixed frequency |
| **Message Queue Consumer** | `jms:listener`, `vm:listener`, `anypoint-mq:subscriber`, `sqs:receive-messages`, `kafka:consumer`, `amqp:consumer`, `ibm-mq:listener`, `azure-service-bus:listener` |
| **File / SFTP Watcher** | `file:listener`, `sftp:listener`, `ftp:listener` |
| **Database Polling** | `db:listener` |
| **SaaS Event / Streaming** | `salesforce:subscribe-topic`, `salesforce:subscribe-channel`, `salesforce:subscribe-streaming-channel` |
| **No Own Trigger** | Sub-flow or private flow — triggered only via `flow-ref` |
| **Custom / Java** | `spring:object`, `scripting:execute` as entry point |

**Captured per trigger:** connector name, namespace prefix, configuration details, security posture (OAuth2, mTLS, client ID enforcement, API policy), and protocol.

---

#### Section 3 — Processing Steps

An ordered list of every step within the flow body, each classified by type:

| Step Type | XML Elements | Description |
| --- | --- | --- |
| `TRANSFORM` | `ee:transform`, `transform-message` | DataWeave mapping |
| `ENRICH` | `http:request` (lookup), `db:select` (lookup) | Calls external system to enrich payload |
| `ROUTE` | `choice`, `round-robin`, `scatter-gather`, `first-successful` | Conditional branching or fan-out |
| `ASYNC` | `async` scope, `parallel-foreach`, `batch:job` | Asynchronous or parallel processing |
| `CALL_FLOW` | `flow-ref` | Delegates to another flow or subflow |
| `PERSIST` | `db:insert/update/delete`, `os:store`, `file:write`, `s3:put-object` | Writes data to a store |
| `PUBLISH_EVENT` | `jms:publish`, `vm:publish`, `sqs:send-message`, `kafka:publish`, `anypoint-mq:publish` | Publishes to queue or topic |
| `NOTIFY` | `email:send`, `slack:post-message`, `sns:publish` | Sends notifications |
| `VALIDATE` | `jwt:validate`, expression validators | Validates payload or token |
| `ERROR_HANDLE` | `try`, `error-handler`, `on-error-continue`, `on-error-propagate` | Error handling boundaries |
| `LOG` | `logger` | Logging step |
| `SET_DATA` | `set-payload`, `set-variable`, `set-attributes` | Sets or mutates data |
| `CUSTOM_CODE` | `java:invoke`, `scripting:execute` | Custom Java or script — flagged for human review |

---

#### Section 4 — Transformations

Dedicated section for DataWeave analysis — the primary complexity driver.

**Per transformation captured:**

| Field | How Determined |
| --- | --- |
| File reference | Inline DWL or external `.dwl` filename |
| Input MIME type | `application/json`, `application/xml`, `text/csv`, etc. |
| Output MIME type | Same |
| Complexity estimate | Deterministic: line count + nesting depth + custom function count + use of `reduce` / `groupBy` / recursive patterns |
| Uses external DWL modules | Whether it imports shared `.dwl` library files — reusability signal |
| Mapping summary | AI-generated one-liner, e.g. *"Maps Salesforce Account to internal Customer schema"* |

**DWL Complexity Tiers:**

| Tier | Indicators |
| --- | --- |
| **Low** | Flat field mapping, under 30 lines, no custom functions |
| **Medium** | Conditional logic, 30–100 lines, standard library use |
| **High** | Recursive functions, 100+ lines, custom modules, multi-format handling, `reduce` / `groupBy` patterns |

---

#### Section 5 — Destination (Target System)

A flow can write to or call one or more destinations. Each is captured:

| Destination Type | XML Elements |
| --- | --- |
| **DATABASE_WRITE** | `db:insert`, `db:update`, `db:delete`, `db:stored-procedure` |
| **DATABASE_READ** | `db:select` when result is terminal or returned to caller |
| **QUEUE_PUBLISH** | `jms:publish`, `vm:publish`, `sqs:send-message`, `kafka:publish`, `anypoint-mq:publish`, `azure-service-bus:send` |
| **FILE_WRITE** | `file:write`, `sftp:write`, `ftp:write`, `s3:put-object`, `azure-blob-storage:upload` |
| **API_CALL** | `http:request` — outbound REST or SOAP call to external service |
| **SAAS_WRITE** | `salesforce:create/update/upsert`, `workday:invoke`, `servicenow:invoke`, `sap:invoke`, `netsuite:invoke`, and other SaaS write operations |
| **NOTIFICATION** | `email:send`, `slack:post-message`, `sns:publish` |
| **RESPONSE_RETURN** | HTTP response returned to caller (request-reply flows) |
| **CACHE_WRITE** | `redis:`, `os:` (Object Store) |
| **FLOW_CALL** | `flow-ref` to internal flow |

---

#### Section 6 — Complexity Score

Fully deterministic with scoring breakdown shown to users for auditability. AI advisory notes are clearly labeled as non-deterministic.

| Scoring Factor | Points |
| --- | --- |
| Trigger complexity | +1 (simple HTTP) to +3 (API-managed + policies + OAuth + mTLS) |
| Number of processing steps | +1 per 3 steps, capped at +3 |
| Transformation complexity | +1 (low DWL) to +3 (high DWL, multiple transforms) |
| Number of destinations | +1 per destination beyond the first |
| Async / batch patterns present | +2 if `batch:job` present |
| External system variety | +1 per unique external system type (SaaS, DB, queue, file, API) |
| Custom code present | +2 if `java:invoke` or `scripting:execute` |
| Error handling depth | +0 (none) / +0.5 (basic) / +1 (comprehensive multi-type handling) |
| Cross-app dependencies | +1 per `flow-ref` pointing outside this application |
| Unresolved dependencies | Score rendered as provisional ⚠️ until resolved |

**Complexity Tiers:**

| Score | Tier | Description |
| --- | --- | --- |
| 1–3 | **Low** | Simple passthrough, single connector, minimal logic |
| 4–6 | **Medium** | Multi-step processing, moderate transformation |
| 7–9 | **High** | Complex orchestration, heavy DWL, multiple systems |
| 10 | **Critical** | Large batch jobs, multi-system orchestration, custom code |

**AI Advisory Note** (optional, clearly labeled): The AI may add an observation such as *"DWL logic appears to implement a custom pricing algorithm — manual review recommended."* This is never the sole basis for a complexity tier.

---

#### Section 7 — Agent Clarification Requests

Questions surfaced to the user when the agent cannot deterministically resolve something. Examples:
- *"This flow calls an HTTP endpoint at `${api.endpoint.url}` — what system does this connect to?"*
- *"A custom Java class `com.example.CustomProcessor` is invoked — can you describe what it does?"*
- *"Flow references `process-order-subflow` which was not found in any uploaded application — is it defined elsewhere?"*
- *"Connector namespace `xyz:` could not be resolved via pom.xml — what is this connector?"*

---

### Dependency & Reusability Graph

Across all uploaded flows and applications, the system builds a directed dependency graph:

- **Node** = each flow or subflow
- **Edge** = a `flow-ref` from one flow to another
- **Ghost node** = referenced application or flow not yet uploaded — displayed with ⚠️ indicator

From this graph the system identifies:
- Flows with no dependents (leaf flows — safe to migrate independently)
- Flows with high fan-in (widely reused — high risk to migrate early)
- Cross-application dependencies (flow in App A calls flow in App B)
- Circular dependency warnings
- Missing applications that must be uploaded before analysis is complete

This graph is the primary input to the project plan generator in Phase 2.

---

## Phase 2 — Documentation Generation

### Integration Requirement Documents (IRDs)

An IRD is generated per flow using the structured analysis from Phase 1 plus any supplemental documentation the user provides.

**IRD sections:**
- Flow purpose and business context (AI-generated, human-editable)
- Trigger mechanism and source system
- Input data contract (schema, MIME type, sample payload if available)
- Step-by-step processing narrative
- Transformations — what maps to what, and why
- Output data contract and destination systems
- Error handling behavior
- Dependencies on other flows and external systems
- Open questions and pending clarifications

**IRD editing modes:**
- **Inline edit** — the IRD renders as a web page; users edit text directly
- **Chat update** — user describes a change conversationally; agent updates the document
- **External doc upload** — attach PDFs, existing IRDs, API specs, JSON logs, or sample payloads per flow or application to improve AI context

### Project Plan Generation

Once multiple applications are analyzed and dependencies are mapped:

- Applications with no dependencies → candidate **P1**
- Applications whose dependencies are resolved first → candidate **P2**
- Highly complex, deeply coupled, or custom-code-heavy applications → candidate **P3+**
- Applications with unresolved / missing dependencies → **blocked** until resolved or marked out of scope
- User-assigned priority labels can override auto-suggested sequence
- Output: visual sequenced project plan with dependency rationale shown per application

---

## Phase 3 — Knowledge Chat Agent

A centralized chat interface over all project knowledge.

**Knowledge sources:**
- Original XML and DWL source files from all uploaded ZIPs
- Per-flow structured analysis records (all seven sections)
- AI-generated and human-edited IRDs
- External documentation uploaded per flow or application
- Human clarification responses
- Dependency graph and complexity scores

**Scope levels:**
- **Project scope** — queries across all applications
- **Application scope** — scoped to a single application
- **Flow scope** — deep-dive on a specific flow

**Example queries:**
- *"Which flows use the Salesforce connector?"*
- *"What applications depend on the Order Processing application?"*
- *"List all flows with complexity score 7 or above."*
- *"What does the Customer Sync subflow do and who calls it?"*
- *"Which flows have unresolved dependencies?"*
- *"Which flows have no error handling?"*

---

## Phase 4 — Migration Architecture & Diagrams

### Default Mule → AWS Component Mapping

Built-in reference mapping provided at project creation. Users can customize per project via UI or chat.

| MuleSoft Component | Default AWS Mapping | Notes |
| --- | --- | --- |
| HTTP Listener / REST API | API Gateway + CloudFront + WAF | CDN and WAF included by default |
| APIkit Router (managed API) | API Gateway + Usage Plans + Authorizers | Policies map to Lambda authorizers |
| VM Queue (VMQ) | SQS (Standard or FIFO) | FIFO for ordered queues |
| Anypoint MQ | SQS + SNS | Fan-out → SNS + SQS |
| JMS / ActiveMQ | Amazon MQ | Direct equivalent |
| IBM MQ | Amazon MQ for IBM MQ | |
| Apache Kafka | Amazon MSK | |
| Secure Properties | AWS Secrets Manager | Primary |
| Environment Variables | SSM Parameter Store | |
| Batch Processing | AWS Batch + Step Functions | |
| Scheduler | EventBridge Scheduler | |
| SFTP / File Processing | S3 + AWS Transfer Family (SFTP) | |
| Database Connector (relational) | RDS / Aurora | Engine-specific |
| MongoDB Connector | DocumentDB or MongoDB Atlas | |
| Redis / Object Store | ElastiCache (Redis) | |
| Flow Processing Logic (stateless) | Lambda | Default compute |
| Flow Processing Logic (long-running) | ECS Fargate | For timeouts > 15 min or stateful |
| Batch / Heavy Compute | ECS Fargate or AWS Batch | |
| OAuth2 Provider | Amazon Cognito | |
| JWT Validation | API Gateway Lambda Authorizer | |
| mTLS | ACM + API Gateway / ALB | |
| Logging | CloudWatch Logs | |
| Alerting / Notifications | SNS + CloudWatch Alarms | |
| Email (SMTP) | Amazon SES | |
| Salesforce Connector | Lambda + Salesforce REST/Bulk API | EventBridge for streaming events |

### Flow Diagram Generation

For each flow, two diagrams are generated:

1. **Current State** — visual representation of the MuleSoft flow as-is
2. **Future State** — proposed AWS architecture using the component mapping

Diagrams rendered using **Mermaid** and/or **React Flow**, stored as JSON/YAML.

**Diagram editing modes:**
- **Visual editor** — drag-and-drop modifications
- **Chat update** — *"Replace SQS with Amazon MQ here"*, *"Use ECS Fargate instead of Lambda"*

---

## Tech Stack

### Summary

```text
Infrastructure:   AWS (ECS Fargate, Lambda, ALB, S3, CloudFront, RDS PostgreSQL + pgvector)
                  Terraform for all IaC
AI / Agents:      Azure OpenAI · Google ADK (Python)
Backend:          Python 3.12 · FastAPI · SSE (StreamingResponse)
                  SQLAlchemy async · asyncpg · Alembic · pgvector
                  Pydantic v2 · boto3/aioboto3 · lxml · pytest
Frontend:         React 18 · TypeScript · Vite · TanStack Query · EventSource 
                  Tailwind CSS · shadcn/ui · Lucide React · Simple Icons
                  React Flow · Mermaid.js · Shiki · React Hook Form + Zod
                  Inter (UI font) · React Router v6
```

---

### Cloud & Infrastructure

| Concern | Choice | Notes |
| --- | --- | --- |
| **Cloud host** | AWS | Primary compute and hosting platform |
| **Frontend hosting** | S3 + CloudFront | Static React build served via CDN |
| **Backend compute** | ECS Fargate (primary) + Lambda (async jobs) | |
| **Database** | RDS PostgreSQL | pgvector extension enabled for RAG |
| **Vector store** | pgvector on RDS | Co-located with application DB |
| **File storage** | S3 | Uploaded ZIPs, extracted files, IRDs, diagrams |
| **Infrastructure as Code** | Terraform | All AWS resources defined in Terraform, co-located in monorepo |
| **AI models** | Azure OpenAI + Google Cloud AI | Azure OpenAI primary; Google Cloud AI supplemental |
| **Agentic framework** | Google ADK (Agent Development Kit) | All agent orchestration in Python via Google ADK |

#### Compute Strategy

Both FastAPI services (`mitra-backend` and `mitra-agents`) run as **ECS Fargate** tasks inside the private VPC. Lambda is used exclusively for background async jobs.

**Why ECS Fargate:**
- Containers run inside the private VPC — direct private connectivity to RDS, SQS, ElastiCache without going through the public internet
- Native SSE support — no response buffering, no timeout constraints on long-running agentic flows
- The two services can call each other privately within the VPC
- Full control over scaling policies, CPU and memory allocation per service

**Network architecture:**

```text
Internet → CloudFront + WAF
               ↓
           ALB (public subnet — HTTPS 443)
           ├── /api/*    → mitra-backend ECS service  (private subnet)
           └── /agents/* → mitra-agents ECS service   (private subnet)
                               ↓
                         Private VPC Subnet
                         ├── RDS PostgreSQL
                         ├── SQS (via VPC endpoint)
                         └── S3 (via VPC gateway endpoint)
```

![MITRA AI AWS Architecture](docs/assets/mitra-ai-aws-arch.png)

**Lambda is used for:**
- Background analysis pipeline (triggered via SQS after ZIP upload)
- Batch IRD generation jobs
- Scheduled dependency graph refresh
- Any fire-and-forget async task that does not require streaming back to the client

---

### Backend

| Concern | Choice |
| --- | --- |
| **Language** | Python 3.12+ |
| **API framework** | FastAPI |
| **SSE streaming** | FastAPI `StreamingResponse` |
| **Schema validation** | Pydantic v2 + Pydantic Settings |
| **ORM** | SQLAlchemy 2.x (async) |
| **DB driver** | asyncpg |
| **DB migrations** | Alembic |
| **Vector search** | pgvector + SQLAlchemy |
| **AWS SDK** | boto3 / aioboto3 |
| **XML parsing** | `lxml` + `xmltodict` |
| **ZIP handling** | Python `zipfile` (stdlib) |
| **Testing** | pytest + pytest-asyncio |

---

### Frontend

| Concern | Choice |
| --- | --- |
| **Language** | TypeScript (strict mode) |
| **Framework** | React 18+ |
| **Build tool** | Vite |
| **Data fetching** | TanStack Query (React Query v5) |
| **SSE consumption** | Native `EventSource` API |
| **Styling** | Tailwind CSS v3 |
| **Component library** | shadcn/ui |
| **Icons** | Lucide React + react-icons (Simple Icons subset) |
| **Font** | Inter (Google Fonts) |
| **Code rendering** | Shiki |
| **Diagrams** | React Flow + Mermaid.js |
| **Form handling** | React Hook Form + Zod |
| **Routing** | React Router v6 |
| **Testing** | Vitest + React Testing Library |

---

## Monorepo Structure

All code — frontend, backend, agents, scheduled jobs, and infrastructure — lives in a single Git repository. GitLab CI path-based triggers ensure each sub-project's pipeline only runs when its own files change.

```text
mitra-analyze/                          # Git root
│
├── README.md
├── CONTRIBUTING.md
├── docker-compose.yml                  # Local dev: backend + agents + postgres
├── Makefile                            # make dev, make test, make lint, etc.
├── .env.example
├── .gitignore
├── .gitlab-ci.yml
│
├── packages/
│   └── db/                             # THE single owner of the data model
│       ├── pyproject.toml
│       ├── alembic.ini
│       ├── alembic/
│       │   └── versions/
│       └── mitra_db/
│           ├── base.py
│           ├── session.py
│           └── models/
│               ├── project.py
│               ├── application.py
│               ├── flow.py
│               ├── analysis.py
│               ├── ird.py
│               └── embedding.py        # pgvector embedding model
│
├── frontend/                           # React app → S3 + CloudFront
│   └── src/
│       ├── components/
│       │   ├── ui/                     # shadcn/ui generated components
│       │   ├── layout/
│       │   ├── projects/
│       │   ├── applications/
│       │   ├── flows/
│       │   ├── diagrams/
│       │   ├── irds/
│       │   └── chat/
│       ├── hooks/
│       └── lib/
│           ├── api.ts
│           ├── query-client.ts
│           ├── sse.ts
│           ├── auth.ts
│           └── schemas/                # Zod schemas mirroring backend Pydantic models
│
├── backend/                            # FastAPI API → ECS Fargate
│   └── app/
│       ├── routers/
│       │   ├── projects.py
│       │   ├── applications.py
│       │   ├── flows.py
│       │   ├── analysis.py
│       │   ├── irds.py
│       │   ├── diagrams.py
│       │   └── chat.py
│       ├── services/
│       │   ├── zip_extractor.py
│       │   ├── xml_parser.py
│       │   ├── dwl_analyzer.py
│       │   ├── connector_resolver.py
│       │   ├── complexity_scorer.py
│       │   ├── dependency_graph.py
│       │   ├── ird_generator.py
│       │   └── diagram_generator.py
│       └── aws/
│           ├── s3.py
│           ├── sqs.py
│           └── secrets.py
│
├── agents/                             # Google ADK agents → ECS Fargate
│   └── app/
│       ├── analyze_agent/
│       ├── ird_agent/
│       ├── diagram_agent/
│       ├── chat_agent/
│       └── shared/
│           ├── llm_client.py
│           ├── vector_store.py
│           └── context_builder.py
│
├── jobs/                               # Background jobs → Lambda (SQS-triggered)
│   ├── analysis_pipeline.py
│   ├── ird_batch.py
│   └── dependency_refresh.py
│
├── infra/                              # Terraform → all AWS infrastructure
│   ├── modules/
│   │   ├── networking/
│   │   ├── frontend/
│   │   ├── api/
│   │   ├── agents/
│   │   ├── jobs/
│   │   ├── database/
│   │   └── iam/
│   └── environments/
│       ├── dev/
│       └── prod/
│
├── docs/
└── scripts/
    ├── setup_local.sh
    ├── seed_db.py
    └── test_zip_parse.py
```

### Key Structural Decisions

**`packages/db/`** is the single owner of the data model. All SQLAlchemy ORM models and Alembic migrations live here. `backend/`, `agents/`, and `jobs/` install this as a local Python package and import from it — they never define models of their own. Alembic runs only from this package, in a dedicated CI step that runs before any service deployment.

**`agents/`** is a separate ECS Fargate service from `backend/`. Keeping it separate allows independent scaling — if analysis agent workloads spike, only the agents service scales up, and the two services communicate privately within the VPC.

**`jobs/`** are Lambda functions invoked via SQS for fire-and-forget async work. They import from `packages/db/` and `backend/services/` but never run in the FastAPI request cycle.

**`infra/`** uses an environments pattern — `dev/` and `prod/` compose the same Terraform modules with different variable values. No duplication between environments.

**GitLab CI pipeline strategy** — each sub-directory has its own `.gitlab-ci.yml` included from the root. Path-based `changes:` rules mean only the affected service's pipeline runs on each commit. Infra pipelines run `terraform plan` on merge requests and `terraform apply` on merge to `main`.

---

## Testing Strategy

All deterministic code must be unit tested. Tests run as a required CI job on every merge request — a failing test pipeline blocks the merge.

### Python — Backend, Agents, Jobs

| Tool | Purpose |
| --- | --- |
| **pytest** | Test runner and assertion framework |
| **pytest-asyncio** | Async test support for FastAPI routes and SQLAlchemy async sessions |
| **pytest-cov** | Code coverage reporting |
| **httpx** | Async HTTP client for testing FastAPI routes |
| **factory-boy** | Test data factories for SQLAlchemy models |
| **pytest-mock** | Mocking and patching |
| **freezegun** | Freeze or travel time in tests |

**What to unit test (deterministic parsing and scoring code):**

```text
services/xml_parser.py          → every element type extraction
services/dwl_analyzer.py        → complexity scoring per DWL pattern
services/connector_resolver.py  → namespace → connector name resolution
services/complexity_scorer.py   → every scoring factor in isolation
services/dependency_graph.py    → graph construction, cycle detection, missing node flagging
services/zip_extractor.py       → ZIP parsing, invalid ZIP handling, Mule 3 detection
```

**Test database pattern:** Use a real PostgreSQL instance for service-layer tests that touch the DB (run in CI via a GitLab service container). Do not mock SQLAlchemy sessions for anything above the repository layer.

### React — Frontend

| Tool | Purpose |
| --- | --- |
| **Vitest** | Fast test runner — Vite-native |
| **React Testing Library** | Component testing focused on user behaviour |
| **@testing-library/user-event** | Simulates real user interactions |
| **@testing-library/jest-dom** | Custom matchers: `toBeInTheDocument()`, `toHaveValue()`, etc. |
| **jsdom** | DOM environment for Vitest |

Tests are co-located with source files — easier to find, harder to neglect.

### GitLab CI — Test Pipeline

```yaml
stages:
  - test        # Runs on MR open, update, and push to main
  - build       # Runs on push to main only
  - migrate     # Runs on push to main only
  - deploy      # Runs on push to main only
```

Tests run automatically on every merge request. The pipeline must pass before a merge is allowed (enforced via GitLab branch protection on `main`).

---

## What MITRA Analyze Does NOT Do

- Does not generate production-ready code — that is MITRA Build's scope
- Does not deploy anything to AWS
- Does not connect live to a customer's MuleSoft runtime — everything is file-based (ZIP upload)
- Does not support Mule 3.x
- Does not provide a definitive complexity score for flows with unresolved dependencies

---

## Open Questions

1. **Application versioning** — Should re-uploading a newer ZIP version be supported with diff / comparison between versions?
2. **Clarifications & Actions** — Should every project and application have a dedicated clarifications or actions section, in addition to the per-flow Section 7 agent clarification requests?
