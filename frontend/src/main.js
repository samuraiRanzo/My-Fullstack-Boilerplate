import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { setAuthProvider } from './services/http'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// Wire the HTTP layer to the auth store for silent refresh
const auth = useAuthStore()
setAuthProvider({
  getAccess: async () => auth.access,
  refresh: async () => await auth.refreshAccess(),
  logout: () => auth.logout(),
})

app.use(router)
app.mount('#app')
