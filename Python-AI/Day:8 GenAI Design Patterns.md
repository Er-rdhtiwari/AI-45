# Day 8 – Design Patterns & Clean Architecture for GenAI Systems

## 1. Beginner Summary

1. **Design patterns** are reusable approaches to common software design problems.
2. **Clean architecture** keeps business logic separate from frameworks, databases, APIs, and model providers.
3. In GenAI systems, patterns help you switch LLMs, vector databases, retrievers, and rerankers without rewriting the whole application.
4. A well-designed RAG or agent system is made of small components with clear responsibilities.
5. The main goal is not to use as many patterns as possible—it is to make the system easier to test, change, operate, and understand.

---

# 2. Why Architecture Matters in GenAI Systems

A prototype GenAI application may initially look like this:

```python
def answer_question(question: str) -> str:
    documents = vector_db.search(question)
    prompt = build_prompt(question, documents)
    response = openai_client.chat(prompt)
    return response
```

This is acceptable for an experiment. However, a production system soon needs:

* Multiple LLM providers
* Different embedding models
* Hybrid retrieval
* Reranking
* Prompt versioning
* Caching
* Authentication
* Rate limiting
* Logging and tracing
* Evaluation
* Guardrails
* Retry logic
* Agent tools
* Human escalation
* Background ingestion workers

If all of this logic is placed in one function or one large class, the application becomes difficult to:

* Test
* Debug
* Extend
* Deploy
* Operate
* Replace individual components

Clean architecture divides the application into components that have clear responsibilities.

---

# 3. Core Architecture Mental Model

A useful production architecture is:

```text
Client
  |
  v
API Layer
  |
  v
Application / Service Layer
  |
  v
Domain Interfaces and Business Rules
  |
  v
Infrastructure Implementations
  |
  +---- LLM provider
  +---- Vector database
  +---- SQL database
  +---- Cache
  +---- Message queue
  +---- External tools
```

The most important dependency rule is:

> Core application logic should not depend directly on a specific framework or vendor.

For example, your RAG service should not require OpenAI-specific objects throughout the application. It should depend on a general `LLMClient` interface.

```text
Bad dependency:

RagService ---> OpenAI SDK directly


Better dependency:

RagService ---> LLMClient interface
                    ^
                    |
             OpenAIAdapter
             AnthropicAdapter
             WatsonxAdapter
```

This makes provider replacement much easier.

---

# 4. SOLID Principles for GenAI Services

SOLID is a collection of five design principles that help produce maintainable object-oriented systems.

You do not need to apply every principle rigidly. Use them as design guidance.

---

## 4.1 S — Single Responsibility Principle

> A class or module should have one primary reason to change.

A class should not retrieve documents, build prompts, call the LLM, evaluate answers, and save audit logs all at once.

### Poor design

```python
class RagApplication:
    def answer(self, question: str) -> str:
        # Connect to vector DB
        # Retrieve chunks
        # Rerank chunks
        # Build prompt
        # Call LLM
        # Save audit record
        # Calculate evaluation score
        # Return response
        ...
```

This class has too many responsibilities.

### Better design

```text
Retriever              -> finds relevant documents
Reranker               -> reorders retrieved documents
PromptBuilder           -> creates the LLM prompt
LLMClient               -> communicates with a model provider
ConversationRepository  -> stores conversation data
RagService              -> coordinates the workflow
```

### GenAI examples

* `DocumentChunker` only chunks documents.
* `EmbeddingClient` only produces embeddings.
* `Retriever` only retrieves candidate chunks.
* `GuardrailService` only validates input or output.
* `AgentOrchestrator` coordinates agent steps but does not implement every tool itself.

### Interview explanation

“Single responsibility prevents the RAG orchestration class from becoming a god object. Retrieval, prompting, model calls, persistence, and evaluation should be separate components.”

---

## 4.2 O — Open/Closed Principle

> Software components should be open for extension but closed for modification.

You should be able to add a new retrieval strategy or model provider without modifying large amounts of existing code.

### Poor design

```python
class Retriever:
    def retrieve(self, query: str, mode: str):
        if mode == "vector":
            ...
        elif mode == "keyword":
            ...
        elif mode == "hybrid":
            ...
        elif mode == "graph":
            ...
```

Every new retrieval mode requires editing the same class.

### Better design

```python
from typing import Protocol


class RetrievalStrategy(Protocol):
    def retrieve(self, query: str) -> list[str]:
        ...


class VectorRetrieval:
    def retrieve(self, query: str) -> list[str]:
        return ["vector result 1", "vector result 2"]


class KeywordRetrieval:
    def retrieve(self, query: str) -> list[str]:
        return ["keyword result 1", "keyword result 2"]


class HybridRetrieval:
    def retrieve(self, query: str) -> list[str]:
        return ["combined result 1", "combined result 2"]
```

The service depends on the strategy interface:

```python
class SearchService:
    def __init__(self, strategy: RetrievalStrategy):
        self.strategy = strategy

    def search(self, query: str) -> list[str]:
        return self.strategy.retrieve(query)
```

Now new strategies can be added without changing `SearchService`.

---

## 4.3 L — Liskov Substitution Principle

> Any implementation of an interface should be usable without breaking the expected behavior.

Suppose a service accepts an `LLMClient`. Every provider implementation should follow the same behavioral contract.

```python
from typing import Protocol


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

Possible implementations:

```python
class OpenAIClient:
    def generate(self, prompt: str) -> str:
        return "Response from OpenAI"


class WatsonxClient:
    def generate(self, prompt: str) -> str:
        return "Response from watsonx"
```

Both should:

* Accept the same expected input type
* Return the same output type
* Raise documented application-level exceptions
* Follow similar timeout and cancellation behavior

### Violation example

Imagine one implementation returns plain text:

```python
"Generated answer"
```

But another returns a provider-specific object:

```python
ProviderResponse(
    choices=[...],
    usage={...},
    provider_metadata={...},
)
```

The second implementation cannot transparently replace the first.

### Better approach

Normalize provider responses:

```python
from dataclasses import dataclass


@dataclass
class GenerationResult:
    text: str
    input_tokens: int
    output_tokens: int
    model_name: str
```

Every provider adapter returns `GenerationResult`.

---

## 4.4 I — Interface Segregation Principle

> Clients should not be forced to depend on methods they do not use.

Avoid creating one giant interface for all AI operations.

### Poor design

```python
class AIProvider:
    def chat(self, messages): ...
    def embed(self, texts): ...
    def transcribe(self, audio): ...
    def generate_image(self, prompt): ...
    def fine_tune(self, dataset): ...
    def rerank(self, query, documents): ...
```

A text-only model provider may not support embeddings, images, transcription, or reranking.

### Better design

```python
class ChatModel:
    def generate(self, messages):
        ...


class EmbeddingModel:
    def embed(self, texts):
        ...


class Reranker:
    def rerank(self, query, documents):
        ...


class SpeechToTextModel:
    def transcribe(self, audio):
        ...
```

A provider adapter implements only the interfaces it supports.

### GenAI benefit

This is especially useful because AI providers have different capabilities. One provider may offer chat and embeddings, while another may only offer reranking.

---

## 4.5 D — Dependency Inversion Principle

> High-level business logic should depend on abstractions, not concrete infrastructure implementations.

### Poor design

```python
class RagService:
    def __init__(self):
        self.vector_db = PineconeClient(...)
        self.llm = OpenAIClient(...)
```

`RagService` is tightly coupled to Pinecone and OpenAI.

### Better design

```python
from typing import Protocol


class Retriever(Protocol):
    def retrieve(self, query: str, top_k: int) -> list[str]:
        ...


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class RagService:
    def __init__(
        self,
        retriever: Retriever,
        llm_client: LLMClient,
    ):
        self.retriever = retriever
        self.llm_client = llm_client
```

Dependencies are provided from outside:

```python
retriever = PineconeRetriever(...)
llm_client = OpenAIAdapter(...)

rag_service = RagService(
    retriever=retriever,
    llm_client=llm_client,
)
```

This is called **dependency injection**.

### Benefits

* Easy unit testing
* Easy provider replacement
* Lower vendor lock-in
* Cleaner configuration
* Easier local development

---

# 5. Factory Pattern

## Concept

The Factory pattern centralizes object creation.

Instead of spreading provider-selection logic across the codebase, one factory decides which implementation to create.

### Typical GenAI uses

* Selecting an LLM provider
* Selecting an embedding provider
* Selecting a vector database
* Selecting a document loader
* Selecting an agent tool
* Selecting a model based on task or tenant

---

## Model Provider Factory

```python
from typing import Protocol


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class OpenAIAdapter:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # Real implementation would call the OpenAI API.
        return f"OpenAI response from {self.model_name}"


class WatsonxAdapter:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # Real implementation would call watsonx.ai.
        return f"watsonx response from {self.model_name}"


class LLMFactory:
    @staticmethod
    def create(provider: str, model_name: str) -> LLMClient:
        if provider == "openai":
            return OpenAIAdapter(model_name)

        if provider == "watsonx":
            return WatsonxAdapter(model_name)

        raise ValueError(f"Unsupported LLM provider: {provider}")
```

Usage:

```python
llm = LLMFactory.create(
    provider="openai",
    model_name="production-chat-model",
)

response = llm.generate("Explain RAG")
```

---

## Where the Factory Helps

Without a factory, code may contain repeated conditional logic:

```python
if provider == "openai":
    ...
elif provider == "watsonx":
    ...
```

This may appear in:

* API handlers
* Worker jobs
* Evaluation scripts
* Agent services
* Batch pipelines

A factory keeps creation logic in one place.

---

## Factory Trade-offs

### Advantages

* Centralized object creation
* Hides provider-specific setup
* Simplifies configuration-based selection
* Makes dependency wiring easier

### Risks

* The factory can become a giant conditional block
* It may hide too much configuration
* It can become a service locator, where dependencies are obtained globally

### Better extension

For many providers, use a registry:

```python
class LLMFactory:
    _providers = {}

    @classmethod
    def register(cls, name: str, provider_class):
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name: str, **kwargs):
        try:
            provider_class = cls._providers[name]
        except KeyError as exc:
            raise ValueError(f"Unknown provider: {name}") from exc

        return provider_class(**kwargs)
```

Registration:

```python
LLMFactory.register("openai", OpenAIAdapter)
LLMFactory.register("watsonx", WatsonxAdapter)
```

---

# 6. Strategy Pattern

## Concept

The Strategy pattern defines multiple interchangeable ways to perform an operation.

The caller selects a strategy without needing to know its internal implementation.

### Typical GenAI uses

* Dense retrieval
* Sparse retrieval
* Hybrid retrieval
* Reranking algorithms
* Chunking algorithms
* Prompt selection
* Model routing
* Agent planning approaches
* Response validation
* Cost optimization policies

---

## Retrieval Strategy Example

```python
from typing import Protocol


class RetrievalStrategy(Protocol):
    def retrieve(self, query: str, top_k: int) -> list[str]:
        ...


class DenseRetrievalStrategy:
    def retrieve(self, query: str, top_k: int) -> list[str]:
        # Uses embeddings and vector similarity.
        return [f"Dense result for '{query}'"][:top_k]


class KeywordRetrievalStrategy:
    def retrieve(self, query: str, top_k: int) -> list[str]:
        # Uses lexical matching such as BM25.
        return [f"Keyword result for '{query}'"][:top_k]


class HybridRetrievalStrategy:
    def __init__(
        self,
        dense: RetrievalStrategy,
        keyword: RetrievalStrategy,
    ):
        self.dense = dense
        self.keyword = keyword

    def retrieve(self, query: str, top_k: int) -> list[str]:
        dense_results = self.dense.retrieve(query, top_k)
        keyword_results = self.keyword.retrieve(query, top_k)

        # A production implementation would normalize scores,
        # merge duplicates, and possibly use reciprocal rank fusion.
        merged = dense_results + keyword_results

        return merged[:top_k]
```

RAG service:

```python
class RagService:
    def __init__(
        self,
        retrieval_strategy: RetrievalStrategy,
        llm_client: LLMClient,
    ):
        self.retrieval_strategy = retrieval_strategy
        self.llm_client = llm_client

    def answer(self, question: str) -> str:
        documents = self.retrieval_strategy.retrieve(
            query=question,
            top_k=5,
        )

        context = "\n".join(documents)
        prompt = f"""
Answer the question using only the supplied context.

Context:
{context}

Question:
{question}
"""

        return self.llm_client.generate(prompt)
```

The retrieval approach can be changed without modifying `RagService`.

---

## Runtime Strategy Selection

A system may select strategies based on query type:

```python
class RetrievalRouter:
    def __init__(
        self,
        dense: RetrievalStrategy,
        keyword: RetrievalStrategy,
        hybrid: RetrievalStrategy,
    ):
        self.dense = dense
        self.keyword = keyword
        self.hybrid = hybrid

    def select(self, query: str) -> RetrievalStrategy:
        # IDs and exact names often work better with keyword search.
        if "policy id" in query.lower():
            return self.keyword

        # A real router might use a classifier or rules.
        if len(query.split()) > 8:
            return self.hybrid

        return self.dense
```

Be careful: a router selects a strategy, while the strategy performs the operation.

---

# 7. Adapter Pattern

## Concept

The Adapter pattern converts one interface into another interface expected by the application.

Different providers have different:

* Method names
* Request formats
* Authentication methods
* Response schemas
* Error types
* Streaming formats
* Metadata structures

Adapters hide these differences.

---

## LLM Provider Adapter

Your application interface:

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class GenerationResult:
    text: str
    input_tokens: int
    output_tokens: int
    model_name: str


class ChatModel(Protocol):
    def generate(
        self,
        messages: list[ChatMessage],
    ) -> GenerationResult:
        ...
```

OpenAI-style adapter:

```python
class OpenAIChatAdapter:
    def __init__(self, sdk_client, model_name: str):
        self.sdk_client = sdk_client
        self.model_name = model_name

    def generate(
        self,
        messages: list[ChatMessage],
    ) -> GenerationResult:
        provider_messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

        response = self.sdk_client.chat(
            model=self.model_name,
            messages=provider_messages,
        )

        return GenerationResult(
            text=response.output_text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            model_name=self.model_name,
        )
```

Another provider may use a different request and response format, but its adapter still returns `GenerationResult`.

---

## Vector Database Adapter

Application interface:

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass
class RetrievedChunk:
    chunk_id: str
    content: str
    score: float
    metadata: dict


class VectorStore(Protocol):
    def search(
        self,
        vector: list[float],
        top_k: int,
        filters: dict | None = None,
    ) -> list[RetrievedChunk]:
        ...
```

Implementations might include:

```text
PineconeVectorStoreAdapter
MilvusVectorStoreAdapter
WeaviateVectorStoreAdapter
PgVectorStoreAdapter
ElasticsearchVectorStoreAdapter
```

The rest of the application does not need provider-specific result objects.

---

## Adapter Benefits

* Reduces vendor lock-in
* Normalizes provider behavior
* Keeps SDK objects out of business logic
* Simplifies testing
* Makes migrations safer

## Adapter Limitation

Not every provider feature fits into one universal interface.

For example, one model may support:

* Prompt caching
* Native tool calls
* JSON schema output
* Reasoning controls
* Multimodal inputs

A very generic interface may hide useful provider capabilities.

A practical solution is:

* Keep a common core interface
* Add optional capability interfaces
* Avoid exposing raw SDK objects in the whole codebase

---

# 8. Decorator Pattern

## Concept

A Decorator wraps an existing component and adds behavior without changing the original component.

Typical GenAI decorators include:

* Logging
* Tracing
* Metrics
* Caching
* Authentication
* Authorization
* Retries
* Rate limiting
* Token-budget enforcement
* Content filtering
* Cost tracking

---

## Logging Decorator

```python
import time


class LoggingLLMDecorator:
    def __init__(self, wrapped: LLMClient):
        self.wrapped = wrapped

    def generate(self, prompt: str) -> str:
        start_time = time.perf_counter()

        try:
            result = self.wrapped.generate(prompt)

            elapsed = time.perf_counter() - start_time
            print(
                f"LLM request succeeded in {elapsed:.3f} seconds"
            )

            return result

        except Exception:
            elapsed = time.perf_counter() - start_time
            print(
                f"LLM request failed after {elapsed:.3f} seconds"
            )
            raise
```

---

## Cache Decorator

```python
import hashlib


class CachedLLMDecorator:
    def __init__(self, wrapped: LLMClient, cache: dict[str, str]):
        self.wrapped = wrapped
        self.cache = cache

    def generate(self, prompt: str) -> str:
        cache_key = hashlib.sha256(
            prompt.encode("utf-8")
        ).hexdigest()

        if cache_key in self.cache:
            return self.cache[cache_key]

        result = self.wrapped.generate(prompt)
        self.cache[cache_key] = result

        return result
```

---

## Retry Decorator

```python
import time


class RetryLLMDecorator:
    def __init__(
        self,
        wrapped: LLMClient,
        max_attempts: int = 3,
        initial_delay_seconds: float = 0.5,
    ):
        self.wrapped = wrapped
        self.max_attempts = max_attempts
        self.initial_delay_seconds = initial_delay_seconds

    def generate(self, prompt: str) -> str:
        delay = self.initial_delay_seconds

        for attempt in range(1, self.max_attempts + 1):
            try:
                return self.wrapped.generate(prompt)

            except TimeoutError:
                # Retry only errors known to be temporary.
                if attempt == self.max_attempts:
                    raise

                time.sleep(delay)
                delay *= 2

        raise RuntimeError("Unreachable retry state")
```

---

## Combining Decorators

```python
base_llm = OpenAIAdapter("production-model")

llm = LoggingLLMDecorator(
    CachedLLMDecorator(
        RetryLLMDecorator(
            wrapped=base_llm,
            max_attempts=3,
        ),
        cache={},
    )
)
```

Conceptually:

```text
Logging
   |
Caching
   |
Retries
   |
OpenAI Adapter
```

The order matters.

For example:

```text
Cache outside retry:
- Cache is checked first.
- Only cache misses enter retry logic.

Retry outside cache:
- Every retry may repeat the cache lookup.
```

---

## Decorator vs Middleware

They are related but not identical.

* **Decorator:** wraps a particular object or component.
* **Middleware:** usually wraps request processing at the framework or transport level.

Examples:

* API authentication → often middleware
* LLM cost tracking → often an LLM decorator
* Retrieval tracing → often a retriever decorator

---

# 9. Facade Pattern

## Concept

A Facade exposes a simple interface over a complex subsystem.

A production RAG system may contain:

```text
Query validation
Query rewriting
Retrieval
Metadata filtering
Reranking
Context building
Prompt creation
Model invocation
Citation formatting
Guardrails
Audit logging
Evaluation sampling
```

The API layer should not coordinate every step directly.

Instead, it calls a simple facade such as:

```python
result = rag_service.answer(request)
```

---

## RagService Facade

```python
from dataclasses import dataclass


@dataclass
class RagRequest:
    question: str
    user_id: str
    conversation_id: str | None = None


@dataclass
class Citation:
    document_id: str
    chunk_id: str


@dataclass
class RagResponse:
    answer: str
    citations: list[Citation]


class RagService:
    def __init__(
        self,
        query_validator,
        retriever,
        reranker,
        prompt_builder,
        llm_client,
        audit_repository,
    ):
        self.query_validator = query_validator
        self.retriever = retriever
        self.reranker = reranker
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        self.audit_repository = audit_repository

    def answer(self, request: RagRequest) -> RagResponse:
        # 1. Validate the incoming question.
        self.query_validator.validate(request.question)

        # 2. Retrieve a broad candidate set.
        candidates = self.retriever.retrieve(
            query=request.question,
            top_k=20,
        )

        # 3. Rerank and keep the strongest chunks.
        selected_chunks = self.reranker.rerank(
            query=request.question,
            documents=candidates,
            top_k=5,
        )

        # 4. Build a grounded prompt.
        prompt = self.prompt_builder.build(
            question=request.question,
            chunks=selected_chunks,
        )

        # 5. Generate the final answer.
        generated_answer = self.llm_client.generate(prompt)

        # 6. Extract citations from selected chunks.
        citations = [
            Citation(
                document_id=chunk.metadata["document_id"],
                chunk_id=chunk.chunk_id,
            )
            for chunk in selected_chunks
        ]

        response = RagResponse(
            answer=generated_answer,
            citations=citations,
        )

        # 7. Save an audit record.
        self.audit_repository.save(
            request=request,
            response=response,
        )

        return response
```

The API layer remains simple:

```python
def answer_endpoint(request: RagRequest) -> RagResponse:
    return rag_service.answer(request)
```

---

## Facade vs God Object

A facade coordinates components. It should not contain all their internal logic.

Good facade:

```text
RagService calls Retriever, Reranker, PromptBuilder, LLMClient
```

Bad facade:

```text
RagService implements vector search, reranking mathematics,
prompt templates, provider API calls, SQL persistence, and metrics
inside one huge class
```

The facade is an orchestrator, not the entire application.

---

# 10. How Patterns Work Together

These patterns are commonly combined.

```text
                         Factory
                            |
                            v
                   Creates configured objects
                            |
                            v
API ---> RagService Facade ---> Retrieval Strategy
              |                       |
              |                       v
              |                Vector DB Adapter
              |
              v
       Decorated LLM Client
              |
       +------+------+
       |             |
    Logging       Caching
       |             |
       +------v------+
              |
        Provider Adapter
              |
          External LLM
```

Example:

* **Factory** creates the selected model provider.
* **Adapter** normalizes the provider API.
* **Decorator** adds retries, logging, and caching.
* **Strategy** determines the retrieval algorithm.
* **Facade** exposes one simple `answer()` operation.

---

# 11. Layered Architecture

A layered architecture separates the application according to responsibility.

A practical GenAI system may contain four main areas:

```text
1. API / Presentation Layer
2. Application / Service Layer
3. Domain Layer
4. Infrastructure / Data Layer
```

The user explicitly requested API, service, and data/infra layers. Adding a lightweight domain layer often improves separation further.

---

## 11.1 API Layer

### Responsibilities

* Accept HTTP requests
* Validate transport-level input
* Handle authentication
* Convert request payloads into application commands
* Call application services
* Map errors to HTTP responses
* Serialize responses

### Should not contain

* Vector search logic
* Prompt construction
* Agent planning
* LLM provider SDK calls
* Database queries
* Business rules

### Example

```python
# api/routes/rag.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    citations: list[str]


@router.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    rag_service=Depends(get_rag_service),
):
    result = rag_service.answer(
        RagRequest(
            question=request.question,
            user_id="authenticated-user-id",
        )
    )

    return AskResponse(
        answer=result.answer,
        citations=[
            citation.document_id
            for citation in result.citations
        ],
    )
```

The endpoint is thin.

---

## 11.2 Service Layer

### Responsibilities

* Coordinate use cases
* Execute RAG workflows
* Execute agent workflows
* Apply business policies
* Manage transactions
* Call domain interfaces
* Return application-level results

Examples:

```text
RagService
AgentService
DocumentIngestionService
ConversationService
EvaluationService
ModelRoutingService
```

### Example use case

```python
class DocumentIngestionService:
    def __init__(
        self,
        parser,
        chunker,
        embedding_model,
        vector_store,
    ):
        self.parser = parser
        self.chunker = chunker
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def ingest(self, file_path: str) -> int:
        document = self.parser.parse(file_path)
        chunks = self.chunker.split(document)

        embeddings = self.embedding_model.embed(
            [chunk.content for chunk in chunks]
        )

        self.vector_store.upsert(chunks, embeddings)

        return len(chunks)
```

---

## 11.3 Domain Layer

The domain layer contains stable business concepts and interfaces.

Examples:

```text
Document
DocumentChunk
Conversation
AgentState
ToolCall
Citation
RetrievalResult
GenerationResult
```

It may also contain business rules:

* A user can access only authorized documents.
* Every generated answer must include source citations.
* A high-risk response requires human review.
* An agent cannot execute a destructive tool without approval.
* Retrieved chunks must belong to the user's tenant.

The domain layer should not depend directly on:

* FastAPI
* Pinecone
* OpenAI SDK
* PostgreSQL drivers
* Redis
* Kafka

---

## 11.4 Data and Infrastructure Layer

### Responsibilities

* LLM API integration
* Vector database access
* SQL and NoSQL persistence
* Redis caching
* Message queues
* Object storage
* External tool APIs
* Observability integrations

Examples:

```text
OpenAIAdapter
WatsonxAdapter
PineconeVectorStore
PgVectorRepository
RedisCache
S3DocumentStorage
KafkaEventPublisher
ServiceNowToolAdapter
```

Infrastructure implements interfaces defined closer to the application or domain layer.

---

# 12. Dependency Direction

A clean dependency flow is:

```text
API Layer
   |
   v
Application Services
   |
   v
Domain Interfaces
   ^
   |
Infrastructure Implementations
```

Infrastructure depends on domain contracts—not the reverse.

For example:

```python
# domain/interfaces.py

class ConversationRepository(Protocol):
    def save(self, conversation: "Conversation") -> None:
        ...
```

Infrastructure implementation:

```python
# infrastructure/repositories/postgres_conversation_repository.py

class PostgresConversationRepository:
    def __init__(self, database):
        self.database = database

    def save(self, conversation: "Conversation") -> None:
        self.database.execute(
            """
            INSERT INTO conversations (id, user_id)
            VALUES (:id, :user_id)
            """,
            {
                "id": conversation.id,
                "user_id": conversation.user_id,
            },
        )
```

The domain does not need to know that PostgreSQL is used.

---

# 13. RAG Architecture Example

```text
                         ┌──────────────────────┐
                         │      API Layer       │
                         │  POST /v1/rag/ask    │
                         └──────────┬───────────┘
                                    |
                                    v
                         ┌──────────────────────┐
                         │     RagService       │
                         │      Facade          │
                         └──────────┬───────────┘
                                    |
              ┌─────────────────────┼──────────────────────┐
              |                     |                      |
              v                     v                      v
     ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
     │ Query Rewriter │    │   Retriever    │    │ Prompt Builder │
     └────────────────┘    └───────┬────────┘    └────────────────┘
                                    |
                             Strategy Interface
                                    |
                  ┌─────────────────┼─────────────────┐
                  |                 |                 |
                  v                 v                 v
             Dense Search     Keyword Search    Hybrid Search
                  |
                  v
           Vector Store Adapter
                  |
                  v
             Vector Database

                                    |
                                    v
                           Decorated LLM Client
                                    |
                     Logging -> Retry -> Cache
                                    |
                                    v
                            Provider Adapter
                                    |
                                    v
                              External LLM
```

---

# 14. Agent System Architecture

Agent systems introduce additional concerns:

* State
* Planning
* Tool selection
* Tool execution
* Permissions
* Checkpointing
* Human approval
* Retry and recovery
* Maximum step limits

A clean agent design may look like:

```text
API
 |
 v
AgentService / AgentFacade
 |
 +---- Planner Strategy
 |
 +---- State Repository
 |
 +---- Tool Registry
 |       |
 |       +---- SearchToolAdapter
 |       +---- TicketToolAdapter
 |       +---- DatabaseToolAdapter
 |
 +---- Policy Engine
 |
 +---- LLM Adapter
 |
 +---- Checkpoint Repository
```

---

## Agent Tool Interface

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass
class ToolResult:
    success: bool
    output: str
    error_code: str | None = None


class AgentTool(Protocol):
    @property
    def name(self) -> str:
        ...

    def execute(self, arguments: dict) -> ToolResult:
        ...
```

Concrete tool:

```python
class KnowledgeSearchTool:
    def __init__(self, retriever):
        self.retriever = retriever

    @property
    def name(self) -> str:
        return "knowledge_search"

    def execute(self, arguments: dict) -> ToolResult:
        query = arguments.get("query")

        if not query:
            return ToolResult(
                success=False,
                output="",
                error_code="MISSING_QUERY",
            )

        results = self.retriever.retrieve(query, top_k=5)

        return ToolResult(
            success=True,
            output="\n".join(
                result.content for result in results
            ),
        )
```

---

## Tool Registry as Factory and Lookup

```python
class ToolRegistry:
    def __init__(self, tools: list[AgentTool]):
        self._tools = {
            tool.name: tool
            for tool in tools
        }

    def get(self, tool_name: str) -> AgentTool:
        try:
            return self._tools[tool_name]
        except KeyError as exc:
            raise ValueError(
                f"Unknown agent tool: {tool_name}"
            ) from exc
```

The agent does not need to construct tools directly.

---

## Agent Planning as Strategy

```python
class PlanningStrategy(Protocol):
    def next_action(self, state: "AgentState") -> "AgentAction":
        ...


class RuleBasedPlanner:
    def next_action(self, state: "AgentState") -> "AgentAction":
        # Deterministic planning for predictable workflows.
        ...


class LLMPlanner:
    def next_action(self, state: "AgentState") -> "AgentAction":
        # Uses an LLM to choose the next action.
        ...
```

The same orchestrator can work with deterministic or LLM-based planning.

---

# 15. Suggested Project Structure

Here is a practical structure for a medium-to-large GenAI application:

```text
genai_app/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── error_handlers.py
│   │   ├── middleware/
│   │   │   ├── authentication.py
│   │   │   ├── request_logging.py
│   │   │   └── correlation_id.py
│   │   └── routes/
│   │       ├── rag.py
│   │       ├── agents.py
│   │       ├── documents.py
│   │       └── health.py
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── agent_service.py
│   │   ├── ingestion_service.py
│   │   ├── evaluation_service.py
│   │   └── model_routing_service.py
│   │
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── document.py
│   │   │   ├── chunk.py
│   │   │   ├── conversation.py
│   │   │   └── agent_state.py
│   │   ├── interfaces/
│   │   │   ├── llm.py
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   ├── reranker.py
│   │   │   ├── vector_store.py
│   │   │   └── repositories.py
│   │   └── exceptions.py
│   │
│   ├── models/
│   │   ├── requests.py
│   │   ├── responses.py
│   │   └── internal.py
│   │
│   ├── infrastructure/
│   │   ├── llms/
│   │   │   ├── openai_adapter.py
│   │   │   ├── watsonx_adapter.py
│   │   │   └── decorators.py
│   │   ├── embeddings/
│   │   │   ├── openai_embeddings.py
│   │   │   └── sentence_transformer.py
│   │   ├── vector_stores/
│   │   │   ├── pinecone_adapter.py
│   │   │   ├── pgvector_adapter.py
│   │   │   └── elasticsearch_adapter.py
│   │   ├── repositories/
│   │   │   ├── conversation_repository.py
│   │   │   └── audit_repository.py
│   │   ├── cache/
│   │   │   └── redis_cache.py
│   │   └── messaging/
│   │       └── event_publisher.py
│   │
│   ├── retrieval/
│   │   ├── dense_strategy.py
│   │   ├── keyword_strategy.py
│   │   ├── hybrid_strategy.py
│   │   ├── query_rewriter.py
│   │   └── filters.py
│   │
│   ├── reranking/
│   │   ├── cross_encoder.py
│   │   └── reciprocal_rank_fusion.py
│   │
│   ├── prompts/
│   │   ├── rag_prompt.py
│   │   ├── agent_prompt.py
│   │   └── prompt_registry.py
│   │
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── state.py
│   │   ├── planners/
│   │   ├── policies/
│   │   └── tools/
│   │       ├── search_tool.py
│   │       ├── ticket_tool.py
│   │       └── database_tool.py
│   │
│   ├── workers/
│   │   ├── document_ingestion_worker.py
│   │   ├── embedding_worker.py
│   │   └── evaluation_worker.py
│   │
│   ├── factories/
│   │   ├── llm_factory.py
│   │   ├── retriever_factory.py
│   │   └── vector_store_factory.py
│   │
│   ├── configs/
│   │   ├── settings.py
│   │   ├── logging.py
│   │   └── model_catalog.yaml
│   │
│   └── observability/
│       ├── metrics.py
│       ├── tracing.py
│       └── audit.py
│
├── tests/
│   ├── unit/
│   │   ├── test_rag_service.py
│   │   ├── test_hybrid_retrieval.py
│   │   └── test_agent_policy.py
│   ├── integration/
│   │   ├── test_vector_store.py
│   │   └── test_llm_adapter.py
│   ├── evaluation/
│   │   ├── test_retrieval_quality.py
│   │   └── test_answer_groundedness.py
│   └── fixtures/
│
├── scripts/
│   ├── ingest_documents.py
│   ├── create_index.py
│   └── run_evaluation.py
│
├── migrations/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 16. Purpose of the Requested Folders

## `api/`

Contains:

* REST endpoints
* API request validation
* Middleware
* Authentication integration
* HTTP error mapping

It should remain thin.

---

## `services/`

Contains application use cases:

* Answer a RAG question
* Run an agent
* Ingest a document
* Evaluate a response
* Route a request to a model

Services coordinate other components.

---

## `models/`

This name can be ambiguous in GenAI projects.

It may refer to:

1. API data models
2. Domain models
3. Machine learning model wrappers

To reduce confusion, many projects use:

```text
schemas/       -> API request and response schemas
domain/        -> business entities
infrastructure/llms/ -> LLM implementations
```

If your team uses `models/`, document its exact purpose.

---

## `configs/`

Contains configuration definitions:

* Environment variables
* Model names
* Timeout values
* Retrieval parameters
* Feature flags
* Logging setup

Avoid hardcoding these throughout the code.

Example:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_provider: str = "openai"
    llm_model_name: str
    retrieval_top_k: int = 20
    rerank_top_k: int = 5
    request_timeout_seconds: float = 30.0
```

Secrets should come from a secure secret manager or environment—not be committed to source control.

---

## `workers/`

Contains background processing logic:

* Document parsing
* Chunking
* Embedding generation
* Index updates
* Batch evaluations
* Conversation summarization
* Dead-letter retry processing

A request-response API should not perform long ingestion workloads synchronously.

---

## `tests/`

A mature GenAI codebase usually needs:

* Unit tests
* Integration tests
* Contract tests
* End-to-end tests
* Retrieval evaluation
* Generation evaluation
* Regression datasets

GenAI evaluation does not replace software testing. Both are required.

---

# 17. Dependency Injection Example

Dependency injection connects implementations at application startup.

```python
def build_rag_service(settings: Settings) -> RagService:
    llm_client = LLMFactory.create(
        provider=settings.llm_provider,
        model_name=settings.llm_model_name,
    )

    llm_client = LoggingLLMDecorator(
        RetryLLMDecorator(
            wrapped=llm_client,
            max_attempts=3,
        )
    )

    dense_retrieval = DenseRetrievalStrategy(...)
    keyword_retrieval = KeywordRetrievalStrategy(...)

    retrieval_strategy = HybridRetrievalStrategy(
        dense=dense_retrieval,
        keyword=keyword_retrieval,
    )

    return RagService(
        query_validator=QueryValidator(),
        retriever=retrieval_strategy,
        reranker=CrossEncoderReranker(...),
        prompt_builder=GroundedPromptBuilder(),
        llm_client=llm_client,
        audit_repository=PostgresAuditRepository(...),
    )
```

This wiring belongs near the application entry point, not inside the domain service.

This area is sometimes called the:

* Composition root
* Dependency injection container
* Bootstrap layer

---

# 18. Testing Benefits of Clean Architecture

Because services depend on interfaces, tests can use simple fake implementations.

```python
class FakeRetriever:
    def retrieve(self, query: str, top_k: int):
        return [
            RetrievedChunk(
                chunk_id="chunk-1",
                content="Employees receive 20 paid leave days.",
                score=0.95,
                metadata={"document_id": "policy-123"},
            )
        ]


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "Employees receive 20 paid leave days."


class FakeAuditRepository:
    def __init__(self):
        self.saved_records = []

    def save(self, request, response):
        self.saved_records.append((request, response))
```

Unit test:

```python
def test_rag_service_returns_grounded_answer():
    audit_repository = FakeAuditRepository()

    service = RagService(
        query_validator=QueryValidator(),
        retriever=FakeRetriever(),
        reranker=PassThroughReranker(),
        prompt_builder=GroundedPromptBuilder(),
        llm_client=FakeLLM(),
        audit_repository=audit_repository,
    )

    response = service.answer(
        RagRequest(
            question="How many paid leave days do employees receive?",
            user_id="user-1",
        )
    )

    assert "20" in response.answer
    assert response.citations[0].document_id == "policy-123"
    assert len(audit_repository.saved_records) == 1
```

No real LLM, vector database, or SQL database is needed for this test.

---

# 19. Best Practices

## 19.1 Keep Framework Code at the Edges

Avoid passing these objects deep into business logic:

* FastAPI `Request`
* Provider SDK response objects
* Database sessions
* Framework-specific agent state
* Raw Redis clients

Convert them into application-level objects at the boundary.

---

## 19.2 Define Stable Internal Data Models

Normalize external responses into internal objects:

```text
GenerationResult
EmbeddingResult
RetrievedChunk
RerankResult
ToolResult
AgentAction
```

This protects the application from provider API changes.

---

## 19.3 Separate Workflow Logic from Component Logic

The service should coordinate:

```text
retrieve -> rerank -> build prompt -> generate
```

The retriever should implement retrieval—not orchestration.

The prompt builder should build prompts—not call the LLM.

---

## 19.4 Make Provider Boundaries Explicit

Wrap:

* LLM providers
* Vector databases
* Reranking services
* Search systems
* External enterprise APIs

This gives you one place to handle:

* Authentication
* Timeouts
* Rate limits
* Provider errors
* Response normalization
* Observability

---

## 19.5 Use Application-Level Exceptions

Do not leak provider exceptions everywhere.

```python
class ModelTimeoutError(Exception):
    pass


class ModelRateLimitError(Exception):
    pass


class RetrievalUnavailableError(Exception):
    pass
```

The adapter converts SDK exceptions:

```python
try:
    response = provider_client.generate(...)
except ProviderTimeoutException as exc:
    raise ModelTimeoutError("Model request timed out") from exc
```

The service handles application-level exceptions without knowing the provider.

---

## 19.6 Treat Configuration as Data

Model selection and retrieval parameters should be configurable.

```yaml
llm:
  provider: openai
  model: production-chat-model
  timeout_seconds: 30

retrieval:
  strategy: hybrid
  candidate_top_k: 20
  final_top_k: 5

reranker:
  enabled: true
  model: cross-encoder-model
```

Validate configuration at startup rather than discovering errors during requests.

---

## 19.7 Design for Observability

Important GenAI metadata includes:

* Request ID
* User or tenant ID
* Model name
* Prompt version
* Retrieval strategy
* Retrieved document IDs
* Retrieval latency
* Model latency
* Input and output tokens
* Estimated cost
* Tool calls
* Retry count
* Guardrail decisions
* Final status

Do not log sensitive prompts or retrieved documents without security review.

---

## 19.8 Keep Authorization Separate from Retrieval

Filtering documents only after retrieval may expose sensitive information internally.

Prefer authorization-aware retrieval:

```text
Query
  |
  +-- tenant_id
  +-- user permissions
  +-- document access filters
  |
  v
Vector search with metadata filters
```

Access control should be enforced before documents enter the LLM context.

---

## 19.9 Prefer Composition Over Deep Inheritance

Prefer:

```python
rag_service = RagService(
    retriever=HybridRetriever(...),
    reranker=CrossEncoderReranker(...),
)
```

Avoid complex inheritance trees such as:

```text
BaseRetriever
  -> CloudRetriever
     -> HybridCloudRetriever
        -> AuthenticatedHybridCloudRetriever
           -> CachedAuthenticatedHybridCloudRetriever
```

Composition is usually easier to change and test.

---

# 20. Trade-offs

## 20.1 Abstraction vs Simplicity

More interfaces improve flexibility but increase code volume.

For a small proof of concept:

```text
One provider
One vector database
One workflow
Two developers
```

A simple design may be enough.

For a production platform:

```text
Multiple providers
Multiple tenants
Strict reliability requirements
Many integrations
Independent teams
```

Adapters and interfaces become valuable.

Do not build a multi-provider abstraction before there is a realistic need.

---

## 20.2 Generic Interfaces vs Provider Features

A universal `LLMClient` interface simplifies portability but may hide:

* Native tool use
* Structured output capabilities
* Prompt caching
* Multimodal features
* Provider-specific safety controls

A balanced approach:

```text
Base ChatModel interface
        +
Optional capability interfaces
```

For example:

```python
class StructuredOutputModel(Protocol):
    def generate_structured(self, messages, schema):
        ...


class ToolCallingModel(Protocol):
    def generate_with_tools(self, messages, tools):
        ...
```

---

## 20.3 Facade Convenience vs Hidden Complexity

A simple `RagService.answer()` API is useful, but excessive hiding may make debugging harder.

Return useful metadata where appropriate:

```python
@dataclass
class RagResponse:
    answer: str
    citations: list[Citation]
    model_name: str
    retrieval_strategy: str
    trace_id: str
```

Do not expose sensitive internal chain-of-thought or raw credentials.

---

## 20.4 Decorators vs Operational Clarity

Multiple decorators are composable, but deeply nested wrappers can make execution order confusing.

Document the order clearly:

```text
Metrics
  -> Cache
      -> Retry
          -> Rate limiter
              -> Provider adapter
```

For complex cross-cutting behavior, middleware or an explicit execution pipeline may be clearer.

---

# 21. Common Mistakes

## Mistake 1: Putting Everything in the API Route

```python
@router.post("/ask")
def ask(request):
    # Embed query
    # Query vector DB
    # Rerank documents
    # Build prompt
    # Call LLM
    # Save SQL record
    # Update metrics
```

### Problem

* Hard to test
* Hard to reuse
* Framework tightly coupled to application logic

### Better

Call a service or use-case object.

---

## Mistake 2: Creating Unnecessary Interfaces

Do not create an interface for every five-line helper.

An abstraction is useful when:

* Multiple implementations exist
* An external system needs isolation
* Testing requires substitution
* The component changes independently

---

## Mistake 3: Leaking Provider Types

Bad:

```python
def answer() -> OpenAIChatCompletionResponse:
    ...
```

Better:

```python
def answer() -> GenerationResult:
    ...
```

Provider-specific types should remain inside adapters.

---

## Mistake 4: Giant Factory Classes

A factory that creates every object in the application becomes difficult to maintain.

Separate factories by concern:

```text
LLMFactory
RetrieverFactory
VectorStoreFactory
ToolFactory
```

Or use dependency injection at the composition root.

---

## Mistake 5: One Universal Provider Interface

Trying to force chat, embeddings, reranking, speech, and image generation into one interface violates interface segregation.

Use smaller capability-based interfaces.

---

## Mistake 6: Retrying Every Failure

Retry only transient failures:

* Timeouts
* Temporary network errors
* Rate limits
* Service-unavailable errors

Do not blindly retry:

* Invalid API keys
* Invalid request schemas
* Policy violations
* Context-length errors without changing the request
* Permission failures

Retries also require:

* Exponential backoff
* Jitter
* Maximum attempts
* Time budgets
* Idempotency awareness

---

## Mistake 7: Caching Without Considering Security

A cache key based only on the question can leak answers between users.

The cache key may need:

```text
tenant_id
user permission scope
prompt version
model name
retrieval index version
question
generation parameters
```

---

## Mistake 8: Mixing Offline and Online Workflows

Document parsing and embedding generation are usually offline or background operations.

```text
Online path:
User question -> retrieve -> generate -> respond

Offline path:
Document upload -> parse -> chunk -> embed -> index
```

Do not perform full ingestion inside a user-facing question request.

---

## Mistake 9: Overengineering the Prototype

Patterns should solve actual design problems.

A small experiment does not always need:

* Ten interfaces
* Three factories
* A dependency injection framework
* Twelve architecture layers

Start with clear modules, then introduce abstractions at unstable boundaries.

---

# 22. Pattern Recognition Guide

Use this quick guide during interviews.

| Problem                                                  | Useful pattern        |
| -------------------------------------------------------- | --------------------- |
| Choose OpenAI, watsonx, or another provider              | Factory               |
| Switch dense, sparse, and hybrid retrieval               | Strategy              |
| Normalize different provider SDKs                        | Adapter               |
| Add retries, caching, logging, or metrics                | Decorator             |
| Expose one simple API over a complex RAG pipeline        | Facade                |
| Keep API, business workflow, and infrastructure separate | Layered architecture  |
| Make services depend on interfaces                       | Dependency inversion  |
| Give each component one purpose                          | Single responsibility |

---

# 23. End-to-End Example

A request arrives:

```text
“Can an employee carry unused leave into the next year?”
```

The architecture processes it as follows:

```text
1. API layer validates the HTTP request.
2. Authentication middleware identifies the user.
3. RagService receives an application-level request.
4. Authorization filters determine accessible policies.
5. Retrieval Strategy chooses hybrid retrieval.
6. Vector Store Adapter queries the configured database.
7. Reranker Strategy selects the strongest chunks.
8. PromptBuilder creates a grounded prompt.
9. Decorated LLM client:
   - checks the cache,
   - applies rate limits,
   - retries temporary failures,
   - records metrics.
10. LLM Adapter calls the selected provider.
11. Adapter normalizes the provider response.
12. RagService builds citations and saves an audit record.
13. API layer returns a stable JSON response.
```

The API response might be:

```json
{
  "answer": "Employees may carry forward up to five unused leave days, subject to manager approval.",
  "citations": [
    {
      "document_id": "leave-policy-2026",
      "section": "4.2"
    }
  ],
  "trace_id": "trace-abc123"
}
```

---

# 24. Interview Q&A

## Q1. Why are design patterns useful in GenAI systems?

They provide proven ways to manage changing providers, retrieval methods, tools, and infrastructure. Patterns reduce coupling and improve maintainability, testing, and extensibility.

---

## Q2. How would you support multiple LLM providers?

I would define a provider-independent `ChatModel` or `LLMClient` interface, implement an adapter for each provider, and use dependency injection or a factory to select the implementation from configuration.

---

## Q3. What is the difference between Factory and Strategy?

A Factory creates an object. A Strategy performs an operation using an interchangeable algorithm.

For example:

* `RetrieverFactory` creates a hybrid retriever.
* `HybridRetrievalStrategy` performs hybrid retrieval.

---

## Q4. Where would you use the Adapter pattern in a RAG application?

I would use adapters around LLM providers, embedding providers, vector databases, reranking APIs, and enterprise tools. The adapters translate provider-specific requests, responses, and exceptions into application-level models.

---

## Q5. How is a Facade different from a service containing all logic?

A facade provides a simple interface and coordinates specialized components. It should delegate retrieval, reranking, prompting, and persistence rather than implementing all their internal logic itself.

---

## Q6. How does dependency inversion improve testability?

The service depends on interfaces instead of concrete SDKs or databases. Unit tests can inject fake retrievers, fake LLMs, and in-memory repositories without external network calls.

---

## Q7. How would you add retries without modifying every provider adapter?

I could wrap the provider adapter with a retry decorator. The decorator implements the same interface, catches transient application-level errors, and retries using exponential backoff and a maximum attempt limit.

---

## Q8. What belongs in the API layer versus the service layer?

The API layer handles HTTP concerns such as request parsing, authentication integration, status codes, and serialization. The service layer coordinates business workflows such as retrieval, reranking, generation, auditing, and agent execution.

---

## Q9. What are the risks of over-abstraction?

Too many interfaces and layers increase cognitive load, boilerplate, debugging difficulty, and development time. I introduce abstractions mainly around unstable boundaries, external systems, and components with multiple implementations.

---

## Q10. How would you structure an agent system safely?

I would separate the agent orchestrator, planner, state repository, tool registry, tool adapters, and policy engine. Tools would use strict schemas and permissions, state would be checkpointed, destructive actions would require approval, and the agent would have execution limits.

---

# 25. Interview-Ready Two-Minute Answer

A production GenAI system should separate orchestration from infrastructure. The API layer handles HTTP requests and authentication, while the service layer coordinates use cases such as RAG answering or agent execution. Domain interfaces define capabilities such as retrieval, generation, reranking, and persistence, and infrastructure adapters implement those interfaces for specific providers.

I use the Factory pattern to create configured providers, the Strategy pattern to switch retrieval or reranking algorithms, the Adapter pattern to normalize LLM and vector database APIs, the Decorator pattern for retries, caching, logging, and metrics, and a Facade such as `RagService` to expose a simple interface over the full pipeline.

I also follow SOLID principles pragmatically. Components have focused responsibilities, services depend on abstractions, and provider-specific types remain at infrastructure boundaries. This improves testability, limits vendor lock-in, and makes it easier to replace models, databases, and retrieval approaches without rewriting the application. At the same time, I avoid overengineering by adding abstractions only where the system has meaningful variability or operational complexity.

---

# 26. Day 8 Revision Checklist

Make sure you can explain:

* [ ] Why clean architecture matters in a GenAI system
* [ ] All five SOLID principles at a high level
* [ ] Factory for provider creation
* [ ] Strategy for retrieval and reranking
* [ ] Adapter for LLMs and vector databases
* [ ] Decorator for retries, caching, logging, and metrics
* [ ] Facade for a simple `RagService` API
* [ ] API, service, domain, and infrastructure responsibilities
* [ ] Dependency injection and dependency inversion
* [ ] How clean architecture improves unit testing
* [ ] How the same patterns apply to agent tools and planners
* [ ] Why overengineering and excessive abstraction are also risks
