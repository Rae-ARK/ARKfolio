// The deployed address, used for absolute URLs (structured data, RSS feed).
// Plain module with no imports so scripts/build-feed.mjs can read it too.
// Keep in sync with the og:* tags in index.html, public/sitemap.xml and
// public/robots.txt.
export const SITE_ORIGIN = 'https://rae-ark.horizonarkstudio.workers.dev'
