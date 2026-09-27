"""Feedback page.

The original (`useFeedbackForm.ts`) captures a subject dropdown, an
optional name field, and a free-text message via Vue's two-way
`v-model` binding, then builds a single `mailto:` link on submit.

As of this alpha, ARKlight's `Input`/`Textarea` *do* support two-way
binding (`Bind.model(...)`, `runtime/model.py`) -- so name/message
capture itself is reachable now. What's still missing is a way to
*use* that captured state to build the `mailto:` link: `Action`'s
vocabulary is closed to `set`/`increment`/`decrement`/`toggle_bool`/
`reset`/`append`/`remove` (`arklight.ir.schema.ACTION_REGISTRY`), with
no "navigate" or "compose a URL from state" action, and `Bind(...)` is
only accepted as an `Action.set`/`.append` *value* -- not as a
component prop like `Link(href=...)` (`docs/Foundational/
AUTHORING-GUIDE.md`, "Bind(...) as an argument"). So a state-driven
`mailto:` href still can't be expressed in the declared vocabulary.

A `<form method="post" enctype="text/plain" action="mailto:...">` was
considered as a zero-JS stand-in for the whole form, but that trick's
actual behavior (whether a mail client's Subject field even gets set
that way) is inconsistent across browsers, so it was rejected -- a
real regression per user, not just a cosmetic one.

Kept the original solution: pick a subject via a static button per
option (`Link` to a `mailto:` URL with subject and, where useful, a
short body prompt already filled in) -- same "click your topic"
mailto-based flow the Vue site used, minus the ability to customize
the subject line or pre-fill your name from the same page. Revisit if
`Action`/`Bind` ever grows a way to read live state into a prop like
`href`.
"""

from urllib.parse import quote

from arklight import Page, Section, Container, Span, Heading, Text, Link, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import PAGE_STYLESHEET_LINKS, PAGE_FAVICON

RECIPIENT = "horizonarkstudio@gmail.com"

FEEDBACK_SUBJECTS = [
    "Feedback on the writing",
    "Feedback on the website",
    "Feedback on a paperback",
    "Feedback about the author",
]


def _mailto(subject: str) -> str:
    return f"mailto:{RECIPIENT}?subject={quote(subject)}"


def _subject_button(subject: str):
    """One "pick your topic" button.

    Pulled into its own function, same reasoning as home.py's
    _status_row(): keeps this page's own call tree under ARKlight's
    8-level bracket-nesting cap.
    """
    return Link(subject, href=_mailto(subject), class_name="btn btn-primary feedback-subject-btn")


def feedback():
    return Page(
        State("theme", False, persist=True),
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
                            *[_subject_button(subject) for subject in FEEDBACK_SUBJECTS],
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
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
