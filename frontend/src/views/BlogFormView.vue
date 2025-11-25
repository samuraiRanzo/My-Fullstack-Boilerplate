<template>
  <div class="container">
    <p><router-link to="/blogs">← Back to blogs</router-link></p>

    <h1>{{ isEdit ? 'Edit Post' : 'New Post' }}</h1>

    <form class="form" @submit.prevent="onSubmit">
      <label>
        Title
        <input type="text" v-model.trim="form.title" required />
      </label>

      <label>
        Content
        <textarea v-model="form.content" rows="10" required></textarea>
      </label>

      <label>
        Cover Image
        <input type="file" @change="onFileChange" accept="image/*">
      </label>

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
import { useAuthStore } from '../stores/auth'
import { retrieve, createPost, updatePost } from '../services/blog'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isEdit = computed(() => route.name === 'blog-edit' || Boolean(route.params.id))
const id = computed(() => route.params.id)
const selectedFile = ref(null)

const form = reactive({ title: '', content: '' })
const error = ref('')
const submitting = ref(false)

function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

onMounted(async () => {
  if (isEdit.value && id.value) {
    try {
      const data = await retrieve(id.value, auth.access)
      form.title = data.title || ''
      form.content = data.content || ''
    } catch (e) {
      error.value = e.message || 'Failed to load post'
    }
  }
})

async function onSubmit() {
  error.value = ''
  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('title', form.title)
    formData.append('content', form.content)
    if (selectedFile.value) {
      formData.append('cover_image', selectedFile.value)
    }

    if (isEdit.value && id.value) {
      const updated = await updatePost(id.value, formData, auth.access)
      router.push({ name: 'blog-detail', params: { id: updated.id } })
    } else {
      const created = await createPost(formData, auth.access)
      router.push({ name: 'blog-detail', params: { id: created.id } })
    }
  } catch (e) {
    error.value = e.message || 'Failed to submit'
    if (e.status === 401 || e.status === 403) {
      // If unauthorized, redirect to login and come back here
      router.push({ name: 'login', query: { next: route.fullPath } })
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
input, textarea { padding: 0.6rem 0.7rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; font-family: inherit; }
button { padding: 0.6rem 1rem; font-size: 1rem; border-radius: 6px; background: #42b883; color: white; border: none; cursor: pointer; width: fit-content; }
button:disabled { opacity: .75; cursor: default; }
.error { color: #c00; white-space: pre-line; }
</style>
