import os, re, sys, json, html as H
src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
def rep(old, new, count=1):
    global h
    assert h.count(old) >= 1, ('missing', old[:90])
    if count: assert h.count(old) == count, ('count', h.count(old), old[:90])
    h = h.replace(old, new)
def insert_before(marker, new):
    global h
    assert h.count(marker) == 1, ('marker', h.count(marker), marker[:80])
    h = h.replace(marker, new + marker)
e = H.escape

# ---------- head ----------
rep('<script src="js/webfont.js" type="text/javascript"></script><script type="text/javascript">WebFont.load({  google: {    families: ["Italiana:300,400,500,600,700","Manrope:300,400,500,600,700"]  }});</script>', '')
rep('<link href="https://fonts.googleapis.com" rel="preconnect"/>', '')
rep('<link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous"/>', '') if '<link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous"/>' in h else rep('<link href="https://fonts.gstatic.com" rel="preconnect"/>', '')
rep('<html data-wf-domain', '<html lang="en-GB" data-wf-domain')
TITLE = 'Hospitality Marketing Agency London | Restaurants, Hotels & Bars | The Wonder Agency'
DESC = 'Digital marketing agency specialising in restaurants, hotels and bars. Content, social media, ads, SEO and AI search, websites and email: everything you need to get more bookings.'
URL = 'https://thewonderagency.co/'
h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % e(TITLE), h, count=1)
h, n = re.subn(r'<meta content="[^"]*" name="description"/>', '<meta content="%s" name="description"/>' % e(DESC), h, count=1); assert n == 1
h = re.sub(r'<meta content="Webflow" name="generator"/>', '', h)
FAQ = [
 ("What kind of businesses do you work with?", "Our specialism is hospitality and lifestyle: restaurants, hotels, bars, and food and drink brands, from Michelin-starred rooms to hotel groups and independents. It's where we have the deepest experience and the strongest results, so it's where we start. The same approach works for other consumer-facing brands, and we take that work on selectively."),
 ("What services do you offer?", "Content creation (photography, videography, reels, design), social media management, targeted advertising across Meta and Google, SEO and AI search visibility, influencer marketing, web design and build, and email marketing. Most clients take several together, because the channels work harder when they're aligned."),
 ("What is AI search visibility, or GEO?", "Generative Engine Optimisation is making your brand visible inside AI-generated answers: ChatGPT, Gemini, Perplexity, Google's AI overviews. When someone asks an assistant where to eat in your area, GEO decides whether you're in the answer. We measure it with our own tool, Wonder Score, then do the work that moves it."),
 ("How quickly will we see results?", "Most clients see measurable movement within three months. We've delivered a 58% year-on-year increase in food and beverage revenue and a 95% increase in set lunch bookings, both inside a three-month window. Compounding gains in search, brand and audience take longer and are worth more."),
 ("Do you work outside London?", "Yes. We work across the UK and internationally. Content production travels; strategy, social, paid and search are location-independent. Several of our clients are outside London entirely."),
 ("How do you report on performance?", "Monthly reporting on bookings, revenue, engagement, follower growth and advertising return: commercial outcomes rather than vanity metrics. We say plainly what worked, what didn't, and what we're changing next month."),
]
SVC_LINKS = [('Content creation', 'services/content-creation/'), ('Social media management', 'services/social-media-management/'), ('Paid advertising', 'services/paid-advertising/'),
             ('SEO and AI search', 'services/seo-ai-search/'), ('Influencer marketing', 'services/influencer-marketing/'), ('Website design', 'services/website-design/'), ('Email marketing', 'services/email-marketing/')]
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": ["ProfessionalService", "Organization"], "@id": URL + "#org", "name": "The Wonder Agency", "alternateName": "Wonder Agency", "legalName": "C Plus C Ltd",
   "url": URL, "logo": {"@type": "ImageObject", "url": URL + "images/x/icon-512.png", "width": 512, "height": 512}, "image": URL + "images/x/og.jpg",
   "description": DESC, "slogan": "Everything you need to be doing to get more bookings.", "email": "hello@thewonder.group", "telephone": "+447775022514",
   "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
   "areaServed": [{"@type": "City", "name": "London"}, {"@type": "Country", "name": "United Kingdom"}, "International"],
   "founder": [{"@type": "Person", "name": "Charles Morris", "jobTitle": "Founder"}, {"@type": "Person", "name": "Charlotte Giles", "jobTitle": "Co-founder"}],
   "parentOrganization": {"@type": "Organization", "name": "The Wonder Group", "url": "https://www.thewonder.group/"},
   "sameAs": ["https://www.instagram.com/the.wonder.list/"],
   "knowsAbout": ["Hospitality marketing", "Restaurant marketing", "Hotel marketing", "Bar and pub marketing", "Food and drink brand marketing", "Social media management", "Food photography and video",
                  "Meta advertising", "Google advertising", "Influencer marketing", "Restaurant SEO", "Local SEO", "AI search visibility", "Generative engine optimisation (GEO)", "Email marketing", "Website design"],
   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Hospitality marketing services", "itemListElement": [
       {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": URL + u, "serviceType": n, "audience": {"@type": "Audience", "audienceType": "Restaurants, hotels, bars and food and drink brands"}}} for n, u in SVC_LINKS]}},
  {"@type": "WebSite", "@id": URL + "#website", "url": URL, "name": "The Wonder Agency", "inLanguage": "en-GB", "publisher": {"@id": URL + "#org"}},
  {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": TITLE, "description": DESC, "isPartOf": {"@id": URL + "#website"}, "about": {"@id": URL + "#org"}, "inLanguage": "en-GB",
   "primaryImageOfPage": URL + "images/x/og.jpg"},
  {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
head_extra = ''.join([
 '<link rel="canonical" href="%s"/>' % URL,
 '<meta property="og:type" content="website"/><meta property="og:site_name" content="The Wonder Agency"/>',
 '<meta property="og:title" content="%s"/><meta property="og:description" content="%s"/>' % (e(TITLE), e(DESC)),
 '<meta property="og:url" content="%s"/><meta property="og:image" content="%simages/x/og.jpg"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>' % (URL, URL),
 '<meta name="twitter:card" content="summary_large_image"/><meta name="theme-color" content="#000000"/>',
 '<link rel="preload" href="fonts/italiana-400.woff2" as="font" type="font/woff2" crossorigin/>',
 '<link href="css/extend.css" rel="stylesheet" type="text/css"/>',
 '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False).replace('</', '<\\/'),
])
rep('<link href="css/site.css" rel="stylesheet" type="text/css"/>', '<link href="css/site.css" rel="stylesheet" type="text/css"/>' + head_extra)

# ---------- swap stock imagery for real hospitality imagery ----------
SWAP = {  # stock file fragment -> new image, alt
 '63512561ee86389a576073df_art-supplies-in-red-1-': ('connaught-bartender', 'Bartender throwing a cocktail at The Connaught Bar'),
 '63512561ee863843dd6073dd_colorful-gift-bag-1-': ('dessert-pour', 'Sauce being poured over a plated dessert'),
 '63512561ee8638d6166073da_10': ('reel-temper', 'Burger in front of flames at Temper'),
 '63512561ee8638cf0e6073dc_stefan-stefancik-pzA7QWNCIYg-unsplash': ('connaught-team', 'Bar team at work behind the bar'),
 '63512561ee8638bd786073db_27': ('lombard-dome', 'Domed dining room at 1 Lombard Street'),
 '63512561ee8638de3f6073de_colorful-candy-gumdrops-2-': ('reel-sushi', 'Chef brushing nigiri'),
 '63512561ee86382aa06073d9_pexels-anna-nekrashevich-8534253-1': ('connaught-room', 'Bar interior'),
 '63512561ee86388cc1607386_ae41d41e2fba4593d179c9c61bb259d9': ('connaught-pour', 'Bartender pouring a drink'),
 '63512561ee86385879607387_2a8f3c6fcddf2b749e9c65c2806c257e2': ('reel-steak', 'Sliced steak with sea salt'),
 '63512561ee86381ccf607388_Rectangle-5': ('connaught-shake', 'Bartender mixing a cocktail'),
 '63512561ee8638d157607389_M-06': ('dining-room', 'Dining room with chandeliers'),
 '63512561ee86389f7160738a_1': ('reel-burger', 'Pulled beef burger'),
 '63512561ee8638867760738c_CARD1': ('reel-caviar', 'Fish with caviar and sauce'),
 '63512561ee8638339060738b_card2': ('reel-flame', 'Burger patty flamed on the grill'),
 '63512561ee863878726073d1_cover2': ('reel-temper', 'Burger in front of flames at Temper'),
 '63512561ee86381f6c6073d0_cover-2-': ('reel-sushi', 'Chef brushing nigiri'),
 '63512561ee86384e9b6073ce_cover-3-': ('connaught-bartender', 'Bartender throwing a cocktail at The Connaught Bar'),
}
def swap_img(m):
    tag = m.group(0)
    for frag, (new, alt) in SWAP.items():
        if 'images/' + frag + '.' in tag:
            tag = re.sub(r' srcset="[^"]*"', '', tag); tag = re.sub(r' sizes="[^"]*"', '', tag)
            tag = re.sub(r' src="[^"]*"', ' src="images/x/%s.webp"' % new, tag)
            tag = re.sub(r' alt="[^"]*"', ' alt="%s"' % e(alt), tag)
            swap_img.n += 1
            return tag
    return tag
swap_img.n = 0
h = re.sub(r'<img\b[^>]*>', swap_img, h)
assert swap_img.n >= 24, swap_img.n

# ---------- hero: say what the agency is for ----------
rep('<h1 id="Top"', '<div class="x-hero-sub"><div class="x-label">Made to be booked out</div><p>Content, social, ads and search for hospitality brands that refuse to be scrolled past.</p><a href="#Contact" class="x-btn hover-cursor">Start a project <i>→</i></a></div><h1 id="Top"')

# ---------- sticky panel: real reels + positioning copy ----------
h, n = re.subn(r'<div data-poster-url="images/63512eef7e0d42c30732bcab_cars-poster-00001\.jpg".*?</noscript>',
  '<div class="background-video w-background-video w-background-video-atom"><video id="x-reel" autoplay muted playsinline poster="images/x/clip-w31.webp" src="videos/clips/w31-l.mp4" data-reels="videos/clips/w31-l.mp4,videos/clips/w12-l.mp4,videos/clips/w33-l.mp4,videos/clips/w08-l.mp4,videos/clips/w48-l.mp4,videos/clips/w21-l.mp4" data-object-fit="cover" aria-label="Client content: food and drink being prepared and served"></video>', h, count=1, flags=re.S); assert n == 1
h, n = re.subn(r'aria-controls="[^"]*-video"', 'aria-controls="x-reel"', h); assert n == 1
rep('>Creating lasting value</div>', '>Where we go deep</div>')
rep('We are an <strong>award winning full </strong>service marketing agency', 'Most agencies spread themselves thin. <strong>We went deep instead.</strong>')
h, n = re.subn(r'Specialising in content creation.*?sales and awareness\.', 'Restaurants, hotels and bars: the rooms we know best. That depth is why our clients grow.', h, count=1, flags=re.S); assert n == 1
rep('>Creative digital solutions<br/></div>', '>What we know</div>')
rep('We share a common passion for visual identities and digital technologies.', 'We know what fills a Tuesday, what makes people press save, and what turns a follower into a booking.')
h, n = re.subn(r'We create data driven solutions with imagination.*?by the right people\.', 'Born from The Wonder List and an audience of hundreds of thousands. And the principles travel further than the sector does.', h, count=1, flags=re.S); assert n == 1
h, n = re.subn(r'>SOCIAL.{0,40}?</div>', '>How we work</div>', h, count=1); assert n == 1
rep('We discover ideas, explore concepts and provide long lasting creative solutions.', 'One plan across content, social, ads and search.')
h, n = re.subn(r'As expert designers, photographers videographers.*?relevant and present\.\s*', 'Every channel works together and every campaign has a clear goal: more bookings, more revenue, more recognition.', h, count=1, flags=re.S); assert n == 1

# ---------- stats replace the old skills list ----------
i = h.index('<div class="w-layout-grid grid-2-columns gap-40">'); j = h.index('<div class="services-section"><div class="row display-flex-horizontal left second"><div class="point"></div>', i)
STATS = [('30', 'M+', 'Impressions per month'), ('4200', '+', 'Content pieces produced')]
stats = '<section class="x-numbers" aria-label="In numbers"><div class="x-label x-r">In numbers</div><div class="x-stats">' + ''.join('<div class="x-stat x-r" style="--x-d:%.2fs"><b data-count="%s" data-suffix="%s">%s%s</b><span>%s</span></div>' % (k*0.1, n_, s, format(int(n_), ','), s, l) for k, (n_, s, l) in enumerate(STATS)) + '</div></section>'
h = h[:i] + h[j:]
rep('<div class="services"><div class="services-section">', stats + '<div class="services"><div class="services-section">')

def heading(lines, sec_id=None):
    out = ''
    for k, (txt, indent) in enumerate(lines):
        cls = 'row display-flex-horizontal left' + (' second' if indent else '')
        out += '<div class="%s">%s<h2 class="heading-large secondary-font text-style-all-caps second x-r">%s</h2></div>' % (cls, '<div class="point"></div>' if k == 0 else '', txt)
    return '<div class="x-head">' + out + '</div>'

# ---------- services ----------
SVC = [
 ('Content creation', 'Photo / Video / Reels', 'Photos and videos of your venue, food and team, made for every channel.', 'We plan and run shoots in your venue, then produce everything that comes out of them. One shoot day feeds a month of social, your website, your ads and your email, so you are not paying for content twice.', ['Photography and video shoots on location', 'Reels and short-form edits', 'Menu, interior and team photography', 'Graphic design and creative direction']),
 ('Social media management', 'Strategy / Daily posting', 'We run your Instagram, TikTok and Facebook: posting, replies and monthly reports.', 'We take the accounts off your hands entirely. Strategy, calendar, daily posting, replying to every comment and DM, and a monthly report that tells you what actually moved.', ['Content calendars and daily scheduling', 'Community management, comments and DMs', 'Platform and algorithm optimisation', 'Monthly performance reporting']),
 ('Paid advertising', 'Meta / Google', 'Meta and Google ads that bring in bookings.', 'Paid campaigns judged on covers and revenue, not impressions. We build the creative, set the targeting, and cut what is not working fast.', ['Meta and Google campaign management', 'Audience targeting and retargeting', 'Paid creative production and testing', 'Tracking to the booking']),
 ('SEO and AI search', 'SEO / Wonder Score', 'Get found on Google, and recommended when people ask ChatGPT where to eat.', 'People increasingly ask ChatGPT and Gemini where to eat rather than searching. We do the traditional SEO work and the newer work that decides whether an AI assistant names you, tracked with our own tool, Wonder Score.', ['Technical SEO and site performance', 'Local SEO and Google Business Profile', 'Content and keyword strategy', 'AI search visibility (GEO) and Wonder Score tracking']),
 ('Influencer marketing', 'Creators / Visits / Reporting', 'The right local creators at your tables, briefed properly and measured on bookings.', 'A good creator visit is a recommendation from a friend, seen by thousands. We find creators whose audience matches your guests, brief them on what to show, handle the invitations and report on what they brought in.', ['Creator sourcing and vetting', 'Invitations, visits and briefing', 'Paid partnerships and usage rights', 'Reporting on reach and bookings']),
 ('Website design', 'Design / Build / Convert', 'Fast websites that turn visitors into bookings.', 'Most hospitality websites lose people between the menu and the booking button. We design and build fast, mobile-first sites around that single journey, then keep them updated so they do not go stale.', ['Custom design and build', 'Booking system integration', 'Speed and Core Web Vitals work', 'Ongoing updates and maintenance']),
 ('Email marketing', 'Campaigns / Automation', 'Newsletters and automated emails that bring guests back.', 'The cheapest way to fill a quiet week is to talk to people who have already been in. We build the list, segment it properly, and send campaigns and automated flows that bring them back.', ['Campaign design and copywriting', 'List growth and segmentation', 'Automated flows and sequences', 'Deliverability and reporting']),
]
CLIP = ['w68', 'w12', 'w58', 'w18', 'w83', 'w33', 'w48']
CLIP_ALT = ['Sushi being sliced', 'Dinner rush in a busy restaurant', 'Smash burger on the griddle', 'Japanese fine dining', 'A creator tasting dinner on camera', 'Japanese tasting menu', 'Tiramisu made at the table']
def vid(clip, size, alt, extra=''):
    return '<video muted loop playsinline preload="none" poster="images/x/clip-%s.webp" data-src="videos/clips/%s-%s.mp4" data-x-auto aria-label="%s"%s></video>' % (clip, clip, size, e(alt), extra)
rows = ''
for k, (name, tag, promise, body, inc) in enumerate(SVC):
    op = k == 0
    rows += ('<div class="x-acc-item x-r%s" data-peek="videos/clips/%s-s.mp4" data-peek-poster="images/x/clip-%s.webp"><button type="button" class="x-acc-btn hover-cursor" aria-expanded="%s" aria-controls="x-svc-%d"><span class="x-acc-num">0%d</span><span class="x-acc-name">%s</span><span class="x-acc-tag">%s</span><span class="x-acc-icon" aria-hidden="true"></span></button>'
             '<div class="x-acc-panel" id="x-svc-%d"><div class="x-acc-inner"><div class="x-svc"><div class="x-svc-media">%s</div><div><h4>%s</h4><p>%s</p></div><ul>%s</ul></div></div></div></div>') % (
        ' is-open' if op else '', CLIP[k], CLIP[k], 'true' if op else 'false', k, k+1, e(name), e(tag), k, vid(CLIP[k], 'm', CLIP_ALT[k]), e(promise), e(body), ''.join('<li>%s</li>' % e(x) for x in inc))
services = '<section id="WhatWeDo" class="x-section" aria-label="What we do">' + heading([('Six ways', True), ('we fill', False), ('the room', True)]) + '<div class="x-wrap"><div class="x-acc">' + rows + '</div></div></section>'
work_head = '<section class="x-section" aria-hidden="false">' + heading([('Who we', True), ('work with', False)]) + '</section>'
insert_before('<div id="Work" class="portfolio-section">', services + work_head)
rep('<div class="overflow-hidden display-flex bottom"><div data-w-id="', '<div class="overflow-hidden display-flex bottom" style="display:none"><div data-w-id="')

# ---------- results + wonder score (after the work section) ----------
results = ('<section id="Results" class="x-section x-section--tight" aria-label="The results">' + heading([('Results for', True), ('our clients', False)]) + '<div class="x-wrap">'
 '<article class="x-case x-r"><div class="x-case-stat">£3.2m<em>→</em>£4.6m</div><div class="x-case-body"><div><div class="x-label">Restaurant, three years</div><h3>Annual revenue, with Instagram from 3,000 to 20,000+ followers.</h3></div><p>Every channel aligned: weekly shoots, daily social, paid, email and SEO. Google rating 4.0 to 4.6.</p><div class="x-case-svc">Content · Social · Ads<br/>Web · Influencer</div></div></article>'
 '<article class="x-case x-case--right x-r"><div class="x-case-stat"><em style="padding-left:0">+</em>58%</div><div class="x-case-body"><div><div class="x-label">Hotel group, three months</div><h3>Year-on-year food and beverage revenue. Room bookings up 26%.</h3></div><p>A restaurant-first content strategy that made the hotel a destination for locals, not just guests.</p><div class="x-case-svc">Content · Social · Ads<br/>Web · Influencer</div></div></article>'
 '<div class="x-more"><div class="x-r"><b>+95%</b><h3>Michelin-starred restaurant</h3><p>Mid-week set lunch bookings within three months. We repositioned the lunch offer, ran a three-week paid push and rebuilt the booking journey.</p></div>'
 '<div class="x-r" style="--x-d:.12s"><b>+18%</b><h3>Three-restaurant group</h3><p>Q4 revenue year-on-year after a full digital overhaul: new sites, new photography and a new paid structure.</p></div></div>'
 '</div></section>')
ws = ('<section id="WonderScore" class="x-section" aria-label="Wonder Score"><div class="x-wrap"><div class="x-ws"><div class="x-r"><div class="x-label">Wonder Score</div><h2>The algorithm eats first.</h2>'
 '<p>People are asking ChatGPT, Gemini and Perplexity where to eat. Wonder Score, our own tool, measures whether the answer is you. Then we do the work that changes it.</p>'
 '<ul class="x-ws-plat"><li>ChatGPT</li><li>Gemini</li><li>Perplexity</li><li>Google AI</li></ul>'
 '<a href="https://wonderscore.ai" target="_blank" rel="noopener" class="x-btn hover-cursor">Get your score <i>→</i></a></div>'
 '<div class="x-chat" role="img" aria-label="Example: an AI assistant asked for the best restaurant for a special occasion in London recommends your restaurant first">'
 '<div class="x-chat-q">Best restaurant for a special occasion in London?</div>'
 '<div class="x-chat-a"><span class="x-chat-who">AI assistant</span>Three places stand out, and the first is <strong>your restaurant</strong>.</div>'
 '<div class="x-chat-score"><b>86</b><span>Wonder Score</span></div></div></div></div></section>')
faq = ('<section id="Questions" class="x-section" aria-label="Questions">' + heading([('Questions', True)]) + '<div class="x-wrap"><div class="x-acc x-acc--q">' +
 ''.join('<div class="x-acc-item x-r"><button type="button" class="x-acc-btn hover-cursor" aria-expanded="false" aria-controls="x-q-%d"><span class="x-acc-name">%s</span><span class="x-acc-icon" aria-hidden="true"></span></button><div class="x-acc-panel" id="x-q-%d"><div class="x-acc-inner"><p>%s</p></div></div></div>' % (k, e(q), k, e(a)) for k, (q, a) in enumerate(FAQ)) +
 '</div></div><div style="height:150px"></div></section>')
marker = '<div data-w-id="b562a5e1-4e8a-767a-a4be-3ed0560fe856"'
insert_before(marker, results + ws + '<div class="x-section" style="padding-top:120px"></div>')
insert_before('<div id="Contact"', faq)

# ---------- contact + footer ----------
rep('primary-font left">get in</h2>', 'primary-font left">Hungry</h2>')
rep('primary-font right">touch</h2>', 'primary-font right">yet?</h2>')
rep('<input class="form-label text-size-large form primary-font w-input" maxlength="256" name="name"', '<p class="x-form-intro">Tell us about your venue. We&#x27;ll tell you exactly what we&#x27;d do with it.</p><input class="form-label text-size-large form primary-font w-input" maxlength="256" name="name"')
h, n = re.subn(r'<div class="text text-size-small margin-top margin-small hide-tablet _2">© 2022\. All rights reserved</div>', '', h); assert n == 1
footer = ('<footer class="x-footer"><div class="x-footer-grid"><div><div class="x-footer-brand">The Wonder Agency</div><p>Hospitality marketing, done properly. Restaurants, hotels and bars, plus consumer brands who want the same standard. Content, social, ads and search that turn attention into bookings.</p></div>'
 '<div><h3>Services</h3><ul><li>Content Creation</li><li>Social Media</li><li>Targeted Ads</li><li>AI Search &amp; SEO</li><li>Web Design</li><li>Email Marketing</li></ul></div>'
 '<div><h3>Contact</h3><ul><li><a href="mailto:hello@thewonder.group">hello@thewonder.group</a></li><li><a href="tel:+447775022514">+44 777 502 2514</a></li><li><a href="https://www.instagram.com/the.wonder.list/" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://wonderscore.ai" target="_blank" rel="noopener">Wonder Score</a></li></ul></div></div>'
 '<div class="x-footer-base"><span>© 2026 The Wonder Agency</span><span>Made to be booked out</span></div></footer>')
insert_before('<div class="works-container">', '')
i = h.index('<div class="works-container">'); k = h.rfind('</div>', 0, i)  # closes .page-wrapper
h = h[:k] + footer + h[k:]

# ---------- nav + scripts ----------
rep('<a href="#Services" class="link-nav', '<a href="#WhatWeDo" class="link-nav')
rep('<span class="text-span">→ </span>Works</div>', '<span class="text-span">→ </span>Work</div>')
rep('<script src="js/contact-form.js" type="text/javascript"></script>', '<script src="js/contact-form.js" type="text/javascript"></script><script src="js/extend.js" type="text/javascript"></script>')
h = h.replace('<img src="images/635126a6ee8638db306082d0_The-Wonder-List-Logo.png" loading="lazy" alt=""', '<img src="images/635126a6ee8638db306082d0_The-Wonder-List-Logo.png" loading="lazy" alt="The Wonder Agency"')

# ================= phase 2 =================
def remove_el(start_marker):
    """remove the <div ...> element that begins at start_marker (balanced)"""
    global h
    assert h.count(start_marker) == 1, ('remove', h.count(start_marker), start_marker[:70])
    i = h.index(start_marker); depth = 0; pos = i
    for m in re.finditer(r'<(/?)div\b[^>]*>', h[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: pos = i + m.end(); break
    assert pos > i
    h = h[:i] + h[pos:]

# ---- hero: stack -> scatter -> name ----
hs = h.index('<div id="hero"'); he = h.index('<section id="About"')
hero = h[hs:he]
hero, n = re.subn(r'<img\b[^>]*class="hero-image position-absolute"[^>]*/>', '', hero); assert n == 7, n
CARDS = [  # kind, name, alt, tx(vw), ty(vh), r, stack r, depth, mobile (tx,ty) or None
 ('i', 'ph-47-t', 'Burger with a steak knife', -40, -27, -5, -8, .8, None),
 ('v', 'w19', 'Steak on an open-fire grill', -17, -35, 3, 5, -.6, (-32, -38)),
 ('v', 'w68', 'Tuna being sliced for sushi', 11, -33, -2, -3, 1.1, None),
 ('i', 'ph-02-t', 'Tomato and feta in hard sunlight', 37, -25, 5, 7, -.9, (32, -38)),
 ('v', 'w24', 'A cocktail being made at the bar', -44, 5, 4, -6, 1.3, (-35, -15)),
 ('v', 'w16', 'Dim sum being served', 43, 8, -4, 4, .7, (35, -15)),
 ('i', 'ph-01-t', 'Sea urchins on an ornate plate', -6, 36, -3, -2, -1.1, None),
 ('v', 'w73', 'Champagne on the dunes at sunset', 14, 34, 2, 6, .9, None),
 ('v', 'w58', 'Smash burger on the griddle', 30, 26, 6, 0, -.7, (0, -34)),
]
cards = ''
for i, (kind, name, alt, tx, ty, r, sr, d, mob) in enumerate(CARDS):
    st = '--i:%d;--tx:%dvw;--ty:%dvh;--r:%ddeg;--sr:%ddeg;--d:%s' % (i, tx, ty, r, sr, d)
    if mob: st += ';--mtx:%dvw;--mty:%dvh' % mob
    media = ('<video autoplay muted loop playsinline preload="auto" poster="images/x/clip-%s.webp" src="videos/clips/%s-s.mp4" aria-label="%s"></video>' % (name, name, e(alt))) if kind == 'v' else '<img src="images/x/%s.webp" alt="%s"/>' % (name, e(alt))
    cards += '<div class="x-card%s" style="%s">%s</div>' % ('' if mob else ' x-card--d', st, media)
hero = hero.replace('<div class="x-hero-sub">', '<div class="x-cards">' + cards + '</div><div class="x-dim"></div><div class="x-hero-sub">')
hero, n = re.subn(r'<h1 id="Top"[^>]*>.*?</h1>', '<h1 id="Top" class="heading-xlarge relative x-name" aria-label="The Wonder Agency"><span class="x-line" aria-hidden="true"><span>The Wonder</span></span><span class="x-line" aria-hidden="true"><span>Agency</span></span></h1>', hero, flags=re.S); assert n == 1
h = h[:hs] + hero + h[he:]

# ---- selected work: one client per slot, with their footage ----
WORK = [('Restaurants', 'w66', 'Oysters, uni and tuna', 'restaurants', 'From Michelin-starred dining rooms to neighbourhood favourites.', 'Marketing for restaurants'),
        ('Hotels', 'w74', 'Sunset by the sea at a coastal hotel', 'hotels', 'Rooms, restaurants, bars, events and weddings.', 'Marketing for hotels'),
        ('Bars', 'w20', 'Bartenders at work in a busy bar', 'bars-and-pubs', 'Cocktail bars, pubs and late-night venues.', 'Marketing for bars and pubs'),
        ('Brands', 'beeble', 'Spirits campaign', 'food-and-drink-brands', 'Food and drink brands, from launch to shelf.', 'Marketing for food and drink brands')]
ws = h.index('<div id="Work"'); we = h.index('navigation-2', ws)
work = h[ws:we]; it = iter(WORK)
def rename(m):
    if m.group(1).strip() == 'st': return m.group(0)
    return m.group(0).replace('>' + m.group(1) + '<', '>' + next(it)[0] + '<')
work, n = re.subn(r'class="heading-large text-style-all-caps primary-font">([^<]*)</div>', rename, work); assert n == 5, n
for k, (name, clip, alt, slug, line, more) in enumerate(WORK):
    work, n = re.subn(r'(<div id="0%d" data-w-id="[^"]*"[^>]*class="image-work) hover-cursor"><img[^>]*/>' % (k+1),
                      lambda m: m.group(1) + '">' + '<a class="x-work-link" href="who-we-work-with/%s/" aria-label="%s"><video %s class="image" muted loop playsinline preload="none" poster="images/x/clip-%s.webp" data-src="videos/clips/%s.mp4" data-x-auto aria-label="%s"></video></a>' % (slug, e(more), re.search(r'data-w-id="[^"]*"', m.group(0).split('<img', 1)[1]).group(0), clip, clip + ('-l' if os.path.exists(os.path.join(os.path.dirname(out), 'videos/clips/%s-l.mp4' % clip)) else '-m'), e(alt)),
                      work); assert n == 1, (k, n)
for name, clip, alt, slug, line, more in WORK:
    work, n = re.subn(r'(primary-font">%s</div></div>)' % name, lambda m: m.group(1) + '<div class="x-work-sub"><p>%s</p><a href="who-we-work-with/%s/" class="x-link">%s</a></div>' % (e(line), slug, e(more)), work, count=1); assert n == 1, name
h = h[:ws] + work + h[we:]

# ---- reel wall after the work section ----
WALL = [('w57', 'Soufflé and caramel', 'Soufflé and caramel'), ('w50', 'Ribs on the grill', 'Ribs'), ('w78', 'Focaccia', 'Focaccia'), ('w01', 'Spaghetti tossed in the pan', 'Spaghetti'),
        ('w42', 'Sunday roast', 'Sunday roast'), ('w60', 'Izakaya', 'Izakaya'), ('w55', 'Busy hands in the kitchen', 'In the kitchen'), ('w49', 'Fresh truffle', 'Fresh truffle'),
        ('w54', 'Steak, butter-basted', 'Steak'), ('w26', 'Guest chef evening', 'Events'), ('w25', 'Grill feast at a long table', 'Grill feast'), ('w62', 'French classics', 'French classics'),
        ('w61', 'Burgers and grill', 'Burgers'), ('w76', 'Rabbit and langoustine lasagne', 'Lasagne'), ('w34', 'Flambéed at the table', 'Flambé'), ('w04', 'Banana soufflé, caramel poured', 'Banana soufflé')]
wall = '<section class="x-wall" aria-label="Recent content"><div class="x-wall-sticky"><div class="x-wall-track">' + ''.join('<figure class="x-wall-card">%s%s</figure>' % (vid(c, 's', a), ('<figcaption>%s</figcaption>' % n) if n else '') for c, a, n in WALL) + '</div></div></section>'
# ---- our photography: a mosaic of stills from our shoots ----
SHOTS = [('35', 'Sharing feast', 1), ('21', 'Lamb cutlets', 0), ('04', 'Stuffed courgette flower', 0), ('36', 'Chefs making pasta', 0), ('44', 'Scallops and samphire', 1)]
tiles = ''.join('<a href="work/#library" class="x-shot%s x-r" style="--x-d:%.2fs"><img src="images/x/ph-%s%s.webp" alt="%s" loading="lazy" decoding="async"/><span>%s</span></a>' % (
    ' x-shot--wide' if wide else '', (k % 4) * 0.06, n, '' if wide else '-t', e(cap), e(cap)) for k, (n, cap, wide) in enumerate(SHOTS))
tiles += '<a href="work/#library" class="x-shot x-shot--more x-r"><b>128</b><span>films and photographs in the full library</span><em>See the library →</em></a>'
shots = ('<section class="x-section x-shots-sec" aria-label="Our photography">' + heading([('Our', True), ('photography', False)]) +
         '<div class="x-wrap"><p class="x-lede x-r">Every photo and film on this site is our own work, shot in our clients’ kitchens, dining rooms and bars.</p><div class="x-shots">' + tiles + '</div></div></section>')
insert_before('<section id="Results"', wall)  # (the photography mosaic was removed at C's request)

# ---- instagram band: moving video instead of stills ----
cs = h.index('<div data-w-id="b562a5e1-4e8a-767a-a4be-3ed0560fe856"'); ce = h.index('<section id="Questions"')
band = h[cs:ce]; clips = iter([('w35', 'Omakase'), ('w59', 'Steak and martinis'), ('w37', 'Plated dishes'), ('w09', 'Ravioli with brown butter and sage')])
def to_video(m):
    wid = re.search(r'data-w-id="[^"]*"', m.group(0)).group(0); c, a = next(clips)
    return '<video %s class="hero-image position-absolute" muted loop playsinline preload="none" poster="images/x/clip-%s.webp" data-src="videos/clips/%s-s.mp4" data-x-auto aria-label="%s"></video>' % (wid, c, c, e(a))
band, n = re.subn(r'<img\b[^>]*class="hero-image position-absolute"[^>]*/>', to_video, band); assert n == 4, n
h = h[:cs] + band + h[ce:]

# ---- "become one of the wonders": video instead of the still, with WONDERS in front ----
h, n = re.subn(r'<img\b[^>]*class="about-image _2"/>', '<video class="about-image _2" muted loop playsinline preload="none" poster="images/x/clip-w38.webp" data-src="videos/clips/w38-m.mp4" data-x-auto aria-label="Japanese grill, sushi and cocktails"></video>', h); assert n == 1, n

# ================= phase 3: a clear offer and calls to action =================
BTN = '<a href="#Contact" data-x-audit class="x-btn hover-cursor">%s <i>→</i></a>'
# hero copy + buttons
rep('<div class="x-label">Made to be booked out</div><p>Content, social, ads and search for hospitality brands that refuse to be scrolled past.</p><a href="#Contact" class="x-btn hover-cursor">Start a project <i>→</i></a>',
    '<div class="x-label"><span class="x-hide-m">Hospitality marketing · </span>Made to be booked out</div><p>We fill restaurants, hotels and bars. Content, social, ads and search, run as one plan.</p><div class="x-hero-btns">' + BTN % 'Get a free audit' + '<a href="#Results" class="x-link hover-cursor">See the results</a></div>')
# the big statement now says what the agency does
h, n = re.subn(r'(<h2 data-w-id="[^"]*"[^>]*class="heading-large secondary-font text-style-all-caps second">)we work(</h2>)', r'\1we turn\2', h); assert n == 1
h, n = re.subn(r'(class="heading-large secondary-font text-style-all-caps second">)to give ?(</h2>)', r'\1attention\2', h); assert n == 1
h, n = re.subn(r'(class="heading-large secondary-font text-style-all-caps second">)customers ?(</h2>)', r'\1into\2', h); assert n == 1
for old, new in (('>dynamic</h2>', '>covers</h2>'), ('>unique</h2>', '>regulars</h2>'), ('>compelling</h2>', '>revenue</h2>'), ('<span>Wonderful</span>', '<span>bookings</span>')):
    rep(old, new)
h, n = re.subn(r'(class="heading-large secondary-font text-style-all-caps second">)experiences(</h2>)', r'\1for hospitality\2', h); assert n == 1
# call to action after the services
insert_before('<section class="x-section" aria-hidden="false">', '')
h = h.replace('</div></div></section><section class="x-section" aria-hidden="false">', '</div><div class="x-cta x-r"><p>Not sure which of the seven you need? The free audit tells you.</p>' + BTN % 'Get a free audit' + '</div></div></section><section class="x-section">', 1)
assert 'Not sure which of the seven' in h
# the audit offer + how it works, after the results
AUDIT = [('Social and content', 'What you post, how it looks, and whether anyone acts on it.'), ('Paid ads', 'Where the budget goes and what it brings back in bookings.'),
         ('Search and AI search', 'How you show up on Google, and whether AI assistants name you.'), ('Website and booking', 'How many people you lose between the menu and the booking button.')]
STEPS = [('We audit', 'You tell us about your venue. We review your marketing and send back what we found. Free, with no obligation.'),
         ('We plan', 'One plan across the channels you need, with a clear goal: more bookings, more revenue, more recognition.'),
         ('We run it', 'Shoots, posting, ads and search, handled. A monthly report says plainly what worked, what didn&#x27;t and what changes next.')]
audit = ('<section id="Audit" class="x-section" aria-label="The free audit">' + heading([('The free', True), ('audit', False)]) + '<div class="x-wrap"><div class="x-audit">'
 '<div class="x-r"><h3>See what we&#x27;d fix first.</h3><p>Send us your venue and we&#x27;ll review your marketing from the outside, the way a guest sees it. You get a plain account of what&#x27;s working, what isn&#x27;t, and what we&#x27;d do first. No charge and no obligation.</p>' + BTN % 'Get your free audit' + '</div>'
 '<ol class="x-audit-list">' + ''.join('<li class="x-r" style="--x-d:%.2fs"><span>0%d</span><div><b>%s</b><em>%s</em></div></li>' % (k*0.08, k+1, t, d) for k, (t, d) in enumerate(AUDIT)) + '</ol></div>'
 '<div class="x-steps">' + ''.join('<div class="x-step x-r" style="--x-d:%.2fs"><span>Step %d</span><h3>%s</h3><p>%s</p></div>' % (k*0.1, k+1, t, d) for k, (t, d) in enumerate(STEPS)) + '</div>'
 '</div></section>')
insert_before('<section id="WonderScore"', audit)
# the form becomes an audit request
rep('<p class="x-form-intro">Tell us about your venue. We&#x27;ll tell you exactly what we&#x27;d do with it.</p>', '<p class="x-form-intro">Tell us about your venue and we&#x27;ll send back a free audit of your marketing: what&#x27;s working, what isn&#x27;t, and what we&#x27;d do first.</p>')
h, n = re.subn(r'(<input class="form-label text-size-large form primary-font w-input" maxlength="256" name="email"[^>]*/>)', r'\1<input class="form-label text-size-large form primary-font w-input" maxlength="256" name="venue" placeholder="Your venue" type="text" id="venue" required=""/><input class="form-label text-size-large form primary-font w-input" maxlength="256" name="link" placeholder="Website or Instagram" type="text" id="link"/>', h); assert n == 1
rep('<textarea placeholder="Your message"', '<textarea placeholder="Anything we should know? (optional)"')
rep('<div>Thank you! Your submission has been received!</div>', '<div>Thank you. Your audit request is in and we&#x27;ll be in touch.</div>')
rep('<div>Oops! Something went wrong while submitting the form.</div>', '<div>Sorry, something went wrong. Please email <a href="mailto:hello@thewonder.group" style="color:inherit;text-decoration:underline">hello@thewonder.group</a> instead.</div>')
# always-there button


# ---- hover preview element ----
rep('<script src="js/jquery-3.5.1.min.dc5e7f18c8.js"', '<div class="x-peek" aria-hidden="true"><video muted loop playsinline></video></div><script src="js/jquery-3.5.1.min.dc5e7f18c8.js"')


# ================= phase 4: the combined version =================
# ---- visible nav bar ----
NAV_LINKS = [('#WhatWeDo', 'Services'), ('#Work', 'Work'), ('#Results', 'Results'), ('#Audit', 'How it works'), ('#WonderScore', 'Wonder Score'), ('#News', 'News')]
NAV = ('<header class="x-nav" id="x-nav"><a href="#top" class="x-nav-brand hover-cursor">The Wonder Agency</a>'
       '<nav class="x-nav-links" aria-label="Main">' + ''.join('<a href="%s" class="hover-cursor">%s</a>' % (u, t) for u, t in NAV_LINKS if t != 'Work') + '</nav>'
       '<div class="x-nav-right"><a href="#Contact" data-x-audit class="x-nav-cta hover-cursor">Free audit <i>→</i></a>'
       '<button type="button" class="x-nav-burger" aria-label="Open menu" aria-expanded="false" aria-controls="x-menu"><span></span><span></span></button></div></header>'
       '<div class="x-menu" id="x-menu" aria-hidden="true"><nav aria-label="Menu">' + ''.join('<a href="%s" style="--i:%d">%s</a>' % (u, k, t) for k, (u, t) in enumerate(NAV_LINKS + [('#Questions', 'Questions')])) + '</nav>'
       '<a href="#Contact" data-x-audit class="x-nav-cta x-menu-cta">Get a free audit <i>→</i></a><p class="x-menu-contact"><a href="mailto:hello@thewonder.group">hello@thewonder.group</a><a href="tel:+447775022514">+44 777 502 2514</a></p></div>'
       '<div class="x-grain" aria-hidden="true"></div>')
insert_before('<div data-animation="default" class="navbar w-nav"', NAV)

# ---- logo marquee straight after the hero; drop the old grid + its heading ----
gs = h.index('<div class="w-layout-grid grid-3">'); ge = h.index('</div>', h.rfind('<img', gs, h.index('<div id="Work"'))) + 6
logos = re.findall(r'<img src="(images/[^"]+)"[^>]*class="clients-image-three"', h[gs:ge]); assert len(logos) >= 20, len(logos)
DROP = ('686d31194225aeb22860ac5d_6', 'logo-the-barley-mow')  # Victor Garvey at The Midland Grand, The Barley Mow
old = [l for l in logos if not any(d in l for d in DROP)]; assert len(old) == len(logos) - 2, len(old)
NEW = ['zahter', 'beeble', 'hutong', 'aqua-shard', 'harrys', 'dim-sum-library', 'visit-england', 'aqua-kyoto', 'wild-group', 'azzurra', 'shiro', 'aqua-nueva', 'script', 'temper-tantrums']
new = ['images/x/logos/%s.webp' % n for n in NEW]; logos = []
for k in range(max(len(old), len(new) * 2)):
    if k < len(old): logos.append(old[k])
    if k % 2 == 0 and k // 2 < len(new): logos.append(new[k // 2])
row = lambda ls: ''.join('<span class="x-logo"><img src="%s" alt="" decoding="async"/></span>' % src for src in ls)
ra, rb = row(logos[0::2]), row(logos[1::2])
marquee = ('<section class="x-logos-wrap" aria-label="Selected clients"><div class="x-logos-head x-r"><div class="x-label">Selected clients</div>'
           '<p>Restaurants, hotels, bars and food and drink brands, from London to Paris.</p><a href="work/" class="x-link">See our work</a></div>'
           '<div class="x-logos"><div class="x-logos-track">' + ra + ra + '</div><div class="x-logos-track x-logos-track--rev">' + rb + rb + '</div></div></section>')
insert_before('<div class="about-section-second">', marquee)
remove_el('<div class="w-layout-grid grid-3">')
m = re.search(r'<div class="services"><div class="services-section">', h); assert m
remove_el('<div class="services">')

# ---- services: pinned chapters with video ----
SVC_VID = [('w28', 'Salmon aburi'), ('w52', 'Brunch'), ('w46', 'Burgers and steak'), ('w15', 'On the grill'), ('w83', 'Creator visit, first bite'),
           ('w64', 'Fine dining plates'), ('w23', 'Christmas lunch')]
idx = ''.join('<li><button type="button" class="hover-cursor" data-i="%d"><i>0%d</i>%s</button></li>' % (k, k+1, e(n)) for k, (n, *_r) in enumerate(SVC))
chs = ''.join(('<article class="x-sv-ch%s" data-i="%d"><span class="x-sv-n">0%d / %s</span><h3>%s</h3><p class="x-sv-promise">%s</p><p class="x-sv-body">%s</p>'
               '<ul class="x-sv-inc">%s</ul></article>') % (' is-on' if k == 0 else '', k, k+1, e(tag), e(name), e(promise), e(body), ''.join('<li>%s</li>' % e(x) for x in inc))
              for k, (name, tag, promise, body, inc) in enumerate(SVC))
meds = ''.join('<figure class="x-sv-med%s"><video muted loop playsinline preload="none" poster="images/x/clip-%s.webp" data-src="videos/clips/%s-m.mp4" aria-label="%s"></video><figcaption>%s</figcaption></figure>' % (' is-on' if k == 0 else '', v, v, e(c), e(c)) for k, (v, c) in enumerate(SVC_VID))
sv = ('<section id="WhatWeDo" class="x-section" aria-label="What we do">' + heading([('The seven things', True), ('that fill', False), ('your tables', True)]) + '<div class="x-wrap"><p class="x-lede x-r">These are the seven things that decide whether people find you, choose you and book. Get them right and the bookings follow. Take one, or let us run them all.</p></div></section>'
      '<section class="x-sv" aria-label="Services in detail"><div class="x-sv-pin"><div class="x-sv-grid">'
      '<div class="x-sv-index"><ol>' + idx + '</ol><div class="x-sv-rail"><i></i></div></div>'
      '<div class="x-sv-stage">' + chs + '</div>'
      '<div class="x-sv-media">' + meds + '<span class="x-sv-count">01 / 07</span></div>'
      '</div></div></section>'
      '<section class="x-section x-section--tight"><div class="x-wrap"><div class="x-cta x-r" style="margin-top:0"><p>Not sure which of the seven you need? The free audit tells you.</p>' + BTN % 'Get a free audit' + '</div></div></section>')
ss = h.index('<section id="WhatWeDo"'); se = h.index('<section class="x-section">', ss)
h = h[:ss] + sv + h[se:]

# ---- results: full-screen video case studies ----
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cases as _cases
_BG = {'revenue': ('v', 'fish-b'), 'hotel': ('v', 'grill-c'), 'overhaul': ('i', 'case-overhaul-bg'), 'michelin': ('i', 'case-michelin'), 'brunch': ('i', 'case-brunch'), 'longboard': ('v', 'lb-film'), 'square': ('d', 'x-cases-books')}
def _bg(k, c):
    kind, src = _BG[c['key']]; on = ' class="is-on"' if k == 0 else ''
    if kind == 'd': return '<div class="%s%s" aria-hidden="true"><span>Savoury</span><span>Sweet</span><span>Collector’s edition</span></div>' % (src, ' is-on' if k == 0 else '')
    if kind == 'v': return '<video%s muted loop playsinline preload="none" poster="images/x/clip-%s.webp" data-src="videos/clips/%s-m.mp4" aria-hidden="true"></video>' % (on, src, src)
    return '<img%s src="images/x/cases/%s.webp" alt="" loading="lazy" decoding="async"/>' % (on, src)
CASES = _cases.CASES
cases = ('<div class="x-cases" style="--n:%d"><div class="x-cases-stick"><div class="x-cases-bg">' % len(CASES) +
         ''.join(_bg(k, c) for k, c in enumerate(CASES)) +
         '</div>' + ''.join('<article class="x-case2%s"><div class="x-label">%s</div><div class="x-case2-stat">%s</div><h3>%s</h3><p>%s</p><a href="work/%s/" class="x-link">Read the case study</a></article>' % (
             ' is-on' if k == 0 else '', e(c['label']), e(c['stat']).replace('→', '<em>→</em>').replace('+', '<em>+</em>', 1), e(c['line']), e(c['overview']), c['slug']) for k, c in enumerate(CASES)) +
         '<div class="x-cases-dots">' + ''.join('<span class="%s">0%d</span>' % ('is-on' if k == 0 else '', k+1) for k in range(len(CASES))) + '</div></div></div>')
rs = h.index('<section id="Results"'); r1 = h.index('<article class="x-case x-r">', rs); r2 = h.index('<div class="x-more">', rs)
h = h[:r1] + '</div>' + cases + '<div class="x-wrap" style="margin-top:4rem">' + h[r2:]


# ---- the old 2022 case study pop-ups are no longer used ----
remove_el('<div class="works-container">')

# ---- latest news / articles ----
POSTS = [('AI search', 'Why AI search will change how restaurants get discovered', 'Customers are increasingly asking AI where to eat. Here is how to make sure your restaurant is part of the answer.', 'clip-fish-c'),
         ('Social', 'The five Instagram mistakes holding restaurants back', 'We look at a lot of hospitality accounts. These are the patterns we see most often, and how to fix them.', 'clip-azzurra-weekend'),
         ('Case study', 'How a restaurant-first strategy grew a hotel group’s F&amp;B revenue by 58%', 'The thinking behind a 58% rise in food and beverage revenue in three months, and what it did for room bookings.', 'connaught-team')]
news = ('<section id="News" class="x-section" aria-label="News and articles">' + heading([('Latest', True), ('thinking', False)]) + '<div class="x-wrap"><div class="x-news">' +
        ''.join('<article class="x-post x-r" style="--x-d:%.2fs"><div class="x-post-img"><img src="images/x/%s.webp" alt="" loading="lazy"/></div><div class="x-label">%s</div><h3>%s</h3><p>%s</p><span class="x-post-soon">Article coming soon</span></article>' % (k*0.1, img, tag, title, ex) for k, (tag, title, ex, img) in enumerate(POSTS)) +
        '</div></div></section>')
qs = h.index('<section id="Questions"'); qe = h.index('<div id="Contact"')
h = h[:qe] + news + h[qe:]

# ---- scripts ----
rep('<script src="js/extend.js" type="text/javascript"></script>', '<script src="js/extend.js" type="text/javascript"></script><script src="js/lenis.min.js" type="text/javascript"></script><script src="js/extend3.js" type="text/javascript"></script>')


# ================= phase 5: plain wording =================
rep('<div class="x-label"><span class="x-hide-m">Hospitality marketing · </span>Made to be booked out</div><p>We fill restaurants, hotels and bars. Content, social, ads and search, run as one plan.</p>',
    '<div class="x-label">Marketing agency for restaurants, hotels and bars</div><p>Everything you need to be doing to get more bookings: content, social media, ads, search, websites and email. All done for you, by one team.</p>')
rep('>Where we go deep</div>', '>Our specialism</div>')
rep('Most agencies spread themselves thin. <strong>We went deep instead.</strong>', 'A digital agency that <strong>specialises in hospitality.</strong>')
rep('Restaurants, hotels and bars: the rooms we know best. That depth is why our clients grow.', 'Restaurants, hotels, bars and food and drink brands are what we know best. Michelin-starred restaurants, hotel groups and independents trust us to run their marketing, with one team covering content, social, ads, search, websites and email.')
rep('We know what fills a Tuesday, what makes people press save, and what turns a follower into a booking.', 'We know what makes people book.')
rep('Born from The Wonder List and an audience of hundreds of thousands. And the principles travel further than the sector does.', 'Why someone picks one restaurant over another, books a hotel for the weekend, or comes back for a second visit. Everything we make is built around that.')
rep('One plan across content, social, ads and search.', 'Measured in bookings and revenue.')
rep('Every channel works together and every campaign has a clear goal: more bookings, more revenue, more recognition.', 'Not likes. Every month you get a plain report: what worked, what didn&#x27;t, and what we&#x27;re changing next.')
rep('<h2>The algorithm eats first.</h2>', '<h2>Are you recommended by AI?</h2>')
rep('<p>People are asking ChatGPT, Gemini and Perplexity where to eat. Wonder Score, our own tool, measures whether the answer is you. Then we do the work that changes it.</p>',
    '<p>More and more people ask ChatGPT, Gemini and Perplexity where to eat, drink and stay, and AI recommends just a handful of names. Wonder Score, our own tool, analyses your website and your competitors, shows where you stand, and tells you what to change to get recommended more. Then we can do the work for you.</p>')
rep('class="x-btn hover-cursor">Get your score <i>→</i></a>', 'class="x-btn hover-cursor">Check your Wonder Score <i>→</i></a>')
rep('primary-font left">Hungry</h2>', 'primary-font left">Your free</h2>')
rep('primary-font right">yet?</h2>', 'primary-font right">audit</h2>')
rep('<p>Hospitality marketing, done properly. Restaurants, hotels and bars, plus consumer brands who want the same standard. Content, social, ads and search that turn attention into bookings.</p>',
    '<p>The Wonder Agency is a London digital marketing agency specialising in restaurants, hotels and bars, working across the UK and internationally. Content, social media, ads, search, websites and email: everything you need to get more bookings.</p>')


# ================= phase 6: link the homepage to the new pages =================
SLUGS = [('Content creation','content-creation'),('Social media management','social-media-management'),('Paid advertising','paid-advertising'),('SEO and AI search','seo-ai-search'),('Influencer marketing','influencer-marketing'),('Website design','website-design'),('Email marketing','email-marketing')]
for name, slug in SLUGS:
    old = '<h3>%s</h3>' % e(name)
    i = h.index('<article class="x-sv-ch'); assert h.count(old) >= 1, name
    j = h.index(old, i); k = h.index('</article>', j)
    h = h[:k] + '<a class="x-link x-sv-more" href="services/%s/">More about %s</a>' % (slug, e(name.lower())) + h[k:]
rep('<a href="#Audit" class="hover-cursor">How it works</a>', '<a href="about/" class="hover-cursor">About</a>')
rep('<a href="#Questions" style="--i:6">Questions</a></nav>', '<a href="#Questions" style="--i:6">Questions</a><a href="services/" style="--i:7">All services</a><a href="about/" style="--i:8">About</a></nav>')
old_ul = '<ul><li>Content Creation</li><li>Social Media</li><li>Targeted Ads</li><li>AI Search &amp; SEO</li><li>Web Design</li><li>Email Marketing</li></ul>'
rep(old_ul, '<ul>' + ''.join('<li><a href="services/%s/">%s</a></li>' % (slug, e(name)) for name, slug in SLUGS) + '</ul>')
rep('<li><a href="https://wonderscore.ai" target="_blank" rel="noopener">Wonder Score</a></li></ul>', '<li><a href="https://wonderscore.ai" target="_blank" rel="noopener">Wonder Score</a></li><li><a href="about/">About</a></li></ul>')

# audit buttons go to the free audit page rather than the form at the bottom
h = h.replace('href="#Contact" data-x-audit', 'href="free-audit/"')
open(out, 'w', encoding='utf-8').write(h)
print('ok', len(h))
