# AI engineering interview revision capstone

This folder is a deduplicated revision path audited against all 41 Markdown source files in `ijp`, `Python-AI`, `revision`, and `project`.

The four source folders contain 75,285 lines. Concepts have one primary revision home, while the two real projects supply evidence-backed scenarios and interview framing. The original folders remain the detailed reference library and were not modified.

## Start here

1. Read [final-review-report.md](final-review-report.md) for the final four-folder audit, fixes, and unresolved boundaries.
2. Read [project-scenario-mapping.md](project-scenario-mapping.md) for the real-project evidence used on each day.
3. Read [analysis.md](analysis.md) for the original duplicate, overlap, unique-topic, and 39-file source-coverage analysis.
4. Follow [10-day-revision-plan.md](10-day-revision-plan.md) for the schedule and daily practice.
5. Use the detailed day files below and their source links when a deeper reference is needed.

## Daily revision notes

| Day | Focus | Detailed notes |
|---:|---|---|
| 1 | Production Python, OOP, typing, validation, errors, logging, and testing | [day-01-python-engineering.md](day-01-python-engineering.md) |
| 2 | Backend patterns, APIs, databases, concurrency, reliability, and DSA | [day-02-backend-dsa-and-concurrency.md](day-02-backend-dsa-and-concurrency.md) |
| 3 | ML, EDA, NLP, deep learning, transformers, LLMs, and fine-tuning | [day-03-ml-data-llm-foundations.md](day-03-ml-data-llm-foundations.md) |
| 4 | RAG, embeddings, vector/keyword/hybrid retrieval, reranking, and evaluation | [day-04-rag-and-retrieval.md](day-04-rag-and-retrieval.md) |
| 5 | LlamaIndex, LangChain, MCP, boundaries, governance, and framework selection | [day-05-frameworks-and-mcp.md](day-05-frameworks-and-mcp.md) |
| 6 | LangGraph, agent workflows, multi-agent patterns, safety, durability, and evaluation | [day-06-agents-and-langgraph.md](day-06-agents-and-langgraph.md) |
| 7 | Databricks, Delta Lake, ETL/ELT, MLflow, lineage, promotion, and rollback | [day-07-data-and-ml-platforms.md](day-07-data-and-ml-platforms.md) |
| 8 | APIs, serving, MLOps/LLMOps, security, inference, monitoring, and governance | [day-08-production-mlops-and-security.md](day-08-production-mlops-and-security.md) |
| 9 | Cloud, AWS, Kubernetes, Helm, Terraform, CI/CD, frontend, and DevEx | [day-09-cloud-platform-and-delivery.md](day-09-cloud-platform-and-delivery.md) |
| 10 | Enterprise architecture, AgentRun design, Staff-level trade-offs, and project storytelling | [day-10-enterprise-system-design.md](day-10-enterprise-system-design.md) |

## Topic navigation

### Senior AI Engineer

Prioritize:

- Day 1 for reliable Python and testability.
- Day 3 for ML/LLM fundamentals.
- Day 4 for RAG design and evaluation.
- Day 7 for data/model lifecycle.
- Day 8 for production MLOps.
- Day 10 for system design and ownership.

### Staff AI Engineer

Prioritize:

- Day 4 for quality decomposition.
- Day 5 for architecture boundaries and framework selection.
- Day 6 for controlled autonomy.
- Days 8–9 for operational/platform ownership.
- Day 10 for trade-offs, evolution, and leadership framing.

### GenAI Backend Engineer

Prioritize:

- Days 1–2 for service implementation.
- Day 4 for the retrieval path.
- Days 5–6 for frameworks, MCP, and agents.
- Day 8 for secure APIs and operations.
- Day 10 for end-to-end design.

### AI Platform Engineer

Prioritize:

- Day 2 for contracts, state, queues, and persistence.
- Day 7 for governed data/model lifecycle.
- Day 8 for MLOps/LLMOps.
- Day 9 for infrastructure and delivery.
- Day 10 for complete platform architecture.

## Canonical topic ownership

This map prevents unnecessary rereading:

| Topic | Canonical day |
|---|---:|
| Python language/service engineering | 1 |
| OOP, protocols, validation, logging, testing | 1 |
| APIs, databases, caching, concurrency | 2 |
| DSA patterns and graph/DP recognition | 2 |
| ML, EDA, NLP, transformers, LLM foundations | 3 |
| Prompting versus RAG/tools/fine-tuning | 3 |
| RAG ingestion/query, retrieval, evaluation | 4 |
| LlamaIndex, LangChain, MCP | 5 |
| LangGraph, agents, multi-agent systems | 6 |
| Databricks, Delta Lake, MLflow | 7 |
| MLOps, APIs, serving, security, monitoring | 8 |
| Cloud, Kubernetes, Terraform, CI/CD, frontend | 9 |
| Enterprise GenAI system design and leadership | 10 |

## Core interview memory map

```text
Business problem
→ choose deterministic, ML, RAG, or agent approach
→ establish data and knowledge lifecycle
→ define service, model, retrieval, and tool contracts
→ separate interactive and asynchronous work
→ deploy through governed platform controls
→ measure reliability, AI quality, cost, and business outcome
→ state trade-offs and evolution triggers
```

For design answers:

```text
requirements
→ NFRs
→ capacity
→ APIs
→ data model
→ architecture
→ reliability
→ security
→ observability/evaluation
→ cost
→ trade-offs
→ evolution
```

For every major decision:

```text
constraint
→ decision
→ benefit
→ trade-off
→ mitigation
→ metric
→ trigger to revisit
```

## Source coverage

The final audit and remediation record is in [final-review-report.md](final-review-report.md). The original 39-file `ijp`/`Python-AI`/`revision` audit trail and primary/secondary day mapping is in the [source-to-day coverage ledger](analysis.md#source-to-day-coverage-ledger); the two project files are traced separately in [project-scenario-mapping.md](project-scenario-mapping.md).

## Files in this folder

```text
capstone/
├── README.md
├── analysis.md
├── 10-day-revision-plan.md
├── final-review-report.md
├── project-scenario-mapping.md
├── day-01-python-engineering.md
├── day-02-backend-dsa-and-concurrency.md
├── day-03-ml-data-llm-foundations.md
├── day-04-rag-and-retrieval.md
├── day-05-frameworks-and-mcp.md
├── day-06-agents-and-langgraph.md
├── day-07-data-and-ml-platforms.md
├── day-08-production-mlops-and-security.md
├── day-09-cloud-platform-and-delivery.md
└── day-10-enterprise-system-design.md
```
