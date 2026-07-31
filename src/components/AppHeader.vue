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
        <a class="icon-btn" href="https://x.com/Rae7866" target="_blank" rel="noopener" aria-label="Follow on X">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.9l-5.4-6.6L4.4 22H1.3l8.1-9.3L1 2h7l4.9 6z"/></svg>
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
      </nav>

      <button class="nav-toggle" aria-label="Open menu" :aria-expanded="navOpen" @click="navOpen = !navOpen">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </header>
</template>
