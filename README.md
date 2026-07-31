<<<<<<< HEAD
# Rae ARK — Author Site

A static author site for web novelist [Rae ARK](https://x.com/Rae7866) — home for three ongoing novels, print editions, and a running journal of the writing process.

No framework, no build step, no dependencies. Plain HTML, CSS, and JavaScript, hosted free on Cloudflare Pages.

---

## 📄 Pages

| Page | File | Purpose |
|---|---|---|
| Home | `index.html` | Hero, featured works, currently-writing status, where to read |
| Works | `works.html` | Full synopses for all three novels |
| Store | `store.html` | Paperback retailer links (grows as titles go to print) |
| Journal | `journal.html` | Timeline of author's notes, drawn from Royal Road afterwords |
| About | `about.html` | Author bio and writing philosophy |
| Feedback | `feedback.html` | Mailto-based contact form with preset subjects |

## 🛠️ Stack

- **HTML/CSS/JS** — no framework, no build tooling
- **Fonts** — Fraunces (display), Work Sans (body), IBM Plex Mono (labels), loaded via Google Fonts `<link>`
- **Hosting** — [Cloudflare Pages](https://pages.cloudflare.com/) (static, free tier)
- Formatted per the [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)
- Progressive enhancement throughout — every interactive feature (mobile nav, feedback form) degrades to a working `<noscript>` fallback if JavaScript fails to load

## 📁 Structure

```
├── index.html
├── works.html
├── store.html
├── journal.html
├── about.html
├── feedback.html
├── style.css          # shared stylesheet, all pages
├── script.js           # shared behavior, all pages
└── assets/
    └── images/          # covers, author photo, imprint logo
```

## 🚀 Deploying

No build command, no output directory beyond the repo root:

1. Connect this repo to Cloudflare Pages
2. **Build command:** leave empty
3. **Output directory:** `/`
4. Deploy

## 📄 License

Code (HTML/CSS/JS) is [MIT licensed](LICENSE) — use it, fork it, build on it.

All written content (synopses, journal entries, author bio) and artwork (covers, logos) are © Rae ARK / Horizon ARK Studio. All rights reserved.
=======
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
>>>>>>> 405de62 (Migrating portfolio in vue 3 framework)
