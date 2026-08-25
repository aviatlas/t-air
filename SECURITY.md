# Security

T-AIR is a static site. There is no server, no account, no cookie and no
database — the whole thing is one HTML file, one JSON file, and the assets
beside them. That removes most of the usual attack surface, but not all of it,
so this is what has been checked and what the remaining exposure is.

## What the page executes

All text that comes from the data — model names, Persian and English notes,
roles, armament, engine names, photograph credits — reaches the DOM through
`textContent`, never through `innerHTML`. The only `innerHTML` assignments in
`assets/app.js` are literal SVG icons and the methodology text, whose only
interpolated values are counts computed from the data as numbers. There is no
`eval`, no `new Function`, and no `document.write`.

The `#/<id>` deep link is looked up in an id map; an id that is not in the map
opens nothing. Nothing from the address bar is written into the page.

## What the page fetches

| Host | What for | What it sends |
|---|---|---|
| `fonts.googleapis.com`, `fonts.gstatic.com` | the four typefaces | the visitor's IP and browser, as any font CDN does |
| `en.wikipedia.org` | the lead-image lookup when a record is opened and no local photo exists | the article title of the aircraft the visitor opened |
| `upload.wikimedia.org` | the image itself | the image request |

Search terms never leave the browser: filtering and search run entirely on the
loaded JSON. The Wikipedia request carries `referrerPolicy: no-referrer`, so
the site's own URL is not passed on, and the image URL returned by the API is
refused unless it is on `upload.wikimedia.org`.

With no network at all the site still works; only the photographs are missing.

Self-hosting the fonts would remove the Google request entirely — that is the
one privacy improvement left, and it costs about 400 KB in the repository.

## Content-Security-Policy

`index.html` carries a CSP `<meta>`. `script-src` has to keep `'unsafe-inline'`
because the single-file build inlines its own script and style; what the policy
still enforces is that no external script can load, no object or plugin can be
embedded, no `<base>` can rewrite relative URLs, no form can post anywhere, and
images and API calls are limited to Wikimedia.

`frame-ancestors` is missing because a `<meta>` CSP cannot carry it — it needs
a real HTTP response header, which GitHub Pages does not let a project set. If
clickjacking matters for your deployment, serve the site somewhere you control
the headers and add `frame-ancestors 'self'` and `X-Content-Type-Options:
nosniff` there.

## Data export

The CSV export prefixes any cell beginning with `=`, `+`, `-`, `@`, a tab or a
carriage return with an apostrophe, so a spreadsheet reads it as text instead of
executing it as a formula. Quoting follows RFC 4180.

## The photograph downloader

`scripts/fetch_photos.py` runs on your machine, not on the site, and only it
touches the network with write access to the repository. It refuses any URL
that is not on `upload.wikimedia.org`, refuses a response whose content type is
not an image, stops reading at 25 MB, caps decoded pixels against a
decompression bomb, and rejects a record id that is not `[a-z0-9-]` before
using it as a filename.

## Continuous integration

`.github/workflows/checks.yml` runs on `push` and `pull_request` — not
`pull_request_target` — so a fork's pull request never runs with repository
secrets. The workflow needs no secrets and has no write permission.

## Reporting something

Open an issue in the repository. If you would rather not do that in public,
say so in an issue without the details and a private channel can be arranged.
