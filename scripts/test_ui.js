/* Smoke test for the built single-file page.
 *
 *   npm install playwright && npx playwright install chromium
 *   node scripts/test_ui.js
 *
 * Covers the paths that have broken during development: bilingual search,
 * the filter combinations, comparison, deep links, both themes and phone
 * width. Exits non-zero on the first failure so it works as a CI gate.
 */

const { chromium } = require("playwright");
const path = require("path");

const URL = "file://" + path.resolve(__dirname, "..", "dist", "t-air.html");

let failures = 0;
function check(name, ok, detail) {
  if (ok) { console.log(`  ok    ${name}`); }
  else { failures++; console.log(`  FAIL  ${name}${detail ? " — " + detail : ""}`); }
}

const fa = s => s.replace(/[۰-۹]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d));

(async () => {
  const browser = await chromium.launch();
  const errors = [];

  // ---------------------------------------------------------------- desktop
  const page = await browser.newPage({ viewport: { width: 1340, height: 1000 } });
  page.on("pageerror", e => errors.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/ERR_/.test(m.text())) errors.push(m.text()); });
  await page.goto(URL);
  await page.waitForTimeout(1500);

  const total = Number(fa(await page.textContent("#count")));
  check("the whole database renders", total > 600, `${total} records`);
  check("the first page is capped", (await page.$$(".card")).length === 96);

  // search, both languages
  for (const [q, min] of [["بویینگ ۷۳۷", 10], ["boeing 737", 10], ["spitfire", 4],
                          ["tomcat", 1], ["اسپیتفایر", 4], ["helicopter", 40]]) {
    await page.fill("#q", q);
    await page.waitForTimeout(220);
    const n = Number(fa(await page.textContent("#count")));
    check(`search "${q}"`, n >= min, `${n} results`);
  }
  await page.fill("#q", "");
  await page.waitForTimeout(220);

  // filters
  await page.click(".seg__btn:nth-child(3)");
  await page.waitForTimeout(300);
  const mil = Number(fa(await page.textContent("#count")));
  check("military filter", mil > 400 && mil < total);
  await page.click(".seg__btn:nth-child(1)");
  await page.waitForTimeout(300);

  const bars = await page.$$(".timeline__bar");
  check("decade histogram is drawn", bars.length >= 10);
  await page.click(".timeline__bar:nth-child(5)");
  await page.waitForTimeout(300);
  const dec = Number(fa(await page.textContent("#count")));
  check("decade filter narrows the set", dec > 0 && dec < total);
  await page.click(".timeline__clear");
  await page.waitForTimeout(300);

  // comparison
  await page.fill("#q", "f-14");
  await page.waitForTimeout(250);
  await page.click(".cardwrap .card__pick");
  await page.fill("#q", "mig-29");
  await page.waitForTimeout(250);
  await page.click(".cardwrap .card__pick");
  await page.waitForTimeout(200);
  check("comparison tray appears", !(await page.$eval("#tray", e => e.hidden)));
  await page.click(".tray__go");
  await page.waitForTimeout(500);
  check("comparison table has rows", (await page.$$(".cmp tbody tr")).length >= 8);
  check("a leader is marked per row", (await page.$$(".cmp__v.is-best")).length > 0);
  await page.keyboard.press("Escape");
  await page.waitForTimeout(250);
  await page.click(".tray__clear");
  await page.fill("#q", "");
  await page.waitForTimeout(250);

  // deep link and history
  await page.click(".card");
  await page.waitForTimeout(500);
  const hash = await page.evaluate(() => location.hash);
  check("opening a card sets the address", /^#\/[a-z0-9-]+$/.test(hash), hash);
  await page.goBack();
  await page.waitForTimeout(350);
  check("back closes the sheet", await page.$eval("#scrim", e => e.hidden));

  // methodology sheet
  await page.click("#aboutBtn");
  await page.waitForTimeout(400);
  check("methodology sheet opens", (await page.$$(".prose h4")).length >= 5);
  await page.keyboard.press("Escape");
  await page.waitForTimeout(250);

  // language
  await page.click("#langBtn");
  await page.waitForTimeout(400);
  check("English switches direction", await page.evaluate(() => document.documentElement.dir) === "ltr");
  check("English keeps the record count",
        Number(await page.textContent("#count")) === total);
  await page.fill("#q", "بویینگ ۷۳۷");
  await page.waitForTimeout(250);
  check("Persian query still works in English",
        Number(await page.textContent("#count")) >= 10);
  await page.click("#langBtn");
  await page.waitForTimeout(350);
  check("Persian restores direction",
        await page.evaluate(() => document.documentElement.dir) === "rtl");

  // ------------------------------------------------------------------- dark
  const dark = await browser.newPage({ viewport: { width: 1340, height: 1000 }, colorScheme: "dark" });
  dark.on("pageerror", e => errors.push("dark: " + e.message));
  await dark.goto(URL);
  await dark.waitForTimeout(1200);
  const bg = await dark.$eval("body", e => getComputedStyle(e).backgroundColor);
  check("dark theme paints a dark ground", /rgb\((\d+), (\d+), (\d+)\)/.test(bg) &&
        bg.match(/\d+/g).slice(0, 3).every(v => Number(v) < 60), bg);

  // ----------------------------------------------------------------- mobile
  const phone = await browser.newPage({ viewport: { width: 390, height: 844 } });
  phone.on("pageerror", e => errors.push("mobile: " + e.message));
  await phone.goto(URL);
  await phone.waitForTimeout(1200);
  check("no horizontal overflow on a phone",
        !(await phone.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)));

  check("no console or page errors", errors.length === 0, errors.slice(0, 3).join(" | "));

  await browser.close();
  console.log();
  if (failures) { console.log(`${failures} check(s) failed`); process.exit(1); }
  console.log("all checks passed");
})();
