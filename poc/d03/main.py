from __future__ import annotations

# hashlib: creates SHA-256 hashes so we can compare request bodies safely.
import hashlib
# json: converts validated request data into a stable string before hashing.
import json
# uuid: creates unique request ids for new generation responses.
import uuid
# Literal: restricts status fields to specific allowed string values.
from typing import Literal

# FastAPI tools:
# - FastAPI creates the web app and route decorators.
# - Header reads HTTP headers such as Idempotency-Key.
# - HTTPException returns structured API errors.
# - Query validates query parameters such as limit and cursor.
# - status provides named HTTP status codes instead of raw numbers.
from fastapi import FastAPI, Header, HTTPException, Query, status
# Pydantic tools:
# - BaseModel defines request/response schemas.
# - ConfigDict configures model behavior.
# - Field adds validation rules and defaults.
# - field_validator adds custom validation logic.
from pydantic import BaseModel, ConfigDict, Field, field_validator

# This file implements a small GenAI-style API:
# 1. POST /v1/generations validates input, enforces idempotency, and creates a response.
# 2. GET /v1/generations lists previous responses with cursor-based pagination.

# App metadata appears in the automatically generated OpenAPI docs.
app = FastAPI(title="Production GenAI API", version="1.0.0")


class Usage(BaseModel):
    """Purpose: describe token usage for a generated answer."""

    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)


class GenerateRequest(BaseModel):
    """Purpose: define and validate the JSON body accepted by POST /v1/generations."""

    # Reject unknown fields so clients cannot accidentally send unsupported data.
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
        """Purpose: prevent prompts that contain only spaces or line breaks."""

        # Field(min_length=1) allows whitespace, so trim and reject blank prompts.
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("prompt must not be blank")
        return cleaned


class GenerateResponse(BaseModel):
    """Purpose: define the successful response shape for a generation request."""

    request_id: str
    status: Literal["completed"]
    answer: str
    model: str
    usage: Usage


class GenerationListItem(BaseModel):
    """Purpose: provide a smaller history item for list responses."""

    request_id: str
    status: Literal["completed"]
    model: str


class GenerationListResponse(BaseModel):
    """Purpose: wrap list results and the cursor for the next page."""

    items: list[GenerationListItem]
    next_cursor: str | None = None


class ErrorResponse(BaseModel):
    """Purpose: document the expected error format in OpenAPI docs."""

    code: str
    message: str

# In-memory stores keep this proof of concept simple.
# A real production service would use durable storage such as Redis/Postgres.
idempotency_store: dict[str, dict] = {}
generation_history: list[GenerateResponse] = []


def create_request_hash(payload: GenerateRequest) -> str:
    """Purpose: create a stable fingerprint for detecting idempotency-key misuse."""

    # Sorting keys makes the hash stable even if dict fields arrive in a different order.
    stable_json = json.dumps(payload.model_dump(mode="json"), sort_keys=True)
    return hashlib.sha256(stable_json.encode("utf-8")).hexdigest()


def fake_llm_call(payload: GenerateRequest) -> GenerateResponse:
    """Purpose: simulate an LLM provider call while preserving the real response shape."""

    # This intentionally simple token estimate makes the example deterministic.
    words = payload.prompt.split()
    prompt_tokens = len(words)

    # In a real service, this is where the external model response would be used.
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
    """Purpose: create a generation while making client retries safe through idempotency."""

    # Require an idempotency key so clients can safely retry the same request.
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "MISSING_IDEMPOTENCY_KEY",
                "message": "Idempotency-Key header is required.",
            },
        )

    request_hash = create_request_hash(payload)

    # If this key was already used, return the original response for the same body.
    # Reusing the key with different input is blocked to prevent accidental overwrites.
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

    # First time seeing this idempotency key: perform the generation.
    response = fake_llm_call(payload)

    # Store both the request fingerprint and response so an identical retry is stable.
    idempotency_store[idempotency_key] = {
        "request_hash": request_hash,
        "response": response,
    }

    # Keep a simple history so the GET endpoint can list generated requests.
    generation_history.append(response)

    return response


@app.get("/v1/generations", response_model=GenerationListResponse)
def list_generations(
    limit: int = Query(default=10, ge=1, le=100),
    cursor: str | None = Query(default=None),
) -> GenerationListResponse:
    """Purpose: return generated requests using cursor-based pagination."""

    start_index = 0

    # The cursor is the last request_id the client saw; resume after that item.
    if cursor:
        for index, item in enumerate(generation_history):
            if item.request_id == cursor:
                start_index = index + 1
                break

    selected_items = generation_history[start_index : start_index + limit]

    # Expose a next cursor only when more records exist after this page.
    next_cursor = None
    if start_index + limit < len(generation_history):
        next_cursor = selected_items[-1].request_id

    return GenerationListResponse(
        # Convert full responses into compact list items for this endpoint.
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
