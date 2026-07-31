import { ref, watch } from 'vue'

export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'ark-theme'

// index.html already sets data-theme on <html> before first paint (to avoid
// a flash of the wrong palette) — read that same value back instead of
// recomputing it, so the two stay in sync.
function getInitialTheme(): Theme {
  const current = document.documentElement.getAttribute('data-theme')
  return current === 'dark' ? 'dark' : 'light'
}

const theme = ref<Theme>(getInitialTheme())

watch(
  theme,
  (value) => {
    document.documentElement.setAttribute('data-theme', value)
    try {
      window.localStorage.setItem(STORAGE_KEY, value)
    } catch {
      // Storage can be unavailable (private browsing, disabled cookies) —
      // theme still works for the session, it just won't persist.
    }
  },
  { immediate: false }
)

export function useTheme() {
  function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  return { theme, toggleTheme }
}
