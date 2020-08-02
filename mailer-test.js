const nodemailer = require('nodemailer');
const gmail_creds = require('./email_secret.json');

// number to send notifications
const PHONE_NUMBER = 6143701557;
const GATEWAY = 'messaging.sprintpcs.com';

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
  text: '',
};

const name = 'sigma 16mm F/1.4 asdf asdf asdf a df sfd';
const price = 350;
const lowPrice = 400;
const url =
  'https://www.ebay.com/itm/Sigma-16mm-f-1-4-DC-DN-Contemporary-Lens-for-Sony-E-Mount-Cameras/283933951345?hash=item421bc84571%3Ag%3Aik4AAOSw2QZe%7EOQc&LH_BIN=1';
const produrl =
  'https://www.ebay.com/sch/i.html?_from=R40&_nkw=sigma+16mm+1.4+e+mount&_sacat=0&LH_TitleDesc=0&LH_BIN=1&_sop=15';

// shorten url
let finalUrl = url.slice(0, url.indexOf('?'));

mailOptions.text = `FOUND DEAL
${name}
$${price} / $${lowPrice}`;

transporter.sendMail(mailOptions);
