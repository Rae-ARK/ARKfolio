"""Small shared helpers used by every page."""

from arklight import Container, Span


def asterism():
    """The site's recurring section-divider mark: three dots in a row,
    styled by .asterism/.dot in assets/site.css -- matches the original
    AppFooter/HomePage markup (a flex row of <span class="dot">), not a
    Unicode glyph, so the CSS's exact spacing/color rules still apply.
    """
    return Container(
        Span(class_name="dot"),
        Span(class_name="dot"),
        Span(class_name="dot"),
        class_name="asterism",
    )


def section_divider():
    return Container(asterism(), class_name="section-divider")


# The original ARKfolio's design system (fonts, colors, spacing) lives in
# assets/site.css, ported close to verbatim from src/styles/main.css.
# Every page links it the same way via Page(links=[...]) -- ARKlight's
# structured <head> extension point (v0.048 Stage A), not a raw-HTML
# escape hatch.
PAGE_STYLESHEET_LINKS = [
    {"rel": "preconnect", "href": "https://fonts.googleapis.com"},
    {"rel": "preconnect", "href": "https://fonts.gstatic.com", "crossorigin": ""},
    {
        "rel": "stylesheet",
        "href": (
            "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;"
            "9..144,500;9..144,600;9..144,700&family=Work+Sans:wght@400;500;600&"
            "family=IBM+Plex+Mono:wght@400;500&display=swap"
        ),
    },
    {"rel": "stylesheet", "href": "/assets/site.css"},
]
