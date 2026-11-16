import { createRouter, createWebHistory, type RouteRecordRaw, type RouteRecordSingleView } from 'vue-router'
import { buildJsonLd, type SchemaKind } from '@/seo/structuredData'
import { SITE_ORIGIN } from '@/seo/site'
import { useLocale } from '@/composables/useLocale'
import type { Locale } from '@/I18n'

// Augment vue-router's RouteMeta so `to.meta.title` / `to.meta.description`
// are typed instead of `unknown` under strict mode.
declare module 'vue-router' {
  interface RouteMeta {
    title: string
    description: string
    /** Which language this route renders in (en = unprefixed, ja = /ja/...). */
    locale: Locale
    /** Adds <meta name="robots" content="noindex"> while this route is active. */
    noindex?: boolean
    /** Injects the matching JSON-LD block (see seo/structuredData.ts). */
    schema?: SchemaKind
  }
}

const DEFAULT_DESCRIPTION =
  "Rae ARK writes fantasy and science-fantasy stories about people rebuilding themselves — reincarnation, isekai, and the quiet work of learning how to live again."

interface PageMeta {
  title: string
  description: string
  noindex?: boolean
  schema?: SchemaKind
}

interface PageDef {
  path: string
  name: string
  component: RouteRecordSingleView['component']
  meta: Record<Locale, PageMeta>
}

// Japanese localization (0012): every page exists twice — `/works` (en) and
// `/ja/works` (ja). The URL is the only language switch; there is no toggle
// button. Page bodies that haven't been translated yet (stages 3–4) still
// render English text inside the /ja route; <title> and description are
// already Japanese.
const pages: PageDef[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage.vue'),
    meta: {
      en: { title: 'Rae ARK — Web Novelist', description: DEFAULT_DESCRIPTION, schema: 'person' },
      ja: {
        title: 'Rae ARK（嵐久 怜）— Web小説家',
        description:
          '転生や異世界、そして「もう一度生き方を学ぶ」静かな営みを通じて、自分自身を作り直していく人々の物語を、ファンタジーとサイエンスファンタジーで綴るWeb小説家です。',
        schema: 'person',
      },
    },
  },
  {
    path: '/works',
    name: 'works',
    component: () => import('@/pages/WorksPage.vue'),
    meta: {
      en: {
        title: 'Works — Rae ARK',
        description:
          'Full synopses for Rae ARK\u2019s three ongoing web novels — Enigmatic Pathways Mystic Circuits, Summoned by Mistake I Decided to Learn How to Live, and The Shadow I Cast Over Two Beautiful Flowers.',
      },
      ja: {
        title: '作品 — Rae ARK',
        description:
          'Rae ARKが連載中の3つのWeb小説 ― Enigmatic Pathways Mystic Circuits、Summoned by Mistake I Decided to Learn How to Live、The Shadow I Cast Over Two Beautiful Flowers ― の詳しいあらすじ。',
      },
    },
  },
  {
    path: '/store',
    name: 'store',
    component: () => import('@/pages/StorePage.vue'),
    meta: {
      en: {
        title: 'Store — Rae ARK',
        description: 'Paperback editions of Rae ARK\u2019s web novels, with links to retailers as titles go to print.',
        schema: 'book',
      },
      ja: {
        title: 'ストア — Rae ARK',
        description: 'Rae ARKのWeb小説のペーパーバック版。書籍化されるたびに、取扱店へのリンクを掲載していきます。',
        schema: 'book',
      },
    },
  },
  {
    path: '/journal',
    name: 'journal',
    component: () => import('@/pages/JournalPage.vue'),
    meta: {
      en: {
        title: 'Journal — Rae ARK',
        description: 'A running journal of Rae ARK\u2019s writing process — the breaks, the doubts, the small wins — as it actually happens.',
      },
      ja: {
        title: 'ジャーナル — Rae ARK',
        description: '休筆、迷い、ささやかな前進 ― Rae ARKの執筆の過程を、ありのままに綴る連載日誌。',
      },
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/pages/AboutPage.vue'),
    meta: {
      en: {
        title: 'About — Rae ARK',
        description: 'Rae ARK writes character-driven fantasy and science fantasy about people rebuilding themselves. Read about the author and the stories behind the stories.',
        schema: 'person',
      },
      ja: {
        title: '作者について — Rae ARK',
        description: 'Rae ARKは、自分を作り直していく人々を描く、キャラクター重視のファンタジー／サイエンスファンタジーを執筆しています。作者と物語の背景をご紹介します。',
        schema: 'person',
      },
    },
  },
  {
    path: '/feedback',
    name: 'feedback',
    component: () => import('@/pages/FeedbackPage.vue'),
    meta: {
      en: {
        title: 'Feedback — Rae ARK',
        description: "Send feedback on Rae ARK's stories, paperbacks, or this site directly via email.",
      },
      ja: {
        title: 'フィードバック — Rae ARK',
        description: 'Rae ARKの物語、ペーパーバック、このサイトについてのご意見・ご感想をメールで直接お送りください。',
      },
    },
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: () => import('@/pages/PrivacyPolicyPage.vue'),
    meta: {
      en: {
        title: 'Privacy Policy — Rae ARK',
        description: 'How the Rae ARK site and Android app handle data and permissions.',
      },
      ja: {
        title: 'プライバシーポリシー — Rae ARK',
        description: 'Rae ARKのサイトおよびAndroidアプリにおける、データと権限の取り扱いについて。',
      },
    },
  },
  {
    path: '/terms',
    name: 'terms',
    component: () => import('@/pages/TermsPage.vue'),
    meta: {
      en: {
        title: 'Terms & Conditions — Rae ARK',
        description: 'Terms of use for the Rae ARK site and Android app.',
      },
      ja: {
        title: '利用規約 — Rae ARK',
        description: 'Rae ARKのサイトおよびAndroidアプリのご利用にあたっての規約。',
      },
    },
  },
  // Catch-all, must stay last. The host serves index.html (HTTP 200) for any
  // unknown path, so this page tells crawlers not to index it (a "soft 404" fix).
  // The /ja variant is more specific, so unknown /ja/... paths land on it
  // instead of the English one.
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: {
      en: { title: 'Page not found — Rae ARK', description: 'This page could not be found.', noindex: true },
      ja: { title: 'ページが見つかりません — Rae ARK', description: 'このページは見つかりませんでした。', noindex: true },
    },
  },
]

const JA_PREFIX = '/ja'

/** `/works` -> `/ja/works`, `/` -> `/ja`, `/:pathMatch(.*)*` -> `/ja/:pathMatch(.*)*`. */
function toJaPath(path: string): string {
  return path === '/' ? JA_PREFIX : `${JA_PREFIX}${path}`
}

/** `/ja/works` -> `/works`, `/ja` -> `/`. Paths without the prefix pass through. */
function toEnPath(path: string): string {
  if (path === JA_PREFIX) return '/'
  return path.startsWith(`${JA_PREFIX}/`) ? path.slice(JA_PREFIX.length) : path
}

const routes: RouteRecordRaw[] = pages.flatMap((page) =>
  (['en', 'ja'] as const).map((locale): RouteRecordRaw => ({
    path: locale === 'ja' ? toJaPath(page.path) : page.path,
    name: locale === 'ja' ? `${page.name}-ja` : page.name,
    component: page.component,
    meta: { ...page.meta[locale], locale },
  }))
)

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
})

function setMetaTag(name: string, content: string) {
  let tag = document.head.querySelector<HTMLMetaElement>(`meta[name="${name}"]`)
  if (!tag) {
    tag = document.createElement('meta')
    tag.setAttribute('name', name)
    document.head.appendChild(tag)
  }
  tag.setAttribute('content', content)
}

function setRobots(noindex: boolean) {
  const existing = document.head.querySelector<HTMLMetaElement>('meta[name="robots"]')
  if (noindex) setMetaTag('robots', 'noindex')
  else existing?.remove()
}

const JSON_LD_ID = 'route-json-ld'

function setJsonLd(data: Record<string, unknown> | null) {
  let tag = document.getElementById(JSON_LD_ID)
  if (!data) {
    tag?.remove()
    return
  }
  if (!tag) {
    tag = document.createElement('script')
    tag.id = JSON_LD_ID
    tag.setAttribute('type', 'application/ld+json')
    document.head.appendChild(tag)
  }
  tag.textContent = JSON.stringify(data)
}

// --- Language follows the URL -------------------------------------------------

const { setLocale } = useLocale()

// Browser back/forward must be able to land on an English URL; only in-app
// link clicks get bounced back into /ja (see the guard below). History
// listeners all run synchronously on popstate, before any navigation guard,
// so this flag is already set by the time beforeEach looks at it.
let isPopNavigation = false
router.options.history.listen((_to, _from, info) => {
  isPopNavigation = String(info.type) === 'pop'
})

router.beforeEach((to, from) => {
  // The pages still link to unprefixed paths (`/works`, `/feedback`, ...).
  // Once you're reading Japanese, keep you in it: send those links to their
  // /ja twin, keeping query and hash (the store page links with ?subject=).
  if (to.meta.locale === 'en' && from.meta.locale === 'ja' && !isPopNavigation) {
    return { path: toJaPath(to.path), query: to.query, hash: to.hash }
  }
  setLocale(to.meta.locale)
})

// --- <head> bookkeeping ---------------------------------------------------------

const HREFLANG_ATTR = 'data-route-hreflang'

function setAlternates(path: string | null) {
  document.head.querySelectorAll(`link[${HREFLANG_ATTR}]`).forEach((el) => el.remove())
  if (path === null) return
  const en = toEnPath(path)
  const alternates: [string, string][] = [
    ['en', en],
    ['ja', toJaPath(en)],
    ['x-default', en],
  ]
  for (const [hreflang, href] of alternates) {
    const link = document.createElement('link')
    link.setAttribute('rel', 'alternate')
    link.setAttribute('hreflang', hreflang)
    link.setAttribute('href', `${SITE_ORIGIN}${href === '/' ? '' : href}`)
    link.setAttribute(HREFLANG_ATTR, '')
    document.head.appendChild(link)
  }
}

router.afterEach((to) => {
  isPopNavigation = false
  document.title = to.meta.title ?? 'Rae ARK — Web Novelist'
  setMetaTag('description', to.meta.description ?? DEFAULT_DESCRIPTION)
  setRobots(to.meta.noindex === true)
  setJsonLd(to.meta.schema ? buildJsonLd(to.meta.schema) : null)
  // Every indexable page has an en/ja twin; 404s have none.
  setAlternates(to.meta.noindex ? null : to.path)
})

export default router
