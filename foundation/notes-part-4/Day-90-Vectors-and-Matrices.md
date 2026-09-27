# Day 90: Vectors and Matrices for Machine Learning

## 1. Day Number

**Day 90**

## 2. Topic Name

**Vectors and Matrices**

Today you will learn how machine learning represents groups of numbers using **vectors** and **matrices**.

These ideas connect directly to NumPy arrays.

---

## 3. Connection

You already learned NumPy arrays such as:

```python
import numpy as np

values = np.array([10, 20, 30])
```

In mathematics, an array like this can represent a **vector**.

A two-dimensional NumPy array can represent a **matrix**:

```python
data = np.array([
    [10, 20],
    [30, 40]
])
```

This is important because machine learning datasets are often stored as matrices.

A useful connection is:

```text
1D NumPy array → vector
2D NumPy array → matrix
```

---

## 4. Important Topics

### Scalar

A **scalar** is just one number.

For example:

```text
5
42
3.14
```

In machine learning:

```text
house price = 5000000
```

is one scalar value.

---

### Vector

A **vector** is an ordered collection of numbers.

For example:

```text
[1200, 3]
```

This could describe one house:

```text
1200 → house size
3    → number of bedrooms
```

So one vector can represent the features of one observation.

---

### Matrix

A **matrix** is a rectangular arrangement of numbers containing rows and columns.

For example:

```text
[
  [1200, 3],
  [1500, 4],
  [900,  2]
]
```

This could represent three houses.

Each row represents one house.

Each column represents one feature.

---

### Rows

A **row** usually represents one observation.

For example:

```text
[1200, 3]
```

could represent one house.

---

### Columns

A **column** usually represents one feature.

For example:

```text
Column 1 → house size
Column 2 → bedrooms
```

---

### Shape

The **shape** tells us the dimensions of an array or matrix.

For example:

```text
3 rows × 2 columns
```

has shape:

```python
(3, 2)
```

Think:

```text
shape = (number of rows, number of columns)
```

---

# 5. Foundational Notes

Machine learning models usually work with numbers.

Suppose you have a dataset:

```text
House | Size | Bedrooms
------|------|---------
A     | 1200 | 3
B     | 1500 | 4
C     | 900  | 2
```

The words `A`, `B`, and `C` are labels for us.

The numerical information can be represented as:

```text
[
  [1200, 3],
  [1500, 4],
  [900,  2]
]
```

This matrix can then be stored in NumPy and eventually given to an ML model.

The key idea is:

```text
rows    → observations
columns → features
```

---

# 6. Feature Vector Using One House

Suppose one house has:

```text
Size = 1200 square feet
Bedrooms = 3
```

We can describe that house using a feature vector:

```text
[1200, 3]
```

Here:

```text
Feature 1 = 1200
Feature 2 = 3
```

In NumPy:

```python
house = np.array([1200, 3])
```

Its shape is conceptually:

```python
(2,)
```

because it contains two values in a one-dimensional array.

For beginner-level ML thinking, the important idea is simply:

> One observation can be represented by a vector of feature values.

---

# 7. Data Matrix Using Multiple Observations

Now suppose we have three houses:

```text
House A → size 1200, bedrooms 3
House B → size 1500, bedrooms 4
House C → size 900, bedrooms 2
```

Each house has its own feature vector:

```text
House A → [1200, 3]
House B → [1500, 4]
House C → [900, 2]
```

Putting those vectors together gives a matrix:

```text
[
  [1200, 3],
  [1500, 4],
  [900,  2]
]
```

Now:

```text
Rows    = 3 houses
Columns = 2 features
```

Therefore the shape is:

```text
(3, 2)
```

---

# 8. Easy Example

Imagine customer data with two features:

```text
age
monthly_spending
```

One customer:

```text
Age = 25
Monthly spending = 4000
```

Feature vector:

```text
[25, 4000]
```

Three customers:

```text
[
  [25, 4000],
  [30, 5500],
  [22, 3000]
]
```

This matrix has:

```text
3 rows
2 columns
```

so its shape is:

```python
(3, 2)
```

In NumPy:

```python
customers = np.array([
    [25, 4000],
    [30, 5500],
    [22, 3000]
])
```

You could inspect:

```python
customers.shape
```

to see the dimensions.

---

# 9. Problem Statement

Represent three houses using two numerical features:

```text
House A:
size = 1000
bedrooms = 2

House B:
size = 1400
bedrooms = 3

House C:
size = 1800
bedrooms = 4
```

Your task is to:

1. represent each house as a feature vector
2. combine the three vectors into one matrix
3. identify the number of rows
4. identify the number of columns
5. determine the matrix shape
6. represent the matrix using a NumPy array

Do not perform any advanced matrix calculations yet.

---

# 10. Concepts Used

You will use:

- scalar
- vector
- feature
- feature vector
- matrix
- observation
- row
- column
- dimensions
- shape
- NumPy array

A useful summary is:

```text
one number             → scalar
one group of features  → vector
many feature vectors   → matrix
```

---

# 11. Thought Process

Start with one house.

Ask:

> How many features describe this house?

In the exercise:

```text
size
bedrooms
```

So there are:

```text
2 features
```

That means each house's vector contains two numbers.

For example:

```text
[1000, 2]
```

Then ask:

> How many houses are there?

There are:

```text
3 houses
```

Therefore there should be:

```text
3 vectors
```

Stack those vectors as rows:

```text
[
  [house A features],
  [house B features],
  [house C features]
]
```

Finally count:

```text
rows    = number of houses
columns = number of features
```

That gives the matrix shape.

---

# 12. Beginner-Friendly Pseudocode / NumPy Representation

Pseudocode:

```text
START

create vector for house A
    [size, bedrooms]

create vector for house B
    [size, bedrooms]

create vector for house C
    [size, bedrooms]

combine all three vectors into one matrix

print matrix

print matrix shape

END
```

NumPy structure:

```python
import numpy as np

houses = np.array([
    [size_house_a, bedrooms_house_a],
    [size_house_b, bedrooms_house_b],
    [size_house_c, bedrooms_house_c]
])

print(houses)
print(houses.shape)
```

Notice the structure:

```text
outer brackets → complete matrix

inner brackets → individual house vectors
```

---

# 13. Easy Edge Cases

## One Feature

Suppose each house only has:

```text
size
```

Then your data might look like:

```text
[
  [1000],
  [1400],
  [1800]
]
```

You still have:

```text
3 observations
1 feature
```

So the matrix shape would be:

```text
(3, 1)
```

---

## One Observation

Suppose you have only one house with two features:

```text
size = 1000
bedrooms = 2
```

As a matrix, you might represent it as:

```text
[
  [1000, 2]
]
```

Now:

```text
1 row
2 columns
```

so the shape is:

```text
(1, 2)
```

This is different from the one-dimensional vector:

```text
[1000, 2]
```

whose NumPy shape would normally be:

```text
(2,)
```

That distinction becomes useful later in machine learning.

---

# 14. Expected Matrix and Shape

For the exercise, your final structure should contain three rows:

```text
House A
House B
House C
```

and two columns:

```text
size
bedrooms
```

So conceptually:

```text
[
  [size A, bedrooms A],
  [size B, bedrooms B],
  [size C, bedrooms C]
]
```

Expected dimensions:

```text
Rows    = 3
Columns = 2
```

Therefore:

```text
Shape = (3, 2)
```

Try filling in the actual values yourself.

---

# 15. Hint Only

Start by turning each house into this pattern:

```text
[size, bedrooms]
```

So House A begins with:

```text
[1000, 2]
```

Do the same for House B and House C.

Then place all three vectors inside another pair of brackets:

```python
houses = np.array([
    [...],
    [...],
    [...]
])
```

To determine the shape, ask:

```text
How many houses?
→ number of rows

How many features for each house?
→ number of columns
```

The key lesson for **Day 90** is:

> **A vector can represent the features of one observation, while a matrix can represent many observations. In machine learning, rows commonly represent observations and columns commonly represent features.**