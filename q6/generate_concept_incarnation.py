from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "concept-incarnation.png"

W = 1800
H = 1350


def lerp(a, b, t):
    return int(a + (b - a) * t)


def make_background():
    img = Image.new("RGBA", (W, H))
    px = img.load()
    top = (32, 22, 16)
    bottom = (86, 61, 40)
    for y in range(H):
        t = y / (H - 1)
        row = (
            lerp(top[0], bottom[0], t),
            lerp(top[1], bottom[1], t),
            lerp(top[2], bottom[2], t),
            255,
        )
        for x in range(W):
            px[x, y] = row
    return img


def add_workshop_walls(img):
    wall = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wall)

    draw.rectangle((0, 0, W, int(H * 0.62)), fill=(48, 34, 25, 255))
    draw.rectangle((0, int(H * 0.62), W, H), fill=(112, 77, 48, 255))

    for y in range(int(H * 0.64), H, 26):
        draw.line((0, y, W, y), fill=(132, 94, 58, 95), width=3)
    for x in range(0, W, 140):
        draw.line((x, int(H * 0.62), x + 40, H), fill=(92, 61, 38, 75), width=2)

    # Pegboard region.
    peg = (1050, 120, 1710, 690)
    draw.rounded_rectangle(peg, radius=18, fill=(78, 55, 38, 255), outline=(102, 74, 52, 180), width=3)
    for py in range(160, 650, 34):
        for px_ in range(1090, 1670, 34):
            draw.ellipse((px_ - 3, py - 3, px_ + 3, py + 3), fill=(58, 40, 28, 190))

    return Image.alpha_composite(img, wall)


def add_bench_light(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.polygon(
        [
            (-50, 260),
            (420, 180),
            (1080, H),
            (0, H),
        ],
        fill=(255, 223, 172, 56),
    )
    draw.ellipse((980, 820, 1760, 1380), fill=(255, 215, 160, 44))
    overlay = overlay.filter(ImageFilter.GaussianBlur(48))
    return Image.alpha_composite(img, overlay)


def add_dust(img, seed=1415):
    rnd = random.Random(seed)
    dust = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dust)
    for _ in range(13000):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        alpha = rnd.randint(4, 16)
        value = rnd.randint(150, 210)
        draw.point((x, y), fill=(value, value - 8, value - 16, alpha))
    dust = dust.filter(ImageFilter.GaussianBlur(0.4))
    return Image.alpha_composite(img, dust)


def lock_body(draw, x, y, w, h, fill, outline=None):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=int(w * 0.12), fill=fill, outline=outline, width=3 if outline else 1)


def draw_standard_lock(draw, x, y, scale, metal):
    body_w = 120 * scale
    body_h = 150 * scale
    shackle_w = 72 * scale
    shackle_h = 90 * scale

    lock_body(draw, x, y, body_w, body_h, metal, outline=(40, 32, 28, 110))
    draw.arc((x + body_w * 0.20, y - shackle_h * 0.55, x + body_w * 0.80, y + shackle_h * 0.75), start=188, end=352, fill=(186, 186, 176, 240), width=max(2, int(12 * scale)))
    key_x = x + body_w * 0.50
    key_y = y + body_h * 0.60
    draw.rounded_rectangle((key_x - 12 * scale, key_y - 20 * scale, key_x + 12 * scale, key_y + 20 * scale), radius=int(5 * scale), fill=(42, 30, 25, 220))
    draw.polygon(
        [
            (key_x, key_y - 16 * scale),
            (key_x - 22 * scale, key_y - 2 * scale),
            (key_x - 16 * scale, key_y + 20 * scale),
            (key_x + 16 * scale, key_y + 20 * scale),
            (key_x + 22 * scale, key_y - 2 * scale),
        ],
        fill=(42, 30, 25, 220),
    )


def draw_vise(draw, x, y):
    draw.rounded_rectangle((x, y, x + 380, y + 120), radius=26, fill=(74, 90, 102, 255))
    draw.rounded_rectangle((x + 40, y + 30, x + 300, y + 170), radius=18, fill=(93, 112, 124, 255))
    draw.rounded_rectangle((x + 268, y + 18, x + 380, y + 182), radius=16, fill=(120, 136, 146, 255))
    draw.rectangle((x + 160, y + 170, x + 230, y + 290), fill=(74, 90, 102, 255))
    draw.rounded_rectangle((x + 100, y + 280, x + 290, y + 324), radius=18, fill=(62, 74, 84, 255))
    draw.rectangle((x + 375, y + 80, x + 485, y + 110), fill=(168, 176, 184, 255))
    draw.ellipse((x + 452, y + 58, x + 512, y + 132), fill=(176, 182, 188, 255))


def draw_distorted_lock(draw, x, y, scale=1.0):
    body_w = 240 * scale
    body_h = 285 * scale
    body = [
        (x + 10, y + 40),
        (x + body_w * 0.16, y + 6),
        (x + body_w * 0.44, y + 26),
        (x + body_w * 0.62, y + 0),
        (x + body_w * 0.88, y + 52),
        (x + body_w * 0.96, y + body_h * 0.26),
        (x + body_w * 0.88, y + body_h * 0.92),
        (x + body_w * 0.24, y + body_h),
        (x + 0, y + body_h * 0.74),
    ]
    draw.polygon(body, fill=(167, 130, 84, 255))
    draw.line(body + [body[0]], fill=(75, 54, 31, 255), width=5)

    # Shackle
    draw.arc((x + 46, y - 80, x + 190, y + 124), start=194, end=352, fill=(190, 182, 170, 255), width=17)

    # Scratches and dents
    for pts in [
        [(x + 38, y + 90), (x + 92, y + 70), (x + 132, y + 96)],
        [(x + 56, y + 202), (x + 118, y + 194), (x + 166, y + 221)],
        [(x + 86, y + 246), (x + 148, y + 260)],
    ]:
        draw.line(pts, fill=(92, 70, 45, 170), width=3)

    # Warped keyway matched to the custom key teeth.
    keyway = [
        (x + 118, y + 136),
        (x + 136, y + 130),
        (x + 150, y + 144),
        (x + 170, y + 132),
        (x + 184, y + 150),
        (x + 174, y + 164),
        (x + 188, y + 182),
        (x + 174, y + 194),
        (x + 150, y + 192),
        (x + 136, y + 214),
        (x + 118, y + 206),
        (x + 104, y + 184),
        (x + 90, y + 178),
        (x + 98, y + 156),
    ]
    draw.polygon(keyway, fill=(44, 30, 22, 255))


def brass_gradient(size, base=(192, 140, 70), highlight=(250, 220, 120)):
    w, h = size
    img = Image.new("RGBA", size)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / max(1, w - 1)) * 0.78 + (1 - y / max(1, h - 1)) * 0.22
            r = lerp(base[0], highlight[0], min(1.0, t))
            g = lerp(base[1], highlight[1], min(1.0, t))
            b = lerp(base[2], highlight[2], min(1.0, t))
            px[x, y] = (r, g, b, 255)
    return img


def custom_key_mask():
    img = Image.new("L", (920, 360), 0)
    draw = ImageDraw.Draw(img)
    # Bow
    draw.rounded_rectangle((30, 70, 270, 300), radius=95, fill=255)
    draw.rounded_rectangle((94, 132, 206, 238), radius=36, fill=0)

    # Shaft
    draw.rounded_rectangle((250, 156, 760, 222), radius=20, fill=255)

    # Teeth: intentionally too specific and noisy.
    teeth = [
        (760, 156),
        (792, 156),
        (792, 134),
        (822, 134),
        (822, 188),
        (846, 188),
        (846, 118),
        (880, 118),
        (880, 232),
        (844, 232),
        (844, 202),
        (810, 202),
        (810, 246),
        (774, 246),
        (774, 222),
        (760, 222),
    ]
    draw.polygon(teeth, fill=255)

    # Fine notches.
    draw.polygon([(646, 222), (670, 222), (670, 248), (694, 248), (694, 222), (720, 222), (720, 156), (646, 156)], fill=255)
    return img


def place_custom_key(base):
    mask = custom_key_mask()
    brass = brass_gradient(mask.size)
    brass.putalpha(mask)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_key = brass.copy().rotate(-11, resample=Image.Resampling.BICUBIC, expand=True)
    s_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sx = 390
    sy = 855
    shadow_alpha = Image.new("L", s_key.size, 0)
    shadow_alpha.paste(s_key.getchannel("A"))
    shadow_layer = Image.new("RGBA", s_key.size, (22, 16, 12, 210))
    shadow_layer.putalpha(shadow_alpha)
    s_img.alpha_composite(shadow_layer, (sx + 18, sy + 18))
    s_img = s_img.filter(ImageFilter.GaussianBlur(14))
    base = Image.alpha_composite(base, s_img)

    main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    main.alpha_composite(s_key, (sx, sy))
    # Highlights and wear marks.
    d = ImageDraw.Draw(main)
    d.line((sx + 250, sy + 125, sx + 675, sy + 152), fill=(255, 236, 162, 160), width=8)
    d.line((sx + 675, sy + 152, sx + 820, sy + 120), fill=(255, 231, 150, 150), width=6)
    for off in [0, 18, 36]:
        d.arc((sx + 48 + off, sy + 86 + off // 3, sx + 224 - off, sy + 264 - off), start=18, end=332, fill=(118, 78, 32, 120), width=3)
    base = Image.alpha_composite(base, main)
    return base


def add_background_locks(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    positions = [
        (1160, 210, 0.86),
        (1385, 250, 0.98),
        (1570, 190, 0.78),
        (1115, 438, 0.92),
        (1360, 470, 0.86),
        (1565, 408, 0.95),
    ]
    for x, y, s in positions:
        draw_standard_lock(draw, x, y, s, (176, 182, 175, 248))
    layer = layer.filter(ImageFilter.GaussianBlur(1.5))

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    for x, y, s in positions:
        draw_standard_lock(sdraw, x + 12, y + 18, s, (22, 18, 16, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base, shadow)
    base = Image.alpha_composite(base, layer)
    return base


def add_metal_filings(base, seed=415):
    rnd = random.Random(seed)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for _ in range(380):
        x = rnd.randint(760, 1240)
        y = rnd.randint(930, 1220)
        length = rnd.randint(6, 24)
        angle = rnd.uniform(-0.9, 0.4)
        x2 = x + math.cos(angle) * length
        y2 = y + math.sin(angle) * length
        color = (220, 184, 104, rnd.randint(80, 180))
        draw.line((x, y, x2, y2), fill=color, width=rnd.randint(1, 3))
    layer = layer.filter(ImageFilter.GaussianBlur(0.35))
    return Image.alpha_composite(base, layer)


def add_vignette(base):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(34):
        inset = i * 20
        alpha = int(8 + i * 3.1)
        draw.rounded_rectangle((inset, inset, W - inset, H - inset), radius=60, outline=(0, 0, 0, alpha), width=22)
    layer = layer.filter(ImageFilter.GaussianBlur(24))
    return Image.alpha_composite(base, layer)


def build():
    img = make_background()
    img = add_workshop_walls(img)
    img = add_bench_light(img)
    img = add_background_locks(img)

    # Foreground vise and damaged lock.
    fg_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(fg_shadow)
    draw_vise(sdraw, 140, 640)
    draw_distorted_lock(sdraw, 288, 500, 1.0)
    fg_shadow = fg_shadow.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, fg_shadow)

    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    draw_vise(d, 120, 620)
    draw_distorted_lock(d, 268, 480, 1.0)

    # Small glints.
    d.ellipse((332, 564, 360, 592), fill=(250, 224, 161, 108))
    d.ellipse((412, 514, 432, 534), fill=(252, 224, 168, 96))
    img = Image.alpha_composite(img, fg)

    img = place_custom_key(img)
    img = add_metal_filings(img)
    img = add_dust(img)
    img = add_vignette(img)

    img = img.convert("RGB")
    img.save(OUT, quality=96)


if __name__ == "__main__":
    build()
