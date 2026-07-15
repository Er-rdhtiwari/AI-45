# Day 4 – Async & Concurrency in Python for GenAI Systems

## 1. Five-line revision summary

* **Synchronous code** waits for one operation to finish before starting the next.
* **Asynchronous code** allows other work to progress while one task waits for network, database, or file I/O.
* Use **async I/O** for LLM APIs, vector databases, HTTP tools, object storage, and async database drivers.
* Use **threads** for blocking I/O libraries that do not support async; use **processes** for CPU-heavy Python work.
* Production concurrency requires limits, timeouts, cancellation handling, backpressure, thread-safe design, logging, and metrics.

---

# 2. What concurrency means

**Concurrency** means handling multiple pieces of work during overlapping periods.

**Parallelism** means multiple pieces of work are literally executing at the same instant, usually on different CPU cores, processes, machines, or accelerators.

These are related but different:

```text
Concurrency:
Task A runs
Task A waits for API
Task B runs
Task B waits for DB
Task C runs

Parallelism:
CPU Core 1 executes Task A
CPU Core 2 executes Task B
at the same time
```

A typical `asyncio` event loop uses **cooperative scheduling**. It runs one task until that task reaches an `await` and gives control back to the event loop. The event loop can then run another task while the first task waits. ([Python documentation][1])

## GenAI example

A RAG request might require:

1. Query rewriting with an LLM
2. Vector database search
3. Keyword search
4. User-permission lookup
5. Reranking
6. Final LLM generation

Some steps depend on previous results, but others are independent:

```text
                       ┌─ Vector search ──────┐
User query → Rewrite ──┼─ Keyword search ─────┼→ Merge → Rerank → LLM
                       └─ Permission lookup ──┘
```

The three middle operations can run concurrently.

---

# 3. Synchronous versus asynchronous I/O

## 3.1 Synchronous execution

In synchronous code, every operation blocks the current execution flow until it finishes.

```python
def build_answer(query: str) -> str:
    # This call may wait two seconds for a remote LLM.
    rewritten_query = rewrite_query(query)

    # This call starts only after rewrite_query finishes.
    documents = search_vector_database(rewritten_query)

    # This call starts only after vector search finishes.
    return generate_answer(query, documents)
```

This is easy to understand, but it can waste resources when the application spends most of its time waiting for remote services.

## 3.2 Asynchronous execution

An asynchronous function can suspend itself while waiting:

```python
async def build_answer(query: str) -> str:
    # While the remote LLM is processing this request,
    # the event loop may handle another user request.
    rewritten_query = await rewrite_query(query)

    documents = await search_vector_database(rewritten_query)

    return await generate_answer(query, documents)
```

The event loop is the central scheduler for an `asyncio` application. It runs tasks and callbacks and handles network I/O and subprocesses. Application code normally starts it through a high-level function such as `asyncio.run()`. ([Python documentation][2])

## Important distinction

Async does **not** automatically make one remote LLM call faster.

It helps when:

* Many users call your API concurrently.
* One request requires several independent network calls.
* The application waits heavily on LLM APIs, databases, tools, storage, or search systems.
* You want to stream tokens while monitoring cancellation or client disconnects.
* Your server must remain responsive while remote services are slow.

It helps less when:

* The work is CPU-heavy Python computation.
* The model is running locally and saturating the GPU.
* Operations are strictly dependent and must run one after another.
* The underlying SDK is synchronous and blocks the event loop.
* You have only one small script processing one request at a time.

---

# 4. Understanding `async`, `await`, coroutines, and tasks

## 4.1 Coroutine function

A function declared using `async def` is a coroutine function.

```python
async def retrieve_documents(query: str) -> list[str]:
    return ["document-1", "document-2"]
```

## 4.2 Coroutine object

Calling an async function does not immediately execute the entire function.

```python
coroutine = retrieve_documents("refund policy")
```

`coroutine` represents work that can be awaited or scheduled.

## 4.3 Awaiting a coroutine

```python
documents = await retrieve_documents("refund policy")
```

`await` means:

> Suspend this coroutine until the operation finishes, allowing the event loop to run other ready tasks.

`await` may only be used inside an async function, except in environments that provide special top-level async support.

## 4.4 Task

A task schedules a coroutine to run concurrently:

```python
task = asyncio.create_task(
    retrieve_documents("refund policy"),
    name="refund-policy-retrieval",
)

documents = await task
```

Tasks are the event loop’s scheduled units of coroutine execution. `asyncio.create_task()` schedules a coroutine to run soon, while retaining a task handle that can be awaited, cancelled, named, or inspected. ([Python documentation][3])

---

# 5. Event loop mental model

Consider three network operations:

```text
Time ───────────────────────────────────────────────────────→

LLM task:     RUN ── await HTTP ─────────────────── RUN
DB task:            RUN ── await database ───── RUN
Tool task:                RUN ── await HTTP ────────── RUN

Event loop:   LLM → DB → Tool → DB → LLM → Tool
```

The event loop does not continuously execute all tasks simultaneously on one thread. Instead:

1. It runs a ready task.
2. The task reaches `await`.
3. The task is suspended.
4. Another ready task runs.
5. The original task resumes when its I/O result becomes available.

## Cooperative scheduling

A task must cooperate by reaching an `await`.

This function is declared async but still blocks:

```python
import time


async def bad_function() -> None:
    # BAD: time.sleep blocks the event-loop thread.
    # Other requests cannot progress during these five seconds.
    time.sleep(5)
```

This function cooperates correctly:

```python
import asyncio


async def good_function() -> None:
    # GOOD: this suspends the current task.
    # Other tasks may run during these five seconds.
    await asyncio.sleep(5)
```

While a task runs ordinary Python code, another task on that same event-loop thread cannot run. The current task must reach an `await` or complete. ([Python documentation][1])

---

# 6. Sequential awaits versus concurrent awaits

## Sequential version

```python
async def sequential_search(query: str) -> tuple[list[str], list[str]]:
    # First wait for vector search.
    vector_results = await vector_search(query)

    # Only after vector search finishes, begin keyword search.
    keyword_results = await keyword_search(query)

    return vector_results, keyword_results
```

Suppose each search takes one second. Total time is approximately two seconds.

## Concurrent version

```python
async def concurrent_search(query: str) -> tuple[list[str], list[str]]:
    # Both coroutine calls are supplied to gather.
    # They can make progress during overlapping periods.
    vector_results, keyword_results = await asyncio.gather(
        vector_search(query),
        keyword_search(query),
    )

    return vector_results, keyword_results
```

Total time is approximately the duration of the slower operation, plus scheduling and application overhead.

---

# 7. `asyncio.gather`

`asyncio.gather()` runs multiple awaitables concurrently and returns their results as a list in the **same order as the supplied awaitables**, not completion order. By default, the first exception is propagated to the caller, but other submitted awaitables are not automatically cancelled merely because one failed. ([Python documentation][3])

```python
results = await asyncio.gather(
    call_first_model(),
    call_second_model(),
    call_third_model(),
)
```

## `return_exceptions=True`

```python
results = await asyncio.gather(
    call_first_model(),
    call_second_model(),
    call_third_model(),
    return_exceptions=True,
)
```

With this option, exceptions are included in the result list. They must be inspected explicitly.

This can be useful for an optional multi-provider comparison where one failure should not destroy every successful result.

It can be dangerous when developers forget to check for exceptions.

---

# 8. Real-world example 1: Concurrent LLM calls

Imagine an evaluation service that asks three models to answer the same prompt.

```python
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelAnswer:
    provider: str
    text: str


async def call_llm(provider: str, prompt: str) -> ModelAnswer:
    """
    Simulated async LLM call.

    In a real service, this function would use an async HTTP or provider
    client. The important point is that the remote wait must be awaitable.
    """

    # Simulate waiting for a remote inference API.
    # asyncio.sleep yields control instead of blocking the event loop.
    await asyncio.sleep(0.5)

    return ModelAnswer(
        provider=provider,
        text=f"Answer from {provider} for: {prompt}",
    )


async def compare_models(prompt: str) -> list[ModelAnswer]:
    """
    Call several independent models concurrently.

    Edge-case policy:
    - One provider failure should not discard successful provider responses.
    - Every result must therefore be checked for exceptions.
    """

    providers = ["provider-a", "provider-b", "provider-c"]

    # create_task schedules each model call immediately.
    # Naming tasks makes logs and debugging output easier to understand.
    tasks = [
        asyncio.create_task(
            call_llm(provider, prompt),
            name=f"llm-call-{provider}",
        )
        for provider in providers
    ]

    # return_exceptions=True supports partial success.
    raw_results = await asyncio.gather(
        *tasks,
        return_exceptions=True,
    )

    successful_answers: list[ModelAnswer] = []

    for provider, result in zip(providers, raw_results):
        if isinstance(result, Exception):
            # Production code should log:
            # - provider
            # - exception type
            # - request or trace ID
            # - latency
            # - retry attempt
            print(f"{provider} failed: {result!r}")
            continue

        successful_answers.append(result)

    # Business decision:
    # If every provider failed, returning an empty list may hide the problem.
    # Raise a service-level error instead.
    if not successful_answers:
        raise RuntimeError("All LLM providers failed")

    return successful_answers


async def main() -> None:
    answers = await compare_models("Explain embeddings simply.")

    for answer in answers:
        print(answer.provider, answer.text)


if __name__ == "__main__":
    asyncio.run(main())
```

## Production improvements

The example needs additional controls before production use:

* Per-call timeout
* Overall request deadline
* Retry policy for transient failures
* Provider rate-limit handling
* Maximum concurrency
* Circuit breaker or provider-health logic
* Request cancellation propagation
* Token and cost accounting
* Structured logging and tracing

---

# 9. Limiting concurrency with a semaphore

Launching 10,000 LLM requests simultaneously can exhaust:

* Provider rate limits
* HTTP connections
* Memory
* Database connections
* File descriptors
* Internal queues
* Your budget

An `asyncio.Semaphore` maintains a counter and suspends tasks when no permits remain. It is useful for limiting concurrent access to a remote provider or constrained resource. ([Python documentation][4])

```python
import asyncio


# At most five tasks may enter the protected section simultaneously.
llm_limit = asyncio.Semaphore(5)


async def bounded_llm_call(prompt: str) -> str:
    # A task waits here when five other calls are already active.
    async with llm_limit:
        # Always use a timeout around remote calls.
        try:
            async with asyncio.timeout(15):
                return await send_prompt_to_provider(prompt)

        except TimeoutError as exc:
            # Convert low-level timeout information into an application error.
            raise RuntimeError("LLM provider timed out") from exc
```

`asyncio.timeout()` limits the time spent in its block. When the deadline is exceeded, it cancels the current task internally and exposes a `TimeoutError` outside the timeout context. ([Python documentation][3])

## Senior-level insight

A semaphore is a **concurrency limit**, not necessarily a complete rate limiter.

For example:

* Semaphore: at most 10 active requests.
* Rate limiter: at most 100 requests per minute.

A production service may need both.

---

# 10. `asyncio.create_task` and task lifecycle

Use `create_task()` when:

* Work should start before you await its result.
* You need a handle for cancellation or inspection.
* You are coordinating several activities.
* You want to name tasks for debugging.

```python
async def answer_request(query: str) -> str:
    # Start independent operations immediately.
    permission_task = asyncio.create_task(
        load_user_permissions(),
        name="permission-check",
    )

    retrieval_task = asyncio.create_task(
        retrieve_documents(query),
        name="document-retrieval",
    )

    # Perform other lightweight synchronous preparation here.
    normalized_query = query.strip()

    # Await both results before continuing.
    permissions, documents = await asyncio.gather(
        permission_task,
        retrieval_task,
    )

    allowed_documents = filter_documents(documents, permissions)
    return await generate_answer(normalized_query, allowed_documents)
```

## Avoid careless fire-and-forget

```python
asyncio.create_task(store_audit_event(event))
```

This is risky when the task reference is discarded:

* The task may fail without proper error handling.
* The process may terminate before it finishes.
* A deployment may interrupt it.
* The application may have no way to cancel or monitor it.
* The event loop keeps only weak references in some task-related situations, so explicit references are important for reliable task management. ([Python documentation][3])

Maintain a task collection or use structured concurrency.

---

# 11. `TaskGroup`: safer structured concurrency

Although `asyncio.gather()` is important and commonly used, modern Python also provides `asyncio.TaskGroup`.

```python
async def collect_context(query: str) -> tuple[list[str], list[str]]:
    async with asyncio.TaskGroup() as group:
        vector_task = group.create_task(
            vector_search(query),
            name="vector-search",
        )

        keyword_task = group.create_task(
            keyword_search(query),
            name="keyword-search",
        )

    # Exiting the async-with block waits for all tasks.
    return vector_task.result(), keyword_task.result()
```

A `TaskGroup` waits for all tasks when its context exits. When one child task fails with a non-cancellation exception, the remaining tasks are cancelled and the errors are collected according to structured-concurrency rules. This generally provides stronger failure safety than `gather()` for groups of related subtasks. ([Python documentation][5])

### Practical choice

Use `gather()` when:

* You want a straightforward list of independent results.
* Partial success is meaningful.
* You will explicitly inspect exceptions.

Consider `TaskGroup` when:

* The tasks form one logical operation.
* A failure means sibling tasks should stop.
* Predictable cleanup and cancellation are important.

---

# 12. Real-world example 2: Concurrent hybrid retrieval

A production RAG system may combine:

* Vector search
* Keyword search
* Metadata database lookup
* Access-control lookup

```python
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchContext:
    vector_documents: list[str]
    keyword_documents: list[str]
    allowed_document_ids: set[str]


async def vector_search(query: str) -> list[str]:
    # Represents an async call to a vector database.
    await asyncio.sleep(0.4)
    return ["doc-101", "doc-202"]


async def keyword_search(query: str) -> list[str]:
    # Represents an async call to a search engine.
    await asyncio.sleep(0.3)
    return ["doc-202", "doc-303"]


async def load_allowed_document_ids(user_id: str) -> set[str]:
    # Represents an async relational-database query.
    await asyncio.sleep(0.2)
    return {"doc-101", "doc-303"}


async def retrieve_context(query: str, user_id: str) -> SearchContext:
    """
    Run independent I/O concurrently.

    These operations do not depend on one another, so running them
    sequentially would add their waiting times together unnecessarily.
    """

    try:
        # The entire retrieval stage has a deadline.
        # This prevents retrieval from consuming the complete API timeout.
        async with asyncio.timeout(2):
            vector_docs, keyword_docs, allowed_ids = await asyncio.gather(
                vector_search(query),
                keyword_search(query),
                load_allowed_document_ids(user_id),
            )

    except TimeoutError as exc:
        raise RuntimeError("Retrieval stage exceeded its deadline") from exc

    return SearchContext(
        vector_documents=vector_docs,
        keyword_documents=keyword_docs,
        allowed_document_ids=allowed_ids,
    )


def merge_and_filter(context: SearchContext) -> list[str]:
    """
    Merge results after all asynchronous I/O has completed.

    A set removes duplicate document IDs.
    Authorization filtering happens before documents reach the LLM.
    """

    merged = set(context.vector_documents) | set(context.keyword_documents)

    return [
        document_id
        for document_id in merged
        if document_id in context.allowed_document_ids
    ]
```

## Important architecture principle

Do not run operations concurrently merely because you can.

These operations are dependent:

```text
Generate search query
        ↓
Retrieve documents
        ↓
Rerank documents
        ↓
Generate answer
```

Reranking cannot start before retrieval returns candidates.

Concurrency should follow the dependency graph.

---

# 13. Threads versus processes versus async I/O

| Model            | Best fit                        | Memory model                              | Main advantage                              | Main risk                                           |
| ---------------- | ------------------------------- | ----------------------------------------- | ------------------------------------------- | --------------------------------------------------- |
| Async I/O        | Many waiting network operations | Usually one process and event-loop thread | High I/O concurrency with low task overhead | One blocking call can stall the loop                |
| Threads          | Blocking I/O libraries or SDKs  | Shared process memory                     | Easy integration with synchronous code      | Race conditions, deadlocks, shared-state complexity |
| Processes        | CPU-heavy Python work           | Separate memory per process               | Multi-core CPU parallelism                  | Serialization and startup overhead                  |
| External workers | Durable or long-running jobs    | Separate services/processes               | Reliability, retry, scaling and isolation   | Operational complexity                              |

---

# 14. Threads

Threads share the same process memory.

They are commonly useful for:

* Synchronous HTTP clients
* Legacy database drivers
* Blocking file operations
* SDKs without async support
* Several I/O-bound operations

`ThreadPoolExecutor` provides a pool of threads and returns `Future` objects for submitted operations. The official documentation also warns that futures waiting on each other can create deadlocks. ([Python documentation][6])

## Bridging blocking code with `asyncio.to_thread`

```python
import asyncio
import time


def blocking_legacy_llm_call(prompt: str) -> str:
    """
    A synchronous SDK call that blocks its calling thread.

    Imagine this belongs to a legacy provider SDK that has no async client.
    """
    time.sleep(2)
    return f"Legacy answer for: {prompt}"


async def call_legacy_provider(prompt: str) -> str:
    """
    Move the blocking call to a worker thread.

    The event-loop thread remains free to serve other asynchronous tasks.
    """

    return await asyncio.to_thread(
        blocking_legacy_llm_call,
        prompt,
    )
```

`asyncio.to_thread()` runs a function in a separate thread and returns an awaitable result. It is primarily useful for blocking I/O that would otherwise block the event loop. ([Python documentation][3])

## Thread limitation

Moving blocking code to threads does not make it magically unlimited.

You still need:

* Bounded thread pools
* Timeouts
* Thread-safe clients
* Connection limits
* Protection for shared mutable state
* Graceful shutdown

---

# 15. Processes

Processes use separate Python interpreters and separate memory spaces.

They are useful for CPU-heavy work such as:

* Complex document parsing
* CPU-based image transformations
* Heavy custom tokenization
* Large pure-Python scoring operations
* Feature computation
* CPU-intensive data cleaning

`ProcessPoolExecutor` uses separate processes and can bypass the traditional Global Interpreter Lock limitation for Python execution. Its functions, arguments, and results generally need to be picklable, and worker processes need to import the main module correctly. ([Python documentation][6])

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor


def cpu_heavy_document_score(text: str) -> int:
    """
    Simplified CPU-heavy function.

    This must be declared at module level so process workers can import it.
    Real examples could perform complex parsing or scoring.
    """

    score = 0

    # Artificial CPU work.
    for character in text:
        score += ord(character) ** 2

    return score


async def score_documents(
    documents: list[str],
    process_pool: ProcessPoolExecutor,
) -> list[int]:
    """
    Submit CPU-heavy work to a reusable process pool.

    Do not create a fresh process pool for every API request.
    A service should normally create it during application startup and
    shut it down during application termination.
    """

    loop = asyncio.get_running_loop()

    futures = [
        loop.run_in_executor(
            process_pool,
            cpu_heavy_document_score,
            document,
        )
        for document in documents
    ]

    return await asyncio.gather(*futures)
```

## Process-pool costs

Processes introduce:

* Process startup cost
* Data serialization
* Interprocess communication
* Higher memory consumption
* More complicated deployment and shutdown

Do not use a process pool for simple remote HTTP calls.

---

# 16. `concurrent.futures` basics

The module provides a common abstraction for thread and process pools.

Important concepts:

* `Executor`: manages workers.
* `submit()`: schedules one callable.
* `Future`: represents a result that may become available later.
* `result()`: retrieves the result or raises its exception.
* `map()`: applies a callable across inputs.
* `as_completed()`: processes futures in completion order.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed


def blocking_tool_call(tool_name: str) -> str:
    # Placeholder for a synchronous external tool call.
    return f"{tool_name} completed"


tools = ["weather", "inventory", "pricing"]

# The context manager shuts down the pool when work is complete.
with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_tool = {
        executor.submit(blocking_tool_call, tool): tool
        for tool in tools
    }

    # as_completed yields each future as soon as it finishes.
    for future in as_completed(future_to_tool):
        tool = future_to_tool[future]

        try:
            result = future.result()
        except Exception as exc:
            print(f"{tool} failed: {exc!r}")
        else:
            print(result)
```

Thread-pool deadlocks can occur when a worker waits for another future from the same exhausted pool. Process-pool tasks must also avoid calling pool methods from within submitted worker functions. ([Python documentation][6])

---

# 17. Real-world example 3: Background workers

A GenAI system may perform work that should not delay the immediate API response:

* Document ingestion
* Embedding generation
* Evaluation runs
* Conversation summarization
* Audit-event processing
* Batch report generation

## In-process async queue example

```python
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingJob:
    document_id: str
    text: str


async def generate_embedding(job: EmbeddingJob) -> None:
    """
    Simulate calling a remote embedding service and storing the result.
    """
    await asyncio.sleep(0.25)
    print(f"Embedded {job.document_id}")


async def embedding_worker(
    worker_name: str,
    queue: asyncio.Queue[EmbeddingJob | None],
) -> None:
    """
    Continuously consume jobs from the queue.

    None is used as a shutdown signal.
    """

    while True:
        job = await queue.get()

        try:
            if job is None:
                # The worker received a graceful-shutdown signal.
                return

            try:
                async with asyncio.timeout(10):
                    await generate_embedding(job)

            except TimeoutError:
                # Real production code might:
                # - retry a limited number of times
                # - move the job to a failure queue
                # - record the failure in persistent storage
                print(f"{worker_name}: job timed out: {job.document_id}")

            except Exception as exc:
                # A worker should not normally die because one job failed.
                print(
                    f"{worker_name}: job failed: "
                    f"{job.document_id}: {exc!r}"
                )

        finally:
            # task_done must correspond to every successful queue.get(),
            # including shutdown signals and failed jobs.
            queue.task_done()


async def main() -> None:
    # maxsize provides backpressure.
    # Producers must wait when the queue already contains 100 jobs.
    queue: asyncio.Queue[EmbeddingJob | None] = asyncio.Queue(maxsize=100)

    workers = [
        asyncio.create_task(
            embedding_worker(f"worker-{index}", queue),
            name=f"embedding-worker-{index}",
        )
        for index in range(3)
    ]

    for index in range(10):
        await queue.put(
            EmbeddingJob(
                document_id=f"doc-{index}",
                text=f"Document text {index}",
            )
        )

    # Wait until every currently queued job has called task_done().
    await queue.join()

    # Send one shutdown signal per worker.
    for _ in workers:
        await queue.put(None)

    # Wait until shutdown signals have been consumed.
    await queue.join()

    await asyncio.gather(*workers)


if __name__ == "__main__":
    asyncio.run(main())
```

An `asyncio.Queue` supports producer-consumer workflows. A bounded queue pauses producers when it reaches its maximum size, creating backpressure. `queue.join()` waits until each enqueued item has been matched by `task_done()`. ([Python documentation][7])

## Production warning

An in-memory queue is not durable.

Jobs may disappear when:

* The process crashes.
* The container restarts.
* A deployment replaces the service.
* The machine becomes unavailable.

Use an external durable queue and separate workers when the job must survive process failure or deployment.

---

# 18. Race conditions and shared state

Async code can have race conditions even when it uses only one event-loop thread.

## Unsafe example

```python
import asyncio


counter = 0


async def unsafe_increment() -> None:
    global counter

    # Read the current value.
    current_value = counter

    # Simulate an asynchronous boundary.
    # Another task may modify counter before this task resumes.
    await asyncio.sleep(0)

    # Several tasks may write the same calculated value.
    counter = current_value + 1
```

Suppose 100 tasks read `counter == 0` before any writes. They may all later write `1`.

## Protecting shared state with `asyncio.Lock`

```python
import asyncio


counter = 0
counter_lock = asyncio.Lock()


async def safe_increment() -> None:
    global counter

    # Only one asyncio task at a time may enter this block.
    async with counter_lock:
        counter += 1
```

An `asyncio.Lock` guarantees exclusive access among asyncio tasks using that lock. It is not designed for synchronization between OS threads. ([Python documentation][4])

## Better design

Prefer reducing shared mutable state instead of locking everything.

Possible alternatives:

* Immutable request-scoped objects
* Database atomic updates
* Message passing through queues
* One owner task for each mutable resource
* Idempotent operations
* Distributed locks only when truly necessary

---

# 19. Major pitfalls

## 19.1 Blocking I/O inside async functions

```python
async def bad_handler() -> str:
    # These examples may block the event loop:
    response = synchronous_http_client.get("...")
    time.sleep(2)
    rows = synchronous_database_client.query("...")
    return response.text
```

Fix it by using:

* Async-native client libraries
* `asyncio.to_thread()` for unavoidable blocking I/O
* A separate worker process or service for long-running work

---

## 19.2 Unbounded `gather`

```python
# Dangerous when prompts contains hundreds of thousands of entries.
await asyncio.gather(*(call_llm(prompt) for prompt in prompts))
```

Possible consequences:

* Provider throttling
* Memory exhaustion
* Connection-pool exhaustion
* Huge retry storms
* High cost

Use semaphores, queues, chunked batches, and service-level capacity limits.

---

## 19.3 No timeout

A dependency may remain slow or unresponsive indefinitely.

Every external operation should normally have a deadline:

```python
async with asyncio.timeout(10):
    result = await remote_service_call()
```

Also define an overall request deadline so several individually acceptable operations do not collectively exceed the user-facing latency target.

---

## 19.4 Incorrect exception handling with `gather`

```python
results = await asyncio.gather(
    *tasks,
    return_exceptions=True,
)

# BUG: results may contain exception objects.
return results
```

Inspect every result when partial failure is enabled.

---

## 19.5 Swallowing cancellation

Cancellation is how an async service stops work after:

* Client disconnect
* Timeout
* Application shutdown
* Parent-task failure

```python
async def bad_operation() -> None:
    try:
        await long_operation()
    except BaseException:
        # BAD: this can swallow cancellation.
        pass
```

Cleanup should normally happen in `finally`, and `CancelledError` should generally be allowed to propagate after cleanup. Structured-concurrency components depend on cancellation semantics working correctly. ([Python documentation][5])

```python
async def better_operation() -> None:
    resource = await acquire_resource()

    try:
        await long_operation()
    finally:
        # Runs during normal completion, failure, or cancellation.
        await resource.close()
```

---

## 19.6 Holding a lock during remote I/O

```python
async with shared_lock:
    # BAD: every other task needing the lock waits for a slow network call.
    result = await call_remote_llm()
    shared_cache[key] = result
```

Better:

```python
# Perform slow remote work without holding the lock.
result = await call_remote_llm()

# Hold the lock only for the short shared-state update.
async with shared_lock:
    shared_cache[key] = result
```

Be careful: this may allow duplicate remote calls. The correct solution may require single-flight request deduplication rather than one large lock.

---

## 19.7 Assuming async objects are thread-safe

Most `asyncio` objects are not intended to be manipulated from arbitrary OS threads. Cross-thread interaction should use supported thread-safe mechanisms such as `loop.call_soon_threadsafe()` or `asyncio.run_coroutine_threadsafe()` where appropriate. ([Python documentation][1])

---

## 19.8 Creating process pools per request

Process creation is expensive.

Create shared pools during service startup and shut them down gracefully during application termination.

---

## 19.9 Using background tasks for critical durable work

A task running inside the API process is suitable only when losing it is acceptable or its state is persisted elsewhere.

Payment-like, ingestion, audit, or compliance-critical jobs generally require durable external job storage.

---

## 19.10 Retrying non-idempotent operations

A timed-out request may have succeeded remotely even though your service did not receive the response.

Retrying could create:

* Duplicate database writes
* Duplicate tool actions
* Duplicate messages
* Duplicate workflow transitions

Use idempotency keys and design operations so repeated execution is safe.

---

# 20. Debugging and observability

Async failures are difficult to understand when logs show only:

```text
Request failed
```

## 20.1 Name tasks

```python
task = asyncio.create_task(
    retrieve_documents(query),
    name=f"retrieval-{request_id}",
)
```

Include identifiers such as:

* Request ID
* Trace ID
* User-safe tenant ID
* Task name
* Provider
* Model
* Tool
* Attempt number
* Deadline
* Dependency latency

## 20.2 Enable asyncio debug mode in development

```python
asyncio.run(main(), debug=True)
```

Asyncio debug mode can identify wrong-thread API usage, report slow callbacks, and log unusually slow event-loop operations. It can also be enabled through development settings or environment configuration. ([Python documentation][1])

Do not automatically enable extremely verbose debugging in high-volume production environments without understanding its overhead.

## 20.3 Track useful metrics

For LLM services, monitor:

* Active requests
* Active LLM calls
* Queue depth
* Semaphore wait time
* Thread-pool saturation
* Process-pool saturation
* Event-loop lag
* Provider latency
* Timeout count
* Cancellation count
* Retry count
* Rate-limit responses
* Token usage and cost
* Partial-success rate

## 20.4 Distributed tracing

A RAG request should produce child spans such as:

```text
POST /answer
├── permission_lookup
├── query_rewrite
├── vector_search
├── keyword_search
├── reranking
└── llm_generation
```

Concurrent spans should overlap in the trace. This makes unnecessary sequential execution easy to identify.

---

# 21. Production best practices

## 21.1 Use async end to end

An async API handler only benefits fully when its dependencies are also async:

```text
Async endpoint
  → async HTTP client
  → async database driver
  → async vector client
  → async LLM provider client
```

One blocking SDK can stall the event loop.

## 21.2 Bound every constrained resource

Apply limits to:

* LLM providers
* Vector databases
* Database pools
* HTTP connection pools
* Background queues
* CPU pools
* Per-user operations

## 21.3 Define timeout budgets

Example for a five-second API target:

```text
Total request deadline:       5.0 s
Permission lookup:            0.3 s
Retrieval stage:              1.0 s
Reranking:                    0.7 s
LLM generation:               2.5 s
Serialization and overhead:   0.5 s
```

Timeouts should be derived from the overall user-facing deadline.

## 21.4 Handle cancellation intentionally

When a client disconnects:

* Cancel unnecessary provider calls.
* Release database connections.
* Close streams.
* Avoid storing incomplete assistant responses as successful.
* Preserve genuinely required audit work through a durable mechanism.

## 21.5 Use backpressure

A bounded queue or semaphore communicates:

> The service is at capacity; producers must slow down.

Without backpressure, requests may accumulate until the service crashes.

## 21.6 Avoid shared global mutable state

Global caches, counters, dictionaries, and client objects require careful lifecycle and concurrency design.

Prefer:

* Request-scoped data
* Concurrency-safe clients
* External stores
* Atomic database operations
* Immutable configuration

## 21.7 Separate online and offline workloads

Online path:

```text
User request → Retrieval → LLM → Response
```

Offline path:

```text
Document upload → Durable queue → Parsing → Chunking
                → Embeddings → Indexing → Validation
```

Long ingestion work should not occupy an API request until completion.

## 21.8 Test failure behavior

Test:

* One concurrent task fails.
* One task times out.
* All tasks fail.
* Request is cancelled.
* Queue reaches capacity.
* Worker crashes.
* Provider rate-limits requests.
* A blocking function accidentally enters an async route.
* Shutdown begins while tasks are active.

---

# 22. Choosing the correct model

Use this decision process:

```text
Is the task mostly waiting for network, DB, or storage?
    └── Yes → Use async I/O

Is the library blocking and difficult to replace?
    └── Yes → Use a bounded thread pool or asyncio.to_thread()

Is the work CPU-heavy pure Python?
    └── Yes → Use a process pool or separate compute service

Must the work survive API process failure?
    └── Yes → Use durable external workers/queues

Is the work GPU-heavy inference?
    └── Use model-serving batching and GPU-level scheduling;
       Python async mainly coordinates requests around the inference system
```

---

# 23. Interview Q&A

## 1. What is the difference between concurrency and parallelism?

**Concurrency** means tasks make progress during overlapping periods. **Parallelism** means tasks execute simultaneously on separate compute resources. Async I/O provides concurrency but does not necessarily provide CPU parallelism.

## 2. Why is async useful in an LLM backend?

LLM backends spend significant time waiting for model APIs, vector databases, HTTP tools, databases, and storage. Async allows the event loop to process other requests during those waits.

## 3. Does adding `async` make a function non-blocking?

No. An async function can still block if it calls `time.sleep()`, a synchronous HTTP client, CPU-heavy Python code, or another blocking library without offloading it.

## 4. What happens at an `await`?

The current coroutine may suspend and return control to the event loop. The event loop can run another ready task until the awaited operation completes.

## 5. What is the difference between a coroutine and a task?

A coroutine is an awaitable computation produced by calling an async function. A task schedules a coroutine on the event loop and provides lifecycle operations such as awaiting, cancellation, naming, and result inspection.

## 6. When would you use `asyncio.gather()`?

Use it to run several independent awaitables concurrently and collect their results. Be deliberate about exception behavior, particularly when using `return_exceptions=True`.

## 7. What is the difference between `gather()` and `TaskGroup`?

`gather()` conveniently aggregates results and can support partial success. `TaskGroup` provides structured-concurrency behavior and normally cancels sibling tasks when one related task fails.

## 8. When should you use threads instead of async?

Use threads when integrating blocking I/O libraries that cannot be replaced with async equivalents. Threads may also help with native operations that release the GIL, but shared-state safety must be considered.

## 9. When should you use processes?

Use processes for CPU-heavy Python work that benefits from multiple cores. Account for process startup, serialization, separate memory, pickling restrictions, and deployment complexity.

## 10. Can race conditions happen in single-threaded asyncio code?

Yes. A task can read shared state, reach an `await`, and later write based on stale data after another task has changed it. Use locks, atomic external operations, queues, ownership patterns, or immutable state.

## 11. How do you protect an LLM provider from excessive concurrency?

Use a semaphore or bounded worker queue, along with connection-pool limits, provider-specific rate limiting, retries with backoff, timeout budgets, and load shedding.

## 12. Why are timeouts essential?

Without timeouts, slow dependencies can consume tasks, connections, memory, and request capacity indefinitely. Timeouts also allow the service to fail predictably and preserve its latency objectives.

## 13. Why is `asyncio.create_task()` dangerous for background jobs?

A task may fail unnoticed, be cancelled during shutdown, or disappear when the process restarts. Critical jobs should be persisted and executed through durable workers.

## 14. How would you debug a slow async service?

Check for blocking calls, event-loop lag, connection-pool waits, semaphore waits, queue depth, slow callbacks, dependency latency, thread-pool saturation and incorrectly sequential awaits. Use task names, structured logs, metrics, tracing and asyncio debug mode.

## 15. How would you parallelize vector and keyword retrieval?

Start both operations concurrently because they depend only on the query. Await both, merge their results, deduplicate, apply authorization, and then pass the candidates into reranking.

---

# 24. Final revision checklist

Before calling a GenAI Python service concurrency-safe, verify:

* I/O clients are async or deliberately offloaded.
* Independent operations execute concurrently.
* Dependent operations remain correctly ordered.
* Concurrency is bounded.
* External calls have timeouts.
* Retries are limited and idempotent.
* Cancellation is propagated.
* Shared state is protected or removed.
* Queues provide backpressure.
* Critical jobs are durable.
* Thread and process pools have controlled lifecycles.
* Logs contain request and task context.
* Metrics expose saturation, waits, failures and latency.
* Shutdown waits for or safely cancels active work.

[1]: https://docs.python.org/3/library/asyncio-dev.html?utm_source=chatgpt.com "Developing with asyncio"
[2]: https://docs.python.org/3/library/asyncio-eventloop.html "Event loop — Python 3.14.6 documentation"
[3]: https://docs.python.org/3/library/asyncio-task.html?utm_source=chatgpt.com "Coroutines and tasks"
[4]: https://docs.python.org/3/library/asyncio-sync.html?utm_source=chatgpt.com "Synchronization Primitives"
[5]: https://docs.python.org/3/library/asyncio-task.html "Coroutines and tasks — Python 3.14.6 documentation"
[6]: https://docs.python.org/3/library/concurrent.futures.html "concurrent.futures — Launching parallel tasks — Python 3.14.6 documentation"
[7]: https://docs.python.org/3/library/asyncio-queue.html?utm_source=chatgpt.com "asyncio.Queue"
