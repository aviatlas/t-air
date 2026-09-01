# -*- coding: utf-8 -*-
"""Two corrections the build's own checks demanded after the verification run.

Both are the same shape. An agent moved a record's first-flight year onto the
variant the record actually names, which was right — but left the service-entry
year belonging to the original model, so the aircraft ended up entering service
years before it first flew. The date checks caught it immediately; this file
finishes the move the verification started.
"""

FIXES = {
    # MD 500 Defender: 1966 is the Model 500 / OH-6 line, not the Defender,
    # which first flew and entered service in 1976
    "mcdonnell-md-500": {"introduced": 1976},

    # F-8E: 1957 is the F8U-1's service entry; the E model reached squadrons
    # in 1962, a year after its 1961 first flight
    "vought-f-8e": {"introduced": 1962},
}
