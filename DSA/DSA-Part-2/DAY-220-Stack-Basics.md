# Day 220 — Stack Fundamentals

Today we move from arrays and prefix sums to a new data-structure idea.

> **Arrays store a general sequence. A stack stores items so that the most recently added item is handled first.**

That rule is called **LIFO**:

> **Last In, First Out**

---

# 1. Real-World Analogy: Stack of Plates

Imagine plates in a cafeteria:

```text
        ┌───────┐
        │ Plate D│  ← top
        ├───────┤
        │ Plate C│
        ├───────┤
        │ Plate B│
        ├───────┤
        │ Plate A│
        └───────┘
```

Plate `D` was added last.

Which plate do you normally remove first?

```text
D
```

So:

```text
Last added
    ↓
First removed
```

That's a stack.

---

# 2. LIFO

Suppose we push:

```text
10
20
30
```

The stack becomes:

```text
TOP
 ↓

30
20
10
```

If we remove one element, we remove:

```text
30
```

Then:

```text
TOP
 ↓

20
10
```

So:

```text
push 10
push 20
push 30

pop → 30
pop → 20
pop → 10
```

That's **Last In, First Out**.

---

# 3. Important Stack Operations

You need to know five basic ideas:

```text
push
pop
peek / top
empty
LIFO
```

In Python, a normal `list` works very well as a stack.

---

# 4. Creating an Empty Stack

```python
stack = []
```

Visualization:

```text
stack = []

EMPTY
```

Check whether it's empty:

```python
if not stack:
    print("Stack is empty")
```

Or:

```python
if len(stack) == 0:
    print("Stack is empty")
```

Usually this is cleaner:

```python
if not stack:
```

---

# 5. Push

**Push** means:

> Add an item to the top of the stack.

Python:

```python
stack.append(10)
```

Then:

```text
stack = [10]
```

Push another:

```python
stack.append(20)
```

Now:

```text
stack = [10, 20]
```

Think of the **right side** of the Python list as the top:

```text
[10, 20]
     ↑
    TOP
```

Push `30`:

```python
stack.append(30)
```

```text
[10, 20, 30]
         ↑
        TOP
```

---

# 6. Pop

**Pop** means:

> Remove and return the top item.

Python:

```python
value = stack.pop()
```

Suppose:

```python
stack = [10, 20, 30]
```

Then:

```python
value = stack.pop()
```

Afterward:

```text
value = 30

stack = [10, 20]
```

Visualization:

```text
Before:

30  ← removed
20
10


After:

20  ← TOP
10
```

---

# 7. Peek / Top

Sometimes we want to look at the top item without removing it.

That's called:

```text
peek
```

or:

```text
top
```

Python doesn't have a special `peek()` method for lists.

Use:

```python
stack[-1]
```

Example:

```python
stack = [10, 20, 30]

print(stack[-1])
```

Output:

```text
30
```

The stack remains:

```python
[10, 20, 30]
```

Nothing was removed.

---

# 8. Push vs Pop vs Peek

Suppose:

```python
stack = [10, 20]
```

### Push

```python
stack.append(30)
```

Result:

```text
[10, 20, 30]
```

### Peek

```python
stack[-1]
```

Returns:

```text
30
```

Stack remains:

```text
[10, 20, 30]
```

### Pop

```python
stack.pop()
```

Returns:

```text
30
```

Stack becomes:

```text
[10, 20]
```

So:

```text
push  → add
peek  → inspect
pop   → remove
```

---

# 9. Basic Stack Example in Python

```python
stack = []

# Push
stack.append(10)
stack.append(20)
stack.append(30)

print(stack)
# [10, 20, 30]

# Peek
print(stack[-1])
# 30

# Pop
value = stack.pop()

print(value)
# 30

print(stack)
# [10, 20]
```

---

# 10. Stack Operation Complexity

Using the end of a Python list:

```python
stack.append(x)
stack.pop()
stack[-1]
```

the usual complexities are:

| Operation | Python | Complexity |
|---|---|---:|
| Push | `append()` | O(1) amortized |
| Pop | `pop()` | O(1) |
| Peek | `stack[-1]` | O(1) |
| Check empty | `if not stack` | O(1) |

This is why we normally use the **end** of a Python list as the top.

Avoid doing this for a stack:

```python
stack.insert(0, value)
stack.pop(0)
```

because operations at the beginning of a list can require shifting many elements:

```text
O(n)
```

Prefer:

```python
stack.append(value)
stack.pop()
```

---

# 11. The Empty-Stack Problem

Suppose:

```python
stack = []
```

and you do:

```python
stack.pop()
```

Python raises:

```text
IndexError
```

Similarly:

```python
stack[-1]
```

also fails when the stack is empty.

So before popping or peeking, sometimes you need:

```python
if stack:
    value = stack.pop()
```

or:

```python
if stack:
    top = stack[-1]
```

This becomes extremely important in interview problems.

---

# 12. How to Recognize Stack Problems

Think stack when the problem behaves like:

```text
most recent thing must be handled first
```

Common signals:

```text
matching brackets
undo
backtracking one step
nested structures
remove previous item
process most recent unfinished item
```

Examples:

```text
()
{}
[]
```

or:

```text
undo last action
```

or:

```text
remove previous character
```

---

# 13. Why Stacks Work for Matching Brackets

Consider:

```text
({[]})
```

When we see an opening bracket:

```text
(
{
[
```

we don't yet know when it will close.

So we store it.

Suppose we read:

```text
(
```

Stack:

```text
[
  (
]
```

Then:

```text
{
```

Stack:

```text
{
(
```

Then:

```text
[
```

Stack:

```text
[
{
(
```

Now we see:

```text
]
```

Which opening bracket should match it?

The **most recent** unmatched opening bracket:

```text
[
```

Perfect stack behavior.

Pop it.

Stack becomes:

```text
{
(
```

Next:

```text
}
```

matches:

```text
{
```

Pop.

Finally:

```text
)
```

matches:

```text
(
```

Pop.

Stack becomes empty.

Therefore the brackets are valid.

---

# 14. Example of Invalid Brackets

Consider:

```text
([)]
```

Process:

```text
(
```

Stack:

```text
(
```

Then:

```text
[
(
```

Now we encounter:

```text
)
```

But the top of the stack is:

```text
[
```

`[` expects:

```text
]
```

not:

```text
)
```

So the expression is invalid.

The key rule is:

> A closing bracket must match the **top** opening bracket.

Not just any opening bracket somewhere in the stack.

---

# 15. Why Stacks Work for Undo

Imagine you're typing:

```text
A
B
C
```

History:

```text
A
B
C ← latest action
```

Now press Undo.

Which action should be reversed?

```text
C
```

Press Undo again:

```text
B
```

Again:

```text
A
```

That's exactly:

```text
Last action
   ↓
First action undone
```

LIFO.

Example:

```python
history = []

history.append("Type A")
history.append("Type B")
history.append("Type C")

last_action = history.pop()

print(last_action)
```

Output:

```text
Type C
```

---

# 16. Simple Undo Simulation

```python
history = []

history.append("Write hello")
history.append("Make text bold")
history.append("Change font size")

print(history)

undo_action = history.pop()

print("Undo:", undo_action)
print("Remaining:", history)
```

Output conceptually:

```text
Undo: Change font size
```

because that was the most recent action.

---

# 17. Guided Problem — Valid Parentheses

Let's use the most important beginner stack problem.

## Problem

Given:

```python
s = "({[]})"
```

return:

```python
True
```

because every opening bracket is correctly closed.

Given:

```python
s = "([)]"
```

return:

```python
False
```

Valid pairs are:

```text
()
[]
{}
```

---

# 18. Step 1 — What Should We Store?

When we see:

```text
(
[
{
```

store the opening bracket.

So:

```python
stack.append(char)
```

---

# 19. Step 2 — What Happens for a Closing Bracket?

Suppose we see:

```text
)
```

Before doing anything, ask:

```text
Is the stack empty?
```

If yes, that's immediately invalid.

Example:

```text
")("
```

The very first character is:

```text
)
```

There is nothing available to match it.

So:

```python
if not stack:
    return False
```

---

# 20. Step 3 — Check the Top

Suppose:

```text
top = [
current = )
```

These don't match.

Return:

```python
False
```

A useful mapping is:

```python
pairs = {
    ')': '(',
    ']': '[',
    '}': '{'
}
```

Then for a closing character:

```python
pairs[char]
```

tells you the opening bracket you expected.

---

# 21. Guided Skeleton

Complete this yourself:

```python
def is_valid(s):

    stack = []

    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    for char in s:

        if char in "([{":
            # TODO: push opening bracket

        else:
            # TODO:
            # What if stack is empty?

            # TODO:
            # Compare stack top with expected opening bracket

            # TODO:
            # If correct, pop

    # TODO:
    # What should be true about the stack at the end?
```

Do not forget the last condition.

Consider:

```text
"((("
```

There are no mismatched closing brackets.

But there are still unmatched opening brackets.

So the final stack matters.

---

# 22. Detailed Dry Run

Take:

```text
s = "{[()]}"
```

Start:

```text
stack = []
```

Character:

```text
{
```

Push:

```text
stack = ['{']
```

Character:

```text
[
```

Push:

```text
stack = ['{', '[']
```

Character:

```text
(
```

Push:

```text
stack = ['{', '[', '(']
```

Character:

```text
)
```

Expected:

```text
(
```

Top:

```text
(
```

Match.

Pop:

```text
stack = ['{', '[']
```

Character:

```text
]
```

Expected:

```text
[
```

Top:

```text
[
```

Match.

Pop:

```text
stack = ['{']
```

Character:

```text
}
```

Expected:

```text
{
```

Top:

```text
{
```

Match.

Pop:

```text
stack = []
```

End:

```text
stack is empty
```

Therefore:

```text
True
```

---

# 23. Complexity of the Guided Problem

Suppose the string length is:

```text
n
```

We inspect every character once.

So:

```text
Time = O(n)
```

In the worst case:

```text
"((((((((("
```

we may store all characters.

So:

```text
Space = O(n)
```

Your eventual answer should always state both.

---

# 24. Important Empty-Stack Edge Cases

### Case 1

```text
""
```

No unmatched brackets.

Normally considered valid.

---

### Case 2

```text
")"
```

Closing bracket appears while stack is empty.

Invalid.

---

### Case 3

```text
"("
```

Stack still contains:

```text
(
```

at the end.

Invalid.

---

### Case 4

```text
"()"
```

Valid.

---

### Case 5

```text
"(()"
```

One opening bracket remains.

Invalid.

---

### Case 6

```text
"())"
```

The final `)` tries to pop an empty stack.

Invalid.

These edge cases are important because many stack bugs happen here.

---

# 25. Common Stack Mistakes

### Mistake 1 — Pop from an empty stack

Wrong:

```python
top = stack.pop()
```

without checking whether anything exists.

Safer when necessary:

```python
if not stack:
    return False

top = stack.pop()
```

---

### Mistake 2 — Peek before checking empty

Wrong:

```python
if stack[-1] == "(":
```

If:

```python
stack = []
```

this crashes.

Correct idea:

```python
if not stack:
    return False

if stack[-1] == "(":
    ...
```

---

### Mistake 3 — Forgetting to pop

Suppose brackets match, but you never remove the opening bracket.

Wrong:

```python
if stack[-1] == pairs[char]:
    continue
```

The matched bracket remains forever.

You usually need:

```python
stack.pop()
```

---

### Mistake 4 — Only counting brackets

Suppose:

```text
([)]
```

You might think:

```text
2 opening
2 closing
```

so valid.

Wrong.

The **order** matters.

Stack preserves the nesting order.

---

### Mistake 5 — Checking only whether closing brackets match

Consider:

```text
"(("
```

No bad closing bracket occurs.

But at the end:

```text
stack = ['(', '(']
```

So invalid.

Always consider whether the stack should be empty at the end.

---

### Mistake 6 — Using the beginning of a Python list

Avoid:

```python
stack.insert(0, x)
stack.pop(0)
```

Prefer:

```python
stack.append(x)
stack.pop()
```

because those are efficient stack operations.

---

# 26. Independent Problem 1 — Easy

## Remove Adjacent Duplicates

Given:

```python
s = "abbaca"
```

Repeatedly remove two adjacent equal characters.

For example:

```text
abbaca
 ↑↑

remove bb
```

becomes:

```text
aaca
```

Then:

```text
aaca
↑↑
```

remove:

```text
aa
```

Result:

```text
ca
```

Return:

```text
"ca"
```

Think about this question:

> When reading a new character, which previous character matters most?

Do not solve it yet with nested loops.

Your answer should contain:

```text
1. Why a stack may help
2. Pseudocode
3. Python
4. Time complexity
5. Space complexity
6. Empty-stack handling
```

I won't give the solution initially.

---

# 27. Independent Problem 2 — Easy

## Undo Operations

You receive commands:

```python
operations = [
    "type A",
    "type B",
    "type C",
    "undo",
    "type D",
    "undo"
]
```

Rules:

```text
"type X" → add X
"undo"   → remove the most recently typed item
```

Return the remaining typed characters.

For the example, think through:

```text
type A
type B
type C
undo
type D
undo
```

You'll need to decide what happens if:

```text
undo
```

appears while the stack is already empty.

For your answer provide:

```text
1. Stack state after every operation
2. Pseudocode
3. Python
4. Time complexity
5. Space complexity
6. Empty-stack behavior
```

No solution yet.

---

# 28. A Useful Stack Template

For many beginner problems:

```python
stack = []

for item in items:

    if should_push:
        stack.append(item)

    else:
        if stack:
            top = stack[-1]

            if some_condition:
                stack.pop()
```

Don't memorize it blindly.

Instead think:

```text
What does my stack represent?

What causes a push?

What causes a pop?

What does the top mean?
```

Those four questions are much more useful.

---

# 29. Stack State Is Important

When solving a stack interview problem, physically write the stack while learning.

For example:

```text
Input: "abbaca"

Read a:

[a]

Read b:

[a, b]

Read b:

compare with top
...
```

This makes stack problems much easier than trying to imagine everything mentally.

---

# 30. Stack vs Normal Array Thinking

An array allows you to access:

```python
nums[0]
nums[5]
nums[20]
```

A stack usually says:

> I mostly care about the latest item.

So even though our Python implementation is a list:

```python
stack = []
```

we deliberately restrict how we use it.

We mainly use:

```python
stack.append(x)
stack.pop()
stack[-1]
```

That's the **stack behavior**.

---

# Day 220 — One-Page Revision Cheat Sheet

```text
STACK
=====

Core rule:

LIFO
Last In, First Out


PYTHON STACK
============

stack = []

Push:
stack.append(x)

Pop:
stack.pop()

Peek:
stack[-1]

Empty:
if not stack:


VISUALIZATION
=============

[10, 20, 30]
         ↑
        TOP


PUSH 40

[10, 20, 30, 40]
             ↑
            TOP


POP

returns 40

[10, 20, 30]
         ↑
        TOP


COMPLEXITY
==========

append()    O(1) amortized
pop()       O(1)
stack[-1]   O(1)
empty check O(1)


THINK STACK WHEN
================

most recent item matters

matching brackets
undo
nested structures
remove previous item
backtracking-like behavior


BRACKET PATTERN
===============

Opening bracket:
    push

Closing bracket:
    if empty:
        invalid

    check top

    if mismatch:
        invalid

    pop


AT THE END
==========

Often ask:

Should the stack now be empty?


COMMON BUGS
===========

pop empty stack
peek empty stack
forget to pop
ignore order
forget leftover items
use pop(0)


KEY QUESTIONS
=============

1. What does my stack store?
2. When do I push?
3. When do I pop?
4. What does stack[-1] represent?
```

For **Day 220 practice**, start with the guided **Valid Parentheses** problem. Before writing Python, first write 5–8 lines of pseudocode and state the expected **time and space complexity**.