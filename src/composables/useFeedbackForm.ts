import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const RECIPIENT = 'horizonarkstudio@gmail.com'

// Subjects used by the Store page's "I'm waiting for ..." buttons, which link
// to /feedback?subject=<one of these keys> so the form opens pre-selected.
// Keys map to src/locales/*.json's feedback.subjects.* — the subject text
// itself is translated, so it travels as a key rather than display text.
export const waitingSubjects = {
  epmc: 'waitingEpmc',
  stbf: 'waitingStbf',
} as const

export const feedbackSubjectKeys = [
  'writing',
  'website',
  'paperback',
  'author',
  'waitingEpmc',
  'waitingStbf',
] as const

export type FeedbackSubjectKey = (typeof feedbackSubjectKeys)[number]

type CopyTarget = 'address' | 'message'

// Builds a mailto: link and hands off to the user's email app.
// No server, no data collection. Copy helpers cover visitors who have no
// email app configured.
export function useFeedbackForm() {
  const route = useRoute()
  const { t } = useI18n()

  const requested = route.query.subject
  const initial =
    feedbackSubjectKeys.find((s) => s === requested) ?? feedbackSubjectKeys[0]

  const subject = ref<FeedbackSubjectKey>(initial)
  const name = ref('')
  const message = ref('')
  const copied = ref<CopyTarget | 'failed' | null>(null)

  function subjectText() {
    return t(`feedback.subjects.${subject.value}`)
  }

  function body() {
    return (name.value.trim() ? `From: ${name.value.trim()}\n\n` : '') + message.value.trim()
  }

  function submit() {
    const mailto =
      `mailto:${RECIPIENT}?subject=${encodeURIComponent(subjectText())}&body=${encodeURIComponent(body())}`
    window.location.href = mailto
  }

  async function copy(target: CopyTarget) {
    const text = target === 'address' ? RECIPIENT : `Subject: ${subjectText()}\n\n${body()}`
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
