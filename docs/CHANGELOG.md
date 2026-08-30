# Changelog

All notable changes to the ARKlight edition of ARKfolio, in one running
list. Dates are UTC.

## [Unreleased]

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
