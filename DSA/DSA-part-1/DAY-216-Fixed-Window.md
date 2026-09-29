# Day 216 — Fixed Sliding Window

**Connection:** Yesterday, two pointers taught you how to move boundaries through an array. Today, **sliding window** uses those boundaries to maintain a useful **contiguous region** of the array.

The big idea is:

> Instead of recalculating information for every subarray from scratch, keep a window and update only what changed.

For today, we will focus only on **fixed-size sliding windows**.

---

## 1. What is a contiguous subarray?

A **subarray** is a continuous part of an array.

Given:

```python
nums = [1, 2, 3, 4, 5]
```

These are contiguous subarrays:

```text
[1, 2]
[2, 3]
[3, 4, 5]
[1, 2, 3, 4]
```

But this is **not** contiguous:

```text
[1, 3, 5]
```

because we skipped elements.

Sliding window is especially useful when the problem says something like:

> Find something among all **contiguous subarrays of size k**.

---

# 2. What is a window?

Suppose:

```python
nums = [2, 1, 5, 1, 3, 2]
k = 3
```

A window of size `3` means we look at exactly three adjacent elements.

First window:

```text
[2, 1, 5]
```

Second window:

```text
[1, 5, 1]
```

Third:

```text
[5, 1, 3]
```

Fourth:

```text
[1, 3, 2]
```

The window moves one position at a time.

---

# 3. Visualizing sliding window

Start:

```text
Index:   0   1   2   3   4   5
Value:   2   1   5   1   3   2
         └───────┘
          window
```

Window:

```text
[2, 1, 5]
```

Then slide one position:

```text
Index:   0   1   2   3   4   5
Value:   2   1   5   1   3   2
             └───────┘
              window
```

Now:

```text
[1, 5, 1]
```

Notice what happened:

```text
2 left the window
1 entered the window
```

That observation is the key to optimization.

---

# 4. Important sliding-window terms

For:

```text
[2, 1, 5]
```

we can think of:

```text
left  = start of window
right = end of window
```

Example:

```text
Index:   0   1   2
Value:   2   1   5
         ↑       ↑
       left    right
```

Window size:

```text
right - left + 1
```

Here:

```text
2 - 0 + 1 = 3
```

So the window size is `3`.

---

# 5. Fixed-size sliding window

A **fixed-size window** means the window always contains exactly `k` elements.

For:

```python
k = 3
```

the window always has three elements.

It moves:

```text
[0, 1, 2]

then

[1, 2, 3]

then

[2, 3, 4]

then

[3, 4, 5]
```

The size never changes.

---

# 6. First problem — maximum sum of k consecutive elements

Let's use:

```python
nums = [2, 1, 5, 1, 3, 2]
k = 3
```

We want:

> Find the maximum sum among all contiguous subarrays of size `3`.

Possible windows:

```text
[2, 1, 5] → 8
[1, 5, 1] → 7
[5, 1, 3] → 9
[1, 3, 2] → 6
```

Answer:

```text
9
```

from:

```text
[5, 1, 3]
```

---

# 7. Brute-force approach

The simplest approach is:

1. Start every possible window.
2. Recalculate its entire sum.
3. Keep track of the maximum.

Example:

```python
def max_sum_k(nums, k):
    max_sum = float("-inf")

    for i in range(len(nums) - k + 1):
        current_sum = 0

        for j in range(i, i + k):
            current_sum += nums[j]

        if current_sum > max_sum:
            max_sum = current_sum

    return max_sum
```

Let's understand:

```python
for i in range(len(nums) - k + 1):
```

`i` is the starting position of each window.

If:

```text
n = 6
k = 3
```

window starts can be:

```text
0
1
2
3
```

There are:

```text
n - k + 1
```

windows.

---

# 8. Why brute force is wasteful

Look at two neighboring windows:

```text
First:
[2, 1, 5]

Second:
[1, 5, 1]
```

The values:

```text
1, 5
```

are shared.

But brute force recalculates everything.

It calculates:

```text
2 + 1 + 5
```

Then again:

```text
1 + 5 + 1
```

Even though most of the window didn't change.

That's wasteful.

---

# 9. Brute-force complexity

Suppose there are approximately `n` windows.

For every window, we sum `k` elements.

So:

```text
Time Complexity: O(n × k)
```

If `k` becomes similar to `n`, this can approach:

```text
O(n²)
```

Extra space:

```text
O(1)
```

because we don't create another growing data structure.

---

# 10. Optimized sliding-window idea

Instead of recalculating the new window from scratch:

> Start with the previous window sum.

Then:

```text
subtract the value leaving
add the value entering
```

That's the entire sliding-window trick.

Let's see it.

Initial window:

```text
[2, 1, 5]
```

Sum:

```text
8
```

Next window:

```text
[1, 5, 1]
```

Instead of recalculating:

```text
1 + 5 + 1
```

do:

```text
old sum
- outgoing
+ incoming
```

So:

```text
8 - 2 + 1 = 7
```

---

# 11. Add incoming, remove outgoing

Let's visualize:

```text
Old window:
[2, 1, 5]

New window:
   [1, 5, 1]
```

The outgoing value is:

```text
2
```

The incoming value is:

```text
1
```

Therefore:

```python
window_sum = window_sum - outgoing + incoming
```

or:

```python
window_sum -= outgoing
window_sum += incoming
```

This is the core pattern.

---

# 12. Full optimized walkthrough

Given:

```python
nums = [2, 1, 5, 1, 3, 2]
k = 3
```

First calculate:

```text
2 + 1 + 5 = 8
```

So:

```text
window_sum = 8
max_sum = 8
```

Slide once.

Outgoing:

```text
2
```

Incoming:

```text
1
```

New sum:

```text
8 - 2 + 1 = 7
```

So:

```text
max_sum = 8
```

---

Slide again.

Previous window:

```text
[1, 5, 1]
```

Outgoing:

```text
1
```

Incoming:

```text
3
```

New sum:

```text
7 - 1 + 3 = 9
```

Now:

```text
max_sum = 9
```

---

Slide again.

Outgoing:

```text
5
```

Incoming:

```text
2
```

New:

```text
9 - 5 + 2 = 6
```

Final answer:

```text
9
```

---

# 13. Optimized Python solution

```python
def max_sum_k(nums, k):
    if len(nums) < k:
        return None

    window_sum = 0

    for i in range(k):
        window_sum += nums[i]

    max_sum = window_sum

    for right in range(k, len(nums)):
        incoming = nums[right]
        outgoing = nums[right - k]

        window_sum += incoming
        window_sum -= outgoing

        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum
```

Test:

```python
print(max_sum_k([2, 1, 5, 1, 3, 2], 3))
```

Output:

```text
9
```

---

# 14. Understanding `right - k`

This is one of the most important lines:

```python
outgoing = nums[right - k]
```

Suppose:

```text
k = 3
right = 3
```

Then:

```text
right - k = 0
```

So:

```python
nums[0]
```

leaves the window.

That's correct:

```text
Old:
index 0, 1, 2

New:
index 1, 2, 3
```

Index `0` left.

Now if:

```text
right = 4
```

then:

```text
right - k = 1
```

So index `1` leaves.

Pattern:

```text
incoming index = right
outgoing index = right - k
```

---

# 15. Sliding-window complexity

Initial sum:

```text
O(k)
```

Then we slide through the remaining elements once:

```text
O(n - k)
```

Together:

```text
O(k + n - k)
```

which becomes:

```text
O(n)
```

So:

```text
Time Complexity: O(n)
Space Complexity: O(1)
```

Compare:

```text
Brute force:
O(n × k)

Sliding window:
O(n)
```

That's the improvement.

---

# 16. Guided Problem — Maximum average of k elements

## Problem

Given:

```python
nums = [1, 12, -5, -6, 50, 3]
k = 4
```

Find the maximum average of any contiguous subarray of size `4`.

Possible windows:

```text
[1, 12, -5, -6]
[12, -5, -6, 50]
[-5, -6, 50, 3]
```

We could calculate every average, but there's a simpler observation:

> If every window has the same size `k`, the window with the largest sum also has the largest average.

So first find the maximum window sum.

Then:

```text
average = max_sum / k
```

---

# 17. Guided thought process

We need:

```text
exactly k consecutive elements
```

That strongly suggests:

```text
fixed sliding window
```

Maintain:

```text
window_sum
```

For each slide:

```text
remove outgoing
add incoming
```

And track:

```text
max_sum
```

At the end:

```text
return max_sum / k
```

---

# 18. Guided pseudocode

```text
if array size is smaller than k:
    return None

calculate sum of first k elements

set max_sum to that sum

for every remaining element:
    add incoming element
    remove outgoing element

    update max_sum if needed

return max_sum / k
```

---

# 19. Guided Python solution

```python
def max_average(nums, k):
    if len(nums) < k:
        return None

    window_sum = 0

    for i in range(k):
        window_sum += nums[i]

    max_sum = window_sum

    for right in range(k, len(nums)):
        window_sum += nums[right]
        window_sum -= nums[right - k]

        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum / k
```

Test:

```python
print(max_average([1, 12, -5, -6, 50, 3], 4))
```

The maximum window is:

```text
[12, -5, -6, 50]
```

Sum:

```text
51
```

Average:

```text
51 / 4 = 12.75
```

So output:

```text
12.75
```

---

# 20. Independent Problem 1 — Maximum sum of k elements

Now solve this yourself.

Given:

```python
nums = [4, 2, 1, 7, 8, 1, 2, 8, 1, 0]
k = 3
```

Return the largest sum of any contiguous subarray of size `3`.

Write:

```python
def max_window_sum(nums, k):
    # your code
```

Test cases:

```python
print(max_window_sum([4, 2, 1, 7, 8, 1, 2, 8, 1, 0], 3))
# Expected: 16
```

Because:

```text
[1, 7, 8]
```

has sum:

```text
16
```

Also test:

```python
print(max_window_sum([5], 1))
# Expected: 5
```

```python
print(max_window_sum([1, 2, 3], 3))
# Expected: 6
```

```python
print(max_window_sum([1, 2], 3))
# Expected: None
```

For this exercise, do **not** give me only the code. Give me:

```text
1. Thought process
2. Pseudocode
3. Python
4. Time complexity
5. Space complexity
```

I am intentionally not showing the solution.

---

# 21. Independent Problem 2 — Count windows with sum above threshold

## Problem

Given:

```python
nums = [2, 1, 5, 1, 3, 2]
k = 3
threshold = 6
```

Count how many contiguous windows of size `3` have a sum **greater than** `6`.

Windows:

```text
[2, 1, 5]
[1, 5, 1]
[5, 1, 3]
[1, 3, 2]
```

Your job is to calculate the answer.

Write:

```python
def count_windows(nums, k, threshold):
    # your code
```

Test:

```python
print(count_windows([2, 1, 5, 1, 3, 2], 3, 6))
```

Also test:

```python
print(count_windows([1, 2, 3], 1, 1))
```

```python
print(count_windows([1, 2, 3], 3, 5))
```

```python
print(count_windows([1, 2], 3, 5))
# Expected: 0
```

For this problem, return:

```text
0
```

when the array is smaller than `k`.

Again provide:

```text
Thought process
Pseudocode
Python
Time Complexity
Space Complexity
```

No solution yet.

---

# 22. Edge case — `k = 1`

Suppose:

```python
nums = [4, 2, 9]
k = 1
```

Your windows are:

```text
[4]
[2]
[9]
```

Each element forms its own window.

For maximum window sum, the answer is simply the maximum element:

```text
9
```

But your sliding-window code should work naturally without special logic.

Initial:

```text
window_sum = 4
```

Slide:

```text
4 - 4 + 2 = 2
```

Slide:

```text
2 - 2 + 9 = 9
```

Good.

---

# 23. Edge case — `k` equals array length

Suppose:

```python
nums = [1, 2, 3, 4]
k = 4
```

There is exactly one window:

```text
[1, 2, 3, 4]
```

Sum:

```text
10
```

The second sliding loop:

```python
for right in range(k, len(nums)):
```

becomes:

```python
range(4, 4)
```

which runs zero times.

That's fine.

The initial window is already the complete answer.

---

# 24. Edge case — array smaller than `k`

Suppose:

```python
nums = [1, 2]
k = 3
```

Can we create a window containing three consecutive elements?

No.

So you need to decide what the function should return.

For our first problem:

```python
return None
```

For the second counting problem:

```python
return 0
```

In real interview problems, follow the problem statement.

Always check:

```python
if len(nums) < k:
```

when appropriate.

---

# 25. Common mistake — recalculating every window

This:

```python
for i in range(...):
    current_sum = sum(nums[i:i + k])
```

is easy to write, but each:

```python
sum(...)
```

processes `k` elements.

So you lose the main benefit of sliding window.

The whole point is:

```text
Old answer
- outgoing
+ incoming
```

not:

```text
Calculate everything again
```

---

# 26. Common mistake — removing the wrong value

Suppose:

```python
right = 4
k = 3
```

The incoming element is:

```python
nums[4]
```

The outgoing element is:

```python
nums[4 - 3]
```

which is:

```python
nums[1]
```

Correct.

A common mistake is:

```python
nums[right - 1]
```

But that's usually still inside the new window.

Remember:

```text
outgoing index = right - k
```

for this implementation style.

---

# 27. Common mistake — wrong number of initial elements

If:

```python
k = 3
```

the first window should contain exactly:

```text
indices 0, 1, 2
```

So:

```python
for i in range(k):
```

is correct.

This gives:

```text
0
1
2
```

Do not use:

```python
range(k + 1)
```

because that would include four elements.

---

# 28. Common mistake — initializing maximum to zero

Suppose:

```python
nums = [-8, -3, -5]
k = 2
```

Possible sums:

```text
-11
-8
```

The maximum is:

```text
-8
```

But if you do:

```python
max_sum = 0
```

you would incorrectly return:

```text
0
```

even though no window sums to zero.

Better:

```python
max_sum = window_sum
```

after calculating the first real window.

This is the same lesson you learned earlier with minimum/maximum problems.

---

# 29. Common mistake — confusing window size with indexes

If:

```text
left = 2
right = 4
```

the window size is:

```text
right - left + 1
```

So:

```text
4 - 2 + 1 = 3
```

Not:

```text
right - left = 2
```

Why the `+1`?

Because indexes `2`, `3`, and `4` are three positions.

---

# 30. Common mistake — confusing subarray and subsequence

Sliding window is normally about:

```text
contiguous
```

elements.

This:

```text
[1, 2, 3]
```

from neighboring positions is a valid window.

This:

```text
[1, 3, 5]
```

where positions were skipped is not a sliding window.

Strong signal:

> contiguous subarray / substring

---

# 31. Fixed window recognition signals

When you see:

```text
"exactly k elements"
"subarray of size k"
"substring of length k"
"maximum sum of k consecutive values"
"average of every k elements"
"count windows of size k"
```

think:

```text
Fixed Sliding Window
```

Then ask:

> What information can I maintain when the window slides?

For sums:

```text
remove outgoing
add incoming
```

Later you will learn windows maintaining:

```text
character frequencies
counts
maximum/minimum information
distinct values
```

But not today.

---

# 32. Fixed window vs two pointers

Two pointers:

```text
Two indexes move based on some condition.
```

Sliding window:

```text
Those indexes define a contiguous region
whose information we maintain.
```

For fixed window:

```text
the distance between boundaries stays fixed.
```

For example:

```text
L       R
↓       ↓
2 1 5
```

Slide:

```text
  L       R
  ↓       ↓
  1 5 1
```

Both boundaries move together.

---

# 33. Day 216 mental model

Keep this picture in your head:

```text
Previous window:

[A B C]

Slide right:

  [B C D]
```

What changed?

```text
A left
D entered
```

Therefore:

```text
new information
=
old information
- effect of A
+ effect of D
```

For sums:

```python
window_sum -= outgoing
window_sum += incoming
```

This is the core of fixed sliding window.

---

## Day 216 assignment

Solve the two independent problems:

```text
1. Maximum sum of a contiguous subarray of size k
2. Count windows of size k whose sum is greater than a threshold
```

For each, send me:

```text
1. Thought process
2. Pseudocode
3. Python
4. Time Complexity
5. Space Complexity
```

And for the first problem, also answer this in your own words:

> **Why is sliding window O(n), while recalculating every window can be O(n × k)?**

That explanation is the key concept I want you to understand from **Day 216**.