// Render a preview HTML at desktop (1440) and phone (390) widths.
// Usage: node scripts/render_preview.js docs/previews/shop-chunky.html
// Output: docs/previews/renders/<name>-1440.png and <name>-390.png
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const input = path.resolve(process.argv[2]);
  const name = path.basename(input, '.html');
  const outDir = path.join(path.dirname(input), 'renders');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const width of [1440, 390]) {
    // Phone capture is shown to a person, so use deviceScaleFactor 2 for both.
    const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 2 });
    await page.goto('file://' + input, { waitUntil: 'load' });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    const out = path.join(outDir, `${name}-${width}.png`);
    await page.screenshot({ path: out, fullPage: true });
    console.log(`${out} horizontal_overflow_px=${overflow}`);
    await page.close();
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
