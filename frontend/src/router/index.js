import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAdminStore } from '../stores/admin'
import { userRoutes } from './userRoutes'
import { adminRoutes } from './adminRoutes'

const routes = [
  ...userRoutes,
  ...adminRoutes,
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: 'active',
  linkExactActiveClass: 'active',
})

router.beforeEach((to) => {
  if (to.meta?.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isAuthenticated) {
      return { name: 'login', query: { next: to.fullPath } }
    }
  }
  if (to.meta?.requiresAdmin) {
    const admin = useAdminStore()
    if (!admin.isAuthenticated) {
      return { name: 'admin-login', query: { next: to.fullPath } }
    }
  }
  return true
})

export default router
