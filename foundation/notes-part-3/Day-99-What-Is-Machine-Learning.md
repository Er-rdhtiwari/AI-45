# Day 99: Machine Learning Fundamentals

## 1. Day Number
**Day 99**

## 2. Topic Name
**Machine Learning, Features, Labels, and Workflow**

## 3. Connection

You now understand basic **data handling** and some of the mathematics used in machine learning, such as statistics, probability, derivatives, and gradients.

Today, you will connect those ideas and learn what **machine learning actually does**.

The basic idea is:

**Data → Learn patterns → Make predictions**

---

## 4. Important Topics

Today you should understand these terms:

- **Machine learning (ML):** teaching a computer to learn patterns from data instead of giving it every rule manually.
- **Dataset:** a collection of data used for analysis or machine learning.
- **Example / observation:** one individual row or case in a dataset.
- **Feature:** information used as input to a model.
- **Label / target:** the value we want the model to predict.
- **Model:** a mathematical system that learns relationships from data.
- **Prediction:** the model's estimated output for new input data.

---

## 5. Foundational Notes

Imagine this dataset:

| Size (sq ft) | Bedrooms | Age | Price |
|---:|---:|---:|---:|
| 1000 | 2 | 10 | 50 |
| 1500 | 3 | 5 | 75 |
| 2000 | 4 | 2 | 100 |

Each **row** represents one house.

Therefore, each row is one **observation** or **example**.

Suppose we want to predict house prices.

Then:

**Features:**

`Size`, `Bedrooms`, `Age`

These contain information that may help predict the price.

**Label / Target:**

`Price`

This is what we want the model to learn to predict.

Conceptually:

```text
Features
   ↓
Machine Learning Model
   ↓
Prediction
```

For example:

```text
Size = 1800
Bedrooms = 3
Age = 4
        ↓
      Model
        ↓
Predicted Price
```

You do **not** need to know how the model calculates that prediction yet.

---

## 6. Traditional Rules vs Machine Learning

Traditional programming usually looks like:

```text
Data + Rules → Answer
```

You tell the computer exactly what rules to follow.

For example:

```text
if temperature > 30:
    print("Hot")
else:
    print("Not hot")
```

You created the rule:

```text
temperature > 30
```

Machine learning is different.

Instead of manually creating every rule, we provide examples:

```text
Data + Correct Answers → Learning Algorithm
                         ↓
                       Model
```

The model tries to discover useful patterns.

For example, instead of writing:

```text
If house size is X
and bedrooms are Y
and age is Z,
then price should be ...
```

we could provide many previous houses with their actual prices.

The machine-learning system tries to learn the relationship between:

```text
Size
Bedrooms
Age
```

and:

```text
Price
```

A useful simplification is:

**Traditional programming:** humans write the rules.

**Machine learning:** the computer learns useful patterns from examples.

---

## 7. Supervised vs Unsupervised Learning

There are many types of machine learning. For now, focus on two broad categories.

### Supervised Learning

In supervised learning, the dataset contains the **correct target or label**.

Example:

| Size | Bedrooms | Price |
|---:|---:|---:|
| 1000 | 2 | 50 |
| 1500 | 3 | 75 |
| 2000 | 4 | 100 |

If we want to predict `Price`, we already have known prices in our training examples.

The model can learn:

```text
Features → Label
```

Common supervised-learning tasks include predicting things such as:

```text
House information → Price
Customer information → Will purchase or not
Email information → Spam or not spam
```

### Unsupervised Learning

In unsupervised learning, there is usually **no target label telling the model the correct answer**.

Instead, we ask the system to discover patterns or groups in the data.

For example:

```text
Customer age
Customer spending
Number of purchases
```

We might ask:

> Are there groups of customers with similar behavior?

The system could discover groups such as:

```text
Group A → low spending
Group B → medium spending
Group C → high spending
```

At this stage, remember:

```text
Supervised
→ Features + known label

Unsupervised
→ Features, but usually no known label
```

---

# 8. Easy Example: Predicting House Price

Suppose we have:

| House | Size | Bedrooms | Age | Price |
|---|---:|---:|---:|---:|
| A | 900 | 2 | 15 | 45 |
| B | 1400 | 3 | 8 | 70 |
| C | 1800 | 3 | 4 | 90 |

Our goal is:

> Predict the price of a house.

One observation might be:

```text
House B
```

Its features are:

```text
Size = 1400
Bedrooms = 3
Age = 8
```

The value we want to predict is:

```text
Price
```

So conceptually:

```text
[1400, 3, 8] → Model → Price prediction
```

A dataset containing many such examples could eventually be used to train a model.

Today, however, we are **only identifying the parts of the ML problem**. We are not training anything yet.

---

# 9. Problem Statement

Consider this small house dataset:

| House | Size | Bedrooms | Age | Price |
|---|---:|---:|---:|---:|
| A | 1200 | 2 | 10 | 60 |
| B | 1600 | 3 | 6 | 80 |
| C | 2100 | 4 | 2 | 110 |

Your goal is to identify:

1. What represents an **observation/example**?
2. Which columns could be **features**?
3. Which column should be the **label/target** if the goal is to predict house price?
4. How many observations are present?
5. What information would you give to a future model to predict the price of a new house?

Do not train a model.

---

# 10. Concepts Used

This exercise uses:

- datasets
- rows and columns
- observations
- features
- labels
- predictions
- supervised learning
- basic data preparation ideas

Notice how this connects directly to your earlier Pandas lessons.

A DataFrame might eventually contain:

```text
rows → observations
columns → variables
selected input columns → features
prediction column → target
```

---

# 11. Thought Process

When looking at a machine-learning problem, first ask:

**What is one example?**

Usually one row represents one example.

Then ask:

**What information do I already know about each example?**

Those values may become features.

Next ask:

**What am I trying to predict?**

That usually becomes the target.

For the house example, think:

```text
What information describes the house?
          ↓
Possible features

What value do I want the model to estimate?
          ↓
Target
```

This simple way of thinking will help with many future ML problems.

---

# 12. Beginner-Friendly ML Workflow

A simplified machine-learning workflow looks like this:

```text
1. Define the problem
        ↓
2. Collect data
        ↓
3. Inspect the data
        ↓
4. Clean the data
        ↓
5. Choose features and target
        ↓
6. Split data for training/testing
        ↓
7. Train a model
        ↓
8. Evaluate the model
        ↓
9. Make predictions
```

Several of these steps should already look familiar.

You previously learned about:

```text
CSV / JSON / databases
        ↓
Pandas
        ↓
Data inspection
        ↓
Cleaning
        ↓
Encoding / scaling
        ↓
Features and labels
```

You are now reaching the point where these data-processing skills connect to actual machine-learning models.

For **Day 99**, focus mainly on steps 1–5.

We will not train a model yet.

---

# 13. Easy Edge Cases

### Missing Feature

Suppose a new house contains:

```text
Size = 1500
Bedrooms = ?
Age = 5
```

A feature is missing.

This can create problems because the model may expect all required input values.

Possible future solutions include:

```text
fill the missing value
remove incomplete data
use a model that can handle missing values
```

For now, simply remember:

**Check whether required features are missing.**

### Unavailable Label

Suppose we have:

| Size | Bedrooms | Age | Price |
|---:|---:|---:|---|
| 1500 | 3 | 5 | ? |

If we are trying to learn how to predict price, the missing price means this example does not provide a known target value.

However, this could also represent a **new house** for which we actually want the trained model to make a prediction.

The meaning depends on the stage of the ML workflow.

---

# 14. Expected Identification

When solving today's exercise, your identification should have this general form:

```text
Observation:
One ______ in the dataset

Features:
Columns that describe ______

Label:
The value that we want to ______

Number of observations:
Count the number of ______
```

You should also be able to describe a future prediction conceptually:

```text
New house features
        ↓
Model
        ↓
Predicted house price
```

The important skill today is not calculation. It is correctly identifying the **role each part of the data plays**.

---

# 15. Hint Only

Look at the question:

> **What are we trying to predict?**

That column is likely your **target**.

Then look at the other useful information describing each house:

```text
Size
Bedrooms
Age
```

Ask yourself whether those values could help predict the target.

Finally, remember:

> **One row usually represents one observation/example.**

Do not build or train a model yet. The goal of Day 99 is simply to understand how a normal dataset becomes a **machine-learning problem**.