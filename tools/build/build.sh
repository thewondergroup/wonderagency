#!/bin/bash
set -e
S=/tmp/claude-0/-home-claude/5ebe2286-d1ca-5e11-b1a4-090b78facc58/scratchpad
rm -rf $S/v3 && cp -a $S/site $S/v3 && cd $S/v3
cp $S/script/node_modules/@fontsource/italiana/files/italiana-latin-400-normal.woff2 fonts/italiana-400.woff2
cp $S/script/node_modules/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2 fonts/manrope-var.woff2
cp $S/reels/reel-*.mp4 videos/
mkdir -p videos/clips images/x && cp $S/clips3/*.mp4 videos/clips/ && cp $S/clips3/*.webp images/x/ && for f in $S/clips3/*.webp; do b=$(basename $f .webp); mv images/x/$b.webp images/x/clip-$b.webp; done
cp $S/media4/*.mp4 videos/clips/ && cp $S/media4/*.webp images/x/
python3 $S/build3/prep_images.py $S
cp $S/build3/extend.css css/extend.css; cp $S/build3/extend.js $S/build3/extend3.js js/; cp $S/script/node_modules/lenis/dist/lenis.min.js js/lenis.min.js
sed -i "s#'PASTE_APPS_SCRIPT_WEB_APP_URL_HERE'#'https://script.google.com/macros/s/AKfycbzzPgtb-gHU8EsYfempzwVKaS_g3TtE_8aqz2OQfLsmGA_qhBLciC1_FPOA-lUy9cikzw/exec'#" js/contact-form.js
python3 -I $S/build3/patch_form.py $S/v3/js/contact-form.js
mkdir -p images/x/logos && cp $S/build3/assets/logos/*.webp images/x/logos/
python3 -I $S/build3/transform.py $S/site/index.html $S/v3/index.html
python3 $S/build3/trim_logos.py $S/v3
python3 $S/build3/optimise.py $S/v3
cp $S/build3/pages.css css/pages.css
mkdir -p images/x/sites && cp $S/sites-img/*.webp images/x/sites/
python3 -I $S/build3/pages.py $S/v3
cp $S/build3/mega.js js/mega.js; cp $S/build3/library.js js/library.js
python3 -I $S/build3/prune.py $S/v3
python3 -I $S/build3/names.py $S/v3
python3 -I $S/build3/seo.py $S/v3
python3 -I $S/build3/recolor.py $S/v3
python3 -I $S/build3/bust.py $S/v3
# old address for influencer marketing (it was a paid ads page until October 2026): send people and search engines to the new one
mkdir -p $S/v3/services/paid-advertising/influencer-marketing
cat > $S/v3/services/paid-advertising/influencer-marketing/index.html <<'HTML'
<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Influencer marketing | The Wonder Agency</title><link rel="canonical" href="https://thewonderagency.co/services/influencer-marketing/"><meta name="robots" content="noindex, follow"><meta http-equiv="refresh" content="0; url=/services/influencer-marketing/"><script>location.replace('/services/influencer-marketing/'+location.hash)</script><style>body{background:#000;color:#fff;font-family:sans-serif;padding:40px}a{color:#5eadba}</style></head><body><p>Influencer marketing has moved to <a href="/services/influencer-marketing/">its own page</a>.</p></body></html>
HTML
du -sh $S/v3
