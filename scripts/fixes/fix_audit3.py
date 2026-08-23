# -*- coding: utf-8 -*-
"""Third audit — a stratified sample of 60 records (20 civil, 40 military,
every ~11th id in each category) read field by field, plus two full passes
over the error classes that sample exposed.

Three things came out of it:

1. A column transposition in the military rotorcraft table: 40 of 42 rows
   were written (speed, range) where the schema wants (range, speed), which
   is why Sea Kings were flying at 1230 km/h. That one is fixed at source in
   parts/rotary_mil.py, not here, because it is a data-entry bug rather than
   a disputed figure — and test_build.py now refuses to build a rotorcraft
   faster than 420 km/h so it cannot come back.

2. Production totals that quote the whole type on a single-variant record.
   This is the same failure mode the first two audits found; the ids are in
   FAMILY_COUNT so the interface marks the number.

3. Airliners marked retired that are still in daily service. The vocabulary
   here reads "retired" as "no longer flying" and "active" as "in service
   but out of production" — the 30 types below are all out of production and
   all still working, most of them in large numbers. Types genuinely down to
   a handful of airframes are left alone and listed in UNRESOLVED.
"""

FIXES = {
    # ---- dates taken from a different variant of the same aircraft --------
    "grumman-a-6":        {"firstFlight": 1970, "introduced": 1971},
    # 1960/1963 belong to the A-6A; the E model flew in 1970
    "lockheed-f-104g":    {"firstFlight": 1960, "introduced": 1961},
    # 1954 is the XF-104 and 1958 the F-104A; the G is a 1960 aircraft
    "xian-jh-7a":         {"firstFlight": 2002, "introduced": 2004},
    # 1988/1992 are the original JH-7
    "boeing-ch-47f":      {"firstFlight": 2001},
    # 1961 is the CH-47A — a 46-year gap to a 2007 service entry
    "sikorsky-uh-60m":    {"firstFlight": 2003, "introduced": 2007},
    # 1974/1979 are UH-60A figures

    # ---- production figures ----------------------------------------------
    "supermarine-spitfire-mk-vb": {"built": 3911},
    # 6,487 is every Mk V; the VB sub-variant is 3,911, and the family total
    # is neither number (about 20,300 Spitfires of all marks)

    # ---- family flags that were set the wrong way round -------------------
    # (the status change for these two is folded in here — a dict literal
    # keeps only the last entry for a repeated key)
    "airbus-a320-200":    {"builtFamily": False, "status": "active"},
    "airbus-a321-200":    {"builtFamily": False, "status": "active"},
    # 4,745 and 1,791 are the variants' own delivery counts (4,745 includes
    # 21 A320-100s), not the ceo family, which is about 8,100 aircraft — the
    # sibling records airbus-a319 and boeing-737-800 carry the same kind of
    # figure unflagged

    # ---- range ------------------------------------------------------------
    "airbus-a340-200":    {"rangeKm": 15000},
    # the shortened -200 out-ranged the -300 (13,500 km here); 12,400 km is
    # below its own sibling and contradicts the record's own note

    # ---- translation ------------------------------------------------------
    "beriev-a-50": {
        "armament": "بدون تسلیحات؛ رادار چرخان شمل (زنبور)",
        "armament_en": "Unarmed; the rotating Shmel ('Bumblebee') radar",
    },
    # Vega Shmel is Russian for bumblebee — "sword" was a mistranslation

    # ---- out of production, still in service ------------------------------
    # (see the docstring; all of these were marked retired)
    "airbus-a300-600r":   {"status": "active"},   # the FedEx and UPS freighters
    "airbus-a310-300":    {"status": "active"},   # MRTT tankers and freighters
    "airbus-a319":        {"status": "active"},
    # a320-200 and a321-200 are above, with their family flags
    "airbus-a330-200":    {"status": "active"},
    "airbus-a330-300":    {"status": "active"},
    "airbus-a340-300":    {"status": "active"},
    "airbus-a380-800":    {"status": "active"},
    "atr-72-500":         {"status": "active"},
    "bae-146-300":        {"status": "active"},   # regional, freight and firefighting
    "boeing-737-300":     {"status": "active"},   # largely as freighters now
    "boeing-737-400":     {"status": "active"},
    "boeing-737-500":     {"status": "active"},
    "boeing-737-700":     {"status": "active"},
    "boeing-737-800":     {"status": "active"},
    "boeing-737-900er":   {"status": "active"},
    "boeing-747-400":     {"status": "active"},   # the freighter fleet above all
    "boeing-757-200":     {"status": "active"},
    "boeing-777-200er":   {"status": "active"},
    "bombardier-crj200":  {"status": "active"},
    "bombardier-crj700":  {"status": "active"},
    "bombardier-crj900":  {"status": "active"},
    "dehavilland-dash8-300": {"status": "active"},
    "dornier-328":        {"status": "active"},
    "embraer-e190":       {"status": "active"},
    "embraer-erj-145":    {"status": "active"},
    "fokker-50":          {"status": "active"},   # still flying, Iran included
    "fokker-100":         {"status": "active"},   # Iran Air's fleet is the largest left
    "saab-340b":          {"status": "active"},
}

# Production totals that are published only for the whole type. The record
# keeps the number — it is the one figure that exists — and the interface
# marks it so it is not read as this variant's output.
FAMILY_COUNT = [
    "bristol-beaufighter-mk-vif",  # 5,928 is every Beaufighter mark
    "curtiss-p-36a-hawk",          # 1,115 is the P-36/Hawk 75 line with exports
    "dornier-do-17z",              # 2,139 is every Do 17
    "grumman-a-6",                 # 693 is the whole A-6 line
    "lavochkin-la-5fn",            # 9,920 is every La-5
    "mikoyan-mig-25p",             # 1,186 is every MiG-25, P through BM
    "mitsubishi-ki-21",            # 2,064 is Mitsubishi and Nakajima together
    "saab-j-29f",                  # 661 is all Saab 29s; the F was a rebuild
    "tupolev-tu-95ms",             # about 500 covers the Tu-95 and Tu-142 line
    "airbus-a310-300",             # 255 is the A310 total, as on the -200 record
]

UNRESOLVED = [
    "bae-jetstream-31, tupolev-tu-154m, mcdonnell-md-82/-83: down to a handful "
    "of freighters or government aircraft — 'retired' overstates it and "
    "'active' overstates it more, so both are left as they were",
    "boeing-747sp: cruise 994 km/h is high against the 907-917 of every other "
    "747 here, but the SP genuinely cruised faster and sources disagree",
    "lockheed-t-33a: 6,557 includes Canadair and Kawasaki licence production; "
    "Lockheed alone built 5,691 and the record may intend either",
    "variant records carrying the parent type's first-flight date: the sample "
    "suggests 40 to 70 of them, but the ones checked were a mix of deliberate "
    "and accidental, so they need a full pass rather than a sampled guess",
    "military types marked retired that a few air forces still fly (MiG-21, "
    "F-5E, Mirage F1): the same question as the airliners above, but the "
    "fleets are small and poorly documented",
]
