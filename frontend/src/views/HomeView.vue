<template>
  <div class="container">
    <h1>Home</h1>
    <p>Status: <strong>{{ store.status }}</strong></p>
    <p v-if="store.message">Backend says: <code>{{ store.message }}</code></p>
    <button @click="store.fetchHello" :disabled="store.loading">
      {{ store.loading ? 'Loading…' : 'Call /api/hello/' }}
    </button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useHelloStore } from '../stores/hello'

const store = useHelloStore()

onMounted(() => {
  if (!store.message) {
    store.fetchHello()
  }
})
</script>

<style scoped>
.container { padding: 2rem; }
button { padding: 0.5rem 1rem; font-size: 1rem; }
code { background: #f5f5f5; padding: 0.2rem 0.4rem; border-radius: 4px; }
</style>
