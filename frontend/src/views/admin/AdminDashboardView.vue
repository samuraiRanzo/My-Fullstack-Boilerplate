<template>
  <div class="container">
    <h1>Admin Dashboard</h1>
    <p>Welcome, <strong>{{ admin.admin?.first_name || admin.admin?.username || admin.admin?.email }}</strong></p>
    <ul class="nav">
      <li><router-link :to="{ name: 'admin-blogs' }">Manage Blogs</router-link></li>
      <li><button class="link" @click="onLogout">Logout</button></li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import router from "../../router/index.js";

const admin = useAdminStore()

onMounted(() => {
  if (admin.access && !admin.admin) admin.loadMe()
})

async function onLogout() {
  await admin.logout()
  await router.push({ name: 'home' })
}
</script>

<style scoped>
.container { padding: 1rem 0; }
.nav { list-style: none; padding: 0; display: flex; gap: 1rem; }
.link { background: transparent; border: none; color: #333; cursor: pointer; padding: 0; }
</style>
