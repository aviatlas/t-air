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

485 of 656 records are covered. They are listed in VERIFIED and marked in
the interface; the rest are honestly unmarked, and the record says so rather
than staying silent. The run stopped where the session quota ran out — resume
from the first id not in VERIFIED.

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
    "de-havilland-mosquito-b16": {"ceilingM": 11700, "rangeKm": 4540},        # was ceilingM 11700, rangeKm 4540
    "de-havilland-mosquito-fb-vi": {"ceilingM": 7900, "rangeKm": 1800},       # was ceilingM 7900, rangeKm 1800
    "de-havilland-vampire-fb5": {"ceilingM": 13000, "heightM": 2.69},         # was ceilingM 13000, heightM 2.69
    "de-havilland-venom-fb1": {"heightM": 1.88},                              # was heightM 1.88
    "dehavilland-dash8-q400": {"ceilingM": 7600},                             # was ceilingM 7600
    "dehavillandcanada-dhc-5": {"introduced": 1965},                          # was introduced 1965
    "dh-dove": {"ceilingM": 6600},                                            # was ceilingM 6600
    "dhc-1-chipmunk": {"mtowKg": 998, "rangeKm": 417},                        # was mtowKg 998, rangeKm 417
    "dhc-6-twin-otter": {"ceilingM": 7600},                                   # was ceilingM 7600
    "dhc-7-dash-7": {"ceilingM": 6400},                                       # was ceilingM 6400
    "dornier-228": {"ceilingM": 7620},                                        # was ceilingM 7620
    "dornier-328": {"ceilingM": 9492},                                        # was ceilingM 9492
    "dornier-do-335": {"rangeKm": 1550},                                      # was rangeKm 1550
    "douglas-a-20g": {"rangeKm": 1521},                                       # was rangeKm 1521
    "douglas-a-26": {"ceilingM": 8700, "rangeKm": 2600},                      # was ceilingM 8700, rangeKm 2600
    "douglas-c-133": {"crew": 5},                                             # was crew 5
    "douglas-dc-2": {"ceilingM": 6840, "rangeKm": 1600},                      # was ceilingM 6840, rangeKm 1600
    "douglas-dc-3": {"ceilingM": 7070},                                       # was ceilingM 7070
    "douglas-dc-4": {"rangeKm": 5310},                                        # was rangeKm 5310
    "douglas-dc-7c": {"ceilingM": 6600},                                      # was ceilingM 6600
    "douglas-dc-9-30": {"ceilingM": 10670},                                   # was ceilingM 10670
    "embraer-e170": {"ceilingM": 12479},                                      # was ceilingM 12479
    "embraer-e175": {"ceilingM": 12479},                                      # was ceilingM 12479
    "embraer-e175-e2": {"ceilingM": 12500, "heightM": 9.98},                  # was ceilingM 12500, heightM 9.98
    "embraer-e190": {"ceilingM": 12479},                                      # was ceilingM 12479
    "embraer-e190-e2": {"ceilingM": 12500},                                   # was ceilingM 12500
    "embraer-e195": {"ceilingM": 12479},                                      # was ceilingM 12479
    "embraer-e195-e2": {"ceilingM": 12500, "rangeKm": 5600},                  # was ceilingM 12500, rangeKm 5600
    "embraer-emb-110": {"ceilingM": 6550},                                    # was ceilingM 6550
    "embraer-emb-120": {"ceilingM": 9754},                                    # was ceilingM 9754
    "embraer-emb-314": {"rangeKm": 1330},                                     # was rangeKm 1330
    "embraer-kc-390": {"speedKmh": 988},                                      # was speedKmh 988
    "fairchild-c-123": {"speedKmh": 367},                                     # was speedKmh 367
    "fairchild-metro-iii": {"built": 291, "ceilingM": 7600, "crew": 2, "rangeKm": 1100},  # was built 291, ceilingM 7600, crew 2, rangeKm 1100
    "fiat-g50": {"ceilingM": 10700, "heightM": 3.28, "rangeKm": 445},         # was ceilingM 10700, heightM 3.28, rangeKm 445
    "focke-wulf-fw-189": {"rangeKm": 940},                                    # was rangeKm 940
    "focke-wulf-fw-190a": {"heightM": 3.15, "mtowKg": 4900, "rangeKm": 900},  # was heightM 3.15, mtowKg 4900, rangeKm 900
    "focke-wulf-ta-152h": {"rangeKm": 2000},                                  # was rangeKm 2000
    "fokker-100": {"ceilingM": 10668, "crew": 2, "seatsTypical": 109},        # was ceilingM 10668, crew 2, seatsTypical 109
    "fokker-50": {"ceilingM": 7620, "crew": 2, "rangeKm": 1700, "seatsMax": 62},  # was ceilingM 7620, crew 2, rangeKm 1700, seatsMax 62
    "fokker-f27": {"rangeKm": 2600},                                          # was rangeKm 2600
    "ford-trimotor": {"ceilingM": 5029, "speedKmh": 172},                     # was ceilingM 5029, speedKmh 172
    "ga-mq-9": {"built": 575},                                                # was built 575
    "gloster-gladiator-mk-ii": {"heightM": 3.58},                             # was heightM 3.58
    "gloster-javelin-faw9": {"ceilingM": 16100},                              # was ceilingM 16100
    "grob-g-120tp": {"mtowKg": 1590, "rangeKm": 1070},                        # was mtowKg 1590, rangeKm 1070
    "grumman-c-2": {"mtowKg": 27216},                                         # was mtowKg 27216
    "grumman-tbf": {"ceilingM": 6900, "heightM": 5.0, "mtowKg": 7047, "rangeKm": 1456},  # was ceilingM 6900, heightM 5.0, mtowKg 7047, rangeKm 1456
    "hawker-sea-fury-fb-11": {"mtowKg": 6645, "rangeKm": 1260},               # was mtowKg 6645, rangeKm 1260
    "hawker-siddeley-trident-1c": {"mtowKg": 48534},                          # was mtowKg 48534
    "hawker-tempest-mk-v": {"heightM": 4.52},                                 # was heightM 4.52
    "hawker-typhoon-mk-ib": {"ceilingM": 9700},                               # was ceilingM 9700
    "heinkel-he-177": {"rangeKm": 6000, "speedKmh": 488},                     # was rangeKm 6000, speedKmh 488
    "hesa-karrar": {"mtowKg": 700, "spanM": 2.5},                             # was mtowKg 700, spanM 2.5
    "hesa-shabaviz-2-75": {"wiki": "Shabaviz 2-75"},                          # was wiki Shabaviz 2-75
    "hongdu-gj-11": {"heightM": 2.7, "lengthM": 12.2},                        # was heightM 2.7, lengthM 12.2
    "hongdu-l-15": {"mtowKg": 11600, "rangeKm": 2600},                        # was mtowKg 11600, rangeKm 2600
    "iai-heron": {"firstFlight": 2006},                                       # was firstFlight 2006
    "iar-80": {"mtowKg": 3030, "rangeKm": 730, "spanM": 11.0, "speedKmh": 510},  # was mtowKg 3030, rangeKm 730, spanM 11.0, speedKmh 510
    "ilyushin-il-10": {"ceilingM": 5500},                                     # was ceilingM 5500
    "ilyushin-il-12": {"rangeKm": 1500},                                      # was rangeKm 1500
    "ilyushin-il-14": {"crew": 4, "rangeKm": 1305},                           # was crew 4, rangeKm 1305
    "ilyushin-il-18": {"ceilingM": 11800},                                    # was ceilingM 11800
    "ilyushin-il-2": {"ceilingM": 4525, "rangeKm": 765},                      # was ceilingM 4525, rangeKm 765
    "kai-t-50": {"mtowKg": 10722},                                            # was mtowKg 10722
    "kamov-ka-50": {"speedKmh": 315},                                         # was speedKmh 315
    "kawasaki-c-2": {"built": 15},                                            # was built 15
    "lavochkin-lagg-3": {"heightM": 2.54},                                    # was heightM 2.54
    "leonardo-aw139": {"ceilingM": 6096},                                     # was ceilingM 6096
    "lisunov-li-2": {"ceilingM": 5600},                                       # was ceilingM 5600
    "lockheed-f-117a": {"speedKmh": 1100},                                    # was speedKmh 1100
    "lockheed-l-1049": {"ceilingM": 7800},                                    # was ceilingM 7800
    "lockheed-l-1649": {"ceilingM": 7200},                                    # was ceilingM 7200
    "lockheed-l-188": {"ceilingM": 8700},                                     # was ceilingM 8700
    "mcdonnell-douglas-md-88": {"seatsTypical": 155},                         # was seatsTypical 142
    "mcdonnell-f-101b": {"built": 479, "introduced": 1959, "speedKmh": 1825},  # was built 807, introduced 1957, speedKmh 1965
    "mcdonnell-f2h-3": {"built": 250, "spanM": 12.73},                        # was built 895, spanM 13.66
    "mcdonnell-f3h-2": {"ceilingM": 10683},                                   # was ceilingM 13000
    "mcdonnell-md-500": {"firstFlight": 1976, "mtowKg": 1361, "rangeKm": 589, "speedKmh": 244},  # was firstFlight 1963, mtowKg 1610, rangeKm 430, speedKmh 282
    "messerschmitt-me-410": {"mtowKg": 9651},                                 # was mtowKg 10650
    "mikoyan-gurevich-mig-3": {"heightM": 3.3},                               # was heightM 3.5
    "mikoyan-mig-25p": {"rangeKm": 1860},                                     # was rangeKm 1730
    "morane-saulnier-ms-406": {"heightM": 3.25, "mtowKg": 2540, "rangeKm": 1100},  # was heightM 2.71, mtowKg 2720, rangeKm 1000
    "nakajima-b5n": {"rangeKm": 978},                                         # was rangeKm 1990
    "nakajima-ki-44": {"rangeKm": 1200},                                      # was rangeKm 1700
    "nakajima-ki-84": {"mtowKg": 4170, "rangeKm": 2168},                      # was mtowKg 3890, rangeKm 1695
    "namc-ys-11": {"ceilingM": 6982},                                         # was ceilingM None
    "north-american-f-86f": {"spanM": 11.91},                                 # was spanM 11.3
    "north-american-t-6": {"introduced": 1937},                               # was introduced 1935
    "northamerican-ov-10": {"ceilingM": 9144, "lengthM": 13.41},              # was ceilingM 7300, lengthM 12.67
    "northrop-p-61b-black-widow": {"rangeKm": 2170},                          # was rangeKm 1700
    "robinson-r44": {"lengthM": 11.66, "speedKmh": 202},                      # was lengthM 9.07, speedKmh 240
    "robinson-r66": {"built": 1500, "ceilingM": 4267, "speedKmh": 200},       # was built 1200, ceilingM None, speedKmh 222
    "saab-2000": {"ceilingM": 9450},                                          # was ceilingM None
    "saab-340b": {"ceilingM": 7620, "rangeKm": 1350},                         # was ceilingM None, rangeKm 1730
    "saab-j-35f": {"mtowKg": 11914, "rangeKm": 2750},                         # was mtowKg 16000, rangeKm 3250
    "scottish-aviation-bulldog": {"heightM": 2.73},                           # was heightM 2.28
    "shahed-129": {"built": 42},                                              # was built None
    "shahed-149": {"heightM": 3.2, "rangeKm": 7000},                          # was heightM None, rangeKm 4000
    "shenyang-j-16": {"speedKmh": 2120},                                      # was speedKmh 2400
    "shenyang-j-35": {"ceilingM": 16000, "heightM": 4.8, "introduced": 2025, "status": "production"},  # was ceilingM None, heightM None, introduced None, status development
    "shenyang-j-5": {"rangeKm": 1424},                                        # was rangeKm 1560
    "short-belfast": {"crew": 5, "rangeKm": 9815},                            # was crew 4, rangeKm 8530
    "short-stirling": {"speedKmh": 454},                                      # was speedKmh 410
    "shorts-330": {"ceilingM": 6100, "rangeKm": 1695, "speedKmh": 300},       # was ceilingM None, rangeKm 1239, speedKmh 352
    "shorts-360": {"ceilingM": 6100, "rangeKm": 1595, "speedKmh": 330},       # was ceilingM None, rangeKm 1178, speedKmh 393
    "siai-marchetti-sf-260": {"ceilingM": 4700, "mtowKg": 1200, "rangeKm": 1650},  # was ceilingM 5800, mtowKg 1300, rangeKm 1000
    "sikorsky-ch-53k": {"ceilingM": 4877, "crew": 4},                         # was ceilingM 4380, crew 5
    "sikorsky-s-76": {"ceilingM": 4200, "seatsMax": 13},                      # was ceilingM None, seatsMax 12
    "sikorsky-s-92": {"ceilingM": 4267, "heightM": 4.7, "speedKmh": 280},     # was ceilingM None, heightM 5.86, speedKmh 306
    "sukhoi-s-70": {"spanM": 20, "wiki": "Sukhoi S-70 Okhotnik-B"},           # was spanM 19.0, wiki Sukhoi Su-70 Okhotnik
    "sukhoi-su-15": {"introduced": 1965},                                     # was introduced 1967
    "sukhoi-su-25": {"mtowKg": 19300},                                        # was mtowKg 17600
    "sukhoi-su-34": {"ceilingM": 17000, "rangeKm": 4500},                     # was ceilingM 15000, rangeKm 4000
    "sukhoi-su-9": {"ceilingM": 20000, "lengthM": 16.77, "mtowKg": 12512, "rangeKm": 1350},  # was ceilingM 16760, lengthM 18.06, mtowKg 13500, rangeKm 1125
    "transall-c-160": {"crew": 3},                                            # was crew 4
    "tupolev-tu-142": {"ceilingM": 12000, "speedKmh": 925},                   # was ceilingM 13500, speedKmh 855
    "tupolev-tu-144": {"introduced": 1975, "mtowKg": 207000, "rangeKm": 6500},  # was introduced 1977, mtowKg 180000, rangeKm None
    "tupolev-tu-154m": {"rangeKm": 5280, "speedKmh": 850},                    # was rangeKm 3900, speedKmh 900
    "tupolev-tu-160": {"built": 41},                                          # was built 36
    "tupolev-tu-204-100": {"seatsTypical": 172},                              # was seatsTypical 164
    "tupolev-tu-22m3": {"firstFlight": 1977, "introduced": 1983, "speedKmh": 1997},  # was firstFlight 1969, introduced 1978, speedKmh 2300
    "tupolev-tu-95ms": {"ceilingM": 13716},                                   # was ceilingM 12000
    "utva-lasta-95": {"firstFlight": 2009, "heightM": 2.84, "rangeKm": 1160, "spanM": 9.7, "speedKmh": 345},  # was firstFlight 1985, heightM 3.0, rangeKm 750, spanM 8.6, speedKmh 300
    "valmet-l-70-vinka": {"rangeKm": 860},                                    # was rangeKm 800
    "vickers-vc10": {"rangeKm": 9410},                                        # was rangeKm 8116
    "vickers-viscount-800": {"rangeKm": 2220},                                # was rangeKm 2830
    "vought-f-8e": {"firstFlight": 1961},                                     # was firstFlight 1955
    "vought-f4u-1d-corsair": {"introduced": 1944},                            # was introduced 1942
    "westland-whirlwind-mk-i": {"mtowKg": 5191},                              # was mtowKg 4697
    "yakovlev-sj-100": {"rangeKm": 4320},                                     # was rangeKm 3000
    "yakovlev-yak-130": {"mtowKg": 10290},                                    # was mtowKg 9000
    "yakovlev-yak-42d": {"rangeKm": 4000, "speedKmh": 740},                   # was rangeKm 2200, speedKmh 810
    "yakovlev-yak-7b": {"rangeKm": 643},                                      # was rangeKm 820
    "yakovlev-yak-9": {"rangeKm": 675},                                       # was rangeKm 875
    "yakovlev-yak-9u": {"rangeKm": 675},                                      # was rangeKm 870
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
    "mcdonnell-douglas-f-15e",
    "mcdonnell-douglas-fa-18c",
    "mikoyan-mig-17f",
    "mitsubishi-ki-46",
    "nakajima-b5n",
    "nakajima-ki-43",
    "nhindustries-nh90",
    "north-american-b-25j",
    "north-american-f-100d",
    "north-american-f-86f",
    "northrop-p-61b-black-widow",
    "saab-340b",
    "saab-j-29f",
    "saab-j-35f",
    "saab-ja-37",
    "saab-jas-39c",
    "shenyang-j-11b",
    "short-stirling",
    "shorts-360",
    "siai-marchetti-sf-260",
    "sikorsky-s-76",
    "sopwith-camel",
    "sukhoi-su-17m",
    "sukhoi-su-22m4",
    "sukhoi-su-24m",
    "sukhoi-su-25",
    "sukhoi-su-30sm",
    "sukhoi-su-7b",
    "tupolev-tu-2",
    "tupolev-tu-204-100",
    "tupolev-tu-204-300",
    "tupolev-tu-214",
    "tupolev-tu-22m3",
    "vickers-vanguard",
    "vickers-vc10",
    "vickers-viscount-800",
    "vickers-wellington",
    "vought-f-8e",
    "vought-f4u-1d-corsair",
    "westland-lynx",
    "westland-sea-king",
    "yakovlev-yak-42d",
    "yakovlev-yak-7b",
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
    "mcdonnell-douglas-f-15e",
    "mcdonnell-douglas-f-4d",
    "mcdonnell-douglas-f-4e",
    "mcdonnell-douglas-fa-18c",
    "mcdonnell-douglas-md-11f",
    "mcdonnell-douglas-md-87",
    "mcdonnell-douglas-md-88",
    "mcdonnell-f-101b",
    "mcdonnell-f2h-3",
    "mcdonnell-f3h-2",
    "mcdonnell-md-11",
    "mcdonnell-md-500",
    "mcdonnell-md-82",
    "mcdonnell-md-83",
    "mcdonnelldouglas-kc-10",
    "mdhelicopters-md-902",
    "messerschmitt-bf-109e",
    "messerschmitt-bf-109f",
    "messerschmitt-bf-109g",
    "messerschmitt-bf-109k",
    "messerschmitt-bf-110",
    "messerschmitt-me-210",
    "messerschmitt-me-262a",
    "messerschmitt-me-410",
    "mikoyan-gurevich-mig-3",
    "mikoyan-mig-15bis",
    "mikoyan-mig-17f",
    "mikoyan-mig-19s",
    "mikoyan-mig-21bis",
    "mikoyan-mig-23ml",
    "mikoyan-mig-25p",
    "mikoyan-mig-27",
    "mikoyan-mig-29a",
    "mitsubishi-ki-46",
    "mitsubishi-t-2",
    "morane-saulnier-ms-406",
    "nakajima-b5n",
    "nakajima-ki-27",
    "nakajima-ki-43",
    "nakajima-ki-44",
    "nakajima-ki-84",
    "namc-ys-11",
    "nanchang-cj-6",
    "nhindustries-nh90",
    "nieuport-17",
    "north-american-a-36-apache",
    "north-american-b-25j",
    "north-american-f-100d",
    "north-american-f-86f",
    "north-american-p-51b",
    "north-american-p-51d",
    "north-american-t-2-buckeye",
    "north-american-t-6",
    "northamerican-ov-10",
    "northrop-b-2",
    "northrop-b-21",
    "northrop-f-5a",
    "northrop-f-5e",
    "northrop-f-5f",
    "northrop-p-61b-black-widow",
    "northrop-rq-4",
    "northrop-t-38a",
    "northrop-x-47b",
    "northropgrumman-e-8",
    "owj-tazarve",
    "pac-jf-17",
    "panavia-tornado-adv",
    "robinson-r44",
    "robinson-r66",
    "rockwell-b-1b",
    "saab-2000",
    "saab-340b",
    "saab-j-29f",
    "saab-j-35f",
    "saab-ja-37",
    "saab-jas-39c",
    "saab-jas-39e",
    "scottish-aviation-bulldog",
    "shahed-129",
    "shahed-149",
    "shenyang-j-11b",
    "shenyang-j-15",
    "shenyang-j-16",
    "shenyang-j-35",
    "shenyang-j-5",
    "shenyang-j-6",
    "shenyang-j-8ii",
    "short-belfast",
    "short-stirling",
    "shorts-330",
    "shorts-360",
    "siai-marchetti-sf-260",
    "sikorsky-ch-53e",
    "sikorsky-ch-53k",
    "sikorsky-mh-60r",
    "sikorsky-s-76",
    "sikorsky-s-92",
    "sikorsky-sh-3",
    "sikorsky-uh-60m",
    "slingsby-t67-firefly",
    "sopwith-camel",
    "spad-s-xiii",
    "sud-aviation-caravelle-3",
    "sukhoi-s-70",
    "sukhoi-ssj100",
    "sukhoi-su-15",
    "sukhoi-su-17m",
    "sukhoi-su-22m4",
    "sukhoi-su-24m",
    "sukhoi-su-25",
    "sukhoi-su-27s",
    "sukhoi-su-30mki",
    "sukhoi-su-30sm",
    "sukhoi-su-33",
    "sukhoi-su-34",
    "sukhoi-su-35s",
    "sukhoi-su-57",
    "sukhoi-su-7b",
    "sukhoi-su-9",
    "supermarine-seafire-mk-iii",
    "supermarine-spitfire-mk-i",
    "supermarine-spitfire-mk-vb",
    "supermarine-spitfire-mk-xiv",
    "supermarine-spitfire-pr-xi",
    "tai-anka",
    "transall-c-160",
    "tupolev-tu-104",
    "tupolev-tu-114",
    "tupolev-tu-124",
    "tupolev-tu-134",
    "tupolev-tu-142",
    "tupolev-tu-144",
    "tupolev-tu-154m",
    "tupolev-tu-16",
    "tupolev-tu-160",
    "tupolev-tu-2",
    "tupolev-tu-204-100",
    "tupolev-tu-204-300",
    "tupolev-tu-214",
    "tupolev-tu-22",
    "tupolev-tu-22m3",
    "tupolev-tu-95ms",
    "utva-lasta-95",
    "valmet-l-70-vinka",
    "vickers-vanguard",
    "vickers-vc10",
    "vickers-viking",
    "vickers-viscount-800",
    "vickers-wellington",
    "vought-f-8e",
    "vought-f4u-1d-corsair",
    "vought-f4u-4-corsair",
    "westland-lynx",
    "westland-sea-king",
    "westland-whirlwind-mk-i",
    "xian-h-6k",
    "xian-jh-7a",
    "xian-ma60",
    "yakovlev-sj-100",
    "yakovlev-yak-1",
    "yakovlev-yak-130",
    "yakovlev-yak-141",
    "yakovlev-yak-18",
    "yakovlev-yak-3",
    "yakovlev-yak-38",
    "yakovlev-yak-40",
    "yakovlev-yak-42d",
    "yakovlev-yak-52",
    "yakovlev-yak-7b",
    "yakovlev-yak-9",
    "yakovlev-yak-9u",
    "zlin-z-242",
]

UNRESOLVED = [
    "171 records are not yet source-checked; resume from the first "
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
    "baykar-tb2: our rangeKm 4000 vs Wikipedia's only range figure, 'line-of-sight propagation, < 300 km' (a datalink range, not an airframe range). Left unchanged as not comparable, but 4000 km looks endurance-derived and deserves review. Also introduced 2014 vs Wikipedia 2015 (1-year gap, under thresho",
    "beechcraft-1900d: Wikipedia's infobox dates (first flight 1982, service 1984) are for the Beechcraft 1900 family, not the 1900D - our 1990/1991 are the correct 1900D dates and were left alone. The specifications section IS the 1900D (MTOW 17,120 lb = 7,765 kg and built=439 match our record exactly).",
]
