<script setup lang="ts">
import { journalEntries } from '@/data/journal'
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">From the Writing Desk</span>
      <h1>Journal</h1>
      <p class="lede">Not news. Just the process — the breaks, the doubts, the small wins — as it actually happens.</p>
      <p class="rss-link"><a href="/feed.xml" target="_blank" rel="noopener">Follow by RSS ↗</a></p>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap container-narrow">
      <div class="timeline">
        <div class="journal-entry" v-reveal v-for="entry in journalEntries" :key="entry.date + entry.title">
          <div class="journal-card">
            <div class="journal-head">
              <span class="journal-date">{{ entry.date }}</span>
            </div>
            <h3>{{ entry.title }}</h3>
            <p>{{ entry.body }}</p>
            <div class="journal-tag-row">
              <div class="work-thumb small" :class="entry.tags.thumb" aria-hidden="true"></div>
              <span class="journal-tag">{{ entry.tags.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
