# Changelog

Shipped changes that resolve a proposal or an audit finding. Newest first.

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
