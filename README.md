# ARKfolio — ARKlight Edition

Rae ARK's author site, rewritten on [ARKlight](https://github.com/Rae-ARK/ARKlight)
(alpha branch): Python-authored pages compiled to plain, dependency-free
HTML/CSS/JS — no Vue, no framework runtime shipped to the browser. With
`Site(app_shell=True)` (see "Status" below), internal navigation between
pages now boosts in-place via htmx rather than doing a full page reload,
so the "no client-side router" trade-off from earlier revisions of this
README no longer really applies.

**Original:** [Rae-ARK/ARKfolio](https://github.com/Rae-ARK/ARKfolio) (Vue 3 + Vite + Capacitor)
**Compiler:** [Rae-ARK/ARKlight](https://github.com/Rae-ARK/ARKlight) `alpha`, currently tracking `v0.069` (`v0.06616`)

## Why this migration

ARKfolio's content — works, journal entries, store listings — was already
plain data (`src/data/*.ts`) rendered into static markup at build time.
That's exactly the shape ARKlight is built for: write the structure and
content in Python, get inspectable static HTML out, with none of a
Vue/vue-router runtime's weight along for the ride on what is, page for
page, a static site.

## Status

This is a **migration in progress**, not a finished rewrite, but most of
what blocked full parity earlier has since landed upstream. Tracking
against the original site's 8 routes:

| Page | Status | Notes |
|---|---|---|
| Home | ✅ ported | static content + `on_reveal="reveal"` |
| Works | ✅ ported | static content + `on_reveal="reveal"` |
| Store | ✅ ported | static content + `on_reveal="reveal"` |
| Journal | ✅ ported | static content + `on_reveal="reveal"` |
| About | ✅ ported | static content + `on_reveal="reveal"` |
| Privacy | ✅ ported | static content + `on_reveal="reveal"` |
| Terms | ✅ ported | static content + `on_reveal="reveal"` |
| Feedback | ⚠️ intentionally not 1:1 | see "Known gaps" below — this one's a real, permanent trade-off, not a "not built yet" |

Theme-toggle persistence, scroll-reveal, app-shell navigation, PWA
support, and the Android wrapper are all done — see "Resolved" below.

## Known gaps (why this isn't a 1:1 port)

- **Feedback form.** The original captures a subject, name, and message
  via Vue's two-way `v-model`, then builds a `mailto:` link from them on
  submit. ARKlight's `Input`/`Textarea` *do* support two-way binding now
  (`Bind.model(...)`) — but `Action`'s vocabulary is closed to
  `set`/`increment`/`decrement`/`toggle_bool`/`reset`/`append`/`remove`,
  with nothing to build a URL from state, and `Bind(...)` is only valid
  as an `Action.set`/`.append` *value*, not as an arbitrary component
  prop like `Link(href=...)`. So captured input still can't drive a
  `mailto:` href. This page keeps the original "click your topic"
  static-buttons flow instead (`pages/feedback.py`'s docstring has the
  full reasoning, including why a zero-JS `<form action="mailto:...">`
  was rejected). Revisit if `Action`/`Bind` ever grows a way to read
  live state into a prop.

Nothing above blocks anything else; it's scoped entirely to the
Feedback page's subject-line customization and name pre-fill.

## Resolved

- **Theme toggle persistence.** `State("theme", False, persist=True)`
  on every page — ARKlight's own native `localStorage` round-trip for
  `State(...)`, landed since the last time this README was accurate.
  This replaces the old `components/theme_persist.py` +
  `Site.raw_postprocess(...)` workaround entirely (that escape hatch
  is itself now removed upstream; see `docs/PROGRESS.md`'s changelog
  for the whole story). No extra wiring in `site.py` at all now.
- **Scroll-reveal.** `on_reveal="reveal"` (native as of ARKlight
  `v0.063`) replaces the Vue site's `v-reveal` directive — same
  `is-visible` toggle-class convention, so `assets/site.css`'s reveal
  rules only needed a selector rename
  (`[data-reveal]` → `[data-ark-on-reveal]`, matching what ARKlight's
  JS backend actually emits).
- **App-shell navigation.** `Site(app_shell=True)` in `site.py` boosts
  internal-link clicks via htmx instead of a full page reload. The
  footer is `shell_persistent=True` (safe — nothing in it varies by
  page); the header deliberately isn't, since its active-link
  highlighting is computed per page and would go stale under
  `hx-preserve` — see `components/nav.py`'s docstring.
- **PWA / offline / installable.** `scripts/build.sh` runs
  `arklight build` then `arklight pwa` with the original
  `manifest.json`'s values (name, colors, icon) as far as the CLI's
  flags allow — see that script for what's not expressible yet
  (`description`, `scope`, `id`, `orientation`, a `maskable` icon
  variant) and why `start_url` differs from the original ("/" vs.
  "index.html" — this is a static multi-page build, not an SPA with a
  server-side rewrite).
- **Android wrapper.** Turned out to already be done, just
  undocumented here: `android-project/` is a native
  `arklight android scaffold` output (a plain WebView-based Android
  Studio/Gradle project — *not* Capacitor; the "point Capacitor at
  ARK/ instead of dist/" plan a couple of README revisions ago was
  superseded by this before anyone updated the prose). Regenerated
  as part of this pass so its bundled assets reflect
  the PWA/app-shell/persist changes above — see "Android app" below
  for the regeneration command and a couple of rough edges to know
  about.

## Project structure

Following the pattern used in ARKlight's own reference sites
(`Product-Showcase`, `Data_Viz_With_ARKlight_Alpha_Compiler`):

```
site.py             entry point — registers every @site.page(...) route,
                    app_shell=True for boosted navigation
pages/              one function per route (home, works, store, journal, ...)
components/         shared pieces (nav, footer, work card, styles, ...)
content/            plain Python data — works, journal entries, store listings
                    (ported 1:1 from the original src/data/*.ts)
assets/             images, icons — copied into the build output as-is
scripts/build.sh    arklight build + arklight pwa in one step
android-project/    `arklight android scaffold` output (native WebView app)
tests/              a couple of lightweight sanity checks over pages/*.py
wrangler.jsonc      Cloudflare Workers deploy config
```

## Building

```bash
pip install -e /path/to/ARKlight   # installs the `arklight` package, alpha branch
./scripts/build.sh                 # -> ARK/ — build + PWA manifest/service worker
```

Or, without PWA support: `arklight build site.py -o ARK` on its own is
still a complete, working build — `scripts/build.sh` only exists
because `arklight pwa` is a separate CLI pass over the build output,
not something `Site(...)` can request on its own yet.

Useful flags on the underlying `arklight build`: `-o/--output <dir>`
(default `ARK`), `--no-open` (skip auto-opening the built site),
`--verbose`/`--debug` (stage-by-stage build narration).

## Deploying

Same Cloudflare Workers target as the original:

```bash
./scripts/build.sh
wrangler deploy
```

## Android app

`android-project/` is a real, buildable Android Studio/Gradle project,
generated (not hand-written) by:

```bash
./scripts/build.sh ARK                                       # build + PWA data first --
arklight android scaffold ARK -o android-project --release   # the scaffolder picks up
                                                               # the PWA manifest's app
                                                               # name for the package
                                                               # id if it's there
```

`--release` matches what this repo already had wired up (a signed
release job in CI, gated on repo secrets — see
`android-project/README.md`'s "Building a release APK"). Re-run the
two commands above and re-copy `android-project/` whenever `pages/*.py`
changes meaningfully; nothing about it is hand-maintained.

Two things worth knowing before re-running this:
- **The generated CI workflow doesn't stay at
  `android-project/.github/workflows/`.** GitHub only discovers
  workflow files under the checkout root's `.github/workflows/`, so
  that file (and `android-project/.github/scripts/`) move up to this
  repo's own `.github/`, with `working-directory: android-project`
  added to every Gradle-touching job step and artifact path prefixed
  to match — `.github/workflows/android-build.yml` has the full
  explanation in its header comment. The scaffold's own
  `android-project/README.md` documents this exact situation, so it's
  not a workaround so much as the documented way to use this command
  inside a larger repo.
- **`android-project/README.md` currently says there's no
  release-build job**, in the same breath as documenting one — that's
  a real inconsistency in this alpha's `arklight android scaffold
  --release` output (the README template doesn't seem to branch on
  whether `--release` was passed), not something introduced by this
  repo. Left as-is rather than hand-edited, since it'll be regenerated
  away the next time this command is re-run against a fixed compiler.

## Notes for whoever's touching this next

- Content lives in `content/*.py` — edit those, not the page files, to
  update works/journal/store listings, same philosophy as the original
  `src/data/*.ts`.
- `pages/*.py` follows a bracket-nesting convention ARKlight enforces at
  build time: an opening call's body must be indented deeper than the
  call itself, and no expression tree may nest more than 8 brackets
  deep (pull a repeated or deeply-nested piece into its own module-level
  function instead — see `_status_row()` in `pages/home.py`,
  `_find_stories_row()` in `pages/about.py`, or `_subject_button()` in
  `pages/feedback.py` for the pattern already in use here).
