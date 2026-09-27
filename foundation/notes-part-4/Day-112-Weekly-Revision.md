# Day 112: Weekly Revision — Supervised ML and Evaluation

## 1. Day number

**Day 112**

## 2. Topic name

**Revision of Days 106–111: Supervised Machine Learning and Evaluation**

## 3. Connection

Over the last six days, you learned several beginner **supervised machine-learning models** and the metrics used to evaluate them.

The big picture is:

```text
Labeled data
    ↓
Choose classification or regression
    ↓
Train a suitable model
    ↓
Make predictions
    ↓
Evaluate those predictions
```

Today is about connecting those pieces rather than learning a new algorithm.

---

# 4. Revision summary of Days 106–111

### Day 106 — Logistic Regression

Logistic Regression is commonly used for **classification**, especially binary classification.

Example:

```text
Customer features
      ↓
Logistic Regression
      ↓
Churn / No Churn
```

It can estimate a probability and then convert that into a predicted class.

Remember:

> Despite its name, Logistic Regression is primarily a classification algorithm.

---

### Day 107 — K-Nearest Neighbors

KNN classifies a new example by looking at its nearby training examples.

```text
New point
   ↓
Find k nearest points
   ↓
Look at their classes
   ↓
Majority vote
   ↓
Predicted class
```

Main idea:

> Nearby examples help decide the new example's class.

---

### Day 108 — Naive Bayes

Naive Bayes uses **probability**.

It asks:

> Given the evidence I see, which class appears more likely?

For spam classification:

```text
Words/features
     ↓
Probability evidence
     ↓
Spam vs Not Spam
```

The "naive" part comes from its simplifying conditional-independence assumption about features.

---

### Day 109 — Decision Tree

A Decision Tree predicts by following simple learned decisions.

Think of your early Python `if-else` statements:

```text
Question?
   ↓
Yes / No
   ↓
Another question?
   ↓
Leaf prediction
```

Important tree terms:

```text
Root
Split
Branch
Leaf
```

---

### Day 109 — Random Forest

Random Forest extends the Decision Tree idea.

Instead of using one tree:

```text
Tree → prediction
```

it uses many:

```text
Tree 1 ─┐
Tree 2 ─┤
Tree 3 ─┼→ combine predictions → final result
Tree 4 ─┤
Tree 5 ─┘
```

For classification, the trees can effectively vote.

---

### Day 110 — Classification evaluation

For classification, you learned:

```text
True Positive
True Negative
False Positive
False Negative
```

These form the **confusion matrix**.

From them, you can calculate:

```text
Accuracy
Precision
Recall
F1 score
```

Each metric answers a slightly different question.

---

### Day 111 — Regression evaluation

For numerical predictions, you learned:

```text
MAE
MSE
RMSE
```

All measure prediction error differently.

You also learned **cross-validation**, where different portions of the available training data take turns being used for validation.

---

# 5. Important topics recap

| Topic | Beginner meaning |
|---|---|
| Logistic Regression | Probability-based binary classifier |
| KNN | Classify using nearby examples |
| Naive Bayes | Classify using probability and evidence |
| Decision Tree | Follow learned yes/no decisions |
| Random Forest | Combine many Decision Trees |
| Confusion matrix | Count types of classification results |
| Accuracy | Overall fraction classified correctly |
| Precision | How reliable positive predictions are |
| Recall | How many actual positives were found |
| F1 | Balance of precision and recall |
| MAE | Average absolute regression error |
| MSE | Average squared regression error |
| RMSE | Square-root version of MSE |
| Cross-validation | Evaluate repeatedly using different folds |

---

# 6. Foundational notes

Before choosing an algorithm or metric, ask the most important question:

> **What type of target am I predicting?**

If the target is a category:

```text
Yes / No
Spam / Not Spam
A / B
```

you have a:

```text
Classification problem
```

If the target is a continuous number:

```text
House price
Temperature
Sales amount
```

you have a:

```text
Regression problem
```

This immediately affects both your model and your evaluation metrics.

A simple mental map is:

```text
                 Target
                   |
          +--------+--------+
          |                 |
      Category            Number
          |                 |
   Classification       Regression
          |                 |
 confusion matrix      MAE / MSE / RMSE
 accuracy
 precision
 recall
 F1
```

---

# 7. Easy example

Imagine a real-estate dataset containing:

```text
house_size
bedrooms
location_score
```

We could create two different ML problems from similar features.

### Problem A

Predict:

```text
Will the house sell within 30 days?
```

Possible target:

```text
Yes / No
```

This is:

**Classification**

Possible models:

```text
Logistic Regression
KNN
Naive Bayes
Decision Tree
Random Forest
```

Possible evaluation:

```text
Confusion matrix
Accuracy
Precision
Recall
F1
```

### Problem B

Predict:

```text
What will the house sell for?
```

Possible target:

```text
₹62 lakh
₹78 lakh
₹1.1 crore
```

This is:

**Regression**

A beginner model could be Linear Regression from Day 104.

Possible evaluation:

```text
MAE
MSE
RMSE
```

Cross-validation can also help estimate how consistently the model performs across different subsets of the available training data.

---

# 8. Revision problem statement

You have two small ML problems.

## Problem A — Classification

A company has:

```text
monthly_usage
support_calls
```

and wants to predict:

```text
churn = Yes / No
```

Your job:

1. Identify whether this is classification or regression.
2. Choose one reasonable beginner classification model.
3. Identify useful classification metrics.
4. Explain what a false negative would mean if **Churn = Positive**.

---

## Problem B — Regression

You have:

```text
house_size
bedrooms
```

and want to predict:

```text
house_price
```

Your job:

1. Identify whether this is classification or regression.
2. Choose an appropriate model type.
3. Identify suitable regression metrics.
4. Explain what MAE would mean.
5. Explain conceptually how cross-validation could evaluate the model several times.

Do not build large models. Focus on choosing the correct **problem type, model family, and evaluation method**.

---

# 9. Concepts used

This revision combines three major stages.

### Stage 1 — Define the problem

Identify:

```text
Features → X
Target   → y
```

Then decide:

```text
Classification?
or
Regression?
```

### Stage 2 — Choose a model

For classification, beginner options now include:

```text
Logistic Regression
KNN
Naive Bayes
Decision Tree
Random Forest
```

For simple numerical prediction, you already know:

```text
Linear Regression
```

### Stage 3 — Evaluate

Classification:

```text
Confusion matrix
Accuracy
Precision
Recall
F1
```

Regression:

```text
MAE
MSE
RMSE
```

Cross-validation:

```text
Repeat evaluation across different folds
```

---

# 10. Thought process

When someone gives you an ML problem, don't start by immediately choosing an algorithm.

Use this sequence.

First ask:

```text
What is my target?
```

If it is:

```text
0 / 1
Yes / No
A / B
```

think:

```text
Classification
```

If it is:

```text
52.4
₹750000
28.7°C
```

think:

```text
Regression
```

Then choose a sensible beginner model.

After training, ask:

```text
How should I measure mistakes?
```

For classification:

```text
What classes were predicted correctly?
What kinds of classification errors occurred?
```

For regression:

```text
How far are predictions from actual numbers?
```

Finally, consider whether a single train/validation split gives enough information or whether cross-validation would provide a broader view.

---

# 11. Beginner-friendly pseudocode

```text
START

identify features X
identify target y

IF y contains categories:

    problem = classification

    choose a classifier

    train classifier

    make predictions

    build confusion matrix

    calculate useful metrics:
        accuracy
        precision
        recall
        F1

ELSE IF y contains continuous numerical values:

    problem = regression

    choose regression model

    train model

    make numerical predictions

    calculate:
        MAE
        MSE
        RMSE

OPTIONALLY:

    divide training data into folds

    repeat training and validation
    with different folds

    summarize cross-validation results

END
```

---

# 12. Suggested solving approach — conceptual model selection

Use a simple three-question method.

### Question 1: What am I predicting?

```text
Category → Classification
Number   → Regression
```

### Question 2: What model makes sense?

For a beginner classification exercise:

```text
Logistic Regression → useful starting classifier
KNN                 → classify using nearby points
Naive Bayes         → probability/evidence approach
Decision Tree       → learned if-else rules
Random Forest       → many trees combined
```

You do **not** need to decide that one of these is universally "best." Different algorithms behave differently depending on the dataset.

For a simple regression exercise:

```text
Linear Regression
```

is a good starting point.

### Question 3: What should I evaluate?

```text
Classification
    ↓
Confusion matrix
Accuracy
Precision
Recall
F1

Regression
    ↓
MAE
MSE
RMSE
```

Then consider cross-validation when you want evaluation across multiple data splits.

---

# 13. Easy edge cases

### Imbalanced classification data

Suppose:

```text
95 customers → No Churn
5 customers  → Churn
```

A model predicting `No Churn` every time gets:

```text
95% accuracy
```

but detects no churn customers.

Therefore:

> Accuracy alone can be misleading.

Look at precision, recall, F1, and the confusion matrix.

---

### No positive predictions

If a classifier never predicts the positive class, normal precision calculation becomes problematic because there are no positive predictions to evaluate.

This is another reason to inspect model behavior rather than trusting one metric blindly.

---

### One huge regression error

Suppose errors are:

```text
1
2
2
30
```

That `30` will strongly influence:

```text
MSE
RMSE
```

because the errors are squared.

MAE is generally less strongly affected by that single large error.

---

### Perfect predictions

Classification:

```text
FP = 0
FN = 0
```

Regression:

```text
all errors = 0
```

In the regression case:

```text
MAE = 0
MSE = 0
RMSE = 0
```

---

### Tiny dataset

With very little data:

- classification metrics may vary greatly,
- regression errors may be unstable,
- individual examples can strongly affect the model,
- cross-validation folds can become extremely small.

Do not assume that a complicated model or many folds can replace having useful data.

---

# 14. Common mistakes to avoid

1. **Using a regression model when the target is a category.**  
   First identify the target type.

2. **Using classification metrics for numerical predictions.**  
   Accuracy does not tell you how close two house-price numbers are.

3. **Looking only at accuracy.**  
   Especially avoid this with imbalanced classes.

4. **Confusing precision and recall.**  
   Remember:

```text
Precision:
"When I predicted positive, how often was I right?"

Recall:
"Of all actual positives, how many did I find?"
```

5. **Thinking lower MAE/MSE/RMSE is worse.**  
   These measure errors, so generally:

```text
smaller error → better
```

6. **Assuming Random Forest is simply one large tree.**  
   It is a collection of multiple trees.

7. **Thinking cross-validation means training one model once.**  
   The train/validation roles rotate across folds.

8. **Choosing an algorithm before understanding the target.**  
   Start from the problem, not the model name.

---

# 15. Quick self-check questions

**1.** You want to predict whether a transaction is Fraud or Not Fraud. Is this classification or regression?

**2.** Which metric asks, “Of all actual positive examples, how many did my classifier find?”

**3.** What is the basic difference between a Decision Tree and a Random Forest?

**4.** You predict house prices. Which group of metrics is appropriate: accuracy/F1 or MAE/MSE/RMSE?

**5.** Why might cross-validation give you more information than evaluating using only one validation split?

Try answering these without looking back.

---

# 16. Hint only

For the revision problems, begin with the **target**, not the algorithm:

```text
Churn = Yes / No
      ↓
?

House price = numerical amount
      ↓
?
```

Then connect each problem to its metric family:

```text
Classification
→ confusion matrix
→ accuracy / precision / recall / F1

Regression
→ prediction errors
→ MAE / MSE / RMSE
```

For cross-validation, remember:

```text
Fold A validates once
Fold B validates once
Fold C validates once
...
```

The central idea from **Day 112** is:

> **First identify whether the task is classification or regression, then choose a suitable supervised model, and finally evaluate it with metrics that match the type of prediction.**