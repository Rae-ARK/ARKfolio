# 0007 — Redesign the Store page with modern CSS motion

- **Status:** Proposed
- **Scope:** Store page (`StorePage.vue`) first. The motion primitives below are
  written so other pages can adopt them later; nothing here changes the
  other pages in this proposal.
- **Relates to:** [0006](0006-print-interest-via-feedback.md),
  [UI/UX audit](../implementation/ui-ux-audit.md)

## Problem

The Store is the one page whose job is to turn a reader into a buyer, and it
is currently the plainest page on the site: a cover, a paragraph and a grid
of retailer buttons, followed by a note about the books that aren't in print.
Motion is limited to the shared `v-reveal` fade-and-slide and a few hover
transitions. Nothing makes the paperback feel like an object, and the
"not in print yet" area (now a card, see the changelog) is still a block of
text rather than part of the page's design.

## Goals

- Make the paperback feel like a physical book on a shelf, in line with the
  footer quote about books sitting on shelves.
- Use current CSS features for motion instead of adding a JavaScript
  animation library.
- Keep it calm. Motion should reward attention (hover, scroll, first load),
  never loop loudly or compete with reading.
- Remain fully usable with reduced motion, in light and dark themes, and
  inside the Capacitor Android WebView.

## Non-goals

- No new runtime dependencies (no GSAP, Framer-style libraries, Lottie).
- No change to retailer data, link behavior or the feedback flow.
- No autoplaying or looping animation that runs while the visitor is just
  reading.

## Proposed changes

### 1. Staggered entrance with `@keyframes`

Replace the single fade-and-slide on the book block with a short choreographed
sequence: cover, then edition label, title, description, retailer buttons.
Each piece uses the same keyframes with a delay from a custom property
(`animation-delay: calc(var(--i) * 70ms)`), animating only `opacity` and
`transform`. Runs once on load, 500ms total or less.

### 2. A book you can tilt

Give the cover CSS 3D depth: `perspective` on the container, a thin spine
and page-edge made from pseudo-elements, and a small `rotateY` / lift on
hover and focus (pointer devices only, as the existing `.retailer-btn` hover
rules already do). On touch devices the cover stays flat with a subtle
one-time settle animation.

### 3. Scroll-driven animation, with a fallback

Use `animation-timeline: view()` so the cover eases in and the shelf line
draws across as the visitor scrolls, wrapped in `@supports
(animation-timeline: view())`. Where it isn't supported, the existing
`v-reveal` IntersectionObserver behavior stays as the fallback. Support
should be checked before shipping, including the WebView version the Android
build targets.

### 4. A living border on the "Still to come" card

The print-interest card gets a slow, subtle brass highlight that travels
around its border using a registered custom property
(`@property --angle`) and a `conic-gradient`. It runs only while the card is
on screen and pauses on hover. The "I'm waiting for EPMC / STBF" buttons
get a small press and focus animation so they read clearly as the action.

### 5. Ghost spines for the books that aren't in print

Inside that card, show EPMC and STBF as dashed "ghost" book spines on a shelf
line, each with a soft shimmer. The buttons attach to the matching spine. This
makes "not in print yet" visible as an empty space on the shelf instead of
only a sentence.

### 6. Smaller modern touches

- `text-wrap: balance` on the page heading and lede.
- `color-mix()` for hover and tint colors, so both themes derive from the
  existing `--accent` and `--brass` tokens instead of new hard-coded values.
- Container queries on `.store-book` so the cover and text rearrange based on
  the card's width rather than the viewport.
- Optional: the View Transitions API (`document.startViewTransition`) on the
  Store to Feedback navigation, so choosing "I'm waiting for EPMC" carries the
  button into the form's page. Treated as an enhancement only.

## Constraints

- **Reduced motion:** everything above is disabled or reduced to a plain fade
  under `prefers-reduced-motion: reduce`, in the same style as the existing
  rule at the end of `main.css`.
- **Performance:** animate `transform` and `opacity` only; no layout-affecting
  properties. No animation on more than a handful of elements at once.
- **Progressive enhancement:** each feature sits behind `@supports` or degrades
  to the current static look. The page must never depend on a feature to be
  readable or to complete a purchase.
- **Themes and Android:** check both light and dark themes, and the edge-to-edge
  layout and safe-area insets used by the Android build.
- **Maintenance:** keyframes and tokens go in named sections of `main.css`,
  not inline styles (see audit finding 8).

## Rollout

1. Entrance stagger and `text-wrap` (low risk, no 3D or new APIs).
2. Book cover 3D and the card border highlight.
3. Scroll-driven animation and ghost spines.
4. View Transitions, only if the first three land well.

Each step can ship on its own.

## Open questions

- Should the other pages (Works, Home) adopt the same primitives afterward, or
  does the Store stay the one expressive page?
- How far should the shelf metaphor go? A full shelf illustration, or just a
  shelf line and spines?
- Which Android WebView versions does the app need to support? That decides
  whether scroll-driven animation needs its fallback or can be dropped.
- Is a one-off celebratory motion (for example on clicking a retailer) wanted,
  or is that too much for this site's tone?

## Verification

As with [0003](0003-header-nav-breakpoint-bug.md), the CSS is written from
reading the stylesheet, so each step needs a browser check (desktop, a phone
width, dark theme, reduced-motion on) before it is marked `Implemented`.
