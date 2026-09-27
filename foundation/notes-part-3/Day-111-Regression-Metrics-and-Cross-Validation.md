# Day 111: Regression Evaluation and Cross-Validation Basics

## 1. Day number

**Day 111**

## 2. Topic name

**MAE, MSE, RMSE, and Cross-Validation**

## 3. Connection

Yesterday, you evaluated **classification models** using:

```text
Accuracy
Precision
Recall
F1 Score
```

Those metrics work when the model predicts categories such as:

```text
Spam / Not Spam
Churn / No Churn
```

Today, we return to **regression**, where the model predicts numerical values such as:

```text
House price → ₹52 lakh
Temperature → 29°C
Sales → ₹85,000
```

Now we need to measure:

> **How far are the predicted numbers from the real numbers?**

We will use:

```text
MAE
MSE
RMSE
```

Then we will learn **cross-validation**, which gives us a more reliable way to evaluate a model using different portions of the available data.

---

# 4. Important topics

### Prediction error

For one example, prediction error is the difference between:

```text
Actual value
and
Predicted value
```

Suppose:

```text
Actual house price    = 50 lakh
Predicted house price = 47 lakh
```

The model missed by:

```text
3 lakh
```

Regression evaluation metrics summarize errors like this across many predictions.

### MAE

**MAE = Mean Absolute Error**

Think:

> On average, how far away are my predictions from the actual values?

### MSE

**MSE = Mean Squared Error**

Think:

> Square each error before averaging, so large mistakes receive much more attention.

### RMSE

**RMSE = Root Mean Squared Error**

Think:

> Start with MSE, then take the square root so the result returns to the original unit.

### Fold

A **fold** is one portion of a dataset used during cross-validation.

For example, with 5-fold cross-validation:

```text
Dataset
↓
Fold 1
Fold 2
Fold 3
Fold 4
Fold 5
```

### Cross-validation

Cross-validation repeatedly changes which fold is used for validation.

This helps us see whether the model performs reasonably across different parts of the dataset.

---

# 5. Foundational notes

Suppose a house-price model makes these predictions:

| House | Actual price | Predicted price |
|---|---:|---:|
| A | 40 | 38 |
| B | 50 | 54 |
| C | 60 | 59 |

The errors in size are:

```text
House A → 2
House B → 4
House C → 1
```

A perfect prediction would have:

```text
Error = 0
```

Generally, for MAE, MSE, and RMSE:

> **Smaller is better.**

And:

```text
0 = perfect predictions
```

However, what counts as a "small" error depends on the meaning and scale of your target.

An RMSE of `5` could be tiny for house prices measured in lakhs but enormous for something measured between `0` and `1`.

---

# 6. MAE, MSE, and RMSE intuitively

## MAE — average size of mistakes

Imagine your prediction errors are:

```text
2
4
1
```

MAE simply asks:

> What is their average size?

It does not care whether the model predicted too high or too low.

That's why we use **absolute** values.

Simple formula:

```text
MAE =
sum of absolute errors
----------------------
number of predictions
```

For our errors:

```text
MAE = (2 + 4 + 1) / 3
```

You can calculate the final value yourself.

### How to interpret it

If:

```text
MAE = 3 lakh
```

you can say:

> The model's predictions are off by about 3 lakh on average.

This direct interpretation is one reason MAE is beginner-friendly.

---

# 7. MSE — punish large mistakes more

MSE first **squares each error**.

Suppose two errors are:

```text
2
10
```

Squaring gives:

```text
2²  = 4
10² = 100
```

Notice how the large error becomes much more influential.

Simple formula:

```text
MSE =
sum of squared errors
---------------------
number of predictions
```

So MSE is useful when you want large prediction mistakes to receive extra emphasis.

One drawback is that its units are squared.

If the target is measured in:

```text
lakh rupees
```

MSE is effectively measured in:

```text
(lakh rupees)²
```

which is less intuitive to explain directly.

---

# 8. RMSE — MSE returned to the original unit

RMSE means:

**Root Mean Squared Error**

You first calculate MSE and then take its square root:

```text
RMSE = √MSE
```

The main benefit is that RMSE returns to the same unit as the target.

If house prices are measured in lakhs:

```text
RMSE → lakhs
```

rather than squared lakhs.

So you can interpret something like:

```text
RMSE = 4 lakh
```

more naturally.

A useful comparison:

| Metric | Main intuition | Large errors |
|---|---|---|
| MAE | Average absolute mistake | Normal influence |
| MSE | Average squared mistake | Strong influence |
| RMSE | Square-root version of MSE | Strong influence |

---

# 9. Easy example

Suppose a model predicts monthly sales.

| Month | Actual | Predicted |
|---|---:|---:|
| 1 | 10 | 12 |
| 2 | 20 | 18 |
| 3 | 30 | 33 |
| 4 | 40 | 39 |

First find the errors:

```text
Actual 10, Predicted 12 → difference = 2
Actual 20, Predicted 18 → difference = 2
Actual 30, Predicted 33 → difference = 3
Actual 40, Predicted 39 → difference = 1
```

For MAE, you would average:

```text
2, 2, 3, 1
```

For MSE, square them first:

```text
2², 2², 3², 1²
```

For RMSE:

```text
calculate MSE
↓
take its square root
```

Do the final arithmetic yourself as today's exercise.

---

# 10. Cross-validation — dataset rotation analogy

Suppose you have five groups of data:

```text
A  B  C  D  E
```

Instead of choosing one validation group forever, cross-validation **rotates** the validation role.

### Round 1

```text
Train:      B C D E
Validation: A
```

### Round 2

```text
Train:      A C D E
Validation: B
```

### Round 3

```text
Train:      A B D E
Validation: C
```

Continue until every group has had a turn as validation data.

This is similar to a group of students taking turns being the examiner:

```text
Round 1 → Student A checks everyone else
Round 2 → Student B checks everyone else
Round 3 → Student C checks everyone else
...
```

No single group permanently decides the evaluation result.

---

# 11. Why use cross-validation?

Imagine you perform only one train/validation split.

By chance, your validation data might be:

```text
very easy
```

or:

```text
unusually difficult
```

Your evaluation could therefore give a misleading impression.

Cross-validation asks:

> Does the model behave reasonably when different parts of the dataset are held out?

For example:

```text
Fold 1 MAE → 3.1
Fold 2 MAE → 2.8
Fold 3 MAE → 3.4
Fold 4 MAE → 2.9
Fold 5 MAE → 3.2
```

You could then summarize the results using their average.

Conceptually:

```text
Train/evaluate several times
         ↓
collect several scores
         ↓
look at average performance
```

This gives a broader picture than relying on one lucky or unlucky split.

---

# 12. Problem statement

Suppose these are actual and predicted house prices, measured in lakhs:

| House | Actual | Predicted |
|---|---:|---:|
| A | 30 | 28 |
| B | 40 | 43 |
| C | 50 | 49 |
| D | 60 | 64 |

### Part A — Regression errors

For each house:

1. Find the prediction error size.
2. Use the absolute errors to calculate MAE.
3. Square the errors and calculate MSE.
4. Take the square root of MSE to obtain RMSE.
5. Explain each result in simple language.

### Part B — Cross-validation

Imagine you have:

```text
12 training examples
```

and use:

```text
3-fold cross-validation
```

Conceptually divide them into:

```text
Fold A → 4 examples
Fold B → 4 examples
Fold C → 4 examples
```

Explain how the three rounds would work:

```text
Round 1 → ? used for validation
Round 2 → ? used for validation
Round 3 → ? used for validation
```

Do not build a complicated model. Focus on understanding the rotation.

---

# 13. Concepts used

This lesson combines:

```text
Actual value
Predicted value
Prediction error
Absolute error
Squared error
MAE
MSE
RMSE
Training data
Validation data
Fold
Cross-validation
```

The important distinction is:

```text
Error metrics
→ measure how wrong predictions are

Cross-validation
→ changes which examples are used to evaluate the model
```

They solve related but different problems.

---

# 14. Thought process

For regression evaluation, start with one row.

Suppose:

```text
Actual    = 30
Predicted = 28
```

Ask:

```text
How far apart are they?
```

Then repeat for every prediction.

Once you have all errors:

```text
MAE
→ make errors positive and average

MSE
→ square errors and average

RMSE
→ square root of MSE
```

For cross-validation, think differently.

Ask:

```text
How can I avoid judging my model
using only one particular validation group?
```

Answer:

```text
Rotate the validation group.
```

So the full conceptual picture becomes:

```text
Train model
     ↓
make predictions
     ↓
calculate errors
     ↓
repeat evaluation with different folds
     ↓
summarize performance
```

---

# 15. Beginner-friendly calculation steps

### MAE

Given:

```text
Actual:    30, 40, 50, 60
Predicted: 28, 43, 49, 64
```

Step 1:

```text
Find each difference
```

Step 2:

```text
Ignore the + or - direction
by taking absolute values
```

Step 3:

```text
Add those absolute errors
```

Step 4:

```text
Divide by 4
```

That gives:

```text
MAE
```

---

### MSE

Start with the same errors.

Then:

```text
square error 1
square error 2
square error 3
square error 4

add them

divide by 4
```

That gives:

```text
MSE
```

---

### RMSE

Take your MSE:

```text
RMSE = square root of MSE
```

---

### Cross-validation pseudocode

```text
split dataset into k folds

FOR each fold:

    use that fold as validation data

    use all other folds as training data

    train the model

    predict validation examples

    calculate an error score

store the score

calculate the average score
```

At this stage, understanding this workflow matters more than writing complete Python code.

---

# 16. Easy edge cases

## Perfect prediction

Suppose:

```text
Actual:    10, 20, 30
Predicted: 10, 20, 30
```

Every error is:

```text
0
```

Therefore:

```text
MAE  = 0
MSE  = 0
RMSE = 0
```

This represents perfect predictions on those examples.

---

## One very large error

Suppose the errors are:

```text
1
2
1
20
```

MAE sees the large error, but MSE squares it:

```text
20² = 400
```

That one mistake can therefore influence MSE and RMSE strongly.

This demonstrates an important difference:

> **MSE and RMSE react more strongly to large errors than MAE.**

---

## Very small dataset

Suppose you have only three examples.

Trying to create many folds would leave very little training data in each round.

Cross-validation can still be conceptually possible, but evaluation from extremely small datasets may be unstable.

More folds are not automatically better in every situation.

---

## Unequal-looking fold performance

Imagine:

```text
Fold 1 MAE = 2
Fold 2 MAE = 3
Fold 3 MAE = 15
```

The model behaves very differently on Fold 3.

Do not look only at the average and ignore this variation.

At beginner level, simply notice:

> Cross-validation can reveal that performance changes depending on which data the model is evaluated on.

---

# 17. Expected interpretation

After solving the regression exercise, your explanation should sound like:

```text
MAE:
Predictions are off by about ___ lakh
on average.

MSE:
The average squared error is ___.
Larger mistakes receive extra weight.

RMSE:
The typical error measured in the
original target unit is about ___ lakh.
```

For cross-validation:

```text
Each fold gets one turn as validation data.

The remaining folds are used for training.

Therefore, the model is evaluated on
multiple different portions of the dataset.
```

You should understand the meaning of the numbers rather than simply calculating them.

---

# 18. Hint only

For the house-price problem, start here:

```text
Actual       Predicted       Absolute error
30           28              ?
40           43              ?
50           49              ?
60           64              ?
```

Then:

```text
MAE
→ average the absolute-error column

MSE
→ square each error, then average

RMSE
→ √MSE
```

For the 3-fold exercise:

```text
Round 1:
Train = Fold ? + Fold ?
Validate = Fold ?

Round 2:
Train = Fold ? + Fold ?
Validate = Fold ?

Round 3:
Train = Fold ? + Fold ?
Validate = Fold ?
```

The key idea from **Day 111** is:

> **MAE, MSE, and RMSE tell us how far numerical predictions are from actual values, while cross-validation evaluates the model repeatedly by rotating which portion of the data is held out for validation.**