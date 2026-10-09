# Changelog

Shipped changes that resolve a proposal or an audit finding. Newest first.

## 2026-10-09

### Header nav collapses at 900px — proposal [0003](../proposals/0003-header-nav-breakpoint-bug.md)

- The hamburger menu now takes over at `max-width: 900px` (previously
  `700px`), so the full nav and icon group no longer crowd the brand just
  above phone width.
- `.brand-row` no longer shrinks; the brand name and the
  "嵐久 怜 · WEB NOVELIST" subtitle no longer wrap.
- Between 701px and 900px the mobile dropdown uses 32px side padding to
  match `.wrap`; at 700px and below it stays at 20px.
- Files: `src/styles/main.css`.
- **Not yet verified in a browser.** The 900px value is an estimate from the
  CSS; check 700-1000px.

### Paperback card on the home page — proposal [0002](../proposals/0002-paperback-card-on-home.md)

- Added a **Paperback** card to the Where to Read section, linking to
  `/store` ("Summoned by Mistake, Vol. 1 →").
- Uses `→` rather than `↗` because the link is internal (see
  [audit finding 2](ui-ux-audit.md)).
- Files: `src/pages/HomePage.vue`.
- The section heading ("Every chapter, free, wherever you already read") was
  left unchanged.

### GitHub links point to `ARKfolio` — audit finding 9

- Header, footer and About page links updated in `ecbf336`.
- `README.md` still references `Rae-ARK/My-Portfolio`.
