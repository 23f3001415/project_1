# Q7 - Image: The Style Transplant

## What you finally submit

You submit **two public URLs separated by one space**:

1. the image URL
2. the JSON URL

The image URL must come first.

## ELI15 idea

This question is asking you to do two things at once:

1. show a data-science concept
2. show it in a real historical visual tradition

So you should not think:

- "make it look old"

You should think:

- "what are the actual visual rules of one specific tradition?"

Then:

1. choose the concept
2. choose the tradition
3. identify the tradition's grammar
4. rebuild the concept using those rules
5. host the image and JSON publicly
6. submit the two URLs

## What I chose

Concept:

- `gradient descent`

Tradition:

- `Bauhaus graphic design`
- period: `1919-1933`

Why this pairing works:

- Bauhaus already uses geometry, movement, grids, circles, lines, and asymmetry
- gradient descent is also about a state moving through a structured space toward a minimum

So the concept and the tradition fit each other naturally.

## What visual grammar I targeted

I deliberately used:

- asymmetrical composition
- geometric sans-serif type
- black construction lines
- flat primary-color forms
- off-white paper
- circles, rectangles, and diagonal motion

That makes it read like Bauhaus instead of generic retro poster art.

## Files in this folder

- `style-transplant.png` - final image
- `submission.json` - required metadata file
- `generate_style_transplant.py` - script used to generate the image

## How to regenerate

Run:

```powershell
python q7\generate_style_transplant.py
```

## Final submission format

Submit:

```text
IMAGE_URL JSON_URL
```

with exactly one space between them.
