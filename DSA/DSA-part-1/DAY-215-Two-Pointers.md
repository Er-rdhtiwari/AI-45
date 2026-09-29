# Day 215 — Two Pointer Technique

**Connection:** Yesterday you learned that hashing can reduce repeated searching by using extra memory. Today you will learn another important pattern: **two pointers**, which can often solve problems efficiently while using very little extra memory.

The main idea is simple:

> Instead of using one index, use two indexes that move through the data in a controlled way.

For today, focus on understanding **where the pointers start, why they move, and when they stop**.

---

## 1. What is a pointer in DSA?

In Python DSA problems, a pointer is usually just an integer index.

Example:

```python
nums = [10, 20, 30, 40, 50]

left = 0
right = len(nums) - 1
```

Here:

```text
left = 0
right = 4
```

Visualization:

```text
Index:     0    1    2    3    4
Value:    10   20   30   40   50
           ↑                 ↑
         left              right
```

The pointers tell us which positions we are currently examining.

---

# 2. Two common types of two pointers

There are two major beginner patterns.

### Pattern A — Moving toward each other

Start:

```text
left  → beginning
right → end
```

Then:

```text
left moves right
right moves left
```

Example:

```text
a b c b a
↑       ↑
L       R
```

Then:

```text
a b c b a
  ↑   ↑
  L   R
```

Useful for:

- palindrome checking
- sorted pair problems
- reversing
- comparing opposite ends

---

### Pattern B — Moving in the same direction

Example:

```text
0 1 2 3 4 5
↑
L
↑
R
```

Later:

```text
0 1 2 3 4 5
    ↑
    L
        ↑
        R
```

Both pointers move toward the right, but they can move at different speeds.

This pattern appears later in problems involving:

- removing duplicates
- compacting arrays
- filtering values
- sliding window problems

Today we'll mainly build intuition rather than go deeply into sliding windows.

---

# 3. When are two pointers useful?

Two pointers are especially useful when the problem involves relationships between different positions in a sequence.

For example:

```text
Compare first and last
Find two numbers with a target sum
Move values around
Remove duplicates from a sorted array
Check whether a string is a palindrome
```

A powerful recognition question is:

> Am I repeatedly comparing or searching between positions in the same array/string?

If yes, two pointers may help.

---

# 4. Pointer movement visualization

Consider:

```python
nums = [2, 4, 6, 8, 10]
```

Start:

```text
Index:    0   1   2   3   4
Value:    2   4   6   8  10
          ↑               ↑
          L               R
```

Move both inward:

```text
Index:    0   1   2   3   4
Value:    2   4   6   8  10
              ↑       ↑
              L       R
```

Again:

```text
Index:    0   1   2   3   4
Value:    2   4   6   8  10
                  ↑
                 L/R
```

Usually the loop continues while:

```python
left < right
```

or sometimes:

```python
left <= right
```

depending on the problem.

Understanding that stopping condition is very important.

---

# 5. Palindrome using two pointers

You already learned a simple palindrome approach:

```python
text == text[::-1]
```

That works, but it creates a reversed copy.

Two pointers let us compare both ends without creating another string.

Example:

```text
"radar"
```

Visualization:

```text
Index:   0   1   2   3   4
Char:    r   a   d   a   r
         ↑               ↑
         L               R
```

Compare:

```text
r == r
```

So move inward:

```text
Index:   0   1   2   3   4
Char:    r   a   d   a   r
             ↑       ↑
             L       R
```

Compare:

```text
a == a
```

Move again:

```text
Index:   0   1   2   3   4
Char:    r   a   d   a   r
                 ↑
                L/R
```

Nothing failed.

Therefore:

```text
"radar" is a palindrome
```

---

# 6. Palindrome Python code

```python
def is_palindrome(text):
    left = 0
    right = len(text) - 1

    while left < right:
        if text[left] != text[right]:
            return False

        left += 1
        right -= 1

    return True
```

Tests:

```python
print(is_palindrome("radar"))
# True

print(is_palindrome("hello"))
# False

print(is_palindrome(""))
# True

print(is_palindrome("a"))
# True
```

---

# 7. Why does palindrome use `left < right`?

Suppose:

```text
radar
```

Eventually both pointers reach the middle character.

```text
r a d a r
    ↑
   L/R
```

Do we need to compare the middle character with itself?

No.

So:

```python
while left < right:
```

is enough.

When:

```text
left == right
```

we can stop.

---

# 8. Palindrome complexity

Each pointer moves through roughly half the string.

Overall, each character is examined at most once as part of a comparison.

Therefore:

```text
Time Complexity: O(n)
```

We only use:

```text
left
right
```

and no reversed string.

Therefore:

```text
Extra Space Complexity: O(1)
```

Compare that with:

```python
text == text[::-1]
```

which is also O(n) time but needs:

```text
O(n) extra space
```

for the reversed string.

This demonstrates today's connection:

> Sometimes two pointers improve **space complexity** even when time complexity stays the same.

---

# 9. Brute force vs two pointers

Let's consider another kind of problem.

Suppose:

```python
nums = [1, 2, 4, 6, 8, 9]
target = 10
```

We want to know whether two numbers add to `10`.

Possible answer:

```text
2 + 8 = 10
```

---

## Brute-force thinking

The simplest idea:

```text
Try every pair.
```

Conceptually:

```text
1 + 2
1 + 4
1 + 6
1 + 8
1 + 9

2 + 4
2 + 6
2 + 8
...
```

Code:

```python
def has_pair(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return True

    return False
```

Complexity:

```text
Time: O(n²)
Space: O(1)
```

Correct, but potentially slow.

---

# 10. Sorted-array advantage

Now notice something important:

```python
nums = [1, 2, 4, 6, 8, 9]
```

The array is **sorted**.

That gives us information.

Start with:

```text
smallest value
+
largest value
```

Visualization:

```text
Index:   0   1   2   3   4   5
Value:   1   2   4   6   8   9
         ↑                   ↑
         L                   R
```

Calculate:

```text
1 + 9 = 10
```

We immediately found the target.

Let's use an example where we have to move pointers.

---

# 11. Sorted-array example

```python
nums = [1, 2, 4, 6, 8, 9]
target = 12
```

Start:

```text
1 + 9 = 10
```

But:

```text
10 < 12
```

We need a **larger sum**.

Because the array is sorted, moving `left` to the right gives us a larger number.

So:

```text
Index:   0   1   2   3   4   5
Value:   1   2   4   6   8   9
             ↑               ↑
             L               R
```

Now:

```text
2 + 9 = 11
```

Still too small.

Move `left` again:

```text
4 + 9 = 13
```

Now:

```text
13 > 12
```

The sum is too large.

To make it smaller, move `right` left.

Now:

```text
4 + 8 = 12
```

Found.

---

# 12. Why does this work?

Because the array is sorted.

If:

```text
current sum < target
```

we need a bigger number.

So:

```python
left += 1
```

If:

```text
current sum > target
```

we need a smaller number.

So:

```python
right -= 1
```

If:

```text
current sum == target
```

we found the pair.

This logic depends on sorted order.

If the array were:

```python
[8, 1, 9, 2, 4, 6]
```

the same movement logic would not be reliable.

---

# 13. Sorted pair Python code

```python
def has_pair_with_sum(nums, target):
    left = 0
    right = len(nums) - 1

    while left < right:
        current_sum = nums[left] + nums[right]

        if current_sum == target:
            return True

        if current_sum < target:
            left += 1
        else:
            right -= 1

    return False
```

Example:

```python
print(has_pair_with_sum([1, 2, 4, 6, 8, 9], 12))
```

Output:

```text
True
```

---

# 14. Complexity improvement

Brute force:

```text
Check every pair

Time: O(n²)
Space: O(1)
```

Two pointers on a **sorted array**:

```text
Move each pointer across the array at most once

Time: O(n)
Space: O(1)
```

That's a major improvement.

Notice something interesting:

Yesterday, for Two Sum, hashing gave approximately:

```text
Time: O(n)
Space: O(n)
```

Today, if the input is already sorted, two pointers can give:

```text
Time: O(n)
Space: O(1)
```

So input structure matters.

---

# 15. Hashing vs two pointers

Suppose the array is unsorted:

```python
nums = [8, 2, 7, 1]
```

Hashing can work directly:

```text
Time: O(n) average
Space: O(n)
```

Two pointers don't have the useful sorted-order guarantee yet.

You could sort first, but that introduces other considerations and may affect original indexes.

For a sorted array:

```python
nums = [1, 2, 7, 8]
```

two pointers become very attractive.

A useful early mental model:

```text
Unsorted + fast lookup
→ think hashing

Sorted + pair relationship
→ think two pointers
```

Not an absolute rule, but an excellent starting signal.

---

# 16. Two pointers moving in the same direction

Not all two pointers start at opposite ends.

Consider:

```python
nums = [1, 1, 2, 2, 3]
```

Imagine we eventually want to keep unique values together.

We might have:

```text
1  1  2  2  3
↑
L
   ↑
   R
```

One pointer can represent:

```text
where to write
```

while another represents:

```text
what we are currently reading
```

Then both move toward the right.

This pattern becomes important later in:

```text
remove duplicates
move zeros
filter arrays
sliding window
```

For Day 215, simply recognize:

> Two pointers do not always mean one starts at each end.

---

# 17. Guided Problem — Reverse a list in place

## Problem

Given:

```python
nums = [1, 2, 3, 4, 5]
```

modify it so it becomes:

```python
[5, 4, 3, 2, 1]
```

Do not create another list.

---

# 18. Thought process

We need to swap:

```text
first ↔ last
second ↔ second-last
```

That strongly suggests:

```text
left pointer
right pointer
```

Start:

```text
1   2   3   4   5
↑               ↑
L               R
```

Swap:

```text
5   2   3   4   1
```

Move inward:

```text
5   2   3   4   1
    ↑       ↑
    L       R
```

Swap:

```text
5   4   3   2   1
```

Now pointers meet around the middle.

Stop.

---

# 19. Guided pseudocode

```text
set left to first index
set right to last index

while left is before right:
    swap values at left and right
    move left one step right
    move right one step left
```

---

# 20. Guided Python solution

```python
def reverse_list(nums):
    left = 0
    right = len(nums) - 1

    while left < right:
        nums[left], nums[right] = nums[right], nums[left]

        left += 1
        right -= 1
```

Test:

```python
nums = [1, 2, 3, 4, 5]

reverse_list(nums)

print(nums)
```

Output:

```text
[5, 4, 3, 2, 1]
```

---

# 21. Guided problem complexity

Each swap moves both pointers inward.

So:

```text
Time Complexity: O(n)
```

No second list is created.

Therefore:

```text
Extra Space Complexity: O(1)
```

---

# 22. Edge cases for reverse

Empty list:

```python
[]
```

No problem.

One element:

```python
[5]
```

Already reversed.

Two elements:

```python
[1, 2]
```

becomes:

```python
[2, 1]
```

Odd number of values:

```python
[1, 2, 3, 4, 5]
```

The middle element:

```text
3
```

doesn't need to move.

---

# 23. Independent Problem 1 — Valid Palindrome

You know the basic palindrome pattern already.

Now solve it yourself using two pointers.

## Problem

Return `True` if a string reads the same forward and backward.

For this problem:

```text
Comparison is case-sensitive.
Spaces count as characters.
```

Examples:

```python
"level"   # True
"python"  # False
"a"       # True
""        # True
"Level"   # False
```

Write:

```python
def is_palindrome(text):
    # your code
```

Before Python code, give me:

```text
Thought process
Pseudocode
Python
Time Complexity
Space Complexity
```

Do **not** use:

```python
text[::-1]
```

The goal is to practice two pointers.

I am intentionally not providing the solution here.

---

# 24. Independent Problem 2 — Pair Sum in Sorted Array

## Problem

You are given a **sorted** list:

```python
nums = [1, 2, 3, 4, 6]
target = 6
```

Determine whether two different elements add up to `target`.

Here:

```text
2 + 4 = 6
```

so the answer is:

```text
True
```

Write:

```python
def has_pair_sum(nums, target):
    # your code
```

Tests:

```python
print(has_pair_sum([1, 2, 3, 4, 6], 6))
# True

print(has_pair_sum([1, 2, 4, 8], 20))
# False

print(has_pair_sum([2, 3], 5))
# True

print(has_pair_sum([5], 10))
# False

print(has_pair_sum([], 5))
# False
```

Important:

```text
The list is already sorted.
You cannot use the same element twice.
```

Again provide:

```text
Thought process
Pseudocode
Python code
Time Complexity
Space Complexity
```

Do not use a set or dictionary for this exercise.

---

# 25. Common mistake — forgetting to move pointers

This is dangerous:

```python
while left < right:
    if nums[left] == nums[right]:
        pass
```

If neither pointer changes, the loop keeps examining the same positions forever.

You can create an infinite loop.

Usually something inside the loop must eventually do:

```python
left += 1
```

or:

```python
right -= 1
```

or both.

---

# 26. Common mistake — moving the wrong pointer

In a sorted pair-sum problem:

```text
current_sum < target
```

means:

```text
sum is too small
```

So we need to increase it.

Because the array is sorted:

```python
left += 1
```

moves toward a larger value.

But if you accidentally do:

```python
right -= 1
```

you usually make the sum even smaller.

Likewise:

```text
current_sum > target
```

means:

```python
right -= 1
```

to reduce the sum.

Remember:

```text
Too small → move left rightward
Too large → move right leftward
```

for the standard sorted-array pair-sum pattern.

---

# 27. Common mistake — using `left <= right`

For problems requiring **two different elements**, this can be dangerous.

Suppose:

```python
nums = [5]
target = 10
```

If you allow:

```python
left <= right
```

then:

```text
left = right = 0
```

and you might incorrectly calculate:

```text
5 + 5 = 10
```

using the same element twice.

For pair problems with distinct positions, this is commonly safer:

```python
while left < right:
```

---

# 28. Common mistake — assuming two pointers work on every pair-sum problem

This movement:

```python
if current_sum < target:
    left += 1
else:
    right -= 1
```

depends on the array being sorted.

Without sorted order, moving one pointer does not give predictable information.

Always ask:

> Is there some ordering or structure that tells me which pointer to move?

If not, another approach such as hashing may be better.

---

# 29. Common mistake — sorting without considering the problem

Suppose a problem asks for the original indexes.

You might think:

```python
nums.sort()
```

then use two pointers.

But sorting changes the positions.

Example:

```text
Original:
[8, 2, 5]

Indexes:
 0  1  2
```

After sorting:

```text
[2, 5, 8]
```

Those positions are no longer the original indexes.

So before sorting, ask:

> Do I need to preserve original order or indexes?

This is particularly important in Two Sum.

---

# 30. Common mistake — confusing pointer with value

Suppose:

```python
nums = [10, 20, 30]
left = 0
```

`left` contains:

```text
0
```

not:

```text
10
```

To get the value:

```python
nums[left]
```

So keep this distinction clear:

```text
left
→ index

nums[left]
→ value at that index
```

---

# 31. How to decide pointer updates

This is one of the most important skills in two-pointer problems.

Don't randomly move pointers.

Ask:

> What does moving this pointer change?

In a sorted list:

```text
Moving left rightward
→ usually increases the left-side value

Moving right leftward
→ usually decreases the right-side value
```

That's why pair-sum logic works.

For palindrome:

```text
After the outside characters match,
we no longer need them.

So move both inward.
```

Every pointer movement should have a reason.

---

# 32. Brute force before two pointers

Continue the habit from Day 214.

Suppose you're asked:

> Find whether a sorted array contains two values whose sum equals target.

First think:

```text
Brute force:
try every pair
```

Complexity:

```text
O(n²)
```

Then ask:

> What property can I exploit?

Answer:

```text
The array is sorted.
```

That allows:

```text
left + right
```

and controlled pointer movement.

Result:

```text
O(n)
```

That reasoning is more important than memorizing the final code.

---

# 33. Recognition signals for two pointers

When you see phrases such as:

```text
sorted array
pair of values
two numbers sum to...
palindrome
reverse in place
compare from both ends
first and last
remove duplicates
move values
in-place
very little extra space
```

ask:

> Can I use two positions that move through the input instead of repeatedly searching?

A particularly strong signal is:

```text
sorted array + pair condition
```

Think:

```text
left + right pointers
```

Another strong signal:

```text
compare beginning and end
```

Think:

```text
pointers moving toward each other
```

And later, when you see:

```text
read position + write position
```

think:

```text
two pointers moving in the same direction
```

---

# Day 215 mental model

Keep these three templates in your head.

### Opposite ends

```python
left = 0
right = len(nums) - 1

while left < right:
    # inspect nums[left] and nums[right]

    left += 1
    right -= 1
```

Useful when both sides can be discarded after processing.

### Sorted pair sum

```text
sum too small
→ move left right

sum too large
→ move right left

sum matches
→ answer found
```

### Same direction

```text
one pointer reads
another pointer tracks another useful position
```

You'll use that more in upcoming array and sliding-window problems.

---

## Day 215 assignment

Solve both independent problems without checking a ready-made solution:

```text
1. is_palindrome(text)
2. has_pair_sum(nums, target)
```

For **each problem**, send me your work in this exact order:

```text
1. Thought process
2. Pseudocode
3. Python code
4. Time Complexity
5. Space Complexity
```

For the sorted pair problem, also explain in one sentence **why `left` moves when the sum is too small and `right` moves when the sum is too large**. That explanation will show whether you genuinely understand the two-pointer technique rather than just memorizing the code.