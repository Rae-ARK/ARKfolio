import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { vReveal } from './composables/useScrollReveal'
import { useTheme } from './composables/useTheme'
import './styles/fonts.css'
import './styles/main.css'

const app = createApp(App)
app.use(router)
app.directive('reveal', vReveal)
app.mount('#app')

// Stage 3: on Android this wires the hardware back button, status bar icon
// color, splash screen hide, and Custom Tab links. No-op on the web build.
import('./native/nativeShell').then(({ initNativeShell }) => {
  const { theme } = useTheme()
  initNativeShell(router, theme.value)
})

// Linux/Windows/macOS desktop build: wires up the Neutralino window shell
// (title, show, clean exit on close). No-op on the web/Android build.
import('./native/neutralinoShell').then(({ initNeutralinoShell }) => {
  initNeutralinoShell()
})

// Register the service worker for offline support + installability.
// Skipped in dev so `npm run dev` never serves stale cached files.
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      console.error('Service worker registration failed:', err)
    })
  })
}
