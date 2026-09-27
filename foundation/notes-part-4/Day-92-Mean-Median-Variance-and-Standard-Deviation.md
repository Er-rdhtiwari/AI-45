# Day 92: Descriptive Statistics

## 1. Day number

**Day 92**

## 2. Topic name

**Mean, Median, Variance, and Standard Deviation**

## 3. Connection

You can already represent numerical datasets using Python lists and NumPy arrays.

Today you will learn how to **summarize how those numbers behave**.

Instead of looking at every individual value, descriptive statistics can answer questions such as:

- What is the typical value?
- Where is the middle of the data?
- Are the values close together?
- Are the values spread far apart?

---

## 4. Important topics

The main ideas are:

- **Mean** — the average value
- **Median** — the middle value
- **Spread** — how far apart the values are
- **Variance** — average squared distance from the mean
- **Standard deviation** — a more intuitive measurement of spread

A useful mental model is:

**Mean/median → center of the data**

**Variance/standard deviation → spread of the data**

---

## 5. Foundational notes

Consider monthly sales:

```text
10, 12, 14, 16, 18
```

There are two basic things we might want to know.

First, what value represents the **center**?

Second, how much do the individual values **move away from that center**?

Descriptive statistics help answer these questions without making predictions about the future.

---

## 6. Understanding each concept intuitively

### Mean

The **mean** is what we normally call the **average**.

Imagine combining all the sales and redistributing them equally across the five months. The amount each month would receive is the mean.

Conceptually:

```text
Mean = total of all values / number of values
```

For:

```text
10, 12, 14, 16, 18
```

the total is:

```text
70
```

There are five values:

```text
70 / 5 = 14
```

So:

**Mean = 14**

### Median

The **median** is the value sitting in the middle after the numbers have been sorted.

```text
10, 12, 14, 16, 18
        ↑
      middle
```

Therefore:

**Median = 14**

For an odd number of values, there is one middle value.

For an even number of values, we normally take the average of the two middle values.

### Spread

Two datasets can have the same mean but behave very differently.

For example:

```text
Dataset A: 13, 14, 14, 14, 15
Dataset B:  2,  8, 14, 20, 26
```

Both are centered around `14`, but Dataset B is much more spread out.

That is why the mean alone does not completely describe a dataset.

### Variance

Variance measures how far the values are spread around the mean.

The basic idea is:

1. Find the mean.
2. Measure how far every value is from the mean.
3. Square those distances.
4. Find their average.

Squaring prevents positive and negative differences from cancelling each other.

For our example, the mean is `14`.

```text
Value    Difference from mean    Squared difference

10             -4                     16
12             -2                      4
14              0                      0
16              2                      4
18              4                     16
```

The squared differences total:

```text
16 + 4 + 0 + 4 + 16 = 40
```

For this beginner example, divide by the number of values:

```text
40 / 5 = 8
```

So:

**Variance = 8**

A **small variance** means the numbers are relatively close together.

A **large variance** means they are more spread out.

### Standard deviation

Standard deviation is closely related to variance.

It is simply the **square root of the variance**.

For our example:

```text
Variance = 8

Standard deviation = √8
                   ≈ 2.83
```

So:

**Standard deviation ≈ 2.83**

Standard deviation is often easier to interpret because it uses roughly the **same units as the original data**.

For example, if sales were measured in thousands of units, the standard deviation would also be interpreted in thousands of units.



---

## 7. Easy numerical example

Suppose five months produced these sales:

```text
10, 12, 14, 16, 18
```

The main descriptive statistics are:

| Statistic | Result |
|---|---:|
| Mean | 14 |
| Median | 14 |
| Variance | 8 |
| Standard deviation | ≈ 2.83 |

You can read this as:

> Sales are centered around 14, and the individual monthly values have some moderate spread around that center.

---

## 8. Problem statement

Given these five monthly sales numbers:

```text
20, 25, 25, 30, 50
```

Your task is to:

1. Calculate the **mean**.
2. Calculate the **median**.
3. Think about how far the numbers are from the mean.
4. Explain what **variance** tells you about these sales.
5. Explain what **standard deviation** tells you about these sales.

Notice that `50` is quite far from the other values. Think about how this might affect the mean and the spread.

---

## 9. Concepts used

You will use:

- numerical data
- sorting
- addition
- division
- mean
- median
- difference from the mean
- squaring
- variance
- square root
- standard deviation

These ideas will become important later when working with **data analysis and machine learning**.

---

## 10. Thought process

When you receive a small numerical dataset, think in this order:

```text
What are my values?
        ↓
What is their center?
        ↓
Calculate mean
        ↓
Sort them and find median
        ↓
How far is each value from the mean?
        ↓
Square those differences
        ↓
Calculate variance
        ↓
Square root the variance
        ↓
Get standard deviation
```

Do not try to memorize everything at once.

Remember the simpler distinction:

```text
Mean + Median
      ↓
Where is the data centered?


Variance + Standard deviation
      ↓
How spread out is the data?
```

---

## 11. Beginner-friendly calculation steps

Suppose:

```text
values = 10, 12, 14, 16, 18
```

### Step 1: Add the values

```text
10 + 12 + 14 + 16 + 18
= 70
```

### Step 2: Calculate the mean

```text
70 / 5
= 14
```

### Step 3: Find the median

The values are already sorted:

```text
10, 12, 14, 16, 18
```

Middle value:

```text
14
```

### Step 4: Find differences from the mean

```text
10 - 14 = -4
12 - 14 = -2
14 - 14 =  0
16 - 14 =  2
18 - 14 =  4
```

### Step 5: Square the differences

```text
(-4)² = 16
(-2)² = 4
  0²  = 0
  2²  = 4
  4²  = 16
```

### Step 6: Calculate variance

```text
(16 + 4 + 0 + 4 + 16) / 5

= 40 / 5

= 8
```

### Step 7: Calculate standard deviation

```text
√8 ≈ 2.83
```

---

## 12. How Python/NumPy could calculate them conceptually

NumPy already provides functions for these calculations.

Conceptually:

```python
import numpy as np

sales = np.array([...])

mean_value = np.mean(sales)
median_value = np.median(sales)
variance_value = np.var(sales)
standard_deviation = np.std(sales)
```

Think of the functions as:

```text
np.mean()
     ↓
Find the average

np.median()
     ↓
Find the middle

np.var()
     ↓
Measure squared spread

np.std()
     ↓
Measure spread in a more intuitive form
```

For now, understanding **what each result means** is more important than memorizing the functions.

---

## 13. Easy edge cases

### All values are equal

Suppose:

```text
20, 20, 20, 20, 20
```

Mean:

```text
20
```

Every value is exactly equal to the mean.

Therefore there is no spread:

```text
Variance = 0
Standard deviation = 0
```

This makes intuitive sense: nothing varies.

### Only one value

Suppose:

```text
25
```

Then:

```text
Mean = 25
Median = 25
```

For the simple population-style calculation used here:

```text
Variance = 0
Standard deviation = 0
```

There is only one value, so there is no spread between values.

---

## 14. Expected calculations

For the example:

```text
10, 12, 14, 16, 18
```

you should obtain:

```text
Mean = 14

Median = 14

Squared differences:
16, 4, 0, 4, 16

Variance = 8

Standard deviation ≈ 2.83
```

The key interpretation is:

**14 describes the center.**

**8 and 2.83 describe the spread around that center.**

One important beginner distinction is:

```text
Mean       → average
Median     → middle
Variance   → squared spread
Std. dev.  → easier-to-interpret spread
```

---

## 15. Hint only

For your exercise:

```text
20, 25, 25, 30, 50
```

Start by calculating:

```text
20 + 25 + 25 + 30 + 50
```

Then divide by the **number of months**.

For the median, sort the numbers and look for the **middle value**.

For variance, first ask:

> How far is each sales number from the mean?

For standard deviation, remember:

```text
standard deviation = square root of variance
```

Also pay special attention to `50`. Ask yourself: **does a value far away from the others increase or decrease the spread?**