<template>
  <div class="container">
    <h1>Home</h1>
    <div v-if="authStore.user">
      <h2>Welcome, {{ authStore.user.username }}</h2>
      <div v-if="authStore.user.profile_picture">
        <img :src="authStore.user.profile_picture" alt="Profile picture" width="100">
      </div>
      <div>
        <input type="file" @change="onFileChange" accept="image/*">
        <button @click="uploadProfilePicture" :disabled="!selectedFile">Upload</button>
      </div>
    </div>
    <p>Status: <strong>{{ helloStore.status }}</strong></p>
    <p v-if="helloStore.message">Backend says: <code>{{ helloStore.message }}</code></p>
    <button @click="helloStore.fetchHello" :disabled="helloStore.loading">
      {{ helloStore.loading ? 'Loading…' : 'Call /api/hello/' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useHelloStore } from '../stores/hello'
import { apiFetch } from '../services/http'

const helloStore = useHelloStore()
const authStore = useAuthStore()

const selectedFile = ref(null)

function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function uploadProfilePicture() {
  if (!selectedFile.value) {
    return
  }

  const formData = new FormData()
  formData.append('profile_picture', selectedFile.value)

  try {
    await apiFetch('/auth/user/profile-picture/', {
      method: 'PUT',
      body: formData,
      headers: {
        // Do not set Content-Type, the browser will set it with the correct boundary
      }
    }, { auth: true })
    await authStore.loadUser()
  } catch (error) {
    console.error('Error uploading profile picture:', error)
  }
}

onMounted(() => {
  if (!helloStore.message) {
    helloStore.fetchHello()
  }
})
</script>

<style scoped>
.container { padding: 2rem; }
button { padding: 0.5rem 1rem; font-size: 1rem; }
code { background: #f5f5f5; padding: 0.2rem 0.4rem; border-radius: 4px; }
</style>