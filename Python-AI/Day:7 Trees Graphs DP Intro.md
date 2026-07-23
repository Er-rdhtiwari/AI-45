# Day 7 – Trees, Graphs, Dynamic Programming Intro & Week 1 Review

## 1. The Big Picture

Trees, graphs, and dynamic programming solve different types of problems:

| Concept             | Main idea                                | Typical interview signal                                 |
| ------------------- | ---------------------------------------- | -------------------------------------------------------- |
| Tree                | Hierarchical relationships               | Parent/child, folders, organization hierarchy            |
| Graph               | General relationships between entities   | Networks, dependencies, routes, workflows                |
| DFS                 | Explore one path deeply before returning | “Find any path,” recursion, nested structures            |
| BFS                 | Explore level by level                   | Shortest path in an unweighted graph                     |
| Dynamic Programming | Reuse answers to overlapping subproblems | Optimization, counting, “maximum/minimum number of ways” |

A useful mental model:

```text
Tree  = a special graph with no cycles
Graph = nodes connected by edges
DFS   = go deep
BFS   = go wide
DP    = solve once, remember, reuse
```

---

# Part 1: Trees

## 2. What Is a Tree?

A tree is a collection of nodes connected in a hierarchy.

```text
             A
           /   \
          B     C
         / \     \
        D   E     F
```

Important terms:

* **Root:** The top node. Here, `A`.
* **Parent:** A node directly above another node.
* **Child:** A node directly below another node.
* **Leaf:** A node with no children. Here, `D`, `E`, and `F`.
* **Depth:** Distance from the root to a node.
* **Height:** Longest downward path from a node to a leaf.
* **Subtree:** A node and everything below it.

A tree with `n` nodes has exactly `n - 1` edges.

## Binary Tree

A binary tree is a tree where each node has at most two children:

* Left child
* Right child

A binary tree is not automatically a binary search tree.

## Binary Search Tree

In a valid binary search tree, or BST:

```text
All values in the left subtree  < node value
All values in the right subtree > node value
```

Example:

```text
          8
        /   \
       3     10
      / \      \
     1   6      14
```

Searching a balanced BST usually takes `O(log n)`. In the worst case, a badly skewed BST can take `O(n)`.

---

# Part 2: Tree Traversals

Tree traversal means visiting every node in a particular order.

The three standard depth-first traversals are:

1. Pre-order
2. In-order
3. Post-order

Consider this tree:

```text
        A
       / \
      B   C
     / \
    D   E
```

## 3. Pre-order Traversal

Order:

```text
Node → Left → Right
```

Result:

```text
A, B, D, E, C
```

### Intuition

Process the current node before processing its children.

Use pre-order when:

* Copying or serializing a tree
* Creating a hierarchical outline
* Processing a parent before its children
* Propagating configuration from parent to child

---

## 4. In-order Traversal

Order:

```text
Left → Node → Right
```

Result:

```text
D, B, E, A, C
```

### Intuition

Process the node between its left and right subtrees.

Important interview fact:

> In-order traversal of a valid binary search tree returns values in sorted order.

Use in-order when:

* Reading BST values in sorted order
* Finding the kth-smallest element in a BST
* Validating certain BST properties

---

## 5. Post-order Traversal

Order:

```text
Left → Right → Node
```

Result:

```text
D, E, B, C, A
```

### Intuition

Process the children before processing the parent.

Use post-order when:

* Deleting a tree
* Calculating directory sizes
* Calculating subtree results
* Evaluating expression trees
* Shutting down child services before parent services

---

## 6. Python Code for Tree Traversals

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    value: str
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def preorder(node: Optional[TreeNode]) -> None:
    """
    Pre-order: Node -> Left -> Right
    """
    # Base case:
    # When we move past a leaf node, the child is None.
    if node is None:
        return

    # Process the current node before its children.
    print(node.value)

    # Recursively visit the left subtree.
    preorder(node.left)

    # Recursively visit the right subtree.
    preorder(node.right)


def inorder(node: Optional[TreeNode]) -> None:
    """
    In-order: Left -> Node -> Right
    """
    if node is None:
        return

    # Visit everything on the left first.
    inorder(node.left)

    # Process the current node.
    print(node.value)

    # Visit everything on the right.
    inorder(node.right)


def postorder(node: Optional[TreeNode]) -> None:
    """
    Post-order: Left -> Right -> Node
    """
    if node is None:
        return

    # Children must be processed before the parent.
    postorder(node.left)
    postorder(node.right)

    print(node.value)


# Build this tree:
#
#         A
#        / \
#       B   C
#      / \
#     D   E

root = TreeNode(
    value="A",
    left=TreeNode(
        value="B",
        left=TreeNode("D"),
        right=TreeNode("E"),
    ),
    right=TreeNode("C"),
)

print("Pre-order:")
preorder(root)

print("In-order:")
inorder(root)

print("Post-order:")
postorder(root)
```

## Complexity

Each traversal visits every node exactly once:

* Time: `O(n)`
* Recursive stack space:

  * Balanced tree: `O(log n)`
  * Completely skewed tree: `O(n)`

## Common Pitfalls

* Forgetting the `node is None` base case
* Mixing up traversal order
* Assuming every binary tree is a BST
* Ignoring recursion depth for extremely deep trees
* Using node values as unique identifiers when duplicate values may exist

---

# Part 3: Graphs

## 7. What Is a Graph?

A graph contains:

* **Vertices or nodes:** The entities
* **Edges:** The relationships between entities

Example:

```text
A ----- B
|       |
|       |
C ----- D
```

Graphs are more general than trees.

A graph may:

* Have cycles
* Have multiple paths between nodes
* Be directed or undirected
* Be weighted or unweighted
* Have disconnected sections

## Directed Graph

Edges have direction:

```text
A → B → C
```

Example:

```text
Data ingestion → Embedding generation → Vector indexing
```

## Undirected Graph

Edges work in both directions:

```text
A — B
```

Examples:

* Friendship network
* Bidirectional network connection
* Undirected map representation

## Weighted Graph

Each edge has a cost:

```text
A --5--> B
```

Weights may represent:

* Distance
* Network latency
* Financial cost
* Processing time
* Risk score

## Directed Acyclic Graph

A DAG is a directed graph with no directed cycles.

```text
A → B → D
 \      ↑
  → C ──
```

You cannot follow the arrows and return to the same node.

DAGs are heavily used in:

* Data pipelines
* Job scheduling
* Build systems
* Dependency management
* Airflow workflows
* LangGraph workflows
* Model training pipelines

---

# Part 4: Representing a Graph in Python

## 8. Adjacency List

The most common representation is an adjacency list.

```python
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": []
}
```

This means:

```text
A → B
A → C
B → D
C → D
```

An adjacency list is efficient when the graph is sparse, meaning most possible edges do not exist.

For `V` vertices and `E` edges:

* Space: `O(V + E)`

---

# Part 5: Depth-First Search

## 9. DFS Intuition

DFS explores one path as deeply as possible before returning.

Imagine exploring folders:

```text
Root
├── Documents
│   ├── Reports
│   └── Invoices
└── Images
```

DFS might explore:

```text
Root
→ Documents
→ Reports
→ back
→ Invoices
→ back
→ Images
```

A useful phrase:

> DFS goes deep first, then backtracks.

DFS can be implemented using:

* Recursion
* An explicit stack

## DFS Is Useful For

* Checking whether a path exists
* Detecting cycles
* Exploring all possibilities
* Tree traversal
* Connected components
* Dependency analysis
* Backtracking problems
* Processing nested structures

---

## 10. Recursive DFS in Python

```python
from typing import Dict, List, Set


def dfs(
    graph: Dict[str, List[str]],
    node: str,
    visited: Set[str],
) -> None:
    """
    Visit all nodes reachable from 'node' using DFS.
    """

    # Important:
    # Mark the node before visiting its neighbors.
    # Otherwise, cycles could cause infinite recursion.
    visited.add(node)

    print(node)

    # Explore each neighboring node.
    for neighbor in graph.get(node, []):
        # Only explore nodes that have not already been visited.
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": [],
}

visited_nodes: Set[str] = set()
dfs(graph, "A", visited_nodes)
```

Possible output:

```text
A
B
D
C
```

The exact traversal order depends on the order of neighbors.

## Tricky Part: Why Do We Need `visited`?

Consider:

```text
A → B
↑   ↓
└── C
```

Without a visited set:

```text
A → B → C → A → B → C ...
```

The traversal would never end.

Trees normally do not require a visited set when moving only from parent to child. General graphs usually do.

---

## 11. Iterative DFS Using a Stack

```python
from typing import Dict, List, Set


def iterative_dfs(
    graph: Dict[str, List[str]],
    start: str,
) -> List[str]:
    """
    Perform DFS without recursion.
    """

    # A stack follows Last In, First Out behavior.
    stack = [start]

    visited: Set[str] = set()
    traversal_order: List[str] = []

    while stack:
        # Remove the most recently added node.
        current = stack.pop()

        # The same node may have been added from multiple paths.
        # Skip it if we already processed it.
        if current in visited:
            continue

        visited.add(current)
        traversal_order.append(current)

        # Reverse the neighbors only to preserve a predictable
        # left-to-right traversal when using a stack.
        for neighbor in reversed(graph.get(current, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return traversal_order


graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [],
    "E": [],
}

print(iterative_dfs(graph, "A"))
```

Output:

```text
['A', 'B', 'D', 'C', 'E']
```

---

# Part 6: Breadth-First Search

## 12. BFS Intuition

BFS explores nodes level by level.

For this tree:

```text
        A
       / \
      B   C
     / \   \
    D   E   F
```

BFS order is:

```text
A, B, C, D, E, F
```

A useful phrase:

> BFS explores the nearest nodes first.

BFS uses a queue because a queue follows First In, First Out behavior.

## BFS Is Useful For

* Shortest path in an unweighted graph
* Level-order tree traversal
* Finding the nearest matching node
* Network hop calculations
* Minimum-number-of-steps problems
* Dependency layers
* Job execution by readiness level

---

## 13. BFS in Python

```python
from collections import deque
from typing import Dict, List, Set


def bfs(
    graph: Dict[str, List[str]],
    start: str,
) -> List[str]:
    """
    Visit all nodes reachable from 'start' using BFS.
    """

    # deque supports efficient removal from the left.
    queue = deque([start])

    # Mark the starting node as visited immediately.
    # This prevents it from being added to the queue multiple times.
    visited: Set[str] = {start}

    traversal_order: List[str] = []

    while queue:
        # Remove the node that has been waiting the longest.
        current = queue.popleft()
        traversal_order.append(current)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                # Mark as visited when adding to the queue,
                # not when removing it.
                #
                # Otherwise, several nodes may add the same neighbor.
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal_order


graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": [],
    "F": [],
}

print(bfs(graph, "A"))
```

Output:

```text
['A', 'B', 'C', 'D', 'E', 'F']
```

## Why Mark a Node Visited When Enqueuing?

Suppose both `B` and `C` connect to `D`.

```text
A → B → D
 \→ C → D
```

If `D` is marked visited only when removed from the queue:

* `B` may add `D`
* `C` may also add `D`

The queue contains duplicate work.

Marking the node when it enters the queue prevents this.

---

# Part 7: DFS vs BFS

| Question                 | DFS                         | BFS                         |
| ------------------------ | --------------------------- | --------------------------- |
| Main data structure      | Stack or recursion          | Queue                       |
| Exploration style        | Deep first                  | Level by level              |
| Unweighted shortest path | Not guaranteed              | Yes                         |
| Memory usage             | Often lower for wide graphs | Can be high for wide graphs |
| Cycle detection          | Commonly used               | Can also be used            |
| Tree traversals          | Pre-, in-, post-order       | Level-order                 |
| Path existence           | Good                        | Good                        |
| Nearest result           | Not guaranteed              | Good                        |

## Recognition Rule

Use DFS when the question sounds like:

* Explore every possibility
* Check whether any path exists
* Process nested data
* Detect cycles
* Traverse an entire hierarchy
* Compute a result from child subtrees

Use BFS when the question sounds like:

* Find the shortest path
* Find the nearest item
* Find the minimum number of moves
* Process nodes level by level
* Execute dependency layers

## Complexity

For both DFS and BFS:

* Time: `O(V + E)`
* Space: `O(V)`

Every reachable vertex and edge is processed at most a constant number of times.

---

# Part 8: Real-System Application—Dependency Graphs

## 14. Data Pipeline Example

Consider an AI document-ingestion pipeline:

```text
Read documents
      |
      v
Clean documents
      |
      v
Split into chunks
      |
      v
Generate embeddings
      |
      v
Store in vector database
```

Some steps may execute in parallel:

```text
                     ┌→ Extract metadata ─┐
Read → Clean → Chunk ┤                    ├→ Vector index
                     └→ Generate embedding┘
```

This is naturally represented as a DAG.

Each step is a node. Dependencies are directed edges.

---

## 15. Why DAGs Matter in Airflow

In an Airflow-style pipeline:

```text
download_data
      |
      v
clean_data
    /     \
   v       v
train   evaluate
   \       /
    v     v
    deploy
```

A scheduler must understand:

* Which jobs are ready?
* Which jobs still have dependencies?
* Which jobs can run in parallel?
* Is there an invalid cycle?
* What should happen after failure?

A cyclic dependency would be invalid:

```text
A depends on B
B depends on C
C depends on A
```

No task can start.

---

# Part 9: Topological Ordering for Scheduling

A topological order places every dependency before the task that depends on it.

Example:

```text
A → C
B → C
C → D
```

Possible topological order:

```text
A, B, C, D
```

Another valid order:

```text
B, A, C, D
```

Topological ordering only works for DAGs.

## 16. Simple Topological Sort with Kahn’s Algorithm

```python
from collections import defaultdict, deque
from typing import Dict, List, Tuple


def topological_sort(
    tasks: List[str],
    dependencies: List[Tuple[str, str]],
) -> List[str]:
    """
    Each dependency is represented as:

        (prerequisite, dependent_task)

    For example:
        ("clean_data", "train_model")

    means clean_data must finish before train_model.
    """

    graph: Dict[str, List[str]] = defaultdict(list)

    # indegree[task] tells us how many unfinished
    # prerequisites the task currently has.
    indegree = {task: 0 for task in tasks}

    for prerequisite, dependent in dependencies:
        graph[prerequisite].append(dependent)
        indegree[dependent] += 1

    # Tasks with indegree 0 have no unmet prerequisites.
    queue = deque(
        task
        for task in tasks
        if indegree[task] == 0
    )

    execution_order: List[str] = []

    while queue:
        current = queue.popleft()
        execution_order.append(current)

        # Completing 'current' satisfies one dependency
        # for each task that depends on it.
        for dependent in graph[current]:
            indegree[dependent] -= 1

            # This task is now ready to execute.
            if indegree[dependent] == 0:
                queue.append(dependent)

    # If we could not process every task, the graph contains a cycle.
    if len(execution_order) != len(tasks):
        raise ValueError("Dependency graph contains a cycle")

    return execution_order


tasks = [
    "load_documents",
    "clean_documents",
    "create_chunks",
    "generate_embeddings",
    "build_index",
]

dependencies = [
    ("load_documents", "clean_documents"),
    ("clean_documents", "create_chunks"),
    ("create_chunks", "generate_embeddings"),
    ("generate_embeddings", "build_index"),
]

print(topological_sort(tasks, dependencies))
```

Output:

```text
[
    'load_documents',
    'clean_documents',
    'create_chunks',
    'generate_embeddings',
    'build_index'
]
```

## Interview Connection

Topological sort commonly appears in questions such as:

* Course Schedule
* Build Order
* Package Dependency Resolution
* Job Scheduling
* Pipeline Execution
* Detecting circular dependencies

---

# Part 10: LangGraph Connection

A LangGraph workflow may contain nodes such as:

```text
Receive request
      |
      v
Classify intent
   /         \
  v           v
Retrieve     Call tool
  \           /
   v         v
Generate response
      |
      v
Human approval?
   /       \
 yes       no
  |         |
  v         v
Return     Revise
```

Graph concepts map naturally:

| Graph concept    | LangGraph-style meaning                                  |
| ---------------- | -------------------------------------------------------- |
| Node             | LLM call, tool call, retrieval step, validation step     |
| Edge             | Transition to another step                               |
| Conditional edge | Route based on state or model result                     |
| State            | Information passed through the workflow                  |
| Cycle            | Repeated refinement, retry, or agent loop                |
| Checkpoint       | Saved workflow state                                     |
| DFS/BFS          | Useful mental models for graph exploration and debugging |

Unlike a strict pipeline DAG, an agent graph may intentionally contain cycles:

```text
Plan → Use tool → Evaluate → Plan again
```

The cycle must have a stopping condition, such as:

* Maximum number of attempts
* Sufficient answer quality
* Tool result found
* Human approval
* Timeout or budget limit

Otherwise, the agent may loop indefinitely.

---

# Part 11: Dynamic Programming

## 17. What Is Dynamic Programming?

Dynamic programming, or DP, is a technique for problems where:

1. A problem can be divided into smaller subproblems.
2. The same subproblems appear repeatedly.
3. Their answers can be stored and reused.

Mental model:

```text
Brute force:
Solve the same smaller problem again and again.

Dynamic programming:
Solve it once, store the answer, reuse it.
```

DP is not a single algorithm. It is a problem-solving pattern.

---

## 18. Two Main DP Properties

### Overlapping Subproblems

The same smaller problem is calculated multiple times.

For Fibonacci:

```text
fib(5)
├── fib(4)
│   ├── fib(3)
│   └── fib(2)
└── fib(3)
```

`fib(3)` is calculated more than once.

### Optimal Substructure

The best answer for the larger problem can be built from the best answers to smaller problems.

For example:

```text
Best value using first 5 items
```

can be built from:

```text
Best value using first 4 items
```

---

# Part 12: Top-Down vs Bottom-Up DP

## 19. Top-Down DP: Memoization

Top-down DP starts with the original problem and recursively asks for smaller answers.

Results are cached.

```text
Original problem
      ↓
Smaller problem
      ↓
Even smaller problem
      ↓
Base case
```

Memoization means:

> Store the result of a function call so the same input does not need to be solved again.

### Fibonacci with Memoization

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """
    Return the nth Fibonacci number using top-down DP.
    """

    # Base cases stop the recursion.
    if n <= 1:
        return n

    # These results are automatically cached.
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(10))  # 55
```

Complexity:

* Time: `O(n)`
* Space: `O(n)`

Without memoization, recursive Fibonacci takes approximately `O(2^n)` time.

---

## 20. Bottom-Up DP: Tabulation

Bottom-up DP starts from the smallest known answers and builds upward.

```python
def fibonacci_bottom_up(n: int) -> int:
    """
    Return the nth Fibonacci number using bottom-up DP.
    """

    if n <= 1:
        return n

    # dp[i] stores the answer for fibonacci(i).
    dp = [0] * (n + 1)

    # Known base values.
    dp[0] = 0
    dp[1] = 1

    # Build larger answers from smaller answers.
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


print(fibonacci_bottom_up(10))  # 55
```

Space can be optimized because we only need the previous two values:

```python
def fibonacci_optimized(n: int) -> int:
    if n <= 1:
        return n

    previous_two = 0
    previous_one = 1

    for _ in range(2, n + 1):
        current = previous_two + previous_one

        # Shift the values for the next iteration.
        previous_two = previous_one
        previous_one = current

    return previous_one
```

Complexity:

* Time: `O(n)`
* Space: `O(1)`

---

## Top-Down vs Bottom-Up

| Factor                 | Top-down                            | Bottom-up                |
| ---------------------- | ----------------------------------- | ------------------------ |
| Style                  | Recursive                           | Iterative                |
| Cache                  | Dictionary or memoization decorator | Array/table              |
| Computes               | Only requested states               | Usually all states       |
| Recursion depth risk   | Yes                                 | No                       |
| Often easier initially | Yes                                 | Sometimes less intuitive |
| Space optimization     | Possible, but less direct           | Often easier             |

---

# Part 13: How to Recognize a DP Problem

DP is a strong candidate when a question asks for:

* Maximum or minimum result
* Number of ways
* Whether something is possible
* Best score, profit, cost, or path
* Repeated choices across positions
* Optimization under a constraint

Common phrases:

```text
Maximum profit
Minimum cost
Number of combinations
Can we form...
Longest...
Fewest operations...
Best possible...
```

Before applying DP, define:

1. **State:** What information uniquely describes a smaller problem?
2. **Choice:** What decisions can be made?
3. **Transition:** How does one state lead to another?
4. **Base case:** What are the smallest known answers?
5. **Final answer:** Which state contains the result?

---

# Part 14: 0/1 Knapsack Intuition

## 21. The Problem

You have several items.

Each item has:

* A weight
* A value

You have a bag with limited capacity.

Each item can be:

* Included once
* Excluded

You cannot take half an item.

Example:

| Item    | Weight | Value |
| ------- | -----: | ----: |
| Laptop  |      3 |     8 |
| Camera  |      2 |     5 |
| Battery |      1 |     3 |

Bag capacity:

```text
4
```

Possible selections:

* Laptop only: weight `3`, value `8`
* Camera + Battery: weight `3`, value `8`
* Laptop + Battery: weight `4`, value `11`
* All three: weight `6`, not allowed

Best answer:

```text
Laptop + Battery = value 11
```

## Why Is It Called 0/1 Knapsack?

For every item:

```text
0 = do not take it
1 = take it
```

You cannot take the same item multiple times.

---

## 22. Knapsack Decision Tree

For each item, make one of two choices:

```text
                    Item i
                  /        \
             Exclude       Include
                |             |
         Solve remaining   Add value and
         items normally    reduce capacity
```

The fundamental recurrence is:

```text
best(i, capacity) =
    max(
        skip item i,
        take item i
    )
```

More precisely:

```text
skip = best(i + 1, capacity)

take = value[i] + best(
    i + 1,
    capacity - weight[i]
)
```

The `take` option is only valid when the item fits.

---

# Part 15: Top-Down 0/1 Knapsack

```python
from functools import lru_cache
from typing import List


def knapsack_top_down(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> int:
    """
    Return the maximum total value that fits within capacity.

    Each item may be selected at most once.
    """

    if len(weights) != len(values):
        raise ValueError("weights and values must have equal length")

    if capacity < 0:
        raise ValueError("capacity cannot be negative")

    @lru_cache(maxsize=None)
    def solve(index: int, remaining_capacity: int) -> int:
        """
        State:
        - index: the item currently being considered
        - remaining_capacity: unused capacity in the bag
        """

        # No items remain.
        if index == len(weights):
            return 0

        # Choice 1: Skip the current item.
        skip_current = solve(
            index + 1,
            remaining_capacity,
        )

        # Choice 2 starts as invalid.
        take_current = 0

        # We may take the item only if it fits.
        if weights[index] <= remaining_capacity:
            take_current = values[index] + solve(
                index + 1,
                remaining_capacity - weights[index],
            )

        # Keep the better of the two decisions.
        return max(skip_current, take_current)

    return solve(0, capacity)


weights = [3, 2, 1]
values = [8, 5, 3]

print(knapsack_top_down(weights, values, capacity=4))  # 11
```

## State Explanation

The state is:

```text
(index, remaining_capacity)
```

Why is this enough?

At any point, the future result depends only on:

* Which item we are considering
* How much capacity remains

It does not matter exactly how we reached that state.

## Complexity

Let:

* `n` = number of items
* `C` = capacity

There are at most `n × C` distinct states.

* Time: `O(n × C)`
* Space: `O(n × C)`

---

# Part 16: Bottom-Up 0/1 Knapsack

```python
from typing import List


def knapsack_bottom_up(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> int:
    """
    Bottom-up solution for 0/1 knapsack.
    """

    if len(weights) != len(values):
        raise ValueError("weights and values must have equal length")

    item_count = len(weights)

    # dp[i][c] means:
    # Maximum value using the first i items
    # with a bag capacity of c.
    dp = [
        [0] * (capacity + 1)
        for _ in range(item_count + 1)
    ]

    # Row 0 is already 0:
    # With zero items, the maximum value is zero.
    #
    # Column 0 is already 0:
    # With zero capacity, no item can be selected.

    for item_number in range(1, item_count + 1):
        # Arrays are zero-indexed, but DP rows start at 1.
        # Therefore, the actual array index is item_number - 1.
        item_index = item_number - 1

        current_weight = weights[item_index]
        current_value = values[item_index]

        for current_capacity in range(capacity + 1):
            # Option 1: Do not take this item.
            dp[item_number][current_capacity] = (
                dp[item_number - 1][current_capacity]
            )

            # Option 2: Take this item, if it fits.
            if current_weight <= current_capacity:
                value_if_taken = current_value + dp[
                    item_number - 1
                ][current_capacity - current_weight]

                dp[item_number][current_capacity] = max(
                    dp[item_number][current_capacity],
                    value_if_taken,
                )

    return dp[item_count][capacity]


weights = [3, 2, 1]
values = [8, 5, 3]

print(knapsack_bottom_up(weights, values, capacity=4))  # 11
```

## Tricky Index Detail

The DP table contains an extra row:

```text
Row 0 = no items
Row 1 = first item
Row 2 = first two items
```

But Python arrays start at index `0`.

Therefore:

```python
item_index = item_number - 1
```

This is a common off-by-one source of bugs.

---

# Part 17: One-Dimensional Knapsack Optimization

The two-dimensional table can be optimized to `O(C)` space.

```python
from typing import List


def knapsack_space_optimized(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> int:
    """
    Space-optimized 0/1 knapsack.
    """

    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        # Critical tricky part:
        # Iterate backward for 0/1 knapsack.
        #
        # Going backward ensures the current item is not reused
        # multiple times during the same iteration.
        for current_capacity in range(
            capacity,
            weight - 1,
            -1,
        ):
            dp[current_capacity] = max(
                dp[current_capacity],
                value + dp[current_capacity - weight],
            )

    return dp[capacity]


print(
    knapsack_space_optimized(
        weights=[3, 2, 1],
        values=[8, 5, 3],
        capacity=4,
    )
)
```

## Why Iterate Backward?

Suppose an item has:

```text
weight = 2
value = 5
```

If you move forward:

```text
dp[2] becomes 5
dp[4] may then use the newly updated dp[2]
```

That would use the same item twice.

Backward iteration ensures every item is used at most once.

This is one of the most important 0/1 knapsack interview details.

---

# Part 18: DP in AI and Backend Systems

Classic DP questions are often simplified interview exercises, but the thinking appears in real systems.

## Resource Allocation

Suppose you have a limited GPU budget and several jobs:

| Job               | GPU hours | Business value |
| ----------------- | --------: | -------------: |
| Fine-tuning job A |        10 |             30 |
| Evaluation job B  |         4 |             15 |
| Indexing job C    |         6 |             18 |

You need to select the most valuable combination within the available compute budget.

This resembles knapsack.

## Prompt Context Selection

An LLM has a limited context window.

You have candidate document chunks with:

* Token cost
* Relevance score

You want the highest-value combination that fits into the token budget.

This can resemble knapsack, although production systems often use faster heuristics because the exact DP solution may be too expensive.

## Scheduling

Jobs may have:

* Dependencies
* Costs
* Deadlines
* Priorities
* Resource constraints

Graphs model dependencies; optimization methods, including DP in certain formulations, help decide resource allocation or execution plans.

## Model Routing

Given:

* Request complexity
* Model cost
* Latency budget
* Quality requirements

A system may optimize which model or tool chain to use.

The production formulation may be more complex than classic DP, but the same state-and-transition reasoning is useful.

---

# Part 19: Common Mistakes

## Trees and Graphs

1. **Forgetting visited tracking in graphs**

   This can cause infinite loops or duplicate processing.

2. **Marking BFS nodes visited too late**

   Mark them when adding them to the queue.

3. **Assuming graph traversal order is always unique**

   Order depends on adjacency-list ordering.

4. **Confusing a binary tree with a BST**

   A binary tree does not guarantee sorted relationships.

5. **Using BFS for weighted shortest paths**

   Standard BFS guarantees shortest paths only when every edge has equal cost.

6. **Forgetting disconnected components**

   Starting from one node may not visit the entire graph.

```python
for node in graph:
    if node not in visited:
        dfs(graph, node, visited)
```

7. **Ignoring recursion depth**

   Recursive DFS may fail for extremely deep graphs in Python.

## Dynamic Programming

1. Starting to code without defining the state
2. Missing a base case
3. Using too much state
4. Writing an incorrect transition
5. Using current-row values when previous-row values are required
6. Iterating forward in space-optimized 0/1 knapsack
7. Confusing 0/1 knapsack with unbounded knapsack
8. Assuming every optimization problem requires DP

---

# Part 20: Interview Pattern-Recognition Cheat Sheet

## Use Tree Traversal When

* The input has parent-child relationships
* You need subtree calculations
* You need sorted BST output
* You must process children before a parent
* You must process a parent before children

## Use Graph DFS When

* You need to explore connected components
* You need cycle detection
* You need to determine whether a path exists
* The problem involves backtracking
* You need to recursively follow dependencies

## Use Graph BFS When

* You need the shortest unweighted path
* You need the minimum number of moves
* You need level-by-level processing
* You need the nearest matching node

## Use Topological Sort When

* Tasks have prerequisites
* Courses have prerequisite courses
* Packages have dependencies
* Pipeline stages must be ordered
* You must detect circular dependencies

## Consider DP When

* Choices repeat across positions
* The problem asks for maximum, minimum, or number of ways
* Brute force generates repeated states
* A larger answer can be formed from smaller answers

---

# Part 21: Interview Q&A

## 1. What is the main difference between a tree and a graph?

A tree is a special graph that is connected and has no cycles. A general graph may contain cycles, multiple paths, directed edges, or disconnected components.

---

## 2. When should you use BFS instead of DFS?

Use BFS when you need level-order processing or the shortest path in an unweighted graph. BFS explores nodes in increasing distance from the starting node.

---

## 3. Why does graph traversal need a visited set?

A graph can contain cycles or multiple paths to the same node. A visited set prevents infinite loops and repeated processing.

---

## 4. What are the time complexities of DFS and BFS?

Both run in:

```text
O(V + E)
```

where `V` is the number of vertices and `E` is the number of edges.

---

## 5. Which tree traversal returns sorted values from a BST?

In-order traversal:

```text
Left → Node → Right
```

It returns BST values in ascending order, assuming the BST ordering rules are valid.

---

## 6. What is a DAG, and where is it used?

A DAG is a directed acyclic graph. It is used for dependency ordering, data pipelines, workflow engines, build systems, job schedulers, Airflow pipelines, and many LangGraph workflow designs.

---

## 7. How can you detect a cycle using topological sorting?

Run topological sort. If fewer than `V` nodes are processed, some nodes still have unresolved dependencies, indicating a cycle.

---

## 8. What is dynamic programming?

Dynamic programming solves problems by breaking them into overlapping subproblems, storing their answers, and reusing those answers instead of recomputing them.

---

## 9. What is the difference between memoization and tabulation?

Memoization is top-down and normally recursive. It calculates states as needed and caches them.

Tabulation is bottom-up and iterative. It starts from base states and fills a table until reaching the final answer.

---

## 10. Why does space-optimized 0/1 knapsack iterate backward?

Backward iteration prevents the current item from being used more than once. Forward iteration could reuse an updated state from the same item, incorrectly converting the solution into an unbounded-knapsack behavior.

---

# Part 22: Week 1 Review Checklist

## Day 1: Python Core and Environment

You should remember:

* Variables are references to objects.
* Mutable objects can change after creation; immutable objects cannot.
* Lists are mutable; tuples and strings are immutable.
* Dictionaries provide average `O(1)` lookup.
* Sets are useful for membership testing and duplicate removal.
* Functions create reusable units of behavior.
* Exceptions should be handled deliberately, not silently ignored.
* Virtual environments isolate project dependencies.
* Dependency versions should be pinned for reproducibility.
* Generators yield values lazily and can reduce memory usage.

### Core interview check

Can you explain:

```text
list vs tuple
set vs dictionary
shallow copy vs deep copy
iterator vs generator
*args vs **kwargs
mutable default argument problem
```

---

## Day 2: Object-Oriented Programming

You should remember:

* **Encapsulation:** Keep related state and behavior together.
* **Abstraction:** Expose what a component does, hiding unnecessary details.
* **Inheritance:** Extend or reuse behavior carefully.
* **Polymorphism:** Different implementations share a common interface.
* Prefer composition when components should be replaceable.
* Use abstract interfaces for LLM, embedding, storage, and vector database providers.
* Dependency injection improves testing.
* Classes should have clear responsibilities.
* Avoid overly large “God classes.”

### AI-system connection

A common abstraction is:

```python
class ModelProvider:
    def generate(self, prompt: str) -> str:
        ...
```

Implementations might include:

```text
OpenAIProvider
WatsonxProvider
LocalModelProvider
```

The rest of the application depends on the interface rather than a specific provider.

---

## Day 3: Advanced Python, Typing, Validation and Testing

You should remember:

* Type hints improve readability, IDE support, and refactoring.
* Static type checkers catch some errors before runtime.
* `Optional[T]` means a value may be `T` or `None`.
* `Union[A, B]` means either type is accepted.
* `TypedDict` describes dictionary structure.
* Runtime validation is still required at API boundaries.
* Use specific exception types.
* Unit tests verify small components.
* Integration tests verify components working together.
* Mock external systems, but do not over-mock internal logic.
* Test normal cases, edge cases, and failures.

### Core testing structure

```text
Arrange → Act → Assert
```

---

## Day 4: Async and Concurrency

You should remember:

* Concurrency means multiple tasks make progress during overlapping time.
* `asyncio` is most helpful for I/O-bound work.
* `async def` defines a coroutine.
* `await` pauses one coroutine without blocking the entire event loop.
* Blocking code inside async functions blocks the event loop.
* `asyncio.gather()` can run independent async operations concurrently.
* Use semaphores to limit concurrency.
* Use timeouts, retries, and cancellation carefully.
* Threads are useful for certain blocking I/O workloads.
* Multiprocessing is more appropriate for CPU-bound Python work.

### GenAI connection

Good async candidates:

```text
Parallel LLM calls
Vector database lookup
Database query
Tool invocation
Remote API request
```

---

## Day 5: Arrays, Strings, Hashing and Prefix Sums

You should remember:

* Array traversal is commonly `O(n)`.
* Hash maps support frequency counting and fast lookups.
* Sets support duplicate detection.
* Prefix sums answer range-sum queries efficiently.
* Strings are immutable in Python.
* Avoid repeatedly concatenating strings in large loops.
* Define index ranges carefully.
* Decide whether boundaries are inclusive or exclusive.

### Pattern signals

```text
Frequency/count      → hash map
Seen before?         → set
Contiguous range sum → prefix sum
Pair lookup          → hash map
```

---

## Day 6: Two Pointers, Sliding Window, Stack and Queue

You should remember:

### Two pointers

Use when:

* The input is sorted
* You are comparing elements from opposite ends
* You need pairs or triplets
* You want to remove duplicates in place

```text
left →             ← right
```

### Sliding window

Use for contiguous subarrays or substrings.

Fixed window:

```text
Maximum sum of exactly k elements
```

Variable window:

```text
Longest substring satisfying a condition
```

Important invariant:

```text
Expand right
Update state
Shrink left while invalid
Record answer
```

### Stack

Last In, First Out.

Use for:

* Parentheses validation
* Undo behavior
* Expression evaluation
* Monotonic-stack problems
* DFS

### Queue

First In, First Out.

Use for:

* BFS
* Scheduling
* Task processing
* Producer-consumer workflows

---

# Final Week 1 Memory Map

```text
Python foundations
        ↓
Write reliable functions and data structures
        ↓
OOP and abstractions
        ↓
Design maintainable AI components
        ↓
Typing, validation and testing
        ↓
Make components safer
        ↓
Async and concurrency
        ↓
Handle multiple external AI calls efficiently
        ↓
Core DSA patterns
        ↓
Process data and reason about efficiency
        ↓
Trees, graphs and DP
        ↓
Model workflows, dependencies and optimization
```

## Final Self-Test

By the end of Week 1, you should be able to explain:

* How Python stores and passes objects
* How to design a provider abstraction
* How type hints differ from runtime validation
* When asynchronous programming improves an AI service
* When to use a hash map, two pointers, or sliding window
* Why DFS uses recursion or a stack
* Why BFS uses a queue
* How DAGs represent pipeline dependencies
* How to detect a circular dependency
* How memoization avoids repeated work
* How to define the state and transition for a basic DP problem
* Why 0/1 knapsack iterates backward when using one-dimensional DP
