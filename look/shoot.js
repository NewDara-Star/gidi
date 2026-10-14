// Renders matching A/B screenshots from the five camera spots.
// NODE_PATH=~/node_modules node look/shoot.js [views] [looks] [time]
const { chromium } = require('playwright-core');
const path = require('path');
const views = (process.argv[2] || 'overview,steal,aisle,boss,ring').split(',');
const looks = (process.argv[3] || 'a,b').split(',');
const time = process.argv[4] || 'day';
(async () => {
  const browser = await chromium.launch({ channel: process.env.PW_CHANNEL || 'chrome', args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('console:', m.text().slice(0, 300)); });
  page.on('pageerror', e => console.log('pageerror:', e.message));
  const file = 'file://' + path.join(__dirname, 'ladi-lane-look.html');
  for (const look of looks) for (const view of views) {
    const t = Date.now();
    await page.goto(`${file}?shot&ui=0&labels=0&look=${look}&view=${view}&time=${time}`);
    await page.waitForFunction(() => document.title.startsWith('READY'), null, { timeout: 180000 });
    const out = path.join(__dirname, 'shots', `${view}-${look}${time === 'dusk' ? '-dusk' : ''}.jpg`);
    await page.screenshot({ path: out, type: 'jpeg', quality: 88 });
    console.log(out, (await page.title()).slice(6), ((Date.now() - t) / 1000).toFixed(1) + 's');
  }
  await browser.close();
})();
