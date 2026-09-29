# Day 211 — DSA Foundation: Big-O Notation and Array Fundamentals

**Connection to your previous learning:** You have already seen **Big-O** and **Python lists** before. Today, we will deliberately rebuild the foundation from the beginning so that when we start solving DSA problems, you can look at code and understand both **what it does** and **how efficiently it does it**.

For today, don't worry about advanced optimization. Your goal is simply:

> **Understand how the amount of work changes when the input becomes larger.**

---

## 1. What is an algorithm?

An **algorithm** is simply a sequence of steps used to solve a problem.

For example, suppose you have:

```python
nums = [10, 20, 30, 40]
```

And you want to print every number.

One algorithm is:

```python
for num in nums:
    print(num)
```

The algorithm is:

1. Start from the first element.
2. Print it.
3. Move to the next element.
4. Repeat until the list ends.

DSA is largely about learning different ways to organize these steps efficiently.

---

# 2. What is input size?

You will frequently see the letter:

```text
n
```

In complexity analysis.

`n` normally represents the **input size**.

For example:

```python
nums = [10, 20, 30]
```

Here:

```text
n = 3
```

For:

```python
nums = [10, 20, 30, 40, 50, 60]
```

Here:

```text
n = 6
```

So when someone says:

> "This algorithm takes O(n) time."

They are saying:

> "The amount of work grows roughly in proportion to the number of input elements."

---

# 3. What is time complexity?

Time complexity does **not normally mean actual seconds**.

We are not primarily asking:

```text
Does this program take 0.01 seconds?
```

Instead, we ask:

> **How does the amount of work grow when the input grows?**

Imagine an array with:

```text
10 elements
100 elements
1,000 elements
1,000,000 elements
```

Will the algorithm perform approximately:

```text
1 operation?
n operations?
n × n operations?
```

That is what Big-O helps describe.

---

# 4. Real-life intuition for Big-O

Imagine you have **1,000 books** in a room.

### O(1) — Direct access

Someone tells you:

> "The book is in locker number 25."

You go directly to locker 25.

It doesn't matter whether there are:

```text
100 lockers
1,000 lockers
1,000,000 lockers
```

You still directly access locker 25.

That's the intuition behind:

```text
O(1)
```

---

### O(n) — Check every item

Now someone says:

> "I don't know where the book is. Check every locker."

You may need to inspect all lockers.

If there are:

```text
10 lockers   → around 10 checks
100 lockers  → around 100 checks
1000 lockers → around 1000 checks
```

That's:

```text
O(n)
```

---

### O(n²) — Compare everything with everything

Now suppose you have 100 students and want every student to shake hands with every other student.

You're doing many comparisons between pairs.

Very roughly:

```text
10 students  → around 100 operations
100 students → around 10,000 operations
1000 students → around 1,000,000 operations
```

That's the intuition behind:

```text
O(n²)
```

Here's a visual way to compare how these growth rates separate as `n` increases:



For today, focus only on:

```text
O(1)
O(n)
O(n²)
```

We will learn the other complexities later.

---

# 5. O(1) — Constant time

Consider:

```python
nums = [10, 20, 30, 40, 50]

print(nums[2])
```

Output:

```text
30
```

Python can directly access index `2`.

It does **not** need to check:

```text
10
20
30
```

one by one.

It directly accesses that location.

Therefore:

```text
Time Complexity: O(1)
```

This is called **constant time**.

Even if the list contains one million elements:

```python
print(nums[2])
```

is still considered:

```text
O(1)
```

---

# 6. O(n) — Linear time

Now consider:

```python
nums = [10, 20, 30, 40, 50]

for num in nums:
    print(num)
```

The loop visits every element.

For 5 elements:

```text
5 iterations
```

For 100 elements:

```text
100 iterations
```

For 1,000 elements:

```text
1,000 iterations
```

Therefore:

```text
Time Complexity: O(n)
```

This is called **linear time**.

---

# 7. O(n²) — Quadratic time

Look at this:

```python
nums = [1, 2, 3, 4]

for num1 in nums:
    for num2 in nums:
        print(num1, num2)
```

For every value in the outer loop, the inner loop runs through the entire array.

For:

```text
n = 4
```

approximately:

```text
4 × 4 = 16
```

operations happen.

For:

```text
n = 100
```

approximately:

```text
100 × 100 = 10,000
```

operations happen.

Therefore:

```text
Time Complexity: O(n²)
```

A beginner-friendly rule:

```text
One full loop        → often O(n)

Loop inside a loop   → often O(n²)
```

This is not a universal rule, but it is a very useful starting intuition.

---

# 8. Why do we ignore constants in Big-O?

Suppose we have:

```python
nums = [1, 2, 3, 4, 5]

for num in nums:
    print(num)

for num in nums:
    print(num)
```

We traverse the array twice.

Technically, the work is approximately:

```text
2n
```

But in Big-O, we say:

```text
O(n)
```

not:

```text
O(2n)
```

Why?

Because Big-O focuses on **how the algorithm grows**, not the exact number of operations.

Compare:

```text
n
2n
5n
100n
```

All of them grow **linearly**.

But:

```text
n²
```

grows fundamentally faster.

For example, with:

```text
n = 1,000
```

we get:

```text
n      = 1,000
2n     = 2,000
10n    = 10,000
n²     = 1,000,000
```

So when learning Big-O:

```text
O(2n)   → O(n)
O(5n)   → O(n)
O(100n) → O(n)
```

We care primarily about the **growth pattern**.

---

# 9. Space complexity

Time complexity asks:

> How much work does the algorithm perform?

Space complexity asks:

> How much **extra memory** does the algorithm use?

Consider:

```python
nums = [10, 20, 30, 40]

total = 0

for num in nums:
    total += num
```

We only created:

```python
total
num
```

The amount of extra memory doesn't grow significantly with the input size.

Therefore:

```text
Extra Space Complexity: O(1)
```

---

Now consider:

```python
nums = [10, 20, 30, 40]

result = []

for num in nums:
    result.append(num)
```

If `nums` contains `n` elements, `result` can also contain `n` elements.

Therefore:

```text
Extra Space Complexity: O(n)
```

A useful distinction:

```text
Input:
nums = [...]

Extra memory:
result = [...]
```

When discussing algorithm space complexity in interviews, we commonly focus on the **additional memory created by the algorithm**.

---

# 10. Python list as an array

For our DSA practice, we will mostly use Python's:

```python
list
```

as our array.

For example:

```python
nums = [10, 20, 30, 40, 50]
```

Conceptually:

```text
Index:    0   1   2   3   4
          ↓   ↓   ↓   ↓   ↓
Value:   10  20  30  40  50
```

Important:

> Python indexing starts at **0**, not 1.

So:

```python
nums[0]
```

gives:

```text
10
```

And:

```python
nums[4]
```

gives:

```text
50
```

---

# 11. Direct indexing

Example:

```python
nums = [10, 20, 30, 40, 50]

print(nums[0])
print(nums[2])
print(nums[4])
```

Output:

```text
10
30
50
```

Complexity of each direct access:

```text
Time:  O(1)
Space: O(1)
```

---

## Updating using an index

We can also modify a value:

```python
nums = [10, 20, 30, 40]

nums[1] = 100

print(nums)
```

Output:

```text
[10, 100, 30, 40]
```

Accessing/updating a normal list element by index is treated as:

```text
O(1)
```

---

# 12. Array traversal

**Traversal** simply means:

> Visit elements one by one.

Example:

```python
nums = [10, 20, 30, 40]

for num in nums:
    print(num)
```

Output:

```text
10
20
30
40
```

Because we visit every element:

```text
Time Complexity: O(n)
Space Complexity: O(1)
```

assuming we aren't creating another array.

---

## Traversing using indexes

You can also write:

```python
nums = [10, 20, 30, 40]

for i in range(len(nums)):
    print(nums[i])
```

Here:

```text
i = 0
i = 1
i = 2
i = 3
```

And therefore:

```text
nums[0]
nums[1]
nums[2]
nums[3]
```

This is also:

```text
Time:  O(n)
Space: O(1)
```

---

# 13. When should I use `num` vs `i`?

If you only need the values:

```python
for num in nums:
    print(num)
```

is usually clearer.

If you specifically need the index:

```python
for i in range(len(nums)):
    print(i, nums[i])
```

Example output:

```text
0 10
1 20
2 30
3 40
```

You will use both styles frequently in DSA.

---

# 14. Guided Easy Problem

## Problem: Find the largest number

Given:

```python
nums = [4, 2, 9, 1, 7]
```

Return the largest number.

Expected result:

```text
9
```

Do **not** worry about clever algorithms.

Let's solve it step by step.

---

## Step 1 — Think manually

If I gave you:

```text
4  2  9  1  7
```

you might think:

```text
Largest so far = 4

Compare 2 with 4
→ keep 4

Compare 9 with 4
→ largest becomes 9

Compare 1 with 9
→ keep 9

Compare 7 with 9
→ keep 9
```

Final answer:

```text
9
```

This idea — maintaining something **"so far"** — will appear constantly in DSA.

---

## Step 2 — Translate that into Python

```python
nums = [4, 2, 9, 1, 7]

largest = nums[0]

for num in nums:
    if num > largest:
        largest = num

print(largest)
```

Output:

```text
9
```

---

## Step 3 — Dry run

Initial:

```text
largest = 4
```

Iteration 1:

```text
num = 4

4 > 4? No

largest = 4
```

Iteration 2:

```text
num = 2

2 > 4? No

largest = 4
```

Iteration 3:

```text
num = 9

9 > 4? Yes

largest = 9
```

Iteration 4:

```text
num = 1

1 > 9? No

largest = 9
```

Iteration 5:

```text
num = 7

7 > 9? No

largest = 9
```

Final:

```text
largest = 9
```

---

## Complexity

We inspect every element once.

Therefore:

```text
Time Complexity: O(n)
```

We only store:

```text
largest
num
```

No second array is created.

Therefore:

```text
Extra Space Complexity: O(1)
```

---

# 15. Important edge cases

Whenever you solve an array problem, start developing the habit of checking edge cases.

### Case 1 — One element

```python
nums = [7]
```

Answer:

```text
7
```

---

### Case 2 — All negative numbers

```python
nums = [-8, -3, -10, -2]
```

Answer:

```text
-2
```

This is why doing this can be dangerous:

```python
largest = 0
```

Because every number may be negative.

Better:

```python
largest = nums[0]
```

---

### Case 3 — Duplicate values

```python
nums = [5, 5, 5]
```

Answer:

```text
5
```

---

### Case 4 — Already sorted

```python
nums = [1, 2, 3, 4, 5]
```

Answer:

```text
5
```

---

### Case 5 — Reverse sorted

```python
nums = [5, 4, 3, 2, 1]
```

Answer:

```text
5
```

For today's exercises, assume the array contains at least one element unless the problem explicitly says otherwise.

---

# 16. Independent Easy Problem — Your Turn

Don't look for a clever solution. Use today's concepts only.

## Problem: Count even numbers

Given an integer list:

```python
nums = [1, 2, 4, 7, 8, 11]
```

Return the **number of even values**.

Expected result:

```text
3
```

Because:

```text
2
4
8
```

are even.

### Your constraints

Use:

```python
for
if
%
```

You do **not** need another list.

Remember:

```python
number % 2 == 0
```

means the number is even.

I am intentionally **not giving you the solution yet**.

Try writing:

```python
def count_even(nums):
    # your code
```

Then test it using these easy cases:

```python
print(count_even([1, 2, 4, 7, 8, 11]))
# Expected: 3

print(count_even([2, 4, 6]))
# Expected: 3

print(count_even([1, 3, 5]))
# Expected: 0

print(count_even([10]))
# Expected: 1

print(count_even([]))
# Expected: 0
```

After writing the code, also tell me:

```text
Time Complexity = ?
Space Complexity = ?
```

Don't just write `O(n)` because you think that is probably correct. Explain **why**.

---

# 17. Common beginner mistakes

### Mistake 1 — Confusing index with value

Given:

```python
nums = [10, 20, 30]
```

This:

```python
for i in range(len(nums)):
    print(i)
```

prints:

```text
0
1
2
```

because `i` is the index.

This:

```python
for i in range(len(nums)):
    print(nums[i])
```

prints:

```text
10
20
30
```

because `nums[i]` is the value.

---

### Mistake 2 — Starting indexing from 1

Wrong mental model:

```text
10 → index 1
20 → index 2
30 → index 3
```

Python actually uses:

```text
10 → index 0
20 → index 1
30 → index 2
```

---

### Mistake 3 — Going outside the array

Given:

```python
nums = [10, 20, 30]
```

Valid indexes are:

```text
0
1
2
```

This fails:

```python
print(nums[3])
```

with:

```text
IndexError
```

---

### Mistake 4 — Assuming every loop is O(n)

Usually:

```python
for num in nums:
```

suggests O(n).

But you need to understand **what the loop actually does**.

For now, the simple rule is enough:

```text
Full traversal → O(n)
```

Later we'll become more precise.

---

### Mistake 5 — Thinking two loops always mean O(n²)

This:

```python
for num in nums:
    print(num)

for num in nums:
    print(num)
```

is:

```text
n + n = 2n
```

So:

```text
O(n)
```

It is **not** O(n²).

But this:

```python
for num1 in nums:
    for num2 in nums:
        print(num1, num2)
```

is:

```text
n × n
```

Therefore:

```text
O(n²)
```

Remember:

```text
Two separate loops:

n + n
→ 2n
→ O(n)
```

versus:

```text
Nested loops:

n × n
→ n²
→ O(n²)
```

This distinction is extremely important.

---

### Mistake 6 — Confusing time complexity and space complexity

Consider:

```python
total = 0

for num in nums:
    total += num
```

Time:

```text
O(n)
```

because we process `n` elements.

Space:

```text
O(1)
```

because we don't create memory proportional to `n`.

Time and space complexity do **not** need to be the same.

---

# 18. Today's mental model

For Day 211, memorize this much:

| Code pattern | Typical time |
|---|---:|
| `nums[5]` | **O(1)** |
| One full traversal | **O(n)** |
| Two separate full traversals | **O(n)** |
| Nested full traversals | **O(n²)** |

And:

```text
No growing extra collection
→ often O(1) extra space

New list containing n items
→ often O(n) extra space
```

Don't try to memorize dozens of Big-O rules today.

Build the intuition first.

---

# 19. Five quick self-check questions

Answer these **without looking back** if possible.

### Q1

What is the time complexity?

```python
nums = [10, 20, 30, 40]

print(nums[2])
```

```text
A. O(1)
B. O(n)
C. O(n²)
```

---

### Q2

What is the time complexity?

```python
for num in nums:
    print(num)
```

```text
A. O(1)
B. O(n)
C. O(n²)
```

---

### Q3

What is the time complexity?

```python
for x in nums:
    for y in nums:
        print(x, y)
```

```text
A. O(1)
B. O(n)
C. O(n²)
```

---

### Q4

Why do we normally simplify:

```text
O(5n)
```

to:

```text
O(n)
```

Explain it in **one sentence in your own words**.

---

### Q5

Consider:

```python
result = []

for num in nums:
    result.append(num * 2)
```

Tell me:

```text
Time Complexity = ?
Extra Space Complexity = ?
```

---

## Day 211 assignment

Before moving to Day 212, send me **two things**:

```python
def count_even(nums):
    # your solution
```

and your answers to:

```text
Time Complexity = ?
Space Complexity = ?
```

Also answer **Q1–Q5**.

I'll review your code like an interviewer/DSA mentor: first checking correctness, then your Big-O reasoning, and only after that showing you the clean solution.