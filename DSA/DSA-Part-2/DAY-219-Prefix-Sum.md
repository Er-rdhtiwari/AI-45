# Day 219 — Prefix Sum

Today’s connection is:

> **Sliding window helps when a contiguous range is moving. Prefix sum helps when you need to answer many range-sum questions quickly.**

Suppose:

```python
nums = [2, 4, 1, 3, 5]
```

Someone asks:

```text
What is the sum from index 1 to index 3?
```

You could calculate:

```text
4 + 1 + 3 = 8
```

Easy.

But imagine they ask **100,000 different range-sum questions** on the same array.

Repeatedly looping through each range becomes expensive.

Prefix sum says:

> Do some work once at the beginning, then answer each range query very quickly.

---

# 1. First Idea: Running Sum

Before prefix arrays, understand a **running sum**.

Given:

```python
nums = [2, 4, 1, 3]
```

Start:

```python
running_sum = 0
```

Process elements one by one.

```text
Read 2:
running_sum = 0 + 2 = 2

Read 4:
running_sum = 2 + 4 = 6

Read 1:
running_sum = 6 + 1 = 7

Read 3:
running_sum = 7 + 3 = 10
```

Python:

```python
nums = [2, 4, 1, 3]

running_sum = 0

for num in nums:
    running_sum += num
    print(running_sum)
```

Output:

```text
2
6
7
10
```

This gives us the basic idea behind prefix sums.

---

# 2. What Is a Prefix Sum?

A **prefix sum** stores:

> The sum of everything from the beginning of the array up to a certain point.

Given:

```python
nums = [2, 4, 1, 3, 5]
```

We could create:

```text
prefix = [2, 6, 7, 10, 15]
```

Meaning:

```text
prefix[0] = 2

prefix[1] = 2 + 4
          = 6

prefix[2] = 2 + 4 + 1
          = 7

prefix[3] = 2 + 4 + 1 + 3
          = 10

prefix[4] = 2 + 4 + 1 + 3 + 5
          = 15
```

So:

```text
nums:    [2, 4, 1, 3, 5]
prefix:  [2, 6, 7,10,15]
```

---

# 3. Building a Prefix Array Step by Step

Let's build:

```python
nums = [3, 1, 4, 2, 5]
```

Start:

```python
prefix = []
running_sum = 0
```

Process `3`.

```text
running_sum = 3

prefix = [3]
```

Process `1`.

```text
running_sum = 4

prefix = [3, 4]
```

Process `4`.

```text
running_sum = 8

prefix = [3, 4, 8]
```

Process `2`.

```text
running_sum = 10

prefix = [3, 4, 8, 10]
```

Process `5`.

```text
running_sum = 15

prefix = [3, 4, 8, 10, 15]
```

Python:

```python
nums = [3, 1, 4, 2, 5]

prefix = []
running_sum = 0

for num in nums:
    running_sum += num
    prefix.append(running_sum)

print(prefix)
```

Output:

```python
[3, 4, 8, 10, 15]
```

Time complexity:

```text
O(n)
```

Space complexity:

```text
O(n)
```

---

# 4. Another Common Prefix-Sum Style

There's another version that I recommend learning because it makes range queries cleaner.

Instead of:

```text
prefix length = n
```

we create:

```text
prefix length = n + 1
```

Given:

```python
nums = [3, 1, 4, 2, 5]
```

Create:

```text
prefix = [0, 3, 4, 8, 10, 15]
```

Notice the leading `0`.

Meaning:

```text
prefix[0] = sum of first 0 elements = 0
prefix[1] = sum of first 1 element
prefix[2] = sum of first 2 elements
prefix[3] = sum of first 3 elements
...
```

This definition is extremely useful:

```text
prefix[i] = sum of elements BEFORE index i
```

For example:

```text
nums:

index     0   1   2   3   4
         [3,  1,  4,  2,  5]


prefix:

index     0   1   2   3   4   5
         [0,  3,  4,  8, 10, 15]
```

Python:

```python
nums = [3, 1, 4, 2, 5]

prefix = [0]

for num in nums:
    prefix.append(prefix[-1] + num)

print(prefix)
```

Output:

```python
[0, 3, 4, 8, 10, 15]
```

For today's lesson, we'll mainly use this **`n + 1` version** because it avoids many boundary problems.

---

# 5. Range Sum

Now comes the important part.

Suppose:

```python
nums = [3, 1, 4, 2, 5]
```

We want:

```text
sum from index 1 through index 3
```

That means:

```text
nums[1] + nums[2] + nums[3]
```

or:

```text
1 + 4 + 2 = 7
```

Our prefix array is:

```text
prefix = [0, 3, 4, 8, 10, 15]
```

Look at:

```text
prefix[4] = 10
```

That represents:

```text
3 + 1 + 4 + 2
```

But we don't want the `3` before index `1`.

So subtract:

```text
prefix[1] = 3
```

Therefore:

```text
10 - 3 = 7
```

The formula is:

```python
range_sum = prefix[right + 1] - prefix[left]
```

This is one of the main formulas to remember from today.

---

# 6. Why Does the Formula Work?

Suppose:

```text
nums = [3, 1, 4, 2, 5]
```

We want:

```text
left = 1
right = 3
```

We need:

```text
1 + 4 + 2
```

Now:

```text
prefix[right + 1]
```

means:

```text
prefix[4]
```

which contains:

```text
3 + 1 + 4 + 2
```

Then:

```text
prefix[left]
```

means:

```text
prefix[1]
```

which contains:

```text
3
```

Subtract:

```text
(3 + 1 + 4 + 2)
-
(3)
=
1 + 4 + 2
```

Therefore:

```python
prefix[right + 1] - prefix[left]
```

isolates exactly the range we want.

---

# 7. Visual Way to Understand It

Imagine:

```text
nums = [3, 1, 4, 2, 5]

       └─────────────┘
       prefix[right + 1]

       [3, 1, 4, 2]

        remove
       ┌─┐
       [3]

Result:

          [1, 4, 2]
```

We're essentially saying:

```text
sum from beginning to right
-
sum before left
=
sum from left to right
```

---

# 8. Preprocessing

Creating the prefix array before answering queries is called:

> **Preprocessing**

For example:

```python
nums = [3, 1, 4, 2, 5]
```

First preprocess:

```python
prefix = [0]

for num in nums:
    prefix.append(prefix[-1] + num)
```

That costs:

```text
O(n)
```

But once we have it, a query like:

```text
sum from index 1 to 3
```

becomes:

```python
prefix[4] - prefix[1]
```

That's only a couple of operations.

So one range query becomes:

```text
O(1)
```

---

# 9. Why Preprocessing Helps

Imagine an array has:

```text
n = 100,000
```

elements.

And you receive:

```text
100,000 range queries
```

Without prefix sums, each query might scan many elements.

Worst case:

```text
O(n) per query
```

For `q` queries:

```text
O(n × q)
```

If:

```text
n = 100,000
q = 100,000
```

that could become roughly:

```text
10,000,000,000 operations
```

With prefix sums:

```text
Build prefix:
O(n)

Each query:
O(1)

q queries:
O(q)
```

Total:

```text
O(n + q)
```

That's the power of preprocessing.

---

# 10. Repeated Loops vs Prefix Sum

Suppose:

```python
nums = [3, 1, 4, 2, 5]
```

Queries:

```text
sum(0, 2)
sum(1, 3)
sum(2, 4)
```

Without prefix sums:

```python
sum(nums[0:3])
sum(nums[1:4])
sum(nums[2:5])
```

We're repeatedly visiting elements.

With prefix sums, preprocess once:

```python
prefix = [0, 3, 4, 8, 10, 15]
```

Then:

```python
prefix[3] - prefix[0]
prefix[4] - prefix[1]
prefix[5] - prefix[2]
```

Each query is constant-time.

| Approach | Preprocessing | Each Query | `q` Queries |
|---|---:|---:|---:|
| Repeated loop | O(1) | O(n) worst case | O(nq) |
| Prefix sum | O(n) | O(1) | O(n + q) |

Prefix sum makes sense when:

> The array stays mostly unchanged and we need many range queries.

---

# 11. Important Boundary Cases

This is where beginners commonly make mistakes.

Suppose:

```python
nums = [2, 4, 1, 3]
prefix = [0, 2, 6, 7, 10]
```

## Range starts at index 0

We want:

```text
sum index 0 to 2
```

Answer:

```python
prefix[2 + 1] - prefix[0]
```

```text
prefix[3] - prefix[0]
= 7 - 0
= 7
```

Works perfectly.

That's one major reason the extra leading zero is useful.

---

## Single element

Want:

```text
index 2 to 2
```

Formula:

```python
prefix[3] - prefix[2]
```

```text
7 - 6 = 1
```

Correct.

---

## Entire array

Want:

```text
index 0 to 3
```

Formula:

```python
prefix[4] - prefix[0]
```

```text
10 - 0 = 10
```

Correct.

---

## Last element

Want:

```text
index 3 to 3
```

Formula:

```python
prefix[4] - prefix[3]
```

```text
10 - 7 = 3
```

Correct.

---

# 12. Common Off-by-One Mistake

This is probably the biggest prefix-sum bug.

Suppose:

```python
nums = [3, 1, 4, 2, 5]
```

You want:

```text
left = 1
right = 3
```

Correct formula:

```python
prefix[right + 1] - prefix[left]
```

So:

```python
prefix[4] - prefix[1]
```

But beginners often write:

```python
prefix[right] - prefix[left]
```

That would be:

```python
prefix[3] - prefix[1]
```

which represents only:

```text
nums[1] + nums[2]
```

It misses:

```text
nums[3]
```

Why?

Because `prefix[i]` means:

> sum of elements before index `i`.

So to include `right`, you need:

```text
right + 1
```

---

# 13. A Helpful Interpretation

Instead of memorizing strange indexes, memorize this sentence:

```text
prefix[i] = sum of the first i elements
```

Then:

```text
prefix[right + 1]
```

means:

> sum of all elements up through `right`.

And:

```text
prefix[left]
```

means:

> sum of everything before `left`.

Therefore:

```python
prefix[right + 1] - prefix[left]
```

---

# 14. Complete Basic Template

```python
nums = [3, 1, 4, 2, 5]

# Build prefix sum
prefix = [0]

for num in nums:
    prefix.append(prefix[-1] + num)

# Example query
left = 1
right = 3

range_sum = prefix[right + 1] - prefix[left]

print(range_sum)
```

Output:

```text
7
```

---

# 15. Building Prefix Sum Using Indexes

You'll also often see:

```python
nums = [3, 1, 4, 2, 5]

prefix = [0] * (len(nums) + 1)

for i in range(len(nums)):
    prefix[i + 1] = prefix[i] + nums[i]

print(prefix)
```

Let's understand one line:

```python
prefix[i + 1] = prefix[i] + nums[i]
```

For:

```text
i = 2
```

we calculate:

```python
prefix[3] = prefix[2] + nums[2]
```

Meaning:

```text
sum of first 3 elements
=
sum of first 2 elements
+
third element
```

This form is extremely common in interviews.

---

# 16. Guided Problem

## Range Sum Queries

Given:

```python
nums = [5, 2, 7, 3, 6]
```

Queries:

```text
(0, 2)
(1, 3)
(2, 4)
```

Each pair means:

```text
(left, right)
```

and both indices are inclusive.

Your goal is to answer each range sum efficiently.

Let's build the reasoning together.

### Step A — Create the prefix array

Start:

```python
prefix = [0]
```

For `5`:

```text
prefix = [0, 5]
```

For `2`:

```text
prefix = [0, 5, 7]
```

Continue this yourself.

You should get a prefix array of length:

```text
len(nums) + 1
```

which is:

```text
6
```

### Step B — Query formula

For:

```text
left = 1
right = 3
```

use:

```python
prefix[right + 1] - prefix[left]
```

### Your task

Complete:

```python
def build_prefix(nums):

    prefix = [0]

    for num in nums:
        # complete this

    return prefix


def range_sum(prefix, left, right):

    # complete this
```

Then test:

```python
nums = [5, 2, 7, 3, 6]

queries = [
    (0, 2),
    (1, 3),
    (2, 4)
]
```

For this guided problem, explain:

- preprocessing time complexity
- preprocessing space complexity
- one query's time complexity

---

# 17. Independent Problem 1 — Easy

## Multiple Range Sum Queries

Given:

```python
nums = [2, 6, 3, 8, 5, 1]
```

and:

```python
queries = [
    (0, 3),
    (2, 5),
    (1, 1),
    (0, 5)
]
```

For every query `(left, right)`, return the sum of the inclusive range.

Do not solve each query by repeatedly looping through the requested range.

Your answer should contain:

1. Brute-force reasoning
2. Brute-force time complexity for `q` queries
3. Prefix-sum reasoning
4. Prefix construction
5. Range-sum formula
6. Python code
7. Preprocessing time complexity
8. Query time complexity
9. Overall complexity
10. Space complexity

I won't give you the solution initially.

---

# 18. Independent Problem 2 — Easy / Early Medium

## Find the Pivot Index

Given:

```python
nums = [1, 7, 3, 6, 5, 6]
```

Find an index where:

```text
sum of everything on the left
=
sum of everything on the right
```

For example, if index `i` is the pivot:

```text
left side        i        right side

[ ... ]       nums[i]       [ ... ]

left sum                  right sum
```

The pivot element itself is **not included** in either side.

If no pivot index exists, return:

```python
-1
```

Think about whether prefix-sum information could help you calculate:

```text
left_sum
```

and:

```text
right_sum
```

efficiently.

For your answer, provide:

```text
Brute-force reasoning
Optimized reasoning
Python
Time complexity
Space complexity
```

No solution yet.

---

# 19. Prefix Sum vs Sliding Window

This distinction is worth understanding clearly.

Sliding window usually answers:

```text
"What happens as I move a contiguous region?"
```

For example:

```text
Longest subarray with sum <= k
```

The boundaries move:

```text
left →
right →
```

Prefix sum usually answers:

```text
"What is the sum of this particular range?"
```

For example:

```text
sum from index 20 to 73
```

Prefix sum doesn't need to move a window.

It jumps directly to the answer using:

```python
prefix[right + 1] - prefix[left]
```

---

# 20. Running Sum vs Prefix Sum

A running sum is:

```python
running_sum += num
```

It usually keeps only one accumulated value.

Example:

```text
2 → 6 → 7 → 10
```

A prefix array stores those historical running sums:

```python
prefix = [0, 2, 6, 7, 10]
```

So:

```text
Running sum
    ↓
creates
    ↓
Prefix array
```

The stored history is what allows later range queries.

---

# 21. Typical Prefix-Sum Bugs

The most important mistakes to watch for are:

- forgetting the initial `0`
- creating an array of size `n` when your formula assumes `n + 1`
- using `prefix[right]` instead of `prefix[right + 1]`
- subtracting `prefix[left - 1]` while using the `n + 1` style
- mixing two different prefix-sum conventions
- treating `right` as exclusive when the problem says inclusive
- accessing `nums[right + 1]` instead of `prefix[right + 1]`
- accidentally including the pivot/current element when computing left or right sums

The biggest rule is:

> **Choose one prefix definition and stay consistent.**

For our course, prefer:

```python
prefix[0] = 0
```

and:

```text
prefix[i] = sum of first i elements
```

Then the inclusive range formula is always:

```python
prefix[right + 1] - prefix[left]
```

---

# Day 219 Recognition Signals

When reading an interview problem, think **prefix sum** when you notice something like:

```text
same array
   +
many range queries
```

or:

```text
sum between index L and R
```

or:

```text
sum before this position
sum after this position
```

or:

```text
repeated subarray-sum calculations
```

or:

```text
precompute once
answer many times
```

Your core mental model should be:

```text
Normal approach:

L ───────────── R
loop through everything
O(length of range)


Prefix sum:

prefix[R + 1] - prefix[L]

O(1)
```

And the one formula to remember from **Day 219** is:

```python
range_sum = prefix[right + 1] - prefix[left]
```

Build the prefix array in **O(n)** once, then answer each range-sum query in **O(1)**.