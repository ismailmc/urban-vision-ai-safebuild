const puppeteer = require('../frontend/node_modules/puppeteer');
const path = require('path');
const fs = require('fs');

async function captureEvidence() {
  const outDir = path.join(__dirname, '../evidence/screenshots');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  console.log("Navigating to http://localhost:3000/...");
  await page.goto('http://localhost:3000/', { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('.maplibregl-canvas', { timeout: 15000 }).catch(() => console.log('Canvas wait timeout, continuing'));

  // Click "Try the Kakkanad example" to populate the model
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.includes('Try the Kakkanad example') || b.textContent.includes('Try Kakkanad example'));
    if (btn) btn.click();
  });
  await new Promise(r => setTimeout(r, 3000));

  // 1. Step 1: Road screen
  await page.screenshot({ path: path.join(outDir, '01_step1_road_selection.png') });
  console.log("Captured 01_step1_road_selection.png");

  // 2. Click Step 2: Access
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.trim().includes('2. Access'));
    if (btn) btn.click();
  });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(outDir, '02_step2_access_impact.png') });
  console.log("Captured 02_step2_access_impact.png");

  // 3. Click Step 3: Compare
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.trim().includes('3. Compare'));
    if (btn) btn.click();
  });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(outDir, '03_step3_compare_arrangements.png') });
  console.log("Captured 03_step3_compare_arrangements.png");

  // 4. Click Evidence & Advanced modal button
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.includes('Evidence & Advanced'));
    if (btn) btn.click();
  });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(outDir, '04_evidence_advanced_modal.png') });
  console.log("Captured 04_evidence_advanced_modal.png");

  // Close modal
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.includes('✕'));
    if (btn) btn.click();
  });
  await new Promise(r => setTimeout(r, 500));

  // 5. Click Explain with AI modal button
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.includes('Explain with AI'));
    if (btn) btn.click();
  });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(outDir, '05_ai_analyst_guarded_modal.png') });
  console.log("Captured 05_ai_analyst_guarded_modal.png");

  await browser.close();
  console.log("All evidence screenshots captured successfully!");
}

captureEvidence().catch(err => {
  console.error("Error capturing evidence:", err);
  process.exit(1);
});
