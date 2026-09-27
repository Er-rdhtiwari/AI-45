# Day 115: PCA and Association Learning — Beginner Concepts

## 1. Day number

**Day 115**

## 2. Topic name

**Dimensionality Reduction and Association Learning**

Today you will learn two more unsupervised-learning ideas:

- **PCA** — reducing the number of features while keeping as much useful information as possible.
- **Association learning** — finding items or events that frequently occur together.

---

## 3. Connection

You recently learned clustering algorithms such as **K-Means** and **DBSCAN**.

Those algorithms can work with several features, for example:

```text
Age
Income
Monthly Spending
Number of Purchases
Website Visits
```

But sometimes a dataset has **many features**, and some of them contain similar information.

Today you will see:

```text
Many related features
        ↓
       PCA
        ↓
Fewer combined features
```

You will also learn a different unsupervised idea:

```text
Shopping transactions
        ↓
Association learning
        ↓
"These products often appear together"
```

---

# 4. Important topics

## Feature

A **feature** is an input characteristic describing an observation.

For a customer:

```text
Age
Income
Spending
Number of Visits
```

are possible features.

---

## Dimension

At a beginner level, you can think of a **dimension** as roughly one numerical feature used to describe your data.

For example:

```text
Height
```

is one feature, so the data is one-dimensional.

Using:

```text
Height
Weight
```

gives us two dimensions.

Using:

```text
Height
Weight
Age
Income
Spending
```

gives us five feature dimensions.

---

## Dimensionality reduction

**Dimensionality reduction** means representing data using fewer dimensions.

For example:

```text
10 original features
        ↓
3 new features
```

The goal is usually to keep useful information while simplifying the dataset.

---

## PCA intuition

**PCA** stands for:

> **Principal Component Analysis**

PCA creates new combined features called **principal components**.

Instead of keeping many original features separately, PCA tries to represent the strongest patterns in the data using fewer new dimensions.

---

## Association / rule idea

Association learning looks for patterns such as:

```text
If product A appears,
product B also appears frequently.
```

For example:

```text
Bread → Butter
```

might represent an observed purchasing association.

This does **not automatically mean** bread causes people to buy butter.

It only says the items tend to appear together in the available data.

---

# 5. Foundational notes

Both PCA and association learning can be used without a traditional target label.

That means they belong broadly to **unsupervised learning**.

But they solve different problems.

### PCA asks:

> Can I represent this numerical data with fewer features?

### Association learning asks:

> Which items or events tend to occur together?

So:

```text
PCA
→ numerical feature simplification

Association learning
→ co-occurrence patterns
```

They are very different techniques even though both can work without known target labels.

---

# 6. PCA — keeping important information using fewer dimensions

Imagine a student dataset containing:

| Student | Math | Physics | Chemistry |
|---|---:|---:|---:|
| A | 90 | 88 | 89 |
| B | 80 | 78 | 81 |
| C | 60 | 62 | 59 |
| D | 40 | 42 | 39 |

Notice something.

A student with a high Math score often also has high Physics and Chemistry scores in this tiny example.

So the three columns contain somewhat related information.

Conceptually:

```text
Math ────────┐
Physics ─────┼──→ general science-performance pattern
Chemistry ───┘
```

PCA might discover that much of the variation across those three features can be represented by a smaller number of new components.

Instead of:

```text
Math
Physics
Chemistry
```

we might represent much of the useful pattern with something like:

```text
Principal Component 1
```

or perhaps:

```text
Principal Component 1
Principal Component 2
```

depending on how much information we want to keep.

The new components are not necessarily as easy to interpret as the original columns.

That is an important tradeoff.

---

## A visual intuition

Suppose points use two related features:

```text
Feature 2
   ↑
   |             •
   |          •
   |       •
   |    •
   | •
   +----------------→ Feature 1
```

The points mostly follow one direction.

Even though technically there are two features, most of the interesting variation occurs along one main direction.

PCA tries to identify that important direction.

Conceptually:

```text
2 dimensions
     ↓
Find strongest direction of variation
     ↓
Represent points mainly along that direction
     ↓
1 dimension
```

Some information may be lost, but ideally the most useful structure is retained.

---

## Important beginner point

PCA does **not simply delete random columns**.

It usually creates **new features by combining information from the original numerical features**.

So instead of saying:

```text
Keep Age
Delete Income
Delete Spending
```

PCA is more like:

```text
Combine patterns from several numerical features
        ↓
Create Component 1
Create Component 2
...
```

You do not need the mathematical formulas behind those combinations yet.

---

# 7. Association learning with a shopping-basket example

Imagine a supermarket has these baskets:

```text
Basket 1:
Bread, Milk

Basket 2:
Bread, Butter

Basket 3:
Bread, Milk, Butter

Basket 4:
Milk

Basket 5:
Bread, Butter
```

Look carefully.

You may notice that:

```text
Bread and Butter
```

appear together several times.

Association learning tries to discover patterns like this.

A simple conceptual rule could be:

```text
Bread → Butter
```

meaning:

> When bread appears in a basket, butter also appears often enough to be interesting.

Another possible pattern could be:

```text
Bread → Milk
```

if the data supports it.

Again, the rule means **association**, not causation.

---

## Association learning is different from prediction

Suppose you had:

```text
Customer features → Will customer buy?
```

That would be closer to supervised prediction.

Association learning instead examines transactions like:

```text
Bread, Milk
Bread, Butter
Eggs, Milk
Bread, Milk, Butter
```

and asks:

> Which items commonly occur together?

---

# 8. Easy examples

## Example A: PCA

Suppose a customer dataset contains:

```text
Monthly Income
Yearly Income
Monthly Spending
Yearly Spending
```

Some of these features may be strongly related.

For example:

```text
Monthly Income
```

and:

```text
Yearly Income
```

carry very similar underlying information.

Using every related column may add unnecessary dimensionality.

PCA could potentially transform these four original numerical features into fewer components:

```text
Original:
4 dimensions

After PCA:
2 dimensions
```

while attempting to preserve much of the useful variation.

---

## Example B: Association learning

Transactions:

```text
T1 → Tea, Sugar
T2 → Tea, Biscuits
T3 → Tea, Sugar, Biscuits
T4 → Coffee, Sugar
T5 → Tea, Sugar
```

A simple pattern you might notice is:

```text
Tea ↔ Sugar
```

because they appear together frequently in this tiny dataset.

A more rule-like expression could be:

```text
Tea → Sugar
```

provided the transaction pattern supports that interpretation.

For today's lesson, simply identifying frequent co-occurrence is enough.

---

# 9. Problem statement

You have two small tasks.

### Part A — PCA

Suppose a customer dataset contains:

| Customer | Monthly Income | Yearly Income | Monthly Spending | Yearly Spending |
|---|---:|---:|---:|---:|
| A | 3000 | 36000 | 1000 | 12000 |
| B | 4000 | 48000 | 1400 | 16800 |
| C | 5000 | 60000 | 1800 | 21600 |
| D | 6000 | 72000 | 2200 | 26400 |

Explain conceptually:

1. Which features appear strongly related?
2. Why might using all four dimensions contain repeated information?
3. Why could PCA be useful?
4. What might be the benefit of reducing four dimensions to fewer components?

Do not calculate PCA manually.

### Part B — Association learning

Consider:

```text
Basket 1 → Bread, Milk
Basket 2 → Bread, Butter
Basket 3 → Bread, Milk, Butter
Basket 4 → Milk, Cereal
Basket 5 → Bread, Butter
```

Identify one product pair that appears together often enough to be an interesting possible association.

Do not calculate advanced rule statistics.

---

# 10. Concepts used

This exercise uses:

- unsupervised learning,
- features,
- dimensions,
- related numerical variables,
- dimensionality reduction,
- PCA,
- principal components,
- transaction data,
- co-occurrence,
- association rules.

The two ideas can be remembered as:

```text
PCA:
many numerical features
        ↓
fewer combined dimensions
```

and:

```text
Association learning:
many transactions
        ↓
frequent item relationships
```

---

# 11. Thought process

## PCA thought process

Start by asking:

**1. How many numerical features do I have?**

```text
Income
Spending
Visits
Purchases
...
```

**2. Do some features seem to contain similar information?**

For example:

```text
Monthly Income
Yearly Income
```

are probably closely related.

**3. Could fewer dimensions make the data simpler?**

If yes, dimensionality reduction may help.

**4. Can I accept less direct interpretability?**

The new PCA components will not necessarily have simple names such as:

```text
Income
Age
```

They are combinations of the original features.

**5. Reduce the dimensions.**

Conceptually:

```text
X with many columns
      ↓
PCA
      ↓
X_reduced with fewer columns
```

---

## Association-learning thought process

Start with transactions:

```text
Transaction 1 → A, B
Transaction 2 → A, C
Transaction 3 → A, B
```

Then ask:

**1. Which products repeatedly appear?**

**2. Which products repeatedly appear together?**

**3. Could that repeated pattern form a useful association?**

For example:

```text
A → B
```

Again, do not interpret this as cause and effect.

---

# 12. Beginner-friendly conceptual pseudocode

## PCA pseudocode

```text
START

load numerical dataset

select numerical features

inspect whether some features are related

standardize features if appropriate

choose a smaller number of components

apply PCA

create transformed dataset

compare:
    original number of features
    reduced number of components

use reduced data for later analysis if useful

END
```

A future scikit-learn workflow might look conceptually like:

```text
prepare X

scale X

create PCA model

fit and transform X

get reduced features
```

You do not need the full implementation today.

---

## Association-learning pseudocode

```text
START

collect shopping baskets

for each basket:
    record which products appear

look for products that frequently occur together

identify a possible association

example:
    Bread → Butter

interpret it as:
    these products often occur together

do not automatically assume causation

END
```

For Day 115, keeping this conceptual is enough.

---

# 13. Easy edge cases

## PCA edge case 1: Features are not very related

Suppose you have:

```text
Age
Rainfall
Shoe Size
Website Visits
```

and these features do not share much common structure.

Trying to compress them aggressively might lose useful information.

Dimensionality reduction is not automatically beneficial just because many columns exist.

---

## PCA edge case 2: Reducing too much

Suppose you have:

```text
20 original dimensions
```

and reduce them to:

```text
1 component
```

That may make the data much simpler, but could throw away too much useful information.

There is usually a tradeoff:

```text
fewer dimensions
        vs
information retained
```

---

## PCA edge case 3: Different feature scales

Imagine:

```text
Age        → 20 to 70
Income     → 20,000 to 2,000,000
```

Their numerical scales are very different.

Since PCA is sensitive to scale, preprocessing such as standardization is often important before PCA.

For now, just remember:

> **Check the scales of numerical features before applying PCA.**

---

## Association edge case 1: Very few baskets

If only two transactions exist:

```text
Bread, Milk
Bread, Butter
```

there may not be enough evidence to identify useful associations.

---

## Association edge case 2: Extremely common product

Suppose almost every customer buys a shopping bag.

You might find:

```text
Bread → Shopping Bag
Milk → Shopping Bag
Eggs → Shopping Bag
```

but that may not be especially interesting because the bag appears almost everywhere.

So frequent co-occurrence does not always mean a useful business insight.

---

## Association edge case 3: Association is not causation

If:

```text
Coffee → Sugar
```

appears frequently, that does **not** prove coffee causes people to buy sugar.

The data only shows that they frequently appear together.

---

# 14. Expected interpretation

For PCA, you should be able to say something like:

> Several numerical features seem to contain overlapping information. PCA could create fewer combined dimensions that preserve much of the important variation, making the dataset simpler for later analysis.

For association learning, you should be able to say:

> Bread and butter occur together in several baskets, so they may form an interesting product association. This represents co-occurrence, not proof that buying one causes the other purchase.

The main distinction to remember is:

```text
PCA
↓
Reduce many numerical features
into fewer dimensions
```

versus:

```text
Association learning
↓
Find items that frequently
occur together
```

---

# 15. Hint only

For the PCA part, compare:

```text
Monthly Income
Yearly Income
```

and:

```text
Monthly Spending
Yearly Spending
```

Ask yourself:

> Are these columns giving completely different information, or are some describing nearly the same underlying behavior?

If several columns are strongly related, that is a clue that dimensionality reduction might be useful.

For the shopping-basket part, count informally how often pairs appear:

```text
Bread + Milk
Bread + Butter
Milk + Butter
```

Look for a pair that repeats several times.

Keep today's mental model simple:

```text
Many related features
        ↓
       PCA
        ↓
Fewer useful dimensions
```

and:

```text
Repeated shopping baskets
        ↓
Find repeated combinations
        ↓
Possible association
```

You do **not** need eigenvectors, eigenvalues, Apriori calculations, support/confidence formulas, or other advanced mathematics for Day 115.