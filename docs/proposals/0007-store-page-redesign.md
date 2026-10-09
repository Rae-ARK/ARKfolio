# 0007 — Site-wide modern CSS motion, starting with the Store page

- **Status:** Proposed
- **Scope:** Widened from Store-only to the whole site. The motion
  primitives in this proposal are written as shared, reusable pieces
  (keyframes, custom properties, utility classes in `main.css`) from the
  start, not Store-only code that happens to get copied later. The Store
  still ships first as the proving ground — it's the page with a single
  clear job (turn a reader into a buyer) and the least amount of running
  text to disturb — but Home, Works, Journal and About are in scope for
  the same primitives once the Store step lands and gets a browser check.
- **Relates to:** [0006](0006-print-interest-via-feedback.md),
  [UI/UX audit](../implementation/ui-ux-audit.md), the mobile-nav redesign
  shipped alongside this revision (see the changelog and audit finding 10).

## Problem

The Store is the one page whose job is to turn a reader into a buyer, and it
is currently the plainest page on the site: a cover, a paragraph and a grid
of retailer buttons, followed by a note about the books that aren't in print.
Motion sitewide is limited to the shared `v-reveal` fade-and-slide and a few
hover transitions. Nothing makes the paperback feel like an object, the
"not in print yet" area (now a card, see the changelog) is still a block of
text rather than part of the page's design, and the same flatness — one
reveal style, a few hover states, nothing that responds to scroll or layout
— repeats across Home, Works, Journal and About. Treating the Store as a
one-off fixes the most visible page without giving the rest of the site a
shared visual language to grow into.

## Goals

- Make the paperback feel like a physical book on a shelf, in line with the
  footer quote about books sitting on shelves.
- Build the motion and layout primitives once, as shared CSS, so the Store,
  then Home/Works/Journal/About, all draw from the same small vocabulary
  instead of each page inventing its own.
- Use current CSS features for motion instead of adding a JavaScript
  animation library.
- Keep it calm. Motion should reward attention (hover, scroll, first load),
  never loop loudly or compete with reading — in line with what an editorial,
  literary-site audience expects (see References): generous whitespace and
  restrained typography-first design, not ornament for its own sake.
- Remain fully usable with reduced motion, in light and dark themes, and
  inside the Capacitor Android WebView.

## Non-goals

- No new runtime dependencies (no GSAP, Framer-style libraries, Lottie).
- No change to retailer data, link behavior or the feedback flow.
- No autoplaying or looping animation that runs while the visitor is just
  reading.
- No redesign of the site's palette, type system or the asterism/paper-grain
  identity — this proposal is about motion and a couple of layout primitives
  (container queries, the TOC-style nav grid already shipped), not a visual
  rebrand.

## Proposed changes

### Shared primitives (new, named sections in `main.css`)

These are written once and reused by every page in the rollout, rather than
living inside `StorePage.vue`'s styles:

1. **Staggered entrance** — `@keyframes reveal-stagger`, driven by
   `animation-delay: calc(var(--i) * 70ms)` on a `--i` custom property set
   per child. Replaces a single fade-and-slide with a short choreographed
   sequence (cover/heading, then supporting lines, then the call to action).
   Runs once on load, 500ms total or less.
2. **Scroll-driven reveal, with a fallback** — `animation-timeline: view()`
   wrapped in `@supports (animation-timeline: view())`, with the existing
   `v-reveal` IntersectionObserver behavior as the fallback everywhere it
   isn't supported. Per the compatibility data gathered for this proposal
   (see References), this has been supported in Chrome/Edge/Samsung
   Internet (hence Android WebView on current OS versions) since 2023 and in
   Safari since version 26; the IntersectionObserver fallback stays
   in place rather than being dropped, since older WebViews on devices that
   haven't picked up a System WebView update will still fall through to it.
3. **`color-mix()` tints** — hover/tint colors derived from the existing
   `--accent` and `--brass` tokens instead of new hard-coded values, so both
   themes stay in sync automatically.
4. **Container queries** on card-style components (`.store-book`,
   `.work-card`, `.journal-card`) so internal layout responds to the
   component's own width, not the viewport — useful since several of these
   cards appear in more than one column arrangement across pages.
5. **`text-wrap: balance`** on page headings and ledes sitewide.

### Store page (first to ship)

6. **A book you can tilt** — `perspective` on the cover's container, a thin
   spine and page-edge made from pseudo-elements, and a small `rotateY` /
   lift on hover and focus (pointer devices only, as `.retailer-btn` already
   does). Touch devices get a flat cover with a subtle one-time settle
   animation instead.
7. **A living border on the "Still to come" card** — a slow, subtle brass
   highlight traveling around the border via a registered custom property
   (`@property --angle`) and a `conic-gradient`. Runs only while the card is
   on screen and pauses on hover.
8. **Ghost spines** for EPMC and STBF on a shelf line inside that card, each
   with a soft shimmer, buttons attached to the matching spine — "not in
   print yet" as an empty space on the shelf, not just a sentence.
9. **Optional:** the View Transitions API
   (`document.startViewTransition`) on the Store → Feedback navigation, so
   choosing "I'm waiting for EPMC" carries the button into the form's page.
   Enhancement only.

### Later pages (same primitives, applied where each page's content fits)

- **Home** — staggered entrance on the hero and the "Where to Read" cards;
  container queries so those cards rearrange by their own width rather than
  the viewport, matching how they already sit in a responsive grid.
- **Works** — scroll-driven reveal per work card as the visitor scrolls
  through the three synopses, replacing the current all-at-once `v-reveal`;
  `color-mix()` for the status-pill backgrounds (Ongoing / On Hiatus / On
  Break) so they derive from the shared tokens instead of their own values.
- **Journal** — staggered entrance for each entry's thumb + title as it
  scrolls in; no 3D or shelf metaphor here, since the ghost-spine motif
  belongs to the Store's book-on-a-shelf framing specifically.
- **About** — `text-wrap: balance` on the lede and section headings;
  otherwise the lightest touch of the four, since the page is mostly running
  text and shouldn't compete with it.

Each page is its own step in Rollout below and ships only once the shared
primitive it depends on has already landed and been checked in a browser.

## Constraints

- **Reduced motion:** everything above is disabled or reduced to a plain fade
  under `prefers-reduced-motion: reduce`, in the same style as the existing
  rule at the end of `main.css`.
- **Performance:** animate `transform` and `opacity` only; no layout-affecting
  properties. No animation on more than a handful of elements at once.
- **Progressive enhancement:** each feature sits behind `@supports` or degrades
  to the current static look. No page may ever depend on one of these
  features to be readable, navigable, or to complete a purchase.
- **Themes and Android:** check both light and dark themes, and the
  edge-to-edge layout and safe-area insets used by the Android build, on
  every page in the rollout — not only the Store.
- **Maintenance:** keyframes and tokens go in named, shared sections of
  `main.css` (see "Shared primitives" above), not inline styles and not
  duplicated per page (see audit finding 8).

## References

Gathered while widening this proposal's scope, to ground "modern web
design" in what's actually shipping rather than a vague impression of it:

- Scroll-driven animations and the View Transitions API are now described as
  baseline/standard-track browser features rather than experiments — both
  are tied to actual browser versions (Chrome/Edge 115+ for
  `animation-timeline`, Safari 26+), which is the compatibility data behind
  the `@supports` fallback above.
- The View Transitions API (`@view-transition`, `document.startViewTransition`)
  for same-document and cross-document transitions has shipped across
  Chrome, Firefox and Safari, confirming the optional Store → Feedback
  transition in this proposal is reasonable as an enhancement, not a bet on
  an experimental API.
- Current guidance on CSS vs. JavaScript animation libraries (GSAP and
  similar) converges on: use CSS for reveal/fade, scroll-tied progress and
  hover/focus states; reach for a JS library only for scrubbed pinning or
  gesture-driven interaction — which matches this proposal's non-goal of
  adding no animation library.
- Editorial/literary author-site design references (serif-led typography,
  restrained palettes, generous whitespace, motion that's quiet rather than
  decorative) line up with ARKfolio's existing warm-paper/ink-teal/brass
  system — the takeaway was "extend the current language," not "replace
  it," which is why this proposal has no palette or type-system changes.
- Mobile navigation research (grid/table-of-contents style layouts vs. a
  single cramped column, and "beyond the hamburger" pattern surveys) directly
  informed the separate mobile-nav fix shipped alongside this revision —
  called out here because it's the same "modern web design, whole site"
  effort even though it isn't part of this proposal's own change list.

## Rollout

1. Shared primitives land in `main.css` (entrance stagger, `text-wrap`,
   `color-mix()` tokens) — low risk, no 3D or scroll-driven APIs yet.
2. Store: book cover 3D, the card border highlight, ghost spines.
3. Store: scroll-driven animation (with its fallback already in place from
   step 1's primitives).
4. Home and Works adopt the shared primitives (staggered entrance,
   container queries, scroll-driven reveal, `color-mix()` status pills).
5. Journal and About adopt the shared primitives (lightest touch).
6. View Transitions on Store → Feedback, only if steps 1–3 land well.

Each step can ship on its own and gets its own browser check before being
marked `Implemented` (see Verification).

## Open questions

- How far should the shelf metaphor go on the Store? A full shelf
  illustration, or just a shelf line and spines? (The ghost-spine motif is
  Store-specific either way — see "Later pages" above.)
- Which Android WebView versions does the app need to support in practice?
  That decides how long the scroll-driven animation fallback needs to stay,
  versus eventually being simplified away.
- Is a one-off celebratory motion (for example on clicking a retailer)
  wanted anywhere, or is that too much for this site's tone?
- Once Home/Works/Journal/About have the shared primitives, is there still
  a reason to treat the Store as "the one expressive page," or does the
  whole site read as one consistent, quietly animated system at that point?

## Verification

As with [0003](0003-header-nav-breakpoint-bug.md), the CSS is written from
reading the stylesheet, so each step in Rollout needs a browser check
(desktop, a phone width, dark theme, reduced-motion on) on every page it
touches before that step is marked `Implemented`.
