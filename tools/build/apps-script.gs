// The Wonder Agency website forms -> this Google Sheet (two tabs), an alert to the team,
// and a branded thank-you email to the person who filled it in.
//
// Paste over everything in Extensions > Apps Script, save, then:
// Deploy > Manage deployments > edit (pencil) > Execute as: Me, Who has access: Anyone > New version > Deploy.

var NOTIFY = 'charles@thewonder.group,hello@thewonder.group';   // who gets the alerts
var REPLY_TO = 'hello@thewonder.group';                          // where replies to the thank-you email go
var SITE = 'https://thewonderagency.co/';
var IMG = SITE + 'images/email/';
var INSTAGRAM = 'https://www.instagram.com/the.wonder.list/';

var TABS = {
  audit:   { name: 'Free audits', head: ['Received', 'Name', 'Email', 'Venue', 'Website / Instagram', 'Notes', 'Accepted privacy policy', 'Page'] },
  contact: { name: 'Enquiries',   head: ['Received', 'Name', 'Email', 'Company', 'Topic', 'Message', 'Accepted privacy policy', 'Page'] }
};

// Opening the web app link in a browser shows this, so you can check it's public.
function doGet() {
  return ContentService.createTextOutput('Wonder Agency form is working');
}

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};
    if (p.website) return reply({ ok: true });            // spam trap filled in: ignore quietly
    var f = {
      kind: p.kind === 'contact' ? 'contact' : 'audit',
      name: clean(p.name), email: clean(p.email), venue: clean(p.venue), link: clean(p.link),
      topic: clean(p.topic), notes: clean(p.notes != null ? p.notes : p.field),
      consent: clean(p.checkbox), page: clean(p.page)
    };
    if (!f.email && !f.notes) return reply({ ok: false });
    var validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email);

    // 1. the Sheet
    tab(f.kind).appendRow(f.kind === 'audit'
      ? [new Date(), f.name, f.email, f.venue, f.link, f.notes, f.consent, f.page]
      : [new Date(), f.name, f.email, f.venue, f.topic, f.notes, f.consent, f.page]);

    // 2. the alert to the team
    var alert = {
      to: NOTIFY,
      subject: (f.kind === 'audit' ? 'Free audit request from ' : 'Website enquiry from ') + (f.name || f.email || 'someone'),
      body: alertText(f),
      htmlBody: alertHtml(f),
      name: 'The Wonder Agency website'
    };
    if (validEmail) alert.replyTo = f.email;
    MailApp.sendEmail(alert);

    // 3. the thank-you email to them
    if (validEmail) {
      var t = thanks(f);
      MailApp.sendEmail({ to: f.email, subject: t.subject, body: t.text, htmlBody: t.html, name: 'The Wonder Agency', replyTo: REPLY_TO });
    }
    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false });
  }
}

// ---------- the thank-you email ----------
function thanks(f) {
  var first = (f.name || '').split(' ')[0] || 'there';
  var audit = f.kind === 'audit';
  var subject = audit ? 'We’re preparing your marketing audit' : 'Thank you for getting in touch';
  var pre = audit ? 'We’ve got your request and we’re getting started on your audit.' : 'We’ve got your message and we’ll be in touch soon.';
  var hero = IMG + (audit ? 'audit-hero.jpg' : 'contact-hero.jpg');
  var label = audit ? 'Your free audit' : 'Message received';
  var heading = 'Thank you, ' + esc(first) + '.';
  var intro = audit
    ? 'We’ve got your request' + (f.venue ? ' for <span style="color:#ffffff">' + esc(f.venue) + '</span>' : '') + ', and we’ll begin preparing your marketing audit.'
    : 'We’ve got your message, and someone from the team will get back to you soon.';
  var body = audit
    ? 'We’ll look at your marketing the way a guest finds you: your social media, your ads, how you show up on Google and in AI search, and your website and booking journey. Then we’ll send you a plain summary of what’s working, what isn’t and what we’d fix first.'
    : 'If it’s about your marketing and you’d like a proper look at what’s working, we also offer a free audit. There’s a link below.';
  var steps = audit ? [['01', 'Social and content'], ['02', 'Paid ads'], ['03', 'Search and AI search'], ['04', 'Website and booking']] : [];
  var quote = !audit && f.notes ? f.notes : '';
  var extra = audit
    ? 'Anything you’d like us to look at in particular? Just reply to this email.'
    : 'Need us sooner? Reply to this email or call <a href="tel:+447775022514" style="color:#5eadba;text-decoration:none">+44 777 502 2514</a>.';

  var html = shell(pre,
    // hero
    '<tr><td style="padding:0"><img src="' + hero + '" width="600" alt="" style="display:block;width:100%;max-width:600px;height:auto;border:0;border-radius:18px 18px 0 0"></td></tr>' +
    // copy
    '<tr><td style="background:#0b0b0b;padding:44px 44px 12px">' +
      '<div style="font:500 11px/1.4 Manrope,Helvetica,Arial,sans-serif;letter-spacing:3px;text-transform:uppercase;color:#5eadba">' + label + '</div>' +
      '<h1 style="margin:16px 0 18px;font:400 38px/1.12 Marcellus,Georgia,serif;letter-spacing:.5px;text-transform:uppercase;color:#ffffff">' + heading + '</h1>' +
      '<p style="margin:0 0 16px;font:400 17px/1.6 Manrope,Helvetica,Arial,sans-serif;color:#e6e6e6">' + intro + '</p>' +
      '<p style="margin:0 0 8px;font:300 15px/1.7 Manrope,Helvetica,Arial,sans-serif;color:#bdbdbd">' + body + '</p>' +
    '</td></tr>' +
    (steps.length ? '<tr><td style="background:#0b0b0b;padding:16px 44px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' +
      steps.map(function (s) { return '<tr><td style="padding:13px 0;border-top:1px solid #262626;font:400 12px/1.4 Manrope,Helvetica,Arial,sans-serif;color:#5eadba;width:44px">' + s[0] + '</td><td style="padding:13px 0;border-top:1px solid #262626;font:400 19px/1.3 Marcellus,Georgia,serif;color:#ffffff;text-transform:uppercase;letter-spacing:.5px">' + s[1] + '</td></tr>'; }).join('') +
      '<tr><td colspan="2" style="border-top:1px solid #262626;font-size:0;line-height:0">&nbsp;</td></tr></table></td></tr>' : '') +
    (quote ? '<tr><td style="background:#0b0b0b;padding:18px 44px 6px"><div style="border-left:2px solid #255A63;padding:4px 0 4px 18px;font:300 14px/1.7 Manrope,Helvetica,Arial,sans-serif;color:#9a9a9a;white-space:pre-wrap">' + esc(quote).slice(0, 1200) + '</div></td></tr>' : '') +
    '<tr><td style="background:#0b0b0b;padding:18px 44px 40px;border-radius:0 0 18px 18px"><p style="margin:0 0 26px;font:300 15px/1.7 Manrope,Helvetica,Arial,sans-serif;color:#bdbdbd">' + extra + '</p>' +
      button(audit ? SITE + 'work/' : SITE + 'free-audit/', audit ? 'See what our audits lead to' : 'Get a free audit') + '</td></tr>' +
    // The Wonder List
    '<tr><td style="padding:14px 0 0;background:#000">&nbsp;</td></tr>' +
    '<tr><td style="padding:0"><a href="' + INSTAGRAM + '"><img src="' + IMG + 'wonder-list.jpg" width="600" alt="" style="display:block;width:100%;max-width:600px;height:auto;border:0;border-radius:18px 18px 0 0"></a></td></tr>' +
    '<tr><td style="background:#255A63;padding:36px 44px 40px;border-radius:0 0 18px 18px">' +
      '<div style="font:500 11px/1.4 Manrope,Helvetica,Arial,sans-serif;letter-spacing:3px;text-transform:uppercase;color:#cfe7ea">In the meantime</div>' +
      '<h2 style="margin:14px 0 14px;font:400 28px/1.15 Marcellus,Georgia,serif;text-transform:uppercase;letter-spacing:.5px;color:#ffffff">Where to go next</h2>' +
      '<p style="margin:0 0 24px;font:300 15px/1.7 Manrope,Helvetica,Arial,sans-serif;color:#e3f1f2">Looking for somewhere good to eat, drink or stay? Our sister account, The Wonder List, shares the restaurants, bars and hotels we can’t stop talking about.</p>' +
      button(INSTAGRAM, 'Follow The Wonder List', true) +
    '</td></tr>');

  var text = (audit ? 'Thank you, ' + first + '.\n\nWe’ve got your request' + (f.venue ? ' for ' + f.venue : '') + ', and we’ll begin preparing your marketing audit. We’ll look at your social media, ads, Google and AI search, and your website, then send you a plain summary of what’s working, what isn’t and what we’d fix first.\n\nAnything you’d like us to look at in particular? Just reply to this email.'
                    : 'Thank you, ' + first + '.\n\nWe’ve got your message, and someone from the team will get back to you soon. Need us sooner? Reply to this email or call +44 777 502 2514.') +
    '\n\nIn the meantime, looking for somewhere good to eat, drink or stay? Follow The Wonder List: ' + INSTAGRAM +
    '\n\nThe Wonder Agency\n' + SITE + '\nhello@thewonder.group · +44 777 502 2514';
  return { subject: subject, html: html, text: text };
}

// ---------- the alert to the team ----------
function alertText(f) {
  var lines = f.kind === 'audit'
    ? ['Name: ' + f.name, 'Email: ' + f.email, 'Venue: ' + f.venue, 'Website / Instagram: ' + f.link]
    : ['Name: ' + f.name, 'Email: ' + f.email, 'Company: ' + f.venue, 'Topic: ' + f.topic];
  return lines.join('\n') + '\n\n' + f.notes + '\n\nAccepted privacy policy: ' + f.consent + '\nSent from: ' + f.page;
}
function alertHtml(f) {
  var rows = f.kind === 'audit'
    ? [['Name', f.name], ['Email', f.email], ['Venue', f.venue], ['Website / Instagram', f.link], ['Notes', f.notes]]
    : [['Name', f.name], ['Email', f.email], ['Company', f.venue], ['Topic', f.topic], ['Message', f.notes]];
  rows.push(['Privacy policy', f.consent], ['Sent from', f.page]);
  return shell(f.kind === 'audit' ? 'New free audit request' : 'New website enquiry',
    '<tr><td style="background:#0b0b0b;padding:40px 44px;border-radius:18px">' +
    '<div style="font:500 11px/1.4 Manrope,Helvetica,Arial,sans-serif;letter-spacing:3px;text-transform:uppercase;color:#5eadba">' + (f.kind === 'audit' ? 'New free audit request' : 'New website enquiry') + '</div>' +
    '<h1 style="margin:14px 0 24px;font:400 30px/1.15 Marcellus,Georgia,serif;text-transform:uppercase;color:#ffffff">' + esc(f.name || f.email || 'Someone') + (f.venue ? '<br><span style="color:#5eadba">' + esc(f.venue) + '</span>' : '') + '</h1>' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' +
    rows.map(function (r) { return '<tr><td style="padding:12px 0;border-top:1px solid #262626;font:500 11px/1.5 Manrope,Helvetica,Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#8c8c8c;width:150px;vertical-align:top">' + r[0] + '</td><td style="padding:12px 0;border-top:1px solid #262626;font:400 15px/1.6 Manrope,Helvetica,Arial,sans-serif;color:#ffffff;white-space:pre-wrap">' + linkify(esc(r[1] || '–')) + '</td></tr>'; }).join('') +
    '</table><p style="margin:26px 0 0;font:300 13px/1.6 Manrope,Helvetica,Arial,sans-serif;color:#8c8c8c">Reply to this email to answer them directly. They’ve already been sent a thank-you email.</p></td></tr>', true);
}

// ---------- building blocks ----------
function shell(preheader, rows, plain) {
  return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><meta name="supported-color-schemes" content="dark light">' +
    '<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Manrope:wght@300;400;500&display=swap" rel="stylesheet">' +
    '<style>@media (max-width:620px){.wa-pad{padding-left:16px!important;padding-right:16px!important}h1{font-size:30px!important}}a{color:#5eadba}</style></head>' +
    '<body style="margin:0;padding:0;background:#000000">' +
    '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#000">' + esc(preheader) + '&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</div>' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#000000"><tr><td align="center" class="wa-pad" style="padding:36px 20px 40px">' +
    '<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px">' +
    // header
    '<tr><td style="padding:0 4px 28px"><a href="' + SITE + '" style="text-decoration:none"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>' +
      '<td style="vertical-align:middle;padding-right:12px"><img src="' + IMG + 'w-mark.png" width="40" alt="" style="display:block;width:40px;height:auto;border:0"></td>' +
      '<td style="vertical-align:middle;font:400 14px/1 Marcellus,Georgia,serif;letter-spacing:4px;text-transform:uppercase;color:#ffffff">The Wonder Agency</td></tr></table></a></td></tr>' +
    rows +
    // footer
    (plain ? '' : '<tr><td style="padding:36px 4px 0;font:300 12px/1.8 Manrope,Helvetica,Arial,sans-serif;color:#7a7a7a">' +
      '<span style="font:400 13px/1 Marcellus,Georgia,serif;letter-spacing:3px;text-transform:uppercase;color:#bdbdbd">Made to be booked out</span><br><br>' +
      'The Wonder Agency · London<br><a href="mailto:hello@thewonder.group" style="color:#bdbdbd;text-decoration:none">hello@thewonder.group</a> · <a href="tel:+447775022514" style="color:#bdbdbd;text-decoration:none">+44 777 502 2514</a><br>' +
      '<a href="' + SITE + '" style="color:#5eadba;text-decoration:none">thewonderagency.co</a> · <a href="' + INSTAGRAM + '" style="color:#5eadba;text-decoration:none">Instagram</a><br><br>' +
      'You’re getting this one email because you contacted us through our website. See our <a href="' + SITE + 'privacy/" style="color:#7a7a7a">privacy policy</a>.</td></tr>') +
    '</table></td></tr></table></body></html>';
}

function button(href, text, light) {
  var bg = light ? '#ffffff' : '#255A63', fg = light ? '#0b2a2f' : '#ffffff';
  return '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-radius:999px;background:' + bg + '">' +
    '<a href="' + href + '" style="display:inline-block;padding:15px 28px;font:600 12px/1 Manrope,Helvetica,Arial,sans-serif;letter-spacing:2.5px;text-transform:uppercase;color:' + fg + ';text-decoration:none;border-radius:999px">' + text + ' &nbsp;&rarr;</a></td></tr></table>';
}

// Finds the tab for this form, creating it with a bold, frozen header row the first time.
function tab(kind) {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), t = TABS[kind];
  var sh = ss.getSheetByName(t.name);
  if (!sh) {
    sh = ss.insertSheet(t.name);
    sh.appendRow(t.head);
    sh.getRange(1, 1, 1, t.head.length).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  return sh;
}

function esc(v) { return String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
function linkify(s) { return s.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" style="color:#5eadba">$1</a>'); }

// Stops spreadsheet formulas being injected and trims very long input.
function clean(v) {
  v = String(v == null ? '' : v).slice(0, 5000);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
