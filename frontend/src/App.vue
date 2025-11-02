<template>
  <div>
    <nav class="nav">
      <router-link to="/" class="brand">Vue 3 + Vite + Django</router-link>
      <router-link to="/" class="link" active-class="active" exact-active-class="active">Home</router-link>
      <router-link to="/about" class="link" active-class="active">About</router-link>
      <router-link to="/blogs" class="link" active-class="active">Blogs</router-link>
      <router-link v-if="showAdminLink" to="/admin" class="link" active-class="active">Admin</router-link>
      <div class="spacer" />
      <template v-if="auth.isAuthenticated">
        <router-link to="/blogs/my" class="link" active-class="active">My Blogs</router-link>
        <span class="user">Hello, {{ auth.user?.first_name || auth.user?.username || auth.user?.email }}</span>
        <button class="link like-button" @click="onLogout">Logout</button>
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
