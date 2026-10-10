Place your image files here (see README) — profile.png, horizon-ark-logo.png, and the three cover images.

Covers and profile.png also have a .webp copy with the same base name. main.css
serves the WebP through image-set() and keeps the PNG as the fallback, so keep
both files together. If you replace a PNG, regenerate its WebP (quality ~82).
og-card.jpg stays a JPEG on purpose: link-preview scrapers don't all read WebP.
