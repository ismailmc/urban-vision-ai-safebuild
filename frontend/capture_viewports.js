const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const targets = [
    { name: '1920x1080', width: 1920, height: 1080, isMobile: false },
    { name: '390x844_mobile', width: 390, height: 844, isMobile: true }
  ];

  for (const t of targets) {
    const page = await browser.newPage();
    await page.setViewport({ width: t.width, height: t.height, isMobile: t.isMobile });

    await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({
      path: `/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/landing_${t.name}.png`,
      fullPage: t.isMobile
    });
    console.log(`Saved landing_${t.name}.png`);

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
      path: `/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/studio_${t.name}.png`,
      fullPage: t.isMobile
    });
    console.log(`Saved studio_${t.name}.png`);

    await page.close();
  }

  await browser.close();
  console.log('Capture finished.');
})();
