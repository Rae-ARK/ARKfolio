"""Feedback page.

The original (`useFeedbackForm.ts`) captures a subject dropdown, an
optional name field, and a free-text message via Vue's two-way
`v-model` binding, then builds a single `mailto:` link on submit.

ARKlight's JS backend only wires up `on_click` today -- `on_input`/
two-way binding for `Input`/`Textarea`/`Select` is designed (v0.054)
but not implemented (see docs/PROGRESS.md). A `<form method="post"
enctype="text/plain" action="mailto:...">` was considered as a
zero-JS stand-in, but that trick's actual behavior (whether a mail
client's Subject field even gets set that way) is inconsistent across
browsers, so it was rejected -- a real regression per user, not just a
cosmetic one.

Straightforward alternative for now: pick a subject via a static
button per option (`Link` to a `mailto:` URL with subject and, where
useful, a short body prompt already filled in) -- same "click your
topic" mailto-based flow the original used, minus the ability to
customize the subject line or pre-fill your name from the same page.
Revisit once v0.054 (two-way binding) ships.
"""

from urllib.parse import quote

from arklight import Page, Section, Container, Span, Heading, Text, Link, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import PAGE_STYLESHEET_LINKS

RECIPIENT = "horizonarkstudio@gmail.com"

FEEDBACK_SUBJECTS = [
    "Feedback on the writing",
    "Feedback on the website",
    "Feedback on a paperback",
    "Feedback about the author",
]


def _mailto(subject: str) -> str:
    return f"mailto:{RECIPIENT}?subject={quote(subject)}"


def feedback():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/feedback"),
        Section(
            Container(
                Span("Get in Touch", class_name="eyebrow"),
                Heading("Feedback", level=1),
                Text(
                    "Thoughts on a story, the site, or anything else \u2014 this goes "
                    "straight to my inbox.",
                    class_name="lede",
                ),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(
                Container(
                    Text(
                        "Pick the topic closest to your feedback -- it opens your own email "
                        "app, addressed to "
                        f"{RECIPIENT}, with that subject already filled in. Write your "
                        "message and your name (if you'd like) right there before sending.",
                        class_name="notice-box",
                    ),
                    Container(
                        *[
                            Link(subject, href=_mailto(subject), class_name="btn btn-primary feedback-subject-btn")
                            for subject in FEEDBACK_SUBJECTS
                        ],
                        class_name="feedback-subject-grid",
                    ),
                    class_name="feedback-card",
                ),
                class_name="wrap",
            ),
        ),
        footer(),
        bind_class=Bind.when("theme", "dark"),
        class_name="page-shell",
        ),
        title="Feedback \u2014 Rae ARK",
        description="Send feedback on Rae ARK's stories, paperbacks, or this site directly via email.",
        links=PAGE_STYLESHEET_LINKS,
    )
