# News section: /news/ hub, one page per story, latest-three strips on the homepage and Insights hub, menu and footer links.
# Images: assets/news/* -> images/x/news/<name>.webp (hero 16:9, card 4:3) and website screenshots for launch posts.
# Client names are allowed here (news is the one place they belong), so names.py skips news pages and anything between <!--names-ok--> markers.
import os, sys, re, json, html as H
from datetime import date
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from news_content import NEWS, SITE_NEWS
import sites

ROOT = sys.argv[1]; e = H.escape
SITE = 'https://thewonderagency.co/'
B = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(B, 'assets', 'news'); OUT = os.path.join(ROOT, 'images', 'x', 'news'); os.makedirs(OUT, exist_ok=True)

# ---- borrow the shared chrome from pages.py without re-running it ----
src = open(os.path.join(B, 'pages.py'), encoding='utf-8').read()
chrome = src.split('# ---------- service pages ----------')[0]
g = {'__name__': 'chrome', 'sys': sys, '__file__': os.path.join(B, 'pages.py')}
sys.argv = [sys.argv[0], ROOT]
exec(compile(chrome, 'pages.py', 'exec'), g)
head, chrome_top, chrome_bottom, crumbs, crumb_ld, end_cta, ORG = (g[k] for k in ('head', 'chrome_top', 'chrome_bottom', 'crumbs', 'crumb_ld', 'end_cta', 'ORG'))

def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(text)

def fmt(d):
    y, m, dd = map(int, d.split('-')); return date(y, m, dd).strftime('%-d %B %Y')

def crop(im, ratio):
    w, h = im.size
    if w / h > ratio: nw = int(h * ratio); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = max(0, int((h - nh) * 0.1)); return im.crop((0, y, w, y + nh))   # favour the upper part (signage, faces)

def prep(name, fit):
    """Make hero + card images; returns (hero_rel, card_rel, w, h)."""
    stem = os.path.splitext(name)[0]
    hero, card = 'images/x/news/%s.webp' % stem, 'images/x/news/%s-c.webp' % stem
    im = Image.open(os.path.join(SRC, name)).convert('RGB')
    if fit == 'contain':
        im.save(os.path.join(ROOT, hero), 'WEBP', quality=86); im.save(os.path.join(ROOT, card), 'WEBP', quality=86); return hero, card, im.size[0], im.size[1]
    h = crop(im, 16 / 9); h.thumbnail((1800, 1800)); h.save(os.path.join(ROOT, hero), 'WEBP', quality=82)
    c = crop(im, 4 / 3); c.thumbnail((1000, 1000)); c.save(os.path.join(ROOT, card), 'WEBP', quality=80)
    return hero, card, h.size[0], h.size[1]

# ---- assemble the full list: stories, then website launches ----
posts = []
for n in NEWS:
    hero, card, w, h = prep(n['img'], n.get('fit', 'cover'))
    posts.append(dict(n, hero=hero, card=card, w=w, h=h))
for s in sites.available():
    key, url, dom, what, does, _ = s
    if key not in SITE_NEWS: continue
    title, body = SITE_NEWS[key]
    shot = os.path.join(sites.IMG, 'site-%s.webp' % key)
    im = Image.open(shot).convert('RGB'); w0, h0 = im.size
    hero = im.crop((0, 0, w0, int(w0 * 9 / 16))); hero.thumbnail((1800, 1800)); hero.save(os.path.join(OUT, 'site-%s.webp' % key), 'WEBP', quality=82)
    card = im.crop((0, 0, w0, int(w0 * 3 / 4))); card.thumbnail((1000, 1000)); card.save(os.path.join(OUT, 'site-%s-c.webp' % key), 'WEBP', quality=80)
    posts.append(dict(slug='new-website-%s' % key.replace('-soho', ''), date='2026-10-17', label='Website launch', title=title, ex='%s. %s.' % (what, does),
                      hero='images/x/news/site-%s.webp' % key, card='images/x/news/site-%s-c.webp' % key, w=hero.size[0], h=hero.size[1], fit='cover',
                      img_alt='The new %s website' % dom, body=body, source=None, client=(dom, url),
                      credit='Designed and built by The Wonder Agency.', service='services/website-design/'))

def card_html(pre, p, k=0):
    return ('<article class="x-post x-r" style="--x-d:%.2fs"><a class="x-post-link" href="%snews/%s/"><div class="x-post-img%s"><img src="%s%s" alt="" loading="lazy" decoding="async"/></div>'
            '<div class="x-label">%s</div><h3>%s</h3><p>%s</p><span class="x-post-more">Read more →</span></a></article>') % (
        (k % 3) * 0.1, pre, p['slug'], ' p-nw-contain' if p.get('fit') == 'contain' else '', pre, p['card'], e(p['label']), e(p['title']), e(p['ex']))

# ---- post pages ----
for k, p in enumerate(posts):
    pre = '../../'; path = 'news/%s/' % p['slug']
    trail = [('', 'Home'), ('news/', 'News'), (path, p['title'])]
    ld = [ORG, crumb_ld(trail), {"@type": "NewsArticle", "headline": p['title'], "description": p['ex'], "image": SITE + p['hero'], "datePublished": p['date'], "dateModified": p['date'],
          "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"}, "mainEntityOfPage": SITE + path, "articleSection": p['label'], "inLanguage": "en-GB"}]
    if p['client']: ld[2]['about'] = {"@type": "Organization", "name": p['client'][0], "url": p['client'][1]}
    if p['source']: ld[2]['citation'] = {"@type": "CreativeWork", "name": p['source'][0], "url": p['source'][1]}
    body = ''.join('<p%s>%s</p>' % (' class="p-art-first"' if i == 0 else '', e(x)) for i, x in enumerate(p['body']))
    links = ''
    if p['source']: links += '<a class="p-nw-link" href="%s" target="_blank" rel="noopener">Read the piece at %s<i>↗</i></a>' % (p['source'][1], e(p['source'][0]))
    if p['client']: links += '<a class="p-nw-link" href="%s" target="_blank" rel="noopener">Visit %s<i>↗</i></a>' % (p['client'][1], e(p['client'][0]))
    credit = '<aside class="p-nw-credit x-r"><div class="x-label">Our part</div><p>%s</p><a href="%s%s" class="x-link">More about this →</a></aside>' % (e(p['credit']), pre, p['service'])
    others = [o for o in posts if o is not p][:3]
    more = '<section class="p-sec"><h2 class="p-h2 x-r">More news</h2><div class="x-news">%s</div><p class="p-nw-all"><a href="%snews/" class="x-link">All news →</a></p></section>' % (''.join(card_html(pre, o, i) for i, o in enumerate(others)), pre)
    title = p['title'] + ' | The Wonder Agency'
    desc = p['ex'] if len(p['ex']) <= 160 else p['ex'][:157].rsplit(' ', 1)[0] + '…'
    write(path + 'index.html', head(pre, title, desc, path, ld).replace('<meta property="og:type" content="website"/>', '<meta property="og:type" content="article"/>').replace('images/x/og.jpg"', p['hero'] + '"') + chrome_top(pre) +
          '<section class="p-art-hero">' + crumbs(pre, [('', 'Home'), ('news/', 'News'), (None, p['label'])]) +
          '<div class="x-label">%s</div><h1>%s</h1><div class="p-art-meta"><span>The Wonder Agency</span><span><time datetime="%s">%s</time></span></div></section>' % (e(p['label']), e(p['title']), p['date'], fmt(p['date'])) +
          '<div class="p-art-media%s"><img src="%s%s" alt="%s" width="%d" height="%d" fetchpriority="high" decoding="async"/></div>' % (' p-nw-contain' if p.get('fit') == 'contain' else '', pre, p['hero'], e(p.get('img_alt', '')), p['w'], p['h']) +
          '<article class="p-art">%s<div class="p-nw-links">%s</div></article>%s' % (body, links, credit) +
          more + end_cta(pre) + chrome_bottom(pre))

# ---- hub ----
pre = '../'; path = 'news/'
ld = [ORG, crumb_ld([('', 'Home'), (path, 'News')]), {"@type": "CollectionPage", "name": "News from The Wonder Agency", "url": SITE + path,
      "hasPart": [{"@type": "NewsArticle", "headline": p['title'], "url": SITE + 'news/%s/' % p['slug'], "datePublished": p['date']} for p in posts]}]
write(path + 'index.html', head(pre, 'News | Openings, Launches and Press | The Wonder Agency',
      'News from the restaurants, hotels, bars and brands we work with: openings, new menus, websites, awards and press, plus what we have been making.', path, ld) + chrome_top(pre) +
      '<section class="p-hero p-hero--text" style="min-height:0"><div>' + crumbs(pre, [('', 'Home'), (None, 'News')]) +
      '<div class="x-label">News</div><h1>What’s happening</h1><p class="p-lede">Openings, launches, reviews and press from the places we work with, and the things we have been making for them.</p></div></section>' +
      '<section class="p-sec" style="padding-top:0"><div class="x-news">%s</div></section>' % ''.join(card_html(pre, p, k) for k, p in enumerate(posts)) +
      '<section class="p-sec"><h2 class="p-h2 x-r">Longer reads</h2><div class="p-spec"><a class="x-r" href="../insights/">Articles and guides<i>→</i></a><a class="x-r" href="../work/">Case studies<i>→</i></a><a class="x-r" href="../wonder-score/">Are you recommended by AI?<i>→</i></a></div></section>' +
      end_cta(pre) + chrome_bottom(pre))

# ---- strips: homepage (after Latest thinking) and Insights hub ----
def strip(pre, n=3, wrap=True):
    inner = ('<div class="p-ns-head"><div><div class="x-label">News</div><h2 class="p-ns-h">From the places we work with</h2></div><a href="%snews/" class="x-link">All news →</a></div>'
             '<div class="x-news">%s</div>') % (pre, ''.join(card_html(pre, p, k) for k, p in enumerate(posts[:n])))
    return '<!--names-ok--><section class="x-section p-newsstrip" aria-label="Client news">%s</section><!--/names-ok-->' % (('<div class="x-wrap">%s</div>' % inner) if wrap else inner)

hp = os.path.join(ROOT, 'index.html'); hh = open(hp, encoding='utf-8').read()
i = hh.find('<section id="News"'); j = hh.find('</section>', i) + len('</section>')
assert i > 0 and '<!--names-ok-->' not in hh
hh = hh[:j] + strip('') + hh[j:]
open(hp, 'w', encoding='utf-8').write(hh)

ip = os.path.join(ROOT, 'insights', 'index.html'); ih = open(ip, encoding='utf-8').read()
ih = ih.replace('<section class="p-sec"><h2 class="p-h2 x-r">Guides</h2>', strip('../', wrap=False).replace('x-section p-newsstrip', 'p-sec p-newsstrip') + '<section class="p-sec"><h2 class="p-h2 x-r">Guides</h2>', 1)
open(ip, 'w', encoding='utf-8').write(ih)

# ---- footer + mobile menu links on every page ----
n = 0
for d, _, fs in os.walk(ROOT):
    if 'index.html' not in fs and d != ROOT: continue
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); t = open(p, encoding='utf-8').read(); o = t
        t = re.sub(r'(<li><a href="([^"]*)insights/">Insights</a></li>)', lambda m: m.group(1) + '<li><a href="%snews/">News</a></li>' % m.group(2), t, count=1)
        t = re.sub(r'(<div class="x-mi" style="--i:4"><a class="x-mi-t" href="([^"]*)insights/">Insights<span class="x-arr">→</span></a></div>)',
                   lambda m: m.group(1) + '<div class="x-mi" style="--i:4"><a class="x-mi-t" href="%snews/">News<span class="x-arr">→</span></a></div>' % m.group(2), t, count=1)
        if t != o: open(p, 'w', encoding='utf-8').write(t); n += 1
print('news: %d posts, links added on %d pages' % (len(posts), n))
