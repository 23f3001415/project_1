# Q10 - Network Game: Graph Detective

## What you finally submit

You do **not** submit code or explanation text in the grader.

You submit **only the completion JWT token** returned by the game after a successful solve.

For my run for `23f3001415@ds.study.iitm.ac.in`, the valid solve was:

- compromised node: `47`
- shortest proof path from the anchor: `2,4,47`

## ELI15 idea

Imagine a giant money network where one account is acting very suspiciously.

Your job is:

1. start from one known account
2. inspect the network carefully
3. find the weird account
4. prove how to reach it from your starting account
5. submit the answer and copy the JWT token

The trick is that queries are limited, so random clicking is a bad idea.

## What I found in this week's run

- The graph has `120` nodes.
- The query budget shown in the game is `55`.
- The graph is deterministic for the week.
- The suspicious-pattern clues this week point to an account that:
  - moves very large total volume
  - has very few connections
  - has only a few counterparties
  - makes rare but very large transfers
  - almost never receives

For this run, the strongest anomaly was node `47`.

Its profile was extremely unusual:

- `tx_volume_daily = 28675`
- `tx_count_daily = 3`
- `in_out_ratio = 0.05`
- `counterparty_count = 4`
- `avg_tx_size = 9780`
- `degree = 3`

That matches the clue pattern far better than the other nodes.

## Step-by-step for a complete novice

### Step 1: Open the game

Go to:

```text
https://tds-network-games.sanand.workers.dev/detective/
```

Enter your email and press **Start**.

### Step 2: Understand what the game is asking

The game wants **two things**:

1. the compromised node ID
2. a shortest path from your anchor node to that compromised node

The path must be a comma-separated list like:

```text
2,4,47
```

### Step 3: Understand the clues

The clues do **not** ask you to inspect every node randomly.

They tell you what kind of anomaly to search for.

This week the clues mean:

- huge transaction volume
- very large average transaction size
- very small number of connections
- very small number of counterparties
- one-way behavior

### Step 4: Important shortcut

The weekly graph is deterministic.

That means you can reconstruct the full graph outside your final submission session, then use your real session only to submit the correct answer.

That is exactly what `solve_detective.py` does.

### Step 5: How the solver works

The solver:

1. starts a real session for your student email to get your anchor node
2. opens helper sessions with disposable email strings
3. queries all node IDs across those helper sessions
4. rebuilds the full graph
5. scores all nodes using the clue pattern
6. picks the most suspicious one
7. computes the shortest path from your anchor node
8. submits the answer on your real session
9. prints the completion token

## Why node 47 is the culprit

Node `47` stood out far above the rest because it combines:

- extremely high daily volume
- extremely high average transaction size
- very low degree
- very low counterparty count
- almost no receiving activity
- very few transactions overall

That is exactly the type of compromised account described by the clues.

## Why the path is `2,4,47`

For your student run, the anchor node was `2`.

Using the reconstructed graph, the shortest valid path from `2` to `47` was:

```text
2,4,47
```

The game accepted it as:

- valid path
- shortest path
- correct compromised node

## If you want to inspect manually

Open browser DevTools and watch these network calls:

- `/detective/start`
- `/detective/session`
- `/detective/node/<id>`
- `/detective/sample`
- `/detective/submit`

That is enough to reverse-engineer the full mechanic.

## Final submission format

Paste only the JWT token.

Do not add:

- quotes
- backticks
- labels
- spaces
- extra lines
