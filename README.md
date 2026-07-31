# ARKfolio — Stage 1 (MVP)

Vue 3 + Vite + TypeScript port of the original static site
([Rae-ARK/My-Portfolio](https://github.com/Rae-ARK/My-Portfolio)). This
stage is deliberately just parity — same look, same content, same pages,
now as components instead of six copy-pasted HTML files.

## What's here

- Router with the original 6 pages: Home, Works, Store, Journal, About, Feedback
- Content (works, journal entries, store listings) lives in `src/data/*.ts` —
  edit those files to update the site, no HTML hunting required
- `src/styles/main.css` is your original `style.css`, relocated as-is
  (class names unchanged, so nothing needed rewriting)
- Mobile nav + active-link highlighting now driven by Vue/vue-router
  instead of manual DOM classList code
- Feedback form's mailto-link logic ported into `src/composables/useFeedbackForm.ts`

## Before you run it

1. **Install dependencies** (this sandbox has no network access, so this
   step has to happen on your machine):
   ```
   npm install
   ```
2. **Copy your images** into `public/assets/images/`:
   - `profile.png`
   - `horizon-ark-logo.png`
   - `Enigmatic Pathways Mystic Circuits vol 1.png`
   - `Summoned By Mistake, I Decided To Learn How To Live Arc 1.png`
   - `The Shadow I Cast Over Two Beautiful Girls Act 1.png`
   (Same filenames as your old `assets/images/` folder — just drag the
   whole folder into `public/assets/images/`.)
3. **Run it**:
   ```
   npm run dev
   ```

## Not in Stage 1 (on purpose)

- No PWA / service worker yet — added in Stage 2 along with a proper
  fix for the `install` listener that had drifted into `script.js`
- No dark theme toggle yet — Stage 2
- No reveal-on-scroll animation yet — Stage 2 (trivial to add back,
  skipped for now to keep this stage boring and verifiable)
- No Capacitor / Android wrapper yet — Stage 3, once this web app is
  confirmed working and matches the old site

## Staged plan (recap)

1. **MVP (this)** — Vue 3 web app, full parity, no extras
2. **Polish** — PWA/offline caching, dark mode, scroll reveal, SEO meta
3. **Android** — Capacitor wrap, touch/safe-area tuning, icon/splash, APK
4. **Later** — Tauri desktop build, any native extras you actually want
