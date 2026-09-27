# Day 37: Remove Item from Cart
# Day 37 — Remove Item from Cart

## 1. Day Number

**Day 37**

## 2. Topic Name

### List `remove()` Method

Today you will learn how to remove an existing item from a Python list using:

```python
remove()
```

You will also learn an important habit:

> **Check whether the item exists before trying to remove it.**

---

## 3. Connection

Earlier, you learned how to **add products to a cart** using a list and `append()`.

For example:

```text
Cart
 ↓
["Laptop", "Mouse", "Keyboard"]
```

Today you will do the opposite:

```text
Add item
   ↓
append()

Remove item
   ↓
remove()
```

So your cart can now support both:

```text
Product
   ↓
Add to Cart
   ↓
Cart List
   ↓
Remove from Cart
```

---

# 4. Important Topics

The important concepts for today are:

* `list`
* `remove()`
* `in`
* `if-else`
* function
* function parameter
* searching before removing

The most important pattern is:

```text
Is item in cart?
       |
    ┌──┴──┐
   Yes    No
    |      |
 Remove   Print
 item     not found
```

---

# 5. Foundational Notes

## What is a list?

A list stores multiple values together.

Example:

```python
cart = ["Laptop", "Mouse", "Keyboard"]
```

Here:

```text
Index       Item
-------------------
0           Laptop
1           Mouse
2           Keyboard
```

---

## What does `remove()` do?

The `remove()` method removes a particular **value** from a list.

Example:

```python
fruits = ["apple", "banana", "mango"]

fruits.remove("banana")
```

After removing:

```python
["apple", "mango"]
```

Notice that we provide the **value**:

```python
remove("banana")
```

not the index.

---

## `remove()` vs `append()`

You have already used:

```python
append()
```

to add something.

Example:

```python
cart.append("Mouse")
```

Today:

```python
cart.remove("Mouse")
```

Conceptually:

```text
append()
   |
   v
["Laptop"]
   |
   + Mouse
   |
   v
["Laptop", "Mouse"]


remove()
   |
   v
["Laptop", "Mouse"]
   |
   - Mouse
   |
   v
["Laptop"]
```

---

## Why search before removing?

Suppose:

```python
cart = ["Laptop", "Mouse"]
```

and you try:

```python
cart.remove("Keyboard")
```

But `"Keyboard"` is not inside the list.

Python would produce an error similar to:

```text
ValueError
```

Therefore, for today's exercise, first check:

```python
if item in cart:
```

and only then use:

```python
remove()
```

The logic becomes:

```text
item
 |
 v
Is item in cart?
 |
 +---- Yes ----> remove item
 |
 +---- No -----> item not found
```

---

## The `in` operator

Python's `in` operator checks whether something exists inside a collection.

Example:

```python
colors = ["red", "blue", "green"]

if "blue" in colors:
    print("Found")
```

Here:

```text
"blue" in colors
```

evaluates to:

```python
True
```

But:

```python
"yellow" in colors
```

evaluates to:

```python
False
```

This is exactly what we need before removing an item.

---

# 6. Easy Example

Consider a simple list of students:

```python
students = ["Amit", "Rahul", "Neha"]

name = "Rahul"

if name in students:
    students.remove(name)
    print("Student removed")
else:
    print("Student not found")
```

After the removal:

```text
Before:

["Amit", "Rahul", "Neha"]

             remove Rahul
                   ↓

After:

["Amit", "Neha"]
```

The important idea is not the student example itself.

The pattern is:

```text
Check
  ↓
Found?
  ↓
Remove
```

You will apply the same idea to a shopping cart.

---

# 7. Problem Statement

Create a cart containing some item names.

For example, conceptually:

```text
Laptop
Mouse
Keyboard
```

Then:

1. Ask the user to enter an item name.
2. Check whether that item exists in the cart.
3. If the item exists:

   * remove it from the cart.
4. Otherwise:

   * print `"Item not found"`.
5. Show the updated cart.

Example flow:

```text
Cart
["Laptop", "Mouse", "Keyboard"]

User enters:
Mouse

        ↓

Is Mouse in cart?
        ↓
       Yes
        ↓
Remove Mouse
        ↓

Updated cart
["Laptop", "Keyboard"]
```

---

# 8. Concepts Used

### List

Used to store cart items.

Conceptually:

```python
cart = [...]
```

---

### User Input

Used to ask which item should be removed.

```python
input()
```

---

### Membership Check

Use:

```python
in
```

to determine whether the requested item exists.

Conceptually:

```text
item in cart
```

---

### Condition

Use:

```python
if
```

for the successful case.

And:

```python
else
```

for the item-not-found case.

---

### `remove()`

Used to remove the matching value.

```text
cart.remove(item)
```

---

### Function

Instead of placing all logic directly in the main program, today's suggested approach is to put the removal logic inside a function.

Conceptually:

```text
Main Program
     |
     | cart + requested item
     v
Remove Function
     |
     | checks item
     |
     +---- found ----> remove
     |
     +---- not found -> message
```

---

# 9. Thought Process

Before writing Python, think through the problem step by step.

### Step 1: What data do I have?

A cart containing item names.

```text
["Laptop", "Mouse", "Keyboard"]
```

---

### Step 2: What information do I need from the user?

The name of the item they want to remove.

Example:

```text
Mouse
```

---

### Step 3: Can I immediately call `remove()`?

Not safely.

First ask:

```text
Does this item exist in the cart?
```

---

### Step 4: How do I check that?

Use:

```python
in
```

Conceptually:

```text
item in cart
```

---

### Step 5: What happens if the item exists?

Use:

```python
remove()
```

---

### Step 6: What happens if it does not exist?

Do not call `remove()`.

Instead print:

```text
Item not found
```

---

### Complete thinking flow

```text
START
  |
  v
Create cart
  |
  v
Ask item name
  |
  v
Call function
  |
  v
Is item in cart?
  |
  +----------------+
  |                |
 Yes               No
  |                 |
  v                 v
Remove item     Print "Item not found"
  |                 |
  +--------+--------+
           |
           v
     Show cart
           |
           v
          END
```

---

# 10. Pseudocode

Do not worry about exact Python syntax yet.

```text
FUNCTION remove_item(cart, item)

    IF item exists in cart
        remove item from cart
        print item removed
    ELSE
        print item not found

END FUNCTION


Create cart with item names

Ask user which item should be removed

Call remove_item function

Print updated cart
```

Notice that the pseudocode answers the important questions before coding:

```text
What data?
What condition?
What happens when true?
What happens when false?
```

---

# 11. Suggested Solving Approach — Functional Approach

Use a small function responsible for removing an item.

Think of the function like this:

```text
            cart
              \
               \
                v
             Function
                ^
               /
              /
            item

              |
              v

      Check item exists
              |
        ┌─────┴─────┐
        |           |
      Found       Missing
        |           |
      Remove      Message
```

A possible function structure is:

```python
def remove_item(cart, item):
    # check whether item exists

    # if found:
        # remove item

    # otherwise:
        # print item not found
```

This is intentionally incomplete.

Your job is to fill in the condition and removal logic.

---

# 12. Easy Edge Cases

## Edge Case 1: Item Not Found

Cart:

```text
["Laptop", "Mouse", "Keyboard"]
```

User enters:

```text
Monitor
```

Since `"Monitor"` is not present:

```text
Item not found
```

The cart should remain unchanged:

```text
["Laptop", "Mouse", "Keyboard"]
```

---

## Edge Case 2: Empty Cart

Cart:

```text
[]
```

User enters:

```text
Mouse
```

There is nothing to remove.

Therefore:

```text
Item not found
```

This is useful because your same condition can naturally handle an empty cart.

```text
[]
 |
 | Search Mouse
 v
Not found
```

You do not need complicated special logic for this beginner exercise.

---

## Small Extra Observation: Duplicate Items

Suppose:

```text
["Mouse", "Keyboard", "Mouse"]
```

If you use:

```python
remove("Mouse")
```

Python removes the **first matching occurrence**.

Result:

```text
["Keyboard", "Mouse"]
```

You do not need to solve duplicate removal today, but it is useful to know how `remove()` behaves.

---

# 13. Expected Input

Your program can start with a predefined cart, so the main user input is an item name.

Example:

```text
Enter item to remove: Mouse
```

Another example:

```text
Enter item to remove: Monitor
```

The input is a string.

Conceptually:

```text
User
 |
 | "Mouse"
 v
Program
```

---

# 14. Expected Output

### Case 1 — Item Exists

Suppose the cart initially contains:

```text
["Laptop", "Mouse", "Keyboard"]
```

Input:

```text
Enter item to remove: Mouse
```

Expected behavior:

```text
Item removed
Updated cart: ['Laptop', 'Keyboard']
```

---

### Case 2 — Item Does Not Exist

Input:

```text
Enter item to remove: Monitor
```

Expected behavior:

```text
Item not found
Updated cart: ['Laptop', 'Mouse', 'Keyboard']
```

---

### Case 3 — Empty Cart

Cart:

```text
[]
```

Input:

```text
Enter item to remove: Mouse
```

Expected behavior:

```text
Item not found
Updated cart: []
```

---

# 15. Hint Only

Start by creating something similar to:

```python
cart = ["Laptop", "Mouse", "Keyboard"]
```

Then get the item from the user:

```python
item = input(...)
```

Inside your function, think about this question:

```text
How can I write:

"if item exists inside cart"
```

You learned the keyword you need today:

```python
in
```

Then, only inside the successful condition, use:

```python
cart.remove(...)
```

Your core logic should mentally look like:

```text
IF requested item is inside cart
    remove requested item
ELSE
    print item not found
```

**Do not call `remove()` before checking that the item exists.**
