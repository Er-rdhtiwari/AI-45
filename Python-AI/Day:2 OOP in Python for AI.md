# Day 2 – OOP in Python for Senior AI Engineer Interviews

## 1. Five-line beginner summary

* **Object-oriented programming, or OOP**, organizes software around objects that combine data and behavior.
* In AI systems, OOP helps separate model providers, retrievers, vector databases, prompt builders, evaluation components, and APIs.
* **Abstraction and polymorphism** allow the same application code to work with OpenAI, Anthropic, local models, or other backends.
* **Composition** is usually safer than deep inheritance because AI systems frequently combine interchangeable components.
* Good OOP makes production GenAI systems easier to test, extend, monitor, and maintain.

---

# 2. Why OOP matters in AI and GenAI systems

A small AI prototype may start as a few functions:

```python
def embed_text(text):
    ...

def search_vector_db(embedding):
    ...

def call_llm(prompt):
    ...
```

This is acceptable for experimentation. As the system grows, however, you may need:

* Multiple LLM providers
* Different embedding models
* Different vector databases
* Retry and timeout handling
* Authentication
* Prompt versions
* Caching
* Logging and tracing
* Offline evaluation
* Streaming responses
* User-specific configuration
* Mock components for testing

Putting all this behavior into unrelated functions or one large file quickly becomes difficult to maintain.

OOP lets us model the system as cooperating components:

```text
RagPipeline
 ├── QueryRewriter
 ├── Embedder
 ├── VectorStore
 ├── Reranker
 ├── PromptBuilder
 └── ModelProvider
```

Each component has:

* A clear responsibility
* Its own configuration
* A stable interface
* Replaceable implementations
* Independent tests

The main goal of OOP is not merely to create classes. The goal is to create **clear boundaries between responsibilities**.

---

# 3. Classes, objects, attributes, and methods

## 3.1 Class

A class is a blueprint describing:

* What data an object contains
* What operations the object can perform

```python
class EmbeddingModel:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]
```

The class describes the behavior of an embedding model.

---

## 3.2 Object

An object is a concrete instance of a class.

```python
embedding_model = EmbeddingModel()
vector = embedding_model.embed("Disney vacation policy")
```

Here:

* `EmbeddingModel` is the class.
* `embedding_model` is an object.
* `embed()` is a method.
* `vector` is the method result.

Two objects created from the same class can have different configurations:

```python
small_embedder = EmbeddingModel()
large_embedder = EmbeddingModel()
```

In a real system, one object might use a small, fast embedding model while another uses a larger, more accurate model.

---

## 3.3 Attributes

Attributes are variables associated with an object.

```python
class ModelClient:
    def __init__(self, model_name: str, timeout_seconds: float):
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds
```

Usage:

```python
client = ModelClient(
    model_name="production-chat-model",
    timeout_seconds=30.0,
)

print(client.model_name)
print(client.timeout_seconds)
```

Attributes usually represent the object's state.

For an AI model client, this could include:

* Model name
* API endpoint
* Timeout
* Maximum tokens
* Retry policy
* Organization ID
* Deployment name

Avoid storing raw secrets as publicly printable attributes because they may appear in logs or exception messages.

---

## 3.4 Methods

Methods define object behavior.

```python
class ModelClient:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        return f"Response from {self.model_name}: {prompt}"
```

`self` refers to the current object.

```python
client = ModelClient("chat-model")
response = client.generate("Summarize this document")
```

Conceptually, Python converts this call into something similar to:

```python
ModelClient.generate(client, "Summarize this document")
```

That is why instance methods receive `self`.

---

# 4. Encapsulation

## 4.1 What encapsulation means

Encapsulation means:

* Keeping related state and behavior together
* Controlling how internal state is accessed or changed
* Hiding unnecessary implementation details

For example, callers should not need to understand how an LLM client:

* Builds HTTP headers
* Refreshes authentication tokens
* Parses provider-specific responses
* Handles retries
* Records latency

They should only need to call:

```python
response = provider.generate(request)
```

---

## 4.2 Python does not enforce strict privacy

Python primarily uses naming conventions.

### Public attribute

```python
self.model_name
```

This is intended for normal external use.

### Protected-by-convention attribute

```python
self._client
```

The leading underscore means:

> This is an internal implementation detail. Avoid accessing it directly.

Python still allows access:

```python
provider._client
```

But application code should normally not do this.

### Name-mangled attribute

```python
self.__api_key
```

Python transforms it internally into a name such as:

```python
_ModelProvider__api_key
```

This helps prevent accidental access or overriding. It does not provide strong security.

It should not be treated as a secret-protection mechanism.

---

## 4.3 Encapsulation example

```python
class TemperatureConfig:
    def __init__(self, temperature: float):
        # Use the property setter so validation is applied during construction.
        self.temperature = temperature

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        # Centralizing validation prevents the object from entering
        # an invalid state later in its lifetime.
        if not 0.0 <= value <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")

        self._temperature = value
```

Usage:

```python
config = TemperatureConfig(0.2)
config.temperature = 0.5

# Raises ValueError instead of silently storing an invalid value.
config.temperature = 5.0
```

The important design idea is not the getter itself. The important idea is that the object protects its own invariants.

An **invariant** is a rule that must always remain true, such as:

```text
0.0 <= temperature <= 2.0
```

---

# 5. Abstraction

## 5.1 What abstraction means

Abstraction exposes the essential behavior while hiding implementation details.

Consider three model providers:

* Cloud model provider A
* Cloud model provider B
* A locally hosted LLM

Their SDKs, request formats, authentication methods, and response schemas may differ.

Your RAG application should not contain provider-specific code everywhere:

```python
if provider == "provider_a":
    ...
elif provider == "provider_b":
    ...
elif provider == "local":
    ...
```

Instead, define one common abstraction:

```python
class ModelProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
```

Each provider implements that interface.

The application depends on the behavior `generate()`, not on the provider's internal SDK.

---

## 5.2 Abstract base classes

Python's `abc` module can explicitly define abstract behavior.

```python
from abc import ABC, abstractmethod


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError
```

A subclass must implement `generate()` before it can be instantiated.

```python
class LocalModelProvider(ModelProvider):
    def generate(self, prompt: str) -> str:
        return f"Local response: {prompt}"
```

This fails:

```python
class IncompleteProvider(ModelProvider):
    pass


# TypeError: abstract method generate is not implemented.
provider = IncompleteProvider()
```

Abstract base classes are useful when you want:

* A clear inheritance relationship
* Runtime enforcement
* Shared implementation
* A formal framework extension point

---

## 5.3 Protocols and structural typing

In many Python systems, `Protocol` provides a more flexible abstraction.

```python
from typing import Protocol


class ModelProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

Any object with a compatible `generate()` method can satisfy this contract:

```python
class LocalProvider:
    def generate(self, prompt: str) -> str:
        return "Local output"
```

`LocalProvider` does not need to inherit from `ModelProvider`.

This is called **structural typing**:

> An object is accepted because it has the required behavior, not because it inherits from a particular class.

Protocols are especially useful for:

* Dependency injection
* Unit testing
* Adapters around third-party SDKs
* Avoiding unnecessary inheritance coupling

---

# 6. Inheritance

Inheritance creates a relationship where one class extends another.

```python
class BaseModelProvider:
    def validate_prompt(self, prompt: str) -> None:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")


class CloudModelProvider(BaseModelProvider):
    def generate(self, prompt: str) -> str:
        self.validate_prompt(prompt)
        return "Generated cloud response"
```

`CloudModelProvider` inherits `validate_prompt()` from `BaseModelProvider`.

Inheritance is appropriate when there is a real **is-a** relationship:

```text
OpenAIProvider is a ModelProvider.
AnthropicProvider is a ModelProvider.
LocalLLMProvider is a ModelProvider.
```

It can also help when implementations genuinely share stable behavior.

---

## 6.1 Method overriding

A subclass can replace a parent method.

```python
class ModelProvider:
    def generate(self, prompt: str) -> str:
        return "Generic response"


class LocalProvider(ModelProvider):
    def generate(self, prompt: str) -> str:
        return f"Local model response for: {prompt}"
```

The subclass overrides the parent's implementation.

---

## 6.2 The `super()` function

`super()` calls parent-class behavior.

```python
class ModelProvider:
    def __init__(self, model_name: str):
        self.model_name = model_name


class LocalProvider(ModelProvider):
    def __init__(self, model_name: str, device: str):
        # Initialize the parent portion of the object.
        super().__init__(model_name)
        self.device = device
```

Use `super()` rather than directly calling the parent's class name:

```python
# Less flexible:
ModelProvider.__init__(self, model_name)
```

`super()` works better with multiple inheritance and future refactoring.

---

# 7. Polymorphism

Polymorphism means that different objects can be used through the same interface.

```python
def answer_question(
    provider: ModelProvider,
    question: str,
) -> str:
    return provider.generate(question)
```

The function does not care which provider is passed:

```python
answer_question(openai_provider, "What is RAG?")
answer_question(anthropic_provider, "What is RAG?")
answer_question(local_provider, "What is RAG?")
```

Each object handles the request using its own implementation.

This is extremely valuable in AI systems because providers frequently differ across:

* Development and production
* Cloud environments
* Cost tiers
* Geographic regions
* Data-sensitivity requirements
* Latency requirements
* Availability incidents

Polymorphism lets you change providers without rewriting the business workflow.

---

## 7.1 Polymorphism is more than inheritance

Python supports polymorphism through duck typing:

> If an object behaves like the required type, it can be used as that type.

```python
class TestModel:
    def generate(self, prompt: str) -> str:
        return "Fixed response for testing"
```

Even without inheriting from `ModelProvider`, it may work anywhere a compatible object is expected.

This makes unit testing easier.

---

# 8. Composition versus inheritance

## 8.1 Composition

Composition means building one object from other objects.

```python
class RagPipeline:
    def __init__(
        self,
        embedder,
        vector_store,
        model_provider,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.model_provider = model_provider
```

A `RagPipeline`:

* Has an embedder
* Has a vector store
* Has a model provider

This is a **has-a** relationship.

---

## 8.2 Inheritance

Inheritance describes an **is-a** relationship:

```text
OpenAIProvider is a ModelProvider.
PineconeVectorStore is a VectorStore.
```

---

## 8.3 Why composition is usually preferred

Imagine trying to model all RAG combinations using inheritance:

```text
OpenAIPineconeRagPipeline
OpenAIWeaviateRagPipeline
AnthropicPineconeRagPipeline
AnthropicWeaviateRagPipeline
LocalFaissRagPipeline
```

The number of subclasses grows rapidly.

With composition, the pipeline receives interchangeable components:

```python
pipeline = RagPipeline(
    embedder=some_embedder,
    vector_store=some_vector_store,
    model_provider=some_provider,
)
```

You can replace any component independently.

---

## 8.4 When to use inheritance

Use inheritance when:

* There is a genuine subtype relationship.
* Subclasses honor the same behavioral contract.
* Shared behavior is stable and meaningful.
* The hierarchy remains shallow.
* Framework extension requires subclassing.

Use composition when:

* Behavior must be changed at runtime.
* Components vary independently.
* You need easier testing.
* The system integrates multiple third-party services.
* Inheritance would create many combinations.
* The relationship is naturally “has-a.”

A strong default for production AI systems is:

> Use interfaces for contracts and composition for assembling behavior.

---

# 9. Python-specific OOP features

## 9.1 `__init__`

`__init__` initializes an already created object.

```python
class Retriever:
    def __init__(self, top_k: int):
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        self.top_k = top_k
```

`__init__` should generally:

* Store dependencies
* Validate basic configuration
* Establish simple invariants

Avoid doing expensive work in `__init__`, such as:

* Downloading a model
* Calling an external API
* Reading millions of records
* Creating a vector index
* Starting a background thread

Expensive constructors make:

* Testing slow
* Failures harder to control
* Dependency injection difficult
* Object creation unpredictable

Prefer an explicit initialization method, factory, or dependency injection.

---

## 9.2 Instance variables

Instance variables belong to one object.

```python
class ModelProvider:
    def __init__(self, model_name: str):
        self.model_name = model_name
```

```python
provider_a = ModelProvider("model-a")
provider_b = ModelProvider("model-b")

print(provider_a.model_name)  # model-a
print(provider_b.model_name)  # model-b
```

Each object has its own value.

---

## 9.3 Class variables

Class variables are shared at the class level.

```python
from typing import ClassVar


class ModelProvider:
    supported_api_version: ClassVar[str] = "v1"

    def __init__(self, model_name: str):
        self.model_name = model_name
```

Usage:

```python
print(ModelProvider.supported_api_version)
```

Good class-variable use cases include:

* Provider name
* Supported schema version
* Constant defaults
* Registry metadata
* Capability flags

Example:

```python
class LocalProvider:
    provider_name: ClassVar[str] = "local"
    supports_streaming: ClassVar[bool] = True
```

---

## 9.4 Common class-variable pitfall

Do not unintentionally create shared mutable state:

```python
class BadRequestTracker:
    requests = []  # Shared by every instance

    def record(self, request: str) -> None:
        self.requests.append(request)
```

All instances share the same list.

Safer:

```python
class RequestTracker:
    def __init__(self):
        self.requests: list[str] = []
```

This creates a separate list for each object.

---

# 10. `@staticmethod`

A static method belongs logically to a class but does not use:

* `self`
* `cls`

```python
class PromptValidator:
    @staticmethod
    def is_valid(prompt: str) -> bool:
        return bool(prompt.strip())
```

Usage:

```python
PromptValidator.is_valid("Explain RAG")
```

Good use cases:

* Validation helpers
* Stateless transformations
* Parsing utilities closely related to the class

Example:

```python
class TokenBudget:
    @staticmethod
    def calculate_available_tokens(
        context_limit: int,
        prompt_tokens: int,
        reserved_output_tokens: int,
    ) -> int:
        available = context_limit - prompt_tokens - reserved_output_tokens
        return max(available, 0)
```

A module-level function may be better when the helper has no meaningful relationship with the class.

Do not put every utility into a class merely to use `@staticmethod`.

---

# 11. `@classmethod`

A class method receives the class as `cls`.

It is often used for:

* Alternative constructors
* Factory methods
* Subclass-aware object creation

```python
class ModelConfig:
    def __init__(self, model_name: str, timeout_seconds: float):
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_dict(cls, data: dict) -> "ModelConfig":
        # cls is used instead of ModelConfig so subclasses can reuse
        # this alternative constructor correctly.
        return cls(
            model_name=data["model_name"],
            timeout_seconds=float(data.get("timeout_seconds", 30)),
        )
```

Usage:

```python
config = ModelConfig.from_dict(
    {
        "model_name": "production-chat-model",
        "timeout_seconds": 20,
    }
)
```

Difference:

```text
Instance method  -> receives self and operates on one object
Class method     -> receives cls and operates on the class
Static method    -> receives neither self nor cls
```

---

# 12. `@property`

A property allows method-controlled access using attribute syntax.

```python
class RetrievalConfig:
    def __init__(self, top_k: int):
        self.top_k = top_k

    @property
    def top_k(self) -> int:
        return self._top_k

    @top_k.setter
    def top_k(self, value: int) -> None:
        if value <= 0:
            raise ValueError("top_k must be greater than zero")

        if value > 100:
            raise ValueError("top_k must not exceed 100")

        self._top_k = value
```

Usage:

```python
config = RetrievalConfig(top_k=5)
print(config.top_k)

config.top_k = 10
```

Properties are useful when:

* Validation is required
* A value is computed
* Internal representation may change
* Access must be read-only
* You want to preserve a stable public API

Read-only property:

```python
class ModelDeployment:
    def __init__(self, provider: str, model: str):
        self._provider = provider
        self._model = model

    @property
    def identifier(self) -> str:
        return f"{self._provider}:{self._model}"
```

There is no setter, so callers cannot assign directly to `identifier`.

Do not create trivial properties for every attribute. Plain public attributes are acceptable in Python when no control is needed.

---

# 13. Dataclasses

A dataclass automatically generates common methods such as:

* `__init__`
* `__repr__`
* `__eq__`

```python
from dataclasses import dataclass


@dataclass
class GenerationConfig:
    model_name: str
    temperature: float = 0.2
    max_tokens: int = 500
```

Without `@dataclass`, you would need to write the constructor and representation manually.

Usage:

```python
config = GenerationConfig(
    model_name="chat-model",
    temperature=0.1,
    max_tokens=800,
)

print(config)
```

Possible output:

```text
GenerationConfig(
    model_name='chat-model',
    temperature=0.1,
    max_tokens=800
)
```

---

## 13.1 Dataclasses for AI configuration

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class RagConfig:
    top_k: int = 10
    rerank_top_n: int = 4
    minimum_score: float = 0.65
    max_context_characters: int = 12_000
```

`frozen=True` makes the dataclass effectively immutable:

```python
config = RagConfig()

# Raises FrozenInstanceError.
config.top_k = 50
```

Immutable configuration objects are valuable because they:

* Prevent accidental runtime mutation
* Are easier to reason about
* Reduce concurrency problems
* Improve reproducibility
* Make tests more predictable

---

## 13.2 Dataclasses for payloads

```python
@dataclass(frozen=True)
class GenerationRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 500


@dataclass(frozen=True)
class GenerationResponse:
    text: str
    model_name: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
```

Typed request and response objects are preferable to unstructured dictionaries in large systems.

Compare:

```python
response["usage"]["output_tokens"]
```

with:

```python
response.output_tokens
```

The dataclass version is easier for:

* IDE completion
* Type checking
* Refactoring
* Testing
* Documentation

---

## 13.3 Dataclasses for retrieved chunks

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DocumentChunk:
    text: str
    score: float
    document_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
```

Use `default_factory` for mutable defaults.

Correct:

```python
metadata: dict[str, Any] = field(default_factory=dict)
```

Incorrect:

```python
metadata: dict[str, Any] = {}
```

The incorrect version would risk sharing the same mutable dictionary.

---

## 13.4 Validation with `__post_init__`

```python
@dataclass(frozen=True)
class RetrievalConfig:
    top_k: int
    minimum_score: float

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")

        if not 0.0 <= self.minimum_score <= 1.0:
            raise ValueError("minimum_score must be between 0 and 1")
```

`__post_init__()` runs after the generated `__init__()`.

Dataclasses are excellent for data-oriented objects, but a class with extensive mutable behavior may be clearer as a regular class.

---

# 14. Dunder methods

“Dunder” means **double underscore**.

Dunder methods let your objects participate in Python's built-in syntax and operations.

---

## 14.1 `__repr__`

`__repr__` provides a developer-focused representation.

```python
class ModelProvider:
    def __init__(self, model_name: str, timeout_seconds: float):
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model_name={self.model_name!r}, "
            f"timeout_seconds={self.timeout_seconds!r})"
        )
```

Usage:

```python
provider = ModelProvider("chat-model", 30)
print(repr(provider))
```

A useful `__repr__` helps with:

* Debugging
* Logs
* Test failures
* Interactive development

Never include:

* API keys
* Access tokens
* Passwords
* Sensitive customer data

---

## 14.2 `__str__`

`__str__` provides a user-friendly representation.

```python
class ModelDeployment:
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model

    def __str__(self) -> str:
        return f"{self.provider} deployment using {self.model}"

    def __repr__(self) -> str:
        return (
            f"ModelDeployment("
            f"provider={self.provider!r}, model={self.model!r})"
        )
```

```python
deployment = ModelDeployment("local", "llama-model")

print(str(deployment))
print(repr(deployment))
```

Conceptually:

* `__str__`: readable for users
* `__repr__`: useful for developers

---

## 14.3 `__len__`

`__len__` defines the behavior of `len()`.

```python
class RetrievalResult:
    def __init__(self, chunks: list[str]):
        self._chunks = chunks

    def __len__(self) -> int:
        return len(self._chunks)
```

```python
result = RetrievalResult(["chunk 1", "chunk 2"])
print(len(result))  # 2
```

Use this only when the object has a natural concept of length.

---

## 14.4 `__eq__`

`__eq__` defines equality behavior.

```python
class ModelReference:
    def __init__(self, provider: str, model_name: str):
        self.provider = provider
        self.model_name = model_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelReference):
            return NotImplemented

        return (
            self.provider == other.provider
            and self.model_name == other.model_name
        )
```

Usage:

```python
first = ModelReference("local", "model-a")
second = ModelReference("local", "model-a")

print(first == second)  # True
```

Returning `NotImplemented` for unsupported types allows Python to try the reverse comparison or handle the comparison correctly.

Dataclasses generate `__eq__` automatically by default.

---

## 14.5 Other useful dunder methods

### `__hash__`

Allows immutable objects to be used as dictionary keys or set values.

```python
@dataclass(frozen=True)
class ModelKey:
    provider: str
    model_name: str
```

A frozen dataclass can often be hashable automatically.

---

### `__call__`

Makes an object callable like a function.

```python
class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def __call__(self, question: str, context: str) -> str:
        return self.template.format(
            question=question,
            context=context,
        )
```

Usage:

```python
build_prompt = PromptTemplate(
    "Context:\n{context}\n\nQuestion: {question}"
)

prompt = build_prompt(
    question="What is the refund policy?",
    context="Refunds are available within 30 days.",
)
```

This can be useful for configurable transformations.

---

### `__iter__`

Makes an object iterable.

```python
class RetrievedChunks:
    def __init__(self, chunks: list[str]):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)
```

---

### `__enter__` and `__exit__`

Support context managers.

```python
class ModelSession:
    def __enter__(self):
        print("Opening model session")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing model session")
```

Usage:

```python
with ModelSession() as session:
    ...
```

This is useful for managing:

* Database connections
* GPU resources
* Temporary files
* Tracing spans
* Network sessions

Only implement dunder methods when the behavior is natural and unsurprising.

---

# 15. Design Exercise 1: Model provider hierarchy

## 15.1 Requirements

We want application code that can use:

* An OpenAI-style provider
* An Anthropic-style provider
* A locally hosted model

The application should not depend directly on any provider SDK.

We also want:

* Typed request and response payloads
* Basic validation
* Provider-specific adapters
* Easy testing
* Safe object representations

---

## 15.2 Design

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Mapping


@dataclass(frozen=True)
class GenerationRequest:
    """Provider-neutral request used by the rest of the application."""

    prompt: str
    temperature: float = 0.2
    max_tokens: int = 500


@dataclass(frozen=True)
class GenerationResponse:
    """Normalized response independent of any provider's SDK schema."""

    text: str
    model_name: str
    provider_name: str
    input_tokens: int = 0
    output_tokens: int = 0


class ModelProvider(ABC):
    """
    Common abstraction for all text-generation providers.

    The rest of the system depends on this contract instead of depending
    directly on provider-specific SDK classes.
    """

    provider_name: ClassVar[str] = "unknown"

    def __init__(
        self,
        model_name: str,
        timeout_seconds: float = 30.0,
    ):
        if not model_name.strip():
            raise ValueError("model_name cannot be empty")

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")

        self._model_name = model_name
        self._timeout_seconds = timeout_seconds

    @property
    def model_name(self) -> str:
        """Read-only public access to the configured model."""
        return self._model_name

    @property
    def timeout_seconds(self) -> float:
        return self._timeout_seconds

    @staticmethod
    def validate_request(request: GenerationRequest) -> None:
        """
        Validation does not depend on one provider instance, so a static
        method is reasonable here.
        """
        if not request.prompt.strip():
            raise ValueError("prompt cannot be empty")

        if not 0.0 <= request.temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")

        if request.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        **dependencies: Any,
    ) -> "ModelProvider":
        """
        Alternative constructor.

        Using cls instead of ModelProvider means subclasses construct
        instances of their own type.
        """
        return cls(
            model_name=str(config["model_name"]),
            timeout_seconds=float(config.get("timeout_seconds", 30.0)),
            **dependencies,
        )

    @abstractmethod
    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Every concrete provider must implement this operation."""
        raise NotImplementedError

    def __repr__(self) -> str:
        # Do not include API keys, authorization headers, or sensitive data.
        return (
            f"{self.__class__.__name__}("
            f"model_name={self.model_name!r}, "
            f"timeout_seconds={self.timeout_seconds!r})"
        )


class OpenAIModelProvider(ModelProvider):
    provider_name: ClassVar[str] = "openai"

    def __init__(
        self,
        model_name: str,
        client: Any,
        timeout_seconds: float = 30.0,
    ):
        super().__init__(model_name, timeout_seconds)

        # The SDK client is injected rather than created internally.
        # This makes the provider easier to test with a fake client.
        self._client = client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        self.validate_request(request)

        # This is intentionally SDK-neutral pseudocode. The adapter is
        # the only class that should know the provider's exact API shape.
        raw_response = self._client.generate(
            model=self.model_name,
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            timeout=self.timeout_seconds,
        )

        # Normalize the provider-specific result into our domain object.
        return GenerationResponse(
            text=raw_response.text,
            model_name=self.model_name,
            provider_name=self.provider_name,
            input_tokens=raw_response.input_tokens,
            output_tokens=raw_response.output_tokens,
        )


class AnthropicModelProvider(ModelProvider):
    provider_name: ClassVar[str] = "anthropic"

    def __init__(
        self,
        model_name: str,
        client: Any,
        timeout_seconds: float = 30.0,
    ):
        super().__init__(model_name, timeout_seconds)
        self._client = client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        self.validate_request(request)

        # This provider may use a different request and response format.
        raw_response = self._client.create_message(
            model=self.model_name,
            content=request.prompt,
            temperature=request.temperature,
            output_limit=request.max_tokens,
            timeout=self.timeout_seconds,
        )

        return GenerationResponse(
            text=raw_response.content,
            model_name=self.model_name,
            provider_name=self.provider_name,
            input_tokens=raw_response.usage.input_tokens,
            output_tokens=raw_response.usage.output_tokens,
        )


class LocalModelProvider(ModelProvider):
    provider_name: ClassVar[str] = "local"

    def __init__(
        self,
        model_name: str,
        inference_engine: Any,
        timeout_seconds: float = 30.0,
    ):
        super().__init__(model_name, timeout_seconds)
        self._inference_engine = inference_engine

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        self.validate_request(request)

        generated_text = self._inference_engine.generate(
            prompt=request.prompt,
            temperature=request.temperature,
            max_new_tokens=request.max_tokens,
        )

        return GenerationResponse(
            text=generated_text,
            model_name=self.model_name,
            provider_name=self.provider_name,
        )
```

---

## 15.3 Using the providers polymorphically

```python
def summarize_document(
    provider: ModelProvider,
    document: str,
) -> GenerationResponse:
    """
    Business logic depends only on ModelProvider.

    It does not know whether the provider is OpenAI, Anthropic,
    locally hosted, or a fake used during testing.
    """
    request = GenerationRequest(
        prompt=f"Summarize the following document:\n\n{document}",
        temperature=0.1,
        max_tokens=300,
    )

    return provider.generate(request)
```

The provider can be changed without changing the function:

```python
result = summarize_document(openai_provider, document)
result = summarize_document(anthropic_provider, document)
result = summarize_document(local_provider, document)
```

---

## 15.4 Why this design works

### Abstraction

`ModelProvider` defines what a provider must do.

### Encapsulation

SDK-specific request construction and response parsing remain inside each adapter.

### Inheritance

Concrete providers inherit a common contract.

### Polymorphism

The same application function accepts all provider implementations.

### Composition

Each provider contains an injected SDK client or inference engine.

### Dependency inversion

High-level business logic depends on `ModelProvider`, not on a vendor SDK.

---

## 15.5 Adding retry through composition

Do not force retry logic into every subclass. Wrap providers instead.

```python
import time


class RetryingModelProvider:
    """
    Decorator around any model provider.

    This object exposes the same generate() behavior while adding retry
    without changing the concrete provider classes.
    """

    def __init__(
        self,
        provider: ModelProvider,
        max_attempts: int = 3,
        initial_delay_seconds: float = 0.5,
    ):
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive")

        self._provider = provider
        self._max_attempts = max_attempts
        self._initial_delay_seconds = initial_delay_seconds

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        delay = self._initial_delay_seconds

        for attempt in range(1, self._max_attempts + 1):
            try:
                return self._provider.generate(request)

            except TimeoutError:
                # Only retry errors known to be transient.
                # Validation and authentication failures normally should
                # not be retried blindly.
                if attempt == self._max_attempts:
                    raise

                time.sleep(delay)
                delay *= 2

        # This line is logically unreachable but helps static analyzers.
        raise RuntimeError("Retry loop ended unexpectedly")
```

Usage:

```python
reliable_provider = RetryingModelProvider(
    provider=openai_provider,
    max_attempts=3,
)
```

This design follows the **decorator pattern** and favors composition.

---

# 16. Design Exercise 2: Maintainable RAG pipeline

## 16.1 RAG responsibilities

A production RAG request may perform:

1. Validate the question.
2. Rewrite or normalize the query.
3. Generate an embedding.
4. Retrieve candidate chunks.
5. Filter low-scoring results.
6. Rerank results.
7. Build context.
8. Construct the prompt.
9. Call the LLM.
10. Return the answer and sources.

A common mistake is placing every step in one enormous `RagPipeline` class.

A better design gives each component one clear responsibility.

---

## 16.2 Interfaces and data models

```python
from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence


@dataclass(frozen=True)
class DocumentChunk:
    text: str
    document_id: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    sources: tuple[DocumentChunk, ...]


@dataclass(frozen=True)
class RagConfig:
    top_k: int = 10
    final_context_count: int = 4
    minimum_score: float = 0.60
    max_context_characters: int = 12_000

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")

        if self.final_context_count <= 0:
            raise ValueError("final_context_count must be positive")

        if self.final_context_count > self.top_k:
            raise ValueError(
                "final_context_count cannot exceed top_k"
            )

        if not 0.0 <= self.minimum_score <= 1.0:
            raise ValueError(
                "minimum_score must be between 0 and 1"
            )


class QueryRewriter(Protocol):
    def rewrite(self, question: str) -> str:
        ...


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]:
        ...


class VectorStore(Protocol):
    def search(
        self,
        vector: Sequence[float],
        top_k: int,
    ) -> list[DocumentChunk]:
        ...


class Reranker(Protocol):
    def rerank(
        self,
        question: str,
        chunks: list[DocumentChunk],
        top_n: int,
    ) -> list[DocumentChunk]:
        ...


class PromptBuilder(Protocol):
    def build(
        self,
        question: str,
        chunks: list[DocumentChunk],
    ) -> str:
        ...


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

These protocols define small, focused contracts.

This follows the **interface segregation principle**:

> Components should depend only on the operations they actually use.

The RAG pipeline does not need to know every capability of a model SDK or vector database.

---

## 16.3 Concrete prompt builder

```python
class GroundedPromptBuilder:
    def build(
        self,
        question: str,
        chunks: list[DocumentChunk],
    ) -> str:
        # Numbering chunks helps the model cite or reference sources.
        context_sections = []

        for index, chunk in enumerate(chunks, start=1):
            section = (
                f"[Source {index} | Document {chunk.document_id}]\n"
                f"{chunk.text}"
            )
            context_sections.append(section)

        context = "\n\n".join(context_sections)

        return (
            "Answer the question using only the supplied context.\n"
            "If the context does not contain the answer, say that the "
            "available information is insufficient.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
```

---

## 16.4 RAG orchestrator

```python
class RagPipeline:
    """
    Coordinates the RAG workflow.

    It does not implement embedding, vector search, reranking, or text
    generation itself. Those responsibilities belong to injected components.
    """

    def __init__(
        self,
        config: RagConfig,
        query_rewriter: QueryRewriter,
        embedder: Embedder,
        vector_store: VectorStore,
        reranker: Reranker,
        prompt_builder: PromptBuilder,
        generator: TextGenerator,
    ):
        self._config = config
        self._query_rewriter = query_rewriter
        self._embedder = embedder
        self._vector_store = vector_store
        self._reranker = reranker
        self._prompt_builder = prompt_builder
        self._generator = generator

    def answer(self, question: str) -> RagAnswer:
        self._validate_question(question)

        # Step 1: Improve the retrieval query. The original question is
        # still retained for reranking and answer generation.
        retrieval_query = self._query_rewriter.rewrite(question)

        # Step 2: Convert the query into the vector representation expected
        # by the configured vector store.
        query_vector = self._embedder.embed(retrieval_query)

        # Step 3: Retrieve a broad candidate set to improve recall.
        candidates = self._vector_store.search(
            vector=query_vector,
            top_k=self._config.top_k,
        )

        # Step 4: Remove candidates below the configured relevance threshold.
        relevant_candidates = [
            chunk
            for chunk in candidates
            if chunk.score >= self._config.minimum_score
        ]

        if not relevant_candidates:
            return RagAnswer(
                answer=(
                    "I could not find sufficiently relevant information "
                    "in the indexed documents."
                ),
                sources=(),
            )

        # Step 5: Reranking uses the original user question and selects
        # a smaller, more precise context set.
        reranked_chunks = self._reranker.rerank(
            question=question,
            chunks=relevant_candidates,
            top_n=self._config.final_context_count,
        )

        # Step 6: Enforce the context-size limit before constructing the prompt.
        bounded_chunks = self._fit_context_budget(reranked_chunks)

        # Step 7: Build a grounded prompt.
        prompt = self._prompt_builder.build(
            question=question,
            chunks=bounded_chunks,
        )

        # Step 8: Generate the final answer.
        answer_text = self._generator.generate(prompt)

        return RagAnswer(
            answer=answer_text,
            sources=tuple(bounded_chunks),
        )

    @staticmethod
    def _validate_question(question: str) -> None:
        if not question.strip():
            raise ValueError("question cannot be empty")

    def _fit_context_budget(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:
        """
        Add chunks until the configured character budget is exhausted.

        Production systems commonly use token-aware budgeting instead,
        but character budgeting keeps this example provider-independent.
        """
        selected: list[DocumentChunk] = []
        current_size = 0

        for chunk in chunks:
            next_size = current_size + len(chunk.text)

            if next_size > self._config.max_context_characters:
                break

            selected.append(chunk)
            current_size = next_size

        return selected
```

---

## 16.5 Why this design is maintainable

The pipeline is responsible for **orchestration**, not every implementation detail.

You can independently replace:

```python
pipeline = RagPipeline(
    config=config,
    query_rewriter=rule_based_rewriter,
    embedder=open_source_embedder,
    vector_store=pgvector_store,
    reranker=cross_encoder_reranker,
    prompt_builder=GroundedPromptBuilder(),
    generator=model_provider,
)
```

Later:

```python
pipeline = RagPipeline(
    config=config,
    query_rewriter=llm_query_rewriter,
    embedder=managed_embedding_service,
    vector_store=enterprise_search_store,
    reranker=managed_reranking_service,
    prompt_builder=GroundedPromptBuilder(),
    generator=different_model_provider,
)
```

The orchestration code does not need to change.

---

# 17. Testing the RAG pipeline with fake objects

Dependency injection makes testing possible without:

* Calling a real LLM
* Paying API costs
* Connecting to a vector database
* Downloading an embedding model
* Depending on network availability

```python
class FakeQueryRewriter:
    def rewrite(self, question: str) -> str:
        return question.lower()


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        # A deterministic vector keeps the test repeatable.
        return [0.1, 0.2, 0.3]


class FakeVectorStore:
    def search(
        self,
        vector: Sequence[float],
        top_k: int,
    ) -> list[DocumentChunk]:
        return [
            DocumentChunk(
                text="Employees may carry forward five leave days.",
                document_id="leave-policy",
                score=0.92,
            )
        ]


class FakeReranker:
    def rerank(
        self,
        question: str,
        chunks: list[DocumentChunk],
        top_n: int,
    ) -> list[DocumentChunk]:
        return chunks[:top_n]


class FakeGenerator:
    def __init__(self):
        self.received_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        # Store the prompt so the test can inspect pipeline behavior.
        self.received_prompt = prompt
        return "You may carry forward five leave days."
```

Test:

```python
def test_rag_pipeline_returns_grounded_answer() -> None:
    generator = FakeGenerator()

    pipeline = RagPipeline(
        config=RagConfig(),
        query_rewriter=FakeQueryRewriter(),
        embedder=FakeEmbedder(),
        vector_store=FakeVectorStore(),
        reranker=FakeReranker(),
        prompt_builder=GroundedPromptBuilder(),
        generator=generator,
    )

    result = pipeline.answer(
        "How many leave days can I carry forward?"
    )

    assert result.answer == "You may carry forward five leave days."
    assert len(result.sources) == 1
    assert result.sources[0].document_id == "leave-policy"

    # This verifies that the retrieved evidence reached the model prompt.
    assert generator.received_prompt is not None
    assert "five leave days" in generator.received_prompt
```

This test is:

* Fast
* Deterministic
* Offline
* Cheap
* Focused on orchestration behavior

Separate integration tests should verify actual provider and database adapters.

---

# 18. Real-world AI/ML OOP examples

## Example 1: Model provider abstraction

### Problem

Your application supports several LLM providers.

### OOP design

```text
ModelProvider
 ├── OpenAIModelProvider
 ├── AnthropicModelProvider
 └── LocalModelProvider
```

### Benefit

Business code calls one operation:

```python
provider.generate(request)
```

This supports:

* Provider migration
* Failover
* Cost-based routing
* A/B testing
* Development fakes
* Region-specific deployments

---

## Example 2: RAG pipeline composition

### Problem

A RAG service uses several independently changing components.

### OOP design

```text
RagPipeline
 ├── QueryRewriter
 ├── Embedder
 ├── VectorStore
 ├── Reranker
 ├── PromptBuilder
 └── TextGenerator
```

### Benefit

Each component can be:

* Replaced
* Tested
* Benchmarked
* Configured
* Monitored independently

---

## Example 3: Vector database adapters

### Problem

Different vector stores expose different APIs.

One may use:

```python
client.query(vector=..., limit=...)
```

Another may use:

```python
collection.search(embedding=..., top_k=...)
```

Your application should not depend on these differences.

### Common interface

```python
class VectorStore(Protocol):
    def search(
        self,
        vector: Sequence[float],
        top_k: int,
    ) -> list[DocumentChunk]:
        ...
```

Adapters normalize vendor behavior:

```python
class PgVectorStore:
    def search(
        self,
        vector: Sequence[float],
        top_k: int,
    ) -> list[DocumentChunk]:
        ...


class ManagedVectorStore:
    def search(
        self,
        vector: Sequence[float],
        top_k: int,
    ) -> list[DocumentChunk]:
        ...
```

The RAG pipeline remains independent of the database vendor.

This is an example of the **adapter pattern**.

---

# 19. Important OOP design principles for AI systems

## 19.1 Single Responsibility Principle

A class should have one primary reason to change.

Bad design:

```text
RagService
 ├── Loads documents
 ├── Chunks documents
 ├── Creates embeddings
 ├── Writes to vector DB
 ├── Retrieves chunks
 ├── Builds prompts
 ├── Calls LLM
 ├── Sends emails
 └── Writes audit records
```

This is a “God class.”

Better:

```text
DocumentLoader
DocumentChunker
EmbeddingService
VectorStore
Retriever
PromptBuilder
ModelProvider
AuditLogger
RagPipeline
```

The pipeline coordinates the components.

---

## 19.2 Open/Closed Principle

Software should be open for extension but closed for unnecessary modification.

Adding a new provider should ideally require:

```python
class NewProvider(ModelProvider):
    ...
```

It should not require editing 15 unrelated `if provider == ...` blocks.

---

## 19.3 Liskov Substitution Principle

A subtype must be usable wherever its parent type is expected without surprising behavior.

Suppose `ModelProvider.generate()` promises:

* It accepts a valid request.
* It returns a `GenerationResponse`.
* It raises documented exceptions on failure.

A subclass should not:

* Return an unrelated dictionary
* Silently return `None`
* Reject temperatures accepted by the common contract without documentation
* Modify the request object unexpectedly
* require hidden global setup

A subclass that violates the contract breaks polymorphism.

---

## 19.4 Interface Segregation Principle

Prefer small interfaces.

Too broad:

```python
class AIPlatform:
    def generate(...): ...
    def embed(...): ...
    def index(...): ...
    def rerank(...): ...
    def fine_tune(...): ...
    def deploy(...): ...
    def evaluate(...): ...
```

A simple RAG pipeline might only need `generate()`.

Better:

```python
class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]:
        ...
```

---

## 19.5 Dependency Inversion Principle

High-level policy should not depend directly on low-level vendor details.

Bad:

```python
class RagPipeline:
    def __init__(self):
        self.client = SpecificVendorSDK(api_key="...")
```

Better:

```python
class RagPipeline:
    def __init__(self, generator: TextGenerator):
        self._generator = generator
```

The application startup code creates the concrete provider and injects it.

This separates:

* Object construction
* Business workflow
* Vendor integration

---

# 20. Useful design patterns in GenAI systems

## 20.1 Strategy pattern

Encapsulates interchangeable algorithms.

Examples:

* Chunking strategies
* Retrieval strategies
* Reranking strategies
* Prompt selection strategies
* Model routing strategies

```python
class ChunkingStrategy(Protocol):
    def chunk(self, text: str) -> list[str]:
        ...
```

Implementations:

```text
FixedSizeChunker
SentenceChunker
MarkdownChunker
SemanticChunker
```

---

## 20.2 Adapter pattern

Converts an external service's interface into your internal interface.

Examples:

* LLM SDK adapter
* Vector DB adapter
* Embedding service adapter
* Observability adapter

The `OpenAIModelProvider` in the earlier example is an adapter.

---

## 20.3 Factory pattern

Centralizes object creation.

```python
class ModelProviderFactory:
    @staticmethod
    def create(
        provider_name: str,
        config: dict,
        clients: dict,
    ) -> ModelProvider:
        if provider_name == "openai":
            return OpenAIModelProvider(
                model_name=config["model_name"],
                client=clients["openai"],
            )

        if provider_name == "anthropic":
            return AnthropicModelProvider(
                model_name=config["model_name"],
                client=clients["anthropic"],
            )

        if provider_name == "local":
            return LocalModelProvider(
                model_name=config["model_name"],
                inference_engine=clients["local"],
            )

        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )
```

Factories can help when construction requires configuration and several dependencies.

Do not hide the entire application behind complicated factories. Object creation should remain traceable.

---

## 20.4 Decorator pattern

Adds behavior around an object without changing it.

Examples:

* Retry
* Caching
* Tracing
* Metrics
* Rate limiting
* Circuit breaking
* Input redaction

```text
TracingProvider
  └── RetryingProvider
       └── CachedProvider
            └── OpenAIProvider
```

Be careful not to create so many wrappers that debugging becomes difficult.

---

## 20.5 Repository pattern

Separates domain logic from storage details.

Examples:

* Conversation repository
* Prompt repository
* Evaluation-result repository
* Document metadata repository

```python
class ConversationRepository(Protocol):
    def save_message(self, conversation_id: str, message: str) -> None:
        ...

    def get_history(self, conversation_id: str) -> list[str]:
        ...
```

Implementations might use PostgreSQL, Redis, or an in-memory store.

---

# 21. Best practices for production AI OOP

## 21.1 Keep domain objects provider-neutral

Prefer:

```python
GenerationRequest
GenerationResponse
DocumentChunk
RagAnswer
```

Avoid passing provider SDK objects throughout the application.

This prevents vendor-specific types from contaminating the entire codebase.

---

## 21.2 Inject dependencies

Prefer:

```python
pipeline = RagPipeline(
    embedder=embedder,
    vector_store=vector_store,
    generator=generator,
    ...
)
```

Avoid creating dependencies deep inside business classes.

Dependency injection supports:

* Unit testing
* Configuration
* Provider replacement
* Local development
* Clear lifecycle management

---

## 21.3 Use immutable configuration

```python
@dataclass(frozen=True)
class ModelConfig:
    model_name: str
    timeout_seconds: float
```

Immutable config prevents unexpected runtime changes.

---

## 21.4 Separate configuration from runtime state

Configuration:

```python
@dataclass(frozen=True)
class RetryConfig:
    max_attempts: int
    initial_delay_seconds: float
```

Runtime state:

```python
class CircuitBreaker:
    def __init__(self):
        self._failure_count = 0
        self._is_open = False
```

Do not mix long-lived mutable operational state into configuration objects.

---

## 21.5 Keep constructors lightweight

Constructors should not perform unpredictable external operations.

Prefer:

```python
provider = Provider(client=client)
```

over:

```python
provider = Provider()  # Internally authenticates, downloads models,
                       # opens DB connections and starts threads.
```

---

## 21.6 Design explicit exceptions

Instead of exposing arbitrary provider exceptions everywhere, define application-level errors:

```python
class ModelProviderError(Exception):
    """Base error for model-provider failures."""


class ModelTimeoutError(ModelProviderError):
    pass


class ModelRateLimitError(ModelProviderError):
    pass


class ModelAuthenticationError(ModelProviderError):
    pass
```

Provider adapters can translate SDK errors into these normalized exceptions.

This prevents higher-level code from depending on vendor-specific exception classes.

---

## 21.7 Keep synchronous and asynchronous contracts clear

Avoid one implementation returning a normal value while another unexpectedly returns a coroutine.

Use separate explicit contracts when needed:

```python
class AsyncTextGenerator(Protocol):
    async def generate(self, prompt: str) -> str:
        ...
```

Do not mix sync and async behavior under an ambiguous interface.

---

## 21.8 Make observability a boundary concern

Metrics and tracing are often cleaner as decorators or injected collaborators rather than scattered logging statements.

Capture information such as:

* Provider
* Model name
* Request duration
* Token usage
* Retry count
* Error category
* Retrieval latency
* Number of retrieved chunks
* Prompt version

Never log raw confidential prompts by default.

---

## 21.9 Prefer explicit behavior over “clever” metaprogramming

Dynamic class creation, complicated descriptors, and deep metaclass logic may reduce readability.

In production AI systems, maintainability usually matters more than saving a few lines of code.

---

## 21.10 Use type hints

```python
def answer(
    self,
    question: str,
) -> RagAnswer:
    ...
```

Type hints improve:

* IDE support
* Static analysis
* Code review
* Interface clarity
* Refactoring safety

Type hints do not enforce correctness at runtime by themselves, but they make large codebases significantly easier to understand.

---

# 22. Common OOP pitfalls in AI systems

## 22.1 Creating classes without meaningful state or behavior

Unnecessary:

```python
class TextUtils:
    @staticmethod
    def clean(text: str) -> str:
        return text.strip()
```

A module-level function may be clearer:

```python
def clean_text(text: str) -> str:
    return text.strip()
```

Not every function needs a class.

---

## 22.2 Deep inheritance hierarchies

Problematic:

```text
BaseProvider
  └── CloudProvider
       └── ManagedCloudProvider
            └── StreamingManagedProvider
                 └── RegionalStreamingProvider
```

Deep hierarchies create:

* Hidden behavior
* Fragile overrides
* Difficult debugging
* Strong coupling

Prefer shallow interfaces and composition.

---

## 22.3 A giant base class

A base provider should not force every implementation to support:

* Streaming
* Embeddings
* Fine-tuning
* Image generation
* Audio
* Batch jobs
* Tool calling

Use smaller capability interfaces:

```python
class TextGenerator(Protocol):
    ...


class StreamingTextGenerator(Protocol):
    ...


class Embedder(Protocol):
    ...
```

---

## 22.4 Leaking SDK types

Bad:

```python
def answer(...) -> VendorSpecificResponse:
    ...
```

This couples the entire application to a provider.

Normalize at the adapter boundary:

```python
def answer(...) -> GenerationResponse:
    ...
```

---

## 22.5 Mutable class variables

Bad:

```python
class ModelCache:
    entries = {}
```

Every instance shares `entries`.

Make sharing intentional and thread-safe, or use an instance variable.

---

## 22.6 Mutable default arguments

Bad:

```python
def __init__(self, metadata={}):
    self.metadata = metadata
```

Safer:

```python
def __init__(self, metadata=None):
    self.metadata = {} if metadata is None else metadata
```

For dataclasses:

```python
metadata: dict = field(default_factory=dict)
```

---

## 22.7 Expensive constructors

Avoid network calls, large model loading, and index building in `__init__`.

These make failure handling and testing difficult.

---

## 22.8 Overusing getters and setters

Java-style code is often unnecessary in Python:

```python
def get_model_name(self):
    return self._model_name

def set_model_name(self, value):
    self._model_name = value
```

Use a public attribute when no logic is needed or use `@property` when validation or computation is required.

---

## 22.9 Breaking subclass contracts

A subclass should not return a completely different response type or silently ignore required behavior.

This breaks polymorphism and violates substitutability.

---

## 22.10 Catching every exception

Bad:

```python
try:
    ...
except Exception:
    return None
```

This hides:

* Programming bugs
* Authentication failures
* Invalid configuration
* Data corruption

Catch only errors you can meaningfully handle, and preserve context when re-raising.

---

## 22.11 Logging secrets in `__repr__`

Bad:

```python
def __repr__(self):
    return f"Client(api_key={self.api_key})"
```

Secrets may appear in:

* Logs
* Tracebacks
* Notebooks
* Monitoring systems
* Test output

---

## 22.12 Overengineering early prototypes

A ten-line experiment does not need fifteen interfaces and a dependency-injection framework.

A practical progression is:

```text
Simple functions
    ↓
Repeated responsibilities become clear
    ↓
Extract cohesive classes
    ↓
Introduce interfaces at changing external boundaries
    ↓
Add factories/decorators only when justified
```

---

# 23. Practical strategy for a large AI codebase

A maintainable project might use a structure like:

```text
src/
├── domain/
│   ├── generation.py
│   ├── retrieval.py
│   └── documents.py
├── interfaces/
│   ├── model_provider.py
│   ├── embedder.py
│   └── vector_store.py
├── adapters/
│   ├── openai_provider.py
│   ├── local_provider.py
│   ├── pgvector_store.py
│   └── managed_vector_store.py
├── services/
│   ├── rag_pipeline.py
│   └── ingestion_pipeline.py
├── config/
│   └── settings.py
└── tests/
    ├── unit/
    └── integration/
```

### Domain layer

Contains provider-neutral concepts:

* `GenerationRequest`
* `GenerationResponse`
* `DocumentChunk`
* `RagAnswer`

### Interfaces

Define required behavior:

* `TextGenerator`
* `Embedder`
* `VectorStore`

### Adapters

Contain vendor-specific integration logic.

### Services

Coordinate business workflows.

### Tests

* Unit tests use fakes.
* Integration tests test actual adapters.
* End-to-end tests verify the deployed flow.

---

# 24. Senior-level design checklist

Before creating a class, ask:

* Does this object have a clear responsibility?
* Does it own meaningful state or behavior?
* Can its public contract be explained in one sentence?
* Are external vendor details isolated?
* Can dependencies be injected?
* Can I test it without network calls?
* Is inheritance truly representing an “is-a” relationship?
* Would composition make change easier?
* Are configuration objects immutable where practical?
* Could `__repr__` expose secrets?
* Are errors explicit and meaningful?
* Are async and sync behaviors unambiguous?
* Is the abstraction based on a real variation point rather than speculation?

---

# 25. Interview Q&A

## Q1. What are the four main OOP principles?

**Answer:**

* **Encapsulation:** Keep related state and behavior together and protect object invariants.
* **Abstraction:** Expose essential behavior while hiding implementation details.
* **Inheritance:** Create specialized classes from a common parent.
* **Polymorphism:** Use different implementations through the same interface.

In production Python, composition and protocols are often used alongside these principles.

---

## Q2. How would you design support for multiple LLM providers?

**Answer:**

Define a small provider-neutral interface such as `generate(request) -> response`. Create one adapter per provider, normalize request and response objects, inject the selected provider into business services, and translate provider-specific exceptions into application-level errors. This prevents vendor SDK details from spreading through the codebase.

---

## Q3. Why is composition often better than inheritance for a RAG pipeline?

**Answer:**

Embedding, retrieval, reranking, prompt building, and generation vary independently. Composition lets each component be replaced or tested separately. Inheritance would create rigid hierarchies and potentially one subclass for every component combination.

---

## Q4. What is the difference between an abstract base class and a protocol?

**Answer:**

An abstract base class uses explicit inheritance and can provide shared implementation plus runtime enforcement. A protocol uses structural typing: an object satisfies the contract if it has the required methods. Protocols create looser coupling and are often convenient for dependency injection and testing.

---

## Q5. When would you use `@classmethod` rather than `@staticmethod`?

**Answer:**

Use `@classmethod` when the method needs the class, usually for alternative constructors or subclass-aware factories. Use `@staticmethod` for stateless logic that belongs conceptually to the class but needs neither the instance nor the class.

---

## Q6. Why use dataclasses in ML and GenAI systems?

**Answer:**

Dataclasses reduce boilerplate for configuration, requests, responses, retrieved chunks, tool inputs, and evaluation records. They generate methods such as `__init__`, `__repr__`, and `__eq__`. Frozen dataclasses are useful for immutable configuration and reproducibility.

---

## Q7. What is the Liskov Substitution Principle in an LLM provider hierarchy?

**Answer:**

Any concrete model provider should be usable wherever the base provider contract is expected. It must accept the documented request, return the documented response type, preserve expected semantics, and raise predictable errors. A subclass that returns an unrelated type or silently changes the contract is not substitutable.

---

## Q8. How would you make a RAG pipeline easy to unit test?

**Answer:**

Inject interfaces for the embedder, vector store, reranker, prompt builder, and generator. In unit tests, replace them with deterministic fakes. Test orchestration and edge cases without calling real external systems. Test each adapter separately with integration tests.

---

## Q9. What problems can mutable class variables cause?

**Answer:**

Mutable class variables are shared across every instance. This can cause state leakage, test interference, race conditions, and unexpected behavior. Use instance variables unless shared state is intentional, controlled, and thread-safe.

---

## Q10. What is a common sign that an OOP design is overengineered?

**Answer:**

The code has many base classes, factories, wrappers, or extension points but only one implementation and no realistic variation requirement. Good abstractions usually emerge around actual boundaries such as model providers, vector stores, storage systems, or test doubles—not hypothetical future needs.

---

# 26. Final revision summary

```text
Class       = Blueprint
Object      = Instance of a class
Attribute   = Object state
Method      = Object behavior

Encapsulation = Protect state and hide internals
Abstraction   = Expose a stable contract
Inheritance   = Model a genuine is-a relationship
Polymorphism  = Use multiple implementations through one interface
Composition   = Assemble objects using has-a relationships

Instance variable = Unique to one object
Class variable    = Shared at class level
@staticmethod     = Uses neither self nor cls
@classmethod      = Receives cls
@property             = Controlled attribute access
@dataclass         = Data-oriented class with generated boilerplate

Best production default:
Small interfaces + dependency injection + composition + typed domain objects
```

The key Senior AI Engineer insight is that OOP is not primarily about writing more classes. It is about defining stable boundaries so models, retrieval systems, databases, and external services can evolve without forcing the entire AI platform to change.
