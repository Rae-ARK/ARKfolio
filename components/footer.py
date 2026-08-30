"""Shared site footer, ported from ARKfolio's AppFooter.vue.

The original's `@error="hideImage"` (hide the Horizon ARK logo if it
404s) needs a runtime `on_error` hook ARKlight doesn't expose yet --
left as a plain `Image`, noted here rather than silently dropped.
"""

from arklight import Footer, Container, Text, Span, Image, Link

FOOTER_QUOTE = (
    "\u201cI hope for people to hold the book in their hands someday, "
    "and to sit on the shelves.\u201d"
)


def footer():
    return Footer(
        Container(
            Text(FOOTER_QUOTE, class_name="footer-quote"),
            Text("\u2014 Rae ARK", class_name="footer-attrib"),
            Container(
                Image(
                    src="/assets/images/horizon-ark-logo.png",
                    alt="Horizon ARK Studio",
                ),
                Span("Published under Horizon ARK Studio"),
                class_name="footer-imprint",
            ),
            Container(
                Text("\u00a9 2026 Rae ARK"),
                Container(
                    Link("Works", href="/works"),
                    Link("Store", href="/store"),
                    Link("Journal", href="/journal"),
                    Link("About", href="/about"),
                    Link("Feedback", href="/feedback"),
                    Link("Privacy", href="/privacy"),
                    Link("Terms", href="/terms"),
                    Link("X", href="https://x.com/Rae7866", target="_blank"),
                    Link("GitHub", href="https://github.com/Rae-ARK/ARKfolio", target="_blank"),
                    class_name="footer-links",
                ),
                class_name="footer-bottom",
            ),
            class_name="wrap",
        ),
        class_name="site-footer",
    )
