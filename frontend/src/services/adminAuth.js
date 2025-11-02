// Admin auth service
// Base: /admin-api
import { apiFetch } from './http'

const ADMIN_API_BASE = '/admin-api'

export async function adminLogin({ email, password }) {
  // Returns: { access, refresh, user: { ... , is_staff, is_superuser } }
  return await apiFetch(`${ADMIN_API_BASE}/auth/login/`, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  }, { auth: false })
}

export async function adminMe(provider) {
  // provider is a per-request auth provider from admin store
  return await apiFetch(`${ADMIN_API_BASE}/auth/me/`, {
    method: 'GET',
  }, { auth: true, provider })
}
