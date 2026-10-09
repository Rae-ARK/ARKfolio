<!--
  Horizon ARK Studio's mark (ring + inverted triangle), redrawn as a plain
  SVG so it stays crisp at any display size instead of being a flattened
  PNG scaled down to a sliver. Colors and structure are matched to the
  original artwork at full zoom: the ring reads as a glossy metal tube
  (dark edge / bright band / mid band / bright band / dark edge, banded
  radially rather than a single flat gradient stroke) with a soft specular
  highlight along its top arc, and the triangle has its own inner highlight
  line plus a center-weighted fill — not just the flat ring + single-
  gradient fill of the first vector pass. Colors are the mark's own
  cyan/blue palette, not the site's warm-paper/ink-teal tokens, since this
  is a fixed brand mark rather than a themed UI icon.
-->
<template>
  <svg class="logo-mark" viewBox="0 0 100 100" role="img" aria-label="Horizon ARK Studio logo">
    <defs>
      <linearGradient id="arkHighlightArc" gradientUnits="userSpaceOnUse" x1="14.93" y1="29.75" x2="85.07" y2="29.75">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
        <stop offset="50%" stop-color="#ffffff" stop-opacity="0.85" />
        <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
      </linearGradient>
      <radialGradient id="arkTriFill" cx="50%" cy="28%" r="75%">
        <stop offset="0%" stop-color="#f3feff" />
        <stop offset="40%" stop-color="#9df3ff" />
        <stop offset="100%" stop-color="#1fb3e0" />
      </radialGradient>
    </defs>

    <!-- ring, banded outer to inner to read as a glossy tube -->
    <circle cx="50" cy="50" r="42.3" fill="none" stroke="#07263f" stroke-width="1.2" />
    <circle cx="50" cy="50" r="40.5" fill="none" stroke="#8ff0ff" stroke-width="3.2" />
    <circle cx="50" cy="50" r="37.3" fill="none" stroke="#13578a" stroke-width="4.3" />
    <circle cx="50" cy="50" r="34.3" fill="none" stroke="#6fe3fa" stroke-width="2.1" />
    <circle cx="50" cy="50" r="32.4" fill="none" stroke="#07263f" stroke-width="1.3" />

    <!-- specular glint along the top of the ring -->
    <path d="M 14.93 29.75 A 40.5 40.5 0 0 1 85.07 29.75" fill="none" stroke="url(#arkHighlightArc)" stroke-width="3.6" stroke-linecap="round" />

    <!-- triangle: dark outline, inner highlight line, center-weighted fill -->
    <path d="M22.5 33.5 L77.5 33.5 L50 83 Z" fill="#07263f" stroke="#07263f" stroke-width="6.5" stroke-linejoin="round" />
    <path d="M22.5 33.5 L77.5 33.5 L50 83 Z" fill="url(#arkTriFill)" stroke="#6fe3fa" stroke-width="1.4" stroke-linejoin="round" />
  </svg>
</template>
