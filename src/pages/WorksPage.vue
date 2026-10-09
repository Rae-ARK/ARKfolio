<script setup lang="ts">
import { works } from '@/data/works'
</script>

<template>
  <section class="hero page-hero roomy">
    <div class="wrap">
      <span class="eyebrow">The Works</span>
      <h1>Three stories, read in full elsewhere</h1>
      <p class="lede">Every chapter lives on Royal Road and Scribble Hub — this page is just the map. Synopses below, links to the real thing at the end of each.</p>
    </div>
  </section>

  <template v-for="(work, i) in works" :key="work.slug">
    <section :id="work.slug" v-reveal :class="['work-section', 'page-body', i === 0 ? 'snug' : 'flush']">
      <div class="wrap container-narrow">
        <span class="eyebrow">{{ work.kind }} &middot; {{ work.status }}</span>
        <div class="work-heading-row">
          <div class="work-thumb" :class="work.coverClass"></div>
          <div>
            <h2 class="work-title">{{ work.title }}</h2>
            <span class="work-short">{{ work.shortTitle }}</span>
          </div>
        </div>

        <div class="tags">
          <span v-for="tag in work.tags" :key="tag" class="badge" :class="{ mature: tag === 'Mature Content' }">{{ tag }}</span>
        </div>

        <div v-if="work.contentNotice" class="content-notice">
          <strong>Content notice — 18+</strong>
          <p>{{ work.contentNotice }}</p>
        </div>

        <p v-for="(para, idx) in work.synopsis" :key="idx">{{ para }}</p>

        <div v-if="work.expectRows" class="not-expect">
          <p v-for="row in work.expectRows" :key="row.text" :class="row.yes ? 'yes' : 'no'">{{ row.text }}</p>
        </div>

        <div class="work-links">
          <a v-for="link in work.links" :key="link.label" :href="link.url" target="_blank" rel="noopener">Read on {{ link.label }} ↗</a>
        </div>
      </div>
    </section>
    <div v-if="i < works.length - 1" class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>
  </template>
</template>
