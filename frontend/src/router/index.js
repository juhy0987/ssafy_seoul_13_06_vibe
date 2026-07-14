import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/board/:category',
      name: 'board',
      component: () => import('@/views/BoardView.vue'),
      props: true,
    },
    {
      path: '/board/:category/new',
      name: 'post-create',
      component: () => import('@/views/PostFormView.vue'),
      props: true,
    },
    {
      path: '/board/:category/:id(\\d+)',
      name: 'post-detail',
      component: () => import('@/views/PostDetailView.vue'),
      props: true,
    },
    {
      path: '/board/:category/:id(\\d+)/edit',
      name: 'post-edit',
      component: () => import('@/views/PostFormView.vue'),
      props: true,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition ?? { top: 0 }
  },
})

export default router
