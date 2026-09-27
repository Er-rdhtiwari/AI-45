# Day 59: Manual Testing and Debugging
# Day 59: Manual Testing and Debugging

## 1. Day Number

**Day 59**

## 2. Topic Name

**Basic Testing and Debugging**

Today you will learn how to check whether a small Python program behaves correctly before learning automated testing tools such as `pytest`.

---

## 3. Connection

You have already built many small programs using:

* functions
* classes and objects
* conditions
* loops
* file handling
* bank account operations

Until now, you may have mostly run a program once and checked whether it worked.

Today you will learn a better habit:

> **Run the program with different inputs and compare the actual output with the expected output.**

This is called **manual testing**.

---

## 4. Important Topics

### Test cases

A **test case** is one situation that you intentionally test.

For example:

```text
Password entered: correct password
Expected result: Login successful
```

Another test case:

```text
Password entered: wrong password
Expected result: Access denied
```

---

### Expected output

Before running your program, think:

> What should happen for this input?

Example:

```text
Starting balance = 1000
Deposit = 500

Expected balance = 1500
```

Then run the program and compare.

```text
Expected: 1500
Actual:   1500
```

If they match, the test passes.

---

### Print debugging

Sometimes your program gives the wrong result, but you do not know why.

Temporary `print()` statements can help you inspect values.

Example:

```python
balance = 1000
amount = 200

print("Balance before:", balance)

balance = balance + amount

print("Balance after:", balance)
```

These debugging prints help you see what happens step by step.

---

### Edge cases

An **edge case** is an unusual input that can expose a problem.

For a bank program:

```text
deposit = -100
withdraw = 0
withdraw = 5000 when balance is only 1000
wrong password
```

Testing only normal situations is not enough.

---

# 5. Foundational Notes

## What is testing?

Testing means checking whether your program behaves as expected.

Think of this simple pattern:

```text
Input
  ↓
Program
  ↓
Actual Output
  ↓
Compare with Expected Output
  ↓
Pass / Fail
```

---

## Normal case vs edge case

A normal case could be:

```text
Balance = 1000
Deposit = 500
```

An edge case could be:

```text
Balance = 1000
Deposit = -500
```

Good programmers test **both**.

---

## What is debugging?

Testing and debugging are related but different.

**Testing** finds that something is wrong.

```text
Expected balance: 1500
Actual balance:   500
```

**Debugging** investigates why it is wrong.

For example:

```python
print("balance =", balance)
print("amount =", amount)
```

You might discover that your code accidentally subtracts the deposit.

---

## A useful testing habit

For every important operation, think about three kinds of cases:

```text
Normal input
Invalid input
Boundary / edge input
```

For example, for withdrawal:

```text
Normal:
withdraw 200 from balance 1000

Invalid:
withdraw -200

Edge:
withdraw 1000 from balance 1000
```

---

# 6. Easy Example

Imagine this very small function:

```python
def add_money(balance, amount):
    return balance + amount
```

You could manually test it like this:

```text
Test 1

Starting balance: 100
Amount: 50
Expected result: 150
```

Then run it and check the result.

Another test:

```text
Test 2

Starting balance: 0
Amount: 100
Expected result: 100
```

The important idea is not the function itself.

The important idea is:

```text
Choose input
    ↓
Predict output
    ↓
Run program
    ↓
Compare result
```

---

# 7. Problem Statement

Create a **simple manual test checklist** for a bank account program.

The bank account program should be tested for:

1. Correct password
2. Wrong password
3. Deposit
4. Withdraw
5. Insufficient balance

You do **not** need to build a complicated testing system.

For each test, identify:

```text
Input
Expected result
Actual result
Pass or Fail
```

## Bank Account Manual Test Checklist

* [ ] **Correct password**

  * Enter the correct password.
  * Expected: Access should be allowed.

* [ ] **Wrong password**

  * Enter an incorrect password.
  * Expected: Access should be denied.

* [ ] **Valid deposit**

  * Start with a known balance and deposit a positive amount.
  * Expected: The balance should increase by the deposit amount.

* [ ] **Valid withdrawal**

  * Withdraw a positive amount smaller than or equal to the available balance.
  * Expected: The balance should decrease by the withdrawal amount.

* [ ] **Insufficient balance**

  * Try to withdraw more money than the available balance.
  * Expected: The withdrawal should be rejected and the balance should remain unchanged.

* [ ] **Negative deposit**

  * Try to deposit a negative amount.
  * Expected: The deposit should be rejected.

* [ ] **Negative withdrawal**

  * Try to withdraw a negative amount.
  * Expected: The withdrawal should be rejected.

---

# 8. Concepts Used

For today's exercise, you may use:

* variables
* `input()`
* `print()`
* `if`
* `elif`
* `else`
* comparison operators
* functions or methods
* object attributes if using OOP
* expected output
* actual output
* test cases
* edge cases
* debugging with `print()`

You are **not** learning automated unit-testing libraries yet.

---

# 9. Thought Process

Suppose your bank account starts with:

```text
Password = python123
Balance = 1000
```

### Step 1: Test authentication

First ask:

```text
What should happen with the correct password?
```

Expected:

```text
Access allowed
```

Then test:

```text
What should happen with a wrong password?
```

Expected:

```text
Access denied
```

---

### Step 2: Test deposit

Suppose:

```text
Balance = 1000
Deposit = 500
```

Calculate the expected result manually:

```text
1000 + 500 = 1500
```

So:

```text
Expected balance = 1500
```

Run your program and compare.

---

### Step 3: Test withdrawal

Suppose:

```text
Balance = 1500
Withdraw = 300
```

Expected:

```text
1500 - 300 = 1200
```

---

### Step 4: Test insufficient balance

Suppose:

```text
Balance = 1200
Withdraw = 2000
```

The program should **not** allow it.

Expected:

```text
Insufficient balance
Balance remains 1200
```

---

### Step 5: Test invalid amounts

Now deliberately enter:

```text
Deposit = -100
```

or:

```text
Withdraw = -500
```

Ask:

> Should a bank account accept this operation?

No.

Your validation should prevent the balance from changing.

---

# 10. Pseudocode-Style Testing Steps

This is testing pseudocode, not the full Python solution.

```text
SET correct password
SET starting balance

TEST 1: Correct password
    ENTER correct password
    EXPECT access allowed
    COMPARE actual result with expected result

TEST 2: Wrong password
    ENTER wrong password
    EXPECT access denied
    COMPARE actual result with expected result

TEST 3: Deposit
    NOTE current balance
    ENTER positive deposit amount
    CALCULATE expected new balance
    RUN deposit
    COMPARE actual balance with expected balance

TEST 4: Withdraw
    NOTE current balance
    ENTER valid withdrawal amount
    CALCULATE expected new balance
    RUN withdrawal
    COMPARE actual balance with expected balance

TEST 5: Insufficient balance
    ENTER amount greater than current balance
    EXPECT withdrawal rejected
    EXPECT balance unchanged

TEST 6: Negative amount
    ENTER negative deposit or withdrawal
    EXPECT operation rejected
    EXPECT balance unchanged
```

---

# 11. Suggested Solving Approach

Both approaches are suitable today.

### Functional approach

You could organize logic into functions such as:

```text
check_password(...)
deposit(...)
withdraw(...)
```

This is easier if you want to focus mainly on **testing concepts**.

### OOP-based approach

Since you have already worked with `BankAccount`, you could continue with something conceptually like:

```text
BankAccount
    holder
    balance

    deposit()
    withdraw()
    get_balance()
```

Then manually test each method.

For your current learning sequence, **OOP-based is a good choice** because it also reinforces the `BankAccount` work from earlier days.

---

# 12. Easy Edge Cases

## Wrong password

```text
Expected:
Access denied
```

Make sure no banking operation is performed.

---

## Negative amount

Example:

```text
Deposit = -500
```

Expected:

```text
Invalid amount
Balance unchanged
```

Similarly:

```text
Withdraw = -200
```

should not increase the balance accidentally.

---

## Withdrawal greater than balance

Example:

```text
Balance = 1000
Withdraw = 1500
```

Expected:

```text
Insufficient balance
Balance = 1000
```

The balance should remain unchanged.

---

## Extra useful case: zero amount

Try:

```text
Deposit = 0
```

and:

```text
Withdraw = 0
```

Think about whether your program should accept them.

For a simple program, treating them as invalid is reasonable because the amount should usually be **greater than 0**.

---

# 13. Expected Input Examples

Assume:

```text
Correct password: python123
Starting balance: 1000
```

### Example 1 — correct password

```text
Password: python123
```

### Example 2 — wrong password

```text
Password: abc123
```

### Example 3 — deposit

```text
Deposit amount: 500
```

### Example 4 — withdrawal

```text
Withdraw amount: 300
```

### Example 5 — insufficient balance

```text
Starting balance: 1000
Withdraw amount: 1500
```

### Example 6 — invalid amount

```text
Deposit amount: -200
```

---

# 14. Expected Output Examples

### Correct password

```text
Access granted
```

### Wrong password

```text
Access denied
```

### Successful deposit

If:

```text
Balance = 1000
Deposit = 500
```

Expected:

```text
Deposit successful
Balance: 1500
```

### Successful withdrawal

If:

```text
Balance = 1500
Withdraw = 300
```

Expected:

```text
Withdrawal successful
Balance: 1200
```

### Insufficient balance

If:

```text
Balance = 1000
Withdraw = 1500
```

Expected:

```text
Insufficient balance
Balance: 1000
```

### Negative amount

```text
Invalid amount
Balance unchanged
```

The exact wording does not matter. What matters is that the **behavior and balance are correct**.

---

# 15. Hint Only

Start with a known state:

```text
password = "python123"
balance = 1000
```

Before running each test, write down:

```text
Input:
Expected output:
Expected balance:
```

Then run your program and compare:

```text
Expected balance: ?
Actual balance:   ?
```

If something is wrong, temporarily add debugging statements around the suspicious operation:

```python
print("Before:", ...)
print("Amount:", ...)
print("After:", ...)
```

Do not immediately change the code when a test fails. First identify **which value became wrong and at which step**. This habit will make debugging much easier as your Python programs become larger.
