/* The pictures in the README's features section.
 *
 *   npm install playwright && npx playwright install chromium
 *   node scripts/shots_features.js     →  assets/_feat-*.png
 *   python3 scripts/shots_features.py  →  assets/shot-compare.png
 *                                         assets/shot-mobile.png
 *
 * Same reasoning as scripts/shot.js: a screenshot taken by hand is out of
 * date the next time the database grows, so these are driven from the real
 * interface and can be regenerated at any point.
 */
const { chromium } = require("playwright");
const path = require("path");
const URL = "file://" + path.resolve(__dirname, "..", "dist", "t-air.html");
const OUT = path.resolve(__dirname, "..", "assets");

const pick = async (p, q) => {
  await p.fill("#q", q);
  await p.waitForTimeout(350);
  await p.click(".cardwrap .card__pick");
  await p.waitForTimeout(150);
};

(async () => {
  const b = await chromium.launch();

  // --- the comparison table, three aircraft, light -------------------------
  const c = await b.newPage({ viewport: { width: 1280, height: 1500 },
                              deviceScaleFactor: 2 });
  await c.goto(URL);
  await c.waitForTimeout(1600);
  await pick(c, "f-14a");
  await pick(c, "mig-29");
  await pick(c, "f-16c");
  await c.click(".tray__go");
  await c.waitForTimeout(700);
  const cmp = await c.evaluate(() => {
    // the dialog that holds the table, trimmed to the table itself
    const t = document.querySelector(".cmp");
    const r = t.closest(".sheet, dialog, .modal, [role=dialog]") || t;
    const box = r.getBoundingClientRect();
    return { x: Math.round(box.x), y: Math.round(Math.max(box.y, 0)),
             width: Math.round(box.width),
             height: Math.round(Math.min(box.height, window.innerHeight - Math.max(box.y, 0))) };
  });
  await c.screenshot({ path: path.join(OUT, "_feat-compare.png"), clip: cmp });

  // --- three phones: the results, one record, and the dark theme ----------
  // The hero fills the first screen, so the list shot has to scroll past it
  // — a phone frame showing only the title says nothing about the app.
  const phones = [
    { file: "_feat-phone-list.png", hash: "", dark: false, scroll: true },
    { file: "_feat-phone-card.png", hash: "#/airbus-a350-900", dark: false, sheet: true },
    { file: "_feat-phone-dark.png", hash: "#/grumman-f-14a", dark: true, sheet: true },
  ];
  for (const s of phones) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 },
                                deviceScaleFactor: 3,
                                colorScheme: s.dark ? "dark" : "light",
                                isMobile: true, hasTouch: true });
    await p.goto(URL + s.hash);
    await p.waitForTimeout(1800);
    if (s.scroll) {
      // Land a card top flush under the sticky toolbar. Scrolling by a
      // guessed offset leaves a card sliced across the top edge, which is
      // the one thing a screenshot must not show.
      await p.evaluate(() => {
        // Put the search box at the very top of the frame: everything that
        // makes the app worth showing — the filters, the decade histogram,
        // the export buttons and the first card — follows it in one screen.
        const q = document.querySelector("#q");
        const box = q.closest("form, .search, div").getBoundingClientRect();
        window.scrollTo(0, window.scrollY + box.top - 8);
      });
      await p.waitForTimeout(600);
    }
    if (s.sheet) {
      // Until the photo library is fetched the band at the top of a record
      // is a placeholder; scroll it out of frame so the shot leads with the
      // specifications, which are the point.
      await p.evaluate(() => {
        const fig = document.querySelector(".sheet__photo");
        if (!fig) return;
        // Whichever ancestor actually scrolls — the sheet, a wrapper, or the
        // window — move it by the height of the band.
        let el = fig.parentElement, by = fig.offsetHeight;
        while (el && el !== document.body) {
          if (el.scrollHeight > el.clientHeight + 4) { el.scrollTop += by; return; }
          el = el.parentElement;
        }
        window.scrollBy(0, by);
      });
      await p.waitForTimeout(500);
    }
    await p.screenshot({ path: path.join(OUT, s.file) });
    await p.close();
  }

  await b.close();
  console.log("panels written — now run: python3 scripts/shots_features.py");
})();
