# Developer Guide

This guide explains how to extend the application by adding new integrations,
modifying the AI extraction prompt, changing the output format, or adding new
API endpoints. It assumes you have already completed the [setup steps in the README](../README.md#setup).

---

## Table of Contents

1. [Adding a New Resume Source](#1-adding-a-new-resume-source)
2. [Adding a New AI Extractor](#2-adding-a-new-ai-extractor)
3. [Adding a New Output Store](#3-adding-a-new-output-store)
4. [Modifying the AI System Prompt](#4-modifying-the-ai-system-prompt)
5. [Extending the CandidateDetails Schema](#5-extending-the-candidatedetails-schema)
6. [Adding a New API Endpoint](#6-adding-a-new-api-endpoint)
7. [Adding New Configuration Variables](#7-adding-new-configuration-variables)
8. [Writing Tests](#8-writing-tests)
9. [Authentication — How the Hubble Token Works](#9-authentication--how-the-hubble-token-works)

---

## 1. Adding a New Resume Source

The batch processor depends on the `CandidateSource` protocol defined in
[`src/app/ports.py`](../src/app/ports.py):

```python
class CandidateSource(Protocol):
    def fetch_page(self, *, page_number: int, page_size: int) -> list[HubbleResume]: ...
    def last_modified(self, resume: HubbleResume) -> datetime | None: ...
    def update_candidate_skills(self, updates: list[CandidateSkillStatus]) -> bool: ...
```

### Steps

1. Create a new file in `src/app/integrations/`, e.g. `sftp.py`.
2. Implement a class that satisfies the `CandidateSource` protocol
   (no explicit inheritance required — Python structural typing):

```python
# src/app/integrations/sftp.py
from datetime import datetime
from app.schemas.resume import CandidateSkillStatus, HubbleResume

class SFTPCandidateSource:
    def fetch_page(self, *, page_number: int, page_size: int) -> list[HubbleResume]:
        # Pull resumes from SFTP and return HubbleResume objects
        ...

    def last_modified(self, resume: HubbleResume) -> datetime | None:
        # Return the file modification time
        ...

    def update_candidate_skills(self, updates: list[CandidateSkillStatus]) -> bool:
        # No-op or custom status write
        return True
```

3. Wire it into the route in [`src/app/api/routes/resumes.py`](../src/app/api/routes/resumes.py):

```python
from app.integrations.sftp import SFTPCandidateSource

processor = ResumeBatchProcessor(
    source=SFTPCandidateSource(),   # <-- swap here
    extractor=OpenAIResumeExtractor(),
    output_store=S3OutputStore(),
)
```

> The batch processor, retry logic, and S3 output are completely unchanged.

---

## 2. Adding a New AI Extractor

The batch processor calls `extractor.extract(resume_url=...)` via the
`ResumeExtractor` protocol:

```python
class ResumeExtractor(Protocol):
    def extract(self, *, resume_url: str) -> CandidateDetails: ...
```

### Steps

1. Create a new file, e.g. `src/app/integrations/anthropic_ai.py`.
2. Implement the class:

```python
# src/app/integrations/anthropic_ai.py
import anthropic
from app.schemas.resume import CandidateDetails

class AnthropicResumeExtractor:
    def extract(self, *, resume_url: str) -> CandidateDetails:
        client = anthropic.Anthropic()
        # Download resume bytes, send to Anthropic, parse response
        ...
        return CandidateDetails.model_validate(parsed_dict)
```

3. Swap it in `resumes.py`:

```python
from app.integrations.anthropic_ai import AnthropicResumeExtractor

processor = ResumeBatchProcessor(
    source=HubbleCandidateSource(),
    extractor=AnthropicResumeExtractor(),   # <-- swap here
    output_store=S3OutputStore(),
)
```

---

## 3. Adding a New Output Store

The `OutputStore` protocol requires two methods:

```python
class OutputStore(Protocol):
    def exists(self, *, key: str) -> bool: ...
    def write_json(self, *, key: str, payload: dict) -> None: ...
```

### Example — Azure Blob Storage

```python
# src/app/integrations/azure_blob.py
from azure.storage.blob import BlobServiceClient

class AzureBlobOutputStore:
    def __init__(self) -> None:
        self.client = BlobServiceClient.from_connection_string(...)
        self.container = "resume-output"

    def exists(self, *, key: str) -> bool:
        blob = self.client.get_blob_client(self.container, key)
        return blob.exists()

    def write_json(self, *, key: str, payload: dict) -> None:
        import json
        blob = self.client.get_blob_client(self.container, key)
        blob.upload_blob(json.dumps(payload).encode(), overwrite=True)
```

---

## 4. Modifying the AI System Prompt

The system prompt is **entirely configuration-driven** — no code change needed.

Edit `.env`:

```dotenv
AI_SYSTEM_PROMPT="You are an expert ATS resume parser. Extract the following fields from the resume and return strict JSON: full_name, email, phone, location, skills (array), experience (array of objects), education (array of objects). Do NOT include any commentary outside the JSON object."
```

Restart the server and the new prompt takes effect immediately.

> **Tip:** The model is also configurable — to switch from `gpt-4.1-mini` to
> `gpt-4o` just set `AI_MODEL=gpt-4o` in `.env`.

---

## 5. Extending the CandidateDetails Schema

`CandidateDetails` is defined in [`src/app/schemas/resume.py`](../src/app/schemas/resume.py).

### Add a new optional field

```python
class CandidateDetails(BaseModel):
    ...
    certifications: list[str | dict] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    linkedin_url: str | None = None
```

Pydantic will automatically include the new fields in the JSON response and
S3 output payload without any additional changes. The AI model will populate
them when present in the resume text (assuming the system prompt asks for them).

### Alias support (camelCase API compatibility)

If the AI returns `linkedinUrl` instead of `linkedin_url`, add an alias:

```python
linkedin_url: str | None = Field(
    default=None,
    validation_alias=AliasChoices("linkedin_url", "linkedinUrl"),
)
```

---

## 6. Adding a New API Endpoint

### Step 1 — Create a route module

```python
# src/app/api/routes/candidates.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):
    ...
```

### Step 2 — Register in the router

Open [`src/app/api/router.py`](../src/app/api/router.py) and add:

```python
from app.api.routes import candidates

api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
```

The endpoint will be available at `/api/v1/candidates/{candidate_id}` and
will appear automatically in Swagger UI.

---

## 7. Adding New Configuration Variables

All configuration lives in [`src/app/core/config.py`](../src/app/core/config.py).

### Step 1 — Add the field to `Settings`

```python
class Settings(BaseSettings):
    ...
    sftp_host: str = ""
    sftp_port: int = 22
    sftp_username: str = ""
```

### Step 2 — Add to `.env.example`

```dotenv
SFTP_HOST=
SFTP_PORT=22
SFTP_USERNAME=
```

### Step 3 — Use in your integration

```python
from app.core.config import settings

client = SFTPClient(host=settings.sftp_host, port=settings.sftp_port)
```

`pydantic-settings` automatically maps `SFTP_HOST` → `sftp_host` via
case-insensitive env var resolution.

---

## 8. Writing Tests

Tests live in `tests/` and use `pytest`. The project favours **in-process
fakes** over mocking frameworks for integration tests.

### Fake pattern (preferred)

See `tests/test_batch_processing.py` for the `FakeSource`, `FakeExtractor`,
and `FakeStore` pattern — they implement the same `Protocol` interfaces as
the real adapters, letting you test all orchestration logic without any I/O.

### FastAPI test client

```python
# tests/test_my_endpoint.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_my_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
```

### Run tests

```powershell
pytest                              # all tests
pytest tests/test_batch_processing.py  # one file
pytest -k "test_failed"            # by keyword
pytest --cov=app                   # with coverage
```

---

## 9. Authentication — How the Hubble Token Works

The Hubble API requires a dynamically generated Bearer token on every request.

### Token generation flow

```
AWS SSM Parameter Store
    /hubble/resume/jwt
         |
         v
   Hubble JWT key  (16/24/32 byte AES key)
         |
         v
   AES-CBC encrypt( current Eastern time string )
         |
         v
   Base64-encode → replace "/" with "-"
         |
         v
   Authorization: Bearer <token>
```

This is implemented in:

- [`core/key_extractor.py`](../src/app/core/key_extractor.py) — fetches the JWT key from SSM at startup.
- [`core/token_generator.py`](../src/app/core/token_generator.py) — `encrypt_value(key, value)` + `get_encrypted_current_edt()`.
- [`integrations/hubble.py`](../src/app/integrations/hubble.py) — `_get_headers()` calls these on every request so the timestamp is always fresh.

### Local development without SSM

Set `HUBBLE_KEY=<your-jwt-key>` directly in `.env`. The application will use
this value and skip the SSM fetch.
