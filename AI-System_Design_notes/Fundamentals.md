# AI SYSTEM DESIGN
## Research Notes – From Fundamentals to Production Architecture

**Learning approach:** Fundamentals → Architecture → Implementation → Evaluation → Production → Optimization

**Running example:** Enterprise AI Customer Support Assistant

---

# PART 1: UNDERSTANDING SYSTEM DESIGN

## Chapter 1: Introduction to System Design

### 1.1 What is System Design?

System Design is the process of defining the architecture, components, interactions, data flows, and infrastructure required to build a software system.

In simple terms, System Design answers:

- What components do we need?
- How will these components communicate?
- Where will data be stored?
- How will requests be processed?
- How will the system handle increasing users?
- How will we maintain reliability and security?

System Design is not just about writing code. It is about planning how an entire application should work.

### 1.2 Why do we need System Design?

Consider a simple application that allows users to upload documents.

Initially, we might build:

1. A frontend for uploading documents.
2. A backend API for receiving files.
3. A database for storing document information.
4. Storage for maintaining uploaded files.

This may work perfectly for ten users.

But what happens when the application has 100,000 users?

We may encounter:

- Slow responses.
- Database overload.
- Storage limitations.
- Server failures.
- Concurrent request handling problems.

Without proper system design, an application that works as a prototype may fail when used at scale.

**Core principle:** System Design helps us move from a working application to a reliable and maintainable application.

### 1.3 How does a traditional software system work?

Consider an online shopping application.

The basic request flow is:

User → Frontend → Backend → Database → Backend → Frontend → User

Each component has a responsibility.

| Component | Responsibility |
|---|---|
| Frontend | Provides user interaction |
| Backend | Executes application logic |
| API | Enables communication between components |
| Database | Stores structured information |
| Storage | Stores files and other objects |
| Infrastructure | Provides computing and networking resources |

### 1.4 When do we need System Design?

System Design becomes particularly important when:

- An application has multiple components.
- Multiple users access the system simultaneously.
- Data volume increases.
- Performance becomes important.
- Different services need to communicate.
- The application needs high availability.
- Security and reliability become business requirements.

Even small applications benefit from basic design decisions. The depth of design should match the complexity of the problem.

### 1.5 Who is involved in System Design?

Different roles contribute to the system:

- Software Architects: Define overall architecture.
- Backend Engineers: Design application logic and APIs.
- Frontend Engineers: Design user-facing applications.
- Database Engineers: Design data storage and retrieval.
- DevOps Engineers: Manage infrastructure and deployment.
- Security Engineers: Protect systems and information.
- Product Managers: Define business requirements.

### 1.6 Important System Design terminology

**Client:** A program or device that requests a service.

**Server:** A system that receives and processes client requests.

**API:** An interface that allows software components to communicate.

**Database:** An organized system for storing and retrieving data.

**Scalability:** The ability of a system to handle increasing workloads.

**Availability:** The ability of a system to remain accessible when needed.

**Latency:** The time taken to process a request and return a response.

**Throughput:** The amount of work a system processes within a given time.

**Reliability:** The ability of a system to perform consistently and correctly.

---

# Chapter 2: From System Design to AI System Design

### 2.1 What is AI System Design?

AI System Design is the process of designing a complete software system that uses artificial intelligence to solve a specific problem.

It combines traditional software architecture with AI-specific components such as:

- Machine Learning models.
- Large Language Models.
- Data processing pipelines.
- Embedding models.
- Retrieval systems.
- AI agents.
- Model serving infrastructure.
- Evaluation and monitoring systems.

An important distinction:

AI System Design is not simply connecting an LLM API to a frontend.

It requires designing how the AI model interacts with the application, data, tools, users, and infrastructure.

### 2.2 Why is AI System Design different?

Traditional applications generally execute predefined instructions and business rules.

For example:

IF account_balance >= withdrawal_amount:
    Allow withdrawal
ELSE:
    Reject withdrawal

The output is determined by the implemented rules and input.

Now consider an AI application.

A user asks:

"Summarize the key risks mentioned in this contract."

The system must:

1. Receive the document.
2. Extract its contents.
3. Understand the user's request.
4. Process the document using an AI model.
5. Generate a summary.
6. Evaluate or validate the response.
7. Return the result.

The processing is more complex because AI models introduce uncertainty, model-specific limitations, and additional computational requirements.

### 2.3 Traditional System Design vs AI System Design

| Dimension | Traditional System | AI System |
|---|---|---|
| Processing | Programmed business logic | Business logic + AI inference |
| Output | Often deterministic | Often probabilistic |
| Data | Application data | Application data + contextual information |
| Intelligence | Rules and algorithms | ML models and LLMs |
| Testing | Functional testing | Functional + AI evaluation |
| Monitoring | Application health | Application + model performance |
| Optimization | Code and database optimization | Code + model + token + inference optimization |

AI System Design extends traditional System Design. It does not replace it.

### 2.4 Who needs AI System Design?

- AI Engineers
- ML Engineers
- LLM Engineers
- Software Architects
- Backend Engineers working on AI applications
- Data Engineers
- MLOps Engineers
- Technical Product Architects

### 2.5 When do we need AI System Design?

Whenever a business application depends on AI capabilities beyond a simple isolated model prediction.

Examples:

- Enterprise knowledge assistants.
- AI-powered customer support.
- Resume screening and extraction.
- Document intelligence.
- Code review assistants.
- Fraud detection systems.
- AI workflow automation.

---

# Chapter 3: Understanding the AI System Design Landscape

Before studying individual technologies, understand the major areas that form a complete AI system.

### 3.1 The major building blocks

1. Problem Definition – Understand the business problem.
2. Application Architecture – Design frontend, backend, APIs, and services.
3. Data Architecture – Understand data sources, processing, and storage.
4. Model Architecture – Select appropriate ML or LLM models.
5. AI Application Layer – Integrate prompts, retrieval, memory, and tools.
6. Infrastructure – Provide compute, storage, networking, and deployment.
7. Evaluation – Measure correctness, relevance, and performance.
8. Operations – Monitor, secure, maintain, and optimize the system.

### 3.2 The AI System Design lifecycle

Problem Identification
→ Requirement Analysis
→ Architecture Design
→ Data Preparation
→ Model Selection
→ Application Development
→ Evaluation
→ Deployment
→ Monitoring
→ Continuous Improvement

The lifecycle is iterative. Production observations may require changes to the original architecture.

---

# PART 2: THE FIVE-LAYER AI SYSTEM DESIGN FRAMEWORK

This section uses the five-layer framework discussed in the reference video as a learning structure. It is an organizing framework, not the only accepted way to design AI systems.

## Layer 1: Scope and Assumptions

Understand what needs to be built.

Research questions:

- What business problem are we solving?
- Who are the users?
- What inputs and outputs are expected?
- What are the functional requirements?
- What are the non-functional requirements?
- What should AI be allowed to do?
- What should require human approval?

## Layer 2: Architecture

Design how the system works.

Study:

- Frontend and backend architecture.
- Client-server communication.
- Databases and storage.
- Model integration.
- RAG architecture.
- Tool calling.
- Memory.
- Agent orchestration.

A useful mental framework from the video is KARC:

**Know:** What information should the AI access?

**Act:** What actions should the AI perform?

**Remember:** What information should it retain?

**Coordinate:** How should the different capabilities work together?

## Layer 3: Observability

Understand what is happening inside the system.

Study:

- Logging.
- Tracing.
- Metrics.
- Model input and output tracking.
- Tool execution tracking.
- Failure analysis.
- AI evaluation.

## Layer 4: Production and Operations

Make the application reliable for real users.

Study:

- Scalability.
- Latency.
- Reliability.
- Availability.
- Security.
- Data freshness.
- Infrastructure.
- Deployment.

## Layer 5: Optimization

Continuously improve the system.

Study:

- Model selection.
- Prompt optimization.
- Token optimization.
- Caching.
- Cost reduction.
- Latency reduction.
- Quality improvement.
- Architecture trade-offs.

---

# PART 3: OUR RUNNING RESEARCH EXAMPLE

## Chapter 4: Designing an Enterprise Customer Support Assistant

### Business problem

An e-commerce company receives thousands of customer support requests.

The existing support team manually handles:

- Order status questions.
- Refund requests.
- Return policies.
- Product questions.
- Support ticket creation.

The company wants an AI-powered assistant to automate appropriate support tasks.

### Functional requirements

The system should:

1. Answer common customer questions.
2. Retrieve order information.
3. Search company policies.
4. Create support tickets.
5. Escalate complex requests to human agents.

### Non-functional requirements

The system should:

- Respond quickly.
- Support concurrent users.
- Protect customer information.
- Avoid unauthorized actions.
- Provide reliable responses.
- Maintain reasonable operating costs.

### Basic architecture

Customer
→ Frontend
→ Backend API
→ Authentication
→ AI Application
→ Knowledge Retrieval / Business Tools
→ LLM
→ Response Validation
→ Customer

Supporting components:

- Database
- Document storage
- Model provider
- Monitoring
- Evaluation
- Infrastructure

### Example interaction

Customer: "Can I return my order?"

The system:

1. Receives the question.
2. Identifies the customer's intent.
3. Retrieves the return policy.
4. Checks order information if required.
5. Uses the LLM to formulate an answer.
6. Returns the response.
7. Escalates the request if necessary.

### Important architectural decision

Not every question needs an agent, a vector database, or a complex multi-agent architecture.

The architecture should be based on the actual requirements.

Start with the simplest design that meets the requirements. Introduce complexity only when justified.

---

# PART 4: LEARNING AND RESEARCH DIRECTION

The following subjects will be explored progressively.

## Stage 1 – Traditional System Design

- Client-server architecture.
- Monolithic and microservices architecture.
- APIs and HTTP.
- Databases.
- Caching.
- Load balancing.
- Scalability.
- Availability and reliability.

## Stage 2 – AI and ML Fundamentals

- Artificial Intelligence.
- Machine Learning.
- Deep Learning.
- Neural networks.
- Transformers.
- LLM fundamentals.
- Training and inference.

## Stage 3 – LLM Engineering

- Tokenization.
- Embeddings.
- Prompt engineering.
- Context windows.
- Model selection.
- Fine-tuning.
- Quantization.
- Inference optimization.

## Stage 4 – AI Application Architecture

- RAG.
- Vector databases.
- Hybrid search.
- Reranking.
- Function calling.
- Tool integration.
- Memory.
- AI agents.
- Multi-agent systems.
- Agent orchestration.

## Stage 5 – Production AI Engineering

- Model serving.
- GPU and CPU infrastructure.
- API gateways.
- Asynchronous processing.
- Queues.
- Caching.
- Security.
- Guardrails.
- Monitoring.
- Observability.
- Evaluation.

## Stage 6 – Advanced AI System Design

- Large-scale inference systems.
- Distributed AI architecture.
- Multi-model orchestration.
- Agent reliability.
- Cost optimization.
- High-availability AI systems.
- Enterprise AI architecture.

---

# FINAL RESEARCH OBJECTIVE

By completing this learning journey, the objective is to be able to:

1. Understand a business problem and translate it into technical requirements.
2. Identify the components required for an AI application.
3. Design an end-to-end AI architecture.
4. Explain why a particular technology is selected.
5. Compare different architectural approaches.
6. Identify limitations, bottlenecks, and failure scenarios.
7. Build a working proof of concept.
8. Evaluate and deploy the application.
9. Explain the architecture and design decisions to a technical team.

**The ultimate goal is not just to learn AI technologies. It is to develop the ability to design complete, reliable, scalable, and cost-effective AI-powered systems.**
