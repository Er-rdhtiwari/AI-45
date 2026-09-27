# Day 96: Derivatives for Machine Learning

## 1. Day number

**Day 96**

## 2. Topic name

**Derivative and Rate of Change**

A derivative tells us **how quickly something is changing at a particular point**.

---

## 3. Connection

Machine learning models often try to reduce an **error**, also called a loss.

For example:

```text
Model makes prediction
        ↓
Prediction has some error
        ↓
Change model parameters
        ↓
Try to reduce the error
```

But which direction should the model change its parameters?

Derivatives help answer that question because they tell us:

> If I change this value slightly, does the error go up or down, and how quickly?

That idea becomes the foundation of optimization methods such as **gradient descent**.

---

## 4. Important topics

Today you will learn:

- **Function**
- **Slope**
- **Rate of change**
- **Derivative**
- Positive slope
- Negative slope
- Zero slope
- How derivatives connect to ML optimization

---

## 5. Foundational notes

### Function

A **function** takes an input and produces an output.

For example:

```text
f(x) = x²
```

If:

```text
x = 2
```

then:

```text
f(2) = 2²
     = 4
```

So:

```text
input       function       output

  2     →      x²      →      4
```

In machine learning, a function might represent something more useful, such as:

```text
model parameter
      ↓
error function
      ↓
amount of error
```

---

# 6. What is slope?

Before understanding derivatives, understand **slope**.

Slope describes how much one quantity changes when another quantity changes.

Imagine:

```text
x increases by 1
y increases by 3
```

The slope is:

```text
change in y
───────────
change in x
```

So:

```text
3 / 1 = 3
```

A larger positive slope means the function is rising more steeply.

---

## Positive slope

Imagine a line going upward:

```text
y
|
|         /
|       /
|     /
|   /
| /
+-------------- x
```

As `x` increases, `y` increases.

Therefore:

**Slope > 0**

---

## Negative slope

Now imagine:

```text
y
|
| \
|   \
|     \
|       \
|         \
+-------------- x
```

As `x` increases, `y` decreases.

Therefore:

**Slope < 0**

---

## Zero slope

A flat line:

```text
y
|
|
| -------------
|
|
+-------------- x
```

As `x` changes, `y` does not change.

Therefore:

**Slope = 0**

---

# 7. What is a derivative?

For a straight line, the slope is the same everywhere.

But many functions are curved.

For example:

```text
f(x) = x²
```

Its graph looks approximately like:

```text
y
|
|           *
|         *   *
|       *       *
|     *           *
|   *               *
+---------*-------------- x
```

The slope changes depending on where you are on the curve.

A **derivative** tells us the slope of the curve **at one particular point**.

Think:

```text
Slope
→ direction and steepness

Derivative
→ slope at a particular point
```

Here is the visual idea: as we look at two points closer and closer together, the slope between them approaches the slope at one point.



You do not need to master the limit formula yet. Focus on the visual meaning: **the derivative is the local slope of the curve**.

---

# 8. Easy example using a simple function

Consider:

```text
f(x) = x²
```

Let's inspect nearby values:

```text
x     f(x)

1       1
2       4
3       9
4      16
```

Notice that the output grows faster as `x` increases.

Between `1` and `2`:

```text
change in y = 4 - 1 = 3
change in x = 2 - 1 = 1

slope ≈ 3
```

Between `2` and `3`:

```text
change in y = 9 - 4 = 5

slope ≈ 5
```

Between `3` and `4`:

```text
change in y = 16 - 9 = 7

slope ≈ 7
```

The function becomes steeper as we move right.

A derivative lets us talk about that slope at an **exact point**, rather than only between two widely separated points.

---

# 9. Problem statement

Imagine a quantity changes like this:

```text
x     y

1     10
2     15
3     20
4     25
```

For each step, ask:

1. Does `y` increase, decrease, or remain unchanged?
2. Is the slope positive, negative, or zero?
3. What does that slope tell us about the relationship between `x` and `y`?

Then compare it with:

```text
x     y

1     20
2     15
3     10
4      5
```

And finally:

```text
x     y

1     10
2     10
3     10
4     10
```

Your goal is to identify the **direction of change**, not use advanced calculus.

---

# 10. Concepts used

You are using:

- input
- output
- function
- change
- slope
- rate of change
- derivative
- positive slope
- negative slope
- zero slope

Later these ideas become:

```text
model parameter
       ↓
loss/error function
       ↓
derivative
       ↓
direction to change parameter
```

---

# 11. Thought process

When looking at a changing quantity, think:

```text
Start with two nearby values
        ↓
Did x increase?
        ↓
What happened to y?
        ↓
y increased
→ positive slope

y decreased
→ negative slope

y stayed unchanged
→ zero slope
```

Then consider a curved function.

Instead of asking only about two distant points, ask:

> What is the slope right here?

That local slope is what the derivative describes.

---

# 12. Beginner-friendly mathematical steps

Suppose:

```text
Point 1:
x = 2
y = 5

Point 2:
x = 3
y = 8
```

### Step 1: Find the change in x

```text
3 - 2 = 1
```

### Step 2: Find the change in y

```text
8 - 5 = 3
```

### Step 3: Calculate slope

```text
slope =
change in y / change in x
```

Therefore:

```text
slope = 3 / 1
      = 3
```

The slope is positive.

Interpretation:

> Increasing `x` is associated with an increase in `y` over this interval.

---

## Negative example

Suppose:

```text
Point 1 = (2, 8)
Point 2 = (3, 5)
```

Then:

```text
change in x = 1
change in y = -3

slope = -3 / 1
      = -3
```

The negative sign tells us the function is moving downward.

---

## Flat example

Suppose:

```text
Point 1 = (2, 5)
Point 2 = (3, 5)
```

Then:

```text
change in y = 0
```

Therefore:

```text
slope = 0
```

The function is flat across that interval.

---

# 13. Connection to model optimization

This is where derivatives become extremely important in machine learning.

Suppose a model has one adjustable parameter:

```text
w
```

and an error function:

```text
Error(w)
```

Imagine the error curve:

```text
Error
  |
  | *
  |   *
  |     *
  |       *       *
  |         *   *
  |           *
  +-------------------- w
              ↑
          low error
```

The model wants to move toward the bottom.

### If the derivative is positive

Imagine we are on the right side:

```text
          /
        /
      *
```

The function rises as we move right.

So the derivative is positive.

To reduce the error, we generally want to move in the **opposite direction**.

```text
positive derivative
        ↓
move parameter lower
        ↓
try to reduce error
```

### If the derivative is negative

On the left side:

```text
*
 \
  \
   \
```

The derivative is negative.

Moving right may reduce the error.

```text
negative derivative
        ↓
move parameter higher
        ↓
try to reduce error
```

### If the derivative is around zero

Near the bottom:

```text
       __
     /    \
```

the curve may be almost flat.

So:

```text
derivative ≈ 0
```

This can indicate that we are near a minimum, although later you will learn that a zero derivative does not always guarantee a minimum.

---

# 14. Why this matters for gradient descent

A simplified gradient descent idea is:

```text
Current parameter
       ↓
Calculate derivative of error
       ↓
See which direction error increases
       ↓
Move in the opposite direction
       ↓
Hopefully reduce error
       ↓
Repeat
```

A very simplified update looks like:

```text
new value
=
old value - small step × derivative
```

You do **not** need to memorize this yet.

The important intuition is:

> The derivative acts like a direction sign telling the model which way the error is changing.

For example:

```text
Derivative = positive
→ error rises toward the right
→ move left

Derivative = negative
→ error falls toward the right
→ move right

Derivative ≈ 0
→ curve is locally flat
```

This is one of the key mathematical ideas behind training many ML models.

---

# 15. Easy edge cases

### Flat slope

Suppose:

```text
f(x) = 10
```

No matter what `x` is:

```text
x = 1 → y = 10
x = 2 → y = 10
x = 3 → y = 10
```

Nothing changes.

Therefore:

```text
slope = 0
derivative = 0
```

---

### Negative slope

Suppose:

```text
x     y

1     10
2      8
3      6
4      4
```

As `x` increases:

```text
y decreases
```

Therefore the slope is negative.

---

### Very steep slope

If a tiny change in `x` produces a large change in `y`, the magnitude of the slope is large.

For example:

```text
x changes by 1
y changes by 100
```

This indicates a much steeper change than:

```text
x changes by 1
y changes by 2
```

---

# 16. Expected interpretation

For:

```text
x     y

1     10
2     15
3     20
4     25
```

you should recognize:

```text
y increases as x increases
        ↓
positive slope
```

For:

```text
1     20
2     15
3     10
4      5
```

you should recognize:

```text
y decreases as x increases
        ↓
negative slope
```

For:

```text
1     10
2     10
3     10
4     10
```

you should recognize:

```text
y does not change
        ↓
zero slope
```

The most important idea from Day 96 is:

```text
Derivative
    ↓
tells us the local slope

Slope
    ↓
tells us direction and rate of change

In machine learning
    ↓
derivatives help determine how
to change model parameters
to reduce error
```

---

# 17. Hint only

For each dataset in the exercise, first ignore calculus completely.

Compare one row with the next and ask:

```text
When x increases,
what happens to y?
```

Use this rule:

```text
y goes up   → positive slope
y goes down → negative slope
y stays     → zero slope
```

Then connect it to machine learning:

> If `y` represented model error, which direction would you want to move `x` so that the error becomes smaller?

That question captures the basic intuition behind using derivatives for optimization.