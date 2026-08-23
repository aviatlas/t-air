# -*- coding: utf-8 -*-
"""Audit of the military records.

Reviewed all 374 fixed-wing military records — rotorcraft and uncrewed types
are audited in fill_rotary_uav.py and fix_audit3.py — against known figures,
looking for the failure mode
the civil audit surfaced: a record named for one variant but carrying the
whole family's first-flight year or production total. Only mismatches of five
years or more, and production counts off by a clear multiple, are corrected
here — smaller variant-vs-family differences are a convention question rather
than an error, and are noted in the README instead.
"""

FIXES = {
    # --- production counts that belong to the whole programme, not the variant
    "boeing-b-52h": {"built": 102},                    # 744 is every B-52; the H model was 102
    "boeing-b-17g": {"built": 8680,                    # 12,731 is every B-17
                     "firstFlight": 1943, "introduced": 1943},
    "grumman-f4f-4-wildcat": {"built": 1169,           # 7,885 counts the GM-built FM series too
                              "firstFlight": 1941, "introduced": 1942},
    "lockheed-f-104g": {"built": 1122},                # 2,578 is every F-104
    "mcdonnell-douglas-f-4e": {"built": 1370},         # 5,195 is every Phantom II

    # --- first flight of the prototype recorded against a much later variant
    "rockwell-b-1b": {"firstFlight": 1984},            # 1974 is the B-1A
    "douglas-a-20g": {"firstFlight": 1943, "introduced": 1943},   # 1938 is the DB-7
    "bell-p-39q-airacobra": {"firstFlight": 1944, "introduced": 1944},  # 1938 is the XP-39
    "curtiss-p-40e-warhawk": {"firstFlight": 1941},    # 1938 is the XP-40
    "junkers-ju-87d": {"firstFlight": 1941, "introduced": 1942},  # 1935 is the Ju 87 V1
    "heinkel-he-111h": {"firstFlight": 1939, "introduced": 1939},  # 1935 is the He 111 V1
    "messerschmitt-bf-110": {"firstFlight": 1942, "introduced": 1943},  # G-4; 1936 is the V1
    "gloster-meteor-f8": {"firstFlight": 1948, "introduced": 1950},  # 1943 is the prototype
    "de-havilland-vampire-fb5": {"firstFlight": 1948, "introduced": 1949},
    "english-electric-lightning-f6": {"firstFlight": 1964, "introduced": 1965},  # 1954 is the P.1
    "republic-f-84g": {"firstFlight": 1951, "introduced": 1952},   # 1946 is the XP-84
    "tupolev-tu-95ms": {"firstFlight": 1979, "introduced": 1984},  # 1952 is the Tu-95/1
    "sukhoi-su-22m4": {"firstFlight": 1983},           # 1966 is the S-32 / Su-17 prototype
    "bristol-blenheim-iv": {"firstFlight": 1937, "introduced": 1939},

    # --- outright wrong figures
    "xian-h-6k": {"mtowKg": 95000},                    # 79,000 is the original Tu-16
    "northrop-b-21": {"engineCount": 2},               # was null, which rendered as "— × jet"
}

# Same airframe entered the database twice under two names.
DROP = [
    "aero-l-39c",       # duplicate of aero-l-39-albatros, identical production count
    "lockheed-t-33",    # duplicate of lockheed-t-33a, identical production count
]

UNRESOLVED = [
    "sukhoi-su-17m / sukhoi-su-22m4: both carry 2,867, the whole Su-17/20/22 family total",
    "dassault-mirage-iiie: 1,422 is every Mirage III and 5 built",
    "supermarine-spitfire-mk-i: 1936 is the prototype; the Mk I itself flew in 1938",
    "fairchild-a-10: rangeKm 1,200 sits between the combat radius and the ferry range",
    "hesa-azarakhsh: sources disagree on whether it is single or twin engined",
    "iaio-qaher-313: no published figures at all; the airframe's status is itself disputed",
]
