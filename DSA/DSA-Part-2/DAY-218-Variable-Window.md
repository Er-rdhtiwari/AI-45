# Day 218 — Variable Sliding Window

Yesterday, with **fixed sliding window**, the window always had the same length.

```text
Fixed window:
[1, 2, 3] 4 5
   [2, 3, 4] 5
      [3, 4, 5]
```

Today, the window can **grow and shrink dynamically** depending on whether it satisfies a condition.

```text
Variable window:

right expands →
[2]
[2, 1]
[2, 1, 3]
[2, 1, 3, 2]   ← condition fails

left shrinks →
   [1, 3, 2]    ← valid again
```

The central idea is:

> **Expand `right`. If the window becomes invalid, move `left` forward until the window becomes valid again.**

---

# 1. Connection to Fixed Sliding Window

With a fixed window, we knew the size beforehand.

For example:

> Find the maximum sum of any subarray of size `k = 3`.

```python
window_size = 3
```

The window was always exactly 3 elements.

Variable sliding window is different.

For example:

> Find the longest subarray whose sum is at most `7`.

We don't know the correct window size.

It could be:

```text
size 1
size 2
size 3
size 4
...
```

The condition determines the size.

So think:

```text
Fixed Window
------------
size controls window

Variable Window
---------------
condition controls window
```

---

# 2. The Four Main Pieces

A variable sliding window usually looks like this:

```python
left = 0

for right in range(len(nums)):

    # 1. Expand window
    add nums[right]

    # 2. Check condition
    while window is invalid:

        # 3. Shrink window
        remove nums[left]
        left += 1

    # 4. Window is valid here
    update answer
```

The pointers represent:

```text
             right
               ↓
1   4   2   3   5   1
        ↑
       left

Current window = nums[left : right + 1]
```

---

# 3. Expand Right

Usually `right` is controlled by a `for` loop.

```python
for right in range(len(nums)):
```

Every iteration brings a new element into the window.

For a sum problem:

```python
window_sum += nums[right]
```

For a character-frequency problem:

```python
freq[s[right]] += 1
```

For counting zeros:

```python
if nums[right] == 0:
    zero_count += 1
```

You can think:

> `right` explores new possibilities.

---

# 4. Shrink Left

Suppose the condition is:

```text
window sum <= 7
```

and currently:

```text
window = [2, 1, 3, 2]

sum = 8
```

The window is invalid.

So remove elements from the left:

```text
[2, 1, 3, 2]
 ↑
remove 2

[1, 3, 2]

sum = 6
```

Now it is valid.

In code:

```python
while window_sum > 7:
    window_sum -= nums[left]
    left += 1
```

Notice the `while`.

We may need to remove **multiple elements**, not just one.

---

# 5. Window Condition

This is the most important part of recognizing variable sliding window problems.

The problem normally gives you some rule that a contiguous region must satisfy.

Examples:

```text
sum <= k

sum >= target

at most k zeros

at most k distinct characters

no duplicate characters

at most k replacements

product < k
```

That rule is the **window condition**.

For example:

> Longest subarray whose sum is at most 7.

Valid:

```text
[2, 1, 3]

sum = 6
```

Invalid:

```text
[2, 1, 3, 2]

sum = 8
```

Condition:

```python
window_sum <= 7
```

Invalid condition:

```python
window_sum > 7
```

---

# 6. Longest Valid Window

This is probably the most common variable-window pattern.

Question:

> Find the **longest** contiguous region satisfying some condition.

Basic template:

```python
left = 0
answer = 0

for right in range(len(nums)):

    # Add new element

    while window_is_invalid:
        # Remove nums[left]
        left += 1

    answer = max(answer, right - left + 1)
```

The important detail is:

```python
right - left + 1
```

That is the current window length.

Example:

```text
left = 2
right = 5
```

Indices:

```text
2 3 4 5
```

There are four elements.

Therefore:

```python
5 - 2 + 1 = 4
```

---

# 7. Shortest Valid Window

There is another important variation.

Instead of:

> longest window that remains valid

the problem may ask:

> shortest window that achieves something.

Example:

> Find the shortest subarray whose sum is at least `7`.

Suppose:

```text
[2, 3, 1, 4]
```

Once the sum reaches `7` or more, we don't stop.

We try shrinking it.

```text
[2, 3, 1, 4] = 10
```

Try removing `2`:

```text
[3, 1, 4] = 8
```

Still valid.

Try removing `3`:

```text
[1, 4] = 5
```

Invalid.

So `[3,1,4]` was a candidate.

Typical shortest-window structure:

```python
left = 0
answer = float("inf")

for right in range(len(nums)):

    # expand

    while window_is_valid:

        answer = min(answer, right - left + 1)

        # shrink
        left += 1
```

Notice a subtle difference.

### Longest valid window

```python
while window is INVALID:
    shrink

update longest
```

### Shortest valid window

```python
while window is VALID:
    update shortest
    shrink
```

This difference is very important.

---

# 8. How to Recognize Variable Sliding Window

Look for these clues.

### Clue 1 — Contiguous

Words such as:

```text
subarray
substring
consecutive elements
continuous segment
```

Sliding window operates on contiguous regions.

---

### Clue 2 — Longest or shortest

Especially:

```text
longest substring...
longest subarray...
minimum length subarray...
smallest window...
```

These are strong signals.

---

### Clue 3 — There is a condition

For example:

```text
sum <= k
at most k zeros
at most k distinct characters
no duplicates
sum >= target
```

You can maintain that condition while moving the pointers.

---

### Clue 4 — The size isn't fixed

If the problem says:

```text
window size = k
```

that's fixed sliding window.

If it asks:

```text
longest possible
shortest possible
```

the size probably needs to change dynamically.

---

### Clue 5 — Removing from the left can restore validity

Imagine:

```text
[2, 1, 3, 5]
```

Suppose the sum is too large.

Removing elements from the left can make the sum smaller.

That makes sliding window useful.

---

## Important limitation

Sliding window does **not automatically work for every sum problem**.

Suppose numbers can be negative:

```text
[5, -10, 20]
```

Adding another number might make the sum smaller instead of larger.

That destroys the simple monotonic behavior we depend on.

For beginner problems, when you see something like:

> positive integers + longest/shortest subarray + sum constraint

variable sliding window should immediately come to mind.

---

# 9. Detailed Dry Run

Consider:

```python
nums = [2, 1, 3, 2, 4, 1]
k = 7
```

Question:

> Find the length of the longest contiguous subarray whose sum is at most `7`.

We maintain:

```python
left = 0
window_sum = 0
max_length = 0
```

### right = 0

Add:

```python
2
```

Window:

```text
[2]
```

Sum:

```text
2
```

Valid because:

```text
2 <= 7
```

Length:

```text
1
```

Therefore:

```python
max_length = 1
```

---

### right = 1

Add `1`.

```text
[2, 1]
```

Sum:

```text
3
```

Still valid.

Length:

```text
2
```

So:

```python
max_length = 2
```

---

### right = 2

Add `3`.

```text
[2, 1, 3]
```

Sum:

```text
6
```

Valid.

Length:

```text
3
```

So:

```python
max_length = 3
```

---

### right = 3

Add `2`.

```text
[2, 1, 3, 2]
```

Sum:

```text
8
```

But:

```text
8 > 7
```

The window is invalid.

We shrink from the left.

Remove:

```text
2
```

New window:

```text
[1, 3, 2]
```

New sum:

```text
6
```

And:

```text
6 <= 7
```

Valid again.

Pointers are now approximately:

```text
     L
     ↓
[2, 1, 3, 2, 4, 1]
           ↑
           R
```

Current length:

```python
right - left + 1
```

```python
3 - 1 + 1
```

```text
3
```

Maximum remains:

```text
3
```

---

### right = 4

Add `4`.

Current window becomes:

```text
[1, 3, 2, 4]
```

Sum:

```text
10
```

Invalid.

Shrink once.

Remove `1`:

```text
[3, 2, 4]
```

Sum:

```text
9
```

Still invalid!

This is why we need:

```python
while
```

rather than:

```python
if
```

Shrink again.

Remove `3`:

```text
[2, 4]
```

Sum:

```text
6
```

Now valid.

Length:

```text
2
```

Maximum is still `3`.

---

### right = 5

Add `1`.

```text
[2, 4, 1]
```

Sum:

```text
7
```

Valid.

Length:

```text
3
```

Final answer:

```text
3
```

---

# 10. Python Solution for the Dry Run

```python
nums = [2, 1, 3, 2, 4, 1]
k = 7

left = 0
window_sum = 0
max_length = 0

for right in range(len(nums)):

    # Expand the window
    window_sum += nums[right]

    # Shrink until valid again
    while window_sum > k:
        window_sum -= nums[left]
        left += 1

    # Current window is valid
    current_length = right - left + 1
    max_length = max(max_length, current_length)

print(max_length)
```

Output:

```text
3
```

---

# 11. Brute Force vs Sliding Window

For the same problem:

```python
nums = [2, 1, 3, 2, 4, 1]
k = 7
```

Brute force could try every starting point.

```text
start = 0:
[2]
[2,1]
[2,1,3]
[2,1,3,2]
...

start = 1:
[1]
[1,3]
[1,3,2]
...

start = 2:
[3]
[3,2]
...
```

There can be roughly:

```text
n²
```

different subarrays.

So a reasonable brute-force solution is:

```text
Time: O(n²)
```

Sliding window instead lets `right` move forward once and `left` move forward once.

```text
right → → → → → →
left      →   → →
```

Neither needs to restart.

Therefore:

```text
Time: O(n)
Space: O(1)
```

for the sum example.

---

# 12. Why Doesn't `left` Usually Move Backward?

This is one of the most important insights.

Suppose:

```text
[2, 1, 3, 2]
```

is invalid because:

```text
sum = 8 > 7
```

We remove `2`:

```text
[1, 3, 2]
```

Now the left pointer moves from:

```text
0 → 1
```

Why don't we later move it back to `0`?

Because we've already processed windows starting there.

Under the conditions where sliding window works, once that old starting position can no longer be part of the current valid window, we don't need to reconsider it for this `right`.

And future `right` values move even farther right.

So pointers move:

```text
left  → → → →
right → → → →
```

not:

```text
left → ← → ← → ←
```

That is what makes sliding window efficient.

Another way to understand the complexity:

Each element is:

```text
added to the window at most once
removed from the window at most once
```

So although there is a `while` loop inside a `for` loop, the algorithm is normally **O(n)**, not O(n²).

---

# 13. Longest-Window Template

A useful beginner template:

```python
left = 0
answer = 0

for right in range(len(nums)):

    # Add nums[right] to window

    while window_is_invalid:

        # Remove nums[left]
        left += 1

    answer = max(answer, right - left + 1)

return answer
```

Memorize the idea rather than memorizing the exact code:

```text
EXPAND
   ↓
INVALID?
   ↓ yes
SHRINK
   ↓
VALID
   ↓
UPDATE ANSWER
```

---

# 14. Shortest-Window Template

For shortest valid windows:

```python
left = 0
answer = float("inf")

for right in range(len(nums)):

    # Add nums[right]

    while window_is_valid:

        answer = min(
            answer,
            right - left + 1
        )

        # Remove nums[left]
        left += 1
```

Mental model:

```text
Expand until valid
        ↓
Window valid
        ↓
Record answer
        ↓
Shrink
        ↓
Still valid?
   yes ↙   ↘ no
 shrink    expand again
```

---

# 15. Typical Bugs When Shrinking

### Bug 1 — Using `if` instead of `while`

Wrong:

```python
if window_sum > k:
    window_sum -= nums[left]
    left += 1
```

What if removing one element isn't enough?

Example:

```text
[1, 3, 2, 4]
sum = 10
k = 7
```

Remove `1`:

```text
[3,2,4]

sum = 9
```

Still invalid.

So use:

```python
while window_sum > k:
```

---

### Bug 2 — Moving `left` before removing its value

Wrong:

```python
left += 1
window_sum -= nums[left]
```

Now you're removing the wrong element.

Correct:

```python
window_sum -= nums[left]
left += 1
```

Think:

```text
remove old left
then move left
```

---

### Bug 3 — Updating the longest answer before restoring validity

Wrong:

```python
window_sum += nums[right]

max_length = max(max_length, right - left + 1)

while window_sum > k:
    ...
```

You may accidentally count an invalid window.

Usually:

```python
while invalid:
    shrink

max_length = max(...)
```

---

### Bug 4 — Forgetting `+1`

Wrong:

```python
right - left
```

Correct:

```python
right - left + 1
```

---

### Bug 5 — Forgetting to update window state while shrinking

For example:

```python
while window_sum > k:
    left += 1
```

The sum never changes.

You need:

```python
while window_sum > k:
    window_sum -= nums[left]
    left += 1
```

---

### Bug 6 — Frequency count isn't updated

For string problems, suppose you maintain:

```python
freq[char]
```

When shrinking, you must decrease the departing character:

```python
freq[s[left]] -= 1
left += 1
```

Sometimes you should also remove counts that become zero:

```python
if freq[s[left]] == 0:
    del freq[s[left]]
```

This becomes especially important for problems involving **distinct characters**.

---

# 16. Guided Problem

Let's solve this one together, but **you write the solution first**.

## Problem — Longest Sequence with At Most `k` Zeros

Given:

```python
nums = [1, 1, 0, 0, 1, 1, 1, 0]
k = 2
```

Find the longest contiguous subarray containing **at most 2 zeros**.

You can imagine that you're allowed to convert at most two zeros into ones.

Example window:

```text
[1, 1, 0, 0, 1, 1, 1]
```

Zeros:

```text
2
```

So this window is valid.

### Step 1: What does the window need to track?

We don't really care about the sum.

We need:

```python
zero_count
```

### Step 2: When does `right` expand?

Every iteration:

```python
for right in range(len(nums)):
```

If:

```python
nums[right] == 0
```

increase:

```python
zero_count
```

### Step 3: What's the invalid condition?

The rule says:

```text
at most k zeros
```

So invalid means:

```python
zero_count > k
```

### Step 4: What happens while shrinking?

Look at:

```python
nums[left]
```

If the element leaving the window is a zero, what should happen to `zero_count`?

Then move:

```python
left += 1
```

### Step 5: When do we calculate the answer?

Only once:

```text
zero_count <= k
```

again.

Then:

```python
current_length = right - left + 1
```

Your skeleton:

```python
def longest_ones(nums, k):

    left = 0
    zero_count = 0
    max_length = 0

    for right in range(len(nums)):

        # TODO:
        # What happens if nums[right] == 0?


        while __________:

            # TODO:
            # If nums[left] is zero,
            # update zero_count


            left += 1

        # TODO:
        # calculate current window length


        # TODO:
        # update max_length


    return max_length
```

For:

```python
nums = [1, 1, 0, 0, 1, 1, 1, 0]
k = 2
```

Work out the expected answer manually first.

For this guided problem, send me:

1. Your invalid-window condition.
2. Completed Python code.
3. Time complexity.
4. Space complexity.

---

# 17. Independent Problem 1 — Easy

## Longest Subarray With Sum ≤ `k`

Given an array of **positive integers**:

```python
nums = [1, 2, 1, 1, 3, 1, 1]
k = 5
```

Return the length of the longest contiguous subarray whose sum is at most `k`.

Do not just give me code.

Your answer should include:

```text
1. Brute-force reasoning
2. Brute-force complexity
3. Optimized reasoning
4. Window condition
5. Pseudocode
6. Python code
7. Time complexity
8. Space complexity
```

I am intentionally not giving you the solution yet.

---

# 18. Independent Problem 2 — Early Medium

## Minimum Size Subarray Sum

Given:

```python
nums = [2, 3, 1, 2, 4, 3]
target = 7
```

Find the **minimum length** of a contiguous subarray whose sum is at least `target`.

For example, you're looking for something satisfying:

```text
sum >= 7
```

But among all such windows, return the shortest length.

Again, provide:

```text
1. Brute-force reasoning
2. Brute-force complexity
3. Optimized reasoning
4. Window condition
5. Explain when you expand
6. Explain when you shrink
7. Pseudocode
8. Python
9. Time complexity
10. Space complexity
```

Pay special attention here:

> This is a **shortest valid window**, so think carefully about whether you shrink when the window is invalid or when it is already valid.

I won't reveal the answer until you attempt it.

---

# Day 218 Recognition Cheat Sheet

```text
VARIABLE SLIDING WINDOW
=======================

Question mentions:
    subarray / substring / contiguous
                 +
       longest / shortest
                 +
            a condition
                 ↓
      Think Sliding Window


LONGEST VALID WINDOW
--------------------

right expands

while window INVALID:
    remove left
    left += 1

answer = max(
    answer,
    right - left + 1
)


SHORTEST VALID WINDOW
---------------------

right expands

while window VALID:
    answer = min(
        answer,
        right - left + 1
    )

    remove left
    left += 1


COMMON CONDITIONS
-----------------

sum <= k
sum >= target
zeros <= k
distinct chars <= k
duplicates == 0


POINTER JOBS
------------

right = explore / expand

left = repair / shrink


KEY COMPLEXITY IDEA
-------------------

right moves forward at most n times
left moves forward at most n times

Total ≈ 2n operations

Time: O(n)


MOST COMMON BUG
---------------

if invalid:
    shrink

often WRONG

while invalid:
    shrink

usually CORRECT


MOST IMPORTANT QUESTION
-----------------------

"What information describes my
 current window, and exactly what
 makes that window valid or invalid?"
```

Start with the **guided problem only**. Write your condition, code, and complexity. I’ll review your reasoning line by line before we move to the two independent problems.