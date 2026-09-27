# Day 83: SQL Fundamentals — `SELECT` and `WHERE`

## 1. Day Number

**Day 83**

## 2. Topic Name

**Querying Database Data with SQL**

Today you will learn how to **retrieve information from a database table** using simple SQL queries.

The main commands are:

```sql
SELECT
FROM
WHERE
ORDER BY
```

---

## 3. Connection

Yesterday, you learned that a database can contain tables made of:

```text
rows
columns
primary keys
```

For example:

```text
products
--------------------------------
product_id | name     | price
--------------------------------
1          | Keyboard | 1200
2          | Mouse    | 600
3          | Monitor  | 9000
```

Today you will learn how to ask the database questions such as:

```text
Show me all products.

Show me products costing more than 1000.

Show me products from cheapest to most expensive.
```

SQL lets us express these questions as queries.

---

# 4. Important Topics

### `SELECT`

`SELECT` tells the database **which columns you want to see**.

Example:

```sql
SELECT name
```

means:

```text
Show me the name column.
```

You will also often see:

```sql
SELECT *
```

The `*` means:

```text
all columns
```

---

### `FROM`

`FROM` tells SQL **which table to read**.

Example:

```sql
FROM products
```

means:

```text
Get the data from the products table.
```

---

### `WHERE`

`WHERE` filters the rows.

For example:

```sql
WHERE price > 1000
```

means:

```text
Only keep products whose price is greater than 1000.
```

---

### Comparison operators

Some common SQL comparison operators are:

| Operator | Meaning |
|---|---|
| `=` | equal to |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |
| `<>` or `!=` | not equal to |

For example:

```text
price > 1000
```

and:

```text
price >= 1000
```

are slightly different.

The second one also includes products priced **exactly 1000**.

---

### `ORDER BY`

`ORDER BY` sorts the result.

Example idea:

```sql
ORDER BY price
```

usually sorts from lower values to higher values.

You may also encounter:

```sql
ORDER BY price DESC
```

where `DESC` means descending:

```text
highest → lowest
```

---

# 5. Foundational Notes

SQL stands for:

**Structured Query Language**

It is commonly used to communicate with relational databases.

You can think of SQL as a language for asking questions about tables.

Suppose you have:

| product_id | name | price |
|---:|---|---:|
| 1 | Keyboard | 1200 |
| 2 | Mouse | 600 |
| 3 | Monitor | 9000 |
| 4 | Webcam | 1800 |

A SQL query might ask:

```text
From the products table,
show me products where
price is greater than 1000.
```

The database examines the rows and returns only the ones that satisfy the condition.

---

# 6. A SQL Query in Plain English

Consider this query structure:

```sql
SELECT ...
FROM ...
WHERE ...
ORDER BY ...;
```

Read it in plain English as:

```text
SELECT
→ What information do I want?

FROM
→ Which table should I look inside?

WHERE
→ Which rows should I keep?

ORDER BY
→ How should I sort the result?
```

For example:

```sql
SELECT name, price
FROM products
WHERE price > 1000;
```

means:

```text
Show the name and price
from the products table
for products costing more than 1000.
```

The semicolon:

```sql
;
```

marks the end of the SQL statement.

---

# 7. Easy Example

Suppose our table is:

### `products`

| product_id | name | price |
|---:|---|---:|
| 1 | Keyboard | 1200 |
| 2 | Mouse | 600 |
| 3 | Monitor | 9000 |
| 4 | Webcam | 1800 |
| 5 | Cable | 300 |

Suppose you only wanted to see product names.

You could think:

```text
What column?
→ name

What table?
→ products
```

A simple SQL query would follow this pattern:

```sql
SELECT name
FROM products;
```

Expected result:

| name |
|---|
| Keyboard |
| Mouse |
| Monitor |
| Webcam |
| Cable |

This is a basic `SELECT` query without filtering.

---

# 8. Problem Statement

Use this simple `products` table:

| product_id | name | price |
|---:|---|---:|
| 1 | Keyboard | 1200 |
| 2 | Mouse | 600 |
| 3 | Monitor | 9000 |
| 4 | Webcam | 1800 |
| 5 | Cable | 300 |
| 6 | Headphones | 1200 |

Write SQL queries that conceptually perform these tasks:

1. Show **all products**.
2. Show only products whose price is **greater than 1000**.
3. Show all products ordered by **price from lowest to highest**.

Try to write each query yourself before looking at the hint.

---

# 9. Concepts Used

This exercise uses:

```text
database table
rows
columns
SQL query
SELECT
FROM
WHERE
comparison operators
ORDER BY
ascending order
filtering
```

The basic mental model is:

```text
Table
  ↓
SELECT columns
  ↓
WHERE condition
  ↓
ORDER BY column
  ↓
Result
```

---

# 10. Thought Process

Suppose the question says:

> Show products costing more than 1000.

Think through it in this order.

### Step 1: Which table contains the data?

```text
products
```

### Step 2: Which columns do I want?

Perhaps all product information:

```text
product_id
name
price
```

Or simply:

```text
all columns
```

### Step 3: Is there a condition?

Yes:

```text
price greater than 1000
```

In SQL-style thinking:

```text
price > 1000
```

Then combine those ideas into the correct SQL structure.

---

# 11. Beginner-Friendly Pseudocode Before SQL

### Task 1: Show every product

```text
START

look inside the products table

select every column

return every row

END
```

SQL pattern:

```text
SELECT ...
FROM ...;
```

---

### Task 2: Find expensive products

```text
START

look inside the products table

select the required columns

check each product price

if price is greater than 1000
    include that row

return matching rows

END
```

SQL pattern:

```text
SELECT ...
FROM ...
WHERE ...;
```

---

### Task 3: Sort products by price

```text
START

look inside the products table

select the required columns

sort using the price column
from smallest price to largest price

return the sorted rows

END
```

SQL pattern:

```text
SELECT ...
FROM ...
ORDER BY ...;
```

---

# 12. Suggested Solving Approach: SQL

For each question, identify four things:

```text
1. Which table?
2. Which columns?
3. Do I need a condition?
4. Do I need sorting?
```

For this exercise:

```text
Table
→ products
```

Then decide whether you need:

```text
SELECT
```

only, or:

```text
SELECT + WHERE
```

or:

```text
SELECT + ORDER BY
```

You do not need subqueries, joins, or advanced SQL for today's exercise.

---

# 13. Easy Edge Cases

## No Matching Rows

Suppose you ask for:

```text
price > 50000
```

but your most expensive product costs only `9000`.

The database may return:

```text
0 rows
```

That does **not** necessarily mean the query failed.

It simply means:

```text
No row satisfied the condition.
```

---

## Equal Values

Our table contains:

```text
Keyboard   → 1200
Headphones → 1200
```

If you filter using:

```text
price = 1200
```

both rows should match.

If you sort by price, equal-price products may appear beside each other.

This is completely normal.

Also remember:

```text
price > 1200
```

does **not** include `1200`.

But:

```text
price >= 1200
```

does.

---

# 14. Expected Result Table

For the condition:

```text
price > 1000
```

you should expect rows conceptually similar to:

| product_id | name | price |
|---:|---|---:|
| 1 | Keyboard | 1200 |
| 3 | Monitor | 9000 |
| 4 | Webcam | 1800 |
| 6 | Headphones | 1200 |

Notice that:

```text
Mouse → 600
Cable → 300
```

are not included because they do not satisfy:

```text
price > 1000
```

For the sorting task, the result should begin with the cheapest product and end with the most expensive one.

---

# 15. Hint Only

For **show all products**, remember that:

```sql
*
```

means:

```text
all columns
```

For **products above 1000**, your query needs this structure:

```sql
SELECT ...
FROM products
WHERE price ... 1000;
```

Think carefully about which comparison operator belongs in the blank.

For **sorting by price**, think:

```sql
SELECT ...
FROM products
ORDER BY ...;
```

Your goal for Day 83 is to understand this flow:

```text
SELECT → what should I display?

FROM → where is the data?

WHERE → which rows should remain?

ORDER BY → how should the result be sorted?
```

Try writing the **three complete queries yourself** before moving on to more SQL commands.