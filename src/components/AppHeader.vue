<script setup lang="ts">
import { ref } from 'vue'

// Stage 1: mobile nav open/close now lives in Vue state instead of
// DOM classList toggling — same CSS class ("open"), same behavior.
const navOpen = ref(false)
function closeNav() {
  navOpen.value = false
}
</script>

<template>
  <header class="site-header">
    <div class="wrap">
      <div class="brand-row">
        <router-link to="/about">
          <div class="avatar" style="background-image:url('/assets/images/profile.png')"></div>
        </router-link>
        <div class="brand">
          <span class="name">
            <router-link to="/">
              Rae ARK
              <span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
            </router-link>
          </span>
          <span class="sub">嵐久 怜 · WEB NOVELIST</span>
        </div>
      </div>

      <nav class="main-nav" :class="{ open: navOpen }">
        <router-link to="/" active-class="active" exact-active-class="active" @click="closeNav">Home</router-link>
        <router-link to="/works" active-class="active" @click="closeNav">Works</router-link>
        <router-link to="/store" active-class="active" @click="closeNav">Store</router-link>
        <router-link to="/journal" active-class="active" @click="closeNav">Journal</router-link>
        <router-link to="/about" active-class="active" @click="closeNav">About</router-link>
        <a class="icon-btn" href="https://x.com/Rae7866" target="_blank" rel="noopener" aria-label="Follow on X">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.9l-5.4-6.6L4.4 22H1.3l8.1-9.3L1 2h7l4.9 6z"/></svg>
        </a>
      </nav>

      <button class="nav-toggle" aria-label="Open menu" :aria-expanded="navOpen" @click="navOpen = !navOpen">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </header>
</template>
