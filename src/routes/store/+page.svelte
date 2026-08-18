<script lang="ts">
	import { storeBooks, notYetInPrintNote } from '$lib/data/store';
</script>

<svelte:head>
	<title>Store — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:36px;">
	<div class="wrap">
		<span class="eyebrow">Paperbacks</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Store</h1>
		<p class="lede">
			Every chapter is free to read online. These are the print editions, for anyone who'd
			rather have one on a shelf.
		</p>
	</div>
</section>

<section style="padding-top:36px;">
	<div class="wrap container-narrow">
		{#each storeBooks as book (book.title)}
			<div class="store-book">
				<div class="work-thumb {book.thumbClass}"></div>
				<div>
					<span class="eyebrow" style="margin-bottom:0.3em;">{book.edition}</span>
					<h2 style="margin-bottom:0.2em;">{book.title}</h2>
					<p style="font-size:0.9rem; margin-bottom:4px;">{book.description}</p>
					<p class="retailer-note">{book.note}</p>
					<div class="retailer-grid">
						{#each book.retailers as r (r.label)}
							<a class="retailer-btn" href={r.url} target="_blank" rel="noopener">
								<span>{r.label}</span><span class="arrow">↗</span>
							</a>
						{/each}
					</div>
					{#if book.retailerNote}
						<p class="retailer-note" style="margin-top:14px;">{book.retailerNote}</p>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</section>

<div class="section-divider">
	<span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"
		></span></span
	>
</div>

<section style="padding-top:0;">
	<div class="wrap container-narrow">
		<div class="store-empty">{notYetInPrintNote}</div>
	</div>
</section>
