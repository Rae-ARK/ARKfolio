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
    "--maxw": "1080px",
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
    site.style_selector(":root", LIGHT_TOKENS)
    site.style_selector('[data-theme="dark"]', DARK_TOKENS)

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
    site.style_selector("nav.main-nav", {"display": "flex", "align-items": "center", "gap": "26px"})
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
    site.style_selector(
        ".nav-icons",
        {
            "display": "flex",
            "align-items": "center",
            "gap": "8px",
            "margin-left": "6px",
            "padding-left": "20px",
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
            "background": "transparent",
            "transition": "background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease",
        },
    )
    site.style_selector(
        ".icon-btn:active",
        {"background": "var(--ink)", "border-color": "var(--ink)", "color": "var(--paper)", "transform": "scale(0.92)"},
    )
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

    # -- Mobile nav (matches assets/site.css's surviving @media block
    #    for widths still handled there; the .nav-toggle/.main-nav.open
    #    show/hide pairing itself is native from here on) -------------
    site.style_selector("nav.main-nav.open", {"display": "flex"})
