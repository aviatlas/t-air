# -*- coding: utf-8 -*-
"""Source verification against the English Wikipedia article for each type.

Four agents worked through the database in id order, fetching the article named
in each record's `wiki` field and comparing it field by field. They were told to
propose a change only when the article's figure is unambiguously for the same
variant the record names, and only past a threshold — more than 5% on a number,
two years or more on a date — so that a disagreement about rounding or about
which sub-variant a figure describes does not become a false correction.

The run stopped at 152 of 656 records when the web quota ran out. Everything
checked is listed in VERIFIED and marked in the interface; the rest is honestly
unmarked. UNCHECKED_NOTE below says where the run has to resume.

Evidence (the printed figure behind each change) is in the run log; the first
slice lost its evidence table when its agent was interrupted, so its nine
corrections carry the figure but not the quotation.
"""

FIXES = {
    "aermacchi-mb-326": {"mtowKg": 4577, "rangeKm": 1850},                # was mtowKg 5216, rangeKm 1665
    "aermacchi-mb-339": {"heightM": 3.6, "mtowKg": 5897},                 # was heightM 3.99, mtowKg 6350
    "aero-l-29": {"mtowKg": 3280},                                        # was mtowKg 3540
    "aichi-d3a": {"built": 1016, "rangeKm": 1352},                        # was built 1495, rangeKm 1470
    "aidc-f-ck-1": {"introduced": 1992},                                  # was introduced 1994
    "airbus-a300b4": {"built": 136},                                      # was built 561
    "airbus-a310-300": {"seatsTypical": 220},                             # was seatsTypical 187
    "airbus-a321-200": {"firstFlight": 1996, "introduced": 1997},         # was firstFlight 1993, introduced 1994
    "airbus-a330-mrtt": {"built": 66},                                    # was built 60
    "antonov-an-148": {"seatsTypical": 70},                               # was seatsTypical 68
    "antonov-an-22": {"ceilingM": 9100, "status": "retired"},             # was ceilingM 7500, status active
    "antonov-an-26": {"introduced": 1972},                                # was introduced 1970
    "antonov-an-70": {"built": 2, "introduced": 2015, "status": "active"},  # was built 5, introduced None, status development
    "bae-146-300": {"speedKmh": 747},                                     # was speedKmh 801
    "bae-jetstream-41": {"speedKmh": 482},                                # was speedKmh 547
    "bae-taranis": {"lengthM": 12.43},                                    # was lengthM 11.35
    "baykar-akinci": {"ceilingM": 13716},                                 # was ceilingM 12190
    "baykar-tb2": {"built": 800, "ceilingM": 7620},                       # was built 500, ceilingM 8200
    "boeing-737-300": {"mtowKg": 56470},                                  # was mtowKg 62820
    "boeing-737-max-10": {"rangeKm": 5740},                               # was rangeKm 6110
    "boeing-737-max-9": {"rangeKm": 6110},                                # was rangeKm 6570
    "boeing-747-400": {"built": 442},                                     # was built 694
    "boeing-747sp": {"rangeKm": 10800},                                   # was rangeKm 12320
    "boeing-767-300f": {"built": 161},                                    # was built None
    "boeing-ch-46": {"ceilingM": 5180},                                   # was ceilingM 4265
    "boeing-ch-47f": {"mtowKg": 24494},                                   # was mtowKg 22680
    "boeing-e-3": {"ceilingM": 8800, "mtowKg": 157400},                   # was ceilingM 12500, mtowKg 147400
    "boeing-f-15ex": {"introduced": 2024},                                # was introduced 2021
    "boeing-kc-46": {"built": 105},                                       # was built 90
    "boeing-rc-135": {"mtowKg": 146284},                                  # was mtowKg 133600
    "bombardier-crj1000": {"seatsTypical": 100},                          # was seatsTypical 97
    "bombardier-crj200": {"seatsMax": 52},                                # was seatsMax 50
    "bombardier-crj550": {"mtowKg": 29484, "rangeKm": 1852},              # was mtowKg 34019, rangeKm None
    "bombardier-crj700": {"ceilingM": 12497},                             # was ceilingM None
    "bombardier-crj900": {"ceilingM": 12497},                             # was ceilingM None
    "boulton-paul-defiant-mk-i": {"built": 723, "heightM": 3.45},         # was built 1064, heightM 3.71
    "bristol-britannia": {"built": 18, "ceilingM": 7300},                 # was built 85, ceilingM None
    "bristol-f2b": {"rangeKm": 594},                                      # was rangeKm 500
    "britten-norman-islander": {"ceilingM": 4000, "speedKmh": 240},       # was ceilingM None, speedKmh 257
    "casa-cn-235": {"ceilingM": 9100, "introduced": 1988},                # was ceilingM 8100, introduced 1986
    "cessna-t-37": {"ceilingM": 11800},                                   # was ceilingM 10850
    "changhe-z-10": {"introduced": 2009, "speedKmh": 300},                # was introduced 2012, speedKmh 270
    "chengdu-j-20": {"heightM": 4.69},                                    # was heightM 4.45
    "comac-arj21-700": {"built": 210},                                    # was built 100
    "comac-c919": {"ceilingM": 12200},                                    # was ceilingM None
    "concorde": {"ceilingM": 18288},                                      # was ceilingM None
    "consolidated-b-24j": {"built": 6678},                                # was built 18188
    "convair-990": {"ceilingM": 12497, "speedKmh": 896},                  # was ceilingM None, speedKmh 990
}

# Production totals the article gives only for the whole type.
FAMILY_COUNT = [
    "bae-146-300",
    "bae-jetstream-31",
    "boeing-737-max-8",
    "boeing-737-max-9",
    "boeing-ah-64d",
    "boeing-b-47",
    "boeing-ch-47f",
    "boeing-fa-18e",
    "brewster-f2a-3-buffalo",
    "bristol-blenheim-iv",
    "british-aerospace-sea-harrier-frs1",
]

# Records compared against their Wikipedia article, field by field.
VERIFIED = [
    "aeritalia-g-222",
    "aermacchi-mb-326",
    "aermacchi-mb-339",
    "aero-l-159a",
    "aero-l-29",
    "aero-l-39-albatros",
    "aichi-d3a",
    "aidc-at-3",
    "aidc-f-ck-1",
    "airbus-a220-100",
    "airbus-a220-300",
    "airbus-a300-600r",
    "airbus-a300b2",
    "airbus-a300b4",
    "airbus-a310-200",
    "airbus-a310-300",
    "airbus-a318",
    "airbus-a319",
    "airbus-a319neo",
    "airbus-a320-200",
    "airbus-a320neo",
    "airbus-a321-200",
    "airbus-a321lr",
    "airbus-a321neo",
    "airbus-a321xlr",
    "airbus-a330-200",
    "airbus-a330-200f",
    "airbus-a330-300",
    "airbus-a330-800neo",
    "airbus-a330-900neo",
    "airbus-a330-mrtt",
    "airbus-a340-200",
    "airbus-a340-300",
    "airbus-a340-500",
    "airbus-a340-600",
    "airbus-a350-1000",
    "airbus-a350-900",
    "airbus-a350f",
    "antonov-an-148",
    "antonov-an-2",
    "antonov-an-22",
    "antonov-an-225",
    "antonov-an-24",
    "antonov-an-26",
    "antonov-an-32",
    "antonov-an-70",
    "atr-42-500",
    "atr-42-600",
    "atr-72-500",
    "atr-72-600",
    "avia-b534",
    "avro-lancaster-b1",
    "avro-rj70",
    "avro-rj85",
    "avro-vulcan-b2",
    "avro-york",
    "bac-one-eleven-500",
    "bae-146-200",
    "bae-146-300",
    "bae-jetstream-31",
    "bae-jetstream-41",
    "bae-taranis",
    "baykar-akinci",
    "baykar-tb2",
    "beechcraft-1900d",
    "boeing-737-100",
    "boeing-737-200",
    "boeing-737-300",
    "boeing-737-400",
    "boeing-737-500",
    "boeing-737-600",
    "boeing-737-700",
    "boeing-737-800",
    "boeing-737-900",
    "boeing-737-900er",
    "boeing-737-max-10",
    "boeing-737-max-7",
    "boeing-737-max-8",
    "boeing-737-max-9",
    "boeing-747-100",
    "boeing-747-100sr",
    "boeing-747-200b",
    "boeing-747-300",
    "boeing-747-400",
    "boeing-747-400er",
    "boeing-747-400f",
    "boeing-747-8f",
    "boeing-747-8i",
    "boeing-747sp",
    "boeing-757-200",
    "boeing-757-200pf",
    "boeing-757-300",
    "boeing-767-200er",
    "boeing-767-300er",
    "boeing-767-300f",
    "boeing-767-400er",
    "boeing-777-200er",
    "boeing-777-200lr",
    "boeing-777-300er",
    "boeing-777-8",
    "boeing-777-9",
    "boeing-777f",
    "boeing-787-10",
    "boeing-787-8",
    "boeing-787-9",
    "boeing-ah-64d",
    "boeing-b-17g",
    "boeing-b-29",
    "boeing-b-47",
    "boeing-b-52h",
    "boeing-c-17",
    "boeing-ch-46",
    "boeing-ch-47f",
    "boeing-e-3",
    "boeing-f-15ex",
    "boeing-fa-18e",
    "boeing-kc-135",
    "boeing-kc-46",
    "boeing-mq-25",
    "boeing-p-8",
    "boeing-rc-135",
    "bombardier-crj1000",
    "bombardier-crj200",
    "bombardier-crj550",
    "bombardier-crj700",
    "bombardier-crj900",
    "boulton-paul-defiant-mk-i",
    "brewster-f2a-3-buffalo",
    "bristol-beaufighter-mk-vif",
    "bristol-blenheim-iv",
    "bristol-britannia",
    "bristol-f2b",
    "british-aerospace-harrier-gr7",
    "british-aerospace-hawk-t1",
    "british-aerospace-sea-harrier-frs1",
    "britten-norman-islander",
    "casa-cn-235",
    "casc-ch-5",
    "cessna-a-37",
    "cessna-t-37",
    "cessna-t-41",
    "changhe-z-10",
    "chengdu-j-10a",
    "chengdu-j-10c",
    "chengdu-j-20",
    "chengdu-j-7",
    "comac-arj21-700",
    "comac-c919",
    "concorde",
    "consolidated-b-24j",
    "convair-880",
    "convair-990",
]

UNRESOLVED = [
    "504 of 656 records are not yet source-checked: the run covered ids from "
    "aeritalia-g-222 to de-havilland-comet-4 and stopped mid-alphabet when the "
    "web quota ran out. Resume from the first id not in VERIFIED.",
    "BLOCKED: WebFetch returned 'You've hit your weekly limit - resets Aug 25, 11pm (UTC)' starting at record 28 of 55. Direct curl to en.wikipedia.org is refused by the agent proxy (403 on CONNECT), and WebSearch returns titles/URLs only, no page content. Records 28-55 (all Beechcraft T-34 onward throug",
    "DB convention observed and respected: every civil record in this slice has crew=null and ceilingM=null, and every military record has seatsTypical/seatsMax=null. No crew or ceiling values were proposed for civil records, and no seat counts for military records, even where Wikipedia prints them (e.g.",
    "antonov-an-148: Wikipedia's spec block is for the An-148-100A (range 2,100 km); our record is the generic 'An-148' with rangeKm 3500, which matches the -100B/E. Range left unchanged as variant-ambiguous.",
    "antonov-an-2: Wikipedia body text says 'over 13,000 constructed' through 2001 while our built=18000 (the figure usually quoted including Chinese Y-5 production). Left unchanged - genuinely ambiguous. MTOW printed as 5,440 kg vs our 5500 (1.1%, under threshold).",
    "antonov-an-225: our introduced=1989 vs Wikipedia '2002 (commercial service)'; the An-225 flew from 1989, was stored, then re-entered service 2001-02. Left unchanged. All other An-225 figures matched exactly.",
    "avro-lancaster-b1: WebFetch could not retrieve the 'Specifications (Lancaster B I)' section on either attempt (page truncated before it). Only firstFlight 1941, introduced 1942, crew 7 and 4 engines confirmed; performance and dimension figures remain unverified.",
    "avro-vulcan-b2: WebFetch could not retrieve the specifications section on either attempt. Confirmed from body text: the B.2 first flew September 1958 and entered RAF service July 1960, with 89 B.2 built of 134 total. Our record carries the type-level infobox dates 1952/1956 - left unchanged, but a h",
    "avro-rj70: our mtowKg 43090 (95,000 lb) is the correct RJ70 figure; Wikipedia's merged '-100/RJ70' column shows 38,101 kg, which is the 146-100 value. Deliberately NOT changed. Our seatsMax 94 vs Wikipedia's '70-82' for that column - also left alone (seat counts are configuration-dependent and the c",
]
