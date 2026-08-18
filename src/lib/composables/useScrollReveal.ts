function prefersReducedMotion(): boolean {
	return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

let observer: IntersectionObserver | null = null;

function getObserver(): IntersectionObserver {
	if (!observer) {
		observer = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						entry.target.classList.add('is-visible');
						observer?.unobserve(entry.target);
					}
				}
			},
			{ threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
		);
	}
	return observer;
}

// Usage: <section use:reveal>...</section>
// Fades/slides an element in the first time it scrolls into view, then
// stops watching it. Elements are shown immediately (no animation) if the
// visitor has requested reduced motion.
//
// Svelte actions are the direct equivalent of Vue custom directives here:
// the function body runs once on mount (same as `mounted(el)`), and the
// returned `destroy()` runs on unmount (same as `unmounted(el)`).
export function reveal(node: HTMLElement) {
	if (prefersReducedMotion()) {
		node.classList.add('is-visible');
		return;
	}
	node.setAttribute('data-reveal', '');
	getObserver().observe(node);

	return {
		destroy() {
			observer?.unobserve(node);
		}
	};
}
