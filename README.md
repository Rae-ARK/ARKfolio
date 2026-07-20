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