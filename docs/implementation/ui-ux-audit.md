# UI/UX Audit — ARKfolio

- **Site:** <https://rae-ark.horizonarkstudio.workers.dev/>
- **Date recorded:** 2026-10-09
- **Scope:** Observations on the current Vue/Vite SPA and repository

## Status summary

| # | Finding | Status |
| --- | --- | --- |
| 1 | Redundant bottom-row nav in the footer | Proposed — [0001](../proposals/0001-remove-footer-nav-row.md) |
| 2 | ↗ arrows on internal links | Open |
| 3 | Mislabeled "Amazon" retailer link | Open |
| 4 | Inconsistent external-link affordance | Open |
| 5 | Store page has no way to express interest | Open |
| 6 | Feedback form is a `mailto:` launcher, disclosed late | Open |
| 7 | Two parallel codebases in the repo | Open |
| 8 | Heavy use of inline `style=""` | Open |
| 9 | GitHub links point to a renamed repo | Open |

## Findings

### 1. Redundant bottom-row nav in the footer

`AppFooter.vue`'s `.footer-links` row repeats Works, Store, Journal and
About, identical to the header nav, then adds Feedback, Privacy, Terms, X
and GitHub into the same unstyled flex row. Nine links of equal visual
weight with no grouping, sitting right under a quote and the imprint line.
It reads like filler rather than a designed footer.

### 2. "↗" (external-link) arrows on internal links

On the homepage's "Where to Read" section, the Royal Road and Scribble Hub
cards use the ↗ external-link glyph but route internally to `/works`
(`<router-link to="/works">`), not off-site. The icon promises a new
destination it doesn't deliver. Only the X/Twitter card actually leaves the
site.

### 3. Mislabeled retailer link in the Store

In `data/store.ts`, the retailer labeled "Amazon" points to a
`royalroad.com/amazon/...` redirect URL, not `amazon.com`. It is visually
indistinguishable from the other direct retailer links (Walmart, eBay,
Saxo), so a reader has no way to know it's a redirect before clicking.

### 4. Inconsistent external-link affordance

Some external links get the ↗ suffix (Works page retailer links, About page
read-links), others don't (header's X/GitHub icon buttons, footer's X/GitHub
text links). There is no consistent visual rule for "this leaves the site."

### 5. Store page promises content it doesn't have yet

The Store's empty-state note says only SBM is in print and that EPMC/STBF
"aren't in print yet... they'll appear here first". That's honest copy, but
there's no separate way to express interest or get notified, so the message
is a dead end.

### 6. Feedback form's actual behavior is undersold until the end

The form looks like a normal web form (select, text input, textarea, submit
button) but is actually a `mailto:` launcher; it only opens the visitor's
local email client. That's disclosed in a hint line below the submit
button, after the user has already filled it in. Anyone without a
configured desktop mail client (increasingly common) hits a dead end with
no fallback.

### 7. Two parallel codebases in the repo

The repo root still has a full static multi-page site (`index.html`,
`works.html`, `journal.html`, `store.html`, `about.html`, `script.js`,
`style.css`) alongside the real, deployed Vue/Vite SPA in `src/`.
`wrangler.jsonc` only ships `dist/` (the Vite build), so the static files
are dead weight, but nothing marks them as deprecated, so a future edit
could easily land in the wrong place and never go live.

### 8. Heavy use of inline `style=""` attributes

Page components (`WorksPage`, `StorePage`, `AboutPage`, `FeedbackPage`,
`JournalPage`) lean on inline styles for layout (`padding-top:36px`,
`font-size:clamp(...)`, etc.) instead of the stylesheet. Not visible to a
visitor, but it makes the design system harder to keep consistent as the
site grows.

### 9. GitHub links point to a renamed repo

Header, footer, and About page all link to
`github.com/Rae-ARK/My-Portfolio`, while the repo is now `ARKfolio`.
GitHub's redirect covers it for now, but it's a stale reference waiting to
break.
