from arklight import Site
from pages.home import home
from pages.works import works
from pages.store import store
from pages.journal import journal
from pages.about import about
from pages.feedback import feedback
from pages.privacy import privacy
from pages.terms import terms

site = Site(name="arkfolio-arklight")


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
