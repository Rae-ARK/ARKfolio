"""Journal page, ported from ARKfolio's JournalPage.vue."""

from arklight import Page, Section, Container, Span, Heading, Text, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import PAGE_STYLESHEET_LINKS, PAGE_FAVICON
from content.journal import JOURNAL_ENTRIES


def _entry(entry: dict):
    return Container(
        Container(
            Container(Span(entry["date"], class_name="journal-date"), class_name="journal-head"),
            Heading(entry["title"], level=3),
            Text(entry["body"]),
            Container(
                Container(class_name=f"work-thumb small {entry['tags']['thumb']}"),
                Span(entry["tags"]["label"], class_name="journal-tag"),
                class_name="journal-tag-row",
            ),
            class_name="journal-card",
        ),
        class_name="journal-entry",
    )


def journal():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/journal"),
        Section(
            Container(
                Span("From the Writing Desk", class_name="eyebrow"),
                Heading("Journal", level=1),
                Text(
                    "Not news. Just the process \u2014 the breaks, the doubts, the small wins "
                    "\u2014 as it actually happens.",
                    class_name="lede",
                ),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(
                Container(*[_entry(e) for e in JOURNAL_ENTRIES], class_name="timeline"),
                class_name="wrap container-narrow",
            ),
        ),
        footer(),
        bind_class=Bind.when("theme", "dark"),
        class_name="page-shell",
        ),
        title="Journal \u2014 Rae ARK",
        description=(
            "A running journal of Rae ARK\u2019s writing process \u2014 the breaks, the "
            "doubts, the small wins \u2014 as it actually happens."
        ),
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
