<script lang="ts">
	import { works } from '$lib/data/works';
	import { reveal } from '$lib/composables/useScrollReveal';
</script>

<svelte:head>
	<title>Works — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:48px;">
	<div class="wrap">
		<span class="eyebrow">The Works</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Three stories, read in full elsewhere</h1>
		<p class="lede">
			Every chapter lives on Royal Road and Scribble Hub — this page is just the map. Synopses
			below, links to the real thing at the end of each.
		</p>
	</div>
</section>

{#each works as work, i (work.slug)}
	<section id={work.slug} use:reveal style={i === 0 ? 'padding-top:24px;' : 'padding-top:0;'}>
		<div class="wrap container-narrow">
			<span class="eyebrow">{work.kind} &middot; {work.status}</span>
			<div class="work-heading-row">
				<div class="work-thumb {work.coverClass}"></div>
				<div>
					<h2 style="margin-bottom:0.2em;">{work.title}</h2>
					<span
						style="font-family:var(--mono); font-size:0.7rem; color:var(--ink-faint); letter-spacing:0.05em;"
						>{work.shortTitle}</span
					>
				</div>
			</div>

			<div class="tags" style="margin-bottom:20px;">
				{#each work.tags as tag (tag)}
					<span class="badge" class:mature={tag === 'Mature Content'}>{tag}</span>
				{/each}
			</div>

			{#if work.contentNotice}
				<div
					style="background:var(--warn-tint); border:1px solid var(--warn); border-radius:6px; padding:16px 18px; margin-bottom:24px;"
				>
					<strong style="color:var(--warn); font-size:0.85rem;">Content notice — 18+</strong>
					<p style="margin:6px 0 0; font-size:0.88rem; color:var(--ink-soft);">
						{work.contentNotice}
					</p>
				</div>
			{/if}

			{#each work.synopsis as para, idx (idx)}
				<p>{para}</p>
			{/each}

			{#if work.expectRows}
				<div class="not-expect" style="margin:24px 0;">
					{#each work.expectRows as row (row.text)}
						<p class={row.yes ? 'yes' : 'no'}>{row.text}</p>
					{/each}
				</div>
			{/if}

			<div class="work-links" style="margin-top:8px;">
				{#each work.links as link (link.label)}
					<a href={link.url} target="_blank" rel="noopener">Read on {link.label} ↗</a>
				{/each}
			</div>
		</div>
	</section>
	{#if i < works.length - 1}
		<div class="section-divider">
			<span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"
				></span></span
			>
		</div>
	{/if}
{/each}
