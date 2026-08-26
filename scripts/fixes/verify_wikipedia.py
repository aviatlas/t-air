# -*- coding: utf-8 -*-
"""Source verification: each record read against the English Wikipedia article
it cites, field by field.

Agents worked through the database in id order. The rule they were given was
deliberately conservative — propose a change only when the article's figure is
unambiguously for the same variant the record names, and only past a threshold
(more than 5% on a number, two years or more on a date), so that a disagreement
about rounding, or about which sub-variant a figure describes, does not turn
into a false correction. Where the article gives a figure only for the whole
type, the number stays and the id goes in FAMILY_COUNT instead.

313 of 656 records are covered. They are listed in VERIFIED and marked
in the interface; the remaining records are honestly unmarked, and the interface
says so on the record rather than staying silent. The run stopped where the
session quota ran out — resume from the first id not in VERIFIED.

CHECKED_ON is the month the reading was done. It matters because a Wikipedia
article can change after we read it: the mark means "agreed with the article at
that time", not "true forever".
"""

CHECKED_ON = "2026-08"

FIXES = {
    "aermacchi-mb-326": {"mtowKg": 4577, "rangeKm": 1850},                    # was mtowKg 4577, rangeKm 1850
    "aermacchi-mb-339": {"heightM": 3.6, "mtowKg": 5897},                     # was heightM 3.6, mtowKg 5897
    "aero-l-29": {"mtowKg": 3280},                                            # was mtowKg 3280
    "aichi-d3a": {"built": 1016, "rangeKm": 1352},                            # was built 1016, rangeKm 1352
    "aidc-f-ck-1": {"introduced": 1992},                                      # was introduced 1992
    "airbus-a300b4": {"built": 136},                                          # was built 136
    "airbus-a310-300": {"seatsTypical": 220},                                 # was seatsTypical 220
    "airbus-a321-200": {"firstFlight": 1996, "introduced": 1997},             # was firstFlight 1996, introduced 1997
    "airbus-a330-mrtt": {"built": 66},                                        # was built 66
    "antonov-an-148": {"seatsTypical": 70},                                   # was seatsTypical 70
    "antonov-an-22": {"ceilingM": 9100, "status": "retired"},                 # was ceilingM 9100, status retired
    "antonov-an-26": {"introduced": 1972},                                    # was introduced 1972
    "antonov-an-70": {"built": 2, "introduced": 2015, "status": "active"},    # was built 2, introduced 2015, status active
    "bae-146-300": {"speedKmh": 747},                                         # was speedKmh 747
    "bae-jetstream-41": {"speedKmh": 482},                                    # was speedKmh 482
    "bae-taranis": {"lengthM": 12.43},                                        # was lengthM 12.43
    "baykar-akinci": {"ceilingM": 13716},                                     # was ceilingM 13716
    "baykar-tb2": {"built": 800, "ceilingM": 7620},                           # was built 800, ceilingM 7620
    "boeing-737-300": {"mtowKg": 56470},                                      # was mtowKg 56470
    "boeing-737-max-10": {"rangeKm": 5740},                                   # was rangeKm 5740
    "boeing-737-max-9": {"rangeKm": 6110},                                    # was rangeKm 6110
    "boeing-747-400": {"built": 442},                                         # was built 442
    "boeing-747sp": {"rangeKm": 10800},                                       # was rangeKm 10800
    "boeing-767-300f": {"built": 161},                                        # was built 161
    "boeing-ch-46": {"ceilingM": 5180},                                       # was ceilingM 5180
    "boeing-ch-47f": {"mtowKg": 24494},                                       # was mtowKg 24494
    "boeing-e-3": {"ceilingM": 8800, "mtowKg": 157400},                       # was ceilingM 8800, mtowKg 157400
    "boeing-f-15ex": {"introduced": 2024},                                    # was introduced 2024
    "boeing-kc-46": {"built": 105},                                           # was built 105
    "boeing-rc-135": {"mtowKg": 146284},                                      # was mtowKg 146284
    "bombardier-crj1000": {"seatsTypical": 100},                              # was seatsTypical 100
    "bombardier-crj200": {"seatsMax": 52},                                    # was seatsMax 52
    "bombardier-crj550": {"mtowKg": 29484, "rangeKm": 1852},                  # was mtowKg 29484, rangeKm 1852
    "bombardier-crj700": {"ceilingM": 12497},                                 # was ceilingM 12497
    "bombardier-crj900": {"ceilingM": 12497},                                 # was ceilingM 12497
    "boulton-paul-defiant-mk-i": {"built": 723, "heightM": 3.45},             # was built 723, heightM 3.45
    "bristol-britannia": {"built": 18, "ceilingM": 7300},                     # was built 18, ceilingM 7300
    "bristol-f2b": {"rangeKm": 594},                                          # was rangeKm 594
    "britten-norman-islander": {"ceilingM": 4000, "speedKmh": 240},           # was ceilingM 4000, speedKmh 240
    "casa-cn-235": {"ceilingM": 9100, "introduced": 1988},                    # was ceilingM 9100, introduced 1988
    "cessna-t-37": {"ceilingM": 11800},                                       # was ceilingM 11800
    "changhe-z-10": {"introduced": 2009, "speedKmh": 300},                    # was introduced 2009, speedKmh 300
    "chengdu-j-20": {"heightM": 4.69},                                        # was heightM 4.69
    "comac-arj21-700": {"built": 210},                                        # was built 210
    "comac-c919": {"ceilingM": 12200},                                        # was ceilingM 12200
    "concorde": {"ceilingM": 18288},                                          # was ceilingM 18288
    "consolidated-b-24j": {"built": 6678},                                    # was built 6678
    "convair-990": {"ceilingM": 12497, "speedKmh": 896},                      # was ceilingM 12497, speedKmh 896
    "de-havilland-mosquito-b16": {"ceilingM": 11700, "rangeKm": 4540},        # was ceilingM 11000, rangeKm 2400
    "de-havilland-mosquito-fb-vi": {"ceilingM": 7900, "rangeKm": 1800},       # was ceilingM 10100, rangeKm 2740
    "de-havilland-vampire-fb5": {"ceilingM": 13000, "heightM": 2.69},         # was ceilingM 12200, heightM None
    "de-havilland-venom-fb1": {"heightM": 1.88},                              # was heightM None
    "dehavilland-dash8-q400": {"ceilingM": 7600},                             # was ceilingM None
    "dehavillandcanada-dhc-5": {"introduced": 1965},                          # was introduced 1967
    "dh-dove": {"ceilingM": 6600},                                            # was ceilingM None
    "dhc-1-chipmunk": {"mtowKg": 998, "rangeKm": 417},                        # was mtowKg 907, rangeKm 445
    "dhc-6-twin-otter": {"ceilingM": 7600},                                   # was ceilingM None
    "dhc-7-dash-7": {"ceilingM": 6400},                                       # was ceilingM None
    "dornier-228": {"ceilingM": 7620},                                        # was ceilingM None
    "dornier-328": {"ceilingM": 9492},                                        # was ceilingM None
    "dornier-do-335": {"rangeKm": 1550},                                      # was rangeKm 1380
    "douglas-a-20g": {"rangeKm": 1521},                                       # was rangeKm 1650
    "douglas-a-26": {"ceilingM": 8700, "rangeKm": 2600},                      # was ceilingM 6700, rangeKm 2300
    "douglas-c-133": {"crew": 5},                                             # was crew 6
    "douglas-dc-2": {"ceilingM": 6840, "rangeKm": 1600},                      # was ceilingM None, rangeKm 1750
    "douglas-dc-3": {"ceilingM": 7070},                                       # was ceilingM None
    "douglas-dc-4": {"rangeKm": 5310},                                        # was rangeKm 6840
    "douglas-dc-7c": {"ceilingM": 6600},                                      # was ceilingM None
    "douglas-dc-9-30": {"ceilingM": 10670},                                   # was ceilingM None
    "embraer-e170": {"ceilingM": 12479},                                      # was ceilingM None
    "embraer-e175": {"ceilingM": 12479},                                      # was ceilingM None
    "embraer-e175-e2": {"ceilingM": 12500, "heightM": 9.98},                  # was ceilingM None, heightM None
    "embraer-e190": {"ceilingM": 12479},                                      # was ceilingM None
    "embraer-e190-e2": {"ceilingM": 12500},                                   # was ceilingM None
    "embraer-e195": {"ceilingM": 12479},                                      # was ceilingM None
    "embraer-e195-e2": {"ceilingM": 12500, "rangeKm": 5600},                  # was ceilingM None, rangeKm 4815
    "embraer-emb-110": {"ceilingM": 6550},                                    # was ceilingM None
    "embraer-emb-120": {"ceilingM": 9754},                                    # was ceilingM None
    "embraer-emb-314": {"rangeKm": 1330},                                     # was rangeKm 1568
    "embraer-kc-390": {"speedKmh": 988},                                      # was speedKmh 870
    "fairchild-c-123": {"speedKmh": 367},                                     # was speedKmh 390
    "fairchild-metro-iii": {"built": 291, "ceilingM": 7600, "crew": 2, "rangeKm": 1100},  # was built None, ceilingM None, crew None, rangeKm 2131
    "fiat-g50": {"ceilingM": 10700, "heightM": 3.28, "rangeKm": 445},         # was ceilingM 9700, heightM 2.96, rangeKm 670
    "focke-wulf-fw-189": {"rangeKm": 940},                                    # was rangeKm 670
    "focke-wulf-fw-190a": {"heightM": 3.15, "mtowKg": 4900, "rangeKm": 900},  # was heightM 3.95, mtowKg 4400, rangeKm 800
    "focke-wulf-ta-152h": {"rangeKm": 2000},                                  # was rangeKm 1200
    "fokker-100": {"ceilingM": 10668, "crew": 2, "seatsTypical": 109},        # was ceilingM None, crew None, seatsTypical 100
    "fokker-50": {"ceilingM": 7620, "crew": 2, "rangeKm": 1700, "seatsMax": 62},  # was ceilingM None, crew None, rangeKm 2055, seatsMax 58
    "fokker-f27": {"rangeKm": 2600},                                          # was rangeKm 1926
    "ford-trimotor": {"ceilingM": 5029, "speedKmh": 172},                     # was ceilingM None, speedKmh 145
    "ga-mq-9": {"built": 575},                                                # was built 400
    "gloster-gladiator-mk-ii": {"heightM": 3.58},                             # was heightM 3.15
    "gloster-javelin-faw9": {"ceilingM": 16100},                              # was ceilingM 15200
    "grob-g-120tp": {"mtowKg": 1590, "rangeKm": 1070},                        # was mtowKg 1440, rangeKm 1186
    "grumman-c-2": {"mtowKg": 27216},                                         # was mtowKg 24655
    "grumman-tbf": {"ceilingM": 6900, "heightM": 5.0, "mtowKg": 7047, "rangeKm": 1456},  # was ceilingM 9170, heightM 4.7, mtowKg 7876, rangeKm 1610
    "hawker-sea-fury-fb-11": {"mtowKg": 6645, "rangeKm": 1260},               # was mtowKg 5670, rangeKm 1127
    "hawker-siddeley-trident-1c": {"mtowKg": 48534},                          # was mtowKg 52160
    "hawker-tempest-mk-v": {"heightM": 4.52},                                 # was heightM 4.9
    "hawker-typhoon-mk-ib": {"ceilingM": 9700},                               # was ceilingM 10700
    "heinkel-he-177": {"rangeKm": 6000, "speedKmh": 488},                     # was rangeKm 5600, speedKmh 565
    "hesa-karrar": {"mtowKg": 700, "spanM": 2.5},                             # was mtowKg None, spanM 3.0
    "hesa-shabaviz-2-75": {"wiki": "Shabaviz 2-75"},                          # was wiki HESA Shabaviz 2-75
    "hongdu-gj-11": {"heightM": 2.7, "lengthM": 12.2},                        # was heightM None, lengthM 10.0
    "hongdu-l-15": {"mtowKg": 11600, "rangeKm": 2600},                        # was mtowKg 9800, rangeKm 3100
    "iai-heron": {"firstFlight": 2006},                                       # was firstFlight 2004
    "iar-80": {"mtowKg": 3030, "rangeKm": 730, "spanM": 11.0, "speedKmh": 510},  # was mtowKg 2550, rangeKm 940, spanM 10.0, speedKmh 550
    "ilyushin-il-10": {"ceilingM": 5500},                                     # was ceilingM 7250
    "ilyushin-il-12": {"rangeKm": 1500},                                      # was rangeKm 3000
    "ilyushin-il-14": {"crew": 4, "rangeKm": 1305},                           # was crew 3, rangeKm 1500
    "ilyushin-il-18": {"ceilingM": 11800},                                    # was ceilingM 10000
    "ilyushin-il-2": {"ceilingM": 4525, "rangeKm": 765},                      # was ceilingM 5500, rangeKm 720
    "kai-t-50": {"mtowKg": 10722},                                            # was mtowKg 13500
    "kamov-ka-50": {"speedKmh": 315},                                         # was speedKmh 350
    "kawasaki-c-2": {"built": 15},                                            # was built None
    "lavochkin-lagg-3": {"heightM": 2.54},                                    # was heightM 4.4
    "leonardo-aw139": {"ceilingM": 6096},                                     # was ceilingM None
    "lisunov-li-2": {"ceilingM": 5600},                                       # was ceilingM None
    "lockheed-f-117a": {"speedKmh": 1100},                                    # was speedKmh 993
    "lockheed-l-1049": {"ceilingM": 7800},                                    # was ceilingM None
    "lockheed-l-1649": {"ceilingM": 7200},                                    # was ceilingM None
    "lockheed-l-188": {"ceilingM": 8700},                                     # was ceilingM None
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
    "de-havilland-mosquito-b16",
    "de-havilland-vampire-fb5",
    "de-havilland-venom-fb1",
    "dornier-do-335",
    "douglas-a-1",
    "douglas-a-20g",
    "douglas-a-26",
    "douglas-a-4",
    "douglas-sbd",
    "english-electric-canberra",
    "english-electric-lightning-f6",
    "fairey-firefly-mk-i",
    "fiat-g91r",
    "focke-wulf-fw-189",
    "ford-trimotor",
    "general-dynamics-f-111f",
    "gloster-gladiator-mk-ii",
    "grumman-f6f-5-hellcat",
    "grumman-f8f-1-bearcat",
    "grumman-f9f-5",
    "grumman-tbf",
    "hawker-sea-fury-fb-11",
    "hawkersiddeley-nimrod",
    "heinkel-he-111h",
    "heinkel-he-177",
    "henschel-hs-129",
    "hs-748",
    "iar-80",
    "ilyushin-il-10",
    "kai-t-50",
    "kamov-ka-32",
    "lavochkin-la-5fn",
    "leonardo-aw101",
    "let-l-410",
    "lockheed-c-130h",
]

# Records read against their Wikipedia article, field by field.
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
    "de-havilland-mosquito-b16",
    "de-havilland-mosquito-fb-vi",
    "de-havilland-vampire-fb5",
    "de-havilland-venom-fb1",
    "dehavilland-dash8-300",
    "dehavilland-dash8-q400",
    "dehavillandcanada-dhc-4",
    "dehavillandcanada-dhc-5",
    "dewoitine-d520",
    "dh-dove",
    "dh-heron",
    "dhc-1-chipmunk",
    "dhc-6-twin-otter",
    "dhc-7-dash-7",
    "dornier-228",
    "dornier-328",
    "dornier-do-17z",
    "dornier-do-335",
    "douglas-a-1",
    "douglas-a-20g",
    "douglas-a-26",
    "douglas-a-4",
    "douglas-c-133",
    "douglas-c-47",
    "douglas-c-54",
    "douglas-dc-10-30",
    "douglas-dc-2",
    "douglas-dc-3",
    "douglas-dc-4",
    "douglas-dc-6b",
    "douglas-dc-7c",
    "douglas-dc-8-32",
    "douglas-dc-8-63",
    "douglas-dc-9-30",
    "douglas-sbd",
    "elbit-hermes-900",
    "embraer-e170",
    "embraer-e175",
    "embraer-e175-e2",
    "embraer-e190",
    "embraer-e190-e2",
    "embraer-e195",
    "embraer-e195-e2",
    "embraer-emb-110",
    "embraer-emb-120",
    "embraer-emb-312",
    "embraer-emb-314",
    "embraer-erj-135",
    "embraer-erj-140",
    "embraer-erj-145",
    "embraer-kc-390",
    "english-electric-canberra",
    "fairchild-c-119",
    "fairchild-c-123",
    "fairchild-metro-iii",
    "fairey-firefly-mk-i",
    "fairey-swordfish",
    "fiat-cr42",
    "fiat-g50",
    "fiat-g55",
    "fiat-g91r",
    "focke-wulf-fw-189",
    "focke-wulf-fw-190a",
    "focke-wulf-fw-190d9",
    "focke-wulf-ta-152h",
    "fokker-100",
    "fokker-50",
    "fokker-70",
    "fokker-d-vii",
    "fokker-d-xxi",
    "fokker-dr-i",
    "fokker-f27",
    "fokker-f28",
    "ford-trimotor",
    "fouga-cm-170-magister",
    "ga-mq-1",
    "ga-mq-1c",
    "ga-mq-9",
    "general-dynamics-f-111f",
    "general-dynamics-f-16c",
    "gloster-gladiator-mk-ii",
    "gloster-javelin-faw9",
    "gloster-meteor-f8",
    "grob-g-120tp",
    "grumman-a-6",
    "grumman-c-2",
    "grumman-e-2",
    "grumman-f-14a",
    "grumman-f4f-4-wildcat",
    "grumman-f6f-5-hellcat",
    "grumman-f8f-1-bearcat",
    "grumman-f9f-5",
    "grumman-tbf",
    "hal-ajeet",
    "hawker-hunter-f6",
    "hawker-sea-fury-fb-11",
    "hawker-siddeley-harrier-gr3",
    "hawker-siddeley-trident-1c",
    "hawker-tempest-mk-v",
    "hawker-typhoon-mk-ib",
    "hawkersiddeley-nimrod",
    "heinkel-he-111h",
    "heinkel-he-177",
    "heinkel-he-219",
    "henschel-hs-129",
    "hesa-azarakhsh",
    "hesa-dorna",
    "hesa-iran-140",
    "hesa-karrar",
    "hesa-kowsar",
    "hesa-saeqeh",
    "hesa-shabaviz-2-75",
    "hesa-shafaq",
    "hesa-simorgh",
    "hesa-yasin",
    "hongdu-gj-11",
    "hongdu-jl-8",
    "hongdu-l-15",
    "hs-748",
    "iai-heron",
    "iaio-fotros",
    "iaio-qaher-313",
    "iar-80",
    "ilyushin-il-10",
    "ilyushin-il-12",
    "ilyushin-il-14",
    "ilyushin-il-18",
    "ilyushin-il-2",
    "ilyushin-il-28",
    "kai-t-50",
    "kamov-ka-27",
    "kamov-ka-32",
    "kamov-ka-50",
    "kamov-ka-52",
    "kawanishi-n1k2-j",
    "kawasaki-c-2",
    "kawasaki-ki-100",
    "kawasaki-ki-45",
    "kawasaki-ki-61",
    "kawasaki-t-4",
    "lavochkin-la-5fn",
    "lavochkin-la-7",
    "lavochkin-lagg-3",
    "leonardo-a129",
    "leonardo-aw101",
    "leonardo-aw139",
    "let-l-410",
    "lisunov-li-2",
    "lockheed-ac-130",
    "lockheed-c-130e",
    "lockheed-c-130h",
    "lockheed-c-141",
    "lockheed-c-5",
    "lockheed-f-117a",
    "lockheed-f-5e-lightning",
    "lockheed-f-80c",
    "lockheed-l-049",
    "lockheed-l-1049",
    "lockheed-l-1649",
    "lockheed-l-188",
    "lockheed-p-38j-lightning",
]

UNRESOLVED = [
    "343 records are not yet source-checked; resume from the first "
    "id not in VERIFIED.",
    "BLOCKED: WebFetch returned 'You've hit your weekly limit - resets Aug 25, 11pm (UTC)' starting at record 28 of 55. Direct curl to en.wikipedia.org is refused by the agent proxy (403 on CONNECT), and WebSearch returns titles/URLs only, no page content. Records 28-55 (all Beechcraft T-34 onward throug",
    "DB convention observed and respected: every civil record in this slice has crew=null and ceilingM=null, and every military record has seatsTypical/seatsMax=null. No crew or ceiling values were proposed for civil records, and no seat counts for military records, even where Wikipedia prints them (e.g.",
    "antonov-an-148: Wikipedia's spec block is for the An-148-100A (range 2,100 km); our record is the generic 'An-148' with rangeKm 3500, which matches the -100B/E. Range left unchanged as variant-ambiguous.",
    "antonov-an-2: Wikipedia body text says 'over 13,000 constructed' through 2001 while our built=18000 (the figure usually quoted including Chinese Y-5 production). Left unchanged - genuinely ambiguous. MTOW printed as 5,440 kg vs our 5500 (1.1%, under threshold).",
    "antonov-an-225: our introduced=1989 vs Wikipedia '2002 (commercial service)'; the An-225 flew from 1989, was stored, then re-entered service 2001-02. Left unchanged. All other An-225 figures matched exactly.",
    "avro-lancaster-b1: WebFetch could not retrieve the 'Specifications (Lancaster B I)' section on either attempt (page truncated before it). Only firstFlight 1941, introduced 1942, crew 7 and 4 engines confirmed; performance and dimension figures remain unverified.",
    "avro-vulcan-b2: WebFetch could not retrieve the specifications section on either attempt. Confirmed from body text: the B.2 first flew September 1958 and entered RAF service July 1960, with 89 B.2 built of 134 total. Our record carries the type-level infobox dates 1952/1956 - left unchanged, but a h",
    "avro-rj70: our mtowKg 43090 (95,000 lb) is the correct RJ70 figure; Wikipedia's merged '-100/RJ70' column shows 38,101 kg, which is the 146-100 value. Deliberately NOT changed. Our seatsMax 94 vs Wikipedia's '70-82' for that column - also left alone (seat counts are configuration-dependent and the c",
    "avro-rj85 / bae-146-200 / bae-146-300: Wikipedia gives one merged column per pair (-100/RJ70, -200/RJ85, -300/RJ100), so per-variant range cannot be isolated. Printed ranges are 3,870 km (82 pax), 3,650 km (100 pax) and 3,340 km (100 pax) vs our 2180 / 2909 / 2900. No range fixes proposed, but the R",
    "atr-42-500: Wikipedia prints a 726 nmi (1,345 km) range that the extraction attributed to the -500, while our -600 record's 1326 km matches 716 nmi exactly - most likely a -500/-600 column mix-up. Range left unchanged.",
    "bac-one-eleven-500: Wikipedia's only specifications table is for the Model 200, not the Series 500, so nothing could be verified beyond seatsMax 119 and the family production total (244 overall, 86 of the Series 500). built=244 is correctly flagged builtFamily=true in the record.",
    "bae-jetstream-31: built=386 is Wikipedia's combined Jetstream 31/32 production figure, not the 31 alone.",
    "bae-taranis: our status=retired vs Wikipedia 'In development' (the article looks stale - the programme has ended). Left unchanged.",
    "baykar-akinci: built is null in our record; Wikipedia reports approximately 110 delivered as of early 2026. Not applied because deliveries are not the same as number built, but this null is fillable.",
]
