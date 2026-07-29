const CACHE = "portfolio-v3";

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

// Install
self.addEventListener("install", (event) => {
    event.waitUntil(
        (async () => {
            const cache = await caches.open(CACHE);
            await cache.addAll(PRECACHE);
        })()
    );

    self.skipWaiting();
});

// Activate
self.addEventListener("activate", (event) => {
    event.waitUntil(
        (async () => {
            const keys = await caches.keys();

            await Promise.all(
                keys
                    .filter((key) => key !== CACHE)
                    .map((key) => caches.delete(key))
            );

            await self.clients.claim();
        })()
    );
});

// Fetch
self.addEventListener("fetch", (event) => {

    if (event.request.method !== "GET") return;

    event.respondWith(
        (async () => {

            const cache = await caches.open(CACHE);

            // Cache First
            const cached = await cache.match(event.request);

            if (cached) {
                return cached;
            }

            try {

                const response = await fetch(event.request);

                // Cache only successful same-origin responses
                if (
                    response &&
                    response.status === 200 &&
                    response.type === "basic"
                ) {
                    cache.put(event.request, response.clone());
                }

                return response;

            } catch {

                // Offline fallback
                const fallback = await cache.match(event.request);

                if (fallback) {
                    return fallback;
                }

                return new Response("Offline", {
                    status: 503,
                    statusText: "Service Unavailable",
                    headers: {
                        "Content-Type": "text/plain"
                    }
                });

            }

        })()
    );

});
