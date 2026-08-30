"""About page, ported from ARKfolio's AboutPage.vue.

`@error="hideOnError"` (hide the Horizon ARK logo if it 404s) has no
ARKlight runtime hook -- left as a plain `Image`, same call as footer.py.
"""

from arklight import Page, Section, Container, Span, Heading, Text, Link, Image, List, Item, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import section_divider, PAGE_STYLESHEET_LINKS

READ_LINKS = [
    {"site": "Royal Road", "title": "Enigmatic Pathways Mystic Circuits", "url": "https://www.royalroad.com/fiction/114101/enigmatic-pathways-mystic-circuits/"},
    {"site": "Royal Road", "title": "Summoned by Mistake, I Decided to Learn How to Live", "url": "https://www.royalroad.com/fiction/163034/summoned-by-mistake-i-decided-to-learn-how-to"},
    {"site": "Royal Road", "title": "The Shadow I Cast Over Two Beautiful Flowers", "url": "https://www.royalroad.com/fiction/173205/the-shadow-i-cast-over-two-beautiful-flowers/"},
    {"site": "Scribble Hub", "title": "Enigmatic Pathways Mystic Circuits", "url": "https://www.scribblehub.com/series/2312083/enigmatic-pathways-mystic-circuits/"},
    {"site": "Scribble Hub", "title": "Summoned by Mistake, I Decided to Learn How to Live", "url": "https://www.scribblehub.com/series/2312017/summoned-by-mistake-i-decided-to-learn-how-to-live/"},
    {"site": "X / Twitter", "title": "@Rae7866", "url": "https://x.com/Rae7866"},
]

CURRENTLY_WRITING_SHORT = [
    "Enigmatic Pathways Mystic Circuits \u2014 Vol. 3, in progress",
    "Summoned by Mistake, I Decided to Learn How to Live \u2014 Arc 3, ongoing",
    "The Shadow I Cast Over Two Beautiful Flowers \u2014 Act 2, on break",
]


def about():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/about"),
        Section(
            Container(
                Span("About", class_name="eyebrow"),
                Heading("Rae ARK", level=1),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(
                Container(
                    Text(
                        "I write character-driven fantasy and science fantasy about people "
                        "rebuilding themselves. Whether through reincarnation, another world, "
                        "or just difficult circumstances, my stories explore regret, "
                        "curiosity, responsibility, and the slow process of learning how to "
                        "live.",
                        class_name="lede-para",
                    ),
                    Text(
                        "My stories rarely revolve around saving the world. They're "
                        "interested in the people who live in it \u2014 the ones who are "
                        "imperfect, lost, and trying to find their place anyway."
                    ),
                    Text(
                        "Some of my projects start with careful planning. Others start with "
                        "a single idea that refuses to leave. Either way, I usually discover "
                        "the story alongside my readers rather than arriving with it fully "
                        "formed \u2014 what you're reading is often close to a first draft, "
                        "mistakes and all."
                    ),
                    Text(
                        "I write as a hobby, in whatever free time I can find around "
                        "everything else. That means release schedules shift, and I take "
                        "real breaks after finishing a big chunk of work \u2014 it's "
                        "practically tradition at this point. But I don't start things to "
                        "abandon them. If a story's still going, expect it to keep going, "
                        "even if slowly."
                    ),
                    section_divider(),
                    Heading("Why these kinds of stories", level=3),
                    Text(
                        "Enigmatic Pathways Mystic Circuits started after an anime watch "
                        "session turned into a real conversation about what family should "
                        "mean beyond raw talent. Re:Zero and Mushoku Tensei both left a mark "
                        "on how I think about second chances and slow, hard-won emotional "
                        "growth \u2014 not power fantasies, but people learning to carry what "
                        "happened to them."
                    ),
                    Text(
                        "Summoned by Mistake, I Decided to Learn How to Live became the place "
                        "for ideas that didn't fit anywhere else \u2014 something looser and "
                        "more relaxing to write. The Shadow I Cast Over Two Beautiful Flowers "
                        "exists for a different reason entirely: I wanted proof, mostly to "
                        "myself, that I could take a story to a real, satisfying ending."
                    ),
                ),
                Container(
                    Image(src="/assets/images/profile.png", alt="Rae ARK", class_name="avatar-large"),
                    Heading("The name", level=4),
                    Text("Rae ARK \u2014 \u5d50\u4e45 \u601c.", class_name="name-note"),
                    Heading("Find the stories", level=4),
                    Container(
                        *[
                            Container(
                                Text(f"{link['site']} \u2014 "),
                                Link(f"{link['title']}\u2197", href=link["url"], target="_blank"),
                                class_name="find-stories-row",
                            )
                            for link in READ_LINKS
                        ],
                        class_name="find-stories-list",
                    ),
                    Heading("Currently writing", level=4),
                    List(*[Item(t) for t in CURRENTLY_WRITING_SHORT]),
                    Container(
                        Image(
                            src="/assets/images/horizon-ark-logo.png",
                            alt="Horizon ARK Studio",
                            class_name="imprint-mark",
                        ),
                        Span("Horizon ARK Studio"),
                        class_name="imprint-credit",
                    ),
                    Link(
                        "This site's source on GitHub",
                        href="https://github.com/Rae-ARK/My-Portfolio",
                        target="_blank",
                        class_name="source-credit",
                    ),
                    class_name="about-side",
                ),
                class_name="wrap about-grid",
            ),
        ),
        footer(),
        bind_class=Bind.when("theme", "dark"),
        class_name="page-shell",
        ),
        title="About \u2014 Rae ARK",
        description=(
            "Rae ARK writes character-driven fantasy and science fantasy about people "
            "rebuilding themselves. Read about the author and the stories behind the stories."
        ),
        links=PAGE_STYLESHEET_LINKS,
    )
