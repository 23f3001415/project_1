# Q3 - Get a Small Open-Source PR Merged

## What you must finally submit

You will **not** submit this tutorial text in the grader.

You must submit **one public GitHub pull request URL** that is:

1. In a repository with **1000+ stars**
2. **Merged**
3. Authored with commit email `23f3001415@ds.study.iitm.ac.in`
4. Merged **after 2026-02-10 UTC**

Your final answer in the portal should look like this:

```text
https://github.com/OWNER/REPO/pull/12345
```

Until your PR is actually merged, there is **no valid final answer** for this question.

## ELI15 idea

Think of open source like helping fix a label in a big public library.

- Do **not** walk in and rearrange the whole building.
- Find one small thing that is clearly wrong.
- Fix only that one thing.
- Leave a short note saying what you changed.
- Make the librarian's job easier, not harder.

That is exactly how you should do this question.

## Why maintainers are overloaded by AI PRs

Many maintainers are receiving low-effort AI-generated pull requests that:

- fix things nobody asked to fix
- ignore contribution rules
- include unrelated edits
- contain confident but wrong explanations
- make reviewers spend time checking bad work

Practical harm:

- reviewer time gets wasted
- real contributors wait longer
- maintainers must clean up noisy PRs
- trust drops when PRs look automated and careless

Rule: send **one careful PR**, not many random PRs.

## How to choose the right PR

Pick a repository that has:

1. More than 1000 stars
2. Recent commits in the last few weeks
3. A `CONTRIBUTING.md` or clear PR instructions
4. Small documentation or typo issues
5. Friendly labels like `good first issue`, `documentation`, `typo`, `docs`

Best first PR types:

- typo fix
- broken link fix
- tiny docs clarification
- tiny test fix
- very small bug fix with obvious cause

Avoid for this exam:

- feature requests
- refactors
- style-only mass formatting
- AI-generated "improvements" with no issue
- touching many files

## Safest strategy for a beginner

Use this order:

1. Find an active repo with 1000+ stars
2. Read `README` and `CONTRIBUTING.md`
3. Look for a tiny open issue, or a clearly broken doc/link
4. Make one focused change
5. Test or preview if possible
6. Open one polite PR
7. Wait and respond quickly if asked

## Step-by-step for a complete novice

### Step 1: Set your Git identity correctly

This matters because the grader checks your commit email.

Run these commands in PowerShell:

```powershell
git config --global user.name "Your Name"
git config --global user.email "23f3001415@ds.study.iitm.ac.in"
```

Check it:

```powershell
git config --global user.name
git config --global user.email
```

### Step 2: Find a good target repository

Search GitHub using filters like:

```text
is:issue is:open label:"good first issue" label:documentation
```

Or:

```text
is:issue is:open label:typo
```

Then open the repository page and verify:

- stars are above 1000
- recent commits exist
- contribution guidelines exist

### Step 3: Read the repo rules before touching anything

Open and read:

- `README.md`
- `CONTRIBUTING.md`
- pull request template if present
- issue template if present

If the repo says "ask before working on an issue", do that.

### Step 4: Choose the tiniest useful fix

Good examples:

- a broken documentation link
- a spelling mistake in setup steps
- wrong command in docs
- tiny test typo

Bad examples:

- "improve performance"
- "clean up code"
- "modernize docs"
- changing ten files at once

### Step 5: Fork the repository

On GitHub:

1. Open the repository
2. Click `Fork`
3. Keep it public

Then clone your fork:

```powershell
git clone https://github.com/YOUR_GITHUB_USERNAME/REPO_NAME.git
cd REPO_NAME
```

Add the original repo as upstream:

```powershell
git remote add upstream https://github.com/ORIGINAL_OWNER/REPO_NAME.git
git remote -v
```

### Step 6: Create a branch

```powershell
git checkout -b docs/fix-broken-link
```

Use a branch name that says exactly what you changed.

### Step 7: Make only one small change

Edit only what is needed.

Before committing, inspect the diff:

```powershell
git diff
```

If you see unrelated changes, remove them before continuing.

### Step 8: Test or verify the change

For docs:

- click the fixed link if possible
- preview markdown if possible
- check spelling and formatting

For code:

- run only the smallest relevant test
- do not open a PR with untested code if the repo expects testing

### Step 9: Commit with a clear message

```powershell
git add .
git commit -m "docs: fix broken setup link"
```

Verify the author email on the latest commit:

```powershell
git log -1 --format="%an <%ae>"
```

It must show:

```text
23f3001415@ds.study.iitm.ac.in
```

### Step 10: Push your branch

```powershell
git push -u origin docs/fix-broken-link
```

### Step 11: Open the pull request

Use a very small PR title, for example:

```text
docs: fix broken setup link
```

Use a short PR body like this:

```markdown
## Summary

Fixes one broken link in the setup documentation.

## Verification

- opened the updated link and confirmed it resolves correctly

## AI usage

I used AI only to help draft wording. I verified the final change and am responsible for it.
```

Why this AI disclosure is good:

- honest
- short
- does not create extra work
- makes it clear you checked the change yourself

## How to disclose AI help properly

Good disclosure:

- say AI helped with drafting if true
- keep it one or two lines
- state that you verified the result yourself

Bad disclosure:

- pasting a long AI conversation
- saying "AI generated this, please review"
- making maintainers figure out whether anything is correct

## What to do after opening the PR

### If maintainers respond with changes

Do this:

1. thank them briefly
2. make exactly the requested change
3. reply clearly

Example:

```text
Thanks. I updated the link text and removed the extra wording.
```

### If maintainers do not respond

Wait patiently.

Reasonable follow-up:

- wait about 7 to 14 days
- send one short polite comment

Example:

```text
Friendly follow-up in case this is useful. Happy to make changes if needed.
```

Do **not** spam comments.

### If maintainers close the PR

That is normal in open source.

Do this:

1. read the reason
2. learn from it
3. pick another tiny issue in another repo
4. do not argue

For this assignment, only a **merged** PR counts.

## Smart checklist before you open the PR

- repo has 1000+ stars
- repo is public
- contribution rules were read
- change is tiny and useful
- no unrelated edits
- commit email is `23f3001415@ds.study.iitm.ac.in`
- PR is polite and short
- AI disclosure is honest and minimal

## Smart checklist before you submit in the grader

- PR is public
- PR is merged
- merge date is after 2026-02-10 UTC
- commit author email matches `23f3001415@ds.study.iitm.ac.in`
- repository still has 1000+ stars

## Final answer template

When your PR is merged, submit only this:

```text
https://github.com/OWNER/REPO/pull/NUMBER
```

## Important reality check

This question cannot be fully "finished" by writing a Markdown file alone.

The real completion event is:

- you open one good PR
- a maintainer merges it

Everything before that is preparation.
