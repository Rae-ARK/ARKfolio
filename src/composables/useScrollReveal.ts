import type { Directive } from 'vue'

function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

let observer: IntersectionObserver | null = null

function getObserver(): IntersectionObserver {
  if (!observer) {
    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          // Toggle rather than one-shot add + unobserve, so the reveal
          // replays on the way back up too, not just scrolling down.
          // Keeps this fallback in sync with the animation-timeline: view()
          // primitive above, which is scroll-position-linked and so
          // already reverses/replays in both directions for free.
          entry.target.classList.toggle('is-visible', entry.isIntersecting)
        }
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    )
  }
  return observer
}

// Usage: <section v-reveal>...</section>
// Fades/slides an element in each time it scrolls into view — forward or
// backward — and fades it back out when it scrolls back past the
// threshold, rather than revealing once and staying. Elements are shown
// immediately (no animation) if the visitor has requested reduced motion.
export const vReveal: Directive<HTMLElement> = {
  mounted(el) {
    if (prefersReducedMotion()) {
      el.classList.add('is-visible')
      return
    }
    el.setAttribute('data-reveal', '')
    getObserver().observe(el)
  },
  unmounted(el) {
    observer?.unobserve(el)
  },
}
