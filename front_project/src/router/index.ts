import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('@/views/LibraryView.vue')
  },
  {
    path: '/reader/:id',
    name: 'Reader',
    component: () => import('@/views/ReaderView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router