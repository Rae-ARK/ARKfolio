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
| Feedback            | PARTIAL     | mailto-per-subject links, not a single composer form — see below |
| Theme toggle (UI)   | DONE        | `Action.toggle_bool` + `Bind.when` |
| Theme persistence   | NOT STARTED | needs `localStorage`, no ARKlight hook for it yet |
| Mobile hamburger nav| NOT STARTED | relies on CSS responsive rules only, no JS toggle |
| PWA / offline       | NOT SCOPED  | see open questions |
| Android/Capacitor   | NOT STARTED | wrapper still points at the Vue build's `dist/` |
| CI (`deploy.yml`, `android-build.yml`) | NOT STARTED | still targets the Vue build |

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

1. **Feedback form parity.** Needs ARKlight's `v0.054` (two-way
   input binding — see ARKlight's own `PROGRESS.md`/`CHANGELOG.md`).
   Until then, staying with the per-subject `mailto:` links already
   shipped — a `<form method="post" enctype="text/plain"
   action="mailto:...">` workaround was tried on paper and rejected:
   whether it actually populates the Subject line is inconsistent
   across browsers/mail clients, which would be a real per-visitor
   regression, not just a cosmetic gap.
2. **Theme persistence + anti-flash script.** `Action.toggle_bool`
   flips the class at runtime, but nothing writes it to
   `localStorage`, and there's no pre-paint `<head>` script to avoid
   a flash of the wrong theme on load — ARKlight's component API has
   no raw-HTML/JS escape hatch as of `v0.048`. Best current lead: a
   custom `Backend` using the `postprocess(output_files)` hook (added
   `v0.043`) to inject a small fixed snippet into the built HTML
   files directly, entirely at the Python build-script level, still
   without needing core support. Not yet prototyped.
3. **Mobile hamburger nav.** Original was per-header-instance Vue
   `ref` state. Needs either page-level `State("nav_open", False)`
   threaded through `nav()` (straightforward, just not done yet), or
   a CSS-only checkbox-driven disclosure pattern if we want to avoid
   the JS dependency entirely.
4. **PWA/offline/installable.** Genuinely unscoped — need to check
   whether ARKlight has (or plans) a service-worker/manifest backend
   at all before deciding how this maps over.
5. **Android/Capacitor wrapper.** Should in principle just need
   pointing `npx cap sync android` at this build's output directory
   instead of Vite's `dist/` — not yet verified end to end.
6. **CI (`deploy.yml`, `android-build.yml`).** Needs updating to run
   `arklight build` instead of (or alongside, during the transition)
   the Vite build.

## Session log

Newest first.

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
