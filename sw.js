/* T-AIR service worker — makes the atlas work with no connection.
 *
 * Why: a reference people reach for is worth having on a plane, on the metro,
 * or on a connection that comes and goes. The whole site is a few static files
 * plus one JSON, so once they are in the cache there is nothing left to fetch.
 *
 * Strategy, deliberately simple:
 *   - install: pre-cache the shell (page, styles, script, strings, data)
 *   - fetch:   serve from cache, and refresh the copy in the background
 *   - activate: delete every cache that is not this version
 *
 * CACHE is stamped by scripts/build_single.py with the build's own signature,
 * so a deploy invalidates the old cache instead of leaving a reader on a
 * version from weeks ago. Requests to other origins (Wikipedia photographs,
 * fonts) are left alone — they are not ours to cache and a stale photo is not
 * worth the risk of serving one that was later removed for a licence problem.
 */

const CACHE = "t-air-0eeab50f84";          /* replaced at build time */

const SHELL = [
  "./",
  "./index.html",
  "./assets/styles.css",
  "./assets/app.js",
  "./assets/i18n.js",
  "./assets/logo.svg",
  "./assets/favicon.svg",
  "./data/aircraft.json"
];

self.addEventListener("install", function (e) {
  /* addAll fails the whole install if any one file is missing, which is the
     behaviour we want: a half-cached shell is worse than no cache. */
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }));
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        return k === CACHE ? null : caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   /* not ours to cache */

  e.respondWith(
    caches.match(req).then(function (hit) {
      var live = fetch(req).then(function (res) {
        if (res && res.status === 200 && res.type === "basic") {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      }).catch(function () {
        /* offline: fall back to the cached page for a navigation, so a deep
           link still opens rather than showing the browser's error page */
        return hit || (req.mode === "navigate" ? caches.match("./index.html") : undefined);
      });
      return hit || live;
    })
  );
});
