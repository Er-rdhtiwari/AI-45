# Day 223 — Linked List Insert and Delete Operations

Yesterday you learned how to **traverse** a linked list:

```text
head
 ↓
10 → 20 → 30 → None
```

Today you’ll learn how to **modify the links safely**.

That is the main idea:

> In a linked list, insertion and deletion are mostly about changing `next` references in the correct order.

---

# 1. Quick Recap

Our node class:

```python
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

Example:

```python
node1 = ListNode(10)
node2 = ListNode(20)
node3 = ListNode(30)

node1.next = node2
node2.next = node3

head = node1
```

Structure:

```text
head
 ↓
10 → 20 → 30 → None
```

Remember:

```python
current.val
```

means the data.

And:

```python
current.next
```

means the reference to the next node.

---

# 2. Why Reference Update Order Matters

Suppose:

```text
10 → 20 → 30 → None
```

You want to insert `15` between `10` and `20`.

Desired:

```text
10 → 15 → 20 → 30 → None
```

There are two links we need:

```text
10 → 15
15 → 20
```

But if we overwrite the original `10 → 20` link too early without saving it, we may lose access to the rest of the list.

That's why linked-list modification often follows this rule:

> **First connect the new node to what comes next. Then change the previous node to point to the new node.**

---

# 3. Insert at Beginning

Suppose:

```text
head
 ↓
10 → 20 → 30 → None
```

You want to insert:

```text
5
```

at the beginning.

Desired result:

```text
head
 ↓
5 → 10 → 20 → 30 → None
```

## Step 1: Create the new node

```python
new_node = ListNode(5)
```

Initially:

```text
5 → None

head
 ↓
10 → 20 → 30 → None
```

## Step 2: Point new node to old head

```python
new_node.next = head
```

Now:

```text
5 ─────┐
       ↓
      10 → 20 → 30 → None

head → 10
```

## Step 3: Move head

```python
head = new_node
```

Final:

```text
head
 ↓
5 → 10 → 20 → 30 → None
```

Python:

```python
def insert_at_beginning(head, value):
    new_node = ListNode(value)

    new_node.next = head
    head = new_node

    return head
```

You can simplify:

```python
def insert_at_beginning(head, value):
    new_node = ListNode(value)
    new_node.next = head
    return new_node
```

---

# 4. Why This Works for an Empty List

Suppose:

```python
head = None
```

Create:

```python
new_node = ListNode(10)
```

Then:

```python
new_node.next = head
```

means:

```python
new_node.next = None
```

So:

```text
10 → None
```

Return `new_node` as the new head.

Result:

```text
head
 ↓
10 → None
```

So the same logic handles:

```text
empty list
one-node list
many-node list
```

---

# 5. Insert After a Node

Suppose:

```text
head
 ↓
10 → 20 → 30 → None
```

You have a reference to the node containing `20`.

You want to insert:

```text
25
```

after it.

Desired:

```text
10 → 20 → 25 → 30 → None
```

Let's call the node containing `20`:

```python
current
```

Before:

```text
current
  ↓
 20 → 30 → None
```

Create:

```python
new_node = ListNode(25)
```

Now the safe update order matters.

---

# 6. Correct Insert-After Order

First:

```python
new_node.next = current.next
```

What does that do?

Before:

```text
current
  ↓
 20 → 30 → None

25 → None
```

After:

```text
current
  ↓
 20 → 30 → None
       ↑
25 ────┘
```

So `25` now points to `30`.

Then:

```python
current.next = new_node
```

Final:

```text
10 → 20 → 25 → 30 → None
```

Python:

```python
def insert_after(node, value):
    if node is None:
        return

    new_node = ListNode(value)

    new_node.next = node.next
    node.next = new_node
```

---

# 7. What Goes Wrong If You Overwrite Too Early?

Suppose:

```text
20 → 30 → None
```

You write this first:

```python
current.next = new_node
```

Now:

```text
20 → 25 → None
```

What happened to `30`?

You overwrote the only reference from `20` to `30`.

If you didn't save it somewhere else, you may no longer know how to reconnect the remainder.

You wanted:

```text
20 → 25 → 30
```

but accidentally got:

```text
20 → 25 → None

30 → None
```

So a safer pattern is:

```python
new_node.next = current.next
current.next = new_node
```

Think:

```text
1. Preserve the old next node
2. Then redirect the previous link
```

---

# 8. Insert After the Tail

Suppose:

```text
10 → 20 → 30 → None
          ↑
         node
```

Insert `40` after `30`.

Run:

```python
new_node.next = node.next
```

Since:

```python
node.next is None
```

you get:

```text
40 → None
```

Then:

```python
node.next = new_node
```

Result:

```text
10 → 20 → 30 → 40 → None
```

The same code works.

---

# 9. Delete the Head

Suppose:

```text
head
 ↓
10 → 20 → 30 → None
```

You want to delete `10`.

The new head should be:

```text
20
```

So simply:

```python
head = head.next
```

Before:

```text
head
 ↓
10 → 20 → 30 → None
```

After:

```text
      head
       ↓
10    20 → 30 → None
```

The list is now:

```text
20 → 30 → None
```

Python:

```python
def delete_head(head):
    if head is None:
        return None

    head = head.next
    return head
```

Or shorter:

```python
def delete_head(head):
    if head is None:
        return None

    return head.next
```

---

# 10. Delete Head from One-Node List

Suppose:

```text
head
 ↓
10 → None
```

Then:

```python
head = head.next
```

Since:

```python
head.next is None
```

the result becomes:

```python
head = None
```

So:

```text
empty list
```

Correct.

---

# 11. Delete by Value

Now suppose:

```text
head
 ↓
10 → 20 → 30 → 40 → None
```

You want to delete:

```text
30
```

We need to change:

```text
20 → 30 → 40
```

into:

```text
20 ─────→ 40
```

The key idea:

> To delete a node, we usually need access to the node before it.

Why?

Because we need to update that previous node's `next`.

---

# 12. Delete by Value — Traversal Setup

We can use:

```python
current = head
```

But rather than stopping on the node to delete, it is often convenient to stop on the node **before** it.

Suppose target is:

```python
target = 30
```

We want:

```text
current
  ↓
 20 → 30 → 40
```

So that:

```python
current.next
```

is the node containing `30`.

Then we can skip it.

---

# 13. The Core Delete Operation

Suppose:

```text
current
  ↓
 20 → 30 → 40
```

Then:

```python
current.next = current.next.next
```

Let's unpack it.

Before:

```text
current.next
     ↓
     30
```

And:

```text
current.next.next
          ↓
          40
```

So:

```python
current.next = current.next.next
```

means:

```text
20 should now point directly to 40
```

Result:

```text
20 → 40
```

and `30` is skipped.

---

# 14. Before-and-After Diagram

Before:

```text
head
 ↓
10 → 20 → 30 → 40 → None
     ↑     ↑
 current target
```

Delete `30`:

```python
current.next = current.next.next
```

After:

```text
head
 ↓
10 → 20 ─────→ 40 → None
```

The node `30` is no longer part of the list.

---

# 15. Full Delete-by-Value Logic

There are three major cases.

## Case 1: Empty list

```text
head = None
```

Nothing to delete.

Return:

```python
None
```

## Case 2: Head contains target

Example:

```text
10 → 20 → 30
```

Delete `10`.

Use:

```python
return head.next
```

## Case 3: Target is later

Traverse until:

```python
current.next
```

is the target node.

Then skip it.

Skeleton:

```python
def delete_value(head, target):

    if head is None:
        return None

    if head.val == target:
        return head.next

    current = head

    while current.next:
        if current.next.val == target:
            current.next = current.next.next
            return head

        current = current.next

    return head
```

We'll use this logic in the guided exercise.

---

# 16. Why `while current.next` Can Be Useful

Suppose:

```text
10 → 20 → 30 → None
```

If we want to inspect:

```python
current.next.val
```

we must first know:

```python
current.next is not None
```

So:

```python
while current.next:
```

keeps us safe.

Inside the loop:

```python
current.next.val
```

is valid.

---

# 17. Deleting the Tail

Suppose:

```text
10 → 20 → 30 → None
```

Delete:

```text
30
```

Eventually:

```text
current
  ↓
 20 → 30 → None
```

Then:

```python
current.next = current.next.next
```

Since:

```python
current.next.next
```

is:

```text
None
```

we get:

```text
20 → None
```

Final:

```text
10 → 20 → None
```

Same logic works.

---

# 18. Complexity of Insert at Beginning

Operation:

```python
new_node.next = head
head = new_node
```

No traversal.

So:

```text
Time: O(1)
Space: O(1)
```

Ignoring the memory needed for the new node itself, auxiliary space is O(1).

---

# 19. Complexity of Insert After a Known Node

If we already have the node reference:

```python
node
```

then:

```python
new_node.next = node.next
node.next = new_node
```

is:

```text
Time: O(1)
Space: O(1)
```

Important distinction:

> Finding the node may take O(n), but inserting after an already-known node is O(1).

---

# 20. Complexity of Delete Head

```python
head = head.next
```

So:

```text
Time: O(1)
Space: O(1)
```

---

# 21. Complexity of Delete by Value

If target might be near the end, you may need to inspect all nodes.

So:

```text
Time: O(n)
Space: O(1)
```

---

# 22. Guided Insertion Exercise

## Insert After a Given Value

Given:

```text
10 → 20 → 30 → None
```

and:

```python
target = 20
value = 25
```

Insert `25` after the first occurrence of `20`.

Expected:

```text
10 → 20 → 25 → 30 → None
```

If the target doesn't exist, leave the list unchanged.

### Step 1 — Traverse

Start:

```python
current = head
```

### Step 2 — Find the target

At each node:

```python
if current.val == target:
```

you've found the node after which insertion should happen.

### Step 3 — Create node

```python
new_node = ListNode(value)
```

### Step 4 — Carefully update links

Ask yourself:

Which must happen first?

```python
new_node.next = ?
```

and then:

```python
current.next = ?
```

### Starter code

```python
def insert_after_value(head, target, value):

    current = head

    while current:

        if current.val == target:

            new_node = ListNode(value)

            # Connect new node safely

            return head

        current = current.next

    return head
```

For your solution, provide:

1. Pseudocode
2. Python
3. Time complexity
4. Space complexity
5. What happens for an empty list
6. What happens if target is the tail

---

# 23. Guided Deletion Exercise

## Delete First Occurrence of a Value

Given:

```text
10 → 20 → 30 → 40 → None
```

and:

```python
target = 30
```

Expected:

```text
10 → 20 → 40 → None
```

But also test:

```python
target = 10
```

because deleting the head requires special handling.

Starter:

```python
def delete_value(head, target):

    if head is None:
        return None

    # Special case:
    # target is at head

    current = head

    while current.next:

        # Check whether next node
        # contains target

        # If yes, skip that node

        current = current.next

    return head
```

For your solution, explain:

```text
Why do we check head separately?

Why do we inspect current.next?

Why do we return head after deletion?
```

And include time/space complexity.

---

# 24. Independent Problem

## Insert and Then Delete

Start with:

```text
5 → 10 → 15 → 20 → None
```

Perform these operations:

```text
1. Insert 12 after 10
2. Delete the first node containing 15
3. Insert 2 at the beginning
4. Delete the first node containing 5
```

Write a function or set of functions that performs these operations safely.

Do not convert the linked list into a Python list.

Your answer must include:

1. Before-and-after ASCII diagram for each operation
2. Pseudocode
3. Python
4. Final linked-list structure
5. Time complexity of each operation
6. Overall time complexity
7. Space complexity
8. What would happen if any delete target did not exist

I won't show the solution initially.

---

# 25. Empty-List Cases

## Insert at beginning

Empty:

```text
None
```

Insert `10`:

```text
10 → None
```

Works naturally.

## Insert after a node

If:

```python
node = None
```

there is no node after which to insert.

You must decide whether to:

```text
do nothing
return
```

or raise an error depending on the problem requirements.

For beginner interview questions, returning without modifying is often fine.

## Delete head

If:

```python
head = None
```

there is nothing to delete.

Return:

```python
None
```

## Delete by value

If list is empty:

```text
Nothing to search.
```

Return:

```python
None
```

---

# 26. Single-Node Cases

Suppose:

```text
10 → None
```

## Insert at beginning

Insert `5`:

```text
5 → 10 → None
```

## Insert after `10`

Insert `20`:

```text
10 → 20 → None
```

## Delete head

Delete `10`:

```text
None
```

## Delete by value

Target:

```python
10
```

Since the head is the target:

```python
return head.next
```

which is:

```python
None
```

## Delete nonexistent target

Target:

```python
99
```

List remains:

```text
10 → None
```

---

# 27. Common Reference Mistake — Wrong Insertion Order

You want:

```text
10 → 15 → 20
```

Wrong:

```python
current.next = new_node
new_node.next = current.next
```

Let's trace it.

After:

```python
current.next = new_node
```

we have:

```text
10 → 15
```

Now:

```python
new_node.next = current.next
```

But `current.next` already points to `new_node`.

So:

```text
15 → 15
```

You accidentally create a self-loop.

Possible result:

```text
10 → 15
      ↑ ↓
      └─┘
```

You also lost the old node `20`.

Correct:

```python
new_node.next = current.next
current.next = new_node
```

---

# 28. Common Reference Mistake — Losing the Rest of the List

Suppose:

```text
10 → 20 → 30 → 40
```

You want to insert `25` after `20`.

If you overwrite:

```python
node20.next = new_node
```

before preserving where `20` used to point, the path to:

```text
30 → 40
```

may be lost.

Think:

> **Preserve before overwrite.**

That principle appears repeatedly in linked-list problems.

---

# 29. Common Reference Mistake — Moving the Wrong Pointer

Suppose:

```python
current = head
```

During traversal, you should normally do:

```python
current = current.next
```

Not:

```python
head = head.next
```

unless you intentionally want to change the head of the list.

Otherwise you may lose your original starting point.

---

# 30. Common Deletion Mistake — Deleting Current Without Previous

Suppose:

```text
10 → 20 → 30
          ↑
       current
```

You discover:

```python
current.val == 30
```

But to remove `current`, you need the previous node to point past it.

That's why many deletion approaches either:

```text
track previous + current
```

or:

```text
stop at the node before the target
```

For today's beginner version, we'll often use:

```python
current.next.val
```

so that `current` is the previous node.

---

# 31. Another Common Delete Pattern: `prev` + `current`

You may also see:

```python
prev = None
current = head
```

Then:

```text
prev      current
 ↓           ↓
10    →     20    → 30
```

When deleting `current`:

```python
prev.next = current.next
```

This is another correct approach.

For now, understand both ideas:

```text
Approach A:
stop at previous node

Approach B:
track prev and current
```

We'll use both more later.

---

# Day 223 Cheat Sheet

```text
LINKED-LIST MODIFICATION
========================

INSERT AT BEGINNING
-------------------

Before:

head
 ↓
10 → 20 → None

new = 5

1. new.next = head
2. head = new

After:

head
 ↓
5 → 10 → 20 → None

Time: O(1)


INSERT AFTER NODE
-----------------

Before:

20 → 30

Insert 25

1. new.next = node.next
2. node.next = new

After:

20 → 25 → 30

Time: O(1)
if node is already known


DELETE HEAD
-----------

head = head.next

Before:

10 → 20 → 30

After:

20 → 30

Time: O(1)


DELETE BY VALUE
---------------

Before:

10 → 20 → 30 → 40

Delete 30:

current.next =
    current.next.next

After:

10 → 20 → 40

Time: O(n)


MOST IMPORTANT RULE
-------------------

Preserve the old link
before overwriting it.


EMPTY LIST
----------

head = None


SINGLE NODE
-----------

10 → None


COMMON BUGS
-----------

overwriting next too early
creating self-loop
losing remaining list
changing head accidentally
accessing current.next when None
forgetting special head deletion
```

The key idea for Day 223 is: **linked-list operations are not difficult because of the values—they are difficult because reference-update order matters.** For insertion, mentally say **“new node points forward first, previous node points to new second.”**