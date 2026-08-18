<script lang="ts">
	import { reveal } from '$lib/composables/useScrollReveal';

	const readLinks = [
		{
			site: 'Royal Road',
			title: 'Enigmatic Pathways Mystic Circuits',
			url: 'https://www.royalroad.com/fiction/114101/enigmatic-pathways-mystic-circuits/'
		},
		{
			site: 'Royal Road',
			title: 'Summoned by Mistake, I Decided to Learn How to Live',
			url: 'https://www.royalroad.com/fiction/163034/summoned-by-mistake-i-decided-to-learn-how-to'
		},
		{
			site: 'Royal Road',
			title: 'The Shadow I Cast Over Two Beautiful Flowers',
			url: 'https://www.royalroad.com/fiction/173205/the-shadow-i-cast-over-two-beautiful-flowers/'
		},
		{
			site: 'Scribble Hub',
			title: 'Enigmatic Pathways Mystic Circuits',
			url: 'https://www.scribblehub.com/series/2312083/enigmatic-pathways-mystic-circuits/'
		},
		{
			site: 'Scribble Hub',
			title: 'Summoned by Mistake, I Decided to Learn How to Live',
			url: 'https://www.scribblehub.com/series/2312017/summoned-by-mistake-i-decided-to-learn-how-to-live/'
		},
		{ site: 'X / Twitter', title: '@Rae7866', url: 'https://x.com/Rae7866' }
	];

	const currentlyWriting = [
		'Enigmatic Pathways Mystic Circuits — Vol. 3, in progress',
		'Summoned by Mistake, I Decided to Learn How to Live — Arc 3, ongoing',
		'The Shadow I Cast Over Two Beautiful Flowers — Act 2, on break'
	];

	function hideOnError(event: Event) {
		(event.target as HTMLImageElement).style.display = 'none';
	}
</script>

<svelte:head>
	<title>About — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:36px;">
	<div class="wrap">
		<span class="eyebrow">About</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Rae ARK</h1>
	</div>
</section>

<section style="padding-top:0;" use:reveal>
	<div class="wrap about-grid">
		<div>
			<p style="font-size:1.08rem; color:var(--ink);">
				I write character-driven fantasy and science fantasy about people rebuilding themselves.
				Whether through reincarnation, another world, or just difficult circumstances, my stories
				explore regret, curiosity, responsibility, and the slow process of learning how to live.
			</p>
			<p>
				My stories rarely revolve around saving the world. They're interested in the people who
				live in it — the ones who are imperfect, lost, and trying to find their place anyway.
			</p>
			<p>
				Some of my projects start with careful planning. Others start with a single idea that
				refuses to leave. Either way, I usually discover the story alongside my readers rather
				than arriving with it fully formed — what you're reading is often close to a first draft,
				mistakes and all.
			</p>
			<p>
				I write as a hobby, in whatever free time I can find around everything else. That means
				release schedules shift, and I take real breaks after finishing a big chunk of work — it's
				practically tradition at this point. But I don't start things to abandon them. If a
				story's still going, expect it to keep going, even if slowly.
			</p>

			<div class="section-divider" style="margin:48px 0;">
				<span class="asterism"
					><span class="dot"></span><span class="dot"></span><span class="dot"></span></span
				>
			</div>

			<h3>Why these kinds of stories</h3>
			<p>
				Enigmatic Pathways Mystic Circuits started after an anime watch session turned into a
				real conversation about what family should mean beyond raw talent. Re:Zero and Mushoku
				Tensei both left a mark on how I think about second chances and slow, hard-won emotional
				growth — not power fantasies, but people learning to carry what happened to them.
			</p>
			<p>
				Summoned by Mistake, I Decided to Learn How to Live became the place for ideas that
				didn't fit anywhere else — something looser and more relaxing to write. The Shadow I Cast
				Over Two Beautiful Flowers exists for a different reason entirely: I wanted proof, mostly
				to myself, that I could take a story to a real, satisfying ending.
			</p>
		</div>

		<aside class="about-side">
			<div class="avatar-large" style="background-image:url('/assets/images/profile.png')"></div>
			<h4>The name</h4>
			<p style="font-size:0.9rem; color:var(--ink-soft); margin-bottom:20px;">Rae ARK — 嵐久 怜.</p>
			<h4>Find the stories</h4>
			<ul>
				{#each readLinks as link (link.url)}
					<li>
						{link.site} —
						<a
							href={link.url}
							target="_blank"
							rel="noopener"
							style="color:var(--accent); font-weight:600;">{link.title}↗</a
						>
					</li>
				{/each}
			</ul>
			<h4 style="margin-top:22px;">Currently writing</h4>
			<ul>
				{#each currentlyWriting as item (item)}
					<li>{item}</li>
				{/each}
			</ul>
			<div class="imprint-credit">
				<img
					class="imprint-mark"
					src="/assets/images/horizon-ark-logo.png"
					alt="Horizon ARK Studio"
					onerror={hideOnError}
				/>
				<span>Horizon ARK Studio</span>
			</div>
			<a
				class="source-credit"
				href="https://github.com/Rae-ARK/My-Portfolio"
				target="_blank"
				rel="noopener"
			>
				<svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"
					><path
						d="M12 2C6.48 2 2 6.58 2 12.17c0 4.47 2.87 8.26 6.84 9.6.5.1.68-.22.68-.5v-1.94c-2.78.62-3.37-1.36-3.37-1.36-.46-1.2-1.11-1.52-1.11-1.52-.9-.63.07-.62.07-.62 1 .07 1.53 1.05 1.53 1.05.9 1.55 2.36 1.1 2.93.84.09-.66.35-1.1.64-1.36-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.74 0 0 .84-.28 2.75 1.05a9.3 9.3 0 0 1 5 0c1.9-1.33 2.75-1.05 2.75-1.05.55 1.43.2 2.48.1 2.74.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9v2.82c0 .28.18.6.69.5A10.19 10.19 0 0 0 22 12.17C22 6.58 17.52 2 12 2Z"
					/></svg
				>
				<span>This site's source on GitHub</span>
			</a>
		</aside>
	</div>
</section>
