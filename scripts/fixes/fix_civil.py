# -*- coding: utf-8 -*-
"""Audit of the 199 civil records — every record read field by field, then the
least certain ones checked against the English Wikipedia article for the type.
The dominant error class is a variant record carrying the *family's* first-flight
year or the *programme's* total production count instead of the variant's own."""

FIXES = {
    # -200 first flew 27 Jul 1967; 1963 is the 727-100's first flight.
    # 1832 is the whole-727 programme total; the -200 series accounts for 1,260.
    "boeing-727-200": {"firstFlight": 1967, "built": 1260},

    # A310-300 first flew 8 Jul 1985; 1982 is the A310-200's first flight.
    "airbus-a310-300": {"firstFlight": 1985},

    # -320B first flew 31 Jan 1962 and entered service with Pan Am in Jun 1962;
    # 1957/1959 are the 707-120 / 707-320 dates. 1010 is the whole-707 total,
    # Boeing's model summary gives 174 for the -320B.
    "boeing-707-320b": {"firstFlight": 1962, "introduced": 1962, "built": 174},

    # A300B4 first flew 26 Dec 1974 and entered service Dec 1975 (Bavaria
    # Germanair); 1972/1974 belong to the A300B1 prototype and the A300B2.
    "airbus-a300b4": {"firstFlight": 1974, "introduced": 1975},

    # 155 is the whole 747-8 programme (48 Intercontinental + 107 Freighter);
    # the -8F record already carries the correct 107.
    "boeing-747-8i": {"built": 48},

    # DC-10-30 first flew 21 Jun 1972, not 1970 (that is the DC-10-10, which
    # this record's sibling already lists). 386 conflates variants: 163 -30s.
    "douglas-dc-10-30": {"firstFlight": 1972, "built": 163},

    # DC-9-30 first flew 1 Aug 1966; 1965 is the DC-9-10's first flight.
    # 976 is the total for all DC-9 series; 662 were Series 30.
    "douglas-dc-9-30": {"firstFlight": 1966, "built": 662},

    # Il-62M first flew in 1971 and entered service in 1973; 1963/1967 are the
    # baseline Il-62's first flight and Aeroflot service entry.
    "ilyushin-il-62m": {"firstFlight": 1971, "introduced": 1973},

    # built was the bare string "N" (corrupt); 47 An-148s were completed.
    "antonov-an-148": {"built": 47},

    # The Aviadvigatel PD-14 powers the MC-21-310; the MC-21-300 that first flew
    # in May 2017 is the Pratt & Whitney PW1400G version.
    "irkut-mc-21-300": {"engineModel": "Pratt & Whitney PW1400G"},

    # York height is 16 ft 6 in = 5.03 m, not 5.44 m.
    "avro-york": {"heightM": 5.03},

    # MD-82 first flew 8 Jan 1981; 1979 is the MD-81's first flight.
    # 1191 is the whole MD-80 series; 539 MD-82s were built.
    "mcdonnell-md-82": {"firstFlight": 1981, "built": 539},

    # 777-200ER first flew 7 Oct 1996; 1994 is the baseline 777-200's.
    "boeing-777-200er": {"firstFlight": 1996},
}

DROP = []  # no duplicates and no non-existent types found among the 199

UNRESOLVED = [
    "airbus-a310-300: introduced 1983 is the A310-200's date and is impossible "
    "(the -300 first flew Jul 1985), but sources split between Dec 1985 and 1986",
    "boeing-767-200er: firstFlight 1981 is the baseline 767-200's; the -200ER's "
    "own first flight (early 1984, service entry Mar 1984) could not be confirmed",
    "bombardier-crj200: firstFlight 1991 / introduced 1992 are the CRJ100's; "
    "Wikipedia gives the CRJ200 a 1994 service entry, other sources say 1996",
    "ford-trimotor: record is the 5-AT, but firstFlight 1926 and built 199 are "
    "the 4-AT / whole-family figures (5-AT flew 1928, 117 built); speedKmh 145 "
    "also looks like a 4-AT number",
    "bae-146-300: built 387 is the entire BAe 146 + Avro RJ programme, not the "
    "146-300/RJ100; per-variant counts not published in the article",
    "ilyushin-il-96-400t: firstFlight 1997 is the Il-96T's; heightM 15.72 "
    "contradicts the ~17.5 m given for the same-fuselage Il-96-300",
    "airbus-a340-200: rangeKm 12400 is shorter than the -300's 13500, which is "
    "backwards for the shorter, lighter variant; sources quote 12,400-13,800 km",
    "vickers-viscount-800: built 445 is the total for all Viscount series",
    "saab-340b: built 459 is the whole Saab 340 run (~300 were 340B)",
    "airbus-a300b4 / airbus-a310-300: built 561 / 255 are whole-family totals "
    "parked on one variant record; left alone because their sibling records "
    "carry None rather than variant counts",
    "handley-page-herald: firstFlight 1955 is the piston HPR.3 prototype; the "
    "Dart Herald Series 200 first flew in 1961",
    "handley-page-hermes: firstFlight 1945 is the Hermes I; the Hermes IV that "
    "this record's dimensions describe first flew in 1948",
    "avro-york: mtowKg 30844 (68,000 lb) vs Wikipedia's 65,000 lb (29,484 kg)",
    "ilyushin-il-62m: mtowKg 167000 vs Wikipedia's 165,000 kg",
    "airbus-a321neo: mtowKg 97000 is the A321LR figure; the standard A321neo is "
    "widely quoted at 93,500 kg, though Airbus now also offers 97 t",
    "antonov-an-24: engineModel 'Ivchenko AI-24VT' is the An-26 engine; the "
    "An-24RV also carries an RU-19A-300 booster turbojet not counted in engineCount",
    "wiki titles: 'Airbus A319neo' and 'Airbus A321neo' are probably redirects "
    "into 'Airbus A320neo family', and 'Sukhoi Superjet 100' may now be split "
    "from 'Yakovlev SJ-100'; could not verify redirect vs article",
    "NOTE: the WebFetch budget was cut off by a session limit after 13 fetches, "
    "so the items above are flagged from record-internal inconsistency only",
]
