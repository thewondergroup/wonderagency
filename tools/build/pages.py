import os, sys, json, re, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_content import SERVICES, MEDIA, SECTORS, COMBOS as _C
from articles_content import ARTICLES as _A
import media4, sites, cases
media4.apply(SERVICES, MEDIA, SECTORS, _C, _A)
ROOT = sys.argv[1]
SITE = 'https://thewonderagency.co/'
ORG = {"@type": "ProfessionalService", "@id": SITE + "#org", "name": "The Wonder Agency", "url": SITE, "logo": SITE + "images/x/icon-512.png", "telephone": "+447775022514", "email": "hello@thewonder.group", "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"}}
e = H.escape
BYSLUG = {s['slug']: s for s in SERVICES}

def exists(rel): return os.path.isfile(os.path.join(ROOT, rel))
def clip(name):
    for size in ('m', 's'):
        if exists('videos/clips/%s-%s.mp4' % (name, size)): return 'videos/clips/%s-%s.mp4' % (name, size)
    raise SystemExit('missing clip ' + name)
def poster(name):
    p = 'images/x/clip-%s.webp' % name; assert exists(p), p; return p

from pages_content import COMBOS
SVC_LINE = {'influencer-marketing': 'Creators who bring the right guests in', 'content-creation': 'Photo and video that makes people want to book', 'social-media-management': 'Instagram and TikTok, run every day',
            'paid-advertising': 'Meta and Google ads, tracked to the booking', 'seo-ai-search': 'Found on Google, recommended by AI',
            'website-design': 'Fast websites that turn visits into bookings', 'email-marketing': 'Bring past guests back, again and again'}
SEC_LINE = {'restaurants': 'Fuller tables, every night of the week', 'hotels': 'Rooms, dining, events and weddings', 'bars-and-pubs': 'Busy bars, booked tables and big nights',
            'restaurant-groups': 'Several brands, one plan', 'food-and-drink-brands': 'Wanted on menus and at home'}
NAV = [('services/', 'Services', 'services'), ('who-we-work-with/', 'Who we work with', 'sectors'), ('wonder-score/', 'AI Search', 'ai'), ('work/', 'Work', None), ('about/', 'About', None), ('contact/', 'Contact', None)]
AI_LINKS = [('wonder-score/', 'Wonder Score: our AI tool'), ('services/seo-ai-search/', 'SEO and AI search'), ('services/seo-ai-search/restaurants/', 'Restaurant SEO'), ('insights/ai-search-for-restaurants/', 'Why AI search changes discovery')]

def mm_video(pre, name, cls=''):
    return '<video%s muted loop playsinline preload="none" data-src="%s%s" data-mm-poster="%s%s" aria-hidden="true"></video>' % (' class="%s"' % cls if cls else '', pre, clip(name), pre, poster(name))
def ai_visual(pre):
    return ('<div class="x-ai" aria-hidden="true"><div class="x-ai-orb"></div><div class="x-ai-grid"></div>'
            '<div class="x-ai-win"><div class="x-ai-bar"><i></i><i></i><i></i><span>AI assistant</span></div><div class="x-ai-body">'
            '<div class="x-ai-q"><span class="x-ai-type" data-text="Where should I book for a birthday dinner in Soho?"></span></div>'
            '<div class="x-ai-a"><p>Three places stand out:</p><ol>'
            '<li><em>1</em><b class="x-ai-you">Your restaurant</b><span class="x-ai-why">Great for occasions</span></li>'
            '<li><em>2</em><span class="x-ai-ghost" style="width:46%"></span></li><li><em>3</em><span class="x-ai-ghost" style="width:34%"></span></li></ol></div></div></div>'
            '<div class="x-ai-score"><div class="x-ai-ring"><svg viewBox="0 0 100 100"><circle class="bg" cx="50" cy="50" r="42"/><circle class="fg" cx="50" cy="50" r="42"/></svg><b><span class="x-ai-num" data-n="86">86</span><small>Score</small></b></div>'
            '<div class="x-ai-rows"><div>Mention rate<span>High</span><i></i></div><div>Website health<span>Strong</span><i></i></div><div>Market position<span>Top 3</span><i></i></div></div></div>'
            '</div>')

def nav_html(pre, home=False):
    P = pre  # prefix for links
    brand = '#top' if home else (pre or './')
    audit = ('%sfree-audit/"' % pre)
    links = ''.join(('<a href="%s%s" class="hover-cursor x-nav-t" data-mega="%s">%s<i class="x-car" aria-hidden="true"></i></a>' % (P, u, m, t)) if m else ('<a href="%s%s" class="hover-cursor">%s</a>' % (P, u, t)) for u, t, m in NAV)
    # services panel
    items = ''.join('<a class="x-mm-item" href="%sservices/%s/" data-s style="--s:%d"><span>0%d</span><div><b>%s</b><em>%s</em></div><i>→</i></a>' % (P, s['slug'], k, k + 1, e(s['name']), e(SVC_LINE[s['slug']])) for k, s in enumerate(SERVICES))
    vids = ''.join(mm_video(pre, s['clip']) for s in SERVICES)
    spec = ''.join('<a href="%s%s">%s</a>' % (P, c['path'], e(c['short'])) for c in COMBOS)
    p_svc = ('<div class="x-mm" data-panel="services" role="region" aria-label="Services" aria-hidden="true"><div class="x-mm-svc-grid">'
             '<div><span class="x-mm-label" data-s>Seven services that fill a room</span><div class="x-mm-list">%s</div></div>'
             '<a class="x-mm-prev" href="%sservices/%s/" data-s style="--s:2" tabindex="-1">%s<div class="x-mm-cap"><b>%s</b><span>Explore →</span></div></a>'
             '<div class="x-mm-cta" data-s style="--s:4">%s<div class="x-label">Free audit</div><h3>Find out what’s costing you bookings</h3>'
             '<p>We review your social media, ads, search and website, and tell you what we’d fix first. Free, with no obligation.</p>'
             '<a href="%s class="x-nav-cta">Get your free audit <i>→</i></a><a href="%sservices/" class="x-mm-sub">See all services →</a></div></div>'
             '<div class="x-mm-spec" data-s style="--s:6"><span class="x-mm-label">Specialist</span>%s</div></div>') % (
             items, P, SERVICES[0]['slug'], vids, e(SERVICES[0]['name']), mm_video(pre, 'w19'), audit, P, spec)
    # sectors panel
    tiles = ''.join('<a class="x-mm-tile" href="%swho-we-work-with/%s/" data-s style="--s:%d">%s<div><b>%s</b><em>%s</em></div></a>' % (P, x['slug'], k, mm_video(pre, x['clip']), e(x['name']), e(SEC_LINE[x['slug']])) for k, x in enumerate(SECTORS))
    tiles += '<a class="x-mm-tile" href="%slondon/" data-s style="--s:5"><img data-mm-src="%simages/x/dining-room.webp" alt=""/><div><b>London</b><em>Our home city, and the toughest market</em></div></a>' % (P, pre)
    p_sec = ('<div class="x-mm" data-panel="sectors" role="region" aria-label="Who we work with" aria-hidden="true"><div class="x-mm-sec-grid">'
             '<div><span class="x-mm-label" data-s>Specialists in hospitality</span><div class="x-mm-tiles">%s</div></div>'
             '<div class="x-mm-cta x-mm-cta--plain" data-s style="--s:3">%s<div class="x-label">Who we work with</div><h3>From Michelin stars to neighbourhood favourites</h3>'
             '<p>Restaurants, hotels, bars and food and drink brands, in London, across the UK and internationally.</p>'
             '<div class="x-mm-links"><a href="%swho-we-work-with/hotels/food-and-beverage/">Hotel F&amp;B marketing<i>→</i></a><a href="%swork/">See our results<i>→</i></a><a href="%swho-we-work-with/">Everyone we work with<i>→</i></a></div>'
             '<div style="margin-top:1.4rem"><a href="%s class="x-nav-cta">Get a free audit <i>→</i></a></div></div></div></div>') % (tiles, mm_video(pre, 'w21'), P, P, P, audit)
    # AI panel
    ail = ''.join('<a href="%s%s">%s<i>→</i></a>' % (P, u, e(t)) for u, t in AI_LINKS)
    p_ai = ('<div class="x-mm" data-panel="ai" role="region" aria-label="AI Search" aria-hidden="true"><div class="x-mm-ai-grid">'
            '<div class="x-mm-ai-copy"><div class="x-label" data-s>AI Search</div><h3 data-s style="--s:1">Are you recommended by AI?</h3>'
            '<p data-s style="--s:2">More guests now ask ChatGPT, Gemini and Perplexity where to eat, drink and stay. Wonder Score shows whether they name you, analyses your website and your competitors, and helps you get recommended more.</p>'
            '<div class="x-mm-btns" data-s style="--s:3"><a href="https://wonderscore.ai" target="_blank" rel="noopener" class="x-nav-cta">Check your Wonder Score <i>→</i></a><a href="%swonder-score/" class="x-link">How it works</a></div>'
            '<div class="x-mm-links" data-s style="--s:4">%s</div></div>'
            '<div data-s style="--s:2">%s</div></div></div>') % (P, ail, ai_visual(pre))
    mega = '<div class="x-mega-wrap"><div class="x-mega">%s%s%s</div></div>' % (p_svc, p_sec, p_ai)
    header = ('<header class="x-nav%s" id="x-nav"><a href="%s" class="x-nav-brand hover-cursor">The Wonder Agency</a><nav class="x-nav-links" aria-label="Main">%s</nav>'
              '<div class="x-nav-right"><a href="%s class="x-nav-cta hover-cursor">Free audit <i>→</i></a>'
              '<button type="button" class="x-nav-burger" aria-label="Open menu" aria-expanded="false" aria-controls="x-menu"><span></span><span></span></button></div>%s</header>'
              '<div class="x-mega-veil" aria-hidden="true"></div>') % ('' if home else ' is-ready', brand, links, audit, mega)
    # mobile menu
    def ms(href, img, name, line):
        return '<a class="x-ms" href="%s"><img data-mm-src="%s%s" alt=""/><div><b>%s</b><em>%s</em></div><i>→</i></a>' % (href, pre, img, e(name), e(line))
    m_svc = ''.join(ms('%sservices/%s/' % (P, s['slug']), poster(s['clip']), s['name'], SVC_LINE[s['slug']]) for s in SERVICES)
    m_sec = ''.join(ms('%swho-we-work-with/%s/' % (P, x['slug']), poster(x['clip']), x['name'], SEC_LINE[x['slug']]) for x in SECTORS) + ms('%slondon/' % P, 'images/x/dining-room.webp', 'London', 'Our home city')
    def mi(k, label, inner):
        return ('<div class="x-mi" style="--i:%d"><button type="button" class="x-mi-t" data-mi aria-expanded="false">%s<span class="x-plus" aria-hidden="true"></span></button>'
                '<div class="x-mi-p"><div><div class="x-mi-in">%s</div></div></div></div>') % (k, label, inner)
    m_ai = ai_visual(pre) + '<div class="x-mm-links">%s<a href="https://wonderscore.ai" target="_blank" rel="noopener">Check your score at wonderscore.ai<i>→</i></a></div>' % ''.join('<a href="%s%s">%s<i>→</i></a>' % (P, u, e(t)) for u, t in AI_LINKS)
    plain = lambda k, u, t: '<div class="x-mi" style="--i:%d"><a class="x-mi-t" href="%s%s">%s<span class="x-arr">→</span></a></div>' % (k, P, u, t)
    mnav = (mi(0, 'Services', m_svc + '<a class="x-mi-all" href="%sservices/">All services →</a>' % P) +
            mi(1, 'Who we work with', m_sec + '<a class="x-mi-all" href="%swho-we-work-with/">Everyone we work with →</a>' % P) +
            mi(2, 'AI Search', m_ai) + plain(3, 'work/', 'Work') + plain(4, 'insights/', 'Insights') + plain(5, 'about/', 'About') + plain(6, 'contact/', 'Work with us'))
    menu = ('<div class="x-menu" id="x-menu" aria-hidden="true" data-lenis-prevent><div class="x-mnav" role="navigation" aria-label="Menu">%s</div>'
            '<a href="%s class="x-nav-cta x-menu-cta">Get a free audit <i>→</i></a>'
            '<p class="x-menu-contact"><a href="mailto:hello@thewonder.group">hello@thewonder.group</a><a href="tel:+447775022514">+44 777 502 2514</a></p></div>') % (mnav, audit)
    return header + menu

def head(pre, title, desc, path, ld):
    return ('<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"/><title>%s</title><meta name="description" content="%s"/>'
            '<meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="canonical" href="%s"/>'
            '<meta property="og:type" content="website"/><meta property="og:site_name" content="The Wonder Agency"/><meta property="og:title" content="%s"/>'
            '<meta property="og:description" content="%s"/><meta property="og:url" content="%s"/><meta property="og:image" content="%simages/x/og.jpg"/>'
            '<meta name="twitter:card" content="summary_large_image"/><meta name="theme-color" content="#000000"/>'
            '<link href="%simages/635179b17db802c3563cd426_Wonder-List-Favicon.png" rel="shortcut icon" type="image/x-icon"/>'
            '<link rel="preload" href="%sfonts/italiana-400.woff2" as="font" type="font/woff2" crossorigin/>'
            '<link href="%scss/extend.css" rel="stylesheet"/><link href="%scss/pages.css" rel="stylesheet"/>'
            '<script>document.documentElement.className+=" w-mod-js"</script>'
            '<script type="application/ld+json">%s</script></head><body>') % (
        e(title), e(desc), SITE + path, e(title), e(desc), SITE + path, SITE, pre, pre, pre, pre,
        json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace('</', '<\\/'))

def chrome_top(pre):
    return nav_html(pre) + '<div class="x-grain" aria-hidden="true"></div><main class="p-main">'

def footer_html(pre):
    svc = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, x['slug'], e(x['name'])) for x in SERVICES)
    sec = ''.join('<li><a href="%swho-we-work-with/%s/">%s</a></li>' % (pre, x['slug'], e(x['name'])) for x in SECTORS)
    return ('<footer class="x-footer"><div class="x-footer-grid x-footer-grid--4"><div><div class="x-footer-brand">The Wonder Agency</div>'
            '<p>The Wonder Agency is a London digital marketing agency specialising in restaurants, hotels and bars, working across the UK and internationally. Content, social media, ads, search, websites and email: everything you need to get more bookings.</p>'
            '<p><a href="mailto:hello@thewonder.group">hello@thewonder.group</a><br/><a href="tel:+447775022514">+44 777 502 2514</a></p></div>'
            '<div><h3>Services</h3><ul>%s</ul></div><div><h3>Who we work with</h3><ul>%s<li><a href="%slondon/">London</a></li></ul></div>'
            '<div><h3>Company</h3><ul><li><a href="%sabout/">About</a></li><li><a href="%swork/">Work</a></li><li><a href="%swonder-score/">AI Search</a></li><li><a href="%sinsights/">Insights</a></li><li><a href="%spricing/">Pricing</a></li>'
            '<li><a href="%sfree-audit/">Free audit</a></li><li><a href="%scontact/">Contact</a></li><li><a href="https://www.instagram.com/the.wonder.list/" target="_blank" rel="noopener">Instagram</a></li></ul></div></div>'
            '<div class="x-footer-base"><span>© 2026 The Wonder Agency · <a href="%sprivacy/">Privacy policy</a></span><span>Made to be booked out</span></div></footer>') % (svc, sec, pre, pre, pre, pre, pre, pre, pre, pre, pre)

def chrome_bottom(pre, extra_js=''):
    return ('</main>' + footer_html(pre) +
            '<script src="%sjs/extend.js"></script><script src="%sjs/lenis.min.js"></script><script src="%sjs/extend3.js"></script><script src="%sjs/mega.js"></script>%s</body></html>') % (pre, pre, pre, pre, extra_js)

def crumbs(pre, items):
    lis = ''.join(('<li><a href="%s">%s</a></li>' % (pre + u if u is not None else '', t)) if u is not None else '<li>%s</li>' % t for u, t in items)
    return '<ol class="p-crumbs">%s</ol>' % lis
def crumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + (u or '')} for i, (u, t) in enumerate(items)]}
def faq_html(faqs):
    return ('<div class="x-acc x-acc--q">' + ''.join('<div class="x-acc-item x-r"><button type="button" class="x-acc-btn hover-cursor" aria-expanded="false" aria-controls="q-%d"><span class="x-acc-name">%s</span><span class="x-acc-icon" aria-hidden="true"></span></button><div class="x-acc-panel" id="q-%d"><div class="x-acc-inner"><p>%s</p></div></div></div>' % (k, e(q), k, e(a)) for k, (q, a) in enumerate(faqs)) + '</div>')
def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
def video(pre, name, eager=True):
    attrs = 'autoplay muted loop playsinline preload="auto" src="%s%s"' % (pre, clip(name)) if eager else 'muted loop playsinline preload="none" data-src="%s%s" data-x-auto' % (pre, clip(name))
    return '<video %s poster="%s%s" aria-hidden="true"></video>' % (attrs, pre, poster(name))
def end_cta(pre, h2='Get your free audit', p='Tell us about your venue and we’ll show you what’s working, what isn’t, and what we’d do first. No charge and no obligation.'):
    return ('<section class="p-end"><h2 class="x-r">%s</h2><p class="x-r">%s</p><div class="p-btns x-r"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a>'
            '<a href="mailto:hello@thewonder.group" class="x-link">Email us</a></div></section>') % (h2, p, pre)

def clip_l(name):
    for size in ('l', 'm', 's'):
        if exists('videos/clips/%s-%s.mp4' % (name, size)): return 'videos/clips/%s-%s.mp4' % (name, size)
    raise SystemExit('missing clip ' + name)
def gallery(pre, items, title='In pictures'):
    cells = ''
    for k, (kind, src, cap) in enumerate(items):
        if kind == 'v': media = video(pre, src, False)
        else: assert exists(src), src; media = '<img src="%s%s" alt="%s" loading="lazy"/>' % (pre, src, e(cap))
        cells += '<figure class="p-gal-cell%s x-r" style="--x-d:%.2fs">%s<figcaption>%s</figcaption></figure>' % (' p-gal-wide' if kind == 'w' else '', (k % 4) * 0.07, media, e(cap))
    return '<section class="p-sec"><h2 class="p-h2 x-r">%s</h2></section><div class="p-gal">%s</div>' % (title, cells)
def band(pre, name, line, sub=''):
    return ('<section class="p-band x-r"><video muted loop playsinline preload="none" poster="%s%s" data-src="%s%s" data-x-auto aria-hidden="true"></video>'
            '<div class="p-band-in"><p>%s</p>%s</div></section>') % (pre, poster(name), pre, clip_l(name), e(line), ('<span>%s</span>' % e(sub)) if sub else '')

def write(rel, text):
    path = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w', encoding='utf-8').write(text)

# ---------- service pages ----------
for s in SERVICES:
    pre = '../../'; path = 'services/%s/' % s['slug']
    items = [('', 'Home'), ('services/', 'Services'), (None, s['name'])]
    ld = [ORG, {"@type": "Service", "name": s['name'] + ' for restaurants, hotels and bars', "serviceType": s['name'], "description": s['desc'], "provider": {"@id": SITE + "#org"},
                "areaServed": ["United Kingdom", "International"], "audience": {"@type": "Audience", "audienceType": "Restaurants, hotels, bars and food and drink brands"}, "url": SITE + path},
          crumb_ld([('', 'Home'), ('services/', 'Services'), (path, s['name'])]), faq_ld(s['faqs'])]
    if s['slug'] == 'website-design': ld.append(sites.ld(SITE))
    inc = ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % ((k % 3) * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(s['inc']))
    steps = ''.join('<div class="x-step x-r" style="--x-d:%.2fs"><span>Step %d</span><h3>%s</h3><p>%s</p></div>' % (k * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(s['steps']))
    proof = ''
    if s['proof']:
        proof = '<section class="p-sec"><h2 class="p-h2 x-r">Results</h2><div class="p-proof x-r"><b>%s</b><p>%s <a href="%s#Results">See more results</a></p></div></section>' % (e(s['proof'][0]), e(s['proof'][1]), pre)
    elif s['slug'] == 'seo-ai-search':
        proof = '<section class="p-sec"><h2 class="p-h2 x-r">Are you recommended by AI?</h2><div class="p-proof x-r"><b>Wonder Score</b><p>Our own tool analyses your website and your competitors, shows how often AI assistants recommend you, and tells you what to change. <a href="https://wonderscore.ai" target="_blank" rel="noopener">Check your Wonder Score</a></p></div></section>'
    rel = ''.join('<a class="p-card x-r" href="%sservices/%s/"><div class="p-card-media">%s</div><h3>%s</h3><p>%s</p><em>Find out more →</em></a>' % (pre, r, video(pre, BYSLUG[r]['clip'], False), e(BYSLUG[r]['name']), e(BYSLUG[r]['card'])) for r in s['related'])
    body = (head(pre, s['title'], s['desc'], path, ld) + chrome_top(pre) +
        '<section class="p-hero"><div>' + crumbs(pre, items) + '<div class="x-label">%s</div><h1>%s</h1><p class="p-lede">%s</p>' % (e(s['name']), e(s['h1']), e(s['lede'])) +
        '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#%s" class="x-link">%s</a></div></div>' % (pre, 'sites' if s['slug'] == 'website-design' else 'included', 'See sites we’ve built' if s['slug'] == 'website-design' else 'What’s included') +
        '<div class="p-hero-media">%s</div></section>' % video(pre, s['clip']) +
        '<section class="p-sec"><div class="p-two"><p class="p-big x-r">%s</p><div class="p-body x-r">%s</div></div></section>' % (e(s['big']), ''.join('<p>%s</p>' % e(t) for t in s['why'])) +
        band(pre, MEDIA[s['slug']]['band'][0], MEDIA[s['slug']]['band'][1]) +
        '<section class="p-sec" id="included"><h2 class="p-h2 x-r">What’s included</h2><div class="p-inc">%s</div></section>' % inc +
        (sites.section(pre, lede='Every one designed and built by us: fast, built for phones, and set up so the booking button is never more than a thumb away.') if s['slug'] == 'website-design' else gallery(pre, MEDIA[s['slug']]['gallery'], 'Recent work' if s['slug'] in ('content-creation', 'social-media-management') else 'In pictures')) +
        '<section class="p-sec"><h2 class="p-h2 x-r">How it works</h2><div class="x-steps" style="margin-top:0">%s</div></section>' % steps +
        proof +
        '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(s['faqs']) +
        '<section class="p-sec"><h2 class="p-h2 x-r">Works well with</h2><div class="p-cards p-cards--small">%s</div></section>' % rel +
        end_cta(pre) + chrome_bottom(pre))
    write(path + 'index.html', body)

# ---------- services overview ----------
pre = '../'; path = 'services/'
cards = ''.join('<a class="p-card x-r" style="--x-d:%.2fs" href="%s/"><div class="p-card-media">%s</div><em>0%d</em><h3>%s</h3><p>%s</p><em>Find out more →</em></a>' % ((k % 3) * 0.08, s['slug'], video(pre, s['clip'], False), k + 1, e(s['name']), e(s['card'])) for k, s in enumerate(SERVICES))
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Services')]),
      {"@type": "ItemList", "name": "Hospitality marketing services", "itemListElement": [{"@type": "ListItem", "position": k + 1, "url": SITE + 'services/%s/' % s['slug'], "name": s['name']} for k, s in enumerate(SERVICES)]}]
write(path + 'index.html', head(pre, 'Hospitality Marketing Services | Restaurants, Hotels & Bars | The Wonder Agency',
      'Content, social media, paid ads, SEO and AI search, websites and email for restaurants, hotels and bars. Everything you need to get more bookings, from one team.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text"><div>' + crumbs(pre, [('', 'Home'), (None, 'Services')]) +
      '<div class="x-label">Services</div><h1>Everything you need to get more bookings</h1><p class="p-lede">Seven services that decide whether people find you, choose you and book. Take one, or let one team run them all, so every channel works towards the same goal.</p>'
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a></div></div></section>' % pre +
      '<section class="p-sec" style="padding-top:2rem"><div class="p-cards">%s</div></section>' % cards +
      end_cta(pre, 'Not sure where to start?', 'The free audit looks at your social media, ads, search and website, and tells you which of the seven will make the biggest difference first.') + chrome_bottom(pre))

# ---------- about ----------
pre = '../'; path = 'about/'
logos = re.findall(r'<span class="x-logo"><img src="([^"]+)"', open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read())
seen = []; [seen.append(x) for x in logos if x not in seen]
logo_grid = ''.join('<span class="p-logo"><img src="%s%s" alt="" loading="lazy"/></span>' % (pre, x) for x in seen)
WALL = [['w19', 'w66', 'w24'], ['w68', 'w20', 'w16'], ['w58', 'w12', 'w75'], ['w18', 'w48', 'w57']]
wall = ''.join('<div class="p-aw-col">%s</div>' % ''.join('<div class="p-aw-cell">%s</div>' % video(pre, n, k < 2 and j < 2) for j, n in enumerate(col + col)) for k, col in enumerate(WALL))
STATS = [('30M+', 'Impressions a month across client accounts'), ('4,200+', 'Pieces of content produced')]
KNOW = [('Covers, not clicks', 'We measure success the way you do: bookings, covers, room nights and revenue. Likes and reach only matter when they lead somewhere.'),
        ('The hospitality calendar', 'Christmas parties are booked in September and Valentine’s in January. We plan campaigns months ahead, around the moments that fill venues.'),
        ('Booking systems', 'We track ads, social and email through to the booking wherever your system allows, so you can see what each booking cost.'),
        ('Hotels beyond rooms', 'Restaurants, bars, events, weddings and corporate. We market every part of a hotel that earns revenue, not just the rooms.'),
        ('Groups and multi-site', 'Several venues and brands, each with its own voice and audience, run from one plan without them blurring together.'),
        ('Shooting around service', 'We shoot in working kitchens and full dining rooms, before or around service, without getting in your team’s way.')]
RESULTS = [('£3.2m → £4.6m', 'Annual revenue for a restaurant over three years, with Instagram from 3,000 to 20,000+ followers.'),
           ('+58%', 'Year-on-year food and beverage revenue for a hotel in three months, with room bookings up 26%.'),
           ('+95%', 'Mid-week set lunch bookings at a Michelin-starred restaurant within three months.'),
           ('+18%', 'Q4 revenue for a three-restaurant group after a full digital overhaul.'),
           ('220–250', 'Brunch covers every Saturday, six weeks after launching a new brunch in a historic City venue with no weekend trade.'),
           ('48 hours', 'For the limited relaunch of The Square cookbooks to sell out, with a website and launch campaign by us.'),
           ('$4,688/kg', 'The highest average lot price of any coffee auction in the world, for Longboard’s first private auction.')]
BELIEFS = [('People choose places that say something about them.', 'Where we eat, drink and stay says something about who we are. Good hospitality marketing makes clear what choosing your venue says about your guests, and makes sure your whole team tells the same story.'),
           ('Attention is an exchange.', 'People give you their attention and expect something back: something useful, something beautiful or something to look forward to. We make content that earns its place in the feed.'),
           ('True stories beat spin.', 'Storytelling is the oldest way people share what matters. We tell the real story of your food, your rooms and your people, because guests can tell the difference.')]
TEAM = [('Content', 'Photographers and videographers who shoot on location in your venue.', 'v', 'w55'), ('Social media', 'Account managers who run your channels day to day.', 'v', 'w12'),
        ('Paid and search', 'Specialists in Meta, Google, SEO and AI search.', 'v', 'w58'), ('Web', 'Designers and developers who build fast, bookable websites.', 'w', 'images/63517e139961b23b9915142b_Lombard-1.webp')]
team = ''.join('<div class="p-card x-r" style="--x-d:%.2fs"><div class="p-card-media">%s</div><em>0%d</em><h3>%s</h3><p>%s</p></div>' % (k * 0.08, video(pre, m, False) if kind == 'v' else '<img src="%s%s" alt="" loading="lazy"/>' % (pre, m), k + 1, e(t), e(d)) for k, (t, d, kind, m) in enumerate(TEAM))
ld = [dict(ORG, description='Digital marketing agency specialising in restaurants, hotels and bars.', email='hello@thewonder.group', telephone='+447775022514',
           address={"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"}, founder=[{"@type": "Person", "name": "Charles Morris"}, {"@type": "Person", "name": "Charlotte Giles"}],
           knowsAbout=['Restaurant marketing', 'Hotel marketing', 'Bar marketing', 'Hospitality social media', 'Food photography', 'Restaurant SEO', 'AI search visibility (GEO)'],
           parentOrganization={"@type": "Organization", "name": "The Wonder Group", "url": "https://www.thewonder.group/"}),
      crumb_ld([('', 'Home'), (path, 'About')]), {"@type": "AboutPage", "url": SITE + path, "about": {"@id": SITE + "#org"}}]
write(path + 'index.html', head(pre, 'About The Wonder Agency | Hospitality Marketing Specialists, London',
      'The Wonder Agency is a London digital marketing agency specialising in restaurants, hotels and bars, trusted by Michelin-starred restaurants, hotel groups and independents.', path, ld) + chrome_top(pre) +
      '<section class="p-ahero"><div class="p-aw" aria-hidden="true">' + wall + '</div><div class="p-ahero-in">' + crumbs(pre, [('', 'Home'), (None, 'About')]) +
      '<div class="x-label">About The Wonder Agency</div><h1>The hospitality marketing specialists</h1>'
      '<p class="p-lede">We’re a London digital marketing agency that specialises in restaurants, hotels and bars. One team runs content, social media, ads, search, websites and email, with one goal: more bookings.</p>'
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#know" class="x-link">What we know</a></div></div></section>' % pre +
      '<section class="p-stats">' + ''.join('<div class="x-r" style="--x-d:%.2fs"><b>%s</b><span>%s</span></div>' % (k * 0.08, n, e(l)) for k, (n, l) in enumerate(STATS)) + '</section>' +
      '<section class="p-sec"><div class="p-two"><p class="p-big x-r">Trusted by Michelin-starred restaurants, hotel groups and independents, from London to Paris.</p><div class="p-body x-r">'
      '<p>Founded by Charles Morris and Charlotte Giles, The Wonder Agency is part of The Wonder Group. Hospitality is where we’ve built our expertise, so we know what makes someone choose one restaurant over another, book a hotel for the weekend, or come back for a second visit.</p>'
      '<p>That depth is why our results are measured in bookings and revenue rather than likes. Hospitality is our specialism, not a limit: the same approach works for consumer brands who want the same standard.</p></div></div></section>' +
      '<section class="p-sec" id="know"><h2 class="p-h2 x-r">What we know that generalists don’t</h2><div class="p-inc">%s</div></section>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % ((k % 3) * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(KNOW)) +
      band(pre, 'w18', 'We built our own AI search tool.', 'Wonder Score checks whether ChatGPT, Gemini and Perplexity recommend your venue, and what to change so they do.') +
      '<section class="p-sec"><h2 class="p-h2 x-r">Results for our clients</h2><div class="p-res">%s</div></section>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><b>%s</b><p>%s</p></div>' % ((k % 2) * 0.08, e(n), e(d)) for k, (n, d) in enumerate(RESULTS)) +
      '<section class="p-sec"><h2 class="p-h2 x-r">What we believe</h2><div class="p-inc">%s</div></section>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % (k * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(BELIEFS)) +
      '<section class="p-sec"><h2 class="p-h2 x-r">One team, every channel</h2><div class="p-cards p-cards--4">%s</div></section>' % team +
      '<section class="p-sec"><h2 class="p-h2 x-r">Selected clients</h2><div class="p-logos">%s</div></section>' % logo_grid +
      end_cta(pre) + chrome_bottom(pre))

# ---------- free audit ----------
pre = '../'; path = 'free-audit/'
form = ('<div class="p-form" id="request"><form id="email-form" name="email-form" data-kind="audit">'
        '<label for="name">Your name</label><input type="text" id="name" name="name" maxlength="256" autocomplete="name" required/>'
        '<label for="email">Your email</label><input type="email" id="email" name="email" maxlength="256" autocomplete="email" required/>'
        '<label for="venue">Your venue or business</label><input type="text" id="venue" name="venue" maxlength="256" required/>'
        '<label for="link">Website or Instagram</label><input type="text" id="link" name="link" maxlength="256"/>'
        '<label for="field">Anything we should know? (optional)</label><textarea id="field" name="field" maxlength="5000" placeholder="What you’d like more of: bookings, covers, room nights, a quiet night filled…"></textarea>'
        '<label class="p-check"><input type="checkbox" id="checkbox" name="checkbox"/> <span>I’m happy for The Wonder Agency to contact me about my audit, as set out in our <a href="../privacy/">privacy policy</a>.</span></label>'
        '<input type="submit" value="Send my audit request" data-wait="Sending…"/></form>'
        '<div class="w-form-done">Thank you. Your audit request is in and we’ll be in touch.</div><div class="w-form-fail">Sorry, something went wrong. Please email hello@thewonder.group instead.</div></div>')
AUDIT = [('Social and content', 'What you post, how it looks, and whether anyone acts on it.'), ('Paid ads', 'Where the budget goes and what it brings back in bookings.'),
         ('Search and AI search', 'How you show up on Google, and whether AI assistants name you.'), ('Website and booking', 'How many people you lose between the menu and the booking button.')]
GET = [('A plain summary', 'What’s working, what isn’t and why, written for you rather than for marketers. No jargon and no 40-page deck.'),
       ('What we’d fix first', 'The few changes most likely to bring in more bookings, in the order we’d do them.'),
       ('A call, if you want one', 'We’ll talk it through and answer your questions. If you’d rather just read it, that’s fine too.')]
HOW = [('You ask', 'Tell us your name, your venue and a link to your website or Instagram. Two minutes.'),
       ('We look', 'We review your marketing from the outside, the way a guest finds you: social, ads, Google, AI search and your website.'),
       ('We report', 'We send you a plain summary and what we’d fix first.'),
       ('You decide', 'Use it yourself, ask us to do it, or do nothing at all. There’s no obligation.')]
AFAQ = [('Is it really free?', 'Yes. There’s no charge and no catch. It’s how most of our clients first got to know us.'),
        ('Will you try to sell me something?', 'We’ll tell you what we’d do, and if you’d like us to do it we’ll explain how. If not, you keep the audit and that’s the end of it.'),
        ('What do you need from me?', 'Just your venue and a link to your website or Instagram. We look at everything from the outside, like a guest would, so you don’t need to give us any logins.'),
        ('Can you look at our ad accounts and analytics too?', 'Yes, if you’d like a deeper look we can arrange read-only access afterwards. It isn’t needed for the audit.'),
        ('Do you only audit hospitality businesses?', 'Restaurants, hotels, bars and food and drink brands are what we know best, but we’re happy to take a look at other businesses too.'),
        ('We have several venues. Can you audit all of them?', 'Yes. Tell us about the group and we’ll look at each venue and how they work together.')]
PROOF = [('£3.2m → £4.6m', 'Annual revenue for a restaurant over three years.', 'work/restaurant-revenue-growth/'),
         ('+58%', 'Food and beverage revenue for a hotel in three months.', 'work/hotel-boost/'),
         ('+95%', 'Set lunch bookings at a Michelin-starred restaurant.', 'work/michelin-star-set-menu/')]
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Free audit')]), faq_ld(AFAQ),
      {"@type": "Offer", "name": "Free marketing audit", "price": "0", "priceCurrency": "GBP", "url": SITE + path, "seller": {"@id": SITE + "#org"},
       "description": "A free review of a restaurant, hotel or bar’s social media, ads, search, AI search and website, with what we’d fix first."}]
write(path + 'index.html', head(pre, 'Free Marketing Audit for Restaurants, Hotels & Bars | The Wonder Agency',
      'Get a free marketing audit for your restaurant, hotel or bar: social media, ads, Google, AI search and website. What’s working, what isn’t, and what we’d fix first. No charge, no obligation.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'Free audit')]) +
      '<div class="x-label">Free audit</div><h1>Get a free marketing audit for your venue</h1><p class="p-lede">Tell us about your venue. We’ll review your marketing from the outside, the way a guest finds you, and send you a plain account of what’s working, what isn’t, and what we’d fix first. No charge and no obligation.</p>'
      '<div class="p-btns"><a href="#request" class="x-nav-cta">Request your audit <i>→</i></a><a href="#look" class="x-link">What we look at</a></div></div></section>' +
      '<section class="p-sec" style="padding-top:0"><div class="p-two">' + form +
      '<div id="look"><h2 class="p-big" style="margin-bottom:1.6rem">What we look at</h2><ul class="p-direct">%s</ul></div></div></section>' % ''.join('<li><b>0%d</b>%s: <span style="color:#bdbdbd">%s</span></li>' % (k + 1, e(t), e(d)) for k, (t, d) in enumerate(AUDIT)) +
      '<section class="p-sec"><h2 class="p-h2 x-r">What you get</h2><div class="p-inc">%s</div></section>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % (k * 0.08, k + 1, e(a), e(b)) for k, (a, b) in enumerate(GET)) +
      '<section class="p-sec"><h2 class="p-h2 x-r">How it works</h2><div class="x-steps" style="margin-top:0">%s</div></section>' % ''.join('<div class="x-step x-r" style="--x-d:%.2fs"><span>Step %d</span><h3>%s</h3><p>%s</p></div>' % (k * 0.08, k + 1, e(a), e(b)) for k, (a, b) in enumerate(HOW)) +
      '<section class="p-sec"><h2 class="p-h2 x-r">What it can lead to</h2><div class="p-res p-res--3">%s</div><p class="x-r" style="margin-top:2rem"><a class="x-link" href="%swork/">See all our case studies</a></p></section>' % (
          ''.join('<a class="x-r p-res-link" style="--x-d:%.2fs" href="%s%s"><b>%s</b><p>%s</p></a>' % (k * 0.08, pre, u, e(a), e(b)) for k, (a, b, u) in enumerate(PROOF)), pre) +
      '<section class="p-sec"><div class="p-two"><p class="p-big x-r">Who it’s for</p><div class="p-body x-r"><p>Restaurants, hotels, bars and pubs, restaurant groups, and food and drink brands, from independents to Michelin-starred dining rooms and hotel groups. One venue or twenty.</p>'
      '<p>Hospitality is what we know best, but if you run another kind of business and want a fresh pair of eyes on your marketing, ask anyway.</p></div></div></section>' +
      '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(AFAQ) +
      '<section class="p-end"><h2 class="x-r">Ready when you are</h2><p class="x-r">It takes two minutes to request, and it’s yours to keep whatever you decide.</p><div class="p-btns x-r"><a href="#request" class="x-nav-cta">Request your audit <i>→</i></a><a href="mailto:hello@thewonder.group" class="x-link">Email us</a></div></section>' +
      chrome_bottom(pre, '<script src="%sjs/contact-form.js"></script>' % pre))

# ---------- contact ----------
pre = '../'; path = 'contact/'
cform = ('<div class="p-form"><form id="email-form" name="email-form" data-kind="contact">'
         '<label for="name">Your name</label><input type="text" id="name" name="name" maxlength="256" autocomplete="name" required/>'
         '<label for="email">Your email</label><input type="email" id="email" name="email" maxlength="256" autocomplete="email" required/>'
         '<label for="venue">Company (optional)</label><input type="text" id="venue" name="venue" maxlength="256" autocomplete="organization"/>'
         '<label for="topic">What’s it about?</label><select id="topic" name="topic"><option>Working together</option><option>Press</option><option>Careers</option><option>Partnerships</option><option>Something else</option></select>'
         '<label for="field">Your message</label><textarea id="field" name="field" maxlength="5000" required></textarea>'
         '<label class="p-check"><input type="checkbox" id="checkbox" name="checkbox"/> <span>I’m happy for The Wonder Agency to reply to me, as set out in our <a href="../privacy/">privacy policy</a>.</span></label>'
         '<input type="submit" value="Send message" data-wait="Sending…"/></form>'
         '<div class="w-form-done">Thank you. Your message is in and we’ll get back to you.</div><div class="w-form-fail">Sorry, something went wrong. Please email hello@thewonder.group instead.</div></div>')
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Contact')]), {"@type": "ContactPage", "url": SITE + path, "about": {"@id": SITE + "#org"}}]
write(path + 'index.html', head(pre, 'Contact The Wonder Agency | Hospitality Marketing Agency, London',
      'Get in touch with The Wonder Agency, a London hospitality marketing agency. Email hello@thewonder.group, call +44 777 502 2514, or send us a message.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'Contact')]) +
      '<div class="x-label">Contact</div><h1>Get in touch</h1><p class="p-lede">Questions, press, careers or a project in mind: send us a message or get in touch directly. If you’d like us to look at your marketing, <a href="%sfree-audit/" style="color:#5eadba">request a free audit</a> instead.</p></div></section>' % pre +
      '<section class="p-sec" style="padding-top:0"><div class="p-two">' + cform +
      '<div><h2 class="p-big" style="margin-bottom:1.2rem">Get in touch directly</h2><ul class="p-direct"><li><b>Email</b><a href="mailto:hello@thewonder.group">hello@thewonder.group</a></li><li><b>Phone</b><a href="tel:+447775022514">+44 777 502 2514</a></li>'
      '<li><b>Instagram</b><a href="https://www.instagram.com/the.wonder.list/" target="_blank" rel="noopener">@the.wonder.list</a></li><li><b>Based in</b><span style="font-family:Marcellus,sans-serif;font-size:1.6rem">London, working across the UK and internationally</span></li></ul>'
      '<div class="p-proof x-r" style="margin-top:3rem"><b style="font-size:clamp(2.2rem,4vw,3.4rem)">Free audit</b><p>Want to know what’s costing you bookings? We’ll review your marketing and tell you what we’d fix first. <a href="%sfree-audit/">Request your free audit</a></p></div>'
      '</div></div></section><div style="height:8rem"></div>' % pre + chrome_bottom(pre, '<script src="%sjs/contact-form.js"></script>' % pre))
# the form script: label general enquiries differently from audit requests
_js = os.path.join(ROOT, 'js', 'contact-form.js'); _t = open(_js, encoding='utf-8').read()
_a = "data.set('field', 'AUDIT REQUEST\\nVenue: ' + (data.get('venue') || '') + '\\nWebsite / Instagram: ' + (data.get('link') || '') + '\\n\\n' + (data.get('field') || ''));"
if _a in _t:
    _t = _t.replace(_a, "data.set('kind', form.dataset.kind || 'audit'); data.set('notes', data.get('field') || '');\n    if (form.dataset.kind === 'contact') data.set('field', 'ENQUIRY: ' + (data.get('topic') || '') + '\\nCompany: ' + (data.get('venue') || '') + '\\n\\n' + (data.get('field') || ''));\n    else " + _a)
    open(_js, 'w', encoding='utf-8').write(_t)

SBYSLUG = {x['slug']: x for x in SECTORS}
def media_el(pre, kind, src, cap):
    if kind == 'v': return video(pre, src, False)
    assert exists(src), src; return '<img src="%s%s" alt="%s" loading="lazy"/>' % (pre, src, e(cap))
def results_html(items):
    return '<div class="p-res">%s</div>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><b>%s</b><p>%s</p></div>' % ((k % 2) * 0.08, e(n), e(d)) for k, (n, d) in enumerate(items))
def service_cards(pre, lines):
    return '<div class="p-cards">%s</div>' % ''.join('<a class="p-card x-r" style="--x-d:%.2fs" href="%sservices/%s/"><div class="p-card-media">%s</div><em>0%d</em><h3>%s</h3><p>%s</p><em>Find out more →</em></a>' % (
        (k % 3) * 0.08, pre, slug, video(pre, BYSLUG[slug]['clip'], False), k + 1, e(BYSLUG[slug]['name']), e(line)) for k, (slug, line) in enumerate(lines))

# ---------- sector pages ----------
for x in SECTORS:
    pre = '../../'; path = 'who-we-work-with/%s/' % x['slug']
    items = [('', 'Home'), ('who-we-work-with/', 'Who we work with'), (None, x['name'])]
    ld = [ORG, {"@type": "Service", "name": 'Marketing for ' + x['name'].lower(), "serviceType": "Hospitality marketing", "description": x['desc'], "provider": {"@id": SITE + "#org"},
                "audience": {"@type": "Audience", "audienceType": x['name']}, "areaServed": ["United Kingdom", "International"], "url": SITE + path},
          crumb_ld([('', 'Home'), ('who-we-work-with/', 'Who we work with'), (path, x['name'])]), faq_ld(x['faqs'])]
    hero_media = video(pre, x['clip'])
    res = ('<section class="p-sec"><h2 class="p-h2 x-r">Results</h2>%s</section>' % results_html(x['results'])) if x['results'] else ''
    rel = ''.join('<a class="p-card x-r" href="%swho-we-work-with/%s/"><div class="p-card-media">%s</div><h3>%s</h3><p>%s</p><em>Find out more →</em></a>' % (pre, r, video(pre, SBYSLUG[r]['clip'], False), e(SBYSLUG[r]['name']), e(SBYSLUG[r]['card'])) for r in x['related'])
    write(path + 'index.html', head(pre, x['title'], x['desc'], path, ld) + chrome_top(pre) +
        '<section class="p-hero"><div>' + crumbs(pre, items) + '<div class="x-label">Who we work with</div><h1>%s</h1><p class="p-lede">%s</p>' % (e(x['h1']), e(x['lede'])) +
        '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#how" class="x-link">How we help</a></div></div><div class="p-hero-media">%s</div></section>' % (pre, hero_media) +
        '<section class="p-sec"><div class="p-two"><p class="p-big x-r">%s</p><div class="p-body x-r">%s</div></div></section>' % (e(x['big']), ''.join('<p>%s</p>' % e(t) for t in x['why'])) +
        band(pre, x['band'][0], x['band'][1]) +
        '<section class="p-sec" id="how"><h2 class="p-h2 x-r">How we help %s</h2>%s</section>' % (e(x['name'].lower()), service_cards(pre, x['help'])) +
        res + gallery(pre, x['gallery'], 'In pictures') +
        '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(x['faqs']) +
        '<section class="p-sec"><h2 class="p-h2 x-r">We also work with</h2><div class="p-cards p-cards--small">%s</div></section>' % rel +
        end_cta(pre) + chrome_bottom(pre))

# ---------- sectors overview ----------
pre = '../'; path = 'who-we-work-with/'
cards = ''.join('<a class="p-card x-r" style="--x-d:%.2fs" href="%s/"><div class="p-card-media">%s</div><em>0%d</em><h3>%s</h3><p>%s</p><em>Find out more →</em></a>' % ((k % 3) * 0.08, x['slug'], video(pre, x['clip'], False), k + 1, e(x['name']), e(x['card'])) for k, x in enumerate(SECTORS))
cards += '<a class="p-card x-r" href="../london/"><div class="p-card-media">%s</div><em>06</em><h3>London</h3><p>Our home city, and the most competitive hospitality market in the country.</p><em>Find out more →</em></a>' % media_el(pre, 'i', 'images/x/dining-room.webp', 'London dining room')
write(path + 'index.html', head(pre, 'Who We Work With | Restaurants, Hotels, Bars & Food Brands | The Wonder Agency',
      'We specialise in hospitality: restaurants, hotels, bars and pubs, restaurant groups and food and drink brands, in London, across the UK and internationally.', path,
      [ORG, crumb_ld([('', 'Home'), (path, 'Who we work with')])]) + chrome_top(pre) +
      '<section class="p-hero p-hero--text"><div>' + crumbs(pre, [('', 'Home'), (None, 'Who we work with')]) +
      '<div class="x-label">Who we work with</div><h1>Specialists in hospitality</h1><p class="p-lede">Restaurants, hotels, bars and pubs, restaurant groups and food and drink brands. From Michelin-starred dining rooms to neighbourhood independents, in London, across the UK and internationally.</p>'
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a></div></div></section>' % pre +
      '<section class="p-sec" style="padding-top:2rem"><div class="p-cards">%s</div></section>' % cards + end_cta(pre) + chrome_bottom(pre))

# ---------- London ----------
pre = '../'; path = 'london/'
LFAQ = [('Are you based in London?', 'Yes. The Wonder Agency is based in London, and most of our shoots happen across the city.'),
        ('Do you work outside London?', 'Yes. We work with venues across the UK, from the Kent coast to Oxford, and internationally, including Paris. Our content team travels.'),
        ('Do you know our neighbourhood?', 'We work across London, from Soho, Mayfair and Marylebone to the City, St John’s Wood and Wimbledon, so we know how guests choose in different parts of town.'),
        ('How do you help London venues stand out?', 'Content that looks like nowhere else, social and ads aimed at the right postcodes, and search and AI visibility for the neighbourhood searches guests actually make.')]
ld = [dict(ORG, areaServed=[{"@type": "City", "name": "London"}, {"@type": "Country", "name": "United Kingdom"}], address={"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"}),
      crumb_ld([('', 'Home'), ('who-we-work-with/', 'Who we work with'), (path, 'London')]), faq_ld(LFAQ)]
write(path + 'index.html', head(pre, 'Hospitality Marketing Agency London | Restaurants, Hotels & Bars | The Wonder Agency',
      'London hospitality marketing agency for restaurants, hotels and bars: content, social media, ads, SEO and AI search, websites and email. Shooting across the city, working UK-wide and internationally.', path, ld) + chrome_top(pre) +
      '<section class="p-hero"><div>' + crumbs(pre, [('', 'Home'), ('who-we-work-with/', 'Who we work with'), (None, 'London')]) +
      '<div class="x-label">London</div><h1>Hospitality marketing agency in London</h1><p class="p-lede">We’re a London digital marketing agency for restaurants, hotels and bars. We shoot across the city, know how its guests choose, and work across the UK and internationally.</p>'
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#how" class="x-link">How we help</a></div></div><div class="p-hero-media">%s</div></section>' % (pre, video(pre, 'w12')) +
      '<section class="p-sec"><div class="p-two"><p class="p-big x-r">London is the most competitive hospitality market in the country.</p><div class="p-body x-r">'
      '<p>New places open every week, guests have endless choice, and most of them decide on their phone: a reel, a Maps search for “best brunch in Soho”, a review, or a question to an AI assistant.</p>'
      '<p>Standing out takes content that looks like nowhere else, marketing aimed at the right neighbourhoods, and being the name that comes up when someone asks where to go. That’s what we do, from Soho and Mayfair to Marylebone, the City, St John’s Wood and Wimbledon.</p></div></div></section>' +
      band(pre, 'w66', 'From Soho to St John’s Wood.') +
      '<section class="p-sec" id="how"><h2 class="p-h2 x-r">How we help London venues</h2>%s</section>' % service_cards(pre, [(x['slug'], x['card']) for x in SERVICES]) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Results</h2>%s</section>' % results_html([('£3.2m → £4.6m', 'Annual revenue for a restaurant over three years.'), ('+95%', 'Mid-week set lunch bookings at a Michelin-starred restaurant within three months.')]) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(LFAQ) + end_cta(pre) + chrome_bottom(pre))

# ---------- Work: a short selection, case studies, logos ----------
pre = '../'; path = 'work/'
RES = [('£3.2m → £4.6m', 'Restaurant, three years. Annual revenue, with Instagram from 3,000 to 20,000+ followers and Google rating from 4.0 to 4.6. Every channel aligned: weekly shoots, daily social, paid, email and SEO.'),
       ('+58%', 'Hotel group, three months. Year-on-year food and beverage revenue, with room bookings up 26%, from a restaurant-first content strategy that made the hotel a destination for locals.'),
       ('+95%', 'Michelin-starred restaurant, three months. Mid-week set lunch bookings, after repositioning the lunch offer, a three-week paid push and a rebuilt booking journey.'),
       ('+18%', 'Three-restaurant group, Q4. Year-on-year revenue after a full digital overhaul: new sites, new photography and a new paid structure.')]
logos = re.findall(r'<span class="x-logo"><img src="([^"]+)"', open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read())
seen = []; [seen.append(l) for l in logos if l not in seen]
# spread the three Aqua logos across the grid and finish on Beeble
_aq = [l for l in seen if '/logos/aqua-' in l]; _bee = [l for l in seen if l.endswith('/logos/beeble.webp')]
seen = [l for l in seen if l not in _aq and l not in _bee]
for _k, _l in zip((3, 17, 31), _aq): seen.insert(min(_k, len(seen)), _l)
seen += _bee
CUTS = media4.load_cuts(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media4', 'cuts.txt'))
SELECT = ['w19', 'w68', 'ph-01', 'w24', 'w66', 'ph-02', 'w75', 'w20', 'ph-34', 'w58', 'w18', 'ph-36']
BYID = {c['id']: c for c in CUTS}
PCAP = dict(media4.PHOTOS)
lib = []
for sid in SELECT:
    if sid.startswith('w'): lib.append(('v', BYID[sid]))
    else: n = sid[3:]; lib.append(('p', dict(id=n, cap=PCAP[n], cat='photo')))
cells = ''
for kind, it in lib:
    if kind == 'v':
        land = it['orient'] == 'l'
        cells += ('<button type="button" class="p-lib-item%s" data-cat="%s video" data-kind="v" data-r="' + ('0.5625' if land else '1.7778') + '" data-full="%svideos/clips/%s-%s.mp4" data-poster="%simages/x/clip-%s.webp" data-cap="%s">'
                  '<video muted loop playsinline preload="none" poster="%simages/x/clip-%s.webp" data-src="%svideos/clips/%s-s.mp4" data-x-auto aria-hidden="true"></video>'
                  '<span class="p-lib-cap">%s</span><i class="p-lib-play" aria-hidden="true"></i><span class="sr-only">Play film: %s</span></button>') % (
            ' p-lib-land' if land else '', it['cat'], pre, it['id'], 'l' if it['big'] else 'm', pre, it['id'], e(it['cap']), pre, it['id'], pre, it['id'], e(it['cap']), e(it['cap']))
    else:
        from PIL import Image as _I
        iw, ih = _I.open(os.path.join(ROOT, 'images/x/ph-%s-t.webp' % it['id'])).size
        cells += ('<button type="button" class="p-lib-item p-lib-photo" data-cat="%s photo" data-kind="p" data-r="%.4f" data-full="%simages/x/ph-%s.webp" data-cap="%s">'
                  '<img src="%simages/x/ph-%s-t.webp" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"/><span class="p-lib-cap">%s</span></button>') % (it['cat'], ih / iw, pre, it['id'], e(it['cap']), pre, it['id'], e(it['cap']), iw, ih, e(it['cap']))
viewer = ('<div class="p-lb" id="p-lb" role="dialog" aria-modal="true" aria-label="Viewer" aria-hidden="true"><button type="button" class="p-lb-x" aria-label="Close">×</button>'
          '<button type="button" class="p-lb-nav p-lb-prev" aria-label="Previous">←</button><figure class="p-lb-stage"><div class="p-lb-media"></div><figcaption class="p-lb-cap"></figcaption></figure>'
          '<button type="button" class="p-lb-nav p-lb-next" aria-label="Next">→</button><span class="p-lb-count"></span></div>')
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Work')]),
      {"@type": "CollectionPage", "name": "Our work", "url": SITE + path, "about": "Food, drink and hospitality photography, video and results",
       "hasPart": [{"@type": "VideoObject", "name": it['cap'], "thumbnailUrl": SITE + 'images/x/clip-%s.webp' % it['id'], "contentUrl": SITE + 'videos/clips/%s-m.mp4' % it['id'], "uploadDate": "2026-10-13", "description": it['cap']} for kind, it in lib if kind == 'v']}, sites.ld(SITE), cases.ld(SITE)]
write(path + 'index.html', head(pre, 'Our Work | Hospitality Photography, Video, Websites & Results | The Wonder Agency',
      'Selected photography, video and websites for restaurants, hotels, bars and food and drink brands, plus seven case studies: £3.2m to £4.6m annual revenue, +58% hotel F&B revenue, +95% set lunch bookings and more.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'Work')]) +
      '<div class="x-label">Work</div><h1>Our work</h1><p class="p-lede">What our work has done for our clients’ bookings and revenue, followed by a selection of what we shoot in restaurants, kitchens, bars and hotels, and the websites we build.</p>' +
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#selected" class="x-link">See the content</a></div></div></section>' % pre +
      '<section class="p-sec" id="results" style="padding-top:0"><h2 class="p-h2 x-r">Case studies</h2>%s</section>' % cases.cards(pre) +
      '<section class="p-sec" id="selected"><h2 class="p-h2 x-r">Selected work</h2>'
      '<div class="p-lib" id="p-lib">%s</div></section>' % cells +
      sites.section(pre, 'Websites', 'Sites we’ve designed and built for restaurants, bars and the people who design them.', sid='websites') +
      '<section class="p-sec"><h2 class="p-h2 x-r">Selected clients</h2><div class="p-logos">%s</div></section>' % ''.join('<span class="p-logo"><img src="%s%s" alt="" loading="lazy"/></span>' % (pre, l) for l in seen) +
      end_cta(pre, 'Want content like this?') + viewer + chrome_bottom(pre, '<script src="%sjs/library.js"></script>' % pre))

# ---------- case study pages ----------
for c in cases.CASES:
    pre = '../../'; path = cases.url(c)
    ld = [ORG, crumb_ld([('', 'Home'), ('work/', 'Work'), (path, c['title'])]), cases.page_ld(SITE, c, SITE + '#org')]
    body = cases.page_body(pre, c).replace('{CRUMBS}', crumbs(pre, [('', 'Home'), ('work/', 'Work'), (None, c['title'])])).replace('{MEDIA}', cases.media_html(pre, c))
    write(path + 'index.html', head(pre, c['seo'] + ' | The Wonder Agency', c['short'], path, ld) + chrome_top(pre) + body + end_cta(pre) + chrome_bottom(pre))

# ---------- Wonder Score ----------
pre = '../'; path = 'wonder-score/'
WFAQ = [('Is Wonder Score free?', 'Yes, you can run a free scan at wonderscore.ai.'),
        ('Is it only for hospitality?', 'No. Wonder Score works for any kind of business. We built it to track AI visibility for our hospitality clients, and it works just as well elsewhere.'),
        ('How is it different from an SEO tool?', 'SEO tools measure where you rank on Google. Wonder Score measures whether AI assistants actually name you when people ask for a recommendation, which is a different question with a different answer.'),
        ('Can you improve our score for us?', 'Yes. That’s our SEO and AI search service: we fix what the scan finds and track the score month by month.')]
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Wonder Score')]), faq_ld(WFAQ),
      {"@type": "SoftwareApplication", "name": "Wonder Score", "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "url": "https://wonderscore.ai", "publisher": {"@id": SITE + "#org"}}]
PARTS = [('60%', 'Mention rate', 'How often AI assistants name you when asked the questions your guests ask. Questions that don’t mention you by name count double, because that’s where new guests come from.'),
         ('30%', 'Website health', 'Whether your website gives AI clear, readable, up-to-date information about who you are, where you are and what you offer.'),
         ('10%', 'Market position', 'How you compare with the competitors guests are choosing between.')]
write(path + 'index.html', head(pre, 'Wonder Score | Is Your Restaurant or Hotel Recommended by AI? | The Wonder Agency',
      'Wonder Score checks whether ChatGPT, Gemini and Perplexity recommend your venue, analyses your website and your competitors, and shows what to change to get recommended more.', path, ld) + chrome_top(pre) +
      '<section class="p-hero"><div>' + crumbs(pre, [('', 'Home'), (None, 'Wonder Score')]) +
      '<div class="x-label">Wonder Score</div><h1>Are you recommended by AI?</h1><p class="p-lede">More and more people ask ChatGPT, Gemini and Perplexity where to eat, drink and stay, and AI recommends just a handful of names. Wonder Score, our own tool, shows whether one of them is you.</p>'
      '<div class="p-btns"><a href="https://wonderscore.ai" target="_blank" rel="noopener" class="x-nav-cta">Check your Wonder Score <i>→</i></a><a href="#how" class="x-link">How it works</a></div></div>'
      '<div class="x-chat x-in" role="img" aria-label="Example: an AI assistant asked for the best restaurant for a special occasion in London recommends your restaurant first">'
      '<div class="x-chat-q">Best restaurant for a special occasion in London?</div><div class="x-chat-a"><span class="x-chat-who">AI assistant</span>Three places stand out, and the first is <strong>your restaurant</strong>.</div>'
      '<div class="x-chat-score"><b>86</b><span>Wonder Score</span></div></div></section>' +
      '<section class="p-sec"><div class="p-two"><p class="p-big x-r">When a guest asks an AI where to go, there are no ten blue links. There’s one answer.</p><div class="p-body x-r">'
      '<p>Search used to give people a page of results to choose from. AI assistants give a short answer with a few names in it, and most people go with it. If you’re not named, that guest never sees you.</p>'
      '<p>Wonder Score measures how visible you are in those answers, analyses your website and your competitors, and gives you a clear list of what to change to get recommended more. Then, if you want, we do the work for you.</p></div></div></section>' +
      '<section class="p-sec" id="how"><h2 class="p-h2 x-r">How the score works</h2><div class="p-res">%s</div></section>' % ''.join('<div class="x-r"><b>%s</b><h3 class="p-res-h">%s</h3><p>%s</p></div>' % (e(a), e(b), e(c)) for a, b, c in PARTS) +
      '<section class="p-sec"><h2 class="p-h2 x-r">From score to recommendations</h2><div class="x-steps" style="margin-top:0">%s</div></section>' % ''.join('<div class="x-step x-r"><span>Step %d</span><h3>%s</h3><p>%s</p></div>' % (k + 1, e(t), e(d)) for k, (t, d) in enumerate(
          [('Scan', 'Run a free scan at wonderscore.ai.'), ('See where you stand', 'Your score, how often AI names you, and how you compare with competitors.'), ('Fix it', 'A clear list of what to change on your website and across the web.'), ('Track it', 'Watch the score move as the changes take effect, or let us do the work.')])) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(WFAQ) +
      end_cta(pre, 'Check your Wonder Score', 'Run a free scan and see whether AI recommends your venue. Or get a free audit and we’ll look at your whole marketing.').replace('href="%sfree-audit/" class="x-nav-cta">Get a free audit' % pre, 'href="https://wonderscore.ai" target="_blank" rel="noopener" class="x-nav-cta">Check your score').replace('href="mailto:hello@thewonder.group" class="x-link">Email us', 'href="%sfree-audit/" class="x-link">Get a free audit' % pre) +
      chrome_bottom(pre))

# ---------- specialist pages (service x sector) ----------
from pages_content import COMBOS, PRICING, COMPARE
from articles_content import ARTICLES
def spec_list(pre, combos):
    return '<div class="p-spec">%s</div>' % ''.join('<a class="x-r" href="%s%s">%s<i>→</i></a>' % (pre, c['path'], e(c['short'])) for c in combos)
for c in COMBOS:
    pre = '../../../'; path = c['path']; s = BYSLUG[c['service']]; x = SBYSLUG.get(c['sector']) if c['sector'] else None
    if path.startswith('who-we-work-with/'):
        trail = [('', 'Home'), ('who-we-work-with/', 'Who we work with'), ('who-we-work-with/%s/' % x['slug'], x['name']), (path, c['short'])]
    else:
        trail = [('', 'Home'), ('services/', 'Services'), ('services/%s/' % s['slug'], s['name']), (path, c['short'])]
    aud = x['name'] if x else 'Restaurants, hotels and bars'
    ld = [ORG, {"@type": "Service", "name": c['h1'], "serviceType": s['name'], "description": c['desc'], "provider": {"@id": SITE + "#org"},
                "audience": {"@type": "Audience", "audienceType": aud}, "areaServed": ["United Kingdom", "International"], "url": SITE + path},
          crumb_ld(trail), faq_ld(c['faqs'])]
    inc = ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % ((k % 3) * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(c['inc']))
    proof = ('<section class="p-sec"><h2 class="p-h2 x-r">Results</h2><div class="p-proof x-r"><b>%s</b><p>%s <a href="%swork/">See our work</a></p></div></section>' % (e(c['proof'][0]), e(c['proof'][1]), pre)) if c['proof'] else ''
    if c['service'] == 'seo-ai-search':
        proof += '<section class="p-sec"><h2 class="p-h2 x-r">Are you recommended by AI?</h2><div class="p-proof x-r"><b>Wonder Score</b><p>Our own tool shows how often AI assistants recommend you against your competitors, and what to change. <a href="%swonder-score/">How Wonder Score works</a></p></div></section>' % pre
    links = [(pre + 'services/%s/' % s['slug'], s['name'], s['card'], s['clip'])]
    if x: links.append((pre + 'who-we-work-with/%s/' % x['slug'], 'Marketing for ' + x['name'].lower(), x['card'], x['clip']))
    others = [o for o in COMBOS if o is not c and (o['service'] == c['service'] or (x and o['sector'] == c['sector']))][:3 - len(links) + 1]
    links += [(pre + o['path'], o['short'], o['lede'], o['clip']) for o in others]
    rel = ''.join('<a class="p-card x-r" href="%s"><div class="p-card-media">%s</div><h3>%s</h3><p>%s</p><em>Find out more →</em></a>' % (u, video(pre, m, False), e(t), e(d)) for u, t, d, m in links[:3])
    write(path + 'index.html', head(pre, c['title'], c['desc'], path, ld) + chrome_top(pre) +
        '<section class="p-hero"><div>' + crumbs(pre, trail[:-1] + [(None, c['short'])]) + '<div class="x-label">%s</div><h1>%s</h1><p class="p-lede">%s</p>' % (e(s['name'] if not path.startswith('who') else 'Hotels'), e(c['h1']), e(c['lede'])) +
        '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#included" class="x-link">What’s included</a></div></div><div class="p-hero-media">%s</div></section>' % (pre, video(pre, c['clip'])) +
        '<section class="p-sec"><div class="p-two"><p class="p-big x-r">%s</p><div class="p-body x-r">%s</div></div></section>' % (e(c['big']), ''.join('<p>%s</p>' % e(t) for t in c['why'])) +
        band(pre, MEDIA[s['slug']]['band'][0], c.get('band_line') or MEDIA[s['slug']]['band'][1]) +
        '<section class="p-sec" id="included"><h2 class="p-h2 x-r">What’s included</h2><div class="p-inc">%s</div></section>' % inc +
        (sites.section(pre, 'Restaurant websites we’ve built', only=('restaurants',)) if c['service'] == 'website-design' else gallery(pre, (x['gallery'] if x and path.startswith('who') else MEDIA[s['slug']]['gallery']), 'In pictures')) +
        proof +
        '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(c['faqs']) +
        '<section class="p-sec"><h2 class="p-h2 x-r">Related</h2><div class="p-cards p-cards--small">%s</div></section>' % rel +
        end_cta(pre) + chrome_bottom(pre))

# ---------- pricing ----------
pre = '../'; path = 'pricing/'
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Pricing')]), faq_ld(PRICING['faqs'])]
write(path + 'index.html', head(pre, 'Hospitality Marketing Agency Pricing | What Affects the Cost | The Wonder Agency',
      'How much does a hospitality marketing agency cost? What affects the price of social media, content, ads, SEO, websites and email for restaurants, hotels and bars, and what to ask any agency.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'Pricing')]) +
      '<div class="x-label">Pricing</div><h1>What does a hospitality marketing agency cost?</h1><p class="p-lede">It depends on what you need, so we don’t sell fixed packages. Here’s what affects the cost, how agencies usually charge, and the questions worth asking before you sign with anyone, including us.</p>'
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit and quote <i>→</i></a></div></div></section>' % pre +
      band(pre, 'w12', 'You pay for what you need, and nothing else.', 'After the free audit we send a clear quote for exactly what we’d recommend.') +
      '<section class="p-sec"><h2 class="p-h2 x-r">What affects the cost</h2><div class="p-inc">%s</div></section>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % ((k % 3) * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(PRICING['drivers'])) +
      '<section class="p-sec"><h2 class="p-h2 x-r">How agencies charge</h2><div class="p-inc">%s</div></section>' % ''.join('<div class="x-r" style="--x-d:%.2fs"><span>0%d</span><h3>%s</h3><p>%s</p></div>' % (k * 0.08, k + 1, e(t), e(d)) for k, (t, d) in enumerate(PRICING['models'])) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Questions to ask any agency</h2><ol class="p-qs">%s</ol></section>' % ''.join('<li class="x-r">%s</li>' % e(q) for q in PRICING['questions']) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(PRICING['faqs']) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Still deciding?</h2><div class="p-spec"><a class="x-r" href="%sagency-vs-in-house/">Agency or in-house marketing?<i>→</i></a><a class="x-r" href="%sservices/">See all services<i>→</i></a><a class="x-r" href="%swork/">See our results<i>→</i></a></div></section>' % (pre, pre, pre) +
      end_cta(pre, 'Get a free audit and quote', 'Tell us about your venue. We’ll show you what we’d do first and send a clear quote, with no obligation.') + chrome_bottom(pre))

# ---------- agency vs in-house ----------
pre = '../'; path = 'agency-vs-in-house/'
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Agency vs in-house')]), faq_ld(COMPARE['faqs'])]
rows = ''.join('<tr class="x-r"><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (e(a), e(b), e(c)) for a, b, c in COMPARE['rows'])
write(path + 'index.html', head(pre, 'Marketing Agency vs In-House for Restaurants & Hotels | The Wonder Agency',
      'Should a restaurant, hotel or bar hire an in-house marketer or use an agency? An honest comparison of skills, content, cover, tools and cost, and when to do both.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'Agency vs in-house')]) +
      '<div class="x-label">Agency vs in-house</div><h1>Agency or in-house marketing?</h1><p class="p-lede">An honest comparison for restaurants, hotels and bars. Both can work. The right answer depends on what you need covered, and many venues end up doing both.</p>'
      '<div class="p-btns"><a href="%sfree-audit/" class="x-nav-cta">Get a free audit <i>→</i></a><a href="#compare" class="x-link">See the comparison</a></div></div></section>' % pre +
      '<section class="p-sec" id="compare" style="padding-top:2rem"><h2 class="p-h2 x-r">Side by side</h2><table class="p-cmp"><thead><tr><th></th><th scope="col">In-house marketer</th><th scope="col">Specialist agency</th></tr></thead><tbody>%s</tbody></table></section>' % rows +
      '<section class="p-sec"><div class="p-two"><p class="p-big x-r">The real choice isn’t a salary against a fee. It’s how much of the job gets done well.</p><div class="p-body x-r">'
      '<p>Hospitality marketing now covers photography, video, social media, paid ads, search, AI search, websites and email. That’s a lot to ask of one person, however good they are, and the gaps usually end up filled by freelancers, tools and the general manager’s evenings.</p>'
      '<p>An agency gives you a team that covers every channel and has seen what works across many venues. An in-house marketer gives you someone on site every day. If you can, the strongest setup is often both: someone in the building, and a specialist team behind them.</p></div></div></section>' +
      band(pre, 'w55', 'One team across every channel.') +
      '<section class="p-sec"><h2 class="p-h2 x-r">Questions</h2>%s</section>' % faq_html(COMPARE['faqs']) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Read next</h2><div class="p-spec"><a class="x-r" href="%spricing/">What an agency costs<i>→</i></a><a class="x-r" href="%sabout/">About The Wonder Agency<i>→</i></a><a class="x-r" href="%sservices/">Our services<i>→</i></a></div></section>' % (pre, pre, pre) +
      end_cta(pre) + chrome_bottom(pre))

# ---------- articles ----------
DATE = '2026-10-07'
def art_body(blocks):
    out = []; first = True
    for kind, v in blocks:
        if kind == 'p': out.append('<p%s>%s</p>' % (' class="p-art-first"' if first else '', e(v))); first = False
        elif kind == 'h': out.append('<h2>%s</h2>' % e(v))
        elif kind == 'q': out.append('<blockquote>%s</blockquote>' % e(v))
        elif kind == 'ul': out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % e(i) for i in v))
    return ''.join(out)
for k, a in enumerate(ARTICLES):
    pre = '../../'; path = 'insights/%s/' % a['slug']
    trail = [('', 'Home'), ('insights/', 'Insights'), (path, a['title'])]
    ld = [ORG, crumb_ld(trail), {"@type": "Article", "headline": a['title'], "description": a['desc'], "image": SITE + a['img'], "datePublished": DATE, "dateModified": DATE,
          "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"}, "mainEntityOfPage": SITE + path, "articleSection": a['tag'], "inLanguage": "en-GB"}]
    t, p, kind = a['cta']
    cta = end_cta(pre, t, p)
    if kind == 'score':
        cta = cta.replace('href="%sfree-audit/" class="x-nav-cta">Get a free audit' % pre, 'href="%swonder-score/" class="x-nav-cta">Check your Wonder Score' % pre).replace('href="mailto:hello@thewonder.group" class="x-link">Email us', 'href="%scontact/" class="x-link">Get a free audit' % pre)
    more = [o for o in ARTICLES if o is not a]
    morehtml = '<section class="p-sec"><h2 class="p-h2 x-r">Read next</h2><div class="x-news" style="grid-template-columns:repeat(2,1fr)">%s</div></section>' % ''.join(
        '<article class="x-post x-r"><a class="x-post-link" href="%sinsights/%s/"><div class="x-post-img"><img src="%s%s" alt="" loading="lazy"/></div><div class="x-label">%s</div><h3>%s</h3><p>%s</p></a></article>' % (pre, o['slug'], pre, o['img'], e(o['tag']), e(o['title']), e(o['ex'])) for o in more)
    write(path + 'index.html', head(pre, a['seo'], a['desc'], path, ld).replace('<meta property="og:type" content="website"/>', '<meta property="og:type" content="article"/>') + chrome_top(pre) +
        '<section class="p-art-hero">' + crumbs(pre, [('', 'Home'), ('insights/', 'Insights'), (None, a['tag'])]) +
        '<div class="x-label">%s</div><h1>%s</h1><div class="p-art-meta"><span>The Wonder Agency</span><span><time datetime="%s">7 October 2026</time></span><span>%d min read</span></div></section>' % (e(a['tag']), e(a['title']), DATE, a['mins']) +
        '<div class="p-art-media">%s</div>' % video(pre, a['clip']) +
        '<article class="p-art">%s</article>' % art_body(a['body']) +
        morehtml + cta + chrome_bottom(pre))

# ---------- Insights hub ----------
pre = '../'; path = 'insights/'
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Insights')]), {"@type": "Blog", "name": "The Wonder Agency Insights", "url": SITE + path,
      "blogPost": [{"@type": "BlogPosting", "headline": a['title'], "url": SITE + 'insights/%s/' % a['slug'], "datePublished": DATE} for a in ARTICLES]}]
posts = ''.join('<article class="x-post x-r" style="--x-d:%.2fs"><a class="x-post-link" href="%s/"><div class="x-post-img"><img src="%s%s" alt="" loading="lazy"/></div><div class="x-label">%s</div><h3>%s</h3><p>%s</p><span class="x-post-more">Read the article →</span></a></article>' % (k * 0.1, a['slug'], pre, a['img'], e(a['tag']), e(a['title']), e(a['ex'])) for k, a in enumerate(ARTICLES))
write(path + 'index.html', head(pre, 'Insights | Hospitality Marketing Articles & Guides | The Wonder Agency',
      'Articles and guides on restaurant, hotel and bar marketing: social media, ads, SEO, AI search and more, from The Wonder Agency.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'Insights')]) +
      '<div class="x-label">Insights</div><h1>Latest thinking</h1><p class="p-lede">Articles and guides on marketing restaurants, hotels and bars: what’s working now in social media, ads, search and AI search.</p></div></section>' +
      '<section class="p-sec" style="padding-top:0"><div class="x-news">%s</div></section>' % posts +
      '<section class="p-sec"><h2 class="p-h2 x-r">Guides</h2><div class="p-spec"><a class="x-r" href="../pricing/">What a hospitality marketing agency costs<i>→</i></a><a class="x-r" href="../agency-vs-in-house/">Agency or in-house marketing?<i>→</i></a><a class="x-r" href="../wonder-score/">Are you recommended by AI?<i>→</i></a></div></section>' +
      end_cta(pre) + chrome_bottom(pre))

# ---------- cross-links to specialist pages ----------
def inject(rel, html):
    p = os.path.join(ROOT, rel); t = open(p, encoding='utf-8').read()
    assert '<section class="p-end">' in t, rel
    open(p, 'w', encoding='utf-8').write(t.replace('<section class="p-end">', html + '<section class="p-end">', 1))
for s in SERVICES:
    cs = [c for c in COMBOS if c['service'] == s['slug'] and c['path'].startswith('services/')]
    if cs: inject('services/%s/index.html' % s['slug'], '<section class="p-sec"><h2 class="p-h2 x-r">Specialist pages</h2>%s</section>' % spec_list('../../', cs))
for x in SECTORS:
    cs = [c for c in COMBOS if c['sector'] == x['slug']]
    if cs: inject('who-we-work-with/%s/index.html' % x['slug'], '<section class="p-sec"><h2 class="p-h2 x-r">Specialist pages</h2>%s</section>' % spec_list('../../', cs))
inject('services/index.html', '<section class="p-sec"><h2 class="p-h2 x-r">Specialist services</h2>%s</section>' % spec_list('../', COMBOS) +
       '<section class="p-sec"><h2 class="p-h2 x-r">Choosing an agency</h2><div class="p-spec"><a class="x-r" href="../pricing/">What it costs<i>→</i></a><a class="x-r" href="../agency-vs-in-house/">Agency or in-house?<i>→</i></a><a class="x-r" href="../work/">Our results<i>→</i></a></div></section>')

# ---------- privacy policy ----------
pre = '../'; path = 'privacy/'
PRIV = [
 ('Who we are', ['The Wonder Agency is a trading name of C Plus C Ltd, part of The Wonder Group. We are the data controller for the personal information described in this policy.',
                 'If you have any questions about this policy or how we use your information, email us at <a href="mailto:hello@thewonder.group">hello@thewonder.group</a>.']),
 ('What we collect', ['When you ask for a free audit or contact us through this website, we collect the details you give us: your name, email address, the name of your venue or business, its website or social media link, and anything you choose to tell us in your message.',
                      'If you email or phone us, we keep a record of that correspondence.',
                      'We do not ask for, and ask you not to send us, sensitive information such as health details or payment card numbers through the website.']),
 ('How we use it', ['We use your information to:',
                    '<ul><li>review your marketing and send you your free audit;</li><li>reply to your enquiry and talk to you about working together;</li><li>keep a record of our conversations so we can pick up where we left off.</li></ul>',
                    'We will not add you to a marketing mailing list unless you ask us to, and we never sell your information.']),
 ('Our lawful basis', ['We process your information because you have asked us to do something for you (to send an audit or reply to your enquiry), and because we have a legitimate interest in responding to people who contact us about our services. Where you tick the box on our form, we also rely on your consent, which you can withdraw at any time by emailing us.']),
 ('Who we share it with', ['Form submissions are stored in Google Workspace (Google Sheets and Gmail), which Google provides to us as a data processor. Google may process data outside the UK; where it does, it uses safeguards approved under UK data protection law.',
                           'Within our team, only the people who need to see your enquiry can access it. We do not share your information with anyone else unless the law requires us to.']),
 ('How long we keep it', ['We keep enquiry and audit details for up to 24 months after our last contact with you, so we can follow up on the audit and keep a record of what we discussed. If you become a client, we keep the information we need for as long as we work together and for as long as the law requires afterwards. You can ask us to delete your details sooner.']),
 ('Cookies and analytics', ['This website does not use advertising or tracking cookies. Our fonts, images and videos are served from our own site, not from third-party services.',
                            'If we add privacy-friendly visitor statistics, they will count visits without using cookies or identifying you personally, and we will update this policy.',
                            'Links to other websites, such as wonderscore.ai or Instagram, are covered by those websites’ own privacy policies.']),
 ('Your rights', ['Under UK data protection law you have the right to ask for a copy of the information we hold about you, to have it corrected or deleted, to object to or restrict how we use it, and to withdraw your consent. To do any of these, email <a href="mailto:hello@thewonder.group">hello@thewonder.group</a>. We will reply within one month.',
                  'If you are unhappy with how we have handled your information, you can complain to the Information Commissioner’s Office at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a>. We would appreciate the chance to put things right first.']),
 ('Changes to this policy', ['We may update this policy from time to time. The latest version will always be on this page.']),
]
pbody = ''.join('<h2>%s</h2>%s' % (e(h), ''.join(x if x.startswith('<ul') else '<p>%s</p>' % x for x in paras)) for h, paras in PRIV)
ld = [ORG, crumb_ld([('', 'Home'), (path, 'Privacy policy')]), {"@type": "WebPage", "name": "Privacy policy", "url": SITE + path, "dateModified": "2026-10-13"}]
write(path + 'index.html', head(pre, 'Privacy Policy | The Wonder Agency', 'How The Wonder Agency collects, uses and protects the information you give us when you ask for a free audit or get in touch.', path, ld) + chrome_top(pre) +
      '<section class="p-art-hero">' + crumbs(pre, [('', 'Home'), (None, 'Privacy policy')]) +
      '<div class="x-label">Privacy</div><h1>Privacy policy</h1><div class="p-art-meta"><span>Last updated <time datetime="2026-10-13">13 October 2026</time></span></div></section>' +
      '<article class="p-art p-legal">%s</article><div style="height:7rem"></div>' % pbody + chrome_bottom(pre))

# ---------- 404 (served by GitHub Pages for any missing address, so links are root-absolute) ----------
nf = (head('/', 'Page not found | The Wonder Agency', 'This page could not be found.', '404/', [ORG]).replace('<meta name="description"', '<meta name="robots" content="noindex"/><meta name="description"') + chrome_top('/') +
      '<section class="p-hero p-hero--text"><div><div class="x-label">404</div><h1>This page has gone off the menu</h1><p class="p-lede">The page you were looking for has moved or no longer exists. Here are the places most people are heading.</p>'
      '<div class="p-btns"><a href="/" class="x-nav-cta">Back to the homepage <i>→</i></a><a href="/free-audit/" class="x-link">Get a free audit</a></div></div></section>'
      '<section class="p-sec" style="padding-top:0"><div class="p-spec"><a href="/services/">Our services<i>→</i></a><a href="/who-we-work-with/">Who we work with<i>→</i></a><a href="/work/">Our work<i>→</i></a><a href="/wonder-score/">AI search and Wonder Score<i>→</i></a><a href="/insights/">Insights<i>→</i></a><a href="/about/">About us<i>→</i></a></div></section>'
      '<div style="height:6rem"></div>' + chrome_bottom('/'))
open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(nf)

# ---------- homepage: shared nav, menu and footer ----------
hp = os.path.join(ROOT, 'index.html'); hh = open(hp, encoding='utf-8').read()
hh, n1 = re.subn(r'<header class="x-nav[^"]*" id="x-nav">.*?(?=<div class="x-grain")', lambda m: nav_html('', home=True), hh, count=1, flags=re.S)
n2 = 1
if 'js/mega.js' not in hh: hh = hh.replace('</body>', '<script src="js/mega.js"></script></body>', 1)
hh, n3 = re.subn(r'<footer class="x-footer">.*?</footer>', footer_html(''), hh, count=1, flags=re.S)
assert (n1, n2, n3) == (1, 1, 1), (n1, n2, n3)
for a in ARTICLES:
    pat = r'<article class="x-post x-r" style="--x-d:([\d.]+)s"><div class="x-post-img">(.*?)</div><div class="x-label">(.*?)</div><h3>(.*?)</h3><p>(.*?)</p><span class="x-post-soon">Article coming soon</span></article>'
    hh, n = re.subn(pat, lambda m: '<article class="x-post x-r" style="--x-d:%ss"><a class="x-post-link" href="insights/%s/"><div class="x-post-img">%s</div><div class="x-label">%s</div><h3>%s</h3><p>%s</p><span class="x-post-more">Read the article →</span></a></article>' % (m.group(1), a['slug'], m.group(2), m.group(3), m.group(4), m.group(5)), hh, count=1, flags=re.S)
    assert n == 1, a['slug']
open(hp, 'w', encoding='utf-8').write(hh)

print('pages written')
