<!--
  Horizon ARK Studio's mark (ring + inverted triangle), redrawn as a plain
  SVG so it stays crisp at any display size instead of being a flattened
  PNG scaled down to a sliver. Colors are the mark's own cyan/blue palette,
  not the site's warm-paper/ink-teal tokens — this is a brand mark, not a
  themed UI icon, so it stays constant across light/dark theme.
-->
<template>
  <svg class="logo-mark" viewBox="0 0 100 100" role="img" aria-label="Horizon ARK Studio logo">
    <defs>
      <linearGradient id="arkRingGrad" x1="15%" y1="5%" x2="85%" y2="95%">
        <stop offset="0%" stop-color="#9ff1ff" />
        <stop offset="32%" stop-color="#1c86c2" />
        <stop offset="62%" stop-color="#0a3a63" />
        <stop offset="100%" stop-color="#1c86c2" />
      </linearGradient>
      <linearGradient id="arkTriGrad" x1="50%" y1="0%" x2="50%" y2="100%">
        <stop offset="0%" stop-color="#eafdff" />
        <stop offset="45%" stop-color="#7fe9ff" />
        <stop offset="100%" stop-color="#1fb3e0" />
      </linearGradient>
    </defs>
    <circle cx="50" cy="50" r="41.5" fill="none" stroke="url(#arkRingGrad)" stroke-width="9" />
    <path d="M23 34 L77 34 L50 83 Z" fill="url(#arkTriGrad)" stroke="#0a3a63" stroke-width="3" stroke-linejoin="round" />
  </svg>
</template>
