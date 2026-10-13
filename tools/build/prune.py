# Remove videos and clip posters that no page or script references.
import os, re, sys
R = sys.argv[1]; text = ''
for d, _, fs in os.walk(R):
    for f in fs:
        if f.endswith(('.html', '.js', '.css')): text += open(os.path.join(d, f), encoding='utf-8', errors='ignore').read()
gone = 0; freed = 0
for sub in ('videos/clips', 'videos', 'images/x'):
    base = os.path.join(R, sub)
    for f in os.listdir(base):
        p = os.path.join(base, f)
        if not os.path.isfile(p): continue
        if sub == 'images/x' and not (f.startswith('clip-') or f.startswith('ph-')): continue
        if not f.endswith(('.mp4', '.webp')): continue
        if f not in text: freed += os.path.getsize(p); os.remove(p); gone += 1
print('pruned', gone, 'files', round(freed / 1e6, 1), 'MB')
