#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write one small static page per aircraft, plus a sitemap.

    python3 scripts/build_pages.py        →  a/<id>.html  ×656, sitemap.xml

Why this exists. The atlas is a single page and every record lives behind a
fragment (`#/boeing-737-800`). A browser handles that perfectly; a search
engine does not — everything after the # is never sent to the server, so as far
as Google is concerned this site has exactly one page and 656 aircraft that
cannot be found. Anyone searching "مشخصات فوکر ۱۰۰" will never arrive.

So each record also gets a real page at its own URL, with its specifications in
the markup rather than assembled by script. These pages are deliberately plain:
they carry the figures, the description, the source link, and a way into the
full atlas. They are not a second interface to maintain — they are generated
from the same data on every build, and they are what a search engine, a link
preview, and a reader with JavaScript off actually see.
"""

import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "a")
DATA = json.load(open(os.path.join(ROOT, "data", "aircraft.json"), encoding="utf-8"))
AIRCRAFT = DATA["aircraft"]

# The site's own address. Relative URLs work everywhere, so this is only
# needed for the sitemap and the canonical tags — but it has to be a constant,
# not something the caller remembers to pass. When it came from the
# environment alone, a build with the variable unset dropped the canonical
# link from all 656 pages, and CI (which compares the build against what is
# committed) went red on every push while both builds were individually fine.
# A fork under a different account overrides it with TAIR_BASE_URL.
BASE = os.environ.get("TAIR_BASE_URL", "https://aviatlas.github.io/t-air").rstrip("/")

TYPE_FA = {
    "narrowbody": "باریک‌پیکر", "widebody": "پهن‌پیکر", "regional": "منطقه‌ای",
    "turboprop": "توربوپراپ", "freighter": "باری", "piston": "ملخی کلاسیک",
    "helicopter": "بالگرد", "fighter": "جنگنده", "bomber": "بمب‌افکن",
    "attack": "تهاجمی", "transport": "ترابری نظامی", "trainer": "آموزشی",
    "recon": "شناسایی", "maritime": "گشت دریایی", "tanker": "سوخت‌رسان",
    "awacs": "هشدار زودهنگام", "utility": "چندمنظوره", "uav": "پهپاد",
}
TYPE_EN = {
    "narrowbody": "Narrow-body airliner", "widebody": "Wide-body airliner",
    "regional": "Regional airliner", "turboprop": "Turboprop airliner",
    "freighter": "Freighter", "piston": "Propliner", "helicopter": "Helicopter",
    "fighter": "Fighter", "bomber": "Bomber", "attack": "Attack aircraft",
    "transport": "Military transport", "trainer": "Trainer",
    "recon": "Reconnaissance aircraft", "maritime": "Maritime patrol aircraft",
    "tanker": "Tanker", "awacs": "Airborne early warning aircraft",
    "utility": "Utility aircraft", "uav": "Uncrewed aircraft",
}
STATUS_FA = {"production": "در حال تولید", "active": "در سرویس",
             "retired": "بازنشسته", "development": "در دست توسعه"}
ENGINE_FA = {"jet": "جت", "turboprop": "توربوپراپ", "turboshaft": "توربوشفت",
             "piston": "پیستونی", "rocket": "موشکی", "electric": "برقی"}

FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"


def fa(v):
    return "".join(FA_DIGITS[int(c)] if c.isdigit() else c for c in str(v))


def num(v):
    return fa(f"{v:,}") if isinstance(v, (int, float)) else "—"


def e(s):
    return html.escape(str(s), quote=True)


def rows(a):
    """The figures worth putting in the markup, in reading order."""
    out = []
    if a["category"] == "civil":
        out += [("ظرفیت معمول", num(a["seatsTypical"]) + " نفر" if a.get("seatsTypical") else None),
                ("بیشترین ظرفیت", num(a["seatsMax"]) + " نفر" if a.get("seatsMax") else None),
                ("سرعت سفر", num(a["speedKmh"]) + " کیلومتر بر ساعت" if a.get("speedKmh") else None)]
    else:
        out += [("خدمه", num(a["crew"]) + " نفر" if a.get("crew") is not None else None),
                ("سرعت بیشینه", num(a["speedKmh"]) + " کیلومتر بر ساعت" if a.get("speedKmh") else None),
                ("سقف پرواز", num(a["ceilingM"]) + " متر" if a.get("ceilingM") else None)]
    out += [
        ("برد", num(a["rangeKm"]) + " کیلومتر" if a.get("rangeKm") else None),
        ("حداکثر وزن برخاست", num(a["mtowKg"]) + " کیلوگرم" if a.get("mtowKg") else None),
        ("طول", fa(a["lengthM"]) + " متر" if a.get("lengthM") else None),
        ("دهانه بال" if a["type"] != "helicopter" else "قطر روتور",
         fa(a["spanM"]) + " متر" if a.get("spanM") else None),
        ("ارتفاع", fa(a["heightM"]) + " متر" if a.get("heightM") else None),
        ("موتور", (fa(a["engineCount"]) + " × " + ENGINE_FA.get(a["engineKind"], a["engineKind"])
                   if a.get("engineCount") else ENGINE_FA.get(a["engineKind"]))),
        ("مدل موتور", a.get("engineModel")),
        ("نخستین پرواز", fa(a["firstFlight"]) if a.get("firstFlight") else None),
        ("ورود به خدمت", fa(a["introduced"]) if a.get("introduced") else None),
        ("تعداد ساخته‌شده", (num(a["built"]) + " فروند" +
                            (" (کل خانواده)" if a.get("builtFamily") else ""))
         if a.get("built") else None),
        ("تسلیحات", a.get("armament")),
    ]
    return [(k, v) for k, v in out if v]


PAGE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
{canonical}<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{ld}</script>
<style>
:root {{
  color-scheme: light dark;
  --bg: #f7f9fb; --card: #fff; --ink: #0c1620; --muted: #5b7085;
  --line: #dfe6ec; --accent: #0b6f80;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #080d13; --card: #0f1720; --ink: #e0e8ef; --muted: #8fa3b5;
          --line: #1e2c3a; --accent: #3fc6d8; }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: Vazirmatn, "Segoe UI", Tahoma, system-ui, sans-serif;
  line-height: 1.7; padding: 24px 16px 56px;
}}
main {{ max-width: 720px; margin: 0 auto; }}
a {{ color: var(--accent); }}
.back {{ font-size: 14px; text-decoration: none; }}
h1 {{ margin: 18px 0 4px; font-size: 30px; letter-spacing: -.01em;
      font-family: "Segoe UI", system-ui, sans-serif; direction: ltr; text-align: right; }}
.sub {{ color: var(--muted); margin: 0 0 18px; font-size: 15px; }}
.tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 20px; padding: 0; list-style: none; }}
.tags li {{ border: 1px solid var(--line); border-radius: 999px;
            padding: 3px 11px; font-size: 13px; color: var(--muted); }}
.note {{ background: var(--card); border: 1px solid var(--line);
         border-radius: 10px; padding: 14px 16px; margin: 0 0 22px; }}
table {{ width: 100%; border-collapse: collapse; background: var(--card);
         border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }}
th, td {{ padding: 10px 14px; text-align: right; border-bottom: 1px solid var(--line);
          font-size: 15px; }}
th {{ color: var(--muted); font-weight: 500; width: 42%; }}
td {{ font-variant-numeric: tabular-nums; }}
tr:last-child th, tr:last-child td {{ border-bottom: 0; }}
.en {{ margin: 22px 0 0; color: var(--muted); font-size: 14px;
       direction: ltr; text-align: left;
       font-family: "Segoe UI", system-ui, sans-serif; }}
.cta {{ display: inline-block; margin: 26px 0 0; padding: 11px 20px;
        background: var(--accent); color: #fff; border-radius: 8px;
        text-decoration: none; font-size: 15px; }}
footer {{ margin-top: 34px; padding-top: 16px; border-top: 1px solid var(--line);
          color: var(--muted); font-size: 13px; }}
</style>
</head>
<body>
<main>
<a class="back" href="../">‹ اطلس هواپیماهای T-AIR</a>
<h1>{model}</h1>
<p class="sub">{mfr} · {country}{role}</p>
<ul class="tags">{tags}</ul>
{note}
<table>{table}</table>
{en}
<a class="cta" href="../#/{id}">باز کردن در اطلس T-AIR</a>
<footer>
{prov}<br>
منبع: <a href="https://en.wikipedia.org/wiki/{wiki}" rel="noopener">مقاله‌ی ویکی‌پدیا</a> ·
داده با مجوز <a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="noopener">CC BY-SA 4.0</a>
</footer>
</main>
</body>
</html>
"""


INDEX_PAGE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>فهرست همه‌ی هواپیماها | T-AIR</title>
<meta name="description" content="فهرست کامل {count} هواپیمای اطلس T-AIR، به تفکیک سازنده.">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<style>
:root {{ color-scheme: light dark; --bg:#f7f9fb; --ink:#0c1620; --muted:#5b7085;
        --line:#dfe6ec; --accent:#0b6f80; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#080d13; --ink:#e0e8ef; --muted:#8fa3b5; --line:#1e2c3a; --accent:#3fc6d8; }}
}}
body {{ margin:0; background:var(--bg); color:var(--ink); padding:24px 16px 64px;
        font-family:Vazirmatn,"Segoe UI",Tahoma,system-ui,sans-serif; line-height:1.7; }}
main {{ max-width:940px; margin:0 auto; }}
a {{ color:var(--accent); }}
h1 {{ font-size:26px; margin:16px 0 6px; }}
.lede {{ color:var(--muted); margin:0 0 28px; font-size:15px; }}
h2 {{ font-size:16px; margin:26px 0 8px; padding-bottom:6px;
      border-bottom:1px solid var(--line); direction:ltr; text-align:right;
      font-family:"Segoe UI",system-ui,sans-serif; }}
ul {{ list-style:none; padding:0; margin:0; columns:3; column-gap:24px; }}
@media (max-width:760px) {{ ul {{ columns:2; }} }}
@media (max-width:480px) {{ ul {{ columns:1; }} }}
li {{ break-inside:avoid; font-size:14px; direction:ltr; text-align:right; }}
li a {{ text-decoration:none; }}
li a:hover {{ text-decoration:underline; }}
</style>
</head>
<body>
<main>
<a href="../" style="font-size:14px">‹ اطلس هواپیماهای T-AIR</a>
<h1>فهرست همه‌ی هواپیماها</h1>
<p class="lede">{count} مدل، به ترتیب سازنده. هر نام به صفحه‌ی مشخصات همان هواپیما می‌رود.</p>
{body}
</main>
</body>
</html>
"""


def write_index():
    """A browsable index of every record.

    Search engines reach a page by following a link to it. Nothing in the atlas
    links to a/, so without this page the 656 static pages would sit there
    unvisited — the sitemap helps, but only after someone submits it. It is also
    the fastest way for a person to see the whole collection at once.
    """
    by_mfr = {}
    for a in sorted(AIRCRAFT, key=lambda r: (r["mfr"].lower(), r["model"].lower())):
        by_mfr.setdefault(a["mfr"], []).append(a)
    parts = []
    for mfr, items in by_mfr.items():
        links = "".join(
            f'<li><a href="{e(a["id"])}.html">{e(a["model"])}</a></li>' for a in items)
        parts.append(f"<h2>{e(mfr)}</h2>\n<ul>{links}</ul>")
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_PAGE.format(count=fa(len(AIRCRAFT)), body="\n".join(parts)))


def build():
    os.makedirs(OUT, exist_ok=True)
    made = 0
    for a in AIRCRAFT:
        kind_fa = TYPE_FA.get(a["type"], a["type"])
        kind_en = TYPE_EN.get(a["type"], a["type"])
        title = f'{a["mfr"]} {a["model"]} — مشخصات فنی | T-AIR'
        desc = (f'{a["mfr"]} {a["model"]}: {kind_fa}'
                + (f'، {fa(a["introduced"])}' if a.get("introduced") else "")
                + (f'، برد {num(a["rangeKm"])} کیلومتر' if a.get("rangeKm") else "")
                + (f'، سرعت {num(a["speedKmh"])} کیلومتر بر ساعت' if a.get("speedKmh") else "")
                + ". " + (a.get("notes") or ""))[:300]

        tags = "".join(f"<li>{e(t)}</li>" for t in [
            kind_fa, ENGINE_FA.get(a["engineKind"], a["engineKind"]),
            STATUS_FA.get(a["status"], a["status"]),
            "در ناوگان ایران" if a.get("iran") else None,
            f'خانواده {a["family"]}' if a.get("family") else None,
        ] if t)

        table = "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in rows(a))
        note = f'<p class="note">{e(a["notes"])}</p>' if a.get("notes") else ""
        def sentence(x):
            x = (x or "").strip()
            return x if not x or x[-1] in ".!?" else x + "."
        en_bits = " ".join(x for x in [
            f'{a["mfr"]} {a["model"]} — {kind_en}.',
            sentence(a.get("role_en")), sentence(a.get("notes_en"))] if x)
        en = f'<p class="en">{e(en_bits)}</p>' if en_bits else ""

        ld = json.dumps({
            "@context": "https://schema.org",
            "@type": "Product",
            "name": f'{a["mfr"]} {a["model"]}',
            "category": kind_en,
            "brand": {"@type": "Brand", "name": a["mfr"]},
            "description": en_bits or desc,
            "isPartOf": {"@type": "Dataset", "name": "T-AIR — World Aircraft Atlas"},
        }, ensure_ascii=False)

        prov = ("این رکورد فیلد به فیلد با مقاله‌ی ویکی‌پدیا مقایسه شده است"
                + (f' — بررسی {fa(DATA.get("checkedOn", ""))}' if DATA.get("checkedOn") else "")
                ) if a.get("checked") else "این رکورد هنوز با منبع مقایسه نشده است"

        page = PAGE.format(
            title=e(title), desc=e(desc), ld=ld, model=e(a["model"]), mfr=e(a["mfr"]),
            country=e(a["country"]),
            role=(" · " + e(a["role"])) if a.get("role") else "",
            tags=tags, note=note, table=table, en=en, id=e(a["id"]),
            wiki=e((a.get("wiki") or a["model"]).replace(" ", "_")),
            prov=e(prov),
            canonical=(f'<link rel="canonical" href="{BASE}/a/{a["id"]}.html">\n' if BASE else ""),
        )
        with open(os.path.join(OUT, a["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
        made += 1

    write_index()

    # A sitemap only means something with an absolute address, so it is written
    # when one is known and skipped when it is not.
    if BASE:
        urls = [f"  <url><loc>{BASE}/</loc><priority>1.0</priority></url>"]
        urls += [f'  <url><loc>{BASE}/a/{a["id"]}.html</loc></url>' for a in AIRCRAFT]
        with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    + "\n".join(urls) + "\n</urlset>\n")
        robots = os.path.join(ROOT, "robots.txt")
        txt = open(robots, encoding="utf-8").read() if os.path.exists(robots) else ""
        if "Sitemap:" not in txt:
            with open(robots, "w", encoding="utf-8") as f:
                f.write(txt.rstrip() + f"\nSitemap: {BASE}/sitemap.xml\n")
        print(f"{made} pages + sitemap.xml ({BASE})")
    else:
        print(f"{made} pages in a/ — set TAIR_BASE_URL to also write sitemap.xml")


if __name__ == "__main__":
    build()
