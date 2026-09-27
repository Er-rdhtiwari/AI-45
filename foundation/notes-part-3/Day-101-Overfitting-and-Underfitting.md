# Day 101: Overfitting and Underfitting

## 1. Day Number

**Day 101**

## 2. Topic Name

**Underfitting, Overfitting, and Generalization**

## 3. Connection

Yesterday you learned why machine-learning data is often separated into:

```text
Training data
Validation data
Test data
```

Today you will learn one major reason we need unseen validation and test data.

A model can perform very well on its **training data** but still perform poorly on new data.

This problem is called **overfitting**.

A model can also be too simple to learn useful patterns at all.

This problem is called **underfitting**.

---

# 4. Important Topics

### Training Performance

This tells us how well the model performs on the examples it learned from.

```text
Training data
     ↓
Model
     ↓
Training performance
```

### Test Performance

This tells us how well the model performs on unseen test examples.

```text
Unseen test data
       ↓
     Model
       ↓
Test performance
```

### Model Complexity

Model complexity describes, at a high level, how flexible a model is.

A very simple model may fail to learn important patterns.

A very complicated model may learn the training data too specifically.

Conceptually:

```text
Too simple        Balanced         Too complex
    ↓                ↓                 ↓
Underfitting     Generalizing      Overfitting
```

---

# 5. Foundational Notes

The goal of machine learning is **not simply to get the highest possible training score**.

The real goal is usually:

> Learn useful patterns that also work on new, unseen examples.

That ability is called **generalization**.

For example, imagine a house-price model.

If it predicts its training houses extremely well but performs badly on houses it has never seen, it has not generalized well.

We therefore compare performance on different datasets.

A simplified interpretation is:

| Training Performance | Test Performance | Possible Situation |
|---|---|---|
| Poor | Poor | Underfitting |
| Good | Good | Reasonable generalization |
| Very good | Much worse | Overfitting |

These are general patterns, not absolute rules.

---

# 6. Simple Analogies

## Underfitting Analogy

Imagine a student preparing for a mathematics exam.

The student barely studies and learns only one simple rule.

When solving practice questions:

```text
poor performance
```

During the final exam:

```text
poor performance
```

The student has not learned enough.

That is similar to **underfitting**.

```text
Training performance → poor
Test performance     → poor
```

The model is too limited to capture the important patterns.

---

## Overfitting Analogy

Now imagine another student who memorizes every answer in the practice book without understanding the ideas.

On those exact questions:

```text
excellent performance
```

But when the final exam contains slightly different questions:

```text
poor performance
```

That is similar to **overfitting**.

```text
Training performance → extremely good
Test performance     → noticeably worse
```

The model learned the training examples too specifically.

---

## Good Generalization Analogy

A third student understands the underlying concepts.

They perform well on:

```text
practice questions
```

and also on:

```text
new exam questions
```

That resembles good generalization.

```text
Training performance → good
Test performance     → good
```

---

# 7. Easy Example

Suppose three models predict whether customers will renew a subscription.

Consider these hypothetical results:

| Model | Training Accuracy | Test Accuracy |
|---|---:|---:|
| Model A | 62% | 60% |
| Model B | 88% | 85% |
| Model C | 99% | 71% |

Do not look only at the training score.

Instead, compare:

```text
Training performance
        vs
Test performance
```

Ask:

- Is performance poor on both?
- Is performance good on both?
- Is training extremely good while test performance is much worse?

Those patterns help identify underfitting and overfitting.

---

# 8. Problem Statement

Consider these three hypothetical house-price models:

| Model | Training Score | Test Score |
|---|---:|---:|
| Model 1 | 58% | 56% |
| Model 2 | 87% | 84% |
| Model 3 | 99% | 68% |

Your task is to identify which model may be:

```text
Underfitting
Reasonable
Overfitting
```

For each model, explain your reasoning using the relationship between its **training score** and **test score**.

Do not use advanced mathematics.

---

# 9. Concepts Used

This exercise combines several concepts you have already learned:

- training data
- test data
- unseen data
- model performance
- generalization
- model complexity
- underfitting
- overfitting

The connection is:

```text
Training/Test Split
        ↓
Compare performance
        ↓
Look for generalization problems
        ↓
Underfitting or Overfitting
```

---

# 10. Thought Process

When comparing a model's training and test results, ask two questions.

### Question 1: Is training performance good?

If training performance is already poor, the model may not have learned the training patterns properly.

That suggests:

```text
possible underfitting
```

### Question 2: Is test performance close to training performance?

Suppose:

```text
Training = very high
Test = much lower
```

The model may have learned the training examples too specifically.

That suggests:

```text
possible overfitting
```

But if:

```text
Training = good
Test = similarly good
```

the model may be generalizing reasonably well.

---

# 11. Beginner-Friendly Decision Steps

Use this simple process.

### Step 1

Look at the training score.

```text
Is it low?
```

If yes, investigate possible underfitting.

### Step 2

Look at the test score.

```text
Is it also low?
```

Low training + low test performance often suggests underfitting.

### Step 3

Compare the two scores.

```text
Training score - Test score
```

You do not need advanced calculations.

Simply ask whether there is a **large difference**.

### Step 4

If training is extremely strong but test performance drops noticeably:

```text
possible overfitting
```

### Step 5

If both training and test performance are reasonably strong and relatively close:

```text
possible good generalization
```

---

# 12. Suggested Solving Approach

Use **conceptual analysis**.

For each model, make a small comparison:

```text
Model X

Training:
high / medium / low

Test:
high / medium / low

Difference:
small / large

Possible conclusion:
underfitting / reasonable / overfitting
```

Focus on the **pattern**, not just which number is largest.

---

# 13. Easy Edge Cases

### Training and Test Scores Are Both Extremely High

For example:

```text
Training = 98%
Test = 97%
```

This does **not automatically mean overfitting**.

If the unseen test data is appropriate and genuinely separate, this could simply mean the problem is easy or the model works very well.

---

### Training and Test Scores Are Both Low

Example:

```text
Training = 55%
Test = 54%
```

The small difference does not necessarily mean the model is good.

Both performances are poor.

This could indicate underfitting.

---

### Test Score Is Slightly Better Than Training Score

Example:

```text
Training = 84%
Test = 86%
```

This can happen.

Real datasets contain variation, so the scores do not have to follow a perfect pattern.

Do not conclude that something is automatically wrong because the test score is slightly higher.

---

### Very Small Test Dataset

Suppose the test set contains only a few examples.

Then a test score can change dramatically because of just one or two predictions.

This makes the result less reliable.

---

# 14. Expected Classification

Your final reasoning should follow a structure like this:

```text
Model 1:
Training performance = ______
Test performance = ______
Difference = ______
Likely situation = ______

Model 2:
Training performance = ______
Test performance = ______
Difference = ______
Likely situation = ______

Model 3:
Training performance = ______
Test performance = ______
Difference = ______
Likely situation = ______
```

Remember these three broad patterns:

```text
Poor training + poor test
→ possible underfitting

Good training + good test
→ possible reasonable generalization

Excellent training + much poorer test
→ possible overfitting
```

---

# 15. Hint Only

For the three-model exercise, do **not** simply choose the model with the highest training score.

Compare each model's training score with its test score.

Ask:

```text
Did the model struggle even on data it learned from?

Or

Did it perform extremely well on training data
but lose much of that performance on unseen data?

Or

Did it perform well on both?
```

Think of the three student analogies:

**didn't learn enough → understood the ideas → memorized the practice questions.**