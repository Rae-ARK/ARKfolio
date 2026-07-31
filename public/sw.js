// Rae ARK — service worker
//
// Hand-rolled on purpose (no Workbox/vite-plugin-pwa) to keep the
// dependency list minimal, per the project's "avoid unnecessary
// dependencies" rule. Three strategies, chosen per request type:
//
//   1. Navigations (HTML pages)   -> network-first, cached fallback
//   2. Same-origin static assets  -> stale-while-revalidate
//   3. Cross-origin (fonts, etc.) -> cache-first
//
// Bump CACHE_VERSION whenever this file's caching *behavior* changes,
// so old caches get cleaned up on activate.
const CACHE_VERSION = 'arkfolio-v1'
const CORE_CACHE = `${CACHE_VERSION}-core`
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`

// Small, hand-picked shell that's safe to precache because these paths
// don't change name between builds — unlike hashed /assets/*.js chunks,
// which get added to the runtime cache the first time they're requested.
const CORE_ASSETS = ['/', '/manifest.webmanifest', '/icons/icon-192.png', '/icons/icon-512.png']

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CORE_CACHE)
      .then((cache) => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.filter((key) => key !== CORE_CACHE && key !== RUNTIME_CACHE).map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  )
})

function putRuntime(request, response) {
  if (response && response.ok) {
    const copy = response.clone()
    caches.open(RUNTIME_CACHE).then((cache) => cache.put(request, copy))
  }
  return response
}

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return

  const url = new URL(request.url)
  const isSameOrigin = url.origin === self.location.origin

  // 1. Page navigations: try the network first (so visitors always get the
  // latest deploy), fall back to the cached shell if offline.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => putRuntime(request, response))
        .catch(() => caches.match('/').then((cached) => cached || caches.match(request)))
    )
    return
  }

  // 2. Same-origin static assets (hashed JS/CSS bundles, local images):
  // stale-while-revalidate — instant from cache, refreshed quietly in the background.
  if (isSameOrigin) {
    event.respondWith(
      caches.match(request).then((cached) => {
        const network = fetch(request)
          .then((response) => putRuntime(request, response))
          .catch(() => cached)
        return cached || network
      })
    )
    return
  }

  // 3. Cross-origin requests (Google Fonts, etc.): cache-first, since these rarely change.
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).then((response) => putRuntime(request, response)))
  )
})
