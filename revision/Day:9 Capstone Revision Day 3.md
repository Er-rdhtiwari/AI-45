# Capstone Revision – Day 3

## 1. Final mental model: how the whole platform fits together

A production GenAI platform is not simply:

> UI → LLM

It is a set of cooperating planes:

```text
Experience plane
  Web/mobile/chat UI, streaming, citations, feedback, admin console
        ↓
API and application plane
  Authentication, tenant context, rate limits, conversations, orchestration
        ↓
Intelligence plane
  RAG, agents, prompts, model routing, tools, guardrails, evaluation
        ↓
Data plane
  PostgreSQL, Redis, object storage, vector index, event queues
        ↓
Platform plane
  Kubernetes, networking, IAM, secrets, autoscaling, managed cloud services
        ↓
Delivery plane
  Git, CI, containers, registry, Helm, deployment promotion
        ↓
Operations and governance plane
  Logs, metrics, traces, cost, security, audit, rollback, incident response
```

### The two flows you must be able to explain

#### A. Software delivery flow

```text
Developer git push
    ↓
Pull request checks
    - lint
    - unit tests
    - type checks
    - security scans
    - RAG/agent regression tests
    ↓
Merge to main
    ↓
Jenkins pipeline
    ↓
Build immutable backend and frontend Docker images
    ↓
Push versioned images to ECR
    ↓
Deploy Helm release to dev
    ↓
Smoke tests + behavioral evaluations
    ↓
Promote the exact same image to stage
    ↓
Approval or policy gate
    ↓
Deploy to production
    ↓
Readiness checks + gradual traffic
    ↓
Observe technical and AI-quality metrics
    ↓
Rollback Helm release or shift traffic if unhealthy
```

ECR provides private Docker/OCI image repositories; Helm packages Kubernetes resources as charts and manages releases through install, upgrade, and rollback operations. ([AWS Documentation][1])

#### B. Runtime request flow

```text
Browser
  ↓ HTTPS
Route53 DNS
  ↓
Application Load Balancer
  ↓
Kubernetes Ingress
  ↓
Frontend or FastAPI Service
  ↓
Authentication + tenant resolution
  ↓
Conversation/orchestration service
  ├─ Redis: cache, quotas, temporary state
  ├─ RDS: tenants, users, conversations, audit
  ├─ Vector DB: retrieve relevant chunks
  ├─ Model provider: generation
  ├─ Tool gateway: approved tool execution
  └─ Queue: ingestion and long-running jobs
  ↓
Stream tokens, citations and status events
  ↓
Store trace, feedback, usage and cost
```

Route 53 alias records can route a domain to an AWS load balancer, while ACM manages TLS certificates and can automatically renew DNS-validated certificates. ([AWS Documentation][2])

### The senior engineer’s design loop

Use this sequence in almost every system design interview:

1. Clarify the user and business problem.
2. Define functional requirements.
3. Define measurable non-functional requirements.
4. Estimate traffic, storage and model usage.
5. Define APIs and data ownership.
6. Draw the simplest architecture that works.
7. Separate synchronous and asynchronous paths.
8. Identify failure modes and security boundaries.
9. Explain scaling, observability and release strategy.
10. State trade-offs, MVP boundaries and future evolution.

A staff-level answer does not merely name technologies. It explains:

* why each component exists;
* what failure it isolates;
* what data it owns;
* how it scales;
* what it costs;
* how it is operated;
* how it could be replaced later.

---

# 2. Topic-by-topic revision notes

## 2.1 Senior-level system design for GenAI products

### Core idea

System design is the process of converting a business requirement into:

* contracts;
* data flows;
* services;
* storage;
* failure boundaries;
* operational guarantees.

For GenAI, you must design both:

* **normal software correctness**: availability, latency, security, consistency;
* **probabilistic AI quality**: grounding, retrieval quality, tool correctness, hallucination rate.

### Requirement clarification

#### Functional requirements

Describe what users can do:

* upload documents;
* ask questions;
* receive streamed answers;
* see citations;
* execute approved tools;
* provide feedback;
* manage tenant settings;
* view conversation history.

#### Non-functional requirements

Make them measurable:

| Requirement  | Good clarification                                         |
| ------------ | ---------------------------------------------------------- |
| Latency      | “Is the target p95 time-to-first-token under two seconds?” |
| Availability | “Do we require 99.9% or 99.99%?”                           |
| Scale        | “How many concurrent streams and requests per second?”     |
| Durability   | “Can conversations or uploaded documents be lost?”         |
| Security     | “Are documents confidential or regulated?”                 |
| Isolation    | “Logical tenant isolation or separate infrastructure?”     |
| Cost         | “Maximum cost per conversation or per tenant?”             |
| Auditability | “Must every retrieval and tool call be traceable?”         |
| Freshness    | “How soon after upload must content become searchable?”    |
| Geography    | “Are there data-residency requirements?”                   |

### Capacity estimation

Use rough numbers, state assumptions and keep moving.

#### Core formulas

```text
Average QPS = requests per day / 86,400

Peak QPS = average QPS × peak multiplier

Daily storage growth =
  objects per day × average object size
  + chunks × embedding size
  + metadata
  + logs/traces

Bandwidth per second =
  QPS × average response bytes

Concurrent requests =
  QPS × average request duration
```

#### Example

Assume:

* 100,000 daily active users;
* 10 questions per user per day;
* 1,000,000 questions per day;
* average model request lasts 8 seconds;
* peak multiplier is 5.

```text
Average QPS = 1,000,000 / 86,400 ≈ 11.6

Peak QPS ≈ 58

Peak concurrent generations ≈ 58 × 8 = 464
```

This tells you that you may need roughly 464 simultaneous generation streams, not merely 58 application threads.

For external model APIs, also estimate:

```text
Daily model tokens =
  requests × average input tokens
  + requests × average output tokens

Daily model cost =
  input tokens × input price
  + output tokens × output price
```

### API contracts

Typical APIs:

```http
POST /v1/conversations
POST /v1/conversations/{conversation_id}/messages
GET  /v1/conversations/{conversation_id}
POST /v1/documents/upload-url
POST /v1/documents/{document_id}/ingest
GET  /v1/jobs/{job_id}
POST /v1/feedback
```

For streamed answers, use:

* Server-Sent Events for simple server-to-browser streaming;
* WebSockets when bidirectional real-time messaging is required.

A streamed event contract might contain:

```json
{
  "event": "citation",
  "request_id": "req_123",
  "data": {
    "document_id": "doc_45",
    "chunk_id": "chunk_9",
    "title": "Refund Policy"
  }
}
```

Good API contracts include:

* request IDs;
* tenant context;
* idempotency keys;
* explicit error codes;
* pagination;
* versioning;
* timeouts;
* cancellation;
* job status for asynchronous work.

### Data model thinking

Core entities:

```text
Tenant
  tenant_id, plan, quotas, settings

User
  user_id, tenant_id, role

Conversation
  conversation_id, tenant_id, user_id, created_at

Message
  message_id, conversation_id, role, content, model, token_usage

Document
  document_id, tenant_id, object_key, status, checksum, version

Chunk
  chunk_id, document_id, tenant_id, content_hash, metadata

IngestionJob
  job_id, document_id, status, retry_count, error

ToolExecution
  execution_id, tenant_id, tool, arguments_hash, approval, result

Feedback
  feedback_id, message_id, rating, reason
```

Every tenant-owned table should normally include `tenant_id`, and important access paths should have composite indexes such as:

```text
(tenant_id, conversation_id)
(tenant_id, created_at)
(tenant_id, document_id)
```

### High-level architecture

Separate responsibilities:

```text
API gateway / ingress
  ↓
Identity and tenant service
  ↓
Conversation API
  ↓
AI orchestration service
  ├─ retrieval service
  ├─ model gateway
  ├─ tool gateway
  ├─ safety service
  └─ evaluation/telemetry hooks
```

Avoid creating microservices for every logical function on day one. Split when you need:

* independent scaling;
* separate ownership;
* strong isolation;
* different release cadence;
* different runtime requirements.

### Synchronous versus asynchronous paths

**Synchronous**

* authentication;
* retrieval;
* prompt assembly;
* model generation;
* short tool calls;
* streaming response.

**Asynchronous**

* document parsing;
* OCR;
* chunking and embedding;
* large report generation;
* offline evaluation;
* analytics aggregation;
* data deletion;
* retryable connector synchronization.

Use queues when work:

* may outlive the HTTP request;
* needs retries;
* has bursty traffic;
* should be rate-controlled;
* is resource-intensive.

### Reliability patterns

| Pattern              | Purpose                           | GenAI example                            |
| -------------------- | --------------------------------- | ---------------------------------------- |
| Timeout              | Prevent indefinite waiting        | Stop a slow model or tool request        |
| Retry                | Recover from transient failure    | Retry a throttled embedding call         |
| Exponential backoff  | Avoid retry storms                | Increase delay after each 429            |
| Jitter               | Desynchronize clients             | Randomize retry delay                    |
| Circuit breaker      | Stop calling a failing dependency | Temporarily disable one model provider   |
| Bulkhead             | Isolate resource pools            | Separate ingestion and chat workers      |
| Backpressure         | Slow intake when capacity is full | Limit queue depth or active generations  |
| Admission control    | Reject excess work early          | Return 429 when tenant quota is exceeded |
| Idempotency          | Prevent duplicate side effects    | Avoid embedding a document twice         |
| Dead-letter queue    | Preserve repeatedly failing jobs  | Store unprocessable documents            |
| Graceful degradation | Preserve core functionality       | Use keyword retrieval if reranker fails  |

### Fault tolerance

Design for failure at every boundary:

* Model unavailable → fallback model or controlled error.
* Vector database unavailable → cached answer or fail closed.
* Reranker unavailable → use first-stage ranking.
* Redis unavailable → database-backed limits or conservative rejection.
* Worker crashes → queue message becomes visible again.
* Pod crashes → readiness removes it from traffic.
* New release fails → rollback to previous image and configuration.

Kubernetes readiness controls whether a pod receives service traffic; liveness can restart unhealthy containers. HPA adjusts replicas according to observed metrics. ([Kubernetes][3])

### Observability

Use three telemetry layers.

#### Infrastructure telemetry

* CPU and memory;
* pod restarts;
* queue depth;
* connection pools;
* database latency;
* network errors.

#### Application telemetry

* request rate;
* error rate;
* p50/p95/p99 latency;
* dependency latency;
* cache hit rate;
* timeout and retry count.

#### AI-quality telemetry

* retrieval recall proxies;
* citation coverage;
* groundedness;
* answer relevance;
* tool success rate;
* fallback rate;
* input/output tokens;
* cost per request;
* user feedback;
* policy violations.

Trace one request across:

```text
request → retrieval → reranking → prompt → model → tools → response
```

### Release safety

Production promotion should require:

* normal unit and integration tests;
* prompt/template versioning;
* golden question evaluation;
* tool-call regression tests;
* schema compatibility;
* canary or gradual rollout;
* health and quality gates;
* an explicit rollback target.

### Product thinking

Technical metrics answer:

> Is the system healthy?

Business metrics answer:

> Is it useful?

Examples:

| Technical         | Business                              |
| ----------------- | ------------------------------------- |
| p95 latency       | Task completion rate                  |
| 5xx rate          | Weekly active users                   |
| retrieval latency | Questions resolved without escalation |
| token cost        | Cost per resolved case                |
| tool failure rate | Successful workflows completed        |
| uptime            | Retention and satisfaction            |

### Trade-offs

* Strict latency target versus answer quality.
* Large context versus token cost.
* Strong isolation versus infrastructure cost.
* Synchronous simplicity versus queue-based resilience.
* Managed services versus control.
* Microservices versus operational overhead.

### Common mistakes

* Designing before clarifying users and scale.
* Ignoring model concurrency and rate limits.
* Calling every component a microservice.
* No tenant ID in data paths.
* Treating retries as unlimited.
* Measuring only API latency, not AI quality.
* No rollback or evaluation gate.
* Assuming the LLM is the source of truth.

### What a senior engineer should say

> “I would first define the user-visible SLOs, isolation requirements and cost envelope. Then I would separate the low-latency conversational path from asynchronous ingestion. I would make model, retrieval and tool dependencies replaceable behind interfaces, and I would treat AI quality metrics as release signals alongside normal reliability metrics.”

---

## 2.2 Productization and UI thinking

### Core idea

An AI capability becomes a product only when users can:

* understand what it can do;
* control it;
* trust its output;
* recover from errors;
* provide feedback.

### Architecture relevance

The UI contract influences backend architecture:

* streaming requires incremental events;
* citations require provenance metadata;
* cancellation requires cancellable backend tasks;
* retries require idempotent requests;
* uploads require secure object transfer;
* agent status requires tool-progress events.

### Chat UI component model

```text
ChatPage
  ├─ ConversationSidebar
  ├─ MessageList
  │    ├─ UserMessage
  │    ├─ AssistantMessage
  │    ├─ CitationList
  │    └─ ToolExecutionCard
  ├─ Composer
  │    ├─ TextInput
  │    ├─ FileAttachment
  │    └─ ModelSelector
  └─ FeedbackControls
```

### Streaming responses

The frontend should represent explicit states:

```text
idle
submitting
retrieving
generating
executing_tool
completed
failed
cancelled
```

Do not show an endlessly spinning loader. Display useful progress:

* “Searching approved documents…”
* “Reviewing three sources…”
* “Waiting for finance system approval…”
* “The model provider timed out. Retry?”

### Citations and trust

A citation should contain:

* source title;
* relevant excerpt;
* document version;
* location or page;
* access timestamp;
* clickable source where authorized.

Avoid presenting a citation merely because a document was retrieved. A stronger approach maps answer claims to source chunks.

### Feedback collection

Collect structured signals:

* thumbs up/down;
* incorrect answer;
* wrong source;
* outdated information;
* unsafe response;
* tool did not work;
* free-text explanation.

Attach feedback to:

* request ID;
* prompt version;
* model version;
* retrieved chunks;
* tool traces;
* tenant;
* latency and cost.

### Streamlit and Gradio

Use them for:

* internal demos;
* rapid experiments;
* stakeholder validation;
* model comparisons.

Do not automatically treat a demo UI as production architecture. Production may require:

* enterprise authentication;
* accessibility;
* audit;
* robust state management;
* scalable streaming;
* tenant administration;
* observability.

### Multi-model playground

Useful capabilities:

* same prompt sent to several models;
* side-by-side latency and cost;
* retrieval configuration comparison;
* prompt version comparison;
* human preference selection;
* hidden randomized evaluation.

### Designing errors

Good error:

> “The answer could not be completed because the CRM tool timed out. No changes were made. Retry the CRM step?”

Bad error:

> “Agent failed: status 500.”

### Best practices

* Show sources near the relevant claim.
* Distinguish model text from confirmed tool results.
* Support stop and retry.
* Preserve the user’s input after failure.
* Explain when a response is incomplete.
* Require confirmation for consequential actions.
* Display model/tool limitations where relevant.

### Trade-offs

* Detailed agent progress versus UI complexity.
* Transparent reasoning metadata versus information leakage.
* Immediate token streaming versus moderation before display.
* Many settings versus simple usability.

### Common mistakes

* Building only a text box and output area.
* Hiding tool failures.
* Showing fake certainty.
* No accessible citation view.
* No loading, cancellation or retry states.
* Passing cloud credentials to the browser.

### What a senior engineer should say

> “For AI UX, trust is part of architecture. The backend must emit provenance, tool state and recoverable error events—not merely tokens. I would design the event contract and failure states before polishing the visual interface.”

---

## 2.3 Terraform and infrastructure as code

### Core idea

**Imperative**

> Run these commands in this order.

**Declarative**

> This is the desired infrastructure state.

Terraform compares declared configuration with real infrastructure and produces an execution plan. ([HashiCorp Developer][4])

### HCL building blocks

```hcl
variable "environment" {
  type = string
}

locals {
  name_prefix = "genai-${var.environment}"
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "documents" {
  bucket = "${local.name_prefix}-documents"
}

output "document_bucket_name" {
  value = aws_s3_bucket.documents.bucket
}
```

* `resource`: infrastructure Terraform manages.
* `data`: existing information Terraform reads.
* `variable`: configurable input.
* `locals`: reusable derived values.
* `output`: exposed result.

### Lifecycle

```text
terraform init
  Initialize providers, modules and backend.

terraform plan
  Preview intended changes.

terraform apply
  Execute approved changes.

terraform destroy
  Remove managed infrastructure.
```

Production pipelines should save and apply an reviewed plan rather than running an uncontrolled apply.

### State file

Terraform state maps configuration addresses to real resources.

It can contain sensitive values and must not be treated as harmless text.

#### Remote state

Use a remote backend for team environments because it provides:

* shared state;
* access control;
* durability;
* locking;
* auditability.

#### Important current note

The historically common AWS pattern was:

```text
S3 = remote state storage
DynamoDB = state lock
```

Modern Terraform S3 backends support native S3 lockfiles with `use_lockfile`; DynamoDB-based locking is deprecated. You should understand the older pattern for existing systems but propose native S3 locking for new designs unless organizational constraints require otherwise. ([developer.hashicorp.com][5])

### Drift

Drift occurs when real infrastructure changes outside Terraform.

Examples:

* someone edits a security group in the console;
* a deployment script changes a resource;
* another stack owns the same resource.

Response:

* detect through `plan`;
* decide whether the manual change is valid;
* update code or revert infrastructure;
* reduce unnecessary console access.

### Modules

```text
infra/
  modules/
    vpc/
    eks/
    rds/
    application/
  environments/
    dev/
    stage/
    prod/
```

* **Child module:** reusable unit such as VPC or RDS.
* **Root module:** environment-specific composition that is applied.

Good module boundaries represent stable infrastructure capabilities, not individual resources.

### Environment strategy

Prefer separate state and usually separate AWS accounts for meaningful isolation:

```text
dev account/state
stage account/state
prod account/state
```

#### Workspaces versus separate state

**Workspaces**

* convenient for similar ephemeral environments;
* easy to reuse configuration;
* weaker visible isolation;
* mistakes may target the wrong workspace.

**Separate roots/state**

* stronger isolation;
* clearer permissions;
* easier production governance;
* some duplication.

Staff-level default:

> Use separate state—and preferably separate accounts—for production boundaries. Use workspaces for genuinely equivalent, lower-risk instances.

### Naming conventions

Example:

```text
<organization>-<product>-<environment>-<region>-<resource>
acme-genai-prod-ap-south-1-documents
```

Also use mandatory tags:

* owner;
* environment;
* application;
* cost center;
* data classification;
* managed-by.

### Terraform responsibilities in this platform

Terraform creates:

* VPC and subnets;
* route tables, gateways and endpoints;
* EKS cluster and node capacity;
* RDS;
* Redis/ElastiCache;
* S3;
* ECR;
* IAM roles and policies;
* Route 53 records;
* ACM certificates;
* monitoring integration.

Terraform should not normally own every Kubernetes application object if Helm already owns those releases. Clear ownership prevents conflicts.

### DNS, certificates and routing

```text
Route53 record
   ↓
ALB DNS endpoint
   ↓
ACM certificate terminates HTTPS
   ↓
Ingress rule
   ↓
Kubernetes Service
```

Route 53 alias records support routing to AWS resources including load balancers, while ACM DNS validation supports ongoing certificate renewal. ([AWS Documentation][6])

### Best practices

* Pin provider and module versions.
* Review plans in CI.
* Encrypt remote state.
* Restrict state access.
* Separate states by blast radius.
* Avoid manual production changes.
* Use modules for stable reuse.
* Add policy and security checks.
* Avoid putting secrets directly in variables or outputs.

### Trade-offs

* Generic modules versus understandable modules.
* One large state versus many small states.
* Reuse versus environment-specific clarity.
* Full automation versus high-risk approval gates.

### Common mistakes

* One state file for the entire company.
* Committing state or credentials.
* Applying from developer laptops to production.
* Circular module dependencies.
* Overusing workspaces for security isolation.
* Terraform and Helm both managing the same resource.
* Using deprecated locking patterns without recognizing them.

### What a senior engineer should say

> “I structure Terraform state around blast radius and ownership. Network, shared platform and application infrastructure may have separate states and permissions. Production applies use reviewed plans, remote locking and constrained CI roles.”

---

## 2.4 AWS infrastructure for GenAI platforms

### VPC mental model

A VPC is a private network boundary.

```text
VPC: 10.0.0.0/16
  ├─ Public subnet AZ-A
  │    ALB, NAT Gateway
  ├─ Public subnet AZ-B
  │    ALB, NAT Gateway
  ├─ Private app subnet AZ-A
  │    EKS nodes/pods
  ├─ Private app subnet AZ-B
  │    EKS nodes/pods
  ├─ Private data subnet AZ-A
  │    RDS/Redis
  └─ Private data subnet AZ-B
       RDS/Redis
```

A public subnet has a route to an Internet Gateway. Private workloads can initiate outbound IPv4 connections through a NAT Gateway without accepting unsolicited inbound internet traffic. AWS recommends multi-AZ patterns for resiliency. ([AWS Documentation][7])

### CIDR

`10.0.0.0/16` provides a network range that can be divided into subnets.

Avoid overlapping CIDRs if you expect:

* VPC peering;
* VPN;
* transit gateway;
* on-premises connectivity.

### Security groups versus NACLs

**Security group**

* attached to resources/network interfaces;
* stateful;
* primary application firewall.

**Network ACL**

* attached to a subnet;
* stateless;
* optional additional boundary.

AWS documentation notes that security groups are generally sufficient for most needs, while NACLs can provide another subnet-level control layer. ([AWS Documentation][8])

### EKS

```text
AWS-managed Kubernetes control plane
        ↓
Managed node groups / dynamic compute
        ↓
Pods running backend, frontend and workers
```

EKS manages the Kubernetes control plane. Managed node groups automate EC2 node provisioning and lifecycle management. ([AWS Documentation][9])

#### Autoscaling layers

* **HPA:** changes pod replica count.
* **Node autoscaling:** adds/removes compute nodes.
* **Application concurrency limits:** protects model and database dependencies.

Do not assume more pods always increase throughput. External model rate limits may be the actual bottleneck.

### ALB ingress integration

```text
Internet
  ↓
ALB
  ↓
Kubernetes Ingress rules
  ↓
Service
  ↓
Ready pods
```

The AWS Load Balancer Controller can create AWS load balancers from Kubernetes Service or Ingress resources. ([AWS Documentation][10])

### RDS

Use RDS/PostgreSQL for:

* tenants;
* identities and entitlements;
* conversations;
* document metadata;
* ingestion state;
* tool approvals;
* billing and usage records;
* audit data.

Production databases should normally be private and use Multi-AZ where availability requirements justify it. RDS DB subnet groups span multiple Availability Zones, and Multi-AZ deployments provide failover support. ([AWS Documentation][11])

### Redis/ElastiCache

Use Redis for transient or recomputable data:

* response cache;
* semantic cache;
* distributed rate limits;
* session state;
* short-lived checkpoints;
* locks;
* deduplication;
* streaming event state.

Do not make Redis the sole durable store for critical conversations or approvals.

### S3

Use S3 for:

* original documents;
* parsed artifacts;
* exports;
* evaluation datasets;
* model outputs;
* logs and backups where appropriate.

For browser uploads:

```text
Browser requests upload permission
  ↓
Backend authenticates tenant and creates object key
  ↓
Backend returns short-lived presigned URL
  ↓
Browser uploads directly to S3
  ↓
Object event starts ingestion
```

A presigned URL grants time-limited access without giving the browser AWS credentials, but it carries the permissions of the principal that created it and must be scoped carefully. ([AWS Documentation][12])

### ECR

Use ECR for immutable application images:

```text
backend:git-sha
frontend:git-sha
worker:git-sha
```

Avoid relying only on mutable tags such as `latest`. ECR stores private Docker and OCI images and supports normal push/pull workflows. ([AWS Documentation][1])

### IAM

Separate roles for:

* Jenkins deployment;
* Terraform provisioning;
* backend pods;
* ingestion workers;
* frontend;
* human operators.

Use pod-specific roles rather than broad node permissions. EKS pod identities or IAM roles for service accounts allow permissions to be scoped to the Kubernetes service account used by a pod. ([AWS Documentation][13])

### Placement

**Public**

* ALB;
* optionally NAT Gateway.

**Private application subnets**

* EKS nodes/pods;
* worker services.

**Private data subnets**

* RDS;
* Redis;
* private vector database.

### Best practices

* Multi-AZ deployment.
* Private databases.
* Least-privilege pod roles.
* VPC endpoints for frequently used AWS services where beneficial.
* Encrypt traffic and storage.
* Separate tenant authorization from network location.
* Restrict egress where feasible.
* Centralize audit logs.

### Trade-offs

* NAT Gateway convenience versus cost.
* EKS flexibility versus operational complexity.
* Managed vector database versus self-hosted control.
* Multi-AZ reliability versus cost.
* Shared cluster efficiency versus stronger environment isolation.

### Common mistakes

* Publicly accessible databases.
* Broad `*:*` IAM policies.
* One security group for everything.
* Giving AWS credentials to the frontend.
* No cross-AZ resilience.
* Scaling pods without scaling nodes.
* Ignoring NAT and cross-zone data-transfer costs.

### What a senior engineer should say

> “Only the load balancer is internet-facing. Application and data workloads remain private. Workloads obtain temporary, least-privilege AWS permissions through pod identities rather than static credentials.”

---

## 2.5 Kubernetes and Helm

### Kubernetes objects

#### Pod

Smallest runnable unit. Usually contains one primary application container and optional sidecars.

#### Deployment

Maintains desired replicas and manages rolling updates for stateless workloads.

#### Service

Provides a stable network identity for a changing set of pods.

#### Ingress

Maps HTTP/HTTPS hosts and paths to services. Kubernetes defines Ingress as an API for external HTTP access and routing to backends. ([Kubernetes][14])

#### ConfigMap

Non-secret configuration.

#### Secret

Sensitive configuration object, although production environments should integrate with an external secret manager and encryption controls.

#### HPA

Scales workload replica count using resource or custom metrics. ([Kubernetes][3])

### Probe meanings

* **Startup:** Has the slow-starting process initialized?
* **Readiness:** Should it receive traffic?
* **Liveness:** Is it stuck and should it restart?

For a GenAI service:

```text
/startup
  application loaded and configuration validated

/ready
  event loop responsive and required local resources initialized

/live
  process is not deadlocked
```

Do not make liveness depend on every external provider. A temporary model outage should not restart all pods.

### Why Kubernetes for GenAI

Useful when you need:

* multiple independently scaled services;
* standardized deployment;
* autoscaling;
* workload isolation;
* rolling releases;
* scheduled/background jobs;
* configurable CPU/GPU pools;
* platform-level observability.

It may be excessive for a small product with one API and low traffic.

### Helm

A chart is a package of related Kubernetes resources. ([Helm][15])

```text
charts/genai-app/
  Chart.yaml
  values.yaml
  templates/
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    configmap.yaml
```

#### Concepts

* **Chart:** deployable package.
* **Template:** parameterized Kubernetes manifest.
* **Values:** environment configuration.
* **Release:** installed instance of a chart.

#### Commands

```bash
helm install genai ./chart
helm upgrade genai ./chart
helm rollback genai 12
```

Helm’s official tooling supports installing charts, upgrading releases and rolling back failed changes. ([Helm][16])

### Backend deployment

```text
FastAPI Deployment
  replicas: 4
  resources: requests/limits
  readiness probe
  service account with model/S3 permissions
  HPA based on CPU plus active-request metric
  PodDisruptionBudget
  Service
```

Workers should usually have a separate Deployment because:

* different scaling metric;
* different concurrency;
* different resource profile;
* failures do not consume API capacity.

### Frontend deployment

For a static React app:

* build assets;
* host through object storage/CDN or lightweight web container.

For Next.js server features:

* run Node.js pods;
* use readiness probes;
* cache appropriately;
* separate browser-visible and server-only environment variables.

### Environment-specific values

```text
values.yaml
values-dev.yaml
values-stage.yaml
values-prod.yaml
```

Change:

* replicas;
* resource requests;
* domains;
* external endpoints;
* autoscaling thresholds;
* logging level.

Do not store secrets in values files committed to Git.

### Rolling update versus blue/green

**Rolling update**

* gradually replaces pods;
* efficient;
* standard Kubernetes behavior;
* old and new versions coexist temporarily.

**Blue/green**

* two full environments;
* rapid traffic switch;
* easier immediate reversal;
* higher cost and data compatibility complexity.

### Common GenAI Kubernetes pitfalls

* No CPU/memory requests.
* HPA based only on CPU for I/O-bound services.
* Long requests terminated during rollout.
* No graceful shutdown.
* Liveness calling external model APIs.
* API and ingestion workers sharing one deployment.
* Unlimited in-process concurrency.
* Mutable image tags.
* Prompt or configuration changes not versioned.
* Secrets stored in ConfigMaps.

### What a senior engineer should say

> “I scale the API, ingestion and tool workers independently. Readiness protects traffic, graceful shutdown drains active streams, and HPA uses a workload-relevant signal such as concurrent generations or queue depth—not only CPU.”

---

## 2.6 Jenkins CI/CD

### Architecture

```text
Jenkins controller
  - schedules jobs
  - stores pipeline configuration and metadata
       ↓
Jenkins agents
  - execute lint, tests, builds and deployments
```

Keep heavy builds off the controller.

### Pipeline as code

Store a `Jenkinsfile` with the application. Jenkins supports declarative pipelines inside a `pipeline` block and pipeline definitions stored in source control. ([Jenkins][17])

### Typical pipeline

```groovy
pipeline {
  agent any

  stages {
    stage('Lint') {
      steps { sh 'make lint' }
    }

    stage('Unit Test') {
      steps { sh 'make test-unit' }
    }

    stage('AI Regression') {
      steps { sh 'make test-rag-golden' }
    }

    stage('Build') {
      steps { sh 'make docker-build' }
    }

    stage('Push') {
      steps { sh 'make ecr-push' }
    }

    stage('Deploy Dev') {
      steps { sh 'make helm-deploy ENV=dev' }
    }

    stage('Smoke Test') {
      steps { sh 'make smoke-test ENV=dev' }
    }
  }
}
```

### Pipeline stages

1. Checkout.
2. Dependency validation.
3. Lint and formatting.
4. Type checking.
5. Unit tests.
6. Integration tests.
7. Secret and vulnerability scans.
8. Golden AI evaluations.
9. Build images.
10. Push immutable images.
11. Deploy.
12. Smoke test.
13. Promote.
14. Verify.
15. Rollback if necessary.

### Docker images

Backend:

* slim base image;
* pinned dependencies;
* non-root user;
* health endpoint;
* minimal build context.

Frontend:

* multi-stage build;
* compile assets separately;
* run minimal production server;
* never bake secrets into browser bundles.

### Credentials

Use Jenkins credential bindings or workload identity, not plaintext environment files in Git. Jenkins supports credential helpers for secret text, username/password and secret files. ([Jenkins][18])

### Promotion

Build once:

```text
image digest sha256:abc...
```

Then promote the same digest:

```text
dev → stage → prod
```

Do not rebuild for production. A rebuild may introduce different dependencies.

### Smoke tests

Examples:

* `/health` returns success;
* create conversation;
* retrieve a known document;
* stream first token;
* verify citation schema;
* perform a read-only test tool call;
* validate no unexpected policy violation.

### Rollback

Rollback triggers:

* readiness failure;
* 5xx increase;
* p95 degradation;
* retrieval quality regression;
* tool failures;
* cost spike.

Mechanisms:

* `helm rollback`;
* traffic shift to previous blue/green environment;
* revert feature flag;
* disable affected model/tool.

### GenAI-specific CI checks

#### Golden RAG test

For a fixed dataset:

```text
question
expected source IDs
required answer facts
forbidden unsupported facts
```

Measure:

* retrieval hit rate;
* citation correctness;
* groundedness;
* answer completeness.

#### Behavioral tests

Examples:

* refuses disallowed actions;
* asks for approval before write tools;
* never accesses another tenant’s documents;
* follows tool schemas;
* handles empty retrieval;
* does not reveal system instructions.

### Trade-offs

* Fast pipeline versus broad evaluation.
* Deterministic checks versus model variability.
* Shared Jenkins agents versus isolation.
* Manual approval versus delivery speed.

### Common mistakes

* Static cloud credentials on agents.
* Building with `latest`.
* No AI regression tests.
* Rebuilding between environments.
* Deployment considered successful before smoke testing.
* Rollback dependent on a new build.
* Production deploy from a developer laptop.

### What a senior engineer should say

> “The artifact is built once, identified by digest, evaluated, and promoted unchanged. Deployment success means both infrastructure health and AI behavioral health meet their gates.”

---

## 2.7 Ansible and operations automation

### Terraform versus Ansible

```text
Terraform:
  Create infrastructure resources and relationships.

Ansible:
  Configure machines and operational software.
```

Examples:

**Terraform**

* EC2 instance;
* VPC;
* EKS;
* IAM role;
* RDS.

**Ansible**

* install Docker;
* configure Jenkins agent;
* install `kubectl`, Helm and AWS CLI;
* deploy monitoring configuration;
* harden bastion hosts.

### Core concepts

* **Inventory:** managed hosts and groups.
* **Playbook:** desired operational workflow.
* **Task:** one action.
* **Module:** reusable unit that performs an operation.
* **Handler:** action triggered by a change, often restart/reload.
* **Role:** reusable structure of tasks, handlers, variables and templates.
* **Vault:** encrypted storage mechanism for sensitive Ansible data.

Ansible defines inventory as managed nodes and groups. Its modules aim for idempotence: repeated execution should produce the same final state rather than repeat unnecessary changes. ([Ansible Documentation][19])

### Example

```yaml
- name: Configure Jenkins agents
  hosts: jenkins_agents
  become: true

  tasks:
    - name: Install Docker
      ansible.builtin.apt:
        name: docker.io
        state: present
        update_cache: true

    - name: Ensure Docker is running
      ansible.builtin.service:
        name: docker
        state: started
        enabled: true
```

Prefer modules to raw shell because modules:

* understand desired state;
* provide structured output;
* support idempotence;
* handle platform differences better.

### Operational use cases

* bootstrap Jenkins agents;
* configure bastions;
* install debugging tools;
* rotate configuration;
* manage certificates on non-managed infrastructure;
* install log collectors;
* standardize developer VMs;
* repair drift on traditional hosts.

### Trade-offs

* Agentless simplicity versus SSH/network dependency.
* Flexible automation versus YAML complexity.
* Vault convenience versus dedicated secret-management systems.
* Ansible-managed servers versus immutable replacement.

### Common mistakes

* Using Ansible to recreate Terraform.
* Heavy use of `shell` commands.
* Non-idempotent playbooks.
* Secrets committed unencrypted.
* No role structure.
* Configuring short-lived Kubernetes pods with Ansible.

### What a senior engineer should say

> “Terraform provisions durable cloud resources; Ansible configures host-level software where immutable images or managed services do not solve the problem. I avoid overlapping ownership.”

---

## 2.8 Frontend for GenAI systems

### React versus Next.js

**React**

* UI library;
* client-side component model;
* flexible build and routing choices.

**Next.js**

* framework around React;
* routing, server rendering and server components;
* backend-for-frontend capabilities;
* optimized deployment conventions.

Current Next.js uses Server Components by default for layouts and pages, while Client Components are used for state, event handlers and browser APIs. ([Next.js][20])

### Component architecture

```text
app/
  chat/
    page.tsx
  components/
    ChatShell.tsx
    MessageList.tsx
    Message.tsx
    CitationDrawer.tsx
    ToolStatus.tsx
    Composer.tsx
    UploadDialog.tsx
    FeedbackButtons.tsx
```

### State management

Separate:

* server state: conversations, messages, sources;
* UI state: open drawer, selected citation;
* streaming state: active partial message;
* authentication state;
* tenant configuration.

Avoid placing everything in one global store.

### Backend API calls

The browser should communicate with:

* the application backend;
* directly with S3 only using scoped presigned URLs.

The browser should not communicate directly with:

* databases;
* Redis;
* privileged cloud APIs;
* internal tool services.

### Streaming UX

Use incremental events:

```text
message_started
retrieval_started
sources_found
token
tool_started
tool_completed
message_completed
error
```

The client should tolerate:

* duplicated events;
* reconnects;
* partial messages;
* out-of-order status updates where possible.

### Signed uploads

```text
1. Browser requests upload URL.
2. Backend validates tenant, size and file type.
3. Backend returns object key and presigned URL.
4. Browser uploads to S3.
5. Backend or S3 event starts ingestion.
6. UI polls or subscribes to job status.
```

### Trust and safety UX

Display:

* “AI-generated” where appropriate;
* citations;
* uncertainty or incomplete result;
* tool actions separately from suggestions;
* approval dialogs;
* reporting controls;
* safety warnings without overwhelming the user.

### Best practices

* Accessible keyboard navigation.
* Responsive streaming.
* Abort controls.
* Error boundaries.
* Preserved drafts.
* Clear source provenance.
* No hidden write actions.
* Secure cookie/session handling.
* Tenant-aware routing.

### Trade-offs

* Server rendering versus client complexity.
* Rich progress events versus protocol complexity.
* Optimistic UI versus correctness for consequential actions.
* Local conversation cache versus privacy.

### Common mistakes

* Rendering raw model HTML.
* Exposing server-only secrets.
* Mixing partial and final messages incorrectly.
* No cancellation.
* No file validation.
* Trusting the tenant ID sent by the client.
* Displaying retrieved sources as proof even when not used.

### What a senior engineer should say

> “The frontend supplies user intent, never authorization truth. Tenant and permission checks happen server-side. Streaming uses a versioned event protocol rather than concatenating arbitrary strings.”

---

## 2.9 Monorepo, environment strategy and developer experience

### Suggested layout

```text
genai-platform/
  apps/
    backend/
    frontend/
    ingestion-worker/
    evaluation-service/
  packages/
    python/
      domain-models/
      llm-clients/
      observability/
    typescript/
      api-types/
      ui-components/
  infra/
    terraform/
      modules/
      environments/
    helm/
      genai-platform/
    ansible/
  tests/
    integration/
    smoke/
    evaluations/
  docs/
    architecture/
    runbooks/
    onboarding/
  Jenkinsfile
  Makefile
```

### Benefits

* atomic cross-stack changes;
* shared contracts;
* centralized tooling;
* easier discovery;
* one PR can update backend, UI and infrastructure.

### Costs

* larger checkout;
* CI complexity;
* unclear ownership without boundaries;
* accidental coupling;
* broader permissions.

### Environment configuration

```text
Local:
  .env.local, mocks, Docker Compose

Dev:
  shared non-production services

Stage:
  production-like topology and controls

Prod:
  separate state, secrets, accounts and strict permissions
```

#### Environment variables

Local `.env`:

* developer-only;
* never committed if sensitive.

Production:

* secret manager;
* workload identity;
* injected at runtime;
* audited and rotated.

### State/configuration alignment

```text
Terraform state:
  dev / stage / prod separated

Helm values:
  values-dev / values-stage / values-prod

Secrets:
  distinct per environment

Domains:
  dev.example.com
  stage.example.com
  app.example.com
```

### Local development

A good workflow:

```bash
make bootstrap
make dev
make test
make eval
make lint
```

Use local substitutes:

* local PostgreSQL;
* local Redis;
* mock model provider;
* fake tool server;
* small vector store;
* deterministic test embeddings where useful.

### Branch strategy

A practical approach:

* short-lived feature branches;
* mandatory PR;
* protected main;
* automated checks;
* frequent merges;
* release tags;
* feature flags for incomplete functionality.

Long-lived environment branches often drift and create painful merges.

### Testing layers

#### Unit

Fast, isolated:

* chunking logic;
* tenant filters;
* prompt assembly;
* tool argument validation.

#### Integration

Real interfaces:

* API + database;
* worker + queue;
* retriever + vector store;
* auth + tenant policy.

#### Smoke

Deployed system:

* login;
* one known query;
* one citation;
* one upload;
* one tool action.

#### Evaluation

AI behavior:

* retrieval;
* groundedness;
* safety;
* tool selection;
* cost and latency.

### Developer experience

A staff engineer treats developer productivity as a platform requirement.

Provide:

* one-command local startup;
* documented service ownership;
* example requests;
* generated API clients;
* pre-commit checks;
* fast unit tests;
* seeded test data;
* architecture decision records;
* runbooks;
* dashboards linked from documentation.

### Common mistakes

* Shared production credentials for developers.
* Unclear source of configuration truth.
* Copy-pasted API models between Python and TypeScript.
* CI runs every test for every small change.
* No local model/tool mocks.
* Onboarding depends on tribal knowledge.
* Infrastructure changes cannot be tested before merge.

### What a senior engineer should say

> “DevEx is an operational multiplier. A reproducible local environment, contract generation and selective CI reduce cycle time and production configuration drift.”

---

## 2.10 Full end-to-end integration story

### Project: multi-tenant enterprise GenAI platform

#### Backend

FastAPI exposes:

* conversation APIs;
* streaming responses;
* document management;
* tenant administration;
* feedback;
* tool approval.

The orchestration layer:

1. authenticates the user;
2. resolves tenant and permissions;
3. classifies intent;
4. retrieves tenant-filtered documents;
5. reranks;
6. builds a grounded prompt;
7. invokes the configured model;
8. optionally calls approved tools;
9. streams output and citations;
10. records metrics and audit events.

#### Data

* **RDS/PostgreSQL:** tenants, conversations, metadata, audit.
* **Redis:** rate limits, cache, transient state.
* **S3:** original files and derived artifacts.
* **Vector DB:** embeddings and tenant-filtered chunks.
* **Queue:** document ingestion and long jobs.

#### Frontend

Next.js chat application provides:

* conversation history;
* token streaming;
* citation panels;
* upload workflow;
* model or mode selection;
* feedback;
* admin settings;
* approval dialogs.

#### Infrastructure

Terraform provisions:

* VPC;
* public/private subnets;
* EKS;
* RDS;
* Redis;
* S3;
* ECR;
* IAM;
* Route 53;
* ACM.

Kubernetes runs:

* frontend;
* FastAPI API;
* ingestion workers;
* agent/tool workers;
* evaluation jobs.

Helm packages deployments and environment-specific configuration.

#### Deployment

```text
Git push
  ↓
Jenkins PR validation
  ↓
Build and scan
  ↓
Push image digest to ECR
  ↓
Helm deploy to dev
  ↓
Smoke and AI evaluation
  ↓
Promote digest to stage/prod
```

#### Operations

Dashboards track:

* QPS and concurrency;
* p95 time-to-first-token;
* full response latency;
* model/provider errors;
* queue depth;
* retrieval hit rate;
* groundedness;
* tool success;
* tokens and cost;
* tenant-level usage;
* user feedback.

#### Security

* authentication through enterprise identity;
* server-derived tenant context;
* tenant filters in every query;
* object keys namespaced by tenant;
* pod-specific IAM roles;
* secrets outside Git;
* document malware/type scanning;
* prompt injection controls;
* tool allowlists and schema validation;
* approval for consequential actions;
* immutable audit events.

#### Cost control

* model routing by complexity;
* token budgets;
* context compression;
* embedding deduplication;
* cached retrieval and responses;
* per-tenant quotas;
* asynchronous batch processing;
* idle worker reduction;
* cost dashboards.

#### Reliability

* model fallback;
* bounded retries;
* queue-based ingestion;
* dead-letter queue;
* circuit breakers;
* readiness and graceful shutdown;
* Multi-AZ data services;
* rollback-ready releases.

---

## 2.11 Leadership, ownership and project storytelling

### How to present a project

Do not say:

> “I built a RAG application using LangChain, Pinecone and GPT.”

Say:

> “We needed to reduce employee time spent locating policy information. I led the design of a tenant-aware retrieval platform that indexed 12 million document chunks, returned cited answers at a two-second p95 time-to-first-token, and reduced support escalations by 28%. I chose asynchronous ingestion to isolate document spikes, introduced retrieval evaluation before model evaluation, and added per-tenant cost controls.”

### STAR plus architecture

#### Situation

* Business problem.
* Users affected.
* Previous system limitation.
* Scale or urgency.

#### Task

* Your ownership.
* Constraints.
* Success criteria.

#### Action

Explain:

* requirements;
* architecture;
* major decisions;
* trade-offs;
* cross-team influence;
* release and operations;
* failure handling.

#### Result

Use measurable outcomes:

* latency;
* availability;
* cost;
* adoption;
* quality;
* incident reduction;
* engineering speed.

#### Reflection

* what failed;
* what changed;
* what you would do differently.

### Technical leadership language

Use phrases such as:

* “I aligned the team on service boundaries.”
* “I documented the decision and alternatives.”
* “I separated the MVP path from the scale path.”
* “I introduced an SLO and error budget.”
* “I reduced operational risk through staged rollout.”
* “I made the trade-off explicit.”
* “I delegated implementation while retaining architectural accountability.”
* “I involved security and compliance before finalizing data flows.”
* “I used production evidence to revisit the original design.”

### Managing ambiguity

A senior engineer:

1. identifies what is unknown;
2. classifies reversible and irreversible decisions;
3. prototypes the highest-risk assumption;
4. defines measurable exit criteria;
5. avoids prematurely building the final platform.

### Speed versus quality

Use a risk-based approach:

| Situation             | Appropriate approach                                |
| --------------------- | --------------------------------------------------- |
| Internal demo         | Managed APIs, simple UI, minimal automation         |
| Limited beta          | Auth, logging, basic evaluation, controlled tenants |
| Enterprise production | Isolation, audit, SLOs, rollback, security reviews  |
| Regulated use         | Strong governance, retention, approval, evidence    |

### Explaining failures

Strong answer:

> “Our first retriever optimized semantic similarity but missed exact product codes. Rather than tuning the LLM, I separated retrieval diagnostics from generation, added hybrid retrieval and created a golden query set. Retrieval hit rate improved from 71% to 91%, and unsupported answers dropped significantly.”

Weak answer:

> “The model hallucinated, so we changed the prompt.”

### Ownership language

> “I was accountable for the service’s reliability and cost, not only delivery. That meant defining alerts, runbooks, rollback criteria, per-tenant budgets and the process for reviewing failed evaluations.”

---

# 3. Mock system design answers

## Mock design 1: Multi-tenant RAG SaaS

### 1. Clarify requirements

Functional:

* tenants upload documents;
* users ask questions;
* responses stream with citations;
* administrators control sources and retention;
* documents become searchable within five minutes.

Non-functional assumptions:

* 100,000 DAU;
* 60 peak query QPS;
* p95 time-to-first-token below two seconds;
* 99.9% availability;
* logical tenant isolation;
* encrypted storage;
* auditable retrieval;
* configurable model providers.

### 2. APIs

```http
POST /v1/documents/upload-url
POST /v1/documents/{id}/complete
GET  /v1/documents/{id}/status
POST /v1/conversations/{id}/messages
GET  /v1/conversations/{id}
POST /v1/feedback
```

Every authenticated request receives server-derived:

```text
user_id
tenant_id
roles
entitlements
request_id
```

### 3. Data model

```text
Tenant
User
Document
DocumentVersion
Chunk
Conversation
Message
Citation
IngestionJob
Feedback
UsageRecord
```

### 4. Architecture

```text
Next.js UI
  ↓
ALB / FastAPI
  ↓
Auth + tenant middleware
  ↓
RAG orchestrator
  ├─ Redis
  ├─ PostgreSQL
  ├─ Vector DB
  ├─ Reranker
  └─ Model gateway
```

Ingestion:

```text
S3 upload
  ↓
Queue
  ↓
Parser workers
  ↓
Chunk + metadata
  ↓
Embedding batch
  ↓
Vector upsert
  ↓
Document status = READY
```

### 5. Retrieval path

1. Validate tenant.
2. Rewrite query only when needed.
3. Hybrid keyword and vector retrieval.
4. Apply tenant, ACL and document-version filters.
5. Rerank.
6. Deduplicate.
7. Assemble context under token budget.
8. Generate answer.
9. Validate citation references.
10. Stream response.

### 6. Reliability

* bounded retry for model 429/5xx;
* model circuit breaker;
* reranker fallback;
* dead-letter queue for ingestion;
* idempotent document checksum;
* graceful pod shutdown;
* cached metadata;
* previous release retained.

### 7. Security

* tenant ID derived from identity, not body;
* vector filters enforced by retrieval service;
* tenant-prefixed object keys;
* encryption;
* signed uploads;
* malware/type scanning;
* prompt injection detection;
* no raw credentials in prompts;
* deletion workflow removes source, chunks and caches.

### 8. Cost

* batch embeddings;
* skip unchanged documents using checksums;
* small model for query classification;
* large model only when required;
* per-tenant quotas;
* cache identical public queries;
* context budget.

### 9. Observability

* retrieval hit rate;
* citation coverage;
* groundedness;
* time-to-first-token;
* model/provider errors;
* cost per tenant;
* ingestion lag;
* feedback.

### 10. Trade-offs

* Shared vector index with tenant filters is cheaper, but dedicated indexes provide stronger isolation.
* Managed model APIs accelerate delivery, but create provider limits and data-governance considerations.
* Hybrid retrieval improves exact-match recall but requires score normalization.

### Senior closing

> “I would launch with shared infrastructure and enforced logical tenant boundaries, but design the storage abstraction so regulated tenants can move to dedicated indexes or databases without changing the product API.”

---

## Mock design 2: Agent platform with tools

### 1. Requirements

The platform lets teams create assistants that can:

* query enterprise data;
* invoke approved tools;
* pause for human approval;
* resume after failure;
* retain an auditable execution history.

Tools include:

* CRM read/write;
* ticketing;
* email;
* analytics;
* internal APIs.

### 2. Core architecture

```text
Chat/API clients
  ↓
Agent gateway
  ↓
Agent runtime / state machine
  ├─ planner or router
  ├─ model gateway
  ├─ tool registry
  ├─ policy engine
  ├─ checkpoint store
  ├─ approval service
  └─ event stream
```

### 3. Tool contract

```json
{
  "name": "create_support_ticket",
  "version": "2",
  "risk": "write",
  "input_schema": {
    "type": "object",
    "required": ["customer_id", "summary"]
  },
  "timeout_seconds": 10,
  "requires_approval": true
}
```

### 4. Execution model

```text
RECEIVED
  ↓
CLASSIFIED
  ↓
PLANNED
  ↓
TOOL_SELECTED
  ↓
POLICY_CHECK
  ├─ denied → FAILED_POLICY
  ├─ approval → WAITING_APPROVAL
  └─ allowed → EXECUTING
  ↓
OBSERVATION_RECORDED
  ↓
NEXT_STEP or COMPLETED
```

Persist state after significant transitions so execution can resume.

### 5. Safety boundaries

* allowlisted tools;
* schema validation;
* tenant-scoped credentials;
* separate read/write tools;
* approval for high-impact actions;
* maximum step count;
* maximum cost;
* timeout per tool and workflow;
* result size limit;
* output sanitization;
* immutable audit record.

### 6. Reliability

* idempotency key per write action;
* no blind retry of non-idempotent tools;
* circuit breaker by tool;
* separate worker pools per tool category;
* checkpoint before external side effects;
* dead-letter path for unresolved executions.

### 7. Scale

Scale independently:

* chat/API pods by request concurrency;
* orchestration workers by active workflows;
* tool workers by queue depth;
* model calls by provider quota;
* checkpoint database by workflow event volume.

### 8. Observability

* tool selection accuracy;
* approval rate;
* tool latency;
* side-effect success;
* retries;
* agent step count;
* abandonment;
* cost per completed task;
* policy denials.

### 9. Trade-offs

* Free-form agent loop is flexible but hard to predict.
* Graph/state-machine orchestration is more controllable but requires workflow design.
* Synchronous tools simplify UX but create long-held connections.
* Central tool gateway improves governance but can become a bottleneck.

### Senior closing

> “I would use deterministic workflow edges for security-sensitive operations and reserve model-driven decisions for bounded choices. The model can propose an action, but policy—not the model—authorizes it.”

---

## Mock design 3: Enterprise document assistant

### 1. Scope

Employees ask questions across:

* HR policies;
* engineering documentation;
* legal templates;
* operational procedures.

Requirements:

* source-level access controls;
* citations;
* document freshness;
* no cross-department leakage;
* audit;
* high answer trust.

### 2. Architecture

```text
Enterprise SSO
  ↓
Assistant API
  ↓
Authorization context
  ↓
Search federation
  ├─ vector search
  ├─ keyword search
  └─ metadata/ACL filters
  ↓
Reranker
  ↓
Grounded generation
  ↓
Citation verification
```

Connectors synchronize content asynchronously:

```text
SharePoint / Drive / Wiki / S3
  ↓
Connector scheduler
  ↓
Change detection
  ↓
Parsing and ACL extraction
  ↓
Index update
```

### 3. Freshness

Store:

* connector cursor;
* source document version;
* content checksum;
* ACL version;
* last indexed timestamp;
* deletion tombstone.

Use incremental synchronization rather than full re-indexing.

### 4. Authorization

Apply authorization before content reaches the LLM:

```text
User groups
  ↓
Allowed document IDs / ACL filter
  ↓
Retrieval
  ↓
Only authorized chunks enter prompt
```

Do not retrieve broadly and then ask the model to hide unauthorized content.

### 5. Trust

* answer only from indexed sources for policy questions;
* show “insufficient evidence” when retrieval is weak;
* map claims to citations;
* show document date/version;
* allow users to open the source;
* distinguish official and community sources.

### 6. Failure modes

* stale connector;
* deleted source remains indexed;
* ACL changed but index not updated;
* exact identifiers missed by semantic search;
* conflicting document versions;
* prompt injection inside a document.

### 7. Mitigations

* freshness SLO;
* deletion reconciliation;
* ACL-aware indexing;
* hybrid search;
* authoritative-source ranking;
* document-level trust metadata;
* treat retrieved content as untrusted data;
* source version shown in UI.

### 8. Trade-offs

* Central index is efficient, but authorization logic becomes critical.
* Per-source indexes simplify ownership, but make ranking and operations harder.
* Immediate indexing improves freshness, but connector APIs may impose limits.
* Strict grounded mode increases trust, but returns more “I don’t know” responses.

### Senior closing

> “For an enterprise assistant, authorization correctness is more important than retrieval recall. Unauthorized content must be excluded before prompt construction, and index deletion/ACL propagation requires its own measurable SLO.”

---

# 4. Trade-offs, pitfalls and senior-level talking points

| Decision                                 | Option A                  | Option B                    | Senior framing                                           |
| ---------------------------------------- | ------------------------- | --------------------------- | -------------------------------------------------------- |
| Monolith vs microservices                | Simpler operations        | Independent scaling         | Start modular; split on ownership/scaling evidence       |
| EKS vs managed serverless                | Control/flexibility       | Low operations              | Choose based on workload diversity and platform maturity |
| Shared vs dedicated tenant data          | Cost-efficient            | Strong isolation            | Offer isolation tiers based on risk                      |
| Sync vs async                            | Immediate result          | Resilience and buffering    | Keep user-critical short path sync; move long work async |
| One model vs model gateway               | Simple                    | Portability/fallback        | Abstract only where switching or policy is real          |
| Vector vs hybrid retrieval               | Semantic                  | Semantic + exact terms      | Hybrid commonly improves enterprise identifiers          |
| Large context vs retrieval               | Simple prompting          | Lower cost and better focus | Use retrieval, reranking and token budgets               |
| Rolling vs blue/green                    | Efficient                 | Fast traffic reversal       | Match release risk and compatibility needs               |
| Terraform workspaces vs separate state   | Convenient                | Strong isolation            | Separate production state and permissions                |
| UI direct model calls vs backend gateway | Low latency to prototype  | Security/governance         | Production calls go through controlled backend           |
| Free-form agents vs workflows            | Flexible                  | Predictable                 | Bound autonomy around side effects                       |
| Retries vs fail fast                     | Recovers transient faults | Limits amplification        | Retry only known transient and idempotent operations     |
| Cache vs freshness                       | Lower cost/latency        | Up-to-date                  | Key cache by tenant, version and policy                  |
| Build per environment vs promote         | Environment customization | Artifact consistency        | Build once and promote the same digest                   |
| CPU HPA vs custom metrics                | Easy                      | Workload-aware              | GenAI often needs concurrency/queue metrics              |

### High-signal pitfalls

1. **Retry amplification**
   HTTP client, service mesh, application and worker all retry the same request.

2. **Tenant leakage**
   Tenant filter is forgotten in one retrieval or cache path.

3. **Prompt-only security**
   The prompt says not to call a dangerous tool, but no policy layer enforces it.

4. **False deployment success**
   Pods are healthy, but retrieval quality or tool behavior regressed.

5. **Queue without idempotence**
   A redelivered message creates duplicate embeddings or side effects.

6. **Mutable releases**
   `latest` points to different images during rollback.

7. **Poor shutdown handling**
   Rolling updates cut active streaming connections.

8. **External dependency coupling**
   Readiness fails because a third-party model has a brief outage.

9. **Unbounded context**
   Cost and latency rise while relevance falls.

10. **No source lifecycle**
    Deleted or access-revoked documents remain retrievable.

### Senior talking-point formula

For any design choice, say:

> “I chose **A** because of **constraint X**. The main benefit is **Y**, while the cost is **Z**. I reduce that risk through **mitigation M**. If scale or requirements change, I would move to **B** when **trigger T** occurs.”

---

# 5. Interview Q&A

## System design

### 1. How do you begin a GenAI system design interview?

Clarify the user, use cases, data sensitivity, scale, latency, availability, quality target, cost envelope and tenant-isolation requirements before drawing components.

### 2. What is different about designing a GenAI system?

You must design for both deterministic software reliability and probabilistic model quality, including retrieval, grounding, safety, tool correctness and cost.

### 3. Why calculate concurrency as well as QPS?

Long-running model requests remain active. Concurrency is approximately QPS multiplied by average request duration and determines connection, memory and provider capacity.

### 4. What belongs in the synchronous path?

Authentication, authorization, retrieval, prompt construction, generation and short user-facing tool calls.

### 5. What belongs in the asynchronous path?

Document ingestion, embedding, large exports, connector synchronization, offline evaluation and long-running workflows.

### 6. How do you handle model-provider failure?

Use strict timeouts, bounded retries for transient failures, a circuit breaker, fallback providers where appropriate and graceful user-visible errors.

### 7. What is backpressure?

A system reduces or rejects incoming work when downstream capacity is saturated rather than allowing unlimited queues or resource exhaustion.

### 8. What is a bulkhead?

Separate resource pools isolate failures—for example, document ingestion workers cannot consume all capacity needed by chat requests.

### 9. How do you measure a RAG system?

Measure retrieval hit rate, ranking quality, citation accuracy, groundedness, answer relevance, latency, cost and user task success.

### 10. What is admission control?

Checking quotas, concurrency or system capacity before accepting expensive work and rejecting excess load early.

## Terraform and AWS

### 11. Terraform versus Ansible?

Terraform provisions infrastructure resources declaratively. Ansible primarily configures operating systems and software on managed hosts.

### 12. Why is Terraform state important?

It maps Terraform configuration to real resources, supports planning and must be protected because corruption or unauthorized access can cause destructive changes.

### 13. How should Terraform state be stored?

In a secured remote backend with encryption, access controls, versioning and locking. Production states should be separated by environment and blast radius.

### 14. Is DynamoDB still the preferred Terraform S3 lock?

No. It is a legacy pattern; current Terraform supports native S3 lockfiles and marks DynamoDB locking as deprecated. ([HashiCorp Developer][21])

### 15. Workspaces or separate state?

Use separate state and permissions for production isolation. Workspaces are more suitable for equivalent, lower-risk instances or ephemeral environments.

### 16. What belongs in public subnets?

Normally internet-facing load balancers and NAT Gateways. Application and data workloads should generally remain private.

### 17. Internet Gateway versus NAT Gateway?

An Internet Gateway supports internet routing for public resources. A NAT Gateway lets private workloads initiate outbound connections without accepting unsolicited inbound internet traffic. ([AWS Documentation][7])

### 18. Security group versus NACL?

Security groups are stateful resource-level firewalls. NACLs are stateless subnet-level controls.

### 19. How should EKS pods access S3?

Through a pod-specific IAM role or EKS pod identity attached to the Kubernetes service account, not static access keys. ([AWS Documentation][13])

### 20. Why use presigned S3 URLs?

They allow time-limited browser upload or download without exposing AWS credentials or proxying large files through the application server. ([AWS Documentation][12])

## Kubernetes and Helm

### 21. Deployment versus Service?

A Deployment manages pod replicas and rollout. A Service provides stable network access to selected pods.

### 22. Readiness versus liveness?

Readiness controls traffic eligibility. Liveness determines whether Kubernetes should restart a container.

### 23. Why should liveness not call the model provider?

A provider outage would cause all pods to restart, creating an unnecessary restart storm without fixing the dependency.

### 24. Why separate API and ingestion workers?

They have different latency, resource, scaling and failure characteristics. Separation protects interactive capacity.

### 25. What should drive HPA for a GenAI service?

Potentially active requests, queue depth, event-loop lag or token-generation concurrency in addition to CPU and memory.

### 26. Helm chart versus release?

A chart is the package/template. A release is an installed instance of that chart with specific values.

### 27. Rolling versus blue/green deployment?

Rolling updates gradually replace pods with lower cost. Blue/green runs two environments and switches traffic, enabling fast reversal at higher cost.

### 28. How do you prevent dropped streams during rollout?

Use readiness transitions, graceful termination, connection draining, sufficient termination grace period and disruption controls.

## CI/CD and evaluation

### 29. Why build once and promote?

It guarantees the tested artifact is the production artifact and prevents dependency or build differences between environments.

### 30. What makes a GenAI deployment gate different?

It adds retrieval, grounding, tool-use and safety evaluations to normal tests, scans and health checks.

### 31. What is a golden RAG test?

A stable set of questions with expected sources, required facts and unsupported-answer checks used to detect retrieval and response regressions.

### 32. How do you rollback a bad prompt change?

Version prompts/configuration, preserve the previous version, and switch configuration or release without requiring a new application build.

### 33. Should AI evaluations block every deployment?

Critical deterministic safety and tenant-isolation checks should block. Noisy model-quality metrics may use thresholds, sample sizes and human review.

## Frontend and product

### 34. SSE or WebSockets for token streaming?

SSE is simpler for one-way server-to-browser streams. WebSockets are useful when continuous bidirectional communication is required.

### 35. How should citations be designed?

Return structured source IDs, titles, locations, versions and excerpts, then map citations to answer claims rather than showing an unrelated source list.

### 36. Why use signed upload URLs?

They reduce application bandwidth and securely enable direct-to-object-storage uploads without exposing cloud credentials.

### 37. How should the UI represent agent execution?

Show clear stages, tool names, approval requirements, results, failures and whether external side effects occurred.

### 38. What is the most important product metric for an assistant?

Task completion or successful resolution is generally more meaningful than raw message count, although the exact metric depends on the business problem.

## Leadership

### 39. How do you balance MVP and production quality?

Keep the product surface small, but do not omit controls whose absence creates unacceptable security, data-loss or compliance risk.

### 40. How do you describe your staff-level impact?

Explain the cross-team problem, architectural direction, decisions influenced, operational mechanisms created, measurable outcome and how the platform enabled other teams.

---

# 6. Reusable project storytelling template

## 90-second version

```text
The problem:
[Users/business] were struggling with [specific problem], causing [measurable impact].

My role:
I owned [architecture/platform/reliability] and coordinated with [teams].

Constraints:
We had [scale, latency, security, time or cost constraints].

Architecture:
I designed [high-level architecture] with [important boundaries].

Key decisions:
I chose [decision A] over [alternative] because [reason].
I handled [major risk] through [mitigation].

Operations:
We added [SLOs, dashboards, evaluations, rollout and rollback].

Result:
We achieved [latency, quality, cost, adoption or business outcome].

Learning:
The biggest lesson was [lesson], and I would now [improvement].
```

## Deep-dive version

### 1. Problem and users

* Who had the problem?
* How often?
* What was the business impact?
* Why did existing systems fail?

### 2. Scope and ownership

* What did you personally own?
* What did others own?
* Which decisions did you influence?

### 3. Requirements

* Scale.
* Latency.
* Availability.
* Security.
* Compliance.
* Cost.
* Quality.

### 4. Architecture

Explain:

* request flow;
* ingestion flow;
* service boundaries;
* data ownership;
* infrastructure;
* deployment.

### 5. Hardest decisions

For each:

```text
Decision
Alternatives
Chosen option
Reason
Risk
Mitigation
Trigger to revisit
```

### 6. Failure and learning

Discuss one real issue:

* symptom;
* root cause;
* why monitoring did or did not catch it;
* immediate mitigation;
* systemic fix;
* process improvement.

### 7. Impact

Use numbers:

* p95 latency reduced from X to Y;
* retrieval hit rate increased;
* cost per request reduced;
* deployment time reduced;
* adoption increased;
* incidents decreased;
* onboarding time improved.

## Sample storytelling answer

> “Our support team spent several hours per day searching fragmented product documentation. I led the design of a multi-tenant RAG platform serving approximately 50 peak QPS. We separated asynchronous ingestion from the interactive query path, used hybrid retrieval because exact product codes were important, and enforced tenant and document ACL filters before prompt construction.
>
> The main trade-off was shared versus dedicated vector indexes. We began with a shared index for cost efficiency but built the retrieval interface so regulated customers could move to dedicated indexes. We added golden retrieval tests, citation validation, per-tenant token budgets and staged Helm deployments.
>
> We reduced median resolution time by 34%, achieved a 1.7-second p95 time-to-first-token, and lowered unsupported answers through retrieval evaluation. Our first semantic-only approach missed exact identifiers, which taught us to diagnose retrieval separately from generation.”

---

# 7. Final capstone checklist for Days 1–37

## Python and software engineering

* [ ] Explain Python mutability, iterators, generators and context managers.
* [ ] Use type hints, protocols and validation.
* [ ] Design clean interfaces using SOLID principles.
* [ ] Apply Factory, Strategy, Adapter, Decorator and Facade patterns.
* [ ] Explain async I/O, event loops and bounded concurrency.
* [ ] Test unit, integration and failure paths.
* [ ] Handle retries, timeouts and exceptions safely.

## DSA and problem solving

* [ ] Arrays, strings and hash maps.
* [ ] Two pointers and sliding windows.
* [ ] Stacks and queues.
* [ ] Trees and graphs.
* [ ] BFS and DFS.
* [ ] Basic dynamic programming.
* [ ] State time and space complexity.
* [ ] Connect graph thinking to workflows and dependency DAGs.

## Backend engineering

* [ ] Design REST and streaming APIs.
* [ ] Explain idempotency and pagination.
* [ ] Use background workers and queues.
* [ ] Model relational data and indexes.
* [ ] Explain transactions and consistency.
* [ ] Use Redis appropriately.
* [ ] Apply rate limiting and admission control.
* [ ] Design authentication and authorization boundaries.

## Machine learning and deep learning

* [ ] Bias versus variance.
* [ ] Training, validation and test sets.
* [ ] Precision, recall, F1 and ROC-AUC.
* [ ] Overfitting and regularization.
* [ ] Embeddings and similarity.
* [ ] Transformer and attention intuition.
* [ ] Fine-tuning versus prompting versus retrieval.
* [ ] Offline versus online evaluation.

## LLM systems

* [ ] Tokens, context windows and sampling.
* [ ] Prompt structure and versioning.
* [ ] Structured outputs.
* [ ] Tool/function calling.
* [ ] Hallucination and grounding.
* [ ] Model routing.
* [ ] Latency and token-cost optimization.
* [ ] Safety and prompt-injection boundaries.

## RAG

* [ ] Ingestion pipeline.
* [ ] Parsing, chunking and metadata.
* [ ] Embedding and indexing.
* [ ] Vector, keyword and hybrid retrieval.
* [ ] Recall versus precision.
* [ ] Reranking.
* [ ] Context assembly.
* [ ] Citations.
* [ ] Retrieval evaluation.
* [ ] Freshness, deletion and ACL propagation.
* [ ] Multi-tenant filtering.

## Frameworks and orchestration

* [ ] Vanilla RAG as a design pattern.
* [ ] LlamaIndex as a data/retrieval-oriented framework.
* [ ] LangChain as an integration and application framework.
* [ ] LangGraph as a stateful orchestration runtime.
* [ ] MCP as a tool/data connectivity protocol.
* [ ] Know when a framework is unnecessary.
* [ ] Keep domain logic independent of framework details.

## Agents

* [ ] Workflow versus agent.
* [ ] State, nodes and conditional routing.
* [ ] Tool registry and schemas.
* [ ] Checkpointing and resumability.
* [ ] Human approval.
* [ ] Step, time and cost limits.
* [ ] Tool idempotency.
* [ ] Policy enforcement outside the model.
* [ ] Agent evaluation.

## System design

* [ ] Clarify functional requirements.
* [ ] Define measurable NFRs.
* [ ] Estimate QPS, concurrency, storage and bandwidth.
* [ ] Define APIs and data model.
* [ ] Draw request and ingestion flows.
* [ ] Separate sync and async.
* [ ] Cover reliability and failure modes.
* [ ] Discuss observability.
* [ ] Cover security and cost.
* [ ] State trade-offs and evolution path.

## Cloud and platform

* [ ] VPC, CIDR, subnets and routing.
* [ ] Internet and NAT gateways.
* [ ] Security groups and NACLs.
* [ ] EKS control plane and nodes.
* [ ] ALB ingress.
* [ ] RDS, Redis, S3 and ECR.
* [ ] IAM and pod identities.
* [ ] Multi-AZ design.
* [ ] DNS and TLS.

## Terraform

* [ ] Resource, data, variable, local and output.
* [ ] Init, plan, apply and destroy.
* [ ] State and remote backend.
* [ ] Native S3 lockfiles and legacy DynamoDB locking.
* [ ] Drift.
* [ ] Modules.
* [ ] Environment separation.
* [ ] Production plan review.
* [ ] State security.

## Kubernetes and Helm

* [ ] Pods, Deployments, Services and Ingress.
* [ ] ConfigMaps and Secrets.
* [ ] Startup, readiness and liveness.
* [ ] Resource requests and limits.
* [ ] HPA and node scaling.
* [ ] Helm chart, values and release.
* [ ] Install, upgrade and rollback.
* [ ] Rolling and blue/green.
* [ ] Graceful shutdown and stream draining.

## CI/CD and operations

* [ ] Jenkins controller and agents.
* [ ] Pipeline as code.
* [ ] Build immutable images.
* [ ] Push to ECR.
* [ ] Promote one artifact.
* [ ] Deploy through Helm.
* [ ] Run smoke and behavioral tests.
* [ ] Define rollback criteria.
* [ ] Use logs, metrics and traces.
* [ ] Maintain runbooks and incident reviews.

## Frontend and product

* [ ] React versus Next.js.
* [ ] Chat component architecture.
* [ ] Streaming event contract.
* [ ] Citation display.
* [ ] Upload through signed URL.
* [ ] Loading, error, cancellation and retry states.
* [ ] Feedback loop.
* [ ] Tool approval UX.
* [ ] Trust and explainability.

## Monorepo and DevEx

* [ ] Clear repository boundaries.
* [ ] Environment configuration strategy.
* [ ] Shared API types.
* [ ] One-command local setup.
* [ ] Model and tool mocks.
* [ ] PR checks.
* [ ] Release tags.
* [ ] Onboarding documentation.
* [ ] Architecture decision records.

## Leadership

* [ ] Tell a project story in 90 seconds.
* [ ] State personal ownership clearly.
* [ ] Explain two major trade-offs.
* [ ] Give one failure and lesson.
* [ ] Quantify business and technical impact.
* [ ] Explain cross-team influence.
* [ ] Show cost, security and reliability ownership.
* [ ] Distinguish MVP choices from production choices.

---

# 8. Last-day-before-interview cheat sheet

## The architecture sentence

> “I separate the experience, application, intelligence, data, platform, delivery and operations planes, with explicit contracts and independent failure boundaries.”

## The design sequence

```text
Requirements
→ NFRs
→ Capacity
→ APIs
→ Data model
→ Architecture
→ Async path
→ Reliability
→ Security
→ Observability
→ Cost
→ Trade-offs
→ Evolution
```

## The GenAI request path

```text
Authenticate
→ Resolve tenant
→ Authorize
→ Retrieve
→ Rerank
→ Build context
→ Generate/tool call
→ Validate
→ Cite
→ Stream
→ Observe
```

## The deployment path

```text
Git push
→ PR checks
→ Build once
→ Push digest
→ Deploy dev
→ Evaluate
→ Promote
→ Verify
→ Observe
→ Rollback
```

## The reliability set

```text
Timeout
Bounded retry
Backoff + jitter
Circuit breaker
Bulkhead
Backpressure
Admission control
Idempotency
Dead-letter queue
Graceful degradation
```

## The security set

```text
Server-derived tenant identity
Authorization before retrieval
Least-privilege workload roles
Secrets outside Git
Encrypted data
Tool allowlists
Schema validation
Human approval
Audit trail
Deletion propagation
```

## The AI-quality set

```text
Retrieval hit rate
Reranking quality
Citation accuracy
Groundedness
Task completion
Tool success
Latency
Tokens
Cost
User feedback
```

## The staff-level answer pattern

```text
Constraint
→ Decision
→ Benefit
→ Trade-off
→ Mitigation
→ Metric
→ Trigger to revisit
```

## Five statements worth memorizing

1. **“The model may propose an action; policy authorizes it.”**

2. **“Unauthorized information must be removed before prompt construction, not hidden by the prompt.”**

3. **“A deployment is healthy only when infrastructure and AI behavioral metrics are healthy.”**

4. **“Build once and promote the same immutable artifact.”**

5. **“I separate retrieval quality from generation quality before tuning the model.”**

## Final interview reminder

A senior answer should consistently cover:

* user and business value;
* architecture;
* scale;
* failure;
* security;
* cost;
* operation;
* trade-offs;
* measurable impact.

Do not try to mention every technology you know. Choose a coherent architecture, state your assumptions, defend the major decisions and show how you would operate the system after launch.

[1]: https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html "https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html"
[2]: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html"
[3]: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/ "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/"
[4]: https://developer.hashicorp.com/terraform "https://developer.hashicorp.com/terraform"
[5]: https://developer.hashicorp.com/terraform/language/backend/s3?utm_source=chatgpt.com "Backend Type: s3 | Terraform"
[6]: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html"
[7]: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html"
[8]: https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html "https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html"
[9]: https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html "https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html"
[10]: https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html "https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html"
[11]: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html"
[12]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html "https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html"
[13]: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html "https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html"
[14]: https://kubernetes.io/docs/concepts/services-networking/ingress/ "https://kubernetes.io/docs/concepts/services-networking/ingress/"
[15]: https://helm.sh/docs/topics/charts/ "https://helm.sh/docs/topics/charts/"
[16]: https://helm.sh/docs/helm/helm_upgrade/ "https://helm.sh/docs/helm/helm_upgrade/"
[17]: https://www.jenkins.io/doc/book/pipeline/syntax/ "https://www.jenkins.io/doc/book/pipeline/syntax/"
[18]: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/ "https://www.jenkins.io/doc/book/pipeline/jenkinsfile/"
[19]: https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_intro.html "https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_intro.html"
[20]: https://nextjs.org/docs/app/getting-started/server-and-client-components "https://nextjs.org/docs/app/getting-started/server-and-client-components"
[21]: https://developer.hashicorp.com/terraform/language/backend/s3 "https://developer.hashicorp.com/terraform/language/backend/s3"
