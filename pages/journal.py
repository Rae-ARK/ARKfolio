"""Journal page, ported from ARKfolio's JournalPage.vue.

`v-reveal` scroll-in animation -> `on_reveal="reveal"` (see
pages/home.py's docstring), applied per-entry, matching the original's
per-`.journal-entry` placement.
"""

from arklight import (
    Page,
    Section,
    Container,
    Span,
    Heading,
    Text,
    Link,
    Button,
    State,
    Computed,
    Bind,
    Derive,
    Predicate,
    Show,
    Action,
)

from components.nav import nav
from components.footer import footer
from components.common import PAGE_STYLESHEET_LINKS, PAGE_FAVICON
from content.journal import JOURNAL_ENTRIES

# Filter ids / display labels, matching JournalPage.vue's `filters` array.
# "all" is special-cased (always matches); the rest match an entry when
# their label is a substring of that entry's tags.label, same semantics
# as the original's `entry.tags.label.includes(filter.label)`.
FILTERS = [
    ("all", "All"),
    ("sbm", "SBM"),
    ("epmc", "EPMC"),
    ("stbf", "STBF"),
]


def _entry_filter_ids(entry: dict):
    """Which filter ids this entry should be visible under, "all" plus
    every story filter whose label is a substring of the entry's tag
    label (an entry tagged "SBM \u00b7 EPMC \u00b7 STBF" matches all three,
    not just the one that picked its thumb -- mirrors the Vue comment)."""
    return ["all"] + [
        filter_id
        for filter_id, label in FILTERS
        if filter_id != "all" and label in entry["tags"]["label"]
    ]


def _empty_filter_ids():
    """Filter ids (besides "all") with zero matching entries -- these are
    the only ones `active_filter` could hold while showing the
    "No entries tagged for that story yet." message."""
    return [
        filter_id
        for filter_id, label in FILTERS
        if filter_id != "all" and not any(label in e["tags"]["label"] for e in JOURNAL_ENTRIES)
    ]


def _entry(entry: dict):
    return Show(
        Predicate.one_of("active_filter", _entry_filter_ids(entry)),
        Container(
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
            on_reveal="reveal",
        ),
    )


def _filter_button(filter_id: str, label: str):
    # Bind.when only reacts to a *named* state's truthiness, so each
    # button compares `active_filter` against its own constant-valued
    # State (the only way to get literal-equality -> class toggling out
    # of the closed Action/Bind vocabulary).
    return Button(
        label,
        class_name="tag-filter-btn",
        on_click=Action.set("active_filter", filter_id),
        bind_class=Bind.when(f"is_filter_{filter_id}", "active"),
    )


def _filter_state_and_computed():
    nodes = [State("active_filter", "all")]
    for filter_id, _label in FILTERS:
        nodes.append(State(f"filter_id_{filter_id}", filter_id))
        nodes.append(
            Computed(
                f"is_filter_{filter_id}",
                deps=("active_filter", f"filter_id_{filter_id}"),
                derive=Derive.compare("active_filter", f"filter_id_{filter_id}", "eq"),
            )
        )
    return nodes


def journal():
    empty_ids = _empty_filter_ids()
    body_children = [
        Container(
            *[_filter_button(filter_id, label) for filter_id, label in FILTERS],
            class_name="tag-filter",
        ),
    ]
    if empty_ids:
        body_children.append(
            Show(
                Predicate.one_of("active_filter", empty_ids),
                Text("No entries tagged for that story yet.", class_name="journal-empty"),
            )
        )
    body_children.append(
        Container(*[_entry(e) for e in JOURNAL_ENTRIES], class_name="timeline")
    )

    return Page(
        State("theme", False, persist=True),
        *_filter_state_and_computed(),
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
                    Container(
                        Link("Follow by RSS \u2197", href="/feed.xml", target="_blank"),
                        class_name="rss-link",
                    ),
                    class_name="wrap",
                ),
                class_name="hero",
            ),
            Section(
                Container(
                    *body_children,
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
