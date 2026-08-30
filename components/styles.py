"""The site's design tokens and core layout system, authored natively
via ARKlight's `Site.style_selector`/`style`/`keyframes` API (added
after v0.048 -- see docs/PROGRESS.md's "ARKlight upgrade" entry).

Scope of this pass: design tokens + dark theme, base reset/typography,
the asterism motif, header/nav/brand, buttons, hero, and footer -- the
structurally load-bearing, highest-value pieces. Everything here is
*removed* from `assets/site.css` as it's ported, so there's exactly
one place each selector is defined (no silently-overridden duplicate
rules sitting in both places).

Page-specific styling (work cards, journal timeline, store/retailer
grid, about/legal/feedback pages) is **not yet ported** -- still lives
in `assets/site.css`, loaded after this generated stylesheet in
`<head>` (see `components/common.py`'s `PAGE_STYLESHEET_LINKS`), so it
keeps working unchanged. See docs/PROGRESS.md for the prioritized
follow-up list.
"""

LIGHT_TOKENS = {
    "--paper": "#f6f2e8",
    "--paper-alt": "#ece4d2",
    "--ink": "#201e19",
    "--ink-soft": "#635b4c",
    "--ink-faint": "#948a75",
    "--accent": "#2c5c4f",
    "--accent-dark": "#1d3e35",
    "--accent-tint": "#e2ece6",
    "--brass": "#ad8434",
    "--brass-dark": "#8c6a28",
    "--warn": "#833e3e",
    "--warn-tint": "#f1e1df",
    "--line": "#dacfb2",
    "--paper-rgb": "246,242,232",
    "--shadow-sm": "0 2px 8px -2px rgba(32,30,25,0.12)",
    "--shadow-md": "0 16px 34px -20px rgba(32,30,25,0.4)",
    "--shadow-lg": "0 28px 60px -24px rgba(32,30,25,0.45)",
    "--serif": "'Fraunces', Georgia, serif",
    "--sans": "'Work Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    "--mono": "'IBM Plex Mono', ui-monospace, monospace",
    "--maxw": "100%",
    "--grain-opacity": "0.5",
    "--card-bg": "#ffffff",
}

DARK_TOKENS = {
    "--paper": "#17160f",
    "--paper-alt": "#201e15",
    "--ink": "#ede7d8",
    "--ink-soft": "#b7ae99",
    "--ink-faint": "#7d765f",
    "--accent": "#5fae9a",
    "--accent-dark": "#3d7d6c",
    "--accent-tint": "#1c2b26",
    "--brass": "#d6ac5c",
    "--brass-dark": "#ad8434",
    "--warn": "#e0a0a0",
    "--warn-tint": "#3a2323",
    "--line": "#34311f",
    "--paper-rgb": "23, 22, 15",
    "--shadow-sm": "0 2px 8px -2px rgba(0, 0, 0, 0.5)",
    "--shadow-md": "0 16px 34px -20px rgba(0, 0, 0, 0.7)",
    "--shadow-lg": "0 28px 60px -24px rgba(0, 0, 0, 0.75)",
    "--grain-opacity": "0.28",
    "--card-bg": "#262319",
}

GRAIN_DATA_URI = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
    "type='fractalNoise' baseFrequency='0.85' numOctaves='2' "
    "stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 "
    "0.13  0 0 0 0 0.12  0 0 0 0 0.10  0 0 0 0.05 0'/%3E%3C/filter%3E%3Crect "
    "width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")"
)


def register_styles(site):
    """Call once on the `Site` instance in `site.py`, before build."""

    # -- Design tokens + dark theme ---------------------------------
    # vue3 toggles dark mode via `[data-theme="dark"]` on <html> (see
    # useTheme.ts) -- an *attribute* selector. ARKlight's only reactive
    # binding primitive is `Bind.when(...)` (see api.py), which toggles
    # a plain CSS *class*, never an attribute value, and there's no way
    # to reach the <body>/<html> tag itself from page content (it's
    # rendered directly by `page_render.py`, not from an ARKNode) --
    # see components/nav.py's docstring for the matching note on the
    # theme-toggle button. So this port uses a `.dark` class instead,
    # applied via `bind_class=Bind.when("theme", "dark")` on each
    # page's outermost `.page-shell` wrapper (see pages/*.py). Custom
    # properties still cascade normally to every descendant from there.
    site.style_selector(":root", LIGHT_TOKENS)
    site.style_selector(".dark", DARK_TOKENS)

    # -- Base reset / typography -------------------------------------
    # `*  { box-sizing: border-box }` already ships in ARKlight's own
    # default stylesheet -- no universal selector in the closed
    # grammar anyway (`site.style_selector("*", ...)` raises
    # `CSSSyntaxError`), and it's redundant here regardless.
    site.style_selector("html", {"scroll-behavior": "smooth"})
    site.style_selector(
        "body",
        {
            "margin": "0",
            "background": "var(--paper)",
            "color": "var(--ink)",
            "font-family": "var(--sans)",
            "font-size": "16px",
            "line-height": "1.6",
            "position": "relative",
            "overscroll-behavior-y": "none",
        },
    )
    site.style_selector(
        "body::before",
        {
            "content": '""',
            "position": "fixed",
            "inset": "0",
            "pointer-events": "none",
            "z-index": "0",
            "opacity": "var(--grain-opacity)",
            "transition": "opacity 0.22s ease",
            "background-image": GRAIN_DATA_URI,
        },
    )
    site.style_selector("img", {"max-width": "100%", "display": "block"})
    site.style_selector("a", {"color": "inherit", "text-decoration": "none"})
    site.style_selector(
        ".wrap",
        {
            "max-width": "var(--maxw)",
            "margin": "0 auto",
            "padding-left": "max(32px, env(safe-area-inset-left))",
            "padding-right": "max(32px, env(safe-area-inset-right))",
            "position": "relative",
            "z-index": "1",
        },
    )
    site.style_selector(
        "h1, h2, h3, h4",
        {
            "font-family": "var(--serif)",
            "font-weight": "600",
            "letter-spacing": "-0.01em",
            "margin": "0 0 0.5em",
            "color": "var(--ink)",
        },
    )
    site.style_selector("p", {"margin": "0 0 1em", "color": "var(--ink-soft)"})
    site.style_selector(
        ".eyebrow",
        {
            "font-family": "var(--mono)",
            "font-size": "0.72rem",
            "letter-spacing": "0.14em",
            "text-transform": "uppercase",
            "color": "var(--brass-dark)",
            "display": "inline-block",
            "margin-bottom": "0.9em",
        },
    )

    # -- Asterism motif + section divider -----------------------------
    site.style_selector(
        ".asterism",
        {
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "gap": "10px",
            "margin": "0 auto",
            "width": "fit-content",
            "color": "var(--brass)",
            "opacity": "0.85",
        },
    )
    site.style_selector(
        ".asterism .dot",
        {"width": "5px", "height": "5px", "border-radius": "50%", "background": "currentColor"},
    )
    site.style_selector(
        ".section-divider",
        {"margin": "0", "text-align": "center", "padding": "56px 0", "position": "relative", "z-index": "1"},
    )

    # -- Header / nav / brand ------------------------------------------
    site.style_selector(
        "header.site-header",
        {
            "position": "sticky",
            "top": "0",
            "z-index": "50",
            "background": "rgba(var(--paper-rgb), 0.9)",
            "backdrop-filter": "saturate(140%) blur(8px)",
            "border-bottom": "1px solid var(--line)",
            "padding-top": "env(safe-area-inset-top, 0px)",
        },
    )
    site.style_selector(
        ".site-header .wrap",
        {
            "display": "flex",
            "align-items": "center",
            "justify-content": "space-between",
            "padding-top": "16px",
            "padding-bottom": "16px",
        },
    )
    site.style_selector(".brand", {"display": "flex", "flex-direction": "column", "line-height": "1.1"})
    site.style_selector(".brand-row", {"display": "flex", "align-items": "center", "gap": "12px"})
    site.style_selector(
        ".avatar",
        {
            "width": "38px",
            "height": "38px",
            "border-radius": "50%",
            "background": "var(--accent-dark) center/cover no-repeat",
            "border": "1.5px solid var(--brass)",
            "flex-shrink": "0",
            "transition": "transform 0.2s ease",
            "&:hover": {"transform": "scale(1.06)"},
        },
    )
    site.style_selector(
        ".avatar-large",
        {
            "width": "176px",
            "height": "176px",
            "border-radius": "50%",
            "background": "var(--accent-dark) center/cover no-repeat",
            "border": "3px solid var(--brass)",
            "box-shadow": "var(--shadow-md)",
            "margin": "0 auto 20px",
        },
    )
    site.style_selector(
        ".brand .name",
        {"font-family": "var(--serif)", "font-weight": "700", "font-size": "1.3rem", "letter-spacing": "0.01em"},
    )
    site.style_selector(
        ".brand .sub",
        {"font-family": "var(--mono)", "font-size": "0.64rem", "letter-spacing": "0.11em", "color": "var(--ink-faint)", "margin-top": "2px"},
    )
    site.style_selector(
        "nav.main-nav",
        {"display": "flex", "align-items": "center", "gap": "40px", "flex": "1", "justify-content": "flex-end"},
    )
    site.style_selector(
        "nav.main-nav a:not(.icon-btn)",
        {
            "font-size": "0.92rem",
            "font-weight": "500",
            "color": "var(--ink-soft)",
            "position": "relative",
            "padding": "4px 0",
            "&:hover": {"color": "var(--ink)"},
        },
    )
    # Active-page indicator: vue3 gets this for free from
    # `router-link`'s `active-class`; this static multi-page build has
    # no router, so `nav()` (components/nav.py) instead compares each
    # link's `href` against a `current_route` passed in from the page
    # and adds this class itself at build time.
    site.style_selector(
        "nav.main-nav a.active",
        {"color": "var(--ink)"},
    )
    site.style_selector(
        "nav.main-nav a.active::after",
        {
            "content": '""',
            "position": "absolute",
            "left": "0",
            "right": "0",
            "bottom": "-2px",
            "height": "2px",
            "background": "var(--accent)",
            "border-radius": "1px",
        },
    )
    # Visually hidden but still announced by screen readers -- used to
    # keep real text content on icon-only controls below instead of
    # relying on `aria-label` alone.
    site.style_selector(
        ".sr-only",
        {
            "position": "absolute",
            "width": "1px",
            "height": "1px",
            "padding": "0",
            "margin": "-1px",
            "overflow": "hidden",
            "clip": "rect(0, 0, 0, 0)",
            "white-space": "nowrap",
            "border": "0",
        },
    )
    site.style_selector(
        ".nav-icons",
        {
            "display": "flex",
            "align-items": "center",
            "gap": "8px",
            "margin-left": "14px",
            "padding-left": "28px",
            "border-left": "1px solid var(--line)",
        },
    )
    site.style_selector(
        ".icon-btn",
        {
            "display": "inline-flex",
            "align-items": "center",
            "justify-content": "center",
            "flex-shrink": "0",
            "width": "44px",
            "height": "44px",
            "border-radius": "50%",
            "border": "1px solid var(--line)",
            "color": "var(--ink-soft)",
            "background-color": "transparent",
            "background-repeat": "no-repeat",
            "background-position": "center",
            "background-size": "18px 18px",
            "transition": "background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease",
            # `Link`'s schema won't allow a nested `.sr-only` `Span` (see
            # components/nav.py), so the real fallback text stays as
            # the element's own text content -- `aria-label` already
            # takes over as the accessible name regardless, and this
            # just keeps it out of view for sighted users so the
            # `background-image` icon is the only thing that shows.
            "font-size": "0",
            "line-height": "0",
        },
    )
    site.style_selector(
        ".icon-btn:active",
        {"background-color": "var(--ink)", "border-color": "var(--ink)", "transform": "scale(0.92)"},
    )
    # ARKlight has no `Svg`/`Icon` element in its component grammar
    # today (see components/nav.py's docstring) -- there's no way to
    # emit raw SVG through the framework. Short-term workaround: keep
    # real (screen-reader-only) text as each button's actual content
    # for accessibility, and paint the icon as a CSS `background-image`
    # data-URI instead of relying on element content, matching the
    # exact glyphs vue3's inline `<svg>`s use (AppHeader.vue) so this
    # still looks identical once ARKlight gains real SVG support and
    # these rules can be deleted.
    ICON_X = (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 24 24' fill='%23635b4c'%3E%3Cpath d='M18.9 2H22l-7.6 "
        "8.7L23 22h-6.9l-5.4-6.6L4.4 22H1.3l8.1-9.3L1 2h7l4.9 6z'/%3E%3C/svg%3E\")"
    )
    ICON_GITHUB = (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 24 24' fill='%23635b4c'%3E%3Cpath d='M12 2C6.48 2 2 "
        "6.58 2 12.17c0 4.47 2.87 8.26 6.84 9.6.5.1.68-.22.68-.5v-1.94c-2.78 "
        ".62-3.37-1.36-3.37-1.36-.46-1.2-1.11-1.52-1.11-1.52-.9-.63.07-.62"
        ".07-.62 1 .07 1.53 1.05 1.53 1.05.9 1.55 2.36 1.1 2.93.84.09-.66"
        ".35-1.1.64-1.36-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03"
        "-2.75-.1-.26-.45-1.31.1-2.74 0 0 .84-.28 2.75 1.05a9.3 9.3 0 0 1 "
        "5 0c1.9-1.33 2.75-1.05 2.75-1.05.55 1.43.2 2.48.1 2.74.64.72 1.03 "
        "1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9v2.82c0 "
        ".28.18.6.69.5A10.19 10.19 0 0 0 22 12.17C22 6.58 17.52 2 12 2Z'/%3E"
        "%3C/svg%3E\")"
    )
    ICON_SUN = (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 24 24' fill='none' stroke='%23635b4c' stroke-width='2' "
        "stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' "
        "cy='12' r='4.5'/%3E%3Cpath d='M12 2.5v2.5M12 19v2.5M4.6 4.6l1.8 "
        "1.8M17.6 17.6l1.8 1.8M2.5 12h2.5M19 12h2.5M4.6 19.4l1.8-1.8M17.6 "
        "6.4l1.8-1.8'/%3E%3C/svg%3E\")"
    )
    ICON_MOON = (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 24 24' fill='%23635b4c'%3E%3Cpath d='M20.6 15.3A8.5 "
        "8.5 0 1 1 8.7 3.4a7 7 0 0 0 11.9 11.9Z'/%3E%3C/svg%3E\")"
    )
    site.style_selector(".icon-btn.icon-x", {"background-image": ICON_X})
    site.style_selector(".icon-btn.icon-github", {"background-image": ICON_GITHUB})
    # Light mode starts on the sun glyph (click to go dark, same as
    # vue3's `v-else` branch when `theme !== 'dark'`); `.dark` flips it
    # to the moon, matching AppHeader.vue's `v-if="theme === 'dark'"`.
    site.style_selector(".icon-btn.theme-toggle", {"background-image": ICON_SUN})
    site.style_selector(".icon-btn.theme-toggle.dark", {"background-image": ICON_MOON})
    site.style_selector(
        ".nav-toggle",
        {
            "display": "none",
            "background": "none",
            "border": "1px solid var(--line)",
            "border-radius": "6px",
            "width": "38px",
            "height": "38px",
            "align-items": "center",
            "justify-content": "center",
            "cursor": "pointer",
            "color": "var(--ink)",
            "font-size": "1.1rem",
            "line-height": "1",
        },
    )

    # -- Buttons ----------------------------------------------------
    site.style_selector(
        ".btn",
        {
            "display": "inline-flex",
            "align-items": "center",
            "gap": "8px",
            "padding": "13px 24px",
            "border-radius": "5px",
            "font-size": "0.92rem",
            "font-weight": "600",
            "border": "1px solid transparent",
            "cursor": "pointer",
            "transition": "all 0.18s ease",
        },
    )
    site.style_selector(
        ".btn-primary",
        {
            "background": "var(--accent)",
            "color": "#fff",
            "box-shadow": "var(--shadow-sm)",
            "&:hover": {"background": "var(--accent-dark)", "box-shadow": "var(--shadow-md)", "transform": "translateY(-1px)"},
            "&:active": {"background": "var(--accent-dark)", "transform": "scale(0.98)"},
        },
    )
    site.style_selector(
        ".btn-ghost",
        {
            "border-color": "var(--ink)",
            "color": "var(--ink)",
            "&:hover": {"background": "var(--ink)", "color": "var(--paper)"},
            "&:active": {"background": "var(--ink)", "color": "var(--paper)"},
        },
    )

    # -- Sections / hero ----------------------------------------------
    site.style_selector("section", {"padding": "76px 0", "position": "relative", "z-index": "1"})
    site.style_selector(
        "section.alt-bg",
        {"background": "var(--paper-alt)", "border-top": "1px solid var(--line)", "border-bottom": "1px solid var(--line)"},
    )
    site.style_selector(".hero", {"padding": "100px 0 76px", "border-bottom": "1px solid var(--line)", "position": "relative", "overflow": "hidden"})
    site.style_selector(".hero .wrap", {"max-width": "760px", "text-align": "center"})
    site.style_selector(
        ".hero::after",
        {
            "content": '"\\2042"',
            "position": "absolute",
            "top": "-40px",
            "left": "50%",
            "transform": "translateX(-50%)",
            "font-size": "220px",
            "font-family": "var(--serif)",
            "color": "var(--brass)",
            "opacity": "0.05",
            "line-height": "1",
            "pointer-events": "none",
        },
    )
    site.style_selector(".hero h1", {"font-size": "clamp(2.2rem, 5vw, 3.5rem)", "line-height": "1.12"})
    site.style_selector(".hero .lede", {"font-size": "1.12rem", "max-width": "560px", "margin": "0 auto 2em"})
    site.style_selector(".hero .cta-row", {"display": "flex", "gap": "14px", "justify-content": "center", "flex-wrap": "wrap"})

    # -- Footer -------------------------------------------------------
    site.style_selector(
        "footer.site-footer",
        {"border-top": "1px solid var(--line)", "padding": "60px 0 max(36px, env(safe-area-inset-bottom))", "background": "var(--paper-alt)"},
    )
    site.style_selector(
        ".footer-quote",
        {"text-align": "center", "font-family": "var(--serif)", "font-style": "italic", "font-size": "1.05rem", "color": "var(--ink)", "max-width": "520px", "margin": "0 auto 8px"},
    )
    site.style_selector(
        ".footer-attrib",
        {"text-align": "center", "font-family": "var(--mono)", "font-size": "0.72rem", "color": "var(--ink-faint)", "margin-bottom": "20px"},
    )
    site.style_selector(
        ".footer-imprint",
        {"display": "flex", "align-items": "center", "justify-content": "center", "gap": "8px", "margin-bottom": "36px"},
    )
    site.style_selector(".footer-imprint img", {"height": "20px", "opacity": "0.85"})
    site.style_selector(
        ".footer-imprint span",
        {"font-family": "var(--mono)", "font-size": "0.66rem", "letter-spacing": "0.08em", "color": "var(--ink-faint)", "text-transform": "uppercase"},
    )
    site.style_selector(
        ".footer-bottom",
        {"display": "flex", "justify-content": "space-between", "align-items": "center", "flex-wrap": "wrap", "gap": "16px", "padding-top": "28px", "border-top": "1px solid var(--line)", "font-size": "0.82rem", "color": "var(--ink-faint)"},
    )
    site.style_selector(".footer-links", {"display": "flex", "gap": "20px", "flex-wrap": "wrap"})
    site.style_selector(".footer-links a", {"&:hover": {"color": "var(--accent)"}})

    # -- Legal-page inline contact link -------------------------------
    # `Text(...)` is schema-restricted to text-only children (see
    # arklight/ir/schema.py), so a `Link` can't be nested inside a run
    # of paragraph text the way vue3's template does it inline. A
    # `Container` has no such restriction, so pages/privacy.py and
    # pages/terms.py use one in place of that final `Text(...)`, styled
    # to flow as an inline run instead of its default block `<div>`.
    site.style_selector(".inline-text", {"display": "inline", "margin": "0 0 1em", "color": "var(--ink-soft)"})
    site.style_selector(".inline-text a", {"color": "var(--accent)", "text-decoration": "underline"})

    # -- Mobile nav (matches assets/site.css's surviving @media block
    #    for widths still handled there; the .nav-toggle/.main-nav.open
    #    show/hide pairing itself is native from here on) -------------
    site.style_selector("nav.main-nav.open", {"display": "flex"})
