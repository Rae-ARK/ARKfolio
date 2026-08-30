"""Privacy Policy page, ported from ARKfolio's PrivacyPolicyPage.vue."""

from arklight import Page, Section, Container, Span, Heading, Text, Link, State, Bind

from components.nav import nav
from components.footer import footer
from components.common import PAGE_STYLESHEET_LINKS, PAGE_FAVICON

LAST_UPDATED = "July 2026"
CONTACT_EMAIL = "contact@rae-ark.example"


def privacy():
    return Page(
        State("theme", False),
        Container(
        nav(theme_state="theme", current_route="/privacy"),
        Section(
            Container(
                Span("Legal", class_name="eyebrow"),
                Heading("Privacy Policy", level=1),
                Text(f"Last updated: {LAST_UPDATED}", class_name="lede"),
                class_name="wrap",
            ),
            class_name="hero",
        ),
        Section(
            Container(
                Container(
                    Text(
                        "This site and app (\u201cRae ARK\u201d) is an author portfolio. It "
                        "exists to showcase web novels, journal updates, and ways to read or "
                        "support the work. This policy explains what little data is involved "
                        "and why."
                    ),
                    Heading("What's collected", level=3),
                    Text(
                        "The site itself does not run analytics, trackers, or advertising, "
                        "and it does not create accounts or store personal data on a server. "
                        "The only place personal information can enter the picture is the "
                        "Feedback page, which opens your own email app with a pre-filled "
                        "address and subject \u2014 anything you write there is sent directly "
                        "from your device using your own email provider, under that "
                        "provider's privacy policy, not ours."
                    ),
                    Heading("App permissions (Android)", level=3),
                    Text(
                        "The Android app requests internet access only. This is used to open "
                        "external links \u2014 Royal Road, Scribble Hub, X/Twitter, and "
                        "similar \u2014 in your browser, and to check for updated content on "
                        "future visits. The app does not request access to your contacts, "
                        "location, camera, microphone, storage, or any other device "
                        "permission."
                    ),
                    Heading("Local storage", level=3),
                    Text(
                        "A single preference \u2014 whether you've chosen light or dark mode "
                        "\u2014 is saved on your own device so it's remembered next time. It "
                        "never leaves your device and isn't linked to you personally."
                    ),
                    Heading("Third-party links", level=3),
                    Text(
                        "Buttons and links to Royal Road, Scribble Hub, X/Twitter, and retail "
                        "storefronts take you to third-party sites with their own privacy "
                        "policies. Once you leave this site or app, this policy no longer "
                        "applies."
                    ),
                    Heading("Children's privacy", level=3),
                    Text(
                        "This site is not directed at children under 13, and no data is "
                        "knowingly collected from them."
                    ),
                    Heading("Changes to this policy", level=3),
                    Text(
                        "If this policy changes, the update will be posted here with a new "
                        "\"last updated\" date."
                    ),
                    Heading("Contact", level=3),
                    Container(
                        Span("Questions about this policy can be sent via the "),
                        Link("Feedback", href="/feedback"),
                        Span(f" page, or to {CONTACT_EMAIL}."),
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
        title="Privacy Policy \u2014 Rae ARK",
        description="How the Rae ARK site and Android app handle data and permissions.",
        favicon=PAGE_FAVICON,
        links=PAGE_STYLESHEET_LINKS,
    )
