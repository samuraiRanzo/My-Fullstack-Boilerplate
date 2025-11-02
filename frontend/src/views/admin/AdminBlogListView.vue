<template>
  <div class="container">
    <header class="head">
      <h1>Admin • Blogs</h1>
      <router-link class="btn" :to="{ name: 'admin-blog-new' }">New</router-link>
    </header>

    <form class="filters" @submit.prevent="applyFilters">
      <label>
        Status
        <select v-model="filters.status">
          <option value="">Any</option>
          <option value="PENDING">PENDING</option>
          <option value="APPROVED">APPROVED</option>
          <option value="DENIED">DENIED</option>
        </select>
      </label>
      <label>
        Author ID
        <input type="number" v-model.number="filters.author_id" min="1" placeholder="e.g., 1" />
      </label>
      <label>
        Page size
        <select v-model.number="filters.page_size">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </label>
      <button type="submit">Apply</button>
      <button type="button" class="ghost" @click="resetFilters">Reset</button>
    </form>

    <p v-if="loading">Loading…</p>
    <p v-if="error" class="error">{{ error }}</p>

    <table v-if="items.length" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Author</th>
          <th>Status</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in items" :key="row.id" @click="open(row.id)" class="click">
          <td>{{ row.id }}</td>
          <td>{{ row.title }}</td>
          <td>{{ row.author?.username || row.author?.email }}</td>
          <td><span class="badge" :data-status="row.status">{{ row.status }}</span></td>
          <td>{{ formatDate(row.created_at) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="!loading && !error">No results.</p>

    <div class="pager" v-if="count > 0">
      <button :disabled="page <= 1" @click="go(page - 1)">Prev</button>
      <span>Page {{ page }} of {{ totalPages }}</span>
      <button :disabled="page >= totalPages" @click="go(page + 1)">Next</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
import { adminBlogList } from '../../services/adminBlog'

const admin = useAdminStore()
const router = useRouter()
const route = useRoute()

const items = ref([])
const count = ref(0)
const loading = ref(false)
const error = ref('')

const filters = reactive({
  status: route.query.status || '',
  author_id: route.query.author_id ? Number(route.query.author_id) : '',
  page: route.query.page ? Number(route.query.page) : 1,
  page_size: route.query.page_size ? Number(route.query.page_size) : 20,
})

const page = computed(() => filters.page)
const totalPages = computed(() => Math.max(1, Math.ceil(count.value / (filters.page_size || 20))))

watch(() => route.query, () => syncFromRoute(), { deep: true })

function syncFromRoute() {
  filters.status = route.query.status || ''
  filters.author_id = route.query.author_id ? Number(route.query.author_id) : ''
  filters.page = route.query.page ? Number(route.query.page) : 1
  filters.page_size = route.query.page_size ? Number(route.query.page_size) : 20
  load()
}

onMounted(() => {
  if (admin.access && !admin.admin) admin.loadMe()
  load()
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const res = await adminBlogList({
      status: filters.status || undefined,
      author_id: filters.author_id || undefined,
      page: filters.page,
      page_size: filters.page_size,
    }, admin.getAuthProvider())
    items.value = res.results || []
    count.value = res.count || 0
  } catch (e) {
    error.value = e.message || 'Failed to load'
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  router.replace({ query: {
    ...(filters.status ? { status: filters.status } : {}),
    ...(filters.author_id ? { author_id: filters.author_id } : {}),
    page: 1,
    page_size: filters.page_size,
  } })
}

function resetFilters() {
  router.replace({ query: { page: 1, page_size: 20 } })
}

function go(p) {
  router.replace({ query: { ...route.query, page: p } })
}

function open(id) {
  router.push({ name: 'admin-blog-detail', params: { id } })
}

function formatDate(s) { try { return new Date(s).toLocaleString() } catch { return s } }
</script>

<style scoped>
.container { padding: 1rem 0; }
.head { display: flex; align-items: center; gap: 1rem; }
.btn { margin-left: auto; text-decoration: none; background: #333; color: #fff; padding: 0.45rem 0.8rem; border-radius: 6px; }
.filters { display: flex; gap: 0.75rem; align-items: end; margin: 0.75rem 0; flex-wrap: wrap; }
.filters label { display: grid; gap: 0.25rem; }
.filters input, .filters select { padding: 0.4rem 0.5rem; border: 1px solid #ddd; border-radius: 6px; }
.filters .ghost { background: transparent; border: 1px solid #ddd; padding: 0.4rem 0.7rem; border-radius: 6px; }
.table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
.table th, .table td { border: 1px solid #eee; padding: 0.5rem; text-align: left; }
.click { cursor: pointer; }
.badge { font-size: 0.8rem; padding: 0.1rem 0.4rem; border-radius: 4px; border: 1px solid #ddd; color: #555; text-transform: capitalize; }
.badge[data-status="APPROVED"] { color: #2b8a3e; border-color: #c6f6d5; background: #f0fff4; }
.badge[data-status="PENDING"] { color: #8a6d3b; border-color: #ffe8a1; background: #fffbeb; }
.badge[data-status="DENIED"] { color: #c00; border-color: #ffd6d6; background: #fff5f5; }
.pager { display: flex; align-items: center; gap: 0.75rem; margin-top: 0.75rem; }
</style>
