# Day 116: Reinforcement Learning Fundamentals and Q-Learning Introduction

## 1. Day number

**Day 116**

## 2. Topic name

**Reinforcement Learning and Very Basic Q-Learning**

---

## 3. Connection

You have now seen three broad machine-learning ideas:

```text
Supervised Learning
→ learn from labeled examples

Unsupervised Learning
→ discover patterns or structure

Reinforcement Learning
→ learn through actions and rewards
```

In reinforcement learning, we usually do not give the model a correct answer for every situation.

Instead, an **agent** interacts with an **environment**, takes actions, receives rewards, and gradually learns which actions tend to work well.

---

# 4. Important topics

## Agent

The **agent** is the learner or decision-maker.

Examples:

```text
Game character
Robot
Software player
Delivery bot
```

The agent chooses what action to take.

---

## Environment

The **environment** is the world the agent interacts with.

For example, in a grid game:

```text
+---+---+---+
|   |   | G |
+---+---+---+
|   |   |   |
+---+---+---+
| S |   |   |
+---+---+---+
```

`S` could be the starting position.

`G` could be the goal.

The grid is the environment.

---

## State

A **state** describes the agent's current situation.

For a grid game, the state could simply be:

```text
Current grid position
```

For example:

```text
State A → bottom-left square
State B → bottom-middle square
State C → middle-middle square
```

---

## Action

An **action** is something the agent can choose to do.

For a grid:

```text
UP
DOWN
LEFT
RIGHT
```

The available actions can depend on the environment.

---

## Reward

A **reward** is feedback from the environment after an action.

For example:

```text
Reach goal        → +10
Hit dangerous area → -5
Normal move        → 0
```

Positive reward usually means:

> That outcome was useful.

Negative reward usually means:

> That outcome was undesirable.

---

## Policy

A **policy** is the agent's strategy for choosing actions.

Conceptually:

```text
If I am in State A → move RIGHT
If I am in State B → move UP
If I am in State C → move RIGHT
```

A policy answers:

> What action should I choose in this state?

---

## Episode

An **episode** is one complete attempt or run.

For example:

```text
Start
  ↓
Move
  ↓
Move
  ↓
Move
  ↓
Reach goal
  ↓
Episode ends
```

Then the environment may reset and another episode begins.

---

## Q-value idea

A **Q-value** represents how useful the agent currently thinks a particular action is in a particular state.

Think of it as:

```text
Q(state, action)
```

For example:

```text
Q(State A, RIGHT) = high
```

could mean:

> Moving right from State A has worked well in past experience.

A low Q-value might mean the action has usually been less useful.

For Day 116, you do not need the full Q-learning equation.

---

# 5. Foundational notes

Reinforcement learning is different from ordinary supervised learning.

In supervised learning:

```text
Input → correct label
```

For example:

```text
Email → Spam
Image → Cat
House features → Price
```

The model learns from known answers.

In reinforcement learning:

```text
State
  ↓
Agent chooses action
  ↓
Environment changes
  ↓
Reward received
```

The agent has to discover which actions lead to better long-term results.

This creates a new problem:

> An action may not give an immediate reward but could still help the agent reach a good outcome later.

That idea becomes very important in reinforcement learning.

---

# 6. The reinforcement-learning interaction loop

The basic RL loop is:

```text
Observe state
     ↓
Choose action
     ↓
Environment responds
     ↓
Receive reward
     ↓
Observe new state
     ↓
Learn
     ↓
Choose another action
```

Suppose a robot is in a maze.

### Step 1: Observe the state

```text
"I am in square A."
```

### Step 2: Choose an action

```text
Move RIGHT
```

### Step 3: Environment changes

The robot moves into square B.

### Step 4: Receive reward

Perhaps:

```text
reward = 0
```

because nothing special happened.

### Step 5: Continue

The robot makes another decision.

Eventually:

```text
Move UP
→ reach goal
→ reward = +10
```

That positive reward gives the agent useful information about the actions that helped reach the goal.

---

# 7. Easy grid analogy

Consider this tiny environment:

```text
+-------+-------+-------+
|   A   |   B   | GOAL  |
+-------+-------+-------+
```

The agent starts at `A`.

Available action:

```text
RIGHT
```

Possible journey:

```text
A
↓ RIGHT
B
↓ RIGHT
GOAL
```

Suppose the rewards are:

```text
A → B      reward = 0
B → GOAL   reward = +10
```

At first, the agent may not know that moving right from `B` is useful.

After trying it:

```text
State B
Action RIGHT
Reward +10
```

the agent learns:

```text
RIGHT is a good action in State B.
```

So its estimate for:

```text
Q(B, RIGHT)
```

can increase.

---

# 8. Q-table conceptually

A **Q-table** stores estimated Q-values for state-action combinations.

Suppose the environment has three states:

```text
A
B
GOAL
```

and two possible actions:

```text
LEFT
RIGHT
```

A simple Q-table might initially look like this:

| State | LEFT | RIGHT |
|---|---:|---:|
| A | 0 | 0 |
| B | 0 | 0 |
| GOAL | 0 | 0 |

At the beginning, the agent may know nothing.

So every value starts at:

```text
0
```

Now suppose the agent reaches `B` and chooses:

```text
RIGHT
```

and receives:

```text
+10
```

The agent should now consider that action more useful.

Conceptually, the table might become:

| State | LEFT | RIGHT |
|---|---:|---:|
| A | 0 | 0 |
| B | 0 | 5 |
| GOAL | 0 | 0 |

The exact value `5` is just an example.

The important idea is:

```text
Good reward
    ↓
Increase confidence in that state-action choice
```

After more experience, values can continue changing.

---

# 9. Problem statement

Consider this tiny environment:

```text
START → MIDDLE → GOAL
```

There are three states:

```text
S0 = START
S1 = MIDDLE
S2 = GOAL
```

Possible actions:

```text
LEFT
RIGHT
```

Suppose the rewards are:

```text
Move normally     → 0
Reach GOAL        → +10
Move into danger  → -5
```

Your task is to identify:

1. Who or what is the **agent**?
2. What is the **environment**?
3. What are the **states**?
4. What are the possible **actions**?
5. What rewards can the agent receive?
6. What does one **episode** look like?
7. If the agent is in `S1`, chooses `RIGHT`, reaches the goal, and receives `+10`, what should happen conceptually to `Q(S1, RIGHT)`?

Do not calculate the exact Q-learning update.

---

# 10. Concepts used

This exercise uses:

- reinforcement learning,
- agent,
- environment,
- state,
- action,
- reward,
- policy,
- episode,
- Q-value,
- Q-table,
- learning through experience.

A useful summary is:

```text
Agent
  ↓
observes
  ↓
State
  ↓
chooses
  ↓
Action
  ↓
Environment changes
  ↓
Reward
  ↓
Agent learns
```

---

# 11. Thought process

When you see a beginner RL problem, think in this order.

### Step 1: Identify the agent

Ask:

> Who is making decisions?

Example:

```text
Robot
```

---

### Step 2: Identify the environment

Ask:

> What world is the agent interacting with?

Example:

```text
Grid or maze
```

---

### Step 3: Identify the states

Ask:

> What situations can the agent be in?

Example:

```text
Position A
Position B
Position C
```

---

### Step 4: Identify the actions

Ask:

> What choices can the agent make?

Example:

```text
LEFT
RIGHT
UP
DOWN
```

---

### Step 5: Identify the rewards

Ask:

> What feedback does the agent get?

For example:

```text
Goal    → +10
Danger  → -5
Move    → 0
```

---

### Step 6: Think about repeated experience

The agent may first make poor decisions:

```text
LEFT
LEFT
Danger
Reward = -5
```

Later it may discover:

```text
RIGHT
RIGHT
Goal
Reward = +10
```

Its estimates should gradually favor the more successful decisions.

---

### Step 7: Think in state-action pairs

Instead of simply asking:

```text
"Is RIGHT good?"
```

ask:

```text
"Is RIGHT good in this particular state?"
```

That distinction is important.

An action can be useful in one state and poor in another.

---

# 12. Beginner-friendly pseudocode

```text
START

create environment

create Q-table
set initial Q-values to 0

repeat for several episodes:

    place agent at starting state

    while episode is not finished:

        observe current state

        choose an action

        perform action

        receive reward

        observe next state

        update the Q-value conceptually:
            good result → value may increase
            bad result  → value may decrease

        move to next state

END
```

A slightly more detailed mental model is:

```text
current state
      ↓
choose action
      ↓
receive reward
      ↓
see next state
      ↓
update Q(state, action)
      ↓
continue
```

The goal is that, after enough experience, the Q-table contains useful information about which actions tend to lead to better outcomes.

---

# 13. Easy edge cases

## Edge case 1: Negative reward

Suppose:

```text
State B
Action LEFT
→ dangerous square
→ reward = -10
```

The agent should learn that:

```text
Q(B, LEFT)
```

is less attractive.

Conceptually:

```text
Negative reward
      ↓
Action becomes less desirable
```

This helps the agent avoid repeating poor decisions.

---

## Edge case 2: No immediate reward

Suppose:

```text
A → B
reward = 0
```

but then:

```text
B → GOAL
reward = +10
```

Moving from `A` to `B` may still have been useful even though it produced no immediate reward.

Why?

Because reaching `B` made it possible to reach the goal afterward.

This is one of the important ideas in reinforcement learning:

> Some useful actions matter because of future rewards, not immediate rewards.

You do not need the mathematics for this yet.

---

## Edge case 3: Several actions seem equally good initially

If every Q-value starts at zero:

```text
LEFT  = 0
RIGHT = 0
UP    = 0
DOWN  = 0
```

the agent initially has little information about which action is best.

It must gain experience.

That is why reinforcement learning usually involves some amount of **exploration**.

For Day 116, just understand exploration as:

> Trying actions so the agent can learn what happens.

---

## Edge case 4: Reward too easy to get

Imagine an environment where:

```text
Standing still → +5
Reaching goal  → +10
```

The agent might repeatedly stand still because it already receives easy rewards.

This illustrates why reward design matters.

The reward should encourage the behavior we actually want.

---

# 14. Expected conceptual result

After repeated episodes, imagine the Q-table becomes:

| State | LEFT | RIGHT |
|---|---:|---:|
| START | -1 | 4 |
| MIDDLE | -2 | 8 |
| GOAL | 0 | 0 |

You do not need to calculate these values.

Conceptually, they suggest:

```text
At START:
RIGHT looks better.

At MIDDLE:
RIGHT looks much better.

At GOAL:
episode is already finished.
```

The learned policy could therefore become:

```text
START  → RIGHT
MIDDLE → RIGHT
GOAL   → stop
```

The complete behavior would be:

```text
START
  ↓ RIGHT
MIDDLE
  ↓ RIGHT
GOAL
```

This is the basic idea behind Q-learning:

> Learn useful values for state-action combinations from repeated rewards and use those values to make better decisions.

---

# 15. Hint only

For the problem, start by separating the pieces:

```text
Who makes decisions?
→ agent

Where does it act?
→ environment

What situations exist?
→ states

What choices can it make?
→ actions

What feedback does it receive?
→ rewards
```

Then focus on this event:

```text
State = MIDDLE
Action = RIGHT
Result = GOAL
Reward = +10
```

Ask:

> After receiving a positive reward, should the agent consider `RIGHT` from `MIDDLE` more useful or less useful?

That tells you what should happen conceptually to:

```text
Q(MIDDLE, RIGHT)
```

For Day 116, keep this mental model:

```text
State
  ↓
Choose action
  ↓
Receive reward
  ↓
Observe next state
  ↓
Update what was learned
  ↓
Repeat
```

You do **not** need deep reinforcement learning, neural networks, or the full Q-learning equation yet.