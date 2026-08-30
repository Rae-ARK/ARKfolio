"""Shared site navigation.

Ported from ARKfolio's AppHeader.vue. Things that don't carry over
1:1, noted in place rather than silently dropped:

- The mobile hamburger open/close now uses ARKlight's native `"toggle"`
  named behavior (`on_click="toggle"`, `behavior_target=...`,
  `toggle_class=...` -- landed after `v0.048`, see docs/PROGRESS.md's
  "ARKlight upgrade" entry). No page-level `State` needed, unlike the
  theme toggle below -- behaviors are stateless/page-independent by
  design, so this works the same on every page without threading
  anything through `nav()`'s caller.
- The theme toggle button lives here in the original. ARKlight
  expresses that one with `Action.toggle_bool` + `Bind.when` -- which
  *does* need a `State("theme", False)` declared on `Page(...)` -- see
  any `pages/*.py` for how that's wired (every page now declares it).
  `Bind.when` only ever toggles a plain CSS *class*, never an
  attribute, and there's no way to reach `<body>`/`<html>` themselves
  from page content (rendered directly by `page_render.py`, not from
  an ARKNode) -- so unlike vue3's `[data-theme="dark"]` on `<html>`,
  this port's dark-mode styling keys off a `.dark` class instead,
  applied to each page's outer `.page-shell` wrapper. See
  `components/styles.py` for the matching CSS-side note.
- ARKlight has no `Svg`/`Icon` element in its component grammar today
  (checked the full public API, including `experimental` -- there's
  no way to emit raw SVG through the framework). The X / GitHub /
  theme-toggle buttons below carry real (but visually hidden) text for
  accessibility, with the icon itself painted as a CSS
  `background-image` -- see `components/styles.py`'s `.icon-btn`
  rules. Delete the workaround once ARKlight ships real SVG support.
- `Link(...)` is schema-restricted to text-only children (see
  `arklight/ir/schema.py`), so an `Image` can't be nested inside one
  the way the original's `<router-link to="/about"><div class="avatar">
  ...</router-link>` does. The avatar is a plain, non-clickable `Image`
  here; only the site name text links to `/` as before (see
  `_asterism()` above for the matching workaround on the three-dot
  motif next to it, which has the same text-only-children problem).
"""

from arklight import Header, Nav, Link, Container, Image, Span, Button, Action, Bind


def _asterism():
    """The site's signature motif (\u2042) next to the wordmark.

    Ported from AppHeader.vue's `<span class="asterism"><span
    class="dot">x3</span></span>`, nested *inside* the `<router-link
    to="/">` there. `Link` (like `Span`) is schema-restricted to
    text-only children (see `arklight/ir/schema.py`), so it can't hold
    this the way the original does -- it's rendered as a sibling of
    the name `Link` below instead. The trade-off (same one already
    made for the icon buttons and avatar elsewhere in this file): the
    three dots sit right next to the link visually but aren't
    themselves part of its click target.
    """
    return Container(
        Span(class_name="dot"),
        Span(class_name="dot"),
        Span(class_name="dot"),
        class_name="asterism",
    )

SITE_TITLE = "Rae ARK"
SITE_SUBTITLE = "\u5d50\u4e45 \u601c \u00b7 WEB NOVELIST"
NAV_ID = "primary-nav"

NAV_LINKS = [
    ("Home", "/"),
    ("Works", "/works"),
    ("Store", "/store"),
    ("Journal", "/journal"),
    ("About", "/about"),
]


def nav(theme_state: str | None = None, current_route: str | None = None):
    """Build the shared header nav.

    `theme_state` is the name of a `State(...)` declared on the calling
    page (e.g. "theme"); every page now declares one (see pages/*.py).

    `current_route` is the calling page's own route (e.g. "/works");
    when it matches one of `NAV_LINKS`, that link gets `class_name=
    "active"` -- vue3's `router-link` does this automatically via
    `active-class`, but a static multi-page site has no router to ask,
    so each page tells `nav()` which one it is instead.
    """
    icons = [
        # `Link` is schema-restricted to text-only children (or
        # `Bind(...)`) -- see the module docstring -- so the sr-only
        # label can't be a nested `Span` here the way the theme-toggle
        # `Container` below manages it. `aria_label` already fully
        # overrides an element's accessible name over its visible text
        # content, so the plain string children below are only ever
        # seen by a screen reader in practice; `.icon-btn`'s CSS
        # additionally visually hides them (`font-size: 0`) so the
        # real icon -- painted as a `background-image`, see
        # `components/styles.py` -- is the only thing sighted users see.
        Link(
            "X",
            href="https://x.com/Rae7866",
            target="_blank",
            class_name="icon-btn icon-x",
            aria_label="Follow on X",
        ),
        Link(
            "GitHub",
            href="https://github.com/Rae-ARK/My-Portfolio",
            target="_blank",
            class_name="icon-btn icon-github",
            aria_label="View source on GitHub",
        ),
    ]
    if theme_state:
        icons.append(
            Container(
                Span("Toggle theme", class_name="sr-only"),
                on_click=Action.toggle_bool(theme_state),
                bind_class=Bind.when(theme_state, "dark"),
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
                    Container(
                        Link(SITE_TITLE, href="/", class_name="name"),
                        _asterism(),
                        class_name="name-row",
                    ),
                    Span(SITE_SUBTITLE, class_name="sub"),
                    class_name="brand",
                ),
                class_name="brand-row",
            ),
            Button(
                "\u2630",
                on_click="toggle",
                behavior_target=f"#{NAV_ID}",
                toggle_class="open",
                class_name="nav-toggle",
                aria_label="Toggle navigation menu",
                aria_controls=NAV_ID,
                type="button",
            ),
            Nav(
                *[
                    Link(label, href=href, class_name="active" if href == current_route else None)
                    for label, href in NAV_LINKS
                ],
                Container(*icons, class_name="nav-icons"),
                class_name="main-nav",
                aria_label="Primary",
                id=NAV_ID,
            ),
            class_name="wrap",
        ),
        class_name="site-header",
    )
