# 0012 — Japanese localization

- **Status:** Proposed
- **Priority:** 5 (as time allows)
- **Constraint:** SPA, no runtime dependencies beyond `vue-i18n`; Android
  and desktop builds share the same bundle, so locale switching must work
  identically in all three targets.

## Problem

The site is English-only: every string lives directly in `.vue` templates
or in `src/data/*.ts`, there is no i18n library, `<html lang="en">` is
static, the self-hosted fonts (`Fraunces`, `Work Sans`, `IBM Plex Mono`)
are Latin-only, and SEO surfaces (`router` meta, `structuredData.ts`,
`sitemap.xml`, `index.html`'s OG tags) all assume one language. The author
writes under a Japanese pen name (嵐久 怜) and the audience includes
Japanese readers, but nothing on the site currently serves them in their
language.

This is a large change by content volume, not by code complexity — the
bulk of the work is translating long-form prose (work synopses, About
page, legal pages, journal), not building the switch itself. It is staged
so the infrastructure and short UI strings can ship well before every
paragraph of prose is translated.

## Proposed changes

### Stage 1 — Infrastructure (content still falls back to English)

1. Add `vue-i18n`. Message files at `src/locales/en.json` /
   `src/locales/ja.json`, legacy mode off, `fallbackLocale: 'en'`.
2. **Path-prefixed routing**: `/ja/...` mirrors every existing route
   (`/ja/works`, `/ja/about`, etc.), not a query param or cookie — each
   language stays independently crawlable, and `router/index.ts`'s
   existing per-route `meta.title` / `meta.description` mechanism extends
   naturally to carry a second set of strings keyed by locale.
3. **Detection + persistence**, mirroring `useTheme.ts`'s exact pattern:
   read `navigator.language` once on first visit, persist the choice to
   `localStorage` (`ark-lang`), and set `<html lang>` in `index.html`
   before first paint the same way `data-theme` is set today — so there's
   no flash of the wrong language the way there's no flash of the wrong
   theme.
4. **Switcher** in `AppHeader.vue`, next to the existing theme toggle.
5. **Fonts**: add `@fontsource/noto-sans-jp` for body text; pick a serif
   JP face for headings so the editorial feel `Fraunces` gives isn't lost
   in Japanese (`Fraunces` itself has no CJK glyphs and would silently
   fall back to the system font without this).
6. **Typography overrides**: `:lang(ja)` rules to drop the
   `letter-spacing` and `text-transform: uppercase` used throughout
   `main.css` for eyebrows/labels — both read as mistakes on CJK text.

### Stage 2 — Short UI strings

Extract nav labels, footer, `AppHeader`/`AppFooter` aria-labels,
`FeedbackPage` form (labels, placeholders, status messages), 404 page,
Journal filter buttons, Mood/Work card microcopy into the message files
and translate. Roughly 100–150 short strings; mechanical, no creative
judgment needed.

### Stage 3 — Long-form site copy

Translate the content that needs a real translator, not string
substitution: `works.ts` (3 synopses, taglines, tags, "expect" rows —
~1,500 words), `store.ts` descriptions, Home page hero/section copy,
About page bio. Store translations as parallel fields on the existing
data shapes (e.g. `title`, `title_ja` on `Work`) so `WorkCard.vue` /
`WorksPage.vue` need only a locale-aware accessor, not a rewrite.

### Stage 4 — Legal pages

Terms and Privacy Policy, translated with care for accuracy rather than
tone — these carry real legal weight. Each needs its own "last updated"
handling per locale.

### Stage 5 — SEO surface

- `hreflang` alternates between every `en`/`ja` route pair.
- `structuredData.ts`: `inLanguage` keyed off the active locale instead of
  hardcoded `'en'`.
- `sitemap.xml`: add the `/ja/*` entries.
- `index.html`'s static OG/Twitter tags stay single-language — link-
  preview scrapers don't run JS, so a client-rendered SPA can only ever
  serve one card per URL without prerendering. Known limitation, already
  true of the English-only card today; out of scope for this proposal.

### Stage 6 — Journal (ongoing, not a one-time translation)

Decide per entry whether a Japanese version ships alongside the English
one (front-matter gets `title_ja` / `body_ja`, or a parallel
`NNN-slug.ja.md` file) or the Journal stays English-only with a visible
note that the Japanese translation lags. This is the one piece of content
that keeps growing, so it needs a workflow, not just a migration.

## Non-goals

- No machine-translated content shipped without human review.
- No content fork — Japanese is a translation of the same site, not a
  separately maintained version.
- No change to the Android Play Store listing metadata (separate from
  in-app content). `android/app/.../strings.xml` only holds the proper
  noun `"Rae ARK"` as `app_name` — nothing to translate there.

## Open questions

- Who translates the long-form prose (Stages 3–4) — the author directly,
  or an outside translator plus author review?
- Does the Journal (Stage 6) get translated going forward, or stay
  English-only with a lag notice?
- Ship Stages 1–2 on their own once ready, or hold the whole feature
  behind having all content translated?

## Verification

- Switching language persists across reloads and across routes, with no
  flash of the wrong `<html lang>` on first paint (same check as the
  existing theme flash-prevention).
- Every `/ja/*` route renders with no residual English fallback once its
  stage is complete, and falls back cleanly (not blank) where it isn't.
- `:lang(ja)` typography overrides checked in both light and dark theme.
- `hreflang` tags validate (no self-referencing errors, reciprocal links
  present on both sides of each pair).
- Android and desktop builds carry the same switcher and fonts as the web
  build (shared bundle, so this should be automatic — confirm it is).
