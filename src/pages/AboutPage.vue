<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppLogoMark from '@/components/AppLogoMark.vue'

const { t, tm } = useI18n()

// Raw (untranslated-interpolation) list content from the about.json /
// about.json(ja) locale files — tm() returns the arrays as-is so each
// locale can list its own read links / in-progress works.
const readLinks = tm('about.readLinks') as unknown as { site: string; title: string; url: string }[]
const currentlyWriting = tm('about.currentlyWriting') as unknown as string[]
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">{{ t('about.hero.eyebrow') }}</span>
      <h1>{{ t('about.hero.title') }}</h1>
    </div>
  </section>

  <section class="page-body" v-reveal>
    <div class="wrap about-grid">
      <div>
        <p class="about-lead">{{ t('about.bio.lead') }}</p>
        <p>{{ t('about.bio.p2') }}</p>
        <p>{{ t('about.bio.p3') }}</p>
        <p>{{ t('about.bio.p4') }}</p>

        <div class="section-divider about-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

        <h3>{{ t('about.why.title') }}</h3>
        <p>{{ t('about.why.p1') }}</p>
        <p>{{ t('about.why.p2') }}</p>
      </div>

      <aside class="about-side">
        <div class="avatar-large" role="img" aria-label="Rae ARK's profile picture"></div>
        <h4>{{ t('about.side.nameHeading') }}</h4>
        <p class="about-name">{{ t('about.side.name') }}</p>
        <h4>{{ t('about.side.findHeading') }}</h4>
        <ul>
          <li v-for="link in readLinks" :key="link.url">
            {{ link.site }} — <a class="side-link" :href="link.url" target="_blank" rel="noopener">{{ link.title }} ↗</a>
          </li>
        </ul>
        <h4 class="spaced">{{ t('about.side.writingHeading') }}</h4>
        <ul>
          <li v-for="item in currentlyWriting" :key="item">{{ item }}</li>
        </ul>
        <div class="imprint-credit">
          <AppLogoMark class="imprint-mark" />
          <span>{{ t('about.side.imprint') }}</span>
        </div>
        <a class="source-credit" href="https://github.com/Rae-ARK/ARKfolio" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 2C6.48 2 2 6.58 2 12.17c0 4.47 2.87 8.26 6.84 9.6.5.1.68-.22.68-.5v-1.94c-2.78.62-3.37-1.36-3.37-1.36-.46-1.2-1.11-1.52-1.11-1.52-.9-.63.07-.62.07-.62 1 .07 1.53 1.05 1.53 1.05.9 1.55 2.36 1.1 2.93.84.09-.66.35-1.1.64-1.36-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.74 0 0 .84-.28 2.75 1.05a9.3 9.3 0 0 1 5 0c1.9-1.33 2.75-1.05 2.75-1.05.55 1.43.2 2.48.1 2.74.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9v2.82c0 .28.18.6.69.5A10.19 10.19 0 0 0 22 12.17C22 6.58 17.52 2 12 2Z"/></svg>
          <span>{{ t('about.side.sourceCredit') }}</span>
        </a>
      </aside>
    </div>
  </section>
</template>
