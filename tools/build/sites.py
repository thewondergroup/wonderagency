# Websites we've built: browser-framed screenshots that scroll on hover, with the phone view alongside.
# Images live in scratchpad/sites-img (site-<key>.webp full page at 960 wide, site-<key>-m.webp phone).
# Captions describe the venue; the address bar shows the real domain and the card links to the live site.
from html import escape as e
from PIL import Image
import os

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sites-img')
SITES = [
    # key, live url, domain shown, what it is, what the site does, sector
    ('zahter', 'https://www.zahter.co.uk/', 'zahter.co.uk', 'Turkish restaurant, Carnaby', 'Booking, menus, gifts and private hire', 'restaurants'),
    ('brix', 'https://brixldn.com/', 'brixldn.com', 'Restaurant and music venue, London Bridge', 'Booking, private hire, events and membership', 'restaurants'),
    ('clio', 'https://cliorestaurant.co.uk/', 'cliorestaurant.co.uk', 'Modern Greek restaurant, Marylebone', 'Reservations, menus and private dining', 'restaurants'),
    ('notto', 'https://www.nottopasta.com/', 'nottopasta.com', 'Fresh pasta bars across London', 'Booking, online ordering, catering and loyalty', 'restaurants'),
    ('kokin', 'https://kokin.co.uk/', 'kokin.co.uk', 'Japanese izakaya, Stratford', 'Reservations, menus, events and brunch', 'restaurants'),
    ('thirst-soho', 'https://thirstbar.com/', 'thirstbar.com', 'Late-night cocktail bars, Soho and Oxford', 'Two venues, one site, with booking for each', 'bars'),
    ('atelier-wren', 'https://atelierwren.com/', 'atelierwren.com', 'Hospitality interior design studio', 'Projects, studio and services', 'design'),
]

def available():
    return [s for s in SITES if os.path.exists(os.path.join(IMG, 'site-%s.webp' % s[0]))]

def card(pre, s, k):
    key, url, dom, what, does, _ = s
    w, h = Image.open(os.path.join(IMG, 'site-%s.webp' % key)).size
    frame = w * 10 / 16
    y = -(1 - frame / h) * 100 if h > frame + 4 else 0
    t = max(2.5, min(9, (h - frame) / 420))
    return ('<a class="p-site x-r%s" style="--x-d:%.2fs;--y:%.2f%%;--t:%.1fs" href="%s" target="_blank" rel="noopener">'
            '<div class="p-site-shot"><div class="p-site-frame"><div class="p-site-bar" aria-hidden="true"><i></i><i></i><i></i><span>%s</span></div>'
            '<div class="p-site-scr"><img src="%simages/x/sites/site-%s.webp" alt="Website we built: %s" width="%d" height="%d" loading="lazy" decoding="async"/></div></div>'
            '<div class="p-site-phone" aria-hidden="true"><img src="%simages/x/sites/site-%s-m.webp" alt="" width="360" height="779" loading="lazy" decoding="async"/></div></div>'
            '<div class="p-site-meta"><div><h3>%s</h3><p>%s</p></div><em>Visit the site <i>↗</i></em></div></a>') % (
        ' p-site--scroll' if y else '', (k % 2) * 0.1, y, t, url, e(dom), pre, key, e(what), w, h, pre, key, e(what), e(does))

def section(pre, title='Websites we’ve built', lede=None, only=None, sid='sites'):
    items = [s for s in available() if not only or s[5] in only]
    if not items: return ''
    intro = ('<p class="p-sites-lede x-r">%s</p>' % e(lede)) if lede else ''
    return ('<section class="p-sec" id="%s"><h2 class="p-h2 x-r">%s</h2>%s<div class="p-sites">%s</div></section>' % (
        sid, title, intro, ''.join(card(pre, s, k) for k, s in enumerate(items))))

def ld(site):
    return {"@type": "ItemList", "name": "Websites built by The Wonder Agency",
            "itemListElement": [{"@type": "ListItem", "position": k + 1, "item": {"@type": "WebSite", "url": s[1], "description": s[3],
                                 "image": site + 'images/x/sites/site-%s-m.webp' % s[0], "creator": {"@id": site + "#org"}}} for k, s in enumerate(available())]}
