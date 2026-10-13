#!/bin/bash
# Copy a build into /v3/ as a hidden preview: every page gets noindex, and robots.txt/sitemap are not used there.
set -e
SRC=${1:?build folder}; REPO=$(cd "$(dirname "$0")/.." && pwd)
rm -rf "$REPO/v3" && cp -r "$SRC" "$REPO/v3"
find "$REPO/v3" -name "*.html" | while read f; do
  sed -i 's#<meta name="robots" content="[^"]*"/>##g; 0,/<head>/s##<head><meta name="robots" content="noindex, nofollow"/>#' "$f"
done
mv "$REPO/v3/robots.txt" "$REPO/v3/_live-robots.txt"
printf 'User-agent: *\nDisallow: /\n' > "$REPO/v3/robots.txt"
echo "preview pages: $(find "$REPO/v3" -name '*.html' | wc -l), without noindex: $(grep -L 'noindex' -r "$REPO/v3" --include=*.html | wc -l)"
