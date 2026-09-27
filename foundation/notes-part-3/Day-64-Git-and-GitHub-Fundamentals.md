# Day-64-Git-and-GitHub-Fundamentals

## 1. Day Number

**Day 64**

## 2. Topic Name

**Git, Repository, Commit, and GitHub**

## 3. Connection

You now have a small Python project with files such as `main.py` and `requirements.txt`.

Today, you will learn how developers **track changes** to those project files using **Git**.

The basic workflow is:

```text
Python Project
      ↓
Initialize Git
      ↓
Check Changes
      ↓
Select Files
      ↓
Commit Changes
      ↓
Later → Upload/Push to GitHub
```

---

## 4. Important Topics

The main ideas for today are:

- **Git repository** — a project folder whose changes Git tracks
- `git init` — starts Git in a folder
- `git status` — shows the current state of files
- `git add` — selects changes for the next commit
- `git commit` — saves a snapshot of selected changes
- **GitHub repository** — an online location for a Git project
- **push** — sending local Git commits to a remote repository such as GitHub

---

## 5. Foundational Notes

### What is Git?

**Git is a version-control system.**

Suppose your Python program originally contains:

```python
print("Hello")
```

Later you change it to:

```python
print("Hello, Python!")
```

Git can help you keep a history of changes like this.

Think of Git as a collection of **checkpoints for your project**.

Instead of creating folders such as:

```text
project_final
project_final2
project_really_final
project_final_fixed
```

Git lets you keep one project while recording meaningful versions of it.

### What is a repository?

A **repository**, often shortened to **repo**, is a project that Git is tracking.

For example:

```text
my_project/
│
├── main.py
├── requirements.txt
└── data/
```

After running:

```bash
git init
```

inside `my_project`, the folder becomes a Git repository.

Git creates a hidden folder named:

```text
.git
```

That folder stores Git's tracking information.

---

## 6. Git vs GitHub

Git and GitHub are related, but they are **not the same thing**.

| Git | GitHub |
|---|---|
| Version-control tool | Website/service for hosting Git repositories |
| Works on your computer | Primarily stores repositories online |
| Tracks changes | Helps share and collaborate on projects |
| Creates commits | Stores commits that you push |
| Can work without internet | Usually requires internet for syncing |

A simple way to remember it:

```text
Git = tracks your project

GitHub = stores/shares your Git project online
```

You can use **Git without GitHub**.

For today's exercise, concentrate on **local Git first**.

---

## 7. Easy Example

Imagine this project:

```text
hello_project/
│
└── main.py
```

`main.py` contains:

```python
print("Hello, Git!")
```

Open a terminal inside `hello_project`.

First initialize Git:

```bash
git init
```

Then check the project:

```bash
git status
```

Git may report that `main.py` is currently **untracked**.

That means:

> Git sees the file, but you have not yet selected it for version tracking.

Select it:

```bash
git add main.py
```

Check again:

```bash
git status
```

Now `main.py` should be ready to commit.

Create a commit:

```bash
git commit -m "Add main Python file"
```

The text:

```text
Add main Python file
```

is the **commit message**.

It describes what this checkpoint contains.

---

# 8. Problem Statement

You have a small Python project.

Your task is to:

1. Open the project folder in a terminal.
2. Initialize Git in the project.
3. Check Git's status.
4. Add `main.py`.
5. Check the status again.
6. Create your **first commit**.
7. Understand conceptually how the repository could later be pushed to GitHub.

Keep everything local for now.

---

## 9. Concepts Used

For this exercise you will use:

```text
Repository
    ↓
git init

Project state
    ↓
git status

Select a file
    ↓
git add

Save checkpoint
    ↓
git commit
```

The basic Git workflow is:

```text
Modify files
     ↓
git status
     ↓
git add
     ↓
git commit
```

You will repeat this pattern frequently while developing projects.

---

## 10. Thought Process

Suppose you have:

```text
my_python_project/
│
├── main.py
├── requirements.txt
└── data/
```

First ask:

**Is Git already tracking this project?**

If not:

```text
Initialize repository
```

Next ask:

**What files have changed or are untracked?**

Use:

```text
git status
```

Next ask:

**Which changes do I want in my next checkpoint?**

Select them with:

```text
git add
```

Finally ask:

**What meaningful description should this checkpoint have?**

Create a commit:

```text
git commit -m "..."
```

This creates a saved point in your project's Git history.

---

## 11. Beginner-Friendly Command Steps

### Step 1 — Enter the project folder

Conceptually:

```bash
cd my_python_project
```

Your terminal should be working inside the project folder.

### Step 2 — Start Git

```bash
git init
```

This turns the folder into a Git repository.

### Step 3 — Check status

```bash
git status
```

Look for `main.py`.

Initially it may appear as an **untracked file**.

### Step 4 — Select `main.py`

```bash
git add main.py
```

This tells Git:

> Include the current version of `main.py` in my next commit.

### Step 5 — Check again

```bash
git status
```

Notice how the status of `main.py` has changed.

### Step 6 — Create the first commit

The command structure is:

```bash
git commit -m "your message"
```

Use a short message explaining what you saved.

For example, a first commit could describe adding the initial Python program.

---

## What Does `git add` Really Do?

A common beginner misunderstanding is:

```text
git add = save permanently
```

Not quite.

Think of three stages:

```text
Working files
     ↓
   git add
     ↓
Staging area
     ↓
 git commit
     ↓
Git history
```

So:

```bash
git add main.py
```

means:

> Prepare this version of `main.py` for the next commit.

And:

```bash
git commit
```

means:

> Record the prepared changes as a checkpoint.

---

## What Is a Commit?

A **commit** is a recorded snapshot/checkpoint in your project's history.

For example:

```text
Commit 1
Initial Python program

        ↓

Commit 2
Add input validation

        ↓

Commit 3
Fix calculation bug
```

Each commit lets you build a history of how the project developed.

Commit messages should briefly explain the change.

Good beginner examples:

```text
Add initial Python program
```

```text
Add requirements file
```

```text
Fix input handling
```

Less useful:

```text
stuff
```

or:

```text
changes
```

---

## 12. Suggested Solving Approach — Local Git First

For now, remember this simple workflow:

```bash
git init
git status
git add <file>
git status
git commit -m "message"
```

Do not worry about GitHub yet.

First become comfortable with:

```text
See changes
     ↓
Choose changes
     ↓
Commit changes
```

Once local Git makes sense, GitHub becomes much easier to understand.

---

## How GitHub Fits In Later

Imagine your computer contains this Git repository:

```text
Your Computer

my_python_project
       │
       │ commits
       ▼
Local Git Repository
```

Later, you can create an empty repository on **GitHub** and connect your local repository to it.

Conceptually:

```text
Your Computer                      GitHub

Local Git Repository  ──push──▶  Online Repository
```

A **push** sends your local commits to the connected remote repository.

For today, you only need to understand:

```text
commit = save checkpoint locally

push = send commits to GitHub
```

You do **not** need to push anything for today's exercise.

---

## 13. Easy Edge Cases

### File is not tracked

You run:

```bash
git status
```

and see `main.py` listed as untracked.

That is normal for a new repository.

Git has discovered the file but it has not yet been selected.

Think:

```text
Untracked
   ↓
git add
   ↓
Staged
```

### Nothing to commit

Sometimes you may run a commit command and Git reports something similar to:

```text
nothing to commit
```

This usually means Git cannot find any new staged changes.

Possible reasons include:

```text
You already committed the changes.
```

or:

```text
You changed nothing since the previous commit.
```

or:

```text
You changed a file but did not git add it.
```

Use:

```bash
git status
```

to understand the situation.

---

## 14. Expected Result

By the end of the exercise, your project should still look something like:

```text
my_python_project/
│
├── main.py
├── requirements.txt
└── data/
```

But internally, it is now also a **Git repository**.

Conceptually:

```text
my_python_project/
│
├── .git/          ← Git's internal information
├── main.py
├── requirements.txt
└── data/
```

And Git should contain at least one commit representing your first project checkpoint.

Your workflow should now make sense as:

```text
Project
   ↓
git init
   ↓
Repository
   ↓
git status
   ↓
See changes
   ↓
git add
   ↓
Stage changes
   ↓
git commit
   ↓
Saved checkpoint
```

Later:

```text
Local commits
     ↓
    push
     ↓
GitHub repository
```

---

## 15. Hint Only

For today's exercise, remember these four ideas:

```text
Start tracking the project
        ↓
git init

See what Git sees
        ↓
git status

Prepare main.py
        ↓
git add ...

Create a checkpoint
        ↓
git commit ...
```

If you get confused at any point, run:

```bash
git status
```

It is one of the most useful Git commands for beginners.