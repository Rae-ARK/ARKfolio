const CACHE = "portfolio-v2";

const PRECACHE = [
    "/",
    "/index.html",
    "/about.html",
    "/works.html",
    "/journal.html",
    "/feedback.html",
    "/store.html",
    "/style.css",
    "/script.js",
    "/manifest.json",
    "/assets/images/profile.png",
    "/assets/images/The Shadow I Cast Over Two Beautiful Girls Act 1.png",
    "/assets/images/Summoned By Mistake, I Decided To Learn How To Live Arc 1.png",
    "/assets/images/Enigmatic Pathways Mystic Circuits vol 1.png"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE).then((cache) =>
            Promise.allSettled(PRECACHE.map((url) => cache.add(url)))
        )
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    event.respondWith(
        caches.open(CACHE).then(async (cache) => {
            const cached = await cache.match(event.request);

            const network = fetch(event.request)
                .then((response) => {
                    if (response.ok) cache.put(event.request, response.clone());
                    return response;
                })
                .catch(() => cached);

            return cached || network;
        })
    );
});