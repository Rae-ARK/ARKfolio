<script setup lang="ts">
import type { Work } from '@/data/works'

defineProps<{ work: Work }>()
</script>

<template>
  <article class="work-card" v-reveal>
    <div
      class="cover"
      :class="work.coverClass"
      role="img"
      :aria-label="`Cover of ${work.title} (${work.kind} · ${work.status})`"
    >
      <span class="status-ribbon" :class="{ mature: work.mature }" aria-hidden="true">{{ work.kind }} &middot; {{ work.status }}</span>
    </div>
    <div class="work-body">
      <p class="tagline">{{ work.tagline }}</p>
      <div class="tags">
        <span v-for="tag in work.tags.slice(0, 3)" :key="tag" class="badge" :class="{ mature: tag === 'Mature Content' }">{{ tag }}</span>
      </div>
      <p class="desc">{{ work.summaryCard }}</p>
      <div class="work-links">
        <router-link :to="`/works#${work.slug}`">Full synopsis →</router-link>
        <a v-for="link in work.links" :key="link.label" :href="link.url" target="_blank" rel="noopener">{{ link.label }} ↗</a>
      </div>
    </div>
  </article>
</template>
