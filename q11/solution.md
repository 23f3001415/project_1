# Q11 - Network Game: The Signal

## What you finally submit

You do **not** submit code or explanation text in the grader.

You submit **only the completion JWT token** returned by the game after a successful solve.

For my run for `23f3001415@ds.study.iitm.ac.in`, the valid solve used:

- PIN: `2021`
- frequency: `104.2`
- Fragment 1: `BGYJ`
- Fragment 2: `TZXP`
- Fragment 3: `WH76`
- final passcode: `BGYJTZXPWH76`

## ELI15 idea

Think of this like a locked building puzzle game:

1. walk through the facility
2. pick up the useful objects
3. solve a number lock
4. solve a radio-frequency clue
5. feed the two fragments into the verification terminal
6. join all 3 fragments together
7. enter the final 12-character passcode
8. copy the JWT token

That JWT token is the only thing the grader wants.

## Step-by-step for a complete novice

### Step 1: Open the game

Go to:

```text
https://tds-network-games.sanand.workers.dev/signal/
```

Enter your email and press **Start**.

### Step 2: Collect the important items

Pick up these items while exploring:

- `MAINTENANCE_KEY`
- `FACILITY_MAP`
- `INSPECTION_CERTIFICATE`
- `NOTEBOOK`
- `ACCESS_CARD`
- `UV_TORCH`
- `SYSTEM_BADGE`
- `TORN_MANUAL`
- `SPECIMEN_KEY`
- `FREQUENCY_TUNER`
- `CLEANING_CLOTH`
- `SOLVENT_BOTTLE`
- `POWER_CELL`
- `BACKUP_LOG`
- `SIGNAL_LOG`

You can also pick up the extra items you see. They do not hurt.

### Step 3: Solve the PIN terminal

Read these two items:

- `INSPECTION_CERTIFICATE`
- `NOTEBOOK`

From this run:

- inspection year = `2016`
- sublevel = `5`

The notebook says the PIN is:

```text
inspection year + sublevel
```

So:

```text
2016 + 5 = 2021
```

Go to `SERVER_ROOM_A` and enter:

```text
2021
```

That reveals Fragment 1:

```text
BGYJ
```

### Step 4: Craft the two useful tools

Combine:

```text
CLEANING_CLOTH + SOLVENT_BOTTLE = DEMAGNETISER
```

Then combine:

```text
ACCESS_CARD + DEMAGNETISER = REPAIRED_ACCESS_CARD
```

And combine:

```text
FREQUENCY_TUNER + POWER_CELL = POWERED_TUNER
```

### Step 5: Solve the radio-frequency puzzle

Read:

- `BACKUP_LOG`
- `SIGNAL_LOG`

Find the frequency that appears in **both** lists.

For this run, the common value was:

```text
104.2
```

Go to `MAINTENANCE_BAY` and use the transmitter with:

```text
104.2
```

That reveals Fragment 2:

```text
TZXP
```

### Step 6: Solve the verification terminal

Go to `CONTROL_ROOM`.

Use `TERMINAL_3` with the two fragments in the same order they were revealed:

```text
BGYJ,TZXP
```

That reveals Fragment 3:

```text
WH76
```

### Step 7: Unlock the final room

Because you already made `REPAIRED_ACCESS_CARD`, you can move from `CONTROL_ROOM` to `CORE_CHAMBER`.

### Step 8: Build the final passcode

The game hint says to concatenate the three fragments in reveal order:

```text
Fragment1 + Fragment2 + Fragment3
```

So the final passcode is:

```text
BGYJTZXPWH76
```

### Step 9: Enter the passcode

In `CORE_CHAMBER`, use `EXIT_KEYPAD` with:

```text
BGYJTZXPWH76
```

The game returns a **completion JWT token**.

That token is your submission.

## If you want to automate it

This folder includes:

```text
solve_signal.py
```

Run it with:

```powershell
python solve_signal.py
```

It will:

1. start or continue your session
2. collect the required items
3. compute the PIN
4. compute the frequency
5. solve Terminal 3
6. build the final passcode
7. print the completion JWT token

## Final submission format

Paste the JWT exactly as returned by the game.

Do not add:

- quotes
- backticks
- labels
- spaces
- extra lines
