"""Every page must declare its "theme" State with persist=True.

Replaces the old test_theme_persist.py, which unit-tested the
hand-rolled inject() HTML-rewriting function in
components/theme_persist.py. That whole module is gone now --
`State("theme", False, persist=True)` is ARKlight's own native
localStorage-persistence flag (arklight.api.State), so there is no
more hand-written persistence logic of ours left to unit-test here.
What's left worth checking mechanically is the one thing every page
has to get right by hand: actually setting persist=True on its
"theme" State node, since a copy-pasted `State("theme", False)`
(persist defaulting back to False) would silently un-persist the
theme toggle on just that one page without breaking the build.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pages.about import about
from pages.feedback import feedback
from pages.home import home
from pages.journal import journal
from pages.privacy import privacy
from pages.store import store
from pages.terms import terms
from pages.works import works

PAGES = {
    "about": about,
    "feedback": feedback,
    "home": home,
    "journal": journal,
    "privacy": privacy,
    "store": store,
    "terms": terms,
    "works": works,
}


def _theme_state_node(page_node):
    """Find the top-level State("theme", ...) node in a Page(...)'s children."""
    for child in page_node.children:
        if getattr(child, "type", None) == "State" and child.props.get("name") == "theme":
            return child
    return None


def test_every_page_declares_persisted_theme_state():
    missing, not_persisted = [], []
    for name, page_fn in PAGES.items():
        state_node = _theme_state_node(page_fn())
        if state_node is None:
            missing.append(name)
        elif state_node.props.get("persist") is not True:
            not_persisted.append(name)

    assert not missing, f"page(s) with no theme State declared: {missing}"
    assert not not_persisted, f"page(s) with theme State but persist != True: {not_persisted}"
