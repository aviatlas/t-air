const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const errors = [];
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  const url = 'file:///home/claude/aircraft-db/dist/atlas-standalone.html';
  await page.goto(url);
  await page.waitForTimeout(1200);

  const count = await page.textContent('#count');
  console.log('results rendered:', count);

  await page.screenshot({ path: '/tmp/shot-light.png', fullPage: false });

  // search test
  await page.fill('#q', 'بویینگ ۷۳۷');
  await page.waitForTimeout(400);
  console.log('fa query "بویینگ ۷۳۷" ->', await page.textContent('#count'));

  await page.fill('#q', 'a350');
  await page.waitForTimeout(400);
  console.log('query "a350" ->', await page.textContent('#count'));

  // open detail
  await page.click('.card');
  await page.waitForTimeout(600);
  await page.screenshot({ path: '/tmp/shot-detail.png' });
  console.log('sheet title:', await page.textContent('#sheetTitle'));

  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);

  // dark theme
  const dark = await browser.newPage({ viewport: { width: 1280, height: 1000 }, colorScheme: 'dark' });
  dark.on('pageerror', e => errors.push('PAGEERROR(dark): ' + e.message));
  await dark.goto(url);
  await dark.waitForTimeout(1000);
  await dark.fill('#q', 'atr');
  await dark.waitForTimeout(300);
  await dark.screenshot({ path: '/tmp/shot-dark.png' });

  // mobile
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto(url);
  await m.waitForTimeout(900);
  const overflow = await m.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  console.log('mobile horizontal overflow:', overflow);
  await m.screenshot({ path: '/tmp/shot-mobile.png' });

  console.log('errors:', errors.length ? errors : 'none');
  await browser.close();
})();
