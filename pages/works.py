"""Works page, ported from ARKfolio's WorksPage.vue.

Each work gets its own #<slug> section with an asterism divider between
them (skipped after the last one), matching the original's `v-for`
template block. `v-reveal` scroll-in animation -> `on_reveal="reveal"`
(see pages/home.py's docstring for the full explanation).
"""

from arklight import Page, Section, Container, Span, Heading, Text, Strong, Link, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import section_divider, PAGE_STYLESHEET_LINKS, PAGE_FAVICON
from content.works import WORKS


def _official_sites():
    """Official reading platforms, derived from the same WORKS[*]['links']
    used below so the notice can't drift out of date: platform -> the
    stories hosted there. Mirrors WorksPage.vue's `officialSites` reduce,
    preserving first-seen platform order (plain dict insertion order).
    """
    grouped = {}
    for work in WORKS:
        for link in work["links"]:
            grouped.setdefault(link["label"], []).append(work["short_title"])
    return list(grouped.items())


def _official_sources_notice():
    sites = _official_sites()
    sites_text = ", ".join(f"{site_name} ({', '.join(titles)})" for site_name, titles in sites)

    return Container(
        Strong("Official sources"),
        Container(
            Span(f"These are the only authorised places to read or buy these stories: {sites_text}, and the paperback through the "),
            Link("Store", href="/store"),
            Span(". A complete copy hosted anywhere else is unauthorised \u2014 see the "),
            Link("Journal", href="/journal"),
            Span(" for why this matters."),
            class_name="inline-text",
        ),
        class_name="notice-box official-sources",
    )


def works():
    sections = []
    for i, work in enumerate(WORKS):
        body = [
            Span(f"{work['kind']} \u00b7 {work['status']}", class_name="eyebrow"),
            Container(
                Container(class_name=f"work-thumb {work['cover_class']}"),
                Container(
                    Heading(work["title"], level=2),
                    Span(work["short_title"], class_name="work-shorttitle"),
                ),
                class_name="work-heading-row",
            ),
            Container(
                *[
                    Span(tag, class_name="badge mature" if tag == "Mature Content" else "badge")
                    for tag in work["tags"]
                ],
                class_name="tags",
            ),
        ]

        if work.get("content_notice"):
            body.append(
                Container(
                    Strong("Content notice \u2014 18+", class_name="content-notice-label"),
                    Text(work["content_notice"]),
                    class_name="content-notice",
                )
            )

        body.extend(Text(para) for para in work["synopsis"])

        if work.get("expect_rows"):
            body.append(
                Container(
                    *[
                        Text(row["text"], class_name="yes" if row["yes"] else "no")
                        for row in work["expect_rows"]
                    ],
                    class_name="not-expect",
                )
            )

        body.append(
            Container(
                *[
                    Link(f"Read on {link['label']} \u2197", href=link["url"], target="_blank")
                    for link in work["links"]
                ],
                class_name="work-links",
            )
        )

        sections.append(
            Section(
                Container(*body, class_name="wrap container-narrow"),
                id=work["slug"],
                on_reveal="reveal",
            )
        )
        if i < len(WORKS) - 1:
            sections.append(section_divider())

    return Page(
        State("theme", False, persist=True),
        Container(
            nav(theme_state="theme", current_route="/works"),
            Section(
                Container(
                    Span("The Works", class_name="eyebrow"),
                    Heading("Three stories, read in full elsewhere", level=1),
                    Text(
                        "Every chapter lives on Royal Road and Scribble Hub \u2014 this page is "
                        "just the map. Synopses below, links to the real thing at the end of each.",
                        class_name="lede",
                    ),
                    class_name="wrap",
                ),
                class_name="hero",
            ),
            Section(
                Container(_official_sources_notice(), class_name="wrap container-narrow"),
                class_name="page-body tight",
            ),
            *sections,
            footer(),
            bind_class=Bind.when("theme", "dark"),
            class_name="page-shell",
        ),
        title="Works \u2014 Rae ARK",
        description=(
            "Full synopses for Rae ARK\u2019s three ongoing web novels \u2014 Enigmatic "
            "Pathways Mystic Circuits, Summoned by Mistake I Decided to Learn How to Live, and "
            "The Shadow I Cast Over Two Beautiful Flowers."
        ),
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
