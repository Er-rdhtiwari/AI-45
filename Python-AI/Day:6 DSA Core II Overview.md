# Day 6 – DSA Core II: Two Pointers, Sliding Window, Stacks & Queues

## 1. Five-Minute Summary

* **Two pointers** use two indexes to scan data efficiently instead of checking every pair.
* **Sliding window** maintains a continuous section of an array or string and updates it incrementally.
* A **stack** follows **Last In, First Out**, making it useful for nested structures, undo operations, and expression validation.
* A **queue** follows **First In, First Out**, making it useful for request processing, streaming, buffering, and breadth-first search.
* These patterns often reduce brute-force solutions from **O(n²)** to **O(n)**.

---

# Part 1: Two Pointers

## Concept

The two-pointer pattern uses two indexes that move through an array or string.

Instead of comparing every possible pair, we move the pointers according to what we learn from the current values.

Two pointers are especially useful when:

* The input is sorted.
* We need to find a pair.
* We need to compare values from both ends.
* We need to remove or rearrange elements in place.
* We need to maintain a readable and writable position.

---

## Diagram in Words

Imagine a sorted array:

```text
[1, 2, 4, 6, 8, 10]
 L               R
```

* `L` points to the smallest value.
* `R` points to the largest value.
* We examine the pair.
* Based on the result, we move either `L` or `R`.

The pointers gradually move inward:

```text
[1, 2, 4, 6, 8, 10]
    L        R
```

This avoids checking every possible pair.

---

## Pattern 1: Inward-Moving Pointers

The left pointer starts at the beginning.

The right pointer starts at the end.

```python
left = 0
right = len(values) - 1

while left < right:
    # Process values[left] and values[right]

    if some_condition:
        left += 1
    else:
        right -= 1
```

Typical problems:

* Two-sum in a sorted array
* Checking whether a string is a palindrome
* Finding the maximum water container
* Comparing values from both ends

---

## Example: Two-Sum in a Sorted Array

### Problem

Given a sorted array and a target, find two numbers whose sum equals the target.

```text
numbers = [1, 2, 4, 6, 8, 10]
target = 14
```

The answer is `4 + 10`.

---

## Intuition

Because the array is sorted:

* If the current sum is too small, move the left pointer right to get a larger value.
* If the current sum is too large, move the right pointer left to get a smaller value.
* If the sum matches, return the result.

---

## Python Solution

```python
from typing import List, Optional, Tuple


def two_sum_sorted(
    numbers: List[int],
    target: int,
) -> Optional[Tuple[int, int]]:
    """
    Return the indexes of two numbers whose sum equals the target.

    The input array must be sorted in ascending order.
    """

    # Start one pointer at each end of the array.
    left = 0
    right = len(numbers) - 1

    # We need two different elements, so stop when the pointers meet.
    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return left, right

        if current_sum < target:
            # The sum is too small.
            # Because the array is sorted, moving left to the right
            # gives us a larger value.
            left += 1
        else:
            # The sum is too large.
            # Moving right to the left gives us a smaller value.
            right -= 1

    # No pair was found.
    return None


numbers = [1, 2, 4, 6, 8, 10]
print(two_sum_sorted(numbers, 14))
```

Output:

```text
(2, 5)
```

---

## Complexity

* Time: **O(n)**
* Extra space: **O(1)**

A brute-force solution would examine every pair and take **O(n²)** time.

---

## Tricky Parts

### 1. The array must be sorted

The pointer movements only work because increasing or decreasing the sum is predictable.

For an unsorted array, a hash map is usually better.

### 2. Use `left < right`

Using `left <= right` could allow the same element to be used twice.

### 3. Clarify the expected output

An interviewer may ask for:

* Indexes
* Actual values
* One pair
* All pairs

---

## Example: Palindrome Check

A palindrome reads the same from left to right and right to left.

Examples:

```text
racecar
level
madam
```

---

## Diagram in Words

```text
r a c e c a r
L           R
```

Compare the outside characters first.

Then move inward:

```text
r a c e c a r
  L       R
```

If any pair differs, the string is not a palindrome.

---

## Python Solution

```python
def is_palindrome(text: str) -> bool:
    """
    Return True if the text is a palindrome.
    This simple version compares every character exactly as provided.
    """

    left = 0
    right = len(text) - 1

    while left < right:
        if text[left] != text[right]:
            return False

        # Move both pointers toward the center.
        left += 1
        right -= 1

    return True
```

---

## Pattern 2: Slow and Fast Pointers

Two pointers do not always start at opposite ends.

Sometimes both move from left to right, but at different speeds or for different purposes.

Common examples:

* Removing duplicates from a sorted array
* Moving zeroes
* Partitioning data
* Detecting a cycle in a linked list
* Maintaining a write position while scanning input

---

## Diagram in Words

Consider:

```text
[1, 1, 2, 2, 3]
 W
 S
```

* `S`, the scan pointer, examines every value.
* `W`, the write pointer, shows where the next valid value should be placed.

As scanning continues:

```text
[1, 2, 3, 2, 3]
       W
             S
```

The front of the array contains the cleaned result.

---

## Example: Remove Duplicates from a Sorted Array

```python
from typing import List


def remove_duplicates(numbers: List[int]) -> int:
    """
    Remove duplicates from a sorted list in place.

    Return the number of unique elements.
    The first 'unique_count' positions contain the unique values.
    """

    if not numbers:
        return 0

    # 'write' points to the position of the last unique value.
    write = 0

    # 'scan' checks each remaining element.
    for scan in range(1, len(numbers)):
        if numbers[scan] != numbers[write]:
            # We found a new unique value.
            write += 1
            numbers[write] = numbers[scan]

    # Since 'write' is an index, the count is write + 1.
    return write + 1
```

---

## Practical AI and Backend Use Cases

### 1. Cleaning sorted event IDs

Suppose a service receives sorted event IDs:

```text
[101, 101, 102, 103, 103]
```

A slow/write pointer approach can remove duplicate events without creating another large array.

### 2. Comparing token sequences

Two pointers can compare:

* Expected tokens and generated tokens
* Original text and normalized text
* Two sorted lists of document IDs

### 3. Merging sorted results

Search results from two sorted sources can be merged using two forward-moving pointers.

For example:

* Keyword-search results
* Vector-search results
* Ranked document IDs from two retrieval systems

---

## How to Recognize Two Pointers

Look for clues such as:

* “Sorted array”
* “Find a pair”
* “Compare both ends”
* “Remove duplicates in place”
* “Move elements”
* “Merge two sorted collections”
* “Palindrome”
* “Use constant extra space”

---

## Common Two-Pointer Pitfalls

### Pitfall 1: Using two pointers on unsorted input

For two-sum, inward pointers require sorted data.

Sorting first costs **O(n log n)** and may lose original indexes.

### Pitfall 2: Moving the wrong pointer

Always ask:

* What change will increase the value?
* What change will decrease the value?

### Pitfall 3: Forgetting pointer progress

Every loop iteration must move at least one pointer unless the function returns.

Otherwise, the loop may never end.

### Pitfall 4: Off-by-one errors

Be careful with:

```python
right = len(numbers) - 1
```

The final valid index is not `len(numbers)`.

---

# Part 2: Sliding Window

## Concept

A sliding window represents a continuous section of an array or string.

Instead of recalculating information for every section, we:

1. Add the new element entering the window.
2. Remove the old element leaving the window.
3. Update the answer.

This often reduces an **O(n × k)** or **O(n²)** solution to **O(n)**.

---

## Diagram in Words

Given:

```text
[2, 1, 5, 1, 3, 2]
```

A window of size three starts as:

```text
[2, 1, 5] 1, 3, 2
```

Then it slides one step:

```text
2 [1, 5, 1] 3, 2
```

Then again:

```text
2, 1 [5, 1, 3] 2
```

Each time:

* One value enters.
* One value leaves.

---

# Fixed-Size Sliding Window

## When to Use It

Use a fixed-size window when the problem explicitly provides a size such as:

* Maximum sum of `k` consecutive values
* Average of every `k` events
* Number of errors in every five-minute bucket
* Maximum token usage in any 100 consecutive requests

Common clues:

* “Subarray of size `k`”
* “Every `k` consecutive elements”
* “Moving average”
* “Rolling sum”

---

## Example: Maximum Sum of `k` Consecutive Elements

### Brute-Force Idea

For every possible starting point:

* Recalculate the sum of the next `k` elements.

This takes:

```text
O(n × k)
```

### Sliding-Window Idea

* Calculate the first window once.
* Add the new incoming value.
* Subtract the outgoing value.

---

## Python Solution

```python
from typing import List


def max_sum_of_size_k(numbers: List[int], k: int) -> int:
    """
    Return the maximum sum of any contiguous subarray of size k.
    """

    if k <= 0:
        raise ValueError("k must be positive")

    if k > len(numbers):
        raise ValueError("k cannot be larger than the list")

    # Build the first window: indexes 0 through k - 1.
    window_sum = sum(numbers[:k])
    best_sum = window_sum

    # 'right' is the index of the new element entering the window.
    for right in range(k, len(numbers)):
        # The outgoing element is exactly k positions behind 'right'.
        outgoing_index = right - k

        window_sum += numbers[right]
        window_sum -= numbers[outgoing_index]

        best_sum = max(best_sum, window_sum)

    return best_sum


numbers = [2, 1, 5, 1, 3, 2]
print(max_sum_of_size_k(numbers, 3))
```

Output:

```text
9
```

The best window is:

```text
[5, 1, 3]
```

---

## Tricky Window Boundary

When `right` enters the window, the outgoing index is:

```python
right - k
```

For example, if:

```text
right = 3
k = 3
```

Then index `0` leaves:

```text
3 - 3 = 0
```

---

## Complexity

* Time: **O(n)**
* Extra space: **O(1)**

---

## Practical Example: Log Processing

Suppose each value represents the number of errors per minute:

```text
[2, 1, 5, 1, 3, 2]
```

To find the highest error count in any three-minute period, use a fixed-size window of three.

The same approach supports:

* Requests per minute
* Token consumption
* Latency measurements
* Failed tool calls
* GPU utilization samples

---

# Variable-Size Sliding Window

## Concept

A variable window grows and shrinks depending on whether it satisfies a condition.

The general process is:

1. Expand the right side.
2. Update the window state.
3. While the window is invalid, shrink from the left.
4. Record the best valid answer.

---

## Diagram in Words

Suppose we want the longest substring with no repeated characters:

```text
a b c a b
L
R
```

Expand right:

```text
[a b c] a b
 L   R
```

When the second `a` enters, the window becomes invalid:

```text
[a b c a] b
 L     R
```

Move `L` forward until there are no duplicates:

```text
a [b c a] b
   L   R
```

---

## General Variable-Window Template

```python
left = 0

for right in range(len(data)):
    # Add data[right] to the window state.

    while window_is_invalid:
        # Remove data[left] from the window state.
        left += 1

    # The window from left to right is valid here.
    current_length = right - left + 1
```

---

## Why `right - left + 1`?

Indexes are inclusive.

For example:

```text
left = 2
right = 4
```

The indexes are:

```text
2, 3, 4
```

That is three elements:

```text
4 - 2 + 1 = 3
```

This `+1` is a common interview bug.

---

## Example: Longest Substring Without Repeating Characters

### Problem

Given a string, return the length of the longest substring containing no repeated characters.

```text
"abcabcbb"
```

The answer is `3`, from `"abc"`.

---

## Intuition

Maintain a window with unique characters.

* Expand the right pointer.
* If a character is repeated, move the left pointer until the window becomes valid again.
* Record the maximum valid window length.

---

## Python Solution Using a Set

```python
def longest_unique_substring(text: str) -> int:
    """
    Return the length of the longest substring
    containing no repeated characters.
    """

    # Stores the characters currently inside the window.
    characters_in_window: set[str] = set()

    left = 0
    best_length = 0

    for right in range(len(text)):
        # If text[right] already exists in the window,
        # shrink from the left until the duplicate is removed.
        while text[right] in characters_in_window:
            characters_in_window.remove(text[left])
            left += 1

        # The new character can now safely enter the window.
        characters_in_window.add(text[right])

        # Both boundaries are included, so use +1.
        current_length = right - left + 1
        best_length = max(best_length, current_length)

    return best_length
```

---

## Complexity

* Time: **O(n)**
* Extra space: **O(min(n, alphabet size))**

Although there is a `while` loop inside a `for` loop, the algorithm is still O(n).

Why?

Every character:

* Enters the window at most once.
* Leaves the window at most once.

So the total pointer movements are proportional to `2n`.

---

## Faster Version Using Last-Seen Index

```python
def longest_unique_substring_fast(text: str) -> int:
    """
    Return the longest substring length with no repeated characters.

    Uses the last index where each character appeared.
    """

    last_seen: dict[str, int] = {}
    left = 0
    best_length = 0

    for right, character in enumerate(text):
        if character in last_seen:
            # Only move left forward.
            #
            # max() is important because the previous occurrence
            # might already be outside the current window.
            left = max(left, last_seen[character] + 1)

        last_seen[character] = right

        current_length = right - left + 1
        best_length = max(best_length, current_length)

    return best_length
```

---

## Important Tricky Part

Do not write only:

```python
left = last_seen[character] + 1
```

The previous occurrence may already be outside the current window.

Correct:

```python
left = max(left, last_seen[character] + 1)
```

The left pointer should never move backward.

---

## Example: Smallest Subarray with Sum at Least Target

### Problem

Find the minimum length of a contiguous subarray whose sum is at least a target.

Assumption: all numbers are positive.

```text
numbers = [2, 3, 1, 2, 4, 3]
target = 7
```

Answer:

```text
[4, 3]
```

Length: `2`

---

## Intuition

* Expand right until the sum reaches the target.
* Once valid, shrink from the left as much as possible.
* Record the shortest valid window.

---

## Python Solution

```python
from typing import List


def min_subarray_length(target: int, numbers: List[int]) -> int:
    """
    Return the minimum length of a contiguous subarray
    whose sum is at least target.

    Assumes all numbers are positive.
    Return 0 if no valid subarray exists.
    """

    left = 0
    window_sum = 0

    # Start with infinity so any valid length will be smaller.
    best_length = float("inf")

    for right in range(len(numbers)):
        # Expand the window by including numbers[right].
        window_sum += numbers[right]

        # While the current window is valid, try to shorten it.
        while window_sum >= target:
            current_length = right - left + 1
            best_length = min(best_length, current_length)

            # Remove the leftmost value before moving left.
            window_sum -= numbers[left]
            left += 1

    if best_length == float("inf"):
        return 0

    return int(best_length)
```

---

## Why Positive Numbers Matter

This sliding-window strategy depends on predictable behavior:

* Adding a positive number cannot decrease the sum.
* Removing a positive number cannot increase the sum.

If negative numbers are allowed, this logic may fail.

A prefix-sum or deque-based technique may be required instead.

---

## Longest vs Shortest Window Pattern

### Longest Valid Window

```python
for right in range(len(data)):
    add_right_value()

    while window_is_invalid:
        remove_left_value()
        left += 1

    update_maximum()
```

### Shortest Valid Window

```python
for right in range(len(data)):
    add_right_value()

    while window_is_valid:
        update_minimum()
        remove_left_value()
        left += 1
```

The key difference is when shrinking happens.

---

## Practical AI and Backend Use Cases

### 1. Request-rate monitoring

Track the number of API requests in the last 60 seconds.

### 2. Token-budget monitoring

Find the longest sequence of messages whose total tokens remain under a model context limit.

### 3. Streaming anomaly detection

Measure:

* Error count in the latest time window
* Average latency over recent requests
* Failed tool calls in the last `k` operations

### 4. Conversation analysis

Find the longest section of a conversation containing:

* No duplicate intent labels
* At most `k` distinct topics
* A token sum below a limit

### 5. Log pattern detection

Find the shortest time range containing all required event types:

```text
LOGIN
MODEL_CALL
DATABASE_WRITE
RESPONSE
```

---

## How to Recognize Sliding Window

Look for:

* “Contiguous”
* “Substring”
* “Subarray”
* “Consecutive”
* “Longest section”
* “Shortest section”
* “At most `k`”
* “Exactly `k`”
* “Within the last `k` events”
* “Rolling average”
* “Recent time interval”

---

## Common Sliding-Window Pitfalls

### Pitfall 1: Applying it to non-contiguous data

Sliding window works with continuous ranges.

It does not directly solve arbitrary subsequence problems.

### Pitfall 2: Incorrect window length

Correct:

```python
right - left + 1
```

### Pitfall 3: Removing after moving left

Usually:

```python
remove(data[left])
left += 1
```

Do not move `left` before removing the old value.

### Pitfall 4: Failing to shrink repeatedly

Use `while`, not always `if`.

Incorrect:

```python
if window_is_invalid:
    left += 1
```

The window may require several removals before becoming valid.

### Pitfall 5: Assuming all sum problems support sliding windows

Variable-size sum windows often require non-negative values.

Negative values can break the monotonic behavior.

### Pitfall 6: Updating the answer at the wrong time

For longest valid windows, update after invalid elements have been removed.

For shortest valid windows, update inside the shrinking loop.

---

# Part 3: Stack

## Concept

A stack follows:

```text
Last In, First Out
```

The most recently added item is the first one removed.

Think of a stack of plates:

```text
Top
[Plate C]  <- removed first
[Plate B]
[Plate A]
Bottom
```

---

## Basic Operations

```python
stack = []

stack.append("A")   # Push
stack.append("B")   # Push

top = stack[-1]     # Peek
value = stack.pop() # Pop
```

All three operations are usually **O(1)**.

---

## Common Stack Use Cases

* Balanced parentheses
* Nested JSON or XML validation
* Function-call tracking
* Undo operations
* Browser history
* Expression evaluation
* Depth-first search
* Monotonic stack problems

---

# Balanced Parentheses

## Problem

Determine whether brackets are correctly matched and properly nested.

Valid:

```text
()[]{}
{[()]}
```

Invalid:

```text
([)]
((()
```

---

## Diagram in Words

Input:

```text
{ [ ( ) ] }
```

Process opening brackets:

```text
Stack: {
Stack: { [
Stack: { [ (
```

When `)` appears, it must match the top:

```text
Stack top: (
```

Pop it.

Then `]` must match `[`, and `}` must match `{`.

At the end, the stack must be empty.

---

## Python Solution

```python
def is_balanced(expression: str) -> bool:
    """
    Return True if (), [], and {} are correctly balanced.
    """

    stack: list[str] = []

    # Map every closing bracket to its required opening bracket.
    matching_opening = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    for character in expression:
        if character in "([{":
            # Opening brackets wait for a future closing bracket.
            stack.append(character)

        elif character in matching_opening:
            # A closing bracket cannot be valid if no opening bracket exists.
            if not stack:
                return False

            # The most recent opening bracket must match this closer.
            opening = stack.pop()

            if opening != matching_opening[character]:
                return False

    # An empty stack means every opening bracket was matched.
    return len(stack) == 0
```

---

## Complexity

* Time: **O(n)**
* Extra space: **O(n)** in the worst case

Worst-case input:

```text
(((((((((
```

Every character is stored in the stack.

---

## Tricky Parts

### 1. Check before popping

Incorrect:

```python
opening = stack.pop()
```

This raises an error when the stack is empty.

Correct:

```python
if not stack:
    return False
```

### 2. Stack must be empty at the end

Input:

```text
(((
```

No mismatch occurred during scanning, but it is still invalid.

### 3. Match bracket types

The total number of opening and closing brackets is not enough.

```text
([)]
```

has equal counts but incorrect nesting.

---

## Practical AI and Backend Use Cases

### 1. Validating structured model output

An LLM may produce:

* JSON
* Tool-call arguments
* Nested expressions
* Template syntax

A stack helps validate nested delimiters.

### 2. Parsing prompts or templates

Stacks can track nested placeholders such as:

```text
{{ user_input }}
```

### 3. Agent execution history

A workflow can push nested actions onto a stack and unwind them during:

* Error recovery
* Rollback
* Debugging

### 4. Undo behavior

Prompt editors or workflow builders may maintain an undo stack.

---

# Monotonic Stack

## Concept

A monotonic stack keeps its values in sorted order while scanning input.

The stack may be:

* Monotonically increasing
* Monotonically decreasing

It is commonly used to find:

* Next greater element
* Previous greater element
* Next smaller element
* Previous smaller element
* Stock span
* Largest rectangle in a histogram
* Daily temperatures

---

## Next Greater Element

For each value, find the first larger value to its right.

Input:

```text
[2, 1, 5, 3, 6]
```

Results:

```text
2 -> 5
1 -> 5
5 -> 6
3 -> 6
6 -> none
```

---

## Intuition

Keep indexes of values that have not yet found a greater element.

When a new larger value appears:

* It resolves one or more values on the stack.
* Pop those indexes.
* Record the current value as their next greater element.

---

## Diagram in Words

Process:

```text
2
Stack: [2]
```

Next value:

```text
1
Stack: [2, 1]
```

Next value:

```text
5
```

Since `5 > 1`, pop `1`.

Since `5 > 2`, pop `2`.

Now:

```text
Stack: [5]
```

One new value may resolve several previous values.

---

## Python Solution

```python
from typing import List


def next_greater_elements(numbers: List[int]) -> List[int]:
    """
    For each number, return the first greater number to its right.

    Return -1 when no greater value exists.
    """

    result = [-1] * len(numbers)

    # Store indexes rather than values.
    #
    # Indexes allow us to write the answer into the correct position.
    stack: list[int] = []

    for current_index, current_value in enumerate(numbers):
        # The current value is the next greater value for every
        # smaller unresolved value on top of the stack.
        while (
            stack
            and numbers[stack[-1]] < current_value
        ):
            previous_index = stack.pop()
            result[previous_index] = current_value

        # This value now waits for a greater value in the future.
        stack.append(current_index)

    # Any indexes still in the stack have no greater value to their right.
    return result
```

---

## Complexity

* Time: **O(n)**
* Extra space: **O(n)**

Although there is a nested `while` loop, each index:

* Is pushed once.
* Is popped at most once.

Therefore, the total work is linear.

---

## Why Store Indexes?

Suppose the array contains duplicate values:

```text
[2, 2, 3]
```

Indexes let us identify the exact result position.

Indexes are also necessary when the answer is a distance, such as:

```text
How many days until a warmer temperature?
```

---

## Practical Use Cases of Monotonic Stacks

### 1. Latency threshold analysis

For each request latency, find the next future request with higher latency.

### 2. Resource monitoring

For each GPU utilization sample, find the next sample exceeding it.

### 3. Queue-pressure analysis

For every queue-depth measurement, determine when a higher queue depth next occurs.

### 4. Token-usage spikes

For each LLM request, find the next request with a larger token count.

---

## How to Recognize Stack Problems

Look for:

* Nested structures
* Matching open and close symbols
* Most recent unresolved item
* Undo or backtracking
* “Next greater”
* “Previous smaller”
* Expression evaluation
* Processing values in reverse dependency order

---

## Common Stack Pitfalls

### Pitfall 1: Not checking whether the stack is empty

Always check before using:

```python
stack[-1]
stack.pop()
```

### Pitfall 2: Storing values when indexes are needed

Store indexes when you need:

* Original positions
* Distances
* Result assignment
* Duplicate-value handling

### Pitfall 3: Choosing the wrong monotonic direction

For next-greater-element problems, the unresolved stack is commonly decreasing.

For next-smaller-element problems, it is commonly increasing.

### Pitfall 4: Thinking the nested loop makes it O(n²)

Each element is pushed and popped at most once.

---

# Part 4: Queue

## Concept

A queue follows:

```text
First In, First Out
```

The earliest inserted item is the first one removed.

Think of people waiting in line:

```text
Front                              Back
Request A -> Request B -> Request C
```

`Request A` is processed first.

---

## Basic Queue Operations

In Python, use `collections.deque`.

```python
from collections import deque

queue = deque()

queue.append("request-1")     # Add to back
queue.append("request-2")

first = queue[0]              # Peek at front
processed = queue.popleft()   # Remove from front
```

Operations are generally **O(1)**.

---

## Why Not Use `list.pop(0)`?

```python
items.pop(0)
```

takes **O(n)** because all remaining elements must shift left.

Use:

```python
queue.popleft()
```

which is **O(1)**.

---

## Common Queue Use Cases

* Request processing
* Task scheduling
* Message buffering
* Breadth-first search
* Streaming pipelines
* Producer-consumer systems
* Retry queues
* Rate limiting
* Agent task orchestration

---

## Example: Simple Request Queue

```python
from collections import deque
from typing import Deque


def process_requests(requests: list[str]) -> list[str]:
    """
    Process requests in the same order they arrived.
    """

    queue: Deque[str] = deque(requests)
    processed: list[str] = []

    while queue:
        # popleft() removes the oldest request.
        request = queue.popleft()

        # Real code might call a model, database, or API here.
        processed.append(f"processed: {request}")

    return processed
```

---

## Practical AI-System Example

An LLM platform may receive requests:

```text
Request 1: Summarize document
Request 2: Generate embedding
Request 3: Run retrieval
```

A queue preserves arrival order.

Workers remove tasks from the front and process them.

Real production systems may use:

* Kafka
* RabbitMQ
* Amazon SQS
* Azure Service Bus
* Google Pub/Sub
* Redis queues

The DSA queue concept is the foundation of these systems.

---

# Queue and Breadth-First Search

A queue is also used for breadth-first search, or BFS.

BFS explores:

1. All items one step away.
2. Then all items two steps away.
3. Then all items three steps away.

This is useful for:

* Shortest paths in unweighted graphs
* Dependency exploration
* Workflow traversal
* Searching connected service relationships
* Multi-step agent planning with bounded depth

---

## Diagram in Words

Suppose:

```text
        A
      /   \
     B     C
    / \     \
   D   E     F
```

BFS visits:

```text
A, B, C, D, E, F
```

Queue behavior:

```text
Start: [A]

Remove A, add B and C:
[B, C]

Remove B, add D and E:
[C, D, E]

Remove C, add F:
[D, E, F]
```

---

# Stack vs Queue

| Property         | Stack              | Queue                |
| ---------------- | ------------------ | -------------------- |
| Ordering         | Last In, First Out | First In, First Out  |
| Add operation    | Push               | Enqueue              |
| Remove operation | Pop                | Dequeue              |
| Remove from      | Top/end            | Front                |
| Common use       | Nested structures  | Ordered processing   |
| Graph traversal  | Depth-first search | Breadth-first search |
| Python structure | `list`             | `collections.deque`  |

---

# Two Pointers vs Sliding Window

These patterns can look similar because both may use `left` and `right`.

## Two Pointers

The pointers usually represent:

* Two values being compared
* Two positions moving independently
* Opposite ends
* Read and write positions

Example:

```text
Find two numbers with target sum.
```

## Sliding Window

The pointers represent the boundaries of one continuous region.

Every element between `left` and `right` belongs to the current window.

Example:

```text
Find the longest substring with no repeated characters.
```

---

# Pattern Recognition Cheat Sheet

## Use Two Pointers When

* The array is sorted.
* You need a pair.
* You compare both ends.
* You need in-place modification.
* You merge sorted sequences.
* You maintain separate read and write positions.

## Use a Fixed Sliding Window When

* The window size is explicitly given.
* You need a rolling sum, count, average, maximum, or minimum.
* The question says “every `k` consecutive elements.”

## Use a Variable Sliding Window When

* You need the longest or shortest contiguous region satisfying a condition.
* The window expands until invalid or valid.
* The question contains “at most,” “minimum length,” or “longest substring.”

## Use a Stack When

* The newest unresolved item must be handled first.
* Structures are nested.
* You need matching pairs.
* You need next-greater or next-smaller information.
* You need undo or backtracking.

## Use a Queue When

* The oldest item must be processed first.
* Tasks must preserve arrival order.
* You are performing breadth-first search.
* You are buffering a stream.
* You are designing producer-consumer processing.

---

# Complexity Summary

| Pattern                 | Typical Time |      Typical Extra Space |
| ----------------------- | -----------: | -----------------------: |
| Two pointers            |         O(n) |                     O(1) |
| Fixed sliding window    |         O(n) |                     O(1) |
| Variable sliding window |         O(n) | O(k) or O(character set) |
| Basic stack operations  |    O(1) each |               O(n) total |
| Balanced parentheses    |         O(n) |                     O(n) |
| Monotonic stack         |         O(n) |                     O(n) |
| Basic queue operations  |    O(1) each |               O(n) total |
| BFS with queue          |     O(V + E) |                     O(V) |

---

# Common Interview Mistakes

## 1. Starting with code before defining the invariant

An invariant is a condition that remains true during the algorithm.

Examples:

* Two-sum: all discarded pairs cannot reach the target.
* Unique substring: the window always contains unique characters.
* Balanced brackets: the stack contains unmatched opening brackets.
* Monotonic stack: stack values remain in monotonic order.

Explain the invariant before coding.

---

## 2. Forgetting edge cases

Always consider:

* Empty input
* One element
* Window size zero
* Window larger than input
* Duplicate values
* No valid answer
* All values equal
* Already valid or already sorted input

---

## 3. Using the wrong data structure in Python

Use:

```python
list.append()
list.pop()
```

for a stack.

Use:

```python
deque.append()
deque.popleft()
```

for a queue.

---

## 4. Miscalculating inclusive boundaries

For a window including both `left` and `right`:

```python
length = right - left + 1
```

---

## 5. Not explaining why the algorithm is O(n)

For sliding windows and monotonic stacks, explain amortized behavior:

* Each element enters once.
* Each element leaves once.
* Total work remains linear.

---

# Interview Q&A

## Question 1: Why does two-sum on a sorted array work with two pointers?

Because the input is ordered. If the current sum is too small, moving the left pointer right increases the sum. If it is too large, moving the right pointer left decreases the sum.

Time complexity is O(n).

---

## Question 2: Can two pointers solve two-sum on an unsorted array?

Not directly with the standard inward-pointer technique.

Options include:

* Use a hash map in O(n) time.
* Sort the array and use two pointers in O(n log n), while preserving original indexes if required.

---

## Question 3: What is the difference between a fixed and variable sliding window?

A fixed window always has a predefined size, such as `k`.

A variable window grows and shrinks according to a condition, such as no duplicates or sum at least a target.

---

## Question 4: Why can a sliding-window algorithm with a nested `while` loop still be O(n)?

Because each element enters the window once and leaves the window at most once. The total number of pointer movements is linear.

---

## Question 5: When does a sum-based variable sliding window fail?

It may fail when negative numbers exist.

With negative values:

* Expanding the window may decrease the sum.
* Shrinking the window may increase the sum.

The algorithm loses its predictable monotonic behavior.

---

## Question 6: Why is a stack appropriate for balanced parentheses?

A closing bracket must match the most recently unmatched opening bracket. This is exactly Last In, First Out behavior.

---

## Question 7: What is a monotonic stack?

It is a stack maintained in increasing or decreasing order while scanning input.

It helps solve next-greater, next-smaller, stock-span, histogram, and temperature problems in O(n) time.

---

## Question 8: Why do monotonic-stack solutions often store indexes instead of values?

Indexes allow us to:

* Update the correct result position.
* Calculate distance.
* Handle duplicate values.
* Access both the value and its original location.

---

## Question 9: Why should a Python queue use `deque` instead of a list?

Removing from the front of a list with `pop(0)` takes O(n) because elements shift.

`deque.popleft()` takes O(1).

---

## Question 10: What is the difference between stack-based DFS and queue-based BFS?

DFS explores one branch deeply before backtracking and commonly uses a stack.

BFS explores level by level and uses a queue.

For an unweighted graph, BFS can find the shortest path by number of edges.

---

# Practice Questions with Concise Solutions

## 1. Valid Palindrome

Determine whether a string reads the same forward and backward.

Recommended pattern: **Inward two pointers**

Complexity:

* Time: O(n)
* Space: O(1)

---

## 2. Two-Sum in a Sorted Array

Find two values whose sum equals a target.

Recommended pattern: **Inward two pointers**

Complexity:

* Time: O(n)
* Space: O(1)

---

## 3. Remove Duplicates from a Sorted Array

Modify the array in place so each value appears once.

Recommended pattern: **Read/write pointers**

Complexity:

* Time: O(n)
* Space: O(1)

---

## 4. Maximum Sum of a Subarray of Size `k`

Recommended pattern: **Fixed sliding window**

Complexity:

* Time: O(n)
* Space: O(1)

---

## 5. Longest Substring Without Repeating Characters

Recommended pattern: **Variable sliding window with a set or dictionary**

Complexity:

* Time: O(n)
* Space: O(character set)

---

## 6. Minimum Size Subarray Sum

Given positive integers, find the shortest contiguous subarray whose sum is at least a target.

Recommended pattern: **Variable sliding window**

Complexity:

* Time: O(n)
* Space: O(1)

---

## 7. Valid Parentheses

Recommended pattern: **Stack**

Complexity:

* Time: O(n)
* Space: O(n)

---

## 8. Next Greater Element

Recommended pattern: **Monotonic decreasing stack**

Complexity:

* Time: O(n)
* Space: O(n)

---

## 9. Process Tasks in Arrival Order

Recommended pattern: **Queue**

Complexity:

* Enqueue: O(1)
* Dequeue: O(1)

Use `collections.deque` in Python.

---

# Final Memory Aid

Remember:

```text
PAIR or BOTH ENDS
    -> Two pointers

CONTIGUOUS RANGE
    -> Sliding window

MOST RECENT UNRESOLVED ITEM
    -> Stack

OLDEST WAITING ITEM
    -> Queue

NEXT GREATER OR NEXT SMALLER
    -> Monotonic stack
```

A compact mental model:

```text
Two pointers = compare or reorganize positions

Sliding window = maintain a continuous region

Stack = resolve the newest unfinished item first

Queue = process the oldest waiting item first
```
