import re, os, sys, glob
from PIL import Image, ImageDraw, ImageFont
root = sys.argv[1]; os.chdir(root)
h = open('index.html', encoding='utf-8').read(); c = open('css/site.css', encoding='utf-8').read()
pat = r'(?:images|videos|fonts|js|css)/[A-Za-z0-9._/-]+'
refs = set(re.findall(pat, h)) | {r for r in re.findall(pat, c)} | set(re.findall(pat, open('css/extend.css').read()))
keep_png = {r for r in refs if 'Favicon' in r or 'Wonder-List-256' in r}
before = sum(os.path.getsize(f) for f in glob.glob('images/**/*', recursive=True) if os.path.isfile(f))
conv = {}
for r in sorted(refs):
    if not r.startswith('images/') or r in keep_png or not os.path.isfile(r): continue
    if not r.lower().endswith(('.png', '.jpg', '.jpeg')): continue
    im = Image.open(r); alpha = im.mode in ('RGBA', 'LA', 'P') and ('transparency' in im.info or im.mode != 'P')
    im = im.convert('RGBA' if alpha else 'RGB'); im.thumbnail((2000, 2000), Image.LANCZOS)
    new = re.sub(r'\.(png|jpe?g)$', '.webp', r, flags=re.I)
    im.save(new, 'WEBP', quality=90 if alpha else 80, method=6)
    conv[r] = new
for old in sorted(conv, key=len, reverse=True):
    h = h.replace(old, conv[old]); c = c.replace(old, conv[old])
open('index.html', 'w', encoding='utf-8').write(h); open('css/site.css', 'w', encoding='utf-8').write(c)
refs2 = set(re.findall(pat, h)) | set(re.findall(pat, c)) | set(re.findall(pat, open('css/extend.css').read())) | {'js/extend.js', 'js/contact-form.js'}
# og image
og = Image.open('images/x/connaught-team.webp').convert('RGB'); w, hh = og.size; t = 1200 / 630
ch = int(w / t); og = og.crop((0, (hh - ch) // 2, w, (hh - ch) // 2 + ch)).resize((1200, 630), Image.LANCZOS)
og = Image.blend(og, Image.new('RGB', og.size, 'black'), 0.62); d = ImageDraw.Draw(og)
f1 = ImageFont.truetype(glob.glob('fonts/*JuliusSansOne*')[0], 92); f2 = ImageFont.truetype(glob.glob('fonts/*JuliusSansOne*')[0], 30)
for i, line in enumerate(['THE WONDER', 'AGENCY']):
    wl = d.textlength(line, font=f1); d.text(((1200 - wl) / 2, 190 + i * 110), line, font=f1, fill='white')
s = 'MADE TO BE BOOKED OUT'; wl = d.textlength(s, font=f2); d.text(((1200 - wl) / 2, 470), s, font=f2, fill='#d3b203')
og.save('images/x/og.jpg', quality=86); refs2.add('images/x/og.jpg')
removed = 0
for f in glob.glob('images/**/*', recursive=True) + glob.glob('videos/*') + glob.glob('js/*') + glob.glob('fonts/*'):
    if os.path.isfile(f) and f not in refs2 and not f.startswith(('images/x/', 'videos/clips/')): os.remove(f); removed += 1
missing = [r for r in refs2 if not os.path.isfile(r)]
after = sum(os.path.getsize(f) for f in glob.glob('images/**/*', recursive=True) if os.path.isfile(f))
print('converted', len(conv), 'removed', removed, 'images MB %.1f -> %.1f' % (before / 1e6, after / 1e6), 'missing', missing)
