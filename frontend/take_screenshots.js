const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  // 1. Landing Page
  console.log('Navigating to landing page...');
  await page.goto('http://localhost:3000', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: '/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/landing_page_studio.png', fullPage: true });
  console.log('Saved landing_page_studio.png');

  // 2. Open Planning Studio
  console.log('Opening Planning Studio...');
  const openButtons = await page.$$('button');
  for (const b of openButtons) {
    const text = await page.evaluate(el => el.innerText, b);
    if (text.includes('OPEN PLANNING STUDIO') || text.includes('Open Planning Studio')) {
      await b.click();
      break;
    }
  }
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: '/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/planning_studio_workspace.png' });
  console.log('Saved planning_studio_workspace.png');

  // 3. Switch to Alternatives Tab
  console.log('Switching to Alternatives tab...');
  const altButtons = await page.$$('button');
  for (const b of altButtons) {
    const text = await page.evaluate(el => el.innerText, b);
    if (text.includes('Alternatives')) {
      await b.click();
      break;
    }
  }
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({ path: '/home/ismail/.gemini/antigravity/brain/60135fd1-7216-428e-b4ee-481e91761cc1/screenshots/planning_studio_alternatives.png' });
  console.log('Saved planning_studio_alternatives.png');

  await browser.close();
  console.log('Screenshots capture complete.');
})();
