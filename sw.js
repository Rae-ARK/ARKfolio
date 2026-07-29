const CACHE = "portfolio-v1";

const FILES = [
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

    "/assets/profile.png",
    "/assets/The Shadow I Cast Over Two Beautiful Girls Act 1.png",
    "/assets/Summoned By Mistake, I Decided To Learn How To Live Arc 1.png",
    "/assets/Enigmatic Pathways Mystic Circuits vol 1.png"
];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE).then(cache => cache.addAll(FILES))
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});