<script lang="ts">
	const LAST_UPDATED = 'July 2026';
	const CONTACT_EMAIL = 'contact@rae-ark.example';
</script>

<svelte:head>
	<title>Privacy Policy — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:36px;">
	<div class="wrap">
		<span class="eyebrow">Legal</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Privacy Policy</h1>
		<p class="lede">Last updated: {LAST_UPDATED}</p>
	</div>
</section>

<section style="padding-top:0;">
	<div class="wrap container-narrow">
		<div class="legal-card">
			<p>
				This site and app ("Rae ARK") is an author portfolio. It exists to showcase web novels,
				journal updates, and ways to read or support the work. This policy explains what little
				data is involved and why.
			</p>

			<h3>What's collected</h3>
			<p>
				The site itself does not run analytics, trackers, or advertising, and it does not create
				accounts or store personal data on a server. The only place personal information can
				enter the picture is the Feedback page, which opens your own email app with a pre-filled
				address and subject — anything you write there is sent directly from your device using
				your own email provider, under that provider's privacy policy, not ours.
			</p>

			<h3>App permissions (Android)</h3>
			<p>
				The Android app requests internet access only. This is used to open external links —
				Royal Road, Scribble Hub, X/Twitter, and similar — in your browser, and to check for
				updated content on future visits. The app does not request access to your contacts,
				location, camera, microphone, storage, or any other device permission.
			</p>

			<h3>Local storage</h3>
			<p>
				A single preference — whether you've chosen light or dark mode — is saved on your own
				device so it's remembered next time. It never leaves your device and isn't linked to you
				personally.
			</p>

			<h3>Third-party links</h3>
			<p>
				Buttons and links to Royal Road, Scribble Hub, X/Twitter, and retail storefronts take you
				to third-party sites with their own privacy policies. Once you leave this site or app,
				this policy no longer applies.
			</p>

			<h3>Children's privacy</h3>
			<p>
				This site is not directed at children under 13, and no data is knowingly collected from
				them.
			</p>

			<h3>Changes to this policy</h3>
			<p>
				If this policy changes, the update will be posted here with a new "last updated" date.
			</p>

			<h3>Contact</h3>
			<p>
				Questions about this policy can be sent via the <a href="/feedback">Feedback</a> page, or
				to {CONTACT_EMAIL}.
			</p>
		</div>
	</div>
</section>
