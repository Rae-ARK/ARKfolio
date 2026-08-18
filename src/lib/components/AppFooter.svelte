<script lang="ts">
	function hideImage(event: Event) {
		const img = event.target as HTMLImageElement | null;
		if (img) {
			img.style.display = 'none';
		}
	}
</script>

<footer class="site-footer">
	<div class="wrap">
		<p class="footer-quote">
			"I hope for people to hold the book in their hands someday, and to sit on the shelves."
		</p>

		<p class="footer-attrib">— Rae ARK</p>

		<div class="footer-imprint">
			<img src="/assets/images/horizon-ark-logo.png" alt="Horizon ARK Studio" onerror={hideImage} />
			<span>Published under Horizon ARK Studio</span>
		</div>

		<div class="footer-bottom">
			<span>© 2026 Rae ARK</span>

			<div class="footer-links">
				<a href="/works">Works</a>
				<a href="/store">Store</a>
				<a href="/journal">Journal</a>
				<a href="/about">About</a>
				<a href="/feedback">Feedback</a>
				<a href="/privacy">Privacy</a>
				<a href="/terms">Terms</a>

				<a href="https://x.com/Rae7866" target="_blank" rel="noopener"> X </a>
				<a href="https://github.com/Rae-ARK/My-Portfolio" target="_blank" rel="noopener"> GitHub </a>
			</div>
		</div>
	</div>
</footer>
