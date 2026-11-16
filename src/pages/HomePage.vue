<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { works, currentlyWriting } from '@/data/works'
import { journalEntries } from '@/data/journal'
import WorkCard from '@/components/WorkCard.vue'
import MoodCard from '@/components/MoodCard.vue'

const { t } = useI18n()

// journalEntries is kept newest-first, so the latest post is just its head.
const latestEntry = journalEntries[0]

// "Where to Read" platform cards, derived from the same story links the rest
// of the site uses: platform -> one link per story hosted there.
const platforms = Object.entries(
  works.reduce<Record<string, { name: string; url: string }[]>>((acc, work) => {
    for (const link of work.links) (acc[link.label] ??= []).push({ name: work.shortTitle, url: link.url })
    return acc
  }, {})
)
</script>

<template>
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow stagger-in" style="--i: 0">{{ t('home.hero.eyebrow') }}</span>
      <h1 class="stagger-in" style="--i: 1">{{ t('home.hero.title') }}</h1>
      <p class="lede stagger-in" style="--i: 2">{{ t('home.hero.lede') }}</p>
      <MoodCard class="stagger-in" style="--i: 3" />
      <div class="cta-row stagger-in" style="--i: 4">
        <router-link to="/works" class="btn btn-ghost">{{ t('home.hero.ctaWorks') }}</router-link>
        <router-link to="/journal" class="btn btn-ghost">{{ t('home.hero.ctaJournal') }}</router-link>
      </div>
    </div>
  </section>

  <section id="works" v-reveal>
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">{{ t('home.works.eyebrow') }}</span>
        <h2>{{ t('home.works.title') }}</h2>
        <p>{{ t('home.works.lede') }}</p>
      </div>
      <div class="card-grid">
        <WorkCard v-for="work in works" :key="work.slug" :work="work" />
      </div>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section class="alt-bg" v-reveal>
    <div class="wrap container-narrow">
      <div class="section-head">
        <span class="eyebrow">{{ t('home.writing.eyebrow') }}</span>
        <h2>{{ t('home.writing.title') }}</h2>
      </div>
      <div class="status-panel">
        <div class="status-row" v-for="item in currentlyWriting" :key="item.title">
          <div>
            <div class="status-title">{{ item.title }}</div>
            <p class="status-note">{{ item.note }}</p>
          </div>
          <span class="status-state" :class="{ paused: item.paused }">{{ item.state }}</span>
        </div>
      </div>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section v-reveal v-if="latestEntry">
    <div class="wrap container-narrow">
      <div class="section-head">
        <span class="eyebrow">{{ t('home.journal.eyebrow') }}</span>
        <h2>{{ t('home.journal.title') }}</h2>
      </div>
      <router-link to="/journal" class="journal-teaser">
        <div class="work-thumb small" :class="latestEntry.tags.thumb" aria-hidden="true"></div>
        <div>
          <span class="journal-date">{{ latestEntry.date }}</span>
          <h3>{{ latestEntry.title }}</h3>
          <p class="journal-teaser-body">{{ latestEntry.body }}</p>
          <span class="go">{{ t('home.journal.readMore') }}</span>
        </div>
      </router-link>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section v-reveal>
    <div class="wrap pull-quote">
      <blockquote>{{ t('home.quote.text') }}</blockquote>
      <cite>{{ t('home.quote.attrib') }}</cite>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section class="alt-bg" v-reveal>
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">{{ t('home.reads.eyebrow') }}</span>
        <h2>{{ t('home.reads.title') }}</h2>
      </div>
      <div class="reads">
        <div class="read-card" v-reveal :style="{ '--i': idx }" v-for="([site, links], idx) in platforms" :key="site">
          <span class="k">{{ site }}</span>
          <a v-for="link in links" :key="link.url" class="go" :href="link.url" target="_blank" rel="noopener">{{ link.name }} ↗</a>
        </div>
        <div class="read-card" v-reveal :style="{ '--i': platforms.length }">
          <span class="k">{{ t('home.reads.paperbackLabel') }}</span>
          <router-link class="go" to="/store">{{ t('home.reads.paperbackLink') }}</router-link>
        </div>
      </div>
    </div>
  </section>
</template>
