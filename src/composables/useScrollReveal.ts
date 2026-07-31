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
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            observer?.unobserve(entry.target)
          }
        }
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    )
  }
  return observer
}

// Usage: <section v-reveal>...</section>
// Fades/slides an element in the first time it scrolls into view, then
// stops watching it. Elements are shown immediately (no animation) if the
// visitor has requested reduced motion.
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
