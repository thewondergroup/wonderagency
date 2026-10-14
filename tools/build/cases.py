# Case studies, from the agency's case study deck (October 2026). Used on the homepage, the Work page, About and llms.txt.
from html import escape as e

SCOPE = [('Content creation', 'content-creation'), ('Social media', 'social-media-management'), ('Influencer marketing', 'influencer-marketing'),
         ('Design', None), ('Paid ads', 'paid-advertising'), ('Web design', 'website-design')]

CASES = [
    dict(key='revenue', label='Restaurant · three years', title='Revenue growth and business transformation',
         stat='£3.2m → £4.6m', line='Annual revenue, grown over three years.',
         overview='A focused digital marketing strategy that significantly increased the venue’s visibility, engagement and booking demand, and strengthened its digital presence and reputation.',
         results=['Annual revenue grew from £3.2m to £4.6m over three years.', 'Instagram audience grew from 3,000 to over 20,000 followers.',
                  'Google review score rose from 4.0 to 4.6.', 'A new website and digital strategy improved discovery, booking conversion and data capture.'],
         short='Restaurant, three years. Annual revenue from £3.2m to £4.6m, Instagram from 3,000 to 20,000+ followers and Google rating from 4.0 to 4.6.'),
    dict(key='hotel', label='Hotel · three months', title='Hotel boost',
         stat='+58%', line='Year-on-year food and beverage revenue, with room bookings up 26%.',
         overview='Brought in to drive performance across both rooms and food and beverage. In three months we overhauled the hotel’s digital presence, refined its storytelling, tightened targeting and made it easier to find, so more interest turned into bookings.',
         results=['Food and beverage revenue up 58% year on year within three months.', 'Room bookings up 26% over the same period.'],
         short='Hotel, three months. Food and beverage revenue up 58% year on year, with room bookings up 26%.'),
    dict(key='overhaul', label='Three-restaurant group · Q4', title='Marketing overhaul',
         stat='+18%', line='Year-on-year revenue across Q4 for a group of three Central London restaurants.',
         overview='Brought in to drive performance across three Central London restaurants during a key trading period. Across Q4 we refreshed the group’s digital presence, sharpened its messaging and visual storytelling, and used targeted distribution to turn demand into bookings.',
         results=['18% year-on-year increase in revenue across Q4.'],
         short='Three-restaurant group, Q4. An 18% year-on-year increase in revenue after a full marketing overhaul.'),
    dict(key='michelin', label='Michelin-starred restaurant · three months', title='Michelin-star set menu',
         stat='+95%', line='Set lunch bookings by month three, against before the campaign.',
         overview='Mid-week lunches and early evenings were a struggle. We worked with the chef to reshape the set menu so it caught people’s imagination, then ran a full marketing campaign around it.',
         results=['Set lunch bookings up 79% in month two, once the campaign launched.', 'Up 95% by month three: close to double where they started.'],
         chart=[('Month 1', 'Setup', 0), ('Month 2', 'Campaign launch', 79), ('Month 3', 'Campaign running', 95)],
         short='Michelin-starred restaurant, three months. Set lunch bookings up 95% after reshaping the set menu with the chef and a full campaign.'),
    dict(key='brunch', label='Historic City venue · six weeks', title='Brunch launch',
         stat='220–250', line='Covers every Saturday, six weeks after launch.',
         overview='We launched a Saturday brunch in a historic City of London venue with no history of weekend trade, using content, social, creators and targeted ads together. Six weeks in, it sells out consistently.',
         results=['220 to 250 brunch covers every Saturday, six weeks after launch.', 'Weekend trade from a standing start, in a venue that had none.'],
         short='Historic City venue, six weeks. A new Saturday brunch now does 220 to 250 covers every week, from no weekend trade at all.'),
    dict(key='square', label='Cookbook relaunch · October 2025', title='The Square cookbooks',
         stat='48 hours', line='To sell out the limited run.',
         overview='Phil Howard’s The Square: Savoury and Sweet are two of the most celebrated cookbooks of a generation, and had been out of print for years. We built the website and ran the launch campaign to bring them back, possibly for the last time, alongside a combined collector’s edition limited to 250 hand-numbered copies.',
         results=['The limited run sold out within 48 hours of launch.', 'A new website selling Savoury, Sweet and the collector’s edition direct, with the story behind the books.',
                  'A launch campaign built around the chef, the books and the collector’s edition.'],
         scope=[('Website design', 'website-design'), ('Launch campaign', None), ('Social media', 'social-media-management'), ('Design', None)],
         site='https://thesquarecookbook.co.uk/', panel=True,
         short='Cookbook relaunch, October 2025. We built the website and launch campaign for Phil Howard’s The Square cookbooks; the limited run sold out within 48 hours.'),
]

def scope_html(pre, scope=None):
    return ''.join(('<a href="%sservices/%s/">%s</a>' % (pre, s, e(n))) if s else '<span>%s</span>' % e(n) for n, s in (scope or SCOPE))

def panel_html():
    # a typographic stand-in for photography: the two volumes and the collector's edition
    return ('<div class="p-cs-media p-cs-media--books" aria-hidden="true"><div class="p-books">'
            '<div class="p-book p-book--a"><span>Volume one</span><b>Savoury</b><i>12 chapters · 500+ pages</i></div>'
            '<div class="p-book p-book--b"><span>Volume two</span><b>Sweet</b><i>12 chapters</i></div>'
            '<div class="p-book p-book--c"><span>Collector’s edition</span><b>Savoury<br/>&amp; Sweet</b><i>250 hand-numbered copies</i></div>'
            '</div><div class="p-books-tag">Sold out in 48 hours</div></div>')

def chart_html(c):
    if 'chart' not in c: return ''
    return '<div class="p-cs-chart" aria-label="Set lunch bookings against before the campaign">%s</div>' % ''.join(
        '<div class="p-cs-bar" style="--h:%d%%"><b>%s</b><i></i><span>%s<em>%s</em></span></div>' % (max(8, v), ('+%d%%' % v) if v else 'Before', e(m), e(s)) for m, s, v in c['chart'])

def work_section(pre):
    out = ''
    for k, c in enumerate(CASES):
        media = panel_html() if c.get('panel') else ('<div class="p-cs-media"><img class="p-cs-main" src="%simages/x/cases/case-%s.webp" alt="" loading="lazy" decoding="async"/>'
                 '<img class="p-cs-inset" src="%simages/x/cases/case-%s-2.webp" alt="" loading="lazy" decoding="async"/></div>') % (pre, c['key'], pre, c['key'])
        body = ('<div class="p-cs-body"><div class="x-label">Case study 0%d · %s</div><h3>%s</h3><div class="p-cs-stat">%s</div><p class="p-cs-line">%s</p>'
                '<p>%s</p><ul class="p-cs-res">%s</ul>%s<div class="p-cs-scope"><span class="p-cs-scope-h">Scope</span>%s</div>%s</div>') % (
            k + 1, e(c['label']), e(c['title']), e(c['stat']), e(c['line']), e(c['overview']), ''.join('<li>%s</li>' % e(r) for r in c['results']), chart_html(c), scope_html(pre, c.get('scope')), ('<a class="x-link p-cs-site" href="%s" target="_blank" rel="noopener">Visit the site ↗</a>' % c['site']) if c.get('site') else '')
        out += '<article class="p-cs x-r%s" id="case-%s">%s%s</article>' % (' p-cs--flip' if k % 2 else '', c['key'], media, body)
    return '<div class="p-css">%s</div>' % out

def ld(site):
    return {"@type": "ItemList", "name": "Case studies", "itemListElement": [{"@type": "ListItem", "position": k + 1, "item": {
        "@type": "Article", "headline": c['title'], "description": c['short'], "url": site + 'work/#case-' + c['key'],
        "author": {"@id": site + "#org"}, **({"image": site + 'images/x/cases/case-%s.webp' % c['key']} if not c.get('panel') else {"about": c.get('site')})}} for k, c in enumerate(CASES)]}
