from arklight import Site
from components.styles import register_styles
from components.theme_persist import apply_theme_persist
from pages.home import home
from pages.works import works
from pages.store import store
from pages.journal import journal
from pages.about import about
from pages.feedback import feedback
from pages.privacy import privacy
from pages.terms import terms

site = Site(name="arkfolio-arklight", max_width="100%")
register_styles(site)

# Theme-toggle persistence across page loads. Uses ARKlight's
# `Site.raw_postprocess(...)` escape hatch (experimental) rather than a
# separate build script -- see components/theme_persist.py for why
# this is needed and how it works. Plain `arklight build site.py -o
# ARK` is enough now; no wrapper script required.
site.raw_postprocess(apply_theme_persist)


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
