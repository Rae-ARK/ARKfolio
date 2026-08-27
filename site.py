from arklight import Site
from pages.home import home

site = Site(name="arkfolio-arklight")


@site.page("/")
def _home():
    return home()
