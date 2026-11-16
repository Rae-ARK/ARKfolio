<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppLogoMark from './AppLogoMark.vue'

const { t } = useI18n()
</script>

<template>
  <footer class="site-footer">
    <div class="wrap">
      <p class="footer-quote">
        {{ t('footer.quote') }}
      </p>

      <p class="footer-attrib">{{ t('footer.attrib') }}</p>

      <div class="footer-imprint">
        <AppLogoMark class="imprint-logo" />
        <span>{{ t('footer.imprint') }}</span>
      </div>

      <div class="footer-bottom">
        <span>{{ t('footer.copyright') }}</span>

        <nav class="footer-legal" aria-label="Footer">
          <router-link to="/feedback">{{ t('footer.feedback') }}</router-link>
          <router-link to="/privacy">{{ t('footer.privacy') }}</router-link>
          <router-link to="/terms">{{ t('footer.terms') }}</router-link>
        </nav>
      </div>
    </div>
  </footer>
</template>
