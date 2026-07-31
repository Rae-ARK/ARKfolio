import { createRouter, createWebHistory } from 'vue-router'

// Augment vue-router's RouteMeta so `to.meta.title` / `to.meta.description`
// are typed instead of `unknown` under strict mode.
declare module 'vue-router' {
  interface RouteMeta {
    title: string
    description: string
  }
}

const DEFAULT_DESCRIPTION =
  "Rae ARK writes fantasy and science-fantasy stories about people rebuilding themselves — reincarnation, isekai, and the quiet work of learning how to live again."

// Stage 1: simple flat route table matching the original static pages 1:1.
// Stage 2: each route carries its own <title>/description for SEO.
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage.vue'),
    meta: { title: 'Rae ARK — Web Novelist', description: DEFAULT_DESCRIPTION },
  },
  {
    path: '/works',
    name: 'works',
    component: () => import('@/pages/WorksPage.vue'),
    meta: {
      title: 'Works — Rae ARK',
      description:
        'Full synopses for Rae ARK\u2019s three ongoing web novels — Enigmatic Pathways Mystic Circuits, Summoned by Mistake I Decided to Learn How to Live, and The Shadow I Cast Over Two Beautiful Flowers.',
    },
  },
  {
    path: '/store',
    name: 'store',
    component: () => import('@/pages/StorePage.vue'),
    meta: {
      title: 'Store — Rae ARK',
      description: 'Paperback editions of Rae ARK\u2019s web novels, with links to retailers as titles go to print.',
    },
  },
  {
    path: '/journal',
    name: 'journal',
    component: () => import('@/pages/JournalPage.vue'),
    meta: {
      title: 'Journal — Rae ARK',
      description: 'A running journal of Rae ARK\u2019s writing process — the breaks, the doubts, the small wins — as it actually happens.',
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/pages/AboutPage.vue'),
    meta: {
      title: 'About — Rae ARK',
      description: 'Rae ARK writes character-driven fantasy and science fantasy about people rebuilding themselves. Read about the author and the stories behind the stories.',
    },
  },
  {
    path: '/feedback',
    name: 'feedback',
    component: () => import('@/pages/FeedbackPage.vue'),
    meta: {
      title: 'Feedback — Rae ARK',
      description: "Send feedback on Rae ARK's stories, paperbacks, or this site directly via email.",
    },
  },
]

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

router.afterEach((to) => {
  document.title = to.meta.title ?? 'Rae ARK — Web Novelist'
  setMetaTag('description', to.meta.description ?? DEFAULT_DESCRIPTION)
})

export default router
