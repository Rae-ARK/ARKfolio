"""Home page, ported from ARKfolio's HomePage.vue.

Sections dropped or altered from the original, each noted at the call
site below rather than silently omitted:
- `v-reveal` scroll-in animation -- no ARKlight equivalent yet.
- The asterism (\u2042) section dividers were inline SVG-ish `<span>`
  dot clusters -- kept as plain text glyphs for now.
"""

from arklight import Page, Section, Container, Span, Heading, Text, Link, Blockquote, Cite, State, Bind

from components.nav import nav
from components.footer import footer
from components.work_card import work_card
from components.common import section_divider, PAGE_STYLESHEET_LINKS, PAGE_FAVICON
from content.works import WORKS, CURRENTLY_WRITING


def home():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/"),
        Section(
            Container(
                Span("Fantasy \u00b7 Science Fantasy \u00b7 Slice of Life", class_name="eyebrow"),
                Heading("Stories about people learning how to live again.", level=1),
                Text(
                    "Reincarnation, isekai, and the quiet, unglamorous work of rebuilding a "
                    "life \u2014 told through people who are imperfect, lost, and trying anyway.",
                    class_name="lede",
                ),
                Container(
                    Link("Read the works", href="/works", class_name="btn btn-primary"),
                    Link("From the writing desk", href="/journal", class_name="btn btn-ghost"),
                    class_name="cta-row",
                ),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(
                Container(
                    Span("Featured Works", class_name="eyebrow"),
                    Heading("Three stories, one question", level=2),
                    Text(
                        "Each begins differently \u2014 a second life, a wrong world, a body "
                        "that isn't yours \u2014 but all of them ask the same thing: what does "
                        "it take to actually live, not just survive?"
                    ),
                    class_name="section-head",
                ),
                Container(*[work_card(work) for work in WORKS], class_name="card-grid"),
                class_name="wrap",
            ),
            id="works",
        ),
        section_divider(),
        Section(
            Container(
                Container(
                    Span("Currently Writing", class_name="eyebrow"),
                    Heading("What's alive on the desk right now", level=2),
                    class_name="section-head",
                ),
                Container(
                    *[
                        Container(
                            Container(
                                Text(item["title"], class_name="status-title"),
                                Text(item["note"], class_name="status-note"),
                            ),
                            Span(
                                item["state"],
                                class_name="status-state paused" if item["paused"] else "status-state",
                            ),
                            class_name="status-row",
                        )
                        for item in CURRENTLY_WRITING
                    ],
                    class_name="status-panel",
                ),
                class_name="wrap container-narrow",
            ),
            class_name="alt-bg",
        ),
        section_divider(),
        Section(
            Container(
                Blockquote(
                    "\u201cI believe stories deserve endings. Some of mine span years; others "
                    "are written short and focused, on purpose \u2014 so I can keep learning how "
                    "to bring a narrative to a close I actually believe in.\u201d"
                ),
                Cite("\u2014 Rae ARK, on why The Shadow I Cast Over Two Beautiful Flowers exists"),
                class_name="wrap pull-quote",
            ),
        ),
        section_divider(),
        Section(
            Container(
                Container(
                    Span("Where to Read", class_name="eyebrow"),
                    Heading("Every chapter, free, wherever you already read", level=2),
                    class_name="section-head",
                ),
                Container(
                    Container(
                        Span("Royal Road", class_name="k"),
                        Link("All three stories \u2197", href="/works", class_name="go"),
                        class_name="read-card",
                    ),
                    Container(
                        Span("Scribble Hub", class_name="k"),
                        Link("Two stories \u2197", href="/works", class_name="go"),
                        class_name="read-card",
                    ),
                    Container(
                        Span("X / Twitter", class_name="k"),
                        Link("@Rae7866 \u2197", href="https://x.com/Rae7866", target="_blank", class_name="go"),
                        class_name="read-card",
                    ),
                    class_name="reads",
                ),
                class_name="wrap",
            ),
            class_name="alt-bg",
        ),
        footer(),
        bind_class=Bind.when("theme", "dark"),
        class_name="page-shell",
        ),
        title="Rae ARK \u2014 Web Novelist",
        description=(
            "Rae ARK writes fantasy and science-fantasy stories about people rebuilding "
            "themselves \u2014 reincarnation, isekai, and the quiet work of learning how to "
            "live again."
        ),
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
