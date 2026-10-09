<script setup lang="ts">
import { useFeedbackForm, feedbackSubjects } from '@/composables/useFeedbackForm'

const { subject, name, message, submit, copy, copied, recipient } = useFeedbackForm()
</script>

<template>
  <section class="hero page-hero">
    <div class="wrap">
      <span class="eyebrow">Get in Touch</span>
      <h1>Feedback</h1>
      <p class="lede">Thoughts on a story, the site, or anything else — this goes straight to my inbox.</p>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap">
      <div class="feedback-card">
        <div class="notice-box">
          This form opens your own email app with the message ready to send to {{ recipient }} — nothing is sent from this page, and nothing is stored. No email app? Use the copy buttons under the form. Please pick the subject that fits, so your message isn't lost in a crowded inbox.
        </div>

        <form @submit.prevent="submit">
          <div class="form-field">
            <label for="fb-subject">Subject</label>
            <select id="fb-subject" v-model="subject" required>
              <option v-for="s in feedbackSubjects" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="form-field">
            <label for="fb-name">Your name <span class="optional">(optional)</span></label>
            <input id="fb-name" v-model="name" type="text" placeholder="So I know who to thank">
          </div>
          <div class="form-field">
            <label for="fb-message">Message</label>
            <textarea id="fb-message" v-model="message" required placeholder="Whatever's on your mind..."></textarea>
          </div>
          <button type="submit" class="btn btn-primary form-submit">Send Feedback</button>
          <div class="form-fallback">
            <span>No email app?</span>
            <button type="button" class="copy-btn" @click="copy('address')">Copy address</button>
            <button type="button" class="copy-btn" @click="copy('message')">Copy message</button>
          </div>
          <p class="form-hint" role="status" aria-live="polite">
            <template v-if="copied === 'address'">Address copied.</template>
            <template v-else-if="copied === 'message'">Subject and message copied.</template>
            <template v-else-if="copied === 'failed'">Couldn't copy automatically — the address is {{ recipient }}.</template>
            <template v-else>Send it from any email service you like.</template>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>
