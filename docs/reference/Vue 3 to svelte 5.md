# Run down

~1,167 lines of Vue/TS across 21 files, plus 1,358 lines of CSS and ~106 lines of PWA config (manifest + service worker).

Splitting by how much actually has to change:

## Copy-paste, near zero work (~1,500 lines, but free)

- `src/styles/main.css` (1,358 lines) — pure CSS, framework-agnostic, copies straight over.
- `src/data/works.ts`, `journal.ts`, `store.ts` (214 lines) — plain TS objects/arrays, no Vue in them at all.
- `public/manifest.webmanifest`, `sw.js`, `icons` — unchanged.
- Images in `assets/`

## Mechanical translation (~610 lines)

8 pages (460 lines) + 3 components (150 lines): `AppHeader`, `AppFooter`, `WorkCard`.

Mostly `<template>` → markup and `<script setup>` → `<script>` syntax swaps. Nothing structurally different.

This is the bulk of the "typing," not the thinking.

## Actual rework (~265 lines, but conceptually different)

- `useTheme.ts`, `useScrollReveal.ts`, `useFeedbackForm.ts` (110 lines) — `ref`/`computed`/`watch` → `$state`/`$derived`/`$effect`. Small files, but you're rethinking reactivity, not just retyping it.
- `router/index.ts` (114 lines) — this one doesn't port at all. It gets deleted. SvelteKit's file-based routing replaces it; the per-page `<title>`/meta logic moves into each `+page.svelte`/`+page.ts`.
- `nativeShell.ts` (79 lines) — plain TS, should port nearly as-is. It just needs to be wired into a Svelte lifecycle hook (`onMount` in the root layout) instead of wherever it's currently called from `main.ts`/`App.vue`.

## To Do

1. **Wire up the shell**
   - Import `$lib/styles/main.css` into `src/routes/+layout.svelte`.
   - Port `AppHeader`/`AppFooter` into it so every page gets them for free.
   - This replaces what Vue's `App.vue` was doing.

2. **`useTheme` as a rune**
   - Do this before any pages, since the header/footer and page backgrounds likely read it.

3. **One full page end-to-end**
   - Pick `WorksPage`, since it exercises the most patterns:
     - Data import
     - `WorkCard` component
     - Routing
   - Once that pattern is proven, the other 7 pages should be mostly repetitive.

4. **Remaining 7 pages + `WorkCard`**
   - Mechanical conversion once the page pattern is established.

5. **`useScrollReveal` and `useFeedbackForm`**
   - Convert these as the pages that need them are ported.

6. **`nativeShell.ts` wiring**
   - Call it from the root layout's `onMount`.
   - Gate it so it's a no-op on web, matching its existing behavior.

7. **Android re-verification**
   - Run the equivalent of `android:sync`.
   - Check safe-area handling and status-bar behavior.