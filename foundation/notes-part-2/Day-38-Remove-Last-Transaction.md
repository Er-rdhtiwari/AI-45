# Day 38: Remove Last Transaction Using pop()
# Day 38 — Remove Last Transaction Using `pop()`

## 1. Day Number

**Day 38**

---

## 2. Topic Name

### List `pop()` Method

Today you will learn how to remove the **last item from a Python list** using:

```python
pop()
```

---

## 3. Connection

Previously, you worked with lists such as a shopping cart.

Now imagine you are storing a **transaction history**:

```text
Transaction 1
Transaction 2
Transaction 3
```

Sometimes the most recent transaction may need to be removed.

Today you will learn:

```text
Transaction History
        ↓
Check if list has items
        ↓
Remove last transaction
        ↓
Updated history
```

The important idea is:

> **Check that the list is not empty before calling `pop()`.**

---

## 4. Important Topics

Today's main concepts are:

* Python `list`
* `pop()`
* checking whether a list is empty
* `if` condition
* returning or displaying the removed item
* function-based problem solving

---

# 5. Foundational Notes

## What is `pop()`?

`pop()` is a built-in list method.

It removes an item from a list.

Without giving an index:

```python
my_list.pop()
```

Python removes the **last item**.

Example list:

```python
numbers = [10, 20, 30]
```

If `pop()` is used:

```text
Before:
[10, 20, 30]

        pop()

After:
[10, 20]
```

The value `30` was removed.

---

## `pop()` also returns the removed value

This is an important difference from some other list operations.

You can store the removed item:

```python
removed_item = numbers.pop()
```

Conceptually:

```text
[10, 20, 30]
        ↓ pop()
removed item = 30
        ↓
[10, 20]
```

So `pop()` does **two useful things**:

```text
1. Removes an item
2. Gives that removed item back
```

---

## Why check for an empty list?

Suppose:

```python
transactions = []
```

There is nothing available to remove.

Calling:

```python
transactions.pop()
```

would produce an error.

So first check:

```python
if transactions:
```

This means:

> If the list contains at least one item.

Conceptually:

```text
Is transaction list empty?
        |
   +----+----+
   |         |
  No        Yes
   |         |
 pop()    Do nothing /
   |      show message
   ↓
Updated list
```

---

## `pop()` vs `remove()`

Yesterday you learned `remove()`.

They solve different problems.

### `remove()`

Use it when you know the **value** you want to remove.

```python
cart.remove("Laptop")
```

Meaning:

> Find `"Laptop"` and remove it.

### `pop()`

Use it when you want to remove an item based on its **position**.

```python
transactions.pop()
```

Meaning:

> Remove the last item.

Simple comparison:

| Method          | Main idea                               |
| --------------- | --------------------------------------- |
| `remove(value)` | Remove a specific value                 |
| `pop()`         | Remove the last item                    |
| `pop(index)`    | Remove an item at a particular position |

For today's exercise, concentrate only on:

```python
pop()
```

---

# 6. Easy Example

Consider a list of tasks:

```python
tasks = ["Study", "Exercise", "Shopping"]
```

You could remove the most recently added task using:

```python
last_task = tasks.pop()
```

Afterward:

```text
Removed:
Shopping

Remaining:
["Study", "Exercise"]
```

But a safer pattern is:

```python
if tasks:
    # remove the last task
```

This prevents an error if `tasks` is empty.

This is only an example of the concept, **not today's complete solution**.

---

# 7. Problem Statement

### Remove Last Transaction

Create a list containing some transaction names.

For example, the transactions could represent:

```text
Deposit
Shopping
Electricity Bill
```

Your program should:

1. Create a transaction list.
2. Check whether the list contains any transactions.
3. If it contains transactions:

   * remove the **last transaction** using `pop()`
   * display the removed transaction
   * display the remaining transactions
4. If the list is empty:

   * print a suitable message such as:

```text
No transactions available.
```

### Important rule

Use `pop()` only when the list is **not empty**.

Do not provide a hardcoded solution specifically removing a named transaction.

The program should simply remove whichever transaction is currently last.

---

# 8. Concepts Used

You will practice:

### List

Used to store multiple transactions.

```python
transactions = [...]
```

### `pop()`

Used to remove the last transaction.

```python
transactions.pop()
```

### `if`

Used to check whether a transaction exists before removing anything.

```python
if transactions:
```

### Variable

A variable can store the removed transaction.

Conceptually:

```text
removed_transaction = last transaction
```

### Function

You can place the transaction-removal logic inside a function.

Conceptually:

```text
remove_last_transaction(...)
```

---

# 9. Thought Process

Before writing code, think about the problem step by step.

### Step 1 — What data do I have?

A list of transactions.

Example:

```text
["Deposit", "Shopping", "Electricity Bill"]
```

### Step 2 — Which transaction should be removed?

Not a transaction selected by name.

You want the:

```text
LAST transaction
```

Therefore `pop()` is suitable.

### Step 3 — Can I always call `pop()`?

No.

The list could be:

```python
[]
```

So first ask:

```text
Does the list contain at least one transaction?
```

### Step 4 — If yes

Remove the last transaction.

```text
["Deposit", "Shopping", "Electricity Bill"]
                            ↑
                         remove
```

After removal:

```text
["Deposit", "Shopping"]
```

### Step 5 — What if the list is empty?

Do not call `pop()`.

Instead display something such as:

```text
No transactions available.
```

So the overall thinking is:

```text
Transactions
     ↓
Is list non-empty?
     ↓
 +---+---+
 |       |
Yes      No
 |       |
pop()    Message
 |
Store removed transaction
 |
Show updated list
```

---

# 10. Pseudocode

```text
START

CREATE a function for removing the last transaction

    IF transaction list is not empty

        REMOVE the last transaction using pop()
        STORE the removed transaction

        DISPLAY removed transaction
        DISPLAY remaining transactions

    ELSE

        DISPLAY "No transactions available"

CREATE transaction list

CALL the function

END
```

Notice that the pseudocode describes the logic without giving you the complete Python implementation.

---

# 11. Suggested Solving Approach — Functional Approach

Use a small function to handle the removal logic.

Think of the structure as:

```text
Main Program
     |
     v
Transaction List
     |
     v
remove_last_transaction()
     |
     v
Check empty?
   /     \
 No       Yes
 |         |
pop()    Message
 |
Updated transactions
```

Your function could conceptually receive:

```text
transactions
```

Then it should decide whether `pop()` can safely be used.

A useful mental model is:

```text
Input
  ↓
Function
  ↓
Validation
  ↓
Operation
  ↓
Result
```

For this problem:

```text
transaction list
      ↓
remove function
      ↓
empty-list check
      ↓
pop()
      ↓
updated transaction list
```

---

# 12. Easy Edge Cases

## Edge Case 1 — Empty List

Input data:

```python
transactions = []
```

There is nothing to remove.

Expected behavior:

```text
No transactions available.
```

Your program should **not call `pop()`**.

---

## Edge Case 2 — One Item List

Suppose:

```text
["Deposit"]
```

After removing the last transaction:

```text
Removed transaction: Deposit
```

The remaining list becomes:

```python
[]
```

This is completely valid.

---

## Edge Case 3 — Multiple Transactions

Suppose:

```text
["Deposit", "Shopping", "Electricity Bill"]
```

Only:

```text
Electricity Bill
```

should be removed.

Remaining transactions:

```text
["Deposit", "Shopping"]
```

---

# 13. Expected Input

For this beginner exercise, you do not necessarily need `input()` from the keyboard.

You can start with a predefined list such as:

```text
["Deposit", "Shopping", "Electricity Bill"]
```

Think of that list as your input data.

Another test input can be:

```text
[]
```

And another:

```text
["Deposit"]
```

Testing these three situations will help you understand the behavior.

---

# 14. Expected Output

For:

```text
["Deposit", "Shopping", "Electricity Bill"]
```

Expected result could look like:

```text
Removed transaction: Electricity Bill
Remaining transactions: ['Deposit', 'Shopping']
```

For:

```text
["Deposit"]
```

Expected result:

```text
Removed transaction: Deposit
Remaining transactions: []
```

For an empty list:

```text
[]
```

Expected result:

```text
No transactions available.
```

The exact wording can differ. The important thing is that the **logic is correct**.

---

# 15. Hint Only

Start by thinking about this structure:

```python
def remove_last_transaction(transactions):
    if ...:
        removed_transaction = ...
        # print removed transaction
        # print remaining transactions
    else:
        # print empty-list message
```

Ask yourself three questions:

1. How can Python check whether a list contains at least one item?
2. Which list method removes and returns the last item?
3. Where should you call `pop()` so that an empty list never causes an error?

The central idea for **Day 38** is:

```text
List
 ↓
Check not empty
 ↓
pop()
 ↓
Last item removed
```

**Do not use `remove()` for today's exercise — practice `pop()` specifically.**
