# Day 93: Probability Fundamentals

## 1. Day number

**Day 93**

## 2. Topic name

**Probability and Simple Events**

Probability is a way to describe **how likely something is to happen**.

---

## 3. Connection

Yesterday, descriptive statistics helped you summarize **data that has already been observed**.

Today, probability helps you describe **uncertainty about outcomes that could happen**.

A simple way to remember the difference:

```text
Statistics   → What happened in the data?
Probability  → What could happen, and how likely is it?
```

---

## 4. Important topics

Today you will learn:

- **Experiment**
- **Outcome**
- **Event**
- Probability between **0 and 1**
- **Complement** of an event

For simple cases where every outcome is equally likely:

```text
Probability =
number of favorable outcomes
─────────────────────────────
total number of possible outcomes
```

---

## 5. Foundational notes

Probability always lies between:

```text
0 and 1
```

Think of the scale like this:

```text
0 ---------------- 0.5 ---------------- 1
Impossible        uncertain            Certain
```

For example:

```text
Probability = 0
```

means the event cannot happen.

```text
Probability = 1
```

means the event will definitely happen.

And:

```text
Probability = 0.5
```

means a 50% chance.

Probability does **not** guarantee what will happen in one individual attempt. It describes likelihood.

---

## 6. Experiment, outcome, and event

### Experiment

An **experiment** is an action whose result is uncertain.

Examples:

- flipping a coin
- rolling a die
- randomly selecting a customer
- randomly selecting a product

Suppose we roll a normal six-sided die.

That is the **experiment**.

### Outcome

An **outcome** is one possible result of the experiment.

For a die:

```text
1, 2, 3, 4, 5, 6
```

Each number is an individual outcome.

### Event

An **event** is one or more outcomes that we are interested in.

For example:

> Rolling an even number.

The successful outcomes are:

```text
2, 4, 6
```

So the event contains three possible outcomes.

---

# 7. Probability using simple examples

## Coin example

A normal coin has two possible outcomes:

```text
Heads
Tails
```

Suppose we want:

> Probability of getting Heads.

There is:

```text
1 favorable outcome
2 total outcomes
```

Therefore:

```text
P(Heads) = 1 / 2
         = 0.5
```

So the probability is:

**0.5 or 50%**

---

## Dice example

Suppose we roll a fair six-sided die:

```text
1, 2, 3, 4, 5, 6
```

What is the probability of rolling `4`?

There is one favorable outcome:

```text
4
```

out of six possible outcomes.

Therefore:

```text
P(4) = 1 / 6
```

Approximately:

```text
0.167
```

or:

```text
16.7%
```

---

## Business example

Imagine a box contains five customer orders:

```text
Order 1 → Delivered
Order 2 → Pending
Order 3 → Delivered
Order 4 → Delivered
Order 5 → Pending
```

Suppose one order is selected randomly.

There are:

```text
3 delivered orders
5 total orders
```

So:

```text
P(Delivered) = 3 / 5
             = 0.6
```

That means:

**60% probability**

This is a simplified example where every order has an equal chance of being selected.

---

# 8. Easy example

Suppose a bag contains four cards:

```text
Red
Blue
Red
Green
```

One card is selected randomly.

What is the probability of selecting a **red card**?

First count the total cards:

```text
4
```

Count the favorable outcomes:

```text
2 red cards
```

Therefore:

```text
P(Red) = 2 / 4
       = 0.5
```

So:

**Probability of red = 0.5 = 50%**

---

# 9. Complement

The **complement** of an event means:

> The event does not happen.

Suppose:

```text
P(Rain) = 0.3
```

Then:

```text
P(No Rain) = 0.7
```

Why?

Because either it rains or it does not rain, so their probabilities must total `1`.

The basic complement rule is:

```text
P(not A) = 1 - P(A)
```

For example:

```text
P(Rain) = 0.3

P(No Rain)
= 1 - 0.3
= 0.7
```

A useful check is:

```text
P(A) + P(not A) = 1
```

---

# 10. Problem statement

A fair six-sided die contains:

```text
1, 2, 3, 4, 5, 6
```

Calculate the probability of:

1. Rolling a `3`
2. Rolling an even number
3. Rolling a number greater than `4`
4. Not rolling a `6`

Do the calculations manually before using Python.

---

# 11. Concepts used

This exercise uses:

- experiment
- sample of possible outcomes
- outcome
- event
- favorable outcomes
- total outcomes
- simple probability
- complement
- fractions
- decimals
- percentages

---

# 12. Thought process

When solving a beginner probability problem, follow this pattern:

```text
What is the experiment?
        ↓
What outcomes are possible?
        ↓
Which outcomes satisfy my event?
        ↓
Count favorable outcomes
        ↓
Count total outcomes
        ↓
favorable / total
        ↓
Convert to decimal or percentage if needed
```

For example, suppose the event is:

> Roll an even number.

Start with all outcomes:

```text
1, 2, 3, 4, 5, 6
```

Then identify only the outcomes belonging to the event:

```text
2, 4, 6
```

Now compare the number of favorable outcomes with the total number of outcomes.

---

# 13. Beginner-friendly formulas and calculations

For equally likely outcomes:

```text
P(Event) =
Favorable outcomes / Total possible outcomes
```

Suppose there are `2` favorable outcomes from `8` possible outcomes:

```text
P(Event) = 2 / 8
```

Simplify:

```text
= 1 / 4
```

As a decimal:

```text
= 0.25
```

As a percentage:

```text
= 25%
```

So all of these describe the same probability:

```text
1/4 = 0.25 = 25%
```

For a complement:

```text
P(not A) = 1 - P(A)
```

If:

```text
P(A) = 0.25
```

then:

```text
P(not A)

= 1 - 0.25

= 0.75
```

---

# 14. Percentage vs probability

Probability is commonly written as either a decimal or a percentage.

For example:

```text
Probability = 0.75
```

means the same thing as:

```text
75%
```

To convert a probability to a percentage:

```text
probability × 100
```

Example:

```text
0.4 × 100 = 40%
```

To convert a percentage back to probability:

```text
percentage / 100
```

Example:

```text
40 / 100 = 0.4
```

A useful reference is:

| Probability | Percentage | Meaning |
|---:|---:|---|
| `0` | `0%` | Impossible |
| `0.25` | `25%` | One-quarter chance |
| `0.5` | `50%` | Half chance |
| `0.75` | `75%` | Three-quarter chance |
| `1` | `100%` | Certain |

---

# 15. Easy edge cases

### Impossible event

Suppose we roll a normal six-sided die.

What is the probability of rolling `10`?

The die contains:

```text
1, 2, 3, 4, 5, 6
```

There are no favorable outcomes.

Therefore:

```text
P(10) = 0 / 6 = 0
```

So an impossible event has:

**Probability = 0**

### Certain event

What is the probability of rolling a number between `1` and `6`?

Every possible outcome satisfies this condition.

```text
6 favorable outcomes
6 total outcomes
```

Therefore:

```text
6 / 6 = 1
```

So a certain event has:

**Probability = 1**

---

# 16. Expected calculations

For a simple problem, your working should generally look like this:

```text
Possible outcomes:
{...}

Favorable outcomes:
{...}

Number of favorable outcomes = ?

Total number of outcomes = ?

Probability =
favorable / total

Decimal = ?

Percentage = ?%
```

For complements:

```text
P(event) = ...

P(not event)
= 1 - P(event)
```

The most important rule for today is:

```text
0 ≤ Probability ≤ 1
```

---

# 17. Hint only

For the die exercise:

```text
1, 2, 3, 4, 5, 6
```

For **rolling a 3**, count how many `3`s appear among the six possibilities.

For **rolling an even number**, first identify:

```text
2, 4, 6
```

For **greater than 4**, identify which outcomes satisfy:

```text
number > 4
```

For **not rolling a 6**, you can either count all outcomes except `6`, or use the complement:

```text
P(not 6) = 1 - P(6)
```

Keep everything in the form:

```text
favorable outcomes
──────────────────
total outcomes
```

before converting your answer to a decimal or percentage.