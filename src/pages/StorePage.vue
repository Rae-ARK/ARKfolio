<script setup lang="ts">
import { storeBooks, notYetInPrintNote } from '@/data/store'
</script>

<template>
  <section class="hero" style="padding-bottom:36px;">
    <div class="wrap">
      <span class="eyebrow">Paperbacks</span>
      <h1 style="font-size:clamp(2rem,4vw,2.8rem);">Store</h1>
      <p class="lede">Every chapter is free to read online. These are the print editions, for anyone who'd rather have one on a shelf.</p>
    </div>
  </section>

  <section style="padding-top:36px;">
    <div class="wrap container-narrow">
      <div class="store-book" v-for="book in storeBooks" :key="book.title">
        <div class="work-thumb" :class="book.thumbClass"></div>
        <div>
          <span class="eyebrow" style="margin-bottom:0.3em;">{{ book.edition }}</span>
          <h2 style="margin-bottom:0.2em;">{{ book.title }}</h2>
          <p style="font-size:0.9rem; margin-bottom:4px;">{{ book.description }}</p>
          <p class="retailer-note">{{ book.note }}</p>
          <div class="retailer-grid">
            <a v-for="r in book.retailers" :key="r.label" class="retailer-btn" :href="r.url" target="_blank" rel="noopener">
              <span>{{ r.label }}</span><span class="arrow">↗</span>
            </a>
          </div>
          <p v-if="book.retailerNote" class="retailer-note" style="margin-top:14px;">{{ book.retailerNote }}</p>
        </div>
      </div>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section style="padding-top:0;">
    <div class="wrap container-narrow">
      <div class="store-empty">{{ notYetInPrintNote }}</div>
    </div>
  </section>
</template>
