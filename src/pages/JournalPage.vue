<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { journalEntries } from '@/data/journal'

const { t } = useI18n()

type Filter = 'all' | 'sbm' | 'epmc' | 'stbf'

// Story abbreviations (SBM / EPMC / STBF) are the works' own short titles and
// stay the same across locales; only the "All" filter has a translation.
// Kept as a computed (not a plain const) so the label stays correct if the
// locale changes via client-side navigation rather than a fresh page load.
const filters = computed<{ id: Filter; label: string }[]>(() => [
  { id: 'all', label: t('journal.filters.all') },
  { id: 'sbm', label: 'SBM' },
  { id: 'epmc', label: 'EPMC' },
  { id: 'stbf', label: 'STBF' },
])

const activeFilter = ref<Filter>('all')

// Filters against the entry's label rather than just its thumb, so an entry
// tagged for more than one story (e.g. "SBM · EPMC · STBF") still shows up
// under each of its stories' filters, not only the one that picked its thumb.
const filteredEntries = computed(() =>
  activeFilter.value === 'all'
    ? journalEntries
    : journalEntries.filter((entry) => entry.tags.label.includes(filters.value.find((f) => f.id === activeFilter.value)!.label))
)
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">{{ t('journal.hero.eyebrow') }}</span>
      <h1>{{ t('journal.hero.title') }}</h1>
      <p class="lede">{{ t('journal.hero.lede') }}</p>
      <p class="rss-link"><a href="/feed.xml" target="_blank" rel="noopener">{{ t('journal.hero.rss') }}</a></p>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap container-narrow">
      <div class="tag-filter" role="group" :aria-label="t('journal.filterAriaLabel')">
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

      <p v-if="filteredEntries.length === 0" class="journal-empty">{{ t('journal.empty') }}</p>

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
