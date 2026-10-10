<script setup lang="ts">
import { storeBooks, notYetInPrint, notYetInPrintNote, notYetInPrintCta } from '@/data/store'
import { waitingSubjects } from '@/composables/useFeedbackForm'
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow stagger-in" style="--i: 0">Paperbacks</span>
      <h1 class="stagger-in" style="--i: 1">Store</h1>
      <p class="lede stagger-in" style="--i: 2">Every chapter is free to read online. These are the print editions, for anyone who'd rather have one on a shelf.</p>
    </div>
  </section>

  <section class="page-body tight">
    <div class="wrap container-narrow">
      <div
        class="store-book"
        :class="{ 'is-coming-soon': book.status === 'coming-soon' }"
        v-reveal
        v-for="book in storeBooks"
        :key="book.edition"
      >
        <div class="work-thumb" :class="book.thumbClass"></div>
        <div>
          <span class="eyebrow">{{ book.edition }}</span>
          <h2>{{ book.title }}</h2>
          <p class="book-desc">{{ book.description }}</p>
          <p v-if="book.note" class="retailer-note">{{ book.note }}</p>

          <template v-if="book.status === 'coming-soon'">
            <span class="coming-soon-badge">{{ book.availability }}</span>
          </template>
          <template v-else>
            <template v-for="main in [book.retailers.find((r) => r.primary)]" :key="'main'">
              <a v-if="main" class="retailer-btn retailer-primary" :href="main.url" target="_blank" rel="noopener">
                <span>Buy on {{ main.label }}</span><span class="arrow">↗</span>
              </a>
            </template>
            <template v-if="book.retailers.some((r) => !r.primary)">
              <p class="retailer-group-label">Other retailers</p>
              <div class="retailer-grid tight">
                <a v-for="r in book.retailers.filter((x) => !x.primary)" :key="r.label" class="retailer-btn" :href="r.url" target="_blank" rel="noopener">
                  <span>{{ r.label }}</span><span class="arrow">↗</span>
                </a>
              </div>
            </template>
            <div class="retailer-notes">
              <p v-for="r in book.retailers.filter(x => x.note)" :key="r.label" class="retailer-note">
                <strong>{{ r.label }}:</strong> {{ r.note }}
              </p>
            </div>
          </template>
        </div>
      </div>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section class="page-body flush">
    <div class="wrap container-narrow">
      <div class="print-card" v-reveal>
        <span class="eyebrow">Still to come</span>
        <p class="print-card-lead">{{ notYetInPrintNote }}</p>
        <p class="print-card-cta">{{ notYetInPrintCta }}</p>
        <div class="upcoming-shelf">
          <div class="store-book is-coming-soon" v-for="item in notYetInPrint" :key="item.slug">
            <div class="work-thumb" :class="item.slug"></div>
            <div>
              <span class="eyebrow">{{ item.shortTitle }}</span>
              <h2>{{ item.title }}</h2>
              <span class="coming-soon-badge">Not yet in print</span>
              <div class="upcoming-cta">
                <router-link
                  class="btn btn-primary btn-small"
                  :to="{ path: '/feedback', query: { subject: waitingSubjects[item.slug] } }"
                >
                  I'm waiting for {{ item.shortTitle }} →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
