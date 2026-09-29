# Resume Candidate Details Extraction

> **POC** — FastAPI service that ingests candidate resumes from the Hubble recruitment API, extracts structured candidate details using an OpenAI-compatible LLM, stores the results in AWS S3, and reports processing status back to Hubble.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Layout](#project-layout)
4. [Prerequisites](#prerequisites)
5. [Setup](#setup)
6. [Configuration Reference](#configuration-reference)
7. [Running the API](#running-the-api)
8. [API Reference](#api-reference)
9. [Batch Processing Workflow](#batch-processing-workflow)
10. [Output Structure](#output-structure)
11. [Docker](#docker)
12. [Testing & Linting](#testing--linting)

---

## Overview

The service implements the following end-to-end pipeline:

```
Hubble GET API  →  Batch Processor  →  AI Extraction  →  S3 JSON Store
                         ↑                                      ↓
                  Duplicate Check               Hubble PUT (status update)
```

Key capabilities:

| Capability | Detail |
|---|---|
| Resume sources | Hubble pagination API (presigned S3 URLs) |
| Supported formats | PDF, DOC, DOCX |
| AI provider | OpenAI (`gpt-4.1-mini`) **or** Azure OpenAI |
| Output | One JSON file per resume in S3 |
| Idempotency | S3 existence check skips already-processed resumes |
| Retries | Configurable count with exponential backoff |
| Failure tracking | Separate `output/failed/` prefix in S3 |
| Status reporting | Batch `PUT` to Hubble update-skills endpoint |
| Scale | Designed for ~300,000 resumes via incremental page-by-page batches |

---

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the full Mermaid flow diagram.

The application follows a **ports-and-adapters** (hexagonal) pattern:

```
api/routes          ← HTTP boundary
    │
services/           ← Use-case orchestration (ResumeBatchProcessor)
    │
ports.py            ← Protocol interfaces (CandidateSource, ResumeExtractor, OutputStore)
    │
integrations/       ← Concrete adapters
  hubble.py         ← Hubble API client
  ai.py             ← OpenAI / Azure OpenAI adapter
  s3.py             ← AWS S3 adapter
    │
core/               ← Settings, token auth helpers
schemas/            ← Pydantic contracts
```

---

## Project Layout

```text
resume-candidate-details-extraction/
├── src/app/
│   ├── main.py                  # FastAPI app factory + lifespan startup
│   ├── ports.py                 # Protocol interfaces (abstractions)
│   ├── api/
│   │   ├── router.py            # Mounts all route modules
│   │   └── routes/
│   │       ├── health.py        # GET /health
│   │       └── resumes.py       # POST /resumes/process, POST /resumes/upload
│   ├── core/
│   │   ├── config.py            # Settings (pydantic-settings, reads .env)
│   │   ├── key_extractor.py     # AWS SSM → Hubble JWT key fetch
│   │   └── token_generator.py   # AES-CBC token for Hubble auth
│   ├── integrations/
│   │   ├── ai.py                # OpenAI / AzureOpenAI resume extractor
│   │   ├── hubble.py            # Hubble GET & PUT API client
│   │   └── s3.py                # S3 output store (exists + write_json)
│   ├── schemas/
│   │   ├── common.py            # HealthResponse
│   │   └── resume.py            # CandidateDetails, HubbleResume, ExtractedResume, …
│   └── services/
│       └── batch_processing.py  # ResumeBatchProcessor orchestration
├── tests/
│   ├── test_batch_processing.py
│   ├── test_resume_routes.py
│   ├── test_hubble_integration.py
│   └── test_health.py
├── docs/
│   └── architecture.md          # Architecture diagram + notes
├── .env.example                 # Template for environment variables
├── Dockerfile
└── pyproject.toml
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | >= 3.11 |
| AWS account | S3 bucket + (optional) SSM parameter |
| OpenAI **or** Azure OpenAI | API key |
| uv *(recommended)* or pip | any recent |

---

## Setup

### 1. Clone and enter the project

```powershell
git clone <repo-url>
cd resume-candidate-details-extraction
```

### 2. Create a virtual environment

```powershell
# Using uv (recommended)
uv venv
.venv\Scripts\Activate.ps1
uv pip install -e ".[dev]"

# --- or plain pip ---
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

### 3. Configure environment variables

```powershell
Copy-Item .env.example .env
# Open .env and fill in your credentials (see Configuration Reference below)
```

---

## Configuration Reference

All settings are read from `.env` (or the process environment).
Settings are managed by `pydantic-settings` in [`src/app/core/config.py`](src/app/core/config.py).

### Application settings

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Resume Candidate Details Extraction` | API title shown in `/docs` |
| `APP_VERSION` | `0.1.0` | API version shown in `/docs` |
| `API_PREFIX` | `/api/v1` | Global URL prefix for all routes |
| `HOST` | `0.0.0.0` | Uvicorn bind host |
| `PORT` | `8000` | Uvicorn port |
| `RELOAD` | `false` | Enable Uvicorn hot-reload (dev only) |

### Hubble API settings

| Variable | Default | Description |
|---|---|---|
| `HUBBLE_API_URL` | `https://uat-hubble-api.miraclesoft.com/v2/recruitment/candidate-resumes` | Hubble GET endpoint for paginated resumes |
| `HUBBLE_UPDATE_SKILLS_URL` | `https://uat-hubble-api.miraclesoft.com/v2/recruitment/candidate/update-skills` | Hubble PUT endpoint for status updates |
| `HUBBLE_API_TIMEOUT_SECONDS` | `30.0` | HTTP timeout for Hubble requests |
| `HUBBLE_KEY` | *(empty)* | Pre-set Hubble JWT key (overrides SSM fetch) |
| `HUBBLE_SSM_PARAMETER` | `/hubble/resume/jwt` | AWS SSM parameter name for the Hubble JWT key |

### AI settings

| Variable | Default | Description |
|---|---|---|
| `AI_API_KEY` | *(empty)* | OpenAI API key |
| `AI_MODEL` | `gpt-4.1-mini` | Model name passed to the chat completions API |
| `AI_BASE_URL` | *(empty)* | Custom OpenAI-compatible base URL (optional) |
| `AZURE_OPENAI_ENDPOINT` | *(empty)* | If set, switches to Azure OpenAI |
| `AZURE_OPENAI_API_KEY` | *(empty)* | Azure OpenAI API key |
| `AZURE_OPENAI_API_VERSION` | `2025-01-01-preview` | Azure OpenAI API version |
| `AI_SYSTEM_PROMPT` | *(see config.py)* | System prompt instructing the model on extraction |

> **Note:** If `AZURE_OPENAI_ENDPOINT` is set, the Azure client is used. Otherwise the standard OpenAI client is used with `AI_API_KEY`.

### AWS / S3 settings

| Variable | Default | Description |
|---|---|---|
| `AWS_REGION` | `us-east-1` | AWS region for S3 and SSM |
| `AWS_ACCESS_KEY_ID` | *(empty)* | AWS access key (uses instance role/profile if absent) |
| `AWS_SECRET_ACCESS_KEY` | *(empty)* | AWS secret key |
| `OUTPUT_BUCKET` | *(empty — **required**)* | S3 bucket where extracted JSON is stored |
| `OUTPUT_PREFIX` | `output/resumes` | S3 key prefix for successful results |

### Batch processing settings

| Variable | Default | Description |
|---|---|---|
| `BATCH_SIZE` | `500` | Maximum resumes per batch (hard ceiling, also capped at 500) |
| `MAX_RETRIES` | `3` | Number of AI extraction attempts per resume |
| `RETRY_BACKOFF_SECONDS` | `2.0` | Base backoff; actual wait = `backoff x 2^attempt` |

---

## Running the API

```powershell
# With hot-reload (development)
uvicorn app.main:app --app-dir src --reload

# Or via the installed entry point
resume-api
```

- Swagger UI: **http://localhost:8000/docs**
- ReDoc:      **http://localhost:8000/redoc**

---

## API Reference

All endpoints are prefixed with `/api/v1`.

---

### `GET /api/v1/health`

Returns a simple liveness check.

**Response `200 OK`**

```json
{ "status": "ok" }
```

---

### `POST /api/v1/resumes/process`

Fetches one page of candidate resumes from Hubble, extracts candidate details via AI, stores JSON in S3, and updates processing status back in Hubble.

**Query parameters**

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `page_number` | integer | `1` | >= 1 | Hubble page to process |
| `page_size` | integer | `10` | 1 – 500 | Resumes to request per page |

**Example request**

```powershell
curl.exe -X POST "http://localhost:8000/api/v1/resumes/process?page_number=1&page_size=50"
```

**Response `200 OK`**

```json
{
  "message": "Successfully processed 50 candidate(s) from Hubble GET API, stored JSON result(s) in S3 bucket 'resume-details-extraction', and updated processing statuses via Hubble PUT API.",
  "total_candidates": 50,
  "processed_count": 44,
  "skipped_count": 4,
  "failed_count": 1,
  "unsupported_count": 1,
  "status_updated": true,
  "results": [
    { "candidate_id": "719789", "status": "processed",   "output_key": "output/resumes/719789/resume.pdf.json", "error": null },
    { "candidate_id": "719778", "status": "skipped",     "output_key": "output/resumes/719778/resume.pdf.json", "error": null },
    { "candidate_id": "719001", "status": "failed",      "output_key": "output/failed/719001/resume.pdf.json",  "error": "AI unavailable" },
    { "candidate_id": "719002", "status": "unsupported", "output_key": "output/resumes/719002/resume.txt.json", "error": "Only PDF, DOC, and DOCX resumes are supported" }
  ]
}
```

**Item status values**

| Status | Meaning |
|---|---|
| `processed` | Extracted and saved to S3 successfully |
| `skipped` | Output already exists in S3; not reprocessed |
| `failed` | All retry attempts exhausted; failure record saved to S3 |
| `unsupported` | File extension not in `{.pdf, .doc, .docx}` |

**Error responses**

| Code | Condition |
|---|---|
| `503` | `OUTPUT_BUCKET` is not configured |
| `500` | Unexpected workflow error |

---

### `POST /api/v1/resumes/upload`

Upload a single resume file to test AI extraction interactively. Does **not** interact with Hubble or S3.

**Request** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | file | Resume file (PDF, DOCX, TXT, …) |

**Example request**

```powershell
curl.exe -X POST http://localhost:8000/api/v1/resumes/upload `
  -F "file=@C:\resumes\john_doe.pdf"
```

**Response `200 OK`** — `CandidateDetails`

```json
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0100",
  "location": "Austin, TX, USA",
  "skills": ["Python", "FastAPI", "AWS"],
  "experience": [
    { "company": "Acme Corp", "role": "Backend Engineer", "duration": "2020-2024" }
  ],
  "education": [
    { "institution": "UT Austin", "degree": "B.S. Computer Science", "year": "2020" }
  ],
  "personal": null,
  "work": null,
  "dice_context": false
}
```

> **`dice_context`**: `true` when Dice-specific text indicators are detected in the resume (e.g., `@mail.dice.com`, `dice.com/employer/talent`). Signals that the document may include appended Dice context pages that were excluded from extraction.

**Error responses**

| Code | Condition |
|---|---|
| `400` | Uploaded file is empty |
| `500` | Text extraction or AI call failed |

---

## Batch Processing Workflow

The `POST /api/v1/resumes/process` endpoint implements the complete pipeline:

```
Step 1 ── Hubble GET API
          |  page of HubbleResume records (presigned S3 URLs)

Step 2 ── Sort by added_at timestamp (oldest first), then resume_path

Step 3 ── For each resume:
          |── Extension check  -->  unsupported?  -->  record + skip
          |── S3 existence check (output_key)  -->  exists?  -->  skipped
          +── AI Extraction (with retry + exponential backoff)
                |── Download resume from presigned URL
                |── Extract text  (PDF via pypdf, DOCX byte fallback, TXT as UTF-8)
                |── Send [system prompt + resume text] to AI model
                +── Validate JSON against CandidateDetails schema

Step 4 ── S3 Output
          |── Success  -->  s3://<BUCKET>/output/resumes/<candidate_id>/<filename>.json
          +── Failure  -->  s3://<BUCKET>/output/failed/<candidate_id>/<filename>.json

Step 5 ── Hubble PUT API
          +── Single batch PUT with all { candidateId, status } pairs
```

### Idempotency / restart safety

Because the S3 existence check runs before every extraction attempt, the workflow is **safe to restart**.
If the service crashes mid-batch, re-running the same page request will skip already-written keys and only process the remaining resumes.

### Processing large datasets

Call the endpoint repeatedly while advancing `page_number`:

```powershell
# Example: process pages 1-600 (500 resumes each = 300 000 total)
for ($i = 1; $i -le 600; $i++) {
    curl.exe -X POST "http://localhost:8000/api/v1/resumes/process?page_number=$i&page_size=500"
}
```

---

## Output Structure

### Successful extraction

**S3 key:** `output/resumes/<candidate_id>/<resume_filename>.json`

```json
{
  "candidate_id": "719789",
  "source_resume_path": "input/candidates/719789/resume.pdf",
  "candidate": {
    "full_name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+1-555-0199",
    "location": "New York, NY",
    "skills": ["Java", "Spring Boot", "Kubernetes"],
    "experience": [],
    "education": [],
    "personal": null,
    "work": null,
    "dice_context": false
  }
}
```

### Failed extraction

**S3 key:** `output/failed/<candidate_id>/<resume_filename>.json`

```json
{
  "candidate_id": "719001",
  "resume_path": "input/candidates/719001/resume.pdf",
  "batch_id": "page_1",
  "attempt_count": 3,
  "error_type": "TimeoutException",
  "error_message": "Read timed out.",
  "timestamp": "2026-09-29T09:30:00+00:00"
}
```

---

## Docker

```powershell
# Build
docker build -t resume-extractor .

# Run
docker run --rm -p 8000:8000 --env-file .env resume-extractor
```

> The Dockerfile installs only production dependencies. Pass credentials via `--env-file` or individual `-e` flags.

---

## Testing & Linting

```powershell
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Lint
ruff check .

# Check formatting
ruff format --check .

# Auto-fix formatting
ruff format .
```

Test files are in `tests/` and cover:

| File | Coverage |
|---|---|
| `test_batch_processing.py` | Ordering, skip-existing, retry/failure, status updates |
| `test_resume_routes.py` | `/resumes/process` and `/resumes/upload` endpoints |
| `test_hubble_integration.py` | Hubble GET/PUT client behaviour |
| `test_health.py` | Health endpoint |
