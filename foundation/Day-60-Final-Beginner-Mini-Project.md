# Day 60: Final Beginner Python Mini Project 🎉

## 1. Day Number

**Day 60 of your Beginner Python Foundation Journey**

You have reached the final day of your 60-day Python foundation track.

---

## 2. Topic Name

**Final Revision Mini Project — Simple Bank App**

Today you will combine the main Python concepts you have learned into one small program.

---

## 3. Connection

During the last 60 days, you gradually moved from basic Python statements to functions, files, error handling, and object-oriented programming.

Your progression was roughly:

```text
Variables
   ↓
Input / Output
   ↓
Conditions
   ↓
Loops
   ↓
Strings
   ↓
Lists / Dictionaries
   ↓
Functions
   ↓
Error Handling
   ↓
Files
   ↓
Classes and Objects
   ↓
BankAccount methods
   ↓
Manual Testing
   ↓
Final Mini Project
```

Today you will bring those ideas together in a **very small bank application**.

The goal is not to create a real banking system. The goal is to prove that you can connect your Python fundamentals together.

---

# 4. Revision Summary of the Full 60 Days

Your 60-day journey covered several important stages.

### Stage 1 — Basic Python

You started with things such as:

```python
name = "Rahul"
age = 25
balance = 1000
```

You learned that variables store information.

You also learned output:

```python
print(balance)
```

and user input:

```python
name = input("Enter name: ")
```

---

### Stage 2 — Type Conversion

`input()` normally gives you a string.

For calculations, you often convert it.

Example:

```python
amount = float(input("Enter amount: "))
```

or:

```python
age = int(input("Enter age: "))
```

---

### Stage 3 — Conditions

You learned how programs make decisions.

```python
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

Later you used:

```text
if
elif
else
```

for multiple choices.

---

### Stage 4 — Loops

Loops allow repeated work.

You practiced ideas such as:

```python
for item in items:
    print(item)
```

and:

```python
while condition:
    # repeat something
```

Loops became especially useful when working with lists and dictionaries.

---

### Stage 5 — Strings

Strings represent text.

You practiced operations such as:

```python
name.lower()
name.upper()
name.strip()
```

You also compared strings:

```python
if password == "1234":
```

That idea will appear again in today's project.

---

### Stage 6 — Lists

Lists store multiple values.

```python
transactions = []
```

You learned to add items:

```python
transactions.append("Deposit")
```

and loop through them:

```python
for transaction in transactions:
    print(transaction)
```

Today's project uses a list for a transaction.

---

### Stage 7 — Dictionaries

Dictionaries store information using **key-value pairs**.

Example:

```python
product = {
    "name": "Laptop",
    "price": 50000
}
```

You learned how dictionaries can represent structured information without creating a class.

---

### Stage 8 — Functions

Functions allowed you to organize logic.

```python
def greet(name):
    print("Hello", name)
```

You learned:

* parameters
* arguments
* return values
* reusable logic

For example:

```python
def calculate_total(a, b):
    return a + b
```

---

### Stage 9 — Error Handling

You learned that user input can cause errors.

Example:

```python
try:
    amount = float(input("Enter amount: "))
except ValueError:
    print("Invalid amount")
```

This is very useful in today's bank project.

---

### Stage 10 — Files

You learned basic file writing:

```python
with open("account.txt", "w") as file:
    file.write("Account Summary")
```

and file reading:

```python
with open("account.txt", "r") as file:
    for line in file:
        print(line.strip())
```

You also learned why `with` is useful: Python automatically closes the file.

---

### Stage 11 — Classes and Objects

You moved into object-oriented programming.

You learned the basic structure:

```python
class Student:
    def __init__(self, name):
        self.name = name
```

Then you created objects:

```python
student1 = Student("Amit")
```

You learned that:

```text
Class  → blueprint
Object → actual thing created from blueprint
```

---

### Stage 12 — Methods

You added behavior inside classes.

For example:

```python
class Counter:
    def increase(self):
        # update value
```

Then, in your banking exercises, you practiced ideas like:

```text
deposit()
withdraw()
get_balance()
```

---

### Stage 13 — Basic Encapsulation

You practiced storing balance like:

```python
self._balance
```

instead of freely modifying it everywhere.

The idea was:

```text
Outside code
    ↓
BankAccount method
    ↓
Validate request
    ↓
Update _balance
```

---

### Stage 14 — Product and Cart OOP

You also practiced OOP using:

```text
Product
Cart
```

and methods such as:

```text
add_product()
remove_product()
calculate_total()
search_product()
```

This helped you understand objects stored inside lists.

---

### Stage 15 — Files + OOP Ideas

You then connected account information with files.

You practiced:

```text
Bank/account data
      ↓
Convert to text
      ↓
Write file
```

and:

```text
Text file
   ↓
Read
   ↓
Display account summary
```

---

### Stage 16 — Testing and Debugging

Yesterday, on Day 59, you practiced manually testing programs.

You learned to think about:

```text
Input
   ↓
Expected result
   ↓
Actual result
   ↓
Compare
```

You also considered edge cases such as:

```text
Wrong password
Negative amount
Insufficient balance
```

Today you will use all of that thinking in one mini project.

---

# 5. Important Topics for Today

Your final project mainly combines:

```text
variables
input/output
type conversion
if-elif-else
strings
lists
functions
error handling
classes
objects
methods
```

You also already understand:

```text
loops
dictionaries
files
```

Even though the final project is intentionally small, those topics are now part of your foundation.

---

# 6. Foundational Notes

## A. Keep the project small

Do not try to build:

* multiple bank accounts
* database storage
* login attempts
* transaction history files
* interest calculation
* account transfers
* ATM simulation

Those can come later.

Today's application should perform **one login and one banking action**.

---

## B. Start with a balance

For example, conceptually:

```text
starting balance = 5000
```

The program can create this internally.

The user does not need to enter the starting balance.

---

## C. Check the password first

Your program should follow this order:

```text
Ask password
     ↓
Is password correct?
   /       \
 No        Yes
 ↓          ↓
Stop      Show menu
```

Do not show the banking menu when the password is wrong.

---

## D. Only one action

After successful login, display something like:

```text
1. Check Balance
2. Deposit
3. Withdraw
```

The user chooses **one**.

After that action completes, the program can finish.

You do **not** need a repeated menu loop.

---

## E. Validate money before changing balance

For deposit:

```text
amount > 0
```

For withdrawal:

```text
amount > 0
```

and:

```text
amount <= balance
```

---

## F. Transactions can be very simple

You do not need a complicated transaction system.

For example:

```python
transactions = []
```

After a successful deposit, conceptually you might add:

```text
"Deposited 500"
```

After a successful withdrawal:

```text
"Withdrew 300"
```

You only need to save **one transaction** for this project.

---

## G. Invalid operations should not change the balance

For example:

```text
Balance = 5000
Withdraw = 7000
```

Result:

```text
Insufficient balance
```

Balance should still be:

```text
5000
```

---

# 7. Easy Example

Before building the bank app, think about a much simpler example: a wallet.

Suppose:

```text
Wallet balance = ₹1000
Action = deposit
Amount = ₹200
```

Think through it:

```text
Current balance
    ₹1000
       +
Deposit ₹200
       ↓
New balance
    ₹1200
```

The important Python idea is:

```text
Read value
   ↓
Validate value
   ↓
Update existing value
   ↓
Display result
```

The bank project uses exactly the same thinking.

---

# 8. Final Problem Statement

## Final Beginner Python Mini Project — Simple Bank App

Create a very simple bank application.

The program should:

1. Have a predefined password.
2. Have a starting account balance.
3. Ask the user to enter the password.
4. If the password is wrong, display an error message and stop.
5. If the password is correct, show this menu:

```text
1. Check Balance
2. Deposit
3. Withdraw
```

6. Allow the user to select **only one action**.
7. For **Check Balance**, display the current balance.
8. For **Deposit**, ask for an amount.
9. Deposit only if the amount is valid and greater than `0`.
10. For **Withdraw**, ask for an amount.
11. Withdraw only if the amount is positive and the balance is sufficient.
12. Save one successful deposit or withdrawal transaction in a list.
13. Display the result.
14. End the program.

Keep everything simple.

---

# 9. Concepts Used

### Variables

For things like:

```text
password
balance
choice
amount
```

---

### Input

For:

```text
password
menu choice
deposit amount
withdrawal amount
```

---

### Output

Using:

```python
print()
```

to show messages.

---

### Type Conversion

Convert monetary input from string to a number.

Conceptually:

```text
"500"
  ↓
500.0
```

---

### `if-elif-else`

Used for:

```text
password validation
menu choice
amount validation
balance validation
```

---

### Strings

Used for:

```text
password
messages
transactions
```

---

### Lists

Used for:

```text
transactions
```

---

### Functions

You could separate operations into functions such as:

```text
deposit
withdraw
check balance
```

---

### Error Handling

Useful when the user enters:

```text
hello
```

instead of:

```text
500
```

for an amount.

---

### Classes and Objects

With the preferred OOP approach, you can create:

```text
BankAccount class
```

and one:

```text
BankAccount object
```

---

# 10. Thought Process

Before writing Python, solve the problem logically.

### Step 1 — What data does the account need?

At minimum:

```text
balance
transactions
```

You may also keep the password separately.

---

### Step 2 — What should happen first?

Authentication.

```text
User enters password
```

Compare it with the correct password.

---

### Step 3 — What happens if authentication fails?

Nothing else.

```text
Wrong password
↓
Display message
↓
Program ends
```

---

### Step 4 — What happens after successful login?

Display the menu.

```text
1 → balance
2 → deposit
3 → withdraw
```

---

### Step 5 — What information does each action need?

Check balance:

```text
No additional input
```

Deposit:

```text
deposit amount
```

Withdraw:

```text
withdrawal amount
```

---

### Step 6 — What must be validated?

Deposit:

```text
Is amount a number?
Is amount > 0?
```

Withdrawal:

```text
Is amount a number?
Is amount > 0?
Is amount <= balance?
```

---

### Step 7 — When should a transaction be stored?

Only after a **successful financial operation**.

For example:

```text
deposit successful
      ↓
update balance
      ↓
add transaction
```

Not:

```text
invalid deposit
      ↓
add transaction   ❌
```

---

# 11. Beginner-Friendly Pseudocode

Do not write Python immediately.

First write something similar to this:

```text
START

Create correct password

Create bank account
    starting balance
    empty transactions list

Ask user for password

IF password is wrong
    print "Wrong password"

ELSE
    display menu

    ask user for choice

    IF choice is check balance
        display balance

    ELSE IF choice is deposit
        ask for amount

        try to convert amount to number

        IF amount is greater than zero
            add amount to balance
            save deposit transaction
            display updated balance
        ELSE
            display invalid amount

    ELSE IF choice is withdraw
        ask for amount

        try to convert amount to number

        IF amount is not positive
            display invalid amount

        ELSE IF amount is greater than balance
            display insufficient balance

        ELSE
            subtract amount from balance
            save withdrawal transaction
            display updated balance

    ELSE
        display invalid menu choice

END
```

That is already most of the problem-solving work.

The Python syntax comes afterward.

---

# 12. Suggested Solving Approach

## Preferred: OOP-Based Approach

Because you recently learned classes and objects, this is a good final revision exercise.

Think about this structure:

```text
BankAccount
│
├── _balance
├── transactions
│
├── get_balance()
├── deposit(amount)
└── withdraw(amount)
```

Then your main program handles:

```text
password
   ↓
menu
   ↓
user choice
   ↓
call object method
```

Conceptually:

```text
Main Program
      │
      │ successful login
      ↓
   Menu choice
      │
 ┌────┼─────┐
 ↓    ↓     ↓
Balance Deposit Withdraw
   \    |    /
    \   |   /
     BankAccount
```

This is the recommended approach.

---

## Functional Approach

You could also solve it using variables and functions.

Conceptually:

```text
balance
transactions

check_balance()
deposit()
withdraw()
```

This is also valid.

But for Day 60, try OOP first because it revises more of your recent learning.

---

# 13. Easy Edge Cases

## Edge Case 1 — Wrong Password

Input:

```text
Password: 9999
```

Expected behavior:

```text
Wrong password
```

Do not show the bank menu.

---

## Edge Case 2 — Invalid Deposit Amount

Example:

```text
Deposit amount: -500
```

Expected:

```text
Invalid amount
```

Balance should not change.

---

## Edge Case 3 — Zero Amount

```text
Deposit amount: 0
```

or:

```text
Withdrawal amount: 0
```

Treat it as invalid.

---

## Edge Case 4 — Non-Numeric Amount

Example:

```text
Deposit amount: abc
```

The program should handle the conversion problem rather than crash.

Think about:

```python
try:
    ...
except ValueError:
    ...
```

---

## Edge Case 5 — Withdrawal Greater Than Balance

Suppose:

```text
Balance = ₹5000
Withdrawal = ₹7000
```

Expected:

```text
Insufficient balance
```

Balance remains ₹5000.

---

## Edge Case 6 — Empty Transaction List

At the beginning:

```python
transactions = []
```

That is perfectly valid.

If the user selects only **Check Balance**, it can remain empty.

---

## Edge Case 7 — Invalid Menu Choice

Example:

```text
Choice: 7
```

Expected:

```text
Invalid choice
```

No balance changes should happen.

---

# 14. Common Mistakes to Avoid

### Mistake 1 — Forgetting type conversion

This:

```text
input()
```

returns a string.

For money calculations, you need a number.

---

### Mistake 2 — Depositing negative amounts

Without validation, something like:

```text
deposit -500
```

could incorrectly reduce the balance.

Check:

```text
amount > 0
```

first.

---

### Mistake 3 — Allowing overdrawing

Do not subtract the money before checking whether the account has enough balance.

Correct thinking:

```text
Check balance first
      ↓
Enough?
 /         \
No          Yes
↓             ↓
Reject     Withdraw
```

---

### Mistake 4 — Updating balance before validation

Avoid thinking like:

```text
change balance
↓
check if valid
```

Instead:

```text
validate
↓
change balance
```

---

### Mistake 5 — Forgetting `self`

Inside an OOP method, account attributes usually need:

```text
self.
```

Think:

```text
self._balance
self.transactions
```

---

### Mistake 6 — Forgetting to initialize the transaction list

Each account object should have its own empty list when it is created.

Conceptually:

```text
New BankAccount
    ↓
transactions = []
```

---

### Mistake 7 — Adding failed transactions

Do not add something to the transaction list when:

```text
deposit was invalid
withdrawal failed
password was wrong
```

Store only the successful transaction.

---

### Mistake 8 — Building too much

Do not turn today's exercise into a 500-line project.

You only need:

```text
1 login
1 account
1 menu
1 selected operation
0 or 1 transaction
```

That is enough.

---

# 15. Five Quick Self-Check Questions

### 1. What does `input()` return by default?

Think about whether it returns an integer, float, or string.

---

### 2. Why should the deposit amount be checked before updating the balance?

Think about:

```text
0
negative numbers
invalid values
```

---

### 3. Why do we check the balance before performing a withdrawal?

What would happen if:

```text
Balance = 1000
Withdrawal = 5000
```

---

### 4. What is the difference between a class and an object?

Think:

```text
BankAccount → ?
my_account  → ?
```

---

### 5. When should a transaction be added to the transaction list?

Before validation, or only after a successful operation?

---

# 16. Hint Only 💡

Start with the smallest possible class:

```text
BankAccount
    balance
    transactions
```

Then think about three simple methods:

```text
get_balance()
deposit(amount)
withdraw(amount)
```

Keep password checking and menu selection **outside the class** initially.

Build in this order:

```text
BankAccount class
      ↓
Create account object
      ↓
Ask password
      ↓
Check password
      ↓
Show 3-option menu
      ↓
Read ONE choice
      ↓
Call appropriate method
      ↓
Save successful transaction
      ↓
End
```

For the money input, remember the pattern:

```text
try
    convert input
    validate amount
    perform operation

except ValueError
    show invalid amount
```

And for withdrawal, remember the most important logic:

```text
amount <= 0
      ↓
Invalid

amount > balance
      ↓
Insufficient balance

otherwise
      ↓
Withdrawal allowed
```

**Your Day 60 goal is not complexity. Your goal is to independently connect Python fundamentals into one clean, working mini program without copying a complete solution.**
