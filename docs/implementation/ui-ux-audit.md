# UI/UX Audit — ARKfolio

- **Site:** <https://rae-ark.horizonarkstudio.workers.dev/>
- **Date recorded:** 2026-10-09
- **Scope:** Observations on the current Vue/Vite SPA and repository

## Status summary

| # | Finding | Status |
| --- | --- | --- |
| 1 | Redundant bottom-row nav in the footer | Resolved — [0001](../proposals/0001-remove-footer-nav-row.md) |
| 2 | ↗ arrows on internal links | Resolved |
| 3 | Mislabeled "Amazon" retailer link | Resolved |
| 4 | Inconsistent external-link affordance | Resolved |
| 5 | Store page has no way to express interest | Resolved — [0006](../proposals/0006-print-interest-via-feedback.md) |
| 6 | Feedback form is a `mailto:` launcher, disclosed late | Resolved |
| 7 | Two parallel codebases in the repo | Resolved |
| 8 | Heavy use of inline `style=""` | Resolved |
| 9 | GitHub links point to a renamed repo | Resolved |
| 10 | "Currently writing" said Arc 3 after Arc 3 had wrapped | Resolved |
| 11 | Mobile nav was a cramped single-column list | Resolved |

## Findings

### 1. Redundant bottom-row nav in the footer

`AppFooter.vue`'s `.footer-links` row repeats Works, Store, Journal and
About, identical to the header nav, then adds Feedback, Privacy, Terms, X
and GitHub into the same unstyled flex row. Nine links of equal visual
weight with no grouping, sitting right under a quote and the imprint line.
It reads like filler rather than a designed footer.

**Status:** Resolved by [0001](../proposals/0001-remove-footer-nav-row.md). Only Feedback, Privacy and Terms remain, as a quiet line.

### 2. "↗" (external-link) arrows on internal links

On the homepage's "Where to Read" section, the Royal Road and Scribble Hub
cards use the ↗ external-link glyph but route internally to `/works`
(`<router-link to="/works">`), not off-site. The icon promises a new
destination it doesn't deliver. Only the X/Twitter card actually leaves the
site.

**Status:** Resolved. The Royal Road and Scribble Hub cards on the home page now use → (internal link).

### 3. Mislabeled retailer link in the Store

In `data/store.ts`, the retailer labeled "Amazon" points to a
`royalroad.com/amazon/...` redirect URL, not `amazon.com`. It is visually
indistinguishable from the other direct retailer links (Walmart, eBay,
Saxo), so a reader has no way to know it's a redirect before clicking.

**Status:** Resolved. The link stays (it is the working purchase link) but the Store now says under the buttons that Amazon opens through a Royal Road redirect.

### 4. Inconsistent external-link affordance

Some external links get the ↗ suffix (Works page retailer links, About page
read-links), others don't (header's X/GitHub icon buttons, footer's X/GitHub
text links). There is no consistent visual rule for "this leaves the site."

**Status:** Resolved. Rule: any text link that leaves the site ends in ↗ (now also the About page's GitHub source link and its story links, with consistent spacing); internal links use →; icon-only buttons (header X / GitHub) are exempt and carry an `aria-label`. The footer's duplicate X / GitHub text links were removed with finding 1.

### 5. Store page promises content it doesn't have yet

The Store's empty-state note says only SBM is in print and that EPMC/STBF
"aren't in print yet... they'll appear here first". That's honest copy, but
there's no separate way to express interest or get notified, so the message
is a dead end.

**Status:** Resolved by [0006](../proposals/0006-print-interest-via-feedback.md).

### 6. Feedback form's actual behavior is undersold until the end

The form looks like a normal web form (select, text input, textarea, submit
button) but is actually a `mailto:` launcher; it only opens the visitor's
local email client. That's disclosed in a hint line below the submit
button, after the user has already filled it in. Anyone without a
configured desktop mail client (increasingly common) hits a dead end with
no fallback.

**Status:** Resolved. The notice at the top of the form now says it opens the visitor's email app and sends nothing itself, and "Copy address" / "Copy message" buttons cover visitors with no email app.

### 7. Two parallel codebases in the repo

The repo root still has a full static multi-page site (`index.html`,
`works.html`, `journal.html`, `store.html`, `about.html`, `script.js`,
`style.css`) alongside the real, deployed Vue/Vite SPA in `src/`.
`wrangler.jsonc` only ships `dist/` (the Vite build), so the static files
are dead weight, but nothing marks them as deprecated, so a future edit
could easily land in the wrong place and never go live.

**Status:** Resolved. Removed the old static pages (`about.html`, `works.html`, `journal.html`, `store.html`, `feedback.html`), `script.js`, `style.css`, and the root `sw.js` and `manifest.json`. The live service worker and manifest are `public/sw.js` and `public/manifest.webmanifest`. Root `index.html` is the Vite entry point and stays; the original finding wrongly listed it as legacy.

### 8. Heavy use of inline `style=""` attributes

Page components (`WorksPage`, `StorePage`, `AboutPage`, `FeedbackPage`,
`JournalPage`) lean on inline styles for layout (`padding-top:36px`,
`font-size:clamp(...)`, etc.) instead of the stylesheet. Not visible to a
visitor, but it makes the design system harder to keep consistent as the
site grows.

**Status:** Resolved. All page-level inline styles moved to named classes in `src/styles/main.css` (see "Page layout helpers").

### 9. GitHub links point to a renamed repo

Header, footer, and About page all link to
`github.com/Rae-ARK/My-Portfolio`, while the repo is now `ARKfolio`.
GitHub's redirect covers it for now, but it's a stale reference waiting to
break.

**Status:** Resolved. Header, footer and About page links were updated in
commit `ecbf336`; the `README.md` link was updated on 2026-10-09.

### 10. "Currently writing" said Arc 3 after Arc 3 had wrapped

The About page sidebar and the home page's "Currently writing" list
(`data/works.ts`) both said "Summoned by Mistake... — Arc 3, ongoing". The
Journal's own newest entry — *Arc 3 Is Done — A Short Break Before Arc 4*,
Oct 3, 2026 — says Arc 3 wrapped and Arc 4 was starting the following week.
The status line hadn't been updated to match, so the site was telling two
different stories about the same book depending which page a reader was on.

**Status:** Resolved. `AboutPage.vue` and `data/works.ts` now say "Arc 4,
ongoing". The journal entries themselves were left untouched — they're
dated posts describing what had already happened at the time, not a status
line, so "Arc 3 Is Done..." is correct as written.

### 11. Mobile nav was a cramped single-column list

Below 900px wide, the nav dropdown sat inside `.wrap`, which is
`position: relative` — meaning `.wrap`, not the full-width header, was the
containing block for the dropdown's `position: absolute` panel. The panel's
left/right edges lined up with `.wrap`'s padded content column instead of
the screen edge, then added its own padding on top of that, so on a phone it
rendered as a narrow, left-aligned list of plain text links — never using
the width actually available.

**Status:** Resolved. The dropdown now takes `header.site-header` (already
`position: sticky`, a valid containing block) as its positioning context
instead, so it runs edge-to-edge. The five links are laid out as a numbered
two-column grid (brass index numbers over serif labels, in the site's
existing type pairing) rather than a stacked list, with a single-column
fallback under 420px. Files: `main.css`. Needs a browser check on a real
phone width before being considered fully verified (see
[0007](../proposals/0007-store-page-redesign.md) for why this came up
alongside the site-wide motion proposal).
