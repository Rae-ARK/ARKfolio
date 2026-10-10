<script setup lang="ts">
import { computed, ref } from 'vue'
import { journalEntries } from '@/data/journal'

type Filter = 'all' | 'sbm' | 'epmc' | 'stbf'

const filters: { id: Filter; label: string }[] = [
  { id: 'all', label: 'All' },
  { id: 'sbm', label: 'SBM' },
  { id: 'epmc', label: 'EPMC' },
  { id: 'stbf', label: 'STBF' },
]

const activeFilter = ref<Filter>('all')

// Filters against the entry's label rather than just its thumb, so an entry
// tagged for more than one story (e.g. "SBM · EPMC · STBF") still shows up
// under each of its stories' filters, not only the one that picked its thumb.
const filteredEntries = computed(() =>
  activeFilter.value === 'all'
    ? journalEntries
    : journalEntries.filter((entry) => entry.tags.label.includes(filters.find((f) => f.id === activeFilter.value)!.label))
)
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
      <div class="tag-filter" role="group" aria-label="Filter journal by story">
        <button
          v-for="f in filters"
          :key="f.id"
          type="button"
          class="tag-filter-btn"
          :class="{ active: activeFilter === f.id }"
          :aria-pressed="activeFilter === f.id"
          @click="activeFilter = f.id"
        >
          {{ f.label }}
        </button>
      </div>

      <p v-if="filteredEntries.length === 0" class="journal-empty">No entries tagged for that story yet.</p>

      <div class="timeline" v-else>
        <div
          class="journal-entry"
          v-reveal
          :style="{ '--i': index % 4 }"
          v-for="(entry, index) in filteredEntries"
          :key="entry.date + entry.title"
        >
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
