# Q5 - Image: The Affective Chart

## What you finally submit

You submit **two public URLs separated by one space**:

1. the public image URL
2. the public JSON URL

The image must be first.

## ELI15 idea

This question is asking you to do something harder than a normal chart:

- do not just show numbers
- make the viewer **feel** the numbers
- use a real dataset
- make the picture understandable even without axes or a legend

So the job is:

1. pick one real dataset with a strong insight
2. choose one single thing you want the viewer to feel
3. turn that into a visual metaphor
4. host the image and JSON publicly
5. submit the two URLs

## What I chose

Dataset:

- Our World in Data: global mammal biomass by group

Insight:

- humans and livestock make up `95%` of the world’s mammal biomass
- wild mammals are only `5%`

Why this works well:

- the fact is simple
- the feeling is immediate
- the image can work without labels

## How the image was designed

Instead of making a normal chart, I made:

- a dark upper mass of human and livestock silhouettes
- a tiny lit refuge containing only five wild mammal silhouettes

This makes the viewer feel:

- crowding
- domination
- disappearance

before they even know the exact source.

## Files in this folder

- `affective-chart.png` - final image
- `submission.json` - metadata file required by the assignment
- `generate_affective_chart.py` - script used to generate the image

## How to regenerate

Run:

```powershell
python q5\generate_affective_chart.py
```

## Final submission format

Submit:

```text
IMAGE_URL JSON_URL
```

with exactly one space between them.
