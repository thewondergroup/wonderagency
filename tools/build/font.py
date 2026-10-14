# Heading font: Marcellus replaces Italiana everywhere (October 2026, for legibility).
import os, re, sys, shutil
R = sys.argv[1]; n = 0
HERE = os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(HERE, '..', 'script', 'node_modules', '@fontsource', 'marcellus', 'files', 'marcellus-latin-400-normal.woff2'), os.path.join(R, 'fonts', 'marcellus-400.woff2'))
for d, _, fs in os.walk(R):
    for f in fs:
        if not f.endswith(('.css', '.html')): continue
        p = os.path.join(d, f); t = open(p, encoding='utf-8').read(); o = t
        t = t.replace('italiana-400.woff2', 'marcellus-400.woff2').replace('Italiana', 'Marcellus')
        t = re.sub(r'(@font-face\{font-family:Marcellus;[^}]*?)(\})', lambda m: m.group(1) + ('' if 'size-adjust' in m.group(1) else ';size-adjust:90%') + m.group(2), t, count=1)
        if t != o: open(p, 'w', encoding='utf-8').write(t); n += 1
f = os.path.join(R, 'fonts', 'italiana-400.woff2')
if os.path.exists(f): os.remove(f)
print('heading font: Marcellus in', n, 'files')
