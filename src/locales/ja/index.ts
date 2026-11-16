// The Japanese locale, split into one JSON file per section so each piece
// of UI chrome (nav, header, footer, feedback form, 404 page) stays easy to
// find and diff on its own. This file just reassembles them into the same
// shape I18n.ts always expected from ja.json.
import _stage from './stage.json'
import nav from './nav.json'
import header from './header.json'
import footer from './footer.json'
import feedback from './feedback.json'
import notFound from './notFound.json'

export default {
  _stage,
  nav,
  header,
  footer,
  feedback,
  notFound,
}
