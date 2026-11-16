// The Japanese locale, split into one JSON file per section so each piece
// of UI chrome (nav, header, footer, feedback form, 404 page) and each page's
// content (about, home, journal, privacy, store, terms, works) stays easy to
// find and diff on its own. This file just reassembles them into the same
// shape I18n.ts always expected from ja.json.
import _stage from './stage.json'
import nav from './nav.json'
import header from './header.json'
import footer from './footer.json'
import feedback from './feedback.json'
import notFound from './notFound.json'
import about from './about.json'
import home from './home.json'
import journal from './journal.json'
import privacy from './privacy.json'
import store from './store.json'
import terms from './terms.json'
import works from './works.json'

export default {
  _stage,
  nav,
  header,
  footer,
  feedback,
  notFound,
  about,
  home,
  journal,
  privacy,
  store,
  terms,
  works,
}
