# Search-listing titles and descriptions, kept within what Google shows (~60 and ~155 characters).
# Rewrites <title>, meta description and the og:/twitter: copies on every indexable page. Runs before seo.py so the sitemap/llms.txt pick them up.
import os, re, sys, html

R = sys.argv[1]
A = ' | The Wonder Agency'

T = {
    '': ('Hospitality Marketing Agency, London',
         'London marketing agency for restaurants, hotels and bars: content, social media, ads, SEO and AI search, websites and email. Built to get more bookings.'),
    'about/': ('About Us | Hospitality Marketing, London',
         'London-based digital marketing agency specialising in restaurants, hotels and bars, working across the UK and abroad. Who we are and how we work.'),
    'agency-vs-in-house/': ('Marketing Agency vs In-House Marketer',
         'Should a restaurant, hotel or bar hire an in-house marketer or an agency? A fair comparison of skills, content, cover, tools and cost, and when to do both.'),
    'contact/': ('Contact Us | Work With The Wonder Agency',
         'Get in touch with The Wonder Agency, a London hospitality marketing agency. Email hello@thewonder.group, call +44 777 502 2514 or send us a message.'),
    'free-audit/': ('Free Hospitality Marketing Audit',
         'A free marketing audit for your restaurant, hotel or bar: social media, ads, Google, AI search and website. What’s working, what isn’t, what we’d fix first.'),
    'insights/': ('Insights | Hospitality Marketing Guides',
         'Articles and guides on restaurant, hotel and bar marketing: social media, ads, SEO, AI search and more, from The Wonder Agency.'),
    'insights/ai-search-for-restaurants/': ('How AI Search Changes Restaurant Discovery',
         'More diners ask ChatGPT, Gemini and Perplexity where to eat. How AI assistants choose which restaurants to recommend, and how to be one of them.'),
    'insights/hotel-food-and-beverage-revenue/': ('How We Grew Hotel F&B Revenue by 58%',
         'How a restaurant-first strategy grew a hotel’s food and beverage revenue by 58% in three months, with room bookings up 26%, by marketing to locals first.'),
    'insights/instagram-mistakes-restaurants/': ('Five Instagram Mistakes Restaurants Make',
         'The five Instagram mistakes we see most often on restaurant accounts, from posting without a plan to ignoring messages, and how to fix each one.'),
    'london/': ('London Restaurant, Hotel & Bar Marketing',
         'Hospitality marketing in London: content, social media, ads, SEO and AI search, websites and email for restaurants, hotels and bars. Also UK-wide and abroad.'),
    'pricing/': ('Hospitality Marketing Agency Pricing',
         'How much does a hospitality marketing agency cost? What affects the price of social, content, ads, SEO, websites and email, and what to ask any agency.'),
    'privacy/': ('Privacy Policy',
         'How The Wonder Agency collects, uses and protects the information you give us when you ask for a free audit or get in touch.'),
    'services/': ('Hospitality Marketing Services',
         'Content, social media, ads, SEO and AI search, websites and email for restaurants, hotels and bars. Everything you need to get more bookings, from one team.'),
    'services/content-creation/': ('Content Creation for Restaurants & Hotels',
         'Photography and video for restaurants, hotels and bars: food, drinks, interiors, team and reels, planned around what you need to sell, made for every channel.'),
    'services/content-creation/restaurants/': ('Restaurant Photography & Video, London',
         'Restaurant photography and video: dish, drink, interior and team shoots and reels, shot around service and made for Instagram, TikTok, Google and your website.'),
    'services/email-marketing/': ('Email Marketing for Restaurants & Hotels',
         'Newsletters and automated emails for restaurants, hotels and bars that bring guests back: list growth, segmentation, campaigns and automated flows.'),
    'services/email-marketing/hotels/': ('Email Marketing for Hotels',
         'Email marketing for hotels: pre-arrival and post-stay emails, seasonal breaks, dining and events campaigns, sent to the right guests to grow direct bookings.'),
    'services/influencer-marketing/': ('Influencer Marketing for Hospitality',
         'Influencer marketing for restaurants, hotels and bars: the right local creators, briefed properly, with clear disclosure and reporting on reach and bookings.'),
    'services/paid-advertising/': ('Meta & Google Ads for Restaurants & Hotels',
         'Meta and Google ads for restaurants, hotels and bars, judged on bookings and revenue rather than clicks, with full conversion tracking.'),
    'services/paid-advertising/restaurants/': ('Meta & Google Ads for Restaurants',
         'Instagram, Facebook and Google campaigns for restaurants that fill set lunches, quiet nights and private dining, tracked all the way to the booking.'),
    'services/seo-ai-search/': ('SEO & AI Search for Restaurants & Hotels',
         'Get found on Google Maps and recommended by ChatGPT, Gemini and Perplexity. SEO and AI search for restaurants, hotels and bars, tracked with Wonder Score.'),
    'services/seo-ai-search/restaurants/': ('Restaurant SEO & AI Search',
         'Restaurant SEO: rank in Google and Google Maps for the searches diners make, and get recommended by ChatGPT, Gemini and Perplexity. Tracked with Wonder Score.'),
    'services/social-media-management/': ('Social Media Management for Hospitality',
         'We run Instagram, TikTok and Facebook for restaurants, hotels and bars: strategy, daily posting, comments and messages, and monthly reporting tied to bookings.'),
    'services/social-media-management/hotels/': ('Social Media Management for Hotels',
         'Social media management for hotels: Instagram, TikTok and Facebook that sell the whole hotel, from rooms to the restaurant, bar, events and weddings.'),
    'services/social-media-management/restaurants/': ('Social Media Management for Restaurants',
         'Instagram, TikTok and Facebook for restaurants, run daily: reels that make people hungry, every message answered and reporting tied to covers.'),
    'services/website-design/': ('Website Design for Restaurants & Hotels',
         'Fast, mobile-first websites for restaurants, hotels and bars, built around bookings: menus that work on a phone, booking integration and SEO foundations.'),
    'services/website-design/restaurants/': ('Restaurant Website Design',
         'Restaurant website design: fast, mobile-first sites with menus as readable pages, your booking system built in, and the details search engines and AI need.'),
    'who-we-work-with/': ('Who We Work With | Hospitality Marketing',
         'We specialise in hospitality: restaurants, hotels, bars and pubs, restaurant groups and food and drink brands, in London, across the UK and internationally.'),
    'who-we-work-with/bars-and-pubs/': ('Bar & Pub Marketing Agency',
         'Marketing for bars and pubs: content, social media, events promotion, ads, SEO and AI search, websites and email that fill the room on the nights that matter.'),
    'who-we-work-with/food-and-drink-brands/': ('Marketing for Food & Drink Brands',
         'Marketing for food and drink brands: content, social media, ads, search, websites and email for launches, direct sales and stockists.'),
    'who-we-work-with/hotels/': ('Hotel Marketing Agency, London',
         'Marketing for hotels: more direct bookings, a restaurant and bar that locals choose, and full events and wedding calendars. Content, social, ads, SEO and more.'),
    'who-we-work-with/hotels/food-and-beverage/': ('Hotel Restaurant & Bar Marketing',
         'Hotel food and beverage marketing: turn the hotel restaurant and bar into somewhere locals choose. The approach behind a 58% rise in F&B revenue.'),
    'who-we-work-with/restaurant-groups/': ('Marketing for Restaurant Groups',
         'Marketing for restaurant groups and multi-site operators: every brand and venue with its own voice, run from one plan with group-level reporting.'),
    'who-we-work-with/restaurants/': ('Restaurant Marketing Agency, London',
         'Marketing for restaurants: content, social media, Meta and Google ads, SEO and AI search, websites and email, all aimed at filling tables.'),
    'wonder-score/': ('Wonder Score | Does AI Recommend You?',
         'Wonder Score checks whether ChatGPT, Gemini and Perplexity recommend your venue, analyses your website and competitors, and shows what to change.'),
    'work/': ('Our Work | Case Studies & Showcase',
         'Photography, video and websites for restaurants, hotels and bars, plus seven case studies: £3.2m to £4.6m revenue, +58% hotel F&B, +95% set lunch bookings.'),
    'work/hotel-boost/': ('Hotel F&B Revenue Up 58% | Case Study',
         'Hotel, three months. Food and beverage revenue up 58% year on year, with room bookings up 26%, by marketing the restaurants to locals first.'),
    'work/longboard-coffee-auction/': ('Longboard Coffee Auction | Case Study',
         'A first-ever coffee auction. We rebuilt Longboard’s website, shot the content, marketed the auction and designed the lot artwork. Record average lot price.'),
    'work/michelin-star-set-menu/': ('Set Lunch Bookings Up 95% | Case Study',
         'Michelin-starred restaurant, three months. Set lunch bookings up 95% after reshaping the set menu with the chef and running a full campaign.'),
    'work/restaurant-group-marketing-overhaul/': ('Group Revenue Up 18% | Case Study',
         'Three-restaurant group, Q4. An 18% year-on-year increase in revenue after a full marketing overhaul across content, social, ads and email.'),
    'work/restaurant-revenue-growth/': ('Revenue From £3.2m to £4.6m | Case Study',
         'Restaurant, three years. Annual revenue from £3.2m to £4.6m, Instagram from 3,000 to 20,000+ followers and Google rating from 4.0 to 4.6.'),
    'work/saturday-brunch-launch/': ('New Brunch, 250 Covers a Week | Case Study',
         'Historic City venue, six weeks. A new Saturday brunch now does 220 to 250 covers every week, from no weekend trade at all.'),
    'work/the-square-cookbooks/': ('The Square Cookbooks: Sold Out in 48 Hours',
         'Cookbook relaunch, October 2025. We built the website and launch campaign for Phil Howard’s The Square cookbooks; the limited run sold out within 48 hours.'),
}

def put(t, title, desc):
    et, ed = html.escape(title, quote=False), html.escape(desc)
    t = re.sub(r'<title>.*?</title>', '<title>%s</title>' % et, t, count=1, flags=re.S)
    t = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="%s"' % ed, t)
    t = re.sub(r'<meta content="[^"]*" name="description"', '<meta content="%s" name="description"' % ed, t)
    for p in ('og:title', 'twitter:title'):
        t = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % p, r'\g<1>%s"' % et, t)
    for p in ('og:description', 'twitter:description'):
        t = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % p, r'\g<1>%s"' % ed, t)
    return t

n = 0; long_ = []
for d, _, fs in os.walk(R):
    if 'index.html' not in fs: continue
    rel = os.path.relpath(d, R).replace(os.sep, '/'); rel = '' if rel == '.' else rel + '/'
    if rel not in T: continue
    f = os.path.join(d, 'index.html'); t = open(f, encoding='utf-8').read()
    title, desc = T[rel]; full = title + A
    if len(full) > 62: long_.append((len(full), full))
    if len(desc) > 160: long_.append((len(desc), desc))
    open(f, 'w', encoding='utf-8').write(put(t, full, desc)); n += 1
missing = [p for p in T if not os.path.exists(os.path.join(R, p, 'index.html'))]
print('titles: %d pages rewritten' % n, ('MISSING ' + str(missing)) if missing else '', ('LONG ' + str(long_)) if long_ else '')
