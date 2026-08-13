# Day 33: Apply Discount
# Day 33 — Apply Discount

## 1. Day Number

**Day 33**

## 2. Topic Name

**Percentage and `if-else`**

Today you will learn how to calculate a percentage and use a condition to decide whether a discount should be applied.

---

## 3. Connection

Yesterday, you calculated the **total price of the cart**.

Today, you will take that cart total and apply a simple discount:

```text
Products
   ↓
Cart
   ↓
Cart Total
   ↓
Check Discount Condition
   ↓
Final Amount
```

So your shopping-cart program is becoming more realistic.

---

# 4. Important Topics

Today's important concepts are:

* Percentage
* Arithmetic
* `if-else`
* Comparison operators
* Functions
* Returning a calculated value

The main idea is:

```text
If condition is true
    do something
otherwise
    do something else
```

---

# 5. Foundational Notes

## A. What is a percentage?

A percentage means **a part out of 100**.

For example:

```text
10% means 10 out of 100.
```

So:

```text
10% of 200 = 20
```

Conceptually:

```text
percentage amount = original amount × percentage / 100
```

For example:

```text
20% of 100
= 100 × 20 / 100
= 20
```

---

## B. What is a discount?

A discount reduces the original price.

Suppose:

```text
Original price = 1000
Discount = 10%
```

First calculate the discount amount:

```text
10% of 1000 = 100
```

Then subtract it:

```text
1000 - 100 = 900
```

So:

```text
Final price = 900
```

Think of it as:

```text
Original Total
      |
      v
Calculate Discount
      |
      v
Subtract Discount
      |
      v
Final Total
```

---

## C. What does `if-else` do?

`if-else` lets your program make a decision.

Basic structure:

```python
if condition:
    # run when condition is True
else:
    # run when condition is False
```

For example:

```python
age = 20

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

The program checks:

```text
Is age >= 18?
```

If yes:

```text
Adult
```

Otherwise:

```text
Minor
```

---

## D. Comparison operators

You already need to recognize these:

| Operator | Meaning                  |
| -------- | ------------------------ |
| `>`      | Greater than             |
| `<`      | Less than                |
| `>=`     | Greater than or equal to |
| `<=`     | Less than or equal to    |
| `==`     | Equal to                 |
| `!=`     | Not equal to             |

Today's condition specifically says:

> discount only when total is **greater than 500**

So pay close attention to the difference between:

```python
> 500
```

and

```python
>= 500
```

They are **not** the same.

---

# 6. Easy Example

Let's use a different example from today's problem.

Suppose a shop gives a **20% discount when the amount is greater than 1000**.

Imagine:

```text
amount = 1500
```

Check:

```text
1500 > 1000
```

This is:

```text
True
```

Calculate:

```text
20% of 1500 = 300
```

Then:

```text
1500 - 300 = 1200
```

So the discounted amount would be:

```text
1200
```

But if:

```text
amount = 800
```

the condition:

```text
800 > 1000
```

is false.

Therefore:

```text
Final amount = 800
```

No discount is applied.

---

# 7. Problem Statement

Create a Python program that:

> Asks the user for the cart total.

Then:

> If the cart total is greater than `500`, apply a `10%` discount.

Otherwise:

> Keep the original cart total.

Finally, display the final amount.

### Example logic

```text
Cart total
     ↓
Is total > 500?
   /        \
 Yes         No
  |           |
10% discount  Keep total
  |           |
   \         /
    Final Amount
```

---

# 8. Concepts Used

You will use:

### Variables

To store values such as:

```text
cart total
discount
final total
```

### Arithmetic

You need:

```text
*
/
-
```

for percentage calculation and subtraction.

### Comparison

You need to check whether:

```text
cart total > 500
```

### `if-else`

Used to choose between:

```text
apply discount
```

and:

```text
keep original amount
```

### Function

Instead of putting all logic directly in the program, place the discount calculation inside a function.

---

# 9. Thought Process

Before writing Python, think about the problem in small steps.

### Step 1: Get the cart total

You need a number representing the total amount.

For example:

```text
800
```

### Step 2: Check the condition

Ask:

```text
Is 800 greater than 500?
```

Yes.

Therefore, a discount should be applied.

### Step 3: Calculate 10%

Think:

```text
discount = 10% of cart total
```

For `800`:

```text
10% of 800 = 80
```

### Step 4: Calculate the final amount

```text
800 - 80 = 720
```

### Step 5: Return/display the result

The program should produce:

```text
Final total: 720
```

The overall reasoning is:

```text
Input total
    ↓
Check total > 500
    ↓
+----------+----------+
|                     |
True                 False
|                     |
Calculate 10%       No discount
|                     |
Subtract it          Keep total
|                     |
+----------+----------+
           |
           v
      Final total
```

---

# 10. Pseudocode

Write the logic in plain language before Python:

```text
START

DEFINE a function that receives cart total

    IF cart total is greater than 500
        calculate 10 percent discount
        subtract discount from cart total
        return discounted total
    ELSE
        return original cart total

ASK user for cart total

CONVERT input into a number

CALL the discount function

STORE returned value

PRINT final total

END
```

Notice that this explains the algorithm without giving you the full Python implementation.

---

# 11. Suggested Solving Approach — Functional Approach

Use a **function** to handle the discount calculation.

Conceptually:

```text
main program
    |
    | cart_total
    v
discount function
    |
    | checks > 500
    |
    | calculates result
    v
return final_total
    |
    v
main program prints result
```

A good function design would look conceptually like:

```text
calculate_discount(total)

Input:
    total

Process:
    check discount condition

Output:
    final total
```

The function should have **one simple responsibility**:

> Take a total and determine the final price after the discount rule.

This is better than mixing input, calculation, and printing into one large block of logic.

---

# 12. Easy Edge Cases

## Edge Case 1: Total exactly `500`

Suppose:

```text
total = 500
```

The rule says:

```text
greater than 500
```

Check:

```text
500 > 500
```

This is:

```text
False
```

Therefore:

```text
No discount
```

Final amount:

```text
500
```

This is an important boundary condition.

---

## Edge Case 2: Total below `500`

Example:

```text
total = 400
```

Check:

```text
400 > 500
```

False.

So:

```text
Final amount = 400
```

---

## Edge Case 3: Total `0`

Example:

```text
total = 0
```

Check:

```text
0 > 500
```

False.

Therefore:

```text
Final amount = 0
```

Your program should still behave correctly.

---

# 13. Expected Input

One cart-total value.

For example:

```text
Enter cart total: 800
```

For today's beginner exercise, you can assume the user enters a valid number.

---

# 14. Expected Output

### Example 1 — Discount applied

Input:

```text
Enter cart total: 800
```

Calculation:

```text
10% of 800 = 80
800 - 80 = 720
```

Expected output:

```text
Final total: 720
```

### Example 2 — No discount

Input:

```text
Enter cart total: 450
```

Expected output:

```text
Final total: 450
```

### Example 3 — Exactly 500

Input:

```text
Enter cart total: 500
```

Expected output:

```text
Final total: 500
```

---

# 15. Hint Only

Think about these three questions while coding:

1. Which comparison operator represents **greater than 500**?
2. How can you calculate **10% of `total`** using multiplication and division?
3. What should your function return when the condition is false?

A useful mental model is:

```text
discount_amount = percentage of total

final_total = total - discount_amount
```

Then place that calculation inside the correct branch of your `if-else`.

**Do not forget:** `500` itself should **not** receive the discount because the requirement says **greater than 500**, not greater than or equal to 500.
