# ARKfolio

Vue 3 + Vite + TypeScript author site for Rae ARK, shipped three ways:
as a website, as an installable PWA, and as a native Android app via
Capacitor.

**Repo:** [Rae-ARK/My-Portfolio](https://github.com/Rae-ARK/My-Portfolio)

## What's here

- Router with 8 pages: Home, Works, Store, Journal, About, Feedback,
  Privacy, Terms
- Content (works, journal entries, store listings) lives in `src/data/*.ts`
  — edit those files to update the site, no HTML hunting required
- Light/dark theme toggle (`src/composables/useTheme.ts`), persisted
  per-device
- PWA: offline-capable via a service worker, installable, manifest +
  icons in `public/`
- `src/native/nativeShell.ts` — everything that makes the Android build
  feel native rather than "a website in a box": hardware back button
  wired to app navigation, status bar icon color synced to the theme,
  safe-area-aware layout for edge-to-edge Android, external links
  (Royal Road, Scribble Hub, X) opening in Chrome Custom Tabs instead of
  hijacking the app's own WebView. All of it is a no-op on the web build.

## Local development

```bash
npm install
npm run dev        # http://localhost:5173, hot reload
```

```bash
npm run build       # type-checks (vue-tsc) + builds to dist/
npm run preview      # serve the production build locally
```

## Deploying the site

Hosted on Cloudflare Workers (static assets + SPA fallback, see
`wrangler.jsonc`).

```bash
npm run deploy       # builds, then `wrangler deploy`
```

There's also a `.github/workflows/deploy.yml` for push-to-deploy — it's
manual-trigger only until `CLOUDFLARE_API_TOKEN` is added under this
repo's *Settings → Secrets and variables → Actions*. Once that's set,
switch its `on:` block from `workflow_dispatch` to
`push: branches: [main]`.

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

```
src/
  components/   AppHeader, AppFooter, WorkCard, ...
  composables/  useTheme, useScrollReveal, useFeedbackForm
  data/         works.ts, journal.ts, store.ts — edit these to update content
  native/       nativeShell.ts — Capacitor/Android-only behavior
  pages/        one .vue file per route
  router/       route table + per-page <title>/meta
  styles/       main.css — warm-paper / ink-teal / brass design system
```

## Notes for whoever's touching this next

- `node_modules/` and `dist/` are gitignored — don't re-add them; both
  regenerate from `npm install` / `npm run build`.
- The Android SDK build in CI targets `compileSdk 36` (Android 16),
  which enforces edge-to-edge display and no longer honors
  `StatusBar.setBackgroundColor` / `overlaysWebView` — layout relies on
  `env(safe-area-inset-*)` CSS instead (see `src/styles/main.css`).
- Legal pages (`/privacy`, `/terms`) exist mainly because the Play Store
  requires a privacy policy link for any app requesting permissions —
  update the contact email in `PrivacyPolicyPage.vue` if it changes.
