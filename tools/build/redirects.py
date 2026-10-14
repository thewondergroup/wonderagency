# Redirects for addresses the old Webflow site (and the /v2/ and /v3/ previews) may have used.
# 1) Explicit redirect pages: noindex, canonical to the new page, instant refresh and JS redirect (Google treats this as a redirect).
# 2) A catch-all in 404.html: any other missing address is matched to the closest new page by keyword.
# Runs after seo.py, so none of these pages end up in the sitemap.
import os, sys, json

R = sys.argv[1]
SITE = 'https://thewonderagency.co/'

# old path -> new path (both without leading slash; '' is the homepage)
MAP = {
    # Webflow defaults and common agency pages
    'home': '', 'index': '', 'about-us': 'about/', 'our-story': 'about/', 'team': 'about/', 'our-team': 'about/', 'the-team': 'about/',
    'contact-us': 'contact/', 'get-in-touch': 'contact/', 'enquire': 'contact/', 'audit': 'contact/', 'free-audit': 'contact/',
    'our-work': 'work/', 'portfolio': 'work/', 'case-studies': 'work/', 'case-study': 'work/', 'projects': 'work/', 'clients': 'work/', 'results': 'work/',
    'our-services': 'services/', 'what-we-do': 'services/', 'service': 'services/',
    'social-media': 'services/social-media-management/', 'social': 'services/social-media-management/', 'social-media-marketing': 'services/social-media-management/',
    'content': 'services/content-creation/', 'content-production': 'services/content-creation/', 'photography': 'services/content-creation/', 'videography': 'services/content-creation/',
    'ads': 'services/paid-advertising/', 'paid-ads': 'services/paid-advertising/', 'paid-social': 'services/paid-advertising/', 'meta-ads': 'services/paid-advertising/', 'targeted-ads': 'services/paid-advertising/',
    'seo': 'services/seo-ai-search/', 'ai-search': 'services/seo-ai-search/', 'geo': 'services/seo-ai-search/',
    'web-design': 'services/website-design/', 'websites': 'services/website-design/', 'web-development': 'services/website-design/',
    'email': 'services/email-marketing/', 'newsletters': 'services/email-marketing/',
    'influencers': 'services/influencer-marketing/', 'influencer': 'services/influencer-marketing/',
    'wonderscore': 'wonder-score/', 'wonder-track': 'wonder-score/',
    'blog': 'insights/', 'news': 'insights/', 'articles': 'insights/', 'journal': 'insights/',
    'privacy-policy': 'privacy/', 'privacy-notice': 'privacy/', 'cookies': 'privacy/', 'cookie-policy': 'privacy/', 'terms': 'privacy/', 'terms-and-conditions': 'privacy/',
    'restaurants': 'who-we-work-with/restaurants/', 'hotels': 'who-we-work-with/hotels/', 'bars': 'who-we-work-with/bars-and-pubs/', 'pubs': 'who-we-work-with/bars-and-pubs/',
    'sectors': 'who-we-work-with/', 'industries': 'who-we-work-with/',
    'hotel-marketing': 'who-we-work-with/hotels/', 'restaurant-marketing': 'who-we-work-with/restaurants/', 'bar-marketing': 'who-we-work-with/bars-and-pubs/', 'hospitality-marketing': '',
    # the preview copies shared before launch
    'v2': '', 'v3': '', 'wonderagency': '',
}

def page(new):
    u = '/' + new; full = SITE + new
    return ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>The Wonder Agency</title>'
            '<link rel="canonical" href="%s"><meta name="robots" content="noindex, follow"><meta http-equiv="refresh" content="0; url=%s">'
            '<script>location.replace(%s + location.search + location.hash)</script>'
            '<style>body{background:#000;color:#fff;font-family:sans-serif;padding:40px}a{color:#5eadba}</style></head>'
            '<body><p>This page has moved to <a href="%s">%s</a>.</p></body></html>') % (full, u, json.dumps(u), u, full)

made = 0
for old, new in MAP.items():
    d = os.path.join(R, old)
    if os.path.exists(os.path.join(d, 'index.html')): continue   # a real page lives there now
    os.makedirs(d, exist_ok=True)
    for f in ('index.html',):
        open(os.path.join(d, f), 'w', encoding='utf-8').write(page(new))
    made += 1
    # Webflow also served /about-us.html style addresses on exports
    p2 = os.path.join(R, old + '.html')
    if not os.path.exists(p2): open(p2, 'w', encoding='utf-8').write(page(new))

# ---------- catch-all in 404.html ----------
pages = []
for d, _, fs in os.walk(R):
    if 'index.html' in fs:
        rel = os.path.relpath(d, R).replace(os.sep, '/')
        if rel == '.': continue
        top = rel.split('/')[0]
        if top in MAP or top in ('css', 'js', 'images', 'videos', 'fonts'): continue
        pages.append(rel + '/')
pages.sort()
JS = ('<script>(function(){var M=%s,P=%s,p=location.pathname.replace(/\\/index\\.html$/,"/").replace(/\\.html$/,"").replace(/^\\/+|\\/+$/g,"").toLowerCase();'
      'if(!p)return;var go=null,seg=p.split("/");'
      # /v3/services/x -> /services/x
      'if(seg[0]==="v2"||seg[0]==="v3"||seg[0]==="wonderagency"){var rest=seg.slice(1).join("/");go=rest&&P.indexOf(rest+"/")>-1?rest+"/":(M[seg[1]]!==undefined?M[seg[1]]:"");}'
      'else if(M[seg[0]]!==undefined)go=M[seg[0]];'
      'else{var best=null,bs=0,w=p.replace(/[^a-z0-9]+/g," ").split(" ").filter(function(x){return x.length>2&&["marketing","agency","london","the","and","for","services","service","with","our","your","page","html"].indexOf(x)<0});'
      'P.forEach(function(q){var s=0;w.forEach(function(x){if(q.indexOf(x)>-1)s+=x.length});if(s>bs||(s===bs&&best&&q.length<best.length&&s>0)){bs=s;best=q}});if(bs>=4)go=best;}'
      'if(go!==null&&go!==p+"/")location.replace("/"+go+location.hash);})();</script>') % (json.dumps(MAP), json.dumps(pages))
nf = os.path.join(R, '404.html'); t = open(nf, encoding='utf-8').read()
if 'var M=' not in t: t = t.replace('</head>', JS + '</head>', 1); open(nf, 'w', encoding='utf-8').write(t)
print('redirects: %d pages, catch-all over %d live pages' % (made, len(pages)))
