# Day 217 — DSA Revision: Big-O, Arrays, Strings, Hashing, Two Pointers & Sliding Window

Today is a **revision day**. We will not introduce a major new topic.

The goal is:

> Look at a problem and recognize which pattern is likely useful before writing code.

You have covered:

```text
Day 211 → Big-O + Arrays
Day 212 → Array traversal patterns
Day 213 → Strings
Day 214 → Hash Maps + Sets
Day 215 → Two Pointers
Day 216 → Fixed Sliding Window
```

---

# 1. Revision — Big-O

Big-O tells us how work grows as input size `n` grows.

### O(1)

Constant work.

```python
nums = [10, 20, 30]

print(nums[1])
```

Direct indexing:

```text
Time: O(1)
```

---

### O(n)

Visit every element once.

```python
for num in nums:
    print(num)
```

```text
Time: O(n)
```

---

### O(n²)

Commonly caused by comparing many pairs.

```python
for x in nums:
    for y in nums:
        print(x, y)
```

```text
Time: O(n²)
```

Remember:

```text
Two separate loops:

O(n) + O(n)
→ O(n)
```

but:

```text
Nested full loops:

O(n × n)
→ O(n²)
```

Also keep **time complexity** separate from **space complexity**.

Example:

```python
total = 0

for num in nums:
    total += num
```

is:

```text
Time:  O(n)
Space: O(1)
```

---

# 2. Revision — Arrays

Python lists are our main array structure.

```python
nums = [10, 20, 30, 40]
```

Indexes:

```text
Index:  0   1   2   3
Value: 10  20  30  40
```

Direct indexing:

```python
nums[2]
```

is:

```text
O(1)
```

Full traversal:

```python
for num in nums:
    print(num)
```

is:

```text
O(n)
```

---

## Core array patterns

### Sum

```python
total = 0

for num in nums:
    total += num
```

### Count

```python
count = 0

for num in nums:
    if condition:
        count += 1
```

### Maximum

```python
maximum = nums[0]

for num in nums:
    if num > maximum:
        maximum = num
```

### Minimum

```python
minimum = nums[0]

for num in nums:
    if num < minimum:
        minimum = num
```

### Update array

```python
for i in range(len(nums)):
    nums[i] = nums[i] * 2
```

Recognition question:

> Can I get the answer while visiting every element once?

If yes, simple traversal may be enough.

---

# 3. Revision — Strings

Strings behave like sequences of characters.

```python
text = "hello"
```

```text
Index: 0 1 2 3 4
Char:  h e l l o
```

Character access:

```python
text[1]
```

gives:

```text
e
```

Traversal:

```python
for char in text:
    print(char)
```

is:

```text
O(n)
```

The important difference from lists:

```text
List   → mutable
String → immutable
```

This is invalid:

```python
text[0] = "H"
```

---

## String questions to ask

Before solving:

```text
Does case matter?
Do spaces matter?
Can text be empty?
Can it contain one character?
Do I need indexes or just characters?
Am I creating another string?
```

---

# 4. Revision — Hash Maps

Python:

```python
dict
```

stores:

```text
key → value
```

Example:

```python
frequency = {
    "a": 3,
    "b": 1
}
```

Hash maps are useful when you need information associated with something.

Strong example:

```text
character → frequency
number → index
word → count
```

Average lookup:

```text
O(1)
```

---

## Frequency map

```python
frequency = {}

for item in items:
    frequency[item] = frequency.get(item, 0) + 1
```

Typical total complexity:

```text
Time:  O(n) average
Space: O(n)
```

---

# 5. Revision — Sets

Python:

```python
set
```

stores unique values.

```python
seen = set()

seen.add(10)
seen.add(20)
```

Membership:

```python
10 in seen
```

is average:

```text
O(1)
```

Use a set when you mainly need:

```text
Have I seen this?
Does this exist?
Is there a duplicate?
```

You usually don't need a dictionary if there is no extra information attached to the value.

---

# 6. Dictionary vs Set

Remember this distinction:

```text
Need only existence?
→ Set
```

Example:

```text
Have I already seen 7?
```

Use:

```python
seen = set()
```

But:

```text
Need information associated with 7?
→ Dictionary
```

Example:

```text
7 appeared 4 times
```

Use:

```python
frequency = {}
```

Or:

```text
7 was originally at index 3
```

Use:

```python
positions = {}
```

---

# 7. Revision — Two Pointers

Two pointers usually mean two indexes moving through the same sequence.

Example:

```python
left = 0
right = len(nums) - 1
```

Visualization:

```text
1   2   3   4   5
↑               ↑
L               R
```

Common situations:

```text
Palindrome
Sorted pair sum
Reverse in place
Compare opposite ends
Remove duplicates
```

---

## Palindrome pattern

```text
r a c e c a r
↑           ↑
L           R
```

Compare outside characters.

If equal:

```text
move inward
```

```python
left += 1
right -= 1
```

Typical complexity:

```text
Time:  O(n)
Space: O(1)
```

---

## Sorted pair-sum logic

Given sorted:

```text
[1, 2, 4, 6, 8]
```

If:

```text
nums[left] + nums[right] < target
```

the sum is too small.

Move:

```python
left += 1
```

If:

```text
sum > target
```

move:

```python
right -= 1
```

This works because the array is sorted.

---

# 8. Revision — Fixed Sliding Window

Sliding window is for a **contiguous region**.

Example:

```text
[2 1 5] 1 3 2

  [1 5 1] 3 2

    [5 1 3] 2
```

For fixed-size window `k`, the size never changes.

The key optimization is:

```text
Old window

- outgoing value
+ incoming value

= new window
```

Instead of recalculating all `k` elements.

Example:

```python
window_sum += nums[right]
window_sum -= nums[right - k]
```

Typical complexity:

```text
Brute force: O(n × k)

Sliding window:
Time:  O(n)
Space: O(1)
```

Strong signal:

```text
contiguous + exactly k
```

---

# 9. Pattern-Recognition Table

| Problem signal | First pattern to consider | Why |
|---|---|---|
| Process every array element once | Array traversal | One pass may be enough |
| Count/sum/min/max over an array | Array traversal + accumulator | Maintain answer while traversing |
| Process every character | String traversal | String is a character sequence |
| Count frequency of values | Hash map | Need `value → count` |
| Need to know whether something was seen | Set | Fast membership lookup |
| Need previous value plus extra information | Hash map | Store `value → information` |
| Compare start and end | Two pointers | Move boundaries inward |
| Sorted array + find pair | Two pointers | Sorted order tells which pointer to move |
| Modify/compact array in place | Two pointers | Read/write positions can move independently |
| Exactly `k` contiguous elements | Fixed sliding window | Reuse previous window information |
| Maximum/average of `k` consecutive values | Fixed sliding window | Add incoming, remove outgoing |
| Brute force repeatedly searches for values | Hashing may help | Replace repeated O(n) search with average O(1) lookup |

This table is not saying there is always only one valid pattern. It gives you a good **first pattern to investigate**.

---

# 10. Ten Short Recognition Scenarios

For each scenario, tell me:

```text
Pattern I would try:
Why:
```

Do **not** code yet.

### Scenario 1

Given:

```python
nums = [5, 8, 2, 10, 4]
```

Find the largest number.

Which pattern would you try, and why?

---

### Scenario 2

Given:

```python
text = "engineering"
```

Count how many times `"e"` occurs.

Which pattern would you try?

---

### Scenario 3

Given:

```python
nums = [4, 7, 2, 7]
```

Determine whether any number appears more than once.

Which structure/pattern would you consider?

---

### Scenario 4

Given:

```python
text = "level"
```

Determine whether it reads the same from both ends without creating a reversed string.

Which pattern?

---

### Scenario 5

Given a **sorted** array:

```python
nums = [1, 3, 4, 7, 9]
target = 10
```

Determine whether two numbers add to `10`.

Which pattern?

---

### Scenario 6

Given:

```python
nums = [2, 1, 5, 1, 3, 2]
k = 3
```

Find the largest sum among every three consecutive elements.

Which pattern?

---

### Scenario 7

Given:

```python
text = "banana"
```

Build:

```text
character → number of occurrences
```

Which pattern/data structure?

---

### Scenario 8

Given:

```python
nums = [8, 2, 4, 8, 3]
```

You need to know:

```text
number → first index where it appeared
```

Which data structure?

---

### Scenario 9

Given:

```python
nums = [1, 2, 3, 4]
```

Replace every odd number with `0`.

Which basic traversal style would you use?

Think specifically about:

```text
index vs value
```

---

### Scenario 10

Given a sorted list containing duplicates:

```python
nums = [1, 1, 2, 2, 3, 4, 4]
```

You want to compact unique values toward the beginning using little extra memory.

Which pattern would you investigate?

---

# 11. How I want you to answer the recognition section

For example:

```text
Scenario 1:
Pattern: Array traversal
Why: I need to inspect each value and maintain the maximum seen so far.
```

Do the same for all 10.

After you answer, I can identify where your **pattern recognition is strong and where you're confusing similar patterns**.

---

# 12. Coding Problem 1 — Easy

## Problem: Count Values Greater Than the Average

Given:

```python
nums = [2, 4, 6, 8]
```

Return how many elements are greater than the average of the array.

Here:

```text
Average = 5
```

Numbers greater than `5`:

```text
6
8
```

Expected:

```text
2
```

Write:

```python
def count_above_average(nums):
    # your solution
```

Rules:

```text
If nums is empty:
return 0
```

Tests:

```python
print(count_above_average([2, 4, 6, 8]))
# Expected: 2

print(count_above_average([5]))
# Expected: 0

print(count_above_average([1, 1, 1]))
# Expected: 0

print(count_above_average([]))
# Expected: 0
```

Do not worry about finding a clever one-pass trick. Focus on correctness and complexity.

I am intentionally **not telling you the pattern**.

---

# 13. Coding Problem 2 — Easy

## Problem: First Repeated Value

Given:

```python
nums = [5, 3, 4, 3, 2]
```

Return the **first value encountered during left-to-right traversal that has already appeared before**.

Expected:

```text
3
```

Another:

```python
nums = [1, 2, 3, 1, 2]
```

Expected:

```text
1
```

If there is no repeated value:

```python
nums = [1, 2, 3]
```

return:

```python
None
```

Write:

```python
def first_repeated(nums):
    # your solution
```

Tests:

```python
print(first_repeated([5, 3, 4, 3, 2]))
# 3

print(first_repeated([1, 2, 3, 1, 2]))
# 1

print(first_repeated([1, 2, 3]))
# None

print(first_repeated([]))
# None

print(first_repeated([5, 5]))
# 5
```

Again, no hints yet.

---

# 14. Coding Problem 3 — Easy/Medium

## Problem: Maximum Number of Even Values in a Window

Given:

```python
nums = [1, 2, 4, 5, 6, 8, 3]
k = 3
```

Consider every contiguous group of exactly `3` elements.

Your job is to return the **maximum number of even values contained in any one window**.

Example windows:

```text
[1, 2, 4]
[2, 4, 5]
[4, 5, 6]
...
```

For the input above, return the maximum count.

Write:

```python
def max_even_in_window(nums, k):
    # your solution
```

Rules:

```text
If k <= 0:
return 0

If len(nums) < k:
return 0
```

Tests:

```python
print(max_even_in_window([1, 2, 4, 5, 6, 8, 3], 3))
```

```python
print(max_even_in_window([1, 3, 5], 2))
# Expected: 0
```

```python
print(max_even_in_window([2], 1))
# Expected: 1
```

```python
print(max_even_in_window([2, 4, 6], 3))
# Expected: 3
```

I am intentionally not telling you which pattern this uses.

---

# 15. Required format for all three coding problems

For each problem, don't immediately jump to optimized code.

Use this sequence:

```text
1. Understand the problem

2. Brute-force reasoning

3. Brute-force pseudocode

4. Brute-force complexity
   Time:
   Space:

5. Optimized reasoning

6. Optimized pseudocode

7. Optimized Python code

8. Optimized complexity
   Time:
   Space:

9. Edge cases
```

For some problems, you may discover that the simple approach is already good enough.

That's perfectly valid.

Don't invent optimization just because I asked for an optimized section.

You can say:

> "The brute-force/simple approach is already O(n), so I don't see a meaningful optimization."

That is good algorithmic reasoning.

---

# 16. What I will check after you answer

When you send your answers, I will look for several specific things.

I will check whether you:

```text
Recognize simple traversal instead of overengineering.

Know when a set is enough.

Know when a dictionary is actually required.

Understand why sorted order enables two pointers.

Understand incoming/outgoing values in sliding window.

Separate time complexity from space complexity.

Correctly distinguish O(n), O(n²), and O(n × k).

Handle empty and one-element inputs.

Explain why your optimization works instead of memorizing code.
```

Then I will identify your **weak patterns from your actual answers**, rather than guessing now.

---

# 17. Common Revision Mistakes

One common mistake is thinking:

```text
"Hashing is always better."
```

Not necessarily.

Hashing often trades:

```text
extra memory
```

for:

```text
faster lookup
```

---

Another mistake:

```text
"Two pointers means sorted arrays."
```

Not always.

Palindrome:

```text
racecar
↑     ↑
```

also uses two pointers.

Sorted order is particularly important when pointer movement depends on whether a value is too large or too small.

---

Another mistake:

```text
"Sliding window means two pointers."
```

They are closely related, but the defining feature is different.

Two pointers:

> Maintain two useful positions.

Sliding window:

> Maintain information about a contiguous region between boundaries.

---

Another mistake:

```text
"One loop means O(1)."
```

No.

```python
for num in nums:
```

runs based on input size.

Therefore:

```text
O(n)
```

---

Another mistake is optimizing before solving.

Use:

```text
Correct solution
↓
Analyze complexity
↓
Identify repeated work
↓
Optimize repeated work
```

---

# Day 217 — One-Page Revision Cheat Sheet

## Big-O

```text
Direct index
nums[i]
→ O(1)

One full traversal
→ O(n)

Nested full traversal
→ O(n²)

Dictionary/set lookup
→ O(1) average
```

Remember:

```text
O(2n) → O(n)
O(5n) → O(n)
```

---

## Arrays

Use traversal for:

```text
sum
count
minimum
maximum
update
```

Templates:

```python
total = 0

for num in nums:
    total += num
```

```python
count = 0

for num in nums:
    if condition:
        count += 1
```

Need to modify positions?

```python
for i in range(len(nums)):
    nums[i] = ...
```

---

## Strings

Strings support:

```text
indexing
traversal
slicing
comparison
```

But:

```text
strings are immutable
```

Ask:

```text
Case-sensitive?
Spaces relevant?
Empty string?
```

---

## Set

Think:

```text
Have I seen this?
Does this exist?
Duplicate?
```

Template:

```python
seen = set()

for item in items:
    if item in seen:
        # already seen

    seen.add(item)
```

Typical:

```text
Time:  O(n) average
Space: O(n)
```

---

## Hash Map / Dictionary

Think:

```text
value → information
```

Examples:

```text
character → frequency
number → index
word → count
```

Frequency template:

```python
frequency = {}

for item in items:
    frequency[item] = frequency.get(item, 0) + 1
```

Typical:

```text
Time:  O(n) average
Space: O(n)
```

---

## Two Pointers

Strong signals:

```text
sorted array
pair
palindrome
both ends
reverse in place
remove duplicates
```

Opposite ends:

```python
left = 0
right = len(nums) - 1

while left < right:
    ...
```

Sorted pair rule:

```text
sum too small
→ left += 1

sum too large
→ right -= 1
```

Often:

```text
Time: O(n)
Space: O(1)
```

---

## Fixed Sliding Window

Strong signal:

```text
contiguous + exactly k
```

Core idea:

```text
old window
- outgoing
+ incoming
= new window
```

Template:

```python
window_sum = 0

for i in range(k):
    window_sum += nums[i]

for right in range(k, len(nums)):
    window_sum += nums[right]
    window_sum -= nums[right - k]
```

Typical:

```text
Time:  O(n)
Space: O(1)
```

instead of brute-force:

```text
O(n × k)
```

---

## Pattern-selection checklist

Before coding, ask:

```text
1. Can simple traversal solve this?

2. Do I need to remember whether something appeared?
   → set

3. Do I need information about something?
   → dictionary

4. Does the problem compare two positions or opposite ends?
   → two pointers

5. Is the array sorted and asking about a pair?
   → consider two pointers

6. Does it say contiguous + exactly k?
   → fixed sliding window

7. What repeated work does brute force perform?

8. Can I store or reuse information instead?

9. What is my time complexity?

10. What extra memory am I using?
```

For **Day 217**, first answer the **10 recognition scenarios**, then solve the **3 coding problems** in the required reasoning order. Once you send them, I’ll evaluate not only whether the code works, but also identify whether your weaker area is **complexity analysis, hashing selection, pointer movement, sliding-window updates, or basic traversal recognition**.