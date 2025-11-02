import { defineStore } from 'pinia'

export const useHelloStore = defineStore('hello', {
  state: () => ({
    status: 'ready',
    loading: false,
    message: '',
  }),
  actions: {
    async fetchHello() {
      if (this.loading) return
      this.loading = true
      this.status = 'contacting backend…'
      try {
        const res = await fetch('/api/hello/')
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        this.message = data.message || JSON.stringify(data)
        this.status = 'ok'
      } catch (e) {
        this.status = `error: ${e.message}`
      } finally {
        this.loading = false
      }
    }
  }
})
