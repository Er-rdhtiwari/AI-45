# Day 221 — Queue and Deque Fundamentals

Yesterday you learned a **stack**:

> **Stack = LIFO — Last In, First Out**

Today you learn a **queue**:

> **Queue = FIFO — First In, First Out**

Think of people standing in a line. The person who entered the line first should normally be served first.

---

# 1. Real-World Queue Analogy

Imagine a billing counter:

```text
FRONT                         REAR
  ↓                             ↓
[Alice] [Bob] [Charlie] [David]
  ↑
served first
```

Alice entered before everyone else, so Alice leaves first.

After Alice is served:

```text
FRONT                 REAR
  ↓                      ↓
[Bob] [Charlie] [David]
```

If Emma joins:

```text
FRONT                         REAR
  ↓                             ↓
[Bob] [Charlie] [David] [Emma]
```

This is **FIFO**:

```text
First In
   ↓
First Out
```

---

# 2. Stack vs Queue

Suppose we insert:

```text
10
20
30
```

With a stack:

```text
push 10
push 20
push 30

pop → 30
```

Because the most recently added item leaves first.

With a queue:

```text
enqueue 10
enqueue 20
enqueue 30

dequeue → 10
```

Because the oldest item leaves first.

| Structure | Rule | Insert | Remove |
|---|---|---|---|
| Stack | LIFO | top | top |
| Queue | FIFO | rear | front |
| Deque | both ends | front/rear | front/rear |

---

# 3. Important Queue Terms

The main terms today are:

```text
FIFO
enqueue
dequeue
front
rear
```

Suppose:

```text
FRONT           REAR
 ↓                ↓
[10, 20, 30, 40]
```

**Front** is the next item to leave:

```text
10
```

**Rear** is the most recently added item:

```text
40
```

---

# 4. Enqueue

**Enqueue** means:

> Add something to the rear of the queue.

Starting:

```text
[]
```

Enqueue `10`:

```text
[10]
 F/R
```

Enqueue `20`:

```text
FRONT  REAR
 ↓      ↓
[10,   20]
```

Enqueue `30`:

```text
FRONT       REAR
 ↓            ↓
[10, 20, 30]
```

---

# 5. Dequeue

**Dequeue** means:

> Remove the element from the front.

Suppose:

```text
FRONT       REAR
 ↓            ↓
[10, 20, 30]
```

Dequeue:

```text
10 leaves
```

Queue becomes:

```text
FRONT  REAR
 ↓      ↓
[20,   30]
```

Next dequeue:

```text
20 leaves
```

Notice that removal happens from the opposite side from insertion.

---

# 6. Why Not Just Use a Python List?

You technically could write:

```python
queue = []

queue.append(10)
queue.append(20)
queue.append(30)

value = queue.pop(0)
```

This works logically.

But:

```python
queue.pop(0)
```

is normally inefficient.

Why?

Suppose:

```python
queue = [10, 20, 30, 40, 50]
```

Remove `10`:

```text
[10, 20, 30, 40, 50]
 ↓
remove
```

Now Python needs the remaining elements to occupy positions:

```text
[20, 30, 40, 50]
```

Conceptually, many elements need to shift left.

So:

```python
list.pop(0)
```

is:

```text
O(n)
```

That becomes expensive when the queue is large.

---

# 7. Use `collections.deque`

Python provides a much better structure:

```python
from collections import deque
```

Create a queue:

```python
from collections import deque

queue = deque()
```

Now we can efficiently add to one end and remove from the other.

---

# 8. Queue Using `deque`

Enqueue:

```python
queue.append(10)
queue.append(20)
queue.append(30)
```

Queue:

```text
deque([10, 20, 30])
```

Think:

```text
FRONT       REAR
 ↓            ↓
[10, 20, 30]
```

Dequeue:

```python
value = queue.popleft()
```

Returns:

```text
10
```

Queue becomes:

```text
[20, 30]
```

So the standard Python queue pattern is:

```python
from collections import deque

queue = deque()

queue.append(x)      # enqueue
queue.popleft()      # dequeue
```

---

# 9. Front and Rear

With:

```python
queue = deque([10, 20, 30])
```

Front:

```python
queue[0]
```

returns:

```text
10
```

Rear:

```python
queue[-1]
```

returns:

```text
30
```

Neither removes anything.

```text
FRONT       REAR
 ↓            ↓
[10, 20, 30]
```



---

# 10. Deque — Double-Ended Queue

The name **deque** means:

> **Double-ended queue**

Pronounced approximately:

```text
"deck"
```

A normal queue mainly does:

```text
add → rear
remove → front
```

But a deque allows operations at **both ends**.

```text
              DEQUE

FRONT                     REAR
  ↓                         ↓
[10] [20] [30] [40]

 ↑                     ↑
add/remove            add/remove
```

Python:

```python
from collections import deque

d = deque()
```

Add to right:

```python
d.append(10)
```

Add to left:

```python
d.appendleft(5)
```

Remove from right:

```python
d.pop()
```

Remove from left:

```python
d.popleft()
```

---

# 11. Important Deque Operations

```python
from collections import deque

d = deque()

d.append(10)
d.append(20)
d.appendleft(5)

print(d)
```

Now:

```text
deque([5, 10, 20])
```

Remove from left:

```python
d.popleft()
```

Returns:

```text
5
```

Remove from right:

```python
d.pop()
```

Returns:

```text
20
```

Remaining:

```text
deque([10])
```

The important operations are generally O(1):

| Operation | Meaning | Typical Complexity |
|---|---|---:|
| `append(x)` | add right | O(1) |
| `appendleft(x)` | add left | O(1) |
| `pop()` | remove right | O(1) |
| `popleft()` | remove left | O(1) |
| `d[0]` | inspect front | O(1) |
| `d[-1]` | inspect rear | O(1) |

---

# 12. Stack, Queue and Deque

Here's the mental model.

### Stack

```text
[10, 20, 30]
         ↑
      add/remove
```

Python:

```python
stack.append(x)
stack.pop()
```

Rule:

```text
LIFO
```

---

### Queue

```text
remove              add
   ↓                 ↓
[10, 20, 30, 40]
FRONT             REAR
```

Python:

```python
queue.append(x)
queue.popleft()
```

Rule:

```text
FIFO
```

---

### Deque

```text
add/remove        add/remove
    ↓                 ↓
[10, 20, 30, 40]
```

Python:

```python
d.append(x)
d.appendleft(x)

d.pop()
d.popleft()
```

A deque is flexible enough to behave as either a stack or queue.

---

# 13. One Complete Visual Example

Start:

```python
from collections import deque

queue = deque()
```

### Enqueue 10

```python
queue.append(10)
```

```text
FRONT/REAR
    ↓
   [10]
```

### Enqueue 20

```text
FRONT  REAR
 ↓      ↓
[10,   20]
```

### Enqueue 30

```text
FRONT       REAR
 ↓            ↓
[10, 20, 30]
```

### Dequeue

```python
queue.popleft()
```

`10` leaves.

```text
FRONT  REAR
 ↓      ↓
[20,   30]
```

### Enqueue 40

```text
FRONT       REAR
 ↓            ↓
[20, 30, 40]
```

### Dequeue

`20` leaves:

```text
FRONT  REAR
 ↓      ↓
[30,   40]
```

Notice the order:

```text
Entered:
10 → 20 → 30 → 40

Removed:
10 → 20 → ...
```

That's FIFO.

---

# 14. Empty Queue Edge Cases

Suppose:

```python
from collections import deque

queue = deque()
```

This is dangerous:

```python
queue.popleft()
```

because the queue is empty.

Python raises:

```text
IndexError
```

Similarly:

```python
queue[0]
```

also fails on an empty deque.

So when emptiness is possible:

```python
if queue:
    value = queue.popleft()
```

For front:

```python
if queue:
    front = queue[0]
```

A common queue condition is simply:

```python
while queue:
```

Meaning:

> Keep processing while the queue contains something.

---

# 15. Guided Problem — Process Customers in Arrival Order

Suppose customers arrive:

```python
customers = ["A", "B", "C", "D"]
```

You must serve them in exactly the same order they arrived.

Expected processing:

```text
Serve A
Serve B
Serve C
Serve D
```

We want to use a real queue rather than simply looping over the list, because the purpose is to practice queue operations.

### Step 1 — Create the queue

```python
from collections import deque

queue = deque()
```

### Step 2 — Enqueue every customer

Conceptually:

```text
enqueue A
enqueue B
enqueue C
enqueue D
```

Then:

```text
FRONT          REAR
 ↓               ↓
[A, B, C, D]
```

### Step 3 — Continue while queue isn't empty

You'll need:

```python
while queue:
```

### Step 4 — Remove the next customer

Ask yourself:

> Should you use `pop()` or `popleft()`?

Remember FIFO.

Complete this:

```python
from collections import deque

customers = ["A", "B", "C", "D"]

queue = deque()

for customer in customers:
    # enqueue customer
    pass


while queue:

    # remove next customer
    customer = __________

    print("Serving:", customer)
```

For your solution, include:

```text
Pseudocode
Python
Time complexity
Space complexity
```

### Complexity question

If there are `n` customers:

- How many customers are enqueued?
- How many are dequeued?

Use those facts to determine the final complexity.

---

# 16. Independent Problem 1 — Easy

## Ticket Counter Simulation

You receive:

```python
people = ["Amit", "Neha", "Raj", "Sara"]
```

People must receive tickets in their arrival order.

Your program should simulate:

```text
Amit gets ticket
Neha gets ticket
Raj gets ticket
Sara gets ticket
```

But there's one extra rule:

After serving `"Neha"`, a new person called `"John"` arrives and must join the **rear** of the queue.

Determine the final serving order.

Don't solve it by manually hardcoding the answer.

Your submission should contain:

1. Queue states as processing happens
2. Pseudocode
3. Python using `deque`
4. Time complexity
5. Space complexity
6. Explanation of what happens if the queue becomes empty

I won't show the solution initially.

---

# 17. Independent Problem 2 — Easy / Early Medium

## Recent Tasks

You receive commands:

```python
operations = [
    ("add", "Task A"),
    ("add", "Task B"),
    ("process", None),
    ("add", "Task C"),
    ("process", None),
    ("process", None),
    ("process", None)
]
```

Rules:

```text
("add", task)
```

means:

> Add the task to the rear of the queue.

And:

```text
("process", None)
```

means:

> Remove and process the task that has been waiting the longest.

The final `"process"` happens when the queue may already be empty.

You must decide how your program should handle that safely.

For your answer provide:

```text
queue state after each operation
pseudocode
Python
time complexity
space complexity
empty-queue handling
```

I won't give you the solution yet.

---

# 18. Common Queue Mistakes

A major mistake is using:

```python
queue.pop()
```

for normal FIFO processing.

Suppose:

```text
[10, 20, 30]
```

`pop()` gives:

```text
30
```

That's stack-like behavior.

For a normal queue, you usually want:

```python
queue.popleft()
```

which gives:

```text
10
```

Another mistake is using:

```python
list.pop(0)
```

repeatedly. It's logically correct, but inefficient because each removal from the beginning can cost O(n).

Also be careful with:

```python
queue[0]
queue[-1]
queue.popleft()
queue.pop()
```

when the deque is empty.

---

# 19. Queue Pattern You'll See Later

Queues become extremely important when you learn **BFS — Breadth-First Search**.

For example, suppose you have a tree:

```text
       A
      / \
     B   C
    / \
   D   E
```

If you want to process level by level:

```text
A
B C
D E
```

a queue naturally helps because earlier-discovered nodes should generally be processed before later-discovered ones.

You don't need BFS yet. Just remember:

```text
Queue
  ↓
FIFO
  ↓
process things in discovery/arrival order
```

---

# 20. Queue vs Stack Recognition

Consider:

```text
undo last operation
```

Which structure?

```text
Stack
```

Because we need the most recent operation.

Consider:

```text
serve customers in arrival order
```

Which structure?

```text
Queue
```

Because we need the oldest waiting customer.

Consider:

```text
add/remove at either end
```

Which structure?

```text
Deque
```

That is the distinction to build into your intuition.

---

# Day 221 — Recognition Signals

Think **stack** when you hear:

```text
most recent
last added
undo
matching/nesting
LIFO
```

Think **queue** when you hear:

```text
first come, first served
arrival order
waiting line
oldest pending item
process in discovery order
FIFO
```

Think **deque** when you hear:

```text
both ends matter
add/remove from front
add/remove from rear
maintain candidates at both ends
```

And remember the Python fundamentals:

```python
from collections import deque

q = deque()

# Queue
q.append(x)
q.popleft()

# Front / rear
q[0]
q[-1]

# Deque extras
q.appendleft(x)
q.pop()
```

Your most important Day 221 distinction is:

```text
STACK                       QUEUE

push → [10,20,30]           [10,20,30] ← enqueue
              ↑              ↑
             pop          dequeue

pop returns 30            dequeue returns 10

LIFO                      FIFO
```

For practice, begin with the **guided customer problem** and give me your pseudocode, Python code, and **time + space complexity**.