from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "style-transplant.png"

W = 1600
H = 2200

PAPER = (241, 236, 224, 255)
INK = (24, 24, 26, 255)
RED = (205, 52, 42, 255)
BLUE = (48, 78, 154, 255)
YELLOW = (222, 181, 68, 255)
GREY = (90, 92, 98, 255)


def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/bahnschrift.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_paper():
    img = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    rnd = random.Random(1415)
    for _ in range(24000):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        val = rnd.randint(-16, 12)
        base = max(200, min(255, PAPER[0] + val))
        draw.point((x, y), fill=(base, max(195, min(255, PAPER[1] + val)), max(185, min(255, PAPER[2] + val)), rnd.randint(18, 42)))

    for _ in range(260):
        x0 = rnd.randint(-100, W)
        y0 = rnd.randint(0, H)
        x1 = x0 + rnd.randint(120, 520)
        y1 = y0 + rnd.randint(-18, 18)
        draw.line((x0, y0, x1, y1), fill=(255, 255, 255, rnd.randint(12, 24)), width=rnd.randint(1, 2))

    return img.filter(ImageFilter.GaussianBlur(0.3))


def draw_grid(draw):
    # Thin Bauhaus-like construction lines.
    for x in [140, 300, 460, 880, 1180, 1460]:
        draw.line((x, 120, x, H - 120), fill=(0, 0, 0, 46), width=2)
    for y in [140, 360, 620, 960, 1320, 1660, 1980]:
        draw.line((120, y, W - 120, y), fill=(0, 0, 0, 46), width=2)


def add_geometry(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Main diagonal black staircase / descent path.
    stairs = [
        (300, 520, 1120, 220),
        (420, 700, 1060, 205),
        (540, 870, 980, 190),
        (660, 1025, 900, 178),
        (760, 1165, 820, 164),
    ]
    for x, y, w, h in stairs:
        draw.rectangle((x, y, x + w, y + h), fill=INK)

    # Red starting form and echo discs.
    draw.ellipse((182, 264, 498, 580), fill=RED)
    for i, box in enumerate([(420, 610, 600, 790), (650, 920, 780, 1050), (870, 1228, 960, 1318)]):
        alpha = 150 - i * 32
        draw.ellipse(box, fill=(205, 52, 42, alpha))

    # Large basin/minimum.
    cx, cy = 1080, 1560
    for r, col, width in [
        (320, BLUE, 26),
        (245, INK, 22),
        (170, BLUE, 18),
        (100, INK, 14),
    ]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=width)
    draw.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=YELLOW)

    # Accent triangle and circle for Bauhaus grammar.
    draw.polygon([(160, 1650), (420, 1650), (160, 1910)], fill=BLUE)
    draw.ellipse((1230, 355, 1365, 490), fill=YELLOW)
    draw.rectangle((1280, 1210, 1430, 1360), fill=RED)

    # Black bars and anchors.
    draw.rectangle((140, 140, 210, 940), fill=INK)
    draw.rectangle((210, 140, 545, 205), fill=INK)
    draw.rectangle((1180, 1885, 1460, 1960), fill=INK)

    shadow = layer.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(base, shadow)


def add_type(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    title_font = load_font(150, bold=True)
    small_font = load_font(42, bold=False)
    mid_font = load_font(56, bold=False)

    # Main typography, treated as compositional blocks rather than caption.
    draw.text((220, 135), "gradient", font=title_font, fill=INK)
    draw.text((220, 258), "descent", font=title_font, fill=INK)
    draw.text((1188, 1900), "bauhaus", font=mid_font, fill=PAPER)

    # Rotated side text column.
    side = Image.new("RGBA", (360, 1280), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(side)
    sdraw.text((20, 20), "state", font=mid_font, fill=RED)
    sdraw.text((20, 120), "moves", font=mid_font, fill=INK)
    sdraw.text((20, 220), "down", font=mid_font, fill=BLUE)
    sdraw.text((20, 320), "toward", font=mid_font, fill=INK)
    sdraw.text((20, 420), "minimum", font=mid_font, fill=RED)
    side = side.rotate(90, expand=True)
    layer.alpha_composite(side, (118, 1040))

    # Small footer text blocks.
    draw.text((158, 1978), "asymmetry  circle  line  plane", font=small_font, fill=INK)
    draw.text((990, 252), "1919-1933", font=small_font, fill=INK)

    return Image.alpha_composite(base, layer)


def add_fine_rules(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for y in [600, 780, 950, 1110]:
        draw.line((280, y, 1320, y - 300), fill=(0, 0, 0, 55), width=4)
    draw.line((120, 1510, 820, 1510), fill=(0, 0, 0, 70), width=4)
    draw.line((820, 1510, 820, 2030), fill=(0, 0, 0, 70), width=4)

    # Small target markers.
    for x, y in [(1080, 1560), (340, 422), (1298, 422)]:
        draw.line((x - 22, y, x + 22, y), fill=(0, 0, 0, 110), width=3)
        draw.line((x, y - 22, x, y + 22), fill=(0, 0, 0, 110), width=3)

    layer = layer.filter(ImageFilter.GaussianBlur(0.2))
    return Image.alpha_composite(base, layer)


def add_vignette(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(26):
        inset = i * 18
        alpha = int(4 + i * 2.8)
        draw.rounded_rectangle((inset, inset, W - inset, H - inset), radius=36, outline=(0, 0, 0, alpha), width=18)
    return Image.alpha_composite(base, layer.filter(ImageFilter.GaussianBlur(20)))


def build():
    img = make_paper()
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    img = add_geometry(img)
    img = add_fine_rules(img)
    img = add_type(img)
    img = add_vignette(img)
    img = img.convert("RGB")
    img.save(OUT, quality=96)


if __name__ == "__main__":
    build()
