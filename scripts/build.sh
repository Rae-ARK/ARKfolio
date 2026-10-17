#!/usr/bin/env bash
# Build the site and layer a PWA manifest + service worker on top.
#
# Plain `arklight build site.py -o ARK` is still enough on its own --
# this script only exists because PWA generation is a *second*,
# separate CLI step (`arklight pwa`) over the build output, not
# something `site.py`/`Site(...)` can request on its own yet.
#
# Manifest values mirror the Vue site's manifest.json as closely as
# `arklight pwa`'s flags allow (see that file, kept for reference).
# Not expressible via the CLI today, so left out rather than faked:
# `description`, `scope`, `id`, `orientation`, and per-icon `purpose`
# (`maskable` vs `any` -- this only emits one `"purpose": "any"` icon
# entry from the single --icon flag below; a real maskable icon needs
# its own safe-zone-padded source image, which this repo doesn't have
# -- the profile photo doesn't have the padding maskable icons need).
# `start_url` is "index.html", not the Vue manifest's "/": this is a
# static multi-page build with no server-side rewrite, so "/" would
# resolve to a directory listing, not `index.html`, on most static
# hosts.
set -euo pipefail
cd "$(dirname "$0")/.."

ARK_DIR="${1:-ARK}"

arklight build site.py -o "$ARK_DIR" --no-open

# RSS feed: not a page ARKlight's own build knows how to emit, so it's
# a second pass over the output dir, same division of labour as the
# original Vue site's scripts/build-feed.mjs. See pages/journal.py's
# "/feed.xml" link and arklight.config.py's overdrive note for why the
# link-check lets that href through even though nothing above
# generates it.
python3 "$(dirname "$0")/build_feed.py" "$ARK_DIR"

arklight pwa "$ARK_DIR" \
  --name "Rae ARK — Web Novelist" \
  --short-name "Rae ARK" \
  --start-url "index.html" \
  --theme-color "#111111" \
  --background-color "#111111" \
  --display standalone \
  --icon "assets/images/profile.png:1024x1024"

echo "Built + PWA-enabled -> $ARK_DIR/"
