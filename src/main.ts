import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { vReveal } from './composables/useScrollReveal'
import './styles/main.css'

const app = createApp(App)
app.use(router)
app.directive('reveal', vReveal)
app.mount('#app')

// Register the service worker for offline support + installability.
// Skipped in dev so `npm run dev` never serves stale cached files.
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      console.error('Service worker registration failed:', err)
    })
  })
}
