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

	// TODO(nativeShell port): the Vue version lazy-imports native/nativeShell
	// here to sync the Android status bar color on theme change. Wire this
	// back in once nativeShell.ts is ported — see docs/reference migration
	// scope, step 6.
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
