# Day 80: Beginner Exploratory Data Analysis (EDA)

## 1. Day number

**Day 80**

## 2. Topic name

**Exploratory Data Analysis (EDA)**

EDA means exploring a dataset before doing deeper analysis or machine learning. You inspect the data, summarize it, and visualize it so you understand what is actually inside.

## 3. Connection

You can now **inspect, clean, and visualize data**.

Yesterday, you used Seaborn to create simple visualizations from DataFrames. Today, you will combine several skills:

**Inspect → Check quality → Summarize → Visualize → Observe**

This complete process is the beginning of **Exploratory Data Analysis**.

---

## 4. Important topics

### `shape`

`shape` tells you how many **rows and columns** a DataFrame contains.

For example, a result like:

```text
(5, 3)
```

means:

- 5 rows
- 3 columns

### `columns`

The columns tell you which features or variables exist in the dataset.

A sales dataset might contain:

```text
Product
Advertising
Sales
```

### Data types

Every column has a data type.

Examples:

```text
Product        object
Advertising    int64
Sales          int64
```

Checking data types can reveal problems such as numbers accidentally stored as text.

### Missing values

Real datasets can contain missing information.

For example:

```text
Product       0
Advertising   1
Sales         0
```

This means the `Advertising` column has one missing value.

### Summary statistics

Pandas can calculate basic numerical summaries such as:

- count
- mean
- minimum
- maximum
- quartiles

A common EDA method is:

```python
df.describe()
```

You do not need to understand every statistic deeply yet. At this stage, focus mainly on **count, mean, min, and max**.

### Distributions

A **distribution** describes how values are spread.

Suppose sales values are:

```text
40, 42, 45, 47, 100
```

Most values are around 40–47, but one value is much higher.

A simple plot can make this pattern easier to notice.

### Relationships

EDA also asks whether two variables appear related.

For example:

```text
Advertising spend → Sales
```

You might investigate:

> When advertising spend increases, do sales also seem to increase?

A scatter plot can help you explore this.

---

# 5. Foundational notes

EDA is usually performed **before machine learning or detailed analysis**.

During EDA, you are trying to understand questions such as:

- How large is the dataset?
- What columns exist?
- What type of information does each column contain?
- Are values missing?
- What are typical values?
- Are some values unusually large or small?
- How are values distributed?
- Do two variables appear related?

EDA is mostly about **asking questions about the data**.

You are not trying to prove anything yet.

---

# 6. Purpose of EDA

Imagine someone gives you a spreadsheet containing 10,000 sales records.

It would be risky to immediately build a machine-learning model.

First, you would want to know things like:

```text
Are there missing sales values?

Are prices stored as numbers?

Are there duplicate records?

What is the average sales amount?

Are most sales small or large?

Does advertising appear related to sales?
```

EDA helps answer these questions.

A useful beginner definition is:

> **EDA is the process of inspecting, summarizing, and visualizing data so that we understand it before performing deeper analysis.**

EDA can also reveal problems that need cleaning.

---

# 7. Easy EDA workflow

A beginner-friendly workflow is:

### Step 1 — Look at the dataset

Start by viewing a few rows.

For example:

```python
df.head()
```

Do not immediately modify the data.

First understand what it contains.

### Step 2 — Check its size

Use the DataFrame's shape.

Ask:

```text
How many rows?

How many columns?
```

### Step 3 — Check column names

Understand what each column represents.

For example:

```text
Product
Advertising
Sales
```

### Step 4 — Check data types

Make sure numerical columns are actually numerical.

### Step 5 — Check missing values

Determine whether any columns contain missing information.

### Step 6 — Calculate summaries

For numerical columns, inspect basic values such as:

```text
mean
minimum
maximum
```

### Step 7 — Create a visualization

Choose a simple chart that answers one useful question.

For example:

```text
Does advertising spending appear related to sales?
```

A **scatter plot** would be appropriate.

### Step 8 — Write observations

Do not just create the chart.

Explain what you notice.

For example:

```text
Sales seem to increase when advertising spending increases.
```

That observation is part of EDA.

---

# 8. Problem statement

Create a tiny sales dataset similar to this:

| Product | Advertising | Sales |
|---|---:|---:|
| A | 100 | 40 |
| B | 150 | 55 |
| C | 200 | 65 |
| D | 250 | 78 |
| E | 300 | 90 |

Perform a small exploratory data analysis.

Your program should:

1. Inspect the first few rows.
2. Find the number of rows and columns.
3. Inspect the column names.
4. Check the data types.
5. Check whether values are missing.
6. Calculate basic numerical summary statistics.
7. Create **one useful visualization**.
8. Write one or two simple observations based on the results.

Do not perform advanced statistical testing.

---

# 9. Concepts used

This exercise combines several ideas from previous days:

- Python
- Pandas
- DataFrames
- rows and columns
- `head()`
- `shape`
- `columns`
- `dtypes`
- missing-value checking
- summary statistics
- numerical data
- Seaborn or Matplotlib
- scatter plots
- interpreting visualizations

This is important because EDA is not really one new Python command.

It is a **workflow combining several tools you already know**.

---

# 10. Thought process

Suppose you receive the sales dataset.

First ask:

> What does this dataset contain?

Look at the rows and columns.

Then ask:

> Is the dataset structured correctly?

Check the column names and data types.

Next:

> Is any information missing?

Check missing values.

Then:

> What are the typical numerical values?

Look at summary statistics.

Finally:

> Is there an interesting relationship worth seeing visually?

Since the dataset contains both `Advertising` and `Sales`, comparing those two variables makes sense.

You could place:

```text
Advertising → x-axis
Sales → y-axis
```

Then inspect the pattern.

The goal is not simply:

> "Make a graph."

The better question is:

> "What question can this graph help me answer?"

That mindset is very important in data analysis.

---

# 11. Beginner-friendly pseudocode

```text
START

Import Pandas

Import a simple visualization library

Create a small sales DataFrame

Display the first few rows

Display the DataFrame shape

Display column names

Display data types

Check for missing values

Calculate basic summary statistics

Choose two useful numerical columns

Create one simple visualization

Look at the results

Write one or two observations

END
```

Notice that the order matters.

You should generally **inspect before visualizing or analyzing**.

---

# 12. Suggested solving approach

Use:

**Pandas + one simple visualization**

Pandas can handle:

```text
inspection
shape
columns
data types
missing values
summary statistics
```

Then use either:

```text
Seaborn
```

or

```text
Matplotlib
```

for the visualization.

Because you learned Seaborn yesterday, a simple Seaborn scatter plot would connect naturally with Day 79.

A sensible workflow is:

```text
DataFrame
   ↓
Inspect
   ↓
Check missing values
   ↓
Summarize numerical columns
   ↓
Visualize one relationship
   ↓
Write observations
```

---

# 13. Easy edge cases

### Missing values

Imagine the dataset contains:

```text
Advertising
100
150
missing
250
300
```

The summary may be based only on the available values.

Therefore, checking missing data **before interpreting summaries** is important.

You should ask:

> Is this missing value expected, or does it need cleaning?

You do not need complicated missing-value strategies for this exercise.

### Constant column

Suppose every product had:

```text
Advertising = 100
```

Then a scatter plot might show all points aligned vertically.

That tells you something useful:

> Advertising does not vary in this dataset.

A constant column provides little information for comparing relationships.

---

# 14. Expected observations

With the example dataset, you might notice things such as:

```text
The dataset is very small and contains only a few products.
```

You might also notice:

```text
Advertising and sales are both numerical columns.
```

The summary statistics may show:

```text
Advertising ranges from roughly 100 to 300.
```

And the visualization might suggest:

```text
Higher advertising spending appears to be associated with higher sales.
```

Be careful with wording.

EDA can reveal a **pattern**, but this simple chart does not prove:

```text
Advertising causes higher sales.
```

There could be other factors involved.

For now, your goal is only to **observe the data**.

---

# 15. Hint only

Try solving the exercise using Pandas properties and methods you have already learned.

For inspection, think about:

```python
df.head()

df.shape

df.columns

df.dtypes
```

For missing values, remember the Pandas method beginning with:

```python
is...
```

For numerical summaries, think about:

```python
df.describe()
```

Finally, ask yourself:

> Which plot from Day 79 would let me compare `Advertising` and `Sales` as two numerical variables?

Use one column on the **x-axis** and the other on the **y-axis**.

Do not worry about fancy colors, themes, statistical tests, or advanced plots yet. The important skill for Day 80 is learning to move from **raw DataFrame → inspection → summary → visualization → observation**.