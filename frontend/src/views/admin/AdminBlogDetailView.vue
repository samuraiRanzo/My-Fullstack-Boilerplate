<template>
  <div class="container">
    <p><router-link :to="{ name: 'admin-blogs' }">← Back to list</router-link></p>

    <div v-if="loading">Loading…</div>
    <p v-if="error" class="error">{{ error }}</p>

    <article v-if="post" class="post">
      <header>
        <h1 class="title">#{{ post.id }} • {{ post.title }}</h1>
        <div class="meta">
          <span>by {{ post.author?.first_name || post.author?.username || post.author?.email }}</span>
          <span>•</span>
          <span>{{ formatDate(post.created_at) }}</span>
          <span class="status" :data-status="post.status">{{ post.status }}</span>
        </div>
      </header>
      <div class="content" v-html="formatContent(post.content)"></div>

      <div class="actions">
        <router-link class="btn" :to="{ name: 'admin-blog-edit', params: { id: post.id } }">Edit</router-link>
        <button class="btn ghost" @click="approve('APPROVED')" :disabled="acting || post.status==='APPROVED'">Approve</button>
        <button class="btn ghost" @click="approve('DENIED')" :disabled="acting || post.status==='DENIED'">Deny</button>
        <button class="btn danger" @click="onDelete" :disabled="acting">Delete</button>
      </div>
    </article>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
import { adminBlogRetrieve, adminBlogUpdate, adminBlogDelete } from '../../services/adminBlog'

const route = useRoute()
const router = useRouter()
const admin = useAdminStore()

const post = ref(null)
const loading = ref(false)
const error = ref('')
const acting = ref(false)

onMounted(load)

async function load() {
  loading.value = true
  error.value = ''
  post.value = null
  try {
    post.value = await adminBlogRetrieve(route.params.id, admin.getAuthProvider())
  } catch (e) {
    error.value = e.message || 'Failed to load post'
  } finally {
    loading.value = false
  }
}

async function approve(status) {
  acting.value = true
  error.value = ''
  try {
    const updated = await adminBlogUpdate(post.value.id, { status }, admin.getAuthProvider(), 'PATCH')
    post.value = updated
  } catch (e) {
    error.value = e.message || 'Failed to update status'
  } finally {
    acting.value = false
  }
}

async function onDelete() {
  if (!confirm('Delete this post?')) return
  acting.value = true
  error.value = ''
  try {
    await adminBlogDelete(post.value.id, admin.getAuthProvider())
    router.push({ name: 'admin-blogs' })
  } catch (e) {
    error.value = e.message || 'Failed to delete'
  } finally {
    acting.value = false
  }
}

function formatDate(s) { try { return new Date(s).toLocaleString() } catch { return s } }
function escapeHtml(str) { return String(str).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt','"':'&quot;','\'':'&#39;'}[c])) }
function formatContent(text) { if (!text) return ''; return escapeHtml(text).replace(/\n/g, '<br />') }
</script>

<style scoped>
.container { padding: 1rem 0; }
.post { border: 1px solid #eee; padding: 1rem; border-radius: 8px; }
.title { margin: 0 0 0.25rem; }
.meta { color: #666; font-size: 0.9rem; display: flex; gap: 0.4rem; align-items: center; }
.content { margin-top: 1rem; white-space: pre-wrap; }
.actions { margin-top: 1rem; display: flex; gap: 0.5rem; }
.btn { text-decoration: none; background: #333; color: white; padding: 0.4rem 0.8rem; border-radius: 6px; border: none; cursor: pointer; }
.btn.ghost { background: transparent; color: #333; border: 1px solid #ddd; }
.btn.danger { background: #c00; }
.status { margin-left: auto; font-size: 0.8rem; padding: 0.1rem 0.4rem; border-radius: 4px; border: 1px solid #ddd; color: #555; text-transform: capitalize; }
.status[data-status="APPROVED"] { color: #2b8a3e; border-color: #c6f6d5; background: #f0fff4; }
.status[data-status="PENDING"] { color: #8a6d3b; border-color: #ffe8a1; background: #fffbeb; }
.status[data-status="DENIED"] { color: #c00; border-color: #ffd6d6; background: #fff5f5; }
.error { color: #c00; }
</style>
