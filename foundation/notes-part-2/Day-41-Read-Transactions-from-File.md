# Day 41: Read Transactions from Text File
# Day 41 — Read Transactions from Text File

## 1. Day Number

**Day 41**

## 2. Topic Name

**Basic File Reading**

Today you will learn how Python reads information that has already been saved inside a text file.

---

## 3. Connection with Yesterday

Yesterday, on **Day 40**, you created transaction history and wrote those transactions into a text file.

The flow was:

```text
Python list
   ↓
write transactions
   ↓
transactions.txt
```

Today you will do the opposite:

```text
transactions.txt
   ↓
read file
   ↓
Python program
   ↓
print transactions
```

So the basic lifecycle is becoming:

```text
Create Data
    ↓
Store Data
    ↓
Read Data
    ↓
Use Data
```

This is an important foundation for later working with logs, configuration files, CSV files, databases, and persistent application data.

---

# 4. Important Topics

Today focus on:

* Read mode `"r"`
* `open()`
* `with`
* Looping through file lines
* `strip()`
* Basic idea of file-not-found errors

The important pattern is:

```python
with open("filename.txt", "r") as file:
    # read from file
```

Do not worry about memorizing it immediately. Understand what each part means first.

---

# 5. Foundational Notes

## What does reading a file mean?

Suppose `transactions.txt` contains:

```text
Deposit: 500
Withdraw: 200
Payment: 100
```

Your Python program can open this file and retrieve these values.

Conceptually:

```text
Hard Disk
   │
   │ transactions.txt
   ↓
Python Program
   │
   ↓
Read each line
```

---

## `open()`

Python provides the built-in `open()` function for working with files.

General structure:

```python
open("filename", "mode")
```

For example:

```python
open("transactions.txt", "r")
```

Here:

```text
transactions.txt  → file name
"r"               → read mode
```

---

## What is `"r"` mode?

`"r"` means:

> Open the file for reading.

Think:

```text
r = read
```

You are telling Python:

```text
I only want to read information from this file.
```

Unlike `"w"` mode from yesterday, `"r"` does **not** erase the existing file contents.

---

## Why use `with`?

You will commonly see:

```python
with open(...) as file:
```

The `with` statement handles opening and closing the file safely.

Conceptually:

```text
with
 ↓
Open file
 ↓
Use file
 ↓
Automatically close file
```

Without `with`, you would have to remember to close the file manually.

For beginners, prefer:

```python
with open(...)
```

---

## A text file can be looped through

A file containing:

```text
Deposit 500
Withdraw 100
Payment 50
```

can be processed line by line.

Conceptually:

```text
for each line in file
       ↓
process the line
```

So if there are 3 transaction lines, the loop runs 3 times.

---

## Important: lines usually contain `\n`

Suppose your file visually contains:

```text
Deposit 500
Withdraw 100
```

Internally, Python may see something similar to:

```text
"Deposit 500\n"
"Withdraw 100\n"
```

`\n` represents a newline.

If you directly print a line that already contains `\n`, `print()` adds another newline of its own.

That can produce output such as:

```text
Deposit 500

Withdraw 100
```

Notice the unwanted blank line.

---

## `strip()`

`strip()` helps remove unnecessary whitespace around a string.

Example:

```python
text = "  Deposit 500\n"
```

After using:

```python
text.strip()
```

the result becomes conceptually:

```text
"Deposit 500"
```

So:

```text
"Deposit 500\n"
       ↓ strip()
"Deposit 500"
```

This is why `strip()` is useful when reading lines from text files.

---

# 6. Easy Example

Suppose a file named:

```text
colors.txt
```

contains:

```text
Red
Blue
Green
```

You could conceptually read it using:

```python
with open("colors.txt", "r") as file:
    for line in file:
        color = line.strip()
        print(color)
```

Output:

```text
Red
Blue
Green
```

Here the important flow is:

```text
Open file
   ↓
Get one line
   ↓
Remove newline using strip()
   ↓
Print clean line
   ↓
Repeat
```

This example shows the reading technique, but it is not the solution to today's transaction problem.

---

# 7. Problem Statement

Create a Python program that:

> Reads transaction lines from a text file and prints each transaction without extra newline spaces.

Assume the transaction file may contain:

```text
Deposit: 500
Withdraw: 200
Payment: 100
```

Your program should read the file one line at a time.

For every line:

1. Remove unnecessary newline/whitespace.
2. Print the cleaned transaction.

---

# 8. Concepts Used

You will use:

### File handling

```text
open()
```

to open the transaction file.

### Read mode

```text
"r"
```

to tell Python that the file should be opened for reading.

### Context manager

```text
with
```

to safely manage the file.

### Loop

```text
for
```

to process each transaction line.

### String method

```text
strip()
```

to remove extra whitespace and newline characters.

### Function

You should place the file-reading logic inside a function.

Conceptually:

```text
main program
     ↓
read_transactions(...)
     ↓
open file
     ↓
read lines
     ↓
print transactions
```

---

# 9. Thought Process

Before coding, think through the problem.

### Step 1: Where is the information?

The transactions are no longer only inside a Python list.

They are stored inside:

```text
transactions.txt
```

So you first need to open the file.

---

### Step 2: Which mode should be used?

You only want to read existing information.

Therefore:

```text
read mode → "r"
```

---

### Step 3: How should transactions be processed?

Each transaction is stored on a separate line.

Therefore, looping through the file is a natural approach:

```text
transaction 1
transaction 2
transaction 3
```

Process them one at a time.

---

### Step 4: Why use `strip()`?

Each line may contain:

```text
\n
```

at the end.

So clean the line before printing it.

```text
line
 ↓
strip()
 ↓
clean transaction
```

---

### Step 5: What happens if the file is empty?

If the file contains no lines:

```text
transactions.txt
----------------
nothing
----------------
```

the loop simply has nothing to process.

For today's beginner problem, that is acceptable.

---

### Step 6: What happens if the file does not exist?

If Python tries to read:

```text
transactions.txt
```

but that file does not exist, Python can raise:

```text
FileNotFoundError
```

You do not need advanced error handling yet.

For now, understand the idea:

```text
Python asks for file
        ↓
Does file exist?
     /       \
   Yes        No
    ↓          ↓
 Read      FileNotFoundError
```

Later you can learn `try` and `except` to handle this cleanly.

---

# 10. Pseudocode

```text
FUNCTION read_transactions(file_name)

    OPEN file_name in read mode

    FOR each line in file

        remove extra whitespace/newline from line

        print cleaned transaction

    END FOR

END FUNCTION


CALL read_transactions with transaction file name
```

Notice that the pseudocode focuses on the logic rather than Python syntax.

---

# 11. Suggested Solving Approach

Use a **functional approach**.

Instead of putting everything directly into the main program, create a function responsible for reading the transactions.

Conceptually:

```text
read_transactions(filename)
```

Responsibility:

```text
Input:
    file name

        ↓

Function:
    open file
    read lines
    clean lines
    print transactions

        ↓

Output:
    transactions displayed
```

This keeps one responsibility inside one function.

For example:

```text
read_transactions()
       │
       ├── open
       ├── loop
       ├── strip
       └── print
```

---

# 12. Easy Edge Cases

## Edge Case 1: Empty File

Suppose:

```text
transactions.txt
```

contains nothing.

Then:

```text
for line in file
```

has no lines to process.

Possible output:

```text
No transaction output
```

For today's exercise, you do not necessarily need a special message unless you want to experiment.

---

## Edge Case 2: File Not Found

Suppose your program expects:

```text
transactions.txt
```

but the actual file is missing.

Python may produce:

```text
FileNotFoundError
```

For now, simply understand why this happens.

Common causes include:

```text
wrong filename
wrong folder
typing mistake
file was never created
```

Later you will learn how to handle this with:

```python
try
except
```

---

# 13. Expected Input

Assume `transactions.txt` already exists.

Its content could be:

```text
Deposit: 1000
Withdraw: 300
Payment: 200
```

Your function may receive the filename conceptually as:

```text
transactions.txt
```

No keyboard input is required unless you choose to ask the user for the filename.

---

# 14. Expected Output

The program should print:

```text
Deposit: 1000
Withdraw: 300
Payment: 200
```

It should **not** accidentally print:

```text
Deposit: 1000

Withdraw: 300

Payment: 200
```

The goal is clean output with one transaction per line.

---

# 15. Hint Only

Start by thinking about this structure:

```python
def read_transactions(filename):
    with open(________, "___") as file:
        for ________ in file:
            transaction = ________.strip()
            print(________)
```

Ask yourself four questions:

```text
1. What filename should open() receive?
2. Which mode means read?
3. What variable represents each line?
4. What should strip() be applied to?
```

### Today's mental model

```text
transactions.txt
       ↓
   open(..., "r")
       ↓
      with
       ↓
   for each line
       ↓
     strip()
       ↓
      print
```

**Do not write the entire program immediately.** First try completing the missing pieces in the hint yourself.
