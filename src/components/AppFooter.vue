<template>
  <footer class="site-footer">
    <div class="wrap">
      <p class="footer-quote">
        "I hope for people to hold the book in their hands someday, and to sit on the shelves."
      </p>

      <p class="footer-attrib">— Rae ARK</p>

      <div class="footer-imprint">
        <img
          src="/assets/images/horizon-ark-logo.png"
          alt="Horizon ARK Studio"
          @error="hideImage"
        />
        <span>Published under Horizon ARK Studio</span>
      </div>

      <div class="footer-bottom">
        <span>© 2026 Rae ARK</span>

        <nav class="footer-legal" aria-label="Footer">
          <router-link to="/feedback">Feedback</router-link>
          <router-link to="/privacy">Privacy</router-link>
          <router-link to="/terms">Terms</router-link>
        </nav>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
function hideImage(event: Event) {
  const img = event.target as HTMLImageElement | null
  if (img) {
    img.style.display = 'none'
  }
}
</script>