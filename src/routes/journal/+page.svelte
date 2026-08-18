<script lang="ts">
	import { journalEntries } from '$lib/data/journal';
	import { reveal } from '$lib/composables/useScrollReveal';
</script>

<svelte:head>
	<title>Journal — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:36px;">
	<div class="wrap">
		<span class="eyebrow">From the Writing Desk</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Journal</h1>
		<p class="lede">
			Not news. Just the process — the breaks, the doubts, the small wins — as it actually
			happens.
		</p>
	</div>
</section>

<section style="padding-top:0;">
	<div class="wrap container-narrow">
		<div class="timeline">
			{#each journalEntries as entry (entry.date + entry.title)}
				<div class="journal-entry" use:reveal>
					<div class="journal-card">
						<div class="journal-head">
							<span class="journal-date">{entry.date}</span>
						</div>
						<h3>{entry.title}</h3>
						<p>{entry.body}</p>
						<div class="journal-tag-row">
							<div class="work-thumb small {entry.tags.thumb}"></div>
							<span class="journal-tag">{entry.tags.label}</span>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
</section>
