# Case studies, from the agency's case study deck (October 2026) and C's notes. Each has its own page at /work/<slug>/,
# a card on the Work page, a panel on the homepage, and a line on About and in llms.txt.
from html import escape as e

SCOPE = [('Content creation', 'content-creation'), ('Social media', 'social-media-management'), ('Influencer marketing', 'influencer-marketing'),
         ('Design', None), ('Paid ads', 'paid-advertising'), ('Web design', 'website-design')]

CASES = [
    dict(key='revenue', slug='restaurant-revenue-growth', label='Restaurant · three years', title='Revenue growth and business transformation',
         stat='£3.2m → £4.6m', line='Annual revenue, grown over three years.',
         seo='Restaurant Marketing Case Study: £3.2m to £4.6m Revenue',
         overview='A focused digital marketing strategy that significantly increased the venue’s visibility, engagement and booking demand, and strengthened its digital presence and reputation.',
         challenge='A popular restaurant with more to give: £3.2m a year in revenue, 3,000 followers on Instagram and a Google rating of 4.0. The food deserved a bigger audience, and more of the people who found it online needed to end up at a table.',
         approach=[('Content, constantly', 'Regular photo and video shoots, so there was always something new and good to post.'),
                   ('Social, every day', 'Instagram run daily, building an audience of locals and food lovers rather than chasing numbers.'),
                   ('Creators', 'The right local food creators invited in, briefed and followed up.'),
                   ('Paid ads', 'Targeted Meta and Google ads judged on bookings, not clicks.'),
                   ('A new website', 'Rebuilt for phones and for booking, with data capture so every visit could become a guest list.'),
                   ('Three years, one plan', 'Every channel pulling the same way, year after year.')],
         results=['Annual revenue grew from £3.2m to £4.6m over three years.', 'Instagram audience grew from 3,000 to over 20,000 followers.',
                  'Google review score rose from 4.0 to 4.6.', 'A new website and digital strategy improved discovery, booking conversion and data capture.'],
         nums=[('£4.6m', 'Annual revenue, up from £3.2m'), ('20,000+', 'Instagram followers, up from 3,000'), ('4.6', 'Google rating, up from 4.0')],
         short='Restaurant, three years. Annual revenue from £3.2m to £4.6m, Instagram from 3,000 to 20,000+ followers and Google rating from 4.0 to 4.6.'),
    dict(key='hotel', slug='hotel-boost', label='Hotel · three months', title='Hotel boost',
         stat='+58%', line='Year-on-year food and beverage revenue, with room bookings up 26%.',
         seo='Hotel Marketing Case Study: F&B Revenue Up 58% in Three Months',
         overview='Brought in to drive performance across both rooms and food and beverage. In three months we overhauled the hotel’s digital presence, refined its storytelling, tightened targeting and made it easier to find, so more interest turned into bookings.',
         challenge='The hotel needed both halves of the business to perform: more rooms booked, and a restaurant and bar that people chose for their own sake. And it needed results within a season, not a year.',
         approach=[('Storytelling', 'A clearer story about the hotel, its food and its place, told through new photography and video.'),
                   ('Social', 'Daily social built around the restaurant and bar as much as the rooms.'),
                   ('Creators', 'Creator visits that put the hotel in front of the right audiences.'),
                   ('Tighter targeting', 'Paid campaigns rebuilt around the guests most likely to book, for rooms and for tables.'),
                   ('Easier to find', 'Website and search improvements so interest turned into bookings.'),
                   ('Design', 'Menus, offers and campaigns designed to match.')],
         results=['Food and beverage revenue up 58% year on year within three months.', 'Room bookings up 26% over the same period.'],
         nums=[('+58%', 'Food and beverage revenue, year on year'), ('+26%', 'Room bookings'), ('3', 'Months')],
         short='Hotel, three months. Food and beverage revenue up 58% year on year, with room bookings up 26%.'),
    dict(key='overhaul', slug='restaurant-group-marketing-overhaul', label='Three-restaurant group · Q4', title='Marketing overhaul',
         stat='+18%', line='Year-on-year revenue across Q4 for a group of three Central London restaurants.',
         seo='Restaurant Group Marketing Case Study: Q4 Revenue Up 18%',
         overview='Brought in to drive performance across three Central London restaurants during a key trading period. Across Q4 we refreshed the group’s digital presence, sharpened its messaging and visual storytelling, and used targeted distribution to turn demand into bookings.',
         challenge='Three Central London restaurants going into Q4, the busiest and most competitive trading period of the year, with a digital presence that wasn’t doing them justice.',
         approach=[('A fresh look', 'New photography and video across all three restaurants.'),
                   ('Sharper messaging', 'A clear reason to choose each restaurant, in every post, ad and page.'),
                   ('Social and creators', 'Consistent social for each site, with creator visits timed for the season.'),
                   ('Targeted distribution', 'Paid campaigns aimed at the people most likely to book, when they were planning.'),
                   ('Websites', 'Sites refreshed so the booking journey was quick on a phone.'),
                   ('Design', 'Menus and campaign artwork designed to match.')],
         results=['18% year-on-year increase in revenue across Q4.'],
         nums=[('+18%', 'Revenue, year on year'), ('3', 'Central London restaurants'), ('Q4', 'The busiest quarter of the year')],
         short='Three-restaurant group, Q4. An 18% year-on-year increase in revenue after a full marketing overhaul.'),
    dict(key='michelin', slug='michelin-star-set-menu', label='Michelin-starred restaurant · three months', title='Michelin-star set menu',
         stat='+95%', line='Set lunch bookings by month three, against before the campaign.',
         seo='Michelin Restaurant Marketing Case Study: Set Lunch Bookings Up 95%',
         overview='Mid-week lunches and early evenings were a struggle. We worked with the chef to reshape the set menu so it caught people’s imagination, then ran a full marketing campaign around it.',
         challenge='Mid-week lunches and early evenings were a struggle. A Michelin-starred kitchen with empty tables at lunch is a cost, and a missed chance to win new regulars.',
         approach=[('The menu first', 'We worked with the chef to reshape the set menu so it was easy to explain and hard to resist.'),
                   ('Month one: setup', 'New photography and video of the menu, and the campaign built ready to go.'),
                   ('Month two: launch', 'Social, creators and targeted ads launched together.'),
                   ('Month three: running', 'The campaign kept running and was refined on what was filling tables.'),
                   ('Booking made easy', 'A clear path from every post and ad to a booking.'),
                   ('Design', 'Menu and campaign artwork designed to match.')],
         results=['Set lunch bookings up 79% in month two, once the campaign launched.', 'Up 95% by month three: close to double where they started.'],
         chart=[('Month 1', 'Setup', 0), ('Month 2', 'Campaign launch', 79), ('Month 3', 'Campaign running', 95)],
         nums=[('+79%', 'Set lunch bookings, month two'), ('+95%', 'Set lunch bookings, month three'), ('3', 'Months')],
         short='Michelin-starred restaurant, three months. Set lunch bookings up 95% after reshaping the set menu with the chef and a full campaign.'),
    dict(key='brunch', slug='saturday-brunch-launch', label='Historic City venue · six weeks', title='Brunch launch',
         stat='220–250', line='Covers every Saturday, six weeks after launch.',
         seo='Brunch Launch Case Study: 220–250 Covers Every Saturday in Six Weeks',
         overview='We launched a Saturday brunch in a historic City of London venue with no history of weekend trade, using content, social, creators and targeted ads together. Six weeks in, it sells out consistently.',
         challenge='The City of London empties at weekends. This historic venue had never traded on a Saturday, so there was no audience, no habit and no reviews to build on. The brunch had to be found from a standing start.',
         approach=[('Content', 'The room, the food and the drinks shot to make a weekend trip into the City feel worth it.'),
                   ('Social', 'A launch plan that built anticipation before the first Saturday and kept it going after.'),
                   ('Creators', 'Creators invited in early, so the brunch had a following from week one.'),
                   ('Targeted ads', 'Paid campaigns aimed at people who go out for brunch, wherever they live in London.'),
                   ('Booking', 'A clear way to book from every post and ad.'),
                   ('Design', 'Brunch menus and campaign artwork designed to match.')],
         results=['220 to 250 brunch covers every Saturday, six weeks after launch.', 'Weekend trade from a standing start, in a venue that had none.'],
         nums=[('220–250', 'Covers every Saturday'), ('6', 'Weeks to sell out'), ('Sold out', 'Consistently, every Saturday')],
         short='Historic City venue, six weeks. A new Saturday brunch now does 220 to 250 covers every week, from no weekend trade at all.'),
    dict(key='square', slug='the-square-cookbooks', label='Cookbook relaunch · October 2025', title='The Square cookbooks',
         stat='48 hours', line='To sell out the limited run.',
         seo='The Square Cookbooks Relaunch: Sold Out in 48 Hours',
         overview='Phil Howard’s The Square: Savoury and Sweet are two of the most celebrated cookbooks of a generation, and had been out of print for years. We built the website and ran the launch campaign to bring them back, possibly for the last time, alongside a combined collector’s edition limited to 250 hand-numbered copies.',
         challenge='Two much-loved cookbooks coming back into print, possibly for the last time, plus a collector’s edition of just 250 hand-numbered copies. One chance to reach the people who had wanted them for years, and a short window to do it.',
         approach=[('The website', 'We designed and built thesquarecookbook.co.uk to sell Savoury, Sweet and the collector’s edition direct.'),
                   ('The story', 'A publisher’s note and words from fellow chefs, so the site explained why these books matter.'),
                   ('The launch', 'A campaign built around the chef, the books and the collector’s edition.'),
                   ('Social', 'Launch content that reached cooks, chefs and collectors who knew the books.'),
                   ('Design', 'Launch artwork designed around the books themselves.'),
                   ('Selling out', 'Everything pointed at one thing: getting the right people to the shop in time.')],
         results=['The limited run sold out within 48 hours of launch.', 'A new website selling Savoury, Sweet and the collector’s edition direct, with the story behind the books.',
                  'A launch campaign built around the chef, the books and the collector’s edition.'],
         nums=[('48 hrs', 'To sell out'), ('250', 'Hand-numbered collector’s editions'), ('2', 'Volumes back in print')],
         scope=[('Website design', 'website-design'), ('Launch campaign', None), ('Social media', 'social-media-management'), ('Design', None)],
         site='https://thesquarecookbook.co.uk/',
         short='Cookbook relaunch, October 2025. We built the website and launch campaign for Phil Howard’s The Square cookbooks; the limited run sold out within 48 hours.'),
    dict(key='longboard', slug='longboard-coffee-auction', label='Coffee auction · first ever', title='Longboard’s first private auction',
         stat='$4,688/kg', line='Average lot price: the highest of any coffee auction in the world.',
         seo='Longboard Coffee Auction Case Study: The World’s Highest Average Lot Price',
         overview='Longboard grows rare Panama Geisha at Misty Mountain in Boquete. We launched their first ever private auction: a rebuilt website, new content telling the story of the brand, the marketing for the auction, and the artwork and boxes for the lots and sample sets.',
         challenge='A first auction has no track record. Longboard needed serious buyers around the world to trust a new sale, taste the coffee before bidding and feel the story behind it, from a farm in the cloud forest of western Panama.',
         approach=[('A new website', 'We rebuilt Longboard’s website and built the auction site, with the story, the lots and a way to register.'),
                   ('The story, on camera', 'New photography and video of the farm, the forest and the people, to tell the story of the brand.'),
                   ('Marketing the auction', 'A campaign aimed at specialty buyers and collectors across Asia, the Middle East and Europe.'),
                   ('Lot artwork', 'We designed the artwork for every lot, so each coffee had its own identity.'),
                   ('Boxes and sample sets', 'We designed the presentation boxes for the lots and the sample sets buyers tasted before bidding.'),
                   ('Sample sets that sold out', 'A limited run of sample sets, so buyers could taste every lot and host tastings of their own.')],
         results=['The highest average lot price of any coffee auction in the world: $4,688.82 per kg.', '$256,478 raised across 12 lots, with buyers in 8 countries.',
                  'A top lot of $10,701 per kg.', 'Every sample set sold out before the auction.'],
         nums=[('$4,688', 'Average price per kg, a world record'), ('$256k', 'Raised across 12 lots'), ('8', 'Countries bidding')],
         scope=[('Website design', 'website-design'), ('Content creation', 'content-creation'), ('Auction marketing', None), ('Social media', 'social-media-management'), ('Lot artwork', None), ('Box and packaging design', None)],
         site='https://longboardcoffees.com/',
         film='lb-film', pair=('-2', '-3'),
         short='Coffee auction, first ever. We rebuilt Longboard’s website, shot new content, marketed the auction and designed the lot artwork and boxes; it achieved the highest average lot price of any coffee auction in the world, $4,688.82 per kg.'),
]
for _k, _c in enumerate(CASES): _c['n'] = _k + 1
BYKEY = {c['key']: c for c in CASES}

def url(c): return 'work/%s/' % c['slug']

def scope_html(pre, scope=None):
    return ''.join(('<a href="%sservices/%s/">%s</a>' % (pre, s, e(n))) if s else '<span>%s</span>' % e(n) for n, s in (scope or SCOPE))

def chart_html(c):
    if 'chart' not in c: return ''
    return '<div class="p-cs-chart" aria-label="Set lunch bookings against before the campaign">%s</div>' % ''.join(
        '<div class="p-cs-bar" style="--h:%d%%"><b>%s</b><i></i><span>%s<em>%s</em></span></div>' % (max(8, v), ('+%d%%' % v) if v else 'Before', e(m), e(s)) for m, s, v in c['chart'])

def img(pre, c, n=''):
    return '%simages/x/cases/case-%s%s.webp' % (pre, c['key'], n)

# ---------- cards (Work page) ----------
def cards(pre, skip=None, small=False):
    out = ''
    for k, c in enumerate([c for c in CASES if c is not skip]):
        out += ('<a class="p-csc x-r" style="--x-d:%.2fs" href="%s%s"><div class="p-csc-media"><img src="%s" alt="" loading="lazy" decoding="async"/></div>'
                '<div class="x-label">%s</div><h3>%s</h3><div class="p-csc-stat">%s</div><p>%s</p><em>Read the case study →</em></a>') % (
            (k % 3) * 0.08, pre, url(c), img(pre, c), e(c['label']), e(c['title']), e(c['stat']), e(c['line']))
    return '<div class="p-cscs%s">%s</div>' % (' p-cscs--small' if small else '', out)

# ---------- a case study page ----------
def page_body(pre, c):
    k = CASES.index(c); nxt = CASES[(k + 1) % len(CASES)]
    nums = '<div class="p-res p-res--3">%s</div>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><b>%s</b><p>%s</p></div>' % (j * 0.08, e(a), e(b)) for j, (a, b) in enumerate(c['nums']))
    steps = ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % ((j % 3) * 0.08, j + 1, e(t), e(d)) for j, (t, d) in enumerate(c['approach']))
    site = ('<a class="x-link" href="%s" target="_blank" rel="noopener">Visit the site ↗</a>' % c['site']) if c.get('site') else ''
    return (
        '<section class="p-hero p-hero--case"><div>{CRUMBS}'
        '<div class="x-label">Case study 0%d · %s</div><h1>%s</h1><div class="p-cs-stat p-cs-stat--hero">%s</div><p class="p-lede">%s</p>'
        '<div class="p-btns"><a href="%scontact/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#results" class="x-link">See the results</a></div></div>'
        '<div class="p-hero-media p-hero-media--still"><img src="%s" alt="" decoding="async"/></div></section>'
        '<section class="p-sec" style="padding-top:2rem">%s</section>'
        '<section class="p-sec"><div class="p-two"><p class="p-big x-r">The challenge</p><div class="p-body x-r"><p>%s</p><p>%s</p></div></div></section>'
        '<section class="p-sec"><h2 class="p-h2 x-r">What we did</h2><div class="p-inc">%s</div></section>'
        '{MEDIA}'
        '<section class="p-sec" id="results"><h2 class="p-h2 x-r">Results</h2><div class="p-cs-detail x-r"><ul class="p-cs-res">%s</ul>%s</div></section>'
        '<section class="p-sec"><div class="p-cs-scope x-r"><span class="p-cs-scope-h">Scope</span>%s</div>%s</section>'
        '<section class="p-sec"><div class="p-next x-r"><span class="x-label">Next case study</span><a href="%s%s"><b>%s</b><em>%s</em><i>→</i></a></div></section>'
        '<section class="p-sec"><h2 class="p-h2 x-r">More case studies</h2>%s</section>') % (
        c['n'], e(c['label']), e(c['title']), e(c['stat']), e(c['line']), pre, img(pre, c),
        nums, e(c['challenge']), e(c['overview']), steps, ''.join('<li>%s</li>' % e(r) for r in c['results']), chart_html(c),
        scope_html(pre, c.get('scope')), ('<div style="margin-top:1.6rem">%s</div>' % site) if site else '',
        pre, url(nxt), e(nxt['title']), e(nxt['stat']), cards(pre, skip=c, small=True))

def media_html(pre, c):
    out = ''
    if c.get('film'):
        out += ('<section class="p-sec"><div class="p-cs-film x-r"><video muted loop playsinline preload="none" poster="%simages/x/clip-%s.webp" '
                'data-src="%svideos/clips/%s-l.mp4" data-x-auto aria-hidden="true"></video></div></section>') % (pre, c['film'], pre, c['film'])
    if c.get('pair'):
        out += '<section class="p-sec"><div class="p-cs-pair p-cs-pair--even">%s</div></section>' % ''.join(
            '<img class="x-r" style="--x-d:%.2fs" src="%s" alt="" loading="lazy" decoding="async"/>' % (j * 0.1, img(pre, c, s)) for j, s in enumerate(c['pair']))
    else:
        out += '<section class="p-sec"><div class="p-cs-wide x-r"><img src="%s" alt="" loading="lazy" decoding="async"/></div></section>' % img(pre, c, '-2')
    return out

def page_ld(site, c, org_id):
    return {"@type": "Article", "headline": c['title'] + ': ' + c['line'].rstrip('.'), "description": c['short'], "url": site + url(c),
            "image": site + 'images/x/cases/case-%s.webp' % c['key'], "author": {"@id": org_id}, "publisher": {"@id": org_id},
            "about": "Hospitality marketing case study", "mainEntityOfPage": site + url(c)}

def ld(site):
    return {"@type": "ItemList", "name": "Case studies", "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": site + url(c), "name": c['title']} for k, c in enumerate(CASES)]}
