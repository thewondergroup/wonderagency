import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = "    data.set('page', location.href);\n"
assert s.count(old) == 1
new = old + """    // venue and link travel inside the message, so the existing Sheet script records them
    data.set('field', 'AUDIT REQUEST\\nVenue: ' + (data.get('venue') || '') + '\\nWebsite / Instagram: ' + (data.get('link') || '') + '\\n\\n' + (data.get('field') || ''));
"""
open(p, 'w', encoding='utf-8').write(s.replace(old, new))
