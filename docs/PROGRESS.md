# ARKfolio (ARKlight Edition) — Progress

Living document tracking what's ported, what's deliberately different
from the Vue 3 site, and what's still open. Update this at the end of
every work session. For the plain version-history record, see
[`CHANGELOG.md`](./CHANGELOG.md).

## Snapshot

| Page/Feature       | Status      | Notes |
|---------------------|-------------|-------|
| Home                | DONE        | hero, 3 work cards, currently-writing panel, pull quote, "where to read" |
| Works               | DONE        | full synopses, content notices, expect/don't-expect rows |
| Store               | DONE        | paperback listing, retailer grid |
| Journal             | DONE        | 9 entries, newest first |
| About               | DONE        | bio + sidebar; "find the stories" list restructured, see below |
| Privacy             | DONE        | static legal copy |
| Terms               | DONE        | static legal copy |
| Feedback            | PARTIAL, on purpose | mailto-per-subject links; not a single composer form, and now confirmed that isn't reachable at all yet — see below |
| Theme toggle (UI)   | DONE        | `Action.toggle_bool` + `Bind.when` |
| Theme persistence   | DONE        | native `State(persist=True)` — see below |
| Mobile hamburger nav| DONE        | native `"toggle"` behavior, no `State` needed |
| Scroll-reveal        | DONE        | native `on_reveal="reveal"` (`v0.063`) — see below |
| App-shell navigation | DONE        | `Site(app_shell=True)` + `shell_persistent` footer — see below |
| PWA / offline       | DONE        | `scripts/build.sh` → `arklight pwa` |
| Android             | DONE        | native `arklight android scaffold` output in `android-project/` (not Capacitor) |
| CI (`android-build.yml`) | DONE   | regenerated + re-adapted for the `android-project/` nesting; `deploy.yml` (Cloudflare) still TODO |
| Native CSS (design tokens, reset, header/nav, buttons, hero, footer) | DONE | `components/styles.py`, via `site.style_selector()` |
| Native CSS (work cards, journal, store, about, legal, feedback) | NOT STARTED | still in `assets/site.css` |

## Design decisions

- **CSS: ported the whole stylesheet, not hand-translated.**
  `assets/site.css` is the original `src/styles/main.css`, close to
  verbatim, linked into every page via `Page(links=[{"rel":
  "stylesheet", "href": "/assets/site.css"}, ...])`. This is
  ARKlight's own structured `<head>` extension point (`v0.048` Stage
  A), not a raw-HTML escape hatch — it was evaluated against manually
  reimplementing every rule as `site.style()` calls and rejected as
  both slower and less faithful; `site.style()`'s dict-of-rules API
  doesn't support the descendant/sibling combinators the original
  relies on throughout. A handful of small addendum rules were
  appended at the bottom of the file for ARKlight-specific structural
  substitutions (see the two points below).
- **Header/Footer use real `Header`/`Footer` tags**, not generic
  `Container`s, specifically so `assets/site.css`'s tag-qualified
  selectors (`header.site-header`, `footer.site-footer`) keep
  matching without editing the CSS.
- **`Link` can't nest other components** (`arklight/ir/schema.py`:
  `text_only_children=True`, allows text or `Bind` only). This broke
  three places from the original markup, each resolved differently:
  - Avatar-links-to-`/about` in the nav — avatar is now a
    plain, non-clickable `Image`; only the site name text links.
  - Retailer buttons on Store (`<a><span>Amazon</span><span
    class="arrow">↗</span></a>`) — collapsed into one text string
    (`"Amazon ↗"`). Loses the arrow's independent hover animation;
    cosmetic only.
  - "Find the stories" list on About — `Item` (`<li>`) has the same
    text-only restriction, so a `Link` can't nest inside one either.
    Replaced `List`/`Item` with plain `Container` rows styled to
    match the original `.about-side ul`/`li` look (new
    `.find-stories-list`/`.find-stories-row` rules in
    `assets/site.css`).

## Open items, in rough priority order

1. **Native CSS port, remaining pages.** Work cards, journal timeline,
   store/retailer grid, about/legal/feedback styling is still in
   `assets/site.css` rather than `components/styles.py`. Same pattern
   as the pieces already ported -- next in line by page traffic/
   visual weight would be work cards (Home + Works) and the footer's
   sibling `.journal-card`/`.about-side` family.
2. **Hover-state device gating regression.** `.btn-primary`/
   `.btn-ghost`'s native `&:hover` isn't gated behind `@media (hover:
   hover) and (pointer: fine)` the way the original was, risking a
   "stuck hover" look after a tap on touchscreens. Needs checking
   whether `style_selector()` supports an `@media`-wrapped variant, or
   another way to reintroduce the gate natively. Still open -- the
   `v0.048`→`v0.069` upgrade pass didn't touch this.
3. **CI (`deploy.yml`).** The Cloudflare Workers deploy workflow still
   needs to run `./scripts/build.sh` instead of a Vite build (the
   Android CI side of this item, `android-build.yml`, is now done --
   see the session log below).
4. **`arklight android scaffold --release`'s README/workflow
   mismatch.** Filed against upstream, not this repo: the generated
   `android-project/README.md` says "there is deliberately no
   release-build job here" even when `--release` was passed and the
   workflow it generates in the same run *does* include one. Re-check
   next time this command is re-run against a newer compiler.

**Resolved since the last pass** (was open items 1, 2, 4, 5 above --
see the session log below for how):
- Feedback form parity -- turned out to be a dead end even with
  two-way binding now shipped (see `pages/feedback.py`'s docstring),
  so this is closed as "working as intended," not "still open."
- Theme persistence + anti-flash script -- solved natively,
  `components/theme_persist.py` deleted.
- PWA/offline/installable -- scoped and shipped (`arklight pwa`).
- Android/Capacitor wrapper -- turned out to not need Capacitor at
  all; already-generated `android-project/` regenerated fresh.

## Session log

Newest first.

### ARKlight upgrade: `v0.048` → `v0.069` (`v0.06616`) -- parity pass

Pulled `ARKlight` `alpha` all the way from `v0.048` to the current
`v0.06616` in one jump (see ARKlight's own `CHANGELOG.md` for
everything in between) and used what that unlocked to close out most
of the open items list below.

- **Bracket-nesting bugs, pre-existing.** Before any of the actual
  feature work below would even build: every `pages/*.py` file had the
  outer `Page(... Container(...) ...)` body indented flush with
  `Container(`'s own opening line rather than deeper -- valid under
  whatever compiler version this was originally authored against,
  rejected by the current one's stricter bracket-indentation check.
  Fixed by reindenting each file's outer `Container(...)` block by one
  level. Separately, `home.py`'s "Currently Writing" status panel and
  `about.py`'s "Find the stories" list both then turned out to nest 9
  levels of brackets deep -- one past ARKlight's readability cap.
  Pulled each into its own module-level helper function
  (`_status_row()`, `_find_stories_row()`), same fix the compiler's
  own error message suggests, and the same pattern this codebase
  already used for `_book()`/`_entry()`/`work_card()`.
- **Theme persistence: native at last.** `State(..., persist=True)`
  shipped upstream since `v0.048` -- `State("theme", False,
  persist=True)` on every page replaces the entire
  `components/theme_persist.py` + `Site.raw_postprocess(...)`
  mechanism (both deleted, along with its test,
  `tests/test_theme_persist.py`, replaced with a much smaller
  `tests/test_theme_state_persist.py` that just checks every page
  actually sets `persist=True` and not the default `False`). This
  also sidesteps `raw_postprocess`'s own removal in this same
  version range -- calling it now is a silent no-op, so this would
  have broken outright on upgrade even without the parity push.
- **Scroll-reveal: native as of `v0.063`.** `on_reveal="reveal"`
  matches the Vue site's `v-reveal` directive attribute-for-attribute
  (same `is-visible` default toggle class), added to every section
  that had `v-reveal` in the original. `assets/site.css`'s existing
  (already-ported, previously dead) reveal rules only needed their
  selector renamed from `[data-reveal]` to what ARKlight's JS backend
  actually emits, `[data-ark-on-reveal]`.
- **App-shell navigation.** `Site(app_shell=True)` in `site.py`. Footer
  marked `shell_persistent=True` (stable `id`, no per-page state to go
  stale). Header deliberately left non-persistent -- its active-link
  class is computed per page at build time, and `hx-preserve` would
  freeze it on whatever page the visitor first landed on. Documented
  in `components/nav.py`'s docstring so it doesn't look like an
  oversight to whoever touches this next.
- **`raw_postprocess` → `script-extension`/`Backend.postprocess()`
  research, then not used.** Read ARKlight's own experimental-APIs
  doc expecting to migrate onto `ScriptExtension`
  (`site.register_script_extension(...)`) for the anti-flash script.
  Worked through the actual ordering semantics (deferred
  `arklight.js`'s top-level code runs before the
  `DOMContentLoaded`-gated `arkInitPage()`, so a `ScriptExtension`
  *would* have worked for the initial-load case -- but its
  `htmx:afterSettle`-driven re-init on every boosted navigation, once
  `app_shell=True` is on, would have raced the correction script
  against the very re-init it needed to run before, since
  `ScriptExtension` can only append code, never run before what's
  already in `arklight.js`). Moot in the end: `State(persist=True)`
  covers the same need natively and sidesteps the ordering problem
  entirely, so `ScriptExtension` was never actually wired in. Leaving
  this note in case a future need for it comes up -- the ordering
  gotcha above is real and worth knowing before reaching for it.
- **PWA support.** New `scripts/build.sh`, wrapping
  `arklight build` + `arklight pwa` with the original `manifest.json`'s
  values translated onto `arklight pwa`'s flags as closely as they go
  (see the script's comments for what's not expressible yet).
- **Android wrapper.** Turned out `android-project/` was already a
  real, native `arklight android scaffold` output (WebView-based, not
  Capacitor) -- the README describing a Capacitor plan predated it and
  was just never updated. Regenerated via
  `./scripts/build.sh ARK && arklight android scaffold ARK -o
  android-project --release` so the bundled HTML/JS/CSS reflect
  everything above, and reapplied the same `.github/workflows/`
  root-relocation + `working-directory: android-project` adaptation
  the previous scaffold already had by hand (the freshly generated
  `android-project/README.md` documents this exact situation, so it's
  the tool's own recommended approach, not a one-off workaround).
  Noted, but didn't attempt to fix, an inconsistency in this alpha's
  own scaffold output: with `--release`, the generated README still
  says "there is deliberately no release-build job here" in the same
  breath as documenting the one that *is* in the generated workflow.
- Full rebuild + `pytest tests/` green after every step above.

### 2026-08-27 (later) — ARKlight upgrade: nav toggle + native CSS
- Pulled `ARKlight` `alpha` from `v0.048` to `v0.0501`. See
  `CHANGELOG.md` for the two capabilities this unlocked
  (`Site.style_selector`, named `"toggle"` behavior).
- Mobile hamburger nav: done, via the native `"toggle"` behavior.
  Removed from the open-items list.
- Native CSS port, first pass: design tokens/dark theme, base
  reset/typography, asterism motif, header/nav/brand, buttons, hero,
  footer -- moved from `assets/site.css` into `components/styles.py`
  (`site.style_selector()` calls), with the ported rules removed from
  the external file so there's one source of truth per selector.
  Verified via `grep -c` across both files that no selector is now
  defined twice.
- **Regression, not yet fixed:** the original's `.btn-primary`/
  `.btn-ghost` hover states were gated behind `@media (hover: hover)
  and (pointer: fine)` to avoid a "stuck hover" look on tap. The
  native `&:hover` nesting syntax has no device-capability gate to
  nest inside, so this pass's ported hover rules apply
  unconditionally. Needs either an `@media`-wrapped
  `site.style_selector()` call (if that combination is even
  supported -- not yet checked) or accepting the regression until it
  is.
- Remaining page-specific styling (work cards, journal timeline,
  store/retailer grid, about/legal/feedback) intentionally left in
  `assets/site.css` for this pass -- lower structural priority than
  the pieces above, queued as the next native-CSS chunk.

### 2026-08-27 — Full 8-page port
- Ported all remaining pages (Works, Store, Journal, About, Feedback,
  Privacy, Terms) on top of the earlier Home-page scaffold.
- Ported `src/styles/main.css` wholesale into `assets/site.css`,
  linked via `Page(links=[...])` on every page, instead of hand-
  translating into `site.style()` calls.
- Switched `nav()`/`footer()` to real `Header`/`Footer` tags so the
  CSS's tag-qualified selectors keep matching.
- Hit and resolved three `Link`-can't-nest-children breakages (avatar
  link, retailer button arrow, About's "find the stories" list) — see
  "Design decisions" above.
- Built end-to-end with `arklight build site.py -o ARK` — 8 HTML
  files + `styles.css` + `arklight.js` + `assets/site.css` +
  `assets/images/*`, zero validation warnings.
- Feedback form: evaluated and rejected the `enctype="text/plain"`
  mailto-form trick; shipped static per-subject `mailto:` links
  instead, pending `v0.054`.

### Earlier — Home page scaffold
- Initial `site.py`/`components/`/`content/works.py`/`pages/home.py`
  scaffold, established the project layout (mirroring ARKlight's own
  `Product-Showcase`/`Data_Viz_With_ARKlight_Alpha_Compiler` reference
  sites), and confirmed a first real `arklight build` succeeds.
