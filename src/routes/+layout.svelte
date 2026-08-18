<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import '$lib/styles/main.css';
	import AppHeader from '$lib/components/AppHeader.svelte';
	import AppFooter from '$lib/components/AppFooter.svelte';

	let { children } = $props();
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
