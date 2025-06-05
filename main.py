const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const SocksProxyAgent = require('socks-proxy-agent');
const fs = require('fs');

puppeteer.use(StealthPlugin());

async function fetchBrowserInfoWithProxy() {
  const url = 'https://browserleaks.com/ip';
  const socks5Proxy = 'socks5://80.242.229.86:21399';

  // Launch a headless browser with SOCKS5 proxy
  const browser = await puppeteer.launch({
    args: [--proxy-server=${socks5Proxy}],
  });

  try {
    // Open a new page
    const page = await browser.newPage();

    // Set a longer timeout (e.g., 60 seconds)
    await page.setDefaultNavigationTimeout(60000);

    // Wait for the page to load completely
    await page.goto(url, { waitUntil: 'domcontentloaded' });

    // Wait for the #content element to be present
    await page.waitForSelector('#content');

    // Scroll to the end of the #content element to ensure it's fully visible
    await page.$eval('#content', content => {
      content.scrollTo(0, content.scrollHeight);
    });

    // Wait for additional time (e.g., 5 seconds) to ensure all content is loaded
    await page.waitForTimeout(5000);

    // Capture a screenshot of the entire #content element
    const screenshotBuffer = await page.screenshot({
      clip: await page.$eval('#content', content => {
        const boundingBox = content.getBoundingClientRect();
        return {
          x: boundingBox.x,
          y: boundingBox.y,
          width: boundingBox.width,
          height: boundingBox.height,
        };
      }),
    });

    // Save the screenshot to a file
    fs.writeFileSync('content_screenshot_ip.png', screenshotBuffer);

    console.log('Screenshot saved as content_screenshot_ip.png');

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    // Close the browser after capturing the screenshot
    await browser.close();
  }
}

// Call the function to fetch and save a screenshot of the #content element with SOCKS5 proxy
fetchBrowserInfoWithProxy();