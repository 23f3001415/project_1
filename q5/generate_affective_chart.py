from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "affective-chart.png"

W = 1600
H = 2000

BG_TOP = (21, 17, 13)
BG_BOTTOM = (233, 223, 205)
SHADOW = (37, 28, 22, 235)
HUMAN = (133, 74, 52, 238)
LIVESTOCK = (76, 47, 34, 238)
WILD = (172, 214, 200, 255)
WILD_GLOW = (222, 250, 241, 255)
BEAM = (243, 237, 224, 120)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient_background():
    img = Image.new("RGBA", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        r = lerp(BG_TOP[0], BG_BOTTOM[0], t)
        g = lerp(BG_TOP[1], BG_BOTTOM[1], t)
        b = lerp(BG_TOP[2], BG_BOTTOM[2], t)
        for x in range(W):
            px[x, y] = (r, g, b, 255)
    return img


def add_noise(base, seed=1415):
    rnd = random.Random(seed)
    noise = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(noise)
    for _ in range(14000):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        alpha = rnd.randint(5, 18)
        val = rnd.randint(180, 255)
        draw.point((x, y), fill=(val, val - rnd.randint(5, 20), val - rnd.randint(10, 30), alpha))
    noise = noise.filter(ImageFilter.GaussianBlur(0.35))
    return Image.alpha_composite(base, noise)


def add_beam(base):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    poly = [
        (0, int(H * 0.70)),
        (int(W * 0.72), int(H * 0.57)),
        (int(W * 0.80), H),
        (0, H),
    ]
    draw.polygon(poly, fill=BEAM)
    overlay = overlay.filter(ImageFilter.GaussianBlur(35))
    return Image.alpha_composite(base, overlay)


def ellipse_box(x, y, w, h):
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def draw_human(draw, x, y, s, color):
    head_r = s * 0.12
    draw.ellipse(ellipse_box(x, y - s * 0.33, head_r * 2, head_r * 2), fill=color)
    draw.rounded_rectangle((x - s * 0.10, y - s * 0.18, x + s * 0.10, y + s * 0.20), radius=s * 0.06, fill=color)
    draw.polygon([(x - s * 0.12, y - s * 0.10), (x - s * 0.26, y + s * 0.12), (x - s * 0.18, y + s * 0.16), (x - s * 0.05, y - s * 0.02)], fill=color)
    draw.polygon([(x + s * 0.12, y - s * 0.10), (x + s * 0.26, y + s * 0.12), (x + s * 0.18, y + s * 0.16), (x + s * 0.05, y - s * 0.02)], fill=color)
    draw.polygon([(x - s * 0.08, y + s * 0.20), (x - s * 0.18, y + s * 0.48), (x - s * 0.05, y + s * 0.50), (x + s * 0.01, y + s * 0.25)], fill=color)
    draw.polygon([(x + s * 0.08, y + s * 0.20), (x + s * 0.18, y + s * 0.48), (x + s * 0.05, y + s * 0.50), (x - s * 0.01, y + s * 0.25)], fill=color)


def draw_cow(draw, x, y, s, color):
    draw.rounded_rectangle((x - s * 0.34, y - s * 0.18, x + s * 0.22, y + s * 0.12), radius=s * 0.08, fill=color)
    draw.rounded_rectangle((x + s * 0.18, y - s * 0.12, x + s * 0.38, y + s * 0.02), radius=s * 0.05, fill=color)
    draw.polygon([(x + s * 0.30, y - s * 0.12), (x + s * 0.39, y - s * 0.17), (x + s * 0.35, y - s * 0.08)], fill=color)
    draw.polygon([(x + s * 0.24, y - s * 0.12), (x + s * 0.17, y - s * 0.18), (x + s * 0.21, y - s * 0.08)], fill=color)
    for leg in (-0.22, -0.05, 0.08, 0.21):
        draw.rectangle((x + s * leg, y + s * 0.08, x + s * (leg + 0.05), y + s * 0.42), fill=color)
    draw.line((x - s * 0.33, y - s * 0.10, x - s * 0.47, y - s * 0.24), fill=color, width=max(1, int(s * 0.03)))


def draw_pig(draw, x, y, s, color):
    draw.ellipse((x - s * 0.34, y - s * 0.18, x + s * 0.24, y + s * 0.20), fill=color)
    draw.ellipse((x + s * 0.14, y - s * 0.10, x + s * 0.38, y + s * 0.10), fill=color)
    draw.polygon([(x + s * 0.15, y - s * 0.08), (x + s * 0.06, y - s * 0.22), (x + s * 0.22, y - s * 0.12)], fill=color)
    draw.polygon([(x + s * 0.28, y - s * 0.08), (x + s * 0.22, y - s * 0.22), (x + s * 0.33, y - s * 0.11)], fill=color)
    for leg in (-0.20, -0.02, 0.12, 0.22):
        draw.rectangle((x + s * leg, y + s * 0.10, x + s * (leg + 0.04), y + s * 0.42), fill=color)
    draw.arc((x - s * 0.40, y - s * 0.05, x - s * 0.24, y + s * 0.11), start=20, end=340, fill=color, width=max(1, int(s * 0.04)))


def draw_sheep(draw, x, y, s, color):
    for ox, oy, r in [(-0.20, -0.02, 0.15), (-0.04, -0.08, 0.16), (0.14, -0.02, 0.15), (0.00, 0.04, 0.17)]:
        draw.ellipse((x + s * (ox - r), y + s * (oy - r), x + s * (ox + r), y + s * (oy + r)), fill=color)
    draw.ellipse((x + s * 0.18, y - s * 0.08, x + s * 0.38, y + s * 0.10), fill=color)
    for leg in (-0.14, -0.02, 0.10, 0.20):
        draw.rectangle((x + s * leg, y + s * 0.10, x + s * (leg + 0.035), y + s * 0.42), fill=color)


def draw_horse(draw, x, y, s, color):
    draw.rounded_rectangle((x - s * 0.30, y - s * 0.18, x + s * 0.16, y + s * 0.10), radius=s * 0.08, fill=color)
    draw.polygon([(x + s * 0.10, y - s * 0.14), (x + s * 0.26, y - s * 0.24), (x + s * 0.30, y - s * 0.02), (x + s * 0.18, y + s * 0.02)], fill=color)
    draw.ellipse((x + s * 0.22, y - s * 0.22, x + s * 0.38, y - s * 0.08), fill=color)
    for leg in (-0.18, -0.03, 0.09, 0.18):
        draw.rectangle((x + s * leg, y + s * 0.08, x + s * (leg + 0.04), y + s * 0.45), fill=color)
    draw.polygon([(x - s * 0.28, y - s * 0.12), (x - s * 0.42, y - s * 0.28), (x - s * 0.33, y - s * 0.04)], fill=color)


def draw_elephant(draw, x, y, s, color):
    draw.rounded_rectangle((x - s * 0.34, y - s * 0.18, x + s * 0.18, y + s * 0.14), radius=s * 0.10, fill=color)
    draw.ellipse((x + s * 0.06, y - s * 0.18, x + s * 0.28, y + s * 0.08), fill=color)
    draw.ellipse((x - s * 0.02, y - s * 0.10, x + s * 0.16, y + s * 0.08), fill=(color[0], color[1], color[2], int(color[3] * 0.92)))
    draw.rounded_rectangle((x + s * 0.18, y - s * 0.02, x + s * 0.28, y + s * 0.30), radius=s * 0.05, fill=color)
    for leg in (-0.22, -0.05, 0.08, 0.20):
        draw.rectangle((x + s * leg, y + s * 0.08, x + s * (leg + 0.06), y + s * 0.44), fill=color)


def draw_deer(draw, x, y, s, color):
    draw.rounded_rectangle((x - s * 0.26, y - s * 0.14, x + s * 0.12, y + s * 0.08), radius=s * 0.07, fill=color)
    draw.polygon([(x + s * 0.08, y - s * 0.12), (x + s * 0.24, y - s * 0.22), (x + s * 0.26, y - s * 0.04), (x + s * 0.16, y + s * 0.01)], fill=color)
    draw.ellipse((x + s * 0.20, y - s * 0.24, x + s * 0.32, y - s * 0.12), fill=color)
    draw.line((x + s * 0.27, y - s * 0.22, x + s * 0.34, y - s * 0.34), fill=color, width=max(1, int(s * 0.03)))
    draw.line((x + s * 0.27, y - s * 0.22, x + s * 0.39, y - s * 0.27), fill=color, width=max(1, int(s * 0.03)))
    draw.line((x + s * 0.24, y - s * 0.23, x + s * 0.18, y - s * 0.36), fill=color, width=max(1, int(s * 0.03)))
    draw.line((x + s * 0.24, y - s * 0.23, x + s * 0.13, y - s * 0.29), fill=color, width=max(1, int(s * 0.03)))
    for leg in (-0.18, -0.06, 0.00, 0.10):
        draw.rectangle((x + s * leg, y + s * 0.06, x + s * (leg + 0.03), y + s * 0.44), fill=color)


def draw_whale(draw, x, y, s, color):
    draw.polygon(
        [
            (x - s * 0.36, y + s * 0.02),
            (x - s * 0.10, y - s * 0.16),
            (x + s * 0.22, y - s * 0.10),
            (x + s * 0.34, y + s * 0.02),
            (x + s * 0.20, y + s * 0.10),
            (x - s * 0.06, y + s * 0.16),
        ],
        fill=color,
    )
    draw.polygon([(x - s * 0.34, y), (x - s * 0.48, y - s * 0.12), (x - s * 0.46, y + s * 0.12)], fill=color)
    draw.polygon([(x + s * 0.02, y - s * 0.04), (x + s * 0.10, y - s * 0.20), (x + s * 0.16, y - s * 0.02)], fill=color)


def draw_bat(draw, x, y, s, color):
    pts = [
        (x - s * 0.38, y + s * 0.02),
        (x - s * 0.22, y - s * 0.16),
        (x - s * 0.10, y - s * 0.02),
        (x, y - s * 0.18),
        (x + s * 0.10, y - s * 0.02),
        (x + s * 0.22, y - s * 0.16),
        (x + s * 0.38, y + s * 0.02),
        (x + s * 0.18, y + s * 0.00),
        (x + s * 0.06, y + s * 0.16),
        (x, y + s * 0.06),
        (x - s * 0.06, y + s * 0.16),
        (x - s * 0.18, y + s * 0.00),
    ]
    draw.polygon(pts, fill=color)


def draw_group(image, placements, kind, color, shadow_offset=(12, 16), blur=10):
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(main)

    for x, y, s in placements:
        func = kind
        func(sdraw, x + shadow_offset[0], y + shadow_offset[1], s, SHADOW)
        func(mdraw, x, y, s, color)

    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    image = Image.alpha_composite(image, shadow)
    image = Image.alpha_composite(image, main)
    return image


def jittered_grid(cols, rows, x0, x1, y0, y1, scale_base, seed):
    rnd = random.Random(seed)
    xs = [x0 + (x1 - x0) * (c + 0.5) / cols for c in range(cols)]
    ys = [y0 + (y1 - y0) * (r + 0.5) / rows for r in range(rows)]
    out = []
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            jx = rnd.uniform(-18, 18)
            jy = rnd.uniform(-14, 14)
            scale = scale_base * rnd.uniform(0.90, 1.10) * (1.05 + 0.12 * (y / H))
            out.append((x + jx, y + jy, scale))
    return out


def build_image():
    img = gradient_background()
    img = add_noise(img)
    img = add_beam(img)

    # A heavy visual block of 95% humans + livestock presses down from above.
    human_positions = jittered_grid(cols=6, rows=6, x0=120, x1=820, y0=170, y1=950, scale_base=106, seed=36)
    livestock_positions = jittered_grid(cols=8, rows=8, x0=630, x1=1540, y0=280, y1=1530, scale_base=118, seed=59)
    human_positions = human_positions[:36]
    livestock_positions = livestock_positions[:59]

    img = draw_group(img, human_positions, draw_human, HUMAN, shadow_offset=(8, 12), blur=9)

    livestock_kinds = [draw_cow, draw_pig, draw_sheep, draw_horse]
    for idx, kind in enumerate(livestock_kinds):
        subset = [p for i, p in enumerate(livestock_positions) if i % len(livestock_kinds) == idx]
        img = draw_group(img, subset, kind, LIVESTOCK, shadow_offset=(12, 16), blur=11)

    # A small illuminated refuge with only five wild mammals left in view.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((80, 1450, 780, 2120), fill=(202, 240, 225, 52))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img, glow)

    wild_positions = [
        (280, 1720, 150),
        (430, 1770, 140),
        (565, 1710, 156),
        (370, 1885, 136),
        (560, 1890, 122),
    ]
    wild_kinds = [draw_elephant, draw_deer, draw_whale, draw_bat, draw_deer]

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(main)
    for (x, y, s), kind in zip(wild_positions, wild_kinds):
        kind(sdraw, x + 10, y + 12, s, (17, 29, 27, 180))
        kind(mdraw, x, y, s, WILD)
        kind(mdraw, x, y - 10, s * 0.96, WILD_GLOW)
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    main = main.filter(ImageFilter.GaussianBlur(0.2))
    img = Image.alpha_composite(img, shadow)
    img = Image.alpha_composite(img, main)

    # Add a dark vignette for magazine-cover drama.
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for i in range(28):
        inset = i * 18
        alpha = int(6 + i * 3.5)
        vdraw.rounded_rectangle((inset, inset, W - inset, H - inset), radius=80, outline=(0, 0, 0, alpha), width=22)
    vignette = vignette.filter(ImageFilter.GaussianBlur(24))
    img = Image.alpha_composite(img, vignette)

    img = img.convert("RGB")
    img.save(OUT, quality=96)


if __name__ == "__main__":
    build_image()
