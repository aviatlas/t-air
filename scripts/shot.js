/* Rebuild the README hero from the live interface.
 *
 *   npm install playwright && npx playwright install chromium
 *   node scripts/shot.js          →  assets/screenshot.png
 *
 * The image is two panels: the atlas as it opens, and one record. It is
 * generated rather than captured by hand so it never falls out of date —
 * a README picture showing 300 aircraft when the database holds 656 is
 * worse than none. The composition (rounded corners, drop shadow, the
 * gradient behind) is finished by scripts/shot.py, which needs Pillow.
 */
const { chromium } = require("playwright");
const path = require("path");
const URL = "file://" + path.resolve(__dirname, "..", "dist", "t-air.html");
const OUT = path.resolve(__dirname, "..", "assets");

(async () => {
  const b = await chromium.launch();

  const p = await b.newPage({ viewport: { width: 1440, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto(URL);
  await p.waitForTimeout(1800);
  // end the panel flush with the first row of cards, so nothing is half cut
  const cut = await p.evaluate(() => {
    const cards = [...document.querySelectorAll(".cardwrap")];
    const top = cards[0].getBoundingClientRect().top;
    const row = cards.filter(c => Math.abs(c.getBoundingClientRect().top - top) < 4);
    return Math.round(row[0].getBoundingClientRect().bottom + 2);
  });
  await p.screenshot({ path: path.join(OUT, "_shot-main.png"),
                       clip: { x: 0, y: 0, width: 1440, height: cut } });

  // one record, dark, without the photograph band (which may be empty)
  const d = await b.newPage({ viewport: { width: 1000, height: 1300 },
                              deviceScaleFactor: 2, colorScheme: "dark" });
  await d.goto(URL + "#/grumman-f-14a");
  await d.waitForTimeout(1800);
  const box = await d.evaluate(() => {
    const s = document.querySelector(".sheet").getBoundingClientRect();
    const fig = document.querySelector(".sheet__photo").getBoundingClientRect();
    const parts = [...document.querySelectorAll(".sheet__body > *")];
    const end = parts.find(e => e.textContent.includes("موتور و پیشینه")) || parts[parts.length - 1];
    return { x: Math.round(s.x), y: Math.round(fig.bottom), width: Math.round(s.width),
             height: Math.round(end.getBoundingClientRect().top - fig.bottom) };
  });
  await d.screenshot({ path: path.join(OUT, "_shot-sheet.png"), clip: box });

  await b.close();
  console.log("panels written — now run: python3 scripts/shot.py");
})();
