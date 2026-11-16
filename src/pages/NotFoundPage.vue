<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">{{ t('notFound.eyebrow') }}</span>
      <h1>{{ t('notFound.title') }}</h1>
      <p class="lede">{{ t('notFound.lede') }}</p>
      <div class="cta-row">
        <router-link to="/" class="btn btn-primary">{{ t('notFound.backHome') }}</router-link>
        <router-link to="/works" class="btn btn-ghost">{{ t('notFound.browseWorks') }}</router-link>
      </div>
    </div>
  </section>
</template>
