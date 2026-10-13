# Swap the old gold for the Wonder green across the built site.
import os, re, sys
R = sys.argv[1]
ACC = '#5eadba'; ACC_RGB = '94,173,186'      # text and thin lines: light tint of the deck green (fills use #255a63 directly in the CSS)
DEEP_RGB = '37,90,99'                         # the deck green itself (#255a63), for glows
lot = ['0.8274509803921568', '0.6980392156862745', '0.011764705882352941']
n = 0
for d, _, fs in os.walk(R):
    for f in fs:
        if not f.endswith(('.css', '.html', '.js', '.json', '.svg')): continue
        p = os.path.join(d, f); t = open(p, encoding='utf-8', errors='surrogateescape').read(); o = t
        t = re.sub(r'#d3b203', ACC, t, flags=re.I)
        t = re.sub(r'rgba\(211,\s*178,\s*3,\s*\.28\)', 'rgba(%s,.85)' % DEEP_RGB, t)          # card glows: the real deck green
        t = re.sub(r'rgba\(211,\s*178,\s*3,', 'rgba(%s,' % ACC_RGB, t)
        if f.endswith('.json'):
            t = t.replace(','.join(lot), '0.3686,0.6784,0.7294')
        if t != o: open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t); n += 1
print('recoloured', n, 'files')
