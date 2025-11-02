import { defineStore } from 'pinia'
import { apiLogin, apiRegister, apiRefresh, apiUser } from '../services/auth'

const STORAGE_KEY = 'auth'

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { access: null, refresh: null, user: null }
    const parsed = JSON.parse(raw)
    return { access: parsed.access || null, refresh: parsed.refresh || null, user: parsed.user || null }
  } catch (_) {
    return { access: null, refresh: null, user: null }
  }
}

function saveToStorage({ access, refresh, user }) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ access, refresh, user }))
}

function clearStorage() {
  localStorage.removeItem(STORAGE_KEY)
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    access: loadFromStorage().access,
    refresh: loadFromStorage().refresh,
    user: loadFromStorage().user,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (s) => Boolean(s.access),
  },
  actions: {
    async login({ email, password }) {
      this.error = null
      this.loading = true
      try {
        const data = await apiLogin({ email, password })
        this.access = data.access
        this.refresh = data.refresh
        this.user = data.user
        saveToStorage({ access: this.access, refresh: this.refresh, user: this.user })
        return data
      } catch (e) {
        this.error = e.message || 'Login failed'
        throw e
      } finally {
        this.loading = false
      }
    },
    async register(payload) {
      this.error = null
      this.loading = true
      try {
        const user = await apiRegister(payload)
        // After successful registration, log in user automatically if password provided
        if (payload.email && payload.password) {
          await this.login({ email: payload.email, password: payload.password })
        } else {
          this.user = user
        }
        return user
      } catch (e) {
        this.error = e.message || 'Registration failed'
        throw e
      } finally {
        this.loading = false
      }
    },
    async loadUser() {
      if (!this.access) return null
      try {
        // apiUser uses apiFetch with auth:true which will attempt a silent refresh on 401
        const data = await apiUser()
        this.user = data
        saveToStorage({ access: this.access, refresh: this.refresh, user: this.user })
        return data
      } catch (e) {
        // If still failing (e.g., refresh expired/invalid), logout
        this.logout()
        return null
      }
    },
    async refreshAccess() {
      if (!this.refresh) return null
      try {
        const r = await apiRefresh(this.refresh)
        this.access = r.access
        saveToStorage({ access: this.access, refresh: this.refresh, user: this.user })
        return r.access
      } catch (e) {
        this.logout()
        return null
      }
    },
    logout() {
      this.access = null
      this.refresh = null
      this.user = null
      this.error = null
      clearStorage()
    }
  }
})
