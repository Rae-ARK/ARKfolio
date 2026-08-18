<script lang="ts">
	import { works, currentlyWriting } from '$lib/data/works';
	import WorkCard from '$lib/components/WorkCard.svelte';
</script>

<svelte:head>
	<title>Rae ARK — Web Novelist</title>
</svelte:head>

<section class="hero">
	<div class="wrap">
		<span class="eyebrow">Fantasy · Science Fantasy · Slice of Life</span>
		<h1>Stories about people learning how to live again.</h1>
		<p class="lede">
			Reincarnation, isekai, and the quiet, unglamorous work of rebuilding a life — told through
			people who are imperfect, lost, and trying anyway.
		</p>
		<div class="cta-row">
			<a href="/works" class="btn btn-primary">Read the works</a>
			<a href="/journal" class="btn btn-ghost">From the writing desk</a>
		</div>
	</div>
</section>

<section id="works">
	<div class="wrap">
		<div class="section-head">
			<span class="eyebrow">Featured Works</span>
			<h2>Three stories, one question</h2>
			<p>
				Each begins differently — a second life, a wrong world, a body that isn't yours — but all
				of them ask the same thing: what does it take to actually live, not just survive?
			</p>
		</div>
		<div class="card-grid">
			{#each works as work (work.slug)}
				<WorkCard {work} />
			{/each}
		</div>
	</div>
</section>

<div class="section-divider">
	<span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"
		></span></span
	>
</div>

<section class="alt-bg">
	<div class="wrap container-narrow">
		<div class="section-head">
			<span class="eyebrow">Currently Writing</span>
			<h2>What's alive on the desk right now</h2>
		</div>
		<div class="status-panel">
			{#each currentlyWriting as item (item.title)}
				<div class="status-row">
					<div>
						<div class="status-title">{item.title}</div>
						<p class="status-note">{item.note}</p>
					</div>
					<span class="status-state" class:paused={item.paused}>{item.state}</span>
				</div>
			{/each}
		</div>
	</div>
</section>

<div class="section-divider">
	<span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"
		></span></span
	>
</div>

<section>
	<div class="wrap pull-quote">
		<blockquote>
			"I believe stories deserve endings. Some of mine span years; others are written short and
			focused, on purpose — so I can keep learning how to bring a narrative to a close I actually
			believe in."
		</blockquote>
		<cite>— Rae ARK, on why The Shadow I Cast Over Two Beautiful Flowers exists</cite>
	</div>
</section>

<div class="section-divider">
	<span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"
		></span></span
	>
</div>

<section class="alt-bg">
	<div class="wrap">
		<div class="section-head">
			<span class="eyebrow">Where to Read</span>
			<h2>Every chapter, free, wherever you already read</h2>
		</div>
		<div class="reads">
			<div class="read-card">
				<span class="k">Royal Road</span>
				<a class="go" href="/works">All three stories ↗</a>
			</div>
			<div class="read-card">
				<span class="k">Scribble Hub</span>
				<a class="go" href="/works">Two stories ↗</a>
			</div>
			<div class="read-card">
				<span class="k">X / Twitter</span>
				<a class="go" href="https://x.com/Rae7866" target="_blank" rel="noopener">@Rae7866 ↗</a>
			</div>
		</div>
	</div>
</section>
