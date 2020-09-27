const puppeteer = require('puppeteer');
const nodemailer = require('nodemailer');
const gmail_creds = require('../email_secret.json');
const fs = require('fs');

// number to send notifications
const PHONE_NUMBER = 6143701557;
const GATEWAY = 'messaging.sprintpcs.com';

// interval of time to deviate checking all PRODUCTS
const RAND_TIMER = parseInt(Math.random() * 60000); // RANGE (0,1) minutes

// text notifications
var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: gmail_creds.email,
    pass: gmail_creds.password,
  },
});

let mailOptions = {
  from: gmail_creds.email,
  to: `${PHONE_NUMBER}@${GATEWAY}`,
  subject: '',
  text: 'Started priceTracker',
};

// notify that script has been started
transporter.sendMail(mailOptions);

// notification txt
// item: object w url, currPrice
// productParams: object with product name, url, and lowPrice
async function SendNotification(item, productParams, headline) {
  // shorten url
  let finalUrl = item.url.slice(0, item.url.indexOf('?'));

  // 1st text
  mailOptions.text = `${headline}
${productParams.name}
$${item.currPrice} / $${productParams.lowPrice}`;

  await transporter.sendMail(mailOptions);

  // 2nd text
  mailOptions.text = finalUrl;
  await transporter.sendMail(mailOptions);
}

// product: el from PRODUCTS array
// page: page object from puppeteer
// find items under lowPrice threshold and return as array
async function findDeals(product, page) {
  await page.goto(product.url, { waitUntil: 'networkidle2' }).catch((e) => console.log(e));

  // evaluate page pushing to dealArray if found under threshhold
  dealArray = await page.evaluate((product) => {
    let itemArray = document.querySelectorAll('.srp-results > li');
    let dealArray = [];

    // iterate through items, add to dealArray when under price threshold (lowPrice)
    itemArray.forEach((item) => {
      let currPrice = parseFloat(item.querySelector('.s-item__price').innerText.replace('$', '').replace(',', ''));
      if (typeof currPrice === 'number' && currPrice <= product.lowPrice) {
        let url = item.querySelector('.s-item__info.clearfix > a')['href'];
        dealArray.push({ url, currPrice });
      }
    });
    return dealArray;
  }, product);

  return dealArray;
}

// async forEach function
async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

// check all products every set INTERVAL_TIMER
(async () => {
  console.log('checking for deals...');
  try {
    // init browser
    const browser = await puppeteer.launch({
      product: 'chrome',
      executablePath: '/usr/bin/chromium-browser',
      ignoreHTTPSErrors: true,
    });
    const page = await browser.newPage();
    page.setDefaultTimeout(30000);

    //init PRODUCTS array
    // array of product objects:
    // name: String
    // url: String
    // lowPrice: Float
    const PRODUCTS = JSON.parse(fs.readFileSync('products.json')).products;
    // iterate through PRODUCTS array, find deals for each product
    await asyncForEach(PRODUCTS, async (product) => {
      // find deals on the product page
      let dealArray = await findDeals(product, page);

      // load previously found deals
      let previouslyFoundDeals = JSON.parse(fs.readFileSync('foundDeals.json'));
      // if not previously found or found at cheaper price, send notification and add to previouslyFoundDeals
      await asyncForEach(dealArray, async (deal) => {
        // look if previously found
        let isNewDeal = true;
        let isBetterDeal = false;
        await asyncForEach(previouslyFoundDeals.deals, async (prevDeal) => {
          // if same product
          if (prevDeal.url === deal.url) {
            isNewDeal = false;
            // flag as better better deal if new price is lower
            if (prevDeal.price > deal.currPrice) {
              isBetterDeal = true;
              prevDeal.price = deal.currPrice;
            }
          }
        });

        // found a new deal
        if (isNewDeal) {
          console.log('Found new deal!');
          previouslyFoundDeals.deals.push({ url: deal.url, price: deal.currPrice });
          await SendNotification(deal, product, 'NEW DEAL');
        }
        // found at better price
        if (isBetterDeal) {
          console.log('Found better deal!');
          await SendNotification(deal, product, 'UPDATED DEAL');
        }
      });
      // resave the updated previouslyFoundDeals JSON object
      fs.writeFileSync('foundDeals.json', JSON.stringify(previouslyFoundDeals, null, 2));
      // wait between each fetch
      await new Promise((resolve) => setTimeout(resolve, 18000));
    });
    browser.close();
    // notify session is complete
    console.log('Tracking Session complete');
    mailOptions.text = 'Tracking session complete';
    await transporter.sendMail(mailOptions);
    await new Promise((resolve) => setTimeout(resolve, INTERVAL_TIMER));
  } catch (err) {
    console.log(err);
  }
})();
