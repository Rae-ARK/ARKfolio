Image layout:

  png/    original PNGs: profile.png, horizon-ark-logo.png and the cover images
  webp/   WebP copies of profile.png and the covers (same base names)
  og-card.jpg   share card, kept at the top level (JPEG on purpose: link-preview
                scrapers don't all read WebP)

main.css serves the WebP through image-set() and keeps the PNG as the fallback,
so keep both folders in step. If you replace a PNG, regenerate its WebP
(quality ~82) into webp/ with the same base name.
