import { ref } from 'vue'
import { i18n } from '@/I18n'
import type { Locale } from '@/I18n'

// The URL is the source of truth for language: /ja/... is Japanese, anything
// else is English. The router (router/index.ts) calls setLocale() on every
// navigation. index.html sets <html lang> from the path before first paint,
// and this reads that attribute back so the two agree from the first render.
function getInitialLocale(): Locale {
  return document.documentElement.getAttribute('lang') === 'ja' ? 'ja' : 'en'
}

const locale = ref<Locale>(getInitialLocale())

function setLocale(value: Locale) {
  if (locale.value === value) return
  locale.value = value
  document.documentElement.setAttribute('lang', value)
  i18n.global.locale.value = value
}

export function useLocale() {
  return { locale, setLocale }
}
