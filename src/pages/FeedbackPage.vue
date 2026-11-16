<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useFeedbackForm, feedbackSubjectKeys } from '@/composables/useFeedbackForm'

const { t } = useI18n()
const { subject, name, message, submit, copy, copied, recipient } = useFeedbackForm()
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">{{ t('feedback.eyebrow') }}</span>
      <h1>{{ t('feedback.title') }}</h1>
      <p class="lede">{{ t('feedback.lede') }}</p>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap">
      <div class="feedback-card">
        <div class="notice-box">
          {{ t('feedback.notice', { recipient }) }}
        </div>

        <form @submit.prevent="submit">
          <div class="form-field">
            <label for="fb-subject">{{ t('feedback.subjectLabel') }}</label>
            <select id="fb-subject" v-model="subject" required>
              <option v-for="key in feedbackSubjectKeys" :key="key" :value="key">{{ t(`feedback.subjects.${key}`) }}</option>
            </select>
          </div>
          <div class="form-field">
            <label for="fb-name">{{ t('feedback.nameLabel') }} <span class="optional">{{ t('feedback.optional') }}</span></label>
            <input id="fb-name" v-model="name" type="text" :placeholder="t('feedback.namePlaceholder')">
          </div>
          <div class="form-field">
            <label for="fb-message">{{ t('feedback.messageLabel') }}</label>
            <textarea id="fb-message" v-model="message" required :placeholder="t('feedback.messagePlaceholder')"></textarea>
          </div>
          <button type="submit" class="btn btn-primary form-submit">{{ t('feedback.submit') }}</button>
          <div class="form-fallback">
            <span>{{ t('feedback.noEmailApp') }}</span>
            <button type="button" class="copy-btn" @click="copy('address')">{{ t('feedback.copyAddress') }}</button>
            <button type="button" class="copy-btn" @click="copy('message')">{{ t('feedback.copyMessage') }}</button>
          </div>
          <p class="form-hint" role="status" aria-live="polite">
            <template v-if="copied === 'address'">{{ t('feedback.copiedAddress') }}</template>
            <template v-else-if="copied === 'message'">{{ t('feedback.copiedMessage') }}</template>
            <template v-else-if="copied === 'failed'">{{ t('feedback.copyFailed', { recipient }) }}</template>
            <template v-else>{{ t('feedback.sendHint') }}</template>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>
