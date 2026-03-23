# Q6 - Image: The Concept Incarnation

## What you finally submit

You submit **two public URLs separated by one space**:

1. the image URL
2. the JSON URL

The image must come first.

## ELI15 idea

This question wants you to do something very specific:

- take an abstract ML idea
- turn it into a real physical scene
- avoid diagrams, labels, equations, and text
- make the scene recognizable to an expert from the image alone

So the workflow is:

1. choose one concept
2. find its deep structure
3. find a real-world scene with the same structure
4. generate the image
5. host the image and JSON publicly
6. submit the two URLs

## What I chose

Concept:

- `overfitting`

Core structure of overfitting:

- something becomes too perfectly tuned to one example
- it captures quirks and noise
- then it fails on normal new cases

Physical metaphor:

- a locksmith files one key so obsessively that it fits one damaged lock perfectly
- but that same key no longer works on normal locks

That is why this scene matches overfitting better than generic “AI brain” imagery.

## Files in this folder

- `concept-incarnation.png` - final image
- `submission.json` - required metadata file
- `generate_concept_incarnation.py` - script used to generate the image

## How to regenerate

Run:

```powershell
python q6\generate_concept_incarnation.py
```

## Final submission format

Submit:

```text
IMAGE_URL JSON_URL
```

with exactly one space between them.
