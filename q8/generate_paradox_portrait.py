from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "paradox-portrait.png"

W = 2000
H = 1300
PANEL_GAP = 60
PANEL_W = (W - PANEL_GAP) // 2


BG = (18, 22, 31, 255)
PANEL = (28, 34, 46, 255)
GLOW = (245, 229, 200, 120)
RED = (218, 88, 70, 255)
BLUE = (88, 128, 212, 255)
STONE = (220, 214, 202, 255)
STONE_DARK = (120, 128, 140, 255)
SHADOW = (0, 0, 0, 140)


def make_canvas():
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Subtle vertical gradient.
    for y in range(H):
        alpha = int(120 * (1 - y / H))
        draw.line((0, y, W, y), fill=(38, 46, 66, alpha), width=1)

    # Two gallery-like panels.
    left = (0, 0, PANEL_W, H)
    right = (PANEL_W + PANEL_GAP, 0, W, H)
    draw.rectangle(left, fill=PANEL)
    draw.rectangle(right, fill=PANEL)
    draw.rectangle((PANEL_W, 0, PANEL_W + PANEL_GAP, H), fill=(10, 12, 18, 255))
    return img


def add_atmosphere(base):
    rnd = random.Random(1415)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for _ in range(18000):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        val = rnd.randint(170, 240)
        alpha = rnd.randint(4, 18)
        draw.point((x, y), fill=(val, val, val, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(0.5))
    return Image.alpha_composite(base, layer)


def add_panel_light(base, box, center):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = center
    for r, alpha in [(360, 70), (520, 42), (700, 18)]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 240, 210, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(45))
    return Image.alpha_composite(base, layer)


def staircase_points(panel_x, start_y, step_w, step_h, steps):
    pts = [(panel_x + 70, H - 120), (panel_x + 70, start_y)]
    x = panel_x + 70
    y = start_y
    for _ in range(steps):
        pts.append((x + step_w, y))
        x += step_w
        pts.append((x, y - step_h))
        y -= step_h
    pts.extend([(x, H - 120), (panel_x + 70, H - 120)])
    return pts


def descending_path_points(panel_x, top_y, step_w, step_h, steps):
    pts = [(panel_x + 90, H - 120), (panel_x + 90, top_y)]
    x = panel_x + 90
    y = top_y
    for _ in range(steps):
        pts.append((x + step_w, y))
        x += step_w
        pts.append((x, y + step_h))
        y += step_h
    pts.extend([(x, H - 120), (panel_x + 90, H - 120)])
    return pts


def draw_path(draw, pts, fill, outline):
    draw.polygon(pts, fill=fill)
    draw.line(pts[:2], fill=outline, width=4)
    for i in range(1, len(pts) - 3, 2):
        draw.line((pts[i], pts[i + 1], pts[i + 2]), fill=outline, width=4)
    draw.line((pts[-2], pts[-1]), fill=outline, width=4)


def add_shadows(base, shapes):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for pts in shapes:
        shifted = [(x + 18, y + 22) for x, y in pts]
        draw.polygon(shifted, fill=SHADOW)
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(base, layer)


def marble_cluster(draw, center, radius, count, color, seed):
    rnd = random.Random(seed)
    cx, cy = center
    for _ in range(count):
        x = cx + rnd.randint(-radius, radius)
        y = cy + rnd.randint(-radius, radius)
        r = rnd.randint(12, 22)
        alpha = rnd.randint(215, 255)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(color[0], color[1], color[2], alpha))
        draw.ellipse((x - r + 4, y - r + 4, x - r + 12, y - r + 12), fill=(255, 248, 235, 90))


def add_left_panel(base):
    panel_x = 0
    red_pts = staircase_points(panel_x, start_y=780, step_w=82, step_h=42, steps=8)
    blue_pts = staircase_points(panel_x + 90, start_y=980, step_w=66, step_h=54, steps=8)
    base = add_shadows(base, [red_pts, blue_pts])

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw_path(draw, red_pts, fill=(176, 142, 118, 255), outline=(88, 74, 64, 255))
    draw_path(draw, blue_pts, fill=(156, 162, 174, 255), outline=(82, 90, 106, 255))

    # Separate upward-moving groups.
    marble_cluster(draw, (265, 770), 54, 17, RED, 1)
    marble_cluster(draw, (500, 640), 50, 15, RED, 2)
    marble_cluster(draw, (705, 532), 48, 12, RED, 3)

    marble_cluster(draw, (330, 955), 52, 19, BLUE, 4)
    marble_cluster(draw, (520, 800), 48, 14, BLUE, 5)
    marble_cluster(draw, (700, 620), 46, 10, BLUE, 6)

    # Glowing arches like inevitability / local trend.
    for box in [(130, 300, 530, 700), (350, 230, 770, 680)]:
        draw.arc(box, start=208, end=330, fill=(250, 236, 214, 110), width=6)

    # Subtle floor horizon.
    draw.line((70, H - 120, PANEL_W - 70, H - 120), fill=(255, 255, 255, 70), width=3)
    base = Image.alpha_composite(base, layer)
    return base


def add_right_panel(base):
    panel_x = PANEL_W + PANEL_GAP
    path_pts = descending_path_points(panel_x, top_y=410, step_w=105, step_h=58, steps=7)
    base = add_shadows(base, [path_pts])

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw_path(draw, path_pts, fill=(206, 198, 188, 255), outline=(92, 88, 84, 255))

    # Combined groups now look globally downward.
    combined_centers = [
        (panel_x + 265, 445),
        (panel_x + 430, 556),
        (panel_x + 605, 678),
        (panel_x + 790, 828),
    ]
    seeds = [10, 11, 12, 13]
    for idx, c in enumerate(combined_centers):
        marble_cluster(draw, (c[0] - 18, c[1] - 8), 40, 9, RED, seeds[idx])
        marble_cluster(draw, (c[0] + 24, c[1] + 18), 46, 13, BLUE, seeds[idx] + 20)

    # A few marbles escaping the edge to intensify the fall.
    marble_cluster(draw, (panel_x + 845, 955), 32, 6, RED, 90)
    marble_cluster(draw, (panel_x + 875, 1002), 30, 7, BLUE, 91)

    for box in [(panel_x + 180, 240, panel_x + 610, 640), (panel_x + 460, 380, panel_x + 920, 910)]:
        draw.arc(box, start=200, end=320, fill=(250, 236, 214, 88), width=5)

    draw.line((panel_x + 90, H - 120, W - 70, H - 120), fill=(255, 255, 255, 70), width=3)
    base = Image.alpha_composite(base, layer)
    return base


def add_border_and_gap(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rectangle((0, 0, W - 1, H - 1), outline=(255, 255, 255, 40), width=2)
    draw.rectangle((PANEL_W + 22, 80, PANEL_W + PANEL_GAP - 22, H - 80), fill=(8, 10, 14, 240))
    layer = layer.filter(ImageFilter.GaussianBlur(0.2))
    return Image.alpha_composite(base, layer)


def add_vignette(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(28):
        inset = i * 18
        alpha = int(5 + i * 3)
        draw.rounded_rectangle((inset, inset, W - inset, H - inset), radius=40, outline=(0, 0, 0, alpha), width=20)
    return Image.alpha_composite(base, layer.filter(ImageFilter.GaussianBlur(24)))


def build():
    img = make_canvas()
    img = add_atmosphere(img)
    img = add_panel_light(img, (0, 0, PANEL_W, H), (PANEL_W * 0.48, 780))
    img = add_panel_light(img, (PANEL_W + PANEL_GAP, 0, W, H), (PANEL_W + PANEL_GAP + PANEL_W * 0.45, 620))
    img = add_left_panel(img)
    img = add_right_panel(img)
    img = add_border_and_gap(img)
    img = add_vignette(img)
    img = img.convert("RGB")
    img.save(OUT, quality=96)


if __name__ == "__main__":
    build()
