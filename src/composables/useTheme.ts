import { ref, watch } from 'vue'

export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'ark-theme'

// Same values as --paper in main.css. The browser/PWA status bar colour is
// set from the *in-app* theme here; a prefers-color-scheme media query on the
// <meta> tag only follows the phone's system setting and would ignore the
// toggle. index.html sets the same tag before first paint.
const THEME_COLOR = { light: '#f6f2e8', dark: '#17160f' } as const

function setThemeColor(value: Theme) {
  let tag = document.head.querySelector<HTMLMetaElement>('meta[name="theme-color"]')
  if (!tag) {
    tag = document.createElement('meta')
    tag.setAttribute('name', 'theme-color')
    document.head.appendChild(tag)
  }
  tag.setAttribute('content', THEME_COLOR[value])
}

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
    setThemeColor(value)
    try {
      window.localStorage.setItem(STORAGE_KEY, value)
    } catch {
      // Storage can be unavailable (private browsing, disabled cookies) —
      // theme still works for the session, it just won't persist.
    }
    // Lazy import: keeps this composable usable in plain web builds without
    // pulling in Capacitor plugin code unless it's actually needed.
    import('@/native/nativeShell').then(({ onThemeChange }) => onThemeChange(value))
  },
  { immediate: false }
)

export function useTheme() {
  function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  return { theme, toggleTheme }
}
