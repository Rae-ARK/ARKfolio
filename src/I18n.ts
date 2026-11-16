import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import ja from '@/locales/ja.json'

export type Locale = 'en' | 'ja'

// index.html sets <html lang> before first paint — the same way it sets
// data-theme before useTheme.ts's getInitialTheme() reads it back — so
// there's no flash of the wrong language on first render. Read that same
// attribute here instead of recomputing it, so i18n agrees with the DOM
// from the very first render. useLocale.ts reads the same attribute for
// its own initial value.
function getInitialLocale(): Locale {
  return document.documentElement.getAttribute('lang') === 'ja' ? 'ja' : 'en'
}

export const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: 'en',
  messages: { en, ja },
})
