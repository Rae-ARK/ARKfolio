<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { works } from '@/data/works'

const { t } = useI18n()

// Official reading platforms, derived from the same links used below so the
// notice can't drift out of date: platform -> the stories hosted there.
const officialSites = Object.entries(
  works.reduce<Record<string, string[]>>((acc, work) => {
    for (const link of work.links) (acc[link.label] ??= []).push(work.shortTitle)
    return acc
  }, {})
)
</script>

<template>
  <section class="hero page-hero roomy">
    <div class="wrap">
      <span class="eyebrow">{{ t('works.hero.eyebrow') }}</span>
      <h1>{{ t('works.hero.title') }}</h1>
      <p class="lede">{{ t('works.hero.lede') }}</p>
    </div>
  </section>

  <section class="page-body tight">
    <div class="wrap container-narrow">
      <div class="notice-box official-sources">
        <strong>{{ t('works.notice.title') }}</strong>
        <p>
          {{ t('works.notice.intro') }}
          <template v-for="([site, titles], idx) in officialSites" :key="site">
            <template v-if="idx > 0">, </template>{{ site }} ({{ titles.join(', ') }})
          </template>, {{ t('works.notice.and') }} <router-link to="/store">{{ t('nav.store') }}</router-link>.
          {{ t('works.notice.unauthorized') }}
          <router-link to="/journal">{{ t('nav.journal') }}</router-link> {{ t('works.notice.whyMatters') }}
        </p>
      </div>
    </div>
  </section>

  <template v-for="(work, i) in works" :key="work.slug">
    <section :id="work.slug" v-reveal :class="['work-section', 'page-body', i === 0 ? 'snug' : 'flush']">
      <div class="wrap container-narrow">
        <span class="eyebrow">{{ work.kind }} &middot; {{ work.status }}</span>
        <div class="work-heading-row">
          <div class="work-thumb" :class="work.coverClass" role="img" :aria-label="`Cover of ${work.title}`"></div>
          <div>
            <h2 class="work-title">{{ work.title }}</h2>
            <span class="work-short">{{ work.shortTitle }}</span>
          </div>
        </div>

        <div class="tags">
          <span v-for="tag in work.tags" :key="tag" class="badge" :class="{ mature: tag === 'Mature Content' }">{{ tag }}</span>
        </div>

        <div v-if="work.contentNotice" class="content-notice">
          <strong>{{ t('works.contentNoticeTitle') }}</strong>
          <p>{{ work.contentNotice }}</p>
        </div>

        <p v-for="(para, idx) in work.synopsis" :key="idx">{{ para }}</p>

        <div v-if="work.expectRows" class="not-expect">
          <p v-for="row in work.expectRows" :key="row.text" :class="row.yes ? 'yes' : 'no'">{{ row.text }}</p>
        </div>

        <div class="work-links">
          <a v-for="link in work.links" :key="link.label" :href="link.url" target="_blank" rel="noopener">{{ t('works.readOn', { platform: link.label }) }}</a>
        </div>
      </div>
    </section>
    <div v-if="i < works.length - 1" class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>
  </template>
</template>
