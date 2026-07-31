import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// Stage 1 (MVP) config — plain Vue 3 + Vite web app.
// Capacitor's `webDir` will point at `dist` once Stage 3 adds it.
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) }
  }
})
