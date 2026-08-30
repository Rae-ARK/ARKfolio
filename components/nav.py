"""Shared site navigation.

Ported from ARKfolio's AppHeader.vue. Two things from the original
don't carry over 1:1, both noted in place rather than silently dropped:

- The mobile hamburger open/close toggle was Vue-local `ref` state
  scoped to one component instance. ARKlight's `State`/`Action` model
  is page-level, so a per-page `State("nav_open", False)` would need
  to be threaded through every single page that calls `nav()` --
  doable, but deferred until the CSS-only fallback (a checkbox-driven
  disclosure, zero JS) is confirmed insufficient.
- The theme toggle button lives here in the original. ARKlight can
  express the toggle itself (`Action.toggle_bool` + `Bind.when`), but
  needs a `State("theme", ...)` declared on `Page(...)` -- see
  `pages/home.py` for how that's wired for the pages that have it.
- `Link(...)` is schema-restricted to text-only children (see
  `arklight/ir/schema.py`), so an `Image` can't be nested inside one
  the way the original's `<router-link to="/about"><div class="avatar">
  ...</router-link>` does. The avatar is a plain, non-clickable `Image`
  here; only the site name text links to `/about`/`/` as before.
"""

from arklight import Header, Nav, Link, Container, Image, Span, Action

SITE_TITLE = "Rae ARK"
SITE_SUBTITLE = "\u5d50\u4e45 \u601c \u00b7 WEB NOVELIST"


def nav(theme_state: str | None = None):
    """Build the shared header nav.

    `theme_state` is the name of a `State(...)` declared on the calling
    page (e.g. "theme"); pass None on pages that don't declare one --
    the theme toggle button is simply omitted rather than referencing
    an undeclared state name (which would fail validation).
    """
    icons = [
        Link(
            "X",
            href="https://x.com/Rae7866",
            target="_blank",
            class_name="icon-btn",
            aria_label="Follow on X",
        ),
        Link(
            "GitHub",
            href="https://github.com/Rae-ARK/ARKfolio",
            target="_blank",
            class_name="icon-btn",
            aria_label="View source on GitHub",
        ),
    ]
    if theme_state:
        icons.append(
            Container(
                "Toggle theme",
                on_click=Action.toggle_bool(theme_state),
                class_name="icon-btn theme-toggle",
                role="button",
                tabindex="0",
                aria_label="Toggle light/dark theme",
            )
        )

    return Header(
        Container(
            Container(
                Image(src="/assets/images/profile.png", alt="Rae ARK", class_name="avatar"),
                Container(
                    Span(SITE_TITLE, class_name="name"),
                    Span(SITE_SUBTITLE, class_name="sub"),
                    class_name="brand",
                ),
                class_name="brand-row",
            ),
            Nav(
                Link("Home", href="/"),
                Link("Works", href="/works"),
                Link("Store", href="/store"),
                Link("Journal", href="/journal"),
                Link("About", href="/about"),
                Container(*icons, class_name="nav-icons"),
                class_name="main-nav",
                aria_label="Primary",
            ),
            class_name="wrap",
        ),
        class_name="site-header",
    )
