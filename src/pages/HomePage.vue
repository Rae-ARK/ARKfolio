<script setup lang="ts">
import { works, currentlyWriting } from '@/data/works'
import WorkCard from '@/components/WorkCard.vue'
</script>

<template>
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow">Fantasy · Science Fantasy · Slice of Life</span>
      <h1>Stories about people learning how to live again.</h1>
      <p class="lede">Reincarnation, isekai, and the quiet, unglamorous work of rebuilding a life — told through people who are imperfect, lost, and trying anyway.</p>
      <div class="cta-row">
        <router-link to="/works" class="btn btn-primary">Read the works</router-link>
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
        <h2>Every chapter, free, wherever you already read</h2>
      </div>
      <div class="reads">
        <div class="read-card">
          <span class="k">Royal Road</span>
          <router-link class="go" to="/works">All three stories ↗</router-link>
        </div>
        <div class="read-card">
          <span class="k">Scribble Hub</span>
          <router-link class="go" to="/works">Two stories ↗</router-link>
        </div>
        <div class="read-card">
          <span class="k">X / Twitter</span>
          <a class="go" href="https://x.com/Rae7866" target="_blank" rel="noopener">@Rae7866 ↗</a>
        </div>
      </div>
    </div>
  </section>
</template>
