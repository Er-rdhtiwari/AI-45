# Day 213 — Strings for DSA

**Connection:** Arrays taught you **indexed traversal**. Strings use many of the same ideas.

If you understand:

```python
nums[i]
```

then this will feel familiar:

```python
text[i]
```

Today your goal is to become comfortable treating a string as a sequence of characters.

---

# 1. What is a string?

A string is a sequence of characters.

```python
text = "hello"
```

You can visualize it like this:

```text
Index:   0   1   2   3   4
         ↓   ↓   ↓   ↓   ↓
Char:    h   e   l   l   o
```

Like arrays/lists, string indexing starts at `0`.

```python
text = "hello"

print(text[0])
print(text[1])
print(text[4])
```

Output:

```text
h
e
o
```

Direct character access by index is treated as:

```text
Time Complexity: O(1)
```

---

# 2. Character indexing

Given:

```python
word = "python"
```

Indexes:

```text
p  y  t  h  o  n
0  1  2  3  4  5
```

So:

```python
print(word[0])
```

Output:

```text
p
```

And:

```python
print(word[5])
```

Output:

```text
n
```

The last index is:

```python
len(word) - 1
```

For `"python"`:

```text
len(word) = 6

last index = 5
```

You can therefore write:

```python
print(word[len(word) - 1])
```

Output:

```text
n
```

---

# 3. Negative indexing

Python also supports negative indexing.

```python
word = "python"

print(word[-1])
print(word[-2])
```

Output:

```text
n
o
```

Mental model:

```text
 p   y   t   h   o   n
 0   1   2   3   4   5
-6  -5  -4  -3  -2  -1
```

For DSA, both styles are useful:

```python
word[len(word) - 1]
```

and:

```python
word[-1]
```

But understanding `len(word) - 1` is especially important because it transfers to arrays and many other problems.

---

# 4. String traversal

Exactly like lists, you can traverse strings by value.

```python
text = "hello"

for char in text:
    print(char)
```

Output:

```text
h
e
l
l
o
```

This is:

```text
O(n)
```

because every character is visited once.

---

## Traversing using indexes

```python
text = "hello"

for i in range(len(text)):
    print(i, text[i])
```

Output:

```text
0 h
1 e
2 l
3 l
4 o
```

Use this when the position matters.

---

# 5. String immutability

This is one major difference between Python strings and lists.

Suppose:

```python
text = "hello"
```

You may try:

```python
text[0] = "H"
```

This causes an error.

Why?

Because Python strings are **immutable**.

Immutable means:

> Once a string object is created, individual characters inside that string cannot be changed directly.

So this is not allowed:

```python
text[0] = "H"
```

But this is allowed:

```python
text = "Hello"
```

because you are making `text` refer to a different string.

---

# 6. Why are strings immutable?

At a beginner level, think of a Python string as a completed value.

```python
"hello"
```

Python does not allow you to directly change one position inside it.

If you want a changed string, you create another string.

For example:

```python
text = "hello"

new_text = "H" + text[1:]

print(new_text)
```

Output:

```text
Hello
```

We created a new string instead of modifying the old one.

This matters in DSA because repeated string creation can cost extra time and memory.

We will explore that more deeply later.

---

# 7. String vs list

Compare these:

## List

```python
nums = [10, 20, 30]

nums[0] = 100

print(nums)
```

Output:

```text
[100, 20, 30]
```

Lists are mutable.

---

## String

```python
text = "cat"

text[0] = "b"
```

This is invalid.

You cannot turn `"cat"` into `"bat"` by modifying `text[0]`.

Instead:

```python
text = "cat"

new_text = "b" + text[1:]

print(new_text)
```

Output:

```text
bat
```

---

# 8. String and list operation comparison

| Operation | String | List |
|---|---|---|
| Indexing | Yes | Yes |
| Traversal | Yes | Yes |
| Slicing | Yes | Yes |
| `len()` | Yes | Yes |
| Direct element update | No | Yes |
| Mutable | No | Yes |
| Can contain duplicates | Yes | Yes |

The biggest beginner takeaway:

```text
List   → mutable
String → immutable
```

---

# 9. String slicing

Slicing extracts part of a string.

Syntax:

```python
text[start:end]
```

Important:

```text
start is included
end is excluded
```

Example:

```python
text = "python"

print(text[0:3])
```

Output:

```text
pyt
```

Why not `"pyth"`?

Because index `3` is excluded.

Indexes:

```text
p y t h o n
0 1 2 3 4 5
```

So:

```python
text[0:3]
```

takes:

```text
0
1
2
```

---

## More slicing examples

```python
text = "python"

print(text[:3])
```

Output:

```text
pyt
```

Meaning:

```text
start from beginning
stop before index 3
```

---

```python
print(text[3:])
```

Output:

```text
hon
```

Meaning:

```text
start at index 3
continue to the end
```

---

# 10. Reversing a string using slicing

Python gives us a convenient way:

```python
text = "hello"

reversed_text = text[::-1]

print(reversed_text)
```

Output:

```text
olleh
```

The important part is:

```python
[::-1]
```

It means traverse the string backwards.

For now, you can remember:

```python
text[::-1]
```

as:

> Create a reversed copy of the string.

Because it creates a new string of `n` characters:

```text
Time: O(n)
Space: O(n)
```

---

# 11. String comparison

Strings can be compared using:

```python
==
```

Example:

```python
a = "hello"
b = "hello"

print(a == b)
```

Output:

```text
True
```

But comparison is case-sensitive.

```python
print("hello" == "Hello")
```

Output:

```text
False
```

because:

```text
h
```

and:

```text
H
```

are different characters.

---

# 12. Uppercase and lowercase

You can normalize strings using:

```python
.lower()
```

Example:

```python
text = "Hello"

print(text.lower())
```

Output:

```text
hello
```

Or:

```python
text.upper()
```

Output:

```text
HELLO
```

This becomes important in questions where:

```text
"A"
```

and:

```text
"a"
```

should be treated as equal.

---

# 13. Counting characters

Suppose:

```python
text = "banana"
```

You want to count how many times `"a"` appears.

Use the same counting pattern you learned for arrays.

```python
text = "banana"

count = 0

for char in text:
    if char == "a":
        count += 1

print(count)
```

Output:

```text
3
```

This is the exact same DSA pattern:

```python
count = 0

for item in sequence:
    if condition:
        count += 1
```

Only the sequence changed from an array to a string.

---

# 14. Complexity of character counting

For:

```python
for char in text:
```

every character may be inspected.

Therefore:

```text
Time Complexity: O(n)
```

We only keep:

```text
count
char
```

Therefore:

```text
Extra Space Complexity: O(1)
```

---

# 15. Simple string reversal

There are several ways.

For today, know two.

## Method 1 — Slicing

```python
text = "hello"

reversed_text = text[::-1]

print(reversed_text)
```

Output:

```text
olleh
```

---

## Method 2 — Build a result

```python
text = "hello"

result = ""

for char in text:
    result = char + result

print(result)
```

Output:

```text
olleh
```

Conceptually:

```text
result = ""

h → "h"
e → "eh"
l → "leh"
l → "lleh"
o → "olleh"
```

This is easy to understand, although repeated string concatenation is not usually the most efficient Python approach for large strings.

For today's lesson, understanding the logic matters more.

---

# 16. Palindrome

A **palindrome** is a string that reads the same forward and backward.

Examples:

```text
madam
racecar
level
```

Not palindrome:

```text
hello
python
```

---

# 17. Brute-force thinking first

Before thinking about optimization, ask:

> How would I solve this in the simplest possible way?

For palindrome checking:

```text
Original:
madam

Reverse:
madam
```

If:

```text
original == reversed
```

then it is a palindrome.

This gives us a very simple approach.

---

# 18. Simple palindrome solution

```python
def is_palindrome(text):
    reversed_text = text[::-1]

    if text == reversed_text:
        return True

    return False
```

Test:

```python
print(is_palindrome("madam"))
print(is_palindrome("hello"))
```

Output:

```text
True
False
```

You could also shorten it:

```python
def is_palindrome(text):
    return text == text[::-1]
```

But when you're learning DSA, I recommend understanding the longer version first.

---

# 19. Palindrome complexity

Suppose the string contains `n` characters.

Creating:

```python
text[::-1]
```

requires creating a reversed string.

So approximately:

```text
Time: O(n)
Space: O(n)
```

Then comparison may also inspect characters.

That's another O(n) operation.

So conceptually:

```text
O(n) + O(n)
```

which simplifies to:

```text
O(n)
```

Remember yesterday's lesson:

```text
n + n = 2n

Big-O → O(n)
```

---

# 20. Could palindrome use less space?

Yes.

Instead of creating an entire reversed string, we could compare characters from both ends.

For example:

```text
racecar

r       r
 ↑     ↑

 a     a
  ↑   ↑

   c c
   ↑ ↑
```

This can use:

```text
O(1) extra space
```

But that introduces the **two-pointer pattern**, which you don't need to study deeply today.

For Day 213, the important lesson is:

> First get a correct brute-force solution. Then ask whether unnecessary memory or work can be removed.

That thinking process matters more than immediately producing the optimal solution.

---

# 21. Spaces

Strings can contain spaces.

Example:

```python
text = "hello world"
```

A space is also a character.

For example:

```python
print(len("a b"))
```

Output:

```text
3
```

because the characters are:

```text
'a'
' '
'b'
```

So when solving string problems, always ask:

> Do spaces count?

The problem statement should tell you.

---

# 22. Case sensitivity

Consider:

```text
Madam
```

If we compare it directly with its reverse:

```text
Madam
madaM
```

they are different.

So:

```python
"Madam" == "madaM"
```

is:

```text
False
```

But if the problem says:

> Ignore uppercase/lowercase.

you could normalize:

```python
text = text.lower()
```

Now:

```text
Madam
```

becomes:

```text
madam
```

---

# 23. Empty string

An empty string is:

```python
text = ""
```

Its length is:

```python
print(len(text))
```

Output:

```text
0
```

Is an empty string a palindrome?

In most algorithmic definitions:

```text
Yes
```

because reading it forward and backward gives the same result.

Using:

```python
text == text[::-1]
```

we get:

```python
"" == ""
```

which is:

```text
True
```

---

# 24. One-character string

Example:

```python
text = "a"
```

A single character is naturally a palindrome.

```text
Forward = "a"
Backward = "a"
```

So:

```text
True
```

This is an important edge case.

---

# 25. Guided problem — Count vowels

## Problem

Given a string, count the number of vowels.

Vowels:

```text
a
e
i
o
u
```

Example:

```python
text = "hello"
```

Expected answer:

```text
2
```

because:

```text
e
o
```

are vowels.

---

## Step 1 — Thought process

We need:

```text
how many characters satisfy a condition?
```

That should immediately remind you of:

```text
counting pattern
```

Create:

```python
count = 0
```

Then traverse every character.

For every character, ask:

```text
Is this character a vowel?
```

If yes:

```text
count += 1
```

---

# 26. Pseudocode

```text
set count to 0

for every character in text:
    if character is a vowel:
        increase count

return count
```

---

# 27. Python solution

```python
def count_vowels(text):
    count = 0

    for char in text:
        if char in "aeiou":
            count += 1

    return count
```

Test:

```python
print(count_vowels("hello"))
```

Output:

```text
2
```

---

# 28. Uppercase edge case

What happens with:

```python
count_vowels("HELLO")
```

Our current function checks:

```python
if char in "aeiou":
```

But:

```text
E != e
O != o
```

So uppercase vowels won't match.

One solution is:

```python
def count_vowels(text):
    count = 0

    for char in text.lower():
        if char in "aeiou":
            count += 1

    return count
```

Now:

```python
print(count_vowels("HELLO"))
```

returns:

```text
2
```

This demonstrates an important DSA habit:

> Understand exactly what the problem says about case sensitivity.

Don't automatically lowercase strings unless the requirement says case should be ignored.

---

# 29. Complexity of the guided problem

We inspect each character once.

Therefore:

```text
Time Complexity: O(n)
```

The main counting variable uses constant extra memory.

For beginner analysis, we can describe the traversal itself as:

```text
Extra Space: O(1)
```

If you explicitly create a lowercase copy first, such as:

```python
lower_text = text.lower()
```

then that copy itself occupies O(n) memory.

We'll become more precise about such Python implementation details as your DSA foundation grows.

---

# 30. Independent Problem 1 — Count a target character

Do this yourself.

## Problem

Given:

```python
text = "banana"
target = "a"
```

return how many times `target` appears.

Expected:

```text
3
```

Write:

```python
def count_character(text, target):
    # your code
```

Test cases:

```python
print(count_character("banana", "a"))
# Expected: 3

print(count_character("hello", "l"))
# Expected: 2

print(count_character("python", "z"))
# Expected: 0

print(count_character("", "a"))
# Expected: 0

print(count_character("AaaA", "A"))
# Expected: 2
```

For this problem, treat uppercase and lowercase as different.

So:

```text
A != a
```

Do **not** use:

```python
text.count(target)
```

The purpose is to practice traversal.

For this problem, send me:

```text
1. Thought process
2. Pseudocode
3. Python code
4. Time Complexity
5. Space Complexity
```

I am intentionally not giving the solution yet.

---

# 31. Independent Problem 2 — Check whether first and last characters match

## Problem

Given a string, return `True` if its first and last characters are the same.

Example:

```python
text = "radar"
```

Expected:

```text
True
```

Because:

```text
first = r
last  = r
```

Another example:

```python
text = "hello"
```

Expected:

```text
False
```

because:

```text
h != o
```

Write:

```python
def same_first_last(text):
    # your code
```

Use these rules:

```text
Empty string → False
One character → True
Comparison is case-sensitive
Spaces count as characters
```

Tests:

```python
print(same_first_last("radar"))
# True

print(same_first_last("hello"))
# False

print(same_first_last("a"))
# True

print(same_first_last(""))
# False

print(same_first_last("AbA"))
# True

print(same_first_last("aba "))
# False
```

Again, provide:

```text
1. Thought process
2. Pseudocode
3. Python code
4. Time Complexity
5. Space Complexity
```

Do not worry about clever tricks.

---

# 32. Important complexity question

Look at:

```python
text = "python"

print(text[2])
```

What is the time complexity?

Think carefully.

We don't traverse the string.

We directly access one position.

Therefore:

```text
O(1)
```

Now compare:

```python
for char in text:
    print(char)
```

This visits all characters.

Therefore:

```text
O(n)
```

This is exactly the same distinction you learned with arrays.

---

# 33. Common beginner mistake — trying to modify a character

Incorrect:

```python
text = "hello"

text[0] = "H"
```

Strings are immutable.

Instead, create a new string.

```python
text = "hello"

text = "H" + text[1:]
```

---

# 34. Common mistake — index out of range

Suppose:

```python
text = "cat"
```

Valid indexes:

```text
0
1
2
```

This is invalid:

```python
print(text[3])
```

because:

```text
len(text) = 3
```

but:

```text
last index = 2
```

Remember:

```text
last index = len(text) - 1
```

---

# 35. Common mistake — forgetting case sensitivity

This:

```python
"A" == "a"
```

is:

```text
False
```

Don't lowercase everything automatically.

First understand whether the problem says:

```text
case-sensitive
```

or:

```text
case-insensitive
```

---

# 36. Common mistake — ignoring spaces

Suppose:

```python
text = "a a"
```

Characters are:

```text
'a'
' '
'a'
```

Length:

```text
3
```

The space occupies a position too.

---

# 37. Common mistake — wrong slicing boundary

Suppose:

```python
text = "abcdef"
```

You want:

```text
abc
```

Correct:

```python
text[0:3]
```

because index `3` is excluded.

A beginner often expects:

```python
text[0:2]
```

to produce `"abc"`.

But it produces:

```text
ab
```

Remember:

> Slice end is excluded.

---

# 38. Common mistake — reversing and forgetting extra memory

This is very convenient:

```python
reversed_text = text[::-1]
```

But it creates another string.

So although the code is short, it is not necessarily:

```text
O(1) extra space
```

Short code does not automatically mean low complexity.

This is an important DSA lesson.

---

# 39. Common mistake — solving before understanding requirements

Suppose the question says:

> Is `"A man a plan"` a palindrome ignoring spaces and case?

That is different from asking:

> Is the exact string a palindrome?

Requirements like:

```text
ignore spaces
ignore punctuation
ignore uppercase/lowercase
```

change the problem.

Always identify those rules before coding.

---

# 40. Brute force before optimization

From today onward, build this habit:

```text
Step 1:
Understand input and expected output

Step 2:
Think of the simplest correct solution

Step 3:
Write the solution

Step 4:
Analyze time and space complexity

Step 5:
Ask whether work or memory can be reduced
```

For palindrome:

### Simple approach

```text
reverse entire string
compare
```

Complexity:

```text
Time: O(n)
Space: O(n)
```

Later:

```text
compare left side and right side directly
```

can reduce extra memory.

The important point is not:

> "I must immediately know the optimal solution."

The better habit is:

> "First make it correct. Then understand where inefficiency comes from."

---

# 41. String-problem recognition signals

When you see certain phrases, start associating them with certain ideas.

If the problem says:

```text
How many times does...
Count occurrences...
Count vowels...
```

Think:

```text
Traversal + counter
```

---

If it says:

```text
Palindrome
Same forward and backward
```

Think:

```text
Reverse and compare

or later:
two ends moving inward
```

---

If it says:

```text
First character
Last character
Character at position...
```

Think:

```text
Indexing
```

Usually:

```text
O(1)
```

---

If it says:

```text
Every character
For each character
Count characters satisfying...
```

Think:

```text
Traversal
O(n)
```

---

If it says:

```text
substring
part of the string
characters from index X to Y
```

Think:

```text
Slicing
```

---

If it says:

```text
Ignore uppercase/lowercase
```

Think:

```python
.lower()
```

or:

```python
.upper()
```

---

If it says:

```text
Modify individual characters
```

Remember:

```text
Python strings are immutable.
```

You may need to create another string or later convert to another structure such as a list.

---

# Day 213 mental model

Keep these six ideas in your head:

```text
1. String = sequence of characters.

2. text[i] gives a character.

3. Traversing every character is O(n).

4. Strings cannot be changed character-by-character.

5. Count problems usually need:
   counter + traversal.

6. Palindrome:
   simplest thinking = reverse + compare.
```

And for every string problem, start asking:

```text
Does case matter?

Do spaces matter?

Can the string be empty?

Can it contain only one character?

Do I need an index or only the character?

Am I creating another string?
```

## Your Day 213 practice

Solve these two without looking for a ready-made function:

```text
Problem 1:
count_character(text, target)

Problem 2:
same_first_last(text)
```

For **each one**, write:

```text
Thought process
→ Pseudocode
→ Python code
→ Time complexity
→ Space complexity
```

That reasoning sequence is the main skill we are building in the first part of your 90-day DSA specialization.