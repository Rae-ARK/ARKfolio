<script setup lang="ts">
const readLinks = [
  { site: 'Royal Road', title: 'Enigmatic Pathways Mystic Circuits', url: 'https://www.royalroad.com/fiction/114101/enigmatic-pathways-mystic-circuits/' },
  { site: 'Royal Road', title: 'Summoned by Mistake, I Decided to Learn How to Live', url: 'https://www.royalroad.com/fiction/163034/summoned-by-mistake-i-decided-to-learn-how-to' },
  { site: 'Royal Road', title: 'The Shadow I Cast Over Two Beautiful Flowers', url: 'https://www.royalroad.com/fiction/173205/the-shadow-i-cast-over-two-beautiful-flowers/' },
  { site: 'Scribble Hub', title: 'Enigmatic Pathways Mystic Circuits', url: 'https://www.scribblehub.com/series/2312083/enigmatic-pathways-mystic-circuits/' },
  { site: 'Scribble Hub', title: 'Summoned by Mistake, I Decided to Learn How to Live', url: 'https://www.scribblehub.com/series/2312017/summoned-by-mistake-i-decided-to-learn-how-to-live/' },
  { site: 'X / Twitter', title: '@Rae7866', url: 'https://x.com/Rae7866' },
]

const currentlyWriting = [
  'Enigmatic Pathways Mystic Circuits — Vol. 3, in progress',
  'Summoned by Mistake, I Decided to Learn How to Live — Arc 3, ongoing',
  'The Shadow I Cast Over Two Beautiful Flowers — Act 2, on break',
]

function hideOnError(event: Event) {
  (event.target as HTMLImageElement).style.display = 'none'
}
</script>

<template>
  <section class="hero" style="padding-bottom:36px;">
    <div class="wrap">
      <span class="eyebrow">About</span>
      <h1 style="font-size:clamp(2rem,4vw,2.8rem);">Rae ARK</h1>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="wrap about-grid">
      <div>
        <p style="font-size:1.08rem; color:var(--ink);">I write character-driven fantasy and science fantasy about people rebuilding themselves. Whether through reincarnation, another world, or just difficult circumstances, my stories explore regret, curiosity, responsibility, and the slow process of learning how to live.</p>
        <p>My stories rarely revolve around saving the world. They're interested in the people who live in it — the ones who are imperfect, lost, and trying to find their place anyway.</p>
        <p>Some of my projects start with careful planning. Others start with a single idea that refuses to leave. Either way, I usually discover the story alongside my readers rather than arriving with it fully formed — what you're reading is often close to a first draft, mistakes and all.</p>
        <p>I write as a hobby, in whatever free time I can find around everything else. That means release schedules shift, and I take real breaks after finishing a big chunk of work — it's practically tradition at this point. But I don't start things to abandon them. If a story's still going, expect it to keep going, even if slowly.</p>

        <div class="section-divider" style="margin:48px 0;"><span class="asterism"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span></div>

        <h3>Why these kinds of stories</h3>
        <p>Enigmatic Pathways Mystic Circuits started after an anime watch session turned into a real conversation about what family should mean beyond raw talent. Re:Zero and Mushoku Tensei both left a mark on how I think about second chances and slow, hard-won emotional growth — not power fantasies, but people learning to carry what happened to them.</p>
        <p>Summoned by Mistake, I Decided to Learn How to Live became the place for ideas that didn't fit anywhere else — something looser and more relaxing to write. The Shadow I Cast Over Two Beautiful Flowers exists for a different reason entirely: I wanted proof, mostly to myself, that I could take a story to a real, satisfying ending.</p>
      </div>

      <aside class="about-side">
        <div class="avatar-large" style="background-image:url('/assets/images/profile.png')"></div>
        <h4>The name</h4>
        <p style="font-size:0.9rem; color:var(--ink-soft); margin-bottom:20px;">Rae ARK — 嵐久 怜.</p>
        <h4>Find the stories</h4>
        <ul>
          <li v-for="link in readLinks" :key="link.url">
            {{ link.site }} — <a :href="link.url" target="_blank" rel="noopener" style="color:var(--accent); font-weight:600;">{{ link.title }}↗</a>
          </li>
        </ul>
        <h4 style="margin-top:22px;">Currently writing</h4>
        <ul>
          <li v-for="item in currentlyWriting" :key="item">{{ item }}</li>
        </ul>
        <div class="imprint-credit">
          <img class="imprint-mark" src="/assets/images/horizon-ark-logo.png" alt="Horizon ARK Studio" @error="hideOnError">
          <span>Horizon ARK Studio</span>
        </div>
      </aside>
    </div>
  </section>
</template>
