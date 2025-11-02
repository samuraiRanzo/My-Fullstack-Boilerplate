<template>
  <div class="container">
    <h1>Blogs</h1>
    <p v-if="loading">Loading…</p>
    <p v-if="error" class="error">{{ error }}</p>
    <ul class="list" v-if="posts.length">
      <li v-for="post in posts" :key="post.id" class="item">
        <router-link :to="{ name: 'blog-detail', params: { id: post.id } }" class="title">{{ post.title }}</router-link>
        <div class="meta">
          <span>by {{ post.author?.first_name || post.author?.username || post.author?.email }}</span>
          <span>•</span>
          <span>{{ formatDate(post.created_at) }}</span>
        </div>
      </li>
    </ul>
    <p v-else-if="!loading && !error">No posts yet.</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { listPublic } from '../services/blog'

const posts = ref([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    posts.value = await listPublic()
  } catch (e) {
    error.value = e.message || 'Failed to load posts'
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
.list { list-style: none; padding: 0; margin: 1rem 0; display: grid; gap: 1rem; }
.item { padding: 1rem; border: 1px solid #eee; border-radius: 8px; }
.title { font-weight: 600; text-decoration: none; color: #333; }
.meta { color: #666; font-size: 0.9rem; margin-top: 0.25rem; display: flex; gap: 0.4rem; }
.error { color: #c00; }
</style>
