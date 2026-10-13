# Client names live only in the logos. Replace them in video labels, captions and image descriptions, then check none are left.
import os, re, sys
R = sys.argv[1]
NAMES = ['Temper', 'Azzurra', 'Paradiso', 'Notto', 'NOTTO', 'Beeble', 'Connaught', 'Lombard', 'Gallivant', 'Delamina', 'Harwood', 'Aikens', 'Kitchen W8',
         'Fallow', 'Elystan', 'Cubitt', 'Barley Mow', 'Dorchester', 'Valrhona', 'Artfarm', 'Wolfgang', 'Maroush', 'Cent Anni', 'Zahter', 'Kokin', 'Hutong', 'Freddie']
NP = re.compile('|'.join(re.escape(n) for n in NAMES))
CLIP = {'temper-burger': 'Burger', 'temper-mix': 'Brand film', 'azzurra-weekend': 'Weekend service', 'paradiso-bottomless': 'Bottomless brunch',
        'notto': 'Fresh pasta', 'beeble': 'Spirits campaign'}
ALT = {'Bartender throwing a cocktail at The Connaught Bar': 'Bartender throwing a cocktail', 'Domed dining room at 1 Lombard Street': 'Domed dining room',
       '1 Lombard Street website': 'Restaurant website', '1 Lombard Street': 'Domed dining room'}
def clipname(tag):
    m = re.search(r'videos/clips/([a-z-]+?)-[sml]\.mp4', tag); return m and m.group(1)
def fix_video(m):
    tag = m.group(0); c = clipname(tag)
    if c in CLIP and 'aria-label="' in tag and NP.search(re.search(r'aria-label="([^"]*)"', tag).group(1)):
        tag = re.sub(r'aria-label="[^"]*"', 'aria-label="%s"' % CLIP[c], tag)
    return tag
def fix_fig(m):
    fig = m.group(0); c = clipname(fig)
    def cap(n):
        txt = n.group(1)
        if not NP.search(txt): return n.group(0)
        if c in CLIP: return '<figcaption>%s</figcaption>' % CLIP[c]
        return '<figcaption>%s</figcaption>' % ALT.get(txt, txt)
    return re.sub(r'<figcaption>(.*?)</figcaption>', cap, fig)
left = []
for d, _, fs in os.walk(R):
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); t = open(p, encoding='utf-8').read(); o = t
        t = re.sub(r'<video\b[^>]*>', fix_video, t)
        t = re.sub(r'<figure\b.*?</figure>', fix_fig, t, flags=re.S)
        for a, b in ALT.items(): t = t.replace('alt="%s"' % a, 'alt="%s"' % b)
        if t != o: open(p, 'w', encoding='utf-8').write(t)
        # check: visible text and labels only (ignore file paths, scripts and structured data)
        s = re.sub(r'<script.*?</script>', '', t, flags=re.S)
        s = re.sub(r'(src|href|poster|data-src|data-mm-poster|data-mm-src|data-reels|srcset)="[^"]*"', '', s)
        for m in NP.finditer(s): left.append((p, s[max(0, m.start() - 60):m.end() + 30]))
if left:
    for x in left[:20]: print('NAME LEFT', x)
    raise SystemExit('client names still present: %d' % len(left))
print('client names: only in logos')
