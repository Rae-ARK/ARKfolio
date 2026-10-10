<script setup lang="ts">
import { works, currentlyWriting } from '@/data/works'
import { journalEntries } from '@/data/journal'
import WorkCard from '@/components/WorkCard.vue'
import MoodCard from '@/components/MoodCard.vue'

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
      <span class="eyebrow stagger-in" style="--i: 0">Fantasy · Science Fantasy · Slice of Life</span>
      <h1 class="stagger-in" style="--i: 1">Stories about people learning how to live again.</h1>
      <p class="lede stagger-in" style="--i: 2">Reincarnation, isekai, and the quiet, unglamorous work of rebuilding a life — told through people who are imperfect, lost, and trying anyway.</p>
      <MoodCard class="stagger-in" style="--i: 3" />
      <div class="cta-row stagger-in" style="--i: 4">
        <router-link to="/works" class="btn btn-ghost">Read the works</router-link>
        <router-link to="/journal" class="btn btn-ghost">From the writing desk</router-link>
      </div>
    </div>
  </section>

  <section id="works" v-reveal>
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Featured Works</span>
        <h2>Three stories, one question</h2>
        <p>Each begins differently — a second life, a wrong world, a body that isn't yours — but all of them ask the same thing: what does it take to actually live, not just survive?</p>
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
        <span class="eyebrow">Currently Writing</span>
        <h2>What's alive on the desk right now</h2>
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
        <span class="eyebrow">From the Writing Desk</span>
        <h2>Latest journal entry</h2>
      </div>
      <router-link to="/journal" class="journal-teaser">
        <div class="work-thumb small" :class="latestEntry.tags.thumb" aria-hidden="true"></div>
        <div>
          <span class="journal-date">{{ latestEntry.date }}</span>
          <h3>{{ latestEntry.title }}</h3>
          <p class="journal-teaser-body">{{ latestEntry.body }}</p>
          <span class="go">Read the full journal →</span>
        </div>
      </router-link>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section v-reveal>
    <div class="wrap pull-quote">
      <blockquote>"I believe stories deserve endings. Some of mine span years; others are written short and focused, on purpose — so I can keep learning how to bring a narrative to a close I actually believe in."</blockquote>
      <cite>— Rae ARK, on why The Shadow I Cast Over Two Beautiful Flowers exists</cite>
    </div>
  </section>

  <div class="section-divider"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

  <section class="alt-bg" v-reveal>
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Where to Read</span>
        <h2>Read every chapter free, or keep a copy on your shelf</h2>
      </div>
      <div class="reads">
        <div class="read-card" v-reveal :style="{ '--i': idx }" v-for="([site, links], idx) in platforms" :key="site">
          <span class="k">{{ site }}</span>
          <a v-for="link in links" :key="link.url" class="go" :href="link.url" target="_blank" rel="noopener">{{ link.name }} ↗</a>
        </div>
        <div class="read-card" v-reveal :style="{ '--i': platforms.length }">
          <span class="k">Paperback</span>
          <router-link class="go" to="/store">SBM, Vol. 1 →</router-link>
        </div>
      </div>
    </div>
  </section>
</template>
