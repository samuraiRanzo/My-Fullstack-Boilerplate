<template>
  <div class="container">
    <header class="head">
      <h1>My Blogs</h1>
      <router-link class="btn" :to="{ name: 'blog-new' }">New Post</router-link>
    </header>

    <p v-if="loading">Loading…</p>
    <p v-if="error" class="error">{{ error }}</p>

    <ul class="list" v-if="posts.length">
      <li v-for="post in posts" :key="post.id" class="item">
        <div class="row">
          <router-link :to="{ name: 'blog-detail', params: { id: post.id } }" class="title">{{ post.title }}</router-link>
          <span class="status" :data-status="post.status">{{ post.status }}</span>
        </div>
        <div class="meta">
          <span>{{ formatDate(post.created_at) }}</span>
          <span>•</span>
          <router-link class="small" :to="{ name: 'blog-edit', params: { id: post.id } }">Edit</router-link>
        </div>
      </li>
    </ul>
    <p v-else-if="!loading && !error">You haven't written any posts yet.</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { listMine } from '../services/blog'

const auth = useAuthStore()

const posts = ref([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    posts.value = await listMine(auth.access)
  } catch (e) {
    error.value = e.message || 'Failed to load your posts'
  } finally {
    loading.value = false
  }
})

function formatDate(s) {
  try { return new Date(s).toLocaleString() } catch { return s }
}
</script>

<style scoped>
.container { padding: 1rem 0; }
.head { display: flex; align-items: center; gap: 1rem; }
.head .btn { margin-left: auto; text-decoration: none; background: #42b883; color: white; padding: 0.5rem 0.9rem; border-radius: 6px; }
.list { list-style: none; padding: 0; margin: 1rem 0; display: grid; gap: 1rem; }
.item { padding: 1rem; border: 1px solid #eee; border-radius: 8px; }
.row { display: flex; align-items: center; gap: 0.5rem; }
.title { font-weight: 600; text-decoration: none; color: #333; }
.status { margin-left: auto; font-size: 0.8rem; padding: 0.1rem 0.4rem; border-radius: 4px; border: 1px solid #ddd; color: #555; text-transform: capitalize; }
.status[data-status="APPROVED"], .status[data-status="approved"] { color: #2b8a3e; border-color: #c6f6d5; background: #f0fff4; }
.status[data-status="PENDING"], .status[data-status="pending"] { color: #8a6d3b; border-color: #ffe8a1; background: #fffbeb; }
.status[data-status="DENIED"], .status[data-status="denied"] { color: #c00; border-color: #ffd6d6; background: #fff5f5; }
.meta { color: #666; font-size: 0.9rem; margin-top: 0.25rem; display: flex; gap: 0.4rem; }
.small { font-size: 0.9rem; }
.error { color: #c00; }
</style>
