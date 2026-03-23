# Q9 - Network Game: Data Labyrinth

## What you finally submit

You do **not** submit code or explanation text in the grader.

You submit **only the completion JWT token** returned by the game after a successful solve.

For my run for `23f3001415@ds.study.iitm.ac.in`, the game returned a valid token for:

- `game = labyrinth`
- `week_id = 2026-W13`
- `completed_at = 2026-03-23T15:11:41.949Z`

## ELI15 idea

Think of this like a maze treasure hunt:

1. Start the game with your email.
2. Walk through every room without getting lost.
3. Pick up every data packet you find.
4. Keep only the packets that actually belong to your question.
5. Solve the final maths question from those useful packets.
6. Go to the final room.
7. Submit the answer and copy the JWT token.

That JWT token is the only thing the grader wants.

## What I found in this week's run

- The maze is an `11 x 11` grid with room IDs `0` to `120`.
- Room IDs are row-major:
  - moving `north` means `room_id - 11`
  - moving `south` means `room_id + 11`
  - moving `west` means `room_id - 1`
  - moving `east` means `room_id + 1`
- Exit room is `120`.
- The current question for this run was:

```text
Compute the weighted mean of queue_depth using response_ms as weights. Exclude any incomplete records.
```

- Useful fragments had `type = "required"`.
- Wrong packets had `type = "distractor"`.
- Incomplete or damaged values showed up as:
  - `quality = "degraded"`
  - or field values like `"CORRUPT"`

## Step-by-step for a complete novice

### Step 1: Open the game

Go to:

```text
https://tds-network-games.sanand.workers.dev/labyrinth/
```

Enter your email and press **Start**.

### Step 2: Understand the buttons

- `W A S D` or arrow keys move you
- `C` collects the item in the room
- `Look` refreshes the current room
- `Inventory` shows collected fragments

### Step 3: Notice the important rules

- Not every packet is useful
- Some are distractors
- Some values are broken or incomplete
- You only answer the final question after reaching room `120`

### Step 4: Do not solve by random walking

Random walking wastes moves and makes you lose track.

A better method is:

1. map each room ID
2. note all exits
3. collect every packet once
4. compute the answer from inventory data

### Step 5: Use the solver

In this folder there is a script:

```powershell
python solve_labyrinth.py
```

What it does:

1. starts or restores your session
2. explores the full maze with DFS
3. collects items in every room
4. stores the discovered map locally in `labyrinth_state.json`
5. filters inventory into useful vs distractor records
6. ignores incomplete records
7. computes the weighted mean
8. walks to room `120`
9. submits the answer
10. prints the completion token

## How the final maths was done

The question asked for a **weighted mean**.

That means:

```text
weighted mean = sum(queue_depth * response_ms) / sum(response_ms)
```

But only for records that are:

- `type = required`
- not incomplete
- not corrupted

For this run:

- total collected packets = `46`
- useful packets = `12`
- complete useful packets used in the formula = `9`
- computed answer = `7.2208987547`

## Why this works

Because the game gives all the data you need through:

- room look responses
- move responses
- collect responses
- inventory responses

So you do **not** need to guess the answer.
You only need to:

1. gather all useful rows
2. filter bad rows out
3. calculate correctly
4. submit in the exit room

## If something goes wrong

### If the token expires

Run the solver again. The game checks recency, so a fresh token is fine.

### If the week changes

Run the solver again after the new week starts, because:

- maze data can change
- question can change
- required answer can change
- old token will fail `week_id`

### If you want to inspect manually

Open browser DevTools:

1. go to the **Network** tab
2. start the game
3. watch calls to:
   - `/labyrinth/start`
   - `/labyrinth/look`
   - `/labyrinth/move`
   - `/labyrinth/collect`
   - `/labyrinth/inventory`
   - `/labyrinth/submit`

That is enough to reverse-engineer the whole game.

## Final submission format

Paste the JWT exactly as returned by the game.

Example shape:

```text
eyJ...<many characters>...abc
```

Do not add:

- quotes
- markdown
- labels
- spaces
- extra lines
