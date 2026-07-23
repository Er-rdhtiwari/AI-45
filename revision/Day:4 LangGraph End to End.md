# Day 4 — LangGraph End to End

## 1. Core idea in simple words

**LangGraph helps you build AI applications as controlled workflows rather than one uncontrolled LLM call.**

Imagine a Disney guest asks:

> “My ride was cancelled after I purchased Lightning Lane access. Can I get a refund?”

A simple LLM application might immediately generate an answer.

A production system should instead:

1. Understand the request.
2. retrieve the correct policy,
3. check reservation details,
4. determine whether the request is eligible,
5. ask for human approval when necessary,
6. execute the refund safely,
7. confirm that the refund succeeded,
8. save progress if anything fails,
9. produce a grounded response.

LangGraph lets us represent those steps as a **graph**:

```text
State + Nodes + Edges + Persistence = Controlled AI workflow
```

A useful analogy is a theme-park operations map:

* **State** = the case file travelling through the park.
* **Nodes** = teams performing work.
* **Edges** = rules deciding which team receives the case next.
* **Tools** = systems those teams can operate.
* **Checkpoints** = saved progress.
* **Interrupts** = pauses for manager approval.
* **Recovery** = continuing from the last safe point after failure.

LangGraph is currently described as a low-level orchestration framework and runtime for long-running, stateful agents. Its main capabilities include persistence, durable execution, streaming and human-in-the-loop control. LangChain components are commonly used with it, but LangGraph does not require LangChain. ([Docs by LangChain][1])

---

# 2. Foundational concepts

## 2.1 What is LangGraph?

LangGraph is a framework for creating applications whose execution can:

* move through multiple steps,
* branch into different paths,
* repeat steps,
* call external tools,
* maintain shared state,
* pause for human input,
* recover after failures,
* continue over a long period.

Instead of writing:

```python
answer = llm.invoke(question)
```

you design something closer to:

```text
Understand request
       ↓
Retrieve information
       ↓
Validate evidence
       ↓
Decide next action
       ↓
Call tool or ask human
       ↓
Verify outcome
       ↓
Respond
```

At its core, LangGraph represents workflows using three main concepts:

1. **State** — the current data snapshot.
2. **Nodes** — functions that perform work.
3. **Edges** — rules that select the next node.

Nodes can contain LLM calls, ordinary Python code, database queries, API calls or validation logic. ([Docs by LangChain][2])

---

## 2.2 What problem does LangGraph solve?

LLMs are good at understanding language and making fuzzy decisions.

LLMs are not naturally good at:

* remembering exact workflow progress,
* guaranteeing that required steps are executed,
* controlling how many times a tool is called,
* recovering safely after a crash,
* pausing for approval,
* enforcing business rules,
* showing developers exactly what happened.

Consider a refund agent.

Without workflow control, the LLM might:

* skip policy retrieval,
* misunderstand the refund amount,
* call the refund API twice,
* continue retrying indefinitely,
* perform a refund without approval,
* lose progress when the server restarts.

LangGraph provides the **execution structure** around the model.

> The LLM supplies intelligence.
> LangGraph supplies workflow control.

---

## 2.3 Why simple chains are not enough

A chain normally follows a predictable sequence:

```text
Input → Prompt → LLM → Parser → Output
```

This is excellent for:

* summarization,
* classification,
* translation,
* simple RAG,
* one-time structured extraction.

But many production workflows are not straight lines.

A real workflow may need:

```text
                    ┌── ask for clarification ──┐
                    │                           │
Input → classify → retrieve → validate ─────────┘
                    │
                    ├── low risk → execute automatically
                    │
                    ├── medium risk → apply more validation
                    │
                    └── high risk → human approval
```

You need LangGraph-style orchestration when the application contains:

* branching,
* loops,
* multi-step state,
* tool execution,
* approvals,
* retries,
* long-running work,
* pause and resume,
* different recovery paths.

---

## 2.4 LangChain versus LangGraph

| Area              | LangChain                                          | LangGraph                                            |
| ----------------- | -------------------------------------------------- | ---------------------------------------------------- |
| Main purpose      | Components and higher-level agent abstractions     | Stateful workflow orchestration                      |
| Useful for        | Models, prompts, tools, retrievers and agent loops | Branches, loops, persistence, approvals and recovery |
| Abstraction level | Higher-level                                       | Lower-level and more controllable                    |
| Typical flow      | Chain or prebuilt agent                            | Custom graph                                         |
| State control     | Usually simpler                                    | Explicit shared state                                |
| Human approval    | Possible through integrations                      | A core orchestration pattern                         |
| Recovery          | Application-dependent                              | Checkpoint-based execution                           |
| Best analogy      | AI application toolkit                             | Workflow control engine                              |

A simple way to remember this:

> **LangChain gives you AI components. LangGraph coordinates how those components operate over time.**

LangChain’s higher-level agents use LangGraph underneath for orchestration. When the prebuilt agent loop is sufficient, you may not need to build a custom LangGraph. When you need deeper control, you can work directly with LangGraph primitives. ([Docs by LangChain][1])

---

## 2.5 Deterministic workflow versus agentic workflow

### Deterministic workflow

Your code decides the route.

```python
if refund_amount > 100:
    return "manager_approval"
else:
    return "execute_refund"
```

The LLM does not decide whether approval is required.

This is appropriate for:

* financial actions,
* access control,
* compliance checks,
* security-sensitive operations,
* strict business rules.

### Agentic workflow

The LLM helps decide the next action.

```text
LLM examines the request
        ↓
LLM decides whether to:
- retrieve policy,
- search reservation,
- ask a question,
- call another tool,
- provide an answer
```

This is appropriate when:

* the path is difficult to express with fixed rules,
* information gathering is exploratory,
* the input can take many forms,
* the action remains low-risk.

### Hybrid workflow

Most serious production systems should be **hybrid**:

```text
Deterministic outer workflow
        ↓
Small agentic decision area
        ↓
Deterministic validation
        ↓
Controlled tool execution
```

For example:

* Let the LLM understand the guest’s intent.
* Let the LLM choose which read-only information tool to use.
* Do not let the LLM independently decide whether a ₹50,000 refund is allowed.
* Use code and policy rules for authorization.
* Require human approval for high-risk actions.

---

## 2.6 When LangGraph is a good fit

Use LangGraph when several of these are true:

* The workflow has branches or loops.
* It uses multiple tools.
* It may run for a long time.
* It must pause and resume.
* Human approval is required.
* State must survive a process restart.
* Failures must resume from a safe point.
* You need detailed step-level observability.
* The LLM should have limited rather than unlimited autonomy.
* Different error types require different recovery paths.

### Disney-like examples

Hypothetical examples include:

* guest service case resolution,
* park incident triage,
* content compliance review,
* promotional campaign approval,
* production asset metadata processing,
* internal policy assistance,
* travel reservation change workflows.

---

## 2.7 When LangGraph may be unnecessary

Do not add LangGraph simply because an application uses an LLM.

It may be unnecessary for:

```text
User question → retrieve documents → generate answer
```

or:

```text
Text → extract structured fields
```

or:

```text
Review → classify as positive or negative
```

For these cases, a normal function, a simple LangChain pipeline or a regular backend service may be easier.

LangGraph introduces:

* more concepts,
* more state,
* more code,
* more testing,
* more operational complexity.

> Use the simplest architecture that provides the control you need.

---

# 3. LangGraph building blocks

## 3.1 State

**State is the shared case file for the workflow.**

Every node can read relevant parts of the state. Nodes return updates that change the state.

A hypothetical Disney guest-support state might look like this:

```python
class GuestCaseState:
    request_id: str
    guest_question: str
    guest_id: str | None

    intent: str | None
    reservation_details: dict | None
    retrieved_policies: list
    evidence_quality: str | None

    proposed_action: dict | None
    risk_level: str | None
    approval_status: str | None

    tool_result: dict | None
    retry_count: int
    errors: list

    final_answer: str | None
    status: str
```

### State should contain

* inputs,
* intermediate results,
* decisions,
* counters,
* error information,
* final output,
* audit information.

### State should normally not contain

* database connections,
* HTTP clients,
* open files,
* secrets,
* huge binary objects,
* unnecessary duplicated prompts.

Instead of storing an entire video or document, store:

```python
{
    "asset_id": "asset-783",
    "storage_uri": "secure-object-reference"
}
```

### Store raw data, not display-formatted data

Better:

```python
{
    "refund_amount": 75,
    "currency": "USD",
    "policy_id": "refund-policy-v4"
}
```

Less reusable:

```python
{
    "refund_text": "The guest should receive a $75 refund under policy v4."
}
```

Raw state can be used by:

* validation nodes,
* response nodes,
* audit systems,
* monitoring systems.

The LangGraph documentation recommends thinking of state as shared memory and breaking work into discrete nodes that do one thing well. ([Docs by LangChain][3])

---

## 3.2 State schema

The **state schema** defines what data is allowed in the state.

A strong schema helps answer:

* Which fields are required?
* Which fields may be missing?
* Which node owns each field?
* Which values are valid?
* How are parallel updates combined?
* Which fields contain sensitive information?
* Which fields must be persisted?

Example:

```python
from typing import Literal, TypedDict

class CaseState(TypedDict):
    request_id: str
    question: str
    intent: Literal["refund", "information", "complaint", "unknown"] | None
    retry_count: int
    status: Literal[
        "received",
        "researching",
        "waiting_for_approval",
        "executing",
        "completed",
        "failed"
    ]
```

### Reducers

Suppose two nodes run in parallel:

```text
retrieve_policy ─────┐
                     ├── combine evidence
retrieve_booking ────┘
```

Both may update an `evidence` list.

A **reducer** defines how concurrent updates should be combined:

```text
Current evidence + new evidence
```

rather than one update overwriting the other. Parallel state fields need a clear merging strategy; otherwise concurrent updates can conflict. ([Docs by LangChain][4])

---

## 3.3 Nodes

A node is a function that performs one meaningful step.

```python
def classify_request(state):
    intent = classify_with_model(state["question"])
    return {"intent": intent}
```

Another node:

```python
def retrieve_policy(state):
    documents = policy_retriever.search(state["question"])
    return {"retrieved_policies": documents}
```

Another:

```python
def validate_evidence(state):
    valid = len(state["retrieved_policies"]) > 0
    return {"evidence_quality": "good" if valid else "missing"}
```

### Good node design

```text
classify_request
retrieve_policy
lookup_reservation
validate_evidence
calculate_eligibility
request_approval
execute_refund
verify_refund
generate_response
```

### Poor node design

```text
process_everything
```

A large node is difficult to:

* test,
* retry,
* observe,
* resume,
* optimize,
* replace.

> A node should represent one operational responsibility.

Nodes are ordinary functions. They receive state, perform computation or side effects, and return state updates. ([Docs by LangChain][2])

---

## 3.4 Edges

Edges determine what runs next.

### Fixed edge

```text
classify → retrieve_policy
```

```python
builder.add_edge("classify", "retrieve_policy")
```

### Conditional edge

```text
validate_evidence
     ├── valid → plan_action
     └── missing → ask_clarification
```

```python
def route_after_validation(state):
    if state["evidence_quality"] == "good":
        return "plan_action"
    return "ask_clarification"
```

Edges are where you express **control flow**.

---

## 3.5 Control flow

Control flow means:

> “Under this condition, which step should run next?”

Common graph patterns include:

### Sequence

```text
A → B → C
```

### Branch

```text
       ┌→ B
A ─────┤
       └→ C
```

### Loop

```text
A → B → validate
    ↑       │
    └───────┘
```

### Parallel work

```text
         ┌→ retrieve policy ────┐
Start ───┤                      ├→ combine
         └→ retrieve booking ───┘
```

### Approval gate

```text
proposed action → human approval → execute or cancel
```

LangGraph supports sequences, branches, loops and other graph structures through its Graph API. ([Docs by LangChain][5])

---

## 3.6 Conditional routing

Conditional routing can be based on:

### Code-based rules

```python
if amount > approval_limit:
    return "human_approval"
```

### Model-based classification

```python
intent = llm_classify(question)
return intent
```

### Validation results

```python
if policy_evidence_is_missing:
    return "retrieve_again"
```

### Tool outcomes

```python
if tool_result.status == "temporary_error":
    return "retry"
elif tool_result.status == "not_found":
    return "ask_guest"
else:
    return "continue"
```

For high-risk decisions, prefer deterministic rules.

For fuzzy language understanding, model-based routing may be appropriate.

---

## 3.7 Tool execution steps

A tool is an operation the AI workflow can call.

Examples:

* retrieve policy documents,
* search booking records,
* retrieve attraction status,
* create a support ticket,
* process an approved refund,
* notify an operations team.

A controlled tool pattern is:

```text
LLM proposes tool call
        ↓
Validate tool name
        ↓
Validate arguments
        ↓
Check permission
        ↓
Check approval requirement
        ↓
Execute tool
        ↓
Validate tool result
        ↓
Record audit event
```

Do not design:

```text
LLM → unrestricted production tool
```

Design:

```text
LLM → proposed action → policy validation → authorization → tool
```

---

## 3.8 Checkpointing

A checkpoint is a saved snapshot of graph state.

Suppose the graph reaches:

```text
classify ✓
retrieve policy ✓
calculate eligibility ✓
manager approval pending
```

A checkpoint lets the system remember that progress.

If the server restarts, it should not necessarily repeat all previous work. It can load the saved state and continue from the appropriate step.

LangGraph checkpointers save graph state at super-step boundaries. They enable human-in-the-loop workflows, conversational continuity, time-travel debugging and failure recovery. A `thread_id` identifies the saved execution history. ([Docs by LangChain][6])

### Thread

A thread is the persistent identity of one workflow history.

Example:

```python
config = {
    "configurable": {
        "thread_id": "guest-case-9812"
    }
}
```

Always resume with the same thread ID.

### Development versus production

Development:

```python
InMemorySaver()
```

Production:

```text
Persistent database-backed checkpointer
```

An in-memory checkpointer loses data when the process restarts. The official documentation lists database-backed options such as PostgreSQL for production use. ([Docs by LangChain][7])

---

## 3.9 Durable execution

**Durable execution means the workflow can survive interruptions and continue from persisted progress.**

For example:

```text
10:00 — Case starts
10:01 — Policy retrieved
10:02 — Manager approval requested
14:30 — Manager approves
14:31 — Workflow resumes
```

The application does not need to keep one web request open for four hours.

### Important nuance

Durable does not mean every individual line of code continues from the exact CPU instruction.

When a paused node resumes, the node may restart from its beginning. Therefore, operations before an interrupt must be designed carefully. Side effects should be **idempotent**.

**Idempotent** means repeating the same operation does not create an incorrect duplicate result.

Example:

```python
refund(
    request_id="guest-case-9812",
    idempotency_key="refund-guest-case-9812"
)
```

If the same refund call is repeated, the external system recognizes that it is the same request instead of issuing two refunds.

LangGraph checkpoints graph progress and can restart from the last successful step. Successful writes from parallel nodes can also be retained when another node in the same step fails. ([Docs by LangChain][6])

### Durability modes

LangGraph currently exposes three broad durability choices:

* **`exit`** — persist when execution exits; fastest but weakest mid-run recovery.
* **`async`** — persist while the next step runs; balances speed and durability.
* **`sync`** — persist before moving to the next step; strongest durability with more overhead. ([Docs by LangChain][6])

For a read-only recommendation workflow, asynchronous durability may be reasonable.

For a high-risk transaction workflow, stronger synchronous persistence may be justified.

---

## 3.10 Human-in-the-loop

Human-in-the-loop means the workflow pauses and requests human input.

Example:

```text
Proposed refund: $250
Policy confidence: 0.76
Reason: exceptional disruption

Approve?
[Approve] [Reject] [Edit]
```

LangGraph uses **interrupts** for this pattern.

```python
from langgraph.types import interrupt

def approval_node(state):
    approval = interrupt({
        "question": "Approve this refund?",
        "amount": state["proposed_action"]["amount"],
        "reason": state["proposed_action"]["reason"]
    })

    return {"approval_status": "approved" if approval else "rejected"}
```

When the graph pauses:

1. current state is saved,
2. the caller receives the approval request,
3. execution waits,
4. the graph resumes with the human response.

A checkpointer and stable thread ID are required for reliable pause-and-resume behavior. ([Docs by LangChain][8])

### Use human review where it adds value

Good approval points:

* high-value refunds,
* account changes,
* safety-related decisions,
* low-confidence compliance decisions,
* public-facing sensitive content.

Poor approval design:

```text
Human approves every retrieved paragraph.
Human approves every harmless recommendation.
Human approves every normal support response.
```

That creates bottlenecks and destroys automation value.

---

## 3.11 Streaming

Streaming means sending progress to the application while the graph is running.

The UI could display:

```text
✓ Request understood
✓ Reservation found
✓ Relevant policy retrieved
• Checking eligibility
• Waiting for manager approval
```

You can also stream LLM tokens:

```text
“Based on the cancellation policy…”
```

Useful stream information includes:

* model message chunks,
* node updates,
* full state snapshots,
* custom progress events,
* checkpoints,
* task events,
* debugging information.

LangGraph exposes different streaming modes such as `updates`, `values`, `messages`, `custom`, `checkpoints`, `tasks` and `debug`. ([Docs by LangChain][9])

Streaming improves user experience, but it does not itself make execution durable. Streaming and checkpointing solve different problems.

---

## 3.12 Retry and recovery

A retry repeats a failed operation.

Example:

```text
Reservation API timeout
        ↓
Wait briefly
        ↓
Retry
```

Not every failure should be retried.

### Retry these carefully

* network timeout,
* temporary 5xx API error,
* rate-limit response,
* temporary database unavailability.

### Usually do not retry these automatically

* invalid input,
* permission denied,
* malformed tool arguments,
* policy rejection,
* nonexistent resource,
* deterministic programming bug.

LangGraph supports per-node retries. Current fault-tolerance mechanisms also include timeouts and error handlers that run after retries are exhausted. ([Docs by LangChain][5])

A bounded retry policy might be:

```text
Maximum attempts: 3
Backoff: 1s, 2s, 4s
Retry only transient failures
After exhaustion: use fallback or escalate
```

Never use an unlimited retry loop.

---

# 4. End-to-end workflow example

## Hypothetical Disney Guest Recovery Assistant

### Business request

A guest says:

> “The attraction closed after I purchased access. I want a refund.”

The assistant must:

* understand the request,
* find the relevant reservation,
* retrieve the current policy,
* determine eligibility,
* avoid unsupported promises,
* get approval for exceptional refunds,
* perform an approved action once,
* provide a clear response.

---

## 4.1 Architecture

```text
                        ┌─────────────────────┐
                        │ Guest application   │
                        └──────────┬──────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Receive request  │
                         └────────┬─────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Classify intent  │
                         └────────┬─────────┘
                                  ▼
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
      ┌──────────────────┐                ┌──────────────────┐
      │ Retrieve policy  │                │ Lookup booking   │
      └────────┬─────────┘                └────────┬─────────┘
               └────────────────┬──────────────────┘
                                ▼
                       ┌──────────────────┐
                       │ Validate inputs  │
                       └────────┬─────────┘
                                │
                 ┌──────────────┴───────────────┐
                 │                              │
           Missing information             Complete
                 │                              │
                 ▼                              ▼
       ┌──────────────────┐          ┌────────────────────┐
       │ Ask guest        │          │ Calculate          │
       │ clarification    │          │ eligibility        │
       └────────┬─────────┘          └─────────┬──────────┘
                │                              ▼
                └───────────────┐     ┌────────────────────┐
                                └────▶│ Risk classification│
                                      └─────────┬──────────┘
                                                │
                 ┌──────────────────────────────┼─────────────────────┐
                 ▼                              ▼                     ▼
          Not eligible                    Low risk              High risk
                 │                              │                     │
                 ▼                              ▼                     ▼
       ┌──────────────────┐          ┌──────────────────┐   ┌─────────────────┐
       │ Explain policy   │          │ Execute action   │   │ Human approval  │
       └────────┬─────────┘          └────────┬─────────┘   └────────┬────────┘
                │                             │                      │
                │                             │             approved / rejected
                │                             │                      │
                │                             ▼                      ▼
                │                    ┌──────────────────┐   ┌─────────────────┐
                │                    │ Verify result    │◀──│ Execute/cancel  │
                │                    └────────┬─────────┘   └─────────────────┘
                └─────────────────────────────┼───────────────────────────────┐
                                              ▼                               │
                                    ┌──────────────────┐                      │
                                    │ Generate answer  │◀─────────────────────┘
                                    └────────┬─────────┘
                                             ▼
                                    ┌──────────────────┐
                                    │ Audit + complete │
                                    └──────────────────┘
```

---

## 4.2 State transitions

### Initial state

```python
{
    "request_id": "case-1007",
    "guest_question": "My attraction closed. Can I get a refund?",
    "intent": None,
    "retrieved_policies": [],
    "reservation_details": None,
    "proposed_action": None,
    "risk_level": None,
    "approval_status": None,
    "retry_count": 0,
    "errors": [],
    "status": "received"
}
```

### After classification

```python
{
    "intent": "refund_request",
    "status": "researching"
}
```

### After retrieval

```python
{
    "retrieved_policies": [
        {
            "policy_id": "POL-REFUND-04",
            "section": "Attraction interruption",
            "effective_date": "..."
        }
    ],
    "reservation_details": {
        "reservation_id": "RSV-91",
        "purchase_status": "confirmed"
    }
}
```

### After planning

```python
{
    "proposed_action": {
        "type": "refund",
        "amount": 75,
        "currency": "USD",
        "reason": "eligible_attraction_interruption"
    },
    "risk_level": "medium"
}
```

### After approval

```python
{
    "approval_status": "approved",
    "status": "executing"
}
```

### Final state

```python
{
    "tool_result": {
        "transaction_id": "TX-818",
        "status": "completed"
    },
    "final_answer": "Your refund was approved and processed...",
    "status": "completed"
}
```

---

## 4.3 Simplified LangGraph-style code

This is an architecture skeleton rather than a complete runnable application:

```python
from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy, interrupt


class GuestCaseState(TypedDict):
    request_id: str
    guest_question: str

    intent: str | None
    retrieved_policies: list[dict]
    reservation_details: dict | None

    eligibility: bool | None
    proposed_action: dict | None
    risk_level: Literal["low", "medium", "high"] | None
    approval_status: Literal["approved", "rejected"] | None

    tool_result: dict | None
    errors: list[str]
    retry_count: int

    final_answer: str | None
    status: str


def classify_request(state: GuestCaseState):
    intent = classify_intent_with_llm(state["guest_question"])

    return {
        "intent": intent,
        "status": "researching"
    }


def retrieve_policy(state: GuestCaseState):
    policies = policy_retriever.search(
        query=state["guest_question"],
        filters={"intent": state["intent"]}
    )

    return {"retrieved_policies": policies}


def lookup_reservation(state: GuestCaseState):
    reservation = reservation_api.find_for_case(
        request_id=state["request_id"]
    )

    return {"reservation_details": reservation}


def validate_inputs(state: GuestCaseState):
    missing_policy = not state["retrieved_policies"]
    missing_reservation = state["reservation_details"] is None

    if missing_policy or missing_reservation:
        return {"status": "needs_clarification"}

    return {"status": "ready_for_decision"}


def route_after_validation(
    state: GuestCaseState,
) -> Literal["ask_clarification", "calculate_eligibility"]:
    if state["status"] == "needs_clarification":
        return "ask_clarification"

    return "calculate_eligibility"


def ask_clarification(state: GuestCaseState):
    # In a conversational application, this could pause or return
    # a question to the guest.
    return {
        "final_answer": "Please provide your reservation number.",
        "status": "waiting_for_guest"
    }


def calculate_eligibility(state: GuestCaseState):
    # Important business policy is enforced with deterministic code.
    eligible, amount = policy_engine.calculate(
        policies=state["retrieved_policies"],
        reservation=state["reservation_details"]
    )

    proposed_action = None

    if eligible:
        proposed_action = {
            "type": "refund",
            "amount": amount,
            "currency": "USD"
        }

    return {
        "eligibility": eligible,
        "proposed_action": proposed_action
    }


def classify_risk(state: GuestCaseState):
    if not state["eligibility"]:
        return {"risk_level": "low"}

    amount = state["proposed_action"]["amount"]

    if amount <= 50:
        risk = "low"
    elif amount <= 200:
        risk = "medium"
    else:
        risk = "high"

    return {"risk_level": risk}


def route_by_risk(
    state: GuestCaseState,
) -> Literal["explain_rejection", "execute_refund", "request_approval"]:
    if not state["eligibility"]:
        return "explain_rejection"

    if state["risk_level"] == "low":
        return "execute_refund"

    return "request_approval"


def request_approval(state: GuestCaseState):
    approved = interrupt({
        "case": state["request_id"],
        "action": state["proposed_action"],
        "question": "Approve this refund?"
    })

    return {
        "approval_status": "approved" if approved else "rejected"
    }


def route_after_approval(
    state: GuestCaseState,
) -> Literal["execute_refund", "explain_rejection"]:
    if state["approval_status"] == "approved":
        return "execute_refund"

    return "explain_rejection"


def execute_refund(state: GuestCaseState):
    result = refund_api.refund(
        reservation_id=state["reservation_details"]["reservation_id"],
        amount=state["proposed_action"]["amount"],

        # Prevent duplicate refunds during retries or replay.
        idempotency_key=f"refund:{state['request_id']}"
    )

    return {
        "tool_result": result,
        "status": "executed"
    }


def verify_result(state: GuestCaseState):
    if state["tool_result"]["status"] != "completed":
        return {
            "status": "execution_failed",
            "errors": ["Refund was not confirmed"]
        }

    return {"status": "verified"}


def route_after_verification(
    state: GuestCaseState,
) -> Literal["generate_response", "manual_recovery"]:
    if state["status"] == "verified":
        return "generate_response"

    return "manual_recovery"


def generate_response(state: GuestCaseState):
    answer = response_llm.generate(
        question=state["guest_question"],
        policy_evidence=state["retrieved_policies"],
        verified_tool_result=state["tool_result"]
    )

    return {
        "final_answer": answer,
        "status": "completed"
    }


def explain_rejection(state: GuestCaseState):
    return {
        "final_answer": "This request does not meet the refund policy...",
        "status": "completed"
    }


def manual_recovery(state: GuestCaseState):
    return {
        "final_answer": "Your request has been sent to a support specialist.",
        "status": "escalated"
    }


builder = StateGraph(GuestCaseState)

builder.add_node("classify", classify_request)
builder.add_node(
    "retrieve_policy",
    retrieve_policy,
    retry_policy=RetryPolicy(max_attempts=3)
)
builder.add_node(
    "lookup_reservation",
    lookup_reservation,
    retry_policy=RetryPolicy(max_attempts=3)
)
builder.add_node("validate_inputs", validate_inputs)
builder.add_node("ask_clarification", ask_clarification)
builder.add_node("calculate_eligibility", calculate_eligibility)
builder.add_node("classify_risk", classify_risk)
builder.add_node("request_approval", request_approval)
builder.add_node(
    "execute_refund",
    execute_refund,
    retry_policy=RetryPolicy(max_attempts=2)
)
builder.add_node("verify_result", verify_result)
builder.add_node("generate_response", generate_response)
builder.add_node("explain_rejection", explain_rejection)
builder.add_node("manual_recovery", manual_recovery)

builder.add_edge(START, "classify")

# These two operations are independent and could be parallelized.
builder.add_edge("classify", "retrieve_policy")
builder.add_edge("classify", "lookup_reservation")

builder.add_edge("retrieve_policy", "validate_inputs")
builder.add_edge("lookup_reservation", "validate_inputs")

builder.add_conditional_edges(
    "validate_inputs",
    route_after_validation
)

builder.add_edge("ask_clarification", END)
builder.add_edge("calculate_eligibility", "classify_risk")

builder.add_conditional_edges(
    "classify_risk",
    route_by_risk
)

builder.add_conditional_edges(
    "request_approval",
    route_after_approval
)

builder.add_edge("execute_refund", "verify_result")

builder.add_conditional_edges(
    "verify_result",
    route_after_verification
)

builder.add_edge("generate_response", END)
builder.add_edge("explain_rejection", END)
builder.add_edge("manual_recovery", END)

graph = builder.compile(checkpointer=production_checkpointer)
```

---

# 5. Inter-relation between state, routing, tools and recovery

These concepts should not be learned separately.

They operate as one system.

## 5.1 State tells the graph what has happened

```python
{
    "eligibility": True,
    "risk_level": "high",
    "approval_status": None
}
```

---

## 5.2 Routing examines state

```python
if state["risk_level"] == "high":
    return "request_approval"
```

---

## 5.3 The approval node updates state

```python
{
    "approval_status": "approved"
}
```

---

## 5.4 Routing examines the updated state

```python
if state["approval_status"] == "approved":
    return "execute_refund"
```

---

## 5.5 The tool node performs the action

```python
{
    "tool_result": {
        "transaction_id": "TX-81",
        "status": "completed"
    }
}
```

---

## 5.6 The checkpoint saves progress

```text
Policy retrieved: yes
Eligibility: yes
Approval: approved
Refund transaction: TX-81
Next node: verify_result
```

---

## 5.7 Recovery uses the checkpoint

If the response-generation node crashes, the system should not issue the refund again.

It can resume with:

```text
Next node: verify_result or generate_response
```

depending on the last committed checkpoint.

The relationship is:

```text
State
  ↓
Routing decision
  ↓
Node or tool operation
  ↓
State update
  ↓
Checkpoint
  ↓
Next routing decision
```

### Memory aid

> **State remembers.
> Nodes work.
> Edges decide.
> Tools act.
> Checkpoints save.
> Recovery resumes.**

---

# 6. Production-grade challenges

## 6.1 Unclear state design

### Problem

The state becomes a random dictionary:

```python
{
    "data": ...,
    "result": ...,
    "temp": ...,
    "new_result": ...,
    "final_result2": ...
}
```

Nobody knows:

* which node owns a value,
* whether the value is current,
* whether it may be missing,
* whether it is safe to persist.

### Consequence

* nodes become tightly coupled,
* debugging becomes difficult,
* state migrations become risky,
* sensitive data may be persisted unintentionally.

### Better approach

Define:

* typed fields,
* field ownership,
* allowed values,
* lifecycle,
* retention rules,
* sensitive-data classification.

---

## 6.2 Workflow sprawl

### Problem

The graph grows into hundreds of nodes and edges.

```text
A → B → C → D → ...
    ↘ X → Y → Z ...
```

### Consequence

* developers cannot understand the full path,
* changes cause unexpected behavior,
* tests become unmanageable.

### Better approach

Use:

* subgraphs,
* domain-based modules,
* reusable nodes,
* clear workflow boundaries.

Example:

```text
Parent graph
  ├── Intake subgraph
  ├── Policy-decision subgraph
  ├── Approval subgraph
  └── Fulfilment subgraph
```

LangGraph supports subgraphs, which allow one graph to operate as a node inside another graph. ([Docs by LangChain][10])

---

## 6.3 Infinite loops

### Problem

```text
Agent → tool → agent → tool → agent → tool ...
```

The model never decides to stop.

### Consequence

* high cost,
* high latency,
* rate-limit problems,
* poor user experience.

### Required controls

```python
max_steps = 12
max_tool_calls = 5
max_retrieval_attempts = 2
deadline_seconds = 30
cost_budget = 0.25
```

Possible stopping conditions:

* no tool call requested,
* answer confidence is sufficient,
* maximum steps reached,
* repeated action detected,
* deadline reached,
* budget reached,
* human escalation required.

---

## 6.4 Tool failures

A tool can fail because of:

* timeout,
* invalid arguments,
* authentication failure,
* upstream outage,
* rate limiting,
* duplicate request,
* inconsistent result.

Do not treat every failure as:

```text
“Ask the LLM what to do.”
```

Classify failures:

```text
Transient failure     → retry
Invalid input         → correct or ask user
Permission failure    → stop and escalate
Not found             → clarification path
Business rejection    → explain outcome
Unknown failure       → safe fallback
```

---

## 6.5 Hard-to-debug behavior

A final answer alone is not enough for debugging.

You need to know:

* Which nodes ran?
* Which route was selected?
* What state fields changed?
* Which model and prompt version were used?
* Which tools were called?
* What arguments were sent?
* How many retries occurred?
* Where was time spent?
* Where were tokens spent?

LangGraph’s checkpoint history and streaming events expose step-level information, while LangSmith can be used for tracing, evaluation and observability. ([Docs by LangChain][6])

---

## 6.6 Poor recovery logic

A dangerous assumption is:

> “When anything fails, restart the whole graph.”

Imagine:

```text
Refund completed successfully
        ↓
Response generation failed
        ↓
Restart entire graph
        ↓
Refund called again
```

The workflow must distinguish:

* retrying computation,
* replaying an LLM call,
* repeating a database read,
* repeating an external side effect.

Use:

* idempotency keys,
* tool transaction IDs,
* execution status,
* verification nodes,
* compensating operations.

---

## 6.7 Replay is not business rollback

LangGraph can replay or fork execution from older checkpoints.

But replaying graph state does not automatically undo an external action.

If a previous step issued a refund, replay does not remove the refund. In fact, nodes after the selected checkpoint may execute again, including LLM calls, APIs and interrupts. ([Docs by LangChain][11])

Therefore:

```text
Workflow rollback ≠ Business transaction rollback
```

For business rollback you may need a compensating action:

```text
refund()       → forward action
reverse_refund() → compensating action
```

Some actions cannot be fully reversed, such as sending a message to a guest. Prevention and approval are often more important than rollback.

---

## 6.8 Cost blowups

Every loop may add:

* another LLM call,
* another retrieval,
* another reranker call,
* another tool invocation,
* another checkpoint,
* another trace.

Measure cost by:

```text
Cost per case
Cost per successful resolution
Cost per node
Tokens per node
Tool cost per case
Retry cost
Human-review cost
```

Use smaller models for:

* classification,
* routing,
* simple extraction,
* validation.

Reserve larger models for genuinely difficult reasoning.

---

## 6.9 Latency accumulation

A workflow with eight sequential steps may feel slow even if each step is reasonably fast.

```text
Classification       1 second
Retrieval            1 second
Reranking            1 second
Policy reasoning     2 seconds
Tool call            2 seconds
Validation           1 second
Response generation  2 seconds
--------------------------------
Total                10 seconds
```

Optimization options:

* run independent operations in parallel,
* cache safe results,
* remove unnecessary LLM calls,
* combine very small deterministic steps,
* use faster models for routing,
* stream progress,
* set deadlines.

Do not combine everything into one giant node merely to reduce node count. Node boundaries are valuable for recovery and observability.

---

## 6.10 Multi-step observability problems

A single success-rate metric is insufficient.

Track:

### Workflow metrics

* completion rate,
* escalation rate,
* abandonment rate,
* loop count,
* average node count,
* recovery rate.

### Node metrics

* latency,
* error rate,
* retry rate,
* token count,
* cost.

### Routing metrics

* route distribution,
* incorrect-route rate,
* fallback frequency.

### Tool metrics

* availability,
* timeout rate,
* duplicate prevention,
* rejected actions.

### Human-review metrics

* queue time,
* approval rate,
* edit rate,
* reviewer disagreement.

---

## 6.11 Human-review bottlenecks

A workflow may technically be safe but operationally unusable if every case waits for approval.

Use risk-based review:

```text
Low risk + high confidence
        → automatic

Medium risk
        → additional automated validation

High risk or low confidence
        → human review
```

Measure:

```text
Human-review rate
Average review time
Cases awaiting review
Reviewer overturn rate
```

A high overturn rate can show that the automated decision logic needs improvement.

---

## 6.12 Reliability during graph changes

Long-running threads may resume after your code has changed.

Current LangGraph documentation notes that the latest graph is applied to both new threads and threads resuming from checkpoints. This means graph and state changes must remain compatible with in-flight executions. ([Docs by LangChain][12])

Production strategies include:

* version state schemas,
* keep renamed fields temporarily,
* add migration nodes,
* record graph version in state,
* test old checkpoints against new code,
* deploy backward-compatible graph changes,
* drain or migrate incompatible workflows.

---

# 7. Optimization strategies

## 7.1 Build a strong state schema

Organize state into clear categories:

```python
class WorkflowState:
    # Identity
    request_id
    user_id

    # Input
    question

    # Evidence
    retrieved_documents
    tool_data

    # Decisions
    intent
    eligibility
    risk_level

    # Control
    status
    step_count
    retry_count
    deadline

    # Side effects
    proposed_action
    execution_id
    execution_status

    # Output
    final_answer

    # Diagnostics
    errors
    audit_events
```

Maintain invariants such as:

```text
If execution_status == "completed",
execution_id must not be empty.
```

---

## 7.2 Keep nodes small and clear

A good node:

* has one responsibility,
* has explicit input fields,
* produces explicit output fields,
* can be tested independently,
* has an appropriate timeout,
* has an appropriate retry policy.

Example:

```text
calculate_refund_eligibility
```

Better than:

```text
call_llm_and_maybe_do_refund_and_generate_answer
```

---

## 7.3 Validate at boundaries

Validate:

### Before the LLM

* input length,
* required identifiers,
* supported language,
* prompt-injection risk.

### After the LLM

* schema,
* allowed enum values,
* required fields,
* confidence,
* prohibited content.

### Before a tool

* tool allow-list,
* argument types,
* permissions,
* business rules,
* approval status,
* idempotency key.

### After a tool

* response schema,
* transaction status,
* expected amount,
* expected resource identity.

---

## 7.4 Use explicit routing rules

Avoid vague routing prompts:

```text
“Decide what to do next.”
```

Prefer constrained outputs:

```python
Literal[
    "retrieve_policy",
    "ask_clarification",
    "request_approval",
    "finish"
]
```

Then validate the selected route.

For critical conditions, use code:

```python
if amount > 200:
    return "request_approval"
```

---

## 7.5 Bound every loop

Every loop should have:

```text
Purpose
Entry condition
Success condition
Failure condition
Maximum iterations
Fallback route
```

Example:

```python
if state["retrieval_attempts"] >= 2:
    return "manual_review"
```

---

## 7.6 Use targeted human review

Trigger review based on:

* risk,
* confidence,
* amount,
* compliance category,
* unusual tool arguments,
* repeated failures.

Do not use human review as a substitute for weak validation.

---

## 7.7 Improve telemetry

Record a structured event for every node:

```python
{
    "request_id": "case-1007",
    "thread_id": "thread-1007",
    "graph_version": "guest-recovery-v3",
    "node": "calculate_eligibility",
    "started_at": "...",
    "duration_ms": 382,
    "status": "success",
    "route_selected": "request_approval",
    "model": None,
    "input_tokens": 0,
    "output_tokens": 0,
    "estimated_cost": 0,
    "retry_attempt": 1
}
```

Do not log secrets or unnecessary personal data.

---

## 7.8 Improve testing

### Unit-test each node

```python
def test_high_amount_is_high_risk():
    state = {
        "proposed_action": {"amount": 500}
    }

    result = classify_risk(state)

    assert result["risk_level"] == "high"
```

### Test routing functions

```python
def test_high_risk_goes_to_approval():
    state = {
        "eligibility": True,
        "risk_level": "high"
    }

    assert route_by_risk(state) == "request_approval"
```

### Test workflow scenarios

* eligible request,
* ineligible request,
* missing reservation,
* policy unavailable,
* tool timeout,
* approval rejected,
* process crash after tool success,
* duplicate resume,
* maximum retries reached.

### Test state compatibility

Load an old checkpoint and verify that the new graph can resume safely.

LangGraph’s testing guidance recommends constructing fresh graphs and checkpointers for tests and supports testing individual nodes from the compiled graph. ([Docs by LangChain][13])

---

## 7.9 Design better fallback behavior

Fallbacks should be useful and safe.

Poor fallback:

```text
“An error occurred.”
```

Better fallback:

```text
“I could not confirm the reservation because the booking service is temporarily unavailable. Your case has been saved and routed to support. No refund action was performed.”
```

Useful fallback routes include:

* retry later,
* use cached read-only information,
* ask the user for missing information,
* use a smaller deterministic process,
* escalate to a human,
* stop without performing the action.

---

## 7.10 Control cost and latency

Add explicit budgets:

```python
class WorkflowBudget:
    max_steps = 12
    max_llm_calls = 6
    max_tool_calls = 5
    max_retrieval_calls = 2
    max_duration_seconds = 30
    max_estimated_cost = 0.25
```

Other strategies:

* parallelize independent retrievals,
* cache repeated safe computations,
* trim old conversation context,
* summarize long histories,
* retrieve only relevant state,
* use model tiering,
* skip response-generation LLM calls when a template is sufficient.

LangGraph supports node-level caching policies for avoiding repeated expensive operations. ([Docs by LangChain][5])

---

# 8. Easy real-world example

## Lost-item assistant

A guest says:

> “I lost a blue backpack near an attraction.”

### State

```python
{
    "description": "blue backpack",
    "location": "near attraction",
    "date": None,
    "matches": [],
    "attempts": 0,
    "status": "received"
}
```

### Workflow

```text
Receive request
      ↓
Check required details
      ↓
Is date missing?
  ├── Yes → ask guest for date
  └── No
        ↓
Search lost-item system
        ↓
Any strong matches?
  ├── Yes → show safe next steps
  ├── Weak matches → ask one more question
  └── No → create support case
```

### Loop

```text
Ask question
     ↓
Update state
     ↓
Validate details
     ↓
Still missing information?
     ├── Yes → ask again, within a limit
     └── No → search
```

### Production controls

* Maximum clarification attempts: two.
* Never expose another guest’s personal information.
* Do not claim the item is found until the inventory tool confirms it.
* Require identity verification before handing over an item.
* Create a human case if confidence is low.
* Save the workflow while waiting for the guest’s response.

This example demonstrates why LangGraph is useful:

* there is shared state,
* there are conditional paths,
* there may be a loop,
* a tool is called,
* the workflow may pause,
* a human may become involved.

---

# 9. Staff-level interview angle

## 9.1 A strong 60-second explanation

> “LangGraph is a low-level orchestration framework for building stateful AI workflows and agents. I use it when an application needs more than a linear prompt chain—for example, branching, loops, tool calls, human approval, persistence and recovery. The central abstraction is shared state. Nodes perform individual operations, and edges determine the next operation based on that state. In production, I normally prefer a deterministic outer graph with constrained agentic behavior inside selected nodes. I also design explicit stopping conditions, bounded retries, idempotent tool execution, database-backed checkpointing and node-level observability. The main trade-off is additional orchestration complexity in exchange for greater control, recoverability and auditability.”

---

## 9.2 How to decide whether orchestration needs LangGraph

Ask these questions:

### Question 1: Is the workflow linear?

```text
Yes → simple chain may be enough.
No  → graph may help.
```

### Question 2: Are there loops or conditional branches?

```text
Yes → LangGraph is a strong candidate.
```

### Question 3: Does execution pause for humans or external events?

```text
Yes → persistence and interrupts are valuable.
```

### Question 4: Are production tools performing side effects?

```text
Yes → explicit validation, checkpoints and recovery matter.
```

### Question 5: Must the workflow survive restarts?

```text
Yes → durable execution is important.
```

### Question 6: Do we need step-level debugging and auditability?

```text
Yes → explicit nodes and state transitions help.
```

A practical rule:

> Use LangGraph when orchestration itself has become a core part of the product’s correctness.

---

## 9.3 How LangGraph fits a Disney-like production system

A hypothetical architecture could be:

```text
Web/mobile/client
       ↓
API gateway
       ↓
Authentication and authorization
       ↓
LangGraph orchestration service
       │
       ├── LLM gateway
       ├── Retrieval service
       ├── Policy engine
       ├── Reservation tools
       ├── Case-management tools
       ├── Approval service
       └── Notification service
       ↓
Persistent checkpointer
       ↓
Observability, evaluation and audit platform
```

LangGraph should not own every system responsibility.

### LangGraph should own

* workflow state transitions,
* routing,
* pause and resume,
* orchestration,
* step-level recovery.

### Other services should own

* identity and authentication,
* business data,
* policy source of truth,
* transaction processing,
* authorization,
* secrets,
* enterprise audit storage.

---

## 9.4 Controlled autonomy

At Staff level, do not say:

> “We will build an autonomous agent that handles everything.”

Say:

> “We will assign autonomy according to risk.”

Example:

| Decision                       | Control                        |
| ------------------------------ | ------------------------------ |
| Understand guest intent        | LLM                            |
| Choose a read-only search tool | Constrained agent              |
| Validate tool arguments        | Code                           |
| Calculate eligibility          | Policy engine                  |
| Decide approval threshold      | Deterministic rule             |
| Approve exceptional action     | Human                          |
| Execute transaction            | Authorized service             |
| Verify transaction             | Deterministic node             |
| Explain outcome                | LLM grounded in verified state |

This architecture uses the LLM where language flexibility is useful and deterministic systems where correctness is mandatory.

---

## 9.5 Durable execution trade-offs

More durability generally provides:

* stronger recovery,
* less duplicated work,
* safer long-running execution.

But it may also introduce:

* storage costs,
* serialization overhead,
* checkpoint latency,
* retention requirements,
* privacy concerns,
* state-migration complexity.

A Staff Engineer should discuss:

* which nodes require strong persistence,
* what data may be stored,
* how long checkpoints are retained,
* how checkpoint data is encrypted,
* how old state schemas are migrated,
* which side effects need idempotency,
* whether replay is safe.

---

## 9.6 Reliability trade-offs

LangGraph can help coordinate reliability, but it cannot automatically make external tools reliable.

You must still design:

* timeouts,
* circuit breakers,
* retries,
* idempotency,
* transaction identifiers,
* compensating actions,
* schema validation,
* access control,
* operational alerts.

A good interview statement is:

> “Checkpointing protects workflow progress, while idempotency and transaction design protect external side effects.”

---

## 9.7 Deterministic graph versus free-form agent

Choose a deterministic graph when:

* the business process is known,
* errors are expensive,
* auditability is required,
* there are strict approval rules,
* the allowed paths are limited.

Choose an agentic loop when:

* exploration is needed,
* the appropriate next tool depends on unstructured information,
* there are many possible read-only paths,
* the cost of a wrong intermediate choice is low.

Choose a hybrid when:

* natural-language flexibility is needed,
* but final actions must remain controlled.

For most enterprise systems, the hybrid approach is the strongest default.

---

# 10. Revision checklist

You should be able to answer these without looking at the notes.

## Foundations

* [ ] What problem does LangGraph solve?
* [ ] Why is an LLM call not a workflow engine?
* [ ] Why might a simple chain become insufficient?
* [ ] What is the practical difference between LangChain and LangGraph?
* [ ] What is the difference between deterministic and agentic routing?
* [ ] When would LangGraph be unnecessary?

## Building blocks

* [ ] What is graph state?
* [ ] What makes a good state schema?
* [ ] What does a node do?
* [ ] What does an edge do?
* [ ] What is conditional routing?
* [ ] What is a reducer?
* [ ] How should tool calls be validated?
* [ ] What is a thread ID?
* [ ] What is a checkpoint?
* [ ] What does durable execution mean?
* [ ] Why must side effects be idempotent?
* [ ] What is an interrupt?
* [ ] How does streaming differ from checkpointing?

## Workflow design

* [ ] Can I divide a business workflow into small nodes?
* [ ] Can I identify fixed and conditional edges?
* [ ] Can I define stopping conditions for every loop?
* [ ] Can I specify retryable and non-retryable errors?
* [ ] Can I identify where human approval adds value?
* [ ] Can I define a safe fallback for every external dependency?

## Production

* [ ] Is the graph protected from infinite loops?
* [ ] Are tool retries bounded?
* [ ] Are transaction calls idempotent?
* [ ] Are node latency, cost and errors observable?
* [ ] Can old checkpoints resume after a deployment?
* [ ] Are sensitive state fields protected?
* [ ] Is checkpoint retention controlled?
* [ ] Have we distinguished graph replay from business rollback?
* [ ] Can the workflow safely recover after a tool succeeds but a later node fails?

## Staff-level answer

* [ ] Can I explain LangGraph in 60 seconds?
* [ ] Can I justify why a simple chain is insufficient?
* [ ] Can I describe a deterministic outer graph with constrained agentic nodes?
* [ ] Can I explain durability versus performance trade-offs?
* [ ] Can I explain workflow recovery versus side-effect recovery?
* [ ] Can I show where LangGraph belongs in a larger enterprise architecture?

---

# Final mental model

```text
LangGraph does not replace the LLM.
It controls how the LLM participates in a larger process.

State remembers the case.
Nodes perform work.
Edges choose the path.
Tools interact with systems.
Checkpoints preserve progress.
Interrupts add human control.
Retries handle temporary failures.
Guardrails limit autonomy.
Observability explains what happened.
```

> **For a Staff AI Engineer, LangGraph is not mainly about creating “more autonomous agents.” It is about creating AI workflows whose autonomy is explicit, bounded, recoverable and safe.**

[1]: https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com "LangGraph overview - Docs by LangChain"
[2]: https://docs.langchain.com/oss/python/langgraph/graph-api?utm_source=chatgpt.com "Graph API overview - Docs by LangChain"
[3]: https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph?utm_source=chatgpt.com "Thinking in LangGraph - Docs by LangChain"
[4]: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE?utm_source=chatgpt.com "INVALID_CONCURRENT_GRA..."
[5]: https://docs.langchain.com/oss/python/langgraph/use-graph-api?utm_source=chatgpt.com "Use the graph API - Docs by LangChain"
[6]: https://docs.langchain.com/oss/python/langgraph/checkpointers "Checkpointers - Docs by LangChain"
[7]: https://docs.langchain.com/oss/python/langgraph/add-memory?utm_source=chatgpt.com "Memory - Docs by LangChain"
[8]: https://docs.langchain.com/oss/python/langgraph/interrupts?utm_source=chatgpt.com "Interrupts - Docs by LangChain"
[9]: https://docs.langchain.com/oss/python/langgraph/streaming?utm_source=chatgpt.com "Streaming - Docs by LangChain"
[10]: https://docs.langchain.com/oss/python/langgraph/use-subgraphs?utm_source=chatgpt.com "Subgraphs - Docs by LangChain"
[11]: https://docs.langchain.com/oss/python/langgraph/use-time-travel?utm_source=chatgpt.com "Use time-travel - Docs by LangChain"
[12]: https://docs.langchain.com/oss/python/langgraph/backward-compatibility?utm_source=chatgpt.com "Backward compatibility - Docs by LangChain"
[13]: https://docs.langchain.com/oss/python/langgraph/test?utm_source=chatgpt.com "Test - Docs by LangChain"
