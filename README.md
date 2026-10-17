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
| Home | ⚠️ behind `main` | everything but the hero mood-card carousel (never ported; see "Behind `main`") |
| Works | ⚠️ behind `main` | data in sync; the "Official sources" notice box is not ported |
| Store | ⚠️ partly synced | data in sync (incl. the coming-soon Volume 2); the upcoming-print shelf + "I'm waiting for…" buttons and the primary/other retailer split are not ported |
| Journal | ⚠️ partly synced | all 11 entries; no RSS link or per-story tag filter |
| About | ✅ ported | wrong GitHub link and "Arc 3" wording fixed 2026-10-17 |
| Privacy | ⚠️ decision needed | `main`'s copy now discloses Cloudflare Web Analytics; this build runs none — see "Behind `main`" |
| Terms | ✅ ported | date and copy match `main` |
| Feedback | ⚠️ intentionally not 1:1 | permanent composer-form trade-off below; the subject list is now in sync (6 subjects) |

All 8 routes exist and build (checked against ARKlight `v0.70.0`).
"Ported" means "was in step with `main` at the time of the port";
`main` has since moved on. Statuses above come from an audit of this
branch against `main` on 2026-10-17 — see "Behind `main`" below and
`docs/PROGRESS.md`.

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

### Behind `main` (audit, 2026-10-17)

Separate from the permanent Feedback trade-off above: this branch was
last brought to parity before several `main` updates landed (Arc 4,
the mood card, store redesign, journal feed/filter, polish passes).
An audit on 2026-10-17 compared every page, the shared nav/footer, and
all `content/*.py` arrays against `main`. Everything that is purely
*data* was synced the same day; what remains needs template/CSS work
or a decision. None of it is a compiler limitation unless noted.

**Synced 2026-10-17 (data and wiring):**

- `content/site.py` (new) holds the external links (X, YouTube,
  GitHub). The header, footer and About page all read from it, which
  fixes the old `Rae-ARK/My-Portfolio` GitHub link that was
  hardcoded in three places (now `Rae-ARK/ARKfolio`).
- YouTube icon added to the header (`components/nav.py` +
  `components/styles.py`).
- "Arc 3" -> "Arc 4" in `CURRENTLY_WRITING` (`content/works.py`) and
  `CURRENTLY_WRITING_SHORT` (`pages/about.py`). The dated journal
  entry that mentions Arc 3 is correct history and was left alone.
- `content/journal.py`: the two missing entries (*Arc 3 Is Done...*,
  *Unauthorised Copies on a Mirror Site*), so 11 of 11.
- `content/store.py`: Volume 1 description/note wording, per-retailer
  notes (replacing the book-level `retailer_note`), and the
  coming-soon Volume 2 entry. `pages/store.py` renders optional
  `note`, per-retailer notes, and `status: "coming-soon"` (availability
  badge instead of the retailer grid); the Volume 2 cover and the
  badge CSS were copied from `main`.
- `pages/feedback.py`: the two "Waiting for the EPMC / STBF paperback"
  subjects.
- `content/works.py` `WORKS` was diffed against `main` and already
  matched; no change needed.

**Still open:**

- **Home:** `MoodCard.vue` (hero mood-card carousel, `main`'s proposal
  0009) was never ported and was not previously logged as a gap.
- **Works:** the "Official sources" notice box. It can be derived
  from `WORKS[*]["links"]` the way `main` does, but needs its CSS
  (`.official-sources`) ported.
- **Store template:** the "Still to come" shelf for EPMC/STBF with
  "I'm waiting for ..." buttons (needs `.print-card` /
  `.upcoming-shelf` CSS, and the Feedback page to accept a subject),
  and the primary-retailer button vs. "Other retailers" grouping.
  `NOT_YET_IN_PRINT_NOTE` keeps its arklight-specific wording until
  that lands.
- **Journal:** "Follow by RSS" link (`/feed.xml`) and the per-story tag
  filter (all / SBM / EPMC / STBF). The filter may run into the closed
  `Action`/`Show` vocabulary; check `arklight search` first.
- **Privacy — decision needed, not a plain sync.** `main`'s "What's
  collected" paragraph now says the web version uses Cloudflare Web
  Analytics (and that the Android/desktop apps don't). This build runs
  no analytics, so its current "does not run analytics" wording is
  accurate as it stands, and the "last updated" date
  (`"July 2026"`; `main` says `"October 2026"`) was deliberately *not*
  bumped. Port the copy and date only if this build is also going to
  load the beacon. (For reference, `main`'s `src/native/analytics.ts`
  currently has a placeholder beacon token.)
- **Footer (decision):** `main`'s footer is the quote, attribution,
  imprint and Feedback/Privacy/Terms only; this one adds the full nav
  plus X and GitHub. Match `main` or keep it on purpose and say why.
- **Not audited yet:** `main`'s `NotFoundPage.vue` (no 404 route is
  registered here), SEO/structured data (`src/seo/*`), and the
  generated `feed.xml` (`scripts/build-feed.mjs`). Minor: `main`
  renamed the STBF cover to "...Two Beautiful *Flowers*..."; this
  branch still uses the old "...*Girls*..." filename (works, just
  inconsistent).

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
                    (ported 1:1 from the original src/data/*.ts); site.py
                    holds the shared external links (X, YouTube, GitHub)
assets/             images, icons — copied into the build output as-is
scripts/build.sh    arklight build + arklight pwa in one step
android-project/    `arklight android scaffold` output (native WebView app)
tests/              a couple of lightweight sanity checks over pages/*.py
```

No `wrangler.jsonc` here — unlike the original Vue site, this project has
none checked in, and doesn't need one: `arklight deploy` (see "Deploying"
below) fills in a minimal Workers config (assets directory, Worker name,
compatibility date) itself when a project doesn't already have one.

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

Same Cloudflare Workers target as the original, but handed off through
ARKlight's own CLI rather than a bare `wrangler deploy` — this project has
no `wrangler.jsonc` checked in, so a bare `wrangler deploy` has no config
to read and nothing to deploy from. `arklight deploy` builds the site
first, then runs Wrangler itself, filling in a minimal Workers config
(assets directory, Worker name, compatibility date) since none exists:

```bash
arklight deploy
```

Needs Wrangler on `PATH` and signed in (`npm install --global wrangler &&
wrangler login`) — ARKlight hands the deploy off to Wrangler, it doesn't
install or authenticate it. Note this skips the `arklight pwa` pass
`scripts/build.sh` also runs, so a manifest/service-worker refresh needs
`./scripts/build.sh` run once beforehand if either has changed.

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
