<script setup lang="ts">
function hideOnError(event: Event) {
  (event.target as HTMLImageElement).style.display = 'none'
}
</script>

<template>
  <footer class="site-footer">
    <div class="wrap">
      <p class="footer-quote">"I hope for people to hold the book in their hands someday, and to sit on the shelves."</p>
      <p class="footer-attrib">— Rae ARK</p>
      <div class="footer-imprint">
        <img src="/assets/images/horizon-ark-logo.png" alt="Horizon ARK Studio" @error="hideOnError">
        <span>Published under Horizon ARK Studio</span>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Rae ARK</span>
        <div class="footer-links">
          <router-link to="/works">Works</router-link>
          <router-link to="/store">Store</router-link>
          <router-link to="/journal">Journal</router-link>
          <router-link to="/about">About</router-link>
          <router-link to="/feedback">Feedback</router-link>
          <a href="https://x.com/Rae7866" target="_blank" rel="noopener">X</a>
        </div>
      </div>
    </div>
  </footer>
</template>
