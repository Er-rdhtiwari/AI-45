# Day 84: Weekly Revision — Visualization, EDA and Data Preparation

## 1. Day Number

**Day 84**

## 2. Topic Name

**Revision of Days 78–83: Visualization, EDA, ML Data Preparation, and SQL Basics**

Today you will revise how to move from:

```text
raw data
   ↓
inspect data
   ↓
summarize data
   ↓
visualize data
   ↓
prepare features and target
   ↓
understand database storage
   ↓
query database rows
```

The goal is to connect the topics, not build a large project.

---

## 3. Connection

Over the last few days, you moved through several important data skills.

You learned how to:

```text
visualize data
explore data
prepare data for ML
understand database tables
retrieve data using SQL
```

Today you will combine those ideas in one **small revision exercise**.

---

# 4. Revision Summary of Days 78–83

## Day 78 — Matplotlib Fundamentals

You learned how to create basic charts using Matplotlib.

Important ideas included:

```text
line chart
bar chart
title
x-axis label
y-axis label
```

Example idea:

```python
plt.bar(products, sales)
```

The main purpose was to turn numbers into a visual form that is easier to understand.

---

## Day 79 — Seaborn Fundamentals

You learned that Seaborn works especially well with Pandas DataFrames.

For example, if a DataFrame contains:

```text
advertising_spend
sales
```

a scatter plot can help you visually inspect whether higher advertising spending seems related to higher sales.

You learned the general idea of:

```text
DataFrame
   ↓
Seaborn
   ↓
visual relationship
```

---

## Day 80 — Exploratory Data Analysis

EDA means:

**Exploratory Data Analysis**

Before building a model, you usually want to understand your data.

You practiced checking things such as:

```text
shape
columns
data types
missing values
summary statistics
distributions
relationships
```

EDA asks questions such as:

> How many rows do I have?

> Are values missing?

> What is the average price?

> Are some values unusually high or low?

---

## Day 81 — Basic Train/Test Data Preparation

You learned how machine-learning datasets are commonly divided into:

```text
X → features
y → target
```

For example:

```text
house size → feature
house price → target
```

You also learned the basic train/test idea:

```text
training data
→ used for learning

test data
→ kept aside for later evaluation
```

You should not normally train and evaluate a model using exactly the same examples.

---

## Day 82 — Database Fundamentals

You learned that applications often store structured information in database tables.

Example:

```text
products
--------------------------------
product_id | name | price
--------------------------------
1          | Mouse | 600
2          | Keyboard | 1200
```

Important concepts included:

```text
database
table
row
column
primary key
relational database
```

---

## Day 83 — SQL Fundamentals

You learned how to retrieve database data using SQL.

Important commands were:

```sql
SELECT
FROM
WHERE
ORDER BY
```

For example:

```sql
SELECT name, price
FROM products;
```

You also learned that `WHERE` filters rows.

---

# 5. Important Topics

For this revision, focus on these ideas:

| Topic | Main purpose |
|---|---|
| Matplotlib | Create basic charts |
| Seaborn | Create simple DataFrame-based plots |
| EDA | Understand a dataset |
| Feature | Input information for ML |
| Label/target | Value we want to predict |
| Train/test | Separate learning data from evaluation data |
| Database table | Store structured records |
| `SELECT` | Choose data to display |
| `WHERE` | Filter database rows |

A useful connection is:

```text
Dataset
   ↓
EDA
   ↓
Visualization
   ↓
Feature / target choice
   ↓
ML preparation
```

while database work gives another perspective:

```text
Database
   ↓
Table
   ↓
SQL query
   ↓
Selected data
```

---

# 6. Foundational Notes

Data analysis is rarely just one command.

Usually you perform several small steps.

For example:

```text
1. Get the data
2. Inspect it
3. Check for problems
4. Calculate simple summaries
5. Visualize something useful
6. Decide which columns could be features or targets
```

If the data is stored in a database, another step might happen first:

```text
SQL query
   ↓
retrieve rows
   ↓
load into Python
   ↓
analyze
```

You do not need to combine all of this into one complicated program yet.

The important goal is understanding how the pieces fit together.

---

# 7. Easy Example

Suppose you have this small product dataset:

| product | price | stock | sales |
|---|---:|---:|---:|
| Mouse | 600 | 20 | 15 |
| Keyboard | 1200 | 10 | 8 |
| Monitor | 9000 | 5 | 4 |
| Webcam | 1800 | 12 | 10 |
| Cable | 300 | 30 | 24 |

You could explore it by asking:

```text
How many products are there?

What is the average price?

Which product has the highest sales?

Are any values missing?

What does a bar chart of product vs sales look like?
```

For machine learning, suppose your future goal were:

> Predict product sales.

Then possible inputs could be:

```text
price
stock
```

and the target could be:

```text
sales
```

So conceptually:

```text
X → price, stock
y → sales
```

You are only identifying them today, not training a model.

---

# 8. Revision Problem Statement

Use a very small product dataset containing columns such as:

```text
product
price
stock
sales
```

Your task is to:

1. Create or inspect the product dataset.
2. Check its rows and columns.
3. Check whether any values are missing.
4. Calculate one simple summary, such as average price or total sales.
5. Create **one simple chart**.
6. Decide which columns could be features if your future goal were to predict `sales`.
7. Identify `sales` as the target.
8. Write one SQL `SELECT` query for a similar `products` table.
9. Optionally include a simple `WHERE` condition.
10. Do not train a machine-learning model.

Keep the exercise small.

---

# 9. Concepts Used

This revision combines:

```text
Pandas DataFrame
shape
columns
missing values
mean or sum
Matplotlib or Seaborn
bar chart or scatter plot
features
target
X
y
training/test concept
database table
SQL
SELECT
WHERE
```

You are practicing the relationship between these concepts rather than learning something advanced.

---

# 10. Thought Process

Work through the problem in a simple order.

## Step 1: Understand the dataset

Ask:

```text
What does one row represent?
```

Here:

```text
one row = one product
```

Then check:

```text
columns
number of rows
missing values
```

---

## Step 2: Calculate one useful summary

You might choose:

```text
average price
```

or:

```text
total sales
```

Do not calculate everything just because you can.

Pick one useful summary.

---

## Step 3: Choose one useful visualization

For example, if you want to compare sales between products:

```text
product
   ↓
sales
```

A bar chart makes sense.

If you wanted to compare two numerical columns such as:

```text
price
sales
```

a scatter plot could be useful.

---

## Step 4: Think about ML preparation

Ask:

> What would I want to predict?

Suppose the answer is:

```text
sales
```

Then:

```text
y → sales
```

Next ask:

> Which existing columns might help predict it?

Possible features:

```text
price
stock
```

So:

```text
X → price, stock
```

Do not train anything yet.

---

## Step 5: Think about the database version

Imagine the same product information were stored in:

```text
products
```

You could ask the database:

```text
Show me product names and prices.
```

That becomes a SQL `SELECT` task.

If you only wanted expensive products, you would also need:

```text
WHERE
```

---

# 11. Beginner-Friendly Pseudocode

```text
START

create or load a small product dataset

display the first rows

check:
    number of rows and columns
    column names
    missing values

calculate one simple summary

choose two useful columns for a chart

create one simple chart

decide:
    which columns are possible features?
    which column is the target?

store the idea:
    X = feature columns
    y = target column

think about training data and test data
but do not train a model

write one SQL query:
    choose columns
    choose products table
    optionally add a WHERE condition

END
```

---

# 12. Suggested Solving Approach

Use a **simple data-analysis approach**.

A good order is:

```text
Inspect
   ↓
Clean if needed
   ↓
Summarize
   ↓
Visualize
   ↓
Identify X and y
   ↓
Think about train/test
   ↓
Write one SQL query
```

For Python, Pandas can handle the inspection and summary.

Use either:

```text
Matplotlib
```

or:

```text
Seaborn
```

for the single chart.

For the database part, simply write the SQL query separately.

There is no need to connect Python to an actual database in this revision.

---

# 13. Easy Edge Cases

## Missing value

Suppose the dataset contains:

| product | price | stock | sales |
|---|---:|---:|---:|
| Mouse | 600 | 20 | 15 |
| Keyboard | 1200 | 10 | missing |

Before using `sales` as a target, you should notice that the value is missing.

Do not blindly ignore missing data.

This connects back to your Pandas cleaning lessons.

---

## Empty SQL result

Suppose your table contains prices up to `9000`, but your query asks for:

```text
price > 50000
```

The result could contain:

```text
0 rows
```

That does not automatically mean the query is incorrect.

It may simply mean no product satisfies the condition.

---

# 14. Common Mistakes to Avoid

- Creating a chart before understanding what the columns mean.
- Treating the target column as an input feature accidentally.
- Using every available column without asking whether it makes sense as a feature.
- Forgetting to check for missing values.
- Assuming a SQL query failed simply because it returned no rows.
- Confusing `SELECT` with `WHERE`: `SELECT` chooses columns, while `WHERE` filters rows.
- Using a line chart for unrelated categories when a simple bar chart would communicate the comparison more clearly.
- Training a model before properly separating features and target.

---

# 15. Quick Self-Check Questions

1. What is the main purpose of EDA?

2. If you want to predict `sales`, which variable would normally become `y`?

3. What is the difference between training data and test data?

4. What does `WHERE` do in a SQL query?

5. When would a bar chart be more useful than a scatter plot?

Try answering these without looking back at the notes.

---

# 16. Hint Only

For your revision exercise, begin with a DataFrame shaped roughly like:

```text
product | price | stock | sales
```

For the EDA section, think about methods that can help you inspect:

```text
shape
columns
missing values
```

For the summary, choose only one simple calculation such as:

```text
average price
```

For the chart, ask:

```text
Do I want to compare categories?
```

If yes, a simple bar chart may be appropriate.

For the ML-preparation section, think:

```text
What do I want to predict?
→ sales

What information might help?
→ price and/or stock
```

Therefore, conceptually:

```text
X → possible input columns
y → sales
```

For the SQL section, start from this structure:

```sql
SELECT ...
FROM products
WHERE ...;
```

Fill in the missing parts yourself.

The main revision flow to remember is:

```text
Inspect → Summarize → Visualize → Prepare → Query
```

That connects **Days 78–83** without turning the revision into a large project.