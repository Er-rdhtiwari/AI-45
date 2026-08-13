# Day 13 DSA Track — Heap / Priority Queue

## 1. Beginner-Friendly Summary

A **heap** is useful when you repeatedly need the **smallest or largest item without sorting everything**.

The three recognition patterns for today are:

```text
Top-K
    → Keep only the best K candidates.

Streaming
    → Data arrives continuously.
    → Cannot repeatedly sort everything seen so far.

Scheduling
    → Always process the next task according to
      priority / deadline / finish time.
```

Python's `heapq` implements a **min-heap**:

```python
import heapq

heap = []

heapq.heappush(heap, 10)
heapq.heappush(heap, 4)
heapq.heappush(heap, 7)

print(heapq.heappop(heap))
```

Output:

```text
4
```

The most important invariant is:

> `heap[0]` is always the smallest element in a Python min-heap.

For **Top K largest** problems, an especially useful technique is:

```text
Maintain a MIN heap of size K.

heap[0]
   ↓
smallest among the current K best elements
   ↓
candidate must beat this element to enter Top-K
```

---

# 2. Heap vs Priority Queue

These terms are related but slightly different.

A **priority queue** is an abstract data structure:

```text
insert(item, priority)
remove_highest_priority()
peek_highest_priority()
```

A **heap** is one common implementation of a priority queue.

Conceptually:

```text
Priority Queue
      |
      | implementation
      v
     Heap
```

Other structures could theoretically implement a priority queue, but heaps provide an excellent balance:

```text
Insert     O(log n)
Pop        O(log n)
Peek       O(1)
Build heap O(n)
```

---

# 3. Heap Structure

A binary min-heap obeys:

```text
Parent <= Children
```

Example:

```text
          2
        /   \
       5     4
      / \   / \
     9   8 7   6
```

Notice something important:

This is **not completely sorted**.

For example:

```text
5 > 4
```

even though `5` appears earlier visually.

A heap guarantees only the parent-child relationship necessary to efficiently retrieve the minimum.

---

# 4. Array Representation

Heaps are usually represented using arrays.

For index `i`:

```text
left child  = 2*i + 1
right child = 2*i + 2
parent      = (i-1) // 2
```

Example:

```text
Heap:

          2
        /   \
       5     4
      / \
     9   8


Array:

index:  0  1  2  3  4
value: [2, 5, 4, 9, 8]
```

No tree nodes are required.

---

# 5. Python Heap Operations

```python
import heapq
```

## Push

```python
heapq.heappush(heap, value)
```

Complexity:

```text
O(log n)
```

---

## Pop minimum

```python
value = heapq.heappop(heap)
```

Complexity:

```text
O(log n)
```

---

## Peek minimum

```python
heap[0]
```

Complexity:

```text
O(1)
```

---

## Convert list into heap

```python
heapq.heapify(values)
```

Complexity:

```text
O(n)
```

Not:

```text
O(n log n)
```

`heapify()` uses a bottom-up construction algorithm.

---

## Push and immediately pop

```python
heapq.heappushpop(heap, value)
```

Useful for bounded heaps.

---

# 6. Max Heap in Python

Traditionally, Python `heapq` is used as a min-heap.

A common way to simulate a max-heap is storing negative values:

```python
numbers = [5, 2, 9, 4]

heap = []

for x in numbers:
    heapq.heappush(heap, -x)

largest = -heapq.heappop(heap)

print(largest)
```

Output:

```text
9
```

Conceptually:

```text
Original:

9 > 5 > 4 > 2


Negated:

-9 < -5 < -4 < -2
```

Therefore Python's minimum becomes our original maximum.

---

# 7. Recognition Signals

Before coding, recognize when a heap is appropriate.

## Signal 1 — "Top K"

Words such as:

```text
K largest
K smallest
K closest
K most frequent
K highest scoring
K cheapest
```

should immediately make you consider a heap.

Example:

```text
Find the 10 largest numbers among 10 million values.
```

Sorting 10 million values may be unnecessary.

Maintain only 10 candidates.

---

## Signal 2 — Continually changing best candidate

Examples:

```text
always process smallest distance
always choose highest priority
always choose earliest finishing task
always take cheapest available resource
```

A heap lets us repeatedly find that candidate efficiently.

---

## Signal 3 — Streaming data

Suppose values arrive continuously:

```text
5
12
3
17
8
21
...
```

and the system asks:

> What are the largest 3 values seen so far?

We don't want to repeatedly sort all previous data.

Maintain:

```text
min-heap of size 3
```

Memory becomes:

```text
O(k)
```

instead of storing/sorting everything.

---

## Signal 4 — Scheduling

Words such as:

```text
next available
earliest deadline
minimum finishing time
highest-priority task
next meeting ending
available worker
```

are strong heap signals.

---

## Signal 5 — Repeated minimum/maximum queries

If an algorithm repeatedly does:

```text
Find minimum
remove minimum
insert something
find minimum
remove minimum
...
```

a heap is often better than repeatedly sorting.

---

# 8. Core Pattern 1 — Top K Largest

Suppose:

```text
numbers = [4, 10, 2, 8, 15, 3]
k = 3
```

We want:

```text
15, 10, 8
```

Maintain a **min-heap of size K**.

Why a min-heap?

Because among our current Top-K values, we care most about the weakest candidate.

```text
Top 3 candidates:

[8, 15, 10]

smallest candidate = 8
```

If a new value is:

```text
12
```

then:

```text
12 > 8
```

So `8` should leave.

New Top 3:

```text
10, 12, 15
```

The min-heap exposes `8` in `O(1)`.

---

# 9. Top-K Invariant

This is worth memorizing.

During processing:

> The heap contains the best K elements among all elements processed so far.

And:

```text
heap[0]
```

is:

> The worst element among those K best elements.

That sounds strange initially, but it is the foundation of many Top-K problems.

---

# 10. Top-K Template

```python
import heapq

def top_k_largest(nums, k):
    heap = []

    for num in nums:
        heapq.heappush(heap, num)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap
```

Example:

```python
top_k_largest([4, 10, 2, 8, 15, 3], 3)
```

The heap contains the three largest values.

The internal heap order is not guaranteed to be descending.

---

# 11. Complexity of Top-K Heap

Suppose:

```text
n = total elements
k = required results
```

Each element may cause one heap operation:

```text
O(log k)
```

Therefore:

```text
Time  = O(n log k)
Space = O(k)
```

Compare with sorting:

```text
O(n log n)
```

When:

```text
k << n
```

the heap approach can be substantially better.

---

# 12. Core Pattern 2 — Streaming Selection

Imagine transactions arrive continuously:

```text
Transaction stream
      |
      v
+-------------+
|   Min Heap  |
|   size = K  |
+-------------+
      |
      v
Top-K suspicious scores
```

Suppose:

```text
k = 3
```

Stream:

```text
5, 2, 10, 4, 12, 8
```

Start:

```text
[]
```

5:

```text
[5]
```

2:

```text
[2, 5]
```

10:

```text
[2, 5, 10]
```

4 arrives.

Heap is already size 3.

Compare:

```text
4 > heap[0]
4 > 2
```

Replace 2:

```text
[4, 5, 10]
```

12:

```text
12 > 4

[5, 12, 10]
```

8:

```text
8 > 5

[8, 12, 10]
```

Final values are:

```text
8, 10, 12
```

---

# 13. Better Streaming Implementation

Instead of:

```python
heappush(...)
heappop(...)
```

we can sometimes use:

```python
heapq.heapreplace(heap, value)
```

Example:

```python
if num > heap[0]:
    heapq.heapreplace(heap, num)
```

This removes the minimum and inserts the new element efficiently.

---

# 14. Core Pattern 3 — Scheduling

Imagine three jobs:

```text
Job A finishes at 10
Job B finishes at 4
Job C finishes at 7
```

If the system repeatedly needs:

> Which job becomes available next?

Use:

```text
min-heap ordered by finishing time
```

Heap conceptually:

```text
       4
      / \
    10   7
```

The next available job is immediately:

```text
heap[0] = 4
```

Scheduling problems often store tuples:

```python
(end_time, resource_id)
```

Example:

```python
heapq.heappush(heap, (15, "worker_3"))
```

Python compares the first tuple field first.

---

# 15. Common Scheduling Pattern

Suppose workers become available at:

```text
worker A → time 12
worker B → time 5
worker C → time 9
```

Heap:

```python
[
    (5, "B"),
    (12, "A"),
    (9, "C")
]
```

Pop:

```python
available_time, worker = heapq.heappop(heap)
```

You get worker B because it becomes available first.

After assigning more work:

```python
new_available_time = 14

heapq.heappush(heap, (14, "B"))
```

This pattern appears in:

* job schedulers
* meeting room allocation
* CPU simulation
* worker pools
* server assignment
* event simulation

---

# 16. Important Tuple Pattern

Often we need:

```python
(priority, item)
```

For example:

```python
heapq.heappush(heap, (2, "task-A"))
heapq.heappush(heap, (1, "task-B"))
```

Pop returns:

```text
(1, "task-B")
```

For more complex objects, use a tie-breaker:

```python
(priority, sequence_number, task)
```

Example:

```python
(5, 0, task_a)
(5, 1, task_b)
```

Why?

If priorities are equal, Python otherwise may try to compare the task objects themselves.

---

# 17. Choosing Min-Heap vs Max-Heap

This frequently causes confusion.

### K largest values

Use:

```text
MIN heap of size K
```

because we want quick access to the smallest current winner.

### K smallest values

Use conceptually:

```text
MAX heap of size K
```

because we want quick access to the largest current winner.

In Python that commonly means negating values.

---

# 18. Medium Problem — Top K Frequent Elements

## Problem

Given an integer array `nums` and integer `k`, return the `k` most frequent elements.

Example:

```text
nums = [1,1,1,2,2,3]
k = 2
```

Frequency:

```text
1 → 3
2 → 2
3 → 1
```

Result:

```text
[1, 2]
```

The result order does not matter unless specifically required.

---

# 19. Recognition Signals

The problem says:

```text
K most frequent
```

Immediately recognize:

```text
Top-K problem
       +
frequency counting
```

This suggests two structures:

```text
Hash Map
   +
Heap
```

Pipeline:

```text
nums
 |
 v
frequency map
 |
 v
(element, frequency)
 |
 v
min-heap size K
 |
 v
Top K frequent
```

---

# 20. Brute-Force Reasoning

First count frequencies.

For:

```text
[1,1,1,2,2,3]
```

create:

```python
{
    1: 3,
    2: 2,
    3: 1
}
```

Then convert into something like:

```text
[(1,3), (2,2), (3,1)]
```

Sort by frequency descending:

```text
[(1,3), (2,2), (3,1)]
```

Take first `k`.

---

## Brute-Force Pseudocode

```text
count frequency of every number

create list of (number, frequency)

sort list by frequency descending

return first K numbers
```

---

## Brute-Force Complexity

Let:

```text
n = number of input values
m = number of distinct values
```

Frequency counting:

```text
O(n)
```

Sorting unique values:

```text
O(m log m)
```

Total:

```text
O(n + m log m)
```

Worst case:

```text
m = n
```

giving:

```text
O(n log n)
```

Space:

```text
O(m)
```

---

# 21. Optimized Heap Reasoning

We do not care about fully ordering all `m` unique values.

We need only:

```text
K winners
```

Therefore maintain:

```text
min-heap of size K
```

Each heap entry:

```text
(frequency, number)
```

Why frequency first?

Because we want the heap ordered according to frequency.

Example:

```text
(3, 1)
```

means:

```text
number 1 occurs 3 times
```

---

# 22. Heap Invariant

After processing any number of unique elements:

> The heap contains the K highest-frequency elements encountered so far.

And:

```text
heap[0]
```

represents the least frequent element among the current winners.

Therefore, once the heap exceeds size `k`:

```python
heapq.heappop(heap)
```

removes the weakest candidate.

---

# 23. Optimized Pseudocode

```text
frequency = count every element

heap = empty min-heap

for each number and count:
    push (count, number)

    if heap size > k:
        pop minimum-frequency element

result = numbers remaining in heap

return result
```

---

# 24. Dry Run

Input:

```text
nums = [1,1,1,2,2,3]
k = 2
```

Frequency:

```text
1 → 3
2 → 2
3 → 1
```

Start:

```text
heap = []
```

Process `1`:

```text
push (3,1)

heap:
[(3,1)]
```

Process `2`:

```text
push (2,2)

heap:
[(2,2), (3,1)]
```

Heap size is `2`.

Fine.

Process `3`:

```text
push (1,3)
```

Conceptually:

```text
[(1,3), (3,1), (2,2)]
```

Size:

```text
3 > k
```

Remove smallest frequency:

```text
(1,3)
```

Remaining:

```text
[(2,2), (3,1)]
```

Therefore result:

```text
[2, 1]
```

which correctly represents the two most frequent elements.

---

# 25. Edge Cases

## Edge Case 1 — One element

```text
nums = [5]
k = 1
```

Result:

```text
[5]
```

---

## Edge Case 2 — Every value has same frequency

```text
nums = [1,2,3]
k = 2
```

Any valid two values can be returned if the problem permits arbitrary order for ties.

---

## Edge Case 3 — K equals unique count

```text
nums = [1,1,2,3]
k = 3
```

Return every unique number.

---

## Edge Case 4 — Negative numbers

```text
nums = [-1,-1,-2,-3]
```

No special treatment is needed.

Dictionary keys and heap tuples handle negative integers normally.

---

## Edge Case 5 — Very large input

This is where bounded-heap logic matters.

Instead of sorting potentially millions of unique values, the heap remains bounded by:

```text
k
```

apart from the required frequency map.

---

# 26. Complexity of Optimized Heap Solution

Frequency map:

```text
O(n)
```

For `m` unique values, each heap operation costs:

```text
O(log k)
```

Therefore:

```text
Time:
O(n + m log k)

Space:
O(m + k)
```

The map dominates memory:

```text
O(m)
```

When:

```text
k << m
```

the heap avoids sorting all unique values.

---

# 27. Python Solution

```python
from collections import Counter
import heapq


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    frequencies = Counter(nums)

    heap: list[tuple[int, int]] = []

    for number, frequency in frequencies.items():
        heapq.heappush(heap, (frequency, number))

        if len(heap) > k:
            heapq.heappop(heap)

    return [number for frequency, number in heap]
```

Example:

```python
nums = [1, 1, 1, 2, 2, 3]

print(top_k_frequent(nums, 2))
```

Possible output:

```text
[2, 1]
```

Both:

```text
[1, 2]
```

and:

```text
[2, 1]
```

are correct.

---

# 28. Why the Algorithm Is Correct

The correctness argument comes from the bounded heap invariant.

Suppose the heap currently contains the `k` highest-frequency elements encountered so far.

Now consider a new element with frequency `f`.

We insert it.

The heap temporarily contains:

```text
k + 1
```

candidates.

Exactly one of these candidates cannot belong to the best K.

Which one?

The element with the smallest frequency.

The min-heap exposes exactly that element:

```python
heapq.heappop(heap)
```

After removing it, the heap again contains the best `k` candidates.

Therefore, after every unique number has been processed, the heap contains exactly the `k` most frequent elements.

---

# 29. Why Not Use a Max Heap?

You might think:

> We need the biggest frequencies, so use a max heap.

You could.

But then you would normally store **all unique elements** and pop K times:

```text
Heap size = m
```

That gives approximately:

```text
O(m + k log m)
```

The bounded min-heap approach uses:

```text
Heap size = k
```

and naturally discards bad candidates early.

The deeper Top-K principle is:

```text
Want K largest
      ↓
keep K winners
      ↓
need fast access to weakest winner
      ↓
MIN HEAP
```

---

# 30. Alternative: Bucket Sort

There is an even better theoretical solution for this particular problem.

Frequency cannot exceed:

```text
n
```

so we can create buckets:

```text
frequency 1 → [...]
frequency 2 → [...]
frequency 3 → [...]
...
```

Then scan backward.

This can achieve:

```text
O(n)
```

time.

But for **Day 13**, the heap solution is more useful because it teaches a reusable pattern applicable to:

* Top K prices
* Top K scores
* Top K nearest objects
* Top K frequent events
* streaming ranking
* bounded candidate selection

---

# 31. Common Mistake — Sorting the Heap

Suppose:

```python
heap = [3, 5, 4, 10, 8]
```

Do not assume:

```text
3 < 5 < 4 < 10 < 8
```

A heap is not sorted.

Only this is guaranteed:

```python
heap[0] == minimum
```

If the final answer needs sorted output, sorting the K remaining values costs:

```text
O(k log k)
```

which can still be much cheaper than sorting all `n` elements.

---

# 32. Common Mistake — Wrong Heap Direction

For:

```text
K largest
```

students often create a max-heap of size K.

Ask instead:

> Which element must I efficiently remove when a better candidate arrives?

For K largest:

```text
remove smallest winner
```

Therefore:

```text
min-heap
```

For K smallest:

```text
remove largest winner
```

Therefore:

```text
max-heap
```

---

# 33. Common Mistake — Keeping More Than K Items

This:

```python
for num in nums:
    heapq.heappush(heap, num)
```

creates an `O(n)` heap.

For Top-K streaming selection, the key invariant should be:

```text
len(heap) <= k
```

after each iteration.

---

# 34. Common Mistake — Using `heapify()` Incorrectly

This works:

```python
heap = [5, 3, 8, 1]

heapq.heapify(heap)
```

Afterward the list is a valid heap.

But don't expect:

```python
heap == [1, 3, 5, 8]
```

Heapify creates a valid heap, not a fully sorted list.

---

# 35. Common Mistake — Tuple Comparisons

Consider:

```python
heapq.heappush(heap, (5, custom_object_a))
heapq.heappush(heap, (5, custom_object_b))
```

If both priorities are `5`, Python might need to compare:

```text
custom_object_a
vs
custom_object_b
```

which may fail.

Use:

```python
(priority, counter, object)
```

Example:

```python
import itertools

counter = itertools.count()

heapq.heappush(heap, (5, next(counter), custom_object_a))
heapq.heappush(heap, (5, next(counter), custom_object_b))
```

This is particularly useful in real job schedulers.

---

# 36. Scheduling Pattern to Remember

A very common heap pattern is:

```text
sort events by start time
        |
        v
min-heap of active end times
        |
        +--> earliest ending resource
        |
        v
reuse or allocate resource
```

For example, Meeting Rooms II conceptually does:

```text
Meetings:
[0,30]
[5,10]
[15,20]
```

At each meeting:

```text
Which room becomes available first?
```

That's a heap question.

The heap stores:

```text
meeting end times
```

not the full scheduling history.

---

# 37. Streaming Top-K Template to Memorize

```python
import heapq


def top_k_stream(stream, k):
    heap = []

    for value in stream:
        if len(heap) < k:
            heapq.heappush(heap, value)

        elif value > heap[0]:
            heapq.heapreplace(heap, value)

    return heap
```

Its central invariant:

```text
heap contains largest K values seen so far
```

with:

```text
Time per new value = O(log k)
Memory             = O(k)
```

That makes it suitable for large or unbounded streams.

---

# 38. Pattern Comparison

| Requirement          | Best mental model            | Typical heap    |
| -------------------- | ---------------------------- | --------------- |
| K largest            | Keep winners, remove weakest | Min-heap size K |
| K smallest           | Keep winners, remove weakest | Max-heap size K |
| Stream Top-K         | Bounded candidate set        | Heap size K     |
| Earliest event       | Next event first             | Min-heap        |
| Highest priority     | Best priority first          | Min/max heap    |
| Meeting rooms        | Earliest finishing room      | Min-heap        |
| Merge sorted streams | Smallest current head        | Min-heap        |
| Dijkstra             | Smallest known distance      | Min-heap        |

---

# 39. Heap Complexity Cheat Sheet

For heap size `h`:

```text
Peek:
O(1)

Push:
O(log h)

Pop:
O(log h)

Push + pop:
O(log h)

Heapify:
O(h)
```

For a Top-K problem:

```text
h <= k
```

so operations become:

```text
O(log k)
```

rather than:

```text
O(log n)
```

That distinction is one of the main reasons bounded heaps are powerful.

---

# 40. Today's Mental Model

When you encounter a problem, run this decision process:

```text
Do I repeatedly need smallest/largest?
              |
           yes
              |
              v
           Heap?


Does the problem say Top-K?
              |
           yes
              |
              v
Can I keep only K candidates?
              |
           yes
              |
              v
Bounded heap of size K


Do events/tasks compete by
priority/deadline/finish time?
              |
           yes
              |
              v
Priority Queue / Heap


Does data arrive continuously?
              |
           yes
              |
              v
Maintain heap incrementally
instead of repeatedly sorting
```

The key Day 13 takeaway is:

> **Sorting answers "put everything in order." A heap answers "keep giving me the next best item."**

And for Top-K:

> **Do not rank everything when you only need K winners. Maintain K candidates and efficiently remove the weakest one.**
