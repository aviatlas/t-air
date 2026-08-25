# Licensing of the data and the photographs

The **code** in this repository — everything under `assets/` except the
photographs, everything under `scripts/`, and `index.html` — is MIT licensed.
See `LICENSE`.

## The aircraft data

`data/aircraft.json` and the tables it is built from are compiled from
manufacturers' public material and from reference works, chiefly the English
Wikipedia. Plain factual specifications — a speed, a wingspan, a production
count — are not themselves copyrightable, but a compilation can be, and part
of this one was built by reading Wikipedia articles. The descriptive notes are
original Persian text written for this project.

The whole compilation is released under **CC BY-SA 4.0**, the same licence
English Wikipedia uses, so that anything derived from it stays under the same
terms.

    https://creativecommons.org/licenses/by-sa/4.0/

### Attribution of the sources

Material in this database is derived in part from the English Wikipedia
(<https://en.wikipedia.org>), text there being available under CC BY-SA 4.0:

    https://creativecommons.org/licenses/by-sa/4.0/

**It has been changed.** The figures were re-expressed in metric units, cut
down to one row per variant, translated into Persian, and corrected where an
audit found an error; the article text itself is not reproduced. Each record
names the article it corresponds to in its `wiki` field and links to it, and
records that have been read against that article field by field are marked in
the interface.

If you reuse this data, credit T-AIR and the English Wikipedia, keep the same
licence on any redistributed version, and say what you changed.

## The photographs

Photographs are **not** covered by either licence above. Each one keeps the
licence of its own photographer, recorded per image in `data/photos.json`
alongside the author's name, and shown under the picture in the interface.

`scripts/fetch_photos.py` only downloads files hosted on Wikimedia Commons,
and only those whose licence matches an **allowlist** of terms that permit
reuse and adaptation by anyone — CC0, CC BY, CC BY-SA, public domain, GFDL and
similar. Anything carrying a non-commercial or no-derivatives term, anything
marked fair use or "with permission", and any licence template the script does
not recognise is skipped rather than guessed at. Fair-use stills hosted on
Wikipedia itself are never touched, because the script asks Commons, not
Wikipedia, for the file.

Under each photograph the interface prints the photographer, the licence, and
a link to the file's own page on Commons — the three things CC BY and CC BY-SA
ask for.

If you redistribute the photographs, carry the per-image credit and licence
from `data/photos.json` with them.
