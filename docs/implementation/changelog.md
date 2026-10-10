# Changelog

Shipped changes that resolve a proposal or an audit finding. Newest first.

## 2026-10-10 (latest)

### YouTube button in the header

- Added a YouTube icon button to the header's icon group (between X and
  GitHub), linking to <https://www.youtube.com/@Rae0611>. It uses the
  existing `.icon-btn` styling and `target="_blank"`, so the Android and
  desktop shells open it externally with no extra wiring.
- Files: `src/components/AppHeader.vue`.
- Needs a browser check at desktop width, in the mobile menu, and in dark
  theme.

### Reader conversion — proposal [0009](../proposals/0009-reader-conversion.md)

- **Hero mood card:** new `MoodCard.vue` and a `moods` list in
  `data/works.ts` (EPMC, SBM, STBF; EPMC first). Cross-fading slides,
  auto-advance every 7 s that stops on hover/focus/interaction or Pause,
  arrows + dots + Pause/Play, no animation or auto-advance under reduced
  motion. "Read the works" is now the secondary hero button. Prompt wording
  is a **first draft for the author to approve**.
- **Where to Read:** platform cards link straight to each story
  (derived from `works` links) instead of to `/works`.
- **Store:** Amazon is the primary "Buy on Amazon" button; other retailers
  are grouped under "Other retailers" (`Retailer.primary`).
- **RSS:** `scripts/build-feed.mjs` (no new dependency) writes
  `dist/feed.xml` at the end of `npm run build`; alternate link in
  `index.html` and "Follow by RSS ↗" on the Journal page. Undated
  ("July 2026", "Spring 2026") entries are left without `pubDate`.
- **Also:** `SITE_ORIGIN` moved to `src/seo/site.ts` so the feed script can
  share it; the share card was recompressed from a 198 KB PNG to a 59 KB
  JPEG (`og-card.jpg`).
- Verification: `npm run build` passes; `feed.xml` is valid XML (11 items,
  6 dated). Checked in headless Chromium against the production preview:
  slides advance, the router sets/removes JSON-LD and `noindex` correctly,
  autoplay runs on a normal profile and not under reduced motion, hidden
  slides have no focusable links, and the phone-width layout stacks.
  **Not checked:** dark theme, a real phone, the Android/desktop shells, or
  the feed in a real reader.
- Files: `src/components/MoodCard.vue`, `src/pages/HomePage.vue`,
  `src/pages/StorePage.vue`, `src/pages/JournalPage.vue`,
  `src/data/works.ts`, `src/data/store.ts`, `src/seo/site.ts`,
  `src/seo/structuredData.ts`, `scripts/build-feed.mjs`, `package.json`,
  `index.html`, `src/styles/main.css`.

### Discoverability for the SPA — proposal [0008](../proposals/0008-discoverability-spa.md)

- **Share cards:** static Open Graph + Twitter tags in `index.html` and a
  new 1200×630 `public/assets/images/og-card.jpg` (EPMC cover, name and
  tagline). One card for the whole site, because link-preview scrapers do
  not run the SPA's JavaScript.
- **Crawler files:** `public/robots.txt` and `public/sitemap.xml`.
- **404 page:** catch-all route and `NotFoundPage.vue`; the router sets
  `<meta name="robots" content="noindex">` there and removes it on every
  other route. The host still answers HTTP 200 for unknown paths.
- **Structured data:** `src/seo/structuredData.ts` plus a router
  `afterEach` hook injecting JSON-LD (`Person` on Home/About, `Book` on
  Store). `StoreBook` gained optional `isbn` and `datePublished`.
- **Works page:** an "Official sources" notice built from the `links` data.
- **Also:** `routes` typed as `RouteRecordRaw[]`.
- Verification: `npm run build` (vue-tsc + vite) passes; `robots.txt` and
  `sitemap.xml` land in `dist/`; the generated JSON-LD was checked by
  running `buildJsonLd`. **Not yet checked in a browser or a link-preview /
  rich-results tool** — see the proposal's Verification list.
- Files: `index.html`, `public/robots.txt`, `public/sitemap.xml`,
  `public/assets/images/og-card.jpg`, `src/seo/structuredData.ts`,
  `src/pages/NotFoundPage.vue`, `src/pages/WorksPage.vue`,
  `src/router/index.ts`, `src/data/store.ts`, `src/styles/main.css`.

## 2026-10-10 (later)

### Store page redesign (proposal 0007, steps 1–3) and SBM Volume 2 card

- **Proposal [0007](../proposals/0007-store-page-redesign.md)** — shipped
  Rollout steps 1–3 (Store only; Home/Works/Journal/About and the optional
  View Transitions step remain open). New shared sections in `main.css`:
  - **Staggered entrance** (`@keyframes reveal-stagger`, `.stagger-in`
    utility driven by `--i`) — used for the Store hero's eyebrow/heading/
    lede.
  - **Scroll-driven reveal** (`animation-timeline: view()` behind
    `@supports`), applied to every existing `v-reveal` element; the
    IntersectionObserver fallback in `useScrollReveal.ts` is unchanged and
    still carries browsers/WebViews without the feature.
  - **`color-mix()` tint** (`--brass-glow`) feeding the new Store motion
    below.
  - **Container query** on `.store-book` (`container-type: inline-size`),
    alongside the existing viewport media query rather than replacing it.
  - **`text-wrap: balance`** on `h1`–`h4` and `.lede` site-wide.
  - **Book tilt** — `.store-book .work-thumb` gets a spine and page-edge
    from pseudo-elements and a `rotateY` lift on hover (pointer devices
    only); touch devices get a flat cover with a one-time settle animation
    instead.
  - **Living border** on the "Still to come" card — a `@property --angle`
    + `conic-gradient` ring that runs while the card is visible and pauses
    on hover/focus.
  - **Ghost spines** — EPMC and STBF now render as a shimmering spine on a
    shelf line inside the card (`.ghost-shelf`), each with its own
    "I'm waiting for…" button, replacing the plain `.waiting-links` row.
  - All of the above collapses to the static look under
    `prefers-reduced-motion: reduce`.
  - Files: `src/styles/main.css`, `src/pages/StorePage.vue`. Needs a
    browser check (desktop, phone width, dark theme, reduced motion) per
    [Verification](../proposals/0007-store-page-redesign.md#verification)
    before the proposal can move past `Proposed`.
- **New volume** — added a Volume 2 card to the Store (Arc 3), using the
  newly added cover art. Not yet purchasable, so it renders a
  `coming-soon` badge ("Coming soon — Winter 2027") instead of a retailer
  grid; `StoreBook.note`/`retailers` are now optional to support this.
  Files: `src/data/store.ts`, `src/pages/StorePage.vue`,
  `src/styles/main.css` (new `.work-thumb.sbm2` background,
  `.coming-soon-badge`).
- **Docs cleanup** — removed proposals 0001–0006: all were `Implemented`
  and fully duplicated by their changelog entries, so they no longer
  needed a standalone file. `docs/proposals/README.md` updated to match;
  see that file's note on the convention going forward.
- Verification: `npm install && npm run build` (vue-tsc + vite) passes.

## 2026-10-10

### Arc 3 → Arc 4, mobile nav redesign, and widened proposal 0007

- **Audit 10** — "Currently writing" on the About page and home page said
  "Arc 3, ongoing" after the Journal's own Oct 3, 2026 entry said Arc 3 had
  wrapped and Arc 4 was starting. Updated to "Arc 4, ongoing" in both
  places. Files: `AboutPage.vue`, `data/works.ts`.
- **Audit 11** — the mobile nav dropdown was constrained by `.wrap`'s own
  padding (the actual containing block for its `position: absolute` panel),
  so it rendered as a narrow, left-aligned single-column list rather than
  using the screen's width. Repositioned against `header.site-header`
  instead (edge-to-edge), and replaced the stacked list with a numbered
  two-column table-of-contents-style grid, with a one-column fallback under
  420px and an open/close transition guarded by `prefers-reduced-motion`.
  Files: `main.css`. Needs a real-device/browser check before being
  considered fully verified.
- **Proposal [0007](../proposals/0007-store-page-redesign.md)** — widened
  from "Store page only" to the whole site: the motion primitives are now
  written as shared `main.css` sections from the start, with a page-by-page
  rollout (Store first, then Home/Works, then Journal/About), and a new
  References section grounding "modern web design" in current browser
  support data and design precedent gathered for this revision. Still
  `Proposed`; no page content changed by this revision, only the proposal
  document.
- Sanity-checked the rest of the site for the same kind of drift: router
  links against the route table, external-link (↗) vs internal-link (→)
  usage, copyright year, legal-page "last updated" handling, and leftover
  inline styles — no further issues found.
- Verification: `npm run build` (vue-tsc + vite) passes; no unused
  components, composables, or data files found in `src/`.

## 2026-10-09 (later)

### Journal update and Store print card

- **Journal** — two new entries on `/journal`, taken from the author's own
  Royal Road posts: *Arc 3 Is Done — A Short Break Before Arc 4* (Oct 3, 2026)
  and *Unauthorised Copies on a Mirror Site* (Jul 19, 2026). The source
  comment in `data/journal.ts` no longer refers to the deleted `journal.html`.
  Source notes: [foundational](../foundational/README.md). Files:
  `src/data/journal.ts`.
- **Store "not in print yet" note** now sits in a card (brass top edge, solid
  border, shadow, normal text color) with the waiting buttons as primary
  buttons, instead of a faint dashed box. Files: `StorePage.vue`, `main.css`.
- New proposal: [0007](../proposals/0007-store-page-redesign.md), a Store page
  redesign using modern CSS motion. Not started.

## 2026-10-09

### Round of audit fixes and copy changes

- **Footer** — [0001](../proposals/0001-remove-footer-nav-row.md): the nine-link
  row is replaced by a small Feedback / Privacy / Terms line next to the
  copyright. Files: `AppFooter.vue`, `main.css`.
- **About spacing** — [0004](../proposals/0004-about-text-spacing.md): body
  text no longer sits on the hero divider. Same fix on Feedback, Journal,
  Privacy and Terms. Files: all page components, `main.css`.
- **Home heading** — [0005](../proposals/0005-where-to-read-heading.md): now
  "Read every chapter free, or keep a copy on your shelf". Files:
  `HomePage.vue`.
- **Print interest** — [0006](../proposals/0006-print-interest-via-feedback.md):
  "I'm waiting for EPMC / STBF" buttons on the Store open the feedback form
  with the subject pre-selected. Files: `StorePage.vue`, `data/store.ts`,
  `useFeedbackForm.ts`.
- **Audit 2** — home-page Royal Road / Scribble Hub cards use → not ↗.
- **Audit 3** — Store explains the Amazon link goes through a Royal Road
  redirect. Notes now live on each retailer in `data/store.ts`
  (`retailerNote` removed).
- **Audit 4** — one external-link rule, documented in the audit. About page
  links get a space before ↗; the GitHub source link gets ↗.
- **Audit 6** — feedback form discloses the `mailto:` behavior up front and
  offers Copy address / Copy message.
- **Audit 7** — removed the legacy static site files from the repo root.
- **Audit 8** — page-level inline styles moved into `main.css`.
- **Audit 9** — `README.md` links to `Rae-ARK/ARKfolio`.
- Verification: `npm run build` (vue-tsc + vite) passes. The two changes
  below that were marked unverified were confirmed by the author.

### Header nav collapses at 900px — proposal [0003](../proposals/0003-header-nav-breakpoint-bug.md)

- The hamburger menu now takes over at `max-width: 900px` (previously
  `700px`), so the full nav and icon group no longer crowd the brand just
  above phone width.
- `.brand-row` no longer shrinks; the brand name and the
  "嵐久 怜 · WEB NOVELIST" subtitle no longer wrap.
- Between 701px and 900px the mobile dropdown uses 32px side padding to
  match `.wrap`; at 700px and below it stays at 20px.
- Files: `src/styles/main.css`.
- Verified in a browser by the author on 2026-10-09.

### Paperback card on the home page — proposal [0002](../proposals/0002-paperback-card-on-home.md)

- Added a **Paperback** card to the Where to Read section, linking to
  `/store` ("Summoned by Mistake, Vol. 1 →").
- Uses `→` rather than `↗` because the link is internal (see
  [audit finding 2](ui-ux-audit.md)).
- Files: `src/pages/HomePage.vue`.
- The section heading ("Every chapter, free, wherever you already read") was
  left unchanged.

### GitHub links point to `ARKfolio` — audit finding 9

- Header, footer and About page links updated in `ecbf336`.
- `README.md` was updated in the later 2026-10-09 round above.
