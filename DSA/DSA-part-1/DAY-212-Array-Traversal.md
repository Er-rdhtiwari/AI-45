# Day 212 — Arrays: Traversal and Basic Problem-Solving Patterns

Yesterday, you learned **array complexity, indexing, and traversal**. Today, you will use traversal to solve simple problems.

The main goal is:

> Read an array once, keep track of useful information, and produce the answer.

Today, focus on recognizing a few basic patterns:

```text
Traversal
Accumulator
Minimum / Maximum
Counting
Updating values
```

---

# 1. Forward traversal

Forward traversal means visiting elements from left to right.

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

You can also traverse using indexes:

```python
nums = [10, 20, 30, 40]

for i in range(len(nums)):
    print(nums[i])
```

Both are typically:

```text
Time Complexity: O(n)
```

because every element is visited once.

---

# 2. Reverse traversal

Sometimes we need to process the array from right to left.

Example:

```python
nums = [10, 20, 30, 40]

for i in range(len(nums) - 1, -1, -1):
    print(nums[i])
```

Output:

```text
40
30
20
10
```

Let's understand:

```python
range(len(nums) - 1, -1, -1)
```

For:

```python
nums = [10, 20, 30, 40]
```

we have:

```text
len(nums) = 4
```

Last valid index:

```text
4 - 1 = 3
```

So indexes become:

```text
3
2
1
0
```

This is still:

```text
O(n)
```

because we visit every element once.

---

# 3. Index vs value

This distinction is very important.

Consider:

```python
nums = [10, 20, 30]
```

## Value traversal

```python
for num in nums:
    print(num)
```

Here:

```text
num = 10
num = 20
num = 30
```

`num` represents the **value**.

Use this when you don't care where the number is located.

---

## Index traversal

```python
for i in range(len(nums)):
    print(i)
```

Output:

```text
0
1
2
```

Here, `i` represents the **index**.

You can access the value using:

```python
nums[i]
```

For example:

```python
for i in range(len(nums)):
    print(i, nums[i])
```

Output:

```text
0 10
1 20
2 30
```

A simple rule:

```text
Need only the value?
→ for num in nums

Need position/index or need to modify the array?
→ for i in range(len(nums))
```

---

# 4. The accumulator pattern

The **accumulator pattern** is one of the most important beginner DSA patterns.

The idea is:

> Create a variable before the loop and continuously update it while traversing the array.

Example:

```python
nums = [1, 2, 3, 4]

total = 0

for num in nums:
    total = total + num
```

Here:

```text
total
```

is the accumulator.

Let's dry-run it.

Initially:

```text
total = 0
```

First number:

```text
num = 1
total = 0 + 1
total = 1
```

Second:

```text
num = 2
total = 1 + 2
total = 3
```

Third:

```text
num = 3
total = 3 + 3
total = 6
```

Fourth:

```text
num = 4
total = 6 + 4
total = 10
```

Final answer:

```text
10
```

The general pattern looks like:

```python
answer = initial_value

for item in array:
    answer = updated_answer
```

You will see this pattern repeatedly.

---

# 5. Finding the sum

Problem:

```python
nums = [5, 10, 15]
```

Find the sum.

Solution:

```python
nums = [5, 10, 15]

total = 0

for num in nums:
    total += num

print(total)
```

Output:

```text
30
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

Why?

We inspect all `n` elements once, but only keep one variable:

```text
total
```

---

# 6. Finding the minimum

Suppose:

```python
nums = [8, 3, 10, 2, 7]
```

We want:

```text
2
```

Start by assuming the first value is the minimum:

```python
minimum = nums[0]
```

Then compare every value:

```python
nums = [8, 3, 10, 2, 7]

minimum = nums[0]

for num in nums:
    if num < minimum:
        minimum = num

print(minimum)
```

Dry run:

```text
minimum = 8

3 < 8
→ minimum = 3

10 < 3
→ no

2 < 3
→ minimum = 2

7 < 2
→ no
```

Answer:

```text
2
```

Complexity:

```text
Time: O(n)
Space: O(1)
```

---

# 7. Finding the maximum

Same pattern, but reverse the comparison.

```python
nums = [8, 3, 10, 2, 7]

maximum = nums[0]

for num in nums:
    if num > maximum:
        maximum = num

print(maximum)
```

Output:

```text
10
```

The pattern is:

```text
Minimum:
if num < current_minimum

Maximum:
if num > current_maximum
```

---

# 8. Counting matching values

Suppose we want to count how many numbers are positive.

```python
nums = [-2, 5, 7, -1, 10]
```

Expected answer:

```text
3
```

Use a counter:

```python
nums = [-2, 5, 7, -1, 10]

count = 0

for num in nums:
    if num > 0:
        count += 1

print(count)
```

Output:

```text
3
```

Here:

```text
count
```

is also an accumulator.

But instead of accumulating numbers themselves, we accumulate:

```text
how many matches we found
```

General counting pattern:

```python
count = 0

for item in nums:
    if condition:
        count += 1
```

This is a very common interview pattern.

---

# 9. Updating array values

Sometimes we do not just read the array.

We want to modify it.

Suppose:

```python
nums = [1, 2, 3, 4]
```

We want:

```text
[2, 4, 6, 8]
```

One approach:

```python
nums = [1, 2, 3, 4]

for i in range(len(nums)):
    nums[i] = nums[i] * 2

print(nums)
```

Output:

```text
[2, 4, 6, 8]
```

Notice that we used:

```python
for i in range(len(nums)):
```

instead of:

```python
for num in nums:
```

Why?

Because we need to modify the actual array position:

```python
nums[i]
```

A useful rule:

```text
Reading values
→ value traversal is often enough

Updating values
→ index traversal is often useful
```

---

# 10. Why one traversal is often enough

Suppose you want to find the maximum.

You don't need:

```text
one loop to inspect numbers
another loop to find maximum
another loop to verify
```

You can simply maintain:

```text
maximum so far
```

during one traversal.

Example:

```python
maximum = nums[0]

for num in nums:
    if num > maximum:
        maximum = num
```

Each element gives you enough information to update the answer.

This is a useful question to ask yourself:

> Can I maintain everything I need while visiting each element once?

If yes, one traversal is probably enough.

For many basic problems:

```text
sum
count
minimum
maximum
existence check
```

one traversal is enough.

---

# 11. Empty-array edge case

Consider:

```python
nums = []
```

This will fail:

```python
minimum = nums[0]
```

because index `0` doesn't exist.

Python raises:

```text
IndexError
```

So if an empty array is possible, handle it explicitly.

Example:

```python
def find_minimum(nums):
    if len(nums) == 0:
        return None

    minimum = nums[0]

    for num in nums:
        if num < minimum:
            minimum = num

    return minimum
```

Now:

```python
print(find_minimum([]))
```

returns:

```text
None
```

For interview questions, always check the problem statement.

Sometimes the interviewer guarantees:

```text
nums contains at least one element
```

In that case, you don't need the empty-list handling.

---

# 12. One-element edge case

Suppose:

```python
nums = [8]
```

Minimum:

```text
8
```

Maximum:

```text
8
```

Sum:

```text
8
```

Your algorithm should naturally handle this.

For example:

```python
minimum = nums[0]

for num in nums:
    if num < minimum:
        minimum = num
```

With:

```python
nums = [8]
```

the result remains:

```text
8
```

which is correct.

---

# 13. Common off-by-one mistakes

An **off-by-one error** happens when your loop starts or ends one position too early or too late.

Consider:

```python
nums = [10, 20, 30, 40]
```

Valid indexes are:

```text
0
1
2
3
```

Not:

```text
0
1
2
3
4
```

because:

```text
len(nums) = 4
```

but the last index is:

```text
len(nums) - 1
```

which is:

```text
3
```

---

## Correct forward traversal

```python
for i in range(len(nums)):
    print(nums[i])
```

Python generates:

```text
0
1
2
3
```

---

## Common mistake

```python
for i in range(len(nums) + 1):
    print(nums[i])
```

Eventually:

```text
i = 4
```

and:

```python
nums[4]
```

does not exist.

Result:

```text
IndexError
```

---

## Reverse traversal mistake

Correct:

```python
for i in range(len(nums) - 1, -1, -1):
    print(nums[i])
```

A beginner might write:

```python
for i in range(len(nums), -1, -1):
```

But the first value becomes:

```text
4
```

and:

```python
nums[4]
```

does not exist.

Remember:

```text
Length = number of elements

Last index = length - 1
```

This one sentence prevents many mistakes.

---

# 14. Guided Problem

## Problem: Count numbers greater than a target

Given:

```python
nums = [3, 8, 2, 10, 5]
target = 5
```

Return how many values are greater than `5`.

Expected answer:

```text
2
```

because:

```text
8
10
```

are greater than `5`.

---

## Step 1 — Thought process

Ask:

> What information do I need?

We only need a count.

Therefore, create:

```text
count = 0
```

Then inspect every value.

For each number:

```text
if num > target
```

increase the count.

---

## Step 2 — Pseudocode

```text
set count to 0

for every number in nums:
    if number is greater than target:
        increase count by 1

return count
```

---

## Step 3 — Python

```python
def count_greater(nums, target):
    count = 0

    for num in nums:
        if num > target:
            count += 1

    return count
```

Test:

```python
print(count_greater([3, 8, 2, 10, 5], 5))
```

Output:

```text
2
```

---

## Step 4 — Time complexity

The loop checks every element once.

If there are `n` values:

```text
Time Complexity: O(n)
```

---

## Step 5 — Space complexity

We only use:

```text
count
num
target
```

We don't create another array.

Therefore:

```text
Extra Space Complexity: O(1)
```

---

## Edge cases

Empty array:

```python
count_greater([], 5)
```

Result:

```text
0
```

One value greater than target:

```python
count_greater([10], 5)
```

Result:

```text
1
```

One value smaller than target:

```python
count_greater([2], 5)
```

Result:

```text
0
```

---

# 15. Independent Problem 1 — Find the sum of even numbers

Do this yourself first.

Given:

```python
nums = [1, 2, 3, 4, 5, 6]
```

Return the sum of all even numbers.

Expected answer:

```text
12
```

because:

```text
2 + 4 + 6 = 12
```

Write:

```python
def sum_even(nums):
    # your solution
```

Test cases:

```python
print(sum_even([1, 2, 3, 4, 5, 6]))
# Expected: 12

print(sum_even([1, 3, 5]))
# Expected: 0

print(sum_even([2]))
# Expected: 2

print(sum_even([]))
# Expected: 0

print(sum_even([2, 4, 6]))
# Expected: 12
```

For this problem, send me all five:

```text
1. Thought process
2. Pseudocode
3. Python code
4. Time Complexity
5. Space Complexity
```

I am intentionally not showing the solution yet.

---

# 16. Independent Problem 2 — Replace negative numbers with zero

Given:

```python
nums = [4, -2, 7, -5, 3]
```

Modify the same array so it becomes:

```text
[4, 0, 7, 0, 3]
```

Write:

```python
def replace_negative(nums):
    # your solution
```

Expected:

```python
nums = [4, -2, 7, -5, 3]

replace_negative(nums)

print(nums)
```

Output:

```text
[4, 0, 7, 0, 3]
```

Test these:

```python
nums = [-1, -2, -3]
# Expected after function:
# [0, 0, 0]
```

```python
nums = [1, 2, 3]
# Expected:
# [1, 2, 3]
```

```python
nums = [-5]
# Expected:
# [0]
```

```python
nums = []
# Expected:
# []
```

Again, give me:

```text
1. Thought process
2. Pseudocode
3. Python code
4. Time Complexity
5. Space Complexity
```

Do not create a second array unless you genuinely think it is necessary.

---

# 17. How to recognize which pattern to use

When you read a problem, look for certain words.

If the question says:

```text
Find the total
Find the sum
```

Think:

```python
total = 0
```

Accumulator pattern.

---

If it says:

```text
How many...
Count...
```

Think:

```python
count = 0
```

Counting pattern.

---

If it says:

```text
Find largest
Find maximum
```

Think:

```python
maximum = nums[0]
```

Then:

```python
if num > maximum:
```

---

If it says:

```text
Find smallest
Find minimum
```

Think:

```python
minimum = nums[0]
```

Then:

```python
if num < minimum:
```

---

If it says:

```text
Change each value
Replace values
Modify the array
```

Think:

```python
for i in range(len(nums)):
```

because you probably need access to:

```python
nums[i]
```

---

# 18. One-pass pattern

You'll hear interviewers say:

> "Can you solve it in one pass?"

One pass simply means:

> Traverse the array once.

For example:

```python
for num in nums:
```

is one pass.

If `n = 1,000`, approximately 1,000 values are inspected.

Therefore:

```text
O(n)
```

You will often be able to calculate several things during one pass.

For example:

```python
total = 0
count = 0

for num in nums:
    total += num

    if num > 0:
        count += 1
```

We are calculating:

```text
sum
+
number of positive values
```

during the same traversal.

This is still:

```text
O(n)
```

not:

```text
O(2n)
```

in Big-O terms.

---

# 19. Pattern-recognition notes for Day 212

Keep these mental templates.

### Pattern 1 — Sum

```python
total = 0

for num in nums:
    total += num
```

Think:

> "I need to accumulate values."

---

### Pattern 2 — Count

```python
count = 0

for num in nums:
    if condition:
        count += 1
```

Think:

> "I need to count how many elements satisfy something."

---

### Pattern 3 — Minimum

```python
minimum = nums[0]

for num in nums:
    if num < minimum:
        minimum = num
```

Think:

> "Keep the smallest value seen so far."

---

### Pattern 4 — Maximum

```python
maximum = nums[0]

for num in nums:
    if num > maximum:
        maximum = num
```

Think:

> "Keep the largest value seen so far."

---

### Pattern 5 — Modify array

```python
for i in range(len(nums)):
    if condition:
        nums[i] = new_value
```

Think:

> "I need the index because I need to change the array."

---

### Pattern 6 — Reverse traversal

```python
for i in range(len(nums) - 1, -1, -1):
    print(nums[i])
```

Think:

> "Start from the last valid index, which is `len(nums) - 1`."

---

## Day 212 key takeaway

Don't try to memorize lots of DSA tricks yet.

For now, when you see an easy array problem, ask yourself:

```text
1. What information am I trying to maintain?

2. Do I need the value or the index?

3. Can I solve it while traversing once?

4. What should my accumulator start with?

5. What happens for []?

6. What happens for one element?

7. Am I creating extra memory?
```

Your **Day 212 assignment** is the two independent problems above. For each one, send me your **thought process → pseudocode → Python → time complexity → space complexity**. I’ll review the reasoning first, because developing that sequence is more important at this stage than simply getting the final code correct.