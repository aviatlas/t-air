#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download one freely-licensed photograph per aircraft into the repository.

Run this once on a machine with internet access:

    pip install pillow requests
    python3 scripts/fetch_photos.py

It walks data/aircraft.json, asks the English Wikipedia for each article's
lead image, keeps only files hosted on Wikimedia Commons — those carry a free
licence by policy, unlike the fair-use stills that live on Wikipedia itself —
and writes three sizes plus a credit line.

    assets/photos/<id>.webp          880 px, used on the detail sheet
    assets/photos/thumb/<id>.webp    440 px, used on the result cards
    assets/photos/tiny/<id>.webp     180 px, inlined into the single-file build
    data/photos.json                 { id: {credit, licence, file, page} }

The run is resumable: anything already on disk and listed in photos.json is
skipped, so an interrupted run costs nothing. Requests are rate-limited to be
a polite API client. Aircraft whose article has no Commons lead image are
recorded in photos.json under "missing" so the next run does not retry them
forever — delete that list to re-check.
"""

import io
import json
import os
import re
import sys
import time

try:
    import requests
    from PIL import Image
except ImportError:
    sys.exit("This script needs two packages:\n    pip install pillow requests")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "aircraft.json")
OUT = os.path.join(ROOT, "assets", "photos")
INDEX = os.path.join(ROOT, "data", "photos.json")

API = "https://en.wikipedia.org/w/api.php"
COMMONS = "https://commons.wikimedia.org/w/api.php"
UA = ("T-AIR-atlas/1.0 (open aircraft reference database; "
      "contact: via the project repository)")

SIZES = {"": 880, "thumb": 440, "tiny": 180}   # ≈ 40 + 18 + 4 KB per aircraft
PAUSE = 0.35          # seconds between API calls
BATCH = 40            # titles per pageimages query (API allows 50)


def get(url, params):
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    time.sleep(PAUSE)
    return r.json()


def lead_images(titles):
    """title -> image file name ("File:..."), for a batch of articles."""
    out = {}
    data = get(API, {
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "pageimages", "piprop": "name",
        "titles": "|".join(titles), "redirects": "1",
    })
    # follow redirects back to the title we asked for
    alias = {}
    for r in data.get("query", {}).get("redirects", []):
        alias[r["to"]] = r["from"]
    for page in data.get("query", {}).get("pages", []):
        name = page.get("pageimage")
        if not name:
            continue
        title = page.get("title")
        out[alias.get(title, title)] = "File:" + name
    return out


# Only licences that allow reuse and modification by anyone. This is an
# allowlist on purpose: Commons is mostly free, but its licence templates are
# many and a blocklist would let an unusual restrictive one through, and this
# repository is going to be public.
FREE_PREFIXES = ("cc0", "cc by", "cc-by", "public domain", "pd-", "pd ",
                 "gfdl", "fal", "wtfpl", "attribution")
FORBIDDEN = ("nc", "nd", "non-commercial", "noncommercial", "no derivative",
             "fair", "all rights reserved", "copyright", "©", "with permission")


def free_licence(licence):
    """True only for a licence that lets anyone reuse and adapt the file."""
    if not licence:
        return False
    low = licence.lower()
    if any(bad in low.split() or bad in low for bad in FORBIDDEN):
        return False
    return any(low.startswith(p) for p in FREE_PREFIXES)


def commons_file(file_title):
    """URL, author and licence for a file — but only if Commons hosts it."""
    data = get(COMMONS, {
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "imageinfo", "iiprop": "url|extmetadata",
        "titles": file_title,
    })
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        return None                      # not on Commons → assume non-free
    info = (pages[0].get("imageinfo") or [{}])[0]
    meta = info.get("extmetadata", {})

    def field(key):
        return (meta.get(key, {}).get("value") or "").strip()

    licence = field("LicenseShortName")
    if not free_licence(licence):
        return None

    author = re.sub(r"<[^>]+>", "", field("Artist")).strip()
    return {
        "url": info.get("url"),
        "page": info.get("descriptionurl"),
        "credit": author[:120] or "Unknown",
        "licence": licence,
        "file": file_title,
    }


MAX_BYTES = 25 * 1024 * 1024      # no lead image on Commons is anywhere near this
Image.MAX_IMAGE_PIXELS = 80_000_000   # refuse a decompression bomb outright


def download_image(url):
    """Fetch one image, refusing anything that is not a bounded image file
    served by Wikimedia's own file host."""
    if not url or not url.startswith("https://upload.wikimedia.org/"):
        raise ValueError(f"refusing a non-Wikimedia URL: {url!r}")
    r = requests.get(url, headers={"User-Agent": UA}, timeout=60, stream=True)
    r.raise_for_status()
    ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip()
    if not ctype.startswith("image/"):
        raise ValueError(f"not an image: {ctype!r}")
    buf = io.BytesIO()
    for chunk in r.iter_content(64 * 1024):
        buf.write(chunk)
        if buf.tell() > MAX_BYTES:
            raise ValueError(f"over {MAX_BYTES // 1048576} MB, skipped")
    return buf.getvalue()


def save_sizes(raw, aid):
    if not re.fullmatch(r"[a-z0-9-]+", aid):
        raise ValueError(f"unsafe record id: {aid!r}")
    img = Image.open(io.BytesIO(raw))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    for folder, width in SIZES.items():
        d = os.path.join(OUT, folder) if folder else OUT
        os.makedirs(d, exist_ok=True)
        w = min(width, img.width)
        h = round(img.height * w / img.width)
        img.resize((w, h), Image.LANCZOS).save(
            os.path.join(d, aid + ".webp"), "WEBP",
            quality={"": 72, "thumb": 75, "tiny": 66}[folder], method=6)


def main():
    aircraft = json.load(open(DATA, encoding="utf-8"))["aircraft"]
    index = {"photos": {}, "missing": []}
    if os.path.exists(INDEX):
        index = json.load(open(INDEX, encoding="utf-8"))
    index.setdefault("photos", {})
    index.setdefault("missing", [])

    todo = [a for a in aircraft
            if a["id"] not in index["photos"] and a["id"] not in index["missing"]]
    print(f"{len(aircraft)} aircraft, {len(index['photos'])} already have a photo, "
          f"{len(todo)} to try")

    # ask for lead images in batches, then fetch each file's licence one by one
    by_title = {}
    for a in todo:
        by_title.setdefault(a.get("wiki") or a["model"], []).append(a)

    titles = list(by_title)
    found = {}
    for i in range(0, len(titles), BATCH):
        chunk = titles[i:i + BATCH]
        try:
            found.update(lead_images(chunk))
        except Exception as e:                       # noqa: BLE001
            print(f"  ! batch {i // BATCH}: {e}")
        print(f"  lead images: {min(i + BATCH, len(titles))}/{len(titles)}", end="\r")
    print()

    done = fail = 0
    for title, records in by_title.items():
        file_title = found.get(title)
        meta = None
        if file_title:
            try:
                meta = commons_file(file_title)
            except Exception as e:                   # noqa: BLE001
                print(f"  ! {title}: {e}")
        if not meta:
            for a in records:
                index["missing"].append(a["id"])
            fail += len(records)
            continue
        try:
            raw = download_image(meta["url"])
            time.sleep(PAUSE)
        except Exception as e:                       # noqa: BLE001
            print(f"  ! download {title}: {e}")
            fail += len(records)
            continue
        for a in records:
            try:
                save_sizes(raw, a["id"])
                index["photos"][a["id"]] = {k: meta[k] for k in
                                            ("credit", "licence", "file", "page")}
                done += 1
            except Exception as e:                   # noqa: BLE001
                print(f"  ! encode {a['id']}: {e}")
                fail += 1
        print(f"  photos: {done} saved, {fail} without a free image", end="\r")

        if done % 25 == 0:
            json.dump(index, open(INDEX, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
    print()

    json.dump(index, open(INDEX, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    size = sum(os.path.getsize(os.path.join(dp, f))
               for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"done — {len(index['photos'])} photos in assets/photos/ "
          f"({size / 1048576:.0f} MB), "
          f"{len(index['missing'])} aircraft without a free image")
    print("now run:  python3 scripts/build_single.py")


if __name__ == "__main__":
    main()
