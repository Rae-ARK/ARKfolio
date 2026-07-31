import { ref } from 'vue'

const RECIPIENT = 'horizonarkstudio@gmail.com'

export const feedbackSubjects = [
  'Feedback on the writing',
  'Feedback on the website',
  'Feedback on a paperback',
  'Feedback about the author',
] as const

// Ported 1:1 from the original script.js feedback-form handler:
// builds a mailto: link and hands off to the user's email app.
// No server, no data collection — same as before.
export function useFeedbackForm() {
  const subject = ref<string>(feedbackSubjects[0])
  const name = ref('')
  const message = ref('')

  function submit() {
    const body = (name.value.trim() ? `From: ${name.value.trim()}\n\n` : '') + message.value.trim()
    const mailto =
      `mailto:${RECIPIENT}?subject=${encodeURIComponent(subject.value)}&body=${encodeURIComponent(body)}`
    window.location.href = mailto
  }

  return { subject, name, message, submit, recipient: RECIPIENT }
}
