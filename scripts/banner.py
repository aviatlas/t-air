#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write assets/banner.svg — the animated title at the top of the README.

    python3 scripts/banner.py

Two things make this harder than drawing a rectangle:

Persian shaping. GitHub renders a README image through its own proxy, with
no access to this repository's font files, and a system fallback usually has
no Persian at all. So the two typefaces travel inside the file as data URIs.
The letters stay text, with the font's layout tables intact, rather than
being flattened to outlines: flattening needs a shaper to pick the joined
forms, and without one every letter comes out in its isolated shape, which
is unreadable Persian. Carrying the whole woff2 costs about 80 KB and asks
nothing of the machine that builds it.

Movement. An SVG shown through <img> may not run scripts, so everything
moves with declarative CSS animation: an aircraft crossing the frame on a
long arc, its contrail fading behind it, and the wording rising into place.

The counts come from the built database, so the banner cannot claim a number
the site does not have.
"""
import base64
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")

FA = "اطلس هواپیماهای جهان"
WORD = "T-AIR"

TEAL, GOLD, INK = "#3ec0d1", "#e0a040", "#e8f1f6"

# Length of the flight arc, from getTotalLength() on the same path. The
# contrail animation needs it to stay behind the aircraft rather than ahead.
ARC_LEN = 1275
TRAIL = 520      # how much of the contrail stays visible behind the aircraft


def fa_digits(n):
    return str(n).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def face(family, text):
    """Find the face in fonts.css that covers `text`, return it base64-encoded.

    fonts.css splits every family across several files by unicode range, so
    the one that matters is picked by whether the text is Persian, not by
    taking the first block with the right family name.
    """
    css = open(os.path.join(A, "fonts.css"), encoding="utf-8").read()
    want_arabic = any("؀" <= c <= "ۿ" for c in text)
    for blk in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
        if re.search(r"font-family:\s*'([^']+)'", blk).group(1) != family:
            continue
        rng = re.search(r"unicode-range:\s*([^;]+)", blk)
        if ("U+0600" in (rng.group(1) if rng else "")) != want_arabic:
            continue
        src = os.path.join(A, "fonts",
                           re.search(r"url\(fonts/([^)]+)\)", blk).group(1))
        if not os.path.exists(src):
            return None
        return base64.b64encode(open(src, "rb").read()).decode()
    return None


def main():
    data = json.load(open(os.path.join(ROOT, "data", "aircraft.json"), encoding="utf-8"))
    total = data["count"]
    checked = data.get("checkedCount", 0)
    stat = (f"{fa_digits(total)} هواپیما · {fa_digits(checked)} بررسی‌شده با منبع"
            "  ·  فارسی و English")

    fa_b64 = face("Vazirmatn", FA + stat)
    lat_b64 = face("Archivo", WORD)
    if not (fa_b64 and lat_b64):
        raise SystemExit("fonts are not in the repository yet — "
                         "run scripts/fetch_fonts.py first")

    faces = f"""
@font-face{{font-family:B;font-weight:700;
  src:url(data:font/woff2;base64,{fa_b64}) format('woff2');}}
@font-face{{font-family:L;font-weight:800;
  src:url(data:font/woff2;base64,{lat_b64}) format('woff2');}}"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 400"
     width="1600" height="400" role="img"
     aria-label="T-AIR — {FA}">
<title>T-AIR — {FA}</title>
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="#0a1a22"/>
    <stop offset="0.55" stop-color="#081016"/>
    <stop offset="1" stop-color="#060b10"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.62" cy="0.42" r="0.62">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.22"/>
    <stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>
    <stop offset="0.72" stop-color="{TEAL}" stop-opacity="0.6"/>
    <stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </linearGradient>
  <path id="arc" d="M -180 372 C 260 300 640 210 1000 -70"/>
  <clipPath id="frame"><rect width="1600" height="400" rx="18"/></clipPath>
</defs>

<style>{faces}
  .fa {{ font-family:B, "Vazirmatn", "Segoe UI", Tahoma, sans-serif;
         font-weight:700; direction:rtl; }}
  .lat{{ font-family:L, Archivo, system-ui, sans-serif; font-weight:800; }}

  /* The animation sets `transform`, which beats a transform ATTRIBUTE on the
     same element — anything positioned that way has to be wrapped, or it
     jumps to the origin at the first frame. */
  .rise {{ opacity:0; animation:rise .9s cubic-bezier(.2,.7,.3,1) forwards; }}
  @keyframes rise {{ from {{ opacity:0; transform:translateY(18px); }}
                     to   {{ opacity:1; transform:none; }} }}
  #mark {{ animation-delay:0s }}
  #word {{ animation-delay:.14s }}
  #hair {{ animation-delay:.40s }}
  #tag  {{ animation-delay:.30s }}
  #stat {{ animation-delay:.52s }}

  /* One aircraft crossing the frame, with its contrail drawn behind it. */
  #plane {{ offset-path:path('M -180 372 C 260 300 640 210 1000 -70');
            offset-rotate:auto; animation:fly 14s linear infinite; }}
  @keyframes fly {{ from {{ offset-distance:0%; }} to {{ offset-distance:100%; }} }}
  /* The visible dash has to END where the aircraft is, never begin there.
     The dash occupies path positions [-offset, -offset+{TRAIL}], the aircraft
     sits at {ARC_LEN:.0f}·t, so the offset runs from {TRAIL} down by exactly the
     path's own length over the same 14 seconds. Get either number wrong and
     the contrail streams out ahead of the nose. */
  #contrail {{ stroke-dasharray:{TRAIL} {ARC_LEN:.0f}; stroke-dashoffset:{TRAIL};
               animation:draw 14s linear infinite; }}
  @keyframes draw {{ from {{ stroke-dashoffset:{TRAIL}; }}
                     to   {{ stroke-dashoffset:{TRAIL - ARC_LEN:.0f}; }} }}

  /* A slow breath on the glow, so a still frame is never the whole story. */
  #halo {{ animation:breathe 9s ease-in-out infinite; transform-origin:1000px 170px; }}
  @keyframes breathe {{ 0%,100% {{ opacity:.72; transform:scale(1); }}
                        50%     {{ opacity:1;   transform:scale(1.07); }} }}
</style>

<g clip-path="url(#frame)">
  <rect width="1600" height="400" fill="url(#sky)"/>
  <g id="halo"><rect width="1600" height="400" fill="url(#glow)"/></g>

  <!-- A gradient along the path would have been prettier, except that it is
       fixed to the frame, not to the aircraft: the trail then goes pale
       wherever in the frame the aircraft happens to be. Flat stroke. -->
  <use href="#arc" id="contrail" fill="none" stroke="{TEAL}" opacity="0.42"
       stroke-width="2.8" stroke-linecap="round"/>
  <g id="plane">
    <g transform="rotate(90) scale(1.5)" fill="{TEAL}">
      <path d="M0 -13 L3.1 -3 L15 5.5 L15 8.6 L3.1 5.4 L3.1 11 L6.4 14 L6.4 16
               L0 14.4 L-6.4 16 L-6.4 14 L-3.1 11 L-3.1 5.4 L-15 8.6 L-15 5.5
               L-3.1 -3 Z"/>
    </g>
  </g>

  <!-- The wording sits in the right half, the flight path crosses the left:
       a contrail running through the letters is the one thing that made this
       look like an accident rather than a composition. The mark is wrapped
       because the rise animation would otherwise overwrite the transform
       that places it. -->
  <g transform="translate(1416 40) scale(1.42)">
    <g id="mark" class="rise">
      <g fill="{TEAL}">
        <path d="M19.4 42a1.1 1.1 0 0 1-1.1-1.2l4.9-28.6h7.4v28.7a1.1 1.1 0 0 1-1.1 1.1Z"/>
        <path d="M4.6 7.4h38.8a2.3 2.3 0 0 1 2.2 2.9l-.3 1a1.9 1.9 0 0 1-1.9 1.4H4.6
                 a1.9 1.9 0 0 1-1.9-1.4l-.3-1a2.3 2.3 0 0 1 2.2-2.9Z"/>
      </g>
      <path d="M22.7 25.4h7.5v4.6h-8.3Z" fill="{GOLD}"/>
    </g>
  </g>

  <text id="word" class="lat rise" x="1480" y="222" text-anchor="end"
        font-size="118" letter-spacing="9" fill="{INK}">{WORD}</text>

  <rect id="hair" class="rise" x="1040" y="252" width="440" height="2"
        fill="url(#rule)"/>

  <text id="tag" class="fa rise" x="1480" y="308" text-anchor="start"
        font-size="43" fill="{INK}">{FA}</text>

  <text id="stat" class="fa rise" x="1480" y="356" text-anchor="start"
        font-size="25" fill="{TEAL}">{stat}</text>
</g>
</svg>
"""
    out = os.path.join(A, "banner.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{out}: {os.path.getsize(out) / 1024:.0f} KB "
          f"({total} aircraft, {checked} checked)")


if __name__ == "__main__":
    main()
