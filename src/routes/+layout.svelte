<script lang="ts">
	import { onMount } from 'svelte';
	import favicon from '$lib/assets/favicon.svg';
	import '$lib/styles/main.css';
	import AppHeader from '$lib/components/AppHeader.svelte';
	import AppFooter from '$lib/components/AppFooter.svelte';
	import { useTheme } from '$lib/composables/useTheme.svelte';

	let { children } = $props();

	// Stage 6: on Android this wires the hardware back button, status bar icon
	// color, splash screen hide, and Custom Tab links. No-op on the web build.
	onMount(() => {
		const { theme } = useTheme();
		import('$lib/native/nativeShell').then(({ initNativeShell }) => {
			initNativeShell(theme);
		});
	});

	// Stage 8: on Linux/Windows/macOS (Neutralino) this wires the window
	// title/show, clean exit on close, and OS-browser external links. No-op
	// on the web/Android build.
	onMount(() => {
		import('$lib/native/neutralinoShell').then(({ initNeutralinoShell }) => {
			initNeutralinoShell();
		});
	});
</script>

<svelte:head>
	<title>Rae ARK — Web Novelist</title>
	<link rel="icon" href={favicon} />
</svelte:head>

<AppHeader />
<main>
	{@render children()}
</main>
<AppFooter />
