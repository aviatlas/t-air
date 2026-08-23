# -*- coding: utf-8 -*-
"""Service ceilings and production totals for rotorcraft, uncrewed aircraft,
trainers and the remaining transports.

Ceilings are the published service ceiling, not the hover ceiling out of
ground effect — the two differ sharply for helicopters and mixing them would
make the figures meaningless. Where a type's production is only ever quoted
for the whole family, the id is listed in FAMILY_COUNT and the interface
marks the number so a reader is not misled. Anything genuinely unpublished
is left out; several Iranian and Chinese types are in that position.
"""

FIXES = {
    # ---- helicopter service ceilings --------------------------------------
    "bell-uh-1h":           {"ceilingM": 5910, "built": 7013},
    "bell-ah-1j":           {"ceilingM": 3215, "built": 271},
    "bell-ah-1z":           {"ceilingM": 6100, "built": 189},
    "bell-206-oh-58":       {"ceilingM": 4575, "built": 2200},
    "bell-214a":            {"ceilingM": 4900},
    "boeing-ah-64d":        {"ceilingM": 6400, "built": 2400},
    "boeing-ch-47f":        {"ceilingM": 6100, "built": 1200},
    "boeing-ch-46":         {"ceilingM": 4265},
    "sikorsky-uh-60m":      {"ceilingM": 5790, "built": 5000},
    "sikorsky-mh-60r":      {"ceilingM": 3580, "built": 300},
    "sikorsky-ch-53e":      {"ceilingM": 5640},
    "sikorsky-ch-53k":      {"ceilingM": 4380, "built": 27},
    "sikorsky-sh-3":        {"ceilingM": 4480, "built": 1300},
    "mcdonnell-md-500":     {"ceilingM": 4877, "built": 4700},
    "bell-boeing-v-22":     {"ceilingM": 7620},
    "mil-mi-2":             {"ceilingM": 4000},
    "mil-mi-6":             {"ceilingM": 4500},
    "mil-mi-8":             {"ceilingM": 4500, "built": 17000},
    "mil-mi-17":            {"ceilingM": 6000},
    "mil-mi-24v":           {"ceilingM": 4500, "built": 2600},
    "mil-mi-26":            {"ceilingM": 4600, "built": 320},
    "mil-mi-28n":           {"ceilingM": 5700, "built": 130},
    "kamov-ka-27":          {"ceilingM": 5000, "built": 267},
    "kamov-ka-50":          {"ceilingM": 5500, "built": 15},
    "kamov-ka-52":          {"ceilingM": 5500, "built": 150},
    "westland-lynx":        {"ceilingM": 3230},
    "westland-sea-king":    {"ceilingM": 3050},
    "leonardo-aw101":       {"ceilingM": 4575, "built": 230},
    "airbus-sa330-puma":    {"ceilingM": 4800},
    "airbus-h225m":         {"ceilingM": 6095},
    "airbus-sa342-gazelle": {"ceilingM": 5000, "built": 1775},
    "airbus-tiger":         {"ceilingM": 4000, "built": 180},
    "nhindustries-nh90":    {"ceilingM": 6000, "built": 500},
    "leonardo-a129":        {"ceilingM": 4725},
    "airbus-bo-105":        {"ceilingM": 5180},
    "airbus-alouette-iii":  {"ceilingM": 3200},
    "changhe-z-10":         {"ceilingM": 6400},
    "harbin-z-9":           {"ceilingM": 4500},
    "harbin-z-19":          {"ceilingM": 6000},
    "hal-dhruv":            {"ceilingM": 6000, "built": 400},
    "hal-prachand":         {"ceilingM": 6500, "built": 15},
    "kai-kuh-1":            {"ceilingM": 4600, "built": 200},

    # ---- civil helicopter production --------------------------------------
    "bell-407":             {"built": 1600},
    "bell-412":             {"built": 900},
    "robinson-r66":         {"built": 1200},
    "airbus-h125":          {"built": 6000},
    "airbus-h135":          {"built": 1400},
    "airbus-h145":          {"built": 1600},
    "leonardo-aw139":       {"built": 1200},
    "sikorsky-s-76":        {"built": 875},
    "sikorsky-s-92":        {"built": 300},
    "kamov-ka-32":          {"built": 170},
    "mdhelicopters-md-902": {"built": 120},

    # ---- uncrewed aircraft ------------------------------------------------
    "ga-mq-1":              {"ceilingM": 7620},
    "ga-mq-9":              {"ceilingM": 15420, "built": 400},
    "ga-mq-1c":             {"ceilingM": 8840, "built": 200},
    "northrop-rq-4":        {"ceilingM": 18300, "built": 42},
    "northrop-x-47b":       {"ceilingM": 12190},
    "iai-heron":            {"ceilingM": 13700},
    "elbit-hermes-900":     {"ceilingM": 9100},
    "baykar-tb2":           {"ceilingM": 8200, "built": 500},
    "baykar-akinci":        {"ceilingM": 12190},
    "tai-anka":             {"ceilingM": 9145},
    "sukhoi-s-70":          {"ceilingM": 10500},
    "kronshtadt-orion":     {"ceilingM": 7500},
    "caig-wing-loong-ii":   {"ceilingM": 9000},
    "casc-ch-5":            {"ceilingM": 9000},
    "qods-mohajer-6":       {"ceilingM": 5400},
    "qods-ababil-3":        {"ceilingM": 5000},
    "shahed-129":           {"ceilingM": 7300},
    "shahed-149":           {"ceilingM": 10600},
    "iaio-fotros":          {"ceilingM": 7620},
    "hesa-kaman-22":        {"ceilingM": 8000},

    # ---- trainers ---------------------------------------------------------
    "beechcraft-t-34c":       {"built": 353},
    "beechcraft-t-6-texan-ii": {"built": 900},
    "british-aerospace-hawk-t1": {"built": 1000},
    "grob-g-120tp":           {"built": 150},
    "hal-htt-40":             {"built": 6},
    "hongdu-jl-8":            {"built": 1000},
    "hongdu-l-15":            {"built": 100},
    "kai-kt-1":               {"built": 200},
    "kai-t-50":               {"built": 250},
    "leonardo-m-346":         {"built": 100},
    "pilatus-pc-21":          {"built": 250},
    "pzl-130-orlik":          {"built": 50},
    "slingsby-t67-firefly":   {"built": 250},
    "utva-lasta-95":          {"built": 20},
    "zlin-z-242":             {"built": 300},

    # ---- transports, tankers, maritime ------------------------------------
    "airbus-a330-mrtt":     {"built": 60},
    "boeing-kc-46":         {"built": 90},
    "antonov-an-70":        {"built": 5},
    "lockheed-c-130h":      {"built": 1200},
    "boeing-p-8":           {"built": 180},
}

# The number covers the whole family or programme, not this one variant.
FAMILY_COUNT = [
    "bell-206-oh-58",     # every OH-58 built
    "boeing-ah-64d",      # every Apache
    "boeing-ch-47f",      # every Chinook
    "sikorsky-uh-60m",    # every Black Hawk
    "sikorsky-sh-3",      # every S-61
    "mcdonnell-md-500",   # Model 500 and OH-6 together
    "mil-mi-8",           # Mi-8 and Mi-17 together
    "mil-mi-24v",         # Mi-24, Mi-25 and Mi-35 together
    "leonardo-aw101",     # every AW101
    "airbus-sa342-gazelle",
    "airbus-tiger",
    "nhindustries-nh90",
    "hal-dhruv",
    "kai-kuh-1",
    "bell-412",           # every 412
    "airbus-h125",        # the whole AS350 line
    "airbus-h145",        # BK117 and H145 together
    "sikorsky-s-76",
    "beechcraft-t-6-texan-ii",
    "british-aerospace-hawk-t1",
    "hongdu-jl-8",        # JL-8 and K-8 together
    "kai-t-50",           # the whole T-50 family including FA-50
    "lockheed-c-130h",    # every C-130H
]

UNRESOLVED = [
    "mil-mi-17: production is folded into the Mi-8 total everywhere",
    "changhe-z-10 / harbin-z-9 / harbin-z-19: only inventory estimates are public",
    "hesa-shabaviz-2-75, panha-toufan: no production figure published",
    "lockheed-rq-170, boeing-mq-25, hongdu-gj-11: classified or pre-production",
    "iai-heron, elbit-hermes-900, baykar-akinci, tai-anka: makers do not publish totals",
    "sukhoi-s-70, kronshtadt-orion, caig-wing-loong-ii, casc-ch-5: no reliable count",
    "all Iranian UAVs: announced but never quantified",
    "hesa-dorna, hesa-shafaq, hesa-yasin, owj-tazarve, iriaf-parastu-14: unpublished",
    "cessna-t-41: shares its line with the civil Cessna 172",
    "lockheed-ac-130: conversions from C-130 airframes, counted differently by source",
    "boeing-707-tanker, hesa-simorgh: conversion or pre-production programmes",
    "mikoyan-mig-29ub: counted within MiG-29 production",
]
