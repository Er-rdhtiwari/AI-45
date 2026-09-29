# Day 214 — Hash Maps and Sets for DSA

**Connection:** Yesterday you solved string problems using traversal. Today you will learn how **fast lookup** can improve some of those solutions.

The big idea for today is:

> Instead of repeatedly searching through an array, sometimes we can **remember what we have already seen**.

In Python, the two main tools for that are:

```python
dict
set
```

Your Day 214 goal is to recognize when a problem is really asking:

```text
Have I seen this before?
How many times have I seen this?
Does this value exist?
```

Those are strong signals for hashing.

---

## 1. What is a dictionary?

A Python dictionary stores information as:

```text
key → value
```

Example:

```python
person = {
    "name": "Rahul",
    "age": 30
}
```

Here:

```text
"name" → "Rahul"
"age"  → 30
```

The left side is the **key**.

The right side is the **value**.

You retrieve a value using its key:

```python
print(person["name"])
```

Output:

```text
Rahul
```

For DSA, dictionaries are especially useful when we want to remember information about values.

For example:

```python
frequency = {
    "a": 3,
    "b": 1,
    "c": 2
}
```

This could mean:

```text
"a" appeared 3 times
"b" appeared 1 time
"c" appeared 2 times
```

---

# 2. What is a set?

A set stores **unique values**.

Example:

```python
seen = {10, 20, 30}
```

Unlike a dictionary, a set doesn't need a separate value associated with each item.

It mainly answers questions such as:

```text
Is 20 present?
Have I seen 50 before?
```

Example:

```python
seen = {10, 20, 30}

print(20 in seen)
print(50 in seen)
```

Output:

```text
True
False
```

A useful mental model is:

```text
dictionary:
value → some information about value

set:
just remember whether value exists
```

---

# 3. Average O(1) lookup

This is the main reason dictionaries and sets are important in DSA.

Consider:

```python
seen = {10, 20, 30, 40, 50}

if 30 in seen:
    print("Found")
```

Checking:

```python
30 in seen
```

is **O(1) average time**.

That means Python can usually determine whether the value exists without checking every element one by one.

The same is true for dictionary keys:

```python
frequency = {
    "a": 4,
    "b": 2
}

print(frequency["a"])
```

Dictionary lookup is also:

```text
O(1) average
```

Important wording:

> We normally say **average O(1)** for hash-table lookup.

You do not need to study hash-table internals yet.

---

# 4. Compare that with a list

Suppose:

```python
nums = [10, 20, 30, 40, 50]
```

And you ask:

```python
30 in nums
```

Python may need to scan:

```text
10
20
30
```

And if you're looking for something missing:

```python
100 in nums
```

it may inspect the whole list.

Therefore list membership is generally:

```text
O(n)
```

Compare:

```text
List membership:
x in nums
→ O(n)

Set membership:
x in seen
→ O(1) average

Dictionary-key lookup:
x in freq
→ O(1) average
```

This difference becomes very important in DSA.

---

# 5. When is a dictionary useful?

Use a dictionary when simply knowing that something exists is **not enough**.

You need additional information.

For example:

> How many times did each number appear?

Given:

```python
nums = [2, 3, 2, 5, 3, 2]
```

We want:

```text
2 → 3 times
3 → 2 times
5 → 1 time
```

A dictionary is perfect:

```python
frequency = {
    2: 3,
    3: 2,
    5: 1
}
```

The key is the number.

The value is its count.

This is called a **frequency map**.

---

# 6. When is a set enough?

Imagine the problem asks:

> Does this array contain any duplicate?

Given:

```python
nums = [5, 2, 8, 2]
```

You don't really care that `2` appears:

```text
2 times
```

You only care:

```text
Have I already seen 2?
```

That's a set problem.

You could maintain:

```python
seen = set()
```

Then as you traverse:

```text
5 → not seen → add 5
2 → not seen → add 2
8 → not seen → add 8
2 → already seen!
```

Duplicate found.

No frequency dictionary is required.

---

# 7. Creating dictionaries and sets

Empty dictionary:

```python
frequency = {}
```

or:

```python
frequency = dict()
```

Empty set:

```python
seen = set()
```

Be careful:

```python
seen = {}
```

does **not** create a set.

It creates an empty dictionary.

So:

```text
{}      → dictionary
set()   → set
```

This is a common Python beginner mistake.

---

# 8. Adding values to a set

```python
seen = set()

seen.add(10)
seen.add(20)
seen.add(30)

print(seen)
```

The exact printed order of a set shouldn't be something your algorithm relies on.

What matters is that:

```python
10 in seen
```

works efficiently.

---

# 9. Adding information to a dictionary

Start:

```python
frequency = {}
```

You can add:

```python
frequency["a"] = 1
```

Now:

```python
print(frequency)
```

Conceptually:

```text
{"a": 1}
```

Then:

```python
frequency["a"] = 2
```

Now the value associated with `"a"` becomes `2`.

This ability to repeatedly update a value is exactly what we need for frequency counting.

---

# 10. The frequency-map pattern

Suppose:

```python
text = "banana"
```

We want the frequency of every character.

Expected:

```text
b → 1
a → 3
n → 2
```

Start:

```python
frequency = {}
```

Then traverse:

```python
for char in text:
```

For every character there are two possibilities.

### Character already exists

Increment its count:

```python
frequency[char] += 1
```

### Character doesn't exist yet

Start its count at `1`:

```python
frequency[char] = 1
```

Complete version:

```python
text = "banana"

frequency = {}

for char in text:
    if char in frequency:
        frequency[char] += 1
    else:
        frequency[char] = 1

print(frequency)
```

Result:

```text
{
    'b': 1,
    'a': 3,
    'n': 2
}
```

This pattern is extremely important.

---

# 11. Dry run the frequency map

Let's manually process:

```text
banana
```

Initially:

```text
frequency = {}
```

Read `"b"`:

```text
b doesn't exist

frequency = {
    "b": 1
}
```

Read `"a"`:

```text
frequency = {
    "b": 1,
    "a": 1
}
```

Read `"n"`:

```text
frequency = {
    "b": 1,
    "a": 1,
    "n": 1
}
```

Read another `"a"`:

```text
"a" already exists

frequency["a"] += 1
```

Now:

```text
a → 2
```

Continue, and eventually:

```text
b → 1
a → 3
n → 2
```

---

# 12. Frequency-map complexity

Suppose the string contains `n` characters.

We traverse every character once:

```python
for char in text:
```

That's:

```text
O(n)
```

Each dictionary lookup/update is **O(1) average**.

So total time:

```text
O(n)
```

What about space?

In the worst case, every character/value could be different.

For example, imagine `n` distinct items.

Then the dictionary may contain `n` entries.

Therefore:

```text
Space Complexity: O(n)
```

---

# 13. A shorter Python frequency pattern

Python also lets us write:

```python
frequency[char] = frequency.get(char, 0) + 1
```

Example:

```python
text = "banana"

frequency = {}

for char in text:
    frequency[char] = frequency.get(char, 0) + 1

print(frequency)
```

What does:

```python
frequency.get(char, 0)
```

mean?

It means:

> Give me the current value for this key. If the key doesn't exist, give me `0`.

So for the first `"a"`:

```text
current count = 0
0 + 1 = 1
```

Next `"a"`:

```text
current count = 1
1 + 1 = 2
```

For learning, however, make sure you understand the longer:

```python
if char in frequency:
    ...
else:
    ...
```

version first.

---

# 14. Nested-loop lookup

Now let's see why hashing can improve an algorithm.

Problem:

> Does the array contain duplicates?

Consider:

```python
nums = [4, 7, 2, 4]
```

A straightforward brute-force idea is:

> Compare every element against the elements after it.

```python
def contains_duplicate(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True

    return False
```

For each element, we may compare it against many other elements.

So the time complexity is:

```text
O(n²)
```

Extra space:

```text
O(1)
```

because we aren't creating a growing data structure.

This solution is correct.

It's our **brute-force solution**.

---

# 15. Hash-based lookup

Instead of repeatedly searching ahead, ask:

> Can I remember every value I've already seen?

Start:

```python
seen = set()
```

Process:

```text
4 → haven't seen → add
7 → haven't seen → add
2 → haven't seen → add
4 → already in set
```

Duplicate found.

Python:

```python
def contains_duplicate(nums):
    seen = set()

    for num in nums:
        if num in seen:
            return True

        seen.add(num)

    return False
```

Now each lookup is O(1) average.

We traverse `n` values.

So:

```text
Time: O(n)
Space: O(n)
```

Notice the trade-off:

```text
Brute force:
Time  O(n²)
Space O(1)

Hash set:
Time  O(n) average
Space O(n)
```

We used additional memory to reduce runtime.

This is one of the most important recurring DSA trade-offs.

---

# 16. Don't assume hashing is always "better"

Suppose someone asks:

> Which algorithm is better?

Don't automatically say the hash solution.

Instead understand the trade-off.

The nested-loop solution uses:

```text
less memory
```

but can take much longer.

The set solution uses:

```text
more memory
```

but usually runs much faster for large inputs.

Interviewers commonly want you to recognize this trade-off.

---

# 17. Guided Problem 1 — Character Frequency

## Problem

Given:

```python
text = "apple"
```

create a frequency map of its characters.

Expected idea:

```text
a → 1
p → 2
l → 1
e → 1
```

---

## Step 1 — Thought process

Ask:

> Do I simply need to know whether a character exists?

No.

We need:

```text
character → number of occurrences
```

So a set is not enough.

We need a:

```text
dictionary
```

---

## Step 2 — Pseudocode

```text
create empty frequency dictionary

for every character:
    if character already exists:
        increase its count
    otherwise:
        set its count to 1

return frequency dictionary
```

---

## Step 3 — Python

```python
def character_frequency(text):
    frequency = {}

    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    return frequency
```

Test:

```python
print(character_frequency("apple"))
```

Result:

```text
{
    'a': 1,
    'p': 2,
    'l': 1,
    'e': 1
}
```

---

## Complexity

Every character is visited once:

```text
Time Complexity: O(n)
```

The dictionary can contain up to `n` different keys:

```text
Space Complexity: O(n)
```

---

## Edge cases

Empty:

```python
character_frequency("")
```

Result:

```text
{}
```

One character:

```python
character_frequency("a")
```

Result:

```text
{'a': 1}
```

Repeated same character:

```python
character_frequency("aaaa")
```

Result:

```text
{'a': 4}
```

Case-sensitive:

```python
character_frequency("Aa")
```

would treat:

```text
A
a
```

as different keys unless the problem tells you otherwise.

---

# 18. Guided Problem 2 — Duplicate Detection

## Problem

Given an integer array, return `True` if any value occurs more than once.

Example:

```python
nums = [3, 1, 4, 1]
```

Expected:

```text
True
```

because:

```text
1
```

appears twice.

---

## Step 1 — What information do we need?

Do we need:

```text
1 appeared exactly 2 times?
```

No.

All we need is:

```text
Have I seen this number before?
```

Therefore a:

```text
set
```

is enough.

---

## Step 2 — Pseudocode

```text
create empty set called seen

for every number:
    if number already exists in seen:
        return True

    add number to seen

return False
```

---

## Step 3 — Python

```python
def contains_duplicate(nums):
    seen = set()

    for num in nums:
        if num in seen:
            return True

        seen.add(num)

    return False
```

Tests:

```python
print(contains_duplicate([3, 1, 4, 1]))
# True

print(contains_duplicate([1, 2, 3, 4]))
# False

print(contains_duplicate([]))
# False

print(contains_duplicate([5]))
# False
```

---

## Complexity

We traverse the array once.

Each set lookup/add is O(1) average.

Therefore:

```text
Time Complexity: O(n)
```

In the worst case, every value is unique and gets stored.

Therefore:

```text
Space Complexity: O(n)
```

---

# 19. Dictionary or set?

Here's a simple decision rule.

Suppose the question is:

```text
Have I seen X?
Does X exist?
Is there a duplicate?
```

Think:

```python
set
```

Suppose the question is:

```text
How many times did X occur?
What information belongs to X?
At what position did I previously see X?
```

Think:

```python
dict
```

Example:

```text
Need only:

7 exists

→ set
```

But:

```text
Need:

7 appeared 4 times

→ dictionary
```

---

# 20. Independent Problem — Two Sum

Now we're going one small step beyond basic counting.

This is a classic hash-map problem.

## Problem

Given an integer array:

```python
nums = [2, 7, 11, 15]
```

and:

```python
target = 9
```

return the indexes of the two numbers whose sum equals the target.

Because:

```text
2 + 7 = 9
```

and their indexes are:

```text
0 and 1
```

Expected answer:

```python
[0, 1]
```

Assume:

```text
exactly one valid pair exists
you cannot use the same array element twice
```

Write:

```python
def two_sum(nums, target):
    # your solution
```

---

# 21. First: give me the brute-force approach

Do **not** jump immediately to the dictionary solution.

Start by asking:

> If I know nothing about hashing, how can I solve this?

One idea is to examine pairs.

For:

```text
[2, 7, 11, 15]
```

you might test:

```text
2 + 7
2 + 11
2 + 15

7 + 11
7 + 15

11 + 15
```

Think about:

```text
How many comparisons could that become?
```

Your brute-force solution should use the concepts you've already learned.

---

# 22. Then think about optimization

Now consider this equation:

```text
current number + missing number = target
```

If:

```text
current number = 2
target = 9
```

then:

```text
missing number = 7
```

because:

```text
9 - 2 = 7
```

So while traversing the array, perhaps we can remember numbers we've previously seen.

But there is one important requirement:

> We need to return indexes.

That should make you ask:

```text
Do I only need a set?

Or do I need:

number → index
```

That distinction is the core of today's lesson.

I am intentionally **not giving you the complete optimized solution yet**.

---

# 23. Your independent-problem assignment

For Two Sum, send me both approaches.

### Approach 1 — Brute force

Provide:

```text
Thought process

Pseudocode

Python code

Time Complexity

Space Complexity
```

### Approach 2 — Hash-based optimization

Again provide:

```text
Thought process

Pseudocode

Python code

Time Complexity

Space Complexity
```

For your optimized approach, think about a dictionary shaped approximately like:

```text
number → index
```

But write the solution yourself.

---

# 24. Two Sum test cases

Use:

```python
print(two_sum([2, 7, 11, 15], 9))
# Expected: [0, 1]
```

Another:

```python
print(two_sum([3, 2, 4], 6))
# Expected: [1, 2]
```

Important case:

```python
print(two_sum([3, 3], 6))
# Expected: [0, 1]
```

That final example is important because:

```text
3 + 3 = 6
```

but you cannot use the same index twice.

---

# 25. Common mistake — using a set when you need extra information

Suppose Two Sum needs indexes.

This:

```python
seen = set()
```

can remember:

```text
2 exists
7 exists
```

But it does not naturally tell you:

```text
2 was at index 0
7 was at index 1
```

A dictionary can:

```python
seen = {
    2: 0,
    7: 1
}
```

So always ask:

> Do I just need membership, or do I need information associated with the item?

---

# 26. Common mistake — accessing a missing dictionary key

Suppose:

```python
frequency = {
    "a": 2
}
```

This works:

```python
print(frequency["a"])
```

But:

```python
print(frequency["b"])
```

causes:

```text
KeyError
```

because `"b"` doesn't exist.

You can first check:

```python
if "b" in frequency:
```

or use:

```python
frequency.get("b", 0)
```

---

# 27. Common mistake — `{}` for a set

Incorrect:

```python
seen = {}
```

if you mean an empty set.

Correct:

```python
seen = set()
```

Remember:

```text
{} = dictionary
set() = empty set
```

---

# 28. Common mistake — forgetting frequency initialization

This is dangerous:

```python
frequency = {}

for num in nums:
    frequency[num] += 1
```

The first time a number appears, its key doesn't exist yet.

So you need either:

```python
if num in frequency:
    frequency[num] += 1
else:
    frequency[num] = 1
```

or:

```python
frequency[num] = frequency.get(num, 0) + 1
```

---

# 29. Common mistake — misunderstanding O(1)

Dictionary lookup being O(1) average does **not** mean:

```text
the whole algorithm is automatically O(1)
```

Consider:

```python
seen = set()

for num in nums:
    if num in seen:
        return True
    seen.add(num)
```

Each lookup is O(1) average.

But we may perform that lookup for `n` elements.

So:

```text
n × O(1)
=
O(n)
```

The whole algorithm is:

```text
O(n)
```

---

# 30. Common mistake — thinking a dictionary is O(1) space

Dictionary lookup may be:

```text
O(1) average time
```

but storing `n` entries requires:

```text
O(n) space
```

Don't confuse:

```text
lookup complexity
```

with:

```text
storage complexity
```

---

# 31. Common mistake — losing duplicate information with a set

Suppose:

```python
nums = [2, 2, 2, 5]
```

Then:

```python
set(nums)
```

becomes conceptually:

```text
{2, 5}
```

The set tells you:

```text
2 exists
5 exists
```

But it no longer tells you that:

```text
2 occurred 3 times
```

If frequency matters:

```text
use a dictionary
```

---

# 32. Common mistake — optimizing before writing brute force

If you see Two Sum online, you may memorize:

```text
dictionary → O(n)
```

But interview skill means understanding:

```text
Why did we need the dictionary?
```

The reasoning should be:

```text
Brute force repeatedly searches for a matching number.

Repeated searching causes roughly O(n²).

If I remember previously seen values,
I can look them up in average O(1).

Therefore one traversal becomes possible.
```

That's much more valuable than memorizing code.

---

# 33. Hashing as a time-space trade-off

This pattern appears frequently:

```text
Without extra memory:

search repeatedly
→ slower
```

versus:

```text
Use dictionary/set:

remember previous information
→ faster lookup
```

Often:

```text
O(n²) time + O(1) space
```

becomes:

```text
O(n) average time + O(n) space
```

You're essentially saying:

> I will spend extra memory so I don't have to repeatedly search.

That is one of the core ideas behind hashing problems.

---

# 34. Signals that suggest hashing

As you read DSA questions, pay attention to phrases like:

```text
"contains duplicate"
"already seen"
"appears more than once"
"frequency"
"count occurrences"
"how many times"
"find matching value"
"does X exist?"
"find complement"
"first occurrence"
"remember previous values"
```

These should trigger the thought:

```text
Could a dictionary or set help?
```

Then ask the next question:

```text
Do I only need existence?
```

If yes:

```text
set
```

Or:

```text
Do I need information associated with each value?
```

If yes:

```text
dictionary
```

---

# 35. Day 214 mental model

For today, keep this model:

```text
LIST
→ ordered sequence
→ searching may require O(n)

SET
→ unique values
→ fast average membership
→ "Have I seen this?"

DICTIONARY
→ key → value
→ fast average lookup
→ "What information do I know about this?"
```

And remember the two core patterns.

Frequency:

```python
frequency = {}

for item in items:
    frequency[item] = frequency.get(item, 0) + 1
```

Seen-before:

```python
seen = set()

for item in items:
    if item in seen:
        # seen before

    seen.add(item)
```

---

## Day 214 assignment

Your main independent problem is **Two Sum**:

```python
def two_sum(nums, target):
    # your implementation
```

Don't send me only the final optimized code. Send me your reasoning in this order:

```text
1. Brute-force thought process
2. Brute-force pseudocode
3. Brute-force Python
4. Brute-force time + space

5. Optimized thought process
6. Optimized pseudocode
7. Optimized Python
8. Optimized time + space
```

The most important question I want you to be able to answer after Day 214 is:

> **Why can a hash map turn repeated O(n) searching into average O(1) lookup, and how can that change an O(n²) solution into an O(n) solution?**