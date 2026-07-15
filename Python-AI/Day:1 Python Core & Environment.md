# Day 1 — Python Core & Environment

## 1. Five-line revision summary

* Python’s basic data types represent individual values, while collections organize groups of values.
* Functions divide logic into reusable, testable units; modules and packages organize those functions across([Python documentation][1])Python versions, and `uv` can manage Python versions, environments, dependencies, and project execution.
* Production services should use structured logging, specific exception handling, validated configuration, and clear module boundaries.
* `pytest` verifies individual functions quickly and protects a growing AI codebase from regressions.

---

# 2. Python fundamentals

## 2.1 Variables and dynamic typing

A **variable** is a name that refers to a Python object.

```python
model_name = "text-generation-model"
max_tokens = 500
temperature = 0.2
streaming_enabled = True
```

Python is **dynamically typed**. You do not declare the variable’s type separately:

```python
request_count = 10       # int
request_count = "ten"    # Now it refers to a str
```

Although Python allows this, changing the meaning and type of a variable makes production code harder to understand. Senior engineers therefore use:

* Clear variable names
* Type hints
* Static type checkers
* Small functions with well-defined inputs and outputs

```python
def estimate_cost(token_count: int, price_per_token: float) -> float:
    return token_count * price_per_token
```

Type hints improve readability and tooling, but Python normally does not enforce them at runtime.

---

## 2.2 Basic data types

### `int`

An `int` represents a whole number.

```python
chunk_size = 500
retry_count = 3
document_count = 10_000
```

AI-system examples:

* Number of input tokens
* Number of retrieved documents
* Maximum retry attempts
* Batch size during inference

Be careful not to mix counts with identifiers:

```python
# Although this contains only digits, it is an identifier, not a quantity.
document_id = "001245"
```

Using an integer would remove the leading zeros.

---

### `float`

A `float` represents a number with a fractional component.

```python
temperature = 0.2
similarity_score = 0.873
request_latency_seconds = 1.42
```

AI-system examples:

* LLM temperature
* Embedding similarity score
* Classification probability
* Model latency
* Evaluation metrics

Floating-point values are approximate binary representations. Therefore:

```python
result = 0.1 + 0.2
print(result)  # May print 0.30000000000000004
```

Avoid direct equality comparisons for calculated floats:

```python
import math

assert math.isclose(
    0.1 + 0.2,
    0.3,
    rel_tol=1e-9,
)
```

This matters when testing metrics, probabilities, or normalized scores.

---

### `str`

A `str` represents text. Python strings are immutable, meaning their contents cannot be modified in place.

```python
prompt = "Summarize the following document."
model_name = "enterprise-llm"
document_text = "Employees may carry over ten leave days."
```

Common operations:

```python
query = "  What is the leave policy?  "

clean_query = query.strip()
lower_query = clean_query.lower()
words = clean_query.split()

print(clean_query)
print(words)
```

Formatted strings are useful for readable messages:

```python
model_name = "support-assistant"
latency_ms = 245

message = f"Model {model_name} completed in {latency_ms} ms"
```

### Production warning

Never place untrusted user text directly into:

* SQL queries
* Shell commands
* File paths
* Log templates
* Dynamically evaluated code

Also avoid logging complete prompts or responses when they may contain personal, confidential, or regulated information.

---

### `bool`

A `bool` represents one of two values:

```python
True
False
```

Example:

```python
enable_reranking = True
use_streaming = False
```

Boolean expressions are frequently used in routing:

```python
similarity_score = 0.82
minimum_score = 0.75

should_use_document = similarity_score >= minimum_score
```

Avoid unclear boolean names:

```python
# Unclear
flag = True

# Better
enable_response_caching = True
```

Also avoid string versions of booleans:

```python
# This is a non-empty string, so bool("False") is True.
enable_debug = "False"
```

Configuration values read from environment variables are strings and must be parsed explicitly.

---

## 2.3 Truthy and falsy values

Python treats certain values as false in conditions:

```python
False
None
0
0.0
""
[]
{}
set()
```

Example:

```python
retrieved_documents = []

if not retrieved_documents:
    print("No relevant context was found.")
```

This is convenient, but be precise when `None`, zero, and an empty collection mean different things:

```python
def process_limit(limit: int | None) -> None:
    if limit is None:
        print("No limit was supplied.")
    elif limit == 0:
        print("Processing is disabled.")
```

---

# 3. Python collections

## 3.1 Collection comparison

| Collection |                         Ordered | Mutable |      Duplicates | Typical AI usage                 |
| ---------- | ------------------------------: | ------: | --------------: | -------------------------------- |
| `list`     |                             Yes |     Yes |             Yes | Retrieved chunks, model outputs  |
| `dict`     |                             Yes |     Yes | Keys are unique | Request payloads, metadata       |
| `set`      | Do not rely on positional order |     Yes |              No | Deduplicating IDs or labels      |
| `tuple`    |                             Yes |      No |             Yes | Fixed records and composite keys |

Python’s official tutorial documents these core data structures and their common operations. ([Python documentation][2])ists

A list is an ordered, mutable collection.

```python
documents = [
    "Leave policy",
    "Travel policy",
    "Security policy",
]
```

Accessing elements:

```python
first_document = documents[0]
last_document = documents[-1]
```

Updating:

```python
documents.append("Remote work policy")
documents.remove("Travel policy")
```

### Practical RAG example

```python
retrieved_chunks = [
    {"text": "Employees receive 20 leave days.", "score": 0.91},
    {"text": "Leave must be approved by a manager.", "score": 0.86},
    {"text": "Unused leave may be carried forward.", "score": 0.80},
]

# Sort the same list in place, from highest score to lowest.
retrieved_chunks.sort(
    key=lambda chunk: chunk["score"],
    reverse=True,
)
```

### Common pitfall: shared references

```python
first_list = ["doc-1", "doc-2"]
second_list = first_list

second_list.append("doc-3")

# Both variables refer to the same list.
print(first_list)  # ["doc-1", "doc-2", "doc-3"]
```

Use a copy when independent data is required:

```python
second_list = first_list.copy()
```

---

## 3.3 Dictionaries

A dictionary stores key-value pairs.

```python
request_payload = {
    "query": "What is the leave policy?",
    "top_k": 5,
    "stream": False,
}
```

Reading values:

```python
query = request_payload["query"]
top_k = request_payload.get("top_k", 3)
```

Difference:

* `payload["key"]` raises `KeyError` when the key is missing.
* `payload.get("key")` returns `None`, or a supplied default.

Updating:

```python
request_payload["user_id"] = "user-123"
request_payload["top_k"] = 10
```

### AI metadata example

```python
chunk_metadata = {
    "document_id": "policy-101",
    "page": 4,
    "department": "HR",
    "access_level": "internal",
}
```

Use dictionaries for flexible records, but avoid passing unvalidated dictionaries throughout a large system. Typed models or dataclasses are safer for important domain objects.

---

## 3.4 Sets

A set stores unique values.

```python
document_ids = {
    "doc-101",
    "doc-102",
    "doc-101",
}

print(document_ids)  # Duplicate value is retained only once.
```

Useful operations:

```python
authorized_departments = {"HR", "Legal", "Finance"}
user_departments = {"Engineering", "Finance"}

allowed_matches = authorized_departments & user_departments
```

RAG use cases:

* Deduplicating retrieved document IDs
* Comparing user permissions with document permissions
* Collecting unique model labels
* Detecting already-processed records

### Pitfall

Do not use a set when output order is important. Convert the result to a sorted list when deterministic output is required:

```python
sorted_document_ids = sorted(document_ids)
```

Determinism is valuable in tests, logs, caching, and evaluation pipelines.

---

## 3.5 Tuples

A tuple is an ordered, immutable collection.

```python
model_identifier = ("provider-a", "model-v2")
```

Tuple unpacking:

```python
provider, model_name = model_identifier
```

Useful cases:

* Returning a small fixed group of values
* Dictionary keys composed of multiple fields
* Coordinates or fixed dimensions
* Records that should not be modified accidentally

```python
cache_key = (
    "model-v2",
    "prompt-template-v4",
    "document-set-12",
)
```

For complex domain data, prefer a dataclass or typed model over a large tuple because named fields are easier to understand.

---

# 4. Comprehensions and slicing

## 4.1 List comprehensions

A list comprehension creates a list by transforming or filtering another iterable.

```python
scores = [0.91, 0.42, 0.87, 0.61]

high_scores = [
    score
    for score in scores
    if score >= 0.75
]
```

Equivalent normal loop:

```python
high_scores = []

for score in scores:
    if score >= 0.75:
        high_scores.append(score)
```

### RAG example

```python
chunks = [
    {"id": "c1", "score": 0.92},
    {"id": "c2", "score": 0.55},
    {"id": "c3", "score": 0.84},
]

relevant_ids = [
    chunk["id"]
    for chunk in chunks
    if chunk["score"] >= 0.80
]
```

### Best practice

Use comprehensions only when they remain easy to understand.

Avoid:

```python
# Too much filtering, conversion and conditional logic in one expression.
results = [
    transform(x)
    for x in items
    if valid(x) and authorized(x) and not expired(x)
]
```

A normal loop may be easier to debug and log.

---

## 4.2 Dictionary comprehensions

```python
model_latencies = {
    "model-a": 125,
    "model-b": 240,
    "model-c": 180,
}

latencies_in_seconds = {
    model: latency_ms / 1000
    for model, latency_ms in model_latencies.items()
}
```

Indexing documents by ID:

```python
documents = [
    {"id": "doc-1", "text": "Leave policy"},
    {"id": "doc-2", "text": "Travel policy"},
]

documents_by_id = {
    document["id"]: document
    for document in documents
}
```

### Pitfall

Duplicate keys overwrite previous values:

```python
records = [
    {"id": "doc-1", "version": 1},
    {"id": "doc-1", "version": 2},
]

records_by_id = {
    record["id"]: record
    for record in records
}

# Only version 2 remains.
```

Decide whether overwriting is intentional.

---

## 4.3 Slicing

Slicing selects part of a sequence.

```python
items[start:stop:step]
```

The `stop` position is excluded.

```python
documents = ["d0", "d1", "d2", "d3", "d4"]

print(documents[1:4])   # ["d1", "d2", "d3"]
print(documents[:3])    # First three
print(documents[2:])    # From index 2 onward
print(documents[-2:])   # Last two
print(documents[::2])   # Every second item
print(documents[::-1])  # Reversed copy
```

### Retrieval example

```python
ranked_chunks = ["chunk-a", "chunk-b", "chunk-c", "chunk-d"]

top_k = 3
selected_chunks = ranked_chunks[:top_k]
```

### Pitfall

Slicing a list creates a shallow copy. Nested mutable objects are still shared.

---

# 5. Functions

## 5.1 Defining a function

```python
def build_prompt(query: str, context: str) -> str:
    """Create a grounded question-answering prompt."""
    return (
        "Answer using only the supplied context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}"
    )
```

A strong production function should have:

* One clear responsibility
* Descriptive name
* Typed parameters
* Predictable return value
* Explicit handling of invalid input
* Limited side effects
* A docstring when the behavior is not obvious

---

## 5.2 Parameters and return values

```python
def calculate_average(values: list[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")

    return sum(values) / len(values)
```

Validation near the boundary prevents confusing errors later.

---

## 5.3 Positional and keyword arguments

```python
def retrieve_documents(
    query: str,
    top_k: int = 5,
    use_reranker: bool = True,
) -> list[str]:
    return []
```

Calls:

```python
retrieve_documents("leave policy")

retrieve_documents(
    "leave policy",
    top_k=10,
    use_reranker=False,
)
```

Keyword arguments are clearer when several parameters have similar types.

---

## 5.4 Default argument pitfall

Never use a mutable object as a default value unless shared state is intentionally required.

```python
# Incorrect
def add_document(document: str, documents: list[str] = []) -> list[str]:
    documents.append(document)
    return documents
```

The same list is reused across calls.

Correct pattern:

```python
def add_document(
    document: str,
    documents: list[str] | None = None,
) -> list[str]:
    # Create a fresh list for each call when none is supplied.
    if documents is None:
        documents = []

    documents.append(document)
    return documents
```

---

## 5.5 `*args`

`*args` collects additional positional arguments into a tuple.

```python
def combine_contexts(*contexts: str) -> str:
    # `contexts` is a tuple containing every positional argument.
    non_empty_contexts = [
        context.strip()
        for context in contexts
        if context.strip()
    ]

    return "\n\n".join(non_empty_contexts)
```

Usage:

```python
combined = combine_contexts(
    "Leave policy text",
    "Manager approval text",
    "Carry-forward policy text",
)
```

Use `*args` when the number of homogeneous arguments is genuinely variable.

Do not use it simply to avoid defining a clear interface.

---

## 5.6 `**kwargs`

`**kwargs` collects additional keyword arguments into a dictionary.

```python
def create_model_request(
    prompt: str,
    **generation_options: object,
) -> dict[str, object]:
    return {
        "prompt": prompt,
        "options": generation_options,
    }
```

Usage:

```python
request = create_model_request(
    "Summarize this document.",
    temperature=0.2,
    max_tokens=300,
    stream=False,
)
```

A common forwarding pattern:

```python
def call_provider(**options: object) -> None:
    provider_client.generate(**options)
```

### Production warning

Excessive `**kwargs` usage hides the function contract:

```python
# Caller cannot easily see which options are valid.
def process_request(**kwargs: object) -> None:
    ...
```

For core business logic, explicit parameters or typed configuration objects are better.

---

## 5.7 Pure functions and side effects

A **pure function**:

* Depends only on its arguments
* Does not change external state
* Returns the same output for the same input

```python
def normalize_score(score: float) -> float:
    return max(0.0, min(score, 1.0))
```

A function with side effects may:

* Write to a database
* Call an LLM API
* Modify a global object
* Send a message
* Write a file

Separating pure logic from side effects makes code easier to test.

```python
def create_prompt(query: str, context: str) -> str:
    # Pure transformation.
    return f"Context: {context}\nQuestion: {query}"


def generate_answer(client: object, prompt: str) -> str:
    # External network call: side effect.
    return client.generate(prompt)
```

---

# 6. Modules, packages, and imports

## 6.1 Module

A **module** is usually one Python file.

```text
retrieval.py
```

```python
# retrieval.py

def retrieve(query: str) -> list[str]:
    return []
```

Importing it:

```python
from retrieval import retrieve
```

---

## 6.2 Package

A **package** groups related modules in a directory.

```text
ai_service/
├── __init__.py
├── retrieval.py
├── generation.py
└── evaluation.py
```

Usage:

```python
from ai_service.retrieval import retrieve
```

Packages help establish architectural boundaries:

* `retrieval` finds relevant information.
* `generation` communicates with the LLM.
* `evaluation` scores outputs.
* `api` handles HTTP requests.
* `config` loads application settings.

---

## 6.3 Import best practices

Prefer imports at the top of the file:

```python
import logging
import os

from dotenv import load_dotenv

from ai_service.retrieval import retrieve
```

Typical ordering:

1. Standard-library imports
2. Third-party imports
3. Internal application imports

Prefer absolute imports in large codebases:

```python
from ai_service.clients.llm import LLMClient
```

Avoid wildcard imports:

```python
# Avoid
from ai_service.utils import *
```

They hide where names come from and can create collisions.

---

## 6.4 Avoid import-time side effects

Bad design:

```python
# This API call happens merely because the module is imported.
client = create_client()
client.connect()
```

Better:

```python
def create_llm_client() -> object:
    return LLMClient()
```

Imports should generally define classes, constants, and functions—not start servers, connect to databases, or call remote models.

---

## 6.5 Circular imports

A circular import occurs when modules depend on one another:

```text
retrieval.py imports generation.py
generation.py imports retrieval.py
```

This often indicates unclear architectural boundaries.

Strategies:

* Move shared types into a third module.
* Depend on interfaces rather than concrete implementations.
* Separate orchestration from lower-level components.
* Avoid putting unrelated utilities into one large module.

---

# 7. Environment and tooling

## 7.1 Why environment isolation matters

Two Python projects may require incompatible package versions:

```text
Project A requires package-x 1.x
Project B requires package-x 2.x
```

A virtual environment gives each project an isolated package installation.

This prevents:

* Dependency conflicts
* Accidental reliance on globally installed packages
* “Works on my machine” problems
* Inconsistent local and CI behavior

---

## 7.2 `venv`

`venv` is Python’s built-in virtual-environment tool. It creates an environment using the Python interpreter with which the command is run. ([Python documentation][1])ironment:

```bash
python -m venv .venv
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install pytest python-dotenv
```

Deactivate:

```bash
deactivate
```

### Why use `python -m pip`?

It ensures that `pip` belongs to the currently selected Python interpreter.

### Best use case

Use `venv` when:

* You want standard-library tooling.
* The project has a simple dependency workflow.
* The organization already uses `pip` and requirement files.
* Maximum compatibility is more important than advanced project management.

---

## 7.3 `pyenv`

`pyenv` manages multiple Python versions and selects which interpreter should run. It is not, by itself, the same thing as a dependency-isolated virtual environment. ([GitHub][3])low:

```bash
# View available versions.
pyenv install --list

# Install a Python version.
pyenv install 3.13.5

# Set the version for the current project.
pyenv local 3.13.5

# Verify the selected version.
python --version
```

`pyenv local` normally creates or updates a `.python-version` file. Pyenv checks project-level and global version settings to determine which Python interpreter to use. ([GitHub][4])case

Use `pyenv` when:

* Different projects require different Python versions.
* You test a library against several Python versions.
* Your operating system’s Python must remain untouched.
* Your team explicitly standardizes interpreter selection with `.python-version`.

A common combination is:

```text
pyenv → selects Python 3.x
venv  → isolates that project’s packages
```

---

## 7.4 `uv`

`uv` is a Python package and project manager. Its current tooling supports project creation, dependency management, virtual environments, command execution, locking and Python-version management. ([Astral Docs][5])ect:

```bash
uv init ai-service
cd ai-service
```

Add dependencies:

```bash
uv add python-dotenv
uv add --dev pytest
```

Run the application:

```bash
uv run python -m ai_service.main
```

Run tests:

```bash
uv run pytest
```

Synchronize the environment with the project definition and lockfile:

```bash
uv sync
```

Install or request Python versions:

```bash
uv python install 3.13
uv python list
```

Uv uses virtual environments for project isolation and can run commands without manually activating the environment through `uv run`. ([Astral Docs][6])case

Use `uv` when:

* Starting a modern greenfield Python project
* Fast dependency resolution is useful
* You want one tool for environments, dependencies and execution
* Reproducible lockfiles are required
* The organization has approved and standardized it

---

## 7.5 Tool comparison

| Need                           |                `venv` |               `pyenv` |                       `uv` |
| ------------------------------ | --------------------: | --------------------: | -------------------------: |
| Isolate project packages       |                   Yes |  Not its primary role |                        Yes |
| Select/install Python versions |                    No |                   Yes |                        Yes |
| Add and resolve dependencies   |        Use with `pip` |                    No |                        Yes |
| Project lockfile workflow      |                    No |                    No |                        Yes |
| Included with Python           |                   Yes |                    No |                         No |
| Best mental model              | Environment isolation | Interpreter selection | Integrated project tooling |

### Practical recommendation

For interview discussions:

* Explain the responsibilities before naming a preferred tool.
* Do not say that `pyenv`, `venv`, and `uv` are identical alternatives.
* Mention that team consistency is more valuable than individual tool preference.
* Ensure local development, CI and deployment use compatible Python and dependency versions.

---

# 8. Production project layout

A practical service layout:

```text
rag-service/
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   └── rag_service/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── logging_config.py
│       │
│       ├── api/
│       │   └── routes.py
│       │
│       ├── clients/
│       │   ├── llm_client.py
│       │   └── vector_client.py
│       │
│       ├── services/
│       │   ├── retrieval.py
│       │   ├── generation.py
│       │   └── rag_service.py
│       │
│       └── domain/
│           └── models.py
│
└── tests/
    ├── unit/
    │   ├── test_retrieval.py
    │   └── test_generation.py
    └── integration/
        └── test_rag_workflow.py
```

## Why this structure works

* `api/`: HTTP-specific code
* `clients/`: wrappers around external systems
* `services/`: application use cases and orchestration
* `domain/`: important business objects and rules
* `config.py`: validated configuration
* `logging_config.py`: centralized log setup
* `tests/unit/`: fast isolated tests
* `tests/integration/`: tests involving multiple components

### Senior-engineer principle

Organize code around responsibilities and change boundaries, not around arbitrary file size.

For example, do not create a generic `utils.py` containing unrelated:

* Prompt formatting
* Database operations
* Date conversion
* Authentication
* Token counting
* HTTP retries

Such files eventually become difficult to maintain.

---

# 9. Configuration with `.env`

## 9.1 What `.env` solves

Environment variables keep deployment-specific configuration outside application code.

Example `.env`:

```dotenv
APP_ENV=development
LOG_LEVEL=INFO
LLM_MODEL=model-v2
LLM_API_KEY=local-development-key
REQUEST_TIMEOUT_SECONDS=30
```

`python-dotenv` reads key-value pairs from a `.env` file and can add them to `os.environ`. By default, `load_dotenv()` does not overwrite existing environment variables. ([PyPI][7])ort os

from dotenv import load_dotenv

# Load local development values from .env when the file exists.

load_dotenv()

model_name = os.getenv("LLM_MODEL", "default-model")

````

---

## 9.2 Validate required values

Do not let a missing API key fail much later during a request.

```python
import os

from dotenv import load_dotenv

load_dotenv()


def require_environment_variable(name: str) -> str:
    """Read a required setting and fail clearly when it is unavailable."""
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(
            f"Required environment variable {name!r} is not configured"
        )

    return value


LLM_API_KEY = require_environment_variable("LLM_API_KEY")
````

---

## 9.3 Parse types explicitly

All environment variables begin as strings.

```python
import os


def read_positive_integer(name: str, default: int) -> int:
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    try:
        parsed_value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(
            f"{name} must contain an integer, received {raw_value!r}"
        ) from exc

    if parsed_value <= 0:
        raise RuntimeError(f"{name} must be greater than zero")

    return parsed_value
```

Boolean parser:

```python
def read_boolean(name: str, default: bool = False) -> bool:
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    normalized_value = raw_value.strip().lower()

    if normalized_value in {"true", "1", "yes", "on"}:
        return True

    if normalized_value in {"false", "0", "no", "off"}:
        return False

    raise RuntimeError(
        f"{name} must be a valid boolean value"
    )
```

---

## 9.4 Security practices

* Put `.env` in `.gitignore`.
* Commit `.env.example` containing names but no real secrets.
* Never log API keys, passwords, tokens or connection strings.
* Do not place production secrets in repository files.
* Inject production configuration through the deployment platform.
* Use a managed secret store for sensitive production credentials.
* Rotate leaked credentials immediately.

The `python-dotenv` project specifically recommends excluding `.env` from version control when it contains secrets. ([PyPI][7])dotenv

# .env.example

LLM_API_KEY=
LLM_MODEL=
LOG_LEVEL=INFO
REQUEST_TIMEOUT_SECONDS=30

````

---

# 10. Logging

## 10.1 Why logging instead of `print`

`print()` is useful for temporary local experimentation.

Logging supports:

- Severity levels
- Timestamps
- Module names
- Central formatting
- Filtering
- Production log collection
- Error stack traces
- Request correlation

Python provides standard logging levels such as `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. The recommended module-level pattern is `logging.getLogger(__name__)`. :contentReference[oaicite:18]{index=18}Basic logging pattern

```python
import logging

logger = logging.getLogger(__name__)


def retrieve_documents(query: str) -> list[str]:
    logger.info(
        "Starting document retrieval query_length=%s",
        len(query),
    )

    documents = ["doc-1", "doc-2"]

    logger.info(
        "Document retrieval completed result_count=%s",
        len(documents),
    )

    return documents
````

Configure logging in the application entry point:

```python
import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(name)s "
            "%(message)s"
        ),
    )
```

Avoid calling `basicConfig()` independently in every module.

---

## 10.3 Log levels

### `DEBUG`

Detailed diagnostic information:

```python
logger.debug(
    "Reranker scores calculated candidate_count=%s",
    len(candidates),
)
```

### `INFO`

Normal lifecycle events:

```python
logger.info(
    "Request completed model=%s latency_ms=%s",
    model_name,
    latency_ms,
)
```

### `WARNING`

Unexpected but recoverable situations:

```python
logger.warning(
    "Primary model unavailable; using fallback model"
)
```

### `ERROR`

An operation failed:

```python
logger.error(
    "Document ingestion failed document_id=%s",
    document_id,
)
```

Use `logger.exception()` inside an exception handler when a stack trace is needed:

```python
try:
    index_document(document)
except IndexingError:
    logger.exception(
        "Indexing failed document_id=%s",
        document.id,
    )
    raise
```

---

## 10.4 Parameterized logging

Prefer:

```python
logger.info(
    "Generated answer token_count=%s",
    token_count,
)
```

Over:

```python
logger.info(f"Generated answer token_count={token_count}")
```

The parameterized form allows the logging framework to defer string formatting when the log level is disabled.

---

## 10.5 What to include in production logs

Useful fields:

* Request ID
* Trace ID
* Model name and version
* Prompt-template version
* Retrieval result count
* Token counts
* Latency
* Retry count
* Error category
* Status code

Example:

```python
logger.info(
    "RAG request completed request_id=%s model=%s "
    "retrieved_count=%s latency_ms=%s",
    request_id,
    model_name,
    len(documents),
    latency_ms,
)
```

Avoid logging:

* Raw API keys
* Authorization headers
* Passwords
* Full personal records
* Unredacted prompts containing confidential data
* Complete document content without an approved reason

---

# 11. Error handling

## 11.1 Basic `try/except`

```python
def parse_top_k(raw_value: str) -> int:
    try:
        top_k = int(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"top_k must be an integer, received {raw_value!r}"
        ) from exc

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    return top_k
```

The `from exc` syntax preserves the original failure as the cause.

---

## 11.2 Catch specific exceptions

Avoid:

```python
try:
    call_model()
except Exception:
    return ""
```

Problems:

* Hides programming bugs
* Loses important debugging information
* Makes failed requests appear successful
* Converts many different failures into an ambiguous empty string

Better:

```python
try:
    response = call_model()
except ModelTimeoutError as exc:
    logger.warning("Model request timed out")
    raise ServiceUnavailableError(
        "The model service did not respond in time"
    ) from exc
```

Catch an exception only when you can:

* Recover
* Add useful context
* Translate it at an architectural boundary
* Log it once at the correct layer
* Perform cleanup

---

## 11.3 `else`

The `else` block runs only when the `try` block succeeds.

```python
try:
    payload = parse_json(raw_response)
except InvalidJSONError:
    logger.error("Provider returned invalid JSON")
else:
    logger.info(
        "Provider response parsed key_count=%s",
        len(payload),
    )
```

Keeping only the risky operation inside `try` makes exception handling more precise.

---

## 11.4 `finally`

`finally` runs whether or not an exception occurs and is intended for cleanup. ([Python documentation][8])nection = database.connect()

try:
connection.execute("...")
finally:
connection.close()

````

Usually prefer a context manager where available:

```python
with database.connect() as connection:
    connection.execute("...")
````

Context managers express resource ownership more clearly.

---

## 11.5 Custom exceptions

```python
class RetrievalError(Exception):
    """Base exception for retrieval failures."""


class VectorStoreUnavailableError(RetrievalError):
    """Raised when the vector store cannot be reached."""


class InvalidRetrievalQueryError(RetrievalError):
    """Raised when a retrieval request is invalid."""
```

Custom exceptions let higher layers respond appropriately:

```python
try:
    documents = retriever.search(query)
except InvalidRetrievalQueryError:
    return client_error_response()
except VectorStoreUnavailableError:
    return temporary_service_error_response()
```

---

## 11.6 Retrying errors

Retry only failures likely to be temporary:

Good retry candidates:

* Network timeout
* Rate limit response
* Temporary provider unavailability
* Short-lived database connection failure

Poor retry candidates:

* Invalid API key
* Invalid request schema
* Prompt exceeds a known hard limit
* Permission denied
* Programming error

Retries should normally include:

* Maximum attempts
* Exponential backoff
* Jitter
* Timeout
* Logging
* Metrics
* Idempotency awareness

Do not place an unlimited retry loop around an LLM call.

---

# 12. Testing with `pytest`

## 12.1 Why unit tests matter

A **unit test** checks a small unit of behavior, usually a function or class, in isolation.

For GenAI applications, many parts are still deterministic:

* Prompt construction
* Input validation
* Configuration parsing
* Metadata filters
* Chunk selection
* Score normalization
* Permission rules
* Output parsing

Test these directly instead of calling a real LLM in every test.

Pytest discovers conventionally named test files and test functions and uses normal Python `assert` statements. It scales from small unit tests to larger testing workflows. ([pytest][9])Basic test structure

Application code:

```python
# src/rag_service/scoring.py

def normalize_score(score: float) -> float:
    """Constrain a score to the inclusive range 0.0–1.0."""
    if score < 0.0:
        return 0.0

    if score > 1.0:
        return 1.0

    return score
```

Tests:

```python
# tests/unit/test_scoring.py

from rag_service.scoring import normalize_score


def test_normalize_score_keeps_valid_score() -> None:
    # A score already inside the valid range should be unchanged.
    assert normalize_score(0.75) == 0.75


def test_normalize_score_caps_high_value() -> None:
    # Values above one should be capped at the maximum.
    assert normalize_score(1.4) == 1.0


def test_normalize_score_caps_negative_value() -> None:
    # Negative values should be raised to the minimum.
    assert normalize_score(-0.2) == 0.0
```

Run:

```bash
pytest
```

Or with uv:

```bash
uv run pytest
```

---

## 12.3 Testing exceptions

Application code:

```python
def calculate_average(values: list[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")

    return sum(values) / len(values)
```

Test:

```python
import pytest

from rag_service.metrics import calculate_average


def test_calculate_average_rejects_empty_list() -> None:
    with pytest.raises(
        ValueError,
        match="values must not be empty",
    ):
        calculate_average([])
```

This verifies both the exception type and the useful error message.

---

## 12.4 Test one behavior at a time

Prefer:

```python
def test_build_prompt_includes_question() -> None:
    ...


def test_build_prompt_includes_context() -> None:
    ...


def test_build_prompt_rejects_empty_question() -> None:
    ...
```

Over one large test containing many unrelated conditions.

When a small test fails, the cause is easier to locate.

---

## 12.5 Arrange–Act–Assert

A useful test structure:

```python
def test_select_relevant_chunks() -> None:
    # Arrange: prepare input.
    chunks = [
        {"id": "c1", "score": 0.91},
        {"id": "c2", "score": 0.40},
    ]

    # Act: execute the behavior being tested.
    result = select_relevant_chunks(
        chunks,
        minimum_score=0.80,
    )

    # Assert: verify the observable outcome.
    assert result == [{"id": "c1", "score": 0.91}]
```

---

## 12.6 Unit tests versus integration tests

### Unit test

* Tests one small component
* Fast
* No real network call
* No production database
* Failure is easy to diagnose

### Integration test

* Tests components working together
* May use a test database or local service
* Slower
* Verifies contracts and configuration

### End-to-end test

* Tests the complete user flow
* Slowest and most expensive
* Useful in smaller numbers

A healthy test suite normally has many unit tests and fewer integration and end-to-end tests.

---

# 13. Mini production-style example

## Application code

```python
# src/rag_service/retrieval.py

import logging
from typing import Any

logger = logging.getLogger(__name__)


class InvalidQueryError(ValueError):
    """Raised when a retrieval query is empty."""


def select_relevant_chunks(
    chunks: list[dict[str, Any]],
    minimum_score: float,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Filter, sort and limit retrieved chunks.

    Flow:
    1. Validate configuration.
    2. Keep only chunks meeting the score threshold.
    3. Sort the remaining chunks from best to worst.
    4. Return at most `top_k` results.
    """
    if not 0.0 <= minimum_score <= 1.0:
        raise ValueError(
            "minimum_score must be between 0.0 and 1.0"
        )

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    relevant_chunks = [
        chunk
        for chunk in chunks
        if float(chunk.get("score", 0.0)) >= minimum_score
    ]

    # sorted() returns a new list and leaves the caller's list unchanged.
    ranked_chunks = sorted(
        relevant_chunks,
        key=lambda chunk: float(chunk.get("score", 0.0)),
        reverse=True,
    )

    selected_chunks = ranked_chunks[:top_k]

    logger.info(
        "Selected relevant chunks input_count=%s "
        "selected_count=%s threshold=%s top_k=%s",
        len(chunks),
        len(selected_chunks),
        minimum_score,
        top_k,
    )

    return selected_chunks
```

## Tests

```python
# tests/unit/test_retrieval.py

import pytest

from rag_service.retrieval import select_relevant_chunks


def test_select_relevant_chunks_filters_sorts_and_limits() -> None:
    chunks = [
        {"id": "c1", "score": 0.81},
        {"id": "c2", "score": 0.95},
        {"id": "c3", "score": 0.40},
        {"id": "c4", "score": 0.88},
    ]

    result = select_relevant_chunks(
        chunks,
        minimum_score=0.80,
        top_k=2,
    )

    # c2 and c4 are the two highest-scoring valid chunks.
    assert [chunk["id"] for chunk in result] == ["c2", "c4"]


def test_select_relevant_chunks_does_not_modify_input() -> None:
    chunks = [
        {"id": "c1", "score": 0.81},
        {"id": "c2", "score": 0.95},
    ]
    original_order = chunks.copy()

    select_relevant_chunks(
        chunks,
        minimum_score=0.0,
    )

    assert chunks == original_order


def test_select_relevant_chunks_rejects_invalid_top_k() -> None:
    with pytest.raises(
        ValueError,
        match="top_k must be greater than zero",
    ):
        select_relevant_chunks(
            [],
            minimum_score=0.5,
            top_k=0,
        )
```

This example combines:

* Lists and dictionaries
* Comprehensions
* Slicing
* Functions and type hints
* Logging
* Validation and exceptions
* Unit testing

---

# 14. Real-world AI/ML examples

## Example 1: Model-serving API

A model-serving backend receives JSON:

```python
request = {
    "prompt": "Summarize the report",
    "temperature": 0.2,
    "max_tokens": 300,
}
```

Python concepts involved:

* `dict` for the request payload
* `str`, `float`, `int` for individual fields
* Functions for validation and model invocation
* Environment variables for provider credentials
* Logging for latency, model version and failures
* Exception handling for timeout or rate-limit errors
* Pytest for request validation and response parsing

Production strategy:

```text
HTTP layer
    → validates request
    → service function
    → provider client
    → translates provider response
    → returns stable API schema
```

Do not allow provider-specific dictionaries and exceptions to spread throughout the application.

---

## Example 2: RAG retrieval service

A RAG system may retrieve a list of chunk dictionaries:

```python
chunks = [
    {
        "document_id": "policy-1",
        "text": "Employees receive 20 leave days.",
        "score": 0.91,
    },
    {
        "document_id": "policy-2",
        "text": "Travel requests require approval.",
        "score": 0.37,
    },
]
```

Python concepts involved:

* Lists for ranked candidates
* Dictionaries for chunk metadata
* Sets for document deduplication
* Tuples for cache keys
* Comprehensions for score filtering
* Slicing for top-k selection
* Functions for prompt construction
* Tests for threshold and ordering logic

Senior-level concern:

A high similarity score does not automatically prove that a chunk is correct or authorized. Retrieval must also apply metadata filters, access control and evaluation.

---

## Example 3: Document-ingestion pipeline

A pipeline may:

1. Read documents.
2. Extract text.
3. Divide text into chunks.
4. Attach metadata.
5. Generate embeddings.
6. Store vectors.
7. Record failures.

Python concepts involved:

```python
processed_ids: set[str] = set()
failed_documents: list[dict[str, str]] = []
metadata_by_id: dict[str, dict[str, object]] = {}
```

Error strategy:

```python
for document in documents:
    try:
        process_document(document)
    except UnsupportedFormatError as exc:
        logger.warning(
            "Skipping unsupported document id=%s error=%s",
            document.id,
            exc,
        )
    except TemporaryEmbeddingError:
        # Send to a retry queue rather than silently losing the document.
        enqueue_for_retry(document)
```

A production ingestion pipeline should make partial failures visible instead of stopping the entire batch or silently dropping records.

---

# 15. Senior AI Engineer best practices

## Writing robust Python services

* Validate inputs at system boundaries.
* Use type hints for public functions and important domain objects.
* Separate pure transformations from network and database operations.
* Set explicit timeouts for every external call.
* Catch narrow exception types.
* Preserve exception chains using `raise ... from exc`.
* Avoid mutable default arguments and uncontrolled global state.
* Make operations idempotent where retries are possible.
* Use dependency injection for clients so code can be tested.
* Keep configuration external and validate it during startup.

---

## Working in large codebases

* Define clear ownership boundaries between API, service, client and domain code.
* Prefer small, cohesive modules over large miscellaneous files.
* Avoid circular imports and hidden import-time side effects.
* Maintain stable interfaces between modules.
* Hide third-party SDK details behind internal adapters.
* Add tests before refactoring critical behavior.
* Use consistent formatting, linting and type checking.
* Keep functions readable; do not compress complicated logic into comprehensions.
* Document important architectural decisions and non-obvious trade-offs.

---

## Building production GenAI systems

* Treat prompts as versioned application artifacts.
* Log model and prompt-template versions.
* Track token usage, latency, retries and provider errors.
* Do not log confidential prompts or responses by default.
* Validate structured LLM output before using it.
* Enforce authorization before retrieving private documents.
* Distinguish deterministic application failures from probabilistic model-quality problems.
* Test deterministic code without calling a live LLM.
* Use mocked or fake clients for unit tests.
* Maintain a smaller set of integration tests against real providers.
* Implement fallback and retry policies deliberately.
* Set cost, token and concurrency limits.
* Never treat an LLM-generated answer as trusted executable input.

---

# 16. Common pitfalls

## Python pitfalls

* Using mutable default arguments
* Modifying a list while iterating over it
* Using `is` instead of `==` for value comparison
* Assuming floats compare exactly
* Confusing `None`, zero and an empty collection
* Writing deeply nested comprehensions
* Catching every exception with `except Exception`
* Returning `None` or empty strings for all failures
* Depending on global mutable variables
* Importing the same module under inconsistent paths

## Environment pitfalls

* Installing packages globally
* Forgetting which Python interpreter is active
* Committing `.env`
* Allowing local undeclared dependencies
* Failing to lock dependency versions
* Using different Python versions in local development and CI
* Treating `pyenv` as identical to a virtual environment

## Logging pitfalls

* Logging secrets
* Logging complete prompts containing personal information
* Logging the same exception in multiple layers
* Using `ERROR` for normal application behavior
* Omitting request or trace identifiers
* Using only free-form messages that are difficult to search

## Testing pitfalls

* Calling a real LLM in every unit test
* Testing implementation details instead of behavior
* Sharing mutable state between tests
* Depending on test execution order
* Writing nondeterministic tests
* Comparing floats with strict equality
* Mocking so much that no meaningful behavior remains
* Having only happy-path tests

---

# 17. Interview Q&A

## 1. What is the difference between a list and a tuple?

A list is mutable, while a tuple is immutable. Use a list for a collection that changes, such as retrieved chunks. Use a tuple for a fixed grouping, such as a composite cache key. Immutability can make intent clearer and allows suitable tuples to be used as dictionary keys.

---

## 2. When would you use a set in a RAG pipeline?

A set is useful for deduplicating document IDs, tracking processed chunks and comparing user permissions with document-access labels. I would not rely on set iteration order; I would sort the output when deterministic behavior matters.

---

## 3. What is the mutable-default-argument problem?

Default arguments are evaluated when the function is defined, not separately for every call. Therefore, a default list or dictionary can be shared across calls. The normal solution is to use `None` as the default and create a new object inside the function.

---

## 4. What is the difference between `*args` and `**kwargs`?

`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. They are useful for flexible wrappers, but overusing them hides the function’s contract. Core service APIs should generally use explicit typed parameters.

---

## 5. What is the difference between a module and a package?

A module is generally one Python file. A package is a directory that groups related modules under a namespace. In a production AI service, packages might represent API handling, retrieval, generation, external clients and evaluation.

---

## 6. How do `venv`, `pyenv`, and `uv` differ?

`venv` isolates packages for a project using an existing Python interpreter. `pyenv` installs or selects Python interpreter versions. `uv` provides an integrated workflow for Python versions, virtual environments, dependencies, lockfiles and project commands. They solve overlapping but not identical problems.

---

## 7. Why should production code use logging instead of `print`?

Logging supports severity levels, timestamps, module names, filtering, centralized collection and stack traces. It also enables structured operational fields such as request ID, model version, latency and token usage. `print` is more appropriate for simple command-line output or temporary debugging.

---

## 8. When should an exception be caught?

Catch an exception when the current layer can recover, add meaningful context, translate it into a domain-level exception, perform cleanup or convert it into an API response. Do not catch an exception merely to hide it. Unexpected programming errors should usually propagate to centralized error handling.

---

## 9. How would you test an LLM application without making every test expensive and unreliable?

I would separate deterministic logic from provider calls. Prompt building, validation, metadata filtering, chunk ranking and output parsing would have fast unit tests. The LLM client would be replaced with a fake or mock in those tests. A smaller integration suite would verify the real provider contract.

---

## 10. What makes a Python AI service production-ready?

It needs validated configuration, dependency isolation, clear architecture, type hints, specific error handling, timeouts, controlled retries, structured logging, security controls, unit and integration tests, observability, reproducible dependencies and safe handling of prompts, responses and credentials.

---

# 18. Final revision checklist

Before completing Day 1, make sure you can explain and demonstrate:

* The difference between `int`, `float`, `str` and `bool`
* When to choose a list, dictionary, set or tuple
* How comprehensions and slicing work
* Why mutable default arguments are dangerous
* How `*args` and `**kwargs` work
* The difference between modules and packages
* The different responsibilities of `venv`, `pyenv` and `uv`
* A clean Python service folder structure
* How `.env` values are loaded, parsed and secured
* How to configure and use module-level loggers
* Why narrow exception handling is safer
* How to write and execute a simple `pytest` unit test
* How these foundations support model APIs, RAG services and ingestion pipelines

[1]: https://docs.python.org/3/tutorial/venv.html?utm_source=chatgpt.com "12. Virtual Environments and Packages"
[2]: https://docs.python.org/3/tutorial/index.html?utm_source=chatgpt.com "The Python Tutorial — Python 3.14.6 documentation"
[3]: https://github.com/pyenv/pyenv?utm_source=chatgpt.com "Simple Python Version Management: pyenv"
[4]: https://github.com/pyenv/pyenv/blob/master/README.md?plain=1&utm_source=chatgpt.com "pyenv/README.md at master"
[5]: https://docs.astral.sh/uv/?utm_source=chatgpt.com "uv - Astral Docs"
[6]: https://docs.astral.sh/uv/guides/projects/?utm_source=chatgpt.com "Working on projects | uv - Astral Docs"
[7]: https://pypi.org/project/python-dotenv/?utm_source=chatgpt.com "python-dotenv"
[8]: https://docs.python.org/3/tutorial/errors.html?utm_source=chatgpt.com "8. Errors and Exceptions — Python 3.14.6 documentation"
[9]: https://docs.pytest.org/en/stable/getting-started.html?utm_source=chatgpt.com "Get Started - pytest documentation"
