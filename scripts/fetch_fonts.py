#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download the four typefaces into the repository and switch the page over to
serving them itself.

    pip install requests
    python3 scripts/fetch_fonts.py
    python3 scripts/build_single.py

Why bother. Two reasons, and the second is the important one here:

  * Privacy — as long as the page links to fonts.googleapis.com, every visitor's
    browser announces itself to Google before the site has drawn a single word.
  * Reach — Google's font servers are not reliably reachable from inside Iran,
    which is where most of this site's readers are. A visitor who cannot load
    Vazirmatn gets the browser's default Persian font, and the page they see is
    not the page it was designed as. A font that ships with the site always
    arrives.

All four families are licensed under the SIL Open Font License 1.1, which
permits redistribution as long as the licence travels with the files. This
script writes a copy of it next to them.

It is safe to run twice: existing files are overwritten, and the <link> in
index.html is only rewritten once.
"""

import os
import re
import sys

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "fonts")
INDEX = os.path.join(ROOT, "index.html")
CSS = os.path.join(ROOT, "assets", "fonts.css")

# The Google Fonts CSS API returns different formats depending on the browser
# it thinks is asking. This user agent is the one that gets woff2, which every
# browser released since about 2016 understands and which is roughly half the
# size of the alternatives.
UA_WOFF2 = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

FAMILIES = [
    ("Vazirmatn", "wght@400;600;700"),
    ("IBM+Plex+Sans+Condensed", "wght@400;600"),
    ("IBM+Plex+Mono", "wght@400;500"),
    ("Archivo", "wght@400;600;800"),
]

OFL = """\
These fonts are licensed under the SIL Open Font License, Version 1.1.

    Vazirmatn               https://github.com/rastikerdar/vazirmatn
    IBM Plex Sans Condensed https://github.com/IBM/plex
    IBM Plex Mono           https://github.com/IBM/plex
    Archivo                 https://github.com/Omnibus-Type/Archivo

The full licence text is at https://scripts.sil.org/OFL

In short: you may use, study, modify and redistribute these fonts, including
inside a commercial product, as long as you do not sell them on their own and
as long as this notice travels with them. If you modify one, it has to be
renamed.
"""


def fetch_css(family, axis):
    url = f"https://fonts.googleapis.com/css2?family={family}:{axis}&display=swap"
    r = requests.get(url, headers={"User-Agent": UA_WOFF2}, timeout=30)
    r.raise_for_status()
    return r.text


def main():
    os.makedirs(OUT, exist_ok=True)
    sheets, files = [], 0

    for family, axis in FAMILIES:
        name = family.replace("+", " ")
        print(f"  {name} …", end=" ", flush=True)
        try:
            css = fetch_css(family, axis)
        except Exception as e:                       # noqa: BLE001
            sys.exit(f"\n  could not reach Google Fonts: {e}\n"
                     f"  If it is blocked where you are, use a VPN for this one step.")

        # Rewrite every remote url() to a local file, downloading as we go.
        def localise(match):
            nonlocal files
            url = match.group(1)
            if not url.startswith("https://fonts.gstatic.com/"):
                return match.group(0)               # leave anything unexpected alone
            fname = re.sub(r"[^A-Za-z0-9._-]", "-", url.rsplit("/", 1)[-1])
            if not fname.endswith(".woff2"):
                fname += ".woff2"
            path = os.path.join(OUT, fname)
            if not os.path.exists(path):
                data = requests.get(url, timeout=60).content
                with open(path, "wb") as f:
                    f.write(data)
                files += 1
            return f"url(fonts/{fname})"

        sheets.append(re.sub(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", localise, css))
        print("ok")

    with open(CSS, "w", encoding="utf-8") as f:
        f.write("/* Written by scripts/fetch_fonts.py — do not edit by hand.\n"
                "   The four families, served from assets/fonts/ so the page needs\n"
                "   nothing from Google to render correctly. */\n\n")
        f.write("\n".join(sheets))

    with open(os.path.join(OUT, "LICENSE.txt"), "w", encoding="utf-8") as f:
        f.write(OFL)

    # Point index.html at the local sheet, once.
    html = open(INDEX, encoding="utf-8").read()
    if "assets/fonts.css" not in html:
        html = re.sub(
            r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
            r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*'
            r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^>]*>',
            '<link rel="stylesheet" href="assets/fonts.css">',
            html, count=1)
        # the page no longer talks to Google, so the policy can say so
        html = html.replace(
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com;",
            "style-src 'self' 'unsafe-inline'; font-src 'self';")
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(html)
        print("\nindex.html now loads assets/fonts.css and the CSP no longer "
              "allows Google's hosts.")
    else:
        print("\nindex.html was already pointing at the local sheet.")

    size = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"{files} font files, {size / 1024:.0f} KB in assets/fonts/")
    print("Now run: python3 scripts/build_single.py")


if __name__ == "__main__":
    main()
