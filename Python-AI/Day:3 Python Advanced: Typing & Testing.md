# Day 3 – Python Advanced: Typing, Validation, Errors & Testing

## 1. The production mental model

In a production GenAI system, these four topics solve different problems:

| Technique              | Main question it answers                                 | When it works                   |
| ---------------------- | -------------------------------------------------------- | ------------------------------- |
| Type hints             | “What kind of data should this code receive and return?” | Development and static analysis |
| Pydantic validation    | “Is this runtime input actually valid?”                  | Runtime                         |
| Exceptions and logging | “What failed, why, and can we recover?”                  | Runtime and operations          |
| Testing                | “Does the system behave correctly after changes?”        | Development and CI/CD           |

A useful rule is:

> **Use type hints inside your application, Pydantic at system boundaries, domain exceptions for failures, structured logs for diagnosis, and tests around all important behavior.**

---

# 2. Type hints and static typing

## 2.1 What are type hints?

Python is dynamically typed. This means the following code is syntactically valid:

```python
def create_embedding(text):
    return text
```

Nothing tells another developer:

* Whether `text` should be a string or a list.
* Whether the function returns a vector, string, dictionary, or `None`.
* Whether empty text is allowed.

With type hints:

```python
def create_embedding(text: str) -> list[float]:
    return [0.12, 0.45, 0.91]
```

The contract is clearer:

* Input: one string.
* Output: a list of floating-point values.

Python itself generally does not enforce function and variable annotations at runtime. They are mainly consumed by static type checkers, IDEs, linters, and related development tools. ([Python documentation][1])

## 2.2 Static typing versus runtime validation

Consider:

```python
def calculate_cost(tokens: int) -> float:
    return tokens * 0.00001


# Python may still execute this call.
calculate_cost("1000")
```

The type hint says `tokens` should be an `int`, but Python does not automatically reject `"1000"` before entering the function.

A static checker such as `mypy` can detect this problem before the program runs:

```text
Argument 1 to "calculate_cost" has incompatible type "str";
expected "int"
```

Pydantic, on the other hand, performs runtime validation:

```python
from pydantic import BaseModel


class UsageRecord(BaseModel):
    tokens: int


record = UsageRecord(tokens="invalid")
# Raises a Pydantic ValidationError at runtime.
```

Therefore:

* **Type hints** protect developers from incorrect code usage.
* **Pydantic** protects the application from incorrect runtime data.

---

## 2.3 Important types from the `typing` module

### `List`

`List[T]` means a list whose elements are expected to be of type `T`.

```python
from typing import List


def embed_documents(documents: List[str]) -> List[List[float]]:
    """
    Each input document is a string.
    Each document produces one embedding, represented as a list of floats.
    """
    return [[0.1, 0.2, 0.3] for _ in documents]
```

Interpretation:

```text
List[str]
└── List containing strings

List[List[float]]
└── List of embeddings
    └── Each embedding is a list of floats
```

In modern Python, built-in generic syntax is normally preferred:

```python
def embed_documents(documents: list[str]) -> list[list[float]]:
    ...
```

You will still see `List`, `Dict`, and other `typing` forms in older or compatibility-focused codebases.

---

### `Dict`

`Dict[K, V]` describes a dictionary containing keys of type `K` and values of type `V`.

```python
from typing import Dict


def count_tokens_by_document(
    documents: List[str],
) -> Dict[str, int]:
    """
    The key is a document identifier.
    The value is that document's token count.
    """
    return {
        "document-1": 824,
        "document-2": 1_240,
    }
```

Modern equivalent:

```python
def count_tokens_by_document(
    documents: list[str],
) -> dict[str, int]:
    ...
```

A plain `dict[str, object]` is useful for flexible data, but it becomes difficult to understand as systems grow:

```python
def process_result(result: dict[str, object]) -> None:
    ...
```

Questions immediately arise:

* Which keys must exist?
* Which keys are optional?
* What type is each value?
* Is `"score"` a `float`, string, or integer?
* Can the dictionary contain additional keys?

For a dictionary with a known structure, use `TypedDict` or Pydantic.

---

### `Optional`

`Optional[T]` means:

```python
T or None
```

For example:

```python
from typing import Optional


def find_cached_answer(question: str) -> Optional[str]:
    cached_value = None

    if cached_value is not None:
        return cached_value

    return None
```

Modern syntax:

```python
def find_cached_answer(question: str) -> str | None:
    ...
```

A common interview trap is to say that `Optional` means an argument is optional. It does not.

```python
def generate_answer(model: Optional[str]) -> str:
    ...
```

The caller must still pass `model`; the value can simply be either a string or `None`.

By contrast:

```python
def generate_answer(model: str = "default-model") -> str:
    ...
```

The caller may omit the argument, but the value is always expected to be a string.

`Optional[X]` is equivalent to `X | None` or `Union[X, None]`. ([Python documentation][1])

---

### `Union`

`Union[A, B]` means the value can be either type `A` or type `B`.

```python
from typing import Union


def normalize_document(
    document: Union[str, bytes],
) -> str:
    """
    The ingestion layer may receive text or raw bytes.
    Internally, the system normalizes both to a string.
    """
    if isinstance(document, bytes):
        return document.decode("utf-8")

    return document
```

Modern syntax:

```python
def normalize_document(document: str | bytes) -> str:
    ...
```

A union is helpful when the alternatives are genuinely meaningful. Avoid extremely broad unions:

```python
# Difficult to reason about and maintain.
def process_input(
    value: str | bytes | dict | list | int | None,
) -> object:
    ...
```

At that point, the function probably has too many responsibilities.

`Union[X, Y]` and `X | Y` both describe either `X` or `Y`; current Python documentation recommends the shorter union syntax in supported Python versions. ([Python documentation][1])

---

### `TypedDict`

`TypedDict` describes the expected structure of a dictionary.

```python
from typing import TypedDict


class RetrievedChunk(TypedDict):
    chunk_id: str
    text: str
    similarity_score: float
    source: str


def retrieve_chunks(question: str) -> list[RetrievedChunk]:
    return [
        {
            "chunk_id": "chunk-101",
            "text": "The refund policy allows...",
            "similarity_score": 0.91,
            "source": "refund-policy.pdf",
        }
    ]
```

Static type checkers can detect problems such as:

```python
chunk: RetrievedChunk = {
    "chunk_id": "chunk-101",
    "text": "Example",
    "similarity_score": "high",  # Type error: expected float
    # Missing source
}
```

Optional keys can be represented with `NotRequired`:

```python
from typing import NotRequired, TypedDict


class RetrievedChunk(TypedDict):
    chunk_id: str
    text: str
    similarity_score: float
    source: str
    page_number: NotRequired[int]
```

By default, `TypedDict` keys are required, while `NotRequired` or `total=False` can represent keys that may be omitted. ([Python documentation][1])

### Important limitation

`TypedDict` provides static checking. It does not validate an external dictionary at runtime.

```python
bad_data = {
    "chunk_id": 123,
    "text": None,
    "similarity_score": "excellent",
}

# No automatic runtime validation happens merely because this
# variable is annotated as RetrievedChunk.
chunk: RetrievedChunk = bad_data
```

Use `TypedDict` when:

* The dictionary is internal and already trusted.
* You want low-overhead type documentation.
* You need interoperability with existing dictionary-based code.

Use Pydantic when:

* Data comes from an API.
* Data comes from an LLM.
* Data comes from a queue, file, database, or user.
* Runtime rejection of invalid data is required.

---

## 2.4 Benefits of typing in large AI systems

### Safer refactoring

Suppose an embedding interface changes from:

```python
def embed(text: str) -> list[float]:
    ...
```

to:

```python
def embed(texts: list[str]) -> list[list[float]]:
    ...
```

A static checker can identify callers still passing one string.

Without typing, the failure may appear only:

* During production traffic.
* In a rarely used ingestion job.
* For one particular model provider.
* After a batch has run for several hours.

### Better IDE support

Type hints let an IDE understand:

* Available methods.
* Return types.
* Required arguments.
* Invalid assignments.
* Possible `None` values.

This is especially useful in large RAG or agent codebases with many interacting components.

### Clearer interfaces

Compare:

```python
def execute(data):
    ...
```

with:

```python
def execute(
    request: ToolRequest,
    context: ExecutionContext,
) -> ToolResult:
    ...
```

The second version communicates substantially more design information.

### Better provider abstractions

```python
from typing import Protocol


class LLMProvider(Protocol):
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        ...


class AnswerService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    def answer(self, question: str) -> str:
        prompt = f"Answer this question: {question}"
        return self._provider.generate(prompt)
```

`AnswerService` does not depend directly on OpenAI, IBM, Azure, or another implementation. Any object satisfying the required interface can be used.

This improves:

* Provider replacement.
* Unit testing.
* Dependency injection.
* Separation of business logic from SDK code.

---

## 2.5 Using `mypy`

`mypy` is a static type checker. It analyzes type hints and reports incompatible usage without needing to execute the application. ([mypy.readthedocs.io][2])

Typical command:

```bash
mypy src/
```

Example:

```python
def build_prompt(question: str) -> str:
    return f"Question: {question}"


build_prompt(100)
```

Possible `mypy` result:

```text
Argument 1 to "build_prompt" has incompatible type "int";
expected "str"
```

A basic `pyproject.toml` configuration might look like:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true
show_error_codes = true
```

### Practical adoption strategy

Do not necessarily enable the strictest configuration across a ten-year-old codebase on the first day.

A safer migration strategy is:

1. Type public interfaces and new modules first.
2. Type API, database, model-provider, and queue boundaries.
3. Add typing to important domain models.
4. Enable stricter rules module by module.
5. Prevent new untyped code through CI.
6. Gradually reduce existing type errors.

### Typing pitfalls

#### Excessive use of `Any`

```python
from typing import Any


def call_model(payload: Any) -> Any:
    ...
```

`Any` effectively tells the type checker:

> Do not protect this part of the program.

Sometimes it is necessary when dealing with a poorly typed SDK, but it should be isolated at the integration boundary.

#### Incorrectly assuming hints validate data

```python
def ingest_document(text: str) -> None:
    ...
```

This does not prevent a caller from passing `None` at runtime.

#### Ignoring `None`

```python
def lookup_model(name: str) -> str | None:
    ...


model_id = lookup_model("chat-model")
print(model_id.upper())  # Unsafe: model_id might be None
```

Correct:

```python
model_id = lookup_model("chat-model")

if model_id is None:
    raise ValueError("Model was not found")

print(model_id.upper())
```

#### Overly complicated types

A type that takes ten lines to understand may indicate an overcomplicated design. Consider introducing a named class or Pydantic model.

---

# 3. Data validation with Pydantic

## 3.1 Why runtime validation matters

External data cannot be trusted merely because it is supposed to follow a schema.

In an AI system, invalid data can come from:

* API clients.
* LLM-generated JSON.
* Tool calls.
* Environment variables.
* Configuration files.
* Message queues.
* Databases with older schemas.
* Third-party providers.
* Document metadata pipelines.

Pydantic models inherit from `BaseModel` and define fields through Python annotations. Model creation performs parsing and validation, and the resulting model conforms to its declared field definitions when validation succeeds. ([Pydantic Docs][3])

---

## 3.2 Basic Pydantic model

```python
from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    # Reject unknown fields rather than silently accepting schema mistakes.
    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        min_length=1,
        max_length=4_000,
    )
    session_id: str
    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
    )
    include_citations: bool = True
```

Valid input:

```python
request = ChatRequest(
    question="What is the refund policy?",
    session_id="session-123",
    top_k=8,
)

print(request.question)
print(request.model_dump())
```

Invalid input:

```python
ChatRequest(
    question="",
    session_id="session-123",
    top_k=500,
)
```

This fails because:

* The question is empty.
* `top_k` exceeds the upper limit.

---

## 3.3 Type coercion versus strict validation

By default, Pydantic may convert compatible input values:

```python
class SearchRequest(BaseModel):
    top_k: int


request = SearchRequest(top_k="5")

assert request.top_k == 5
assert isinstance(request.top_k, int)
```

This is convenient for HTTP or environment inputs, but it can hide certain producer errors.

Strict mode can be used when conversion is undesirable:

```python
from pydantic import BaseModel, ConfigDict


class StrictSearchRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    top_k: int
```

Pydantic supports both coercive behavior and strict validation; strict mode requires values to match declared types instead of relying on normal conversion. ([Pydantic Docs][3])

### Senior-level decision

Use coercion when:

* Inputs naturally arrive as strings.
* Conversion is unambiguous.
* User convenience matters.

Use strict validation when:

* The schema is a machine-to-machine contract.
* Silent conversion could hide an integration bug.
* Tool or agent actions have financial or security impact.
* Exact types matter.

---

## 3.4 Custom field validation

Suppose an LLM tool accepts a search query:

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator


class KnowledgeSearchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=1_000)
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("query")
    @classmethod
    def query_must_contain_real_text(cls, value: str) -> str:
        # Normalize whitespace before storing the value.
        normalized = value.strip()

        # A string containing only spaces technically has length,
        # but it is not a useful search query.
        if not normalized:
            raise ValueError("query cannot contain only whitespace")

        return normalized
```

Now:

```python
KnowledgeSearchInput(
    query="   ",
    top_k=5,
)
```

raises a validation error.

---

## 3.5 Cross-field validation

Some rules involve more than one field.

For example:

* `end_date` must be after `start_date`.
* A streaming request cannot request a synchronous output format.
* A tool call requires approval when its risk level is high.

```python
from pydantic import BaseModel, model_validator


class GenerationConfig(BaseModel):
    stream: bool = False
    response_format: str = "text"

    @model_validator(mode="after")
    def validate_streaming_format(self) -> "GenerationConfig":
        # Assume this application does not support streaming JSON objects.
        if self.stream and self.response_format == "json":
            raise ValueError(
                "stream=True is not supported with response_format='json'"
            )

        return self
```

---

## 3.6 Pydantic for API schemas

```python
class Citation(BaseModel):
    document_id: str
    page_number: int | None = None
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    request_id: str
    model_name: str
```

Benefits:

* Clear API contract.
* Automatic serialization.
* Nested validation.
* Easier generation of JSON Schema.
* Fewer malformed responses.

---

## 3.7 Pydantic for LLM tool input and output

LLM-generated tool arguments should always be treated as untrusted input.

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CreateSupportTicketInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=5, max_length=150)
    description: str = Field(min_length=10, max_length=5_000)
    priority: Literal["low", "medium", "high"]
    customer_id: str
```

Execution flow:

```text
LLM proposes tool arguments
          |
          v
Pydantic validates arguments
          |
     +----+----+
     |         |
   valid     invalid
     |         |
Execute tool   Return controlled error to agent
```

Never assume that structured-output mode makes downstream validation unnecessary. The application should still validate:

* Required fields.
* Allowed values.
* Length limits.
* Business rules.
* Authorization.
* Resource ownership.

Validation confirms that an input is structurally acceptable. It does **not** prove that an action is authorized or safe.

---

## 3.8 Pydantic for configuration objects

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RAGConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    embedding_provider: Literal["openai", "watsonx", "local"]
    embedding_model: str
    chunk_size: int = Field(ge=100, le=4_000)
    chunk_overlap: int = Field(ge=0, le=1_000)
    retrieval_top_k: int = Field(ge=1, le=100)
```

`frozen=True` helps prevent accidental runtime mutation:

```python
config = RAGConfig(
    embedding_provider="watsonx",
    embedding_model="example-embedding-model",
    chunk_size=800,
    chunk_overlap=100,
    retrieval_top_k=10,
)
```

A cross-field rule could ensure overlap is smaller than chunk size:

```python
class RAGConfig(BaseModel):
    chunk_size: int = Field(ge=100)
    chunk_overlap: int = Field(ge=0)

    @model_validator(mode="after")
    def check_chunk_overlap(self) -> "RAGConfig":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        return self
```

---

## 3.9 Pydantic pitfalls

### Silently ignoring unexpected fields

Pydantic models ignore extra fields by default unless configured otherwise. For strict external contracts, `ConfigDict(extra="forbid")` is often safer because misspelled or newly introduced fields fail immediately instead of disappearing silently. ([Pydantic Docs][3])

Example problem:

```python
payload = {
    "temperature": 0.2,
    "max_token": 500,  # Typo: expected max_tokens
}
```

If unknown fields are ignored, the application may quietly use a default value.

### Overusing validators

Do not hide complicated business logic inside dozens of validators.

Prefer:

* Pydantic for structural and local validation.
* A domain service for database-dependent or permission-dependent rules.

Bad:

```python
class TicketRequest(BaseModel):
    customer_id: str

    # Avoid performing network or database calls during basic model validation.
```

Better:

```python
request = TicketRequest.model_validate(raw_payload)
authorization_service.verify_customer_access(
    user_id=current_user.id,
    customer_id=request.customer_id,
)
```

### Using validation as authorization

A valid account ID does not mean the current user is permitted to access that account.

### Exposing raw validation details externally

Internal validation errors may contain:

* Input values.
* Internal field names.
* Implementation details.

Transform them into a stable public error format.

---

# 4. Error handling

## 4.1 What good error handling should accomplish

A production error strategy should answer:

1. What failed?
2. Which layer detected it?
3. Is it retryable?
4. Should the client see it?
5. What HTTP or RPC status should it map to?
6. What should be logged?
7. Should an alert be generated?

---

## 4.2 Custom exception hierarchy

Avoid using generic `Exception` or `ValueError` for every domain failure.

```python
class AIServiceError(Exception):
    """Base class for expected application-level AI failures."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str,
        retryable: bool = False,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.retryable = retryable


class ProviderUnavailableError(AIServiceError):
    """The external model provider could not serve the request."""


class InvalidModelResponseError(AIServiceError):
    """The provider returned a response that violated our contract."""


class RetrievalError(AIServiceError):
    """The retrieval subsystem failed."""


class DocumentValidationError(AIServiceError):
    """A document could not be safely ingested."""
```

Usage:

```python
def parse_model_response(raw_response: dict[str, object]) -> str:
    text = raw_response.get("text")

    if not isinstance(text, str) or not text.strip():
        raise InvalidModelResponseError(
            "Provider response did not contain valid text",
            error_code="INVALID_MODEL_RESPONSE",
            retryable=False,
        )

    return text
```

Benefits:

* Callers can catch specific failures.
* API layers can map errors consistently.
* Retry policies can use `retryable`.
* Monitoring can aggregate by `error_code`.
* Tests can verify domain behavior.

---

## 4.3 Translate infrastructure errors at boundaries

Provider SDK errors should not spread across the entire application.

```python
class ProviderClient:
    def generate(self, prompt: str) -> str:
        try:
            raw_response = self._send_request(prompt)

        except TimeoutError as exc:
            # Preserve the original exception as the cause.
            # This keeps the low-level traceback available for debugging.
            raise ProviderUnavailableError(
                "The model provider timed out",
                error_code="PROVIDER_TIMEOUT",
                retryable=True,
            ) from exc

        return parse_model_response(raw_response)

    def _send_request(self, prompt: str) -> dict[str, object]:
        ...
```

The service layer now understands a stable domain exception instead of provider-specific SDK classes.

This means changing providers does not require rewriting error handling across the application.

---

## 4.4 Catch narrow exceptions

Bad:

```python
try:
    answer = provider.generate(prompt)
except Exception:
    return "Something went wrong"
```

Problems:

* Programming bugs are hidden.
* `KeyboardInterrupt`-like operational concerns may be mishandled.
* No distinction between validation, timeout, authorization, and parsing.
* The original traceback may be lost.
* The system may return incorrect success responses.

Better:

```python
try:
    answer = provider.generate(prompt)

except ProviderUnavailableError:
    # An upper layer may retry or return a temporary failure.
    raise

except InvalidModelResponseError:
    # This is normally not solved by immediately retrying the same response.
    raise
```

At an application boundary, a broad handler can be appropriate as a final safety net:

```python
try:
    response = service.answer(request)
except AIServiceError as exc:
    return map_domain_error(exc)
except Exception:
    logger.exception("Unexpected unhandled failure")
    return internal_server_error()
```

---

## 4.5 Do not use exceptions for normal control flow

Bad:

```python
try:
    cached_answer = cache[question]
except KeyError:
    cached_answer = None
```

This is not always wrong, but ordinary “not found” behavior is often clearer as:

```python
cached_answer = cache.get(question)
```

Exceptions should primarily represent exceptional or failure conditions.

---

## 4.6 Preserve exception chaining

```python
try:
    parsed = json.loads(model_output)
except json.JSONDecodeError as exc:
    raise InvalidModelResponseError(
        "The LLM returned malformed JSON",
        error_code="MALFORMED_LLM_JSON",
    ) from exc
```

The `from exc` relationship preserves both:

* The domain-level explanation.
* The original low-level cause.

---

# 5. Logging best practices

## 5.1 Logging levels

### `DEBUG`

Detailed development and diagnostic information.

Examples:

* Number of chunks produced.
* Cache lookup decisions.
* Retrieval filter construction.
* Retry attempt numbers.

```python
logger.debug(
    "Chunking completed document_id=%s chunk_count=%s",
    document_id,
    len(chunks),
)
```

### `INFO`

Normal business or system events.

Examples:

* Request completed.
* Document ingested.
* Model selected.
* Tool executed successfully.

```python
logger.info(
    "RAG request completed request_id=%s model=%s",
    request_id,
    model_name,
)
```

### `WARNING`

Unexpected condition from which the system recovered.

Examples:

* Cache unavailable; continuing without cache.
* Primary provider failed; fallback provider used.
* Retry required.
* Document skipped due to unsupported metadata.

```python
logger.warning(
    "Primary provider unavailable; using fallback provider"
)
```

### `ERROR`

An operation failed, but the process can continue.

```python
logger.error(
    "Document ingestion failed document_id=%s",
    document_id,
)
```

### `CRITICAL`

The service cannot perform an essential function.

Examples:

* Required configuration cannot be loaded.
* All model providers are unavailable.
* Encryption keys cannot be accessed.
* Database initialization failed.

---

## 5.2 Use module-level loggers

```python
import logging


logger = logging.getLogger(__name__)
```

This creates a meaningful logger hierarchy based on module names.

Avoid creating a unique logger for every request or customer. Python’s logging cookbook recommends attaching contextual information through mechanisms such as `LoggerAdapter`, filters, or context-local data rather than creating an unbounded number of loggers. ([Python documentation][4])

---

## 5.3 Prefer parameterized logging

Preferred:

```python
logger.info(
    "Calling provider provider=%s model=%s",
    provider_name,
    model_name,
)
```

Avoid:

```python
logger.info(
    f"Calling provider provider={provider_name} model={model_name}"
)
```

Parameterized logging defers string formatting until the message is actually emitted.

---

## 5.4 Structured logging

A structured event should have machine-searchable fields:

```json
{
  "event": "llm_request_completed",
  "correlation_id": "req-98af",
  "provider": "watsonx",
  "model": "model-x",
  "latency_ms": 842,
  "input_tokens": 950,
  "output_tokens": 211,
  "status": "success"
}
```

This enables queries such as:

* Show all provider timeouts.
* Find requests exceeding two seconds.
* Calculate token usage per model.
* Trace one request across services.
* Compare failure rates between providers.

The standard `logging` package can be combined with a JSON formatter or an observability platform to emit structured events.

---

## 5.5 Correlation IDs

A correlation ID identifies one request or workflow across multiple components.

```text
API gateway
  correlation_id=req-123
        |
        v
RAG service
  correlation_id=req-123
        |
        +--> Vector database
        |
        +--> Reranker
        |
        +--> LLM provider
```

Example with a logging filter:

```python
import logging
from contextvars import ContextVar


correlation_id_var: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-",
)


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Every record receives the current request's correlation ID.
        # ContextVar works appropriately with concurrent async tasks.
        record.correlation_id = correlation_id_var.get()
        return True


handler = logging.StreamHandler()
handler.addFilter(CorrelationIdFilter())

handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s "
        "correlation_id=%(correlation_id)s "
        "%(name)s %(message)s"
    )
)

logger = logging.getLogger("rag_service")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

At request entry:

```python
def handle_request(request_id: str) -> None:
    token = correlation_id_var.set(request_id)

    try:
        logger.info("Request processing started")
        # Execute retrieval and generation.
    finally:
        correlation_id_var.reset(token)
```

Python’s logging guidance documents `LoggerAdapter`, filters, and `contextvars` as mechanisms for adding request-specific context to log records. ([Python documentation][4])

---

## 5.6 Log exceptions correctly

Inside an exception handler:

```python
try:
    result = provider.generate(prompt)
except ProviderUnavailableError:
    logger.exception(
        "Provider request failed provider=%s",
        provider_name,
    )
    raise
```

`logger.exception()` records the traceback automatically.

Outside an exception handler, use `logger.error()` instead.

---

## 5.7 Do not log sensitive data

LLM systems can process sensitive information, including:

* Customer data.
* Employee records.
* Authentication tokens.
* Personal information.
* Proprietary documents.
* Entire user prompts.
* Retrieved document passages.

Bad:

```python
logger.info(
    "Calling LLM api_key=%s prompt=%s",
    api_key,
    full_prompt,
)
```

Better:

```python
logger.info(
    "Calling LLM provider=%s prompt_length=%s",
    provider_name,
    len(prompt),
)
```

Use:

* Redaction.
* Hashes where suitable.
* Document IDs rather than full text.
* Allowlisted metadata.
* Restricted debug logging.
* Appropriate retention policies.

---

## 5.8 Avoid duplicate logging

Suppose three layers all catch, log, and re-raise the same exception:

```text
Provider layer: ERROR timeout
Service layer: ERROR provider failure
API layer: ERROR request failed
```

One failure becomes three error events.

A good convention is:

* Lower layers add context by translating exceptions.
* The boundary responsible for handling or returning the failure logs it.
* Additional layers log only when they add meaningful operational information.

---

# 6. Testing patterns with `pytest`

## 6.1 Types of tests for AI systems

### Unit tests

Test one small component in isolation.

Examples:

* Prompt construction.
* Chunk-size logic.
* Citation formatting.
* Retry classification.
* Response parsing.
* Pydantic validation.

### Integration tests

Test interactions between real components.

Examples:

* Application and vector database.
* Application and test database.
* Embedding pipeline and index.
* API endpoint and service layer.

### Contract tests

Confirm an integration continues to follow an expected schema.

Examples:

* Provider response fields.
* Tool-call JSON structure.
* Queue event schema.
* Internal API response schema.

### End-to-end tests

Test a complete workflow.

```text
Upload document
    -> chunk
    -> embed
    -> index
    -> retrieve
    -> generate answer
    -> return citations
```

### LLM evaluation tests

Evaluate quality rather than ordinary deterministic correctness.

Examples:

* Groundedness.
* Retrieval relevance.
* Citation correctness.
* Refusal behavior.
* Safety.
* Answer completeness.

Do not treat all of these as ordinary unit tests. Model-quality evaluations normally require datasets, thresholds, and statistical interpretation.

---

## 6.2 Basic `pytest` test

Production code:

```python
def build_rag_prompt(
    question: str,
    contexts: list[str],
) -> str:
    joined_context = "\n\n".join(contexts)

    return (
        "Use only the supplied context.\n\n"
        f"Context:\n{joined_context}\n\n"
        f"Question: {question}"
    )
```

Test:

```python
def test_build_rag_prompt_includes_question_and_context() -> None:
    prompt = build_rag_prompt(
        question="What is the leave policy?",
        contexts=[
            "Employees receive 20 days of annual leave.",
            "Unused leave may be carried forward.",
        ],
    )

    assert "What is the leave policy?" in prompt
    assert "20 days of annual leave" in prompt
    assert "carried forward" in prompt
```

---

## 6.3 Fixtures

A fixture provides reusable setup and teardown.

Test functions request fixtures by declaring them as parameters. Pytest creates the fixture value and passes it into the test. Fixtures can also depend on other fixtures and can use scopes such as function, class, module, package, and session. ([pytest][5])

### Database fixture

```python
import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def db_connection(
    tmp_path: Path,
) -> Iterator[sqlite3.Connection]:
    """
    Give each test an isolated temporary database.

    Using a fresh database prevents tests from affecting one another.
    The yield separates setup from teardown.
    """
    database_path = tmp_path / "test.db"
    connection = sqlite3.connect(database_path)

    connection.execute(
        """
        CREATE TABLE documents (
            document_id TEXT PRIMARY KEY,
            content TEXT NOT NULL
        )
        """
    )

    yield connection

    # Teardown runs even when the test fails.
    connection.close()
```

Test:

```python
def test_document_can_be_stored(
    db_connection: sqlite3.Connection,
) -> None:
    db_connection.execute(
        "INSERT INTO documents VALUES (?, ?)",
        ("doc-1", "Example policy text"),
    )

    row = db_connection.execute(
        "SELECT content FROM documents WHERE document_id = ?",
        ("doc-1",),
    ).fetchone()

    assert row == ("Example policy text",)
```

---

## 6.4 LLM mock or fake fixture

First define an interface:

```python
from typing import Protocol


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

Production service:

```python
class AnswerService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    def answer(self, question: str) -> str:
        prompt = f"Answer using company policy: {question}"
        return self._provider.generate(prompt)
```

Fake provider:

```python
class FakeLLMProvider:
    """
    A deterministic fake is often easier to understand than a heavily
    configured mock.

    It records prompts so tests can inspect how it was called.
    """

    def __init__(self, response: str) -> None:
        self.response = response
        self.received_prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.received_prompts.append(prompt)
        return self.response
```

Fixture:

```python
@pytest.fixture
def fake_llm() -> FakeLLMProvider:
    return FakeLLMProvider(
        response="Employees receive 20 days of annual leave."
    )
```

Test:

```python
def test_answer_service_calls_llm_with_question(
    fake_llm: FakeLLMProvider,
) -> None:
    service = AnswerService(fake_llm)

    answer = service.answer("How much annual leave do I receive?")

    assert answer == "Employees receive 20 days of annual leave."
    assert len(fake_llm.received_prompts) == 1
    assert "How much annual leave" in fake_llm.received_prompts[0]
```

Why this is valuable:

* No network call.
* No API cost.
* No rate limit.
* No random provider response.
* Fast and deterministic.
* The test focuses on your application logic.

---

## 6.5 Mocking an external provider

Production client:

```python
class ExternalLLMClient:
    def generate(self, prompt: str) -> str:
        try:
            raw_response = self._send_request(
                {"prompt": prompt}
            )
        except TimeoutError as exc:
            raise ProviderUnavailableError(
                "Provider timed out",
                error_code="PROVIDER_TIMEOUT",
                retryable=True,
            ) from exc

        text = raw_response.get("text")

        if not isinstance(text, str):
            raise InvalidModelResponseError(
                "Missing text in provider response",
                error_code="INVALID_PROVIDER_RESPONSE",
            )

        return text

    def _send_request(
        self,
        payload: dict[str, object],
    ) -> dict[str, object]:
        # Real HTTP request would happen here.
        ...
```

Successful response test:

```python
def test_generate_returns_provider_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = ExternalLLMClient()

    def fake_send_request(
        payload: dict[str, object],
    ) -> dict[str, object]:
        # Check that the integration builds the correct outbound payload.
        assert payload["prompt"] == "Explain RAG"
        return {"text": "RAG combines retrieval and generation."}

    monkeypatch.setattr(
        client,
        "_send_request",
        fake_send_request,
    )

    result = client.generate("Explain RAG")

    assert result == "RAG combines retrieval and generation."
```

Timeout test:

```python
def test_timeout_is_translated_to_domain_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = ExternalLLMClient()

    def fake_timeout(
        payload: dict[str, object],
    ) -> dict[str, object]:
        raise TimeoutError("Network timed out")

    monkeypatch.setattr(
        client,
        "_send_request",
        fake_timeout,
    )

    with pytest.raises(ProviderUnavailableError) as exc_info:
        client.generate("Explain RAG")

    assert exc_info.value.error_code == "PROVIDER_TIMEOUT"
    assert exc_info.value.retryable is True
```

Pytest’s `monkeypatch` fixture can temporarily replace attributes, dictionary values, environment variables, and related process state, restoring the original state after the test. ([pytest][6])

---

## 6.6 Testing Pydantic validation

```python
from pydantic import ValidationError


def test_chat_request_rejects_excessive_top_k() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(
            question="What is the policy?",
            session_id="session-1",
            top_k=1_000,
        )


def test_chat_request_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(
            question="What is the policy?",
            session_id="session-1",
            top_k=5,
            unexpected_setting=True,
        )
```

Test both:

* Valid examples.
* Invalid boundary cases.

For `top_k` with range 1–50, useful cases include:

```text
0   -> invalid
1   -> valid
50  -> valid
51  -> invalid
```

---

## 6.7 Testing logs

Pytest includes `caplog` for capturing log records.

```python
import logging


def use_fallback_provider() -> None:
    logger.warning(
        "Primary provider unavailable; fallback activated"
    )


def test_fallback_is_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING):
        use_fallback_provider()

    assert "fallback activated" in caplog.text
```

Use log assertions for important operational behavior, not every minor log statement.

Good targets:

* Security events.
* Fallback activation.
* Retry exhaustion.
* Data rejection.
* Human escalation.
* Degraded operation.

---

## 6.8 Mocking pitfalls

### Testing the mock instead of the application

Bad tests only verify implementation details:

```python
mock_client.method.assert_called_once()
```

That may be useful, but it should usually be combined with a behavioral assertion:

```python
assert result.answer == "Expected answer"
```

### Mocking too deeply

A test that mocks:

* Five private methods.
* HTTP internals.
* JSON parsing.
* Retry implementation.
* Logging implementation.

will break during harmless refactoring.

Mock at an architectural boundary:

```text
Business service -> provider interface
Repository       -> database interface
RAG pipeline     -> retriever interface
Tool executor    -> external service interface
```

### Returning unrealistic mock data

If a fake provider returns data the real provider could never return, the test creates false confidence.

Maintain representative provider fixtures:

```python
VALID_PROVIDER_RESPONSE = {
    "id": "response-123",
    "output": {
        "text": "Example answer",
    },
    "usage": {
        "input_tokens": 100,
        "output_tokens": 20,
    },
}
```

### Calling real LLM APIs in unit tests

This causes:

* Slow tests.
* Cost.
* Flaky results.
* Rate-limit failures.
* Dependence on network availability.
* Accidental secret exposure.

Real provider calls belong in a small, controlled integration or evaluation test suite.

---

# 7. Three real-world production examples

## Example 1: Safe LLM tool execution

### Problem

An agent generates:

```json
{
  "customer_id": "cust-123",
  "amount": "one thousand",
  "currency": "USD"
}
```

A payment or refund tool expects a numeric amount.

### Solution

1. Define a typed internal interface.
2. Validate LLM-generated arguments with Pydantic.
3. Apply authorization separately.
4. Raise a specific exception when validation fails.
5. Log the request ID and tool name, not sensitive payment details.
6. Test valid, invalid, unauthorized, timeout, and duplicate requests.

```python
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RefundToolInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    customer_id: str
    order_id: str
    amount: Decimal = Field(gt=0)
    currency: Literal["USD", "EUR", "INR"]
    reason: str = Field(min_length=5, max_length=500)
```

Safety improvements:

* Invalid amounts are rejected.
* Unsupported currencies are rejected.
* Unknown fields are rejected.
* Tool code receives a predictable object.
* Tests do not need a real LLM.

---

## Example 2: Reliable RAG ingestion pipeline

### Problem

A large ingestion pipeline processes PDFs, HTML pages, database records, and support tickets.

Common failures include:

* Missing document IDs.
* Empty text.
* Invalid metadata.
* Chunk overlap larger than chunk size.
* Duplicate documents.
* Embedding-provider timeouts.
* Inconsistent vector dimensions.

### Design

```python
class DocumentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source: str
    access_groups: list[str] = Field(min_length=1)
```

Internal chunk structure:

```python
class ChunkRecord(TypedDict):
    chunk_id: str
    document_id: str
    text: str
    start_offset: int
    end_offset: int
```

Error hierarchy:

```python
class IngestionError(AIServiceError):
    pass


class EmbeddingDimensionError(IngestionError):
    pass
```

Tests:

* Empty documents are rejected.
* Chunk boundaries are correct.
* Overlap is correct.
* Metadata is preserved.
* Restricted access groups are attached.
* Provider timeouts become retryable errors.
* Incorrect vector dimensions stop indexing.

Operational logs:

```json
{
  "event": "document_ingestion_failed",
  "correlation_id": "job-812",
  "document_id": "doc-431",
  "stage": "embedding",
  "error_code": "PROVIDER_TIMEOUT",
  "retryable": true
}
```

---

## Example 3: Replacing an LLM provider safely

### Problem

An application initially uses provider A but later adds provider B for:

* Lower cost.
* Regional deployment.
* Compliance.
* Better availability.
* Model specialization.

### Unsafe design

```python
def answer(question: str) -> str:
    # Provider-specific SDK usage is spread throughout business logic.
    ...
```

### Safer design

```python
class LLMProvider(Protocol):
    def generate(
        self,
        prompt: str,
        *,
        temperature: float,
    ) -> str:
        ...
```

Every provider adapter must satisfy the interface.

Each adapter:

* Validates provider responses.
* Translates SDK errors into domain exceptions.
* Produces the same internal response type.
* Emits common metrics.
* Supports the same test contract.

Contract test:

```python
import pytest


@pytest.mark.parametrize(
    "provider_factory",
    [
        build_provider_a_test_client,
        build_provider_b_test_client,
    ],
)
def test_provider_contract(provider_factory) -> None:
    provider = provider_factory()

    response = provider.generate(
        "Return a short greeting",
        temperature=0.0,
    )

    assert isinstance(response, str)
    assert response.strip()
```

The business service can be tested using a fake provider, while each real provider adapter receives its own smaller integration suite.

---

# 8. Best practices for large AI Python codebases

## Typing

* Type public APIs, service interfaces, repositories, and provider adapters.
* Prefer precise domain models over `dict[str, Any]`.
* Use `TypedDict` for trusted dictionary-shaped internal data.
* Use Pydantic for untrusted runtime data.
* Treat `Any` as an escape hatch, not a default.
* Run static checking in CI.
* Introduce strict typing gradually in legacy systems.
* Explicitly handle `None`.
* Keep provider-specific types inside provider adapters.

## Validation

* Validate at every trust boundary.
* Reject unknown fields for strict machine-to-machine contracts.
* Separate structural validation from authorization.
* Put simple field rules in Pydantic.
* Put database and permission rules in domain services.
* Decide explicitly between coercive and strict validation.
* Version long-lived event and API schemas.
* Validate LLM output even when structured output is requested.
* Limit input lengths to control cost and abuse.
* Avoid side effects inside validators.

## Error handling

* Create a clear exception hierarchy.
* Translate infrastructure exceptions into domain exceptions.
* Mark retryable and non-retryable failures.
* Preserve original causes with `raise ... from exc`.
* Catch only exceptions you can meaningfully handle.
* Avoid swallowing unexpected exceptions.
* Map internal errors to safe public responses.
* Do not retry validation, authorization, or permanent schema errors.
* Use bounded retries with backoff for transient failures.
* Avoid logging and re-raising the same failure at every layer.

## Logging

* Use module-level loggers.
* Use structured, searchable fields.
* Include correlation, request, workflow, and document IDs.
* Log event names and error codes consistently.
* Never log secrets.
* Redact sensitive prompts and retrieved content.
* Use `logger.exception()` for unexpected exceptions.
* Track latency, token usage, model, provider, and retry count.
* Keep logs operationally useful rather than excessively verbose.
* Configure logging centrally instead of separately in every module.

## Testing

* Keep most tests fast and deterministic.
* Mock or fake network, database, queue, and model boundaries.
* Prefer simple fakes for important domain interfaces.
* Use fixtures for reusable setup and teardown.
* Test successful and failure paths.
* Test boundary values.
* Test malformed provider and LLM responses.
* Test timeout, rate-limit, fallback, and retry behavior.
* Keep model-quality evaluations separate from ordinary unit tests.
* Maintain a small number of real integration tests.
* Avoid exact wording assertions for genuinely generative output; validate structure and required facts instead.

---

# 9. Common interview pitfalls

## “Type hints make Python statically typed”

Not exactly. Python remains dynamically typed. Type hints enable optional static analysis but are not generally enforced by the Python runtime.

## “`Optional[str]` means the argument is optional”

Incorrect. It means the value can be `str` or `None`.

## “Pydantic and `TypedDict` solve the same problem”

No:

* `TypedDict`: mainly static checking for dictionary structure.
* Pydantic: runtime parsing, validation, constraints, and serialization.

## “Mock every dependency”

Excessive mocking creates brittle tests. Mock external boundaries and use real internal logic where practical.

## “Catch `Exception` everywhere”

This hides programming defects and prevents correct retry and response behavior.

## “Log the entire prompt for debugging”

Prompts can contain confidential data. Log identifiers, sizes, hashes, templates, and approved metadata instead.

## “A valid Pydantic object is safe to execute”

Validation does not replace:

* Authorization.
* Confirmation.
* Policy checks.
* Idempotency.
* Rate limits.
* Business rules.

---

# 10. Interview Q&A

## 1. What is the difference between static typing and runtime validation?

**Static typing** checks how code uses values before execution, usually through tools such as `mypy`. **Runtime validation** checks actual data while the application is running. Type hints support static checking; Pydantic performs runtime validation.

---

## 2. Does Python enforce type hints at runtime?

No. Normal Python execution generally does not reject a value simply because it conflicts with an annotation. Type checkers, IDEs, and linters use those annotations.

---

## 3. What is the difference between `Optional[str]` and a default argument?

`Optional[str]` means the value may be a string or `None`.

```python
name: str | None
```

A default argument means the caller may omit it:

```python
def greet(name: str = "Guest") -> str:
    ...
```

---

## 4. When would you use `TypedDict` instead of Pydantic?

Use `TypedDict` for trusted, internal dictionary-shaped data where static checking is sufficient. Use Pydantic for external or untrusted data that needs runtime validation, constraints, and serialization.

---

## 5. Why is `dict[str, Any]` dangerous in a large AI system?

It removes information about required keys and value types. This weakens IDE assistance, refactoring safety, static checking, and documentation. It also allows schema mistakes to move deeper into the application.

---

## 6. How would you handle errors from multiple LLM providers?

Create provider adapters that translate provider-specific SDK exceptions into a common domain exception hierarchy, such as:

* `ProviderRateLimitError`
* `ProviderUnavailableError`
* `InvalidModelResponseError`

The service layer then handles consistent application-level errors regardless of provider.

---

## 7. What information should be included in AI-service logs?

Common useful fields include:

* Correlation ID.
* Event name.
* Provider and model.
* Latency.
* Token usage.
* Retry count.
* Tool name.
* Document or workflow ID.
* Stable error code.
* Success or failure status.

Sensitive prompts, secrets, and document content should be excluded or redacted.

---

## 8. How would you unit test code that calls an LLM?

Inject an LLM provider interface and use a deterministic fake or mock. Configure it to return controlled responses or raise controlled errors. Verify the service output, prompt construction, error translation, and fallback behavior without making a real network call.

---

## 9. What should be tested around an LLM integration?

Test:

* Valid responses.
* Empty responses.
* Malformed JSON.
* Missing fields.
* Timeouts.
* Rate limits.
* Authentication failures.
* Retry exhaustion.
* Fallback behavior.
* Token or size limits.
* Schema validation.

Model-answer quality should be covered by a separate evaluation suite.

---

## 10. Why should correlation IDs be included in logs?

One user request can pass through an API, retriever, vector database, reranker, LLM, and tool service. A correlation ID links those events, making distributed debugging and latency analysis possible.

---

# 11. Final revision summary

```text
TYPE HINTS
Developer-time contracts
        |
        v
mypy / IDE checks
        |
        v
Fewer incorrect calls and safer refactoring


PYDANTIC
Untrusted runtime input
        |
        v
Parsing + validation + constraints
        |
        v
Trusted application model


EXCEPTIONS
Low-level failure
        |
        v
Translate to domain exception
        |
        v
Retry, fallback, reject, or escalate


LOGGING
Structured event + correlation ID
        |
        v
Search, trace, alert, diagnose


TESTING
Fixtures + fakes + boundary mocks
        |
        v
Fast and deterministic verification
        |
        v
Safer production changes
```

The senior-engineer principle is:

> **Make contracts explicit, validate every external boundary, fail predictably, log enough context to diagnose the failure, and prove behavior through deterministic tests.**

[1]: https://docs.python.org/3/library/typing.html "typing — Support for type hints — Python 3.14.6 documentation"
[2]: https://mypy.readthedocs.io/?utm_source=chatgpt.com "mypy 2.3.0 documentation"
[3]: https://docs.pydantic.dev/latest/concepts/models/ "Models | Pydantic Docs"
[4]: https://docs.python.org/3/howto/logging-cookbook.html?utm_source=chatgpt.com "Logging Cookbook — Python 3.14.6 documentation"
[5]: https://docs.pytest.org/en/stable/how-to/fixtures.html?utm_source=chatgpt.com "How to use fixtures - pytest documentation"
[6]: https://docs.pytest.org/en/stable/how-to/monkeypatch.html?utm_source=chatgpt.com "How to monkeypatch/mock modules and environments"
