if (process.argv.length != 4) {
	console.log('Wrong argument usage. Format: <node.js path> <script path> <url> <output path>');
} 
else
{
	const puppeteer = require('puppeteer');
	const url = process.argv[2];
	const outputPath = process.argv[3];

	(async () => {
		const browser = await puppeteer.launch();
		const page = await browser.newPage();
		// TODO: Should puppeteer job timeout same with axios's timeout?
		await page.goto(url, { timeout: 100000, waitUntil: 'networkidle2' });
		await page.setViewport({width: 1024, height: 768});
		await page.screenshot({path: outputPath, fullPage: true});

		const result = await page.evaluate(() => {
			// TODO: this function might be moved to somewhere https://stackoverflow.com/a/47314102
			// https://stackoverflow.com/a/32201731
			var WebElement_XPath = function (element) {
			    if (element.tagName == 'HTML')    return '/html';
			    if (element===document.body)      return '/html/body';
			    // calculate position among siblings
			    var position = 0;
			    // Gets all siblings of that element.
			    var siblings = element.parentNode.childNodes;
			    for (var i = 0; i < siblings.length; i++) {
			        var sibling = siblings[i];
			        // Check Siblink with our element if match then recursively call for its parent element.
			        if (sibling === element)  return WebElement_XPath(element.parentNode)+'/'+element.tagName+'['+(position+1)+']';

			       // if it is a siblink & element-node then only increments position. 
			        var type = sibling.nodeType;
			        if (type === 1 && sibling.tagName === element.tagName)            position++;
			    }
			}

			var elements = document.getElementsByTagName("*");
			var result = []
			for (var i=110, max=elements.length; i < max; i++) {
				const {x, y, width, height} = elements[i].getBoundingClientRect();
				result.push({left: x, top: y, width, height, path: WebElement_XPath(elements[i])})
			}

			return result;
		});

		console.log(result);
		await browser.close();
	})();
}


