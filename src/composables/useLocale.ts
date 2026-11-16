import { ref, watch } from 'vue'
import { i18n } from '@/I18n'
import type { Locale } from '@/I18n'

const STORAGE_KEY = 'ark-locale'

// index.html already sets lang on <html> before first paint (to avoid a
// flash of the wrong language) — read that same value back instead of
// recomputing it, so the two stay in sync. I18n.ts's getInitialLocale()
// reads the same attribute for the i18n instance's own initial value.
function getInitialLocale(): Locale {
  return document.documentElement.getAttribute('lang') === 'ja' ? 'ja' : 'en'
}

const locale = ref<Locale>(getInitialLocale())

watch(
  locale,
  (value) => {
    document.documentElement.setAttribute('lang', value)
    i18n.global.locale.value = value
    try {
      window.localStorage.setItem(STORAGE_KEY, value)
    } catch {
      // Storage can be unavailable (private browsing, disabled cookies) —
      // locale still works for the session, it just won't persist.
    }
  },
  { immediate: false }
)

export function useLocale() {
  function toggleLocale() {
    locale.value = locale.value === 'ja' ? 'en' : 'ja'
  }

  return { locale, toggleLocale }
}
