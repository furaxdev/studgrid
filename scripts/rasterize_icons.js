// Rasterise icons/svg/*.svg to PNG at 1x, 2x and 3x (24, 48, 72 px) with the pre-installed Chromium.
// Usage: node scripts/rasterize_icons.js
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const svgDir = path.join(root, 'icons', 'svg');
const outRoot = path.join(root, 'icons', 'png');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const names = fs.readdirSync(svgDir).filter((f) => f.endsWith('.svg')).sort();
  for (const scale of [1, 2, 3]) {
    const dir = path.join(outRoot, `${scale}x`);
    fs.mkdirSync(dir, { recursive: true });
    const px = 24 * scale;
    const page = await browser.newPage({ viewport: { width: px, height: px }, deviceScaleFactor: 1 });
    for (const f of names) {
      let svg = fs.readFileSync(path.join(svgDir, f), 'utf8');
      svg = svg.replace('width="24" height="24"', `width="${px}" height="${px}" style="color:#0B120F"`);
      await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
      await page.setViewportSize({ width: px, height: px });
      await page.screenshot({ path: path.join(dir, f.replace('.svg', '.png')), omitBackground: true, clip: { x: 0, y: 0, width: px, height: px } });
    }
    await page.close();
  }
  await browser.close();
  console.log(`rasterised ${names.length} icons at 1x/2x/3x`);
})().catch((e) => { console.error(e); process.exit(1); });
