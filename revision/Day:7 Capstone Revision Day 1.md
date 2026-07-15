# Capstone Revision – Day 1

## 1. Big-picture mental map

A production GenAI backend is not only an LLM call. It is a complete software system:

```text
Client / UI
    |
API Gateway / Load Balancer
    |
FastAPI Service
    |
Application / Service Layer
    |
    +--> LLM Provider
    +--> Retrieval Service --> Vector Database
    +--> Tool Integrations --> External APIs
    +--> Repository Layer --> SQL / NoSQL
    +--> Redis --> Cache / Rate Limit / Locks
    |
Async Queue / Workers
    |
Ingestion and ETL Pipelines
    |
Object Storage + Databases + Vector Indexes
    |
Cloud Infrastructure / Kubernetes
```

The engineering foundations connect as follows:

* **Python** implements the services, workflows, workers, and integrations.
* **OOP, typing, validation, and architecture** keep a growing codebase maintainable.
* **Async and concurrency** reduce waiting time when calling models, retrievers, and tools.
* **DSA** develops the reasoning needed for efficient processing and interview problems.
* **HTTP and APIs** expose AI capabilities safely to clients.
* **SQL and NoSQL** store transactional and flexible application data.
* **Redis** provides fast temporary storage, caching, locking, and rate limiting.
* **Vector databases** support semantic retrieval for RAG.
* **ETL pipelines** turn raw enterprise data into searchable AI knowledge.
* **Cloud and Kubernetes** deploy, scale, and operate the platform.

A senior engineer should think across five dimensions:

```text
Correctness
Reliability
Scalability
Security
Observability
```

---

# 2. Topic-by-topic revision notes

# 2.1 Python Core Revision

## Core idea

Python is popular for AI backends because it combines:

* Easy-to-read application code
* Strong ML and data ecosystems
* Mature web frameworks
* Async support
* Fast development speed

Python is dynamically typed, but production systems should still use type hints, validation, testing, and clear interfaces.

## Fundamental types

### Scalar types

```python
request_count: int = 10
temperature: float = 0.2
model_name: str = "gpt-model"
is_streaming: bool = True
```

Important behavior:

* `int` has arbitrary precision in Python.
* `float` uses binary floating-point and may have precision issues.
* `str` is immutable.
* `bool` is a subclass of `int`, but should be treated semantically as a boolean.

Avoid using `float` for exact financial calculations. Use `decimal.Decimal`.

### Collections

```python
models = ["model-a", "model-b"]        # list: ordered, mutable
coordinates = (10.0, 20.0)            # tuple: ordered, immutable
tenant_ids = {"org-1", "org-2"}        # set: unique elements
config = {"timeout": 30, "retries": 3} # dict: key-value mapping
```

Typical complexities:

* List index access: `O(1)`
* List membership search: `O(n)`
* Dictionary lookup: average `O(1)`
* Set membership: average `O(1)`
* Appending to a list: amortized `O(1)`

### Slicing

```python
tokens = ["a", "b", "c", "d", "e"]

first_three = tokens[:3]
last_two = tokens[-2:]
reversed_tokens = tokens[::-1]
every_second = tokens[::2]
```

Slicing usually creates a new collection, so its cost is proportional to the slice size.

### Comprehensions

```python
active_models = [
    model["name"]
    for model in models
    if model["enabled"]
]

token_counts = {
    document_id: len(tokens)
    for document_id, tokens in tokenized_documents.items()
}
```

Use comprehensions when they remain readable. Do not place complicated business logic inside them.

## Functions

```python
def generate_response(
    prompt: str,
    temperature: float = 0.2,
) -> str:
    return f"Generated response for: {prompt}"
```

Key concepts:

* Positional parameters
* Keyword parameters
* Default values
* Return values
* Scope
* Pure versus side-effecting functions

Avoid mutable default parameters:

```python
# Wrong: the same list is reused across calls.
def add_message(message: str, messages: list[str] = []):
    messages.append(message)
    return messages
```

Correct:

```python
def add_message(
    message: str,
    messages: list[str] | None = None,
) -> list[str]:
    if messages is None:
        messages = []

    messages.append(message)
    return messages
```

### `*args` and `**kwargs`

```python
def call_tools(*tool_names: str, **options: object) -> None:
    print(tool_names)  # Tuple of positional arguments
    print(options)     # Dictionary of keyword arguments
```

Use them for framework-style extensibility, decorators, adapters, and wrappers. Avoid overusing them in business APIs because they weaken discoverability and static checking.

## Modules, packages, and imports

* **Module:** one Python file.
* **Package:** directory containing Python modules.
* **Import:** makes code from another module available.

```python
from app.services.rag_service import RagService
```

Prefer explicit imports. Avoid wildcard imports:

```python
from module import *  # Avoid
```

Common circular-import solution:

* Move shared interfaces into a lower-level module.
* Apply dependency inversion.
* Avoid service modules importing each other bidirectionally.

## Virtual environments

### `venv`

Creates an isolated Python environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

### `pyenv`

Manages multiple Python interpreter versions.

```bash
pyenv install 3.12
pyenv local 3.12
```

### `uv`

A fast Python package and project-management tool. It can manage dependencies, lockfiles, Python versions, and virtual environments.

Conceptually:

```bash
uv init
uv add fastapi pydantic
uv sync
uv run pytest
```

Senior distinction:

* `pyenv`: primarily Python version management.
* `venv`: environment isolation.
* `uv`: broader dependency, project, environment, and execution workflow.

## Production project structure

```text
app/
├── api/
│   ├── routes/
│   │   ├── chat.py
│   │   └── health.py
│   └── dependencies.py
├── core/
│   ├── config.py
│   ├── exceptions.py
│   └── logging.py
├── domain/
│   ├── models.py
│   └── interfaces.py
├── services/
│   ├── chat_service.py
│   ├── rag_service.py
│   └── ingestion_service.py
├── repositories/
│   ├── conversation_repository.py
│   └── document_repository.py
├── integrations/
│   ├── llm_client.py
│   ├── vector_store.py
│   └── redis_client.py
├── workers/
│   └── ingestion_worker.py
└── main.py

tests/
├── unit/
├── integration/
└── conftest.py
```

The dependency direction should generally be:

```text
API → Service → Interface → Infrastructure implementation
```

The domain and service layers should not depend directly on FastAPI, Redis, or a particular LLM vendor.

## Configuration and `.env`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    llm_api_key: str
    request_timeout_seconds: float = 30.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
```

Best practices:

* Do not commit secrets.
* Validate configuration during startup.
* Use environment variables or a secret manager in production.
* Separate development, testing, staging, and production configuration.
* Fail fast when mandatory configuration is missing.

## Logging basics

```python
import logging

logger = logging.getLogger(__name__)

def process_document(document_id: str) -> None:
    logger.info(
        "Processing document",
        extra={"document_id": document_id},
    )
```

Prefer logging over `print()` because logging supports:

* Levels
* Formatting
* Central collection
* Context
* Filtering
* Structured JSON output

Levels:

```text
DEBUG → diagnostic details
INFO → normal business events
WARNING → recoverable abnormal condition
ERROR → operation failed
CRITICAL → service-wide failure
```

Never log:

* Passwords
* API keys
* Access tokens
* Full sensitive prompts
* Unmasked personal information

## Exceptions

```python
class ModelProviderError(Exception):
    """Raised when the model provider cannot complete a request."""


def call_model() -> str:
    try:
        return external_model_call()
    except TimeoutError as exc:
        raise ModelProviderError("Model request timed out") from exc
    finally:
        release_temporary_resources()
```

Use:

* `try` for risky operations
* `except` for expected failure categories
* `else` for logic that runs only when no exception occurs
* `finally` for cleanup

Avoid:

```python
except Exception:
    pass
```

That hides failures and makes debugging difficult.

## `pytest` basics

```python
def calculate_cost(tokens: int, price_per_token: float) -> float:
    if tokens < 0:
        raise ValueError("tokens cannot be negative")
    return tokens * price_per_token


def test_calculate_cost() -> None:
    result = calculate_cost(100, 0.002)
    assert result == 0.2


def test_negative_tokens() -> None:
    import pytest

    with pytest.raises(ValueError):
        calculate_cost(-1, 0.002)
```

Testing pyramid:

```text
Many unit tests
Some integration tests
Few end-to-end tests
```

### GenAI usage

Python core concepts appear in:

* Request parsing
* Document transformations
* Model provider wrappers
* Retrieval pipelines
* Worker jobs
* Configuration
* Error handling
* Testing

### Common pitfalls

* Mutable default arguments
* Broad exception handling
* Shared global state
* Blocking work in request handlers
* Unvalidated configuration
* Depending on import side effects
* Logging sensitive data

### Senior interview angle

Say:

> Python accelerates AI application development, but production reliability comes from explicit interfaces, typing, runtime validation, dependency isolation, structured logging, tests, and controlled side effects.

---

# 2.2 Python OOP and Advanced Python

## Classes, objects, methods, and attributes

```python
class EmbeddingService:
    provider_name = "default-provider"  # Class variable

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name    # Instance variable

    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]
```

* **Class:** blueprint.
* **Object:** instance of a class.
* **Attribute:** stored object state.
* **Method:** behavior belonging to an object.

## Four OOP principles

### Encapsulation

Keep internal state and implementation details controlled.

```python
class RateLimiter:
    def __init__(self, limit: int) -> None:
        self._limit = limit
        self._requests = 0

    def allow(self) -> bool:
        if self._requests >= self._limit:
            return False

        self._requests += 1
        return True
```

Python relies more on conventions than strict private access:

* `_name`: internal-use convention
* `__name`: name mangling, not true security

### Abstraction

Expose what an object does without exposing every implementation detail.

```python
from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        limit: int,
    ) -> list[str]:
        raise NotImplementedError
```

### Inheritance

A child class derives behavior from a parent.

```python
class QdrantVectorStore(VectorStore):
    def search(
        self,
        query_vector: list[float],
        limit: int,
    ) -> list[str]:
        return ["doc-1", "doc-2"]
```

### Polymorphism

Different implementations can be used through the same interface.

```python
def retrieve_documents(
    store: VectorStore,
    query_vector: list[float],
) -> list[str]:
    return store.search(query_vector, limit=5)
```

## Composition versus inheritance

Composition means building an object using other objects.

```python
class RagService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store
```

Prefer composition when:

* Components need independent replacement.
* Testing requires mocks or fakes.
* Behavior may change at runtime.
* There is no genuine “is-a” relationship.

Use inheritance when there is a stable semantic subtype relationship.

A `RagService` is not a `VectorStore`; it has a `VectorStore`.

## Instance, class, and static methods

```python
class ModelConfig:
    default_timeout = 30

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ModelConfig":
        return cls(model_name=data["model_name"])

    @staticmethod
    def validate_temperature(value: float) -> bool:
        return 0.0 <= value <= 2.0
```

* Instance method receives `self`.
* Class method receives `cls` and is useful for alternative constructors.
* Static method receives neither and is a utility logically related to the class.

## Properties

```python
class GenerationConfig:
    def __init__(self, temperature: float) -> None:
        self.temperature = temperature

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if not 0.0 <= value <= 2.0:
            raise ValueError("Invalid temperature")
        self._temperature = value
```

Properties allow controlled access while keeping attribute-like syntax.

## Dataclasses

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RetrievedChunk:
    document_id: str
    text: str
    score: float
    metadata: dict[str, str] = field(default_factory=dict)
```

Dataclasses automatically generate methods such as:

* `__init__`
* `__repr__`
* `__eq__`

Use `frozen=True` for immutable value objects.

Use dataclasses for internal trusted objects. Use Pydantic at external data boundaries where validation and serialization matter.

## Dunder methods

```python
class SearchResults:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        return f"SearchResults(items={self.items!r})"

    def __str__(self) -> str:
        return f"{len(self.items)} search results"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SearchResults):
            return NotImplemented
        return self.items == other.items
```

* `__repr__`: developer-oriented representation.
* `__str__`: user-friendly representation.
* `__eq__`: equality behavior.
* `__len__`: supports `len(obj)`.

## Type hints

Modern Python syntax:

```python
def find_user(user_id: str) -> dict[str, str] | None:
    ...
```

Traditional equivalents:

```python
from typing import Dict, List, Optional, Union

names: List[str]
metadata: Dict[str, str]
value: Optional[str]
identifier: Union[str, int]
```

### `TypedDict`

```python
from typing import TypedDict


class DocumentMetadata(TypedDict):
    source_url: str
    tenant_id: str
    document_type: str
```

Use `TypedDict` when a dictionary has a known shape but creating a class would be unnecessary.

Static typing helps:

* IDE completion
* Safer refactoring
* Interface documentation
* Earlier bug detection
* Provider replacement
* Large-team collaboration

Type hints do not validate runtime input by themselves.

## Pydantic validation

```python
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)
    conversation_id: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
```

Pydantic provides:

* Runtime validation
* Data conversion
* Error messages
* Serialization
* JSON Schema generation
* FastAPI integration

## Custom exceptions

```python
class ApplicationError(Exception):
    error_code = "APPLICATION_ERROR"


class DocumentNotFoundError(ApplicationError):
    error_code = "DOCUMENT_NOT_FOUND"


class RetrievalUnavailableError(ApplicationError):
    error_code = "RETRIEVAL_UNAVAILABLE"
```

Translate infrastructure errors into domain/application errors. Do not expose raw database or provider exceptions to clients.

## Structured logging and correlation IDs

A correlation ID lets logs from one request be connected across services.

```text
request_id=req-81
  API received request
  retrieval started
  vector query completed
  model call started
  response returned
```

Typical fields:

```json
{
  "timestamp": "2026-07-14T12:00:00Z",
  "level": "INFO",
  "request_id": "req-81",
  "tenant_id": "org-7",
  "operation": "chat_completion",
  "latency_ms": 842
}
```

Pass context explicitly or use context-local storage such as `contextvars` in async applications.

## Fixtures and mocks

```python
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_llm() -> AsyncMock:
    client = AsyncMock()
    client.generate.return_value = "Mock response"
    return client


@pytest.mark.asyncio
async def test_chat_service(mock_llm: AsyncMock) -> None:
    service = ChatService(llm=mock_llm)

    result = await service.chat("Hello")

    assert result == "Mock response"
    mock_llm.generate.assert_awaited_once_with("Hello")
```

Mock external boundaries:

* Model APIs
* Vector databases
* Email services
* Payment APIs
* Time-dependent behavior

Do not mock every internal method. Tests become coupled to implementation rather than behavior.

### Senior interview angle

> I combine static type checking with runtime validation. Type hints protect internal contracts, while Pydantic validates untrusted input at API and integration boundaries. I use composition and dependency injection so model, vector-store, and database implementations remain replaceable and testable.

---

# 2.3 Async, Concurrency, and Background Work

## Core idea

Concurrency lets a program make progress on multiple tasks during overlapping time.

Parallelism means tasks actually execute at the same instant, usually across multiple CPU cores.

GenAI backends are commonly I/O-bound because they wait for:

* LLM APIs
* Vector databases
* SQL databases
* Tool APIs
* Object storage
* Network streams

That makes async especially useful.

## Sync versus async

Synchronous:

```python
response_a = call_model_a()
response_b = call_model_b()
```

The second call starts only after the first finishes.

Asynchronous:

```python
response_a, response_b = await asyncio.gather(
    call_model_a(),
    call_model_b(),
)
```

Both network operations can wait concurrently.

## Event loop

The event loop:

1. Starts a coroutine.
2. Runs it until it reaches an `await`.
3. While that operation waits, runs another ready coroutine.
4. Resumes the first when its I/O completes.

Async does not automatically make CPU-heavy Python code faster.

## Coroutines and tasks

```python
import asyncio


async def retrieve_from_vector_db(query: str) -> list[str]:
    await asyncio.sleep(0.1)  # Represents network I/O
    return ["chunk-1"]


async def retrieve_from_keyword_search(query: str) -> list[str]:
    await asyncio.sleep(0.1)
    return ["chunk-2"]


async def hybrid_retrieve(query: str) -> list[str]:
    vector_results, keyword_results = await asyncio.gather(
        retrieve_from_vector_db(query),
        retrieve_from_keyword_search(query),
    )

    return vector_results + keyword_results
```

A coroutine is an awaitable unit of async work.

A task schedules a coroutine on the event loop:

```python
task = asyncio.create_task(retrieve_from_vector_db("query"))
results = await task
```

Use tasks when the operation must begin now and be awaited later.

## Failure behavior with `gather`

By default, one exception can cause `gather` to raise.

For partial results:

```python
results = await asyncio.gather(
    call_tool_a(),
    call_tool_b(),
    return_exceptions=True,
)

successful_results = [
    result
    for result in results
    if not isinstance(result, Exception)
]
```

Be deliberate: silently accepting partial failure can create incorrect answers.

## Timeouts

```python
async def call_with_timeout() -> str:
    try:
        async with asyncio.timeout(10):
            return await model_client.generate()
    except TimeoutError as exc:
        raise ModelProviderError("Model call exceeded 10 seconds") from exc
```

Every external operation should usually have:

* Connection timeout
* Read timeout
* Overall request deadline
* Bounded retries

## Threads, processes, and async

### Async

Best for high-concurrency I/O.

Examples:

* LLM API requests
* Database calls with async drivers
* External tool calls
* Streaming responses

### Threads

Useful for:

* Blocking I/O libraries without async support
* File I/O
* Legacy SDK calls

Python’s GIL limits CPU-bound Python execution in threads, but threads can still help with blocking I/O.

### Processes

Useful for CPU-bound work:

* Large parsing operations
* Image transformations
* CPU-based inference
* Heavy data transformations

Processes have higher memory and communication overhead.

### `concurrent.futures`

```python
from concurrent.futures import ThreadPoolExecutor


def blocking_file_load(path: str) -> str:
    with open(path, encoding="utf-8") as file:
        return file.read()


with ThreadPoolExecutor(max_workers=4) as executor:
    future = executor.submit(blocking_file_load, "document.txt")
    content = future.result()
```

Inside async code:

```python
content = await asyncio.to_thread(
    blocking_file_load,
    "document.txt",
)
```

## Background work

Do not keep long-running ingestion inside a web request.

Preferred flow:

```text
POST /documents
    |
Validate and store job
    |
Publish message to queue
    |
Return 202 Accepted + job ID
    |
Worker reads → cleans → chunks → embeds → indexes
```

Tools may include:

* Celery
* Dramatiq
* RQ
* Kafka consumers
* Cloud-native queues and functions

Background jobs need:

* Idempotency
* Retry policies
* Dead-letter handling
* Progress state
* Cancellation strategy
* Observability

## Race conditions

A race condition occurs when the result depends on uncontrolled execution order.

```python
# Unsafe when multiple tasks update this shared state.
total_tokens += response_tokens
```

Solutions:

* Avoid shared mutable state.
* Use immutable request-local state.
* Use database atomic operations.
* Use `asyncio.Lock` for in-process coordination.
* Use Redis or database locks for distributed coordination.
* Prefer idempotency and uniqueness constraints over locks where possible.

## Blocking I/O in async code

Wrong:

```python
async def handler() -> str:
    response = requests.get("https://example.com")
    return response.text
```

`requests.get()` blocks the event loop.

Better:

```python
async def handler() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://example.com")
        return response.text
```

## Async observability

Capture:

* End-to-end request latency
* Per-dependency latency
* Active task count
* Queue depth
* Timeout count
* Cancellation count
* Event-loop lag
* Connection-pool saturation

Use distributed tracing to identify whether time was spent in:

* Retrieval
* SQL
* Tools
* Model inference
* Queue waiting

### Senior interview angle

> Async improves throughput for I/O-bound AI services, but it does not reduce the duration of an individual external model call. I use concurrency with deadlines, bounded fan-out, connection pooling, cancellation propagation, and backpressure. CPU-heavy work moves to processes or workers.

---

# 2.4 DSA High-Yield Revision

## Big-O basics

Big-O describes how resource usage grows with input size.

Common complexities:

```text
O(1)       constant
O(log n)   binary search
O(n)       one full scan
O(n log n) efficient comparison sorting
O(n²)      nested pair comparison
O(2ⁿ)      subset exploration
```

Ignore constants for asymptotic analysis, but real systems still care about constants, memory, network calls, and data distribution.

## Pattern-recognition map

```text
Fast lookup / count / duplicates       → Hash map or set
Contiguous range                       → Sliding window or prefix sum
Sorted array pair problem              → Two pointers
Nested or matching structure           → Stack
Level-by-level traversal               → BFS
Explore connected components / paths   → DFS or BFS
Repeated overlapping subproblems       → Dynamic programming
Shortest unweighted path               → BFS
All subsets with take/skip decisions   → Backtracking or 0/1 DP
```

## Arrays and strings

Arrays provide indexed storage.

Typical interview operations:

* Traverse
* Reverse
* Partition
* Search
* Count
* Compare ranges

Common mistakes:

* Off-by-one errors
* Modifying while iterating
* Ignoring empty input
* Unnecessary nested loops
* Forgetting strings are immutable

## Prefix sums

Use when repeatedly asking for the sum of a range.

```python
def build_prefix_sum(values: list[int]) -> list[int]:
    prefix = [0]

    for value in values:
        prefix.append(prefix[-1] + value)

    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    # Inclusive range [left, right]
    return prefix[right + 1] - prefix[left]
```

Complexity:

* Build: `O(n)`
* Each range query: `O(1)`
* Space: `O(n)`

Clues:

* “Many range sum queries”
* “Subarray sum”
* “Cumulative count”

Pitfall: incorrect indexing between inclusive and exclusive bounds.

## Hashing

### Frequency maps

```python
from collections import Counter


def token_frequency(tokens: list[str]) -> dict[str, int]:
    return dict(Counter(tokens))
```

Complexity: average `O(n)` time and `O(k)` space.

### Duplicate detection

```python
def contains_duplicate(values: list[int]) -> bool:
    return len(values) != len(set(values))
```

### Anagrams

```python
from collections import Counter


def are_anagrams(first: str, second: str) -> bool:
    return Counter(first) == Counter(second)
```

### Two-sum

```python
def two_sum(values: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}

    for index, value in enumerate(values):
        needed = target - value

        if needed in seen:
            return seen[needed], index

        seen[value] = index

    return None
```

Time: `O(n)`
Space: `O(n)`

Important: check the complement before storing when the same element cannot be reused.

## Two pointers

Use when:

* Input is sorted.
* Processing from both ends.
* Maintaining a read and write position.
* Comparing two sequences.

```python
def has_pair_with_sum(values: list[int], target: int) -> bool:
    left = 0
    right = len(values) - 1

    while left < right:
        current_sum = values[left] + values[right]

        if current_sum == target:
            return True
        if current_sum < target:
            left += 1
        else:
            right -= 1

    return False
```

Time: `O(n)`
Space: `O(1)`

Mistake: using two pointers when the ordering property does not justify pointer movement.

## Sliding window

Use for contiguous sequences.

Clues:

* Longest or shortest subarray/substring
* “At most K”
* “Without repeating”
* Fixed-size range
* Contiguous segment

### Fixed-size window

```python
def maximum_window_sum(values: list[int], size: int) -> int:
    if size <= 0 or size > len(values):
        raise ValueError("Invalid window size")

    window_sum = sum(values[:size])
    best = window_sum

    for right in range(size, len(values)):
        window_sum += values[right]
        window_sum -= values[right - size]
        best = max(best, window_sum)

    return best
```

Time: `O(n)`.

### Variable-size window

```python
def longest_unique_substring(text: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0

    for right, character in enumerate(text):
        if character in last_seen:
            # Never move left backward.
            left = max(left, last_seen[character] + 1)

        last_seen[character] = right
        best = max(best, right - left + 1)

    return best
```

Mistake: moving the left pointer backward.

## Stack

Last in, first out.

Uses:

* Parenthesis validation
* Undo
* Expression evaluation
* DFS
* Monotonic-stack problems

```python
def is_valid_parentheses(text: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for character in text:
        if character in "([{":
            stack.append(character)
        elif character in pairs:
            if not stack or stack.pop() != pairs[character]:
                return False

    return not stack
```

Time: `O(n)`
Space: `O(n)`

## Queue

First in, first out.

Use:

* BFS
* Job processing
* Rate-controlled workflows
* Producer-consumer systems

```python
from collections import deque

queue = deque(["job-1"])
job = queue.popleft()
```

Do not use `list.pop(0)` for large queues because it is `O(n)`.

## Trees and graphs

### Tree

A connected acyclic structure.

Examples:

* File system
* Organization hierarchy
* Abstract syntax tree
* Decision tree

### Graph

Vertices connected by edges.

Examples:

* Workflow dependencies
* Tool-call relationships
* Service dependencies
* Knowledge graphs
* Social networks

Representations:

* Adjacency list: memory-efficient for sparse graphs
* Adjacency matrix: direct edge lookup but `O(V²)` space

## DFS

Explores deeply before backtracking.

```python
def dfs(
    graph: dict[str, list[str]],
    start: str,
) -> set[str]:
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return

        visited.add(node)

        for neighbor in graph.get(node, []):
            visit(neighbor)

    visit(start)
    return visited
```

Uses:

* Connected components
* Cycle detection
* Dependency traversal
* Backtracking

Pitfall: forgetting `visited`, causing infinite loops.

Recursive DFS may hit recursion limits on deep graphs. Use an explicit stack when necessary.

## BFS

Explores level by level.

```python
from collections import deque


def bfs(
    graph: dict[str, list[str]],
    start: str,
) -> list[str]:
    queue = deque([start])
    visited = {start}
    order: list[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                # Mark when enqueued to avoid duplicates.
                visited.add(neighbor)
                queue.append(neighbor)

    return order
```

Use BFS for shortest paths in unweighted graphs.

Complexity for DFS and BFS:

```text
O(V + E) time
O(V) space
```

## Dynamic programming

Use DP when:

1. The problem has overlapping subproblems.
2. The final answer can be built from smaller optimal answers.

### Memoization

Top-down recursion plus cache.

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(number: int) -> int:
    if number < 2:
        return number

    return fibonacci(number - 1) + fibonacci(number - 2)
```

### Tabulation

Bottom-up iteration.

```python
def fibonacci_iterative(number: int) -> int:
    if number < 2:
        return number

    previous, current = 0, 1

    for _ in range(2, number + 1):
        previous, current = current, previous + current

    return current
```

Memoization is often easier to derive. Tabulation avoids recursion overhead and can reduce memory.

## 0/1 knapsack intuition

You have items with weights and values. Each item can be selected either zero or one time.

For every item:

```text
Skip it
or
Take it, if capacity allows
```

State:

```text
dp[i][capacity]
= maximum value using the first i items
```

Transition:

```text
max(
    skip current item,
    value[current] + solution for remaining capacity
)
```

The main interview skill is recognizing the take-or-skip decision, not memorizing code.

### Senior interview angle

Explain:

1. Brute-force approach
2. Bottleneck
3. Selected data structure or pattern
4. Invariant
5. Complexity
6. Edge cases

Do not jump directly to code.

---

# 2.5 Design Patterns and Clean Architecture

## SOLID

### Single Responsibility Principle

A component should have one primary reason to change.

Bad:

```text
RagService loads PDFs, chunks text, embeds data, queries a DB,
calls the LLM, formats HTTP responses, and sends metrics.
```

Better:

```text
DocumentLoader
Chunker
EmbeddingService
Retriever
AnswerGenerator
API route
```

### Open/Closed Principle

Open for extension, closed for unnecessary modification.

Adding a new model provider should require a new implementation, not changes across all services.

### Liskov Substitution Principle

Any implementation of an interface should obey its expected contract.

If a `VectorStore.search()` contract returns tenant-filtered results, one implementation must not ignore the tenant filter.

### Interface Segregation Principle

Prefer small focused interfaces.

Avoid one huge interface containing embedding, chat, image generation, moderation, and transcription when consumers use only one capability.

### Dependency Inversion Principle

High-level business logic should depend on abstractions rather than concrete infrastructure.

```python
class ChatService:
    def __init__(self, model: ChatModel) -> None:
        self.model = model
```

The service should not instantiate a vendor SDK internally.

## Factory pattern

Creates the correct implementation.

```python
def create_vector_store(provider: str) -> VectorStore:
    if provider == "qdrant":
        return QdrantVectorStore()
    if provider == "pinecone":
        return PineconeVectorStore()

    raise ValueError(f"Unsupported provider: {provider}")
```

Use for provider selection and environment-specific construction.

Pitfall: a factory containing too much business behavior.

## Strategy pattern

Encapsulates interchangeable algorithms.

Examples:

* Dense retrieval
* Keyword retrieval
* Hybrid retrieval
* Reranking strategies
* Chunking strategies

```python
class RetrievalStrategy(ABC):
    @abstractmethod
    async def retrieve(self, query: str) -> list[RetrievedChunk]:
        ...


class HybridRetrievalStrategy(RetrievalStrategy):
    async def retrieve(self, query: str) -> list[RetrievedChunk]:
        ...
```

## Adapter pattern

Wraps incompatible external APIs behind an internal interface.

```text
Internal ChatModel interface
    ├── OpenAIAdapter
    ├── AzureModelAdapter
    ├── BedrockAdapter
    └── LocalModelAdapter
```

The adapter translates:

* Parameters
* Authentication
* Response objects
* Error types
* Streaming events

## Decorator pattern

Adds behavior without changing core implementation.

Examples:

* Retries
* Caching
* Metrics
* Logging
* Authorization

```python
def log_latency(function):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()

        try:
            return await function(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            logger.info("operation_completed", extra={"seconds": duration})

    return wrapper
```

Preserve function metadata with `functools.wraps` in real code.

## Facade pattern

Provides one simple interface over many internal components.

```python
class RagFacade:
    async def answer(
        self,
        tenant_id: str,
        question: str,
    ) -> str:
        query_vector = await self.embedder.embed(question)
        chunks = await self.retriever.retrieve(
            tenant_id=tenant_id,
            vector=query_vector,
        )
        return await self.generator.generate(question, chunks)
```

Useful for simplifying API-layer interaction.

## Layered architecture

### API layer

Responsible for:

* HTTP
* Authentication
* Request validation
* Response mapping
* Status codes

### Service/application layer

Responsible for:

* Use cases
* Business workflows
* Transactions
* Authorization decisions
* Orchestration

### Repository/data layer

Responsible for:

* Persistence
* Queries
* Storage abstractions

### Infrastructure/integration layer

Responsible for:

* LLM providers
* Vector databases
* Redis
* External APIs
* Message brokers

## Separation of concerns

Keep these distinct:

```text
Retrieval ≠ generation
Domain errors ≠ HTTP errors
Database models ≠ API schemas
Provider responses ≠ internal domain objects
Configuration ≠ business logic
Observability ≠ core algorithm
```

### Senior interview angle

> I use clean boundaries to isolate change. Provider SDKs and databases live behind adapters and repositories. Business services depend on interfaces. This improves testability, vendor portability, and incident containment without adding abstraction where only one simple implementation exists.

---

# 2.6 HTTP, APIs, and FastAPI/Flask

## HTTP methods

* `GET`: retrieve a resource.
* `POST`: create or trigger an operation.
* `PUT`: replace a resource; generally idempotent.
* `PATCH`: partially update.
* `DELETE`: remove.
* `HEAD`: metadata without response body.
* `OPTIONS`: supported capabilities and CORS behavior.

## Status codes

### Success

* `200 OK`
* `201 Created`
* `202 Accepted` for queued async work
* `204 No Content`

### Client errors

* `400 Bad Request`
* `401 Unauthorized`: authentication missing or invalid
* `403 Forbidden`: authenticated but not allowed
* `404 Not Found`
* `409 Conflict`
* `422 Unprocessable Content`: semantically invalid request
* `429 Too Many Requests`

### Server errors

* `500 Internal Server Error`
* `502 Bad Gateway`
* `503 Service Unavailable`
* `504 Gateway Timeout`

## Request components

```text
POST /v1/conversations/conv-123/messages?stream=true
Authorization: Bearer <token>
Idempotency-Key: abc-123

{
  "message": "Summarize the uploaded contract"
}
```

* Path parameter: `conv-123`
* Query parameter: `stream=true`
* Header: authorization, content type, request IDs
* Body: structured request data

## REST resource modeling

Prefer nouns:

```text
POST /v1/conversations
GET  /v1/conversations/{id}
POST /v1/conversations/{id}/messages
GET  /v1/documents/{id}
```

Avoid action-heavy endpoints such as:

```text
POST /createNewConversationNow
```

Some AI operations are naturally command-like:

```text
POST /v1/embeddings
POST /v1/predictions
```

## Idempotency

An operation is idempotent when repeating the same request has the same intended effect.

For expensive or billable `POST` requests:

```text
Client sends Idempotency-Key
Server stores:
    tenant + key → status/result
Repeated request returns original result
```

Use cases:

* Document upload
* Ingestion job creation
* Model fine-tuning request
* Payment-backed inference

Protect idempotency storage with atomic operations or database uniqueness constraints.

## API versioning

Common approach:

```text
/v1/chat
/v2/chat
```

Also possible:

* Header versioning
* Media-type versioning

Maintain backward compatibility for existing clients. Version public contracts, not every internal code change.

## JSON Schema

Describes:

* Object structure
* Required fields
* Types
* Ranges
* Enumerations
* Nested objects

FastAPI derives JSON Schema from Pydantic models and exposes it through OpenAPI.

## Pagination

### Offset pagination

```text
GET /documents?limit=20&offset=40
```

Simple, but can become slow and inconsistent on changing datasets.

### Cursor pagination

```text
GET /messages?limit=20&after=msg_123
```

Better for large or rapidly changing datasets.

Return:

```json
{
  "items": [],
  "next_cursor": "msg_456",
  "has_more": true
}
```

## AI endpoints

```text
POST /v1/chat
POST /v1/predictions
POST /v1/embeddings
POST /v1/documents
GET  /v1/jobs/{job_id}
GET  /health/live
GET  /health/ready
```

Separate liveness and readiness:

* Liveness: process is alive.
* Readiness: process can receive traffic.

Do not make liveness depend on every external provider; temporary provider failure could restart healthy pods repeatedly.

## FastAPI example

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

app = FastAPI()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)


class ChatResponse(BaseModel):
    answer: str
    request_id: str


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    request: Request,
) -> ChatResponse:
    request_id = request.headers.get("X-Request-ID", "generated-id")

    answer = await chat_service.answer(payload.message)

    return ChatResponse(
        answer=answer,
        request_id=request_id,
    )
```

## Flask versus FastAPI

### Flask

* Minimal and flexible
* Mature ecosystem
* Good for small services and synchronous applications
* Validation and documentation need additional setup

### FastAPI

* Type-hint-driven
* Pydantic validation
* Automatic OpenAPI documentation
* Strong async support
* Well suited to typed AI APIs

Framework choice is secondary to architecture, observability, and operational discipline.

## Middleware

Middleware wraps request processing.

Use for:

* Correlation IDs
* Logging
* Latency measurement
* Authentication
* CORS
* Error translation
* Security headers

Avoid putting domain logic in middleware.

## Authentication concepts

### API keys

Simple machine authentication.

Store only hashed keys when possible. Support rotation, scopes, expiration, and usage tracking.

### JWT

A signed token containing claims.

Typical claims:

* Subject
* Tenant
* Roles/scopes
* Issued time
* Expiration

A signed JWT is not necessarily encrypted. Do not place sensitive data inside it.

### OAuth2

Authorization framework allowing applications to obtain scoped access.

Important distinction:

* OAuth2: delegated authorization
* OpenID Connect: identity layer built on OAuth2

## Standard error format

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "The requested document was not found.",
    "request_id": "req-81",
    "details": {}
  }
}
```

Do not expose stack traces, SQL errors, or provider secrets.

## Async endpoints

An `async def` endpoint helps only when downstream operations also support async or blocking work is safely offloaded.

CPU-heavy parsing inside an async route still blocks the event loop.

## ORM integration

Use one session per request or unit of work.

Do not:

* Keep global database sessions.
* Return lazy ORM relationships after the session is closed.
* Perform uncontrolled queries during serialization.

### Senior interview angle

> I design APIs around stable resources and asynchronous job semantics. I include validation, idempotency, deadlines, standardized errors, pagination, tenant-aware authorization, and observability. For long ingestion tasks I return `202 Accepted` with a job resource instead of holding the HTTP connection.

---

# 2.7 ORM, SQL, and Relational Data Modeling

## ORM basics

An ORM maps objects to relational tables.

```text
Python User object ↔ users table row
Conversation.messages ↔ foreign-key relationship
```

Benefits:

* Object-oriented access
* Query construction
* Relationship management
* Transaction support
* Database portability to a degree

Risks:

* Hidden queries
* N+1 problems
* Poor SQL awareness
* Overly complex object graphs

A senior engineer still understands SQL and execution plans.

## Entities and schema

Possible GenAI schema:

```text
organizations
- id
- name
- created_at

users
- id
- organization_id
- email
- created_at

conversations
- id
- organization_id
- user_id
- title
- created_at

messages
- id
- conversation_id
- role
- content
- model_name
- token_count
- created_at

documents
- id
- organization_id
- source_uri
- status
- checksum
- created_at
- updated_at

ingestion_jobs
- id
- document_id
- status
- attempts
- error_code
- created_at
```

Every tenant-owned resource should normally carry or be traceable to an organization identifier.

## CRUD

```sql
SELECT id, role, content
FROM messages
WHERE conversation_id = :conversation_id
ORDER BY created_at ASC;

INSERT INTO conversations (id, organization_id, user_id)
VALUES (:id, :organization_id, :user_id);

UPDATE documents
SET status = 'INDEXED'
WHERE id = :document_id;

DELETE FROM messages
WHERE id = :message_id;
```

Use parameterized queries. Never build SQL by concatenating untrusted input.

## Sessions and transactions

A transaction groups operations into one atomic unit.

```python
def create_conversation_with_message(
    session: Session,
    conversation: Conversation,
    message: Message,
) -> None:
    try:
        session.add(conversation)
        session.add(message)
        session.commit()
    except Exception:
        session.rollback()
        raise
```

Better architecture often places transaction management at the application-service boundary.

## Rollback pattern

Rollback when any part of a multi-write operation fails.

Be careful with external side effects:

```text
Database commit + external API call
```

A database transaction cannot atomically roll back an external model call or message publication.

Patterns for this include:

* Transactional outbox
* Saga
* Idempotent consumer
* Compensating action

## One-to-many relationships

```text
Organization 1 → many users
Conversation 1 → many messages
Document 1 → many chunks
```

Foreign keys enforce referential integrity.

## N+1 problem

Example:

1. Query 100 conversations.
2. For each conversation, query its messages.
3. Total: 101 queries.

Solutions:

* Eager loading
* Join loading
* Select-in loading
* Explicit batch queries
* Projection into required response shapes

Do not eagerly load huge collections by default.

## SQL clauses

Execution conceptually:

```text
FROM / JOIN
WHERE
GROUP BY
HAVING
SELECT
ORDER BY
LIMIT
```

### `WHERE` versus `HAVING`

* `WHERE` filters rows before grouping.
* `HAVING` filters aggregated groups.

```sql
SELECT organization_id, COUNT(*) AS document_count
FROM documents
WHERE status = 'INDEXED'
GROUP BY organization_id
HAVING COUNT(*) > 100
ORDER BY document_count DESC;
```

## Joins

* `INNER JOIN`: matching rows only.
* `LEFT JOIN`: all left rows plus matching right rows.
* `RIGHT JOIN`: all right rows.
* `FULL OUTER JOIN`: all rows from both sides.
* `CROSS JOIN`: Cartesian product.

```sql
SELECT c.id, COUNT(m.id) AS message_count
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
GROUP BY c.id;
```

## Keys

### Primary key

Uniquely identifies a row.

Options:

* Auto-increment integer
* UUID
* Time-sortable distributed identifier

### Foreign key

References another table and helps enforce relationships.

## Normalization versus denormalization

Normalization reduces duplication and update anomalies.

Denormalization duplicates selected data to improve read performance.

Example:

* Canonical organization name in `organizations`.
* Cached organization name in an analytics table.

Do not denormalize without a read-performance reason and consistency strategy.

## Indexes

An index improves reads for certain access patterns.

Likely indexes:

```text
users(email)
messages(conversation_id, created_at)
documents(organization_id, status)
documents(organization_id, checksum)
```

Composite-index order matters.

An index on `(organization_id, created_at)` commonly supports:

* Filtering by organization
* Filtering by organization and date
* Ordering within one organization

It may not efficiently support filtering by `created_at` alone.

Trade-offs:

* Faster reads
* More storage
* Slower writes
* More maintenance
* Potential planner complexity

Use query plans rather than adding indexes blindly.

## ACID

* **Atomicity:** all transaction operations succeed or none do.
* **Consistency:** constraints and invariants remain valid.
* **Isolation:** concurrent transactions interact according to defined rules.
* **Durability:** committed data survives failure.

Isolation issues include:

* Dirty reads
* Non-repeatable reads
* Phantom reads
* Lost updates

Use optimistic locking, row locks, or stronger isolation when business invariants require them.

## Database tests

```python
@pytest.fixture
def db_session(test_engine):
    with Session(test_engine) as session:
        yield session
        session.rollback()
```

Test:

* Constraints
* Repository queries
* Transaction rollback
* Tenant isolation
* Migrations
* Concurrent updates where relevant

SQLite may behave differently from PostgreSQL. For important integration behavior, test with the same database engine used in production.

### Senior interview angle

> I model transactional entities in SQL, establish tenant-scoped access paths, use explicit transaction boundaries, inspect generated SQL, and select indexes from actual query patterns. I treat ORM convenience as an abstraction over SQL, not as a replacement for understanding the database.

---

# 2.8 NoSQL, Redis, Vector Databases, and Caching

## SQL versus NoSQL

### SQL

Best when:

* Relationships matter
* Transactions matter
* Schemas and constraints provide value
* Complex joins and reporting are needed

### NoSQL

Broad category including:

* Document databases
* Key-value stores
* Wide-column databases
* Graph databases

Best when the access pattern, scale, or flexible structure suits a non-relational model.

Do not choose NoSQL merely because data is JSON.

## MongoDB/document database mental model

A document database stores nested documents:

```json
{
  "_id": "conv-123",
  "organization_id": "org-7",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ]
}
```

Embedding an unbounded message history in one document can become problematic.

Typical decision:

* Embed bounded data read together.
* Reference large or independently updated collections.

## Redis

Redis is an in-memory data platform used for:

* Caching
* Rate limiting
* Distributed coordination
* Session storage
* Idempotency keys
* Queue-like structures
* Counters

## TTL

```text
SET cache:answer:abc "<value>" EX 300
```

TTL automatically expires temporary data.

Choose TTL from:

* Data freshness requirements
* Update frequency
* Cost of recomputation
* Storage pressure

Avoid making every key permanent.

## Rate limiting

Fixed-window idea:

```text
INCR rate:{tenant}:{minute}
EXPIRE rate:{tenant}:{minute} 60
Reject when count > limit
```

More accurate options:

* Sliding window
* Token bucket
* Leaky bucket

Atomic Redis scripts or transactions prevent race conditions.

## Distributed locks

A lock can prevent duplicate processing, but distributed locking is subtle.

Prefer:

* Unique constraints
* Idempotency keys
* Compare-and-set operations
* Atomic queue ownership

Use locks only when the coordination requirement is clear, with:

* Expiration
* Unique ownership token
* Safe release
* Failure recovery

## Read-through cache

```text
Application asks cache for key
    |
Cache hit → return value
    |
Cache miss
    |
Read database
    |
Store result in cache
    |
Return value
```

Pseudo-code:

```python
async def get_document(document_id: str) -> Document:
    cache_key = f"document:{document_id}"

    cached = await redis.get(cache_key)
    if cached is not None:
        return Document.model_validate_json(cached)

    document = await repository.get(document_id)
    await redis.set(
        cache_key,
        document.model_dump_json(),
        ex=300,
    )
    return document
```

Hard part: invalidation.

Strategies:

* TTL only
* Delete on update
* Versioned keys
* Event-driven invalidation

## Cache stampede

Many requests miss the same key and recompute simultaneously.

Mitigations:

* Single-flight/request coalescing
* Short lock per key
* Jittered expiration
* Refresh ahead
* Stale-while-revalidate

## Vector database basics

An embedding converts content into a numeric vector representing semantic characteristics.

```text
"How do I reset my password?"
        ↓ embedding model
[0.12, -0.04, 0.78, ...]
```

A vector database retrieves nearby vectors.

## Similarity intuition

### Cosine similarity

Compares direction. Often useful when vector magnitude should matter less.

### Dot product

Measures alignment and magnitude. For normalized vectors, it closely relates to cosine similarity.

### Euclidean distance

Measures geometric distance.

Use the metric expected by the embedding model and index configuration.

## Vector index types

### Flat

* Exact search
* Highest recall
* Slow on large collections
* Useful as a baseline

### HNSW

Graph-based approximate nearest-neighbor index.

* Strong recall/latency trade-off
* Fast query performance
* Higher memory use
* Tunable construction and search parameters

### IVF

Partitions vectors into clusters and searches selected clusters.

* Efficient at larger scale
* Requires training or clustering
* Recall depends on how many partitions are searched

Approximate nearest-neighbor search trades a small amount of recall for much lower latency.

## Vector schema

```json
{
  "id": "chunk-789",
  "text": "Refunds are available within 30 days...",
  "embedding": [0.12, -0.04, 0.78],
  "metadata": {
    "tenant_id": "org-7",
    "document_id": "doc-11",
    "source_url": "s3://bucket/policy.pdf",
    "document_type": "policy",
    "page_number": 4,
    "embedding_version": "embed-v3"
  }
}
```

Metadata enables:

* Tenant isolation
* Authorization filtering
* Source citations
* Date filtering
* Document-type filtering
* Reindexing

## Tool overview

### FAISS

* Vector-search library
* Good for local and custom deployments
* Not a complete managed database
* You build persistence, metadata, replication, and APIs around it

### Chroma

* Developer-friendly vector store
* Useful for prototypes and smaller applications

### Qdrant

* Purpose-built vector database
* Filtering and production deployment capabilities
* Self-hosted and managed options

### Pinecone

* Managed vector database
* Operational convenience and scalability
* Less infrastructure ownership

The correct choice depends on:

* Scale
* Filtering
* Tenant isolation
* Availability
* Operational expertise
* Cost
* Deployment constraints

## Major pitfalls

### Wrong embedding model

Indexing with one model and querying with another incompatible model makes similarity meaningless.

### Missing versioning

Store:

* Embedding model
* Model version
* Chunking version
* Pipeline version

### Poor metadata

Without source and tenant metadata, security, debugging, filtering, and citations become difficult.

### Weak tenant filtering

Tenant filtering must happen in the database query itself, not after retrieving cross-tenant results.

### Treating vector search as exact truth

Similarity search is probabilistic. Evaluate retrieval quality with representative queries.

### Senior interview angle

> I separate transactional storage from semantic retrieval. SQL remains the system of record, Redis handles ephemeral low-latency concerns, object storage holds source artifacts, and the vector database holds derived searchable chunks. All vector operations enforce tenant and authorization filters at query time.

---

# 2.9 ETL and Ingestion Foundations

## ETL basics

* **Extract:** read data from a source.
* **Transform:** clean, normalize, enrich, and validate.
* **Load:** store processed data in the target system.

For RAG:

```text
Read → Parse → Clean → Enrich → Deduplicate
→ Chunk → Embed → Index → Validate
```

In some architectures, data is loaded into a raw lake before transformation. That is commonly called ELT.

## Batch versus streaming

### Batch

Processes groups periodically.

Use for:

* Nightly document sync
* Historical backfills
* Bulk reindexing
* Large file collections

### Streaming

Processes events continuously or near-real-time.

Use for:

* New support tickets
* Change-data capture
* Live event ingestion
* Rapid knowledge updates

Many production systems use both.

## Sources

* Uploaded files
* S3/GCS/Blob storage
* Relational databases
* Document databases
* External APIs
* Web pages
* Event streams
* SaaS connectors

Each source needs a cursor or checkpoint:

* Last timestamp
* Page token
* Object version
* Database offset
* Event offset

## Text cleaning

Potential steps:

* Normalize Unicode
* Remove control characters
* Repair encoding
* Remove repeated headers and footers
* Remove navigation boilerplate
* Preserve headings
* Preserve table meaning
* Normalize whitespace
* Detect language

Over-cleaning can destroy useful structure.

## Encoding issues

Do not assume every file is UTF-8.

Handle:

* Byte order marks
* Invalid bytes
* Mixed encodings
* Replacement characters
* Normalization differences

Record parsing failures instead of silently dropping content.

## Metadata enrichment

Useful fields:

```text
tenant_id
source_url
source_system
document_id
document_type
title
author
created_at
updated_at
ingested_at
tags
language
checksum
access_control
pipeline_version
```

Metadata is essential for security, filtering, lineage, and troubleshooting.

## Pagination

External APIs often return partial results.

Correct ingestion:

```text
Read page
Process page
Persist checkpoint
Request next page
Repeat until no next token
```

Do not update the checkpoint before durable processing completes.

## Retries and backoff

Retry transient failures:

* Timeouts
* `429`
* Temporary `5xx`
* Connection resets

Do not automatically retry:

* Invalid credentials
* Unsupported format
* Permanent schema errors
* Most `4xx` validation failures

Exponential backoff:

```text
1s → 2s → 4s → 8s
```

Add jitter so many workers do not retry simultaneously.

Respect server-provided retry instructions.

## Duplicate detection

Options:

* Source-system ID
* Object version
* File checksum
* Normalized content hash
* Chunk hash
* Semantic similarity for near-duplicates

Exact hash catches exact duplicates, not paraphrases.

Use database uniqueness constraints to make deduplication race-safe.

## PII masking

Basic process:

```text
Detect sensitive entity
Replace or tokenize
Record policy outcome
Store only allowed data
```

Examples:

* Email addresses
* Phone numbers
* Government identifiers
* Payment details

PII handling needs:

* Defined policy
* Access control
* Audit logs
* Encryption
* Retention rules
* Human review for high-risk data

Regex alone is not enough for every PII type.

## Data lineage

Lineage answers:

* Where did this chunk come from?
* Which source version created it?
* Which parser and chunker were used?
* Which embedding model produced the vector?
* When was it indexed?
* What replaced it?

Example:

```text
source object version
→ parsed document
→ normalized document version
→ chunk IDs
→ embedding version
→ vector index version
```

## Production ingestion flow

```text
1. Detect source change
2. Create ingestion job
3. Acquire idempotency key
4. Fetch source
5. Store immutable raw copy
6. Parse and validate
7. Clean and normalize
8. Enrich metadata and ACL information
9. Calculate checksum and deduplicate
10. Split into chunks
11. Generate embeddings in bounded batches
12. Write chunks to vector index
13. Update searchable-version pointer
14. Mark job successful
15. Emit metrics and audit event
```

For safe reindexing, consider blue/green index versions:

```text
Build new index version
Validate it
Atomically switch alias
Delete old version later
```

### Senior interview angle

> I treat ingestion as a replayable, idempotent data product rather than a one-time script. Raw source data is retained, processing steps are versioned, checkpoints are durable, failures are retryable, and index publication is atomic so partially processed documents do not appear in search.

---

# 2.10 Cloud and Kubernetes Basics

## Cloud mental model

Every major cloud provides similar categories.

| Capability            | AWS             | GCP                 | Azure                |
| --------------------- | --------------- | ------------------- | -------------------- |
| Object storage        | S3              | Cloud Storage       | Blob Storage         |
| Virtual machines      | EC2             | Compute Engine      | Azure VMs            |
| Managed Kubernetes    | EKS             | GKE                 | AKS                  |
| Managed relational DB | RDS             | Cloud SQL           | Azure SQL/PostgreSQL |
| Serverless functions  | Lambda          | Cloud Functions/Run | Azure Functions      |
| Secrets               | Secrets Manager | Secret Manager      | Key Vault            |

Do not focus only on product names. Understand the capability.

## Compute

Options include:

* Virtual machines
* Containers
* Kubernetes
* Serverless functions
* Managed model endpoints
* GPU instances

Choose based on:

* Runtime duration
* Scaling pattern
* Hardware
* Operational ownership
* Startup latency
* Cost

## Object storage

Use S3/GCS/Blob for:

* Raw documents
* Training datasets
* Model artifacts
* Evaluation data
* Audit exports
* Large generated files

Object storage is not a mounted POSIX filesystem by default. Applications interact through object APIs.

## Managed databases

Managed services usually provide:

* Backups
* Patching
* Replication
* Monitoring
* Failover features

You still own:

* Schema
* Queries
* Indexes
* Connection management
* Data security
* Capacity choices

## Kubernetes concepts

### Pod

Smallest deployable execution unit. Usually contains one application container plus optional sidecars.

Pods are ephemeral.

### Deployment

Maintains desired application replicas and manages rolling updates.

```text
Deployment desired replicas = 5
Kubernetes replaces failed pods
```

### Service

Provides stable networking to changing pods.

### Ingress

Routes external HTTP traffic to services, often using host/path rules and TLS.

### ConfigMap

Stores non-secret configuration.

### Secret

Stores sensitive configuration, though additional encryption and external secret-management controls are often needed.

### HPA

Horizontal Pod Autoscaler changes replica count based on metrics.

Possible signals:

* CPU
* Memory
* Request rate
* Queue depth
* In-flight model requests
* Custom latency metric

CPU alone may not reflect AI-service load.

## Load balancing

Distributes traffic across healthy instances.

Consider:

* Health checks
* Connection draining
* Sticky sessions
* Streaming connections
* Timeouts
* Retry behavior
* TLS termination

Avoid retries at multiple layers without coordination because retry amplification can overload dependencies.

## Scale-up versus scale-out

### Scale up

Increase CPU, memory, or GPU of one machine.

Advantages:

* Simpler
* Useful for model memory requirements

Limitations:

* Hardware ceiling
* Larger failure domain
* Expensive machines

### Scale out

Add more machines or pods.

Advantages:

* Better resilience
* Greater aggregate throughput

Limitations:

* Distributed coordination
* Shared-state complexity
* Cold starts
* Load-balancing needs

Stateless API services are easier to scale horizontally.

## API Gateway, ALB, and NLB concepts

### API Gateway

Often handles:

* Authentication
* Quotas
* Routing
* API keys
* Request transformations
* Public API management

### Application Load Balancer

Layer-7 HTTP routing:

* Host-based routing
* Path-based routing
* TLS termination

### Network Load Balancer

Layer-4 TCP/UDP routing:

* High throughput
* Lower-level network behavior
* Static IP requirements in some deployments

## AI platform deployment

```text
Internet
   |
API Gateway / WAF
   |
HTTP Load Balancer / Ingress
   |
FastAPI Chat Pods
   |
   +--> Managed PostgreSQL
   +--> Redis
   +--> Vector Database
   +--> LLM Provider or Model Serving Cluster
   |
Queue
   |
Ingestion Workers
   |
Object Storage
```

Possible separate workloads:

* Chat API pods
* Retrieval service pods
* Ingestion workers
* Evaluation jobs
* Model-serving GPU deployments
* Scheduled synchronization jobs

## Reliability principles

* Multiple replicas
* Multi-zone deployment
* Pod disruption budgets
* Readiness probes
* Graceful shutdown
* Connection draining
* Resource requests and limits
* Autoscaling
* Backups
* Disaster-recovery plan
* Infrastructure as code

### Senior interview angle

> I keep API services stateless, move durable state into managed data services, scale workers from queue depth, and scale model serving using GPU-aware metrics. Kubernetes handles scheduling and desired state, but application-level idempotency, data consistency, observability, and graceful degradation remain our responsibility.

---

# 3. Real-world GenAI examples

## Example 1: Production RAG chat backend

```text
POST /v1/conversations/{id}/messages
    |
Authenticate user and resolve tenant
    |
Validate request with Pydantic
    |
Load conversation from PostgreSQL
    |
Check semantic-answer cache
    |
Run vector + keyword retrieval concurrently
    |
Apply authorization and metadata filters
    |
Rerank retrieved chunks
    |
Build grounded prompt
    |
Call model provider asynchronously
    |
Persist user and assistant messages transactionally
    |
Stream or return response
```

Engineering concepts involved:

* FastAPI validation
* Async I/O
* Repository pattern
* SQL transactions
* Redis caching
* Vector search
* Adapter pattern
* Structured logging
* Request IDs
* Kubernetes scaling

Critical controls:

* Tenant isolation
* Timeouts
* Token limits
* Citation tracking
* Prompt-injection defenses
* Retry boundaries
* Cost metrics
* Retrieval evaluation

## Example 2: Document-ingestion system

```text
Upload document
    |
Store raw file in object storage
    |
Create database row and job
    |
Publish queue event
    |
Worker parses file
    |
Clean and normalize text
    |
Extract metadata and access controls
    |
Deduplicate
    |
Chunk
    |
Embed in batches
    |
Write versioned vector records
    |
Switch searchable version
```

Important design properties:

* Idempotent jobs
* Replayable pipeline
* Dead-letter queue
* Versioned embeddings
* Immutable raw source
* Partial-failure recovery
* Atomic index publication
* Data lineage

## Example 3: Agent platform with parallel tools

```text
User question
    |
Planner selects tools
    |
Concurrent execution:
    +--> SQL analytics
    +--> CRM API
    +--> Knowledge retrieval
    +--> Search service
    |
Merge and validate tool outputs
    |
Model synthesizes answer
```

Use:

* `asyncio.gather`
* Per-tool timeout
* Concurrency semaphore
* Typed tool schemas
* Adapter interfaces
* Correlation IDs
* Partial-failure policy
* Tool authorization
* Audit logging

Do not allow unlimited model-generated fan-out.

## Example 4: Model-serving API

```text
POST /v1/predictions
    |
Validate input
    |
Check model/version
    |
Apply rate limit
    |
Batch or queue inference
    |
Invoke model server
    |
Return prediction + version metadata
```

Senior considerations:

* Dynamic batching
* GPU utilization
* Request deadlines
* Backpressure
* Model version pinning
* Canary deployment
* Shadow traffic
* Drift monitoring
* Input/output schema compatibility

## Example 5: Chat-history storage

Use SQL for:

* Conversation ownership
* Ordered message history
* Audit fields
* Token and model metadata
* Transactional updates

Use Redis for:

* Recent conversation cache
* Rate counters
* Streaming coordination
* Short-lived locks

Use object storage for:

* Large attachments
* Exported transcripts

Avoid using the vector database as the only source of truth.

---

# 4. Cross-cutting best practices and pitfalls

## Reliability

Best practices:

* Timeouts on every external call
* Bounded retries with jitter
* Idempotency for commands and jobs
* Circuit breakers for failing dependencies
* Backpressure and concurrency limits
* Graceful degradation
* Dead-letter queues
* Health and readiness checks

Pitfalls:

* Infinite retries
* Retrying non-idempotent operations blindly
* Nested retries at gateway, service, and SDK levels
* Unlimited async fan-out
* Long operations inside HTTP requests

## Security

Best practices:

* Authenticate every non-public endpoint
* Authorize per resource and tenant
* Apply tenant filters in database/vector queries
* Store secrets in a secret manager
* Encrypt data in transit and at rest
* Redact sensitive logs
* Validate file type and size
* Audit high-risk operations

Pitfalls:

* Trusting tenant IDs supplied by the client
* Filtering cross-tenant vector results after retrieval
* Logging prompts containing confidential data
* Putting secrets in `.env` files committed to Git
* Assuming signed JWTs are encrypted

## Observability

Capture:

* Request count and latency
* Error rate
* Token usage
* Model cost
* Retrieval latency
* Retrieval result count
* Cache hit rate
* Queue depth
* Worker failures
* Database-pool usage
* Model-provider failures

Three pillars:

```text
Logs: what happened
Metrics: how often and how much
Traces: where time was spent
```

Pitfalls:

* Logs without request IDs
* Metrics with unbounded labels such as raw user IDs
* Logging full model prompts by default
* Monitoring only average latency instead of percentiles

## Performance

Best practices:

* Use connection pools.
* Run independent I/O concurrently.
* Cache stable expensive results.
* Batch embedding requests.
* Paginate large responses.
* Inspect SQL query plans.
* Avoid unnecessary serialization.
* Apply request and token limits.

Pitfalls:

* Using async for CPU-heavy tasks
* Creating a new HTTP client per operation
* Over-fetching ORM relationships
* Caching without invalidation
* Premature optimization without measurement

## Maintainability

Best practices:

* Separate API, service, repository, and integration layers.
* Use domain-specific exceptions.
* Keep provider SDK objects out of the domain.
* Use typing and runtime validation.
* Prefer composition.
* Maintain unit, integration, and contract tests.

Pitfalls:

* Giant service classes
* Abstraction for every trivial function
* Vendor SDK usage scattered throughout code
* Global configuration and clients
* Tests coupled to internal method calls

---

# 5. Senior interview angle

A junior answer often explains how a feature works.

A senior answer also explains:

```text
Why this design?
What are the failure modes?
How does it scale?
How is tenant isolation enforced?
What is the source of truth?
How is it monitored?
How is it tested?
How do we migrate it?
What happens during partial failure?
What trade-off did we accept?
```

## A strong answer structure

Use this sequence:

1. Clarify workload and requirements.
2. State the simplest viable design.
3. Identify data ownership and source of truth.
4. Define request and failure flows.
5. Explain scaling constraints.
6. Cover security and tenant isolation.
7. Cover observability.
8. Discuss trade-offs and alternatives.

Example:

> I would expose ingestion as an asynchronous job because parsing and embedding can exceed an HTTP deadline. The API stores a job record and publishes an idempotent queue message. Workers process the source in versioned stages, persist checkpoints, batch embedding calls, and write to a new index version. After validation, an alias is switched atomically. This prevents partially indexed documents from becoming visible and allows replay after failure.

## Trade-off language

Use phrases such as:

* “I would start with…”
* “At this scale, the simpler option is…”
* “The trade-off is…”
* “If the workload grows beyond…, I would introduce…”
* “The system of record remains…”
* “This failure is recoverable because…”
* “This operation must be idempotent because…”
* “I would validate this assumption through metrics…”

## What interviewers look for

* Clear mental models
* Correct interfaces
* Appropriate data structures
* Failure awareness
* Security awareness
* Practical trade-offs
* Ability to avoid overengineering
* Ability to evolve the design

---

# 6. Interview Q&A

## 1. Why use a dictionary instead of a list for lookup?

A dictionary provides average `O(1)` key lookup, while searching a list is `O(n)`. Use a list when ordering and sequential access matter; use a dictionary when fast key-based access matters.

## 2. What is the mutable-default-argument problem?

Default arguments are created once when the function is defined. A mutable default such as `[]` can retain state across calls. Use `None` and create the object inside the function.

## 3. What is the difference between `*args` and `**kwargs`?

`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary.

## 4. What is the difference between `pyenv`, `venv`, and `uv`?

`pyenv` manages Python interpreter versions. `venv` creates isolated environments. `uv` can manage projects, dependencies, lockfiles, Python environments, and command execution.

## 5. Why use Pydantic if Python already has type hints?

Type hints mainly support static analysis and documentation. Pydantic validates and converts data at runtime, which is required for untrusted API input and external responses.

## 6. Composition or inheritance—which should you prefer?

Prefer composition for flexibility and testability. Use inheritance when there is a stable subtype relationship and implementations genuinely obey the parent contract.

## 7. What is dependency inversion in a GenAI service?

The business service depends on an internal interface such as `ChatModel`, not directly on a vendor SDK. Vendor-specific adapters implement that interface.

## 8. When does async improve performance?

When tasks spend time waiting for I/O, such as model APIs, databases, vector search, or external tools. Async increases concurrency and throughput; it does not speed up CPU-heavy work automatically.

## 9. What happens if blocking code runs in an async endpoint?

It blocks the event loop, preventing other coroutines from progressing. Use an async client, move the call to a thread, or execute heavy work in a worker.

## 10. Threads versus processes versus async?

* Async: many I/O-bound operations.
* Threads: blocking I/O or libraries without async support.
* Processes: CPU-bound Python work requiring parallel execution.

## 11. What is a race condition?

A result depends on unpredictable execution order between concurrent operations. Prevent it by avoiding shared mutable state or using atomic operations, locks, transactions, and idempotency.

## 12. When should you use a sliding window?

For contiguous array or string ranges, especially longest, shortest, fixed-size, or “at most K” conditions. A sliding window often reduces `O(n²)` enumeration to `O(n)`.

## 13. When should you use BFS instead of DFS?

Use BFS for level-order traversal and shortest paths in unweighted graphs. Use DFS for deep exploration, cycle detection, connected components, and backtracking.

## 14. What makes a problem suitable for dynamic programming?

It has overlapping subproblems and an answer that can be built from smaller subproblem answers. Define the state, transition, base case, and evaluation order.

## 15. What is the 0/1 knapsack decision?

For each item, either skip it or take it once if capacity permits. The solution chooses the better of those two outcomes.

## 16. What is the repository pattern?

It provides a domain-oriented interface over persistence. Services call operations such as `get_conversation()` rather than writing SQL or ORM queries directly.

## 17. What is API idempotency?

Repeating the same request produces the same intended result. For `POST` operations, an idempotency key can map retries to the original operation rather than creating duplicates.

## 18. Why return `202 Accepted`?

Use it when the request has been accepted but processing will continue asynchronously, such as document ingestion or model-training jobs. Return a job identifier for status polling.

## 19. What is the difference between `401` and `403`?

`401` means authentication is missing or invalid. `403` means the caller is authenticated but lacks permission.

## 20. What is the N+1 query problem?

The application loads a collection with one query and then issues one additional query per item. Solve it with appropriate eager loading, batching, joins, or projections.

## 21. What does ACID mean?

Atomicity, consistency, isolation, and durability. Together they describe important guarantees of relational transactions.

## 22. Why not create an index for every database column?

Indexes consume storage and increase write and maintenance costs. Create them from real query and ordering patterns, then validate with execution plans.

## 23. SQL or NoSQL for conversation history?

SQL is often a strong default because ownership, ordering, relationships, transactions, and auditability matter. A document database may fit when messages are naturally accessed as bounded aggregates and the access pattern supports it.

## 24. What is the hardest part of caching?

Invalidation and consistency. The system needs a policy for expiration, update-time deletion, versioned keys, or event-driven invalidation.

## 25. What is a cache stampede?

Many requests miss the same key and recompute it simultaneously. Use request coalescing, short-lived locks, jittered TTLs, refresh-ahead, or stale-while-revalidate.

## 26. What is the difference between Flat, HNSW, and IVF search?

Flat search is exact but expensive at scale. HNSW uses a navigable graph for fast approximate search. IVF partitions vectors into clusters and searches selected partitions.

## 27. Why is vector metadata important?

It enables tenant filtering, authorization, source attribution, version tracking, document filtering, deletion, and debugging. Vectors without metadata are difficult to operate safely.

## 28. How do you prevent cross-tenant leakage in RAG?

Derive tenant identity from authentication, enforce tenant and ACL filters inside the vector/SQL query, use tenant-aware cache keys, test isolation, and audit retrieval. Never rely only on prompt instructions or post-filtering.

## 29. How should an ingestion pipeline handle retries?

Retry transient failures with exponential backoff and jitter. Make each stage idempotent, persist checkpoints, cap attempts, and send permanently failing jobs to a dead-letter queue.

## 30. What is the difference between a Kubernetes Deployment and Service?

A Deployment manages pod replicas and updates. A Service provides stable networking and load balancing to those changing pods.

---

# 7. Final Day 1 revision checklist

## Python

* [ ] Know collection characteristics and common complexity.
* [ ] Explain mutable default arguments.
* [ ] Know functions, `*args`, and `**kwargs`.
* [ ] Distinguish module, package, and import.
* [ ] Distinguish `pyenv`, `venv`, and `uv`.
* [ ] Explain configuration validation and secret handling.
* [ ] Know exception chaining and cleanup.
* [ ] Write basic `pytest` tests.

## OOP and advanced Python

* [ ] Explain encapsulation, abstraction, inheritance, and polymorphism.
* [ ] Prefer composition for replaceable components.
* [ ] Know class, static, and instance methods.
* [ ] Know properties and dataclasses.
* [ ] Explain type hints versus runtime validation.
* [ ] Create domain-specific exceptions.
* [ ] Use structured logs and correlation IDs.
* [ ] Test dependencies using fixtures and mocks.

## Async and concurrency

* [ ] Explain the event loop.
* [ ] Distinguish coroutine and task.
* [ ] Use `asyncio.gather` carefully.
* [ ] Add timeouts to external calls.
* [ ] Distinguish async, threads, and processes.
* [ ] Recognize blocking code in async handlers.
* [ ] Explain race conditions and shared-state risks.
* [ ] Move long tasks to background workers.

## DSA

* [ ] Explain common Big-O classes.
* [ ] Recognize hashing problems.
* [ ] Recognize prefix-sum problems.
* [ ] Recognize two-pointer and sliding-window clues.
* [ ] Use stacks and queues correctly.
* [ ] Explain DFS versus BFS.
* [ ] State `O(V + E)` for graph traversal.
* [ ] Explain memoization versus tabulation.
* [ ] Explain 0/1 knapsack as take-or-skip.

## Architecture and patterns

* [ ] Explain all five SOLID principles.
* [ ] Map Factory, Strategy, Adapter, Decorator, and Facade to GenAI.
* [ ] Separate API, service, repository, and infrastructure layers.
* [ ] Keep provider-specific objects out of domain logic.
* [ ] Use dependency injection for replaceability and testing.

## HTTP and APIs

* [ ] Know methods and common status codes.
* [ ] Model REST resources with nouns.
* [ ] Explain idempotency.
* [ ] Explain API versioning.
* [ ] Know cursor versus offset pagination.
* [ ] Distinguish API key, JWT, OAuth2, and OpenID Connect.
* [ ] Standardize error responses.
* [ ] Separate liveness and readiness checks.

## Databases

* [ ] Know CRUD and common SQL clauses.
* [ ] Explain joins.
* [ ] Explain transaction and rollback.
* [ ] Explain N+1 queries.
* [ ] Understand primary and foreign keys.
* [ ] Explain normalization versus denormalization.
* [ ] Choose indexes from query patterns.
* [ ] Explain ACID.
* [ ] Test with the production database engine where important.

## Redis, NoSQL, and vectors

* [ ] Explain SQL versus document databases.
* [ ] Know Redis caching, TTL, rate limiting, and locking.
* [ ] Explain read-through caching.
* [ ] Explain cache invalidation and stampedes.
* [ ] Understand embeddings and similarity metrics.
* [ ] Compare Flat, HNSW, and IVF.
* [ ] Store tenant, source, ACL, and version metadata.
* [ ] Never mix incompatible embedding models.

## ETL

* [ ] Explain extract, transform, and load.
* [ ] Compare batch and streaming.
* [ ] Handle pagination and durable checkpoints.
* [ ] Retry only transient errors.
* [ ] Deduplicate using stable identifiers and checksums.
* [ ] Preserve metadata and data lineage.
* [ ] Understand basic PII masking.
* [ ] Make ingestion replayable and idempotent.
* [ ] Publish new index versions atomically.

## Cloud and Kubernetes

* [ ] Map compute, object storage, databases, and Kubernetes across clouds.
* [ ] Know pod, Deployment, Service, and Ingress.
* [ ] Distinguish ConfigMap and Secret.
* [ ] Explain HPA.
* [ ] Compare vertical and horizontal scaling.
* [ ] Explain API Gateway, Layer-7 load balancer, and Layer-4 load balancer.
* [ ] Keep API pods stateless.
* [ ] Scale workers using queue depth.
* [ ] Use resource limits, health checks, and graceful shutdown.

---

# 8. Ultra-short cheat sheet

```text
PYTHON
dict/set lookup: avg O(1)
list search: O(n)
Avoid mutable defaults
Type hints = static contracts
Pydantic = runtime validation
Dataclass = internal value object

OOP
Prefer composition
Depend on interfaces
Adapter hides vendors
Strategy swaps algorithms
Facade simplifies workflows
Decorator adds logging/cache/retries

ASYNC
Async = I/O concurrency
Threads = blocking I/O
Processes = CPU work
Always use timeouts
Bound concurrency
Avoid shared mutable state

DSA
Lookup/count → hash map
Contiguous range → sliding window/prefix sum
Sorted pair → two pointers
Nested matching → stack
Shortest unweighted path → BFS
Deep exploration → DFS
Repeated subproblems → DP

API
POST create/command
PUT replace and idempotent
202 for background jobs
401 unauthenticated
403 unauthorized
409 conflict
429 rate limited
Use idempotency keys
Use cursor pagination at scale

DATABASE
SQL = source of truth
Transaction = atomic unit
N+1 = hidden repeated queries
Indexes speed reads, slow writes
Composite index order matters
ACID = atomicity, consistency, isolation, durability

CACHE
Redis = cache, counters, TTL, locks
Cache invalidation is hard
Tenant must be part of cache key
Protect against cache stampede

VECTOR DB
Embedding = semantic vector
Flat = exact
HNSW = graph ANN
IVF = clustered ANN
Filter tenant inside query
Version embedding and chunking pipelines

ETL
Read → clean → enrich → dedupe → chunk → embed → index
Make stages idempotent
Persist checkpoints
Retry transient failures
Preserve lineage
Atomically publish index versions

CLOUD/K8S
Pod runs workload
Deployment manages replicas
Service provides stable networking
Ingress routes HTTP
HPA scales replicas
Object storage holds raw artifacts
API pods should be stateless
Workers scale from queue depth

SENIOR ANSWER
Requirements → design → source of truth → failure modes
→ scaling → security → observability → trade-offs
```
