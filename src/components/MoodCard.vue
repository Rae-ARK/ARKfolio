<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { moods, works } from '@/data/works'

// Hero "mood card" (proposal 0009). Every slide is rendered and stacked in
// one grid cell, so the card is always as tall as its tallest slide (no
// layout jump) and changing slides is a plain cross-fade in CSS. Slides that
// aren't active are visibility:hidden, so they can't be tabbed to or read.

const AUTO_MS = 7000

const slides = computed(() =>
  moods
    .map((mood) => ({ mood, work: works.find((w) => w.slug === mood.workSlug) }))
    .filter((s): s is { mood: (typeof moods)[number]; work: (typeof works)[number] } => !!s.work)
)

const index = ref(0)
const userPaused = ref(false)
const hovering = ref(false)
const focusing = ref(false)
const reducedMotion = ref(false)

let timer: ReturnType<typeof setInterval> | null = null

function go(to: number) {
  const n = slides.value.length
  index.value = ((to % n) + n) % n
}

function step(by: number) {
  // Any manual use means the visitor is in control: stop auto-advancing.
  userPaused.value = true
  go(index.value + by)
}

const canAutoplay = computed(() => !reducedMotion.value && slides.value.length > 1)

function tick() {
  if (document.hidden || userPaused.value || hovering.value || focusing.value) return
  go(index.value + 1)
}

onMounted(() => {
  reducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (canAutoplay.value) timer = setInterval(tick, AUTO_MS)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <section
    class="mood-card"
    aria-roledescription="carousel"
    aria-label="Where to start reading"
    @mouseenter="hovering = true"
    @mouseleave="hovering = false"
    @focusin="focusing = true"
    @focusout="focusing = false"
  >
    <div class="mood-stage">
      <article
        v-for="(slide, i) in slides"
        :key="slide.work.slug"
        class="mood-slide"
        :class="{ 'is-active': i === index }"
        role="group"
        aria-roledescription="slide"
        :aria-label="`${i + 1} of ${slides.length}`"
      >
        <div class="work-thumb mood-thumb" :class="slide.work.coverClass" aria-hidden="true"></div>
        <div class="mood-copy">
          <p class="mood-prompt">{{ slide.mood.prompt }}</p>
          <h2 class="mood-title">{{ slide.work.title }}</h2>
          <p class="mood-desc">{{ slide.work.summaryCard }}</p>
          <div class="mood-actions">
            <a
              v-if="slide.work.links[0]"
              class="btn btn-primary btn-small"
              :href="slide.work.links[0].url"
              target="_blank"
              rel="noopener"
            >Read on {{ slide.work.links[0].label }} ↗</a>
            <router-link class="mood-more" :to="`/works#${slide.work.slug}`">Full synopsis →</router-link>
          </div>
        </div>
      </article>
    </div>

    <div v-if="slides.length > 1" class="mood-controls">
      <button type="button" class="mood-arrow" aria-label="Previous story" @click="step(-1)">‹</button>
      <div class="mood-dots">
        <button
          v-for="(slide, i) in slides"
          :key="slide.work.slug"
          type="button"
          class="mood-dot"
          :class="{ 'is-active': i === index }"
          :aria-label="`Show ${slide.work.shortTitle}`"
          :aria-current="i === index ? 'true' : undefined"
          @click="step(i - index)"
        ></button>
      </div>
      <button type="button" class="mood-arrow" aria-label="Next story" @click="step(1)">›</button>
      <button
        v-if="canAutoplay"
        type="button"
        class="mood-pause"
        :aria-pressed="userPaused"
        @click="userPaused = !userPaused"
      >{{ userPaused ? 'Play' : 'Pause' }}</button>
    </div>
  </section>
</template>
