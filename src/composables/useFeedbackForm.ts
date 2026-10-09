import { ref } from 'vue'
import { useRoute } from 'vue-router'

const RECIPIENT = 'horizonarkstudio@gmail.com'

// Subjects used by the Store page's "I'm waiting for ..." buttons, which link
// to /feedback?subject=<one of these> so the form opens pre-selected.
export const waitingSubjects = {
  epmc: 'Waiting for the EPMC paperback',
  stbf: 'Waiting for the STBF paperback',
} as const

export const feedbackSubjects = [
  'Feedback on the writing',
  'Feedback on the website',
  'Feedback on a paperback',
  'Feedback about the author',
  waitingSubjects.epmc,
  waitingSubjects.stbf,
] as const

type CopyTarget = 'address' | 'message'

// Builds a mailto: link and hands off to the user's email app.
// No server, no data collection. Copy helpers cover visitors who have no
// email app configured.
export function useFeedbackForm() {
  const route = useRoute()
  const requested = route.query.subject
  const initial = feedbackSubjects.find((s) => s === requested) ?? feedbackSubjects[0]

  const subject = ref<string>(initial)
  const name = ref('')
  const message = ref('')
  const copied = ref<CopyTarget | 'failed' | null>(null)

  function body() {
    return (name.value.trim() ? `From: ${name.value.trim()}\n\n` : '') + message.value.trim()
  }

  function submit() {
    const mailto =
      `mailto:${RECIPIENT}?subject=${encodeURIComponent(subject.value)}&body=${encodeURIComponent(body())}`
    window.location.href = mailto
  }

  async function copy(target: CopyTarget) {
    const text = target === 'address' ? RECIPIENT : `Subject: ${subject.value}\n\n${body()}`
    try {
      await navigator.clipboard.writeText(text)
      copied.value = target
    } catch {
      copied.value = 'failed'
    }
    setTimeout(() => (copied.value = null), 2500)
  }

  return { subject, name, message, submit, copy, copied, recipient: RECIPIENT }
}
