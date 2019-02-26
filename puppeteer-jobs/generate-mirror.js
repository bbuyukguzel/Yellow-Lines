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
			var getXPath = function (element) {
				if (element.tagName == 'HTML')    return '/html';
				if (element===document.body)      return '/html/body';
			    // calculate position among siblings
			    var position = 0;
			    // Gets all siblings of that element.
			    var siblings = element.parentNode.childNodes;
			    for (var i = 0; i < siblings.length; i++) {
			    	var sibling = siblings[i];
			        // Check Siblink with our element if match then recursively call for its parent element.
			        if (sibling === element)  return getXPath(element.parentNode)+'/'+element.tagName+'['+(position+1)+']';

			       // if it is a siblink & element-node then only increments position. 
			       var type = sibling.nodeType;
			       if (type === 1 && sibling.tagName === element.tagName)            position++;
			   }
			}

			var getXPathOther = function (element) {
				if(element && element.parentNode) {
					var xpath = getXPathOther(element.parentNode) + '/' + element.tagName;
					var s = [];
					for(var i = 0; i < element.parentNode.childNodes.length; i++) {
						var e = element.parentNode.childNodes[i];
						if(e.tagName == element.tagName) {
							s.push(e);
						}
					}
					if(1 < s.length) {
						for(var i = 0; i < s.length; i++) {
							if(s[i] === element) {
								xpath += '[' + (i+1) + ']';
								break;
							}
						}
					}

					return xpath.toLowerCase();
				}

				return '';
			}

			// https://github.com/victorlazaro/ScripturesMapped/blob/139bdd639981efbd097ab1e67b725652ed490a6e/ScripturesMapped/geocode.js
			var getXpathOtherOther = function (element) {
				if (element && element.id) {
					return '//*[@id=\"' + element.id + '\"]';
				}

				if (element.tagName != undefined && element.tagName.toLowerCase() === 'body') {
					return '/html/body';
				}

				return getElementTreeXPath(element);
			};

			var getElementTreeXPath = function (element) {
				var index = 1;
				var sibling;

				if (element.nodeType === Node.TEXT_NODE) {
					sibling = element.previousSibling;
					for (; sibling; sibling = sibling.previousSibling) {
						if (sibling.nodeType === Node.TEXT_NODE) {
							++index
						}
					}
					return getXpathOtherOther(element.parentNode) + '/text()[' + index + ']';
				}

				if (element.nodeType === Node.ELEMENT_NODE) {
					sibling = element.previousSibling;

					for (; sibling; sibling = sibling.previousSibling) {
						if (sibling.nodeName === element.nodeName) {
							++index
						}
					}

					return getXpathOtherOther(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + index + ']';
				}

				return index;
			};

			var getXpathOtherOtherOther = function(element) {
				if (element.id !=='')
					return '//*[@id="'+element.id+'"]';
				if (element===document.body)
					return element.tagName;
				var ix= 0;
				var siblings= element.parentNode.childNodes;
				for (var i= 0; i<siblings.length; i++) {
					var sibling= siblings[i];
					if (sibling===element)
						return getXPath(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
					if (sibling.nodeType===1 && sibling.tagName===element.tagName)
						ix++;
				}
			}

			var elements = document.getElementsByTagName("*");
			var result = []
			for (var i=0, max=elements.length; i < max; i++) {
				const {x, y, width, height} = elements[i].getBoundingClientRect();
				result.push({left: x, top: y, width, height, path: getXpathOtherOther(elements[i])})
			}

			return result;
		});

		console.log(result);
		await browser.close();
	})();
}


