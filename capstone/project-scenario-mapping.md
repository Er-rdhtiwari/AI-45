# Project scenario mapping across the 10 capstone days

## Source projects and evidence rule

| Label | Project | Evidence used |
|---|---|---|
| P1 | **DPDK Automation for Network Packet Processing** | AMD-centric benchmark automation: Ansible, Python BIOS/Redfish and Xena integration, command templates, parallel statistics, workload-specific parsers, structured database-backed reporting, multi-server campaigns, UI/dashboard collaboration, and team leadership. |
| P2 | **DPDK BenchOps Copilot** | AI evolution of P1: LlamaIndex ingestion/retrieval, LangChain model/tool composition, LangGraph workflow control, MCP deterministic tools, Postgres plus S3/MinIO truth/artifacts, vector indexing, FastAPI, Kubernetes/Helm/HPA/Jenkins, AI evaluation gates, and operational safeguards. |

Only facts present in the two files under `project/` are treated as implemented. Transferable interpretations are described as concept applications. Anything proposed beyond those files is marked **Hypothetical**.

## Day-by-day mapping

| Day / note | Project scenarios added | Concept connection | Senior/Staff interview emphasis | Evidence gap or hypothetical boundary |
|---|---|---|---|---|
| [Day 1 — Production Python](day-01-python-engineering.md) | P1 reusable Python BIOS, Xena, stats-processing, CLI, and parser boundaries; P2 separation of AI reasoning from deterministic services. | Cohesion, composition, real reuse points, SOLID-style responsibility boundaries, and dependency direction. | Senior deep-dives one module contract; Staff explains how shared platform capabilities were separated from workload-specific logic and how probabilistic/deterministic boundaries governed the AI evolution. | No evidence of protocols, ABCs, Pydantic, `mypy`, or a named Python test framework. |
| [Day 2 — Backend, concurrency, databases, APIs, and DSA](day-02-backend-dsa-and-concurrency.md) | P1 multi-server campaigns, ordered scenario execution, parallel statistics, parsing, and persistence; P2 FastAPI/storage/tool boundaries. | Concurrency versus required ordering, orchestration state, access-pattern-driven storage, adapters/facades, and deterministic operations. | Senior traces one scenario/request; Staff covers capacity, partial failure, correlation, ownership, and storage evolution. | No evidence of `asyncio`, a queue, transactional outbox, cursor pagination, or a named relational/vector product. DSA-specific project examples were not forced. |
| [Day 3 — ML, data, NLP, and LLM foundations](day-03-ml-data-llm-foundations.md) | P1 deterministic parsing and comparison instead of unnecessary ML; P2 selection of RAG, tools, and LLM synthesis instead of documented fine-tuning. | Start with the business decision; allocate deterministic parsing, current/private knowledge, live truth, actions, and language synthesis to the right mechanisms. | Senior traces data and one regression query; Staff explains failure-mode allocation and why fine-tuning would not solve freshness, provenance, or execution safety. | No fine-tuned model, training pipeline, supervised labels, model choice, or quantitative model metric is documented. |
| [Day 4 — RAG and retrieval](day-04-rag-and-retrieval.md) | P1 truth-bearing documents, templates, logs, metrics, and comparisons become P2’s multi-source benchmark-aware RAG corpus. | Normalization, phase-aware chunks, workload/platform/source/run metadata, hybrid retrieval, tool-assisted live truth, verification, citations, and separate truth/index storage. | Senior diagnoses ingestion/retrieval/generation failures; Staff leads with trust, lineage, index publication, evaluation, and evolution triggers. | No named vector DB, lexical engine, embedding model, ANN index, reranker, top-k, or numeric retrieval result. |
| [Day 5 — LlamaIndex, LangChain, MCP, and framework selection](day-05-frameworks-and-mcp.md) | P2 responsibility map across LlamaIndex, LangChain, LangGraph, MCP, Postgres/S3/MinIO, and vector storage; narrow `RunQuery`, `LogFetch`, `RunDiff`, and `CommandBuilder` tools. | Correct framework/protocol category, least-privilege tools, allowlisted templates, audit, and human gate for BIOS/reboot operations. | Senior explains contracts and failure behavior; Staff justifies each layer from a distinct responsibility and accounts for dependency/upgrade/operations cost. | MCP transport, JSON-RPC traces, capability negotiation, sessions, and server topology are not documented. |
| [Day 6 — Agents and LangGraph](day-06-agents-and-langgraph.md) | P2 hybrid flow: model-assisted intent/synthesis plus deterministic retrieval, comparison, plan validation, command construction, parsing, verification, and BIOS approval. | Controlled autonomy, explicit workflow, bounded tool set, human-in-the-loop, audit, and verification. | Senior draws nodes/edges and failures; Staff explains risk-based autonomy and how governance, evaluation, and deployment rollback fit together. | No evidence of checkpoint persistence, replay, long-term memory, or multi-agent implementation. A multi-agent extension is discussed only as **Hypothetical**. |
| [Day 7 — Data and ML platforms](day-07-data-and-ml-platforms.md) | P1 raw logs/stats to normalized metrics and dashboards; P2 multi-source knowledge to normalized chunks, semantic index, evaluated publication, and traced behavior. | Transferable raw/validated/serving layers, lineage, data quality, truth versus retrieval stores, and the RAG data-product lifecycle. | Senior traces raw-to-serving lineage; Staff treats the index as a governed product with quality gates, publication, rollback, and freshness. | **No direct Databricks, Spark, Delta Lake, Unity Catalog, MLflow, feature-store, or model-registry example was available.** A lakehouse/MLflow evolution is explicitly **Hypothetical**. |
| [Day 8 — Production MLOps and security](day-08-production-mlops-and-security.md) | P2 FastAPI/Kubernetes/Helm/HPA/Jenkins delivery and CI gates; P1 command/BIOS risk inherited into P2’s allowlisted MCP tools, audit, verification, and approval. | LLMOps evaluation, behavior-aware releases, timeouts/retries/circuit protection, constrained capabilities, human approval, and risk-tiered controls. | Senior explains a release and one safe tool call; Staff defines the cross-component quality contract, ownership, and risk tiers. | No exact thresholds, availability, traffic, tenant isolation, OAuth/OIDC/JWT, WAF/DDoS, PII, encryption, or secrets-product implementation. |
| [Day 9 — Cloud, platform, and delivery](day-09-cloud-platform-and-delivery.md) | P1 Ansible roles across Ubuntu/RHEL, compilers, tools, BIOS/Xena coordination, and dashboard UX; P2 Kubernetes/Helm/HPA/Jenkins/FastAPI delivery and behavior gates. | Configuration management, deployment responsibilities, scaling limits, behavior-aware CI/CD, rollback, parameter/default/comparison UX, and trust via citations. | Senior explains role/deployment details; Staff justifies platform boundaries, independent failure/scale domains, and UX as a safety surface. | **No direct Terraform or named cloud-provider example was available.** No frontend framework, registry, ingress, probe, network, rollout, or HPA-signal detail is documented. Terraform/workload-separation evolution is **Hypothetical**. |
| [Day 10 — Enterprise system design](day-10-enterprise-system-design.md) | Full P1 → P2 evolution from deterministic benchmark platform to grounded AI copilot, including requirements, architecture, hard decisions, outcomes, and interview scripts. | Problem-to-production design, truth and retrieval layers, deterministic tools, approval, evaluation, deployment safeguards, trade-off formula, and organizational leverage. | Includes a 90-second Senior story and a Staff synthesis centered on platform evolution, risk allocation, metrics, leadership, and revisit triggers. | Capacity/SLOs, cloud/Terraform, Databricks/MLflow, multi-agent, outbox/queue, checkpoints, tenancy, and frontend details are not evidenced; proposed evolutions are **Hypothetical**. |

## Coverage result

Every capstone day had at least one natural project scenario, so **no entire capstone note was left without a project example**.

The following narrower topics intentionally have no claimed implementation example:

- Day 2: DSA algorithms, transactional outbox, and a named async/queue stack.
- Day 3: supervised model training, fine-tuning, and model-training metrics.
- Day 4: specific embedding, vector-index, reranker, and top-k choices.
- Day 6: multi-agent execution, durable checkpoints, replay, and long-term memory.
- Day 7: Databricks, Spark, Delta Lake, Unity Catalog, MLflow, feature store, and model registry.
- Day 8: detailed identity/tenant/PII/WAF/encryption implementation.
- Day 9: Terraform, a named cloud provider, cloud networking, a frontend framework, and detailed Kubernetes rollout/probe configuration.

These gaps are highlighted so the interview narrative stays accurate and does not turn reasonable architecture options into invented project history.

## Cross-project storyline to reuse

```text
P1 established deterministic operational truth:
  domain documentation
  + repeatable environments and BIOS profiles
  + command templates and execution
  + raw logs/statistics
  + workload-specific parsers
  + structured comparisons

P2 used that foundation safely:
  benchmark-aware ingestion and retrieval
  + cited synthesis
  + deterministic tools
  + controlled workflow and verification
  + evaluation and deployment safeguards
```

The strongest interview message is not that many tools were used. It is that the architecture evolved in two deliberate stages: first make the operation repeatable and observable; then add AI only where it improved knowledge access and reasoning without taking control away from deterministic systems.
