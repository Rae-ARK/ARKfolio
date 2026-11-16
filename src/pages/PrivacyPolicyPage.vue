<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const LAST_UPDATED = 'October 2026'
const CONTACT_EMAIL = 'contact@rae-ark.example'
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">{{ t('privacy.hero.eyebrow') }}</span>
      <h1>{{ t('privacy.hero.title') }}</h1>
      <p class="lede">{{ t('privacy.hero.lastUpdated', { date: LAST_UPDATED }) }}</p>
    </div>
  </section>

  <section class="page-body" v-reveal>
    <div class="wrap container-narrow">
      <div class="legal-card">
        <p>{{ t('privacy.intro') }}</p>

        <h3>{{ t('privacy.collected.heading') }}</h3>
        <p>{{ t('privacy.collected.body') }}</p>

        <h3>{{ t('privacy.permissions.heading') }}</h3>
        <p>{{ t('privacy.permissions.body') }}</p>

        <h3>{{ t('privacy.localStorage.heading') }}</h3>
        <p>{{ t('privacy.localStorage.body') }}</p>

        <h3>{{ t('privacy.thirdParty.heading') }}</h3>
        <p>{{ t('privacy.thirdParty.body') }}</p>

        <h3>{{ t('privacy.children.heading') }}</h3>
        <p>{{ t('privacy.children.body') }}</p>

        <h3>{{ t('privacy.changes.heading') }}</h3>
        <p>{{ t('privacy.changes.body') }}</p>

        <h3>{{ t('privacy.contact.heading') }}</h3>
        <i18n-t keypath="privacy.contact.body" tag="p">
          <template #feedbackLink><router-link to="/feedback">{{ t('footer.feedback') }}</router-link></template>
          <template #email>{{ CONTACT_EMAIL }}</template>
        </i18n-t>
      </div>
    </div>
  </section>
</template>
