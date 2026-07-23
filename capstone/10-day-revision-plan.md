# 10-day revision plan

## How to use this plan

Each day has one canonical topic boundary, one production exercise, and one interview drill. The detailed note for that day contains the consolidated explanations, examples, trade-offs, best practices, production use cases, and questions.

Suggested daily sequence:

1. **Recall:** explain the previous day without notes.
2. **Core revision:** read the day’s detailed note.
3. **Active practice:** write code, pseudocode, a data model, or an architecture.
4. **Production review:** enumerate failures, controls, telemetry, and trade-offs.
5. **Interview drill:** answer the selected questions aloud.
6. **Exit check:** complete the checklist from memory.

The sequence moves from implementation foundations to complete enterprise architecture:

```text
Python
  → backend and algorithms
  → ML/LLM foundations
  → RAG
  → frameworks and MCP
  → agents
  → data/ML platforms
  → production operations
  → cloud/platform delivery
  → Staff-level system design
```

## Day 1 — Production Python for AI services

Detailed notes: [day-01-python-engineering.md](day-01-python-engineering.md)

### Coverage

- Core Python types, collections, slicing, comprehensions, iterators, generators, context managers, functions, modules, imports, and environments.
- Project structure, configuration, logging, exceptions, and tests.
- OOP, protocols, abstract base classes, dataclasses, dunder methods, and properties.
- Type hints, `TypedDict`, `mypy`, Pydantic, error hierarchies, Arrange–Act–Assert, fixtures, fakes, and mocks.
- Provider-neutral AI abstractions and dependency injection.

### Practice

- Sketch a provider-neutral RAG service with interfaces for embedder, vector store, reranker, prompt builder, and generator.
- Write one immutable configuration type and one validated API/tool payload.
- Design unit tests using deterministic fakes and a smaller adapter integration suite.

### Interview drill

- Mutable defaults; list versus tuple; set use in RAG.
- ABC versus protocol; composition versus inheritance.
- Type hints versus runtime validation.
- How to test an LLM application without live model calls in every test.

### Exit result

You can explain what makes a Python AI service maintainable, testable, provider-neutral, observable, and safe.

## Day 2 — Backend architecture, concurrency, databases, APIs, and DSA

Detailed notes: [day-02-backend-dsa-and-concurrency.md](day-02-backend-dsa-and-concurrency.md)

### Coverage

- SOLID and Factory, Strategy, Adapter, Decorator, Facade, and Repository patterns.
- Layered architecture and dependency direction.
- Flask/FastAPI, HTTP methods/status codes, REST/CRUD resources, idempotency, pagination, versioning, breaking changes, and standard errors.
- SQL, joins, aggregations, indexes, transactions, normalization, ORM/N+1 behavior, NoSQL, Redis, caching, and vector-store boundaries.
- Async/event loop, coroutines/tasks, gather/task groups, timeouts, cancellation, locks, semaphores, `concurrent.futures`, threads, processes, queues, and background work.
- DSA recognition: hashing, prefix sums, two pointers, sliding windows, monotonic stacks, queues, binary trees/BSTs, graphs, BFS/DFS, topological sort, and DP.

### Practice

- Design `POST /runs`, `GET /runs/{id}`, cancellation, and cursor-paginated run history.
- Model `Tenant`, `Project`, `AgentRun`, `ToolExecution`, `Artifact`, and `AuditLog`.
- Solve one problem from each DSA pattern and state time/space complexity.

### Interview drill

- `202 Accepted`; idempotency; offset versus cursor pagination.
- SQL versus NoSQL; Redis versus durable storage; N+1; index trade-offs.
- Async versus threads versus processes; blocking calls inside async endpoints.
- BFS versus DFS; variable sliding window; prefix sum plus hash map.

### Exit result

You can connect code-level choices to API contracts, storage access patterns, concurrency limits, and interview algorithms.

## Day 3 — ML, data, NLP, deep learning, and LLM foundations

Detailed notes: [day-03-ml-data-llm-foundations.md](day-03-ml-data-llm-foundations.md)

### Coverage

- Supervised, unsupervised, and reinforcement learning.
- Linear/logistic regression, decision-tree/random-forest baselines, classification, clustering, splits, cross-validation, leakage, overfitting, and metrics.
- EDA, missing values, duplicates, outliers, encoding, scaling, feature engineering, and reproducible preprocessing.
- NumPy, Pandas, scikit-learn, PyTorch, TensorFlow/Keras, and Hugging Face selection.
- NLP preprocessing, BoW, TF-IDF, word/sentence embeddings, classification, NER, and sentiment.
- Neural networks, gradients, SGD/Adam, transformers, attention, Q/K/V, model families, and tokenization.
- Pretraining, instruction tuning, fine-tuning, RLHF, DPO, inference controls, context windows, and model risks.
- Prompt roles, few-shot prompting, ReAct, structured output, guardrails, and prompt regression testing.
- Multimodal models, CNN/transfer learning, diffusion, and generative-model comparisons.
- BLEU, ROUGE, LLM-as-judge, human evaluation, and their trade-offs.

### Practice

- Turn a churn business problem into features, leakage-safe splits, metrics, deployment, monitoring, and retraining.
- Explain attention and the encoder/decoder family choices without brand-dependent memorization.
- Compare prompting, RAG, tool use, and fine-tuning for four different failure causes.

### Interview drill

- Accuracy versus precision/recall/F1; data leakage; overfitting.
- Cosine similarity; gradients/backpropagation; self-attention and Q/K/V.
- Pretraining versus fine-tuning versus RAG.
- Why a large context window does not remove the need for retrieval.

### Exit result

You can reason from business problem to data, metric, model family, adaptation method, and production risk.

## Day 4 — RAG, embeddings, vector databases, advanced retrieval, and evaluation

Detailed notes: [day-04-rag-and-retrieval.md](day-04-rag-and-retrieval.md)

### Coverage

- RAG problem statement and the ingestion/query split.
- Parsing, cleaning, metadata, chunking, embeddings, indexing, retrieval, context assembly, prompting, generation, citations, and telemetry.
- Cosine/dot-product/Euclidean similarity, Flat/HNSW/IVF indexes, vector-store positioning, namespaces/collections, metadata filters, top-k, and embedding/index versioning.
- Keyword, semantic, hybrid, fusion, query rewriting, multi-query, reranking, contextual compression, and parent-child/hierarchical retrieval.
- Recall, precision, MRR, context precision/recall, groundedness, faithfulness, relevance, and hallucination.
- Golden datasets, offline evaluation, online feedback, failure diagnosis, caching, freshness, deletion, and ACL propagation.

### Practice

- Design a multi-tenant policy assistant’s offline and online paths.
- Create a vector record schema with identity, lifecycle, security, and citation metadata.
- Diagnose four failures: not indexed, not retrieved, retrieved but ignored, and unauthorized retrieval.

### Interview drill

- RAG versus fine-tuning; vector database versus retriever.
- Choosing chunk size and top-k.
- Hybrid search and reranking.
- Preventing cross-tenant leakage and stale/deleted-document retrieval.
- Decomposing retrieval quality from generation quality.

### Exit result

You can design, evaluate, debug, secure, and optimize a production RAG pipeline without treating the LLM as the only quality lever.

## Day 5 — LlamaIndex, LangChain, MCP, and framework selection

Detailed notes: [day-05-frameworks-and-mcp.md](day-05-frameworks-and-mcp.md)

### Coverage

- Vanilla RAG as a pattern, frameworks as reusable abstractions, orchestration as control flow, and MCP as a protocol.
- LlamaIndex documents, nodes, indexes, retrievers, query engines, postprocessors, and response synthesis.
- LangChain models, prompts, templates, structured output, retrievers, tools, chains, state/memory, callbacks, middleware, and LangSmith positioning.
- MCP host/client/server, tools/resources/prompts, lifecycle, capability negotiation, JSON-RPC, and governance.
- MCP versus function calling and A2A, including when a shared protocol is or is not worth adopting.
- Framework boundaries, testing, observability, lock-in, upgrade risk, and when direct code is better.

### Practice

- Draw the same knowledge assistant as direct code, LlamaIndex-centered retrieval, LangChain application composition, and a combined stack.
- Define a domain interface that hides framework-specific types.
- Design one read-only and one state-changing MCP tool with authorization, validation, approval, idempotency, and audit.

### Interview drill

- LlamaIndex versus LangChain.
- LangChain versus LangGraph.
- MCP versus function calling.
- Tool versus resource; host versus client; protocol session versus conversation memory.
- Why not use every framework.

### Exit result

You can select frameworks based on the complexity they remove, preserve architectural boundaries, and explain MCP without confusing it with agents or orchestration.

## Day 6 — LangGraph, agents, multi-agent systems, and controlled autonomy

Detailed notes: [day-06-agents-and-langgraph.md](day-06-agents-and-langgraph.md)

### Coverage

- Workflow versus agent versus hybrid control.
- State schemas, nodes, fixed/conditional edges, routing, loops, parallel work, tools, checkpoints, durability, streaming, retries, recovery, and shared-state ownership.
- Human approval, bounded loops, time/cost/step limits, idempotent side effects, and audit.
- Planner-executor-verifier, router-specialist, manager-worker, critic, and escalation patterns.
- CrewAI, Semantic Kernel, AutoGen, A2A, ADK, and low-code workflow positioning.
- Short-term versus long-term agent memory and tenant/user/workflow scoping.
- Agent evaluation, tool metrics, policy denial, approval outcomes, and cost per completed task.

### Practice

- Design an IT-support or policy-comparison graph with explicit states and transitions.
- Mark every model-driven versus deterministic decision.
- Add a checkpoint, a human-approval pause, a safe retry, and a compensation/escalation path.

### Interview drill

- When a chain is enough and when a graph is justified.
- Durable execution versus business rollback.
- Why the model may propose but policy authorizes.
- When multi-agent is useful and when it is overkill.
- Preventing infinite loops and unsafe tool calls.

### Exit result

You can design a controllable agent runtime whose autonomy is bounded by state, policy, permissions, approvals, budgets, and observability.

## Day 7 — Databricks, Delta Lake, ETL/ELT, MLflow, and data lifecycle

Detailed notes: [day-07-data-and-ml-platforms.md](day-07-data-and-ml-platforms.md)

### Coverage

- Databricks lakehouse, workspace, notebooks, compute, jobs, SQL, governance, ML, GenAI, Apps, and Agents.
- ETL versus ELT and Bronze/Silver/Gold medallion architecture.
- Delta Lake transactions, schema enforcement/evolution, time travel, batch/streaming, data quality, features, `MERGE`, partitioning, and small files.
- MLflow experiments, parameters, metrics, artifacts, Feature Store integration, registry, aliases, lineage, deployment, GenAI evaluation, promotion, and rollback.
- SQL/NoSQL/object/vector/cache roles in a data and AI platform.

### Practice

- Design a Bronze-to-Gold churn feature pipeline and a document-to-vector RAG ingestion pipeline.
- Show what is stored in Delta Lake, MLflow, object storage, the registry, and serving configuration.
- Create a candidate/challenger/champion promotion and rollback flow.

### Interview drill

- Lake versus warehouse versus lakehouse.
- ETL versus ELT; Bronze/Silver/Gold responsibilities.
- Schema enforcement versus evolution; time travel; `MERGE`.
- Experiment tracking versus registry versus serving versus monitoring.
- Delta Lake, MLflow, Unity Catalog, and Databricks relationship.

### Exit result

You can explain how governed data becomes reproducible features, models, RAG indexes, deployments, and auditable lineage.

## Day 8 — API deployment, MLOps/LLMOps, security, observability, and inference

Detailed notes: [day-08-production-mlops-and-security.md](day-08-production-mlops-and-security.md)

### Coverage

- DevOps versus MLOps versus LLMOps and control-plane versus data-plane responsibilities.
- FastAPI model/RAG/agent contracts, Pydantic validation, auth, authorization, rate/token/concurrency limits, standard errors, async jobs, and health endpoints.
- Model-in-process versus separate serving; batch, real-time, streaming, and edge patterns.
- CI/CD for models and GenAI, tests, canary, shadow, champion/challenger, and rollback.
- Data/model drift; infrastructure, application, model, RAG, agent, and business monitoring.
- Provider API versus self-hosting, batching, caching, quantization, streaming, and REST/gRPC.
- Fixed/sliding-window and token/leaky-bucket limiting; WAF/DDoS controls; safe logging, encryption, PII masking, poisoning defenses, prompt injection, jailbreaks, output filtering, RBAC, tenant isolation, governance, audit, and responsible AI.

### Practice

- Define production-ready prediction, RAG, ingestion-job, and agent-run endpoints.
- Build a release gate containing software tests, model/RAG evaluation, safety tests, canary signals, and rollback criteria.
- Trace one request across API, retrieval, model, tool, response, and audit.

### Interview drill

- Why `async` does not make CPU inference faster.
- Model loaded in API versus separate model server.
- Data drift versus concept/model drift.
- Provider API versus self-hosted model.
- What to monitor for ML, RAG, and agents.
- Defending against prompt injection and data exfiltration.

### Exit result

You can turn a model or GenAI workflow into a secure, observable, versioned, deployable, and reversible production service.

## Day 9 — Cloud, Kubernetes, Terraform, CI/CD, frontend, and developer experience

Detailed notes: [day-09-cloud-platform-and-delivery.md](day-09-cloud-platform-and-delivery.md)

### Coverage

- IBM Cloud/AWS/Azure/GCP service positioning, compute/storage/database choices, containers, networking, load balancing, secrets, naming/tags, scalability, availability, DR, RTO/RPO, and cost.
- AWS VPC, subnets, gateways, security groups/NACLs, EKS, ALB, RDS, Redis, S3, ECR, IAM, DNS, and TLS.
- Kubernetes Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, probes, resources, HPA, node scaling, graceful shutdown, and rollout styles.
- Helm charts/values/releases; Terraform state/modules/drift/environments; Jenkins build/promote/deploy/verify/rollback; Ansible operations.
- React/Next.js, Streamlit/Gradio, model playgrounds, streaming, citations, uploads, approval UX, recoverable errors, feedback, monorepo, configuration, local development, and DevEx.

### Practice

- Draw a multi-AZ cloud deployment for API, workers, databases, caches, object storage, vector search, and observability.
- Trace Git push to immutable image, staged Helm deployment, behavioral evaluation, promotion, and rollback.
- Design the browser upload and streaming-answer paths.

### Interview drill

- Scale-up versus scale-out; availability versus DR.
- Pod versus Deployment versus Service; readiness versus liveness.
- HPA versus node scaling versus application admission control.
- Terraform versus Helm versus Ansible.
- Rolling versus blue/green; build per environment versus promote one artifact.
- SSE versus WebSockets; direct browser-to-model versus backend gateway.

### Exit result

You can connect infrastructure, delivery, and product experience into one governed AI platform rather than treating deployment as an afterthought.

## Day 10 — Enterprise GenAI system design and Staff-level interview synthesis

Detailed notes: [day-10-enterprise-system-design.md](day-10-enterprise-system-design.md)

### Coverage

- IJP role expectations, watsonx/Granite positioning, and end-to-end ownership.
- Requirements, measurable NFRs, capacity, APIs, data model, HLD/LLD, synchronous/asynchronous paths, and evolution.
- Multi-tenant enterprise assistant, AgentRun platform, document assistant, and model-serving design patterns.
- Transactional outbox, at-least-once processing, state machines, reconciliation, fair tenancy, and graceful degradation.
- Cross-layer security, evaluation, observability, governance, cost, and release safety.
- Project storytelling, ownership, decisions, failure lessons, impact, and Staff-level trade-off language.

### Practice

- Complete a 45-minute design for one of:
  - multi-tenant enterprise RAG SaaS;
  - agent platform with approved tools;
  - enterprise document assistant;
  - model-serving and ingestion platform.
- Deliver a five-to-seven-minute version and a 90-second version.
- Answer follow-ups on scale, failure, security, quality, cost, and evolution.

### Interview drill

- Why QPS is insufficient without workflow/model concurrency.
- How to prevent a committed run from being lost before queue publication.
- How to handle duplicate messages and callbacks.
- When to use SQL, NoSQL, queues, caches, object storage, vector stores, and durable workflow engines.
- How to measure a GenAI system across technical, AI-quality, and business outcomes.
- How to present ownership, trade-offs, and a production failure.

### Exit result

You can give a Staff-level answer that moves from constraints to decisions, benefits, trade-offs, mitigations, metrics, and triggers to evolve.

## Final role-specific emphasis

| Role | Highest-priority days | Supporting days |
|---|---|---|
| Senior AI Engineer | 1, 3, 4, 7, 8, 10 | 2, 5, 6, 9 |
| Staff AI Engineer | 4, 5, 6, 8, 9, 10 | 1, 2, 3, 7 |
| GenAI Backend Engineer | 1, 2, 4, 5, 6, 8, 10 | 3, 7, 9 |
| AI Platform Engineer | 2, 7, 8, 9, 10 | 1, 3, 4, 5, 6 |

## Final cumulative check

By the end of Day 10, be able to explain from memory:

```text
Business problem
→ ML/GenAI problem choice
→ data and knowledge lifecycle
→ model/retrieval/tool architecture
→ API and state contracts
→ deployment and delivery
→ reliability and security
→ evaluation and observability
→ cost and governance
→ trade-offs and evolution
```
