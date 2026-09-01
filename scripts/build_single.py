#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inlines index.html + assets + data into two single-file builds.

  dist/t-air.html           full document (open locally, host anywhere)
  dist/t-air-artifact.html  body-only fragment for the Artifact publisher
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


def inline_photos():
    """Embed the 180 px photo set as data URIs, if fetch_photos.py has run.

    The single-file build has to carry its pictures with it — the artifact
    host blocks outside requests — so the tiny tier exists purely for this.
    Returns a script tag, or an empty string when there is no library yet.
    """
    import base64
    idx = os.path.join(ROOT, "data", "photos.json")
    tiny = os.path.join(ROOT, "assets", "photos", "tiny")
    if not (os.path.exists(idx) and os.path.isdir(tiny)):
        return ""
    meta = json.load(open(idx, encoding="utf-8"))
    inline, total = {}, 0
    for aid in meta.get("photos", {}):
        path = os.path.join(tiny, aid + ".webp")
        if not os.path.exists(path):
            continue
        raw = open(path, "rb").read()
        total += len(raw)
        inline[aid] = "data:image/webp;base64," + base64.b64encode(raw).decode()
    if total > 11 * 1024 * 1024:
        print(f"  ! tiny photo set is {total/1048576:.1f} MB — too large to inline, "
              "skipping (the hosted build still shows photos)")
        return ""
    print(f"  inlined {len(inline)} photos, {total/1048576:.1f} MB")
    return ("<script>window.__PHOTOS__=" +
            json.dumps({"photos": meta.get("photos", {})}, ensure_ascii=False,
                       separators=(",", ":")) +
            ";window.__PHOTOS_INLINE__=" +
            json.dumps(inline, separators=(",", ":")) + ";</script>\n")


def inline_fonts(html):
    """Fold a local font sheet into the page, as data URIs.

    Only does anything once scripts/fetch_fonts.py has run. The single-file
    build has to carry everything it needs — a relative url(fonts/…) would
    resolve to nothing once the file is moved — so the woff2 files ride along
    base64-encoded. That costs roughly a third more than the raw files; the
    alternative is a page that renders in the wrong typeface.
    """
    import base64
    sheet = os.path.join(ROOT, "assets", "fonts.css")
    if '"assets/fonts.css"' not in html or not os.path.exists(sheet):
        return html
    css = read("assets", "fonts.css")

    def embed(match):
        name = match.group(1)
        path = os.path.join(ROOT, "assets", "fonts", name)
        if not os.path.exists(path):
            return match.group(0)
        raw = open(path, "rb").read()
        return ("url(data:font/woff2;base64," +
                base64.b64encode(raw).decode() + ")")

    css = re.sub(r"url\(fonts/([^)]+)\)", embed, css)
    print(f"  inlined the font sheet, {len(css)/1024:.0f} KB")
    return html.replace('<link rel="stylesheet" href="assets/fonts.css">',
                        "<style>\n" + css + "\n</style>")


def stamp_worker(data):
    """Give sw.js a cache name that changes when the build does.

    Without this, a returning reader is served whatever the worker cached the
    first time — a site that quietly never updates is worse than one with no
    cache at all. The signature is a short digest of the data file, so any
    change to the database (which is what a deploy is, in practice) mints a
    new cache and the activate handler drops the old one.
    """
    import hashlib
    path = os.path.join(ROOT, "sw.js")
    if not os.path.exists(path):
        return
    sig = hashlib.sha1(data.encode("utf-8")).hexdigest()[:10]
    src = read("sw.js")
    new = re.sub(r'const CACHE = "[^"]*";', f'const CACHE = "t-air-{sig}";', src, count=1)
    if new != src:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"  service worker cache: t-air-{sig}")


def build():
    html = read("index.html")
    css = read("assets", "styles.css")
    js = read("assets", "app.js")
    i18n = read("assets", "i18n.js")
    data = read("data", "aircraft.json")

    stamp_worker(data)
    # the single-file build is one file with no origin of its own: a manifest
    # link and an apple-touch icon would both point at nothing
    html = re.sub(r'\s*<link rel="(manifest|apple-touch-icon)"[^>]*>', "", html)
    html = inline_fonts(html)
    html = html.replace(
        '<link rel="stylesheet" href="assets/styles.css">',
        "<style>\n" + css + "\n</style>")
    html = html.replace(
        '<script src="assets/i18n.js"></script>',
        inline_photos() + "<script>\n" + i18n + "\n</script>")
    html = html.replace(
        '<script src="assets/app.js"></script>',
        "<script>window.__AIRCRAFT__ = " + json.dumps(json.loads(data),
                                                      ensure_ascii=False,
                                                      separators=(",", ":")) +
        ";</script>\n<script>\n" + js + "\n</script>")

    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    with open(os.path.join(ROOT, "dist", "t-air.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # Artifact build: the publisher supplies <!doctype>/<html>/<head>/<body>,
    # so hand it only what goes inside — <title> and the font <link> included.
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)
    # Keep the whole head except the lines the publisher supplies itself
    # (charset, viewport) and the ones that point at files the artifact does
    # not carry — a relative icon or social-card href resolves to nothing
    # there, and the JSON-LD contentUrl would be a dead link.
    drop = ("charset", "viewport", 'rel="icon"', "og:image", "twitter:image")
    keep = "\n".join(
        line for line in head.splitlines()
        if not any(k in line for k in drop)
    )
    frag = ('<script>document.documentElement.lang="fa";'
            'document.documentElement.dir="rtl";</script>\n' + keep + body)
    with open(os.path.join(ROOT, "dist", "t-air-artifact.html"), "w", encoding="utf-8") as f:
        f.write(frag)

    for name in ("t-air.html", "t-air-artifact.html"):
        size = os.path.getsize(os.path.join(ROOT, "dist", name))
        print(f"{name}: {size/1024:.0f} KB")


if __name__ == "__main__":
    build()
