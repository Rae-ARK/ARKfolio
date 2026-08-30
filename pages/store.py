"""Store page, ported from ARKfolio's StorePage.vue."""

from arklight import Page, Section, Container, Span, Heading, Text, Link, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import section_divider, PAGE_STYLESHEET_LINKS, PAGE_FAVICON
from content.store import STORE_BOOKS, NOT_YET_IN_PRINT_NOTE


def _book(book: dict):
    body = [
        Span(book["edition"], class_name="eyebrow"),
        Heading(book["title"], level=2),
        Text(book["description"]),
        Text(book["note"], class_name="retailer-note"),
        Container(
            *[
                Link(
                    f"{r['label']} \u2197",
                    href=r["url"],
                    target="_blank",
                    class_name="retailer-btn",
                )
                for r in book["retailers"]
            ],
            class_name="retailer-grid",
        ),
    ]
    if book.get("retailer_note"):
        body.append(Text(book["retailer_note"], class_name="retailer-note"))

    return Container(
        Container(class_name=f"work-thumb {book['thumb_class']}"),
        Container(*body),
        class_name="store-book",
    )


def store():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/store"),
        Section(
            Container(
                Span("Paperbacks", class_name="eyebrow"),
                Heading("Store", level=1),
                Text(
                    "Every chapter is free to read online. These are the print editions, for "
                    "anyone who'd rather have one on a shelf.",
                    class_name="lede",
                ),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(*[_book(b) for b in STORE_BOOKS], class_name="wrap container-narrow"),
        ),
        section_divider(),
        Section(
            Container(
                Text(NOT_YET_IN_PRINT_NOTE, class_name="store-empty"),
                class_name="wrap container-narrow",
            ),
        ),
        footer(),
        bind_class=Bind.when("theme", "dark"),
        class_name="page-shell",
        ),
        title="Store \u2014 Rae ARK",
        description=(
            "Paperback editions of Rae ARK\u2019s web novels, with links to retailers as "
            "titles go to print."
        ),
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
