<template>
  <div>
    <nav class="nav">
      <router-link to="/" class="brand">Vue 3 + Vite + Django</router-link>
      <router-link to="/" class="link" active-class="active" exact-active-class="active">Home</router-link>
      <router-link to="/about" class="link" active-class="active">About</router-link>
      <router-link to="/blogs" class="link" active-class="active">Blogs</router-link>
      <router-link to="/books" class="link" active-class="active">Books</router-link>
      <router-link to="/pricing" class="link" active-class="active">Pricing</router-link>

      <DropdownMenu v-if="showAdminLink" title="Admin">
        <router-link to="/admin" class="link" active-class="active">Dashboard</router-link>
        <router-link to="/admin/blogs" class="link" active-class="active">Manage Blogs</router-link>
        <router-link to="/admin/books" class="link" active-class="active">Manage Books</router-link>
        <router-link to="/admin/subscription-plans" class="link" active-class="active">Manage Plans</router-link>
        <!-- Add other admin links here -->
      </DropdownMenu>

      <div class="spacer" />

      <template v-if="auth.isAuthenticated">
        <DropdownMenu :title="`Hello, ${auth.user?.first_name || auth.user?.username || auth.user?.email}`">
          <router-link to="/profile" class="link" active-class="active">My Profile</router-link>
          <router-link to="/blogs/my" class="link" active-class="active">My Blogs</router-link>
          <router-link to="/todos" class="link" active-class="active">My Todos</router-link>
          <router-link to="/subscription-management" class="link" active-class="active">Manage Subscription</router-link>
          <router-link to="/premium-feature" class="link" active-class="active">Premium Feature</router-link>
          <router-link v-if="auth.user?.is_staff || auth.user?.is_superuser" to="/books/upload" class="link" active-class="active">Upload Book</router-link>
          <button class="link like-button" @click="onLogout">Logout</button>
        </DropdownMenu>
      </template>
      <template v-else>
        <router-link to="/login" class="link" active-class="active">Login</router-link>
        <router-link to="/register" class="link" active-class="active">Register</router-link>
      </template>
    </nav>
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useAuthStore } from './stores/auth'
import { useAdminStore } from './stores/admin'
import DropdownMenu from './components/DropdownMenu.vue' // Import the new component

const auth = useAuthStore()
const admin = useAdminStore()

const showAdminLink = computed(() => {
  return Boolean(admin.isAuthenticated || auth.user?.is_staff || auth.user?.is_superuser)
})

onMounted(() => {
  // Try to load current user using stored token
  if (auth.access && !auth.user) auth.loadUser()
  // Load admin profile if admin token exists
  if (admin.access && !admin.admin) admin.loadMe()
})

function onLogout() {
  auth.logout()
}
</script>

<style>
body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }
.nav { display: flex; gap: 1rem; align-items: center; padding: 1rem 2rem; border-bottom: 1px solid #eee; }
.nav .brand { font-weight: 600; margin-right: auto; text-decoration: none; color: inherit; }
.link { text-decoration: none; color: #333; }
.link.active { color: #42b883; }
.container { padding: 2rem; }
button { padding: 0.5rem 1rem; font-size: 1rem; }
code { background: #f5f5f5; padding: 0.2rem 0.4rem; border-radius: 4px; }
.spacer { margin-left: auto; }
.user { color: #555; }
.like-button { background: transparent; border: none; color: #42b883; cursor: pointer; padding: 0; }
</style>
