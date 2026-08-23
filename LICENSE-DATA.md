# Licensing of the data and the photographs

The **code** in this repository — everything under `assets/` except the
photographs, everything under `scripts/`, and `index.html` — is MIT licensed.
See `LICENSE`.

## The aircraft data

`data/aircraft.json` and the tables it is built from are compiled from
manufacturers' public material and from reference works, chiefly Wikipedia.
Plain factual specifications are not themselves copyrightable, but the
descriptive notes were written for this project and the compilation as a whole
is released under **CC BY-SA 4.0**, which is compatible with the sources it
draws on.

    https://creativecommons.org/licenses/by-sa/4.0/

If you reuse the data, credit T-AIR and keep the same licence on any
redistributed version.

## The photographs

Photographs are **not** covered by either licence above. Each one keeps the
licence of its own photographer, recorded per image in `data/photos.json`
alongside the author's name, and shown under the picture in the interface.

`scripts/fetch_photos.py` only downloads files hosted on Wikimedia Commons,
which by Commons policy carry a free licence — most commonly CC BY-SA or a
public-domain dedication. Fair-use images hosted on Wikipedia itself are
deliberately skipped, so nothing in `assets/photos/` should be non-free.

If you redistribute the photographs, carry the per-image credit and licence
from `data/photos.json` with them.
