import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAdminStore } from '../stores/admin'

// Lazy-loaded views
const HomeView = () => import('../views/HomeView.vue')
const AboutView = () => import('../views/AboutView.vue')
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const BlogListView = () => import('../views/BlogListView.vue')
const MyBlogsView = () => import('../views/MyBlogsView.vue')
const BlogDetailView = () => import('../views/BlogDetailView.vue')
const BlogFormView = () => import('../views/BlogFormView.vue')

// Admin views (lazy)
const AdminLoginView = () => import('../views/admin/AdminLoginView.vue')
const AdminDashboardView = () => import('../views/admin/AdminDashboardView.vue')
const AdminBlogListView = () => import('../views/admin/AdminBlogListView.vue')
const AdminBlogFormView = () => import('../views/admin/AdminBlogFormView.vue')
const AdminBlogDetailView = () => import('../views/admin/AdminBlogDetailView.vue')

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/blogs', name: 'blogs', component: BlogListView },
  { path: '/blogs/my', name: 'my-blogs', component: MyBlogsView, meta: { requiresAuth: true } },
  { path: '/blogs/new', name: 'blog-new', component: BlogFormView, meta: { requiresAuth: true } },
  { path: '/blogs/:id', name: 'blog-detail', component: BlogDetailView, props: true },
  { path: '/blogs/:id/edit', name: 'blog-edit', component: BlogFormView, meta: { requiresAuth: true }, props: true },

  // Admin routes
  { path: '/admin/login', name: 'admin-login', component: AdminLoginView },
  { path: '/admin', name: 'admin-home', component: AdminDashboardView, meta: { requiresAdmin: true } },
  { path: '/admin/blogs', name: 'admin-blogs', component: AdminBlogListView, meta: { requiresAdmin: true } },
  { path: '/admin/blogs/new', name: 'admin-blog-new', component: AdminBlogFormView, meta: { requiresAdmin: true } },
  { path: '/admin/blogs/:id', name: 'admin-blog-detail', component: AdminBlogDetailView, meta: { requiresAdmin: true }, props: true },
  { path: '/admin/blogs/:id/edit', name: 'admin-blog-edit', component: AdminBlogFormView, meta: { requiresAdmin: true }, props: true },
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
