# 1. The system-design interview mindset

A strong system-design answer is not about finding the “perfect architecture.” It is about showing that you can:

1. Reduce ambiguity.
2. Make reasonable assumptions.
3. Estimate scale.
4. define clean contracts.
5. Choose an architecture that meets the requirements.
6. Explain trade-offs and failure handling.

Your reusable flow should be:

```text
Requirements
    ↓
Capacity
    ↓
APIs
    ↓
Data model
    ↓
High-level architecture
    ↓
Deep dives, trade-offs, and summary
```

Do not jump directly to Kafka, Kubernetes, microservices, or vector databases. First establish why those components are needed.

---

# A. Six-phase system-design interview framework

## Phase 1: Clarify requirements

Separate requirements into two categories.

### Functional requirements

These describe what users and systems can do.

For an AgentRun platform:

* Start an agent workflow.
* Check run status.
* List previous runs.
* Execute tools.
* Receive tool callbacks.
* Cancel a running workflow.
* Store generated artifacts.
* Record feedback.
* Search audit history.

### Non-functional requirements

These describe how well the system must operate.

* Latency
* Availability
* Durability
* Scalability
* Consistency
* Security
* Tenant isolation
* Compliance
* Observability
* Cost
* Data retention
* Disaster recovery

### Interview habit

Summarize the scope before designing:

> “For the MVP, I will focus on starting asynchronous agent runs, tracking status, executing tools, and maintaining an audit trail. I’ll treat human approval, cross-region failover, and advanced scheduling as phase two.”

That prevents scope explosion.

---

## Phase 2: Capacity estimation

Estimate only what influences architecture.

Typical estimates:

* Daily active users
* Actions per user per day
* Average QPS
* Peak QPS
* Read/write ratio
* Payload size
* Storage growth
* Retention
* Network bandwidth
* Concurrent workflows
* Cache hit rate
* Background processing throughput

The interviewer does not expect exact production numbers. They expect:

* Clear assumptions
* Correct formulas
* Reasonable order of magnitude
* Architectural conclusions

---

## Phase 3: API contracts

Define the system boundary before internal components.

For every important API, discuss:

* Method and path
* Request body
* Response body
* Authentication
* Idempotency
* Pagination
* Error handling
* Sync versus async behavior
* Versioning

For long-running operations such as agent execution or document ingestion, usually return quickly with an operation ID:

```http
202 Accepted
```

Do not hold an HTTP request open for a five-minute workflow.

---

## Phase 4: Data model

At HLD level, identify:

* Main entities
* Primary keys
* Foreign keys or ownership relationships
* Status fields
* Timestamps
* Frequently queried attributes
* Required indexes
* Large payload storage strategy

Start from access patterns, not from tables.

Example:

```text
Query: Show the last 20 runs for a project.

Required fields:
- project_id
- created_at
- run_id

Likely index:
(project_id, created_at DESC, run_id DESC)
```

---

## Phase 5: High-level architecture

Draw the major execution path:

```text
Client
  → API Gateway
  → Application Service
  → Database
  → Queue/Event Bus
  → Worker or Workflow Engine
  → External Tools and Models
```

Show separately:

* Synchronous request path
* Asynchronous execution path
* Data storage
* Caching
* External integrations
* Observability
* Failure handling

---

## Phase 6: Deep dives, trade-offs, and summary

The interviewer may ask you to deep dive into:

* Workflow orchestration
* Idempotency
* Retry handling
* Database schema
* Caching
* Queue semantics
* Tool callbacks
* Multi-tenancy
* Security
* Audit logging
* Cost controls

Close with:

1. What the design guarantees
2. Important trade-offs
3. Known bottlenecks
4. What you would build next

---

# Reusable clarifying-question checklist

You do not need to ask all of these. Select the most architecture-changing questions.

## Product and users

1. Who are the primary callers: end users, internal services, or both?
2. What is the main user journey?
3. What is included in the MVP?
4. What is explicitly out of scope?
5. Are agent runs interactive, batch-oriented, or both?
6. Can a workflow run for seconds, minutes, or hours?
7. Must users be able to cancel, pause, or resume runs?
8. Are human approvals required?

## Scale

9. How many DAU or tenant organizations do we expect?
10. How many runs does one user or tenant create per day?
11. What is the expected peak-to-average traffic ratio?
12. How many tools or model calls occur in one run?
13. What is the expected input and output payload size?
14. What is the retention period for runs, logs, and artifacts?

## NFRs

15. What are the latency SLOs for starting and reading a run?
16. What availability target is required: 99.9%, 99.95%, or higher?
17. Is eventual consistency acceptable for run status?
18. What durability or disaster-recovery targets are required?
19. Are there cost limits per run or per tenant?

## Security and tenancy

20. Is this multi-tenant, and what isolation level is required?
21. What authentication and authorization system already exists?
22. Do we handle PII, secrets, regulated data, or customer documents?
23. Are immutable audit logs required?
24. Are there data-residency or regional-compliance requirements?

## Integrations

25. Which LLM providers and tool systems must be supported?
26. Do tools call us back, or do we poll them?
27. Are there integration rate limits?
28. Must the API support REST, gRPC, events, or all three?
29. Are clients able to consume webhooks or streaming events?

A useful interview opening is:

> “Before proposing the architecture, I want to clarify the workload shape, execution duration, consistency expectations, tenancy model, and reliability target because those will determine whether we need asynchronous orchestration, caching, and regional redundancy.”

---

# B. Capacity estimation

## Core formulas

### Daily operations

```text
Daily requests =
    Daily active users
    × actions per user per day
```

Example:

```text
50,000 DAU × 4 runs/day = 200,000 runs/day
```

---

### Average QPS

```text
Average QPS =
    Requests per day / 86,400
```

Example:

```text
200,000 / 86,400 ≈ 2.3 requests/second
```

---

### Peak QPS

```text
Peak QPS =
    Average QPS × peak factor
```

Typical rough peak factors:

* Globally distributed steady traffic: 2–4×
* Business-hour workload: 5–10×
* Event-driven or bursty workload: 10–20× or more

Always state the assumption.

---

### Concurrent requests or workflows

```text
Concurrency ≈ QPS × average operation duration
```

For 20 workflow starts per second where each workflow lasts 60 seconds:

```text
20 × 60 = 1,200 active workflows
```

This is why low API QPS can still create a large worker workload.

---

### Storage growth

```text
Storage/day =
    Records/day
    × average bytes per record
```

Physical storage should include:

* Database indexes
* Replication
* Write-ahead logs
* Backups
* Vector-index overhead
* Object-store versioning

A rough planning multiplier might be 2–3× logical storage, depending on the technology.

---

### Bandwidth

```text
Bandwidth per second =
    QPS × average payload size
```

Convert bytes per second to bits per second:

```text
Mbps = bytes/second × 8 / 1,000,000
```

---

### Cache impact

```text
Database read QPS =
    Read QPS × (1 - cache hit rate)
```

Example:

```text
140 read QPS × (1 - 0.80) = 28 database QPS
```

---

## Mini scenario 1: AgentRun API sizing

### Assumptions

| Item                      | Assumption |
| ------------------------- | ---------: |
| DAU                       |     50,000 |
| Runs per active user/day  |          4 |
| Runs/day                  |    200,000 |
| Status checks per run     |          6 |
| Tool executions per run   |          5 |
| List-runs requests/day    |    100,000 |
| Peak factor               |        10× |
| Status-cache hit rate     |        80% |
| Average workflow duration | 90 seconds |

### API QPS

| Operation      |  Requests/day |  Avg QPS | Peak QPS |
| -------------- | ------------: | -------: | -------: |
| Start run      |       200,000 |      2.3 |       23 |
| Get status     |     1,200,000 |     13.9 |      139 |
| Tool callbacks |     1,000,000 |     11.6 |      116 |
| List runs      |       100,000 |      1.2 |       12 |
| **Total**      | **2,500,000** | **29.0** |  **290** |

### Database read impact

Status requests are the dominant read workload.

With an 80% cache-hit rate:

```text
139 peak status QPS × 20% cache miss
≈ 28 database reads/second
```

This is easily manageable for a relational database, provided queries and indexes are clean.

### Workflow concurrency

At peak:

```text
23 new runs/second × 90 seconds
≈ 2,070 concurrently active workflows
```

The API QPS is modest, but the orchestrator must handle approximately 2,000 active workflows.

### Storage assumptions

| Data                   |   Per run | Daily logical storage |
| ---------------------- | --------: | --------------------: |
| AgentRun metadata      |      4 KB |                0.8 GB |
| Five tool executions   |     10 KB |                2.0 GB |
| Audit events           |      8 KB |                1.6 GB |
| Logs and artifact data |     25 KB |                5.0 GB |
| **Total**              | **47 KB** |        **9.4 GB/day** |

Allowing approximately 2.5× for indexes, replication, and operational overhead:

```text
9.4 GB/day × 2.5 ≈ 23.5 GB/day physical
```

For 30 days:

```text
23.5 × 30 ≈ 705 GB
```

Large logs and artifacts should therefore go to object storage rather than the relational database.

### API bandwidth

Assume average API metadata traffic is approximately 2 KB per request:

```text
290 peak QPS × 2 KB
= 580 KB/s
≈ 4.6 Mbps
```

API bandwidth is not the bottleneck. Tool payloads, model traffic, logs, and artifacts will dominate.

### Architectural conclusion

* A relational database is sufficient for metadata.
* A queue or durable workflow engine is required because execution is asynchronous.
* Redis is useful for hot run status and rate limiting.
* Object storage should hold large inputs, outputs, logs, and artifacts.
* Worker capacity should be based on concurrent runs and tool calls, not just API QPS.

---

## Mini scenario 2: Document ingestion sizing

### Assumptions

| Item                     | Assumption |
| ------------------------ | ---------: |
| PDFs/day                 |     10,000 |
| Average PDF size         |       8 MB |
| Average pages/PDF        |         50 |
| Words/page               |        400 |
| Tokens/word              |        1.3 |
| Chunk size               | 500 tokens |
| Overlap                  |        15% |
| Embedding dimensions     |      1,536 |
| Embedding representation |    float32 |
| Peak factor              |        10× |

### Raw document storage

```text
10,000 PDFs × 8 MB
= 80,000 MB
≈ 80 GB/day
```

---

### Tokens per document

```text
50 pages × 400 words/page
= 20,000 words

20,000 × 1.3
= 26,000 tokens/document
```

With 15% overlap, the effective new content per chunk is:

```text
500 × 0.85 = 425 tokens
```

Estimated chunks per document:

```text
26,000 / 425 ≈ 62 chunks
```

Total chunks/day:

```text
10,000 × 62 = 620,000 chunks/day
```

---

### Processing throughput

Document ingestion:

```text
10,000 / 86,400
≈ 0.116 documents/second average
```

At 10× peak:

```text
≈ 1.2 documents/second
```

Chunk and embedding throughput:

```text
620,000 / 86,400
≈ 7.2 chunks/second average
```

At peak:

```text
≈ 72 chunks/second
```

This is a more useful worker-sizing number than document QPS.

---

### Embedding storage

A 1,536-dimensional float32 vector requires:

```text
1,536 × 4 bytes
= 6,144 bytes
≈ 6 KB
```

Assume approximately 2 KB more for metadata and basic index overhead:

```text
≈ 8 KB/chunk
```

Daily vector storage:

```text
620,000 × 8 KB
≈ 4.96 GB/day
```

Chunk text, at approximately 2 KB/chunk:

```text
620,000 × 2 KB
≈ 1.24 GB/day
```

Logical daily growth:

| Data                 |      Growth/day |
| -------------------- | --------------: |
| Raw PDFs             |           80 GB |
| Chunk text           |         1.24 GB |
| Vectors and metadata |         4.96 GB |
| **Total**            | **86.2 GB/day** |

Vector indexes can add significant overhead, so physical vector storage may be two or more times the raw vector size.

---

### Peak upload bandwidth

```text
1.2 PDFs/second × 8 MB
= 9.6 MB/s
≈ 77 Mbps
```

For large uploads, clients should upload directly to object storage using presigned URLs. The application API should receive metadata and the object URI, not proxy every PDF byte.

### Architectural conclusion

* Object storage is essential for source documents.
* Parsing, chunking, and embedding should be asynchronous.
* Each processing stage should be independently retryable.
* Batch embedding calls should reduce provider overhead.
* The vector store must be sized by chunks and dimensions, not PDF count.
* The ingestion system needs backpressure because model or embedding-provider limits may become the bottleneck.

---

# C. API-design expectations

## General API principles

Use nouns for resources:

```http
/runs
/projects
/documents
/audit-events
```

Avoid action-heavy paths such as:

```http
/startAgentExecutionNow
```

Prefer:

```http
POST /v1/projects/{project_id}/runs
```

The HTTP method already communicates “create.”

---

## API versioning

Common options:

```http
/v1/projects/{project_id}/runs
```

or versioning through headers.

Path-based versioning is usually easier to explain and operate during an interview.

Version APIs when making breaking changes such as:

* Renaming response fields
* Changing field types
* Removing behavior
* Changing pagination semantics
* Changing error contracts

Do not create a new version for every additive optional field.

---

## Filtering and sorting

Example:

```http
GET /v1/projects/proj_123/runs
    ?status=FAILED
    &created_after=2026-07-01T00:00:00Z
    &limit=20
    &cursor=eyJjcmVhdGVkX2F0IjoiLi4uIn0=
```

Validate:

* Allowed filters
* Maximum page size
* Sort directions
* Tenant ownership
* Date ranges

---

## Cursor pagination

Prefer cursor pagination for frequently changing datasets.

Response:

```json
{
  "items": [
    {
      "run_id": "run_01J...",
      "status": "RUNNING",
      "created_at": "2026-07-14T16:20:00Z"
    }
  ],
  "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNi0wNy0xNFQxNjoyMDowMFoiLCJydW5faWQiOiJydW5fMDFKIn0="
}
```

Why not offset pagination?

```text
LIMIT 20 OFFSET 100000
```

Problems:

* Increasing database cost
* Duplicate or missing records when new rows are inserted
* Poor performance for deep pages

A cursor commonly contains the last record’s sort fields:

```text
created_at + run_id
```

---

## Idempotency keys

Use idempotency for operations where retries could create duplicate side effects.

Examples:

* Start an agent run
* Submit a document for ingestion
* Process a payment
* Receive a tool callback
* Approve a workflow step

Request:

```http
POST /v1/projects/proj_123/runs
Idempotency-Key: 44f12d8f-c81c-4d76-9eb8-d08f0f1809db
```

Store:

```text
tenant_id
idempotency_key
request_hash
created_resource_id
response_status
expiration
```

Behavior:

1. First request creates the run.
2. A retry with the same key and same body returns the original response.
3. The same key with a different request body returns a conflict.
4. Idempotency records expire after an agreed period.

---

## Standard error model

```json
{
  "error": {
    "code": "RUN_NOT_FOUND",
    "message": "The requested agent run does not exist.",
    "request_id": "req_01J2ABC123",
    "details": {
      "run_id": "run_123"
    }
  }
}
```

Recommended fields:

* `code`: stable machine-readable error
* `message`: readable explanation
* `request_id`: trace and support correlation
* `details`: optional structured context

Typical mappings:

| HTTP status | Meaning                           |
| ----------- | --------------------------------- |
| 400         | Invalid input                     |
| 401         | Missing or invalid authentication |
| 403         | Authenticated but unauthorized    |
| 404         | Resource not found                |
| 409         | State or idempotency conflict     |
| 422         | Semantically invalid request      |
| 429         | Rate limit exceeded               |
| 500         | Unexpected internal failure       |
| 502/503     | Dependency unavailable            |
| 504         | Dependency timeout                |

Do not expose stack traces, database details, secrets, or internal hostnames.

---

# D. Agent-platform data-model starter

## 1. Tenant

```text
Tenant
- tenant_id: UUID/ULID, primary key
- name
- plan
- status
- region
- created_at
- updated_at
```

Represents the security, billing, and data-isolation boundary.

---

## 2. User

```text
User
- user_id: UUID/ULID, primary key
- tenant_id: foreign key
- email
- display_name
- role
- status
- created_at
```

Important uniqueness constraint:

```text
UNIQUE (tenant_id, email)
```

---

## 3. Project

```text
Project
- project_id: UUID/ULID, primary key
- tenant_id
- name
- description
- created_by
- created_at
- updated_at
```

Every lookup must enforce tenant ownership.

---

## 4. AgentRun

```text
AgentRun
- run_id: time-sortable ULID, primary key
- tenant_id
- project_id
- agent_id
- agent_version
- status
- idempotency_key
- input_artifact_id
- output_artifact_id
- current_step
- error_code
- error_message_sanitized
- created_by
- created_at
- started_at
- completed_at
- updated_at
- version
```

Possible statuses:

```text
QUEUED
RUNNING
WAITING_FOR_TOOL
WAITING_FOR_HUMAN
SUCCEEDED
FAILED
CANCEL_REQUESTED
CANCELLED
TIMED_OUT
```

The `version` field can support optimistic concurrency control.

---

## 5. ToolExecution

```text
ToolExecution
- tool_execution_id
- tenant_id
- run_id
- tool_type
- tool_name
- status
- attempt_number
- external_request_id
- request_artifact_id
- response_artifact_id
- error_code
- started_at
- completed_at
- created_at
```

Tool status:

```text
PENDING
RUNNING
SUCCEEDED
FAILED
TIMED_OUT
CANCELLED
```

---

## 6. Artifact

```text
Artifact
- artifact_id
- tenant_id
- run_id
- artifact_type
- object_uri
- checksum
- content_type
- size_bytes
- encryption_key_reference
- created_at
- expires_at
```

Large data stays in object storage. The table stores metadata and references.

---

## 7. Feedback

```text
Feedback
- feedback_id
- tenant_id
- run_id
- user_id
- rating
- category
- comment
- created_at
```

---

## 8. AuditLog

```text
AuditLog
- audit_id: time-sortable identifier
- tenant_id
- actor_type
- actor_id
- action
- resource_type
- resource_id
- request_id
- source_ip_hash
- details_json
- occurred_at
```

For strong compliance requirements, audit records should be append-only and shipped to immutable storage.

---

## Optional ingestion entities

Because the case study includes document ingestion:

```text
Document
- document_id
- tenant_id
- project_id
- object_uri
- checksum
- ingestion_status
- created_at
- updated_at
```

```text
DocumentChunk
- chunk_id
- tenant_id
- document_id
- chunk_number
- text_uri or text
- embedding_id
- token_count
- metadata_json
```

---

## Five important indexes

### Index 1: Last 20 runs for a project

```sql
CREATE INDEX idx_agent_run_project_created
ON agent_run (project_id, created_at DESC, run_id DESC);
```

Supports:

```sql
WHERE project_id = ?
ORDER BY created_at DESC, run_id DESC
LIMIT 20;
```

---

### Index 2: Idempotent run creation

```sql
CREATE UNIQUE INDEX idx_agent_run_tenant_idempotency
ON agent_run (tenant_id, idempotency_key)
WHERE idempotency_key IS NOT NULL;
```

---

### Index 3: Tenant audit trail by time

```sql
CREATE INDEX idx_audit_tenant_time
ON audit_log (tenant_id, occurred_at DESC, audit_id DESC);
```

---

### Index 4: Tool failures by type and status

```sql
CREATE INDEX idx_tool_failure_type_status
ON tool_execution (
    tenant_id,
    tool_type,
    status,
    started_at DESC
);
```

Supports queries such as:

```sql
WHERE tenant_id = ?
  AND tool_type = 'SEARCH'
  AND status = 'FAILED'
ORDER BY started_at DESC;
```

---

### Index 5: Tool history for one run

```sql
CREATE INDEX idx_tool_execution_run_time
ON tool_execution (run_id, started_at ASC, tool_execution_id ASC);
```

This supports timeline reconstruction.

---

# E. LLD basics

## Responsibility

A class should have a clear reason to exist.

Poor responsibility:

```text
AgentManager
- validates input
- writes SQL
- calls LLMs
- sends emails
- uploads files
- calculates billing
```

Better separation:

```text
RunService             → business use case
RunRepository          → persistence
WorkflowDispatcher     → queue/workflow interaction
ToolGateway            → tool integrations
ArtifactStore          → object storage
AuditWriter            → audit events
```

---

## Cohesion

High cohesion means related behavior stays together.

A `RunRepository` containing run persistence methods is cohesive.

A `RunRepository` that also formats prompts and sends Slack notifications has low cohesion.

---

## Coupling

Coupling describes how strongly components depend on one another.

Bad:

```python
class RunService:
    def start(self):
        # Direct construction couples this class to specific infrastructure.
        db = PostgreSQLClient(...)
        queue = KafkaProducer(...)
        llm = SpecificVendorLLM(...)
```

Better:

```python
class RunService:
    def __init__(
        self,
        repository: RunRepository,
        dispatcher: WorkflowDispatcher,
        audit_writer: AuditWriter,
    ):
        self.repository = repository
        self.dispatcher = dispatcher
        self.audit_writer = audit_writer
```

Dependencies are passed through interfaces, making the service testable and replaceable.

---

## Interfaces

An interface defines what a dependency promises, without tying callers to the implementation.

```python
from typing import Protocol


class RunRepository(Protocol):
    def create(self, run: "AgentRun") -> "AgentRun":
        """Persist a new run and return the stored representation."""
        ...

    def get(self, tenant_id: str, run_id: str) -> "AgentRun | None":
        """Return a tenant-owned run, or None when it does not exist."""
        ...

    def update_status(
        self,
        tenant_id: str,
        run_id: str,
        expected_version: int,
        new_status: str,
    ) -> bool:
        """Atomically update status using optimistic concurrency."""
        ...


class WorkflowDispatcher(Protocol):
    def dispatch(self, run_id: str) -> None:
        """Submit a durable workflow-start command."""
        ...
```

Possible implementations:

```text
PostgresRunRepository
DynamoRunRepository
KafkaWorkflowDispatcher
SQSWorkflowDispatcher
TemporalWorkflowDispatcher
```

The business logic depends on capabilities, not vendors.

---

## Simple LLD template

When an interviewer asks, “Deep dive into the run-starting component,” use this flow.

### 1. Classes

List approximately 4–8 important classes.

```text
RunController
RunService
RunRepository
IdempotencyStore
WorkflowDispatcher
AuditWriter
ArtifactStore
```

### 2. Responsibilities

Explain one responsibility per class.

### 3. Interfaces

Define important method contracts and return values.

### 4. Sequence flow

Show the runtime call order.

### 5. State and concurrency

Explain:

* Transactions
* Locks
* Optimistic concurrency
* Idempotency
* Duplicate messages

### 6. Edge cases

Cover:

* Invalid request
* Duplicate start
* Database success but queue failure
* Queue duplicate
* Timeout
* Cancellation race
* Unauthorized tenant access

### 7. Tests

Include:

* Unit tests
* Repository integration tests
* Contract tests
* Concurrency tests
* Failure-injection tests
* End-to-end tests

---

## Example LLD sequence: start run

```text
Client
  → RunController
      → Authentication/authorization
      → Request validation
      → RunService.start_run()
          → IdempotencyStore.lookup()
          → RunRepository.insert()
          → OutboxRepository.insert_event()
          → AuditWriter.record()
      ← Database transaction commits
  ← 202 Accepted

Outbox Publisher
  → Queue/Workflow Engine
      → Workflow Worker
          → Agent execution starts
```

The run row and outbox event should be created in the same database transaction.

This avoids:

```text
Database insert succeeds
Queue publish fails
Result: run remains QUEUED forever
```

The transactional outbox allows a background publisher to retry safely.

---

# F. Case study: Design an AgentRun service

## Problem statement

Design a service that:

* Starts an agent workflow
* Tracks its status
* Executes external tools
* Receives asynchronous callbacks
* Persists outputs and artifacts
* Maintains an audit trail
* Supports multi-tenant access

---

# Deliverable 1: Functional and NFR list

## MVP functional requirements

1. Start an asynchronous agent run.
2. Provide an initial run ID immediately.
3. Get current run status and summary.
4. List runs for a project.
5. Execute tools as part of a workflow.
6. Receive authenticated tool callbacks.
7. Retry retryable workflow steps.
8. Store run inputs, outputs, and artifacts.
9. Cancel a queued or running workflow.
10. Record audit events.
11. Submit a document for asynchronous ingestion.
12. Search audit history.

## Phase-two functional requirements

1. Pause and resume workflows.
2. Human approval steps.
3. Webhooks for run-state changes.
4. Server-sent events or WebSocket streaming.
5. Workflow scheduling and priorities.
6. Run cloning and replay.
7. Agent-version comparison.
8. Multi-agent collaboration.
9. Cost budgets and per-tenant quotas.
10. Cross-region execution.
11. Advanced evaluation and feedback dashboards.
12. Tool marketplace and dynamic tool registration.

---

## MVP NFRs

### Latency

* Start run: p95 below 300 ms for accepting the request.
* Get status: p95 below 150 ms from cache, below 300 ms from database.
* List runs: p95 below 500 ms.
* Tool callback acknowledgement: p95 below 300 ms.

These are control-plane SLOs. The full workflow may take minutes.

### Availability

* API availability: 99.9% initially.
* Durable workflow submission.
* No accepted run should be silently lost.

### Durability

* Run metadata stored durably.
* Large artifacts stored in replicated object storage.
* Queue/workflow state survives worker restart.

### Consistency

* Strong consistency for run creation and idempotency.
* Eventual consistency acceptable for cache and analytical views.
* Status transitions must be monotonic and validated.

### Security

* OAuth2/JWT or service identity.
* Tenant-level authorization.
* Encryption in transit and at rest.
* Secrets stored in a secrets manager.
* Signed tool callbacks.
* PII redaction in logs.

### Scalability

* Horizontal API and worker scaling.
* Handle approximately 300 peak control-plane QPS.
* Support approximately 2,000 concurrent workflows for the initial estimate.

### Observability

* Metrics, logs, and traces correlated by:

  * `request_id`
  * `run_id`
  * `tenant_id`
  * `tool_execution_id`

### Cost

* Per-tenant model and tool usage accounting.
* Configurable timeouts and token budgets.
* Object-storage lifecycle rules.

---

## Phase-two NFRs

* 99.95% or 99.99% availability
* Regional failover
* Data residency controls
* Immutable compliance archive
* Per-tenant encryption keys
* Priority scheduling
* Fairness across tenants
* Strict cost budgets
* Automated disaster-recovery exercises

---

# Deliverable 2: Capacity table

## AgentRun control-plane capacity

| Metric                             |  Estimate |
| ---------------------------------- | --------: |
| DAU                                |    50,000 |
| Runs/day                           |   200,000 |
| Average total API QPS              |        29 |
| Peak total API QPS                 |       290 |
| Peak start-run QPS                 |        23 |
| Peak status-read QPS               |       139 |
| Peak tool-callback QPS             |       116 |
| Active workflow concurrency        |    ~2,070 |
| Logical metadata and artifacts/day |   ~9.4 GB |
| Physical storage/day               |  ~23.5 GB |
| 30-day physical storage            |   ~705 GB |
| API metadata bandwidth at peak     | ~4.6 Mbps |

## Document-ingestion capacity

| Metric                         |     Estimate |
| ------------------------------ | -----------: |
| PDFs/day                       |       10,000 |
| Raw document growth/day        |        80 GB |
| Chunks/day                     |      620,000 |
| Average embedding throughput   | 7.2 chunks/s |
| Peak embedding throughput      |  72 chunks/s |
| Vector and metadata growth/day |        ~5 GB |
| Chunk-text growth/day          |     ~1.24 GB |
| Total logical storage/day      |       ~86 GB |
| Peak raw upload bandwidth      |     ~77 Mbps |

---

# Deliverable 3: Eight API contracts

## 1. Start a run

```http
POST /v1/projects/{project_id}/runs
Authorization: Bearer <token>
Idempotency-Key: <uuid>
```

Request:

```json
{
  "agent_id": "customer-support-agent",
  "agent_version": "12",
  "input": {
    "message": "Summarize the incident and recommend the next action."
  },
  "execution_options": {
    "timeout_seconds": 600,
    "priority": "NORMAL"
  }
}
```

Response:

```http
202 Accepted
```

```json
{
  "run_id": "run_01J2ABC",
  "status": "QUEUED",
  "created_at": "2026-07-14T16:20:00Z",
  "status_url": "/v1/runs/run_01J2ABC"
}
```

---

## 2. Get run status

```http
GET /v1/runs/{run_id}
```

Response:

```json
{
  "run_id": "run_01J2ABC",
  "project_id": "proj_123",
  "status": "RUNNING",
  "current_step": "SEARCH_KNOWLEDGE_BASE",
  "progress": {
    "completed_steps": 3,
    "total_steps": 7
  },
  "created_at": "2026-07-14T16:20:00Z",
  "started_at": "2026-07-14T16:20:02Z",
  "updated_at": "2026-07-14T16:20:08Z"
}
```

---

## 3. List project runs

```http
GET /v1/projects/{project_id}/runs
    ?status=FAILED
    &limit=20
    &cursor=<opaque-cursor>
```

Response:

```json
{
  "items": [
    {
      "run_id": "run_01J2ABC",
      "status": "FAILED",
      "agent_id": "customer-support-agent",
      "created_at": "2026-07-14T16:20:00Z"
    }
  ],
  "next_cursor": "opaque-value"
}
```

---

## 4. Cancel a run

```http
POST /v1/runs/{run_id}/cancellation
Idempotency-Key: <uuid>
```

Response:

```http
202 Accepted
```

```json
{
  "run_id": "run_01J2ABC",
  "status": "CANCEL_REQUESTED"
}
```

Cancellation is usually cooperative. A tool call may not be interruptible immediately.

---

## 5. Tool callback

```http
POST /v1/tool-executions/{tool_execution_id}/callback
X-Callback-Timestamp: 2026-07-14T16:20:10Z
X-Callback-Signature: <signature>
Idempotency-Key: <provider-event-id>
```

Request:

```json
{
  "external_request_id": "ext_987",
  "status": "SUCCEEDED",
  "result_artifact_id": "artifact_555",
  "completed_at": "2026-07-14T16:20:09Z"
}
```

Response:

```http
202 Accepted
```

Callback processing should verify:

* Signature
* Timestamp freshness
* Expected tool execution
* Tenant or integration ownership
* Duplicate event ID
* Valid status transition

---

## 6. Submit document ingestion

For small documents:

```http
POST /v1/projects/{project_id}/documents
Idempotency-Key: <uuid>
```

Request:

```json
{
  "file_name": "policy.pdf",
  "object_uri": "s3://tenant-bucket/uploads/policy.pdf",
  "checksum": "sha256:...",
  "content_type": "application/pdf"
}
```

Response:

```http
202 Accepted
```

```json
{
  "document_id": "doc_123",
  "ingestion_status": "QUEUED"
}
```

For large files, use a separate API to obtain a presigned upload URL.

---

## 7. Get document-ingestion status

```http
GET /v1/documents/{document_id}
```

Response:

```json
{
  "document_id": "doc_123",
  "ingestion_status": "EMBEDDING",
  "progress": {
    "pages_parsed": 50,
    "chunks_created": 62,
    "chunks_embedded": 40
  }
}
```

---

## 8. Search audit events

```http
GET /v1/audit-events
    ?resource_type=AGENT_RUN
    &resource_id=run_01J2ABC
    &created_after=2026-07-01T00:00:00Z
    &limit=100
    &cursor=<opaque-cursor>
```

Response:

```json
{
  "items": [
    {
      "audit_id": "audit_01J...",
      "actor_id": "user_123",
      "action": "RUN_CREATED",
      "resource_type": "AGENT_RUN",
      "resource_id": "run_01J2ABC",
      "request_id": "req_456",
      "occurred_at": "2026-07-14T16:20:00Z"
    }
  ],
  "next_cursor": null
}
```

---

# High-level architecture

```text
                         ┌──────────────────────────┐
                         │ Web / SDK / API Clients  │
                         └─────────────┬────────────┘
                                       │
                          HTTPS / REST / gRPC
                                       │
                         ┌─────────────▼────────────┐
                         │ API Gateway / Load       │
                         │ Balancer / WAF           │
                         └─────────────┬────────────┘
                                       │
                    Auth, rate limit, request ID, tenant
                                       │
           ┌───────────────────────────▼──────────────────────────┐
           │                  AgentRun API Service                │
           │ validation, authorization, idempotency, run queries │
           └───────────┬────────────────┬────────────────────────┘
                       │                │
                 transaction            │ hot status
                       │                │
               ┌───────▼────────┐  ┌────▼─────┐
               │ PostgreSQL      │  │ Redis    │
               │ Runs, tools,    │  │ status,  │
               │ outbox, audit   │  │ limits   │
               └───────┬────────┘  └──────────┘
                       │
                Outbox publisher
                       │
             ┌─────────▼────────────┐
             │ Queue / Event Bus or │
             │ Durable Workflow     │
             │ Engine               │
             └─────────┬────────────┘
                       │
             ┌─────────▼────────────┐
             │ Agent Workflow       │
             │ Workers              │
             │ state, retries, DAG  │
             └──────┬────────┬──────┘
                    │        │
            ┌───────▼───┐  ┌─▼─────────────────┐
            │ LLM       │  │ Tool Gateway       │
            │ Gateway   │  │ policies, retries, │
            │ routing   │  │ credentials        │
            └───────┬───┘  └────────┬──────────┘
                    │               │
              LLM providers      External tools
                                    │
                           signed callbacks
                                    │
                         ┌──────────▼───────────┐
                         │ Callback API         │
                         └──────────────────────┘

      ┌─────────────────────┐      ┌─────────────────────────────┐
      │ Object Storage      │      │ Document Ingestion Workers  │
      │ inputs, outputs,    │◄────►│ parse → chunk → embed       │
      │ logs, artifacts     │      └──────────────┬──────────────┘
      └─────────────────────┘                     │
                                          ┌───────▼───────┐
                                          │ Vector Store  │
                                          └───────────────┘

      Logs + Metrics + Traces → Observability Platform
      Audit Stream            → Immutable Compliance Archive
```

---

# Important architectural choices

## 1. Async run creation

The start API should:

1. Validate and authorize.
2. Create the run.
3. Create an outbox event.
4. Commit.
5. Return `202 Accepted`.

Actual workflow execution happens asynchronously.

Benefits:

* Fast API response
* Independent scaling
* Durable execution
* Better retry handling
* No long-lived HTTP connections

---

## 2. Transactional outbox

Avoid dual writes:

```text
Write database
Publish queue message
```

Either operation can fail independently.

Instead:

```text
Database transaction:
- Insert AgentRun
- Insert OutboxEvent
- Insert AuditLog
```

A publisher repeatedly scans unpublished outbox rows and sends them to the queue.

The consumer must still be idempotent because the event may be published more than once.

---

## 3. At-least-once delivery

Most practical queues provide at-least-once processing.

Therefore:

```text
Duplicate delivery is expected, not exceptional.
```

Every consumer should use:

* Event ID
* Run ID
* Tool execution ID
* State validation
* Deduplication record
* Idempotent side effects

Avoid claiming “exactly once” without defining the boundary and mechanism.

---

## 4. Run-state machine

Validate transitions:

```text
QUEUED → RUNNING
RUNNING → WAITING_FOR_TOOL
WAITING_FOR_TOOL → RUNNING
RUNNING → SUCCEEDED
RUNNING → FAILED
RUNNING → CANCEL_REQUESTED
CANCEL_REQUESTED → CANCELLED
```

Invalid example:

```text
SUCCEEDED → RUNNING
```

Terminal states should usually be immutable.

Use optimistic concurrency:

```sql
UPDATE agent_run
SET status = ?, version = version + 1
WHERE run_id = ?
  AND version = ?;
```

If no row changes, another worker modified the run and the operation must be retried or rejected.

---

## 5. Polling, webhooks, and streaming

### MVP: Polling

Simplest client behavior:

```http
GET /runs/{run_id}
```

Good for moderate traffic.

### Phase two: Webhooks

Useful for server-to-server clients.

Challenges:

* Callback authentication
* Retry policies
* Dead-letter queues
* Delivery history
* Consumer outages

### Streaming

SSE is often simpler than WebSockets for one-way status and token updates.

Use WebSockets when bidirectional interaction is truly required.

---

## 6. SQL versus NoSQL

Relational storage is a strong starting point because:

* State transitions need transactions.
* Entities are related.
* Queries use project, tenant, status, and time.
* Idempotency requires uniqueness.
* Initial QPS is moderate.

A NoSQL store may become useful when:

* Run volume reaches extreme scale.
* Access patterns are simple and fixed.
* Global active-active writes are required.
* Tenant partitioning maps cleanly to partition keys.

Do not choose NoSQL merely because the system “needs scale.”

---

## 7. Workflow engine versus queue plus custom state machine

### Queue plus custom workers

Advantages:

* Simple initial setup
* Full control
* Lower platform dependency

Costs:

* You implement retries
* State persistence
* Timers
* Recovery
* Workflow versioning
* Compensation
* Long-running execution

### Durable workflow engine

Examples conceptually include durable orchestration systems.

Advantages:

* Durable state
* Retries and timers
* Workflow recovery
* Long-running execution
* Better workflow visibility

Costs:

* New operational model
* Vendor/framework coupling
* Workflow determinism constraints
* Migration complexity

For complex, long-running agent workflows, a durable workflow engine is usually preferable.

---

# Reliability deep dive

## Failure: API succeeds but workflow never starts

Protection:

* Transactional outbox
* Outbox retry
* Alert on old `QUEUED` runs
* Reconciliation job

## Failure: Worker crashes during a tool call

Protection:

* Persist tool-execution state
* Timeout
* Retry policy
* Idempotency key sent to the tool
* Reconcile unknown external state before retrying

## Failure: Duplicate callback

Protection:

* Provider event ID
* Unique constraint
* Current-state validation
* Return success for already-processed events

## Failure: Poison message

Protection:

* Maximum attempts
* Exponential backoff
* Dead-letter queue
* Operator visibility
* Replay tooling

## Failure: LLM provider outage

Protection:

* Timeout
* Circuit breaker
* Retry only retryable failures
* Provider fallback where semantics permit
* Per-provider concurrency limits

## Failure: One tenant overloads workers

Protection:

* Per-tenant rate limits
* Fair queues
* Weighted scheduling
* Quotas
* Maximum concurrent runs
* Priority isolation

---

# Security deep dive

* Authenticate every API request.
* Derive `tenant_id` from trusted identity claims, not request input.
* Apply tenant filtering to every database query.
* Use short-lived tool credentials.
* Store secrets in a secrets manager.
* Sign callbacks and check replay windows.
* Encrypt object storage and databases.
* Redact prompts and outputs before logging.
* Restrict tool egress destinations.
* Keep an immutable audit trail for privileged actions.
* Apply content and authorization policies before tool execution.
* Never allow arbitrary LLM-generated URLs or shell commands without validation.

---

# Observability

## Metrics

* Run starts per second
* Runs by status
* Run duration percentiles
* Queue depth
* Queue age
* Tool success and failure rates
* Tool latency by type
* LLM latency and error rate
* Tokens and cost per tenant
* Retry count
* Dead-letter count
* Stale queued/running runs
* Cache hit rate
* Database latency

## Logs

Use structured logs:

```json
{
  "level": "INFO",
  "event": "tool_execution_completed",
  "request_id": "req_123",
  "tenant_id": "tenant_1",
  "run_id": "run_1",
  "tool_execution_id": "tool_exec_1",
  "tool_type": "SEARCH",
  "duration_ms": 842,
  "status": "SUCCEEDED"
}
```

Do not log raw secrets, credentials, or unrestricted prompt content.

## Tracing

A single trace should connect:

```text
Start API
→ workflow dispatch
→ workflow step
→ model call
→ tool call
→ callback
→ status update
```

Because workflow execution is asynchronous, trace context must be carried in messages.

---

# Twelve common interview mistakes

## Requirements mistakes

1. **Starting with technology instead of the use case**
   Saying “I’ll use Kafka and Kubernetes” before defining requirements.

2. **Not defining MVP scope**
   Attempting streaming, human approval, global failover, analytics, and billing simultaneously.

3. **Ignoring non-functional requirements**
   No latency, availability, security, tenancy, or retention discussion.

4. **Not identifying the execution model**
   Missing the critical fact that agent runs are long-running and asynchronous.

## Capacity mistakes

5. **Using only average QPS**
   Peak traffic and burst behavior usually determine scaling.

6. **Counting only start-run requests**
   Status polling, callbacks, tool calls, and audit events may dominate.

7. **Ignoring concurrency**
   Low QPS can still mean thousands of active workflows.

8. **Using false precision**
   Presenting exact numbers without stating assumptions.

9. **Ignoring storage overhead**
   Counting raw records but omitting indexes, replicas, backups, and logs.

## API mistakes

10. **Making long workflows synchronous**
    Holding the request open until the entire agent finishes.

11. **Skipping idempotency**
    Retries create duplicate runs, documents, or tool side effects.

12. **Using offset pagination and inconsistent errors**
    Leads to poor scaling, unstable results, and difficult client integrations.

Other frequent issues include missing API versioning, tenant authorization, state-transition validation, and callback authentication.

---

# Ten interview Q&A

## 1. Why return `202 Accepted` instead of `200 OK`?

`202 Accepted` indicates that the request has been accepted but processing is still asynchronous. The response returns a run ID that clients can poll or subscribe to.

---

## 2. How do you ensure a run is not lost between the database and queue?

Create the run and an outbox event in the same database transaction. A background publisher reliably sends the outbox event to the queue.

---

## 3. How do you handle duplicate queue messages?

Assume at-least-once delivery. Use an event ID, validate the current run state, and ensure consumers and external calls are idempotent.

---

## 4. Why use a relational database?

The system needs transactions, uniqueness for idempotency, state transitions, tenant relationships, and time-based queries. The estimated QPS is well within relational-database capacity.

---

## 5. How would you prevent one tenant from consuming all workers?

Use per-tenant quotas, concurrency limits, rate limits, fair queues, weighted scheduling, and separate priority pools for critical workloads.

---

## 6. How do you cancel a running workflow?

Set the run to `CANCEL_REQUESTED` and notify the orchestrator. Workers check cancellation between steps. External operations may require provider-specific cancellation or may only stop after timeout.

---

## 7. How do you design retries?

Retry only transient failures, use exponential backoff with jitter, impose maximum attempts and deadlines, make operations idempotent, and send exhausted failures to a dead-letter queue.

---

## 8. How should large prompts, outputs, or artifacts be stored?

Store them in object storage and keep only URIs, checksums, sizes, and content metadata in the relational database.

---

## 9. How do you make tool callbacks secure?

Use signed requests, timestamp validation, replay protection, provider event IDs, allowlisted integrations, TLS, and state-transition checks.

---

## 10. When would you use a durable workflow engine?

When workflows are long-running, contain retries, timers, branching, human approval, resumability, or complex recovery. For a few short background jobs, a queue and workers may be sufficient.

---

# Five-to-seven-minute interview script

Use this as a spoken baseline rather than memorizing every sentence literally.

I’ll begin by clarifying the scope and then move through capacity, APIs, data model, architecture, and reliability trade-offs.

The system needs to start an agent workflow and track its status. I’ll assume it is a multi-tenant platform used through REST APIs. A run may last from several seconds to several minutes and can invoke multiple LLMs and external tools. For the MVP, I’ll support starting a run, reading its status, listing runs for a project, receiving tool callbacks, cancellation, document ingestion, artifact storage, and audit search. I’ll keep human approval, live token streaming, scheduled runs, and cross-region active-active execution for phase two.

For non-functional requirements, I’ll target a p95 latency below 300 milliseconds for accepting a run and below 150 milliseconds for cached status reads. The API should initially provide 99.9% availability. Once a run has been accepted, it must not be silently lost. Strong consistency is important for run creation, idempotency, and valid state transitions, while eventual consistency is acceptable for caches and analytics. The system must enforce tenant isolation, encrypt data, maintain an audit trail, and expose metrics, logs, and distributed traces.

For capacity, I’ll assume 50,000 daily active users and four runs per user per day, resulting in 200,000 runs per day. That is only about 2.3 start requests per second on average, but with a ten-times peak factor, it becomes approximately 23 start requests per second. If each run is checked six times, status traffic reaches approximately 139 peak requests per second. Assuming five tool callbacks per run, callbacks add approximately 116 peak requests per second. Overall, I estimate around 290 peak control-plane requests per second.

The more important execution metric is concurrency. At 23 new runs per second and an average workflow duration of 90 seconds, the platform may have around 2,000 concurrently active workflows. That drives worker and orchestration capacity. I estimate around 9 to 10 gigabytes of new logical metadata, audit, and artifact data per day. With indexes, replication, and operational overhead, physical growth may be around 20 to 25 gigabytes per day. Large prompts, outputs, tool responses, and logs should therefore go to object storage rather than the relational database.

The primary start API would be POST `/v1/projects/{project_id}/runs`. It would accept an idempotency key, agent identifier, version, input, timeout, and priority. It would return `202 Accepted`, a run ID, and the initial `QUEUED` status. Other important APIs are GET `/v1/runs/{run_id}`, GET `/v1/projects/{project_id}/runs` with cursor pagination, POST `/v1/runs/{run_id}/cancellation`, a signed tool-callback endpoint, document-ingestion endpoints, and an audit-search endpoint. All errors use a standard structure containing a stable error code, readable message, request ID, and optional details.

At the data-model level, the main entities are Tenant, User, Project, AgentRun, ToolExecution, Artifact, Feedback, and AuditLog. AgentRun stores tenant and project ownership, agent version, status, timestamps, an idempotency key, and references to input and output artifacts. ToolExecution stores the tool type, attempt number, external request ID, status, timing, and artifact references. Large payloads are placed in object storage.

The most important indexes include project ID plus descending creation time for the last 20 runs, a unique tenant and idempotency-key index, tenant plus audit timestamp for audit history, tenant plus tool type and status for failure analysis, and run ID plus start time for reconstructing a run’s tool timeline.

At the architecture level, clients call an API gateway that performs authentication, rate limiting, and request-ID generation. The AgentRun API validates authorization and writes the AgentRun row, an outbox event, and an audit record in one relational-database transaction. It then returns immediately. A background outbox publisher sends the workflow-start event to a queue or durable workflow engine. Workflow workers execute the agent steps, invoke an LLM gateway and a controlled tool gateway, and persist state changes.

The transactional outbox is important because directly writing the database and publishing to the queue creates a dual-write failure. The database could commit while publishing fails, leaving a run permanently queued. With the outbox, publishing can be retried safely. Since queues usually provide at-least-once delivery, every consumer is idempotent and validates the current state before applying a transition.

I would model the run as an explicit state machine: `QUEUED` to `RUNNING`, optionally to `WAITING_FOR_TOOL`, back to `RUNNING`, and finally to `SUCCEEDED`, `FAILED`, or `CANCELLED`. Terminal states cannot transition back to running. Optimistic concurrency using a version field prevents two workers from overwriting one another.

Redis can cache hot run-status responses and support rate limits, but the relational database remains the source of truth. Object storage holds documents, prompts, outputs, logs, and artifacts. Document ingestion is asynchronous: an upload is stored, then workers parse, chunk, embed, and index it in a vector store.

For reliability, I’ll use bounded retries with exponential backoff and jitter, timeouts, circuit breakers for LLM and tool dependencies, dead-letter queues, and reconciliation jobs for stale queued or running workflows. Callback requests must be signed, timestamped, deduplicated, and checked against the expected tool state.

For multi-tenancy, the authenticated identity determines the tenant. Every database query includes tenant ownership, and per-tenant rate limits and concurrency quotas prevent noisy-neighbor problems. Sensitive payloads are redacted from logs, secrets are stored in a secrets manager, and tool network access is restricted.

Finally, I would monitor queue depth, queue age, workflow latency, run outcomes, tool errors, retries, dead-letter messages, LLM latency, token cost, cache-hit rate, and stale runs. Every trace and structured log carries the request ID, tenant ID, run ID, and tool-execution ID.

The main trade-off is using a queue with a custom state machine versus a durable workflow engine. A queue is simpler for a small MVP, but complex long-running workflows require us to implement persistence, timers, retries, recovery, and workflow versioning. For an agent platform with branching, tool waits, and future human approvals, I would likely choose a durable workflow engine while keeping the API and persistence abstractions independent of that implementation.

Use the capacity section to demonstrate reasoning, but shorten it immediately if the interviewer wants to move to architecture.

---

# Cheat sheet: reusable system-design skeleton

```text
1. CLARIFY
   - Who are the users?
   - What are the top 3 use cases?
   - MVP versus phase two?
   - Sync or async?
   - Latency and availability SLO?
   - Multi-tenant?
   - Security/compliance?
   - Retention?
   - External integrations?

2. ESTIMATE
   - DAU × actions/day
   - Average QPS = requests/day ÷ 86,400
   - Peak QPS = average × peak factor
   - Concurrency = QPS × duration
   - Storage/day = records/day × bytes/record
   - Bandwidth = QPS × payload size
   - DB QPS = read QPS × cache-miss rate

3. DEFINE APIS
   - Resources and methods
   - Request/response shape
   - 202 for long-running operations
   - Idempotency keys
   - Cursor pagination
   - Filters and limits
   - Standard errors
   - Authentication and authorization
   - Versioning

4. MODEL DATA
   - Entities
   - Ownership and tenant key
   - Primary keys
   - Status and timestamps
   - Access patterns
   - Five critical indexes
   - Object storage for large payloads

5. DRAW ARCHITECTURE
   - Client
   - Gateway
   - API service
   - Source-of-truth database
   - Cache
   - Queue/workflow engine
   - Workers
   - External dependencies
   - Object storage
   - Observability

6. DEEP DIVE
   - Idempotency
   - State machine
   - Transactions/outbox
   - Retry and timeout
   - Duplicate messages
   - Caching
   - Tenant isolation
   - Security
   - Failure recovery
   - Cost

7. CLOSE
   - Restate guarantees
   - Name the largest bottleneck
   - Explain one major trade-off
   - Mention phase-two improvements
```

## LLD skeleton

```text
1. Use case and responsibility
2. Classes and responsibilities
3. Interfaces and method contracts
4. Main sequence flow
5. Data/state transitions
6. Concurrency and idempotency
7. Failure and edge cases
8. Unit, integration, contract, and concurrency tests
```
