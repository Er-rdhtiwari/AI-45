# Day 110: Classification Model Evaluation

## 1. Day number

**Day 110**

## 2. Topic name

**Confusion Matrix, Accuracy, Precision, Recall, and F1 Score**

## 3. Connection

You can now train classification models such as:

```text
Logistic Regression
KNN
Naive Bayes
Decision Tree
Random Forest
```

But training a model is only part of machine learning.

Today the question becomes:

> **How do I know whether the model's predictions are actually useful?**

For classification problems, some of the most common evaluation tools are:

```text
Confusion Matrix
Accuracy
Precision
Recall
F1 Score
```

---

# 4. Important topics

We will use one simple scenario throughout the lesson:

> A model predicts whether an email is **Spam** or **Not Spam**.

Let:

```text
Positive class = Spam
Negative class = Not Spam
```

The word **positive** does not mean “good.” It simply means the class we have chosen as the positive class.

---

## True Positive — TP

The email really **is Spam**, and the model predicts **Spam**.

```text
Actual:    Spam
Predicted: Spam
```

This is:

```text
True Positive
TP
```

The model was correct.

---

## True Negative — TN

The email really is **Not Spam**, and the model predicts **Not Spam**.

```text
Actual:    Not Spam
Predicted: Not Spam
```

This is:

```text
True Negative
TN
```

Again, the model was correct.

---

## False Positive — FP

The email is actually **Not Spam**, but the model predicts **Spam**.

```text
Actual:    Not Spam
Predicted: Spam
```

This is:

```text
False Positive
FP
```

The model raised a false alarm.

A useful real-world interpretation:

```text
A normal email was incorrectly placed in spam.
```

---

## False Negative — FN

The email really **is Spam**, but the model predicts **Not Spam**.

```text
Actual:    Spam
Predicted: Not Spam
```

This is:

```text
False Negative
FN
```

The model missed a positive example.

For our scenario:

```text
A spam email reached the normal inbox.
```

---

# 5. Foundational notes

A classification prediction has two things to compare:

```text
Actual label
Predicted label
```

For every example, ask:

```text
Was the real class Positive or Negative?
Was the predicted class Positive or Negative?
```

That gives four possibilities:

| Actual | Predicted | Result |
|---|---|---|
| Positive | Positive | True Positive |
| Negative | Negative | True Negative |
| Negative | Positive | False Positive |
| Positive | Negative | False Negative |

A useful memory trick:

First decide whether the prediction was:

```text
True  = correct
False = incorrect
```

Then look at what the model predicted:

```text
Positive or Negative
```

So:

```text
False Positive
```

means:

> The model predicted Positive, but that prediction was wrong.

---

# 6. Confusion matrix

A **confusion matrix** organizes the four counts into a table.

One common layout is:

|  | Predicted Positive | Predicted Negative |
|---|---:|---:|
| **Actual Positive** | TP | FN |
| **Actual Negative** | FP | TN |

For spam detection:

|  | Predicted Spam | Predicted Not Spam |
|---|---:|---:|
| **Actual Spam** | TP | FN |
| **Actual Not Spam** | FP | TN |

It lets you quickly see not only how many predictions were correct, but also **what kinds of mistakes** the model made.

---

# 7. Easy confusion-matrix example

Suppose we tested the model on **10 emails**.

Results:

```text
TP = 4
TN = 4
FP = 1
FN = 1
```

Confusion matrix:

|  | Predicted Spam | Predicted Not Spam |
|---|---:|---:|
| **Actual Spam** | 4 | 1 |
| **Actual Not Spam** | 1 | 4 |

Total:

```text
4 + 4 + 1 + 1 = 10 emails
```

Now we can calculate our main metrics.

---

# 8. Accuracy

**Accuracy** asks:

> Out of all predictions, how many were correct?

Correct predictions are:

```text
TP + TN
```

So:

```text
Accuracy = correct predictions / all predictions
```

Using our example:

```text
Correct = 4 + 4 = 8
Total = 10
```

Therefore:

```text
Accuracy = 8 / 10
         = 0.80
         = 80%
```

Interpretation:

> The model classified 80% of all emails correctly.

---

# 9. Precision

**Precision** asks:

> When the model predicted Spam, how often was it actually Spam?

Focus only on predictions of the positive class.

Those are:

```text
TP + FP
```

Simple formula:

```text
Precision = TP / (TP + FP)
```

Using our example:

```text
TP = 4
FP = 1
```

So:

```text
Precision = 4 / (4 + 1)
          = 4 / 5
          = 0.80
          = 80%
```

Interpretation:

> Of all emails predicted as Spam, 80% really were Spam.

Precision is useful when **false alarms matter**.

For example, high precision is useful if you do not want many legitimate emails incorrectly marked as spam.

---

# 10. Recall

**Recall** asks:

> Out of all the actual Spam emails, how many did the model successfully find?

Focus on actual positives.

Those are:

```text
TP + FN
```

Simple formula:

```text
Recall = TP / (TP + FN)
```

Using our example:

```text
TP = 4
FN = 1
```

So:

```text
Recall = 4 / (4 + 1)
       = 4 / 5
       = 0.80
       = 80%
```

Interpretation:

> The model detected 80% of all actual Spam emails.

Recall matters when **missing positive cases is costly**.

---

# 11. F1 score

Sometimes we care about both:

```text
Precision
and
Recall
```

The **F1 score** combines them into one number.

A simple formula is:

```text
F1 = 2 × (Precision × Recall)
          --------------------
          Precision + Recall
```

In our example:

```text
Precision = 0.80
Recall = 0.80
```

So:

```text
F1 = 0.80
```

or:

```text
80%
```

At beginner level, remember:

> **F1 is useful when you want a balance between precision and recall.**

You do not need to memorize the formula immediately. Understanding what it represents is more important.

---

# 12. All four metrics in one scenario

Using:

```text
TP = 4
TN = 4
FP = 1
FN = 1
```

we get:

| Metric | Beginner question | Result |
|---|---|---:|
| Accuracy | How many predictions were correct overall? | 80% |
| Precision | When we predicted Spam, how often were we right? | 80% |
| Recall | How many actual Spam emails did we find? | 80% |
| F1 | How balanced are precision and recall? | 80% |

Notice that all four happen to be equal in this very balanced example.

That will **not** always happen.

---

# 13. Why accuracy alone can be misleading

Consider a very different dataset:

```text
100 emails total

95 = Not Spam
5 = Spam
```

Imagine a bad model that predicts:

```text
Not Spam
```

for **every single email**.

It gets:

```text
95 correct
5 wrong
```

Accuracy:

```text
95 / 100 = 95%
```

That sounds excellent.

But the model found:

```text
0 out of 5 Spam emails
```

Its recall for Spam would be:

```text
0%
```

So although accuracy is **95%**, the model is useless if our main goal is to catch spam.

This happens with **imbalanced datasets**, where one class is much more common than another.

Main lesson:

> **Never judge every classification model using accuracy alone.**

Look at the confusion matrix and other metrics too.

---

# 14. Problem statement

Suppose these are the actual and predicted labels for eight emails:

| Email | Actual | Predicted |
|---|---|---|
| 1 | Spam | Spam |
| 2 | Spam | Spam |
| 3 | Spam | Not Spam |
| 4 | Not Spam | Not Spam |
| 5 | Not Spam | Spam |
| 6 | Not Spam | Not Spam |
| 7 | Spam | Spam |
| 8 | Not Spam | Not Spam |

Treat:

```text
Spam = Positive
Not Spam = Negative
```

Your tasks are:

1. Count the **True Positives**.
2. Count the **True Negatives**.
3. Count the **False Positives**.
4. Count the **False Negatives**.
5. Build the confusion matrix.
6. Calculate accuracy.
7. Calculate precision.
8. Calculate recall.
9. Calculate the F1 score.
10. Explain each result in one simple sentence.

---

# 15. Concepts used

This exercise combines:

```text
Actual label
Predicted label
Positive class
Negative class
TP
TN
FP
FN
Confusion matrix
Accuracy
Precision
Recall
F1 score
```

The most important starting point is choosing which class is considered **positive**.

Here:

```text
Positive = Spam
```

Without knowing that, TP, FP, FN, and TN can become confusing.

---

# 16. Thought process

Do not calculate the metrics immediately.

First compare each row individually.

For example:

```text
Actual Spam
Predicted Spam
```

means:

```text
True Positive
```

Then:

```text
Actual Spam
Predicted Not Spam
```

means:

```text
False Negative
```

Continue until every example has been assigned to one of:

```text
TP
TN
FP
FN
```

Only then calculate the metrics.

This makes mistakes much less likely.

---

# 17. Beginner-friendly calculation steps

Follow this order.

### Step 1 — Choose the positive class

```text
Positive = Spam
Negative = Not Spam
```

### Step 2 — Count TP

Find rows where:

```text
Actual = Spam
Predicted = Spam
```

### Step 3 — Count TN

Find rows where:

```text
Actual = Not Spam
Predicted = Not Spam
```

### Step 4 — Count FP

Find rows where:

```text
Actual = Not Spam
Predicted = Spam
```

### Step 5 — Count FN

Find rows where:

```text
Actual = Spam
Predicted = Not Spam
```

### Step 6 — Build the confusion matrix

```text
             Predicted
             +       -
Actual +     TP      FN
Actual -     FP      TN
```

### Step 7 — Accuracy

```text
Accuracy =
(TP + TN) / Total
```

### Step 8 — Precision

```text
Precision =
TP / (TP + FP)
```

### Step 9 — Recall

```text
Recall =
TP / (TP + FN)
```

### Step 10 — F1

Use your precision and recall:

```text
F1 =
2 × Precision × Recall
----------------------
Precision + Recall
```

---

# 18. Easy edge cases

### No predicted positives

Suppose the model predicts every example as:

```text
Negative
```

Then:

```text
TP + FP = 0
```

The usual precision calculation would involve division by zero.

Libraries such as scikit-learn have rules for handling this situation.

At beginner level, simply recognize:

> Precision cannot be meaningfully calculated in the normal way if the model never predicts the positive class.

### No actual positives

Suppose your test set contains no Spam emails.

Then:

```text
TP + FN = 0
```

Recall becomes problematic because there were no actual positive examples to find.

This is another reason test data should represent the classes you care about.

### Perfect model

If:

```text
FP = 0
FN = 0
```

then every prediction is correct.

You would normally have:

```text
Accuracy = 1
Precision = 1
Recall = 1
F1 = 1
```

which means:

```text
100%
```

### Highly imbalanced data

If one class greatly outnumbers another, accuracy may appear high even when the minority class is handled badly.

Always inspect more than one metric.

---

# 19. Expected interpretation

After calculating your exercise, your explanation should sound something like:

```text
Accuracy:
The model correctly classified ___% of all emails.

Precision:
Of all emails predicted as Spam,
___% were really Spam.

Recall:
Of all actual Spam emails,
the model successfully detected ___%.

F1:
The model's balance between precision
and recall is ___.
```

This interpretation is often more useful than simply writing four decimal values.

For example:

```text
Precision = 0.75
```

is easier to understand as:

> 75% of the examples predicted as positive were actually positive.

---

# 20. Hint only

For the eight-email exercise, first create four counters:

```text
TP = ?
TN = ?
FP = ?
FN = ?
```

Go through the rows one by one.

Remember:

```text
Actual Spam + Predicted Spam
→ TP

Actual Not Spam + Predicted Not Spam
→ TN

Actual Not Spam + Predicted Spam
→ FP

Actual Spam + Predicted Not Spam
→ FN
```

Then use:

```text
Accuracy  → correct overall
Precision → correctness of positive predictions
Recall    → how many real positives were found
F1        → balance of precision and recall
```

The key idea from **Day 110** is:

> **A confusion matrix shows what kinds of predictions a classifier got right and wrong, while accuracy, precision, recall, and F1 summarize different aspects of that performance.**