<script setup lang="ts">
import { ref } from 'vue'
import { useTheme } from '@/composables/useTheme'

// Stage 1: mobile nav open/close now lives in Vue state instead of
// DOM classList toggling — same CSS class ("open"), same behavior.
const navOpen = ref(false)
function closeNav() {
  navOpen.value = false
}

const { theme, toggleTheme } = useTheme()
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

        <div class="nav-icons">
          <a class="icon-btn" href="https://x.com/Rae7866" target="_blank" rel="noopener" aria-label="Follow on X">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.9l-5.4-6.6L4.4 22H1.3l8.1-9.3L1 2h7l4.9 6z"/></svg>
          </a>
          <a class="icon-btn" href="https://github.com/Rae-ARK/My-Portfolio" target="_blank" rel="noopener" aria-label="View source on GitHub">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.58 2 12.17c0 4.47 2.87 8.26 6.84 9.6.5.1.68-.22.68-.5v-1.94c-2.78.62-3.37-1.36-3.37-1.36-.46-1.2-1.11-1.52-1.11-1.52-.9-.63.07-.62.07-.62 1 .07 1.53 1.05 1.53 1.05.9 1.55 2.36 1.1 2.93.84.09-.66.35-1.1.64-1.36-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.74 0 0 .84-.28 2.75 1.05a9.3 9.3 0 0 1 5 0c1.9-1.33 2.75-1.05 2.75-1.05.55 1.43.2 2.48.1 2.74.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9v2.82c0 .28.18.6.69.5A10.19 10.19 0 0 0 22 12.17C22 6.58 17.52 2 12 2Z"/></svg>
          </a>
          <button
            type="button"
            class="icon-btn theme-toggle"
            @click="toggleTheme"
            :aria-label="theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'"
          >
            <svg v-if="theme === 'dark'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="4.5"/>
              <path d="M12 2.5v2.5M12 19v2.5M4.6 4.6l1.8 1.8M17.6 17.6l1.8 1.8M2.5 12h2.5M19 12h2.5M4.6 19.4l1.8-1.8M17.6 6.4l1.8-1.8"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.6 15.3A8.5 8.5 0 1 1 8.7 3.4a7 7 0 0 0 11.9 11.9Z"/>
            </svg>
          </button>
        </div>
      </nav>

      <button class="nav-toggle" aria-label="Open menu" :aria-expanded="navOpen" @click="navOpen = !navOpen">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </header>
</template>
