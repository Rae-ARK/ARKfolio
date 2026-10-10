# Changelog

Shipped changes that resolve a proposal or an audit finding. Newest first.

## 2026-10-10 (latest)

### Desktop-only `neutralino.js`, cover file renamed — proposal [0010](../proposals/0010-accessibility-and-polish.md) item 5 and the rest of item 4

- **`neutralino.js` no longer loads on the web.** The `<script
  src="/neutralino.js">` tag is gone from `index.html`. `neutralinoShell.ts`
  now loads it on demand, only when the page is served as
  `http://localhost:<port>/` (Neutralino's built-in server). The hosted site
  (https, own domain) and the Android WebView (`https://localhost`, no port)
  never request it, which removes the `WebSocket ... ws://localhost:undefined`
  console errors there.
- **Different from the plan in the proposal:** the proposal said to inject
  the script "when the `NL_*` globals are present", but those globals come
  from `neutralino.js` itself (the Neutralino server fills them in when it
  serves that file), so there is nothing to test for before loading it. The
  check is the address instead. Neutralino's own `injectGlobals` /
  `injectClientLibrary` window options were the other candidate; they are in
  the current docs, but I couldn't confirm that the pinned 6.3.0 framework
  supports them, so they're not used.
- **Side effects:** the script now loads after the app starts instead of
  before, so the title/show/close wiring runs a moment later (the window
  isn't created hidden, so nothing flashes). `npm run dev` and `preview`
  also look like the desktop shell (http, localhost, port) and still log the
  old console error; it is harmless.
- **Cover file renamed:** "…Two Beautiful Girls Act 1" → "…Two Beautiful
  Flowers Act 1" (PNG and WebP), with the CSS rules updated.
  `CACHE_VERSION` in `public/sw.js` went from `arkfolio-v1` to `arkfolio-v2`,
  so old cached image paths (this rename and the earlier `png/`/`webp/`
  move) are cleaned up on the next visit.
- Files: `index.html`, `src/native/neutralinoShell.ts`, `src/styles/main.css`,
  `public/sw.js`, `public/assets/images/{png,webp}/` (renames), `docs/`.
- Verification: `npm run build` passes. In headless Chromium with the built
  files on a non-local host (standing in for the live site): no request for
  `neutralino.js`, no console errors, and the renamed Flowers cover loads as
  WebP. On `localhost:<port>` the script is requested, as it should be for the
  desktop shell (and, as noted, logs the old harmless error in a plain
  browser). **Not checked:** the desktop build itself (no
  `neu run` / `neu build` here), so whether the title, show-window, clean
  exit and external-link handling still work there is unconfirmed; the
  Android build.

### Accessibility, first half — proposal [0010](../proposals/0010-accessibility-and-polish.md) items 1–3

- **Cover alt text:** covers drawn with CSS `background-image` now have
  `role="img"` and an `aria-label` built from the data (`WorkCard`, Works
  page, both Store shelves, About avatar). On `WorkCard` the label also
  carries the kind and status, and the ribbon is `aria-hidden` so it isn't
  read twice (children of `role="img"` aren't exposed anyway). The Journal
  tag thumbnail and the hero mood-card cover stay hidden from assistive tech
  because text beside them already says the same thing. The header avatar
  link had no accessible name; it is now "About Rae ARK".
- **Focus outlines:** one rule gives `a`, `button`, `.icon-btn`,
  `nav.main-nav a` and `.btn` a 2 px `--accent` outline on `:focus-visible`
  (mouse clicks don't trigger it).
- **Menu button:** the label switches between "Open menu" and "Close menu".
- Files: `src/components/WorkCard.vue`, `src/components/AppHeader.vue`,
  `src/pages/WorksPage.vue`, `src/pages/StorePage.vue`,
  `src/pages/JournalPage.vue`, `src/pages/AboutPage.vue`,
  `src/styles/main.css`, `docs/`.
- Verification: `npm run build` passes. In headless Chromium (light theme):
  the menu label flips to "Close menu" on click, the first keyboard focus
  gets a 2 px solid outline in `--accent`, and the Works covers expose their
  labels. **Not checked:** a full keyboard-only pass, a screen reader, dark
  theme contrast, or whether the outline looks right on the solid primary
  buttons. Items 5 (neutralino.js) and 6 (reveal
  check) are still open, as is the "Girls" file rename.

### RSS cap, Store wording, X card removed from Where to Read

- **RSS:** `build-feed.mjs` now publishes only the newest 20 journal
  entries (`FEED_LIMIT`), taken in the order of `journalEntries`, which is
  newest-first. There are 11 entries today, so the feed doesn't change yet;
  the cap starts to matter at entry 21. The build log reads
  `feed.xml: 11 of 11 entries`. The journal page itself still lists every
  entry.
- **Store:** "limited run" removed from the Volume 1 description. With KDP
  expanded distribution on, the paperback is listed widely and isn't a
  scarce print run, which is what "limited run" implies. It now reads
  "version 1 of this volume — it will be updated later", which is what the
  author meant.
- **Where to Read:** the "X / Twitter" card is gone: it isn't somewhere to
  read. X is still linked from the header. Platforms and Paperback remain.
- Files: `scripts/build-feed.mjs`, `src/data/journal.ts`,
  `src/data/store.ts`, `src/pages/HomePage.vue`, `docs/`.
- Not checked on screen: the Where to Read row now has three cards.

### Images sorted into `png/` and `webp/`

- `public/assets/images/` is now `png/` (profile, logo and the four covers,
  the originals and the fallback), `webp/` (the WebP copies, same base
  names) and `og-card.jpg` at the top level, so the share-card URL stays the
  same. `main.css`, `structuredData.ts` and `README.txt` point at the new
  paths. Nothing else changed in the files.
- **Old image URLs no longer exist** (`/assets/images/profile.png` and the
  cover PNGs). Anything outside this repo that links to them directly, such
  as a hotlink from another site or an already-indexed structured-data
  image, will 404 until it is updated or recrawled.
- Files: `src/styles/main.css`, `src/seo/structuredData.ts`,
  `public/assets/images/` (moves), `docs/`.

### EPMC mood prompt reworded

- The EPMC prompt on the hero mood card changed from "In the mood for
  something a bit different?" to "Want a story about a second life in a
  world of magic?", at the author's request. It is still the first and
  default card. The comment in `data/works.ts` and proposal 0009 now say all
  three prompts were reworded.
- Files: `src/data/works.ts`, `docs/`.
- Not checked on screen: the longer line wrapping at phone width.

### WebP images, new share card, mood prompts reworded

- **WebP with PNG fallback (proposal [0010](../proposals/0010-accessibility-and-polish.md) item 4, partly):**
  the four covers and `profile.png` now have a `.webp` copy beside the
  original (cover payload 91+143+380+257 KB of PNG → 25+40+33+53 KB of
  WebP; profile 70 → 31 KB). Every `background-image: url(...png)` in
  `main.css` is followed by an `image-set()` with `type("image/webp")` and
  `type("image/png")`, so a browser that can't parse it, or can't decode
  WebP, keeps the PNG. AVIF was not used: it is newer and not supported
  everywhere. Not done: renaming the "Girls" cover file.
- **Share card:** `og-card.jpg` re-rendered with the profile picture
  (circle, brass ring, same dark-green backdrop as the site avatar) in place
  of the EPMC cover; text and layout unchanged. It stays a JPEG because
  link-preview scrapers don't all read WebP. The `og:image` and
  `twitter:image` URLs gained `?v=2`, because the filename is unchanged and
  `/assets/*` is cached as immutable, so scrapers and browsers would
  otherwise keep the old card.
- **Mood prompts:** the SBM and STBF prompts were reworded at the author's
  request ("Want something quieter — a fresh start, with an AI for
  company?" and "Want a shorter story, built from the start to reach its
  ending?"). The comment in `data/works.ts` and proposal 0009 no longer
  call them drafts.
- Files: `src/styles/main.css`, `src/data/works.ts`, `index.html`,
  `public/assets/images/` (5 new `.webp`, new `og-card.jpg`, `README.txt`),
  `docs/`.
- Verification: `npm run build` passes; the minified CSS keeps both the
  PNG line and the `image-set()` line for every rule. In headless Chromium
  against the production preview, the covers and avatar were requested as
  `.webp` (200) and the first mood prompt renders. **Not checked:** the
  PNG fallback in a browser without WebP or `image-set()` `type()` support,
  Safari, a real phone, the Android/desktop shells, the SBM/STBF prompts on
  screen (only the data was changed), or the card in a link-preview tool.

### YouTube button in the header

- Added a YouTube icon button to the header's icon group (between X and
  GitHub), linking to <https://www.youtube.com/@Rae0611>. It uses the
  existing `.icon-btn` styling and `target="_blank"`, so the Android and
  desktop shells open it externally with no extra wiring.
- Files: `src/components/AppHeader.vue`.
- Needs a browser check at desktop width, in the mobile menu, and in dark
  theme.

### Status bar follows the in-app theme

- **Android (`nativeShell.ts`):** the icon style was inverted. Capacitor's
  `Style.Dark` means light icons for a dark background and `Style.Light`
  means dark icons for a light background, but the code used the opposite,
  so icons had the wrong contrast in both themes. Light theme now sends
  `Style.Light`, dark theme `Style.Dark`. `capacitor.config.ts` default
  changed from `DARK` to `LIGHT` (dark icons on the light paper splash,
  which is what its comment already intended); needs
  `npm run android:sync` to take effect.
- **Web / PWA (`index.html`, `useTheme.ts`):** the two `theme-color` tags
  were keyed to `prefers-color-scheme`, so the in-app toggle never changed
  them, and the dark value (`#161512`) didn't match `--paper` (`#17160f`).
  There is now one tag, set before first paint and again on every toggle
  to `#f6f2e8` / `#17160f`.
- **Not verified on a device.** Checked in headless Chromium that the tag
  changes with the toggle and persists across reloads; the Android icon
  fix is from Capacitor's documented semantics and its plugin source, not
  from a phone. The installed-PWA title bar is also unchecked.
- Files: `src/native/nativeShell.ts`, `capacitor.config.ts`, `index.html`,
  `src/composables/useTheme.ts`.

### Reader conversion — proposal [0009](../proposals/0009-reader-conversion.md)

- **Hero mood card:** new `MoodCard.vue` and a `moods` list in
  `data/works.ts` (EPMC, SBM, STBF; EPMC first). Cross-fading slides,
  auto-advance every 7 s that stops on hover/focus/interaction or Pause,
  arrows + dots + Pause/Play, no animation or auto-advance under reduced
  motion. "Read the works" is now the secondary hero button. The EPMC
  prompt is the author's own wording; the SBM and STBF prompts are reviewer
  drafts **for the author to approve**.
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
