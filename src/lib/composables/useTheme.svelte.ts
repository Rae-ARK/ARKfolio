export type Theme = 'light' | 'dark';

const STORAGE_KEY = 'ark-theme';

// app.html already sets data-theme on <html> before first paint (to avoid
// a flash of the wrong palette) — read that same value back instead of
// recomputing it, so the two stay in sync.
function getInitialTheme(): Theme {
	if (typeof document === 'undefined') return 'light';
	const current = document.documentElement.getAttribute('data-theme');
	return current === 'dark' ? 'dark' : 'light';
}

// Module-level rune: one shared instance across every component that
// imports useTheme, same effect as the Vue version's module-scoped ref.
let theme = $state<Theme>(getInitialTheme());

function applyTheme(value: Theme) {
	document.documentElement.setAttribute('data-theme', value);
	try {
		window.localStorage.setItem(STORAGE_KEY, value);
	} catch {
		// Storage can be unavailable (private browsing, disabled cookies) —
		// theme still works for the session, it just won't persist.
	}

	// Lazy import: keeps this composable usable in plain web builds without
	// pulling in Capacitor plugin code unless it's actually needed.
	import('$lib/native/nativeShell').then(({ onThemeChange }) => onThemeChange(value));
}

export function useTheme() {
	function toggleTheme() {
		theme = theme === 'dark' ? 'light' : 'dark';
		applyTheme(theme);
	}

	return {
		get theme() {
			return theme;
		},
		toggleTheme
	};
}
