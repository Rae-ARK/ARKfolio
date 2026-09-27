from arklight import Site
from components.styles import register_styles
from pages.home import home
from pages.works import works
from pages.store import store
from pages.journal import journal
from pages.about import about
from pages.feedback import feedback
from pages.privacy import privacy
from pages.terms import terms

# app_shell=True: internal-link clicks do an in-place htmx-boosted swap
# instead of a full page reload (closer to the Vue site's SPA feel,
# and the main point of the Android wrapper below). Pairs with
# shell_persistent=True on the header/footer (components/nav.py,
# components/footer.py) so they aren't torn down between pages.
site = Site(name="arkfolio-arklight", max_width="100%", app_shell=True)
register_styles(site)

# Theme-toggle persistence across page loads used to require a
# hand-rolled `Site.raw_postprocess(...)` escape hatch (see git
# history for components/theme_persist.py) -- raw_postprocess is now
# removed upstream. `State("theme", False, persist=True)` on every
# page (pages/*.py) is the native replacement: it round-trips through
# localStorage on its own, so no extra wiring belongs here at all.


@site.page("/")
def _home():
    return home()


@site.page("/works")
def _works():
    return works()


@site.page("/store")
def _store():
    return store()


@site.page("/journal")
def _journal():
    return journal()


@site.page("/about")
def _about():
    return about()


@site.page("/feedback")
def _feedback():
    return feedback()


@site.page("/privacy")
def _privacy():
    return privacy()


@site.page("/terms")
def _terms():
    return terms()
