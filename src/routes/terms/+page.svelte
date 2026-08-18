<script lang="ts">
	import { reveal } from '$lib/composables/useScrollReveal';

	const LAST_UPDATED = 'July 2026';
</script>

<svelte:head>
	<title>Terms &amp; Conditions — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:36px;">
	<div class="wrap">
		<span class="eyebrow">Legal</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Terms &amp; Conditions</h1>
		<p class="lede">Last updated: {LAST_UPDATED}</p>
	</div>
</section>

<section style="padding-top:0;" use:reveal>
	<div class="wrap container-narrow">
		<div class="legal-card">
			<p>
				By using this site or the Rae ARK Android app, you agree to the terms below. If you
				don't agree, the simplest option is not to use it — nothing here is gated behind
				acceptance of anything more involved than reading a webpage or opening an app.
			</p>

			<h3>The content</h3>
			<p>
				All original writing, artwork, and branding on this site and app — including the web
				novels, journal entries, and cover art — belongs to Rae ARK (Horizon ARK Studio) unless
				stated otherwise. You're welcome to read, link to, and share pages, but reposting,
				republishing, or using the writing or art commercially without permission isn't allowed.
			</p>

			<h3>Third-party platforms</h3>
			<p>
				Royal Road, Scribble Hub, X/Twitter, and any retailers linked from the Store page are
				independent platforms with their own terms of service. Reading, purchasing, or creating
				an account on those platforms is governed by their rules, not these ones.
			</p>

			<h3>No warranty</h3>
			<p>
				This site and app are provided "as is." Every reasonable effort is made to keep content
				accurate and the app functioning, but no guarantee is made that it will be uninterrupted,
				error-free, or available at all times.
			</p>

			<h3>Age and content notices</h3>
			<p>
				Some works are tagged "Mature Content" on the Works page and carry appropriate content
				warnings there. Please check those tags before reading if that matters to you.
			</p>

			<h3>Changes</h3>
			<p>
				These terms may be updated occasionally; continued use after a change means you accept
				the updated terms. Material changes will update the "last updated" date above.
			</p>

			<h3>Contact</h3>
			<p>
				Questions about these terms can be sent via the <a href="/feedback">Feedback</a> page.
			</p>
		</div>
	</div>
</section>
