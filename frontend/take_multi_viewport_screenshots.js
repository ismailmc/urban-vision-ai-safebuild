const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const viewports = [
    { name: '1440x900', width: 1440, height: 900 },
    { name: '1920x1080', width: 1920, height: 1080 },
    { name: '390x844_mobile', width: 390, height: 844, isMobile: true }
  ];

  for (const vp of viewports) {
    const page = await browser.newPage();
    await page.setViewport({ width: vp.width, height: vp.height, isMobile: !!vp.isMobile });

    console.log(`Navigating at ${vp.name}...`);
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 1000));

    // 1. Landing Page screenshot
    await page.screenshot({
      path: `/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/landing_${vp.name}.png`,
      fullPage: vp.isMobile
    });
    console.log(`Saved landing_${vp.name}.png`);

    // 2. Open Planning Studio
    const openButtons = await page.$$('button');
    for (const b of openButtons) {
      const text = await page.evaluate(el => el.innerText, b);
      if (text.includes('Open Planning Studio') || text.includes('OPEN PLANNING STUDIO')) {
        await b.click();
        break;
      }
    }
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({
      path: `/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/studio_${vp.name}.png`
    });
    console.log(`Saved studio_${vp.name}.png`);

    await page.close();
  }

  await browser.close();
  console.log('Multi-viewport screenshot capture complete.');
})();
