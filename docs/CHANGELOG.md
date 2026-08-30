# Changelog

All notable changes to the ARKlight edition of ARKfolio, in one running
list. Dates are UTC.

## [Unreleased]

### Fixed
- **`scripts/build.py` + `scripts/theme_persist_backend.py` restored.**
  Commit `096dbf6` ("Removed some internal files") deleted both, but
  `README.md`'s "Building" section still instructs `python
  scripts/build.py` as the required entry point -- `arklight build
  site.py -o ARK` alone only runs the stock backends and ships a
  build where the theme resets on every navigation (see "Resolved:
  theme toggle persistence" below). With the files gone, `python
  scripts/build.py` failed outright (`No such file or directory`),
  so the compiler's `Backend.postprocess` extension point --
  `ThemePersistBackend`, this site's only user of it -- was never
  being invoked at all. Restored both files verbatim from the last
  commit before the deletion (`a8b1a22`); `python scripts/build.py`
  builds successfully again and the `<!-- theme_persist_backend -->`
  marker + injected `<script>` tags are present in every rendered
  page, confirmed against a real build.
- **Favicon (`/assets/images/profile.png`) now resolves correctly.**
  This was never an ARKfolio-side bug -- `PAGE_FAVICON`
  (`components/common.py`) and every `Page(favicon=...)` call were
  always correct -- but a compiler bug in `arklight/backend/html/
  head_meta.py` (root-relative `favicon`/`og_image` paths resolved
  against the build process's cwd instead of the site's route
  structure, via an un-stripped leading `/` reaching
  `posixpath.relpath()`) meant the emitted `<link rel="icon" ...>`
  could point at a wrong, environment-dependent path. Fixed upstream
  in ARKlight; no ARKfolio-side code change was needed once the site
  is built against a patched `arklight` install. Verified: `<link
  rel="icon" href="assets/images/profile.png">` on every page.

### Added (this session -- ARKlight upgrade: nav toggle + native CSS)
- Pulled `Rae-ARK/ARKlight` `alpha` branch forward from `v0.048` to
  `v0.0501`. Mostly an internal HTMX-integration refactor, but two
  additions directly unblocked open items here:
  - **`Site.style_selector(selector, rules)`** (landed as part of
    "Added Extra CSS support", commit `a01b3e3`) -- real CSS
    authoring: combinators, pseudo-classes/elements, attribute
    selectors, `&`-nesting, plus `Site.keyframes()`/`font_face()`/
    `container_query()`/`supports()`. A closed grammar (raises
    `CSSSyntaxError` outside it), not a raw-CSS escape hatch.
  - **Named `"toggle"` behavior** (`Button(..., on_click="toggle",
    behavior_target="#id", toggle_class="...")`) -- stateless,
    page-independent show/hide, no `State(...)` threading needed.
- `components/nav.py`: mobile hamburger menu wired via the new
  `"toggle"` behavior (`behavior_target="#primary-nav"`,
  `toggle_class="open"`, matching `assets/site.css`'s existing
  `nav.main-nav.open` rule) -- previously on the open-items list as
  "not yet ported."
- `components/styles.py` (new): design tokens + dark theme, base
  reset/typography, the asterism motif, header/nav/brand, buttons,
  hero, and footer, authored natively via `site.style_selector()` /
  registered through `register_styles(site)` in `site.py`. Removed
  the equivalent 52 rule blocks from `assets/site.css` as they were
  ported, so each selector now has exactly one source of truth
  (verified: `grep -c ".eyebrow {"` across both files sums to 1, not
  2).

### Known regression introduced this session
- The original gated `.btn-primary`/`.icon-btn` hover states behind
  `@media (hover: hover) and (pointer: fine)` specifically so a tap on
  a touchscreen doesn't leave the button visually "stuck" inverted.
  `site.style_selector(...)`'s `&:hover` nesting has no equivalent
  device-capability gate to nest inside, so the natively-ported
  `.btn-primary`/`.btn-ghost` hover rules apply unconditionally.
  `assets/site.css` still carries the original's device-gated
  `@media` blocks for `.icon-btn:hover` untouched (left alone since it
  wasn't part of this pass's removal list), so those are unaffected;
  only `.btn-primary`/`.btn-ghost` hover carries this regression.
  Flagged in `docs/PROGRESS.md`, not yet fixed.

## [Unreleased] (original migration entry)

### Added
- Full 8-route site ported to ARKlight (`arklight` alpha, `v0.048`):
  Home, Works, Store, Journal, About, Feedback, Privacy, Terms.
- `content/works.py`, `content/store.py`, `content/journal.py` --
  plain Python data ported 1:1 from the original `src/data/*.ts`.
- `components/nav.py`, `components/footer.py`, `components/work_card.py`,
  `components/common.py` -- shared pieces used across every page.
- `assets/site.css` -- the original `src/styles/main.css` design
  system (warm-paper/ink-teal/brass palette, Fraunces/Work
  Sans/IBM Plex Mono type, the asterism divider motif), linked into
  every page via `Page(links=[...])` rather than reimplemented as
  ARKlight `site.style()` classes.
- Light/dark theme toggle wired via `State("theme", "light")` +
  `Action.toggle_bool` on the Home page's nav.
- Feedback page rebuilt as a set of subject-specific `mailto:` links
  (one per topic), replacing the original's single-form composer.

### Changed
- Header/footer moved to real `Header`/`Footer` tags (ARKlight
  components) so `assets/site.css`'s `header.site-header`/
  `footer.site-footer` tag-qualified selectors still match.
- "Find the stories" list on the About page uses plain rows
  (`Container` per row) instead of `<ul><li>`, since ARKlight's `Item`
  only accepts text/`Bind` children -- a nested `Link` isn't allowed
  inside one. New `.find-stories-list`/`.find-stories-row` CSS rules
  added to `assets/site.css` to match the original `.about-side ul`/
  `li` look.
- Retailer buttons on the Store page render as a single text string
  (`"Amazon ↗"`) rather than a separate `<span class="arrow">`, for
  the same `Link`-is-text-only-children reason. Cosmetic only (loses
  the arrow's independent hover animation).

### Known deviations from the Vue 3 site
- **Feedback form.** No two-way input binding in ARKlight yet
  (`on_input`/`v-model` equivalent is designed as `v0.054`, not
  implemented -- see ARKlight's own `PROGRESS.md`). A
  `<form method="post" enctype="text/plain" action="mailto:...">`
  workaround was evaluated and rejected: its actual behavior (does it
  reliably set the Subject line?) varies by browser/mail client, which
  would be a real per-user regression, not a cosmetic one. Current
  fix: pick-a-topic `mailto:` links, subject pre-filled, free-text
  written directly in the user's email client. No way (yet) to also
  pre-fill the sender's name from the page itself.
- **Theme toggle persistence.** The toggle itself works
  (`Action.toggle_bool`), but the original's `localStorage`
  persistence and pre-paint anti-flash `<head>` script aren't
  reproduced -- no raw-HTML/JS escape hatch in ARKlight's closed
  component API as of `v0.048`. Every page load currently starts in
  light mode regardless of the visitor's last choice.
- **Mobile hamburger nav.** The original's open/close toggle was
  local Vue `ref` state per header instance. Not yet ported --
  `nav.py` always renders the full nav (relies on `assets/site.css`'s
  responsive rules to keep it usable on small screens without JS,
  rather than replicating the show/hide toggle).
- **`v-reveal` scroll-in animations** -- omitted, no ARKlight
  equivalent.
- **PWA (service worker, installability, manifest)** -- not yet
  scoped for the ARKlight build; see `docs/PROGRESS.md`.
- **Capacitor/Android wrapper** -- not yet re-pointed at this build's
  output directory; still targets the Vue site's `dist/`.

## Ordering note

This log will start recording dated entries once the migration
reaches parity and normal iteration begins. Until then, "Unreleased"
is the whole story.
