# -*- coding: utf-8 -*-
"""Production totals for fighters, attack aircraft and bombers — variant figures
where a source records the variant, family totals (flagged) where only the
programme total is documented, and nothing at all where no figure is public.

Sources are the English Wikipedia article named in each record's `wiki` field,
checked against the manufacturer or a specialist reference where the article
splits variants poorly (Hawker Hurricane marks, F-4D, Me 210, IAR 80,
Nieuport 17) or where a still-open production line has moved on since the
article's last figure (Typhoon, F-15EX, F-35, Rafale, Super Hornet).

Two rules decided the hard cases:

* A figure is only recorded when a source presents it as aircraft *built*.
  In-service inventory counts — the only public numbers for several Chinese
  types — are not production totals and were left out rather than converted.
* Where a still-current line has no recent total, the most recent documented
  figure is used and its date noted, rather than extrapolating from delivery
  rates.
"""

FIXES = {
    # ---- First World War -------------------------------------------------
    "albatros-d-iii": {"built": 1866},        # infobox; Albatros + OAW + Oeffag
    "bristol-f2b": {"built": 5329},           # family total, flagged below
    "fokker-d-vii": {"built": 3300},          # "around 3,300 ... in the second half of 1918"
    "nieuport-17": {"built": 3600},           # French records incomplete; 3,600 is the published estimate

    # ---- Interwar and Second World War -----------------------------------
    "fiat-cr42": {"built": 1819},             # "most likely estimate ... 1,819", incl. 63 CR.42LW and 140 export
    "fiat-g50": {"built": 784},               # 426 Fiat + 358 CMASA
    "focke-wulf-fw-190a": {"built": 6655},    # A-8 alone; 13,291 is the whole A-model line
    "focke-wulf-ta-152h": {"built": 69},      # family total, flagged below
    "fokker-d-xxi": {"built": 148},           # Netherlands + Finland + Denmark
    "hawker-hurricane-mk-i": {"built": 14487},  # family total, flagged below
    "hawker-hurricane-mk-iic": {"built": 4711},  # built or converted from IIA/IIB
    "iar-80": {"built": 346},                 # family total, flagged below
    "junkers-ju-87d": {"built": 3300},        # family total (D series), flagged below
    "kawanishi-n1k2-j": {"built": 415},       # N1K2-J alone; 1,532 is every N1K
    "macchi-c200": {"built": 1153},           # Macchi 397 + Breda 556 + SAI 200
    "macchi-c202": {"built": 1106},           # Breda 649 + Aermacchi 390 + SAI 67
    "messerschmitt-bf-109e": {"built": 561},  # all E-4 sub-versions
    "messerschmitt-bf-109f": {"built": 1841},  # all F-4 variants, May 1941 – May 1942
    "messerschmitt-bf-109g": {"built": 12000},  # G-6 series, March 1943 to war's end
    "messerschmitt-bf-109k": {"built": 1593},  # K-4 deliveries to March 1945
    "messerschmitt-bf-110": {"built": 2293},  # G-4 night fighter alone; 6,170 is every Bf 110
    "messerschmitt-me-210": {"built": 352},   # family total (German production), flagged below
    "mitsubishi-a6m2": {"built": 10939},      # family total, flagged below
    "mitsubishi-a6m5": {"built": 10939},      # family total, flagged below
    "pzl-p11c": {"built": 150},               # P.11c alone; ~344 across all P.11 marks

    # ---- Cold War --------------------------------------------------------
    "hawker-siddeley-harrier-gr3": {"built": 122},   # family total, flagged below
    "mcdonnell-douglas-f-4d": {"built": 825},        # F-4D alone; 5,195 is every Phantom II
    "mcdonnell-douglas-f-15c": {"built": 483},       # F-15C alone, 1979–1985
    "mcdonnell-douglas-f-15e": {"built": 236},       # USAF F-15E through 2001; 435 incl. F-15I/S/K/SG
    "mikoyan-mig-29a": {"built": 1600},              # family total, flagged below
    "northrop-f-5e": {"built": 792},                 # Northrop-built F-5E; licence output in CH/KR/TW additional
    "northrop-f-5f": {"built": 146},                 # Northrop-built F-5F
    "general-dynamics-f-16c": {"built": 4600},       # family total, flagged below
    "british-aerospace-harrier-gr7": {"built": 143},  # family total, flagged below

    # ---- In production or recently ended ---------------------------------
    "boeing-f-15ex": {"built": 17},           # delivered to the USAF as of early 2026
    "boeing-fa-18e": {"built": 600},          # family total, flagged below
    "dassault-rafale-c": {"built": 300},      # family total, flagged below
    "embraer-emb-314": {"built": 260},        # April 2023
    "eurofighter-typhoon": {"built": 613},    # delivered as of September 2025
    "kai-fa-50": {"built": 292},              # family total, flagged below
    "lockheed-martin-f-35a": {"built": 797},  # F-35A delivered by end of 2024
    "lockheed-martin-f-35b": {"built": 203},  # F-35B delivered by end of 2024
    "pac-jf-17": {"built": 201},              # plus 6 prototypes, all blocks
    "saab-jas-39c": {"built": 280},           # family total, flagged below
    "shenyang-j-11b": {"built": 440},         # family total, flagged below
    "shenyang-j-15": {"built": 76},           # all J-15/J-15T/J-15D; documented floor
    "shenyang-j-16": {"built": 450},          # serial-number analysis, September 2025
    "chengdu-j-20": {"built": 300},           # open-source estimate, September 2025; China publishes nothing
    "sukhoi-su-30sm": {"built": 630},         # family total, flagged below
    "sukhoi-su-34": {"built": 153},           # at least 153 by December 2022; the line has run on since
    "sukhoi-su-35s": {"built": 155},          # Su-35S, 2007–present
    "sukhoi-su-57": {"built": 25},            # ~13 prototypes + ~12 serial; estimates run 20–30

    # ---- Prototypes and demonstrators (airframes flown) ------------------
    "kai-kf-21": {"built": 6},                # six prototypes flown 2022–2023; deliveries start late 2026
    "northrop-b-21": {"built": 2},            # T-1 flew Nov 2023, second airframe Sept 2025; a third in ground test
}

FAMILY_COUNT = [
    "bristol-f2b",                   # 5,329 is every Bristol Fighter, incl. the 52 F.2A
    "focke-wulf-ta-152h",            # 69 is every Ta 152; Rodeike splits it 44 H-0/V + 25 H-1
    "hawker-hurricane-mk-i",         # 14,487 is every Hurricane; the marks are not split by source
    "iar-80",                        # 346 covers IAR 80 and IAR 81 together
    "junkers-ju-87d",                # 3,300 is the whole D series; 6,000 is every Ju 87
    "messerschmitt-me-210",          # 352 is all German Me 210 output; 267 more built in Hungary
    "mitsubishi-a6m2",               # 10,939 is every A6M — the variant split is not reliably sourced
    "mitsubishi-a6m5",               # 10,939 is every A6M
    "hawker-siddeley-harrier-gr3",   # 122 is the RAF GR.1/GR.3 line, not GR.3 alone
    "british-aerospace-harrier-gr7",  # 143 is every British Harrier II (GR5/GR7/GR9 and T.10)
    "mikoyan-mig-29a",               # 1,600+ covers every MiG-29 variant
    "general-dynamics-f-16c",        # 4,600+ is every F-16; the C is not counted separately
    "boeing-fa-18e",                 # 600+ covers single-seat E and two-seat F together
    "dassault-rafale-c",             # 300 is every Rafale B/C/M, produced by October 2025
    "kai-fa-50",                     # 292 is the whole T-50 family, trainers included
    "saab-jas-39c",                  # 280+ is every Gripen A–F delivered as of 2025
    "shenyang-j-11b",                # 440 is every J-11/J-11A/J-11B, approx. as of 2019
    "sukhoi-su-30sm",                # 630+ is every Su-30, as of 2019
]

UNRESOLVED = [
    "chengdu-j-10a: no production figure published; only PLAAF inventory estimates exist",
    "chengdu-j-10c: same — inventory counts are not build counts",
    "shenyang-j-8ii: no J-8B/J-8II production total in any open source",
    "shenyang-j-35: serial output undisclosed; even the prototype count is only 'at least five'",
    "xian-h-6k: H-6K output never disclosed; published figures are aircraft in service",
    "xian-jh-7a: same — 110–120 in service (2025) is inventory, not production",
    "iaio-qaher-313: Iran publishes nothing, and the airframes shown are unverified",
    "hal-tejas-mk1a: deliveries only beginning; the 38 built are Mk1, a different variant",
    "mikoyan-mig-29smt: new-build and converted SMTs are not separated in any source",
    "mikoyan-mig-35: no total published; Russian orders were repeatedly cut",
    "saab-jas-39e: deliveries to Sweden and Brazil under way, no reliable running total",
]
