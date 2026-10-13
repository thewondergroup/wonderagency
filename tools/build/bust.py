import os, re, sys, hashlib
R = sys.argv[1]
files = ['css/extend.css', 'css/pages.css', 'js/extend.js', 'js/extend3.js', 'js/mega.js', 'js/library.js', 'js/contact-form.js']
ver = {f: hashlib.md5(open(os.path.join(R, f), 'rb').read()).hexdigest()[:8] for f in files if os.path.exists(os.path.join(R, f))}
n = 0
for d, _, fs in os.walk(R):
    for fn in fs:
        if not fn.endswith('.html'): continue
        p = os.path.join(d, fn); t = open(p, encoding='utf-8').read(); o = t
        for f, v in ver.items():
            t = re.sub(r'((?:href|src)="(?:\.\./)*' + re.escape(f) + r')(\?v=[0-9a-f]+)?"', r'\1?v=' + v + '"', t)
        if t != o: open(p, 'w', encoding='utf-8').write(t); n += 1
print('versioned', n, 'pages', ver)
