# Day 224 — DSA Revision: Sliding Window, Prefix Sum, Stack, Queue, Linked List

Today is a **revision day**. No major new topic.

The goal is to look at a problem and start recognizing:

> **What kind of behavior does this problem have, and which tool fits that behavior?**

You covered these topics from Days 218–223:

```text
Day 218 → Variable Sliding Window
Day 219 → Prefix Sum
Day 220 → Stack
Day 221 → Queue / Deque
Day 222 → Linked List Traversal
Day 223 → Linked List Insert / Delete
```

---

# 1. Day 218 Revision — Variable Sliding Window

Variable sliding window handles a **contiguous region whose size changes dynamically**.

Typical structure:

```python
left = 0

for right in range(len(nums)):

    # expand using nums[right]

    while window_is_invalid:
        # remove nums[left]
        left += 1

    # process valid window
```

The two pointers have different jobs:

```text
right → expands/explores

left  → shrinks/repairs
```

Example problem language:

```text
longest substring...
longest subarray...
at most k...
minimum length...
sum <= k...
```

For a longest valid window:

```text
expand
   ↓
invalid?
   ↓ yes
shrink
   ↓
valid
   ↓
update longest
```

For many suitable problems:

```text
Time: O(n)
```

because `left` and `right` mostly move forward only.

---

# 2. Day 219 Revision — Prefix Sum

Prefix sum is useful when you repeatedly need information about **ranges**.

Given:

```python
nums = [3, 1, 4, 2]
```

we can build:

```python
prefix = [0, 3, 4, 8, 10]
```

Our preferred definition is:

```text
prefix[i]
=
sum of the first i elements
```

So the inclusive sum:

```text
left ... right
```

is:

```python
prefix[right + 1] - prefix[left]
```

Example:

```text
nums = [3, 1, 4, 2]

sum from index 1 through 3
= 1 + 4 + 2
= 7
```

Using prefix:

```text
prefix[4] - prefix[1]

10 - 3

= 7
```

Complexity:

```text
Preprocessing: O(n)
Each range query: O(1)
Space: O(n)
```

Recognition:

```text
many range-sum queries
sum between L and R
sum before/after an index
precompute once, query many times
```

---

# 3. Day 220 Revision — Stack

Stack follows:

> **LIFO — Last In, First Out**

Python:

```python
stack = []

stack.append(x)   # push
stack.pop()       # pop
stack[-1]         # peek
```

Visual:

```text
[10, 20, 30]
         ↑
        TOP
```

`30` leaves first because it was added last.

Common uses:

```text
matching brackets
undo
nested structures
most recent unfinished item
remove adjacent previous item
```

Typical operation complexity:

```text
push: O(1) amortized
pop:  O(1)
peek: O(1)
```

Always consider:

```python
if stack:
```

before peeking/popping when an empty stack is possible.

---

# 4. Day 221 Revision — Queue and Deque

Queue follows:

> **FIFO — First In, First Out**

Python normally uses:

```python
from collections import deque

queue = deque()

queue.append(x)      # enqueue
queue.popleft()      # dequeue
```

Visual:

```text
FRONT              REAR
 ↓                   ↓
[10, 20, 30, 40]
```

`10` leaves first.

Common queue signals:

```text
arrival order
first come, first served
oldest waiting item
process in discovery order
```

Avoid repeatedly using:

```python
list.pop(0)
```

because removing from the beginning of a Python list is normally:

```text
O(n)
```

A `deque` supports efficient operations at both ends:

```python
d.append(x)
d.appendleft(x)

d.pop()
d.popleft()
```

---

# 5. Days 222–223 Revision — Singly Linked List

A linked list connects nodes using references.

```text
head
 ↓
10 → 20 → 30 → None
```

A node:

```python
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
```

Basic traversal:

```python
current = head

while current:
    # process current.val
    current = current.next
```

Traversal:

```text
Time: O(n)
Space: O(1)
```

Unlike arrays, linked lists don't provide efficient random indexing.

```text
Array:

nums[500]

usually O(1)


Linked list:

head → node → node → ... → node 500

O(n)
```

The key modification rule from Day 223 is:

> **Preserve a link before overwriting it.**

Insert after a known node:

```python
new_node.next = current.next
current.next = new_node
```

Delete a later node:

```python
current.next = current.next.next
```

Changing links in the wrong order can lose part of the list or accidentally create loops.

---

# 6. Compare All Five

| Pattern / Structure | Main idea | Strong recognition signal | Typical core operation |
|---|---|---|---|
| Sliding Window | Maintain a changing contiguous region | longest/shortest contiguous range under a condition | expand right, shrink left |
| Prefix Sum | Precompute cumulative information | repeated range sums | subtract two prefix values |
| Stack | Most recent item first | nesting, undo, brackets | push/pop top |
| Queue | Oldest item first | arrival/discovery order | enqueue rear, dequeue front |
| Linked List | Nodes connected by references | node traversal/insertion/deletion | follow/change `next` |

A very useful distinction is:

```text
Contiguous range changing dynamically
            ↓
     Sliding Window


Many queries on ranges
            ↓
       Prefix Sum


Most recent item matters
            ↓
          Stack


Oldest waiting item matters
            ↓
          Queue


Nodes + next references
            ↓
      Linked List
```

---

# 7. Pattern-Recognition Test — 10 Mini-Scenarios

Don't code these yet.

For each scenario, tell me which you would try:

```text
Sliding Window
Prefix Sum
Stack
Queue/Deque
Linked List
```

and give **one sentence explaining why**.

### Scenario 1

You receive a string and must find the **longest substring containing at most 2 distinct characters**.

### Scenario 2

You have an array that does not change, followed by 50,000 queries asking:

```text
sum from index L to index R
```

### Scenario 3

Given:

```text
"{[()]}"
```

determine whether every opening bracket closes in the correct order.

### Scenario 4

Customers arrive at a bank. They must be served in exactly the same order they arrived.

### Scenario 5

You receive:

```text
head → 5 → 8 → 12 → None
```

and need to find whether value `12` exists.

### Scenario 6

Find the longest contiguous subarray of positive integers whose sum is at most `k`.

### Scenario 7

An editor needs to implement:

```text
Undo last action
Undo previous action
Undo previous action
```

### Scenario 8

Given an array, you repeatedly need:

```text
sum before index i
sum after index i
```

for many positions.

### Scenario 9

Tasks arrive over time and should be processed based on which one has been waiting longest.

### Scenario 10

You have a reference to a linked-list node and need to insert a new node immediately after it.

Reply later in this format:

```text
1. ______ because ______
2. ______ because ______
...
10. ______ because ______
```

I will check not only whether you picked the right pattern, but whether your **recognition reasoning** is correct.

---

# 8. Mixed Coding Problem 1 — Easy

## Longest Valid Segment

Given:

```python
nums = [1, 1, 0, 1, 0, 0, 1, 1]
k = 2
```

Find the maximum length of a contiguous segment containing at most `k` zeros.

For the example, return the maximum valid length.

Do **not** just provide code.

Your answer must contain:

```text
1. Brute-force reasoning
2. Optimized reasoning
3. Pseudocode
4. Python
5. Time complexity
6. Space complexity
```

I am intentionally not naming the technique.

No hints yet.

---

# 9. Mixed Coding Problem 2 — Easy

## Multiple Interval Totals

Given:

```python
nums = [4, 2, 7, 1, 5, 3]

queries = [
    (0, 2),
    (1, 4),
    (3, 5),
    (0, 5)
]
```

Each pair:

```python
(left, right)
```

represents an **inclusive range**.

Return the sum for every query.

Your solution should be efficient when the number of queries becomes very large.

Provide:

```text
1. Brute-force reasoning
2. Optimized reasoning
3. Any preprocessing you need
4. Pseudocode
5. Python
6. Preprocessing complexity
7. Per-query complexity
8. Overall complexity
9. Space complexity
```

Again, I am not naming the intended technique.

---

# 10. Mixed Coding Problem 3 — Easy / Early Medium

## Remove Consecutive Pairs

Given:

```python
s = "azxxzy"
```

Whenever two equal characters become adjacent, remove both.

Continue until no such adjacent pair remains.

Example process:

```text
azxxzy

xx disappears

azzy

zz disappears

ay
```

Return:

```text
"ay"
```

You should process the string efficiently.

Your answer must include:

```text
1. Brute-force reasoning
2. Optimized reasoning
3. Pseudocode
4. Python
5. Time complexity
6. Space complexity
7. Empty-input behavior
```

No hint about the required data structure yet.

---

# 11. How I Want You to Answer

For each coding problem, don't jump immediately into Python.

Use this reasoning order:

```text
Step 1:
What exactly is the problem asking?

Step 2:
What would brute force do?

Step 3:
Why is brute force inefficient?

Step 4:
What information do I actually need to maintain?

Step 5:
Which pattern/data structure fits that behavior?

Step 6:
Write pseudocode.

Step 7:
Write Python.

Step 8:
State time complexity.

Step 9:
State space complexity.
```

This is important for interviews because I'm checking your **problem-solving process**, not only whether your final code runs.

---

# 12. Complexity Revision

You should be comfortable recognizing these rough complexities.

```text
Sliding through an array once
→ usually O(n)

Building prefix information
→ O(n)

Range query after preprocessing
→ O(1)

Stack push/pop
→ usually O(1)

Queue enqueue/dequeue with deque
→ usually O(1)

Traverse linked list
→ O(n)

Insert after already-known linked-list node
→ O(1)

Search linked list
→ O(n)
```

Be careful with statements like:

```text
"There is a while inside a for,
therefore it must be O(n²)."
```

That's not always true.

In a sliding-window algorithm, if both pointers only move forward, total movement can still be:

```text
O(n)
```

---

# 13. Revision Checklist

Before moving beyond Day 224, you should be able to confidently answer all of these:

- [ ] I can explain the difference between fixed and variable sliding windows.
- [ ] I know what `left` and `right` usually represent.
- [ ] I know why shrinking often uses `while`, not just `if`.
- [ ] I can calculate `right - left + 1`.
- [ ] I understand `prefix[i] = sum of first i elements`.
- [ ] I can use `prefix[right + 1] - prefix[left]`.
- [ ] I understand why prefix preprocessing costs O(n) but later queries can be O(1).
- [ ] I understand LIFO and can implement a stack with a Python list.
- [ ] I understand FIFO and can implement a queue with `collections.deque`.
- [ ] I know why repeated `list.pop(0)` is inefficient.
- [ ] I understand `append`, `appendleft`, `pop`, and `popleft`.
- [ ] I know what `head`, `current`, `val`, and `next` mean in a linked list.
- [ ] I can traverse a linked list without changing `head`.
- [ ] I can handle an empty linked list and a one-node linked list.
- [ ] I understand why linked-list random access is O(n).
- [ ] I can insert at the beginning of a linked list.
- [ ] I understand the safe order for inserting after a node.
- [ ] I can delete the head.
- [ ] I understand how to bypass a node during deletion.
- [ ] I can state time and space complexity for my solution.
- [ ] Most importantly, I can explain **why I chose a particular pattern before coding**.

For Day 224, answer the **10 recognition scenarios first**. Then solve **Mixed Problem 1 only**. I’ll review your pattern recognition and reasoning, point out weak areas, and then we’ll continue with Problems 2 and 3.