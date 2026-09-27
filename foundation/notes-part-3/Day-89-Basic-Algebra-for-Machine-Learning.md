# Day 89: Basic Algebra for Machine Learning

## 1. Day Number

**Day 89**

## 2. Topic Name

**Variables, Equations, Functions, and Simple Linear Relationships**

Today you will learn some school-level algebra that appears frequently in machine learning.

The main ideas are:

- variable
- constant
- equation
- coefficient
- function
- linear equation

No advanced mathematics is needed.

---

## 3. Connection

You already use **variables in Python**:

```python
distance = 5
price = 100
```

In mathematics, variables have a similar purpose.

For example:

\[
x = 5
\]

Here, `x` represents a value.

Machine learning formulas often use variables such as:

```text
x → input
y → output
```

For example:

```text
x = size of a house
y = estimated house price
```

Today you will learn how an input can be mathematically connected to an output.

---

# 4. Important Topics

### Variable

A **variable** represents a value that can change.

For example:

\[
x = \text{distance travelled}
\]

If different customers live at different distances, `x` might be:

```text
1 km
3 km
5 km
10 km
```

In Python, the idea is similar:

```python
x = 5
```

---

### Constant

A **constant** is a fixed value.

Suppose every delivery has a fixed starting charge of ₹40.

Then:

```text
40 = constant
```

It stays the same even when the distance changes.

---

### Equation

An **equation** says that two mathematical expressions are equal.

For example:

\[
y = 10x + 40
\]

It describes how `y` depends on `x`.

---

### Coefficient

A **coefficient** is a number multiplying a variable.

For example:

\[
y = 10x + 40
\]

The coefficient of `x` is:

```text
10
```

because:

\[
10x = 10 \times x
\]

---

### Function

A **function** takes an input and produces an output.

For example:

```text
input distance
     ↓
delivery-cost function
     ↓
output cost
```

You might write:

\[
f(x) = 10x + 40
\]

If `x` changes, the function calculates a new result.

This is similar to a Python function:

```python
def delivery_cost(x):
    return 10 * x + 40
```

---

### Linear Equation

A simple linear equation has a relationship that changes at a constant rate.

One common form is:

\[
y = mx + b
\]

where:

```text
x = input
y = output
m = coefficient / slope
b = constant / intercept
```

---

# 5. Foundational Notes

When learning machine learning mathematics, do not think of the letters as mysterious symbols.

Ask what each letter represents.

For example:

```text
x = delivery distance
y = delivery cost
m = cost added for every kilometre
b = starting delivery charge
```

Then the formula becomes much easier to understand.

A useful translation is:

```text
Mathematics:
y = mx + b

Plain English:
output =
(rate × input)
+ starting amount
```

---

# 6. Understanding `y = mx + b`

Suppose a delivery company charges:

```text
Base delivery charge = ₹40
Additional charge     = ₹10 per kilometre
```

Let:

```text
x = distance in kilometres
y = total delivery cost
```

Here:

```text
m = 10
b = 40
```

The relationship is:



In this example:

### `x`

The input.

```text
x = distance
```

### `y`

The output we want to calculate.

```text
y = delivery cost
```

### `m`

The amount `y` changes when `x` increases by one.

```text
m = ₹10 per kilometre
```

### `b`

The starting value when `x = 0`.

```text
b = ₹40
```

So even for zero kilometres, the model starts with the ₹40 base charge.

---

# 7. Easy Numerical Example

Suppose:

```text
x = 5 km
m = 10
b = 40
```

Substitute the numbers:

\[
y = 10(5) + 40
\]

First multiply:

\[
10 \times 5 = 50
\]

Then add the constant:

\[
50 + 40 = 90
\]

Therefore:

```text
For 5 km:

Delivery cost = ₹90
```

In Python, the same calculation could be written as:

```python
x = 5
m = 10
b = 40

y = m * x + b
```

The mathematical and Python ideas are almost identical.

---

# 8. Problem Statement

A delivery company uses the following rule:

```text
Base delivery charge = ₹30
Cost per kilometre   = ₹8
```

Let:

```text
x = delivery distance
y = total delivery cost
```

Use the linear relationship to calculate the delivery cost for:

```text
x = 2 km
x = 5 km
x = 10 km
```

Your goal is to identify:

```text
m = ?
b = ?
```

and then substitute each value of `x`.

---

# 9. Concepts Used

This exercise uses:

- variable
- input
- output
- constant
- coefficient
- multiplication
- addition
- equation
- function
- linear relationship

The important interpretation is:

```text
x → distance
m → price per kilometre
b → base charge
y → final delivery cost
```

---

# 10. Thought Process

When you see a formula such as a linear relationship, do not immediately calculate.

First identify what everything means.

### Step 1: Identify the input

Here:

```text
x = distance
```

### Step 2: Identify the coefficient

Ask:

> How much does the cost increase for each kilometre?

That number becomes `m`.

### Step 3: Identify the constant

Ask:

> What amount must be paid regardless of distance?

That becomes `b`.

### Step 4: Substitute `x`

For each distance, replace `x` with the given number.

### Step 5: Multiply first

Calculate:

```text
m × x
```

### Step 6: Add the constant

Finally:

```text
(m × x) + b
```

That gives `y`.

---

# 11. Beginner-Friendly Mathematical Steps

For every input value, follow the same pattern:

```text
1. Write the formula.

2. Identify m.

3. Identify b.

4. Replace x with the input value.

5. Multiply m × x.

6. Add b.

7. The answer is y.
```

For example, with different practice numbers:

```text
m = 4
b = 20
x = 3
```

Start with:

\[
y = 4(3) + 20
\]

Multiply:

\[
4 \times 3 = 12
\]

Add:

\[
12 + 20 = 32
\]

Therefore:

```text
x = 3
y = 32
```

---

# 12. Connection to Future Linear Regression

This algebra becomes very important when you learn **Linear Regression**.

Imagine a dataset containing:

```text
House Size | House Price
-----------|------------
800        | ₹...
1000       | ₹...
1200       | ₹...
1500       | ₹...
```

You might use:

```text
x = house size
y = predicted house price
```

A simple linear regression model tries to learn a relationship similar to:

```text
predicted price
=
(coefficient × house size)
+
starting value
```

The important difference is that today **you are given** the coefficient and constant.

Later, in Linear Regression, the machine-learning algorithm will try to **learn suitable values from data**.

For now, simply understand how an input travels through a linear formula to produce an output.

---

# 13. Easy Edge Cases

## Case 1: `x = 0`

Suppose:

```text
m = 10
b = 40
x = 0
```

Then:

\[
y = 10(0) + 40
\]

Since:

\[
10 \times 0 = 0
\]

the output is simply:

```text
y = 40
```

This helps explain the meaning of `b`.

When the input is zero, `b` is the starting output.

---

## Case 2: Coefficient = 0

Suppose:

```text
m = 0
b = 50
```

Now changing `x` does not affect the result because:

```text
0 × x = 0
```

So:

```text
x = 1  → y = 50
x = 5  → y = 50
x = 20 → y = 50
```

The output remains constant.

---

# 14. Expected Calculations

For your delivery-cost exercise, your working should have this structure:

| Distance (`x`) | Calculation | Delivery cost (`y`) |
|---:|---|---:|
| 2 km | `(cost per km × 2) + base charge` | Calculate |
| 5 km | `(cost per km × 5) + base charge` | Calculate |
| 10 km | `(cost per km × 10) + base charge` | Calculate |

You should notice that as distance increases, the delivery cost also increases at a **constant rate**.

For every additional kilometre, the output increases by the same amount.

That constant rate is the **coefficient**.

---

# 15. Hint Only

For the exercise:

```text
Base charge = ₹30
Cost per km = ₹8
```

Ask yourself:

```text
Which number is multiplied by x?
→ that is m

Which number stays fixed?
→ that is b
```

Then, for `x = 2`, begin by substituting the values into the linear formula.

Repeat exactly the same process for:

```text
x = 5
x = 10
```

Try to calculate the three final values yourself.

The key lesson for **Day 89** is:

> **A linear relationship connects an input and an output using a constant rate of change and a starting value. Understanding this simple algebra prepares you for Linear Regression, where a model learns those values from data.**