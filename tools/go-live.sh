#!/bin/bash
# Launch day: move the finished site from /v3/ to the root of the repo, for thewonderagency.co.
# Run after the domain's DNS points at GitHub Pages (see LAUNCH.md).
set -e
REPO=$(cd "$(dirname "$0")/.." && pwd); cd "$REPO"
[ -f v3/index.html ] || { echo "no v3 build"; exit 1; }
rm -rf _site && cp -r v3 _site
find _site -name "*.html" ! -name 404.html | while read f; do
  sed -i 's#<meta name="robots" content="noindex, nofollow"/>#<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>#' "$f"; done
sed -i 's#<meta name="robots" content="noindex, nofollow"/>#<meta name="robots" content="noindex"/>#' _site/404.html
mv _site/_live-robots.txt _site/robots.txt
git rm -rq --ignore-unmatch index.html assets v2 v3
cp -r _site/. . && rm -rf _site
echo "thewonderagency.co" > CNAME; touch .nojekyll
echo "pages: $(find . -path ./.git -prune -o -name '*.html' -print | wc -l)  still noindex (should be 1, the 404): $(grep -rl 'noindex' --include=*.html . | wc -l)"
