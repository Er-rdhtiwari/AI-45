# Revision Day 1 — Data Science, ML and Data Foundations

```text
Act as a senior Data Scientist and beginner-friendly AI mentor.

Today is Revision Day 1 of my IBM AI/GenAI preparation.

Create comprehensive revision notes covering the Data Scientist role, AI project lifecycle, Machine Learning, EDA, data preprocessing, Python AI frameworks and data storage.

Group connected topics together instead of following the original study days separately. Avoid repeating the same explanation in multiple sections.

Cover:

1. Data Scientist role and AI project lifecycle
   - What an enterprise Data Scientist does
   - Difference between data analysis, Machine Learning, GenAI and AI solution architecture
   - Responsibilities of a senior or Band 08 Data Scientist
   - Understanding a business problem
   - Converting a business problem into an ML or AI problem
   - Defining business goals and technical success metrics
   - Data collection
   - Data preparation
   - Model development
   - Evaluation
   - Deployment
   - Monitoring
   - Continuous improvement
   - How backend, cloud, API, CI/CD and automation experience supports AI projects

2. Machine Learning foundations
   - What Machine Learning is
   - Supervised and unsupervised learning
   - Classification
   - Regression
   - Clustering
   - Features
   - Labels
   - Predictions
   - Training, validation and test datasets
   - Train/test split
   - Cross-validation
   - Baseline models
   - Model selection
   - Hyperparameters
   - Overfitting
   - Underfitting
   - Bias and variance

3. Model evaluation
   - Confusion matrix
   - Accuracy
   - Precision
   - Recall
   - F1-score
   - ROC-AUC
   - Class imbalance
   - Prediction thresholds
   - MAE
   - MSE
   - RMSE
   - How business requirements influence metric selection
   - Why accuracy alone may be misleading

4. EDA and data preprocessing
   - Data shape
   - Columns and data types
   - Numerical and categorical variables
   - Summary statistics
   - Missing values
   - Duplicate records
   - Outliers
   - Data distributions
   - Correlation
   - Encoding categorical variables
   - Feature scaling
   - Normalization
   - Feature engineering
   - Feature selection
   - Data leakage
   - Why preprocessing must be fitted only on training data
   - Using pipelines to apply consistent preprocessing

5. Python AI ecosystem
   - NumPy
   - Pandas
   - Matplotlib
   - Scikit-learn
   - TensorFlow
   - Keras
   - PyTorch
   - Hugging Face
   - When each framework should be used
   - How these frameworks work together in an enterprise AI project

6. SQL, NoSQL and AI application storage
   - Tables, rows and columns
   - Primary keys
   - Filtering
   - Joins
   - Grouping
   - Aggregations
   - Relational databases
   - Document databases
   - Key-value databases
   - SQL vs NoSQL
   - Storing training data
   - Storing features and predictions
   - Storing documents and document chunks
   - Storing metadata
   - Storing user queries and model responses
   - How databases connect with ML, RAG and API applications

Use one consistent business example, such as customer churn prediction, to connect the concepts.

Output format:
- 5-line beginner summary
- Clear headings and subheadings
- Detailed but simple explanations
- Key definitions
- Easy examples
- Comparison tables where useful
- ASCII diagram showing the end-to-end ML lifecycle
- Pseudocode for a complete ML workflow
- Explanation of the relationship between EDA, preprocessing, training and evaluation
- Common confusions and mistakes
- Memory aids and simple rules
- Concise final recap
```

---

# Revision Day 2 — NLP, Embeddings, Foundation Models and LLMs

```text
Act as a senior NLP, LLM and enterprise AI mentor.

Today is Revision Day 2 of my IBM AI/GenAI preparation.

Create comprehensive revision notes covering unstructured data, traditional NLP, embeddings, foundation models, LLMs, prompting, fine-tuning and enterprise LLM use cases.

Organize the notes to show how traditional NLP concepts evolved into modern LLM applications. Avoid repeating concepts unnecessarily.

Cover:

1. Structured and unstructured data
   - Structured data
   - Semi-structured data
   - Unstructured data
   - Examples involving tables, JSON, text, PDFs, images, audio and video
   - Why unstructured data requires special processing

2. Traditional NLP pipeline
   - Text extraction
   - Text cleaning
   - Lowercasing
   - Tokenization
   - Stop-word removal
   - Stemming
   - Lemmatization
   - N-grams
   - Bag of Words
   - TF-IDF
   - Limitations of traditional text representations

3. Common NLP tasks
   - Text classification
   - Sentiment analysis
   - Named Entity Recognition
   - Information extraction
   - Summarization
   - Question answering
   - Semantic search

4. Embeddings
   - What embeddings are
   - Why text is converted into vectors
   - Word embeddings
   - Sentence embeddings
   - Document embeddings
   - Dense representations
   - Sparse representations
   - Embedding dimensions
   - Semantic similarity
   - Cosine similarity
   - Embeddings vs generated text
   - How embeddings support semantic search and RAG

5. Foundation models
   - What foundation models are
   - Why they are called foundation models
   - Difference between traditional ML models and foundation models
   - Text foundation models
   - Image foundation models
   - Audio foundation models
   - Multimodal models
   - Open-source models
   - Commercial models
   - Examples involving Llama, Hugging Face, OpenAI and IBM watsonx

6. LLM lifecycle
   - Pretraining
   - Fine-tuning
   - Instruction tuning
   - Alignment
   - Inference
   - Prompting
   - Retrieval-Augmented Generation
   - Model serving

7. Important LLM concepts
   - Tokens
   - Tokenization
   - Context window
   - System prompt
   - User prompt
   - Few-shot prompting
   - Zero-shot prompting
   - Structured output
   - Temperature
   - Top-p
   - Maximum output tokens
   - Deterministic vs creative responses

8. Prompting vs RAG vs fine-tuning
   - When prompting is enough
   - When external knowledge requires RAG
   - When fine-tuning may be useful
   - Why fine-tuning does not automatically provide current enterprise knowledge
   - Cost, complexity and maintenance differences

9. Enterprise LLM use cases
   - Document question answering
   - Customer support
   - Summarization
   - Information extraction
   - Code assistance
   - Internal knowledge assistants
   - Workflow automation

10. LLM risks and limitations
   - Hallucination
   - Knowledge cutoff
   - Bias
   - Prompt injection
   - Sensitive-data exposure
   - Privacy
   - Context-window limits
   - Inference latency
   - Token cost
   - Lack of explainability
   - Need for human oversight

Use easy examples such as sentiment analysis and an employee policy assistant.

Output format:
- 5-line beginner summary
- Clear headings and subheadings
- Detailed beginner-friendly explanations
- Key definitions
- Traditional NLP vs LLM comparison table
- Sparse vs dense representation comparison
- Prompting vs RAG vs fine-tuning comparison table
- Easy examples
- ASCII diagram showing raw text to NLP to embeddings to LLM applications
- ASCII diagram showing the LLM lifecycle
- Pseudocode for using an LLM in an enterprise application
- Explanation of the relationship between NLP, embeddings, LLMs and RAG
- Common confusions and mistakes
- Memory aids
- Concise final recap
```

---

# Revision Day 3 — RAG, Vector Databases and Evaluation

```text
Act as a senior enterprise RAG architect and GenAI evaluation mentor.

Today is Revision Day 3 of my IBM AI/GenAI preparation.

Create comprehensive revision notes covering basic RAG, vector databases, Advanced RAG, reranking, grounded answer generation and RAG evaluation.

Explain the complete lifecycle from document ingestion to retrieval, generation, evaluation, monitoring and continuous improvement.

Use one consistent example: an internal HR policy assistant.

Cover:

1. RAG fundamentals
   - What Retrieval-Augmented Generation is
   - Why normal LLMs are insufficient for enterprise knowledge
   - Hallucination
   - Knowledge cutoff
   - Private organizational knowledge
   - Difference between model knowledge and retrieved knowledge
   - Main components of a RAG system
   - When RAG should and should not be used

2. Document ingestion
   - Loading PDF, Word, HTML, text and database content
   - Text extraction
   - Cleaning
   - Handling document structure
   - Extracting titles, sections and page numbers
   - Metadata extraction
   - Document identifiers
   - Source tracking
   - Access-control metadata
   - Handling tables
   - Handling scanned documents at a conceptual level
   - Updating and deleting documents
   - Re-indexing changed content
   - Avoiding duplicate documents

3. Chunking
   - Why documents are divided into chunks
   - Fixed-size chunking
   - Recursive chunking
   - Semantic chunking
   - Parent-child chunking
   - Chunk size
   - Chunk overlap
   - Preserving headings and section context
   - Problems caused by chunks that are too large
   - Problems caused by chunks that are too small

4. Embedding and indexing
   - Converting chunks into embeddings
   - Embedding-model selection
   - Embedding dimensions
   - Storing vectors and metadata
   - Creating an index
   - Document and index versioning
   - Batch indexing
   - Incremental indexing

5. Vector databases
   - Purpose of a vector database
   - FAISS
   - Chroma
   - Pinecone
   - Weaviate
   - Milvus
   - Similarity search
   - Cosine similarity
   - Top-k retrieval
   - Metadata filtering
   - Namespace or collection concepts
   - Vector database vs relational database
   - When a local vector index is enough
   - When a managed vector database is useful

6. Retrieval methods
   - Keyword search
   - Sparse retrieval
   - Dense vector retrieval
   - Hybrid search
   - Metadata filtering
   - Query rewriting
   - Query expansion
   - Multi-query retrieval
   - Parent-document retrieval
   - Retrieval top-k selection

7. Reranking
   - Why reranking is needed
   - First-stage retrieval
   - Second-stage reranking
   - Bi-encoder retrieval
   - Cross-encoder reranking
   - Small reranking models
   - LLM-based reranking
   - Retrieval top-k vs final context top-n
   - Accuracy, latency and cost trade-offs

8. Context construction
   - Duplicate removal
   - Contextual compression
   - Context ordering
   - Token-budget management
   - Long-document handling
   - Preserving source information
   - Prompt construction
   - Instructions to answer only from retrieved context
   - Source citations
   - Citation validation
   - Refusing or escalating when evidence is insufficient

9. Answer generation
   - Grounded answer generation
   - Faithful summarization
   - Structured answers
   - Citing retrieved sources
   - Preventing unsupported claims
   - Handling conflicting documents
   - Returning a safe fallback answer

10. RAG evaluation
   - Retrieval quality
   - Answer quality
   - Relevance
   - Groundedness
   - Faithfulness
   - Hallucination
   - Context precision
   - Context recall
   - Answer correctness
   - Citation correctness
   - Golden question-answer datasets
   - Human evaluation
   - Offline evaluation
   - Online feedback
   - User satisfaction

11. Continuous improvement
   - Logging failed queries
   - Identifying retrieval failures
   - Identifying generation failures
   - Improving chunking
   - Improving metadata
   - Improving retrieval
   - Improving reranking
   - Updating prompts
   - Updating documents
   - Monitoring production quality

Output format:
- 5-line beginner summary
- Clear headings and subheadings
- Detailed but easy-to-scan explanations
- Key definitions
- Basic RAG vs Advanced RAG comparison table
- Keyword vs vector vs hybrid search comparison table
- Bi-encoder vs cross-encoder comparison
- ASCII diagram showing document ingestion and indexing
- ASCII diagram showing the complete query-time RAG pipeline
- ASCII diagram showing the evaluation and improvement loop
- Pseudocode for document indexing
- Pseudocode for hybrid retrieval and reranking
- Pseudocode for grounded answer generation with fallback
- Pseudocode for RAG evaluation
- Explanation of the relationship between retrieval quality and answer quality
- Common failure scenarios and fixes
- Memory aids
- Concise final recap
```

---

# Revision Day 4 — LangChain, LangGraph and Agentic AI

```text
Act as a senior Agentic AI architect and beginner-friendly GenAI mentor.

Today is Revision Day 4 of my IBM AI/GenAI preparation.

Create comprehensive revision notes covering LangChain, LangGraph, tool-using agents, human-in-the-loop systems and multi-agent frameworks.

Explain the progression from a direct LLM call to chains, deterministic workflows, agents and multi-agent systems.

Use an example such as an HR assistant that answers policy questions and escalates uncertain or sensitive cases to a human.

Cover:

1. Direct LLM applications
   - Prompt and response
   - System and user instructions
   - Structured output
   - Limitations of a single LLM call

2. LangChain fundamentals
   - What LangChain is
   - Model wrappers
   - Prompt templates
   - Chains
   - Runnable pipelines
   - Output parsers
   - Retrievers
   - Tools
   - Memory
   - RAG using LangChain
   - Benefits
   - Limitations
   - When a framework may be unnecessary

3. Deterministic workflows vs agents
   - Fixed workflow
   - Conditional workflow
   - Agentic decision-making
   - Predictability
   - Flexibility
   - Cost
   - Risk
   - When to use a normal workflow
   - When to use an agent

4. Agentic AI
   - What an AI agent is
   - Goal
   - State
   - Planning
   - Reasoning
   - Tool selection
   - Tool execution
   - Observation
   - Iteration
   - Final response
   - Difference between automation and autonomous decision-making

5. Tools, skills and plugins
   - Search tools
   - Database tools
   - API tools
   - File tools
   - Code-execution tools
   - Tool schemas
   - Structured tool arguments
   - Input validation
   - Authentication
   - Authorization
   - Least-privilege access
   - Safe handling of tool output

6. LangGraph
   - What LangGraph is
   - Nodes
   - Edges
   - State
   - Conditional routing
   - Cycles
   - Checkpoints
   - Persistence
   - Pausing and resuming
   - Retry logic
   - Error recovery
   - Timeouts
   - Fallback paths
   - Human-in-the-loop
   - When to use LangGraph instead of a simple chain

7. Agent state and memory
   - Conversation history
   - Working memory
   - Long-term memory
   - State storage
   - Checkpointing
   - Memory summarization
   - Risks of incorrect, stale or excessive memory
   - Privacy considerations

8. Multi-agent systems
   - Why multiple agents may be used
   - Planner agent
   - Researcher agent
   - Executor agent
   - Critic or reviewer agent
   - Supervisor agent
   - Task delegation
   - Agent communication
   - Shared state
   - Sequential collaboration
   - Parallel collaboration
   - Conflict resolution
   - When multi-agent architecture is overkill

9. Framework comparison
   - LangChain
   - LangGraph
   - CrewAI
   - Microsoft Semantic Kernel
   - Chains, workflows, skills, plugins and agents
   - Suitable use cases for each framework

10. Human-in-the-loop
   - Approval steps
   - Review of high-risk actions
   - Escalation
   - Correcting agent decisions
   - Pausing and resuming workflows
   - Human ownership of final decisions

11. Agent evaluation and observability
   - Task completion
   - Correct tool selection
   - Tool-call success rate
   - Number of workflow steps
   - Latency
   - Token usage
   - Cost
   - Failure rate
   - Human intervention rate
   - Quality of final responses
   - Tracing agent decisions and tool calls

12. Risks and guardrails
   - Infinite loops
   - Excessive tool usage
   - Wrong tool selection
   - Hallucinated actions
   - Unauthorized actions
   - Prompt injection
   - Sensitive-data exposure
   - Retry and iteration limits
   - Timeouts
   - Cost limits
   - Audit logs
   - Allow-listed tools
   - Human approval before high-risk actions

Output format:
- 5-line beginner summary
- Clear headings and subheadings
- Detailed beginner-friendly explanations
- Key definitions
- Direct LLM vs chain vs workflow vs agent comparison
- Single-agent vs multi-agent comparison
- LangChain vs LangGraph vs CrewAI vs Semantic Kernel comparison table
- ASCII diagram showing a LangGraph-style workflow
- ASCII diagram showing a multi-agent architecture
- Pseudocode for a stateful agent workflow
- Pseudocode for a multi-agent workflow
- Pseudocode for human approval and fallback handling
- Explanation of the relationship between tools, state, routing, memory and human approval
- Common mistakes and over-engineering risks
- Memory aids
- Concise final recap
```

---

# Revision Day 5 — Databricks, MLOps and Production AI Architecture

```text
Act as a senior Databricks, MLOps, cloud and enterprise AI platform architect.

Today is Revision Day 5 of my IBM AI/GenAI preparation.

Create comprehensive revision notes covering Databricks, Delta Lake, MLflow, MLOps, REST APIs, cloud infrastructure, Kubernetes, monitoring, governance and end-to-end production AI architecture.

Explain how all these components connect to move an ML, RAG or agentic application from development to production.

Use one consistent example: a production internal policy assistant.

Cover:

1. Databricks fundamentals
   - What Databricks is
   - Why enterprises use Databricks
   - Lakehouse architecture
   - Workspace
   - Notebooks
   - Compute
   - Clusters
   - Jobs
   - Workflows
   - Databricks SQL
   - Data ingestion
   - Databricks for data engineering
   - Databricks for Machine Learning
   - Databricks for GenAI
   - Databricks Apps
   - Databricks Agents
   - Relationship among Databricks, Delta Lake and MLflow

2. Data architecture and Delta Lake
   - Data lake
   - Data warehouse
   - Lakehouse
   - ETL
   - ELT
   - Batch processing
   - Streaming basics
   - Bronze layer
   - Silver layer
   - Gold layer
   - ACID transactions
   - Schema enforcement
   - Schema evolution
   - Time travel
   - Data quality checks
   - Deduplication
   - Feature-engineering pipelines
   - Preparing documents and metadata for RAG
   - How Delta Lake supports ML and GenAI workloads

3. MLflow
   - Experiments
   - Runs
   - Parameters
   - Metrics
   - Artifacts
   - Model packaging
   - Model registry
   - Model versions
   - Model aliases or lifecycle stages
   - Model lineage
   - Data lineage relationship
   - Reproducibility
   - Model promotion
   - Rollback
   - MLflow with Databricks
   - MLflow for LLM and RAG evaluation

4. MLOps
   - What MLOps is
   - DevOps vs MLOps
   - Source control
   - Data validation
   - Model validation
   - Unit testing
   - Integration testing
   - Performance testing
   - Security testing
   - CI/CD for ML
   - Model packaging
   - Deployment
   - Batch inference
   - Real-time inference
   - Canary deployment
   - Blue-green deployment
   - Rollback strategy
   - Reproducible environments

5. Monitoring and observability
   - Logs
   - Metrics
   - Traces
   - Application health
   - Latency
   - Throughput
   - Error rate
   - Availability
   - Infrastructure utilization
   - Model accuracy
   - Data drift
   - Concept drift
   - Retrieval quality
   - Groundedness
   - Hallucination rate
   - Agent tool failures
   - Token usage
   - Cost
   - User feedback
   - Alerting and incident response

6. REST API deployment
   - Why AI models are exposed through APIs
   - FastAPI basics
   - Prediction endpoints
   - RAG endpoints
   - Agent endpoints
   - Request schemas
   - Response schemas
   - Input validation
   - Error handling
   - Authentication
   - Authorization
   - Rate limiting
   - API versioning
   - Idempotency where relevant
   - Logging
   - Correlation identifiers
   - Synchronous processing
   - Asynchronous processing
   - Background jobs
   - Timeouts
   - Retries
   - Health endpoints
   - Production-readiness checks

7. Cloud and Kubernetes
   - IBM Cloud, AWS, Azure and GCP at a high level
   - Compute
   - Object storage
   - Managed databases
   - Networking
   - Secrets management
   - Identity and access management
   - Containers
   - Container images
   - Kubernetes pods
   - Deployments
   - Services
   - Configuration
   - Secrets
   - Autoscaling
   - Load balancing
   - High availability
   - Backup
   - Disaster recovery
   - Cost management

8. Governance and Responsible AI
   - Data governance
   - Model governance
   - Model documentation
   - Data lineage
   - Model lineage
   - Auditability
   - Explainability
   - Bias and fairness
   - Privacy
   - Security
   - Access control
   - Compliance
   - Human oversight
   - Approval workflows
   - Retention policies
   - Traceability of prompts, retrieved context and responses

9. End-to-end production AI architecture
   - Business requirements
   - Functional requirements
   - Non-functional requirements
   - Data sources
   - Ingestion pipeline
   - Bronze, Silver and Gold layers
   - Document processing
   - Embedding generation
   - Vector database
   - Retriever
   - Reranker
   - LLM or agent workflow
   - Metadata database
   - REST API
   - Web application
   - MLflow tracking
   - Source control
   - CI/CD
   - Containerization
   - Kubernetes deployment
   - Monitoring
   - Governance
   - Human escalation
   - Continuous improvement

10. Production decision-making
   - Batch vs real-time inference
   - Synchronous vs asynchronous APIs
   - Managed service vs self-hosted model
   - Scaling stateless API components
   - Managing stateful workflow components
   - Reliability, security, performance and cost trade-offs

Output format:
- 5-line beginner summary
- Clear headings and subheadings
- Detailed but easy-to-scan explanations
- Key definitions
- Data lake vs warehouse vs lakehouse comparison
- ETL vs ELT comparison
- Batch vs real-time inference comparison
- DevOps vs MLOps comparison
- Synchronous vs asynchronous API comparison
- ASCII diagram showing Bronze, Silver and Gold architecture
- ASCII diagram showing the MLflow lifecycle
- ASCII diagram showing CI/CD and deployment flow
- ASCII diagram showing the complete production GenAI architecture
- Pseudocode for an ETL pipeline
- Pseudocode for experiment tracking and model registration
- Pseudocode for a production RAG API
- Pseudocode for CI/CD deployment and rollback
- Pseudocode for monitoring and alerting
- Explanation of the relationship between Databricks, Delta Lake, MLflow, APIs, cloud, Kubernetes and MLOps
- Production-readiness checklist
- 2-minute explanation of the complete architecture
- Common follow-up questions and beginner-friendly answers
- Common mistakes
- Memory aids
- Concise final recap
```

# Final 3-Week Copy-Paste-Ready Daily Prompts

## Week 1: AI, ML, Python, NLP and LLM Foundations

## Day 1 — Understand the Role and AI Project Lifecycle

```text
Act as a senior IBM AI/Data Scientist interview mentor.

Today is Day 1 of my 3-week preparation for IBM Data Scientist AI/GenAI IJP roles.

Teach me what this type of role expects in practical terms.

Cover:
1. What a Data Scientist in AI/GenAI does
2. What a Band 08 Data Scientist is expected to handle
3. Difference between data analysis, machine learning, GenAI, and AI solution architecture
4. Common responsibilities in enterprise AI projects
5. End-to-end AI project lifecycle
6. How business problems are converted into AI solutions
7. How backend, cloud, CI/CD and automation experience connects to AI roles
8. What mindset is expected from a senior Data Scientist

Output format:
- 5-line beginner summary
- Descriptive notes in simple language
- Easy real-world example
- ASCII diagram showing AI project lifecycle
- Pseudocode for solving an AI business problem
- Common mistakes
```

---

## Day 2 — Machine Learning Fundamentals

```text
Act as a senior Data Scientist and Machine Learning mentor.

Today is Day 2 of my IBM AI/GenAI preparation.

Teach me Machine Learning fundamentals in beginner-friendly language.

Cover:
1. What Machine Learning is
2. Supervised learning
3. Unsupervised learning
4. Classification
5. Regression
6. Clustering
7. Feature engineering
8. Train/test split
9. Cross-validation
10. Model evaluation metrics
11. Accuracy, precision, recall, F1-score and ROC-AUC
12. Overfitting and underfitting
13. How ML moves from experiment to production

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing ML workflow
- Pseudocode for building an ML model
- Simple comparison table where useful
- Common mistakes
```

---

## Day 3 — Python AI Frameworks

```text
Act as a senior Python AI mentor.

Today is Day 3 of my IBM AI/GenAI preparation.

Teach me the Python AI framework ecosystem.

Cover:
1. Why Python is important in AI projects
2. NumPy for numerical operations
3. Pandas for data analysis
4. Scikit-learn for traditional ML
5. PyTorch basics
6. TensorFlow/Keras basics
7. Hugging Face basics
8. When to use Scikit-learn
9. When to use PyTorch or TensorFlow
10. When to use Hugging Face
11. How these frameworks fit into enterprise AI projects

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples for each framework
- ASCII diagram showing Python AI ecosystem
- Pseudocode for choosing the right framework
- Simple comparison table
- Common mistakes
```

---

## Day 4 — EDA, Data Preprocessing and Feature Engineering

```text
Act as a senior Data Scientist mentor.

Today is Day 4 of my IBM AI/GenAI preparation.

Teach me EDA, data preprocessing and feature engineering.

Cover:
1. What EDA is
2. Why EDA is important before ML
3. Understanding data shape, columns and data types
4. Missing values
5. Duplicate records
6. Outliers
7. Categorical variables
8. Numerical variables
9. Encoding
10. Scaling
11. Feature engineering
12. Data leakage
13. Train/test split after preprocessing
14. How clean data improves model performance

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing data preparation flow
- Pseudocode for EDA and preprocessing
- Simple comparison table where useful
- Common mistakes
```

---

## Day 5 — NLP and Unstructured Data

```text
Act as a senior NLP and GenAI mentor.

Today is Day 5 of my IBM AI/GenAI preparation.

Teach me NLP fundamentals in beginner-friendly language.

Cover:
1. What NLP is
2. Structured vs unstructured data
3. Text preprocessing
4. Tokenization
5. Stop words
6. Stemming and lemmatization
7. Bag of Words
8. TF-IDF
9. Word embeddings
10. Sentence embeddings
11. Text classification
12. Named Entity Recognition
13. Sentiment analysis
14. How NLP connects to LLMs and RAG

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing NLP pipeline
- Pseudocode for text classification
- Pseudocode for converting documents into embeddings
- Common mistakes
```

---

## Day 6 — Foundation Models and LLM Basics

```text
Act as a senior LLM mentor and enterprise AI architect.

Today is Day 6 of my IBM AI/GenAI preparation.

Teach me foundation models and LLM fundamentals.

Cover:
1. What foundation models are
2. What LLMs are
3. Difference between traditional ML models and foundation models
4. Pretraining
5. Fine-tuning
6. Instruction tuning
7. Prompting
8. Tokens and context window
9. Temperature, top-p and max tokens
10. Embeddings vs generated text
11. Open-source LLMs like Llama
12. Commercial LLMs
13. Enterprise use cases of LLMs
14. Risks and limitations of LLMs

Output format:
- 5-line beginner summary
- Descriptive notes
- Beginner-friendly examples
- ASCII diagram showing LLM lifecycle
- Pseudocode for using an LLM in an enterprise app
- Common mistakes
```

---

## Day 7 — SQL, NoSQL and Data Storage for AI

```text
Act as a senior Data Scientist and data platform mentor.

Today is Day 7 of my IBM AI/GenAI preparation.

Teach me SQL, NoSQL and data storage concepts required for AI systems.

Cover:
1. Why databases matter in AI projects
2. SQL basics
3. Tables, rows and columns
4. Joins
5. Aggregations
6. NoSQL basics
7. Document databases
8. Key-value stores
9. SQL vs NoSQL
10. Storing documents
11. Storing chunks
12. Storing embeddings
13. Storing user queries and model responses
14. Metadata storage for AI applications
15. How databases connect with AI pipelines

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy SQL examples
- ASCII diagram showing database usage in AI system
- Pseudocode for storing and retrieving AI application data
- Common mistakes
```

---

# Week 2: RAG, Vector DB, Advanced RAG and Agentic AI

## Day 8 — RAG Fundamentals

```text
Act as a senior GenAI and RAG mentor.

Today is Day 8 of my IBM AI/GenAI preparation.

Teach me Retrieval-Augmented Generation, also called RAG.

Cover:
1. What RAG is
2. Why normal LLMs are not enough for enterprise knowledge
3. Hallucination problem
4. Knowledge cutoff problem
5. How RAG solves document Q&A
6. Document ingestion
7. Chunking
8. Embeddings
9. Vector database
10. Retriever
11. Prompt construction
12. LLM response generation
13. Citations and source grounding
14. Basic RAG evaluation

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy real-world example
- ASCII diagram showing RAG architecture
- Pseudocode for basic RAG pipeline
- Common mistakes
```

---

## Day 9 — Embeddings and Vector Databases

```text
Act as a senior vector database and RAG mentor.

Today is Day 9 of my IBM AI/GenAI preparation.

Teach me embeddings and vector databases in simple language.

Cover:
1. What embeddings are
2. Why text is converted into numbers
3. Sentence embeddings
4. Similarity search
5. Cosine similarity
6. Vector database purpose
7. FAISS
8. Chroma
9. Pinecone
10. Weaviate
11. Milvus
12. Metadata filtering
13. Top-k retrieval
14. How vector DB fits into enterprise RAG

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy example using policy documents
- ASCII diagram showing embedding and search flow
- Pseudocode for indexing documents
- Pseudocode for retrieving top-k chunks
- Common mistakes
```

---

## Day 10 — Advanced RAG

```text
Act as a senior enterprise RAG architect.

Today is Day 10 of my IBM AI/GenAI preparation.

Teach me Advanced RAG patterns.

Cover:
1. Why basic RAG may fail
2. Poor chunking problem
3. Missing context problem
4. Keyword search vs vector search
5. Hybrid search
6. Reranking
7. Query rewriting
8. Multi-query retrieval
9. Contextual compression
10. Context grounding
11. Prompt optimization for RAG
12. Handling long documents
13. Reducing hallucination
14. Improving answer quality

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing advanced RAG
- Pseudocode for hybrid search plus reranking
- Pseudocode for grounded answer generation
- Common mistakes
```

---

## Day 11 — RAG Evaluation and Quality Improvement

```text
Act as a senior GenAI evaluation mentor.

Today is Day 11 of my IBM AI/GenAI preparation.

Teach me how to evaluate and improve a RAG system.

Cover:
1. Why RAG evaluation is important
2. Retrieval quality
3. Answer quality
4. Groundedness
5. Faithfulness
6. Relevance
7. Hallucination detection
8. Context precision
9. Context recall
10. Human evaluation
11. Golden question-answer dataset
12. Offline evaluation
13. Online feedback
14. Continuous improvement loop

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy example using an internal policy assistant
- ASCII diagram showing RAG evaluation flow
- Pseudocode for evaluating RAG responses
- Simple metrics table
- Common mistakes
```

---

## Day 12 — LangChain Fundamentals

```text
Act as a senior LangChain and GenAI application mentor.

Today is Day 12 of my IBM AI/GenAI preparation.

Teach me LangChain fundamentals.

Cover:
1. What LangChain is
2. Why frameworks are used in GenAI apps
3. LLM wrapper
4. Prompt templates
5. Chains
6. Output parsers
7. Retrievers
8. Tools
9. Memory basics
10. RAG using LangChain
11. Benefits of LangChain
12. Limitations of LangChain
13. Where LangChain fits in enterprise AI projects

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing LangChain components
- Pseudocode for a LangChain RAG app
- Common mistakes
```

---

## Day 13 — LangGraph and Agentic Workflows

```text
Act as a senior LangGraph and Agentic AI mentor.

Today is Day 13 of my IBM AI/GenAI preparation.

Teach me LangGraph and agentic workflows.

Cover:
1. What Agentic AI means
2. Difference between normal LLM app and agentic AI app
3. What LangGraph is
4. Nodes
5. Edges
6. State
7. Conditional routing
8. Tool calling
9. Human-in-the-loop
10. Multi-step workflow
11. When to use LangGraph instead of simple chains
12. Enterprise use cases
13. Risks of agents

Output format:
- 5-line beginner summary
- Descriptive notes
- Simple real-world example
- ASCII diagram showing LangGraph workflow
- Pseudocode for an agentic workflow
- Common mistakes
```

---

## Day 14 — Multi-Agent Systems: CrewAI and Semantic Kernel

```text
Act as a senior Agentic AI architecture mentor.

Today is Day 14 of my IBM AI/GenAI preparation.

Teach me CrewAI, Microsoft Semantic Kernel and multi-agent AI patterns.

Cover:
1. What multi-agent systems are
2. Why multiple agents are used
3. Planner agent
4. Researcher agent
5. Critic or reviewer agent
6. Executor agent
7. CrewAI basics
8. Semantic Kernel basics
9. Skills, plugins and tools concept
10. Agent orchestration
11. When multi-agent is useful
12. When multi-agent is overkill
13. Enterprise governance risks

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy business examples
- ASCII diagram showing multi-agent architecture
- Pseudocode for a multi-agent workflow
- Comparison table of LangGraph, CrewAI and Semantic Kernel
- Common mistakes
```

---

# Week 3: Databricks, MLflow, MLOps, Deployment and Governance

## Day 15 — Databricks Fundamentals

```text
Act as a senior Databricks and Data Science mentor.

Today is Day 15 of my IBM AI/GenAI preparation.

Teach me Databricks fundamentals.

Cover:
1. What Databricks is
2. Why enterprises use Databricks
3. Lakehouse concept
4. Workspace
5. Notebooks
6. Clusters
7. Jobs
8. Data ingestion
9. ETL and ELT
10. Databricks SQL
11. Databricks for ML
12. Databricks for GenAI
13. Databricks Apps
14. Databricks Agents
15. How Databricks connects with MLflow and Delta Lake

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing Databricks lakehouse architecture
- Pseudocode for a Databricks data pipeline
- Common mistakes
```

---

## Day 16 — Delta Lake and ETL/ELT Pipelines

```text
Act as a senior Data Engineering and Databricks mentor.

Today is Day 16 of my IBM AI/GenAI preparation.

Teach me Delta Lake and ETL/ELT pipelines.

Cover:
1. What Delta Lake is
2. Why normal data lakes have problems
3. ACID transactions
4. Schema enforcement
5. Schema evolution
6. Time travel
7. Bronze, Silver and Gold architecture
8. ETL vs ELT
9. Batch pipeline
10. Streaming pipeline basics
11. Data quality checks
12. Feature engineering pipeline
13. How Delta Lake supports ML and GenAI use cases

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing Bronze/Silver/Gold architecture
- Pseudocode for an ETL pipeline
- Pseudocode for feature engineering
- Common mistakes
```

---

## Day 17 — MLflow and Model Lifecycle

```text
Act as a senior MLOps and MLflow mentor.

Today is Day 17 of my IBM AI/GenAI preparation.

Teach me MLflow for machine learning lifecycle management.

Cover:
1. What MLflow is
2. Why experiment tracking matters
3. Parameters
4. Metrics
5. Artifacts
6. Model registry
7. Model versioning
8. Model promotion from development to production
9. Reproducibility
10. Model deployment basics
11. MLflow with Databricks
12. MLflow for GenAI evaluation
13. Model lineage
14. Rollback strategy

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing MLflow lifecycle
- Pseudocode for tracking an experiment
- Pseudocode for registering and deploying a model
- Common mistakes
```

---

## Day 18 — MLOps, Monitoring and Governance

```text
Act as a senior MLOps architect and AI platform mentor.

Today is Day 18 of my IBM AI/GenAI preparation.

Teach me MLOps for production AI systems.

Cover:
1. What MLOps is
2. Why ML models need lifecycle management
3. CI/CD for ML
4. Model testing
5. Data validation
6. Model validation
7. Model deployment
8. Batch inference vs real-time inference
9. Model monitoring
10. Data drift
11. Concept drift
12. Performance monitoring
13. Governance frameworks
14. Auditability
15. Compliance
16. Responsible AI basics

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing MLOps pipeline
- Pseudocode for CI/CD model deployment
- Pseudocode for monitoring model drift
- Common mistakes
```

---

## Day 19 — REST API Deployment for ML and GenAI

```text
Act as a senior backend engineer and GenAI platform mentor.

Today is Day 19 of my IBM AI/GenAI preparation.

Teach me how to deploy ML and GenAI models using REST APIs and web applications.

Cover:
1. Why REST APIs are used for AI services
2. Request and response design
3. FastAPI basics
4. Input validation
5. Error handling
6. Authentication basics
7. Rate limiting
8. Logging
9. Observability
10. Async processing
11. Model serving
12. RAG API design
13. Agent API design
14. API versioning
15. Production readiness checklist

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing client to API to model flow
- Pseudocode for ML prediction API
- Pseudocode for RAG API
- Common mistakes
```

---

## Day 20 — Cloud, Kubernetes and Enterprise AI Architecture

```text
Act as a senior cloud AI architect.

Today is Day 20 of my IBM AI/GenAI preparation.

Teach me cloud platforms and enterprise AI architecture.

Cover:
1. Why cloud is important for AI systems
2. IBM Cloud, AWS, Azure and GCP at a high level
3. Compute
4. Storage
5. Managed databases
6. Object storage
7. Kubernetes basics
8. Containers
9. Model deployment on cloud
10. Secure networking basics
11. Secrets management
12. Scalability
13. High availability
14. Cost considerations
15. How cloud supports Databricks, RAG and MLOps

Output format:
- 5-line beginner summary
- Descriptive notes
- Easy examples
- ASCII diagram showing cloud AI architecture
- Pseudocode for cloud deployment workflow
- Common mistakes
```

---

## Day 21 — Final End-to-End AI Solution Design

```text
Act as a senior enterprise AI solution architect and interview coach.

Today is Day 21 of my IBM AI/GenAI preparation.

Help me design one complete end-to-end enterprise GenAI solution.

Use case:
Build an internal policy assistant that answers employee questions from company documents, uses RAG for grounded answers, uses an agent workflow for complex cases, stores metadata, tracks evaluations, and can be deployed as a production API.

Cover:
1. Business problem
2. Functional requirements
3. Non-functional requirements
4. Data sources
5. Document ingestion
6. Chunking strategy
7. Embedding strategy
8. Vector database design
9. Hybrid retrieval
10. Reranking
11. Prompt design
12. LLM response generation
13. Agent workflow
14. Human escalation
15. API layer
16. Metadata storage
17. Evaluation
18. Monitoring
19. Governance
20. Deployment architecture

Output format:
- 5-line beginner summary
- Descriptive architecture notes
- ASCII architecture diagram
- Step-by-step solution design
- Pseudocode for complete workflow
- 2-minute explanation of the solution
- Common follow-up questions and answers
- Common mistakes
```

---
