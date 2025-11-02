<template>
  <div class="auth-container">
    <h1>Create Account</h1>

    <form @submit.prevent="onSubmit" class="form">
      <label>
        Email
        <input type="email" v-model.trim="form.email" required autocomplete="email" />
      </label>

      <label>
        Password
        <input type="password" v-model="form.password" required minlength="8" autocomplete="new-password" />
      </label>

      <label>
        Confirm Password
        <input type="password" v-model="form.password2" required minlength="8" autocomplete="new-password" />
      </label>

      <details>
        <summary>Optional details</summary>
        <label>
          Username (optional)
          <input type="text" v-model.trim="form.username" />
        </label>
        <label>
          First name (optional)
          <input type="text" v-model.trim="form.first_name" />
        </label>
        <label>
          Last name (optional)
          <input type="text" v-model.trim="form.last_name" />
        </label>
      </details>

      <button type="submit" :disabled="auth.loading">
        {{ auth.loading ? 'Creating…' : 'Register' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <p class="hint">
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  password2: '',
  username: '',
  first_name: '',
  last_name: '',
})

const error = ref('')
watch(() => auth.error, (v) => { if (v) error.value = v })

async function onSubmit() {
  error.value = ''
  if (form.password !== form.password2) {
    error.value = 'Passwords do not match.'
    return
  }
  try {
    await auth.register({ ...form })
    router.push('/')
  } catch (e) {
    error.value = e.message || 'Registration failed'
  }
}
</script>

<style scoped>
.auth-container { max-width: 520px; margin: 0 auto; }
.form { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.95rem; }
input { padding: 0.6rem 0.7rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
button { padding: 0.6rem 1rem; font-size: 1rem; border-radius: 6px; background: #42b883; color: white; border: none; cursor: pointer; }
button:disabled { opacity: 0.7; cursor: default; }
.error { color: #c00; white-space: pre-line; }
details { margin-top: 0.5rem; }
summary { cursor: pointer; }
.hint { margin-top: 0.75rem; }
</style>
