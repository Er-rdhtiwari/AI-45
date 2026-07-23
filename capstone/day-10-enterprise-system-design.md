# Day 10 — Enterprise GenAI system design and Staff-level synthesis

## Outcome

Be able to lead a system-design interview from ambiguous business problem to measurable architecture, explain reliability/security/AI quality, and present ownership and trade-offs at Senior or Staff level.

## 1. Interview design sequence

```text
requirements
→ non-functional requirements
→ capacity
→ APIs
→ data model/access patterns
→ high-level architecture
→ sync/async paths
→ reliability
→ security/governance
→ observability/evaluation
→ cost
→ trade-offs/evolution
```

Do not begin with a fashionable framework. First establish the constraint that requires it.

## 2. Clarify requirements

### Functional

For an enterprise assistant/agent platform:

- upload/synchronize documents;
- ask questions and stream cited answers;
- track conversations;
- execute approved tools;
- inspect run/job status;
- cancel work;
- submit feedback;
- view audit/escalation history.

### Non-functional

Clarify:

- p95 latency/time to first token;
- availability and durability;
- requests and concurrent generations/workflows;
- tenant isolation and data classification;
- freshness and deletion/ACL propagation;
- audit/compliance/retention;
- geography/data residency;
- cost per request/tenant;
- quality and abstention targets;
- recovery objectives.

State MVP and deferred scope to prevent design sprawl.

## 3. Capacity

Only estimate what changes architecture.

```text
average QPS = requests/day ÷ 86,400
peak QPS = average QPS × peak multiplier
concurrency = QPS × average duration
storage growth = objects × size + chunks/vectors + metadata + logs
bandwidth = QPS × payload bytes
```

For AI include:

- input/output tokens;
- embedding volume;
- vector dimensions/metadata;
- active streams/workflows;
- tool calls per run;
- provider quotas;
- background ingestion throughput.

QPS alone is insufficient: a 90-second workflow or streamed generation creates much higher concurrency than a short control-plane request.

State assumptions, calculate orders of magnitude, then derive decisions.

Worked source-note example:

```text
50,000 daily active users × 4 runs/day
= 200,000 runs/day

average QPS
= 200,000 / 86,400
≈ 2.3 starts/second
```

If business-hour traffic peaks at `10×`, design the entry path for roughly `23` starts/second. If a workflow lasts `60` seconds:

```text
active workflows ≈ 23 × 60 ≈ 1,380
```

That result drives queue/worker concurrency, provider quotas, tenant fairness, checkpoint storage, and admission control. Apply the same method to ingestion bytes, tokens, vector storage, and bandwidth, then include indexes, replication, logs, backups, and versioning overhead rather than treating logical payload size as physical storage.

## 4. API contracts

```http
POST /v1/conversations
POST /v1/conversations/{id}/messages
POST /v1/documents/upload-url
POST /v1/documents/{id}/ingestion
GET  /v1/jobs/{id}
POST /v1/projects/{id}/runs
GET  /v1/runs/{id}
POST /v1/runs/{id}/cancellation
POST /v1/runs/{id}/approval
POST /v1/feedback
```

Discuss:

- authentication/authorization;
- idempotency;
- cursor pagination;
- synchronous versus `202` asynchronous;
- timeouts/cancellation;
- streaming events;
- stable errors;
- API/component versions.

## 5. Data model and access patterns

Core entities:

```text
Tenant, User, Project
Conversation, Message
Document, Chunk, IngestionJob
AgentRun, ToolExecution, Approval
Artifact, Feedback, AuditLog, OutboxEvent
```

Every tenant-owned path carries trusted `tenant_id`.

Indexes come from queries:

```text
last project runs:
(tenant_id, project_id, created_at DESC, run_id DESC)

idempotent creation:
(tenant_id, idempotency_key) UNIQUE

audit history:
(tenant_id, created_at DESC, audit_id DESC)
```

Storage:

- relational for transactional state and audit;
- object storage for documents/large artifacts;
- vector/keyword search for evidence;
- Redis for transient/recomputable acceleration;
- registry/MLflow for model/app lifecycle.

## 6. Low-level design deep dive

When asked to deep-dive a component, move from boxes to responsibilities, contracts, sequence, state, concurrency, failure, and tests.

### Responsibility, cohesion, and coupling

- One class should have one clear reason to exist.
- High cohesion keeps related behavior together.
- Low coupling makes business logic depend on capabilities rather than vendors.

Instead of one `AgentManager` that validates, writes SQL, calls models, sends notifications, stores files, and calculates billing, separate:

```text
RunService
RunRepository
WorkflowDispatcher
ToolGateway
ArtifactStore
AuditWriter
```

Inject interfaces such as `RunRepository` and `WorkflowDispatcher`; possible implementations can use different databases, queues, or workflow engines.

### Reusable LLD sequence

1. List the important classes.
2. Give one responsibility per class.
3. Define important methods, inputs, return values, and errors.
4. Show the runtime call sequence.
5. Explain transactions, optimistic concurrency, idempotency, and duplicate messages.
6. Cover invalid input, authorization, dual-write failure, timeouts, cancellation races, and duplicate callbacks.
7. Include unit, repository integration, contract, concurrency, failure-injection, and end-to-end tests.

## 7. High-level enterprise architecture

```text
Web / SDK clients
  ↓
WAF / gateway / load balancer
  ↓
Identity, tenant, rate/admission control
  ↓
Conversation / AgentRun API
  ├─ relational DB + outbox + audit
  ├─ Redis cache/limits
  ├─ AI orchestration
  │    ├─ retrieval service
  │    ├─ model gateway
  │    ├─ tool/policy gateway
  │    └─ approval/checkpoint
  └─ queue or durable workflow engine
       ↓
     workers

Documents → object storage → ingestion workers
          → parse/chunk/embed → vector + keyword index

Logs + metrics + traces + evaluations
```

Separate the interactive request path from ingestion, evaluation, and long-running workflows.

## 8. Enterprise document assistant flow

### Ingestion

```text
connectors
→ change detection and ACL extraction
→ raw storage/catalog
→ parse/quality checks
→ structure-aware chunks
→ metadata/permissions/version
→ embeddings + keyword index
→ golden evaluation
→ publish index
```

Store connector cursor, checksum, source version, ACL version, last indexed timestamp, and deletion tombstone.

### Query

```text
SSO identity/groups
→ authorization scope
→ hybrid retrieval with mandatory ACL filters
→ rerank
→ current authoritative evidence
→ grounded generation
→ citation/schema/safety validation
→ stream
→ trace/feedback
```

Authorization correctness is more important than recall. Unauthorized evidence must never reach the prompt.

## 9. AgentRun execution

### Start

One transaction writes:

```text
AgentRun
OutboxEvent
AuditLog
```

Return `202`. The outbox publisher dispatches work. Consumers assume at-least-once delivery.

### State

```text
QUEUED → RUNNING
RUNNING → WAITING_FOR_TOOL | WAITING_APPROVAL
WAITING_* → RUNNING
RUNNING → SUCCEEDED | FAILED | CANCEL_REQUESTED
CANCEL_REQUESTED → CANCELLED
```

Use optimistic concurrency and immutable terminal states.

### Tool boundary

- allowlist;
- schema and business validation;
- tenant-scoped credentials;
- policy decision;
- approval for writes;
- idempotency key;
- timeout and reconciliation;
- immutable audit.

The model proposes; policy authorizes; business service executes.

## 10. Reliability deep dive

| Failure | Protection |
|---|---|
| API commits but workflow not dispatched | Transactional outbox, retry, stale-run alert, reconciliation. |
| Worker crashes | Durable queue/checkpoint, idempotent resume. |
| Duplicate message/callback | Event ID, unique constraint, state validation. |
| Poison job | Max attempts, backoff, DLQ, replay tooling. |
| Timed-out external write | Persist unknown state and reconcile before retry. |
| Model outage | Timeout, circuit breaker, approved fallback or controlled error. |
| Vector store outage | Fail closed/cached approved result or controlled degradation. |
| Reranker outage | First-stage rank when acceptable. |
| Tenant overload | Quotas, fair queues, concurrency pools, admission control. |
| Bad release | Canary, infrastructure + behavioral gates, rollback. |
| Stale/unauthorized document | Freshness/ACL SLO, reconciliation, deletion propagation. |

Queue plus custom workers is simple but requires custom state, timers, recovery, and versioning. A durable workflow engine fits long-running branches, retries, approval, and resumability at the cost of a new operational model and coupling.

## 11. Security and governance

- Authenticate every entry.
- Derive tenant from trusted identity, not request input.
- Enforce authorization on every DB/search/tool operation.
- Use least-privilege workload/tool credentials.
- Encrypt in transit/at rest.
- Store secrets in a manager.
- Redact/safely sample logs.
- Separate trusted instructions from untrusted content.
- Restrict tool egress and commands/URLs.
- Require clear approval for consequential actions.
- Audit privileged operations.
- Version/approve data, models, prompts, indexes, tools, graphs, and policies.
- Define retention/deletion and incident response.

## 12. Evaluation and observability

### Telemetry layers

Infrastructure:

- resources, queues, restarts, DB/vector/cache latency.

Application:

- rate, errors, p95/p99, retries, timeouts, cache, admission.

AI quality:

- retrieval recall/precision;
- citations/groundedness;
- answer relevance/abstention;
- tool success/trajectory;
- safety/policy;
- tokens/cost.

Business:

- task resolution;
- escalation;
- successful workflows;
- user satisfaction/adoption;
- cost per resolved task.

A deployment is healthy only when infrastructure and AI behavioral metrics are healthy.

## 13. Cost and performance

Measure each stage. Optimize in order:

1. Remove unnecessary model calls.
2. Improve retrieval filters and context quality.
3. Deduplicate context.
4. Route simple work to smaller models.
5. Bound output and tool steps.
6. Batch offline work.
7. Cache safe versioned work.
8. Parallelize independent I/O.
9. Right-size compute and autoscale with useful signals.

Do not trade away retrieval or security quality blindly to lower token cost.

## 14. Architecture trade-offs

| Decision | Option A | Option B | Framing |
|---|---|---|---|
| Modular monolith/microservices | Simple operations | Independent scale/ownership | Split on evidence. |
| Sync/async | Immediate/simple | Durable/buffered | Keep short user path sync; long work async. |
| Shared/dedicated tenant store | Efficient | Strong isolation | Offer tiers by risk. |
| Vector/hybrid | Semantic | Semantic + exact | Use measured enterprise identifier needs. |
| One model/gateway | Simple | Routing/fallback/governance | Abstract when switching/policy is real. |
| Free-form agent/graph | Flexible | Predictable | Bound autonomy around side effects. |
| Queue/durable engine | Low platform overhead | Recovery/state semantics | Match workflow duration/complexity. |
| Rolling/blue-green | Efficient | Fast reversal | Match release and compatibility risk. |
| Managed/self-hosted | Low ops | Control/locality | Compare total cost and governance. |

Staff-level formula:

```text
constraint
→ decision
→ benefit
→ trade-off
→ mitigation
→ metric
→ trigger to revisit
```

## 15. Role and leadership expectations

The IJP role notes emphasize:

- owning problem-to-production lifecycle;
- converting vague business needs into AI solutions;
- architecture decisions and trade-offs;
- data, deployment, monitoring, and governance;
- stakeholder communication;
- mentoring and guidance.

The two role emphases differ:

- The AI/Data Scientist direction emphasizes ML/NLP, foundation models, solution architecture, enterprise AI, and Watson/watsonx awareness.
- The Advanced Analytics/GenAI/Databricks direction emphasizes Databricks, Delta Lake, ETL/ELT, MLflow, RAG/advanced RAG, vector databases, and orchestration frameworks.

At a high level, connect IBM’s Watson/watsonx and Granite awareness to trusted enterprise AI, model development/deployment, lifecycle management, governance, and hybrid-cloud needs. The interview goal is architectural understanding, not memorizing every product feature.

Project story:

```text
problem and users
→ personal scope/ownership
→ constraints
→ architecture
→ two hard decisions
→ failure and systemic fix
→ technical/business impact
→ learning/evolution
```

Be precise about what you owned and influenced. Use measured impact when available; do not invent numbers.

For ambiguity, state assumptions, identify the decision that most changes the architecture, and separate the reversible MVP choice from the production evolution trigger. For speed versus quality, protect non-negotiable security, data integrity, and rollback while staging lower-risk capabilities.

## 16. Mock design prompts

### Multi-tenant RAG SaaS

Cover:

- tenant/ACL enforcement;
- ingestion/freshness/deletion;
- hybrid retrieval/citations;
- token/latency/cost;
- shared versus dedicated index;
- quality gates and feedback.

### Agent platform with tools

Cover:

- tool registry/schema/version/risk;
- state/checkpoints/approval;
- idempotency and unknown outcomes;
- policy and audit;
- step/cost/time limits;
- fair tenancy and provider quotas.

### Enterprise document assistant

Cover:

- connector sync/cursor;
- authoritative sources;
- exact identifiers and hybrid retrieval;
- conflicting versions;
- prompt injection in documents;
- citation/source UX.

### Model-serving platform

Cover:

- batch versus online;
- model registry/alias;
- API versus dedicated serving;
- concurrency/batching;
- canary/champion/rollback;
- drift and business monitoring.

## 17. High-signal interview questions

1. How do you begin a GenAI system-design interview?
2. Why calculate concurrency as well as QPS?
3. What belongs in synchronous versus asynchronous paths?
4. How does the outbox prevent a lost run?
5. Why assume at-least-once delivery?
6. How do you cancel a long-running workflow?
7. SQL versus NoSQL versus cache versus object/vector store?
8. Queue workers versus durable workflow engine?
9. How do you prevent one tenant from consuming all capacity?
10. How do you measure RAG separately from generation?
11. How do you protect against prompt injection and cross-tenant retrieval?
12. How do you deploy a new model/prompt/index safely?
13. What is the largest production risk in an enterprise assistant?
14. How do you present a failure and lesson?
15. What makes an answer Staff-level rather than a component list?
16. How do you move from HLD to an LLD for `RunService`?
17. How do the two IBM IJP role emphases differ?

## 18. Five-to-seven-minute answer skeleton

1. State scope and deferred features.
2. Give measurable NFR assumptions.
3. Estimate QPS, concurrency, storage, and tokens.
4. Define critical APIs.
5. Define entities and access-driven indexes.
6. Draw sync request and async ingestion/workflow paths.
7. Deep-dive one hard problem: outbox, retrieval, tools, or tenancy.
8. Cover failures, security, observability, evaluation, and cost.
9. State trade-offs, bottlenecks, and next evolution trigger.

## 19. Final checklist

- [ ] Clarify users, functions, NFRs, and MVP.
- [ ] Estimate QPS, concurrency, storage, bandwidth, tokens, and background throughput.
- [ ] Define stable APIs, entities, indexes, and storage roles.
- [ ] Draw interactive, ingestion, agent, and deployment paths.
- [ ] Explain outbox, at-least-once, state machines, retries, and reconciliation.
- [ ] Enforce tenant, ACL, tool, secret, and audit boundaries.
- [ ] Measure infrastructure, application, AI quality, and business.
- [ ] State cost/performance choices.
- [ ] Use constraint-to-evolution trade-off language.
- [ ] Deliver both 90-second and seven-minute versions.
- [ ] Deep-dive responsibilities, interfaces, sequence, concurrency, edge cases, and tests.

## Source notes

- [System Design Interview Coaching](<../Python-AI/Day:0 System Design Interview Coaching.md>)
- [IBM IJP Roles Preparation](<../ijp/w01/Day:1 IBM IJP Roles Preparation.md>)
- [Enterprise GenAI Solution Design](<../ijp/w03/Day:21 Enterprise GenAI Solution Design.md>)
- [Cloud AI Architecture](<../ijp/w03/Day:20 Cloud AI Architecture Guide.md>)
- [Deploying ML Models API](<../ijp/w03/Day:19 Deploying ML Models API.md>)
- [MLOps for AI Systems](<../ijp/w03/Day:18 MLOps for AI Systems.md>)
- [Vanilla RAG](<../revision/Day:1 Vanilla RAG.md>)
- [Vanilla RAG and Frameworks](<../revision/Day:6 Vanilla RAG and Frameworks.md>)
- [Capstone Revision Day 3](<../revision/Day:9 Capstone Revision Day 3.md>)
