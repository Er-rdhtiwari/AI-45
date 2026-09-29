# Day 222 — Singly Linked List Fundamentals

Today’s connection is:

> **Arrays store elements using indexes. Linked lists store elements inside nodes, and each node points to the next node.**

With an array:

```python
nums = [10, 20, 30]
```

you can directly access:

```python
nums[1]
```

With a linked list, there is no direct index jump. You usually start at the beginning and follow references node by node.

---

# 1. What Is a Linked List?

A singly linked list is a chain of **nodes**.

Each node normally stores two things:

```text
value
next
```

For example:

```text
10 → 20 → 30 → None
```

More explicitly:

```text
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ value = 10  │    │ value = 20  │    │ value = 30  │
│ next ───────────→│ next ───────────→│ next = None │
└─────────────┘    └─────────────┘    └─────────────┘
       ↑
      head
```

`head` tells us where the linked list begins.

---

# 2. Important Terms

## Node

A **node** is one element of the linked list.

Conceptually:

```text
Node
 ├── value
 └── next
```

Example:

```text
value = 20
next  = reference to the node containing 30
```

---

# 3. Value

The actual data stored inside the node.

For:

```text
10 → 20 → 30
```

the node values are:

```text
10
20
30
```

In Python we'll call it:

```python
node.val
```

---

# 4. `next`

`next` stores a reference to the next node.

Suppose:

```text
10 → 20
```

The node containing `10` does not physically contain `20`.

Instead, it stores something conceptually like:

```text
next = reference to node containing 20
```

The final node has:

```python
next = None
```

meaning:

> There is no next node.

---

# 5. `head`

`head` is the reference to the first node.

Example:

```text
head
 ↓
10 → 20 → 30 → None
```

Without the head, we normally don't know where to begin traversing the list.

For an empty linked list:

```python
head = None
```

Visualization:

```text
head
 ↓
None
```

---

# 6. Tail Concept

The **tail** is the last node.

Example:

```text
head                     tail
 ↓                         ↓
10 → 20 → 30 → 40 → None
```

The important property of the tail is:

```python
tail.next is None
```

Not every linked-list problem gives you a separate `tail` variable.

Sometimes you only receive:

```python
head
```

and must traverse until the end.

---

# 7. Beginner-Friendly `ListNode` Class

Let's create a node.

```python
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

What does this mean?

If we write:

```python
node = ListNode(10)
```

then conceptually:

```text
node
 ↓
┌──────────────┐
│ val  = 10    │
│ next = None  │
└──────────────┘
```

We can inspect:

```python
print(node.val)
```

Output:

```text
10
```

And:

```python
print(node.next)
```

Output:

```text
None
```

---

# 8. Connecting Nodes

Create three nodes:

```python
node1 = ListNode(10)
node2 = ListNode(20)
node3 = ListNode(30)
```

Initially:

```text
node1: 10 → None

node2: 20 → None

node3: 30 → None
```

Now connect them:

```python
node1.next = node2
node2.next = node3
```

We now have:

```text
10 → 20 → 30 → None
```

Set:

```python
head = node1
```

Now:

```text
head
 ↓
10 → 20 → 30 → None
```

---

# 9. Complete Construction Example

```python
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


node1 = ListNode(10)
node2 = ListNode(20)
node3 = ListNode(30)

node1.next = node2
node2.next = node3

head = node1
```

The important thing to understand is that:

```python
node1.next = node2
```

doesn't copy `node2`.

It stores a reference to that node.

---

# 10. Linked List Traversal

**Traversal** means:

> Visit the nodes one by one.

Suppose:

```text
head
 ↓
10 → 20 → 30 → None
```

We start with:

```python
current = head
```

Now:

```text
current
 ↓
10 → 20 → 30 → None
```

Process the current value:

```python
print(current.val)
```

Output:

```text
10
```

Then move:

```python
current = current.next
```

Now:

```text
     current
        ↓
10 → 20 → 30 → None
```

Print:

```text
20
```

Move again:

```python
current = current.next
```

Now:

```text
          current
             ↓
10 → 20 → 30 → None
```

Print:

```text
30
```

Move again:

```python
current = current.next
```

Now:

```text
current = None
```

Traversal stops.

---

# 11. Standard Traversal Pattern

This pattern is extremely important:

```python
current = head

while current is not None:
    print(current.val)
    current = current.next
```

Shorter version:

```python
current = head

while current:
    print(current.val)
    current = current.next
```

Both mean the same thing.

---

# 12. Step-by-Step Dry Run

Linked list:

```text
5 → 8 → 12 → None
```

Start:

```python
current = head
```

So:

```text
current → 5
```

### Iteration 1

```python
print(current.val)
```

prints:

```text
5
```

Then:

```python
current = current.next
```

Now:

```text
current → 8
```

### Iteration 2

Print:

```text
8
```

Move:

```text
current → 12
```

### Iteration 3

Print:

```text
12
```

Move:

```text
current → None
```

Now:

```python
while current:
```

becomes false.

Stop.

---

# 13. Arrays vs Linked Lists

Consider:

```text
Array:
[10, 20, 30, 40]
```

You can directly ask:

```python
nums[2]
```

and get:

```text
30
```

An array supports efficient random indexing.

Conceptually:

```text
index:
 0    1    2    3
 ↓    ↓    ↓    ↓
[10] [20] [30] [40]
```

A linked list is different:

```text
10 → 20 → 30 → 40 → None
```

If you want the third node, you normally have to do:

```text
head
 ↓
10 → 20 → 30
     step step
```

You cannot simply do:

```python
head[2]
```

with the normal `ListNode` structure.

---

# 14. Why Random Indexing Is Inefficient

Suppose you want node index `4`.

Linked list:

```text
index   0     1     2     3     4
        ↓     ↓     ↓     ↓     ↓
       10 → 20 → 30 → 40 → 50 → None
```

To reach `50`, you start at `10`.

Then:

```text
10
 ↓
20
 ↓
30
 ↓
40
 ↓
50
```

That takes multiple steps.

Worst case, to access some arbitrary position:

```text
Time = O(n)
```

For an array:

```python
nums[i]
```

is normally:

```text
O(1)
```

That's one of the biggest differences.

---

# 15. Basic Array vs Linked List Comparison

| Feature | Array | Singly Linked List |
|---|---|---|
| Direct indexing | O(1) | O(n) |
| Traverse all elements | O(n) | O(n) |
| Storage style | contiguous sequence abstraction | nodes connected by references |
| Find next element | index + 1 | `node.next` |
| Start | index 0 | `head` |
| End marker | length boundary | `None` |

Later you'll learn that linked lists can make some insertions and deletions very convenient when you already have the relevant node reference.

---

# 16. Empty Linked List

An empty list is:

```python
head = None
```

Suppose you traverse:

```python
current = head

while current:
    print(current.val)
    current = current.next
```

Since:

```python
current = None
```

the loop runs zero times.

That's good.

But this is dangerous:

```python
print(head.val)
```

when:

```python
head = None
```

because there is no node.

---

# 17. One-Node Linked List

Suppose:

```python
head = ListNode(10)
```

Visualization:

```text
head
 ↓
10 → None
```

Traversal:

```python
current = head
```

Iteration:

```text
print 10
current = current.next
```

Now:

```text
current = None
```

Stop.

So the standard traversal works perfectly for:

```text
empty list
one-node list
many-node list
```

That's a good sign that the traversal pattern is robust.

---

# 18. Complexity of Traversal

Suppose there are:

```text
n nodes
```

Traversal visits every node once.

Therefore:

```text
Time: O(n)
```

If you're only using one pointer:

```python
current
```

additional space is:

```text
O(1)
```

So:

```text
Traversal:
Time  = O(n)
Space = O(1)
```

---

# 19. Guided Problem — Sum All Node Values

Given:

```text
2 → 4 → 6 → 8 → None
```

Return:

```text
20
```

We are going to solve this using traversal.

### Step 1 — What do we need?

A running total:

```python
total = 0
```

and a traversal pointer:

```python
current = head
```

### Step 2 — What should happen at each node?

Suppose:

```text
current → 4
```

You need to:

```text
add current value to total
```

Then move:

```python
current = current.next
```

### Step 3 — When should we stop?

When:

```python
current is None
```

Complete this:

```python
def sum_linked_list(head):

    total = 0
    current = head

    while current:
        # add current value

        # move to next node

    return total
```

Before coding, pseudocode could look like:

```text
set total to 0
set current to head

while current exists:
    add current value to total
    move current to next node

return total
```

For:

```text
2 → 4 → 6 → 8 → None
```

the running total should evolve like:

```text
0
2
6
12
20
```

Your solution should include:

```text
Pseudocode
Python
Time complexity
Space complexity
```

---

# 20. Independent Problem — Find a Value

Given the linked list:

```text
10 → 25 → 30 → 42 → None
```

and:

```python
target = 30
```

return:

```python
True
```

because `30` exists.

For:

```python
target = 99
```

return:

```python
False
```

Your job is to write:

```python
def contains_value(head, target):
    ...
```

Do not convert the linked list to a Python list.

Traverse the linked list directly.

Your answer should include:

1. Your traversal reasoning.
2. Pseudocode.
3. Python code.
4. Time complexity.
5. Space complexity.
6. What happens for an empty linked list.
7. What happens for a one-node linked list.

I won't show the solution until you attempt it.

---

# 21. Common Reference Mistake — Losing the Head

Suppose:

```text
head
 ↓
10 → 20 → 30 → None
```

You write:

```python
head = head.next
```

Now:

```text
head
 ↓
20 → 30 → None
```

You've changed your original starting reference.

If nothing else points to `10`, you've effectively lost access to it through `head`.

That's why traversal normally uses:

```python
current = head
```

and moves:

```python
current = current.next
```

while leaving:

```python
head
```

unchanged.

---

# 22. Common Reference Mistake — Forgetting to Move

Wrong:

```python
current = head

while current:
    print(current.val)
```

What happens?

`current` never changes.

So if `current` starts at `10`:

```text
10
10
10
10
10
...
```

Infinite loop.

You need:

```python
current = current.next
```

---

# 23. Common Reference Mistake — Accessing `.next` on `None`

Wrong:

```python
current = current.next.next
```

without knowing whether:

```python
current.next
```

exists.

For example:

```text
30 → None
```

Then:

```python
current.next
```

is:

```text
None
```

and trying:

```python
None.next
```

fails.

You'll encounter this often when linked-list problems become more advanced.

---

# 24. Common Reference Mistake — Replacing a Link Accidentally

Suppose:

```text
10 → 20 → 30 → None
```

and `node1` points to `10`.

If you write:

```python
node1.next = None
```

you've changed the structure to:

```text
10 → None

20 → 30 → None
```

The connection from `10` to `20` is gone.

Reference changes modify the actual linked-list structure.

---

# 25. Common Reference Mistake — Confusing Node and Value

Suppose:

```python
current = head
```

Then:

```python
current
```

is a **node**.

But:

```python
current.val
```

is the value inside that node.

These are different.

For:

```text
10 → 20 → None
```

think:

```text
current     = node object
current.val = 10
current.next = reference to node containing 20
```

A common beginner mistake is writing something like:

```python
current = current.val
```

Now `current` becomes an integer instead of a node, and traversal breaks.

---

# 26. A Useful Traversal Template

For many beginner linked-list problems:

```python
current = head

while current:
    # process current.val

    current = current.next
```

Examples of "process" might be:

```text
print value
sum value
count nodes
search for target
find maximum
```

The traversal structure stays mostly the same.

---

# Day 222 — Recognition Cheat Sheet

```text
SINGLY LINKED LIST
==================

Node contains:

value
next


STRUCTURE
=========

head
 ↓
10 → 20 → 30 → None


HEAD
====

reference to first node


TAIL
====

last node

tail.next = None


TRAVERSAL
=========

current = head

while current:
    process current.val
    current = current.next


COMPLEXITY
==========

Traverse all nodes:
O(n)

Extra traversal space:
O(1)

Access arbitrary index:
O(n)


ARRAY
=====

nums[i]

direct access:
O(1)


LINKED LIST
===========

follow references:

head
 ↓
node → node → node

random access:
O(n)


EMPTY LIST
==========

head = None


ONE NODE
========

head
 ↓
10 → None


COMMON BUGS
===========

changing head accidentally
forgetting current = current.next
accessing .next on None
confusing node with node.val
breaking a next reference


KEY QUESTIONS
=============

What does head point to?

What does current point to?

What does current.val mean?

What does current.next mean?

When does traversal stop?
```

For Day 222 practice, start with the guided **Sum All Node Values** problem. Write the pseudocode first, then Python, then state **time and space complexity**.