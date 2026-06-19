## 1. Five-line beginner summary

FastAPI helps you build backend APIs quickly using Python.
REST APIs allow clients like web apps, mobile apps, or AI tools to talk to your backend.
In GenAI apps, APIs receive prompts, documents, user IDs, and return AI-generated answers.
Pydantic validates request and response data before your backend logic runs.
Good API design means clear routes, correct status codes, safe error handling, and versioning.

---

# 2. Descriptive notes

## What is a REST API?

A **REST API** is a way for two systems to communicate over HTTP.

Example:

```text
Client sends:
POST /api/v1/chat/completions

Backend returns:
{
  "answer": "FastAPI is a Python web framework..."
}
```

REST APIs usually use HTTP methods:

| Method   | Meaning                  | Example                   |
| -------- | ------------------------ | ------------------------- |
| `GET`    | Read data                | Get chat history          |
| `POST`   | Create something         | Send prompt               |
| `PUT`    | Replace something        | Replace document metadata |
| `PATCH`  | Update part of something | Rename document           |
| `DELETE` | Delete something         | Delete uploaded file      |

In GenAI platforms, REST APIs are used for:

```text
User prompt → backend API → LLM service → response
Document upload → backend API → storage/vector DB → document ID
Question → backend API → retrieval + LLM → answer
```

---

# 3. FastAPI basics

**FastAPI** is a Python framework for building APIs.

Why it is popular for AI backend systems:

| Feature                | Why it matters                         |
| ---------------------- | -------------------------------------- |
| Fast development       | Build APIs quickly                     |
| Type hints             | Cleaner request/response contracts     |
| Pydantic validation    | Reject bad input automatically         |
| Async support          | Useful for network-heavy AI calls      |
| Auto docs              | Swagger UI is generated automatically  |
| Good for microservices | Works well in AI platform architecture |

A basic FastAPI endpoint looks like this:

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

This means:

```text
When someone calls GET /health,
run health_check(),
return JSON response.
```

---

# 4. Request and response models

In production backend systems, you should not accept random JSON blindly.

Bad design:

```python
@app.post("/chat")
def chat(request: dict):
    prompt = request["prompt"]
```

Better design:

```python
class ChatRequest(BaseModel):
    user_id: str
    message: str
```

Now the API expects structured input:

```json
{
  "user_id": "user-123",
  "message": "Explain vector databases"
}
```

If `message` is missing, FastAPI automatically returns a validation error.

---

# 5. Pydantic validation

Pydantic validates data before it reaches your service logic.

Example:

```python
class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1, max_length=4000)
```

This protects your backend from:

```text
Empty prompts
Huge prompts
Missing fields
Wrong data types
Invalid payload shape
```

For GenAI apps, validation is important because bad input can increase cost, latency, and security risk.

---

# 6. API routes

A route maps an HTTP path to Python code.

Examples:

```text
GET  /api/v1/health
POST /api/v1/chat/completions
POST /api/v1/documents/upload
GET  /api/v1/documents/{document_id}
```

A good route should be:

```text
Clear
Versioned
Resource-focused
Predictable
Easy to test
```

---

# 7. Status codes

Status codes tell the client what happened.

| Code                        | Meaning                | Example                           |
| --------------------------- | ---------------------- | --------------------------------- |
| `200 OK`                    | Request succeeded      | Chat answer returned              |
| `201 Created`               | Resource created       | Document uploaded                 |
| `400 Bad Request`           | Invalid business input | Empty prompt                      |
| `401 Unauthorized`          | User not logged in     | Missing token                     |
| `403 Forbidden`             | User lacks access      | Accessing another user's document |
| `404 Not Found`             | Resource missing       | Document ID not found             |
| `422 Unprocessable Entity`  | Validation failed      | Wrong JSON schema                 |
| `500 Internal Server Error` | Server failed          | LLM provider error                |

FastAPI automatically returns `422` for Pydantic validation failures.

---

# 8. Error responses

Bad error response:

```json
{
  "error": "Something went wrong"
}
```

Better error response:

```json
{
  "error_code": "DOCUMENT_NOT_FOUND",
  "message": "Document was not found",
  "details": {
    "document_id": "doc-123"
  }
}
```

Good error responses help:

```text
Frontend developers
Backend debugging
Monitoring systems
API clients
Interview system design discussions
```

---

# 9. API versioning

Versioning prevents breaking existing clients.

Common pattern:

```text
/api/v1/chat/completions
/api/v1/documents/upload
```

Later, if your API changes:

```text
/api/v2/chat/completions
```

This allows old clients to keep using `v1`.

For interviews, mention that API versioning is important when mobile apps, enterprise clients, or external developers depend on your API.

---

# 10. Chat completion API design

A GenAI chat completion API should accept:

```text
User ID
Conversation ID
Message
Model name
Temperature
Max tokens
Optional document IDs
```

Example request:

```json
{
  "user_id": "user-123",
  "conversation_id": "conv-001",
  "message": "Summarize my uploaded document",
  "model": "gpt-4.1",
  "temperature": 0.2,
  "max_tokens": 500,
  "document_ids": ["doc-001"]
}
```

Example response:

```json
{
  "conversation_id": "conv-001",
  "answer": "The document explains...",
  "model": "gpt-4.1",
  "usage": {
    "input_tokens": 120,
    "output_tokens": 80
  }
}
```

---

# 11. Document upload API design

A document upload API should handle:

```text
File upload
File type validation
File size validation
Document ID creation
Storage
Metadata extraction
Future vector embedding pipeline
```

Example route:

```text
POST /api/v1/documents/upload
```

Example response:

```json
{
  "document_id": "doc-abc123",
  "filename": "resume.pdf",
  "status": "uploaded"
}
```

In a real GenAI app, after upload:

```text
PDF → text extraction → chunking → embeddings → vector DB → retrieval API
```

---

# 12. Easy real-world examples

## Example 1: Food delivery API

```text
POST /orders
```

Request:

```json
{
  "user_id": "u1",
  "items": ["pizza", "coke"]
}
```

Response:

```json
{
  "order_id": "ord-101",
  "status": "created"
}
```

## Example 2: GenAI chat API

```text
POST /api/v1/chat/completions
```

Request:

```json
{
  "user_id": "u1",
  "message": "Explain Kubernetes simply"
}
```

Response:

```json
{
  "answer": "Kubernetes is like an operating system for containers..."
}
```

## Example 3: AI document Q&A API

```text
POST /api/v1/documents/upload
POST /api/v1/chat/completions
```

Flow:

```text
Upload document first
Ask question later
Backend retrieves relevant document chunks
LLM generates final answer
```

---

# 13. ASCII diagram

```text
+-----------+       HTTP Request        +-------------+
|  Client   |  -----------------------> |  FastAPI    |
| Web/Mobile|                           |  API Layer  |
+-----------+                           +-------------+
                                               |
                                               | Validated Pydantic model
                                               v
                                      +------------------+
                                      | Service Layer    |
                                      | Chat / Documents |
                                      +------------------+
                                               |
                                               | Calls AI workflow
                                               v
                                      +------------------+
                                      | LLM / Vector DB  |
                                      | Storage / Logs   |
                                      +------------------+
                                               |
                                               | JSON result
                                               v
+-----------+       HTTP Response       +-------------+
|  Client   |  <----------------------- |  FastAPI    |
+-----------+                           +-------------+
```

---

# 14. Pseudocode first

```text
START application

Create FastAPI app

Define API version prefix as /api/v1

Define request model for chat:
    user_id
    conversation_id
    message
    model
    temperature
    max_tokens
    document_ids

Define response model for chat:
    conversation_id
    answer
    model
    usage

Define response model for document upload:
    document_id
    filename
    content_type
    status

Create health route:
    return status ok

Create chat completion route:
    receive validated chat request
    if message is empty:
        return 400 error
    call chat service
    service creates fake AI answer
    return answer and token usage

Create document upload route:
    receive file
    validate file type
    validate file size
    create document ID
    return upload response

Create document read route:
    receive document_id
    if document not found:
        return 404 error
    return document metadata

Run API server
END
```

---

# 15. Python FastAPI script

Install first:

```bash
pip install fastapi uvicorn python-multipart
```

Save as:

```text
main.py
```

```python
# 1
from typing import List, Optional, Dict

# 2
from uuid import uuid4

# 3
from fastapi import FastAPI, UploadFile, File, HTTPException, status

# 4
from pydantic import BaseModel, Field


# 5
app = FastAPI(
    title="GenAI Backend API",
    description="FastAPI example for chat completion and document upload",
    version="1.0.0",
)


# 6
API_PREFIX = "/api/v1"


# 7
fake_document_store: Dict[str, dict] = {}


# 8
class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int


# 9
class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="Unique user ID")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID")
    message: str = Field(..., min_length=1, max_length=4000)
    model: str = Field(default="demo-llm")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=500, ge=1, le=4000)
    document_ids: List[str] = Field(default_factory=list)


# 10
class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    model: str
    usage: TokenUsage


# 11
class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    status: str


# 12
class DocumentMetadataResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str
    size_bytes: int
    status: str


# 13
def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


# 14
def generate_demo_answer(message: str, document_ids: List[str]) -> str:
    if document_ids:
        return f"Demo answer using documents {document_ids}: You asked '{message}'."
    return f"Demo answer: You asked '{message}'."


# 15
@app.get(f"{API_PREFIX}/health")
def health_check():
    return {"status": "ok"}


# 16
@app.post(
    f"{API_PREFIX}/chat/completions",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def create_chat_completion(request: ChatRequest):
    conversation_id = request.conversation_id or f"conv-{uuid4().hex[:8]}"

    for document_id in request.document_ids:
        if document_id not in fake_document_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error_code": "DOCUMENT_NOT_FOUND",
                    "message": "One or more documents were not found",
                    "document_id": document_id,
                },
            )

    answer = generate_demo_answer(
        message=request.message,
        document_ids=request.document_ids,
    )

    input_tokens = estimate_tokens(request.message)
    output_tokens = estimate_tokens(answer)

    return ChatResponse(
        conversation_id=conversation_id,
        answer=answer,
        model=request.model,
        usage=TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        ),
    )


# 17
@app.post(
    f"{API_PREFIX}/documents/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(file: UploadFile = File(...)):
    allowed_content_types = {
        "application/pdf",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "UNSUPPORTED_FILE_TYPE",
                "message": "Only PDF, TXT, and DOCX files are supported",
                "content_type": file.content_type,
            },
        )

    content = await file.read()
    size_bytes = len(content)

    max_size_bytes = 5 * 1024 * 1024

    if size_bytes > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "FILE_TOO_LARGE",
                "message": "File size must be less than or equal to 5 MB",
                "size_bytes": size_bytes,
            },
        )

    document_id = f"doc-{uuid4().hex[:8]}"

    fake_document_store[document_id] = {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": size_bytes,
        "status": "uploaded",
    }

    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        content_type=file.content_type,
        status="uploaded",
    )


# 18
@app.get(
    f"{API_PREFIX}/documents/{{document_id}}",
    response_model=DocumentMetadataResponse,
    status_code=status.HTTP_200_OK,
)
def get_document_metadata(document_id: str):
    document = fake_document_store.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "DOCUMENT_NOT_FOUND",
                "message": "Document was not found",
                "document_id": document_id,
            },
        )

    return DocumentMetadataResponse(**document)
```

Run:

```bash
uvicorn main:app --reload
```

Open docs:

```text
http://127.0.0.1:8000/docs
```

---

# 16. Line-by-line explanation

| Line | Explanation                                                                                                                            |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Imports Python typing helpers for lists, optional values, and dictionaries.                                                            |
| 2    | Imports `uuid4` to generate unique IDs for conversations and documents.                                                                |
| 3    | Imports FastAPI classes for app creation, file upload, errors, and status codes.                                                       |
| 4    | Imports Pydantic tools for request and response models.                                                                                |
| 5    | Creates the FastAPI application and adds metadata for API docs.                                                                        |
| 6    | Defines the API version prefix `/api/v1`.                                                                                              |
| 7    | Creates an in-memory fake document store. In production, this would be a database.                                                     |
| 8    | Defines a response model for token usage.                                                                                              |
| 9    | Defines the chat request schema. It validates user ID, message, model settings, and document IDs.                                      |
| 10   | Defines the chat response schema. The API must return this shape.                                                                      |
| 11   | Defines the response returned after a document upload.                                                                                 |
| 12   | Defines the response returned when reading document metadata.                                                                          |
| 13   | Creates a simple token estimator using word count. Real systems use tokenizer libraries.                                               |
| 14   | Creates a fake AI answer. Real systems would call an LLM service here.                                                                 |
| 15   | Defines a health check endpoint for monitoring.                                                                                        |
| 16   | Defines the chat completion endpoint. It validates documents, generates an answer, estimates usage, and returns a structured response. |
| 17   | Defines the document upload endpoint. It validates file type, file size, creates a document ID, and stores metadata.                   |
| 18   | Defines a document metadata endpoint. It returns document info or a `404` error.                                                       |

---

# 17. Testing with curl

## Health check

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Response:

```json
{
  "status": "ok"
}
```

## Chat completion

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "message": "Explain FastAPI in simple terms",
    "temperature": 0.2,
    "max_tokens": 200
  }'
```

Response:

```json
{
  "conversation_id": "conv-a1b2c3d4",
  "answer": "Demo answer: You asked 'Explain FastAPI in simple terms'.",
  "model": "demo-llm",
  "usage": {
    "input_tokens": 5,
    "output_tokens": 8
  }
}
```

## Upload document

```bash
curl -X POST http://127.0.0.1:8000/api/v1/documents/upload \
  -F "file=@notes.txt"
```

Response:

```json
{
  "document_id": "doc-a1b2c3d4",
  "filename": "notes.txt",
  "content_type": "text/plain",
  "status": "uploaded"
}
```

---

# 18. How backend code connects to AI workflows

In real production systems, your API is only the front door.

```text
POST /documents/upload
        |
        v
Store file in S3/GCS
        |
        v
Extract text from PDF/DOCX
        |
        v
Split text into chunks
        |
        v
Create embeddings
        |
        v
Save embeddings in vector DB
```

Then chat works like this:

```text
POST /chat/completions
        |
        v
Validate request
        |
        v
Retrieve relevant document chunks
        |
        v
Build prompt
        |
        v
Call LLM
        |
        v
Return answer with citations/metadata
```

In a serious GenAI backend, you usually separate the code into layers:

```text
api/
  routes/chat.py
  routes/documents.py

schemas/
  chat.py
  documents.py

services/
  chat_service.py
  document_service.py
  embedding_service.py

repositories/
  document_repository.py
  vector_repository.py

core/
  config.py
  logging.py
  errors.py
```

---

# 19. Clean REST API design for GenAI apps

## Good chat route

```text
POST /api/v1/chat/completions
```

Why good?

```text
It creates a completion.
It is versioned.
It clearly belongs to chat.
It matches common LLM API patterns.
```

## Less ideal route

```text
POST /ask-ai
```

Why weaker?

```text
Not versioned.
Not resource-oriented.
Hard to expand later.
```

## Good document route

```text
POST /api/v1/documents/upload
GET  /api/v1/documents/{document_id}
DELETE /api/v1/documents/{document_id}
```

Why good?

```text
Documents are treated as resources.
Each document has an ID.
The API can grow naturally.
```

---

# 20. Common mistakes

## Mistake 1: No request validation

Bad:

```python
def chat(request: dict):
    pass
```

Better:

```python
def chat(request: ChatRequest):
    pass
```

## Mistake 2: Returning random response shapes

Bad:

```json
{
  "data": "answer"
}
```

Then another endpoint returns:

```json
{
  "result": "answer"
}
```

Better: keep response patterns consistent.

## Mistake 3: No API versioning

Bad:

```text
/chat
/documents/upload
```

Better:

```text
/api/v1/chat/completions
/api/v1/documents/upload
```

## Mistake 4: Wrong status codes

Bad:

```python
return {"error": "not found"}
```

Better:

```python
raise HTTPException(status_code=404, detail="Document not found")
```

## Mistake 5: Putting all logic inside API routes

Bad:

```text
Route does validation, database calls, LLM calls, logging, embedding, storage.
```

Better:

```text
Route → Service → Repository → External systems
```

## Mistake 6: No file validation

Never accept unlimited files blindly.

Validate:

```text
File type
File size
User ownership
Virus/malware risk
Storage location
```

## Mistake 7: Not thinking about cost

Every GenAI request may cost money.

Track:

```text
Input tokens
Output tokens
Model used
User ID
Request latency
Error rate
```

---

# 21. Interview relevance for Google/Amazon/Netflix-style roles

## For SDE roles

You should be able to explain:

```text
How REST works
How request validation works
How to design clean routes
How to handle errors
How to structure backend services
How to test APIs
```

## For AI Platform roles

You should connect FastAPI to:

```text
LLM gateway
Prompt orchestration
Embeddings
Vector search
Document ingestion
Model monitoring
Rate limiting
Cost tracking
```

## For Solution Architect roles

You should discuss:

```text
API Gateway
Authentication
Load balancing
Autoscaling
Object storage
Database choice
Vector database
Observability
Security
```

Example architecture:

```text
Client
  ↓
API Gateway
  ↓
FastAPI service
  ↓
Chat service
  ↓
Retriever service → Vector DB
  ↓
LLM provider
  ↓
Response
```

## For TPM roles

You should think about:

```text
API contract ownership
SLA and latency targets
Rollout plan
Backward compatibility
Model cost tracking
Security review
Cross-team dependencies
```

## Strong interview answer

A strong answer sounds like this:

```text
I would expose versioned REST APIs using FastAPI. 
The API layer would validate requests using Pydantic models. 
The route handler would remain thin and delegate business logic to services. 
For document Q&A, uploads would go through a document ingestion pipeline with storage, text extraction, chunking, embedding, and vector indexing. 
The chat endpoint would retrieve relevant chunks, build a prompt, call the LLM, and return a structured response with usage metadata and clear error codes.
```

---

# 22. DSA topic: Strings

A **string** is a sequence of characters.

Examples:

```text
"hello"
"google"
"racecar"
"abc123"
```

In interviews, string questions test:

```text
Character counting
Two pointers
Sliding window
Hash maps
Prefix/suffix logic
Palindrome checks
Anagram checks
Substring problems
```

---

# 23. DSA string patterns

## Pattern 1: Frequency map

Use when you need to count characters.

Example:

```text
"banana"
b → 1
a → 3
n → 2
```

Common problems:

```text
Valid anagram
First unique character
Character replacement
Group anagrams
```

Time complexity:

```text
O(n)
```

Space complexity:

```text
O(k)
```

Where `k` is the number of unique characters.

---

## Pattern 2: Two pointers

Use when checking from both ends.

Example:

```text
racecar
^     ^
left  right
```

Common problems:

```text
Palindrome
Reverse string
Valid palindrome with cleanup
```

Time complexity:

```text
O(n)
```

Space complexity:

```text
O(1)
```

---

## Pattern 3: Sliding window

Use for substring problems.

Example:

```text
Find longest substring without repeating characters.

abcabcbb
[abc] is valid
```

Common problems:

```text
Longest substring without repeating characters
Minimum window substring
Longest repeating character replacement
```

Time complexity:

```text
O(n)
```

Space complexity:

```text
O(k)
```

---

## Pattern 4: Prefix and suffix

Use when comparing starts and ends of strings.

Common problems:

```text
Longest common prefix
String matching
Remove prefix/suffix
```

Time complexity:

```text
O(n * m)
```

For `n` strings and average length `m`.

---

# 24. One string practice question

## Problem: Valid Anagram

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`.

An anagram means both strings contain the same characters with the same frequency.

Example:

```text
Input:
s = "listen"
t = "silent"

Output:
true
```

Example:

```text
Input:
s = "rat"
t = "car"

Output:
false
```

---

## Approach

Use a frequency map.

```text
If lengths are different:
    return false

Create character count map

For each character in s:
    increase count

For each character in t:
    decrease count
    if count becomes negative:
        return false

Return true
```

Time complexity:

```text
O(n)
```

Space complexity:

```text
O(1)
```

For lowercase English letters, because there are only 26 possible characters.

---

## Golang solution

```go
package main

import "fmt"

func isAnagram(s string, t string) bool {
	if len(s) != len(t) {
		return false
	}

	count := make([]int, 26)

	for i := 0; i < len(s); i++ {
		count[s[i]-'a']++
		count[t[i]-'a']--
	}

	for i := 0; i < 26; i++ {
		if count[i] != 0 {
			return false
		}
	}

	return true
}

func main() {
	fmt.Println(isAnagram("listen", "silent")) // true
	fmt.Println(isAnagram("rat", "car"))       // false
}
```

---

## Golang solution explanation

```go
if len(s) != len(t)
```

If the lengths are different, they cannot be anagrams.

```go
count := make([]int, 26)
```

Creates an array for 26 lowercase English letters.

```go
count[s[i]-'a']++
```

Increases the count for a character in `s`.

```go
count[t[i]-'a']--
```

Decreases the count for a character in `t`.

```go
if count[i] != 0
```

If any character count is not zero, the strings are not anagrams.

---

# 25. Day 2 takeaway

Today’s core lesson:

```text
FastAPI gives you the API layer.
Pydantic gives you validation.
REST gives you structure.
Status codes give clients clarity.
Service layers connect APIs to GenAI workflows.
```

For GenAI backend interviews, always connect API design to real AI platform concerns:

```text
Validation
Cost
Latency
Model calls
Document ingestion
Vector search
Error handling
Observability
Versioning
Security
```
# DSA: Strings basics in Go

## 1. Beginner summary

A **string** is a sequence of characters.
In Go, strings are **immutable**, meaning you cannot modify them directly.
`len(s)` gives the number of **bytes**, not always the number of human-visible characters.
For simple lowercase English strings, you can safely use indexing like `s[i]`.
For Unicode text, use `rune`.

---

# 2. String basics in Go

## Declaring strings

### Go

```go
name := "Google"
message := "Hello, backend engineer"
```

### Python equivalent

```python
name = "Google"
message = "Hello, backend engineer"
```

Go uses `:=` for short variable declaration.

---

## String length

### Go

```go
s := "hello"
fmt.Println(len(s)) // 5
```

### Python

```python
s = "hello"
print(len(s)) # 5
```

For normal English letters, both behave similarly.

But with Unicode:

### Go

```go
s := "नमस्ते"
fmt.Println(len(s)) // bytes, not characters
```

### Python

```python
s = "नमस्ते"
print(len(s)) # characters, usually more intuitive
```

Important interview point:

```text
In Go, len(string) returns byte count.
For Unicode-safe character iteration, use rune.
```

---

# 3. Accessing characters

## Go

```go
s := "hello"

fmt.Println(s[0])        // 104
fmt.Println(string(s[0])) // h
```

In Go, `s[0]` gives a **byte**, not a character string.

## Python

```python
s = "hello"

print(s[0]) # h
```

Python directly gives a one-character string.

---

# 4. Looping through a string

## Byte-based loop

Good for lowercase English strings:

```go
s := "hello"

for i := 0; i < len(s); i++ {
    fmt.Println(string(s[i]))
}
```

Similar Python:

```python
s = "hello"

for ch in s:
    print(ch)
```

---

## Rune-based loop

Better for Unicode:

```go
s := "नमस्ते"

for index, ch := range s {
    fmt.Println(index, string(ch))
}
```

Here, `ch` is a `rune`.

A `rune` is Go’s way of representing a Unicode character.

---

# 5. Strings are immutable

You cannot do this in Go:

```go
s := "hello"
s[0] = 'H' // error
```

You also cannot directly modify strings in Python:

```python
s = "hello"
s[0] = "H" # error
```

To modify a string in Go, convert it to a byte slice or rune slice.

## Go example

```go
s := "hello"

chars := []byte(s)
chars[0] = 'H'

s = string(chars)

fmt.Println(s) // Hello
```

## Python equivalent

```python
s = "hello"

chars = list(s)
chars[0] = "H"

s = "".join(chars)

print(s) # Hello
```

---

# 6. Common string operations in Go

Import:

```go
import "strings"
```

## Contains

```go
strings.Contains("hello", "ell") // true
```

Python:

```python
"ell" in "hello"
```

---

## Prefix

```go
strings.HasPrefix("backend", "back") // true
```

Python:

```python
"backend".startswith("back")
```

---

## Suffix

```go
strings.HasSuffix("main.go", ".go") // true
```

Python:

```python
"main.go".endswith(".go")
```

---

## Split

```go
parts := strings.Split("a,b,c", ",")
```

Python:

```python
parts = "a,b,c".split(",")
```

---

## Join

```go
result := strings.Join([]string{"a", "b", "c"}, "-")
fmt.Println(result) // a-b-c
```

Python:

```python
result = "-".join(["a", "b", "c"])
print(result) # a-b-c
```

---

# 7. Go vs Python string syntax and conventions

| Concept            | Go                            | Python           |
| ------------------ | ----------------------------- | ---------------- |
| Declare string     | `s := "hello"`                | `s = "hello"`    |
| Length             | `len(s)`                      | `len(s)`         |
| First character    | `string(s[0])`                | `s[0]`           |
| Loop               | `for i := 0; i < len(s); i++` | `for ch in s`    |
| Unicode-safe loop  | `for _, ch := range s`        | `for ch in s`    |
| Mutable string?    | No                            | No               |
| Convert to mutable | `[]byte(s)` or `[]rune(s)`    | `list(s)`        |
| Join strings       | `strings.Join(arr, "")`       | `"".join(arr)`   |
| String library     | `strings` package             | built-in methods |

---

# 8. Important DSA patterns for strings

## Pattern 1: Frequency counting

Used for:

```text
Anagram
First unique character
Character frequency
Duplicate detection
```

Example idea:

```go
count := make(map[byte]int)
```

Or for lowercase English letters:

```go
count := make([]int, 26)
```

---

## Pattern 2: Two pointers

Used for:

```text
Palindrome
Reverse string
Compare from both ends
```

Example:

```text
racecar
^     ^
left  right
```

---

## Pattern 3: Sliding window

Used for:

```text
Longest substring without repeating characters
Minimum window substring
Longest substring with at most K distinct characters
```

---

# 9. Easy string problem

## Problem: Reverse a String

Given a string, return the reversed string.

Example:

```text
Input:  "hello"
Output: "olleh"
```

Another example:

```text
Input:  "google"
Output: "elgoog"
```

---

# 10. Brute-force thinking

Create an empty result string.
Loop from the end of the original string to the beginning.
Add each character to the result.

Pseudocode:

```text
function reverseString(s):
    result = ""

    for i from len(s)-1 down to 0:
        result = result + s[i]

    return result
```

This works, but repeated string concatenation can be inefficient because strings are immutable.

Time complexity can become:

```text
O(n²)
```

---

# 11. Better Go solution

Use a byte slice for simple English strings.

```go
package main

import "fmt"

func reverseString(s string) string {
    chars := []byte(s)

    left := 0
    right := len(chars) - 1

    for left < right {
        chars[left], chars[right] = chars[right], chars[left]
        left++
        right--
    }

    return string(chars)
}

func main() {
    fmt.Println(reverseString("hello"))  // olleh
    fmt.Println(reverseString("google")) // elgoog
}
```

---

# 12. Line-by-line explanation

```go
func reverseString(s string) string
```

Defines a function that takes a string and returns a string.

```go
chars := []byte(s)
```

Converts the string into a byte slice so we can modify it.

```go
left := 0
right := len(chars) - 1
```

Creates two pointers: one at the start and one at the end.

```go
for left < right
```

Runs the loop until the two pointers meet.

```go
chars[left], chars[right] = chars[right], chars[left]
```

Swaps the characters.

```go
left++
right--
```

Moves the pointers inward.

```go
return string(chars)
```

Converts the byte slice back to a string.

---

# 13. Complexity

```text
Time complexity: O(n)
Space complexity: O(n)
```

Why space is `O(n)`?

Because strings are immutable, so we create a new byte slice.

---

# 14. Python equivalent

```python
def reverse_string(s: str) -> str:
    chars = list(s)

    left = 0
    right = len(chars) - 1

    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1

    return "".join(chars)


print(reverse_string("hello"))   # olleh
print(reverse_string("google"))  # elgoog
```

Python shortcut:

```python
s[::-1]
```

But in interviews, explain the two-pointer logic.

---

# 15. Interview notes

For Go string problems, always clarify:

```text
Are inputs only lowercase English letters?
Do we need Unicode support?
Can we use extra space?
Should we return a new string or modify in-place?
```

For most beginner DSA problems, assume lowercase English letters unless stated otherwise.

Strong answer:

```text
In Go, strings are immutable and indexing gives bytes. 
For ASCII strings, I can convert to []byte and use two pointers. 
For Unicode-safe reversal, I should use []rune instead.
```

Unicode-safe version:

```go
func reverseUnicodeString(s string) string {
    chars := []rune(s)

    left := 0
    right := len(chars) - 1

    for left < right {
        chars[left], chars[right] = chars[right], chars[left]
        left++
        right--
    }

    return string(chars)
}
```
