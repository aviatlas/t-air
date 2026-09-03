#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compose the two panels from scripts/shot.js into assets/screenshot.png.

    python3 scripts/shot.py

Rounded corners, a soft shadow in the brand's teal, and a gradient ground —
the point is that the README's first impression looks composed rather than
like a raw window capture. The panels themselves are never retouched; what
you see is what the site renders.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
W, PAD, GAP, RADIUS = 2400, 48, 36, 22
MAIN_W = 1640
TOP, BOTTOM = (240, 245, 249), (219, 231, 237)


def rounded(im, r):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im.convert("RGB"), (0, 0), mask)
    return out


def shadow(canvas, box, r, blur=30, alpha=48, off=12):
    x, y, w, h = box
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([x, y + off, x + w, y + h + off], r,
                                          fill=(11, 111, 128, alpha))
    canvas.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def main():
    main_im = Image.open(os.path.join(A, "_shot-main.png"))
    sheet = Image.open(os.path.join(A, "_shot-sheet.png"))

    main_im = main_im.resize((MAIN_W, round(main_im.size[1] * MAIN_W / main_im.size[0])),
                             Image.LANCZOS)
    sw = W - PAD * 2 - MAIN_W - GAP
    sheet = sheet.resize((sw, round(sheet.size[1] * sw / sheet.size[0])), Image.LANCZOS)

    h = PAD * 2 + main_im.size[1]
    canvas = Image.new("RGBA", (W, h))
    grad = Image.new("RGBA", (1, h))
    for y in range(h):
        t = y / (h - 1)
        grad.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)) + (255,))
    canvas.alpha_composite(grad.resize((W, h)))

    shadow(canvas, (PAD, PAD, MAIN_W, main_im.size[1]), RADIUS)
    canvas.alpha_composite(rounded(main_im, RADIUS), (PAD, PAD))

    sx = PAD + MAIN_W + GAP
    sy = PAD + (main_im.size[1] - sheet.size[1]) // 2
    shadow(canvas, (sx, sy, sw, sheet.size[1]), RADIUS)
    canvas.alpha_composite(rounded(sheet, RADIUS), (sx, sy))

    out = os.path.join(A, "screenshot.png")
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    for tmp in ("_shot-main.png", "_shot-sheet.png"):
        os.remove(os.path.join(A, tmp))
    print(f"{out}: {canvas.size[0]}x{canvas.size[1]}, "
          f"{os.path.getsize(out) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
