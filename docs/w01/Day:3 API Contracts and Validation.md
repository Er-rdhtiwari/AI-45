# Day 3: API Contracts, Validation, and Idempotency for Production AI Services

## 1. 5-line beginner summary

API contract means a clear agreement between client and backend about request, response, errors, and rules.
Validation checks whether incoming data is correct before business logic runs.
Pydantic helps define request and response schemas using Python classes.
Idempotency prevents duplicate operations when clients retry failed requests.
Production AI APIs must be strict, predictable, versioned, and backward-compatible.

FastAPI uses Pydantic models for request and response validation/documentation, and `response_model` helps validate, document, and filter API output. Pydantic validation creates model objects that conform to declared types and constraints. ([FastAPI][1]) ([Pydantic][2])

---

# 2. Descriptive notes

## 2.1 What is an API contract?

An **API contract** is like a written agreement between two systems.

Example:

```text
Client agrees to send:
{
  "user_id": "u123",
  "prompt": "Summarize this document",
  "max_tokens": 200
}

Server agrees to return:
{
  "request_id": "req_abc",
  "status": "completed",
  "answer": "Short summary..."
}
```

In backend interviews, you should say:

> An API contract defines request schema, response schema, status codes, error format, authentication expectations, pagination rules, versioning rules, and compatibility guarantees.

For GenAI services, API contracts matter even more because AI systems are expensive, slow, and sometimes asynchronous.

---

## 2.2 Why API contracts matter

Without a contract, the frontend, mobile app, CLI, backend service, and data platform may all make different assumptions.

Example problem:

```json
{
  "query": "What is RAG?"
}
```

One client sends `query`, another sends `prompt`, another sends `question`.

Now the backend becomes messy:

```python
prompt = body.get("prompt") or body.get("query") or body.get("question")
```

This is bad because:

```text
No clear contract
Hard to test
Hard to debug
Hard to document
Hard to version
Easy to break clients
```

A good API contract gives:

```text
Predictability
Validation
Clear errors
Easier testing
Backward compatibility
Better team collaboration
```

---

## 2.3 Request schema

A **request schema** defines what the client is allowed to send.

Example GenAI request:

```json
{
  "user_id": "user_123",
  "prompt": "Summarize this PDF",
  "model": "default-ai-model",
  "temperature": 0.3,
  "max_tokens": 300
}
```

Schema decisions:

```text
user_id       required
prompt        required
model         optional, default value
temperature   optional, must be between 0 and 2
max_tokens    optional, must be between 1 and 2000
```

In FastAPI, this is usually represented with a Pydantic model.

Pydantic models are Python classes that inherit from `BaseModel`, and fields can have defaults, optional types, nested dictionaries, and constraints. ([Pydantic][3])

---

## 2.4 Response schema

A **response schema** defines what the backend returns.

Example:

```json
{
  "request_id": "req_123",
  "status": "completed",
  "answer": "This document explains API contracts...",
  "model": "default-ai-model",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 120,
    "total_tokens": 170
  }
}
```

The response contract is important because clients depend on it.

Bad response:

```json
{
  "data": "answer here"
}
```

Better response:

```json
{
  "request_id": "req_123",
  "status": "completed",
  "answer": "answer here",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 120,
    "total_tokens": 170
  }
}
```

Why better?

```text
request_id helps debugging
status tells current state
answer contains actual result
usage helps cost tracking
model helps observability
```

FastAPI’s `response_model` can validate, document, convert, and filter the output returned by an endpoint. ([FastAPI][1])

---

## 2.5 Required vs optional fields

Required field means the API cannot work without it.

Optional field means the API can use a default value.

Example:

```python
class GenerateRequest(BaseModel):
    user_id: str
    prompt: str
    model: str = "default-ai-model"
    temperature: float = 0.3
```

Here:

```text
user_id       required
prompt        required
model         optional because default exists
temperature   optional because default exists
```

Another example:

```python
metadata: dict[str, str] | None = None
```

This means:

```text
metadata can be provided
metadata can be missing
metadata can be null
```

Interview point:

> Required fields should represent business-critical information. Optional fields should have safe defaults.

---

## 2.6 Pydantic models

Pydantic helps you define data shape using Python types.

Example:

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    temperature: float = Field(default=0.3, ge=0, le=2)
```

This means:

```text
prompt must be a string
prompt cannot be empty
prompt cannot be longer than 4000 characters
temperature defaults to 0.3
temperature must be >= 0
temperature must be <= 2
```

FastAPI can use Pydantic `Field` to declare validations and metadata for model attributes. ([FastAPI][4])

---

## 2.7 Validation errors

Validation error means the client sent invalid data.

Example invalid request:

```json
{
  "user_id": "user_123",
  "prompt": "",
  "temperature": 5
}
```

Problems:

```text
prompt is empty
temperature is above allowed range
```

Expected response should be a client error, usually `422 Unprocessable Entity` in FastAPI request validation cases.

FastAPI internally raises `RequestValidationError` when request data is invalid, and it has a default exception handler for such validation errors. ([FastAPI][5])

Good error response should be clear:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": [
      {
        "field": "prompt",
        "reason": "String should have at least 1 character"
      }
    ]
  }
}
```

In interviews, explain:

> Validation should happen before business logic, before database writes, before LLM calls, and before charging the customer.

---

## 2.8 Idempotency keys

Idempotency means:

> If the same request is sent multiple times, the server should not perform the same side effect multiple times.

Example problem:

```text
Client sends request to create an AI job.
Server creates job.
Network timeout happens.
Client does not know if job was created.
Client retries.
Server creates duplicate job.
Customer is charged twice.
```

Solution:

```text
Client sends Idempotency-Key: abc-123
Server checks if abc-123 was already processed.
If yes, return the previous response.
If no, process request and save response.
```

Stripe’s API documentation explains this production pattern clearly: a client generates an idempotency key, the server uses it to recognize retries, and repeated requests with the same key can return the same result instead of performing the operation again. ([Stripe Docs][6])

Example:

```http
POST /v1/generations
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

Important production rule:

```text
Same idempotency key + same request body = return same response
Same idempotency key + different request body = reject with conflict
```

Stripe also documents that systems can compare incoming parameters with the original request and error if they differ, preventing accidental misuse of an idempotency key. ([Stripe Docs][6])

---

## 2.9 Pagination basics

Pagination means returning data page by page instead of returning everything at once.

Bad API:

```http
GET /v1/generations
```

Returns 1 million records. Bad for memory, network, latency, and database load.

Better API:

```http
GET /v1/generations?limit=20&cursor=abc
```

Response:

```json
{
  "items": [
    {
      "request_id": "req_1",
      "status": "completed"
    }
  ],
  "next_cursor": "req_1"
}
```

Common pagination types:

```text
Offset pagination:
GET /items?offset=0&limit=20

Cursor pagination:
GET /items?cursor=req_123&limit=20
```

For production AI systems, cursor pagination is usually better for large event logs, chat history, audit logs, and job history.

---

## 2.10 Backward compatibility

Backward compatibility means:

> Old clients should continue working when the backend changes.

Usually safe changes:

```text
Adding a new optional request field
Adding a new response field if clients ignore unknown fields
Adding a new endpoint
Increasing max limit carefully
```

Usually breaking changes:

```text
Removing a response field
Renaming a field
Changing field type
Changing status code behavior
Making an optional field required
Changing error response format
```

Microsoft’s API design guidance highlights that existing client applications must continue to be supported while new clients use new features, and that more drastic schema changes such as removing or renaming fields can break clients. ([Microsoft Learn][7])

Example:

Old response:

```json
{
  "answer": "Hello"
}
```

Safe addition:

```json
{
  "answer": "Hello",
  "model": "default-ai-model"
}
```

Breaking change:

```json
{
  "generated_text": "Hello"
}
```

Why breaking?

```text
Old client expects answer.
New response removed answer.
Old client fails.
```

---

## 2.11 API compatibility in large platforms

Large companies like Google, Amazon, Netflix, and enterprise AI platforms care deeply about API compatibility.

Why?

```text
Many teams consume the same API
External customers depend on stable contracts
Mobile apps may not update immediately
Partner systems may be slow to migrate
Breaking changes cause incidents
```

In large platforms, teams usually maintain:

```text
OpenAPI specification
Schema registry
API versioning
Contract tests
Backward compatibility checks
Deprecation policy
Client SDKs
Error code standards
Observability and request tracing
```

Interview-quality answer:

> In large platforms, API compatibility is not just a coding concern. It is a product, reliability, and platform governance concern.

---

# 3. Simple GenAI API example

Imagine we are building an AI text generation API.

Client request:

```http
POST /v1/generations
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

Body:

```json
{
  "user_id": "user_123",
  "prompt": "Explain RAG in simple words",
  "model": "default-ai-model",
  "temperature": 0.3,
  "max_tokens": 200
}
```

Server response:

```json
{
  "request_id": "req_123",
  "status": "completed",
  "answer": "RAG means retrieving useful information before asking the AI to answer.",
  "model": "default-ai-model",
  "usage": {
    "prompt_tokens": 7,
    "completion_tokens": 14,
    "total_tokens": 21
  }
}
```

Production behavior:

```text
Invalid prompt -> 422 validation error
Missing idempotency key -> 400 bad request
Same key + same body -> return same previous response
Same key + different body -> 409 conflict
List old generations -> paginated response
```

---

# 4. ASCII diagram

```text
             ┌─────────────────────┐
             │      Client App      │
             │ Web / Mobile / CLI   │
             └──────────┬──────────┘
                        │
                        │ POST /v1/generations
                        │ Idempotency-Key: abc-123
                        │ JSON body
                        ▼
             ┌─────────────────────┐
             │      FastAPI API     │
             │ Routes + HTTP layer  │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │  Pydantic Contract   │
             │ Validate request     │
             │ Validate response    │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Idempotency Store    │
             │ key -> saved result  │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │    GenAI Service     │
             │ LLM / RAG / Agent    │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ JSON Response        │
             │ answer + usage       │
             └─────────────────────┘
```

---

# 5. Pseudocode first

```text
START API

DEFINE request schema:
    user_id required string
    prompt required string, min length 1
    model optional string with default
    temperature optional float between 0 and 2
    max_tokens optional integer between 1 and 2000

DEFINE response schema:
    request_id
    status
    answer
    model
    usage tokens

DEFINE idempotency store:
    idempotency key -> request hash + response

WHEN POST /v1/generations is called:
    READ Idempotency-Key header

    IF idempotency key is missing:
        RETURN 400 error

    VALIDATE request body using Pydantic

    CREATE stable hash from request body

    IF idempotency key already exists:
        IF saved request hash is different:
            RETURN 409 conflict
        ELSE:
            RETURN saved response

    CALL GenAI service
    CREATE response
    SAVE idempotency key, request hash, and response
    SAVE generation in job history
    RETURN response

WHEN GET /v1/generations is called:
    ACCEPT limit and cursor
    VALIDATE limit
    RETURN page of generations
    RETURN next_cursor if more records exist

END API
```

---

# 6. Python FastAPI + Pydantic script

```python
# 1
from __future__ import annotations

# 2
import hashlib
import json
import uuid
from typing import Literal

# 3
from fastapi import FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

# 4
app = FastAPI(title="Production GenAI API", version="1.0.0")

# 5
class Usage(BaseModel):
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)

# 6
class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=4000)
    model: str = Field(default="default-ai-model", min_length=1, max_length=100)
    temperature: float = Field(default=0.3, ge=0, le=2)
    max_tokens: int = Field(default=300, ge=1, le=2000)
    metadata: dict[str, str] | None = None

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("prompt must not be blank")
        return cleaned

# 7
class GenerateResponse(BaseModel):
    request_id: str
    status: Literal["completed"]
    answer: str
    model: str
    usage: Usage

# 8
class GenerationListItem(BaseModel):
    request_id: str
    status: Literal["completed"]
    model: str

# 9
class GenerationListResponse(BaseModel):
    items: list[GenerationListItem]
    next_cursor: str | None = None

# 10
class ErrorResponse(BaseModel):
    code: str
    message: str

# 11
idempotency_store: dict[str, dict] = {}
generation_history: list[GenerateResponse] = []

# 12
def create_request_hash(payload: GenerateRequest) -> str:
    stable_json = json.dumps(payload.model_dump(mode="json"), sort_keys=True)
    return hashlib.sha256(stable_json.encode("utf-8")).hexdigest()

# 13
def fake_llm_call(payload: GenerateRequest) -> GenerateResponse:
    words = payload.prompt.split()
    prompt_tokens = len(words)

    answer = f"AI response for: {payload.prompt}"

    completion_tokens = len(answer.split())
    total_tokens = prompt_tokens + completion_tokens

    return GenerateResponse(
        request_id=f"req_{uuid.uuid4().hex}",
        status="completed",
        answer=answer,
        model=payload.model,
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
    )

# 14
@app.post(
    "/v1/generations",
    response_model=GenerateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def create_generation(
    payload: GenerateRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> GenerateResponse:
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "MISSING_IDEMPOTENCY_KEY",
                "message": "Idempotency-Key header is required.",
            },
        )

    request_hash = create_request_hash(payload)

    if idempotency_key in idempotency_store:
        saved_record = idempotency_store[idempotency_key]

        if saved_record["request_hash"] != request_hash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_BODY",
                    "message": "Use a new Idempotency-Key for a different request body.",
                },
            )

        return saved_record["response"]

    response = fake_llm_call(payload)

    idempotency_store[idempotency_key] = {
        "request_hash": request_hash,
        "response": response,
    }

    generation_history.append(response)

    return response

# 15
@app.get("/v1/generations", response_model=GenerationListResponse)
def list_generations(
    limit: int = Query(default=10, ge=1, le=100),
    cursor: str | None = Query(default=None),
) -> GenerationListResponse:
    start_index = 0

    if cursor:
        for index, item in enumerate(generation_history):
            if item.request_id == cursor:
                start_index = index + 1
                break

    selected_items = generation_history[start_index : start_index + limit]

    next_cursor = None
    if start_index + limit < len(generation_history):
        next_cursor = selected_items[-1].request_id

    return GenerationListResponse(
        items=[
            GenerationListItem(
                request_id=item.request_id,
                status=item.status,
                model=item.model,
            )
            for item in selected_items
        ],
        next_cursor=next_cursor,
    )
```

---

# 7. Line-by-line explanation

## Lines 1–3: Imports

```python
from __future__ import annotations
```

Allows modern type hints to work smoothly.

```python
import hashlib
import json
import uuid
```

Used for request hashing, stable JSON serialization, and unique request IDs.

```python
from typing import Literal
```

Used to restrict status to fixed values like `"completed"`.

```python
from fastapi import FastAPI, Header, HTTPException, Query, status
```

Imports FastAPI app, headers, errors, query validation, and HTTP status constants.

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

Imports Pydantic tools for schema, validation, constraints, and custom validators.

FastAPI supports named status constants through `fastapi.status`, which avoids memorizing raw numeric codes. ([FastAPI][8])

---

## Line 4: FastAPI app

```python
app = FastAPI(title="Production GenAI API", version="1.0.0")
```

Creates the API app.

This also contributes to generated OpenAPI docs.

---

## Line 5: Usage model

```python
class Usage(BaseModel):
```

Defines token usage schema.

```python
prompt_tokens: int = Field(ge=0)
```

Prompt tokens cannot be negative.

```python
completion_tokens: int = Field(ge=0)
```

Generated output tokens cannot be negative.

```python
total_tokens: int = Field(ge=0)
```

Total tokens cannot be negative.

This is useful in GenAI systems because cost is usually tied to token usage.

---

## Line 6: GenerateRequest model

```python
class GenerateRequest(BaseModel):
```

Defines the request contract for creating an AI generation.

```python
model_config = ConfigDict(extra="forbid")
```

Rejects unknown fields.

Example rejected request:

```json
{
  "user_id": "u1",
  "prompt": "hello",
  "random_field": "bad"
}
```

This is stricter and safer for production APIs.

```python
user_id: str = Field(min_length=1, max_length=100)
```

Required user ID.

```python
prompt: str = Field(min_length=1, max_length=4000)
```

Required prompt with length limits.

Why length limit matters:

```text
Prevents huge payloads
Controls cost
Controls latency
Protects LLM context budget
```

```python
model: str = Field(default="default-ai-model", min_length=1, max_length=100)
```

Optional model field.

If the client does not send it, default is used.

```python
temperature: float = Field(default=0.3, ge=0, le=2)
```

Optional temperature with range validation.

```python
max_tokens: int = Field(default=300, ge=1, le=2000)
```

Optional max token limit.

```python
metadata: dict[str, str] | None = None
```

Optional metadata.

Good for request tags like:

```json
{
  "team": "search",
  "feature": "document_qa"
}
```

---

## Custom validator

```python
@field_validator("prompt")
```

Runs custom validation on `prompt`.

Pydantic supports field validators that can check a value and return the validated value; after validators run after internal validation and are usually easier to implement safely. ([Pydantic][9])

```python
def prompt_must_not_be_blank(cls, value: str) -> str:
```

Function receives prompt value.

```python
cleaned = value.strip()
```

Removes spaces.

```python
if not cleaned:
    raise ValueError("prompt must not be blank")
```

Rejects `"     "`.

```python
return cleaned
```

Returns cleaned prompt.

Important: validators should return the validated value.

---

## Line 7: GenerateResponse model

```python
class GenerateResponse(BaseModel):
```

Defines successful response contract.

```python
request_id: str
```

Useful for logs, debugging, tracing, support tickets.

```python
status: Literal["completed"]
```

Only `"completed"` is allowed.

```python
answer: str
```

Generated AI answer.

```python
model: str
```

Model used.

```python
usage: Usage
```

Nested token usage object.

---

## Line 8: GenerationListItem

```python
class GenerationListItem(BaseModel):
```

Defines one item in the list API.

It intentionally does not return the full answer.

Why?

```text
List APIs should be lightweight
Full details can be fetched separately
Better performance
Less data transfer
```

---

## Line 9: GenerationListResponse

```python
class GenerationListResponse(BaseModel):
```

Defines paginated response.

```python
items: list[GenerationListItem]
```

List of generation records.

```python
next_cursor: str | None = None
```

Cursor for the next page.

If `next_cursor` is null, there are no more records.

---

## Line 10: ErrorResponse

```python
class ErrorResponse(BaseModel):
    code: str
    message: str
```

Defines a standard error shape.

Example:

```json
{
  "code": "MISSING_IDEMPOTENCY_KEY",
  "message": "Idempotency-Key header is required."
}
```

In real production, you may also include:

```text
request_id
details
documentation_url
retryable
```

---

## Line 11: In-memory stores

```python
idempotency_store: dict[str, dict] = {}
generation_history: list[GenerateResponse] = []
```

For teaching, we use in-memory dictionaries/lists.

In production, use:

```text
Redis
PostgreSQL
DynamoDB
Cloud Spanner
CockroachDB
```

Important: in-memory storage is lost when the server restarts.

---

## Line 12: Request hash

```python
def create_request_hash(payload: GenerateRequest) -> str:
```

Creates a fingerprint of the request body.

```python
stable_json = json.dumps(payload.model_dump(mode="json"), sort_keys=True)
```

Converts request body to stable JSON.

Why `sort_keys=True`?

```text
{"a": 1, "b": 2}
{"b": 2, "a": 1}
```

These should produce the same hash.

```python
return hashlib.sha256(stable_json.encode("utf-8")).hexdigest()
```

Creates SHA-256 hash.

Used to detect whether same idempotency key was reused with a different request body.

---

## Line 13: Fake LLM call

```python
def fake_llm_call(payload: GenerateRequest) -> GenerateResponse:
```

Simulates a real LLM call.

In production, this would call:

```text
OpenAI
Vertex AI
Bedrock
Azure OpenAI
Internal LLM gateway
RAG pipeline
Agent service
```

```python
words = payload.prompt.split()
prompt_tokens = len(words)
```

Fake token counting.

Real systems use model-specific tokenizers.

```python
answer = f"AI response for: {payload.prompt}"
```

Fake generated answer.

```python
completion_tokens = len(answer.split())
total_tokens = prompt_tokens + completion_tokens
```

Fake usage calculation.

```python
request_id=f"req_{uuid.uuid4().hex}"
```

Creates unique request ID.

---

## Line 14: POST endpoint

```python
@app.post("/v1/generations", ...)
```

Defines API endpoint for creating an AI generation.

```python
response_model=GenerateResponse
```

FastAPI validates/documents/filters the response using this model.

```python
status_code=status.HTTP_201_CREATED
```

Returns 201 Created for new generation request.

HTTP status codes are grouped by meaning: 200–299 for successful responses, 400–499 for client errors, and 500–599 for server errors. ([FastAPI][10])

```python
responses={
    400: {"model": ErrorResponse},
    409: {"model": ErrorResponse},
}
```

Documents extra error responses.

```python
payload: GenerateRequest
```

FastAPI validates JSON request body using the Pydantic model.

```python
idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")
```

Reads `Idempotency-Key` header.

---

## Missing idempotency key

```python
if not idempotency_key:
    raise HTTPException(...)
```

Rejects request if key is missing.

FastAPI’s `HTTPException` is used to abort request execution and return client-facing errors such as invalid data or missing resources. ([FastAPI][11])

---

## Existing idempotency key

```python
if idempotency_key in idempotency_store:
```

Checks if this operation was already processed.

```python
if saved_record["request_hash"] != request_hash:
```

Same key but different body means client made a mistake.

```python
raise HTTPException(status_code=409)
```

Returns conflict.

```python
return saved_record["response"]
```

Same key and same body means safe retry.

Return saved response.

---

## New request

```python
response = fake_llm_call(payload)
```

Call AI service.

```python
idempotency_store[idempotency_key] = {
    "request_hash": request_hash,
    "response": response,
}
```

Save result for future retries.

```python
generation_history.append(response)
```

Save generation to history.

```python
return response
```

Return API response.

---

## Line 15: GET list endpoint

```python
@app.get("/v1/generations", response_model=GenerationListResponse)
```

Defines list API.

```python
limit: int = Query(default=10, ge=1, le=100)
```

Validates `limit`.

Allowed:

```text
1 to 100
```

Rejected:

```text
0
-1
10000
```

```python
cursor: str | None = Query(default=None)
```

Optional cursor.

```python
start_index = 0
```

Default start from beginning.

```python
if cursor:
```

If cursor is provided, find it.

```python
start_index = index + 1
```

Start after cursor.

```python
selected_items = generation_history[start_index : start_index + limit]
```

Get one page.

```python
next_cursor = selected_items[-1].request_id
```

Set cursor for next page.

```python
return GenerationListResponse(...)
```

Return paginated response.

---

# 8. Common mistakes

## Mistake 1: No clear request schema

Bad:

```python
def create_generation(body: dict):
    prompt = body.get("prompt")
```

Good:

```python
def create_generation(payload: GenerateRequest):
    ...
```

Why?

```text
Schema gives validation
Schema gives documentation
Schema gives safer code
```

---

## Mistake 2: Making optional fields required later

Old contract:

```json
{
  "prompt": "hello"
}
```

New contract:

```json
{
  "prompt": "hello",
  "model": "required now"
}
```

This breaks old clients.

Better:

```python
model: str = "default-ai-model"
```

---

## Mistake 3: Reusing idempotency key for different request

Bad:

```text
Request 1:
Idempotency-Key: abc
prompt: "Summarize document A"

Request 2:
Idempotency-Key: abc
prompt: "Summarize document B"
```

Good:

```text
Different business operation = different idempotency key
```

---

## Mistake 4: Idempotency only in memory

Bad for production:

```python
idempotency_store = {}
```

Why bad?

```text
Server restart loses data
Multiple replicas do not share memory
Retry may hit another pod
Duplicates can happen
```

Production solution:

```text
Redis with TTL
Database table with unique constraint
Distributed lock if needed
```

---

## Mistake 5: Returning raw LLM response directly

Bad:

```json
{
  "choices": [
    {
      "message": {
        "content": "answer"
      }
    }
  ]
}
```

Better for your API:

```json
{
  "request_id": "req_123",
  "status": "completed",
  "answer": "answer",
  "usage": {
    "total_tokens": 100
  }
}
```

Why?

```text
Your API contract should hide vendor-specific response shape.
```

---

## Mistake 6: Poor error format

Bad:

```json
{
  "error": "Something wrong"
}
```

Good:

```json
{
  "code": "INVALID_PROMPT",
  "message": "Prompt must not be blank."
}
```

---

## Mistake 7: No pagination

Bad:

```python
return all_generations
```

Good:

```python
return page_of_generations
```

Large systems must protect database, memory, network, and latency.

---

# 9. Interview relevance

## For SDE backend roles

You should be able to explain:

```text
How to design request/response schemas
How validation protects business logic
How to choose status codes
How to prevent duplicate writes
How to design pagination
How to avoid breaking clients
```

Good interview phrase:

> I would define strict request and response contracts using Pydantic models, reject unknown or invalid fields, use standardized error responses, and protect write endpoints with idempotency keys.

---

## For AI platform roles

You should connect API contracts to AI workflow reliability:

```text
Prompt validation controls cost
max_tokens controls latency
temperature controls output behavior
usage response supports billing
request_id supports tracing
idempotency prevents duplicate LLM jobs
pagination supports chat/job history
```

Good interview phrase:

> For GenAI APIs, contracts are not only about JSON shape. They also control cost, safety, latency, retry behavior, and observability.

---

## For Solution Architect roles

You should discuss platform-level design:

```text
API gateway
Authentication
Rate limiting
Schema validation
OpenAPI documentation
Versioning
Backward compatibility
Observability
Idempotency store
Audit logs
```

Good interview phrase:

> I would expose a stable API contract through an API gateway, enforce validation at the boundary, maintain versioned OpenAPI specs, and use compatibility tests before deployment.

---

## For TPM roles

You should focus on coordination:

```text
Align frontend, backend, ML, infra, and customer teams
Define API versioning process
Track breaking changes
Plan migration windows
Maintain deprecation policy
Create rollout and rollback plan
```

Good TPM phrase:

> I would ensure API changes go through contract review, client impact analysis, backward compatibility checks, and a clear deprecation timeline.

---

# 10. DSA topic: HashMap / Dictionary

## 10.1 Beginner explanation

A HashMap stores data as key-value pairs.

Python:

```python
user_scores = {
    "Amit": 90,
    "Riya": 95
}
```

Go:

```go
userScores := map[string]int{
    "Amit": 90,
    "Riya": 95,
}
```

Think of it like a locker system:

```text
Key:   locker number
Value: item inside locker
```

Example:

```text
Key:   "user_123"
Value: "Ravi"
```

---

## 10.2 Why HashMap is important

HashMap gives fast lookup.

Without HashMap:

```text
Search in list one by one
Time: O(n)
```

With HashMap:

```text
Direct lookup by key
Average time: O(1)
```

Example:

```python
users = {
    "u1": "Ravi",
    "u2": "Amit"
}

print(users["u2"])
```

Directly returns:

```text
Amit
```

---

## 10.3 HashMap operations and Big-O

```text
Insert key-value       O(1) average
Search by key          O(1) average
Delete by key          O(1) average
Loop over all items    O(n)
```

Worst case can be O(n), but in interviews we usually say average O(1).

---

## 10.4 Common HashMap patterns

## Pattern 1: Frequency count

Used when counting occurrences.

Example:

```text
Input:  ["apple", "banana", "apple"]
Output: apple -> 2, banana -> 1
```

Python:

```python
freq = {}

for word in words:
    freq[word] = freq.get(word, 0) + 1
```

Go:

```go
freq := make(map[string]int)

for _, word := range words {
    freq[word]++
}
```

---

## Pattern 2: Seen set

Used to detect duplicates.

Python:

```python
seen = set()

for x in nums:
    if x in seen:
        return true
    seen.add(x)
```

Go:

```go
seen := make(map[int]bool)

for _, x := range nums {
    if seen[x] {
        return true
    }
    seen[x] = true
}
```

---

## Pattern 3: Index lookup

Used in Two Sum.

```text
Need: target - current
Store: number -> index
```

---

## Pattern 4: Grouping

Example: group words by first letter.

```text
apple, ant -> a
banana, bat -> b
```

Map type:

```go
map[string][]string
```

---

# 11. One hashmap practice question with Golang solution

## Problem: First non-repeating character

Given a string, return the first character that appears only once.

Example:

```text
Input:  "leetcode"
Output: "l"
```

Example:

```text
Input:  "aabbcdd"
Output: "c"
```

Example:

```text
Input:  "aabb"
Output: ""
```

---

## Brute-force thinking

For each character:

```text
Count how many times it appears by scanning the full string.
If count is 1, return it.
```

Pseudocode:

```text
FOR each character i in string:
    count = 0

    FOR each character j in string:
        IF character i == character j:
            count++

    IF count == 1:
        RETURN character i

RETURN empty string
```

Time complexity:

```text
O(n²)
```

Space complexity:

```text
O(1)
```

Why bad?

```text
For every character, we scan the full string again.
```

---

## Optimized thinking using HashMap

Use two passes.

Pass 1:

```text
Count frequency of every character.
```

Pass 2:

```text
Find first character with frequency 1.
```

Time complexity:

```text
O(n)
```

Space complexity:

```text
O(k)
```

Where `k` is number of unique characters.

---

## Golang solution

```go
package main

import "fmt"

func firstNonRepeatingChar(s string) string {
	freq := make(map[rune]int)

	for _, ch := range s {
		freq[ch]++
	}

	for _, ch := range s {
		if freq[ch] == 1 {
			return string(ch)
		}
	}

	return ""
}

func main() {
	fmt.Println(firstNonRepeatingChar("leetcode")) // l
	fmt.Println(firstNonRepeatingChar("aabbcdd"))  // c
	fmt.Println(firstNonRepeatingChar("aabb"))     // empty string
}
```

---

## Go explanation compared with Python

Python:

```python
freq = {}
for ch in s:
    freq[ch] = freq.get(ch, 0) + 1
```

Go:

```go
freq := make(map[rune]int)
for _, ch := range s {
    freq[ch]++
}
```

Important Go points:

```text
map[rune]int means key is character, value is count
rune handles Unicode characters better than byte
range over string gives index and rune
_ ignores the index
freq[ch]++ increments count
string(ch) converts rune back to string
```

Python equivalent:

```python
def first_non_repeating_char(s):
    freq = {}

    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    for ch in s:
        if freq[ch] == 1:
            return ch

    return ""
```

---

# 12. Short revision sheet

```text
API contract:
Agreement between client and server.

Request schema:
What client sends.

Response schema:
What server returns.

Required field:
Must be provided.

Optional field:
Can be missing because backend has default or can handle null.

Pydantic:
Python library for defining and validating data models.

Validation error:
Client sent invalid data.

Idempotency key:
Unique key used to safely retry write requests.

Pagination:
Return records page by page.

Backward compatibility:
Old clients should continue working after API changes.

Breaking change:
A change that causes old clients to fail.

HashMap:
Key-value data structure with O(1) average lookup.
```

---

# 13. Day 3 interview answer template

Use this in interviews:

> For a production GenAI API, I would first define a clear API contract using request and response schemas. I would validate inputs using Pydantic so invalid prompts, token limits, or unsupported values are rejected before calling the AI model. For write APIs, I would require an idempotency key so retries do not create duplicate jobs or duplicate charges. I would return standardized errors, include request IDs for debugging, support pagination for history endpoints, and maintain backward compatibility through versioned APIs and contract tests.

[1]: https://fastapi.tiangolo.com/tutorial/response-model/?utm_source=chatgpt.com "Response Model - Return Type"
[2]: https://pydantic.dev/docs/validation/latest/concepts/models/ "Models | Pydantic Docs"
[3]: https://pydantic.dev/docs/validation/latest/get-started/ "Welcome to Pydantic | Pydantic Docs"
[4]: https://fastapi.tiangolo.com/tutorial/body-fields/ "Body - Fields - FastAPI"
[5]: https://fastapi.tiangolo.com/tutorial/handling-errors/?utm_source=chatgpt.com "Handling Errors"
[6]: https://docs.stripe.com/api/idempotent_requests "docs.stripe.com"
[7]: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design "Web API Design Best Practices - Azure Architecture Center | Microsoft Learn"
[8]: https://fastapi.tiangolo.com/reference/status/?utm_source=chatgpt.com "Status Codes"
[9]: https://pydantic.dev/docs/validation/latest/concepts/validators/ "Validators | Pydantic Docs"
[10]: https://fastapi.tiangolo.com/tutorial/response-status-code/?utm_source=chatgpt.com "Response Status Code"
[11]: https://fastapi.tiangolo.com/reference/exceptions/?utm_source=chatgpt.com "Exceptions - HTTPException and WebSocketException - FastAPI"
--
You move to a different page by changing the pagination parameter in the API request.

There are two common styles:

---

# 1. Offset pagination

Formula:

```text
offset = (page_number - 1) * limit
```

Example: `limit = 20`

## Page 1

```http
GET /items?offset=0&limit=20
```

Returns items:

```text
1 to 20
```

## Page 2

```http
GET /items?offset=20&limit=20
```

Returns items:

```text
21 to 40
```

## Page 3

```http
GET /items?offset=40&limit=20
```

Returns items:

```text
41 to 60
```

So:

```text
Page 1: offset = 0
Page 2: offset = 20
Page 3: offset = 40
Page 4: offset = 60
```

Python/FastAPI example:

```python
@app.get("/items")
def list_items(offset: int = 0, limit: int = 20):
    return items[offset : offset + limit]
```

---

# 2. Cursor pagination

In cursor pagination, the client does **not calculate page numbers**.

Instead, server returns a `next_cursor`.

## First request

```http
GET /items?limit=20
```

Response:

```json
{
  "items": [
    {"id": "req_1"},
    {"id": "req_2"},
    {"id": "req_20"}
  ],
  "next_cursor": "req_20"
}
```

To get the next page, use that cursor.

## Second request

```http
GET /items?cursor=req_20&limit=20
```

Response:

```json
{
  "items": [
    {"id": "req_21"},
    {"id": "req_22"},
    {"id": "req_40"}
  ],
  "next_cursor": "req_40"
}
```

## Third request

```http
GET /items?cursor=req_40&limit=20
```

Response:

```json
{
  "items": [
    {"id": "req_41"},
    {"id": "req_42"},
    {"id": "req_60"}
  ],
  "next_cursor": "req_60"
}
```

So in cursor pagination:

```text
Page 1: no cursor
Page 2: use next_cursor from page 1
Page 3: use next_cursor from page 2
Page 4: use next_cursor from page 3
```

---

# Easy memory trick

## Offset pagination

You say:

```text
Give me records starting from number 20.
```

Example:

```http
GET /items?offset=20&limit=20
```

## Cursor pagination

You say:

```text
Give me records after this last item.
```

Example:

```http
GET /items?cursor=req_20&limit=20
```

---

# Which one is better?

For small admin tables:

```text
Offset pagination is simple.
```

For large production systems:

```text
Cursor pagination is better.
```

Why cursor is better?

```text
Faster for large datasets
Works better when new records are inserted
Good for chat history, logs, AI generations, transactions
```

---

# Real GenAI example

Suppose user has AI generation history.

## Page 1

```http
GET /v1/generations?limit=2
```

Response:

```json
{
  "items": [
    {"request_id": "req_101", "prompt": "Explain RAG"},
    {"request_id": "req_102", "prompt": "Summarize PDF"}
  ],
  "next_cursor": "req_102"
}
```

## Page 2

```http
GET /v1/generations?cursor=req_102&limit=2
```

Response:

```json
{
  "items": [
    {"request_id": "req_103", "prompt": "Write email"},
    {"request_id": "req_104", "prompt": "Generate quiz"}
  ],
  "next_cursor": "req_104"
}
```

## Page 3

```http
GET /v1/generations?cursor=req_104&limit=2
```

---

# Interview answer

Say this:

> In offset pagination, the client moves to another page by changing the offset. For example, with limit 20, page 1 uses offset 0, page 2 uses offset 20, and page 3 uses offset 40. In cursor pagination, the client does not calculate page numbers. The server returns a `next_cursor`, and the client passes that cursor in the next request to fetch the next page. Cursor pagination is preferred for large production systems because it is more stable and efficient.
