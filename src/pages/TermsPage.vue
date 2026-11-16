<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const LAST_UPDATED = 'July 2026'
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">{{ t('terms.hero.eyebrow') }}</span>
      <h1>{{ t('terms.hero.title') }}</h1>
      <p class="lede">{{ t('terms.hero.lastUpdated', { date: LAST_UPDATED }) }}</p>
    </div>
  </section>

  <section class="page-body" v-reveal>
    <div class="wrap container-narrow">
      <div class="legal-card">
        <p>{{ t('terms.intro') }}</p>

        <h3>{{ t('terms.content.heading') }}</h3>
        <p>{{ t('terms.content.body') }}</p>

        <h3>{{ t('terms.thirdParty.heading') }}</h3>
        <p>{{ t('terms.thirdParty.body') }}</p>

        <h3>{{ t('terms.warranty.heading') }}</h3>
        <p>{{ t('terms.warranty.body') }}</p>

        <h3>{{ t('terms.ageNotices.heading') }}</h3>
        <p>{{ t('terms.ageNotices.body') }}</p>

        <h3>{{ t('terms.changes.heading') }}</h3>
        <p>{{ t('terms.changes.body') }}</p>

        <h3>{{ t('terms.contact.heading') }}</h3>
        <i18n-t keypath="terms.contact.body" tag="p">
          <template #feedbackLink><router-link to="/feedback">{{ t('footer.feedback') }}</router-link></template>
        </i18n-t>
      </div>
    </div>
  </section>
</template>
