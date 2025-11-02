<template>
  <div class="auth-container">
    <h1>Admin Login</h1>

    <form @submit.prevent="onSubmit" class="form">
      <label>
        Email
        <input type="email" v-model.trim="email" required autocomplete="email" />
      </label>

      <label>
        Password
        <input type="password" v-model="password" required autocomplete="current-password" />
      </label>

      <button type="submit" :disabled="admin.loading">
        {{ admin.loading ? 'Signing in…' : 'Login' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'

const route = useRoute()
const router = useRouter()
const admin = useAdminStore()

const email = ref('')
const password = ref('')
const error = ref('')

watch(() => admin.error, (v) => { if (v) error.value = v })

async function onSubmit() {
  error.value = ''
  try {
    await admin.login({ email: email.value, password: password.value })
    const next = route.query.next || '/admin'
    router.push(next)
  } catch (e) {
    error.value = e.message || 'Login failed'
  }
}
</script>

<style scoped>
.auth-container { max-width: 420px; margin: 0 auto; }
.form { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.95rem; }
input { padding: 0.6rem 0.7rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
button { padding: 0.6rem 1rem; font-size: 1rem; border-radius: 6px; background: #333; color: white; border: none; cursor: pointer; }
button:disabled { opacity: 0.7; cursor: default; }
.error { color: #c00; white-space: pre-line; }
</style>
