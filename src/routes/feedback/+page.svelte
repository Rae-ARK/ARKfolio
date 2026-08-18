<script lang="ts">
	import { useFeedbackForm, feedbackSubjects } from '$lib/composables/useFeedbackForm.svelte';

	const form = useFeedbackForm();
</script>

<svelte:head>
	<title>Feedback — Rae ARK</title>
</svelte:head>

<section class="hero" style="padding-bottom:36px;">
	<div class="wrap">
		<span class="eyebrow">Get in Touch</span>
		<h1 style="font-size:clamp(2rem,4vw,2.8rem);">Feedback</h1>
		<p class="lede">
			Thoughts on a story, the site, or anything else — this goes straight to my inbox.
		</p>
	</div>
</section>

<section style="padding-top:0;">
	<div class="wrap">
		<div class="feedback-card">
			<div class="notice-box">
				Please pick one of the subjects below before sending. Messages sent through this form
				use your own email app, and ones without a matching subject are easy to miss in a
				crowded inbox.
			</div>

			<form
				onsubmit={(e) => {
					e.preventDefault();
					form.submit();
				}}
			>
				<div class="form-field">
					<label for="fb-subject">Subject</label>
					<select id="fb-subject" bind:value={form.subject} required>
						{#each feedbackSubjects as s (s)}
							<option value={s}>{s}</option>
						{/each}
					</select>
				</div>
				<div class="form-field">
					<label for="fb-name">Your name <span style="text-transform:none;">(optional)</span></label
					>
					<input
						id="fb-name"
						bind:value={form.name}
						type="text"
						placeholder="So I know who to thank"
					/>
				</div>
				<div class="form-field">
					<label for="fb-message">Message</label>
					<textarea
						id="fb-message"
						bind:value={form.message}
						required
						placeholder="Whatever's on your mind..."
					></textarea>
				</div>
				<button type="submit" class="btn btn-primary form-submit">Send Feedback</button>
				<p class="form-hint">
					Opens in your email app, addressed to {form.recipient} — nothing is sent from this page
					directly.
				</p>
			</form>
		</div>
	</div>
</section>
