# 0008 — Discoverability for a client-rendered SPA (Stage 1 of the site review)

- **Status:** Proposed
- **Priority:** 1 (highest) — cheapest work, biggest effect on how the site
  looks when found or shared.
- **Constraint:** ARKfolio is a **single-page app, not a static site**.
  Routes are rendered in the browser by vue-router and Cloudflare serves
  `index.html` for every path (`not_found_handling: single-page-application`).
  Nothing in this proposal requires prerendering, SSG or SSR.

## Problem

- Per-page `<title>` and description are set by JavaScript in
  `router/index.ts` after load. Link-preview scrapers (Discord, X, Slack,
  Facebook) generally do not run JavaScript, so every shared link shows the
  homepage's generic card.
- There are no Open Graph or Twitter card tags, so shared links carry no
  image.
- There is no `robots.txt` or `sitemap.xml`.
- Unknown URLs return the app shell with a 200 status (a "soft 404").
- Search engines have no structured data identifying the author or the
  paperback.
- The July 2026 journal entry reports all three stories mirrored on a
  copycat site; the site itself never says where the official copies are.

## Proposed changes

1. **Site-level Open Graph / Twitter tags in `index.html`.** Static,
   one card for the whole site: `og:type`, `og:site_name`, `og:title`,
   `og:description`, `og:image` (a cover or the Horizon ARK logo, at least
   1200×630, served from `/assets/`), `twitter:card=summary_large_image`.
   Because scrapers read only the static HTML, this single card is what
   every shared link will show. That is an accepted limit of a SPA.
2. **`public/robots.txt` and `public/sitemap.xml`.** Hand-maintained; there
   are only eight routes. Must be real files in `public/`, otherwise the SPA
   fallback answers `/robots.txt` with `index.html`.
3. **A catch-all `NotFound` route** (`/:pathMatch(.*)*`) with a short page and
   a link home, plus `<meta name="robots" content="noindex">` set by the
   router on that page. This addresses the soft-404 problem without a server.
4. **JSON-LD injected by the router.** Extend the existing `afterEach` hook
   to add or replace one `<script type="application/ld+json">`: `Person`
   (author) on Home/About, `Book` on Store for the June 2026 edition (ISBN
   from `data/store.ts`). Google executes JavaScript, so this works in a
   SPA; scrapers that don't run JS simply won't see it.
5. **"Official sources" notice on the Works page.** A short block listing
   Royal Road, Scribble Hub and the paperback retailers as the only
   authorised places to read or buy, with a line pointing to the journal
   entry. Data comes from the same `links` already in `works.ts`.

## Non-goals

- No `vite-ssg`, prerender plugin, SSR framework or build-time HTML
  generation.
- No per-route social cards (see Open questions).

## Open questions

- **Per-route link previews.** Only possible in a SPA by adding a small
  Cloudflare Worker script that rewrites `<meta>` tags with `HTMLRewriter`
  per path, in front of the static assets. It keeps the app a SPA but adds
  a `main` entry to `wrangler.jsonc` and `run_worker_first` routing. Worth
  it only if per-page previews matter; not part of this stage.
- Which image should be the default share card?

## Verification

- Paste the homepage URL into a preview tool (Discord, X card validator).
- Visit `/robots.txt` and `/sitemap.xml` and confirm they are not HTML.
- Visit `/nope` and confirm the NotFound page and `noindex`.
- Run the Rich Results test on `/store` for the `Book` markup.
