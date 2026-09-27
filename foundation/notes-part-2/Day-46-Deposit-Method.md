# Day 46: Deposit Method
# Day 46 — Deposit Method

## 1. Day Number

**Day 46**

## 2. Topic Name

**Object Method with Validation**

Today you will learn how an object method can:

* receive some data
* check whether the data is valid
* update an object's attribute

---

## 3. Connection

Yesterday, you added a method to your `BankAccount` class to **display account details**.

Conceptually, your class has reached this stage:

```text
BankAccount
│
├── account_holder
├── balance
│
└── display_account()
```

Today, you will add some **behavior**:

```text
BankAccount
│
├── account_holder
├── balance
│
├── display_account()
│
└── deposit()
```

The `deposit()` method will allow money to be added to the account.

---

# 4. Important Topics

Today's important concepts are:

* method
* method parameter
* `self`
* object attributes
* attribute update
* `if` condition
* validation

The important idea is:

```text
Receive deposit amount
        ↓
Check whether amount is valid
        ↓
If amount > 0
        ↓
Update balance
```

---

# 5. Foundational Notes

## What is a method?

A **method** is a function that belongs to a class.

Example structure:

```python
class Student:
    def show_name(self):
        print(self.name)
```

Here:

```python
show_name()
```

is a method of the `Student` class.

---

## Methods can receive values

A method can receive additional information through parameters.

For example:

```python
def add_score(self, score):
```

Here:

* `self` represents the current object
* `score` is the value being passed to the method

The method might be called like:

```python
student.add_score(10)
```

The value:

```text
10
```

goes into:

```text
score
```

---

## What does `self` do?

`self` gives the method access to the current object's data.

Suppose an object has:

```text
balance = 1000
```

Inside a method, you can access it using:

```python
self.balance
```

So:

```text
self.balance
```

means:

> the balance belonging to this particular account object.

---

## Updating an attribute

Suppose:

```text
balance = 1000
deposit = 500
```

The new balance should become:

```text
1000 + 500 = 1500
```

Conceptually:

```python
balance = balance + deposit
```

For an object attribute, the same idea becomes:

```text
self.balance = self.balance + amount
```

Python also provides the shorter form:

```python
self.balance += amount
```

Both represent the same basic idea.

---

## Why do we need validation?

Imagine someone tries:

```text
Deposit = -500
```

If you blindly add it:

```text
1000 + (-500)
```

the balance becomes:

```text
500
```

But a **deposit** should not reduce the balance.

Therefore, before changing the balance, check:

```text
Is amount greater than 0?
```

This is called **validation**.

---

## Deposit rule

For today's problem:

```text
amount > 0
```

means:

```text
Valid deposit
```

But:

```text
amount == 0
```

or:

```text
amount < 0
```

means:

```text
Invalid deposit
```

---

# 6. Easy Example

Consider a simple game player:

```python
class Player:
    def __init__(self, points):
        self.points = points

    def add_points(self, points):
        if points > 0:
            self.points += points
```

Suppose:

```text
Starting points = 10
Added points = 5
```

Then:

```text
New points = 15
```

The important pattern is:

```text
method receives value
        ↓
if value is valid
        ↓
update object attribute
```

Your `BankAccount` problem follows the same pattern.

---

# 7. Problem Statement

Create or continue your existing `BankAccount` class.

Add a method named:

```python
deposit()
```

The method should receive a deposit amount.

### Requirement

If:

```text
amount > 0
```

add the amount to the account balance.

If the amount is:

```text
0
```

or negative:

```text
amount < 0
```

do not add it to the balance.

### Example scenario

Initial account:

```text
Account Holder: Rahul
Balance: 1000
```

Deposit:

```text
500
```

New balance:

```text
1500
```

---

# 8. Concepts Used

You will use:

### Class

Represents the `BankAccount`.

```text
BankAccount
```

### Object

Represents one actual bank account.

```text
account1
```

### Attribute

Stores account information.

```text
account_holder
balance
```

### Method

Represents account behavior.

```text
deposit()
```

### Parameter

Receives the deposit amount.

```text
amount
```

### `self`

Allows the method to access the object's balance.

```text
self.balance
```

### `if`

Checks whether the deposit is valid.

```text
if amount is positive
```

### Attribute update

Changes the account balance.

```text
old balance + deposit
        ↓
new balance
```

---

# 9. Thought Process

Before writing Python, think through the problem.

### Step 1: What object are we working with?

A:

```text
BankAccount
```

---

### Step 2: What information does it already have?

For example:

```text
account_holder
balance
```

---

### Step 3: What new behavior do we need?

We need:

```text
deposit money
```

So we need a method:

```text
deposit
```

---

### Step 4: What information should the method receive?

It needs:

```text
deposit amount
```

So conceptually:

```text
deposit(amount)
```

---

### Step 5: Should every amount be accepted?

No.

The deposit should only happen when:

```text
amount > 0
```

---

### Step 6: What happens for a valid amount?

Add it to the current balance:

```text
new balance = current balance + amount
```

---

### Step 7: What happens for invalid amounts?

For today's simple version:

```text
do not change the balance
```

You may also display a simple message such as:

```text
Invalid deposit amount
```

if you choose.

---

# 10. Pseudocode

```text
CREATE BankAccount class

    CREATE constructor
        STORE account holder
        STORE balance

    CREATE deposit method that receives amount

        IF amount is greater than 0
            ADD amount to current balance

        ELSE
            DO NOT change balance


CREATE one BankAccount object

DISPLAY starting balance

CALL deposit method with an amount

DISPLAY updated balance
```

The main logic is:

```text
deposit(amount)
      ↓
amount > 0?
   /       \
 Yes       No
  ↓         ↓
Add to    Keep balance
balance   unchanged
```

---

# 11. Suggested Solving Approach

Use an **OOP-based approach**.

Keep the behavior inside the class.

Instead of doing something like:

```text
account balance
      ↓
external code changes balance
```

prefer:

```text
BankAccount object
      ↓
deposit()
      ↓
object updates its own balance
```

This is one of the important ideas behind OOP:

```text
Data + behavior
      ↓
kept together
```

For example:

```text
BankAccount
├── account_holder
├── balance
├── display_account()
└── deposit()
```

---

# 12. Easy Edge Cases

## Edge Case 1: Deposit `0`

Example:

```text
Current balance = 1000
Deposit = 0
```

Because:

```text
0 is not greater than 0
```

the balance should remain:

```text
1000
```

---

## Edge Case 2: Negative Deposit

Example:

```text
Current balance = 1000
Deposit = -200
```

Because:

```text
-200 < 0
```

the deposit should not happen.

Balance stays:

```text
1000
```

---

## Edge Case 3: Normal Positive Deposit

```text
Current balance = 1000
Deposit = 300
```

Result:

```text
1300
```

---

# 13. Expected Input

For example, assume the account starts with:

```text
Account Holder: Rahul
Balance: 1000
```

Then call the deposit method with:

```text
500
```

Conceptually:

```text
account1.deposit(500)
```

Another test could be:

```text
account1.deposit(0)
```

or:

```text
account1.deposit(-100)
```

---

# 14. Expected Output

For a valid deposit:

```text
Initial Balance: 1000
Deposit Amount: 500
Updated Balance: 1500
```

For deposit `0`:

```text
Initial Balance: 1000
Deposit Amount: 0
Updated Balance: 1000
```

For a negative deposit:

```text
Initial Balance: 1000
Deposit Amount: -200
Updated Balance: 1000
```

The exact wording of your printed output can be different. The important requirement is that invalid deposits **must not change the balance**.

---

# 15. Hint Only

Start from yesterday's `BankAccount` class.

Add a new method that looks conceptually like:

```python
def deposit(self, amount):
    # check whether amount is positive

    # if valid:
        # update self.balance
```

Remember these two ideas:

```python
if amount > 0:
```

and:

```python
self.balance += amount
```

Your job is to combine them correctly inside the `deposit()` method.

**Do not forget:** the method belongs inside the `BankAccount` class, and you call it through an object:

```text
account object
      ↓
.deposit(...)
      ↓
balance changes
```
