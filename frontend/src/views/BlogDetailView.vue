<template>
  <div class="container">
    <p><router-link to="/blogs">← Back to list</router-link></p>

    <div v-if="loading">Loading…</div>
    <p v-if="error" class="error">{{ error }}</p>

    <article v-if="post" class="post">
      <header>
        <h1 class="title">{{ post.title }}</h1>
        <div class="meta">
          <span>by {{ post.author?.first_name || post.author?.username || post.author?.email }}</span>
          <span>•</span>
          <span>{{ formatDate(post.created_at) }}</span>
          <span v-if="post.status" class="status" :data-status="post.status">{{ post.status }}</span>
        </div>
      </header>
      <div class="content" v-html="formatContent(post.content)"></div>

      <div class="actions" v-if="canEdit">
        <router-link class="btn" :to="{ name: 'blog-edit', params: { id: post.id } }">Edit</router-link>
      </div>
    </article>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { retrieve } from '../services/blog'

const route = useRoute()
const auth = useAuthStore()

const post = ref(null)
const loading = ref(false)
const error = ref('')

const id = computed(() => route.params.id)

onMounted(load)
watch(id, load)

async function load() {
  if (!id.value) return
  loading.value = true
  error.value = ''
  post.value = null
  try {
    post.value = await retrieve(id.value, auth.access)
  } catch (e) {
    error.value = e.message || 'Failed to load post'
  } finally {
    loading.value = false
  }
}

const canEdit = computed(() => {
  if (!post.value || !auth.user) return false
  return auth.user.id === post.value.author?.id
})

function formatDate(s) {
  try { return new Date(s).toLocaleString() } catch { return s }
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt','"':'&quot;','\'':'&#39;'}[c]))
}

function formatContent(text) {
  if (!text) return ''
  // basic formatting: escape and convert newlines to <br>
  return escapeHtml(text).replace(/\n/g, '<br />')
}
</script>

<style scoped>
.container { padding: 1rem 0; }
.post { border: 1px solid #eee; padding: 1rem; border-radius: 8px; }
.title { margin: 0 0 0.25rem; }
.meta { color: #666; font-size: 0.9rem; display: flex; gap: 0.4rem; align-items: center; }
.content { margin-top: 1rem; white-space: pre-wrap; }
.actions { margin-top: 1rem; }
.btn { display: inline-block; text-decoration: none; background: #42b883; color: white; padding: 0.4rem 0.8rem; border-radius: 6px; }
.status { margin-left: auto; font-size: 0.8rem; padding: 0.1rem 0.4rem; border-radius: 4px; border: 1px solid #ddd; color: #555; text-transform: capitalize; }
.status[data-status="APPROVED"], .status[data-status="approved"] { color: #2b8a3e; border-color: #c6f6d5; background: #f0fff4; }
.status[data-status="PENDING"], .status[data-status="pending"] { color: #8a6d3b; border-color: #ffe8a1; background: #fffbeb; }
.status[data-status="DENIED"], .status[data-status="denied"] { color: #c00; border-color: #ffd6d6; background: #fff5f5; }
.error { color: #c00; }
</style>
