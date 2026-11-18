\`\`\`Glean Agents:

Glean Agents are autonomous, AI-powered workplace solutions built on the Glean Enterprise AI Platform that can reason through tasks, plan steps, and take action across your company's connected enterprise data. \[1, 2, 3\]

Key Capabilities

Universal Knowledge & Context: Connects to 275+ enterprise applications (such as Jira, Salesforce, Google Drive, Slack, and Confluence) while strictly respecting underlying user permissions. \[1, 2\]

Read & Write Actions: Goes beyond simple information retrieval by executing multi-step workflows, updating records, creating tickets, drafting messages, and triggering automated processes. \[1, 2, 3\]

Dynamic Task Delegation: Auto mode agents can split complex requests into sub-tasks and delegate them to specialized sub-agents before consolidating the final output. \[1\]

Active Governance: Continuously scans and auto-hides overshared sensitive corporate data to maintain security and compliance (including SOC 2 and ISO 42001 alignment). \[1, 2\]

How to Build Glean Agents

Glean provides two main pathways for creating and managing agents: \[1\]

Pre-Built Templates (Agent Library): Ready-to-use agents that can be discovered, launched, and managed directly from the platform. \[1\]

Custom Agents (Agent Builder): Built using natural language or a visual editor:

Auto Mode: Describe the desired outcome in plain language using the Builder Assistant, and the system generates and structures the agent for you.

Workflow Mode: Build step-by-step control manually, including custom logic, branches, loops, and tool hand-offs. \[1, 2\]

Community Best Practices

Most users on Reddit (r/AI\_Agents) agree that effective agent design relies on constraining data sources tightly, scoping agents to narrow single-workflow tasks rather than general assistants, and extensively testing through debug modes.

Glean Agents automate multi-step workflows across departments by combining company-specific context with actions in connected enterprise tools. Organizations deploy them using pre-built templates from the Glean AI Agent Library or custom builds tailored to specific teams.

Sales & Revenue Operations

Account Briefing & Snapshots. Gather recent meeting transcripts, open Salesforce opportunities, product usage notes, and support tickets to produce a one-page brief before customer calls.

Competitive Briefs. Search internal battlecards and public web data to generate factual competitor comparisons.

Deal Strategy & Call Coaching. Review opportunity history against internal sales methodologies to highlight deal gaps, analyze lost deals, and suggest next steps.

Prospect Outreach. Analyze target companies against ideal customer profiles and draft tailored outreach emails.

Customer Support & IT Operations

Ticket Next-Steps & Triage. Summarize ticket conversations, match them against internal troubleshooting docs, and draft responses for specialist approval.

Automated Ticket Deflection. Resolve routine IT issues such as password resets, software access requests, and policy questions directly inside Slack or Microsoft Teams.

Knowledge Base Generation. Identify recurring support issues and automatically draft new documentation from resolved tickets.

Incident Correlation. Connect incoming alerts with engineering runbooks and recent tickets to recommend an incident owner and draft status updates.

Engineering & Product

Pull Request Reviews. Inspect changed code files against team review checklists and highlight potential risks grouped by severity.

Spec-to-Implementation & Jira Resolution. Translate technical specifications into implementation plans, resolve Jira issues, and generate launch documentation.

CI/CD Debugging. Analyze failed build logs alongside historical Slack threads to suggest root causes and fixes.

Standup & Project Onboarding. Summarize daily engineering updates and help new developers ramp up on unfamiliar repositories.

Marketing

SEO & Content Audits. Evaluate articles against multi-point editorial checklists and analyze sales call transcripts to discover high-value blog topics and keywords.

Customer Reference Summaries. Pull quotes, case study details, and customer testimonials from internal records to support campaigns.

Event & Social Messaging. Convert internal event briefs into customer-facing descriptions, persona-based invites, and LinkedIn post drafts.

HR, Finance & Personal Productivity

Onboarding Readiness. Compare a new hire's onboarding checklist against completed tasks across HR and IT systems to flag missing assignments.

Financial Close & Reconciliation. Flag unusual transactions during monthly closes, match accounts payable records, and compile audit packets.

Intelligent Reminders & Delegation Tracking. Scan emails, calendars, call transcripts, and project trackers to summarize pending commitments and tasks assigned to teammates.

Daily & Weekly Prep. Generate morning focus briefs based on calendar schedules and compile weekly accomplishment reports grouped by project.

Configuring a custom workflow in the Glean Agent Builder follows a structured process of defining triggers, chaining actions, and testing execution. Below is a step-by-step breakdown using a Support Ticket Triage & Draft Agent as a practical example.

1\. Initialize the Agent

Open Agent Builder. Navigate to Agents in the left sidebar of Glean and click Create agent.

Select Build Mode. Choose Auto mode to describe your goal in plain language so the Builder Assistant generates the draft for you. Alternatively, select Workflow mode (Start from scratch) for strict, deterministic step-by-step control.

Configure Identity. Open the Agent Settings (gear icon) to set the agent's name, icon, description, and default LLM (such as GPT-4.1, Gemini, or Claude).

2\. Configure the Trigger

Choose Execution Type. Select how the agent starts—via a Manual Chat/Form (e.g., a user pastes a ticket URL), a Schedule (e.g., every morning at 8 AM), or a Content/Webhook Event (e.g., a new Zendesk ticket or Slack message).

Define Input Fields. Create structured variables for user inputs, such as \[\[Ticket URL\]\] or \[\[Customer Name\]\], so downstream steps can reference them.

3\. Build the Action & Reasoning Steps

In Workflow mode, you add sequential blocks on the visual canvas:

Step 1: Read & Gather Context. Add a Company Search or Read Document action. Restrict the data sources strictly to relevant repositories (e.g., Zendesk, Confluence runbooks, and engineering Slack channels) to keep answers accurate.

Step 2: Analyze & Reason. Add an LLM / Think step. Write clear markdown instructions telling the model how to compare the \[\[Ticket URL\]\] details against the retrieved Confluence troubleshooting guides.

Step 3: Branching & Logic (Optional). Insert conditional branches—for example, route urgent bugs to an engineering sub-agent while sending standard billing questions to a response drafter.

Step 4: Execute Output Action. Add a final Respond or Write action. Configure the agent to post a summary in a Slack thread, draft a reply inside the ticketing system, or generate a Google Doc.

4\. Manage Memory & Context

Optimize Token Usage. By default, each step receives output from the immediately preceding step.

Use Direct References. Set steps to "no prior outputs" and pass only the exact variables needed using double-bracket syntax (e.g., \[\[Step 1 Output\]\]) to speed up execution and avoid context clutter.

5\. Preview, Debug & Publish

Run in Preview Mode. Click Preview in the top bar and enter sample inputs without affecting live systems.

Inspect Step Execution. Review the debug trace to verify which documents the agent retrieved, check permission boundaries, and refine prompts if a step misses key details.

Publish & Share. Once verified, save and publish the agent to the company Glean Agent Library or deploy it directly to a Slack channel.

AI Enabled Finance Transformation

Lead AI-enabled finance transformation

Develop a practical roadmap for moving the finance function towards more analytical and AI-driven decision support.

Improve strategic planning and decision-making

Apply AI to budgeting, rolling forecasts, scenario analysis, profitability, working capital and liquidity forecasting to support business decisions.

Learn automating finance processes and reporting

Identify automation opportunities and build workflows for recurring finance activities using tools such as Power Automate, n8n, Power Query and Office Scripts.

Generate sharper management and board-level insights

Strengthen MIS, variance analysis, management commentary and board summaries, shifting finance from manual reporting toward actionable business insights.

Evaluate AI adoption with governance and ROI discipline

Evaluate AI investments through costing, build-vs-buy decisions and ROI-driven business cases, while addressing data privacy, security, controls and responsible AI governance.

Tomcat Application Log Analysis Agent:

Smarter Log Analysis with Apache Camel and LLMs

https://www.yenlo.com/insights/smarter-log-analysis-with-apache-camel-and-llms/

Spring AI Agent Skills

https://www.javacodegeeks.com/spring-ai-agent-skills-example.html

To build an expert AI agent for analyzing Tomcat and Spring Boot applications, combine automated log/metric ingestion, RAG (Retrieval-Augmented Generation) for configuration and source context, and tool-calling (function calling) so the agent can actively inspect running instances rather than just reading static text. \[1, 2\]

1\. Core Architecture & Stack

Choose an agent framework that integrates smoothly with the Java/JVM ecosystem or Python observability pipelines:

Agent Framework. Use Spring AI (Java) or LangChain4j if you want the agent built directly inside a Spring Boot service using @Tool annotations. Alternatively, use LangGraph or CrewAI (Python) for multi-agent orchestration. \[3, 4\]

LLM & Embeddings. Use a strong reasoning model (such as Claude 3.7/4 Sonnet or GPT-4o) for multi-hop root-cause analysis, or deploy local models via Ollama (gemma3 or llama3.3 with nomic-embed-text) if logs contain sensitive production data. \[3\]

Vector Database. Store indexed runbooks, past incident post-mortems, and application configuration files (application.yml, server.xml) in pgvector, Qdrant, or Chroma so the agent can detect configuration mismatches. \[1\]

2\. Data Ingestion & Preprocessing Pipeline

Raw JVM logs are noisy and will quickly exhaust an LLM's context window if passed directly.

Structured Log Parsing. Configure Spring Boot (Logback/Log4j2) and Tomcat (logging.properties / AccessLogValve) to output JSON-formatted logs containing timestamp, level, logger, traceId, spanId, and thread. \[5\]

Stack Trace Deduplication & Grouping. Before sending logs to the LLM, run a pre-processor (e.g., Drain3 or regex grouping) to collapse repetitive stack traces into a single unique exception template with an occurrence count.

Context Enrichment. Pair log snippets with the active application.yml, pom.xml/build.gradle, and Tomcat server.xml / context.xml so the agent can spot mismatches in HikariCP pool sizes, datasource URLs, or connector thread limits. \[1\]

3\. Essential Tools to Give Your Agent

An expert agent must be able to query live telemetry and inspect application internals. Expose the following functions as tools: \[2\]

Tool Category

Specific Tools / Endpoints to Expose

Purpose

Log & Trace Querying

search\_logs(service, level, time\_range, trace\_id)

Fetches surrounding INFO/DEBUG lines around a SEVERE or ERROR event.

Spring Boot Actuator

get\_health(), get\_metrics(metric\_name), get\_env()

Inspects live JVM heap usage, HikariCP active connections, and resolved property sources.

Tomcat JMX / MBeans

get\_tomcat\_thread\_pool(), get\_servlet\_stats()

Checks Catalina:type=ThreadPool (currentThreadsBusy, maxThreads) and request processing times.

JVM Diagnostics

analyze\_thread\_dump(), check\_gc\_logs()

Identifies thread deadlocks, BLOCKED threads, and long Stop-The-World garbage collection pauses.

Code & Config Lookup

read\_source\_file(class\_name, line\_number)

Maps stack trace line numbers directly to your Git repository to inspect the exact failing method.

4\. Designing Expert System Prompts & Workflows

Structure your agent using a multi-step diagnostic workflow rather than a single prompt: \[6\]

Triage & Categorization. Classify the issue into specific domains (e.g., Startup/BeanCreationException, Database/Connection Pool Exhaustion, Tomcat Thread Starvation, OutOfMemoryError).

Hypothesis & Tool Execution. Instruct the agent to verify hypotheses with tools. For example, if it sees Connection is not available, request timed out after 30000ms, it should automatically call get\_metrics("hikaricp.connections.active") and inspect application.yml for maximum-pool-size. \[1\]

Structured Root-Cause Output. Force the agent to return a consistent report containing:

Root Cause Summary (citing specific exception classes and line numbers).

Evidence (log timestamps, metric anomalies, or config mismatches).

Remediation (exact YAML/XML configuration patches or Java code fixes). \[1\]

5\. Step-by-Step Implementation Plan

Build a Minimal Prototype. Start by creating a Spring Boot service using Spring AI (ChatClient) and define 2–3 @Tool methods that read local catalina.out and application.yml files.

Test with Synthetic Failures. Generate test scenarios with intentional flaws—such as mismatched database credentials, circular bean dependencies, or exhausted Tomcat maxThreads—to verify the agent accurately diagnoses each failure.

Connect Live Observability. Replace local file readers with API clients for Loki / Elasticsearch (logs), Prometheus / Micrometer (metrics), and OpenTelemetry / Jaeger (distributed traces).

Add Guardrails. Restrict Actuator and JMX tools to read-only operations and scrub secrets (passwords, JWTs, API keys) in your log ingestion pipeline before data reaches the LLM. \[1, 4, 7, 8\]

To help you tailor the implementation, could you share:

Your preferred tech stack (e.g., Java with Spring AI/LangChain4j or Python)?

Your deployment environment (standalone Tomcat vs. embedded Tomcat in Spring Boot, Kubernetes, or VMs)?

Where your logs and metrics currently live (local files, ELK stack, Grafana Loki, Datadog)?

I can provide starter code and tool definitions matched to your exact setup.

\[1\] https://medium.com

\[2\] https://www.youtube.com

\[3\] https://www.yenlo.com

\[4\] https://www.youtube.com

\[5\] https://www.openlogic.com

\[6\] https://spring.io

\[7\] https://camel.apache.org

\[8\] https://www.youtube.com

Building AI Powered Log Analysis Agent

Building an AI‑Powered Log Analysis Agent for Spring Boot Applications

https://medium.com/@infranotes/building-an-ai-powered-log-analysis-agent-for-spring-boot-applications-e66d8879805f

Proactive Alerting, Human In the Loop and Safe Remediation

To add proactive alerting, Human-in-the-Loop (HITL) approvals, and safe remediation to your Spring Boot and React AI agent, design an event-driven pipeline where deterministic rules trigger the AI, and stateful approval gates block destructive actions until an engineer approves them.

1\. Proactive Alerting Architecture

Do not let an LLM continuously poll your system—that is expensive and slow. Instead, use lightweight, deterministic checks to wake the agent up only when something breaks.

Threshold & Webhook Triggers. Configure Prometheus Alertmanager, Grafana, or a lightweight Spring @Scheduled check (querying Micrometer metrics every 60 seconds) to fire a webhook to /api/agent/investigate when HTTP 5xx rates, latency, or React error counts spike.

Alert Deduplication & Cooldowns. Store active incidents in a database (like PostgreSQL or Redis) with an incident\_fingerprint (e.g., hashed stack trace or alert name). Suppress duplicate LLM runs for the same issue for 15–30 minutes to prevent alert fatigue and token burn.

Autonomous Investigation Loop. Once triggered, the Spring AI agent runs asynchronously (@Async), calls its read-only @Tool methods (logs, metrics, recent git commits), and writes a structured Incident Report containing the root cause, severity, and a proposed fix.

2\. Human-in-the-Loop (HITL) Approval Workflow

Never let an AI execute state-changing infrastructure or application actions automatically in production. Put an explicit state machine between the AI's recommendation and its execution.

Separate Read Tools from Write Tools. Give the investigation agent only read-only @Tool beans. Define remediation actions as structured JSON proposals rather than direct tool calls during diagnosis.

Persist Action Proposals. Save the agent's proposed remediation in a remediation\_actions table with a status lifecycle: PENDING\_APPROVAL → APPROVED / REJECTED → EXECUTING → COMPLETED / FAILED.

Push Notifications to Engineers. When a PENDING\_APPROVAL action is created, push it immediately to your React dashboard via WebSockets / SSE and send an interactive card to Slack or Microsoft Teams with Approve and Reject buttons.

Audit Logging. Record which engineer approved the action, the timestamp, the exact parameters executed, and the post-action system state for compliance and post-mortems.

3\. Designing Safe Remediation Actions

Start with low-risk, reversible actions that have strict guardrails built into your Spring Boot code.

Remediation Action

Risk Level

Guardrails & Implementation

Clear Application Cache

Low

Expose a Spring service that evicts specific @Cacheable regions (e.g., Redis keys) rather than flushing the entire cache.

Toggle Feature Flag

Low

Integrate with LaunchDarkly, Unleash, or a DB-backed feature flag table to disable a buggy React feature or heavy API endpoint.

Scale Up / Restart Pod

Medium

Call the Kubernetes Java Client or cloud SDK, capped by hard limits (e.g., max 5 replicas, max 1 restart per hour).

Rollback Deployment

Medium

Trigger a CI/CD webhook (GitHub Actions / Jenkins) to revert to the previous known-good Docker image tag.

Database Query Kill

High

Terminate long-running queries (pg\_terminate\_backend) only for non-admin user connections exceeding a strict timeout.

4\. React Dashboard UX for HITL

Your React monitoring console should make reviewing and acting on AI advice fast and unambiguous.

Incident Triage View. Show the AI's confidence score, plain-English root cause, and expandable evidence snippets (the exact stack trace or metric spike the agent found).

Action Confirmation Modal. When an engineer clicks Approve Fix, show a confirmation dialog displaying the exact command or API call that will run, its expected impact, and a rollback plan.

Post-Action Verification. After execution, have the agent automatically re-check metrics after 2–3 minutes and display a "Verified Resolved" or "Issue Persists" badge on the React card.

Would you like to see code examples for implementing this workflow? Let me know if you want:

The Spring Boot state machine & entity design for PENDING\_APPROVAL actions

A React HITL approval card component with real-time status updates

Specific remediation integrations (such as Kubernetes, Docker, Redis, or Slack webhooks)

MQ, Oracle DB, Google Cloud Storage (GCS), Networks, Disk Space

To monitor MQ, Oracle DB, Google Cloud Storage (GCS), Networks, Disk Space, and other infrastructure layers alongside your Spring Boot and React app, adopt a Hub-and-Spoke (Multi-Agent or Modular Toolset) Architecture.

Instead of forcing one massive prompt to know everything, build specialized Diagnostic Agents (or Tool Domains) managed by a central Supervisor Agent in Spring AI.

1\. The Hub-and-Spoke Agent Pattern

When an alert fires (e.g., "Spring Boot checkout API is timing out"), the Supervisor Agent routes the investigation to relevant specialist sub-agents or domain toolkits in parallel.

Supervisor Agent (Orchestrator). Receives the initial alert, correlates symptoms across layers, and delegates checks to specific domain tools.

Domain Toolkits / Sub-Agents. Each infrastructure component gets its own isolated Spring @Service with read-only @Tool methods, strict timeouts, and least-privilege credentials.

Cross-Layer Correlation. The Supervisor combines findings (e.g., Spring Boot thread pool exhausted + Oracle DB row lock + MQ consumer lag) to find the true root cause instead of treating symptoms.

2\. Domain-Specific Monitoring & Remediation Blueprint

Infrastructure Layer

What to Monitor (Read @Tools)

How to Connect from Spring Boot

Safe HITL Remediation Actions

Message Queues (IBM MQ / RabbitMQ / Kafka)

Queue depth, consumer count, dead-letter queue (DLQ) spikes, message age.

IBM MQ Java/JMS PCF commands, RabbitMQ Management REST API, or Kafka AdminClient.

Restart stalled Spring @JmsListener / @KafkaListener containers; replay DLQ messages in batches.

Oracle Database

Active sessions, blocking locks (V$LOCK), tablespace usage, slow SQL (V$SQL), HikariCP pool exhaustion.

Dedicated read-only JdbcTemplate querying V$ dynamic performance views (with strict 3s query timeout).

Kill specific blocking session (ALTER SYSTEM KILL SESSION with safety filters); flush shared pool or resize HikariCP pool.

Google Cloud Storage (GCS)

Bucket availability, 4xx/5xx API error rates, upload/download latency, quota limits.

Google Cloud Java SDK (Storage client) & Cloud Monitoring API (MetricServiceClient).

Switch Spring Boot storage bean to a fallback bucket/region; pause non-critical batch export jobs.

Networks & Connectivity

DNS resolution, TLS certificate expiry, downstream API latency, TCP connection timeouts, firewall drops.

Java InetAddress / SSLSocket, Micrometer HTTP client metrics, or Prometheus Blackbox Exporter API.

Trip a Resilience4j Circuit Breaker manually; switch traffic routing to a secondary endpoint.

Disk Space & Host OS

Filesystem usage (/ and /var/log), inode exhaustion, I/O wait, JVM heap vs. container memory limits.

Prometheus Node Exporter API, GCP Compute/GKE APIs, or Java FileStore checks on local nodes.

Trigger log rotation/compression; purge old /tmp artifacts; expand persistent volume claim (PVC) in Kubernetes.

3\. Handling Access, Security & Scale

Connecting an AI agent to Oracle DB, MQ, and GCP requires strict guardrails so the agent cannot accidentally take down critical enterprise infrastructure.

Dedicated Read-Only Service Accounts. Create an Oracle user with only SELECT\_CATALOG\_ROLE (no INSERT/UPDATE/DELETE), a GCP IAM role with roles/monitoring.viewer and roles/storage.objectViewer, and an MQ user with INQUIRE permissions only.

Leverage Existing Exporters First. If you already run Prometheus (with oracledb\_exporter, node\_exporter, mq\_exporter, and GCP Stackdriver exporter), have your Spring AI @Tool methods query PromQL via HTTP rather than opening direct connections to every database and server from the agent.

Context Window Management. Raw Oracle AWR reports or thousands of MQ messages will overflow an LLM's context window. Always summarize, filter, and cap tool outputs in Java (e.g., "Return only top 5 blocking Oracle sessions" or "Return top 10 deepest queues") before passing data back to the LLM.

4\. Example Investigation Flow Across Layers

Trigger: React users report 504 Gateway Timeout on file uploads; Prometheus fires an alert for high Spring Boot latency.

Supervisor Agent: Dispatches parallel checks to the GCS Tool, Oracle DB Tool, and Disk/Network Tools.

Findings:

GCS latency is normal.

Local container disk /tmp is at 99% capacity (Spring Boot multipart file staging is failing).

Oracle DB shows idle connections waiting on app threads.

HITL Proposal: The agent surfaces an incident card in React: "Root Cause: /tmp disk full on pod app-7f8b blocking multipart uploads. Proposed Action: Purge stale temp files older than 1 hour and restart pod."

To tailor the integration code to your environment, let me know:

Which observability stack you already have in place (e.g., Prometheus/Grafana, Datadog, Dynatrace, GCP Cloud Monitoring, or raw logs/JDBC)

Where your Spring Boot app runs (GKE/Kubernetes, Cloud Run, or on-prem VMs)

Which integration (Oracle DB, MQ, GCS, or OS/Network) you want to build first

\`\`\`