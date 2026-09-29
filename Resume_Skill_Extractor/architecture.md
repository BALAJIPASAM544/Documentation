# Architecture

## Overview

The service follows a **ports-and-adapters (hexagonal)** design.
Business logic in `services/` is decoupled from external systems through
the abstract `Protocol` interfaces defined in `ports.py`. Each integration
(`hubble.py`, `ai.py`, `s3.py`) is a concrete adapter that can be swapped or
mocked independently.

---

## Component Diagram

```mermaid
graph TD
    Client["HTTP Client / Caller"]

    subgraph FastAPI["FastAPI Application"]
        Routes["api/routes/resumes.py\n(POST /resumes/process\nPOST /resumes/upload)"]
        Health["api/routes/health.py\n(GET /health)"]
        Processor["services/batch_processing.py\nResumeBatchProcessor"]

        subgraph Ports["ports.py — Protocol Interfaces"]
            CS["CandidateSource"]
            RE["ResumeExtractor"]
            OS["OutputStore"]
        end

        subgraph Integrations["integrations/"]
            Hubble["hubble.py\nHubbleCandidateSource"]
            AI["ai.py\nOpenAIResumeExtractor"]
            S3["s3.py\nS3OutputStore"]
        end

        subgraph Core["core/"]
            Config["config.py\nSettings / Secrets"]
            KeyEx["key_extractor.py\nSSM → Hubble JWT"]
            TokenGen["token_generator.py\nAES-CBC Auth Token"]
        end

        subgraph Schemas["schemas/"]
            ResSchema["resume.py\nCandidateDetails\nHubbleResume\nExtractedResume\nFailedResumeRecord\nCandidateSkillStatus"]
        end
    end

    HubbleAPI["Hubble API\n(UAT)\nGET candidate-resumes\nPUT update-skills"]
    OpenAIAPI["OpenAI / Azure OpenAI\nchat.completions"]
    S3Bucket["AWS S3 Bucket\noutput/resumes/<candidate_id>.json\noutput/failed/<candidate_id>.json"]
    SSM["AWS SSM Parameter Store\n/hubble/resume/jwt"]

    Client --> Routes
    Client --> Health
    Routes --> Processor
    Processor --> CS
    Processor --> RE
    Processor --> OS
    CS --> Hubble
    RE --> AI
    OS --> S3
    Hubble --> HubbleAPI
    AI --> OpenAIAPI
    S3 --> S3Bucket
    KeyEx --> SSM
    Config --> Hubble
    Config --> AI
    Config --> S3
    TokenGen --> Hubble
    KeyEx --> TokenGen
```

---

## End-to-End Data Flow

```mermaid
sequenceDiagram
    participant Caller
    participant API as FastAPI (resumes.py)
    participant Proc as ResumeBatchProcessor
    participant HubbleGET as Hubble GET API
    participant S3Check as S3 (exists check)
    participant AIModel as AI Model
    participant S3Write as S3 (write JSON)
    participant HubblePUT as Hubble PUT API

    Caller->>API: POST /api/v1/resumes/process?page_number=1&page_size=50
    API->>Proc: process_batch(page_number=1, page_size=50)
    Proc->>HubbleGET: GET candidate-resumes?pageno=1&pagesize=50
    HubbleGET-->>Proc: list[HubbleResume] (presigned URLs)

    loop For each resume (sorted by added_at)
        Proc->>S3Check: exists(output_key)?
        alt Already processed
            S3Check-->>Proc: True → status=skipped
        else Not yet processed
            Proc->>AIModel: extract(resume_url) [with retries]
            AIModel-->>Proc: CandidateDetails JSON
            Proc->>S3Write: write_json(output_key, payload)
            S3Write-->>Proc: OK → status=processed
        end
    end

    Proc->>HubblePUT: PUT update-skills [{candidateId, status}, …]
    HubblePUT-->>Proc: 200 OK
    Proc-->>API: list[BatchItemResult]
    API-->>Caller: ProcessResumesResponse
```

---

## Layered Layout

| Layer | Path | Responsibility |
|---|---|---|
| **HTTP boundary** | `api/routes/` | Request parsing, response shaping, HTTP errors |
| **Orchestration** | `services/batch_processing.py` | Batch loop, ordering, skip/retry/fail logic, status collection |
| **Ports** | `ports.py` | `Protocol` interfaces — the seam between business logic and adapters |
| **Adapters** | `integrations/` | Hubble HTTP client, OpenAI/Azure client, S3 boto3 client |
| **Configuration** | `core/config.py` | `pydantic-settings` — all env-driven settings |
| **Auth helpers** | `core/key_extractor.py`, `core/token_generator.py` | SSM fetch + AES-CBC token generation for Hubble auth |
| **Contracts** | `schemas/resume.py` | Pydantic models for input/output; alias normalisation; dice_context detection |

---

## Key Design Decisions

### Idempotency via S3 existence check
Before each extraction attempt, `S3OutputStore.exists()` is called with the
deterministic `output_key` (`output/resumes/<candidate_id>.json`).
This makes the workflow **restartable at zero cost** — no external state
database is required.

### Ports-and-adapters (Protocol interfaces)
`ResumeBatchProcessor` depends on three `Protocol` types: `CandidateSource`,
`ResumeExtractor`, and `OutputStore`. Tests use `FakeSource`, `FakeExtractor`,
and `FakeStore` — no HTTP or AWS calls needed in CI.

### Configurable AI system prompt
The extraction instructions live entirely in `AI_SYSTEM_PROMPT` (`.env`),
not in application code. This lets the prompt be tuned without a code
deployment.

### Dice context detection
After AI extraction, the raw resume text is scanned for Dice-specific markers
(e.g., `@mail.dice.com`). If found, `dice_context=true` is injected into the
`CandidateDetails` response, flagging that the document may include appended
Dice profile pages that were excluded from the extraction.

### AES-CBC auth token for Hubble
The Hubble API requires a Bearer token generated by AES-CBC encrypting the
current Eastern Date-Time with the Hubble JWT key (fetched from AWS SSM at
startup). This logic is isolated in `core/token_generator.py`.
