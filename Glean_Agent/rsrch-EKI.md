# Enterprise Knowledge Integration for AI-Powered Software Modernization

**Research Document**

**Research focus:** Enterprise Knowledge Systems, Retrieval-Augmented Generation (RAG), Glean, and AI Agent Integration  
**Application context:** Google ADK-based Software Modernization Agent  
**Purpose:** Understand the concepts, evaluate integration possibilities, and identify a practical proof-of-concept approach.

---

## 1. Executive Summary

Modern software modernization is not simply the process of identifying outdated technologies and replacing them with newer versions. Enterprise modernization requires technical analysis as well as an understanding of organizational standards, business requirements, security policies, architectural decisions, and historical project knowledge.

An AI-powered Modernization Agent can inspect source code, identify vulnerabilities, analyze dependencies, detect outdated frameworks, and recommend improvements. However, its recommendations may be incomplete if it does not have access to the organization's internal engineering knowledge.

For example, an agent may identify that an application uses Java 8 and recommend upgrading to a newer Java version. However, the organization may have a specific approved Java version, framework compatibility requirement, migration procedure, or security policy.

This creates an opportunity for **Enterprise Knowledge Integration**.

Enterprise knowledge integration enables AI agents to retrieve relevant information from organizational systems and use it as additional context when analyzing software applications and generating recommendations.

Platforms such as Glean provide enterprise search, knowledge retrieval, connectors, APIs, and agent capabilities that can help make this information accessible to AI applications.

The proposed approach is to explore Glean as an enterprise knowledge layer that complements the existing Modernization Agent rather than replacing its code-analysis and orchestration capabilities.

**Central research proposition:**

> Integrating enterprise knowledge retrieval with AI-powered software modernization can help generate recommendations that are not only technically relevant but also aligned with organizational standards, policies, and engineering decisions.

---

## 2. Introduction: Why Enterprise Knowledge Matters

### 2.1 The modernization challenge

Organizations frequently maintain software systems developed over several years or decades. These applications may contain:

- Legacy programming languages and frameworks.
- Outdated dependencies and libraries.
- Security vulnerabilities.
- Complex application architectures.
- Inconsistent coding standards.
- Limited technical documentation.
- Dependencies on internal infrastructure.
- Historical design decisions that are not obvious from source code.

Modernization teams must understand both the application and the environment in which it operates.

Consider a legacy application using Java 8, an older Spring framework, and several outdated libraries.

A conventional modernization assessment might identify:

1. The Java version is outdated.
2. Some dependencies have known vulnerabilities.
3. Certain libraries are no longer maintained.
4. The application architecture could benefit from modernization.

But these findings do not answer every important question:

- Which Java versions are approved by the organization?
- Which framework versions are supported internally?
- Are there restrictions on cloud deployment?
- Does the company have an approved migration pattern?
- Has another team already modernized a similar application?
- Are there security requirements that affect the migration?

These answers may exist in internal documents, architecture decision records, engineering repositories, project reports, and knowledge-sharing conversations.

This information represents **enterprise knowledge**.

### 2.2 What is enterprise knowledge?

Enterprise knowledge refers to the information, expertise, decisions, and practices accumulated within an organization.

It can include:

| Knowledge category | Examples |
|---|---|
| Technical standards | Approved Java, Python, and framework versions |
| Architecture knowledge | Microservices guidelines, API standards, design patterns |
| Security knowledge | Secure coding policies, authentication standards, vulnerability guidelines |
| Engineering knowledge | Coding conventions, testing practices, deployment procedures |
| Project knowledge | Previous modernization reports, migration experiences |
| Operational knowledge | Infrastructure requirements, monitoring and support procedures |
| Business knowledge | Application priorities, business constraints, compliance requirements |

The challenge is that this knowledge is often distributed across different systems.

Enterprise knowledge integration attempts to make relevant information discoverable and usable by AI applications.

---

## 3. Understanding the Fundamental Technologies

Before exploring Glean and its APIs, it is important to understand the underlying concepts.

### 3.1 Large Language Models (LLMs)

A Large Language Model is an AI model trained on large amounts of text and other data to understand and generate human language.

Examples include GPT, Gemini, and Claude.

In a modernization system, an LLM can:

- Explain source code.
- Identify possible architectural problems.
- Summarize technical findings.
- Suggest migration strategies.
- Generate code transformation recommendations.

However, an LLM does not automatically know an organization's latest internal policies, approved technologies, or private engineering documentation.

This creates a knowledge gap between general model knowledge and organization-specific knowledge.

### 3.2 Enterprise Search

Enterprise Search is the process of searching information across an organization's internal applications and repositories.

Unlike public internet search, enterprise search focuses on internal organizational information.

Possible data sources include:

- SharePoint and Google Drive.
- Confluence.
- Jira.
- Slack and Microsoft Teams.
- GitHub and other source-code platforms.
- Internal documentation repositories.

For example, an engineer could search:

"Find the approved Java modernization guidelines and previous Java migration reports."

An enterprise search platform attempts to retrieve relevant information from connected organizational sources.

**Why it matters:** Instead of manually searching multiple applications, an AI agent can retrieve relevant internal information through a common search interface.

### 3.3 Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation is an approach that combines information retrieval with language generation.

A conventional LLM generates an answer using its learned model knowledge and the context provided in the prompt.

A RAG-based system retrieves relevant external information and supplies it to the LLM before generating an answer.

**Basic RAG workflow:**

1. A user or AI agent submits a question.
2. The retrieval system searches an available knowledge collection.
3. Relevant documents or passages are retrieved.
4. The retrieved information is added to the LLM's context.
5. The LLM generates an answer based on the question and retrieved information.
6. The system can provide references to the source material.

**Example:**

Question: "What is the approved approach for migrating our Java 8 applications?"

The retrieval system searches internal modernization standards and previous migration documents.

It retrieves relevant information, such as the approved Java version, migration sequence, compatibility requirements, and testing guidelines.

The LLM uses this information to generate a context-grounded recommendation.

**Important distinction:** RAG does not retrain the LLM. It supplies relevant information at inference time.

### 3.4 Embeddings and Vector Databases

Many custom RAG systems use embeddings and vector databases.

An embedding is a numerical representation of text that captures aspects of its semantic meaning.

For example, these two phrases have different wording but similar meaning:

- "Upgrade an outdated Java application."
- "Modernize a legacy Java codebase."

An embedding model can represent these phrases as vectors that may be close in a semantic vector space.

A vector database stores and searches these numerical representations.

Examples include:

- FAISS.
- Chroma.
- Pinecone.
- Qdrant.
- PostgreSQL with pgvector.

A typical custom RAG ingestion process is:

1. Collect documents.
2. Extract text and metadata.
3. Split documents into manageable chunks.
4. Generate embeddings.
5. Store embeddings and metadata.
6. Retrieve relevant chunks when a query arrives.
7. Pass retrieved context to the LLM.

This is one possible way to build RAG. It is not the only way.

A managed enterprise knowledge platform may provide its own indexing, retrieval, permission handling, and knowledge infrastructure. Therefore, an organization evaluating Glean should assess whether it can use the platform's existing capabilities instead of building and maintaining a separate retrieval infrastructure.

### 3.5 AI Agents and Agent Orchestration

An AI agent is a system that uses an LLM, instructions, tools, and sometimes memory to perform a task.

A modernization workflow may use multiple specialized agents:

- Assessment Agent.
- Security Agent.
- Dependency Analysis Agent.
- Architecture Agent.
- Code Transformation Agent.
- Validation Agent.

An orchestration framework coordinates their execution and information exchange.

Google Agent Development Kit (ADK) is one such framework.

An important distinction is:

- **Agent orchestration** determines which agent performs a task and how information moves between agents.
- **Knowledge retrieval** provides relevant information that an agent can use while performing that task.

They solve different problems and can work together.

---

## 4. Enterprise Knowledge Integration Architecture

Enterprise knowledge integration connects internal organizational information with AI applications.

At a high level, the architecture contains five major components.

### 4.1 Enterprise Data Sources

These are the systems where organizational knowledge exists.

Examples:

- Documentation platforms.
- Project management tools.
- Communication platforms.
- Source-code repositories.
- Internal knowledge bases.
- Engineering standards and reports.

### 4.2 Connectors and Data Integration

Connectors establish communication between the knowledge platform and the original data sources.

Depending on the connector, they may:

- Retrieve documents and messages.
- Extract relevant content and metadata.
- Collect access permissions.
- Synchronize changes.
- Make indexed information searchable.

### 4.3 Enterprise Knowledge Layer

This layer organizes information from multiple sources and makes it accessible through search and retrieval capabilities.

In Glean's architecture, the Knowledge Graph connects content, people, and activity information.

This can help provide contextual and personalized search results.

### 4.4 Retrieval and AI Services

The retrieval layer finds information relevant to a user query or agent task.

The AI layer uses the retrieved information to generate responses, summaries, or recommendations.

### 4.5 AI Applications and Agents

The final layer contains applications that consume enterprise knowledge.

Examples:

- Enterprise Knowledge Assistants.
- IT Support Agents.
- Software Development Agents.
- Code Review Agents.
- Modernization Agents.

### Architecture overview

```text
        ENTERPRISE DATA SOURCES
  ┌─────────┬─────────┬──────────┬─────────┐
  │ GitHub  │ Conflu. │  Jira    │ SharePt │
  └────┬────┴────┬────┴────┬─────┴────┬────┘
       │         │         │          │
       └─────────┴─────────┴──────────┘
                      │
                      ▼
          CONNECTORS / DATA INGESTION
                      │
                      ▼
          ENTERPRISE KNOWLEDGE LAYER
       Content + People + Permissions
                      │
                      ▼
            SEARCH / RETRIEVAL APIs
                      │
                      ▼
             AI AGENT APPLICATION
                      │
            ┌─────────┴──────────┐
            ▼                    ▼
       LLM Reasoning        Agent Tools
            │                    │
            └─────────┬──────────┘
                      ▼
           CONTEXT-GROUNDED OUTPUT
```

The architecture separates organizational knowledge from the business logic of individual AI applications.

This separation allows multiple agents and applications to reuse the same knowledge infrastructure.

---

## 5. Glean as an Enterprise Knowledge Platform

### 5.1 What is Glean?

Glean is an enterprise AI and knowledge platform designed to connect organizational information across multiple applications and make it accessible through search, chat, and AI agents.

Its developer platform provides APIs and tools for building applications that use enterprise knowledge.

Rather than treating every internal application as an isolated information source, Glean aims to provide a unified way to search and interact with connected enterprise information.

### 5.2 Major capabilities

#### A. Enterprise Connectors

Connectors link Glean with applications where organizational information exists.

Examples include documentation systems, communication platforms, project management tools, and development platforms.

Their responsibilities can include:

- Retrieving content.
- Extracting metadata.
- Synchronizing information.
- Mirroring source permissions.
- Keeping indexed content updated.

A particularly important capability is permission-aware retrieval.

A user should not receive information from a connected application if that user does not have permission to access the original content.

#### B. Knowledge Graph

Glean's Knowledge Graph organizes enterprise information around three major elements:

1. **Content:** Documents, messages, tickets, and other information.
2. **People:** Employees, identities, roles, and organizational relationships.
3. **Activity:** Interactions and engagement signals associated with enterprise information.

This creates relationships between organizational content and the people and activities associated with it.

For example, when investigating a modernization decision, an agent may need to find the relevant architecture document, understand its ownership, and identify related engineering discussions.

The Knowledge Graph can help make this type of enterprise context discoverable.

#### C. Search API

The Search API allows applications and agents to retrieve relevant information from connected enterprise sources.

Possible modernization use cases:

- Search for approved technology standards.
- Find previous migration reports.
- Retrieve security guidelines.
- Locate architecture decisions.
- Find internal documentation related to a dependency.

#### D. Chat API

The Chat API enables developers to create conversational experiences grounded in enterprise knowledge.

Instead of sending a question directly to a general-purpose LLM, an application can use Glean's enterprise knowledge capabilities to generate a response with relevant context and source citations.

For modernization, this could support questions such as:

"What internal guidelines should we follow when upgrading this application's Java version?"

#### E. Agents API

The Agents API provides programmatic access to Glean agents.

The documented capabilities include:

- Discovering available agents.
- Inspecting agent input and output schemas.
- Creating agent runs.
- Checking execution status.
- Handling approval requests where supported.

This makes it possible to explore interactions between Glean agents and other applications.

#### F. MCP Integration

Model Context Protocol (MCP) provides a standardized way for AI applications to interact with external tools and context providers.

Glean provides a Remote MCP Server that can expose its knowledge and enabled tools to supported MCP hosts.

This creates another potential integration path for AI development environments and agent applications.

**Important:** API, MCP, agent, and connector capabilities depend on the organization's Glean deployment, enabled features, permissions, and configuration.

---

## 6. How Enterprise Knowledge Can Enhance a Modernization Agent

### 6.1 Existing Modernization Agent capabilities

The current Modernization Agent is built around a multi-agent architecture using Google ADK.

Its existing workflow includes:

- Repository and source-code assessment.
- Deterministic pre-scan using eight detectors.
- Assessment and specialized analysis agents.
- Context forwarding through finding identifiers and finding details.
- DAG-based task mapping.
- Anti-loop handling.
- Validation stages.

The system focuses on understanding the technical condition of an application and supporting modernization activities.

However, it currently does not have its own RAG or vector knowledge retrieval pipeline.

Specifically, it does not currently contain:

- An embedding generation pipeline.
- A vector database.
- A document chunking and indexing pipeline.
- A dedicated enterprise document retrieval service.

This does not mean the existing system cannot use knowledge. It means there is an opportunity to explore a dedicated enterprise knowledge integration capability.

### 6.2 The knowledge gap

Consider an application that contains:

- Java 8.
- An older Spring framework.
- Outdated dependencies.
- Several security findings.

The existing Modernization Agent may identify these technical issues and recommend possible improvements.

However, the recommendations could be more useful if the agent also knew:

- Which Java versions are approved internally.
- Which Spring versions are compatible with the organization's infrastructure.
- Which security standards must be followed.
- Which migration approach was successful in previous projects.
- Which architecture patterns are preferred.

These details are organizational knowledge, not necessarily discoverable from source code.

### 6.3 Proposed integration

The proposed approach is to use Glean as an external enterprise knowledge layer.

The Modernization Agent continues to analyze source code and coordinate its existing agents.

Glean provides relevant enterprise information when an agent needs organizational context.

```text
                  USER
                   │
                   ▼
         MODERNIZATION WORKFLOW
                   │
                   ▼
          REPOSITORY ASSESSMENT
                   │
                   ▼
          DETERMINISTIC PRE-SCAN
                   │
                   ▼
          TECHNICAL FINDINGS
                   │
                   ▼
       GOOGLE ADK SPECIALIZED AGENTS
                   │
           Need enterprise context?
                   │
                   ▼
          GLEAN RETRIEVAL SERVICE
                   │
                   ▼
       ENTERPRISE KNOWLEDGE SOURCES
                   │
                   ▼
       RETRIEVED CONTEXT + REFERENCES
                   │
                   ▼
        MODERNIZATION AGENT REASONING
                   │
                   ▼
       CONTEXT-AWARE RECOMMENDATIONS
                   │
                   ▼
            VALIDATION STAGE
                   │
                   ▼
          MODERNIZATION REPORT
```

This is a proposed architecture, not a description of an implemented integration.

### 6.4 Example: Java modernization

**Scenario:** The assessment identifies an application using Java 8 and an outdated Spring dependency.

**Without enterprise knowledge integration:**

1. The assessment agent identifies the outdated Java version.
2. The dependency agent identifies outdated libraries.
3. The architecture agent proposes a modernization strategy.
4. The LLM generates recommendations using the repository findings and available model knowledge.

Potential limitation: The recommendation may not reflect internal technology standards.

**With enterprise knowledge integration:**

1. The assessment agent identifies the outdated Java version.
2. The dependency agent identifies affected dependencies.
3. The knowledge retrieval service searches for the approved Java migration standard.
4. Glean retrieves relevant internal documents and their references, subject to permissions.
5. The assessment and architecture agents receive the relevant enterprise context.
6. They combine repository findings with organizational standards.
7. The validation stage checks whether the proposed recommendations are technically consistent.

**Illustrative output:**

| Technical finding | Enterprise context | Possible recommendation |
|---|---|---|
| Application uses Java 8 | Internal standard specifies an approved target Java version | Plan an upgrade to the approved version |
| Outdated Spring dependency | Internal framework compatibility guidelines | Select a compatible approved framework version |
| Missing security configuration | Internal security policy | Apply the required security controls |
| No documented migration strategy | Previous migration reports available | Reuse relevant migration practices |

The target version and policies must come from actual organizational sources. They should never be invented by the agent.

---

## 7. Integration Approaches: Glean and Google ADK

There are multiple possible ways to connect enterprise knowledge with an existing agent architecture.

### Approach 1: Search API Integration

The Modernization Agent invokes Glean's Search API when it needs organizational information.

**Workflow:**

1. An agent identifies a knowledge requirement.
2. It constructs a focused search query.
3. The integration service calls Glean.
4. Glean returns relevant permission-visible results.
5. The service formats the results.
6. The agent uses the retrieved information in its reasoning.

**Advantages:**

- Direct retrieval control.
- Flexible integration with existing ADK agents.
- Allows selected agents to access enterprise knowledge.
- Makes it possible to preserve the existing orchestration design.

**Best suited for:** Targeted retrieval of internal engineering standards and documentation.

### Approach 2: Chat API Integration

The application sends a question to Glean's Chat API to generate an answer grounded in enterprise knowledge.

**Workflow:**

1. The modernization agent identifies a question.
2. It sends the question and required context to the integration service.
3. The service calls Glean Chat.
4. Glean generates an answer using available enterprise context.
5. The answer and source references are returned.
6. The modernization agent evaluates the result before using it.

**Advantages:**

- Provides an answer-oriented interface.
- Can reduce the need to implement a separate answer-generation layer for this particular knowledge task.
- Can provide references for further inspection.

**Best suited for:** Questions requiring synthesis across multiple enterprise documents.

### Approach 3: Glean Agent Integration

The Modernization Agent may interact with a Glean agent through the Agents API, where the required capabilities and permissions are available.

This is useful when a reusable Glean agent already performs a specific enterprise task.

For example, a Glean agent could retrieve and summarize approved architecture documentation.

The Modernization Agent could then use that output as additional context.

**Best suited for:** Reusing existing enterprise agents rather than implementing every knowledge workflow independently.

### Approach 4: MCP Integration

An MCP-compatible application can connect to Glean's Remote MCP Server and use the tools exposed by the configured tenant.

This provides another option for connecting enterprise knowledge to AI applications.

**Best suited for:** Exploring standardized tool access across supported AI clients and agent environments.

### Recommended starting point

For the existing Google ADK-based Modernization Agent, a controlled Search API integration is a reasonable first experiment.

It offers direct control over:

- Which agents can retrieve information.
- When retrieval occurs.
- What query is sent.
- Which retrieved references are passed downstream.
- How the retrieved information affects recommendations.

The Chat API can be evaluated as a second option when answer synthesis is more useful than returning search results.

MCP and Glean Agents API can be explored as additional integration patterns rather than introducing all approaches into the first POC.

---

## 8. Proposed Proof of Concept (POC)

A small POC can help establish whether enterprise knowledge integration provides measurable value.

### 8.1 Objective

Evaluate whether adding enterprise knowledge retrieval improves the accuracy, relevance, and organizational alignment of modernization recommendations.

### 8.2 POC scope

Start with:

- One Java application repository.
- One existing Modernization Agent workflow.
- Three sample enterprise documents.
- One Glean retrieval integration.
- One or two selected ADK agents.

Sample enterprise documents:

1. Java modernization standards.
2. Approved technology stack guidelines.
3. Enterprise security guidelines.

These can be controlled sample documents if an actual Glean tenant is not available. A mock retrieval service can be used to validate the ADK integration design, but it must not be presented as a real Glean integration.

### 8.3 Proposed execution flow

**Step 1: Baseline assessment**

Run the existing Modernization Agent against the sample repository.

Record its findings and recommendations.

**Step 2: Identify knowledge requirements**

Determine which findings require additional organizational context.

For example:

- Framework compatibility.
- Approved Java versions.
- Security requirements.

**Step 3: Retrieve enterprise information**

Use Glean Search API, if an authorized tenant and API access are available.

Retrieve the relevant internal standards and documentation.

**Step 4: Pass context to selected agents**

Initially, consider:

- Assessment Agent.
- Architecture Agent.
- Dependency Analysis Agent.
- Security Agent.

Avoid introducing retrieval into all 22 agents during the first experiment.

**Step 5: Generate recommendations**

Allow the selected agents to combine technical findings with retrieved enterprise information.

**Step 6: Validate the output**

Compare the recommendations against the baseline assessment and the source documents.

### 8.4 Evaluation criteria

| Evaluation area | What to measure |
|---|---|
| Retrieval relevance | Does the retrieved document actually answer the knowledge requirement? |
| Recommendation accuracy | Are recommendations technically correct? |
| Policy alignment | Do recommendations follow the organization's approved standards? |
| Source traceability | Can the agent identify the documents supporting its recommendations? |
| Security | Does retrieval respect the user's access permissions? |
| Latency | How much time does retrieval add to the workflow? |
| Reliability | How does the agent behave when no relevant information is found? |
| Cost | What are the platform, API, and operational costs? |

### 8.5 Success criteria

The POC should demonstrate:

- Relevant enterprise documents are retrieved for selected findings.
- Recommendations accurately reflect retrieved organizational standards.
- Source references are retained.
- Existing modernization analysis remains functional.
- Unauthorized information is not exposed.
- Retrieval failures do not silently produce unsupported recommendations.

The team should define quantitative thresholds before testing rather than assuming the POC is successful simply because an API call works.

---

## 9. Security, Governance, and Reliability Considerations

Enterprise knowledge integration introduces important security and governance requirements.

### 9.1 Permission-aware retrieval

An employee may have access to a particular architecture document while another employee does not.

The AI application must not bypass these permissions.

Glean documents permission-aware search and connector-based permission synchronization. However, the exact behavior depends on the connector, configuration, authentication method, and access mode.

The integration must ensure that the identity used for retrieval reflects the intended user's authorization.

A broad service account should not automatically be assumed to provide safe per-user access.

### 9.2 Data privacy

Before connecting enterprise sources, organizations should evaluate:

- Which data sources can be indexed.
- Whether sensitive documents should be excluded.
- How data is encrypted.
- Data retention and deletion policies.
- Tenant isolation.
- API authentication.
- Auditability and administrative controls.

### 9.3 Source traceability

Every important recommendation should ideally include:

- The technical finding.
- The retrieved enterprise document.
- The relevant source passage or reference.
- The reasoning connecting the finding to the recommendation.

This makes the output easier to review and verify.

### 9.4 Hallucination control

Retrieval does not guarantee correctness.

An agent may still:

- Retrieve an irrelevant document.
- Misinterpret a policy.
- Combine conflicting guidelines.
- Generate a recommendation that is unsupported by its sources.

Recommended controls:

1. Require evidence for organization-specific claims.
2. Preserve source references.
3. Distinguish confirmed policy from general suggestions.
4. Flag conflicting or outdated documents.
5. Ask for human review when critical information is missing.
6. Never invent an approved technology version or organizational rule.

### 9.5 Retrieval failure handling

The system should define what happens when:

- Glean is unavailable.
- API authentication fails.
- No relevant documents are found.
- The user lacks permission.
- Retrieved sources conflict.

A sensible approach is to continue the existing technical assessment where possible, clearly label recommendations that lack enterprise context, and avoid claiming that they comply with internal standards.

---

## 10. Build vs. Buy: Glean vs. Custom RAG

An important architectural decision is whether to use an enterprise knowledge platform or build a custom retrieval system.

| Evaluation area | Glean-based approach | Custom RAG approach |
|---|---|---|
| Data integration | Uses supported connectors and indexing capabilities | Team develops ingestion integrations |
| Retrieval | Uses platform search and retrieval | Team selects and implements retrieval methods |
| Embeddings and indexing | Platform-managed capabilities, subject to configuration | Team manages embedding and indexing pipeline |
| Permissions | Connector-based permission handling and platform controls | Team implements and maintains authorization logic |
| Customization | Depends on exposed APIs and platform capabilities | Greater control over retrieval and processing |
| Infrastructure | Depends on subscription and deployment model | Team operates selected infrastructure |
| Maintenance | Shared with platform provider and internal administrators | Primarily the engineering team's responsibility |
| Cost | Licensing, usage, and integration costs | Infrastructure, development, operations, and maintenance costs |

### 10.1 When Glean may be appropriate

Glean may be a strong candidate when an organization:

- Uses many enterprise applications.
- Needs unified enterprise search.
- Requires permission-aware knowledge access.
- Wants to avoid maintaining multiple custom ingestion pipelines.
- Wants to provide reusable knowledge capabilities to multiple AI applications.

### 10.2 When custom RAG may be appropriate

Custom RAG may be more suitable when an organization:

- Requires specialized retrieval algorithms.
- Has unusual document-processing requirements.
- Needs full control over indexing and embedding models.
- Has a limited set of data sources.
- Wants to build its own knowledge infrastructure.
- Has specific deployment or data-processing constraints.

### 10.3 Hybrid approach

A hybrid approach is also possible.

For example, Glean could provide organizational knowledge retrieval, while a custom retrieval service handles specialized technical artifacts that require repository-specific processing.

The final architecture should be selected based on actual requirements, security, licensing, cost, and performance.

---

## 11. Business Value for an Enterprise Software Modernization Platform

Enterprise knowledge integration can provide value beyond the technical modernization workflow.

### 11.1 Better recommendations

Modernization recommendations can consider internal standards rather than relying only on general model knowledge.

### 11.2 Reuse of organizational experience

Previously completed modernization projects can provide useful migration patterns and lessons.

### 11.3 Reduced manual research

Engineers spend less time locating documentation across multiple internal systems.

### 11.4 Improved governance

Recommendations can be compared with approved architecture and security standards.

### 11.5 Reusable knowledge infrastructure

A common knowledge integration layer can support several enterprise AI applications, not just the Modernization Agent.

For example:

- AI Code Reviewer.
- Enterprise IT Support Agent.
- Application Architecture Assistant.
- Security Compliance Agent.
- Modernization Agent.

This creates an opportunity to establish a shared enterprise knowledge capability across AI initiatives.

---

## 12. Risks, Limitations, and Open Research Questions

The following areas require validation before making an implementation decision.

| Area | Research question |
|---|---|
| Licensing | Does the organization have an appropriate Glean subscription and developer access? |
| Connectors | Are the required internal applications supported and enabled? |
| API access | Which APIs and endpoints are available in the organization's deployment? |
| Authentication | Can the integration preserve the intended user's identity and permissions? |
| Data quality | Are internal standards accurate, current, and properly maintained? |
| Retrieval quality | Can the platform retrieve highly specific technical guidance? |
| Integration | How easily can the retrieval service fit into the existing Google ADK workflow? |
| Performance | What is the additional latency for each retrieval request? |
| Cost | Is a managed platform more economical than custom RAG for the intended workload? |
| Governance | Who owns the approval and maintenance of enterprise knowledge? |

A particularly important question is whether the connected enterprise data contains enough high-quality modernization knowledge to make retrieval valuable.

A knowledge platform cannot compensate for missing, contradictory, or outdated organizational documentation.

---

## 13. Recommended Implementation Roadmap

A phased approach reduces integration risk.

| Phase | Activity | Expected outcome |
|---|---|---|
| Phase 1 | Understand enterprise knowledge and RAG fundamentals | Clear understanding of the technology |
| Phase 2 | Evaluate Glean connectors, Search API, Chat API, and security | Platform capability assessment |
| Phase 3 | Define modernization knowledge requirements | List of required documents and queries |
| Phase 4 | Build a small retrieval integration | Working knowledge retrieval component |
| Phase 5 | Integrate with selected Google ADK agents | Context-aware modernization workflow |
| Phase 6 | Compare baseline and enhanced outputs | Measured POC results |
| Phase 7 | Evaluate security, cost, scalability, and adoption | Implementation recommendation |

**Recommended starting point:** Complete the capability and access evaluation before designing a production integration.

If Glean access is unavailable, the team can still validate the architecture using a mock retrieval service or a small custom RAG prototype. Such a prototype should be treated as a separate experiment, not as proof of Glean functionality.

---

## 14. Conclusion

Enterprise knowledge integration represents an important enhancement opportunity for AI-powered software modernization.

A conventional modernization agent primarily focuses on understanding the technical condition of a software application. Enterprise knowledge integration adds organizational context, allowing the agent to consider internal engineering standards, architecture decisions, security requirements, and historical modernization experience.

Glean is one platform worth evaluating for this purpose because it provides enterprise connectors, knowledge retrieval, search and chat APIs, agent capabilities, and MCP-based integration options.

For the existing Google ADK-based Modernization Agent, the most practical direction is to evaluate Glean as a complementary knowledge layer while retaining the current repository analysis, deterministic detection, agent orchestration, and validation capabilities.

A focused proof of concept involving one repository, a small set of enterprise standards, and a few selected agents would provide evidence about technical feasibility and business value.

The long-term objective should not simply be to add another AI platform. It should be to build modernization systems that understand both the software being modernized and the enterprise environment in which that software must operate.

---

## 15. Key Takeaways

1. LLMs provide general reasoning and language capabilities, but do not automatically know an organization's private engineering standards.
2. Enterprise Search helps retrieve information across organizational applications.
3. RAG supplies relevant external information to an LLM before it generates an answer.
4. Enterprise knowledge platforms can manage much of the connector, indexing, and retrieval infrastructure.
5. Glean can be evaluated as a shared enterprise knowledge layer for existing AI applications.
6. Google ADK can continue to manage the Modernization Agent's specialized workflows and orchestration.
7. Search API integration is a reasonable first experiment for selected modernization agents.
8. Permission-aware retrieval, evidence traceability, and validation are essential.
9. A POC should compare the existing baseline against enterprise-context-enhanced recommendations.
10. Licensing, connector availability, API access, security, and cost must be validated before proposing production adoption.

---

## 16. References and Further Reading

**Glean Developer Platform**

- [Glean Developer Documentation](https://developers.glean.com/)
- [Glean Platform API Overview](https://developers.glean.com/api/platform-api)
- [Glean Search and Developer Capabilities](https://developers.glean.com/)
- [Glean Agents API Overview](https://developers.glean.com/api/platform-api/agents-overview)
- [Glean Remote MCP Server](https://developers.glean.com/guides/mcp/)

**Glean Architecture and Security**

- [Glean Connectors](https://docs.glean.com/connectors/about)
- [How Connectors Power Glean](https://docs.glean.com/connectors/connectors-power-glean)
- [Glean Knowledge Graph](https://docs.glean.com/security/knowledge-graph)
- [Glean Security and Architecture](https://docs.glean.com/security/home)

**Further technical study**

- Retrieval-Augmented Generation (RAG).
- Semantic Search and Vector Databases.
- Embedding Models and Document Chunking.
- Enterprise Identity and Access Management.
- Google Agent Development Kit (ADK).
- Model Context Protocol (MCP).
- AI Agent Evaluation and Observability.

**Research note:** This document describes an architectural proposal and research direction. It does not claim that Glean is currently deployed at Miracle, that the required subscription or API access exists, or that the proposed integration has been tested. Platform features and availability should be confirmed against the applicable tenant and current documentation before implementation.
