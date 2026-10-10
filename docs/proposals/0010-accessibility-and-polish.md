# 0010 — Accessibility and polish (Stage 3 of the site review)

- **Status:** Implemented — items 1–6 shipped. Stays open until the
  Verification list below is done (item 5 untested on desktop).
- **Priority:** 3
- **Constraint:** SPA, and it must keep working in the Capacitor Android
  WebView and the Neutralino desktop shell.

## Problem

- Cover art is applied as CSS `background-image`, so it has no text
  alternative for screen readers.
- `main.css` styles `:focus` only on form fields; links, nav entries and
  buttons have no visible keyboard focus style of their own.
- The mobile menu button's `aria-label` is always "Open menu", even while
  open.
- Cover PNGs are up to ~370 KB and are displayed much smaller.
- One cover file is named "…Two Beautiful Girls Act 1.png" while the title
  is "…Two Beautiful Flowers".
- `index.html` loads `/neutralino.js` on every web visit; only the desktop
  build uses it.
  Confirmed in a headless browser: every page load of the web build logs
  `Failed to construct 'WebSocket': ... ws://localhost:undefined` console
  errors, which come from that script finding no Neutralino runtime.
- The scroll reveal replays in both directions; it respects reduced motion
  but is worth checking on slower phones.

## Proposed changes

1. **Cover alt text.** *Shipped (role="img" + aria-label).* Render covers through `role="img"` with an
   `aria-label` (or an `<img>` element) in `WorkCard.vue`, `StorePage.vue`
   and the Works page, driven by `title` in the data files.
2. **`:focus-visible` outlines** *(shipped)* for `a`, `button`, `.icon-btn`,
   `nav.main-nav a` and `.btn`, using an existing brand colour with enough
   contrast in both themes.
3. **Dynamic menu label** *(shipped)* in `AppHeader.vue`:
   `:aria-label="navOpen ? 'Close menu' : 'Open menu'"`.
4. **Image optimisation.** *Shipped as WebP with the PNG kept as the
   fallback (not AVIF: it is newer and not supported everywhere).* The
   "Girls" file was renamed to match the title and `CACHE_VERSION` bumped to
   `arkfolio-v2`. *(Done.)*
5. **Load `neutralino.js` only in the desktop build.** *Shipped, untested on desktop (see changelog); done differently from this plan.* Original plan:
   have `neutralinoShell.ts` inject the script when the runtime's
   `NL_*` globals are present, then remove the tag from `index.html`.
6. **Reveal check.** *(Done.)* Tested by the author on an upper mid-range
   phone and it works, so the fade-out on scroll-back stays. A low-end
   phone hasn't been tried.

## Non-goals

- No visual redesign; palette and typography are unchanged.
- No new runtime dependencies.

## Open questions

- Confirm the Neutralino runtime exposes its globals before the app
  mounts, otherwise keep the script tag and gate it differently.

## Verification

- Keyboard-only pass through every page (Tab order and visible focus).
- Screen reader pass over Home, Works and Store covers.
- `npm run build`; compare cover payload before and after.
- Android debug build and desktop build both still open external links.
