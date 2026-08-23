# -*- coding: utf-8 -*-
"""Production totals for civil aircraft — deliveries per variant where a source
records the variant, family or programme totals (flagged) where only the
programme figure exists, and nothing where no figure is public.

Method. For every type the English Wikipedia article named in the record's
`wiki` field was read, plus the dedicated orders-and-deliveries lists where one
exists (A320 family, A220, A330neo, A350, 787, 777). Airliner figures are
*deliveries*, not orders. For lines still open the most recent documented
delivery figure is used and its date is given in the comment; delivery rates
were never extrapolated forward.

As-of dates are not uniform, because the sources are not: the Airbus and Boeing
in-production types are current to May 2026 / January–March 2026, the closed
lines carry their final totals, and a handful of slow-moving types (ATR 72-600,
the Airbus and Sikorsky helicopters) carry the last figure their manufacturer
published, which is older. Each comment says which.

Three rules decided the hard cases:

* Fleet and in-service counts are not production counts. Several types — the
  H125, the Mi-8, the Chinese types — have no public build total, only an
  operational inventory. Those were not converted into `built`.
* Where a source gives only the programme total, that total is recorded and the
  id is listed in FAMILY_COUNT so the interface can mark it. This is the case
  for every ATR 42 variant, the A320ceo/A321ceo records, the 737 MAX records
  and most of the helicopters.
* Aircraft with no deliveries yet (A350F, 777-8/-9, MAX 7/10, E175-E2, MC-21,
  SJ-100) are left out entirely. Test and pre-delivery airframes exist for all
  of them but no manufacturer publishes them as a build count.

Caveat on coverage: the fetch quota for this session ran out partway through,
so the last group of types below could not be checked against a source and was
left unresolved rather than filled from memory. They are marked as such in
UNRESOLVED and are all straightforward to fill on a second pass.
"""

FIXES = {
    # ---- ATR -------------------------------------------------------------
    # The ATR 42 article gives a programme total (503) and no split by series,
    # so both -500 and -600 carry it, flagged.
    "atr-42-500": {"built": 503},
    "atr-42-600": {"built": 503},
    "atr-72-500": {"built": 365},   # -500 deliveries; the line closed, so final
    "atr-72-600": {"built": 444},   # delivered by Sept 2018; the line has run on since

    # ---- Airbus, closed lines -------------------------------------------
    "airbus-a300b2": {"built": 61},       # B2-100 32 + B2-200 25 + B2-320 4
    "airbus-a300-600r": {"built": 313},   # all A300-600 versions, flagged below
    "airbus-a310-200": {"built": 255},    # family total, flagged below
    "airbus-a319": {"built": 1484},       # A319ceo delivered, Aug 2025 (1,518 incl. neo)
    "airbus-a320-200": {"built": 4745},   # A320ceo, flagged below
    "airbus-a321-200": {"built": 1791},   # A321ceo, flagged below
    "airbus-a330-200": {"built": 661},    # delivered as of April 2024
    "airbus-a330-300": {"built": 771},    # delivered as of December 2020

    # ---- Airbus, in production ------------------------------------------
    "airbus-a220-100": {"built": 74},      # deliveries to January 2026
    "airbus-a220-300": {"built": 411},     # deliveries to January 2026
    "airbus-a319neo": {"built": 43},       # deliveries to May 2026
    "airbus-a320neo": {"built": 2403},     # deliveries to May 2026
    "airbus-a321neo": {"built": 2124},     # to May 2026; incl. LR/XLR, flagged below
    "airbus-a330-800neo": {"built": 8},    # deliveries to May 2026
    "airbus-a330-900neo": {"built": 187},  # deliveries to May 2026
    "airbus-a350-900": {"built": 609},     # deliveries to May 2026
    "airbus-a350-1000": {"built": 114},    # deliveries to May 2026

    # ---- Boeing ----------------------------------------------------------
    "boeing-737-max-8": {"built": 2233},   # whole MAX programme, flagged below
    "boeing-737-max-9": {"built": 2233},   # whole MAX programme, flagged below
    "boeing-777-300er": {"built": 832},    # deliveries to January 2026
    "boeing-777f": {"built": 297},         # deliveries to January 2026
    "boeing-787-8": {"built": 399},        # deliveries to mid-2025
    "boeing-787-9": {"built": 736},        # deliveries to mid-2025
    "boeing-787-10": {"built": 141},       # deliveries to mid-2025

    # ---- Regional jets ---------------------------------------------------
    "bombardier-crj200": {"built": 709},   # CRJ200 alone; 226 CRJ100 and 86 CRJ440 besides
    "bombardier-crj700": {"built": 330},   # CRJ700 airframes; the CRJ550s are conversions of these
    "bombardier-crj900": {"built": 487},   # to the programme's close, Feb 2021
    "bombardier-crj1000": {"built": 63},   # to the programme's close, Feb 2021
    "embraer-e170": {"built": 191},        # production ended 2017
    "embraer-e175": {"built": 819},        # delivered by June 2025; still in production
    "embraer-e190": {"built": 568},        # E190 alone
    "embraer-e195": {"built": 172},        # E195 alone
    "embraer-e190-e2": {"built": 33},      # deliveries to 27 January 2026
    "embraer-e195-e2": {"built": 166},     # deliveries to 27 January 2026
    "embraer-erj-145": {"built": 1231},    # whole ERJ programme, flagged below

    # ---- Turboprops ------------------------------------------------------
    "dehavilland-dash8-300": {"built": 267},    # Series 300 alone
    "dehavilland-dash8-q400": {"built": 587},   # Series 400 delivered through 2018
    "dhc-6-twin-otter": {"built": 614},         # Series 300 alone; 844 DHC-6 in all
    "dornier-228": {"built": 270},              # German-built 228s, flagged below
    "harbin-y-12": {"built": 200},              # family total, flagged below
    "let-l-410": {"built": 1200},               # family total, flagged below
    "britten-norman-islander": {"built": 1300},  # all BN-2 Islanders since 1965
    "antonov-an-140": {"built": 36},            # Kharkiv, Samara and HESA output together

    # ---- Helicopters -----------------------------------------------------
    "airbus-h125": {"built": 3590},      # AS350/AS550 as of 2009, flagged below
    "airbus-h135": {"built": 1400},      # 1,400th delivered September 2020
    "airbus-h145": {"built": 1600},      # H145 family incl. BK 117, flagged below
    "bell-407": {"built": 1600},         # produced by February 2023
    "bell-412": {"built": 1300},         # all 412 variants, flagged below
    "leonardo-aw139": {"built": 1200},   # produced by July 2024
    "sikorsky-s-76": {"built": 875},     # all S-76 marks, flagged below
    "sikorsky-s-92": {"built": 300},     # 300th delivered Feb 2018; documented floor
    "robinson-r66": {"built": 1500},     # produced by early 2024
    "kamov-ka-32": {"built": 160},       # all Ka-32 modifications, flagged below
    "mil-mi-8t-civil": {"built": 17000},  # whole Mi-8/Mi-17 line, flagged below

    # ---- Chinese programmes ----------------------------------------------
    # COMAC publishes milestones, not running totals; both figures are floors.
    "comac-arj21-700": {"built": 100},   # 100th delivered Dec 2022; the line has run on since
    "comac-c919": {"built": 16},         # delivered by the end of 2024

    # ---- Historic types --------------------------------------------------
    "bac-one-eleven-500": {"built": 244},          # whole One-Eleven programme, flagged below
    "hawker-siddeley-trident-1c": {"built": 24},   # the BEA order; 117 Tridents in all
    "sud-aviation-caravelle-3": {"built": 78},     # Caravelle III alone; 282 Caravelles in all
    "vickers-vc10": {"built": 54},                 # standard and Super VC10 together
    "tupolev-tu-154m": {"built": 320},             # Tu-154M alone; 1,026 Tu-154s in all
}

FAMILY_COUNT = [
    "atr-42-500",          # 503 is every ATR 42; the article does not split the series
    "atr-42-600",          # 503 is every ATR 42
    "airbus-a300-600r",    # 313 covers -600, -600R, -600F and -600RF together
    "airbus-a310-200",     # 255 is every A310; the -200/-300 split is not published
    "airbus-a320-200",     # 4,745 is the A320ceo, -100 and -200 together (21 were -100s)
    "airbus-a321-200",     # 1,791 is the A321ceo, -100 and -200 together
    "airbus-a321neo",      # 2,124 includes the A321LR and A321XLR, which Airbus does not split out
    "boeing-737-max-8",    # 2,233 is every 737 MAX built; the MAX 8 is the large majority
    "boeing-737-max-9",    # 2,233 is every 737 MAX built; the MAX 9 is a small part of it
    "embraer-erj-145",     # 1,231 is every ERJ 135/140/145 plus the Legacy 600/650 derivatives
    "dornier-228",         # 270 is Dornier's own output; HAL and RUAG built more
    "harbin-y-12",         # 200+ covers every Y-12 mark, not the Y-12 IV alone
    "let-l-410",           # 1,200+ covers every L-410 variant
    "bac-one-eleven-500",  # 244 is every One-Eleven, Romanian Rombac output included
    "airbus-h125",         # 3,590 is the AS350/AS550 total as of 2009, the last published build count
    "airbus-h145",         # 1,600 is the whole H145 family, early BK 117s included
    "bell-412",            # 1,300 is every Bell 412, not the 412EPI alone
    "sikorsky-s-76",       # 875 is every S-76 mark, not the S-76D alone
    "kamov-ka-32",         # 160 covers all Ka-32 modifications, not the Ka-32A11BC alone
    "mil-mi-8t-civil",     # 17,000+ is the whole Mi-8/Mi-17 line, military output included
]

UNRESOLVED = [
    # -- no deliveries yet, and no published airframe count --------------
    "airbus-a350f: not yet delivered; Airbus publishes no count of airframes assembled",
    "boeing-737-max-7: not certified, no deliveries; the undelivered airframes are not published as a total",
    "boeing-737-max-10: not certified, no deliveries; same",
    "boeing-777-8: no deliveries; no build count published",
    "boeing-777-9: no deliveries; the flight-test fleet and the stored airframes are not published as a total",
    "embraer-e175-e2: programme deferred to 2027-28, nothing delivered",
    "irkut-mc-21-300: serial deliveries not begun; sources disagree on the prototype count",
    "yakovlev-sj-100: import-substituted SJ-100 still in flight test, nothing delivered",

    # -- figure exists only at a level the record does not describe -------
    "airbus-a321lr: Airbus reports LR deliveries inside the A321neo total, never separately",
    "airbus-a321xlr: same — no separate XLR delivery figure is published",
    "bombardier-crj550: converted from in-service CRJ700s rather than newly built; no production total exists",
    "mdhelicopters-md-902: MD Helicopters never published an MD 900/902 production total",
    "fairchild-metro-iii: SA226/SA227 sources merge the Metro airliners with the Merlin corporate versions; no clean Metro III figure",

    # -- not checked before the session's fetch quota ran out -------------
    # All of these have published figures; none was verified, so none was written.
    "boeing-767-300f: Boeing splits -300F from -300ER in its model summary, but the figure was not verified",
    "ilyushin-il-96-300: Il-96 totals are small and variously quoted; not verified",
    "ilyushin-il-96-400t: same",
    "sukhoi-ssj100: build totals quoted between roughly 220 and 240; not verified",
    "tupolev-tu-204-100: no verified split between -100, -300 and Tu-214 within the ~90-aircraft family",
    "tupolev-tu-204-300: same",
    "tupolev-tu-214: same",
    "xian-ma60: quoted as '100+' with no verified exact figure",
    "de-havilland-comet-1: Comet 1 and 1A counts vary by source and were not verified; 114 is every Comet mark",
]
