#!/bin/bash
set -e
S=/tmp/claude-0/-home-claude/5ebe2286-d1ca-5e11-b1a4-090b78facc58/scratchpad
rm -rf $S/v3 && cp -a $S/site $S/v3 && cd $S/v3
cp $S/script/node_modules/@fontsource/italiana/files/italiana-latin-400-normal.woff2 fonts/italiana-400.woff2
cp $S/script/node_modules/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2 fonts/manrope-var.woff2
cp /home/claude/wonderagency/assets/reel-*.mp4 videos/
mkdir -p videos/clips images/x && cp $S/clips3/*.mp4 videos/clips/ && cp $S/clips3/*.webp images/x/ && for f in $S/clips3/*.webp; do b=$(basename $f .webp); mv images/x/$b.webp images/x/clip-$b.webp; done
cp $S/media4/*.mp4 videos/clips/ && cp $S/media4/*.webp images/x/
python3 $S/build3/prep_images.py $S
cp $S/build3/extend.css css/extend.css; cp $S/build3/extend.js $S/build3/extend3.js js/; cp $S/script/node_modules/lenis/dist/lenis.min.js js/lenis.min.js
sed -i "s#'PASTE_APPS_SCRIPT_WEB_APP_URL_HERE'#'https://script.google.com/macros/s/AKfycbzzPgtb-gHU8EsYfempzwVKaS_g3TtE_8aqz2OQfLsmGA_qhBLciC1_FPOA-lUy9cikzw/exec'#" js/contact-form.js
python3 -I $S/build3/patch_form.py $S/v3/js/contact-form.js
python3 -I $S/build3/transform.py $S/site/index.html $S/v3/index.html
python3 $S/build3/trim_logos.py $S/v3
python3 $S/build3/optimise.py $S/v3
cp $S/build3/pages.css css/pages.css
python3 -I $S/build3/pages.py $S/v3
cp $S/build3/mega.js js/mega.js; cp $S/build3/library.js js/library.js
python3 -I $S/build3/prune.py $S/v3
python3 -I $S/build3/names.py $S/v3
python3 -I $S/build3/seo.py $S/v3
python3 -I $S/build3/recolor.py $S/v3
python3 -I $S/build3/bust.py $S/v3
du -sh $S/v3
