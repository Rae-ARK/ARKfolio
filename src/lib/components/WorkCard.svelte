<script lang="ts">
	import type { Work } from '$lib/data/works';
	import { reveal } from '$lib/composables/useScrollReveal';

	let { work }: { work: Work } = $props();
</script>

<article class="work-card" use:reveal>
	<div class="cover {work.coverClass}">
		<span class="status-ribbon" class:mature={work.mature}>{work.kind} &middot; {work.status}</span>
	</div>
	<div class="work-body">
		<p class="tagline">{work.tagline}</p>
		<div class="tags">
			{#each work.tags.slice(0, 3) as tag (tag)}
				<span class="badge" class:mature={tag === 'Mature Content'}>{tag}</span>
			{/each}
		</div>
		<p class="desc">{work.summaryCard}</p>
		<div class="work-links">
			<a href="/works#{work.slug}">Full synopsis →</a>
			{#each work.links as link (link.label)}
				<a href={link.url} target="_blank" rel="noopener">{link.label} ↗</a>
			{/each}
		</div>
	</div>
</article>
