
if (process.argv.length < 4 || process.argv.length > 4) {
    console.log('Wrong argument usage');
} 
else
{
	const puppeteer = require('puppeteer');
	const url = process.argv[2];
	const outputPath = process.argv[3];

	(async () => {
	  const browser = await puppeteer.launch();
	  const page = await browser.newPage();
	  await page.goto(url, { waitUntil: 'load' });
	  await page.setViewport({width: 1024, height: 768});
	  await page.screenshot({path: outputPath, fullPage: true});

	  await browser.close();
	})();
}
