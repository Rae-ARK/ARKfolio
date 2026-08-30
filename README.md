# ARKfolio — ARKlight Edition

Rae ARK's author site, rewritten on [ARKlight](https://github.com/Rae-ARK/ARKlight)
(alpha branch): Python-authored pages compiled to plain, dependency-free
HTML/CSS/JS — no Vue, no client-side router, no framework runtime shipped
to the browser.

**Original:** [Rae-ARK/ARKfolio](https://github.com/Rae-ARK/ARKfolio) (Vue 3 + Vite + Capacitor)
**Compiler:** [Rae-ARK/ARKlight](https://github.com/Rae-ARK/ARKlight) `alpha`, currently tracking `v0.048`

## Why this migration

ARKfolio's content — works, journal entries, store listings — was already
plain data (`src/data/*.ts`) rendered into static markup at build time.
That's exactly the shape ARKlight is built for: write the structure and
content in Python, get inspectable static HTML out, with none of a
Vue/vue-router runtime's weight along for the ride on what is, page for
page, a static site.

## Status

This is a **migration in progress**, not a finished rewrite. Tracking
against the original site's 8 routes:

| Page | Status | Notes |
|---|---|---|
| Home | ✅ ported | static content |
| Works | ✅ ported | static content |
| Store | ✅ ported | static content |
| Journal | ✅ ported | static content |
| About | ✅ ported | static content |
| Privacy | ✅ ported | static content |
| Terms | ✅ ported | static content |
| Feedback | ⚠️ in progress | see "Known gaps" below |

Theme toggle, PWA/offline support, and the Android wrapper are being
migrated alongside the pages themselves — see "Known gaps."

## Known gaps (why this isn't a 1:1 port yet)

ARKlight is alpha software, and a few things ARKfolio relies on aren't
in the compiler yet:

- **Feedback form.** The original uses two-way input binding
  (`v-model`) to build a `mailto:` link from typed text. ARKlight's
  JS backend only wires up `on_click` today — `on_input`/two-way
  binding is designed (`v0.054`) but not implemented. Current plan:
  a plain `<form method="post" enctype="text/plain" action="mailto:...">`,
  which composes the email client without needing any reactive JS at
  all. Being validated.
- **Theme toggle persistence.** `Action.toggle_bool` + `Bind.when(...)`
  can flip a light/dark class at runtime, but the original's
  anti-flash inline `<head>` script and `localStorage` persistence
  don't fit ARKlight's closed component API (no raw-HTML escape
  hatch as of `v0.048`). Likely path: a small custom `Backend` using
  the `postprocess(output_files)` hook to inject the snippet at build
  time, rather than waiting on core support.
- **PWA / offline / installable.** ARKfolio ships a service worker +
  manifest for offline use and installability. Whether/how this maps
  onto an ARKlight build is still being scoped.
- **Android wrapper.** Capacitor just needs a static output directory,
  so this *should* carry over by pointing it at ARKlight's build
  output instead of Vite's `dist/` — not yet verified end to end.

Nothing above blocks the content pages; it only affects the feedback
form, theme persistence, PWA, and the native wrapper hookup.

## Project structure

Following the pattern used in ARKlight's own reference sites
(`Product-Showcase`, `Data_Viz_With_ARKlight_Alpha_Compiler`):

```
site.py          entry point — registers every @site.page(...) route
pages/           one function per route (home, works, store, journal, ...)
components/      shared pieces (nav, footer, work card, ...)
content/         plain Python data — works, journal entries, store listings
                 (ported 1:1 from the original src/data/*.ts)
assets/          images, icons — copied into the build output as-is
wrangler.jsonc   Cloudflare Workers deploy config
```

## Building

```bash
pip install -e /path/to/ARKlight   # installs the `arklight` CLI, alpha branch
arklight build site.py -o ARK      # -> ARK/index.html etc.
python scripts/postbuild_theme_persist.py ARK   # patches ARK/*.html in place
```

Useful flags: `--verbose` (prints each pipeline stage as it runs),
`--debug` (full traceback on failure), `--no-open` (skip auto-opening
the built site).

The `postbuild_theme_persist.py` step is required, not optional: until
ARKlight grows a `postprocess(output_files)`/raw-HTML-escape-hatch hook
(see "Known gaps" above), theme persistence is implemented entirely as
a post-build HTML patch, not as anything `arklight build` emits on its
own. Skipping it silently ships a build where the theme toggle works
within a page but resets to light on every navigation. It's idempotent
and safe to re-run against the same `ARK/` directory.

## Deploying

Same Cloudflare Workers target as the original:

```bash
arklight build site.py -o ARK
python scripts/postbuild_theme_persist.py ARK
wrangler deploy
```

## Android app

Unchanged in principle: Capacitor wraps a static output directory. Once
the ARKlight build is verified end to end, `npx cap sync android` points
at `ARK/` instead of `dist/`. The native-only behavior (hardware back
button, status bar theme sync, external links via Chrome Custom Tabs)
stays in the Capacitor shell — it's orthogonal to whatever generates the
HTML underneath.

## Notes for whoever's touching this next

- Content lives in `content/*.py` — edit those, not the page files, to
  update works/journal/store listings, same philosophy as the original
  `src/data/*.ts`.
- This README will get trimmed down once the "Known gaps" section is
  empty — until then, treat it as the migration's live status doc as
  much as a usual project README.
