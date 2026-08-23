#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checks on the built database. Run after build_data.py:

    python3 scripts/test_build.py

Exits non-zero on the first failure, so it works as a CI gate. These are the
invariants that have actually been violated at some point during the project,
not a wish list — every check here caught a real bug.
"""

import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "aircraft.json"), encoding="utf-8"))
AIRCRAFT = DATA["aircraft"]

FAILURES = []


def check(name, bad, fmt=lambda x: x):
    if bad:
        FAILURES.append((name, [fmt(b) for b in list(bad)[:8]], len(bad)))
        print(f"  FAIL  {name}: {len(bad)}")
    else:
        print(f"  ok    {name}")


print(f"{len(AIRCRAFT)} records\n")

# --- identity ---------------------------------------------------------------
ids = [a["id"] for a in AIRCRAFT]
check("ids are unique", [i for i, n in collections.Counter(ids).items() if n > 1])
check("ids are url-safe", [i for i in ids if not re.fullmatch(r"[a-z0-9-]+", i)])
names = [(a["mfr"].lower(), a["model"].lower()) for a in AIRCRAFT]
check("no duplicate manufacturer+model",
      [k for k, n in collections.Counter(names).items() if n > 1])

# --- vocabulary -------------------------------------------------------------
CIVIL = {"narrowbody", "widebody", "regional", "turboprop", "freighter", "piston", "helicopter"}
MIL = {"fighter", "bomber", "attack", "transport", "trainer", "recon", "maritime",
       "tanker", "awacs", "utility", "helicopter", "uav"}
check("type matches category",
      [a["id"] for a in AIRCRAFT
       if a["type"] not in (CIVIL if a["category"] == "civil" else MIL)])
check("engineKind is known",
      [a["id"] for a in AIRCRAFT
       if a["engineKind"] not in {"jet", "turboprop", "turboshaft", "piston", "rocket", "electric"}])
check("status is known",
      [a["id"] for a in AIRCRAFT
       if a["status"] not in {"production", "active", "retired", "development"}])

# --- numbers ----------------------------------------------------------------
def positive(field):
    return [a["id"] for a in AIRCRAFT
            if a.get(field) is not None and not (isinstance(a[field], (int, float)) and a[field] > 0)]

for f in ("rangeKm", "speedKmh", "mtowKg", "lengthM", "spanM", "heightM", "ceilingM", "built"):
    check(f"{f} is a positive number", positive(f))

check("crew is a non-negative integer",
      [a["id"] for a in AIRCRAFT
       if a.get("crew") is not None and not (isinstance(a["crew"], int) and a["crew"] >= 0)])
check("years are plausible",
      [a["id"] for a in AIRCRAFT
       for y in (a.get("firstFlight"), a.get("introduced"))
       if y is not None and not 1900 < y < 2035])
check("service entry is not before first flight",
      [a["id"] for a in AIRCRAFT
       if a.get("firstFlight") and a.get("introduced") and a["introduced"] < a["firstFlight"]])

# --- physics sanity ---------------------------------------------------------
check("piston aircraft are not supersonic",
      [a["id"] for a in AIRCRAFT
       if a["engineKind"] == "piston" and (a.get("speedKmh") or 0) > 800])
check("no jets before the jet age",
      [a["id"] for a in AIRCRAFT
       if a["engineKind"] == "jet" and (a.get("firstFlight") or 9999) < 1939])
check("ceilings are below the stratosphere limit",
      [a["id"] for a in AIRCRAFT if (a.get("ceilingM") or 0) > 30000])
check("speeds are below Mach 3.5",
      [a["id"] for a in AIRCRAFT if (a.get("speedKmh") or 0) > 4300])

# --- shape by category ------------------------------------------------------
check("military records carry a role",
      [a["id"] for a in AIRCRAFT if a["category"] == "military" and not a.get("role")])
check("uncrewed aircraft have crew 0",
      [a["id"] for a in AIRCRAFT if a["type"] == "uav" and a.get("crew") != 0])
check("airliners have a seat count",
      [a["id"] for a in AIRCRAFT
       if a["type"] in ("narrowbody", "widebody") and not a.get("seatsTypical")])

# --- bilingual completeness -------------------------------------------------
check("every note has an English twin",
      [a["id"] for a in AIRCRAFT if a.get("notes") and not a.get("notes_en")])
check("every role has an English twin",
      [a["id"] for a in AIRCRAFT if a.get("role") and not a.get("role_en")])
check("every armament has an English twin",
      [a["id"] for a in AIRCRAFT if a.get("armament") and not a.get("armament_en")])
check("no Persian text leaked into an English field",
      [a["id"] for a in AIRCRAFT
       for f in ("notes_en", "role_en", "armament_en")
       if a.get(f) and re.search(r"[؀-ۿ]", a[f])])
check("no English text left in a Persian note",
      [a["id"] for a in AIRCRAFT
       if a.get("notes") and not re.search(r"[؀-ۿ]", a["notes"])])

# --- interface contract -----------------------------------------------------
i18n = open(os.path.join(ROOT, "assets", "i18n.js"), encoding="utf-8").read()
check("every type has a label in both languages",
      [a["type"] for a in AIRCRAFT if f"{a['type']}:" not in i18n and f'"{a["type"]}"' not in i18n])
check("every country has an English name",
      sorted({a["country"] for a in AIRCRAFT if f'"{a["country"]}"' not in i18n}))
check("family-total flag only where a count exists",
      [a["id"] for a in AIRCRAFT if a.get("builtFamily") and a.get("built") is None])
check("wiki title is present", [a["id"] for a in AIRCRAFT if not a.get("wiki")])

print()
if FAILURES:
    print(f"{len(FAILURES)} check(s) failed\n")
    for name, sample, n in FAILURES:
        print(f"  {name} ({n})")
        for s in sample:
            print(f"      {s}")
    sys.exit(1)
print("all checks passed")
