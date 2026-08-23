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


def build():
    html = read("index.html")
    css = read("assets", "styles.css")
    js = read("assets", "app.js")
    i18n = read("assets", "i18n.js")
    data = read("data", "aircraft.json")

    html = html.replace(
        '<link rel="stylesheet" href="assets/styles.css">',
        "<style>\n" + css + "\n</style>")
    html = html.replace(
        '<script src="assets/i18n.js"></script>',
        "<script>\n" + i18n + "\n</script>")
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
    keep = "\n".join(
        line for line in head.splitlines()
        if any(k in line for k in ("<title>", "fonts.googleapis", "fonts.gstatic",
                                   "<style>", "</style>")) or line.startswith(("  ", "/*", "}", ".", ":", "@", "*"))
    )
    # simpler + safer: keep the whole head except charset/viewport meta
    keep = "\n".join(
        line for line in head.splitlines()
        if "charset" not in line and "viewport" not in line
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
