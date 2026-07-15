# Day 5 – DSA Core I: Arrays, Strings, Hashing & Prefix Sums

## 1. The Interview Mental Model

Most array and string problems are not asking you to invent a new algorithm. They are testing whether you recognize a familiar **pattern**.

| Problem signal                     | Likely pattern             |
| ---------------------------------- | -------------------------- |
| “Process every element”            | Traversal                  |
| “Contiguous section”               | Subarray or substring      |
| “Many range-sum queries”           | Prefix sum                 |
| “Count occurrences”                | Frequency dictionary       |
| “Have I seen this before?”         | Set or dictionary          |
| “Find a matching complement”       | Two-sum/hash map           |
| “Same characters with same counts” | Frequency counting/anagram |
| “Count subarrays whose sum is…”    | Prefix sum + hash map      |

A strong interview response usually follows this order:

1. Clarify the input and edge cases.
2. Explain the simple brute-force approach.
3. Identify the repeated work.
4. Choose the appropriate pattern.
5. State time and space complexity.
6. Write and test the code.

---

# 2. Complexity Basics

## Concept: Big-O Time Complexity

Big-O describes how running time grows as the input size `n` grows.

| Complexity   | Typical example          |
| ------------ | ------------------------ |
| `O(1)`       | Accessing `nums[i]`      |
| `O(n)`       | Traversing an array once |
| `O(n log n)` | Sorting                  |
| `O(n²)`      | Comparing every pair     |
| `O(2ⁿ)`      | Generating all subsets   |

### Examples

```python
# O(1): direct access
first_value = nums[0]

# O(n): visit every element once
for value in nums:
    print(value)

# O(n²): inspect every pair
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        print(nums[i], nums[j])
```

## Concept: Space Complexity

Space complexity measures how much additional memory an algorithm uses.

```python
def print_values(nums: list[int]) -> None:
    # Only a small fixed amount of extra memory is used.
    # Extra space: O(1)
    for value in nums:
        print(value)


def copy_values(nums: list[int]) -> list[int]:
    # The new list grows with the input size.
    # Extra space: O(n)
    result = []

    for value in nums:
        result.append(value)

    return result
```

## Important Interview Distinction

Sometimes an algorithm uses:

* `O(n)` input memory
* but only `O(1)` **extra space**

Interviewers usually care about additional memory created by your solution.

## Common Pitfalls

* Assuming two consecutive loops are `O(n²)`.

```python
# O(n), not O(n²), because the loops are consecutive.
for value in nums:
    print(value)

for value in nums:
    print(value * 2)
```

The total is:

```text
O(n) + O(n) = O(2n) = O(n)
```

* Forgetting that slicing creates new data.

```python
substring = text[left:right]
```

Creating this substring generally takes `O(k)` time and space, where `k` is its length.

* Saying hash table operations are always `O(1)`. Dictionary and set lookup are **average-case `O(1)`**.

---

# 3. Arrays and Strings

## Concept: Arrays in Python

Python normally represents dynamic arrays using `list`.

```python
numbers = [10, 20, 30]
```

Array access by index is fast:

```python
value = numbers[1]  # O(1)
```

Searching an unsorted array is generally:

```python
20 in numbers  # O(n)
```

## Concept: Strings in Python

A string is a sequence of characters.

```python
text = "LLM"
```

Strings are **immutable**. You cannot modify an individual character directly.

```python
text = "cat"

# This is invalid:
# text[0] = "b"
```

Instead, you create a new string:

```python
text = "b" + text[1:]  # "bat"
```

Repeated string concatenation inside a loop can be inefficient because each operation may create a new string.

Prefer collecting characters in a list and joining them:

```python
def remove_spaces(text: str) -> str:
    characters: list[str] = []

    for char in text:
        if char != " ":
            characters.append(char)

    # join performs one final string construction.
    return "".join(characters)
```

Time complexity: `O(n)`
Extra space: `O(n)`

---

# 4. Pattern 1: Traversal

## Concept

Traversal means visiting elements one by one.

Use it when you need to:

* Count values
* Find a maximum or minimum
* Validate data
* Transform data
* Search for an element
* Calculate a total

## Example: Count Failed LLM Requests

Suppose each request status is represented as a string.

```python
def count_failed_requests(statuses: list[str]) -> int:
    failed_count = 0

    # Visit each status exactly once.
    for status in statuses:
        if status == "failed":
            failed_count += 1

    return failed_count


statuses = ["success", "failed", "success", "failed"]
print(count_failed_requests(statuses))  # 2
```

### Intuition

Maintain a running count while scanning the array.

### Complexity

* Time: `O(n)`
* Extra space: `O(1)`

## Example: Find the Longest Token

```python
def longest_token(tokens: list[str]) -> str:
    if not tokens:
        # Explicitly handle an empty input.
        return ""

    longest = tokens[0]

    # Start from index 1 because index 0 is already used
    # to initialize the answer.
    for index in range(1, len(tokens)):
        if len(tokens[index]) > len(longest):
            longest = tokens[index]

    return longest
```

### Pitfalls

* Not handling an empty array.
* Starting at the wrong index.
* Accessing `nums[i + 1]` when `i` is already the final index.
* Accidentally using nested loops when one pass is enough.
* Modifying a list while iterating over it.

Bad example:

```python
# Removing items while iterating can cause elements to be skipped.
for value in nums:
    if value < 0:
        nums.remove(value)
```

Safer version:

```python
non_negative = [value for value in nums if value >= 0]
```

---

# 5. Pattern 2: Index-Based Traversal

Use indices when you need:

* The current position
* The previous or next element
* To compare two positions
* To update the array in place

## Example: Detect Adjacent Duplicate Events

```python
def has_adjacent_duplicate(events: list[str]) -> bool:
    # We compare events[index] with events[index - 1].
    # Therefore, begin at index 1.
    for index in range(1, len(events)):
        if events[index] == events[index - 1]:
            return True

    return False
```

### Complexity

* Time: `O(n)`
* Extra space: `O(1)`

## Using `enumerate`

```python
def print_tokens(tokens: list[str]) -> None:
    for index, token in enumerate(tokens):
        print(index, token)
```

`enumerate` is generally cleaner than manually maintaining a counter.

---

# 6. Subarrays and Substrings

## Concept: Subarray

A **subarray** is a contiguous portion of an array.

For:

```python
nums = [1, 2, 3]
```

Some subarrays are:

```text
[1]
[2]
[3]
[1, 2]
[2, 3]
[1, 2, 3]
```

`[1, 3]` is not a subarray because the elements are not contiguous.

## Concept: Substring

A substring is a contiguous portion of a string.

For `"agent"`:

```text
"age"
"gen"
"agent"
```

are substrings.

`"agt"` is not a substring because its characters are not contiguous.

## Subarray vs Subsequence

A subsequence does not have to be contiguous, but it must preserve order.

For `[1, 2, 3]`:

* `[1, 2]` is a subarray and a subsequence.
* `[1, 3]` is a subsequence but not a subarray.
* `[3, 1]` is neither because the order changes.

This distinction is frequently tested.

---

## Example: Generate All Subarrays

```python
def generate_subarrays(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []

    # Choose the starting position.
    for start in range(len(nums)):

        # Choose the ending position.
        # end is inclusive in our conceptual range.
        for end in range(start, len(nums)):

            # Python slicing excludes the right boundary,
            # so use end + 1.
            subarray = nums[start:end + 1]
            result.append(subarray)

    return result
```

### Complexity

There are approximately `n² / 2` subarrays.

* Number of subarrays: `O(n²)`
* Because each slice copies elements, total time can approach `O(n³)`
* Output space can also approach `O(n³)` when storing all copied subarrays

If you only need to process boundaries without copying each subarray, you may avoid slicing.

## How Many Subarrays Exist?

For an array of length `n`:

```text
n × (n + 1) / 2
```

For `n = 3`:

```text
3 × 4 / 2 = 6
```

## Real-System Example

A contiguous range could represent:

* Requests received during a continuous time interval
* Tokens inside a continuous segment of a prompt
* Latency measurements from request `i` through request `j`
* User actions during one continuous session window

## Pitfalls

* Confusing subarray with subsequence.
* Forgetting that Python’s right slice boundary is exclusive.
* Accidentally creating `O(n³)` behavior through repeated slicing and summing.
* Using brute force when the problem can be solved with a prefix sum or sliding window.

---

# 7. Pattern 3: Prefix Sums

## Concept

A prefix sum stores the cumulative total from the beginning of an array.

For:

```python
nums = [2, 4, 1, 3]
```

We create:

```text
prefix = [0, 2, 6, 7, 10]
```

Definition:

```text
prefix[i + 1] = prefix[i] + nums[i]
```

The initial zero makes range calculations easier.

## Why Prefix Sums Matter

Suppose you repeatedly need the sum between indices `left` and `right`.

Without prefix sums, each query may take `O(n)`.

With prefix sums:

```text
range_sum(left, right) = prefix[right + 1] - prefix[left]
```

Each query takes `O(1)`.

---

## Prefix Sum Intuition

For:

```text
nums = [2, 4, 1, 3]
```

To find the sum from index `1` through index `3`:

```text
4 + 1 + 3 = 8
```

`prefix[4]` contains the sum before index `4`:

```text
2 + 4 + 1 + 3 = 10
```

`prefix[1]` contains the sum before index `1`:

```text
2
```

Therefore:

```text
10 - 2 = 8
```

---

## Example: Build Prefix Sums

```python
def build_prefix_sum(nums: list[int]) -> list[int]:
    # The prefix array has one additional element.
    # prefix[0] represents the sum of zero elements.
    prefix = [0] * (len(nums) + 1)

    for index in range(len(nums)):
        # prefix[index] already contains the total
        # of nums[0] through nums[index - 1].
        prefix[index + 1] = prefix[index] + nums[index]

    return prefix
```

## Example: Answer Range-Sum Queries

```python
def range_sum(prefix: list[int], left: int, right: int) -> int:
    """
    Return the sum from left through right, inclusive.

    Example:
        nums = [2, 4, 1, 3]
        left = 1
        right = 3
        answer = 4 + 1 + 3 = 8
    """

    # prefix[right + 1] includes elements through right.
    # prefix[left] includes elements before left.
    return prefix[right + 1] - prefix[left]


nums = [2, 4, 1, 3]
prefix = build_prefix_sum(nums)

print(range_sum(prefix, 1, 3))  # 8
```

### Complexity

Building the prefix array:

* Time: `O(n)`
* Space: `O(n)`

Each query:

* Time: `O(1)`
* Extra space: `O(1)`

For `q` queries:

* Without prefix sum: `O(qn)`
* With prefix sum: `O(n + q)`

---

## Real-System Example: Token Usage Queries

Suppose the number of tokens used by consecutive LLM requests is:

```python
token_usage = [100, 250, 80, 400, 170]
```

You need to answer questions such as:

> How many tokens were consumed by requests 1 through 3?

A prefix sum allows many such queries efficiently.

```python
usage_prefix = build_prefix_sum(token_usage)

# Requests at indices 1, 2, and 3:
print(range_sum(usage_prefix, 1, 3))  # 730
```

## Prefix Sum Pitfalls

### 1. Off-by-One Errors

The most common mistake is using:

```python
prefix[right] - prefix[left]
```

instead of:

```python
prefix[right + 1] - prefix[left]
```

when `right` is inclusive.

### 2. Forgetting the Initial Zero

Without the leading zero, ranges starting at index `0` require special handling.

### 3. Using Prefix Sums for Frequently Updated Arrays

Basic prefix sums work best when the input array is mostly static.

If values change frequently, rebuilding the prefix array costs `O(n)`. More advanced structures such as Fenwick trees or segment trees may be better.

### 4. Integer Overflow

Python integers automatically grow, but languages such as Java or C++ may require 64-bit integers for large totals.

---

# 8. Hashing with Dictionaries and Sets

## Concept

Hashing allows fast lookup based on a key.

Python provides:

* `dict`: stores key-value pairs
* `set`: stores unique values

```python
frequency = {"error": 5, "success": 20}

seen_request_ids = {"req-1", "req-2"}
```

Average-case complexities:

| Operation | Dictionary |    Set |
| --------- | ---------: | -----: |
| Insert    |     `O(1)` | `O(1)` |
| Lookup    |     `O(1)` | `O(1)` |
| Delete    |     `O(1)` | `O(1)` |

## When to Use a Dictionary

Use a dictionary when you need to associate information with a key:

* Character → frequency
* User ID → action count
* Token → number of occurrences
* Number → index
* Request ID → request metadata

## When to Use a Set

Use a set when you only need to know:

* Has this value appeared?
* Is this value unique?
* Does this collection contain the value?

---

# 9. Pattern 4: Frequency Counting

## Concept

A frequency map stores how many times each value appears.

For:

```python
events = ["login", "search", "login", "purchase"]
```

The frequency map is:

```python
{
    "login": 2,
    "search": 1,
    "purchase": 1
}
```

## Example: Count User Actions

```python
def count_actions(actions: list[str]) -> dict[str, int]:
    frequencies: dict[str, int] = {}

    for action in actions:
        if action in frequencies:
            # The action has already appeared.
            frequencies[action] += 1
        else:
            # First occurrence of this action.
            frequencies[action] = 1

    return frequencies
```

Cleaner version using `dict.get`:

```python
def count_actions(actions: list[str]) -> dict[str, int]:
    frequencies: dict[str, int] = {}

    for action in actions:
        # If action does not exist, get returns 0.
        frequencies[action] = frequencies.get(action, 0) + 1

    return frequencies
```

### Complexity

* Time: `O(n)`
* Space: `O(k)`

Here, `k` is the number of distinct actions. In the worst case, `k = n`, so space is `O(n)`.

---

## Example: Count Tokens

```python
def token_frequency(tokens: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}

    for token in tokens:
        # Normalization may be required in a real system.
        normalized_token = token.lower()

        counts[normalized_token] = counts.get(normalized_token, 0) + 1

    return counts


tokens = ["AI", "model", "AI", "RAG"]
print(token_frequency(tokens))
# {'ai': 2, 'model': 1, 'rag': 1}
```

## Real-System Uses

Frequency counting appears in:

* Log analysis
* Token statistics
* User action analytics
* API error categorization
* Detecting hot queries
* Calculating word distributions
* Monitoring repeated tool calls
* Identifying most-used models or endpoints

## Pitfalls

* Forgetting normalization:

```text
"Error", "error", and "ERROR"
```

may need to represent the same category.

* Counting mutable or unhashable objects such as lists.
* Using a list for membership checks, causing `O(n²)` total time.
* Forgetting that dictionary order is not usually relevant to the counting logic.
* Returning the most frequent value without defining tie-breaking behavior.

---

# 10. Pattern 5: Two-Sum Style Lookup

## Problem

Given an array and a target, find two numbers whose sum equals the target.

```text
nums = [2, 7, 11, 15]
target = 9
```

Answer:

```text
2 + 7 = 9
```

## Brute-Force Approach

Check every pair.

```python
def two_sum_brute_force(nums: list[int], target: int) -> list[int]:
    for first in range(len(nums)):
        for second in range(first + 1, len(nums)):
            if nums[first] + nums[second] == target:
                return [first, second]

    return []
```

Complexity:

* Time: `O(n²)`
* Space: `O(1)`

## Optimized Hash-Map Approach

For each value:

```text
required complement = target - current value
```

Ask:

> Have I already seen the complement?

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    # Maps a previously seen number to its index.
    seen: dict[int, int] = {}

    for index, value in enumerate(nums):
        complement = target - value

        # Check before storing the current value.
        # This ensures we do not use the same element twice.
        if complement in seen:
            return [seen[complement], index]

        # Store the current value after checking for its complement.
        seen[value] = index

    # Return an empty list if no pair exists.
    return []
```

### Dry Run

```text
nums = [2, 7, 11, 15], target = 9

value = 2
complement = 7
7 is not in seen
seen = {2: 0}

value = 7
complement = 2
2 is in seen
return [0, 1]
```

### Complexity

* Time: `O(n)` average
* Space: `O(n)`

## Real-System Intuition

Two-sum is not only about adding numbers. It teaches a broader pattern:

> Convert a search for two related values into a lookup for the missing value.

Possible systems examples:

* Match two workloads whose total GPU requirement equals available capacity.
* Find two transaction amounts that produce a target total.
* Match prompt and completion token counts to a quota threshold.
* Find a previously observed event that completes a required pair.

## Pitfalls

### 1. Using the Same Element Twice

For:

```text
nums = [3]
target = 6
```

You cannot use index `0` twice unless the problem explicitly permits it.

Checking before insertion prevents this.

### 2. Returning Values Instead of Indices

Read the problem carefully. Some questions ask for indices; others ask for values.

### 3. Ignoring Duplicate Values

For:

```text
nums = [3, 3]
target = 6
```

The algorithm must return two different indices.

### 4. Sorting Without Considering Original Indices

Sorting can support a two-pointer solution, but it changes index positions unless you preserve them.

---

# 11. Pattern 6: Detecting Duplicates

## Concept

Use a set to remember previously seen values.

```python
def contains_duplicate(values: list[str]) -> bool:
    seen: set[str] = set()

    for value in values:
        if value in seen:
            # The value appeared earlier.
            return True

        seen.add(value)

    return False
```

### Complexity

* Time: `O(n)` average
* Space: `O(n)`

## Alternative: Compare Set Size

```python
def contains_duplicate(values: list[str]) -> bool:
    return len(set(values)) != len(values)
```

This is concise, but the explicit loop is often better during interviews because:

* It demonstrates the pattern clearly.
* It can stop as soon as a duplicate appears.
* It can easily be extended to return the duplicate.

## Example: Find the First Duplicate Request ID

```python
def first_duplicate_request_id(request_ids: list[str]) -> str | None:
    seen: set[str] = set()

    for request_id in request_ids:
        if request_id in seen:
            return request_id

        seen.add(request_id)

    return None
```

## Real-System Uses

* Duplicate event detection
* Request idempotency
* Repeated document IDs during ingestion
* Duplicate chunks in a RAG pipeline
* Duplicate user actions
* Preventing repeated job execution

## Pitfalls

* Using a list instead of a set:

```python
seen = []

for value in values:
    if value in seen:  # O(n) membership test
        return True
    seen.append(value)
```

This may result in `O(n²)` time.

* Assuming that duplicate payloads always have identical raw text. Real systems may require normalization or stable hashes.
* Treating two requests with the same content as duplicates without considering timestamps, users, or idempotency keys.

---

# 12. Pattern 7: Anagram Detection

## Concept

Two strings are anagrams when they contain the same characters with the same frequencies.

Examples:

```text
"listen" and "silent"
"race" and "care"
```

Not anagrams:

```text
"rat" and "car"
"aab" and "abb"
```

Character counts matter, not just character membership.

---

## Approach 1: Sorting

```python
def are_anagrams_sorting(first: str, second: str) -> bool:
    if len(first) != len(second):
        return False

    return sorted(first) == sorted(second)
```

### Complexity

* Time: `O(n log n)`
* Space: typically `O(n)`

## Approach 2: Frequency Dictionary

```python
def are_anagrams(first: str, second: str) -> bool:
    # Strings with different lengths cannot be anagrams.
    if len(first) != len(second):
        return False

    counts: dict[str, int] = {}

    # Count characters in the first string.
    for char in first:
        counts[char] = counts.get(char, 0) + 1

    # Subtract counts using the second string.
    for char in second:
        if char not in counts:
            # The second string contains a character
            # that the first string does not contain.
            return False

        counts[char] -= 1

        if counts[char] < 0:
            # The second string contains this character
            # more times than the first string.
            return False

    # Equal lengths plus no negative counts means that
    # every character frequency matched.
    return True
```

### Complexity

* Time: `O(n)`
* Space: `O(k)`, where `k` is the number of unique characters

## Alternative with `Counter`

```python
from collections import Counter


def are_anagrams(first: str, second: str) -> bool:
    return Counter(first) == Counter(second)
```

This is production-friendly, but an interviewer may ask you to implement the logic manually.

## Real-System Connections

Anagram detection itself may not be common in AI backends, but the underlying pattern is important:

> Two objects are equivalent when their feature counts are equivalent.

The same idea appears in:

* Comparing token distributions
* Detecting reordered event collections
* Verifying that two batches contain the same item counts
* Comparing document term-frequency representations

## Pitfalls

### 1. Checking Only Sets

This is incorrect:

```python
set(first) == set(second)
```

For example:

```text
"aab" and "abb"
```

Both have the set `{"a", "b"}`, but they are not anagrams.

### 2. Ignoring Case and Spaces

Whether these are anagrams depends on the problem definition:

```text
"Listen"
"Silent"
```

You may need normalization:

```python
normalized = "".join(
    char.lower()
    for char in text
    if char.isalnum()
)
```

### 3. Assuming Only English Lowercase Characters

An array of size `26` works only when the input is guaranteed to contain lowercase English letters. A dictionary is safer for general Unicode text.

---

# 13. Combined Pattern: Prefix Sum + Hash Map

This is one of the most important array interview patterns.

## Problem

Count the number of subarrays whose sum equals a target.

```text
nums = [1, 1, 1]
target = 2
```

Valid subarrays:

```text
indices 0–1: [1, 1]
indices 1–2: [1, 1]
```

Answer: `2`

## Key Intuition

Let:

```text
current_prefix = sum from index 0 through current index
```

A previous prefix sum produces a target-sum subarray when:

```text
current_prefix - previous_prefix = target
```

Rearrange:

```text
previous_prefix = current_prefix - target
```

Therefore, at each position, ask:

> How many times have I previously seen `current_prefix - target`?

---

## Example

```python
def count_subarrays_with_sum(nums: list[int], target: int) -> int:
    # prefix_frequency[x] tells us how many times
    # prefix sum x has appeared before the current position.
    #
    # The empty prefix has sum 0. This is necessary to count
    # subarrays that begin at index 0.
    prefix_frequency: dict[int, int] = {0: 1}

    current_prefix = 0
    answer = 0

    for value in nums:
        current_prefix += value

        # We need an earlier prefix whose value is:
        # current_prefix - target
        required_prefix = current_prefix - target

        # Every occurrence of required_prefix creates one valid
        # subarray ending at the current position.
        answer += prefix_frequency.get(required_prefix, 0)

        # Record the current prefix after using earlier prefixes.
        prefix_frequency[current_prefix] = (
            prefix_frequency.get(current_prefix, 0) + 1
        )

    return answer
```

### Complexity

* Time: `O(n)` average
* Space: `O(n)`

## Dry Run

```text
nums = [1, 1, 1], target = 2

Initially:
prefix_frequency = {0: 1}
current_prefix = 0
answer = 0

Read 1:
current_prefix = 1
required = -1
answer = 0
frequency becomes {0: 1, 1: 1}

Read 1:
current_prefix = 2
required = 0
0 appeared once
answer = 1
frequency becomes {0: 1, 1: 1, 2: 1}

Read 1:
current_prefix = 3
required = 1
1 appeared once
answer = 2
```

## Critical Pitfall

Do not replace the frequency dictionary with a set.

The same prefix sum may occur multiple times, and each occurrence may represent a different valid subarray.

This matters especially when the array contains zero or negative values.

---

# 14. Choosing Between Common Approaches

## Array Search

| Requirement                     | Preferred approach       |
| ------------------------------- | ------------------------ |
| Find one value in unsorted data | Linear traversal         |
| Repeated membership checks      | Set                      |
| Preserve associated information | Dictionary               |
| Data is sorted                  | Binary search may apply  |
| Find a pair matching a target   | Hash map or two pointers |

## Range Problems

| Requirement                              | Preferred approach                 |
| ---------------------------------------- | ---------------------------------- |
| One range-sum query                      | Direct traversal may be sufficient |
| Many range-sum queries                   | Prefix sum                         |
| Frequent updates and queries             | Fenwick tree/segment tree          |
| Fixed-size contiguous window             | Sliding window                     |
| Variable window with monotonic condition | Sliding window                     |
| Target-sum subarrays with negatives      | Prefix sum + hash map              |

## Frequency Problems

| Requirement                   | Preferred structure             |
| ----------------------------- | ------------------------------- |
| Only uniqueness matters       | Set                             |
| Counts matter                 | Dictionary/Counter              |
| Need original index           | Dictionary                      |
| Small fixed alphabet          | Fixed-size count array may work |
| General characters or objects | Dictionary                      |

---

# 15. Common Candidate Mistakes

## 1. Coding Before Clarifying

Ask:

* Can the input be empty?
* Are negative numbers possible?
* Are duplicates allowed?
* Should I return indices or values?
* Is the range inclusive?
* Is input case-sensitive?
* Can I modify the input?
* Is there always exactly one answer?

## 2. Giving Complexity Without Explanation

Instead of only saying `O(n)`, explain:

> I traverse the array once, and each dictionary lookup is average-case `O(1)`, so the total average time is `O(n)`.

## 3. Using a Set When Counts Are Needed

A set tracks existence, not frequency.

```python
{"a", "b"}
```

cannot distinguish between `"aab"` and `"abb"`.

## 4. Mishandling Index Boundaries

Common errors:

```python
for i in range(len(nums)):
    print(nums[i + 1])  # Fails at the final index
```

Safer:

```python
for i in range(len(nums) - 1):
    print(nums[i], nums[i + 1])
```

## 5. Ignoring Empty Input

This fails for an empty list:

```python
maximum = nums[0]
```

Check first:

```python
if not nums:
    return None
```

## 6. Accidentally Increasing Complexity

This looks simple but can be `O(n²)`:

```python
for value in nums:
    if value in another_list:
        ...
```

If `another_list` is large and membership is repeated, convert it to a set.

## 7. Overusing Sorting

Sorting changes the input order and costs `O(n log n)`. A hash map may solve the same problem in `O(n)`.

## 8. Not Explaining Space-Time Trade-offs

The optimized two-sum solution uses `O(n)` memory to reduce time from `O(n²)` to `O(n)`.

That trade-off should be stated explicitly.

---

# 16. Interview Problem-Solving Template

Use this verbal structure during interviews:

> “The brute-force approach would compare every possible pair/subarray, which costs `O(n²)`. The repeated work is searching for a previously seen value. I can eliminate that repeated search with a hash map. During one traversal, I store the information needed for future elements. This reduces average time to `O(n)` at the cost of `O(n)` additional space.”

For prefix sums:

> “Because the problem asks for repeated sums over contiguous ranges, I will precompute cumulative sums. The sum from `left` through `right` is `prefix[right + 1] - prefix[left]`. Preprocessing costs `O(n)`, and each query then takes `O(1)`.”

---

# 17. Interview Q&A

## Question 1: What is the difference between a subarray and a subsequence?

**Answer:** A subarray must be contiguous. A subsequence preserves order but may skip elements.

For `[1, 2, 3]`, `[1, 3]` is a subsequence but not a subarray.

---

## Question 2: How would you detect whether an array contains duplicates?

**Answer:** Traverse the array while storing previously seen values in a set. If a value is already in the set, a duplicate exists.

* Time: `O(n)` average
* Space: `O(n)`

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()

    for value in nums:
        if value in seen:
            return True
        seen.add(value)

    return False
```

---

## Question 3: Why is a hash map better than nested loops for two-sum?

**Answer:** Nested loops check every pair and cost `O(n²)`. A hash map lets us check whether the required complement has already appeared in average `O(1)` time, producing an overall average complexity of `O(n)`.

---

## Question 4: How do you answer many subarray-sum queries efficiently?

**Answer:** Build a prefix-sum array in `O(n)`. For an inclusive range `[left, right]`, return:

```python
prefix[right + 1] - prefix[left]
```

Each query then takes `O(1)`.

---

## Question 5: Why does a prefix-sum array often start with zero?

**Answer:** The leading zero represents the sum before the first element. It removes special cases for ranges beginning at index `0` and enables the uniform formula:

```text
prefix[right + 1] - prefix[left]
```

---

## Question 6: How do you check whether two strings are anagrams?

**Answer:** First verify equal lengths, then compare character frequencies using a dictionary or `Counter`.

* Time: `O(n)`
* Space: `O(k)`

Checking only character sets is insufficient because repeated counts matter.

---

## Question 7: Find the first non-repeating character in a string.

**Answer:** Use two passes:

1. Count every character.
2. Traverse the string again and return the first character with count `1`.

```python
def first_unique_character(text: str) -> str | None:
    frequencies: dict[str, int] = {}

    # First pass: count all characters.
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    # Second pass: preserve the original string order.
    for char in text:
        if frequencies[char] == 1:
            return char

    return None
```

* Time: `O(n)`
* Space: `O(k)`

A second traversal is necessary because dictionaries answer frequency questions, while the string determines which unique character appears first.

---

## Question 8: Count subarrays whose sum equals `k`.

**Answer:** Maintain a running prefix sum and a dictionary containing the frequency of previous prefix sums.

At each position, count previous prefixes equal to:

```text
current_prefix - k
```

* Time: `O(n)` average
* Space: `O(n)`

Initialize the frequency dictionary with `{0: 1}` to count subarrays beginning at index `0`.

---

## Question 9: When should you use a set instead of a dictionary?

**Answer:** Use a set when only existence or uniqueness matters. Use a dictionary when you need associated information such as a count, index, timestamp, or metadata.

Examples:

```text
Set: Have I seen this request ID?
Dictionary: At which index did I see this number?
```

---

## Question 10: What is the complexity of generating all subarrays?

**Answer:** There are `n(n + 1) / 2`, or `O(n²)`, possible subarrays.

Enumerating only their boundaries is `O(n²)`. Copying every subarray through slicing can require up to `O(n³)` total time because each slice copies multiple elements.

---

# 18. Mini Practice Problems

Try solving these using the indicated patterns.

| Problem                                        | Main pattern                       |
| ---------------------------------------------- | ---------------------------------- |
| Find the maximum latency                       | Traversal                          |
| Count each API status code                     | Frequency dictionary               |
| Check duplicate request IDs                    | Set                                |
| Return indices of two costs totaling a budget  | Two-sum                            |
| Check whether two token sequences are anagrams | Frequency counting                 |
| Calculate token usage between request indices  | Prefix sum                         |
| Find the first unique event type               | Frequency count + second traversal |
| Count subarrays totaling a quota               | Prefix sum + hash map              |

---

# 19. Final Revision Sheet

## Arrays and Strings

* Traverse once whenever possible.
* Use indices only when positions matter.
* Strings are immutable.
* A subarray/substring is contiguous.
* There are `O(n²)` possible subarrays.

## Prefix Sums

```text
prefix[i + 1] = prefix[i] + nums[i]
```

Inclusive range sum:

```text
prefix[right + 1] - prefix[left]
```

* Build: `O(n)`
* Query: `O(1)`
* Space: `O(n)`

## Dictionary

Use when you need:

* Frequency
* Index
* Associated metadata
* Complement lookup

Average insertion and lookup: `O(1)`.

## Set

Use when you need:

* Membership checking
* Duplicate detection
* Uniqueness

Average insertion and lookup: `O(1)`.

## Two-Sum Pattern

```text
complement = target - current
```

Check whether the complement has already been seen.

* Time: `O(n)`
* Space: `O(n)`

## Anagram Pattern

Same length plus identical character frequencies.

* Sorting: `O(n log n)`
* Hashing: `O(n)`

## Prefix Sum + Hashing

For target-sum subarrays:

```text
required_previous_prefix = current_prefix - target
```

Store prefix **frequencies**, not only unique prefix values.
