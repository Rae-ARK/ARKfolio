# ARKfolio

Svelte 5 + SvelteKit + TypeScript author site for Rae ARK, shipped three
ways: as a website, as an installable PWA, and as a native Android app
via Capacitor.

**Repo:** https://github.com/Rae-ARK/ARKfolio

## What's here

- SvelteKit file-based routing with 8 pages: Home, Works, Store, Journal,
  About, Feedback, Privacy, Terms
- Content (works, journal entries, store listings) lives in
  `src/lib/data/*.ts` — edit those files to update the site, no page
  hunting required
- Svelte 5 runes for reactive state and client-side interactivity
- Light/dark theme toggle, persisted per-device
- PWA: offline-capable via a service worker, installable, manifest +
  icons in `static/`
- `src/lib/native/nativeShell.ts` — everything that makes the Android
  build feel native rather than "a website in a box": hardware back
  button wired to app navigation, status bar icon color synced to the
  theme, safe-area-aware layout for edge-to-edge Android, external links
  (Royal Road, Scribble Hub, X) opening in Chrome Custom Tabs instead of
  hijacking the app's own WebView. All of it is a no-op on the web build.

## Local development

```bash
npm install
npm run dev        # http://localhost:5173, hot reload
npm run check       # Svelte/TypeScript checks
npm run build       # builds the production site
npm run preview     # serve the production build locally
```

## Deploying the site

Hosted on Cloudflare Workers using SvelteKit's static adapter
(`@sveltejs/adapter-static`).

The production build outputs the static site to `build/`.

```bash
npm run build
```

There's also a `.github/workflows/deploy.yml` for push-to-deploy — it's
manual-trigger only until `CLOUDFLARE_API_TOKEN` is added under this
repo's *Settings → Secrets and variables → Actions*. Once that's set,
switch its `on:` block from `workflow_dispatch` to
`push: branches: [main]`.

## Status

Work in Progress.

The goal is to first port the website.

## Android app

Wrapped with [Capacitor](https://capacitorjs.com/). The `android/`
directory is a real, checked-in Android Studio project — open it
directly if you want the IDE, or use the npm scripts below.

```bash
npm run android:sync    # build web app, copy into the Android project
npm run android:open    # ...then open Android Studio
npm run android:build   # ...then build a debug APK via Gradle
```

The debug APK also builds automatically in CI on every push to `main` —
see `.github/workflows/android-build.yml` and the **Actions** tab on
GitHub for a downloadable artifact, no local Android SDK required.

App id: `com.raeark.arkfolio`. Icons/splash live under
`android/app/src/main/res/`; brand colors are defined in
`android/app/src/main/res/values/colors.xml`.

## Project structure

```text
src/
  lib/
    components/   AppHeader, AppFooter, WorkCard, ...
    data/         works.ts, journal.ts, store.ts — edit these to update content
    native/       nativeShell.ts — Capacitor/Android-only behavior
    styles/       main.css — warm-paper / ink-teal / brass design system
  routes/
    +layout.svelte
    +page.svelte
    works/
      +page.svelte
    store/
      +page.svelte
    journal/
      +page.svelte
    about/
      +page.svelte
    feedback/
      +page.svelte
    privacy/
      +page.svelte
    terms/
      +page.svelte
```

SvelteKit's filesystem-based routing replaces the Vue Router setup used
by the previous version of ARKfolio. Route-specific metadata can be
defined alongside each route using SvelteKit's page/layout conventions.

## Svelte 5

This branch uses Svelte 5 and its runes-based reactivity system.

Client-side interactive state should generally use Svelte 5 runes such
as:

```ts
let count = $state(0);
let doubled = $derived(count * 2);
```

Effects that need to interact with browser APIs or other external
systems should use `$effect`.

SvelteKit handles routing, rendering, and the application shell, while
Svelte handles component-level client-side interactivity.

## PWA

PWA assets are kept under `static/` so they are copied directly into the
generated static site.

```text
static/
  manifest.webmanifest
  sw.js
  icons/
  assets/
```

The service worker and manifest are framework-independent and should not
need Svelte-specific changes.

## Native Android behavior

`src/lib/native/nativeShell.ts` contains behavior specific to the
Capacitor Android build.

It handles:

* Hardware back-button navigation
* Android status-bar icon appearance
* Safe-area handling for edge-to-edge Android
* External links through Chrome Custom Tabs
* Native-only behavior guarded so the web build remains unaffected

The native shell is initialized from the SvelteKit root layout using the
appropriate client-side lifecycle hook.

## Notes for whoever's touching this next

* `node_modules/` and `build/` are gitignored — don't re-add them; both
  regenerate from `npm install` / `npm run build`.
* SvelteKit uses `src/routes/` for routing. Do not recreate the old
  Vue `src/pages/` or `src/router/` structure.
* Shared application code belongs under `src/lib/`.
* Static files that need to be served unchanged belong under `static/`.
* The Android SDK build in CI targets `compileSdk 36` (Android 16),
  which enforces edge-to-edge display and no longer honors
  `StatusBar.setBackgroundColor` / `overlaysWebView` — layout relies on
  `env(safe-area-inset-*)` CSS instead (see
  `src/lib/styles/main.css`).
* Legal pages (`/privacy`, `/terms`) exist mainly because the Play Store
  requires a privacy policy link for any app requesting permissions.
  Update the contact email in the privacy page if it changes.
* This branch is a Svelte 5 migration of the original Vue implementation.
  When porting functionality, preserve existing behavior first and
  simplify or refactor only after the Svelte implementation is working.

```
