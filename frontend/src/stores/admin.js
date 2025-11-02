import { defineStore } from 'pinia'
import { adminLogin, adminMe } from '../services/adminAuth'
import { apiRefresh } from '../services/auth'

const STORAGE_KEY = 'adminAuth'

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { access: null, refresh: null, admin: null }
    const parsed = JSON.parse(raw)
    return {
      access: parsed.access || null,
      refresh: parsed.refresh || null,
      admin: parsed.admin || null,
    }
  } catch (_) {
    return { access: null, refresh: null, admin: null }
  }
}

function saveToStorage({ access, refresh, admin }) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ access, refresh, admin }))
}

function clearStorage() {
  localStorage.removeItem(STORAGE_KEY)
}

export const useAdminStore = defineStore('admin', {
  state: () => ({
    access: loadFromStorage().access,
    refresh: loadFromStorage().refresh,
    admin: loadFromStorage().admin,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (s) => Boolean(s.access),
    isAdmin: (s) => Boolean(s.admin?.is_staff || s.admin?.is_superuser),
  },
  actions: {
    async login({ email, password }) {
      this.error = null
      this.loading = true
      try {
        const data = await adminLogin({ email, password })
        this.access = data.access
        this.refresh = data.refresh
        this.admin = data.user
        saveToStorage({ access: this.access, refresh: this.refresh, admin: this.admin })
        return data
      } catch (e) {
        this.error = e.message || 'Admin login failed'
        throw e
      } finally {
        this.loading = false
      }
    },
    getAuthProvider() {
      const self = this
      return {
        getAccess: async () => self.access,
        refresh: async () => {
          if (!self.refresh) return null
          try {
            const r = await apiRefresh(self.refresh)
            self.access = r.access
            saveToStorage({ access: self.access, refresh: self.refresh, admin: self.admin })
            return r.access
          } catch (_) {
            self.logout()
            return null
          }
        },
        logout: () => self.logout(),
      }
    },
    async loadMe() {
      if (!this.access) return null
      try {
        const me = await adminMe(this.getAuthProvider())
        this.admin = me
        saveToStorage({ access: this.access, refresh: this.refresh, admin: this.admin })
        return me
      } catch (e) {
        this.logout()
        return null
      }
    },
    logout() {
      this.access = null
      this.refresh = null
      this.admin = null
      this.error = null
      clearStorage()
    }
  }
})
