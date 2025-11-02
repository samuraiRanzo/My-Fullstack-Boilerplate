// Basic auth service calling Django JWT endpoints via apiFetch with silent refresh
import { apiFetch } from './http'

const API_BASE = '/api'

export async function apiRegister(payload) {
  return await apiFetch(`${API_BASE}/auth/register/`, {
    method: 'POST',
    body: JSON.stringify(payload),
  }, { auth: false })
}

export async function apiLogin({ email, password }) {
  // Expected: { access, refresh, user }
  return await apiFetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  }, { auth: false })
}

export async function apiRefresh(refreshToken) {
  // Returns { access }
  return await apiFetch(`${API_BASE}/auth/refresh/`, {
    method: 'POST',
    body: JSON.stringify({ refresh: refreshToken }),
  }, { auth: false })
}

export async function apiUser() {
  // auth:true attaches Authorization and auto-refreshes on 401
  return await apiFetch(`${API_BASE}/auth/user/`, {
    method: 'GET',
  }, { auth: true })
}
