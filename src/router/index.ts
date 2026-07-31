import { createRouter, createWebHistory } from 'vue-router'

// Stage 1: simple flat route table matching the original static pages 1:1.
const routes = [
  { path: '/', name: 'home', component: () => import('@/pages/HomePage.vue') },
  { path: '/works', name: 'works', component: () => import('@/pages/WorksPage.vue') },
  { path: '/store', name: 'store', component: () => import('@/pages/StorePage.vue') },
  { path: '/journal', name: 'journal', component: () => import('@/pages/JournalPage.vue') },
  { path: '/about', name: 'about', component: () => import('@/pages/AboutPage.vue') },
  { path: '/feedback', name: 'feedback', component: () => import('@/pages/FeedbackPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
})

export default router
