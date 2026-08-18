// Stage 6: makes the Capacitor-wrapped app behave like a native Android app
// instead of "a website in a box". Everything here is a no-op on the web
// build (Capacitor.isNativePlatform() is false there), so this file is safe
// to import unconditionally from the root layout.
import { Capacitor } from '@capacitor/core';
import { StatusBar, Style } from '@capacitor/status-bar';
import { SplashScreen } from '@capacitor/splash-screen';
import { App } from '@capacitor/app';
import { Browser } from '@capacitor/browser';
import { goto } from '$app/navigation';
import type { Theme } from '$lib/composables/useTheme.svelte';

const PAPER = '#f6f2e8';
const PAPER_DARK = '#17160f';

/** Match the status bar icon color to the current theme.
 *  Background color / overlay control is no longer respected by Android
 *  (edge-to-edge is enforced from Android 16 / API 36 onward), so layout
 *  instead relies on safe-area insets in CSS — see main.css. */
async function syncStatusBar(theme: Theme) {
	if (!Capacitor.isNativePlatform()) return;
	try {
		// Light theme -> dark icons (Style.Dark draws dark icons on a light bg).
		await StatusBar.setStyle({ style: theme === 'dark' ? Style.Light : Style.Dark });
	} catch {
		// StatusBar can be unavailable on some OEM WebViews; never block the app on it.
	}
}

/** Hardware/gesture back button: navigate the app's own history first,
 *  and only let Android exit the app once we're already at the root.
 *
 *  Vue Router exposed its own history bookkeeping via `history.state.back`.
 *  SvelteKit doesn't have a router object to ask, but it stamps every
 *  history entry it creates with `history.state['sveltekit:index']`,
 *  starting at 0 on first load and incrementing on each client-side
 *  navigation — checking that index is the direct equivalent here. */
function wireBackButton() {
	if (!Capacitor.isNativePlatform()) return;
	App.addListener('backButton', () => {
		const skIndex = (window.history.state as Record<string, unknown> | null)?.[
			'sveltekit:index'
		];
		if (typeof skIndex === 'number' && skIndex > 0) {
			window.history.back();
		} else if (window.location.pathname !== '/') {
			goto('/');
		} else {
			App.exitApp();
		}
	});
}

/** Open outbound links (Royal Road, Scribble Hub, X, retailers) in a Chrome
 *  Custom Tab instead of navigating the app's own WebView away from the app,
 *  or dropping to a jarring full external browser switch. */
function wireExternalLinks() {
	if (!Capacitor.isNativePlatform()) return;
	document.addEventListener('click', (event) => {
		const anchor = (event.target as HTMLElement)?.closest(
			'a[target="_blank"]'
		) as HTMLAnchorElement | null;
		if (!anchor?.href) return;
		event.preventDefault();
		Browser.open({ url: anchor.href });
	});
}

export async function initNativeShell(initialTheme: Theme) {
	if (!Capacitor.isNativePlatform()) return;

	wireBackButton();
	wireExternalLinks();
	await syncStatusBar(initialTheme);

	// The web app paints almost instantly (it's a small static bundle), so a
	// short deliberate hold + fade reads as a polished native launch rather
	// than a flash of blank screen.
	window.requestAnimationFrame(() => {
		setTimeout(() => {
			SplashScreen.hide({ fadeOutDuration: 220 }).catch(() => {});
		}, 150);
	});
}

export function onThemeChange(theme: Theme) {
	void syncStatusBar(theme);
}

export const NATIVE_BACKGROUND = { light: PAPER, dark: PAPER_DARK };
