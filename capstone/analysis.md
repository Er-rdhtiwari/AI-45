# Corpus analysis: `ijp`, `Python-AI`, and `revision`

## Scope and method

This analysis covers all 39 Markdown files in the three source folders:

| Folder | Files | Lines |
|---|---:|---:|
| `ijp` | 21 | 27,682 |
| `Python-AI` | 9 | 20,218 |
| `revision` | 9 | 26,356 |
| **Total** | **39** | **74,256** |

This file records the original three-folder consolidation analysis. The later four-folder audit also reviewed the two `project` files; its findings, project-claim checks, and final remediation record are in [final-review-report.md](final-review-report.md) and [project-scenario-mapping.md](project-scenario-mapping.md).

The review was performed in batches:

1. Python, software design, concurrency, DSA, and system design.
2. ML, EDA, NLP, LLMs, databases, and Python AI frameworks.
3. RAG, embeddings, evaluation, LangChain, LangGraph, and multi-agent systems.
4. Databricks, Delta Lake, MLflow, MLOps, APIs, cloud, and enterprise GenAI design.
5. The nine `revision` files, including the three large prior capstone summaries.

For every file, the review examined its heading structure and the sections containing definitions, examples, pseudocode or code, comparisons, production practices, risks, trade-offs, common mistakes, checklists, and interview questions.

The duplication scan found:

- 3,727 normalized topic headings.
- 264 headings that recur in at least two files.
- No exact repeated long prose blocks after normalization.

The duplication is therefore mainly **semantic overlap**: the notes explain the same concepts independently, often with different examples or levels of depth.

## Executive summary

The corpus is broad enough to support four related interview profiles:

- Senior AI Engineer
- Staff AI Engineer
- GenAI Backend Engineer
- AI Platform Engineer

Its strongest material is the production path from clean Python and data foundations through RAG, agent orchestration, MLOps, cloud deployment, governance, and end-to-end system design.

The most repeated material is:

1. RAG ingestion and query flow.
2. Embeddings, vector databases, metadata, top-k, hybrid retrieval, and reranking.
3. Hallucination, grounding, citations, and RAG evaluation.
4. LangChain and LangGraph concepts.
5. Security, multi-tenancy, observability, reliability, and cost.
6. Python error handling, logging, testing, OOP, and clean architecture.
7. “Common mistakes,” “best practices,” “interview Q&A,” and “final checklist” sections.

The final 10-day structure removes repetition by assigning each concept one primary home. Later days refer back to that canonical treatment and focus only on the new layer.

## Duplicate topic clusters

### 1. Vanilla RAG fundamentals

Repeated in:

- `ijp/w02/Day:8 RAG for Enterprise Knowledge.md`
- `revision/Day:1 Vanilla RAG.md`
- `revision/Day:6 Vanilla RAG and Frameworks.md`
- `revision/Day:8 Capstone Revision Day 2.md`
- `ijp/w03/Day:21 Enterprise GenAI Solution Design.md`
- portions of the database, NLP, LLM, LangChain, LlamaIndex, and prior capstone files

Repeated ideas:

- RAG as retrieval plus generation.
- Offline ingestion versus online query flow.
- Parsing, cleaning, chunking, embedding, indexing, retrieving, prompting, generating, and citing.
- RAG for private, current, controlled enterprise knowledge.
- RAG reduces but does not eliminate hallucination.

Best consolidated treatment:

- Use `revision/Day:1 Vanilla RAG.md` for the full causal chain and production failure modes.
- Use `ijp/w02/Day:8 RAG for Enterprise Knowledge.md` for the simplest first explanation.
- Use `ijp/w03/Day:21 Enterprise GenAI Solution Design.md` for the production architecture.

Canonical destination: **Day 4**.

### 2. Embeddings, vector stores, and retrieval

Repeated in:

- `ijp/w01/Day:5 NLP Fundamentals for IBM AI.md`
- `ijp/w01/Day:6 LLM Fundamentals Overview.md`
- `ijp/w01/Day7: Databases for AI Systems.md`
- `ijp/w02/Day:8 RAG for Enterprise Knowledge.md`
- `ijp/w02/Day:9 Embeddings and Vector Databases.md`
- `ijp/w02/Day:10 Advanced RAG Patterns.md`
- `revision/Day:1 Vanilla RAG.md`
- `revision/Day:2 LlamaIndex End to End.md`
- `revision/Day:7 Capstone Revision Day 1.md`
- `revision/Day:8 Capstone Revision Day 2.md`

Repeated ideas:

- Embeddings are numeric representations used for similarity.
- The indexing and querying sides must use compatible embedding spaces.
- Vector search handles semantic similarity; keyword search handles exact terms.
- Metadata improves relevance, freshness, access control, and citations.
- Top-k trades recall against noise, latency, and cost.

Best consolidated treatment:

- Use the NLP and LLM notes for conceptual grounding.
- Use the embeddings/vector database file for tool and metadata comparisons.
- Use Vanilla RAG and LlamaIndex for production schemas, versioning, access filters, and tuning.

Canonical destination: **Day 4**.

### 3. Advanced retrieval and RAG quality

Repeated in:

- `ijp/w02/Day:10 Advanced RAG Patterns.md`
- `ijp/w02/Day:11 Evaluating RAG Systems.md`
- `revision/Day:1 Vanilla RAG.md`
- `revision/Day:2 LlamaIndex End to End.md`
- `revision/Day:8 Capstone Revision Day 2.md`
- `ijp/w03/Day:21 Enterprise GenAI Solution Design.md`

Repeated ideas:

- Structure-aware, semantic, parent-child, and hierarchical chunking.
- Hybrid search, result fusion, reranking, query rewriting, multi-query retrieval, and contextual compression.
- Retrieval recall/precision and generation groundedness/faithfulness/relevance.
- Golden datasets, offline evaluation, online feedback, and continuous improvement.
- Citation validation, answerability checks, abstention, and freshness.

Consolidation decision:

- Day 4 owns the mechanisms and metrics.
- Day 5 uses those mechanisms only to explain framework choices.
- Day 10 uses them only inside the enterprise design exercise.

### 4. LangChain

Repeated in:

- `ijp/w02/Day:12 LangChain Fundamentals.md`
- `revision/Day:3 LangChain End to End.md`
- `revision/Day:6 Vanilla RAG and Frameworks.md`
- `revision/Day:8 Capstone Revision Day 2.md`
- `revision/Day:7 Capstone Revision Day 1.md`

Repeated ideas:

- Models, prompt templates, chains, retrievers, tools, parsers, memory/state, and callbacks.
- LangChain assembles LLM application components.
- A simple model call may not need a framework.
- LangChain overlaps with LlamaIndex but has a different center of gravity.
- LangGraph is preferred when explicit state, branches, loops, recovery, or approval are required.

Best consolidated treatment:

- Use the fundamentals file for the concise component map.
- Use the end-to-end revision file for production boundaries, structured output, observability, and framework risks.

Canonical destination: **Day 5**.

### 5. LangGraph, workflows, and agents

Repeated in:

- `ijp/w02/Day:13 LangGraph and Agentic AI.md`
- `revision/Day:4 LangGraph End to End.md`
- `revision/Day:6 Vanilla RAG and Frameworks.md`
- `revision/Day:8 Capstone Revision Day 2.md`
- `revision/Day:9 Capstone Revision Day 3.md`
- `Python-AI/Day:7 Trees Graphs DP Intro.md`
- `ijp/w03/Day:21 Enterprise GenAI Solution Design.md`

Repeated ideas:

- State, nodes, edges, routing, loops, tools, checkpoints, human approval, streaming, retries, and recovery.
- Deterministic workflow versus agentic workflow.
- Bounded autonomy and explicit policy checks.
- Small nodes, explicit state schemas, bounded loops, and idempotent side effects.
- Replay is not the same as business rollback.

Best consolidated treatment:

- Use the end-to-end LangGraph file for durable execution and production challenges.
- Use the IJP file for the simplest node/edge/state introduction.
- Use the enterprise solution and prior capstone for safety boundaries and system integration.

Canonical destination: **Day 6**.

### 6. Multi-agent systems

Repeated in:

- `ijp/w02/Day:14 Multi-Agent AI Overview.md`
- `revision/Day:8 Capstone Revision Day 2.md`
- `ijp/w03/Day:21 Enterprise GenAI Solution Design.md`
- agent sections in the LangGraph and system-design notes

Repeated ideas:

- Planner, researcher, critic/reviewer, executor, router, and escalation roles.
- Sequential, manager-worker, router-specialist, debate/critic, and human-review patterns.
- More agents increase cost, latency, coordination difficulty, and audit complexity.
- Role separation and shared state must be explicit.

Canonical destination: **Day 6**.

### 7. Python production engineering

Repeated in:

- `Python-AI/Day:1 Python Core & Environment.md`
- `Python-AI/Day:2 OOP in Python for AI.md`
- `Python-AI/Day:3 Python Advanced: Typing & Testing.md`
- `Python-AI/Day:4 Async and Concurrency in Python.md`
- `Python-AI/Day:8 GenAI Design Patterns.md`
- `revision/Day:7 Capstone Revision Day 1.md`

Repeated ideas:

- Configuration, logging, exceptions, type hints, validation, testing, and dependency injection.
- Provider-neutral interfaces and adapters.
- Composition over deep inheritance.
- Structured logging with correlation identifiers.
- Unit tests with deterministic fakes and a smaller real-provider integration suite.
- Clear synchronous versus asynchronous contracts.

Consolidation decision:

- Day 1 owns Python language and service engineering.
- Day 2 owns architecture patterns, APIs, persistence, and concurrency.

### 8. Reliability, security, observability, and cost

Repeated broadly across the system-design, RAG, framework, MCP, MLOps, API, cloud, and enterprise-design files.

Common controls:

- Timeouts, bounded retries, backoff, jitter, circuit breakers, bulkheads, backpressure, admission control, idempotency, dead-letter queues, and graceful degradation.
- Authentication, authorization, least privilege, tenant isolation, access filters before retrieval, secret management, encryption, approval, and audit.
- Metrics, structured logs, traces, quality evaluation, token usage, and cost.

Consolidation decision:

- Each day includes only controls specific to that layer.
- Day 8 owns operational implementation.
- Day 9 owns cloud/platform enforcement.
- Day 10 owns the full cross-layer design.

## Overlapping but distinct topics

These topics should not be collapsed into one concept.

| Topics | Shared area | Important distinction |
|---|---|---|
| Prompting vs RAG vs fine-tuning | Adapt model behavior or knowledge | Prompting supplies temporary instructions; RAG supplies runtime evidence; fine-tuning changes learned behavior or task patterns. |
| Embedding model vs generative LLM | Both are model components | Embeddings support representation and search; the generative model produces the answer. |
| Vector database vs retriever | Retrieval stack | A vector database stores/searches vectors; a retriever is the application-facing evidence interface and may combine several search methods. |
| SQL vs NoSQL vs vector store vs object store vs cache | Data persistence | Transactions/relations, flexible documents, semantic search, large immutable artifacts, and transient acceleration are different access patterns. |
| LlamaIndex vs LangChain | LLM application frameworks | LlamaIndex centers on data ingestion/index/retrieval/synthesis; LangChain centers on model/prompt/tool/application composition. |
| LangChain vs LangGraph | Application framework vs orchestration runtime | LangChain supplies components and agent harnesses; LangGraph provides explicit stateful control flow and recovery. |
| LangGraph vs MCP | Agent stack | LangGraph orchestrates; MCP standardizes external connectivity. |
| MCP vs function calling | Tool use | Function calling is a model-request format; MCP standardizes discovery and communication with tool/resource/prompt servers. |
| Workflow vs agent | Multi-step execution | Workflow paths are programmed; an agent makes bounded runtime choices. |
| Multi-agent vs one agent with tools | Autonomy | Multiple agents add specialized roles but also coordination, latency, and governance cost. |
| Async I/O vs threads vs processes | Concurrency | Async fits cooperative I/O; threads fit blocking I/O integration; processes fit CPU-heavy work. |
| Queue workers vs durable workflow engine | Background execution | Queues are simpler; durable engines own persisted state, timers, resumability, and workflow recovery. |
| Databricks vs Delta Lake vs MLflow | Data/AI platform | Databricks is the platform; Delta Lake is the reliable table/storage layer; MLflow manages experiments, models, traces, and lifecycle. |
| ETL vs ELT | Data pipelines | ETL transforms before loading; ELT loads raw data first and transforms inside the target platform. |
| Experiment tracking vs model registry vs serving vs monitoring | ML lifecycle | They answer what was tried, what is approved, what is deployed, and how it behaves. |
| DevOps vs MLOps vs LLMOps | Delivery and operations | MLOps adds data/model lifecycle; LLMOps adds prompts, retrieval, traces, evaluation, tools, safety, and token cost. |
| Availability vs disaster recovery | Reliability | Availability keeps the service operating; disaster recovery restores it after a major loss and is described by RTO/RPO. |
| Terraform vs Helm vs Ansible | Automation | Terraform provisions infrastructure, Helm packages Kubernetes releases, and Ansible automates host/application operations. |
| Readiness vs liveness vs startup probe | Kubernetes health | Traffic eligibility, restart health, and slow-start protection are separate decisions. |
| Technical metrics vs AI-quality metrics vs business metrics | Measurement | Healthy infrastructure does not prove a grounded answer or useful product outcome. |

## Unique or lightly repeated topics

### Unique to the Python and software-engineering material

- Python environment roles of `venv`, `pyenv`, and `uv`.
- Mutable defaults, import-time side effects, circular imports, comprehensions, slicing, and collection-specific pitfalls.
- Protocols, abstract base classes, dataclasses, Pydantic, dunder methods, and exception translation.
- Async event-loop mechanics, coroutines/tasks, `gather`, task groups, semaphores, blocking calls, race conditions, and background-job limits.
- DSA patterns: prefix sum, hashing, two pointers, sliding window, monotonic stack, BFS/DFS, topological sort, and 0/1 knapsack.

### Unique to ML, NLP, and model foundations

- EDA treatment of missing values, duplicates, outliers, categorical encoding, scaling, and leakage-safe preprocessing.
- Traditional NLP: stop words, stemming, lemmatization, bag of words, TF-IDF, NER, sentiment, word versus sentence embeddings.
- Classical algorithms and math refresh: linear/logistic regression, trees/forests, vectors, matrices, gradients, probability, and Bayes.
- Transformer internals: attention, query/key/value, multi-head attention, positional information, and encoder/decoder families.
- Computer vision, CNNs, transfer learning, multimodal systems, diffusion, VAE/GAN comparisons.
- RLHF, DPO, LoRA, QLoRA, PEFT, fine-tuning data preparation, and catastrophic forgetting.

### Unique to frameworks and protocols

- LlamaIndex documents, nodes, query engines, response synthesizers, and index families.
- MCP host/client/server roles; tools, resources, prompts; JSON-RPC; capability negotiation; and session lifecycle.
- CrewAI and Semantic Kernel basics plus AutoGen, A2A, ADK, and low-code/n8n positioning.

### Unique to data platforms and MLOps

- Databricks workspace, notebooks, compute, jobs, SQL, Apps, Agents, and Unity Catalog.
- Delta Lake ACID transactions, schema enforcement/evolution, time travel, `MERGE`, medallion layers, and small-file/partition concerns.
- MLflow parameters, metrics, artifacts, aliases, lineage, champion/challenger promotion, and rollback.
- Model drift versus data drift; batch, streaming, real-time, and edge deployment.
- Model-serving runtimes, batching, quantization, and provider API versus self-hosting.

### Unique to platform engineering and productization

- Terraform state, locking, drift, modules, and environment isolation.
- AWS VPC/subnets, EKS, ALB, RDS, Redis, S3, ECR, IAM, Route 53, and certificates.
- Kubernetes/Helm probes, releases, rollouts, graceful stream draining, HPA, and node scaling.
- Jenkins pipeline stages, immutable artifacts, promotion, smoke tests, and rollback.
- Ansible operations automation.
- React/Next.js, streaming UX, citations, feedback, signed uploads, and tool-approval UX.
- Monorepo, configuration alignment, local development, shared API types, and developer experience.
- Leadership, STAR-plus-architecture storytelling, ownership, failure lessons, and measurable impact.

### Unique to IBM IJP positioning

- Differences between the two role descriptions.
- Band 08 expectations: end-to-end ownership, architecture decisions, stakeholder communication, and mentoring.
- Mapping backend, cloud, CI/CD, and automation experience into AI/Data Scientist responsibilities.
- IBM/Databricks/GenAI interview framing and the end-to-end AI project lifecycle.

## Source-to-day coverage ledger

Every source file has a primary destination. A secondary destination means only its distinct material is carried forward there.

| # | Source file | Primary day | Secondary use | Important material retained |
|---:|---|---:|---:|---|
| 1 | `Python-AI/Day:0 System Design Interview Coaching.md` | 10 | 2, 8 | Six-phase design method, capacity, APIs, data models, AgentRun architecture, outbox, idempotency, reliability, interview script. |
| 2 | `Python-AI/Day:1 Python Core & Environment.md` | 1 | 8 | Core Python, collections, functions, environments, configuration, logging, exceptions, pytest, project layout. |
| 3 | `Python-AI/Day:2 OOP in Python for AI.md` | 1 | 2 | OOP, protocols, dataclasses, composition, SOLID, provider adapters, RAG design exercise, production pitfalls. |
| 4 | `Python-AI/Day:3 Python Advanced: Typing & Testing.md` | 1 | 8 | Static typing, Pydantic, exception hierarchy, structured logging, correlation IDs, fixtures, mocks, contract/evaluation tests. |
| 5 | `Python-AI/Day:4 Async and Concurrency in Python.md` | 2 | 8 | Event loop, tasks, gather/task groups, timeouts, semaphores, threads/processes, race conditions, background work. |
| 6 | `Python-AI/Day:5 DSA Patterns Interview Prep.md` | 2 | — | Complexity, arrays, strings, hashing, prefix sums, subarrays, frequency maps, two-sum. |
| 7 | `Python-AI/Day:6 DSA Core II Overview.md` | 2 | — | Two pointers, sliding windows, stacks, monotonic stacks, queues, BFS connection. |
| 8 | `Python-AI/Day:7 Trees Graphs DP Intro.md` | 2 | 6 | Trees, graph representation, DFS/BFS, DAGs, topological sorting, DP, knapsack, workflow connection. |
| 9 | `Python-AI/Day:8 GenAI Design Patterns.md` | 2 | 1, 5 | SOLID, Factory/Strategy/Adapter/Decorator/Facade, layered architecture, dependency direction, project structure, trade-offs. |
| 10 | `ijp/w01/Day:1 IBM IJP Roles Preparation.md` | 10 | 3, 7 | Role expectations, lifecycle ownership, business framing, stakeholder/mentoring expectations, skills map. |
| 11 | `ijp/w01/Day:2 ML Fundamentals for IBM IJP.md` | 3 | 7, 8 | ML types, metrics, over/underfitting, workflow, leakage, versioning, drift, production lifecycle. |
| 12 | `ijp/w01/Day:3 Python AI Frameworks Overview.md` | 3 | 7 | NumPy, Pandas, scikit-learn, PyTorch, TensorFlow/Keras, Hugging Face, framework selection. |
| 13 | `ijp/w01/Day:4 EDA Data Preprocessing Overview.md` | 3 | 7 | EDA, missing data, duplicates, outliers, encoding, scaling, feature engineering, leakage-safe pipelines. |
| 14 | `ijp/w01/Day:5 NLP Fundamentals for IBM AI.md` | 3 | 4 | NLP preprocessing, tokenization, BoW, TF-IDF, embeddings, classification, NER, sentiment, RAG connection. |
| 15 | `ijp/w01/Day:6 LLM Fundamentals Overview.md` | 3 | 4, 5 | Foundation models, training stages, prompting, tokens, sampling, open/commercial trade-offs, risks, use cases. |
| 16 | `ijp/w01/Day7: Databases for AI Systems.md` | 2 | 4, 7 | SQL, joins, aggregation, NoSQL, document/chunk/embedding/interaction storage, metadata and cache integration. |
| 17 | `ijp/w02/Day:8 RAG for Enterprise Knowledge.md` | 4 | 10 | Concise RAG explanation, components, two flows, basic evaluation, enterprise controls. |
| 18 | `ijp/w02/Day:9 Embeddings and Vector Databases.md` | 4 | 2 | Embeddings, cosine similarity, FAISS/Chroma/Pinecone/Weaviate/Milvus, filters, top-k, mistakes. |
| 19 | `ijp/w02/Day:10 Advanced RAG Patterns.md` | 4 | 5 | Hybrid search, reranking, rewriting, multi-query, compression, long documents, hallucination reduction. |
| 20 | `ijp/w02/Day:11 Evaluating RAG Systems.md` | 4 | 8 | Retrieval/answer metrics, groundedness, faithfulness, golden sets, offline/online feedback loops. |
| 21 | `ijp/w02/Day:12 LangChain Fundamentals.md` | 5 | — | Concise LangChain component model, RAG flow, benefits and limitations. |
| 22 | `ijp/w02/Day:13 LangGraph and Agentic AI.md` | 6 | 5 | Agent basics, nodes/edges/state, routing, tools, human review, risks and enterprise cases. |
| 23 | `ijp/w02/Day:14 Multi-Agent AI Overview.md` | 6 | 5 | Agent roles, orchestration patterns, CrewAI, Semantic Kernel, governance, when multi-agent is overkill. |
| 24 | `ijp/w03/Day:15 Databricks Fundamentals Overview.md` | 7 | 9 | Lakehouse, workspace, notebooks, compute, jobs, SQL, governance, ML/GenAI/Apps/Agents. |
| 25 | `ijp/w03/Day:16 Delta Lake ETL-ELT Guide.md` | 7 | 8 | ACID, schema, time travel, Bronze/Silver/Gold, batch/streaming, quality, `MERGE`, partitioning. |
| 26 | `ijp/w03/Day:17 MLflow for ML Lifecycle.md` | 7 | 8 | Tracking, parameters, metrics, artifacts, registry, aliases, lineage, serving, GenAI evaluation, rollback. |
| 27 | `ijp/w03/Day:18 MLOps for AI Systems.md` | 8 | 7, 9 | CI/CD for ML, testing, deployment modes, drift, monitoring, governance, responsible AI, canary/champion-challenger. |
| 28 | `ijp/w03/Day:19 Deploying ML Models API.md` | 8 | 2, 9 | FastAPI, validation, auth, limits, logs, observability, async jobs, serving patterns, RAG/agent APIs. |
| 29 | `ijp/w03/Day:20 Cloud AI Architecture Guide.md` | 9 | 8, 10 | Compute/storage/databases, containers, Kubernetes, networking, secrets, scaling, HA/DR, cost, full cloud AI design. |
| 30 | `ijp/w03/Day:21 Enterprise GenAI Solution Design.md` | 10 | 4, 6, 8, 9 | Complete enterprise assistant design, requirements, ingestion, retrieval, agents, APIs, evaluation, governance, deployment. |
| 31 | `revision/Day:1 Vanilla RAG.md` | 4 | 10 | Deep RAG explanation, dependencies, failure modes, optimization, reliability, metrics, Staff-level framing. |
| 32 | `revision/Day:2 LlamaIndex End to End.md` | 5 | 4 | Documents/nodes/indexes/retrievers/query engines/synthesis, production concerns, framework boundaries. |
| 33 | `revision/Day:3 LangChain End to End.md` | 5 | 6 | Models/prompts/tools/chains/state/structured output, production risks, tests, framework decisions. |
| 34 | `revision/Day:4 LangGraph End to End.md` | 6 | 8 | State schema, nodes, edges, checkpoints, durability, recovery, loops, HITL, controlled autonomy. |
| 35 | `revision/Day:5 MCP End to End.md` | 5 | 6, 9 | Protocol roles, tools/resources/prompts, JSON-RPC, sessions, governance, narrow tools, platform adoption. |
| 36 | `revision/Day:6 Vanilla RAG and Frameworks.md` | 5 | 4, 6 | Layered comparison of RAG, LlamaIndex, LangChain, LangGraph, MCP; selection and boundary rules. |
| 37 | `revision/Day:7 Capstone Revision Day 1.md` | 1 | 2, 7, 9 | Consolidated Python, DSA, APIs, SQL/NoSQL, Redis, vectors, ETL, cloud/Kubernetes, interview Q&A. |
| 38 | `revision/Day:8 Capstone Revision Day 2.md` | 3 | 4, 5, 6, 8 | ML/DL/transformers/LLMs/multimodal/prompting/RAG/agents/fine-tuning/serving/security. |
| 39 | `revision/Day:9 Capstone Revision Day 3.md` | 9 | 10 | Terraform/AWS/Kubernetes/Helm/Jenkins/Ansible/frontend/DevEx/system design/leadership. |

## Second-pass gap audit

After the first consolidation, a second heading-to-notes and concept-level comparison was run across all 39 source files. It found several useful details that were present in the sources but were either implicit or too briefly represented in the first draft. The daily notes were expanded to make these topics explicit:

- Python: iterators, generators, context managers, `mypy`, Arrange–Act–Assert, class versus instance state, overriding, Pydantic validation boundaries, and correlation IDs.
- Backend and DSA: CRUD, ORM and N+1 queries, decorators versus middleware, Flask versus FastAPI, locks and cancellation, `concurrent.futures`, API-breaking changes, Big-O, graph representation, anagrams, longest-substring, balanced-parentheses, and monotonic-stack patterns.
- ML and LLM foundations: classical ML baselines, prompt-engineering patterns, fine-tuning objectives and data quality, context windows, BLEU, ROUGE, LLM-as-judge, and human evaluation.
- RAG and agent systems: vector similarity metrics, index families, vector-database trade-offs, context pollution, LangSmith, MCP versus A2A, MCP adoption criteria, agent memory, and shared-state ownership.
- Platform and production: Databricks Apps and Agents, DevOps/MLOps/LLMOps boundaries, control plane versus data plane, rate-limiting algorithms, WAF/DDoS controls, PII masking, data-poisoning defenses, and responsible-AI principles.
- Cloud, delivery, and architecture: multi-cloud service mapping, watsonx positioning, load balancing, naming/tagging conventions, Streamlit/Gradio, model playgrounds, Jenkins controller/agent structure, detailed low-level design, staff-level ambiguity trade-offs, and IJP role emphasis.

This pass did not change the 10-day structure; it strengthened the affected daily notes without duplicating whole explanations.

## Prior validation pass

The prior 115-topic validation found ten remaining depth/example gaps rather than missing broad subject areas:

- long-running API completion through polling, webhooks, SSE, and WebSockets;
- relational one-to-many, ACID, isolation, and concurrency controls;
- `gather` failure results, task lifecycle, and bridging blocking libraries with `asyncio.to_thread`;
- classical-ML/framework task selection beyond the four existing baselines;
- EDA variable types plus boxplot/IQR outlier treatment;
- PyTorch/TensorFlow/Hugging Face task examples and tensor positioning;
- neural activation and task-loss examples;
- API Gateway versus ALB versus NLB;
- frontend server/UI/stream/authentication state ownership;
- branch, environment, and promotion workflow.

The affected Day 2, Day 3, and Day 9 notes were strengthened using only the source corpus. A later final review found additional compactness, terminology, link, and project-evidence issues not represented in that 115-topic checklist; those are recorded in [final-review-report.md](final-review-report.md).

## Consolidation rules used in the final notes

1. Define a concept once, in its primary day.
2. Preserve a second explanation only when it adds a distinct mental model.
3. Keep one representative example per concept family; retain additional examples only when they expose a new production risk.
4. Keep comparisons where two topics are often confused.
5. Preserve high-signal interview questions, not every rewording of the same question.
6. Preserve production failure modes and mitigations even when introductory explanations are condensed.
7. Preserve security, governance, and tenant-isolation guidance at the layer where enforcement occurs.
8. Use framework-neutral interfaces and architecture as the baseline; frameworks remain implementation choices.
9. Separate deterministic software correctness from probabilistic AI quality.
10. Keep the original folders as the detailed reference corpus; the `capstone` folder is the deduplicated revision path.
