<script setup lang="ts">
import { storeBooks, notYetInPrint, notYetInPrintNote, notYetInPrintCta } from '@/data/store'
import { waitingSubjects } from '@/composables/useFeedbackForm'
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">Paperbacks</span>
      <h1>Store</h1>
      <p class="lede">Every chapter is free to read online. These are the print editions, for anyone who'd rather have one on a shelf.</p>
    </div>
  </section>

  <section class="page-body tight">
    <div class="wrap container-narrow">
      <div class="store-book" v-reveal v-for="book in storeBooks" :key="book.title">
        <div class="work-thumb" :class="book.thumbClass"></div>
        <div>
          <span class="eyebrow">{{ book.edition }}</span>
          <h2>{{ book.title }}</h2>
          <p class="book-desc">{{ book.description }}</p>
          <p class="retailer-note">{{ book.note }}</p>
          <div class="retailer-grid">
            <a v-for="r in book.retailers" :key="r.label" class="retailer-btn" :href="r.url" target="_blank" rel="noopener">
              <span>{{ r.label }}</span><span class="arrow">↗</span>
            </a>
          </div>
          <div class="retailer-notes">
            <p v-for="r in book.retailers.filter(x => x.note)" :key="r.label" class="retailer-note">
              <strong>{{ r.label }}:</strong> {{ r.note }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section class="page-body flush">
    <div class="wrap container-narrow">
      <div class="store-empty" v-reveal>
        <p>{{ notYetInPrintNote }}</p>
        <p>{{ notYetInPrintCta }}</p>
        <div class="waiting-links">
          <router-link
            v-for="item in notYetInPrint"
            :key="item.slug"
            class="btn btn-ghost"
            :to="{ path: '/feedback', query: { subject: waitingSubjects[item.slug] } }"
          >
            I'm waiting for {{ item.shortTitle }} →
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>
