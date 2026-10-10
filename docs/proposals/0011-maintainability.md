# 0011 — Content workflow and measurement (Stage 4 of the site review)

- **Status:** Implemented — see [changelog](../implementation/changelog.md).
  The analytics open question is resolved (yes, web build only); still
  needs a real Cloudflare beacon token swapped in before it reports
  anything, and the Verification list below hasn't been run in a browser.
- **Priority:** 4 (as time allows)
- **Constraint:** SPA, no runtime dependencies added.

## Problem

- Journal entries are long strings inside `data/journal.ts`, which is
  awkward to write and review.
- There is no way to filter the journal, and the homepage does not
  surface the latest entry.
- There is no measurement of which pages or outbound links readers use.

## Proposed changes

1. **Markdown journal.** One file per entry in `src/data/journal/`
   with front-matter (`date`, `title`, `tag`). Load them with Vite's
   `import.meta.glob('./journal/*.md', { query: '?raw', eager: true })` and
   a tiny front-matter parser in `data/journal.ts`; `JournalEntry` stays
   the type the pages consume, so no component changes.
2. **Tag filter on the Journal page** (SBM / EPMC / STBF) and a
   **latest-entry teaser** on Home linking to `/journal`.
3. **Privacy-friendly analytics.** Cloudflare Web Analytics beacon in
   `index.html` (the site is already on Cloudflare), no cookies. Because
   the Android and desktop builds load the same bundle, decide whether
   to load the beacon only on the web build.

## Non-goals

- No CMS, database or build-time rendering.
- No third-party trackers, no cookies.

## Open questions

- ~~The author is open to analytics but has not committed to it~~ **Decided:
  yes, web build only** (Android and desktop skip it — see changelog).
- ~~Analytics changes what the site collects, so `PrivacyPolicyPage.vue`
  must be updated in the same change~~ Done in the same change; wording
  checked against Cloudflare's current docs (no cookies, no client-side
  state, no PII).
- Migrating existing entries to Markdown is a one-time copy; confirm
  the author is happy to do that review. (Done as a mechanical migration —
  verified byte-for-byte via the RSS feed output — but still worth a quick
  look since it moved every entry's text into a new file.)

## Verification

- All current entries render identically after migration (diff the
  rendered text).
- Filter and teaser work with reduced motion on and in dark theme.
- Analytics script absent from the Android and desktop builds if that
  choice is made.
