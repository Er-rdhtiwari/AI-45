# Day 47: Withdraw Method
# Day 47 — Withdraw Method

## 1. Day Number

**Day 47**

## 2. Topic Name

**Method with `if-elif-else`**

Today you will learn how an object method can make a decision before changing an object's data.

---

## 3. Connection

Yesterday, you added a `deposit()` method to your `BankAccount` class.

The deposit method followed a simple rule:

```text
If amount is positive
    add it to balance
```

Today, withdrawal needs a little more validation because two things must be checked:

```text
Is the withdrawal amount valid?
        ↓
Is enough balance available?
        ↓
Only then reduce balance
```

So today you will add a **`withdraw()` method**.

---

# 4. Important Topics

You will practice:

* method
* `self`
* method parameter
* validation
* `if`
* `elif`
* `else`
* object attributes
* balance update
* preventing invalid operations

The main idea is:

```text
Validate first
     ↓
Update data only when valid
```

---

# 5. Foundational Notes

## What is a method?

A method is a function that belongs to a class.

For example:

```python
class BankAccount:

    def withdraw(self, amount):
        ...
```

Here:

* `withdraw` is the method name
* `self` represents the current account object
* `amount` is the requested withdrawal amount

You might call it like:

```python
account.withdraw(500)
```

---

## Why does withdrawal need validation?

Imagine an account has:

```text
Balance = ₹5000
```

### Valid withdrawal

```text
Withdraw = ₹1000
```

This can be allowed:

```text
₹5000 - ₹1000 = ₹4000
```

---

### Invalid withdrawal

```text
Withdraw = ₹7000
```

The account does not have enough money.

Therefore:

```text
Balance should remain ₹5000
```

---

## Another invalid case

```text
Withdraw = -₹500
```

A negative withdrawal does not make sense.

It must not change the balance.

---

## Three possible situations

Your method can think about the amount in three stages:

```text
Withdrawal request
       |
       v
Is amount <= 0?
   /        \
 yes         no
 |            |
invalid       v
        Is amount <= balance?
           /          \
         yes           no
          |             |
      withdraw     insufficient balance
```

This is why `if-elif-else` is useful.

---

# 6. Easy Example

Consider a simple game player:

```python
class Player:
    def __init__(self, energy):
        self.energy = energy
```

Suppose we want to use some energy.

The logic could be:

```text
if requested energy is invalid:
    reject request

elif enough energy exists:
    reduce energy

else:
    say energy is not enough
```

For example:

```text
Current energy = 100
Use energy = 30

New energy = 70
```

But:

```text
Current energy = 100
Use energy = 150

Not enough energy
Energy remains 100
```

Your bank withdrawal method follows the same idea.

---

# 7. Problem Statement

Create or continue using your `BankAccount` class.

Add a method:

```python
withdraw()
```

The method should accept a withdrawal amount.

### Rules

Allow withdrawal only when:

```text
amount > 0
```

and:

```text
amount <= balance
```

If both conditions are valid:

```text
balance = balance - amount
```

Otherwise, do not change the balance.

You should handle three cases:

```text
amount <= 0
amount is valid and balance is enough
amount > balance
```

---

# 8. Concepts Used

### Class

```python
class BankAccount:
```

Represents the blueprint for bank-account objects.

### Object

Example conceptually:

```python
account = BankAccount(...)
```

The object stores its own balance.

### Method

```python
withdraw()
```

Provides withdrawal behavior to the account.

### `self`

Used to access the current object's balance:

```python
self.balance
```

### Parameter

The method receives:

```text
amount
```

### Validation

Before changing the balance, check whether the requested amount is allowed.

### `if-elif-else`

Used to handle multiple possible situations.

### Attribute update

After successful withdrawal:

```text
old balance → subtract amount → new balance
```

---

# 9. Thought Process

Suppose:

```text
Account balance = ₹5000
Requested withdrawal = ₹2000
```

Think through the problem in this order.

### Step 1: Check whether amount is positive

Ask:

```text
Is ₹2000 greater than 0?
```

Yes.

Continue.

### Step 2: Check available balance

Ask:

```text
Is ₹2000 less than or equal to ₹5000?
```

Yes.

Continue.

### Step 3: Update balance

Calculate:

```text
5000 - 2000
```

New balance:

```text
₹3000
```

---

Now consider:

```text
Balance = ₹5000
Withdrawal = ₹7000
```

Step 1:

```text
7000 > 0
```

Valid.

Step 2:

```text
7000 <= 5000
```

False.

Therefore:

```text
Do not change balance
```

---

For:

```text
Withdrawal = 0
```

Immediately reject it because:

```text
0 is not positive
```

---

# 10. Pseudocode

```text
CLASS BankAccount

    constructor(account_holder, balance)
        store account_holder
        store balance

    METHOD withdraw(amount)

        IF amount is less than or equal to zero
            display invalid withdrawal message

        ELIF amount is less than or equal to balance
            subtract amount from balance
            display successful withdrawal message

        ELSE
            display insufficient balance message
```

Notice the important order:

```text
Check invalid amount
        ↓
Check sufficient balance
        ↓
Otherwise insufficient balance
```

---

# 11. Suggested Solving Approach

Use an **OOP-based approach**.

Your class structure should conceptually look like:

```text
BankAccount
│
├── account_holder
├── balance
│
├── display_account()
├── deposit()
└── withdraw()
```

The important idea is that the account manages its own balance.

Instead of changing balance directly from outside:

```text
outside code → directly modify balance
```

prefer:

```text
outside code
     |
     v
withdraw(amount)
     |
     v
validate request
     |
     v
update self.balance
```

This keeps the account behavior inside the `BankAccount` class.

---

# 12. Easy Edge Cases

## Edge Case 1 — Withdrawal amount is `0`

Example:

```text
Balance: ₹5000
Withdraw: ₹0
```

Expected behavior:

```text
Invalid withdrawal amount
Balance remains ₹5000
```

Because:

```text
0 is not positive
```

---

## Edge Case 2 — Negative withdrawal

Example:

```text
Balance: ₹5000
Withdraw: ₹-500
```

Expected behavior:

```text
Invalid withdrawal amount
Balance remains ₹5000
```

---

## Edge Case 3 — Amount greater than balance

Example:

```text
Balance: ₹5000
Withdraw: ₹6000
```

Expected behavior:

```text
Insufficient balance
Balance remains ₹5000
```

---

## Useful additional case — Withdraw complete balance

Suppose:

```text
Balance: ₹5000
Withdraw: ₹5000
```

This should normally be valid because:

```text
withdraw amount <= balance
```

After withdrawal:

```text
Balance: ₹0
```

So be careful not to accidentally use:

```text
amount < balance
```

when the requirement allows withdrawing exactly the available balance.

---

# 13. Expected Input

For example, your object might initially contain:

```text
Account holder: Radhe
Balance: 5000
```

Then the withdrawal method might receive:

```text
2000
```

Conceptually:

```python
account.withdraw(2000)
```

Another test could be:

```python
account.withdraw(7000)
```

Another:

```python
account.withdraw(0)
```

---

# 14. Expected Output

For a valid withdrawal:

```text
Account holder: Radhe
Starting balance: 5000

Withdrawal amount: 2000
Withdrawal successful

Remaining balance: 3000
```

For insufficient balance:

```text
Starting balance: 5000

Withdrawal amount: 7000
Insufficient balance

Remaining balance: 5000
```

For invalid amount:

```text
Starting balance: 5000

Withdrawal amount: 0
Invalid withdrawal amount

Remaining balance: 5000
```

The exact wording of your messages can be different. The important requirement is that **invalid withdrawals must not change the balance**.

---

# 15. Hint Only

Inside your `withdraw()` method, think about these three conditions:

```python
if amount <= ...:
    # invalid amount

elif amount <= self.balance:
    # update balance

else:
    # insufficient balance
```

For the successful case, remember the balance needs to move in the opposite direction from yesterday's deposit:

```text
Deposit:
balance = balance + amount

Withdraw:
balance = balance - amount
```

Try to complete the missing condition and balance update yourself without looking at a full solution.
