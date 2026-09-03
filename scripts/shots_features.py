#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compose the panels from scripts/shots_features.js into two README images.

    python3 scripts/shots_features.py
      →  assets/shot-compare.png   the comparison table
      →  assets/shot-mobile.png    three phone frames

Same finish as scripts/shot.py — rounded corners, a teal shadow, a gradient
ground — so the pictures in the README look like one set rather than three
unrelated captures. Nothing inside a panel is retouched.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
RADIUS = 22
PHONE_RADIUS = 44
MAX_W = 1900
TOP, BOTTOM = (240, 245, 249), (219, 231, 237)


def rounded(im, r):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1],
                                           r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im.convert("RGB"), (0, 0), mask)
    return out


def shadow(canvas, box, r, blur=30, alpha=48, off=12):
    x, y, w, h = box
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([x, y + off, x + w, y + h + off], r,
                                          fill=(11, 111, 128, alpha))
    canvas.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def ground(size):
    w, h = size
    canvas = Image.new("RGBA", size)
    grad = Image.new("RGBA", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        grad.putpixel((0, y),
                      tuple(int(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)) + (255,))
    canvas.alpha_composite(grad.resize((w, h)))
    return canvas


def trim_to_row(im, bg_tol=14):
    """Cut the bottom at the last full table row.

    Playwright clips at the viewport, which lands mid-row and leaves a
    sliced line of figures across the bottom edge. Rows are separated by a
    hairline rule, so the last rule is the honest place to end.
    """
    px = im.convert("RGB")
    w, h = px.size
    x0, x1 = int(w * 0.1), int(w * 0.9)
    for y in range(h - 1, int(h * 0.5), -1):
        row = [px.getpixel((x, y)) for x in range(x0, x1, 12)]
        light = sum(1 for p in row if max(p) - min(p) < bg_tol and sum(p) / 3 > 200)
        if light > len(row) * 0.9:          # a clear band: no glyphs crossing it
            return im.crop((0, 0, w, y))
    return im


def compose(panels, out_name, radius, pad=48, gap=40, align="top"):
    heights = [p.size[1] for p in panels]
    widths = [p.size[0] for p in panels]
    h = pad * 2 + max(heights)
    w = pad * 2 + sum(widths) + gap * (len(panels) - 1)
    canvas = ground((w, h))
    x = pad
    for p in panels:
        y = pad if align == "top" else pad + (max(heights) - p.size[1]) // 2
        shadow(canvas, (x, y, p.size[0], p.size[1]), radius)
        canvas.alpha_composite(rounded(p, radius), (x, y))
        x += p.size[0] + gap
    # A README image wider than about 1900 px is paying for pixels nobody
    # sees — GitHub lays the column out at well under half that.
    if canvas.size[0] > MAX_W:
        canvas = canvas.resize(
            (MAX_W, round(canvas.size[1] * MAX_W / canvas.size[0])), Image.LANCZOS)
    out = os.path.join(A, out_name)
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"{out}: {canvas.size[0]}x{canvas.size[1]}, "
          f"{os.path.getsize(out) / 1024:.0f} KB")


def main():
    cmp_im = trim_to_row(Image.open(os.path.join(A, "_feat-compare.png")))
    compose([cmp_im], "shot-compare.png", RADIUS)

    phones = [Image.open(os.path.join(A, f"_feat-phone-{n}.png"))
              for n in ("list", "card", "dark")]
    target = 760
    phones = [p.resize((target, round(p.size[1] * target / p.size[0])), Image.LANCZOS)
              for p in phones]
    compose(phones, "shot-mobile.png", PHONE_RADIUS, pad=56, gap=48)

    for f in os.listdir(A):
        if f.startswith("_feat-"):
            os.remove(os.path.join(A, f))


if __name__ == "__main__":
    main()
