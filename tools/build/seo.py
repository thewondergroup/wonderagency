# SEO and AI search files, favicon set, and site-wide head tags. Runs after pages.py.
import os, re, sys, html, datetime
from PIL import Image, ImageDraw, ImageFont

R = sys.argv[1]
SITE = 'https://thewonderagency.co/'
TODAY = datetime.date.today().isoformat()
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- favicon: the gold W mark on black ----------
import shutil
MARK = Image.open(os.path.join(HERE, 'assets', 'w-mark.png')).convert('RGBA')
def icon(size, radius_ratio=0.0, pad=0.16):
    s = size * 4
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * radius_ratio), fill=(0, 0, 0, 255))
    inner = int(s * (1 - 2 * pad)); w = inner; h = round(MARK.height * inner / MARK.width)
    mk = MARK.resize((w, h), Image.LANCZOS)
    im.alpha_composite(mk, ((s - w) // 2, (s - h) // 2 + int(s * 0.02)))
    return im.resize((size, size), Image.LANCZOS)
X = os.path.join(R, 'images', 'x')
icon(32, 0.18, 0.08).save(os.path.join(X, 'icon-32.png'))
icon(180, 0, 0.16).save(os.path.join(X, 'icon-180.png'))
icon(192, 0.2, 0.16).save(os.path.join(X, 'icon-192.png'))
icon(512, 0, 0.16).save(os.path.join(X, 'icon-512.png'))
icon(256, 0.18, 0.08).save(os.path.join(R, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
shutil.copy(os.path.join(HERE, 'assets', 'w-mark-nav.png'), os.path.join(X, 'w-mark.png'))
open(os.path.join(R, 'site.webmanifest'), 'w').write(
    '{"name":"The Wonder Agency","short_name":"Wonder Agency","icons":[{"src":"/images/x/icon-192.png","sizes":"192x192","type":"image/png"},'
    '{"src":"/images/x/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#000000","background_color":"#000000","display":"browser"}')

# optional analytics: paste a snippet into build3/analytics.html to switch it on everywhere
ap = os.path.join(HERE, 'analytics.html')
ANALYTICS = open(ap).read().strip() if os.path.exists(ap) else ''

# ---------- per-page head tags ----------
pages = []
for d, _, fs in os.walk(R):
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); rel = os.path.relpath(p, R).replace(os.sep, '/')
        t = open(p, encoding='utf-8').read(); o = t
        depth = 0 if rel == '404.html' else rel.count('/')
        pre = '/' if rel == '404.html' else '../' * depth
        # favicons: drop the old Wonder List icons, add ours
        t = re.sub(r'<link[^>]*(?:shortcut icon|apple-touch-icon|rel="icon"|rel="manifest")[^>]*/?>', '', t)
        tags = ('<link rel="icon" href="%sfavicon.ico" sizes="any"/><link rel="icon" type="image/png" sizes="32x32" href="%simages/x/icon-32.png"/>'
                '<link rel="apple-touch-icon" href="%simages/x/icon-180.png"/><link rel="manifest" href="%ssite.webmanifest"/>') % (pre, pre, pre, pre)
        if 'og:locale' not in t: tags += '<meta property="og:locale" content="en_GB"/>'
        if 'name="robots"' not in t and rel != '404.html': tags += '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>'
        t = t.replace('</head>', tags + (ANALYTICS if ANALYTICS else '') + '</head>', 1)
        t = re.sub(r'(<a href="[^"]*" class="x-nav-brand hover-cursor">)(The Wonder Agency</a>)', lambda m: m.group(1) + '<img class="x-nav-mark" src="%simages/x/w-mark.png" alt="" width="51" height="30"/>' % pre + m.group(2), t, count=1)
        # homepage form: link the consent line to the policy
        t = t.replace('>Accept our privacy policy</span>', '>Accept our <a href="privacy/" style="color:inherit;text-decoration:underline">privacy policy</a></span>')
        if t != o: open(p, 'w', encoding='utf-8').write(t)
        if rel == '404.html': continue
        url = SITE + (rel[:-len('index.html')] if rel.endswith('index.html') else rel)
        title = html.unescape((re.search(r'<title>(.*?)</title>', t, re.S) or [None, ''])[1])
        dm = re.search(r'<meta (?:name="description" content="([^"]*)"|content="([^"]*)" name="description")', t)
        desc = html.unescape((dm.group(1) or dm.group(2)) if dm else '')
        pages.append((url, title, desc))

# ---------- sitemap.xml ----------
def prio(u):
    path = u[len(SITE):]
    if path == '': return '1.0'
    if path.count('/') == 1: return '0.9'
    return '0.8' if not path.startswith(('privacy', 'insights/')) else ('0.7' if path.startswith('insights/') else '0.3')
pages.sort(key=lambda x: (x[0] != SITE, x[0]))
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, _, _ in pages:
    sm.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (html.escape(u), TODAY, prio(u)))
sm.append('</urlset>')
open(os.path.join(R, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')

# ---------- robots.txt: open to search engines and AI assistants ----------
bots = ['Googlebot', 'Bingbot', 'Applebot', 'DuckDuckBot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
        'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'CCBot', 'meta-externalagent', 'Amazonbot', 'MistralAI-User']
rb = ['# The Wonder Agency: search engines and AI assistants are welcome to read and recommend this site.', '']
rb += ['User-agent: %s\nAllow: /\n' % b for b in bots]
rb += ['User-agent: *', 'Allow: /', 'Disallow: /404.html', 'Disallow: /tools/', '', 'Sitemap: %ssitemap.xml' % SITE]
open(os.path.join(R, 'robots.txt'), 'w').write('\n'.join(rb) + '\n')

# ---------- llms.txt: a plain summary for AI assistants ----------
def sect(prefix, exclude=()):
    return [(u, t, d) for u, t, d in pages if u[len(SITE):].startswith(prefix) and u[len(SITE):] not in exclude]
def clean(t): return t.split(' | ')[0]
L = ['# The Wonder Agency', '',
     '> The Wonder Agency is a London digital marketing agency that specialises in hospitality: restaurants, hotels, bars and pubs, restaurant groups, and food and drink brands. '
     'One team runs content creation (photography and video), social media management, paid advertising (Meta and Google), SEO and AI search, influencer marketing, website design and email marketing, '
     'with one goal: more bookings. It works across London, the UK and internationally, and built its own AI search visibility tool, Wonder Score (wonderscore.ai).', '',
     'Key facts:',
     '- Based in London, United Kingdom; part of The Wonder Group. Founded by Charles Morris and Charlotte Giles.',
     '- Specialism: hospitality and lifestyle brands, from Michelin-starred restaurants to hotel groups and independents.',
     '- Results: one restaurant grew annual revenue from £3.2m to £4.6m over three years; a hotel group grew year-on-year food and beverage revenue by 58% in three months, with room bookings up 26%; a Michelin-starred restaurant grew mid-week set lunch bookings by 95% in three months; a three-restaurant group grew Q4 revenue by 18%; a new Saturday brunch in a historic City venue with no weekend trade reached 220 to 250 covers every Saturday within six weeks; the relaunch of Phil Howard’s The Square cookbooks, website and campaign by the agency, sold out within 48 hours; Longboard’s first private coffee auction, with website, content, marketing, lot artwork and boxes by the agency, achieved the highest average lot price of any coffee auction in the world ($4,688.82 per kg).',
     '- Offers a free marketing audit for restaurants, hotels and bars: ' + SITE + 'contact/',
     '- Contact: hello@thewonder.group, +44 777 502 2514', '']
groups = [('Services', 'services/', ()), ('Who we work with', 'who-we-work-with/', ()), ('London', 'london/', ()), ('Work and results', 'work/', ()), ('AI search', 'wonder-score/', ()),
          ('Insights', 'insights/', ()), ('Guides', 'pricing/', ()), ('', 'agency-vs-in-house/', ()), ('About', 'about/', ()), ('Free audit', 'contact/', ())]
for name, pref, ex in groups:
    rows = sect(pref, ex)
    if not rows: continue
    if name: L.append('## ' + name)
    for u, t, d in rows: L.append('- [%s](%s): %s' % (clean(t), u, d))
    L.append('')
L += ['## Optional', '- [Privacy policy](%sprivacy/)' % SITE, '- [Wonder Score](https://wonderscore.ai): check whether AI assistants recommend your business', '']
open(os.path.join(R, 'llms.txt'), 'w').write('\n'.join(x for x in L) .replace('\n\n\n', '\n\n'))
print('seo: %d pages in sitemap, favicon, robots.txt, llms.txt%s' % (len(pages), ', analytics on' if ANALYTICS else ''))
