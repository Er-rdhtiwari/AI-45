# Day 100: Training, Validation and Test Data

## 1. Day Number

**Day 100**

## 2. Topic Name

**Training, Validation, and Test Datasets**

## 3. Connection

Yesterday you learned about:

- features
- labels
- models
- predictions

Today you will learn what happens **before and during model training**.

Instead of giving all available data to the model in one group, we usually separate it into different parts.

The basic idea is:

```text
Full Dataset
     ↓
Training Data
Validation Data
Test Data
```

Each part has a different job.

---

# 4. Important Topics

### Training Set

The **training set** is the data the model learns from.

Conceptually:

```text
Training examples
      ↓
Model learns patterns
```

If you were predicting house prices, the model might learn from many houses containing:

```text
Size
Bedrooms
Age
Actual Price
```

The training set is normally the largest portion of the available data.

---

### Validation Set

The **validation set** helps us make decisions while developing the model.

For example, imagine trying two versions of a model.

```text
Model A
Model B
```

We could evaluate both using validation data and see how they behave on data they did not directly train on.

The validation set helps answer questions such as:

```text
Which model setup should I use?

Are my model-development choices improving performance?
```

---

### Test Set

The **test set** is kept separate until the model-development process is mostly finished.

Its purpose is to provide a final check of how the model performs on data it has not used during training or model selection.

Conceptually:

```text
Train model
     ↓
Use validation data while developing it
     ↓
Finish model choices
     ↓
Evaluate once on test data
```

---

### Unseen Data

**Unseen data** means data the model did not directly learn from.

For example, suppose this house was not part of the training data:

```text
Size = 1750
Bedrooms = 3
Age = 4
```

It is unseen from the model's training perspective.

Testing performance on unseen data is important because real-world predictions usually involve new examples.

---

### Generalization

**Generalization** means:

> How well does the model work on new data instead of only remembering its training examples?

A useful model should learn patterns that also work on houses, customers, images, or other examples it has not seen before.

---

# 5. Foundational Notes

Imagine you have **100 records**.

It may seem natural to train the model using all 100 records.

But then there is a problem.

If you test the model on the same records it already learned from, good performance does not necessarily mean it will perform well on new data.

It might simply have learned the training examples very closely.

Therefore, we separate the data.

A simple conceptual structure is:

```text
100 records

        ↓ split

Training set
Validation set
Test set
```

For example, one possible split could be:

```text
70% training
15% validation
15% testing
```

This is only an example, not a universal rule.

The appropriate split can depend on how much data is available and what problem you are solving.

---

# 6. Simple Analogy

Imagine you are preparing for an exam.

### Training Set = Study Material

You use textbooks, notes, and practice examples to **learn**.

```text
Study material → learning
```

This is similar to the training set.

---

### Validation Set = Practice Exam

Before the real exam, you take a practice test.

The practice test helps you discover:

```text
What am I doing well?

What should I change?

Which study strategy works better?
```

This is similar to validation data.

You use it to improve your approach.

---

### Test Set = Final Exam

Finally, you take the real exam.

You should not already know all the exact exam questions.

Otherwise, the exam would not tell you whether you truly learned the subject.

This is similar to the test set.

So the analogy is:

```text
Training set   → study material
Validation set → practice exam
Test set       → final exam
```

---

# 7. Easy Example

Suppose we have house data:

| House | Size | Bedrooms | Price |
|---|---:|---:|---:|
| 1 | 1000 | 2 | 50 |
| 2 | 1200 | 2 | 60 |
| 3 | 1400 | 3 | 70 |
| ... | ... | ... | ... |
| 100 | 2200 | 4 | 120 |

Our goal is to predict:

```text
Price
```

Possible features could be:

```text
Size
Bedrooms
```

Instead of using all 100 houses for training, we could separate them.

For example:

```text
Training:
Houses used to learn the relationship between
size, bedrooms, and price.

Validation:
Different houses used while deciding how
the model should be configured.

Test:
Houses kept aside for final evaluation.
```

The important point is not the exact percentages.

The important point is that **each dataset has a different purpose**.

---

# 8. Problem Statement

Suppose you have:

**100 imaginary customer records**

Each record contains:

```text
Age
Annual Spending
Number of Purchases
Will Renew Subscription
```

Your task is to explain conceptually how the 100 records could be separated into:

- training records
- validation records
- test records

Consider:

```text
Which group should contain the most records?

Which group should the model directly learn from?

Which group can help you make development decisions?

Which group should remain untouched until final evaluation?
```

Do not train a model yet.

---

# 9. Concepts Used

This exercise uses:

- dataset
- observation
- features
- label
- model
- training
- validation
- testing
- unseen data
- generalization

It connects directly to Day 99.

Yesterday:

```text
Features → Model → Prediction
```

Today:

```text
Dataset
   ↓
Split the data
   ↓
Train / Validate / Test
```

Later, you will combine both ideas.

---

# 10. Thought Process

When you receive a dataset, first think:

### Step 1: What is the prediction problem?

For example:

```text
Customer features → Predict subscription renewal
```

### Step 2: Which records should teach the model?

These become the:

```text
Training set
```

### Step 3: Which records should help evaluate choices during development?

These become the:

```text
Validation set
```

### Step 4: Which records should be saved for the final evaluation?

These become the:

```text
Test set
```

The overall idea is:

```text
All Data
   ↓
Split
   ↓
┌────────────┬────────────┬────────────┐
│ Training   │ Validation │ Test       │
│            │            │            │
│ Learn      │ Tune/check │ Final check│
└────────────┴────────────┴────────────┘
```

---

# 11. Beginner-Friendly Pseudocode

Conceptually:

```text
START

collect dataset

separate features and label

split dataset into:
    training data
    validation data
    test data

use training data to teach the model

use validation data to compare development choices

after development is finished:
    use test data for final evaluation

END
```

In future Python lessons, this process may eventually look conceptually like:

```text
X = features
y = label

split X and y into different groups
```

But you do not need to implement that yet.

---

# 12. Why Test Data Should Not Guide Training Decisions

This is one of the most important ideas in machine learning.

Imagine you repeatedly check the final exam questions while studying.

You notice:

```text
Question 1 asks about topic A
Question 2 asks about topic C
Question 3 asks about topic D
```

Then you change your studying specifically to perform well on those questions.

Now your final exam is no longer truly testing you on unseen questions.

Something similar happens in machine learning.

Suppose you:

```text
Train Model A
↓
Check test results

Change model
↓
Check test results again

Change model
↓
Check test results again
```

You are now indirectly using the test data to make model-development decisions.

The test data is no longer completely independent.

Instead, model-development decisions should normally be guided by:

```text
Training data
+
Validation data
```

Then the test set remains separate for a final check.

A useful rule is:

```text
Training set
→ Learn

Validation set
→ Make development decisions

Test set
→ Final evaluation
```

---

# 13. Easy Edge Case: Very Small Dataset

Suppose you only have:

```text
10 records
```

Creating three separate groups can become difficult.

For example, if you reserve several records for validation and testing, very few records remain for training.

This can make learning unreliable.

So with very small datasets, splitting requires extra care.

Later you may learn techniques for handling this problem more effectively.

For now, remember:

> The less data you have, the more valuable every observation becomes.

Do not worry about advanced resampling methods yet.

---

# 14. Expected Split Explanation

For the **100-record problem**, your explanation might follow this structure:

```text
Training set:
The largest group.
Used by the model to learn patterns.

Validation set:
A smaller separate group.
Used while comparing model-development choices.

Test set:
Another separate group.
Kept aside until final evaluation.
```

One possible conceptual split is:

```text
100 records
     ↓

70 training
15 validation
15 testing
```

Another project might use different proportions.

So do not memorize **70/15/15** as a strict rule.

Instead, memorize the purposes:

| Dataset | Main Purpose |
|---|---|
| Training | Learn patterns |
| Validation | Guide development choices |
| Test | Final evaluation |
| New real-world data | Make actual predictions |

---

# 15. Hint Only

For the 100-record exercise, start with this question:

> **Which group actually teaches the model?**

That should receive the largest portion.

Then ask:

> **Which group should help me compare choices while building the model?**

Finally ask:

> **Which group should I avoid repeatedly looking at until the end?**

Think:

```text
Learn → Check → Final Check
```

That simple sequence captures the core idea of **training, validation, and test data**.