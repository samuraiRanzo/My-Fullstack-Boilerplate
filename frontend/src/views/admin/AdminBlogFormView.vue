<template>
  <div class="container">
    <p><router-link :to="{ name: 'admin-blogs' }">← Back to blogs</router-link></p>

    <h1>{{ isEdit ? 'Edit Blog (Admin)' : 'New Blog (Admin)' }}</h1>

    <form class="form" @submit.prevent="onSubmit">
      <label>
        Title
        <input type="text" v-model.trim="form.title" required />
      </label>

      <label>
        Content
        <textarea v-model="form.content" rows="10" required></textarea>
      </label>

      <div class="row">
        <label class="small">
          Author ID (optional)
          <input type="number" v-model.number="form.author_id" min="1" placeholder="Leave empty to default to self" />
        </label>
        <label class="small">
          Status
          <select v-model="form.status">
            <option value="PENDING">PENDING</option>
            <option value="APPROVED">APPROVED</option>
            <option value="DENIED">DENIED</option>
          </select>
        </label>
      </div>

      <button type="submit" :disabled="submitting">
        {{ submitting ? (isEdit ? 'Saving…' : 'Creating…') : (isEdit ? 'Save Changes' : 'Create Post') }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
import { adminBlogRetrieve, adminBlogCreate, adminBlogUpdate } from '../../services/adminBlog'

const route = useRoute()
const router = useRouter()
const admin = useAdminStore()

const isEdit = computed(() => route.name === 'admin-blog-edit' || Boolean(route.params.id))
const id = computed(() => route.params.id)

const form = reactive({ title: '', content: '', author_id: '', status: 'PENDING' })
const error = ref('')
const submitting = ref(false)

onMounted(async () => {
  if (isEdit.value && id.value) {
    try {
      const data = await adminBlogRetrieve(id.value, admin.getAuthProvider())
      form.title = data.title || ''
      form.content = data.content || ''
      form.status = data.status || 'PENDING'
      form.author_id = data.author?.id || ''
    } catch (e) {
      error.value = e.message || 'Failed to load post'
    }
  }
})

async function onSubmit() {
  error.value = ''
  submitting.value = true
  try {
    const payload = {
      title: form.title,
      content: form.content,
      status: form.status,
    }
    if (form.author_id) payload.author_id = form.author_id

    if (isEdit.value && id.value) {
      const updated = await adminBlogUpdate(id.value, payload, admin.getAuthProvider())
      router.push({ name: 'admin-blog-detail', params: { id: updated.id } })
    } else {
      const created = await adminBlogCreate(payload, admin.getAuthProvider())
      router.push({ name: 'admin-blog-detail', params: { id: created.id } })
    }
  } catch (e) {
    error.value = e.message || 'Failed to submit'
    if (e.status === 401 || e.status === 403) {
      router.push({ name: 'admin-login', query: { next: route.fullPath } })
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.container { padding: 1rem 0; }
.form { display: grid; gap: 0.75rem; max-width: 720px; }
label { display: grid; gap: 0.35rem; }
.small { max-width: 240px; }
.row { display: flex; gap: 1rem; flex-wrap: wrap; }
input, textarea, select { padding: 0.6rem 0.7rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; font-family: inherit; }
button { padding: 0.6rem 1rem; font-size: 1rem; border-radius: 6px; background: #333; color: white; border: none; cursor: pointer; width: fit-content; }
button:disabled { opacity: .75; cursor: default; }
.error { color: #c00; white-space: pre-line; }
</style>
