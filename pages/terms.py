"""Terms & Conditions page, ported from ARKfolio's TermsPage.vue."""

from arklight import Page, Section, Container, Span, Heading, Text, Link, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import PAGE_STYLESHEET_LINKS, PAGE_FAVICON

LAST_UPDATED = "July 2026"


def terms():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/terms"),
        Section(
            Container(
                Span("Legal", class_name="eyebrow"),
                Heading("Terms & Conditions", level=1),
                Text(f"Last updated: {LAST_UPDATED}", class_name="lede"),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(
                Container(
                    Text(
                        "By using this site or the Rae ARK Android app, you agree to the "
                        "terms below. If you don't agree, the simplest option is not to use "
                        "it \u2014 nothing here is gated behind acceptance of anything more "
                        "involved than reading a webpage or opening an app."
                    ),
                    Heading("The content", level=3),
                    Text(
                        "All original writing, artwork, and branding on this site and app "
                        "\u2014 including the web novels, journal entries, and cover art "
                        "\u2014 belongs to Rae ARK (Horizon ARK Studio) unless stated "
                        "otherwise. You're welcome to read, link to, and share pages, but "
                        "reposting, republishing, or using the writing or art commercially "
                        "without permission isn't allowed."
                    ),
                    Heading("Third-party platforms", level=3),
                    Text(
                        "Royal Road, Scribble Hub, X/Twitter, and any retailers linked from "
                        "the Store page are independent platforms with their own terms of "
                        "service. Reading, purchasing, or creating an account on those "
                        "platforms is governed by their rules, not these ones."
                    ),
                    Heading("No warranty", level=3),
                    Text(
                        "This site and app are provided \"as is.\" Every reasonable "
                        "effort is made to keep content accurate and the app functioning, but "
                        "no guarantee is made that it will be uninterrupted, error-free, or "
                        "available at all times."
                    ),
                    Heading("Age and content notices", level=3),
                    Text(
                        "Some works are tagged \"Mature Content\" on the Works page "
                        "and carry appropriate content warnings there. Please check those "
                        "tags before reading if that matters to you."
                    ),
                    Heading("Changes", level=3),
                    Text(
                        "These terms may be updated occasionally; continued use after a "
                        "change means you accept the updated terms. Material changes will "
                        "update the \"last updated\" date above."
                    ),
                    Heading("Contact", level=3),
                    Container(
                        Span("Questions about these terms can be sent via the "),
                        Link("Feedback", href="/feedback"),
                        Span(" page."),
                        class_name="inline-text",
                    ),
                    class_name="legal-card",
                ),
                class_name="wrap container-narrow",
            ),
        ),
        footer(),
        bind_class=Bind.when("theme", "dark"),
        class_name="page-shell",
        ),
        title="Terms & Conditions \u2014 Rae ARK",
        description="Terms of use for the Rae ARK site and Android app.",
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
